"""Authored source-assurance integration regressions and dependency proofs."""
import copy
import unittest
from decimal import Decimal
from test_presumed_accounting_qa import source_case, run, findings


class AuthoredPresumedSources(unittest.TestCase):
    def test_missing_inputs_and_independent_bad_date_aggregate(self):
        c=source_case();a=c['assets'][0]
        a.pop('residual');a.pop('method');a['ready_date']='bad'
        r=run(case=c)
        paths={n['field_path'] for n in r['validation_requirements']}
        self.assertTrue(any('residual' in p for p in paths))
        self.assertTrue(any('method' in p for p in paths))
        self.assertTrue(any('ready_date' in p for p in paths))
        self.assertEqual(r['calculations']['assets'],[])

    def test_capital_cost_and_routine_expense_need_no_review_memos(self):
        c=source_case();a=c['assets'][0];a.update(opening_cost='0',opening_accumulated='0',residual='0',remaining_life='5',ready_date='2026-01-01')
        c['costs']=[dict(id='purchase',kind='purchase',amount='10000',date='2026-01-01',destination=a['id'],offset='accounts payable'),
                    dict(id='training',kind='training',amount='500',date='2026-01-01',account='training expense',offset='accounts payable')]
        r=run(case=c)
        self.assertEqual(r['calculations']['depreciation'],Decimal('2000'))
        self.assertEqual(r['calculations']['excluded_expense'],Decimal('500'))
        self.assertEqual(r['accounting_determination'],'SUPPORTED')

    def test_unresolved_movement_blocks_only_dependent_asset(self):
        c=source_case();a=c['assets'][0];c['assets'].append({**a,'id':'unrelated'})
        c['costs']=[dict(id='unclear',kind='specialized',amount='1000',date='2026-01-01',destination=a['id'],offset='accounts payable')]
        r=run(case=c)
        self.assertEqual([x['id'] for x in r['calculations']['assets']],['unrelated'])
        self.assertEqual(r['calculations']['depreciation'],Decimal('90000'))

    def test_asset_quantity_arithmetic_prevents_unsupported_basis(self):
        c=source_case();c['assets'][0].update(amount='600000',quantity='10',unit_price='50000')
        r=run(case=c)
        self.assertEqual(r['calculations']['assets'],[])
        self.assertTrue(findings(r,'arithmetic','BLOCKED'))

    def test_multiple_scope_requirements_are_structured(self):
        c=source_case();c.update(entity_type='not_for_profit',framework='OTHER',functional_currency='bad')
        r=run(case=c)
        self.assertEqual(r['status'],'blocked')
        self.assertGreaterEqual(len(r['validation_requirements']),3)
        for n in r['validation_requirements']:self.assertEqual(set(n),{'identifier','field_path','explanation','category'})

    def test_optional_gl_error_never_creates_or_removes_supported_journal(self):
        c=source_case();r=run(case=c)
        c['assets'][0]['gl_cost']='invalid'
        altered=run(case=c)
        self.assertEqual(altered['calculations'],r['calculations'])
        self.assertEqual(altered['proposed_journal_workpaper'],r['proposed_journal_workpaper'])
        self.assertEqual(altered['anomaly_report']['population_status'],'UNRECONCILED')

    def test_optional_po_and_receipt_match_checks_are_separate_and_not_passed(self):
        r=run('accounts-payable')
        skipped=[x for x in findings(r,'arithmetic','NOT_PERFORMED') if 'matching was not performed' in x['explanation']]
        self.assertEqual(len(skipped),2)
        self.assertEqual(r['calculations']['invoices'],Decimal('120'))

    def test_no_policy_elections_are_assumed_and_unknowns_refuse(self):
        c=source_case();self.assertNotIn('policy_elections',c)
        self.assertEqual(run(case=c)['policy_elections_disclosure'],'No policy elections were assumed.')
        c['policy_elections']={'model':'fair_value'}
        self.assertEqual(run(case=c)['status'],'blocked')

    def test_independent_missing_invalid_and_specialist_inputs_aggregate(self):
        c=source_case();a=c['assets'][0]
        a.pop('remaining_life');a.update(opening_cost='-1',ready_date='invalid',lease_like=True)
        result=run(case=c)
        paths={n['field_path'] for n in result['validation_requirements']}
        for field in ('remaining_life','opening_cost','ready_date','lease_like'):
            self.assertTrue(any(field in path for path in paths),field)
        self.assertNotIn('depreciation',result['calculations'])

    def test_independent_invalid_attestation_and_scope_requirements_aggregate(self):
        c=source_case('fixed-assets','AASB')
        c.update(reporting_tier=3,aasb_compilation='future')
        c['source']['hash']='invalid'
        c['source_attestation'].update(timestamp='invalid',represents_company_records=False)
        result=run(case=c)
        paths={n['field_path'] for n in result['validation_requirements']}
        for field in ('reporting_tier','aasb_compilation','source.hash','source_attestation.timestamp','source_attestation.represents_company_records'):
            self.assertIn(field,paths)
        self.assertEqual(result['status'],'blocked')

if __name__=='__main__':unittest.main()
