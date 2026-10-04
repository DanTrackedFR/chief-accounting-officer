"""Synthetic independently controlled sources; no signoff represents a real person."""
import copy
from decimal import Decimal
from cases import base
from production import canonical_knowledge,case_fingerprint,PACKAGES,load_workflow
PACKAGE='insurance-contracts-accounting'

def sources(c):
    w=load_workflow(PACKAGE);c['documents']=[]
    records=c['contracts']+c['groups']+c['cash_events']+c['claims']+c['reports']+c['gl']+[c['population_review'],c['statement_review'],c['disclosure_review']]
    for r in records:r['document_id']='doc-'+r['id']
    for r in c['reports']:
        g=next(g for g in c['groups'] if g['id']==r['group_id'])
        r['contract_population_hash']=w.digest([p for p in c['contracts'] if p['id'] in g['contract_ids']]);r['claim_population_hash']=w.digest([q for q in c['claims'] if q['group_id']==g['id']]);r['cash_population_hash']=w.digest([e for e in c['cash_events'] if e['group_id']==g['id']])
    c['statement_review']['gl_hash']=w.digest(c['gl'])
    for r in records:
        content=copy.deepcopy({k:v for k,v in r.items() if k!='document_id'})
        c['documents'].append(dict(id=r['document_id'],reviewer='Synthetic independent source reviewer',source_system='Synthetic controlled original source',version='1',entity=c['entity'],framework=c['framework'],currency=c['currency'],as_of=c['reporting_period'],content=content,content_hash=w.digest(content)))
    return c

