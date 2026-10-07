"""Current native loan accounting consumes prior closing, rather than metadata."""
import copy
import unittest
from orchestration.tests import stage4_fixtures as fixture
from orchestration.intake.governed import qualify_replacement
from orchestration.runtime import CAO
from additional_cases import certify


class NativeOpening(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.base=fixture.intake_initial()

    def setUp(self):self.f=copy.deepcopy(self.base);self.e=self.f['session']

    def test_actual_current_owner_input_consumes_exact_prior_closing_version(self):
        prior=self.f['nodes']['timing-ENTITY-NL'];current=self.f['nodes']['timing-current-ENTITY-NL']
        source=self.e.sources[current.id];v=self.e.versions.current(current.id)
        self.assertEqual(current.selected_skill,'intercompany-accounting')
        self.assertEqual(v.payload()['calculations']['pairs'][0]['a_functional'],'30.00')
        self.assertEqual(source['pairs'][0]['opening_book_a'],'30.00')
        edge=self.e.edges[self.f['edges'][('timing-ENTITY-NL','timing-current-ENTITY-NL')]]
        self.assertEqual(edge.dependency_type,'OPENING')
        self.assertIn((edge.id,self.e.versions.current(prior.id).version_id),v.dependency_bindings)
        self.assertEqual(source['stage3_input_bindings'][0]['target_path'],['pairs',0,'opening_book_a'])
        self.assertNotEqual(prior.period_id,current.period_id)
        self.assertEqual(source['intercompany_transactions'][0]['period_id'],current.period_id)
        self.assertTrue(source['qualified_input_snapshot'])

    def test_prior_closing_correction_invalidates_native_opening_consumer(self):
        prior=self.f['nodes']['timing-ENTITY-NL'];current=self.f['nodes']['timing-current-ENTITY-NL']
        old=self.e.versions.current(prior.id);payload=old.payload()
        source=fixture.legal_source(self.f,'timing','ENTITY-NL')
        pair=source['pairs'][0]
        for field in ('opening_a','opening_b','opening_book_a','opening_book_b','book_a','book_b','gl_a','gl_b','confirmed_a','confirmed_b'):pair[field]='31'
        source['controls']['population_amount']='31'
        source['intercompany_transactions'][0].update(functional_amount='31.00',transaction_amount='31',source_id='reviewed-prior-correction')
        source=certify('intercompany-accounting',source)
        qualified=fixture.qualified_replacement(self.f,prior.id,source)
        plan=CAO().correct(self.f['case'],prior.id,qualified,'Separately reviewed prior closing correction')
        affected={self.e.graph.nodes[k].logical_id for k in plan['execution_order']}
        self.assertEqual(affected,{'timing-current-ENTITY-NL','timing-effective-ENTITY-NL','nl-opening','nl-comparative','match-timing','match-timing-current','group'})
        self.assertEqual(self.e.versions.state(self.e.versions.current(current.id,allow_stale=True).version_id),'STALE')
        self.assertEqual(old.payload(),payload)
        for label in ('clean-ENTITY-US','mismatch-ENTITY-UK','fx-ENTITY-US','translation','conversion'):
            self.assertIn(self.f['nodes'][label].id,plan['unaffected'])

    def test_equal_value_current_receipt_cannot_replace_opening_relationship(self):
        current=self.f['nodes']['timing-current-ENTITY-NL'];source=fixture.source(self.f,current.logical_id)
        source['stage3_input_bindings'][0]['dependency_id']=self.f['edges'][('clean-ENTITY-NL','conversion')]
        source=certify('intercompany-accounting',source)
        with self.assertRaises(ValueError):CAO().correct(self.f['case'],current.id,source,'Equal amount wrong opening lineage')

    def test_native_effective_interval_executes_and_enters_actual_group_dependency(self):
        node=self.f['nodes']['timing-effective-ENTITY-NL'];source=self.e.sources[node.id]
        self.assertEqual(source['governed_effective_interval']['included_period'],node.period_id)
        self.assertEqual(node.period,['2026-09-20','2026-09-30'])
        version=self.e.versions.current(node.id)
        self.assertEqual(version.payload()['calculations']['pairs'][0]['a_functional'],'30.00')
        edge=self.e.edges[self.f['edges'][('timing-ENTITY-NL',node.logical_id)]]
        self.assertEqual(edge.dependency_type,'PARTIAL_INCLUDED_PERIOD')
        self.assertTrue(version.dependency_bindings)
        group=self.e.versions.current(self.f['nodes']['group'].id)
        self.assertIn((self.f['edges'][(node.logical_id,'group')],version.version_id),group.dependency_bindings)
        self.assertEqual(version.payload()['journal_entry_implications'],[])

    def test_effective_interval_wrong_owner_scope_or_included_period_rejected(self):
        node=self.f['nodes']['timing-effective-ENTITY-NL']
        for field,value in [('owner','revenue-recognition'),('scope_id','ENTITY-UK'),('included_period',self.f['periods']['CALENDAR-SEP'].period_id)]:
            source=fixture.source(self.f,node.logical_id);source['governed_effective_interval'][field]=value
            source=certify('intercompany-accounting',source)
            with self.subTest(field=field),self.assertRaises(ValueError):CAO().correct(self.f['case'],node.id,source,'Wrong effective qualification')
