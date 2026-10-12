"""Independent documented partial snapshot versus real invalidation probes."""
import copy
import unittest
from orchestration.tests import stage3_fixtures as s3
from additional_cases import certify


def documented_control():
    f = s3.initial(s3.build())
    e = f['session']
    case = f['containers']['GROUP-EUR-OCT']
    for state in ('SCOPED','IN_PROGRESS','CHALLENGE'):
        case.transition(state)
    case.challenge_results.append({'kind':'independent residual review','status':'BLOCKED','reason':'Retained current material mismatch'})
    case.transition('CONCLUDED')
    case.transition('DOCUMENTED')
    assert case.outcome == 'partial'
    return f, e, case


class IndependentCaseRefresh(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.base = documented_control()

    def setUp(self): self.f, self.e, self.case = copy.deepcopy(self.base)

    def refresh(self): self.e.cases.refresh(self.e.graph, self.e.versions, self.e.edges)

    def test_unchanged_current_partial_documentation_survives_refresh(self):
        refs = list(self.case.result_version_refs)
        transitions = list(self.case.transitions)
        history = copy.deepcopy(self.case.governance_history)
        self.refresh()
        self.refresh()
        self.assertEqual((self.case.outcome,self.case.status), ('partial','DOCUMENTED'))
        self.assertEqual(self.case.result_version_refs, refs)
        self.assertEqual(self.case.transitions, transitions)
        self.assertEqual(self.case.governance_history, history)

    def test_material_stale_version_reopens_documented_partial(self):
        node = self.f['nodes']['match-mismatch']
        version = self.e.versions.current(node.id)
        self.e.versions.mark_stale(version.version_id, 'independent-review', 'upstream-changed')
        self.refresh()
        self.assertEqual((self.case.outcome,self.case.status), ('partial','IN_PROGRESS'))
        self.assertIn(node.id, self.case.rework_state['required_nodes'])
        self.assertEqual(self.case.transitions[-1], 'REWORK')

    def test_new_current_version_reopens_documented_partial(self):
        before = list(self.case.result_version_refs)
        node = self.f['nodes']['match-mismatch']
        source = copy.deepcopy(self.e.sources[node.id])
        source['evidence'].append('Fresh separately reviewed residual confirmation')
        s3.execute(self.f, 'match-mismatch', source)
        self.assertNotEqual(self.case.result_version_refs, before)
        self.assertEqual((self.case.outcome,self.case.status), ('partial','IN_PROGRESS'))
        self.assertEqual(self.case.transitions[-1], 'REWORK')

    def test_actual_legal_dependency_invalidation_reopens_group_documentation(self):
        before = list(self.case.result_version_refs)
        node = self.f['nodes']['timing-ENTITY-NL']
        source = copy.deepcopy(self.e.sources[node.id])
        source['independent_review_note'] = 'Same source economics; new isolated legal review'
        s3.execute(self.f, 'timing-ENTITY-NL', certify('intercompany-accounting', source))
        # This legal replacement affects the Group's match-timing dependency,
        # so it is genuinely material rather than an unrelated isolation proof.
        self.assertEqual(self.case.status, 'IN_PROGRESS')
        self.assertEqual(self.case.result_version_refs, before)
        self.assertIn(self.f['nodes']['match-timing'].id, self.case.rework_state['required_nodes'])

    def test_partial_documentation_cannot_close(self):
        self.case.observer_ran = True
        self.case.artifacts = [{'kind':'independent reviewed documentation'}]
        with self.assertRaises(ValueError): self.case.transition('CLOSED')
        self.assertEqual(self.case.status, 'DOCUMENTED')

    def test_unrelated_case_result_does_not_reopen_documented_group(self):
        node = s3.add_node(self.f, 'independent-local-review', 'orchestration-local-review', self.f['containers']['ENTITY-UK-OCT'], 'isolated-control')
        from orchestration.governed_plan import observation
        source = dict(scope_id=node.scope_id, period_id=node.period_id,
                      method='QUALIFIED_LOCAL_OBSERVATION', value='0',
                      observation_currency='GBP', evidence=['Separately reviewed unrelated local process'])
        before = list(self.case.result_version_refs)
        self.e.execute(node.id, observation, source, 'Independent unrelated review')
        self.assertEqual((self.case.outcome,self.case.status), ('partial','DOCUMENTED'))
        self.assertEqual(self.case.result_version_refs, before)
        self.assertNotIn('REWORK', self.case.transitions)