def case(fw='IFRS',route='gmm',future_change='0',onerous=False,acquisition_expense=False,deficiency=False):
    c=base(PACKAGE,fw);model=('ASC944_SHORT_DURATION' if fw=='US_GAAP' else ('AASB17' if fw=='AASB' else 'IFRS17')+('_GMM' if route=='gmm' else '_PAA'))
    c.update(package=PACKAGE,insurance_model=model,currency='EUR',execution_date='2027-02-01',requested_action='accounting_workpaper')
    c['policy_elections']['ifrs18_19_early_adoption']=False
    if fw=='AASB':c['aasb_compilation']='AASB17_DEC2022_PRE_JULY2026'
    p=dict(id='policy1',economic_id='policy-economic1',group_id='group1',terms_memo='Executed synthetic policy compensation for insured property fire',risk_scenario_memo='Independent significant additional benefit commercial present-value scenarios',boundary_memo='Actual enforceable single coverage boundary',portfolio='property',product='property_fire',profitability='us_aggregation' if fw=='US_GAAP' else 'onerous' if onerous else 'no_significant_possibility',recognition_date='2026-01-01',coverage_start='2026-01-01',coverage_end='2027-12-31' if route=='gmm' else '2026-12-31',issue_date='2026-01-01',premium_due_date='2026-01-01',onerous_date='2026-01-01',currency='EUR',perspective='issued',cohort='2026',insured_event_benefit='5000',no_event_benefit='0',commercial_substance=True,us_contract_type='short_duration')
    p.update({k:True for k in ('uncertain_event','adverse_effect','nonfinancial_risk','significant_insurance_risk','scope_assessed')});p.update({k:False for k in ('financial_guarantee','seller_warranty','fixed_fee_service','separated_component','investment_component','participating','modification','acquired','transition')})
    g=dict(id='group1',economic_id='group-economic1',portfolio='property',product='property_fire',grouping_memo='Actual similar risks managed together profitability and fixed cohort assessed',recognition_date='2026-01-01',profitability=p['profitability'],model=model,contract_ids=['policy1'],original_contract_ids=['policy1'],cohort='2026',membership_locked=True,assumption_version='assumptions1',model_version='model1',aggregation_basis='US similar acquisition and servicing business')
    report=dict(id='report1',group_id='group1',actuary='Synthetic qualified actuary',qualification_memo='Synthetic independently reviewed qualification evidence',objectivity_memo='Synthetic independent objectivity review',reviewer='Synthetic separate actuarial reviewer',model_version='model1',assumption_version='assumptions1',assumptions_memo='Controlled assumptions register excludes autonomous projections',signed_on='2027-01-20',measurement_date=c['reporting_period'],initial_date=g['recognition_date'],entity=c['entity'],framework=fw,currency='EUR',model=model,product='property_fire',portfolio='property',contract_ids=['policy1'],discount_source='Qualified supplied curve register version1',risk_adjustment_source='Qualified supplied RA workpaper version1',coverage_method='Qualified quantity of benefits and duration units register',change_classification_memo='Nonfinancial future service assumption change distinguished from errors and finance',change_kind='assumption' if future_change!='0' else 'none',change_service='future',change_risk='nonfinancial',unsupported_features=[],boundary_reviewed=True,opening_lrc='0',opening_lic='0',opening_csm='0',opening_ra='0',opening_loss='0',loss_recovery='0',initial_ra='0',closing_ra='0',initial_csm='0',closing_csm='0',csm_release='0',csm_interest='0',initial_loss='0',future_change_locked=future_change,future_change_current=future_change,discount_curve_unchanged=True,locked_rate='0.04',interest_fraction='1',interest_day_basis='actual365_simple',initial_outflows='800',initial_fcf='-150',initial_ra_dummy='0',current_units='25',remaining_units='75',expected_service='400',ra_release='20',fcf_finance='8',closing_pv='408',loss_allocation='0',loss_allocation_method='Qualified actuarial systematic service allocation version1',closing_loss='0',paa_material_equivalence=False,paa_significant_variability=False,paa_inception_reviewed=True,premium_financing_exemption=True,max_service_to_due_days='364',claim_discount_exemption=True,max_claim_to_payment_days='181',revenue_pattern='time',pattern_reviewed=True,service_fraction='0.5',expected_premiums='1000',acquisition_amortization='0',acquisition_expense_election=acquisition_expense,acquisition_attributable=True,onerous_assessed=True,onerous_indicator=False,remaining_fcf='0',paa_loss='0',past_service_change='0',lic_finance='0',incurred='420',claim_paid='200',closing_lic='220',nonperformance_reviewed=True,us_insurance_entity=True,us_contract_scope_reviewed=True,claims_undiscounted=True,successful_acquisition=True,us_aggregation_basis=g['aggregation_basis'],investment_income_policy='exclude',investment_income='0',remaining_claims='0',maintenance_cost='0',dac_writeoff='0',closing_dac='0',deficiency_liability='0')
    premium=Decimal('1000');acq=Decimal('0');claiminc=Decimal('420');paid=Decimal('200');ra=Decimal('50');fchange=Decimal(future_change);expense=claiminc
    if route=='gmm':
        out=Decimal('1050' if onerous else '800');csm0=max(premium-out-ra,Decimal(0));loss0=max(out+ra-premium,Decimal(0));interest=csm0*Decimal('.04');available=csm0+interest-fchange;release=(available*Decimal('.25')).quantize(Decimal('.01'));csm=available-release;alloc=Decimal('40' if onerous else '0');revenue=Decimal('400')+Decimal('20')+release-alloc;lrc=out-Decimal('400')+fchange+Decimal('8')+ra-Decimal('20')+csm;finance=Decimal('8')+interest;expense+=loss0-alloc
        report.update(initial_ra=str(ra),initial_outflows=str(out),initial_fcf=str(out+ra-premium),initial_csm=str(csm0),initial_loss=str(loss0),csm_interest=str(interest),csm_release=str(release),closing_csm=str(csm),closing_ra='30',closing_pv=str(out-Decimal('400')+fchange+Decimal('8')),loss_allocation=str(alloc),closing_loss=str(loss0-alloc),closing_lrc=str(lrc),service_release=str(revenue))
    else:
        premium=Decimal('1200');acq=Decimal('120');claiminc=Decimal('300');paid=Decimal('100');revenue=Decimal('600');amort=Decimal(0) if acquisition_expense else Decimal('60');lrc=premium-(Decimal(0) if acquisition_expense else acq)+amort-revenue;finance=Decimal(0);expense=claiminc+(acq if acquisition_expense else amort)
        report.update(expected_premiums=str(premium),incurred=str(claiminc),claim_paid=str(paid),closing_lic='200',closing_lrc=str(lrc),service_release=str(revenue),acquisition_amortization=str(amort),revenue_pattern='protection' if fw=='US_GAAP' else 'time')
        if fw=='US_GAAP':
            dac=acq-amort;loss=Decimal('100') if deficiency else Decimal('0');writeoff=dac if deficiency else Decimal('0');lrc=premium-revenue+loss;expense=claiminc+amort+writeoff+loss
            report.update(closing_lrc=str(lrc),remaining_claims='650' if deficiency else '400',maintenance_cost='50' if deficiency else '0',dac_writeoff=str(writeoff),closing_dac=str(dac-writeoff),deficiency_liability=str(loss))
    if route!='gmm':
        p.update(recognition_date='2026-07-01',coverage_start='2026-07-01',coverage_end='2027-06-30',premium_due_date='2026-07-01',issue_date='2026-07-01');g['recognition_date']='2026-07-01';report['initial_date']='2026-07-01'
        report['revenue_pattern']='risk' if fw!='US_GAAP' else 'protection';report['risk_release_fraction']='0.5';report['protection_release_fraction']='0.5';report['significant_risk_pattern']=True
    report['incurred_pv']=str(claiminc-(Decimal('20') if fw!='US_GAAP' else Decimal(0)));report['incurred_ra']='20' if fw!='US_GAAP' else '0'
    c['contracts']=[p];c['groups']=[g];c['reports']=[report]
    c['cash_events']=[dict(id='premium1',economic_id='premium-economic1',policy_id='policy1',group_id='group1',kind='premium',date=p['recognition_date'],amount=str(premium)),dict(id='payment1',economic_id='payment-economic1',policy_id='policy1',group_id='group1',kind='claim_payment',date='2026-12-01',amount=str(paid))]
    if acq:c['cash_events'].append(dict(id='acquisition1',economic_id='acquisition-economic1',policy_id='policy1',group_id='group1',kind='acquisition',date=p['recognition_date'],amount=str(acq)))
    c['claims']=[dict(id='claim1',economic_id='claim-economic1',policy_id='policy1',group_id='group1',occurrence_date='2026-09-01',expected_settlement_date='2027-03-01',valuation_date=c['reporting_period'],payment_memo='Original settlement source',incurred=str(claiminc),paid=str(paid))]
    amounts={'Cash':premium-acq-paid,'Insurance remaining coverage group1':-lrc,'Insurance incurred claims group1':-(claiminc-paid),'Insurance service revenue group1':-revenue,'Insurance service expense group1':expense}
    if finance:amounts['Insurance finance group1']=finance
    if fw=='US_GAAP' and Decimal(report['closing_dac'])>0:amounts['US DAC group1']=Decimal(report['closing_dac'])
    elif fw=='US_GAAP':amounts['US DAC group1']=Decimal('0')
    c['gl']=[dict(id=k,opening='0',closing=str(v),statement=str(v)) for k,v in amounts.items()]
    c['population_review']=dict(id='population',reviewer='Synthetic independent completeness reviewer',source_system='Independent original policy claims cash systems',completeness_memo='Independent source totals and unique economic identity review',complete=True)
    c['statement_review']=dict(id='statements',gross_presentation=True,group_ids=['group1'])
    c['disclosure_review']=dict(id='disclosures',reviewer='Synthetic independent disclosure reviewer',framework_checklist=fw+' actual operative insurance requirement source',methods_inputs_memo='Qualified methods inputs',risk_memo='Controlled insurance and finance risk register',complete=True,framework=fw,group_ids=['group1'],report_ids=['report1'],requirement_ids=['amounts','rollforwards','judgments','insurance_risk','financial_risk'])
    return population(c)

