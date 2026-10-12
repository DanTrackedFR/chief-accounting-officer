"""Permanent authored production and adverse source/certification regressions."""
import unittest
from copy import deepcopy
from borrowing_costs_cases import case,ready,remeasure,capture_sources
from operational_cases import approved
from production import assess_case,to_public,case_fingerprint

class BorrowingCostsTests(unittest.TestCase):
    def blocked(self,c):
        capture_sources(c)
        r=assess_case('borrowing-costs',ready(c=c));self.assertEqual(r['status'],'blocked',r.get('conclusion'));self.assertFalse(r['journal_entry_implications']);return r
    def complete(self,c):
        r=assess_case('borrowing-costs',ready(c=c));self.assertEqual(r['status'],'complete',r.get('conclusion'));return r
    def test_ifrs(self):self.assertEqual(str(self.complete(case())['calculations']['capitalized']),'11032.88')
    def test_aasb(self):self.complete(case('AASB'))
    def test_us(self):self.complete(case('US_GAAP'))
    def test_uk(self):self.complete(case('UK_GAAP'))
    def test_specific(self):
        self.assertEqual(str(self.complete(case(method='specific'))['calculations']['capitalized']),'15000.00')
        self.assertEqual(str(self.complete(case('US_GAAP','specific'))['calculations']['capitalized']),'9024.66')
    def test_general(self):self.complete(case(method='general'))
    def test_mixed(self):self.complete(case(method='mixed'))
    def test_uk_expense(self):
        c=case('UK_GAAP');c['accounting_policy']['borrowing_costs']='expense';remeasure(c);capture_sources(c);self.assertEqual(str(self.complete(c)['calculations']['capitalized']),'0.00')
    def test_missing_uk_election(self):c=case('UK_GAAP');c['accounting_policy'].pop('borrowing_costs');self.blocked(c)
    def test_nonqualifying_asset(self):c=case();c['projects'][0]['qualifying_asset']=False;self.blocked(c)
    def test_inventory_specialist(self):c=case();c['projects'][0]['asset_type']='inventory';self.blocked(c)
    def test_duplicate_debt_economics(self):c=case();c['borrowings'][1]['economic_id']=c['borrowings'][0]['economic_id'];self.blocked(c)
    def test_duplicate_expenditure(self):c=case();x=deepcopy(c['projects'][0]['expenditures'][0]);x['id']='second';c['projects'][0]['expenditures'].append(x);c['projects'][0]['expenditure_inventory'].append('second');self.blocked(c)
    def test_rate_reset(self):
        c=case(method='general');b=c['borrowings'][0];s=b['segments'][0];s['end']='2026-06-30';t=deepcopy(s);t.update(id='reset',start='2026-07-01',end='2026-12-31',annual_rate='.10',effective_annual_rate='.10');b['segments'].append(t);b['segment_inventory'].append('reset');remeasure(c);capture_sources(c);self.complete(c)
    def test_draw(self):
        c=case(method='general');b=c['borrowings'][0];b['events']=[approved('draw',date='2026-07-01',kind='draw',amount='100000')];b['event_inventory']=['draw'];remeasure(c);capture_sources(c);self.complete(c)
    def test_repayment(self):
        c=case(method='general');b=c['borrowings'][0];b['events']=[approved('repay',date='2026-07-01',kind='repayment',amount='100000')];b['event_inventory']=['repay'];remeasure(c);capture_sources(c);self.complete(c)
    def test_missing_cashflow(self):c=case();c['borrowings'][0]['cashflow_interest_total']='0';self.blocked(c)
    def test_incomplete_loan_population(self):c=case();c['borrowing_inventory'].append('missing');self.blocked(c)
    def test_rate_tamper(self):c=case();c['borrowings'][0]['segments'][0]['annual_rate']='.07';self.blocked(c)
    def test_interest_overclaim(self):c=case();c['projects'][0]['expected_capitalized']='43000';self.blocked(c)
    def test_missing_expenditure_date(self):c=case();c['projects'][0]['expenditures'][0].pop('date');self.blocked(c)
    def test_future_expenditure(self):c=case();c['projects'][0]['expenditures'][0]['date']='2027-01-01';self.blocked(c)
    def test_later_payment(self):c=case();c['projects'][0]['expenditures'][0]['cash_date']='2026-08-01';self.blocked(c)
    def test_invalid_start(self):c=case();c['projects'][0]['activity_start']='2025-11-01';self.blocked(c)
    def test_invalid_suspension(self):c=case();c['projects'][0]['timeline'][0]['state']='suspended';self.blocked(c)
    def test_valid_suspension(self):
        c=case();p=c['projects'][0];p['timeline'][0].update(state='suspended',extended=True,necessary_delay=False,substantial_technical_activity=False);remeasure(c);capture_sources(c);self.assertEqual(str(self.complete(c)['calculations']['capitalized']),'0.00')
    def test_temporary_interruption(self):c=case();c['projects'][0]['timeline'][0]['state']='temporary';capture_sources(c);self.complete(c)
    def test_invalid_cessation(self):c=case();c['projects'][0]['ready_date']='2025-12-01';self.blocked(c)
    def test_midyear_completion(self):
        c=case();p=c['projects'][0];p['ready_date']='2026-07-01';p['timeline'][0]['end']='2026-06-30';t=deepcopy(p['timeline'][0]);t.update(id='complete',start='2026-07-01',end='2026-12-31',state='complete');p['timeline'].append(t);p['timeline_inventory'].append('complete');remeasure(c);capture_sources(c);self.complete(c)
    def test_shared_partial_completion(self):c=case();c['projects'][0]['shared_components']=True;self.blocked(c)
    def test_abandonment(self):c=case();c['projects'][0]['abandoned']=True;self.blocked(c)
    def test_unsupported_fx(self):c=case();c['borrowings'][0]['fx_adjustment']='100';self.blocked(c)
    def test_specific_investment_income(self):c=case(method='specific');c['borrowings'][0]['segments'][0]['investment_income']='1000';remeasure(c);capture_sources(c);self.assertEqual(str(self.complete(c)['calculations']['capitalized']),'14000.00')
    def test_general_investment_income(self):c=case(method='general');c['borrowings'][0]['segments'][0]['investment_income']='1000';self.blocked(c)
    def test_us_investment_income(self):c=case('US_GAAP');c['borrowings'][0]['segments'][0]['investment_income']='100';self.blocked(c)
    def test_wrong_framework(self):c=case();c['projects'][0]['source_framework']='US_GAAP';self.blocked(c)
    def test_wrong_edition(self):c=case();c['accounting_policy']['effective_standard']='IAS23_OLD';self.blocked(c)
    def test_wrong_entity(self):c=case();c['borrowings'][0]['source_entity']='Other';self.blocked(c)
    def test_wrong_period(self):c=case();c['borrowings'][0]['source_period']=['2025-01-01','2025-12-31'];self.blocked(c)
    def test_wrong_currency(self):c=case();c['borrowings'][0]['currency']='USD';self.blocked(c)
    def test_changed_evidence_version(self):c=case();c['projects'][0]['version']='v2';self.blocked(c)
    def test_interest_gl(self):c=case();c['financing_gl_interest']='1';self.blocked(c)
    def test_asset_gl(self):c=case();c['gl'][0]['closing']='1';self.blocked(c)
    def test_gl_opening_shift(self):c=case();c['gl'][0]['opening']='200001';c['gl'][0]['closing']=str(float(c['gl'][0]['closing'])+1);c['gl'][0]['statement']=c['gl'][0]['closing'];self.blocked(c)
    def test_duplicate_journal_economics(self):c=case();c['imports']=[approved('bogus',package='debt-financing',case={},result={},mode='posting')];self.blocked(c)
    def test_altered_upstream_result(self):c=case();c['imports']=[approved('bogus',package='debt-financing',case={'entity':c['entity'],'framework':c['framework'],'period_start':c['period_start'],'reporting_period':c['reporting_period']},result={'status':'complete'},mode='evidence_only')];self.blocked(c)
    def test_missing_review(self):
        c=ready();c.pop('reviewer_signoff');r=assess_case('borrowing-costs',c);self.assertEqual(r['status'],'partial');self.assertFalse(r['journal_entry_implications'])
    def test_stale_review(self):
        c=ready();c['evidence'].append('changed population');r=assess_case('borrowing-costs',c);self.assertEqual(r['status'],'partial');self.assertFalse(r['journal_entry_implications'])
    def test_missing_knowledge_review(self):c=ready();c.pop('knowledge_review');r=assess_case('borrowing-costs',c);self.assertEqual(r['status'],'blocked')
    def test_cip_only_authority(self):
        from production import load_workflow
        from core_accounting import ReviewRequired
        with self.assertRaises(ReviewRequired):load_workflow('borrowing-costs').assess(case(),[{'topic_id':'TOPIC-04-003'}])
    def test_aasb_tier2(self):c=case('AASB');c['reporting_tier']=2;self.blocked(c)
    def test_fee_eir_difference(self):c=case();c['borrowings'][0]['fees']='100';self.blocked(c)
    def test_public_privacy(self):
        public=str(to_public(self.complete(case())));self.assertNotIn('synthetic complete population reviewer',public);self.assertNotIn('invoice-001',public);self.assertNotIn('case_fingerprint',public)

if __name__=='__main__':unittest.main()
