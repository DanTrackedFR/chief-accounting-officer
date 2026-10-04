"""Authored insurance arithmetic, source, classification and governance regression."""
import copy,json,unittest
from unittest.mock import patch
from pathlib import Path
from decimal import Decimal
from insurance_cases import *
from production import assess_case,to_public,serializable
from interfaces.public_output import ROUTES

class Insurance(unittest.TestCase):
    def run_case(self,c):return assess_case(PACKAGE,ready(population(c)))
    def block(self,c):self.assertEqual('blocked',self.run_case(c)['status'])
    def test_supported_routes(self):
        from generate_insurance_examples import scenarios
        for fw,name,c in scenarios():
            r=self.run_case(c);self.assertEqual('complete',r['status'],name+': '+r['conclusion'])
    def test_named_rollforward_identities(self):
        from generate_insurance_examples import scenarios
        for fw,name,c in scenarios():
            r=self.run_case(c)
            for g in r['calculations']['groups']:
                for label,bridge in g['rollforwards'].items():self.assertEqual(bridge['closing'],sum((v for k,v in bridge.items() if k!='closing'),Decimal(0)),name+' '+label)
    def test_gmm_exact_components(self):
        r=self.run_case(case());g=r['calculations']['groups'][0]
        for k,v in [('csm','117'),('risk_adjustment','30'),('remaining_coverage','555'),('incurred_claims','220'),('revenue','459'),('service_expense','420'),('finance','14')]:self.assertEqual(Decimal(v),g[k])
    def test_future_changes(self):
        for change,csm in [('30','94.5'),('-20','132')]:
            r=self.run_case(case(future_change=change));self.assertEqual(Decimal(csm),r['calculations']['groups'][0]['csm'])
    def test_onerous_allocation(self):
        r=self.run_case(case(onerous=True));g=r['calculations']['groups'][0];self.assertEqual(Decimal('60'),g['loss_component']);self.assertEqual(Decimal('480'),g['service_expense']);self.assertEqual(Decimal('380'),g['revenue'])
    def test_paa_acquisition(self):
        for expense,value in [(False,'540'),(True,'600')]:self.assertEqual(Decimal(value),self.run_case(case(route='paa',acquisition_expense=expense))['calculations']['groups'][0]['remaining_coverage'])
    def test_us_deficiency(self):
        r=self.run_case(case('US_GAAP','us',deficiency=True));g=r['calculations']['groups'][0];self.assertEqual(Decimal('700'),g['remaining_coverage']);self.assertEqual(Decimal('520'),g['service_expense']);self.assertEqual(Decimal('0'),next(r for r in r['calculations']['statement_support'] if r['account']=='US DAC group1')['signed_balance'])
    def test_reinsurance_gross(self):
        r=self.run_case(reinsurance_case());gs=r['calculations']['groups'];self.assertEqual(Decimal('540'),gs[0]['remaining_coverage']);self.assertEqual(Decimal('120'),gs[1]['remaining_coverage']);self.assertEqual(Decimal('40'),gs[1]['incurred_claims'])
        support=r['calculations']['statement_support'];self.assertTrue(any(a['category']=='asset' and a['account']=='Reinsurance incurred recovery held1' for a in support));self.assertTrue(any(a['category']=='liability' and a['account']=='Insurance incurred claims group1' for a in support))
    def test_insurance_revenue_not_ordinary_revenue(self):
        r=self.run_case(case());self.assertTrue(all('Ordinary revenue' not in a['account'] for j in r['journal_entry_implications'] for a in j))
    def test_insurance_liability_not_generic_provision(self):
        r=self.run_case(case());self.assertTrue(all('Provision' not in a['account'] for j in r['journal_entry_implications'] for a in j))
    def test_classifier_actual_features(self):
        for key,value in [('significant_insurance_risk',False),('nonfinancial_risk',False),('uncertain_event',False),('adverse_effect',False),('financial_guarantee',True),('seller_warranty',True),('fixed_fee_service',True),('separated_component',True),('investment_component',True),('scope_assessed',False),('participating',True),('commercial_substance',False)]:
            c=case();c['contracts'][0][key]=value;self.block(c)
    def test_product_label_cannot_create_insurance(self):
        c=case();c['contracts'][0].update(product='insurance',significant_insurance_risk=False);self.block(c)
    def test_additional_benefit(self):
        c=case();c['contracts'][0]['insured_event_benefit']='0';self.block(c)
    def test_duplicate_policy_alias(self):
        c=case();p=copy.deepcopy(c['contracts'][0]);p['id']='alias';c['contracts'].append(p);self.block(c)
    def test_duplicate_claim_alias(self):
        c=case();q=copy.deepcopy(c['claims'][0]);q['id']='alias';c['claims'].append(q);self.block(c)
    def test_duplicate_cash_alias(self):
        c=case();e=copy.deepcopy(c['cash_events'][0]);e['id']='alias';c['cash_events'].append(e);self.block(c)
    def test_duplicate_group_allocation(self):
        c=case();g=copy.deepcopy(c['groups'][0]);g.update(id='group2',economic_id='group2');c['groups'].append(g);r=copy.deepcopy(c['reports'][0]);r.update(id='report2',group_id='group2');c['reports'].append(r);self.block(c)
    def test_missing_policy(self):
        c=case();p=copy.deepcopy(c['contracts'][0]);p.update(id='policy2',economic_id='policy2');c['contracts'].append(p);self.block(c)
    def test_wrong_group_profitability(self):
        c=case();c['groups'][0]['profitability']='onerous';self.block(c)
    def test_group_reassignment(self):
        c=case();c['groups'][0]['original_contract_ids']=['different'];self.block(c)
    def test_population_incomplete(self):
        c=case();c['population_review']['complete']=False;self.block(c)
    def test_report_wrong_scope(self):
        for key,val in [('entity','other'),('currency','USD'),('product','life'),('portfolio','other'),('framework','US_GAAP'),('measurement_date','2026-11-30'),('signed_on','2025-01-01'),('model_version','stale'),('assumption_version','stale')]:
            c=case();c['reports'][0][key]=val;self.block(c)
    def test_actuarial_signoff_not_authenticated(self):
        for key in ('actuary','reviewer'):
            c=case();c['reports'][0][key]=c['preparer'];self.block(c)
    def test_duplicate_actuarial_preparer_reviewer(self):
        c=case();c['reports'][0]['reviewer']=c['reports'][0]['actuary'];self.block(c)
    def test_qualified_inputs_required(self):
        for key in ('discount_source','risk_adjustment_source','coverage_method','qualification_memo','objectivity_memo'):
            c=case();c['reports'][0][key]='';self.block(c)
    def test_invented_ra_total(self):
        c=case();c['reports'][0]['incurred_ra']='99';self.block(c)
    def test_wrong_claim_total(self):
        c=case();c['reports'][0]['incurred']='999';self.block(c)
    def test_wrong_claim_payment(self):
        c=case();c['claims'][0]['paid']='100';self.block(c)
    def test_future_claim(self):
        c=case();c['claims'][0]['occurrence_date']='2027-01-01';self.block(c)
    def test_invented_csm_plug(self):
        c=case();c['reports'][0]['initial_csm']='999';self.block(c)
    def test_wrong_interest(self):
        c=case();c['reports'][0]['csm_interest']='10';self.block(c)
    def test_unbound_coverage_release(self):
        c=case();c['reports'][0]['csm_release']='10';self.block(c)
    def test_csm_exhaustion_blocked(self):self.block(case(future_change='200'))
    def test_wrong_closing_bridge(self):
        for key in ('closing_lrc','closing_lic','closing_csm','closing_ra','closing_pv','closing_loss'):
            c=case();c['reports'][0][key]='999';self.block(c)
    def test_wrong_loss_allocation(self):
        c=case(onerous=True);c['reports'][0]['loss_allocation']='101';self.block(c)
    def test_change_governance(self):
        for key,val in [('change_kind','error'),('change_kind','model'),('change_service','current'),('change_risk','financial')]:
            c=case(future_change='10');c['reports'][0][key]=val;self.block(c)
    def test_paa_ineligible(self):
        c=case(route='paa');c['contracts'][0]['coverage_end']='2028-01-01';self.block(c)
    def test_paa_eligibility_equivalence(self):
        c=case(route='paa');c['contracts'][0]['coverage_end']='2028-01-01';c['reports'][0].update(paa_material_equivalence=True,paa_significant_variability=True);self.block(c)
    def test_paa_financing_exemptions(self):
        for key in ('premium_financing_exemption','claim_discount_exemption','paa_inception_reviewed','onerous_assessed','pattern_reviewed'):
            c=case(route='paa');c['reports'][0][key]=False;self.block(c)
    def test_paa_acquisition_nonattributable(self):
        c=case(route='paa');c['reports'][0]['acquisition_attributable']=False;self.block(c)
    def test_paa_duplicate_amortization(self):
        c=case(route='paa',acquisition_expense=True);c['reports'][0]['acquisition_amortization']='60';self.block(c)
    def test_us_models(self):
        for typ in ('long_duration','universal_life','annuity','market_risk_benefit'):
            c=case('US_GAAP','us');c['contracts'][0]['us_contract_type']=typ;self.block(c)
    def test_us_no_ifrs_mechanics(self):
        for key in ('initial_ra','closing_ra','initial_csm','closing_csm','csm_release','csm_interest'):
            c=case('US_GAAP','us');c['reports'][0][key]='10';self.block(c)
    def test_us_native_output(self):
        r=self.run_case(case('US_GAAP','us',deficiency=True));g=r['calculations']['groups'][0];self.assertEqual(Decimal('100'),g['premium_deficiency_liability'])
        for key in ('csm','risk_adjustment','loss_component'):self.assertNotIn(key,g);self.assertNotIn(key,g['rollforwards'])
    def test_us_scope(self):
        c=case('US_GAAP','us');c['reports'][0]['us_insurance_entity']=False;self.block(c)
    def test_us_dac_pattern(self):
        c=case('US_GAAP','us');c['reports'][0]['acquisition_amortization']='70';self.block(c)
    def test_us_dac_qualification(self):
        for key in ('successful_acquisition','acquisition_attributable','claims_undiscounted'):
            c=case('US_GAAP','us');c['reports'][0][key]=False;self.block(c)
    def test_us_deficiency_order(self):
        c=case('US_GAAP','us',deficiency=True);c['reports'][0]['dac_writeoff']='0';self.block(c)
    def test_reinsurance_counterparty(self):
        c=reinsurance_case();c['reports'][1]['counterparty']='wrong';self.block(c)
    def test_reinsurance_underlying(self):
        c=reinsurance_case();c['contracts'][1]['underlying_policy_ids']=['missing'];self.block(c)
    def test_reinsurance_claim(self):
        c=reinsurance_case();c['claims'][1]['underlying_claim_id']='missing';self.block(c)
    def test_reinsurance_recovery_percentage(self):
        c=reinsurance_case();c['contracts'][1]['recovery_fraction']='0.5';self.block(c)
    def test_reinsurance_loss_recovery_block(self):
        c=reinsurance_case();c['reports'][1]['loss_recovery']='10';self.block(c)
    def test_reinsurance_nonperformance(self):
        c=reinsurance_case();c['reports'][1]['nonperformance_reviewed']=False;self.block(c)
    def test_reinsurance_netting(self):
        c=reinsurance_case();c['statement_review']['gross_presentation']=False;self.block(c)
    def test_opening_contracts(self):
        c=case();c['reports'][0]['opening_lrc']='100';self.block(c)
    def test_posting_not_supported(self):
        for action in ('erp_posting','actuarial_projection','actuarial_certification'):
            c=case();c['requested_action']=action;self.block(c)
    def test_advanced_routes(self):
        for model in ('IFRS17_VFA','IFRS17_TRANSITION','ASC944_LDTI','proposed_risk_mitigation'):
            c=case();c['insurance_model']=model;self.block(c)
    def test_acquired_modified_transition(self):
        for key in ('acquired','modification','transition'):
            c=case();c['contracts'][0][key]=True;self.block(c)
    def test_aasb_scope(self):
        c=case('AASB');c['reporting_tier']=2;self.block(c)
    def test_aasb_actual_compilation(self):
        c=case('AASB');c['aasb_compilation']='generic2026';self.block(c)
    def test_unbound_owner_imports(self):
        for owner in ('financial-instruments-ecl','fair-value-measurement','derivatives-hedge-accounting','foreign-currency'):
            c=case();c['imports']=[{'id':'unbound','package':owner}];self.block(c)
    def test_unknown_policy_election(self):
        c=case();c['policy_elections']['risk_mitigation']=True;self.block(c)
    def test_wrong_currency(self):
        c=case();c['contracts'][0]['currency']='USD';self.block(c)
    def test_wrong_period(self):
        c=case();c['reporting_period']='2027-12-31';self.block(c)
    def test_gl_balance(self):
        c=case();c['gl'][0]['closing']='999';self.block(c)
    def test_gl_statement(self):
        c=case();c['gl'][0]['statement']='999';self.block(c)
    def test_disclosure_incomplete(self):
        c=case();c['disclosure_review']['requirement_ids'].pop();self.block(c)
    def test_source_bytes(self):
        c=ready();c['documents'][0]['content']['terms_memo']='changed';self.assertEqual('blocked',assess_case(PACKAGE,c)['status'])
    def test_stale_knowledge(self):
        c=ready();c['knowledge_review']['documents'][0]['sha256']='stale';self.assertEqual('blocked',assess_case(PACKAGE,c)['status'])
    def test_missing_applied_claim(self):
        c=ready();c['knowledge_review']['applied_claim_ids'].pop();self.assertEqual('blocked',assess_case(PACKAGE,c)['status'])
    def test_partial_without_signoff(self):
        c=ready();c.pop('reviewer_signoff');self.assertEqual('partial',assess_case(PACKAGE,c)['status'])
    def test_stale_case_signoff(self):
        c=ready();c['judgment_memo']='changed';self.assertEqual('partial',assess_case(PACKAGE,c)['status'])
    def test_stale_implementation(self):
        c=ready()
        with patch('production.case_fingerprint',return_value='changed'):self.assertEqual('partial',assess_case(PACKAGE,c)['status'])
    def test_privacy_all_routes(self):
        r=self.run_case(case());r['facts_used']['secret']='private-source-record';r['evidence'][0]['source_note']='Source: ChatGPT training data'
        for route in ROUTES:
            out=json.dumps(to_public(r,route),default=serializable)
            for token in ('Source:','evidence_status','audit_required','approval_track','sha256','case_fingerprint','private-source-record'):self.assertNotIn(token,out)
    def test_malformed(self):
        for c in (None,{},[],dict(framework='OTHER')):self.assertEqual('blocked',assess_case(PACKAGE,c)['status'])
    def test_examples_reproduce(self):
        from generate_insurance_examples import artifacts
        root=Path(__file__).resolve().parents[2]
        for path,obj in artifacts().items():self.assertEqual(json.loads((root/path).read_text()),json.loads(json.dumps(obj,default=serializable)),path)
