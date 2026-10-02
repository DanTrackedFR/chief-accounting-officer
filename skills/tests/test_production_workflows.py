import copy,json,sys,unittest
from decimal import Decimal
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from production import execute,to_public,case_fingerprint,serializable
from core_accounting import ReviewRequired,dec,balance
from cases import revenue,ecl,provision,consolidation,finalize

class Workflows(unittest.TestCase):
    def test_all_four_frameworks_end_to_end(self):
        for fw in ['IFRS','US_GAAP','UK_GAAP','AASB']:
            for pkg,make in [('revenue-recognition',revenue),('financial-instruments-ecl',ecl),('provisions-contingencies',provision),('consolidation',consolidation)]:
                with self.subTest(fw=fw,pkg=pkg):
                    r=execute(pkg,make(fw));self.assertEqual(r['status'],'complete')
                    for j in r['journal_entry_implications']:self.assertTrue(balance(j))
                    for route in ['answer','answer_context','retrieval_snippet','citation','tool_output','user_log','export']:
                        p=to_public(r,route);text=json.dumps(p,default=serializable)
                        self.assertNotIn('source_note',text);self.assertNotIn('MODEL_DERIVED',text)
                        self.assertNotIn('knowledge_documents',text);self.assertTrue(p['guidance'])
                    json.dumps(r,default=serializable)
    def test_period_revenue_not_cumulative(self):
        r=execute('revenue-recognition',revenue())['calculations']
        self.assertEqual(r['cumulative_revenue'],800);self.assertEqual(r['period_revenue'],500)
        self.assertEqual(r['contract_bridge']['closing'],-100);self.assertEqual(r['receivable'],300)
        self.assertEqual(r['contract_cost_asset'],120)
    def test_revenue_legacy_uk_route(self):
        r=execute('revenue-recognition',revenue('UK_GAAP','2025-01-01'));self.assertIn('Legacy',r['method'])
    def test_uk_period_election_mismatch(self):
        c=revenue('UK_GAAP','2025-01-01');c['policy_elections']['section23_model']='revised_2026'
        with self.assertRaises(ReviewRequired):execute('revenue-recognition',c)
    def test_over_time_payment_right_adversarial(self):
        c=revenue();o=c['obligations'][1];o['simultaneous_receipt']=False;o['no_alternative_use']=True;o['right_to_payment_with_margin']=False
        with self.assertRaises(ReviewRequired):execute('revenue-recognition',c)
    def test_variable_constraint_and_specific_allocation(self):
        c=revenue();c['price_components']['variable']=[{'method':'expected_value','outcomes':[{'amount':'200','probability':'0.8'},{'amount':'0','probability':'0.2'}],
          'constraint_memo':'Supported entitlement only100','included_amount':'100','royalty_exception':False}]
        c['specific_allocation']={'amounts':{'delivery':'600','service':'500'},'objective_memo':'Bonus relates only to service'}
        r=execute('revenue-recognition',c)['calculations'];self.assertEqual(r['transaction_price'],1100);self.assertEqual(r['cumulative_revenue'],850)
    def test_duplicate_promise_and_negative_price(self):
        c=revenue();c['obligations'][1]['id']='delivery'
        with self.assertRaises(ReviewRequired):execute('revenue-recognition',c)
        c=revenue();c['price_components']['fixed']='-1'
        with self.assertRaises(ReviewRequired):execute('revenue-recognition',c)
    def test_catch_up_reversal(self):
        c=revenue();c['balance_bridge']['opening_revenue']='900'
        r=execute('revenue-recognition',c);self.assertEqual(r['calculations']['period_revenue'],-100)
        self.assertEqual(r['journal_entry_implications'][0][0]['account'],'revenue')
    def test_ecl_allowance_rollforward(self):
        r=execute('financial-instruments-ecl',ecl())['calculations']
        self.assertEqual(r['allowance'],Decimal('62.50'));self.assertEqual(r['expense'],Decimal('-22.50'))
        self.assertEqual(r['gross_carrying_amount'],980)
    def test_ecl_stage1_horizon(self):
        c=ecl();c['credit']['sicr']=False
        with self.assertRaises(ReviewRequired):execute('financial-instruments-ecl',c)
        c['credit']['horizon']='12_month_default_events';self.assertEqual(execute('financial-instruments-ecl',c)['method']['stage'],1)
    def test_ecl_us_staging_rejected(self):
        c=ecl('US_GAAP');c['instrument']['stage']=1
        with self.assertRaises(ReviewRequired):execute('financial-instruments-ecl',c)
    def test_ecl_uk_election(self):
        c=ecl('UK_GAAP');c['policy_elections']['financial_instruments']='IFRS9';c['instrument']['impairment_model']='general'
        self.assertEqual(execute('financial-instruments-ecl',c)['method']['stage'],2)
    def test_ecl_survival_and_scope(self):
        c=ecl();terms=c['credit']['scenarios'][0]['terms'];terms[0]['marginal_pd']='0.8';terms.append(copy.deepcopy(terms[0]))
        with self.assertRaises(ReviewRequired):execute('financial-instruments-ecl',c)
        c=ecl();c['instrument']['sppi']=False
        with self.assertRaises(ReviewRequired):execute('financial-instruments-ecl',c)
    def test_provision_movement_not_difference(self):
        r=execute('provisions-contingencies',provision())['calculations'];self.assertEqual(r['provision'],45);self.assertEqual(r['provision_bridge']['estimate_change'],15)
    def test_provision_framework_range_difference(self):
        c=provision('US_GAAP');c['estimate'].update(low='100',high='200',best_estimate=None)
        self.assertEqual(execute('provisions-contingencies',c)['calculations']['provision'],100)
        c=provision();c['estimate'].update(basis='continuous_equal_range',low='100',high='200')
        self.assertEqual(execute('provisions-contingencies',c)['calculations']['provision'],150)
    def test_provision_negative_probability(self):
        c=provision();c['estimate']['outcomes'][0]['probability']='-1';c['estimate']['outcomes'][1]['probability']='2'
        with self.assertRaises(ReviewRequired):execute('provisions-contingencies',c)
    def test_provision_disclosure_route(self):
        c=provision();c['obligation'].update(probability='possible',release_memo='Prior obligation no longer probable')
        r=execute('provisions-contingencies',c);self.assertEqual(r['method']['decision'],'disclose_contingency');self.assertEqual(r['calculations']['provision'],0)
    def test_us_discount_and_constructive_obligation(self):
        c=provision('US_GAAP');c['estimate']['discount_rate']='0.05'
        with self.assertRaises(ReviewRequired):execute('provisions-contingencies',c)
        c=provision('US_GAAP');c['obligation']['basis']='constructive'
        with self.assertRaises(ReviewRequired):execute('provisions-contingencies',c)
    def test_reimbursement_capped_and_separate(self):
        c=provision();c['reimbursement'].update(claimed='100',recognition_threshold_met=True)
        r=execute('provisions-contingencies',c)['calculations'];self.assertEqual(r['reimbursement'],45);self.assertEqual(r['provision'],45)
    def test_consolidation_no_intercompany_valid(self):
        r=execute('consolidation',consolidation())['calculations'];self.assertEqual(sum(r['consolidated_balances'].values()),0)
        self.assertEqual(r['consolidated_balances']['investment'],0);self.assertEqual(r['consolidated_balances']['noncontrolling interest'],-20)
    def test_control_not_ownership(self):
        c=consolidation();c['entities'][1]['control']['substantive_power']=False
        with self.assertRaises(ReviewRequired):execute('consolidation',c)
    def test_vie_primary_beneficiary(self):
        c=consolidation('US_GAAP');ctrl=c['entities'][1]['control'];ctrl.update(model='VIE',power_significant_activities=True,potentially_significant_losses_benefits=True)
        self.assertEqual(execute('consolidation',c)['calculations']['perimeter'],['P','S'])
        ctrl['potentially_significant_losses_benefits']=False
        with self.assertRaises(ReviewRequired):execute('consolidation',c)
    def test_unbalanced_tb_and_cashflow(self):
        c=consolidation();c['entities'][0]['balances']['cash']='301'
        with self.assertRaises(ReviewRequired):execute('consolidation',c)
        c=consolidation();c['cash_flow_bridge']['operating']='1'
        with self.assertRaises(ReviewRequired):execute('consolidation',c)
    def test_nonexistent_intercompany_entities(self):
        c=consolidation();c['intercompany']=[{'seller':'X','buyer':'Y','debit_account':'AP','credit_account':'AR','amount':'10','matched':True,'family':'balances','source_id':'x'}]
        with self.assertRaises(ReviewRequired):execute('consolidation',c)
    def test_review_fingerprint_invalidated(self):
        c=revenue();c['balance_bridge']['cash_received']='100'
        self.assertEqual(execute('revenue-recognition',c)['status'],'partial')
        c['reviewer_signoff']['case_fingerprint']=case_fingerprint(c);self.assertEqual(execute('revenue-recognition',c)['status'],'complete')
    def test_knowledge_and_scope_gate(self):
        c=revenue();c['knowledge_review']['claim_ids']=[]
        with self.assertRaises(ReviewRequired):execute('revenue-recognition',c)
        c=revenue('AASB');c['entity_type']='NFP'
        with self.assertRaises(ReviewRequired):execute('revenue-recognition',c)
    def test_public_contamination_fails_closed(self):
        r=execute('revenue-recognition',revenue());r['conclusion']='Source: private note'
        with self.assertRaises(ValueError):to_public(r)
    def test_finite_decimal_and_journal_side(self):
        for bad in ['NaN','Infinity','-Infinity',True,1.2]:
            with self.assertRaises(ReviewRequired):dec(bad)
        with self.assertRaises(ReviewRequired):balance([{'side':'X','account':'cash','amount':'0'}])

if __name__=='__main__':unittest.main()
