"""Independent exact-current October timing relationship attacks."""
import copy
import unittest

from orchestration import stage3
from orchestration.tests import stage4_fixtures as fixture
from orchestration.runtime import CAO
from additional_cases import certify


class IndependentCurrentTiming(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.control = fixture.initial()

    def setUp(self):
        self.f = copy.deepcopy(self.control)
        self.e = self.f['session']
        self.node = self.f['nodes']['match-timing-current']
        self.source = fixture.current_timing_match(self.f)

    def execute(self):
        return stage3.bounded_executor(self.e, self.node, self.source,
            stage3_receipts(self.f, self.node.id))

    def test_current_match_has_sealed_source_exact_versions_and_retained_history(self):
        source = fixture.qualified_replacement(self.f, self.node.id, self.source)
        self.assertIn('qualified_input_snapshot', source)
        self.source = source
        result = self.execute()
        self.assertEqual(result['matching']['classification'], 'MATCHED')
        versions = {self.e.versions.current(self.f['nodes'][label].id).version_id
            for label in ('timing-current-ENTITY-NL', 'timing-ENTITY-UK')}
        self.assertEqual({s['result_version'] for s in source['sides']}, versions)
        old = self.e.versions.current(self.f['nodes']['match-timing'].id).payload()
        self.assertEqual(old['matching']['classification'], 'TIMING_DIFFERENCE')
        self.assertFalse(result['accounting_authority'])
        self.assertEqual(result['journal_entry_implications'], [])

    def test_historical_september_owner_cannot_substitute_current_october(self):
        old = self.e.versions.current(self.f['nodes']['timing-ENTITY-NL'].id)
        self.source['sides'][0].update(owner_node=old.node_id, result_version=old.version_id,
            case_id=old.case_id, period_id=old.period_id)
        with self.assertRaises(ValueError): self.execute()

    def test_wrong_economic_lineage_rejects_equal_principal(self):
        self.source['sides'][0]['economic_id'] = 'clean'
        with self.assertRaises(ValueError): self.execute()

    def test_wrong_counterparty_rejects(self):
        self.source['sides'][0]['counterparty_scope'] = 'ENTITY-US'
        with self.assertRaises(ValueError): self.execute()

    def test_wrong_scope_rejects(self):
        self.source['sides'][0]['scope_id'] = 'ENTITY-US'
        with self.assertRaises(ValueError): self.execute()

    def test_omitted_current_side_rejects_even_with_rewritten_decision(self):
        self.source['sides'].pop()
        from orchestration.intercompany_network import TransactionSide
        side = TransactionSide(**self.source['sides'][0])
        self.source['decision'].update(side_ids=[side.side_id], result_versions=[side.result_version])
        with self.assertRaises(ValueError): self.execute()

    def test_stale_current_legal_result_rejects(self):
        key = self.f['nodes']['timing-ENTITY-NL'].id
        source = fixture.legal_source(self.f, 'timing', 'ENTITY-NL')
        source['independent_reconfirmation'] = 'Independent equal-value prior-close correction'
        CAO().correct(self.f['case'], key, certify('intercompany-accounting', source),
            'Independent stale October owner attack')
        with self.assertRaises(ValueError): self.execute()

    def test_superseded_current_legal_result_rejects(self):
        key = self.f['nodes']['timing-current-ENTITY-NL'].id
        source = fixture.source(self.f, 'timing-current-ENTITY-NL')
        source['independent_reconfirmation'] = 'Independent equal-value October correction'
        CAO().correct(self.f['case'], key, certify('intercompany-accounting', source),
            'Independent superseded October owner attack')
        with self.assertRaises(ValueError): self.execute()


def stage3_receipts(f, node_id):
    from orchestration.tests.stage3_fixtures import receipts
    return receipts(f, node_id)