def population(c):
    for key in ('contracts','groups','reports','cash_events','claims'):c['population_review'][key+'_ids']=[r['id'] for r in c[key]]
    c['statement_review']['group_ids']=[g['id'] for g in c['groups']];c['disclosure_review']['group_ids']=[g['id'] for g in c['groups']];c['disclosure_review']['report_ids']=[r['id'] for r in c['reports']]
    return sources(c)

def ready(c=None):
    c=copy.deepcopy(c or case());claims,docs=canonical_knowledge(PACKAGES[PACKAGE][1],c['framework'],package=PACKAGE)
    c['knowledge_review']=dict(reviewer='Synthetic independent knowledge reviewer',claim_ids=[r['claim_id'] for r in claims],documents=docs,applied_claim_ids=[r['claim_id'] for r in claims],selection_memo='Synthetic reviewed Insurance route and explicit excluded specialist boundaries',public_caveats=['Current qualified inputs and the operative insurance framework are required; complex models require separate governed methods.'])
    c['reviewer_signoff']=dict(reviewer='Synthetic independent implementation reviewer',approved=True,case_fingerprint=case_fingerprint(c));return c

def reinsurance_case(fw='IFRS'):
    c=case(fw,'paa');p=copy.deepcopy(c['contracts'][0]);p.update(id='treaty1',economic_id='treaty-economic1',group_id='held1',portfolio='held_property',product='property_reinsurance',profitability='net_cost',perspective='reinsurance_held',reinsurance_kind='proportionate',counterparty='Qualified reinsurer1',underlying_policy_ids=['policy1'],recovery_fraction='0.2')
    g=copy.deepcopy(c['groups'][0]);g.update(id='held1',economic_id='held-economic1',portfolio=p['portfolio'],product=p['product'],profitability='net_cost',contract_ids=['treaty1'],original_contract_ids=['treaty1'])
    r=copy.deepcopy(c['reports'][0]);r.update(id='heldreport1',group_id='held1',portfolio=p['portfolio'],product=p['product'],contract_ids=['treaty1'],expected_premiums='240',service_release='120',incurred='60',claim_paid='20',closing_lrc='120',closing_lic='40',acquisition_amortization='0',underlying_group_ids=['group1'],underlying_report_ids=['report1'],counterparty='Qualified reinsurer1',incurred_pv='56',incurred_ra='4')
    c['contracts'].append(p);c['groups'].append(g);c['reports'].append(r)
    c['cash_events'] += [dict(id='ceded1',economic_id='ceded-economic1',policy_id='treaty1',group_id='held1',kind='premium',date='2026-07-01',amount='240'),dict(id='recover1',economic_id='recover-economic1',policy_id='treaty1',group_id='held1',kind='recovery',date='2026-12-01',amount='20')]
    c['claims'].append(dict(id='recovery1',economic_id='recovery-economic1',policy_id='treaty1',group_id='held1',underlying_claim_id='claim1',occurrence_date='2026-09-01',expected_settlement_date='2027-03-01',valuation_date=c['reporting_period'],payment_memo='Original recovery settlement',incurred='60',paid='20'))
    for row in c['gl']:
        if row['id']=='Cash':row.update(closing='760',statement='760')
    for account,value in [('Reinsurance remaining coverage held1','120'),('Reinsurance incurred recovery held1','40'),('Reinsurance service expense held1','120'),('Reinsurance service recovery held1','-60')]:c['gl'].append(dict(id=account,opening='0',closing=value,statement=value))
    return population(c)
