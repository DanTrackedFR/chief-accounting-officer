"""Independent refusal proofs; no positive temporal qualification is claimed."""
import copy
import unittest
from decimal import Decimal

from orchestration.tests import stage4_closing_population as whole
from orchestration.runtime import CAO, production
from orchestration.governed_plan import observation
from orchestration.tests import stage4_fixtures as original
from additional_cases import certify


class IndependentTemporalRefusal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.control, cls.record = whole.run()
        cls.source = whole.source(cls.control, 'reporting')

    def assert_native_blocked(self, source):
        result = production.assess_case('financial-statements', source)
        self.assertEqual(result['status'], 'blocked')
        return result

    def test_actual_owner_refuses_unexplained_equity(self):
        result = self.assert_native_blocked(self.source)
        self.assertIn('Restated comparative equity differs', result['conclusion'])

    def test_actual_comparative_is_year_ago_not_adjacent_prior_close(self):
        self.assertEqual(self.source['comparative']['period_end'], '2025-10-31')
        self.assertEqual(self.source['period_start'], '2026-10-01')
        self.assertEqual(self.source['comparative']['restated_version'], 'No restatement')
        self.assertEqual({row['source_version'] for row in self.source['comparative_tb']}, {'reviewed-prior-v1'})
        self.assertEqual(len(self.source['versioned_dependency_receipts']), 1)
        self.assert_native_blocked(self.source)

    def test_missing_comparative_tb_refuses(self):
        source = copy.deepcopy(self.source)
        del source['comparative_tb']
        self.assert_native_blocked(source)

    def test_missing_current_tb_refuses(self):
        source = copy.deepcopy(self.source)
        del source['current_tb']
        self.assert_native_blocked(source)

    def test_missing_equity_opening_refuses(self):
        source = copy.deepcopy(self.source)
        del source['equity_bridge'][0]['opening']
        self.assert_native_blocked(source)

    def test_missing_cash_opening_refuses(self):
        source = copy.deepcopy(self.source)
        del source['cash_flow']['opening']
        self.assert_native_blocked(source)

    def test_false_continuity_review_flag_does_not_override_numeric_refusal(self):
        source = copy.deepcopy(self.source)
        source['comparative']['opening_equity_tie'] = True
        self.assert_native_blocked(source)

    def test_fabricated_bridge_metadata_does_not_supply_accounting(self):
        source = copy.deepcopy(self.source)
        source['temporal_bridge'] = dict(reviewed=True, equity='-2', cash='1', memo='Claimed unsupported bridge')
        self.assert_native_blocked(source)

    def test_restated_label_does_not_execute_accounting_changes(self):
        source = copy.deepcopy(self.source)
        source['comparative']['restated_version'] = 'Claimed restatement v2'
        source['comparative']['adjustments_memo'] = 'Claimed unexplained correction'
        self.assert_native_blocked(source)

    def test_current_group_preserved_and_stale_reporting_cannot_close(self):
        session = self.control['session']
        group = session.versions.current(self.control['nodes']['elimination'].id).payload()
        self.assertEqual(Decimal(group['calculations']['equity']['profit']), Decimal('3'))
        self.assertEqual(Decimal(group['calculations']['cash_flow']['closing_cash']), Decimal('490'))
        for name in ('reporting', 'analytics', 'group'):
            version = session.versions.current(self.control['nodes'][name].id, allow_stale=True)
            with self.subTest(name=name), self.assertRaises(ValueError):
                session.versions.require_current(version.version_id)
        self.assertNotIn(self.control['case'].status, ('COMPLETE', 'CLOSED'))
        self.assertEqual(CAO().public(self.control['case'])['status'], 'partial')

    def test_historical_results_remain_immutable(self):
        session = self.control['session']
        for name, old in self.record['before'].items():
            self.assertEqual(session.versions.versions[old.version_id], old, name)
        self.assertEqual(self.source['comparative_tb'][0]['balance'], '489')
        self.assertEqual(self.source['comparative_tb'][1]['balance'], '-489')

    def test_tqa01_invented_comparative_and_bridge_require_exact_temporal_results(self):
        # Open substantive finding: keep the required rejection assertion.
        # This attack is not a qualified accounting source.
        f = copy.deepcopy(self.control)
        source = copy.deepcopy(self.source)
        source['comparative_tb'][0]['balance'] = '487'
        source['comparative_tb'][1]['balance'] = '-487'
        source['cash_flow']['opening_balance_sheet_bridge'] = '-3'
        source['cash_flow']['classifications'] = [dict(
            id='attack-zero', date='2026-10-31', kind='capital_receipt',
            **{'class': 'financing'}, amount='0', memo='Unsupported attack only')]
        source = certify('financial-statements', source)
        node = f['nodes']['reporting']
        source = original.qualified_replacement(f, node.id, source)
        with self.assertRaises(ValueError):
            f['session'].execute(node.id, observation, source, 'Attack only: invented comparative')
