"""Final independent release-contract audit; failures are release findings.

Uses public existing request/fixture interfaces, not proposed new runtime APIs.
"""
import unittest
from orchestration.runtime import CAO
from orchestration.tests.stage2_fixtures import build, initial, correction


class FinalRuntimeAudit(unittest.TestCase):
    def setUp(self):
        self.f = build()
        self.e = self.f['coordinator']
        self.node = self.f['nodes']['US-SEP']

    def request(self):
        n = self.node
        return dict(objective='Review revenue recognition', scope=dict(
            entity=n.scope_id, framework=n.framework, jurisdiction=n.jurisdiction,
            currency=n.functional_currency, period_start=n.period[0],
            reporting_period=n.period[1], period_id=n.period_id,
            scopes=self.e.cases.scopes.record(), period_registry=self.e.periods.record()),
            facts={'customer_contract': self.f['sources'][n.id]})

    def test_ordinary_case_qualifies_scope_period(self):
        case = CAO().run(self.request())
        self.assertEqual(case.outcome, 'complete')
        self.assertEqual((case.scope_id, case.period_id, case.case_type),
                         (self.node.scope_id, self.node.period_id, 'ENTITY_CASE'))

    def test_ordinary_completed_nodes_bind_governed_case(self):
        case = CAO().run(self.request())
        self.assertEqual(case.outcome, 'complete')
        self.assertTrue(all(n['case_id'] for n in case.workplan_nodes))

    def test_ordinary_complete_result_has_version_lineage(self):
        case = CAO().run(self.request())
        self.assertEqual(case.outcome, 'complete')
        self.assertTrue(case.result_version_refs, 'Completed temporal execution lacks result versions')
        self.assertTrue(all(n['execution_receipt'].get('result_version')
                            for n in case.workplan_nodes))

    def test_closed_period_ordinary_native_execution_fails_closed(self):
        self.e.periods.close(self.node.period_id)
        case = CAO().run(self.request())
        self.assertNotEqual(case.outcome, 'complete')
        self.assertFalse(any(n['status'] == 'complete' for n in case.workplan_nodes))


class FinalProofAudit(unittest.TestCase):
    def test_central_chain_still_selective(self):
        f = initial(build())
        old_uk = f['coordinator'].versions.current(f['nodes']['UK-SEP'].id)
        plan = correction(f)
        self.assertEqual(len(plan['execution_order']), 4)
        f['coordinator'].reexecute(plan, f['executors'], f['sources'])
        self.assertEqual(f['coordinator'].versions.current(old_uk.node_id), old_uk)

    def test_required_unaffected_controls_executable(self):
        f = initial(build())
        e = f['coordinator']
        nodes = list(f['nodes'].values())
        roles = {
            'Treasury': [n for n in nodes if 'treasury' in n.selected_skill.lower() or
                         'treasury' in n.issue.lower()],
            'future period': [n for n in nodes if n.period[0] > '2026-10-31'],
            'nonconsuming Group': [n for n in nodes if n.scope_type == 'GROUP' and
                                   not n.dependencies],
        }
        for role, controls in roles.items():
            with self.subTest(role=role):
                self.assertTrue(controls, 'Missing executable unaffected ' + role + ' control')
                before = {n.id: e.versions.current(n.id).version_id for n in controls}
                plan = correction(f)
                for n in controls:
                    self.assertIn(n.id, plan['unaffected'])
                    self.assertEqual(e.versions.current(n.id).version_id, before[n.id])

    def test_comparative_dependency_is_executed(self):
        f = initial(build())
        e = f['coordinator']
        comparisons = [edge for edge in e.edges.values() if edge.dependency_type == 'COMPARATIVE']
        self.assertTrue(comparisons, 'Period relationship alone is not executed comparative lineage')
        for edge in comparisons:
            e.validate_receipt(e.receipt(edge.id), edge.consumer_node)


class FinalRemediationAttackAudit(unittest.TestCase):
    def test_local_observation_cannot_relabel_producer_currency(self):
        f = build()
        node = f['nodes']['US-REPORT']
        f['sources'][node.id]['observation_currency'] = 'EUR'
        with self.assertRaises((ValueError, AssertionError)):
            initial(f)

    def test_governed_node_cannot_substitute_registered_dimensions(self):
        f = build()
        node = f['nodes']['GROUP-CONTROL']
        node.framework = 'US_GAAP'
        node.functional_currency = 'JPY'
        node.jurisdiction = 'JP'
        with self.assertRaises((ValueError, AssertionError)):
            initial(f)


if __name__ == '__main__':
    unittest.main()
