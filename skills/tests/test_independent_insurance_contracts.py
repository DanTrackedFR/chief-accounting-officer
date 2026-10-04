"""Fresh insurance implementation counterexamples; semantic sources are requalified."""
import copy,json,unittest
from decimal import Decimal as D
from pathlib import Path
from unittest.mock import patch
from insurance_cases import case,population,ready,reinsurance_case,PACKAGE
from production import assess_case,load_workflow,canonical_knowledge,PACKAGES,to_public
from core_accounting import ReviewRequired
from interfaces.public_output import ROUTES

MONEY={'insured_event_benefit','no_event_benefit','amount','incurred','paid','opening','closing','statement','opening_lrc','opening_lic','opening_csm','opening_ra','opening_loss','loss_recovery','initial_ra','closing_ra','initial_csm','closing_csm','csm_release','csm_interest','initial_loss','future_change_locked','future_change_current','initial_outflows','initial_fcf','initial_ra_dummy','expected_service','ra_release','fcf_finance','closing_pv','loss_allocation','closing_loss','expected_premiums','acquisition_amortization','remaining_fcf','paa_loss','past_service_change','lic_finance','claim_paid','incurred_pv','incurred_ra','closing_lic','investment_income','remaining_claims','maintenance_cost','dac_writeoff','closing_dac','deficiency_liability','closing_lrc','service_release'}
def independent(fw='IFRS',route='gmm',**kw):
 c=case(fw,route,**kw);c['case_id']='Independent insurance '+fw+' '+route
 # Independently altered magnitude; preserving rates and service proportions.
 for key in ('contracts','reports','cash_events','claims','gl'):
  for r in c[key]:
   for k in MONEY & set(r):r[k]=str(D(r[k])*D('1.6'))
 return population(c)

