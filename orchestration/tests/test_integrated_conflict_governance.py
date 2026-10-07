"""Generic regression: retain blocked consumers without accounting authority."""
import copy
import unittest
from orchestration.tests.stage3_fixtures import build, initial, add_edge, execute, downstream_source
from orchestration.versions import blocked_payload


class IntegratedConflictGovernance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        f=build()
        add_edge(f,'match-mismatch','group',('matching','classification'))
        cls.base=initial(f)

    def setUp(self):
        self.f=copy.deepcopy(self.base);self.e=self.f['session'];self.n=self.f['nodes']

    def test_material_conflict_blocks_actual_downstream_consumer(self):
        n=self.n['group'];v=self.e.versions.current(n.id)
        self.assertEqual(n.status,'blocked');self.assertEqual(v.payload()['status'],'blocked')
        self.assertFalse(v.payload()['accounting_authority'])
        self.assertEqual(v.payload()['journal_entry_implications'],[])
        self.assertEqual(len(v.dependency_bindings),2)
        self.assertEqual(self.e.cases.get(n.case_id).outcome,'partial')

    def test_unrelated_native_reporting_keeps_exact_current_version(self):
        n=self.n['reporting'];self.assertEqual(n.status,'complete')
        self.e.versions.require_current(self.e.versions.current(n.id).version_id)

    def test_unresolved_owner_cannot_supply_current_receipt(self):
        edge=self.f['edges'][('match-mismatch','group')]
        with self.assertRaises(ValueError):self.e.receipt(edge)

    def test_publishing_fake_complete_result_cannot_bypass_conflict(self):
        n=self.n['group'];v=self.e.versions.current(n.id)
        p=dict(v.payload(),status='complete',unresolved_dependencies=[])
        with self.assertRaises(ValueError):self.e.versions.publish(n,p,self.e.sources[n.id],v.dependency_bindings,'Attack')

    def test_blocked_record_cannot_insert_journal(self):
        n=self.n['group'];v=self.e.versions.current(n.id);p=v.payload()
        p['journal_entry_implications']=[{'plug':'1'}]
        with self.assertRaises(ValueError):self.e.versions.publish(n,p,self.e.sources[n.id],v.dependency_bindings,'Attack')

    def test_conflict_evidence_remains_immutable(self):
        n=self.n['match-mismatch'];v=self.e.versions.current(n.id)
        p=v.payload();p['matching']['classification']='MATCHED'
        self.assertEqual(v.payload()['matching']['classification'],'UNRESOLVED_MISMATCH')

    def test_clear_result_cannot_be_arbitrarily_blocked(self):
        n=self.n['reporting'];v=self.e.versions.current(n.id)
        p=blocked_payload(n,self.e.sources[n.id],v.dependency_bindings,['invented'])
        with self.assertRaises(ValueError):self.e.versions.publish(n,p,self.e.sources[n.id],v.dependency_bindings,'Attack')