class IndependentInsurance(unittest.TestCase):
 def result(self,c):
  c=ready(population(c));claims,_=canonical_knowledge(PACKAGES[PACKAGE][1],c['framework'],package=PACKAGE)
  return load_workflow(PACKAGE).assess(c,claims)
 def blocked(self,c):
  with self.assertRaises(ReviewRequired):self.result(c)
 def test_positive_scaled_gmm_future_and_onerous(self):
  for fw in ('IFRS','AASB'):
   for kw in ({},{'future_change':'24'},{'onerous':True}):
    r=self.result(independent(fw,**kw));self.assertEqual(r['calculations']['groups'][0]['incurred_claims'],D('352'))
 def test_positive_native_us_dac_and_deficiency(self):
  for deficiency in (False,True):
   r=self.result(independent('US_GAAP','paa',deficiency=deficiency));g=r['calculations']['groups'][0]
   self.assertEqual(g['revenue'],D('960'));self.assertNotIn('csm',g);self.assertNotIn('risk_adjustment',g);self.assertNotIn('loss_component',g)
 def test_significant_risk_and_scope_mutations(self):
  for k,v in dict(significant_insurance_risk=False,uncertain_event=False,adverse_effect=False,nonfinancial_risk=False,financial_guarantee=True,seller_warranty=True,fixed_fee_service=True,investment_component=True,separated_component=True,participating=True,transition=True,modification=True,acquired=True,perspective='holder',commercial_substance=False).items():
   c=independent();c['contracts'][0][k]=v
   with self.subTest(k=k):self.blocked(c)
 def test_duplicate_aliases_policy_claim_and_cash(self):
  for key in ('contracts','claims','cash_events'):
   c=independent();r=copy.deepcopy(c[key][0]);r['id']+='alias';c[key].append(r)
   with self.subTest(key=key):self.blocked(c)
 def test_missing_and_reassigned_policy(self):
  for k,v in {'contract_ids':[],'original_contract_ids':['old-policy'],'membership_locked':False,'profitability':'onerous','portfolio':'unrelated','cohort':'2027'}.items():
   c=independent();c['groups'][0][k]=v
   with self.subTest(k=k):self.blocked(c)
 def test_wrong_policy_group_id(self):
  c=independent();c['contracts'][0]['group_id']='nonexistent';self.blocked(c)
 def test_wrong_date_bound_cohort(self):
  c=independent();c['contracts'][0]['cohort']=c['groups'][0]['cohort']='2027';self.blocked(c)
 def test_claim_occurs_before_coverage(self):
  c=independent();c['claims'][0]['occurrence_date']='2025-12-31';self.blocked(c)
 def test_actuarial_semantic_dimensions(self):
  for k,v in dict(measurement_date='2026-11-30',entity='Other',framework='US_GAAP',currency='USD',product='annuity',portfolio='life',assumption_version='changed',model_version='changed',actuary='Synthetic preparer',reviewer='Synthetic preparer',signed_on='2026-12-30',contract_ids=[],discount_source='',risk_adjustment_source='',coverage_method='',unsupported_features=['VFA'],boundary_reviewed=False,change_kind='error',change_service='current',change_risk='financial').items():
   c=independent();c['reports'][0][k]=v
   if k in ('actuary','reviewer'):c['reports'][0][k]=c['preparer']
   with self.subTest(k=k):self.blocked(c)
 def test_gmm_plugs_and_rollforward_errors(self):
  for k,v in dict(initial_csm='1',closing_csm='1',csm_release='1',initial_loss='1',csm_interest='1',closing_pv='1',closing_ra='1',closing_lrc='1',closing_lic='1',closing_loss='1',future_change_current='2',current_units='0',remaining_units='0',opening_csm='1',discount_curve_unchanged=False).items():
   c=independent();c['reports'][0][k]=v
   if k in ('current_units','remaining_units'):c['reports'][0].update(current_units='0',remaining_units='0')
   with self.subTest(k=k):self.blocked(c)
 def test_paa_ineligible_and_exemptions(self):
  for k,v in dict(paa_inception_reviewed=False,premium_financing_exemption=False,claim_discount_exemption=False,onerous_assessed=False,pattern_reviewed=False,acquisition_attributable=False,service_fraction='1.1').items():
   c=independent(route='paa');c['reports'][0][k]=v
   with self.subTest(k=k):self.blocked(c)
  c=independent(route='paa');c['contracts'][0]['coverage_end']='2027-12-31';self.blocked(c)
 def test_time_paa_expired_coverage_cannot_retain_half_lrc(self):
  c=independent(route='paa');c['contracts'][0]['coverage_end']='2026-12-31';self.blocked(c)
 def test_reinsurance_wrong_underlying_and_counterparty(self):
  for k,v in dict(underlying_policy_ids=['absent'],counterparty='',reinsurance_kind='retroactive',recognition_date='2026-02-01',perspective='issued').items():
   c=reinsurance_case();c['contracts'][1][k]=v
   with self.subTest(k=k):self.blocked(c)
  for k,v in dict(loss_recovery='1',underlying_group_ids=['absent'],nonperformance_reviewed=False).items():
   c=reinsurance_case();c['reports'][1][k]=v
   with self.subTest(k=k):self.blocked(c)
 def test_us_no_ifrs_mechanics_or_longduration(self):
  for k,v in dict(initial_ra='1',initial_csm='1',closing_csm='1',revenue_pattern='time',successful_acquisition=False,dac_writeoff='1',closing_dac='1',investment_income='1',claims_undiscounted=False,lic_finance='1').items():
   c=independent('US_GAAP','paa');c['reports'][0][k]=v
   with self.subTest(k=k):self.blocked(c)
  c=independent('US_GAAP','paa');c['contracts'][0]['us_contract_type']='long_duration';self.blocked(c)
 def test_gl_statement_and_gross_presentation(self):
  for k in ('closing','statement','opening'):
   c=independent();c['gl'][0][k]=str(D(c['gl'][0][k])+1)
   with self.subTest(k=k):self.blocked(c)
  c=independent();c['statement_review']['gross_presentation']=False;self.blocked(c)
  c=independent();c['disclosure_review']['requirement_ids']=[];self.blocked(c)
 def test_unsupported_framework_scope(self):
  c=case('UK_GAAP');self.blocked(c)
  c=independent('AASB');c['reporting_tier']=2;self.blocked(c)
  for v in ('IFRS17_VFA','IFRS17_TRANSITION','RiskMitigationProposal'):
   c=independent();c['insurance_model']=v;self.blocked(c)
 def test_stale_source_without_refresh(self):
  c=ready(independent());c['reports'][0]['initial_ra']='123'
  claims,_=canonical_knowledge(PACKAGES[PACKAGE][1],c['framework'],package=PACKAGE)
  with self.assertRaises(ReviewRequired):load_workflow(PACKAGE).assess(c,claims)
 def test_positive_paa_and_reinsurance_scaled(self):
  for fw in ('IFRS','AASB'):
   r=self.result(independent(fw,'paa'));self.assertEqual(r['calculations']['groups'][0]['incurred_claims'],D('320'))
   r=self.result(reinsurance_case(fw));self.assertEqual(len(r['calculations']['groups']),2);self.assertEqual(r['calculations']['groups'][1]['remaining_coverage'],D('120'))
 def test_gmm_expired_with_unreleased_service(self):
  c=independent();c['contracts'][0]['coverage_end']='2026-12-31';self.blocked(c)
 def test_us_unsupported_future_change_not_ignored(self):
  c=independent('US_GAAP','paa');c['reports'][0].update(future_change_locked='10',future_change_current='10',change_kind='assumption');self.blocked(c)
 def test_none_change_cannot_contain_assumption_movement(self):
  c=independent(future_change='24');c['reports'][0]['change_kind']='none';self.blocked(c)
 def test_positive_multiple_groups_no_alias(self):
  c=independent();other=independent(future_change='24')
  def ren(v):
   if isinstance(v,str):return v.replace('group1','group2').replace('policy1','policy2').replace('report1','report2').replace('economic1','economic2')
   if isinstance(v,list):return [ren(x) for x in v]
   if isinstance(v,dict):return {k:ren(x) for k,x in v.items()}
   return v
  for key in ('contracts','groups','reports','cash_events','claims'):
   for r in other[key]:
    row=ren(copy.deepcopy(r))
    if key in ('cash_events','claims'):row['id']+='second';row['economic_id']+='second'
    c[key].append(row)
  for r in other['gl']:
   row=ren(copy.deepcopy(r))
   if row['id']=='Cash':
    target=next(x for x in c['gl'] if x['id']=='Cash');target['closing']=target['statement']=str(D(target['closing'])+D(row['closing']))
   else:c['gl'].append(row)
  r=self.result(c);self.assertEqual(len(r['calculations']['groups']),2)
  c['groups'][1]['economic_id']=c['groups'][0]['economic_id'];self.blocked(c)
 def test_stale_certification_and_case_review(self):
  c=ready(independent());c['reviewer_signoff']['case_fingerprint']='0'*64;self.assertNotEqual(assess_case(PACKAGE,c)['status'],'complete')
  c=ready(independent());c['reviewer_signoff']['reviewer']=c['preparer'];self.assertNotEqual(assess_case(PACKAGE,c)['status'],'complete')
 def test_stale_knowledge_and_implementation(self):
  for typ in ('knowledge','implementation'):
   c=ready(independent());original=Path.read_bytes;target=c['knowledge_review']['documents'][0]['path'] if typ=='knowledge' else PACKAGE+'/workflow.py'
   def modified(path):
    data=original(path);return data+b'\n# stale independent bytes' if str(path).endswith(target) else data
   with patch.object(Path,'read_bytes',modified):self.assertNotEqual(assess_case(PACKAGE,c)['status'],'complete')
 def test_all_public_routes_source_privacy(self):
  c=ready(independent());r=assess_case(PACKAGE,c)
  for route in ROUTES:
   public=json.dumps(to_public(r,route),default=str)
   for forbidden in ('source_note','Source:','approval_track','evidence_status','audit_required','reviewer_signoff'):
    with self.subTest(route=route,forbidden=forbidden):self.assertNotIn(forbidden,public)
 def test_gmm_interest_period_bound_to_coverage(self):
  c=independent();p=c['contracts'][0];p.update(issue_date='2026-07-01',recognition_date='2026-07-01',coverage_start='2026-07-01',premium_due_date='2026-07-01');c['groups'][0]['recognition_date']='2026-07-01';c['reports'][0]['initial_date']='2026-07-01';c['claims'][0]['occurrence_date']='2026-08-01';c['cash_events'][0]['date']='2026-07-01';self.blocked(c)
 def test_paa_claim_exemption_bound_to_actual_settlement(self):
  c=independent(route='paa');c['claims'][0].update(expected_settlement_date='2028-12-31');self.blocked(c)
 def test_report_financial_oci_request_not_ignored(self):
  c=independent();c['policy_elections']['insurance_finance_oci']=True;self.blocked(c)
 def test_positive_actual_time_paa_and_fraction_precision(self):
  c=case(route='paa');r=c['reports'][0];fraction=D(184)/D(365);revenue=(D(1200)*fraction).quantize(D('.01'));lrc=D(1200)-D(120)+D(60)-revenue
  r.update(revenue_pattern='time',service_fraction=str(fraction),service_release=str(revenue),closing_lrc=str(lrc))
  for row in c['gl']:
   if row['id']=='Insurance remaining coverage group1':row['closing']=row['statement']=str(-lrc)
   if row['id']=='Insurance service revenue group1':row['closing']=row['statement']=str(-revenue)
  self.assertEqual(self.result(c)['calculations']['groups'][0]['revenue'],revenue)
  # .004 error rounds to the same two-decimal fraction but changes premium revenue.
  wrong=fraction-D('.004');revenue2=(D(1200)*wrong).quantize(D('.01'));lrc2=D(1140)-revenue2
  r.update(service_fraction=str(wrong),service_release=str(revenue2),closing_lrc=str(lrc2))
  for row in c['gl']:
   if row['id']=='Insurance remaining coverage group1':row['closing']=row['statement']=str(-lrc2)
   if row['id']=='Insurance service revenue group1':row['closing']=row['statement']=str(-revenue2)
  self.blocked(c)
 def handoffs(self):
  import importlib.util
  spec=importlib.util.spec_from_file_location('independent_insurance_handoffs',Path(__file__).resolve().parents[1]/PACKAGE/'handoffs.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
 def test_native_report_and_disclosure_all_supported_frameworks(self):
  from insurance_integration_cases import reporting_fixture,disclosure_fixture
  h=self.handoffs()
  for fw,route,held in [('IFRS','gmm',False),('AASB','paa',False),('US_GAAP','paa',False),('IFRS','paa',True),('AASB','paa',True)]:
   i,r,m=reporting_fixture(fw,held,route);self.assertEqual(h.validate_reporting_handoff(i,r,m)['status'],'validated')
   i,d=disclosure_fixture(fw,held,route);self.assertEqual(h.validate_disclosure_handoff(i,d)['status'],'validated')
 def test_reporting_duplicate_source_and_alias_other_line(self):
  from insurance_integration_cases import reporting_fixture
  from additional_cases import certify
  from production import execute
  h=self.handoffs();i,r,m=reporting_fixture();m.append(copy.deepcopy(m[0]));m[-1]['id']+='alias'
  with self.assertRaises(ReviewRequired):h.validate_reporting_handoff(i,r,m)
  i,r,m=reporting_fixture();row=copy.deepcopy(r['case']['current_tb'][0]);row.update(id='ordinary-revenue-alias',balance='0',line='ordinary-revenue',category='revenue',source_version='different-revenue-owner',cash_account=False);r['case']['current_tb'].append(row)
  r['case']=certify('financial-statements',r['case']);r['result']=execute('financial-statements',r['case'])
  self.assertEqual(r['result']['status'],'complete')
  with self.assertRaises(ReviewRequired):h.validate_reporting_handoff(i,r,m)
 def test_reporting_stale_and_incomplete_exact_mapping(self):
  from insurance_integration_cases import reporting_fixture
  h=self.handoffs()
  for kind in ('missing','stale','wrong'):
   i,r,m=reporting_fixture()
   if kind=='missing':m.pop()
   if kind=='stale':r['result']['conclusion']+=' tampered'
   if kind=='wrong':m[0]['source_id']='unrelated'
   with self.subTest(kind=kind):
    with self.assertRaises(ReviewRequired):h.validate_reporting_handoff(i,r,m)
 def test_disclosure_stale_or_missing_population(self):
  from insurance_integration_cases import disclosure_fixture
  h=self.handoffs()
  for kind in ('stale','missing','wrong_owner'):
   i,d=disclosure_fixture()
   if kind=='stale':d['result']['conclusion']+=' tampered'
   if kind=='missing':d['case']['requirements'].pop()
   if kind=='wrong_owner':d['case']['imports'][0]['package']='revenue-recognition'
   with self.subTest(kind=kind):
    with self.assertRaises(ReviewRequired):h.validate_disclosure_handoff(i,d)
 def test_positive_halfyear_gmm_exact_interest(self):
  c=case();p=c['contracts'][0];p.update(issue_date='2026-07-01',recognition_date='2026-07-01',coverage_start='2026-07-01',premium_due_date='2026-07-01');c['groups'][0]['recognition_date']='2026-07-01';c['claims'][0]['occurrence_date']='2026-08-01';c['cash_events'][0]['date']='2026-07-01';r=c['reports'][0]
  fraction=D(184)/D(365);interest=(D(150)*D('.04')*fraction).quantize(D('.01'));available=D(150)+interest;release=(available/D(4)).quantize(D('.01'));csm=available-release;revenue=D(420)+release;lrc=D(438)+csm;finance=D(8)+interest
  r.update(initial_date='2026-07-01',interest_fraction=str(fraction),csm_interest=str(interest),csm_release=str(release),closing_csm=str(csm),service_release=str(revenue),closing_lrc=str(lrc))
  for row in c['gl']:
   values={'Insurance remaining coverage group1':-lrc,'Insurance service revenue group1':-revenue,'Insurance finance group1':finance}
   if row['id'] in values:row['closing']=row['statement']=str(values[row['id']])
  out=self.result(c);self.assertEqual(out['calculations']['groups'][0]['csm'],csm)
 def test_positive_two_policies_one_group(self):
  c=case(route='paa');p=copy.deepcopy(c['contracts'][0]);p.update(id='policy2',economic_id='policy-economic2');c['contracts'].append(p);c['groups'][0]['contract_ids']=c['groups'][0]['original_contract_ids']=['policy1','policy2'];c['reports'][0]['contract_ids']=['policy1','policy2']
  new=[]
  for r in c['cash_events']:
   r['amount']=str(D(r['amount'])/2);second=copy.deepcopy(r);second.update(id=r['id']+'-second',economic_id=r['economic_id']+'-second',policy_id='policy2');new.append(second)
  c['cash_events']+=new;q=c['claims'][0];q['incurred']=str(D(q['incurred'])/2);q['paid']=str(D(q['paid'])/2);q2=copy.deepcopy(q);q2.update(id='claim2',economic_id='claim-economic2',policy_id='policy2');c['claims'].append(q2)
  out=self.result(c);self.assertEqual(out['calculations']['groups'][0]['contract_ids'],['policy1','policy2'])
 def test_current_other_owners_execute_and_insurance_refuses_takeover(self):
  from production import execute
  from cases import ecl
  from financing_cases import ready as financing_ready
  from additional_cases import fx,certify
  from hedge_cases import ready as hedge_ready,case as hedge_case
  examples=[('financial-instruments-ecl',ecl()),('fair-value-measurement',financing_ready('fair-value-measurement')),('derivatives-hedge-accounting',hedge_ready(hedge_case())),('foreign-currency',certify('foreign-currency',fx()))]
  for package,c in examples:
   with self.subTest(package=package):self.assertEqual(execute(package,c)['status'],'complete')
  for key,value in [('investment_component',True),('separated_component',True),('participating',True),('currency','USD')]:
   c=independent();c['contracts'][0][key]=value
   with self.subTest(boundary=key):self.blocked(c)
 def test_actual_financing_horizon_and_duplicate_underlying_recovery(self):
  c=independent(route='paa');c['reports'][0]['max_service_to_due_days']='1';self.blocked(c)
  c=reinsurance_case();q=copy.deepcopy(c['claims'][1]);q.update(id='duplicate-underlying-recovery',economic_id='new-recovery-economic',incurred='0',paid='0');c['claims'].append(q);self.blocked(c)
 def test_independent_named_schedule_identities_and_signs(self):
  inputs=[independent(future_change='24'),independent(future_change='-24'),independent(onerous=True),independent(route='paa'),independent(route='paa',acquisition_expense=True),independent('US_GAAP','paa',deficiency=True),reinsurance_case('IFRS'),reinsurance_case('AASB')]
  for c in inputs:
   result=self.result(c)
   for g in result['calculations']['groups']:
    b=g['rollforwards'];self.assertGreaterEqual(len(b),4 if g['model']=='ASC944_SHORT_DURATION' else 5)
    for name,bridge in b.items():
     self.assertEqual(sum((D(v) for k,v in bridge.items() if k!='closing'),D(0)),D(bridge['closing']))
     if name not in ('dac','premium_deficiency'):self.assertEqual(D(bridge['closing']),D(g[name]))
     if name=='premium_deficiency':self.assertEqual(D(bridge['closing']),D(g['premium_deficiency_liability']))
    self.assertLessEqual(b['incurred_claims']['claim_payments'],0)
    self.assertEqual(b['incurred_claims']['incurred_pv']+b['incurred_claims']['incurred_ra'],D(next(r for r in c['reports'] if r['group_id']==g['id'])['incurred']))
    if g['model'].endswith('_GMM'):
     r=next(r for r in c['reports'] if r['group_id']==g['id']);self.assertEqual(b['csm']['future_service_change'],-D(r['future_change_locked']));self.assertEqual(b['csm']['service_release'],-D(r['csm_release']))
    if g['model']=='ASC944_SHORT_DURATION':
     self.assertIn('dac',b);self.assertEqual(b['dac']['deficiency_writeoff'],D('-96'));self.assertEqual(b['remaining_coverage']['deficiency_liability'],D('160'))
 def test_final_compilation_early_adoption_and_expensed_acquisition_guard(self):
  c=independent('AASB');c['aasb_compilation']='AASB17_DEC2022_JULY2026';self.blocked(c)
  c=independent();c['policy_elections']['ifrs18_19_early_adoption']='false';self.blocked(c)
  c=independent(route='paa',acquisition_expense=True);c['reports'][0]['acquisition_attributable']=False;self.blocked(c)
 def test_native_us_entity_scope_dac_amortization_and_recognition(self):
  for k,v in [('us_insurance_entity',False),('us_contract_scope_reviewed',False),('acquisition_amortization','59')]:
   c=independent('US_GAAP','paa');c['reports'][0][k]=v
   with self.subTest(key=k):self.blocked(c)
  c=independent('US_GAAP','paa');c['contracts'][0]['premium_due_date']='2026-06-01';self.blocked(c)
 def test_unbound_specialist_imports_and_elections_fail_closed(self):
  for key in ('imports','owner_links','specialist_items'):
   c=independent();c[key]=[{'id':'unbound-investment-owner','amount':'100'}]
   with self.subTest(key=key):self.blocked(c)
  c=independent();c['policy_elections']['invented-insurance-choice']=True;self.blocked(c)
