"""Fresh sealed correction/rework intake on the retained ordinary runtime."""
import copy
import unittest
from dataclasses import replace
from orchestration.tests import stage4_fixtures as fixture
from orchestration.intake.governed import qualify_replacement
from orchestration.runtime import CAO
from orchestration.governed_plan import observation


class ReplacementIntake(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.initial=fixture.intake_initial()

    def setUp(self):
        self.f=copy.deepcopy(self.initial)
        self.key=self.f['nodes']['mismatch-ENTITY-NL'].id
        self.source=fixture.legal_source(self.f,'mismatch','ENTITY-NL',True)
        self.engine,self.prepared,self.pack,self.raw=fixture.replacement_intake(self.f,self.key,self.source)

    def qualify(self):
        return qualify_replacement(self.engine,self.prepared,self.pack,self.f['case'],self.key)

    def source_change(self,change):
        change(self.pack.request['governed_plan']['sources'][self.key])
        self.pack.scoped_packs[0].request['source']=copy.deepcopy(self.pack.request['governed_plan']['sources'][self.key])

    def test_fresh_correction_qualifies_without_execution_or_original_mutation(self):
        e=self.f['session'];before=e.versions.record();old=copy.deepcopy(self.f['raw_sources'])
        source=self.qualify()
        self.assertEqual(e.versions.record(),before);self.assertEqual(self.f['raw_sources'],old)
        self.assertEqual(source['pairs'][0]['confirmed_a'],'10')
        original_ids={r.id for r in old}
        self.assertTrue(set(source['source_population']).isdisjoint(original_ids))
        self.assertTrue(self.prepared.lineage)

    def test_qualified_correction_publishes_new_result_and_preserves_original(self):
        e=self.f['session'];old=e.versions.current(self.key);payload=old.payload()
        plan=CAO().correct(self.f['case'],self.key,self.qualify(),'Fresh sealed correction')
        self.assertNotEqual(old.version_id,plan['new_version'])
        self.assertEqual(e.versions.state(old.version_id),'SUPERSEDED')
        self.assertEqual(old.payload(),payload)
        self.assertEqual(len(plan['execution_order']),6)

    def test_fresh_observation_rework_pack_qualifies_exact_replacement_receipts(self):
        plan=fixture.correct(self.f);key=self.f['nodes']['match-mismatch'].id
        source=fixture.matching_source(self.f,'mismatch')
        engine,prepared,pack,_=fixture.replacement_intake(self.f,key,source)
        qualified=qualify_replacement(engine,prepared,pack,self.f['case'],key)
        self.f['session'].execute(key,observation,qualified,'Dependency rework: '+plan['new_version'])
        self.assertEqual(self.f['session'].versions.current(key).payload()['matching']['classification'],'MATCHED')

    def test_rework_snapshot_cannot_seal_obsolete_receipts(self):
        key=self.f['nodes']['match-mismatch'].id;source=fixture.matching_source(self.f,'mismatch')
        engine,prepared,pack,_=fixture.replacement_intake(self.f,key,source)
        fixture.correct(self.f)
        with self.assertRaises(ValueError):qualify_replacement(engine,prepared,pack,self.f['case'],key)

    def test_changed_source_bytes_rejected(self):
        original=self.prepared._inventory.raw[self.raw[0].id]
        self.prepared._inventory.raw[original.id]=replace(original,payload=original.payload+'tampered')
        with self.assertRaises(ValueError):self.qualify()

    def test_changed_prepared_candidates_rejected(self):
        self.prepared.candidates[0]['claim']['value']='11'
        with self.assertRaises(ValueError):self.qualify()

    def test_hidden_complete_population_change_rejected(self):
        self.source_change(lambda c:c['pairs'][0].update(opening_book_b='12'))
        with self.assertRaises(ValueError):self.qualify()

    def test_snapshot_omitted_from_manifest_rejected(self):
        def change(c):
            snapshot=c['qualified_input_snapshot']['source_id'];c['source_population'].remove(snapshot)
            c['qualified_scope_sources']=[row for row in c['qualified_scope_sources'] if row['source_id']!=snapshot]
        self.source_change(change)
        with self.assertRaises(ValueError):self.qualify()

    def test_wrong_reviewed_scope_rejected(self):
        self.pack.scoped_packs[0].scope_id='ENTITY-UK'
        with self.assertRaises(ValueError):self.qualify()

    def test_wrong_reviewed_period_rejected(self):
        self.pack.scoped_packs[0].period_id=self.f['periods']['CALENDAR-SEP'].period_id
        with self.assertRaises(ValueError):self.qualify()

    def test_wrong_calendar_rejected(self):
        self.pack.scoped_packs[0].calendar_id='US-FISCAL'
        with self.assertRaises(ValueError):self.qualify()

    def test_sibling_case_substitution_rejected(self):
        self.pack.request['governed_plan']['root_case']=self.f['containers']['ENTITY-UK-OCT'].id
        with self.assertRaises(ValueError):self.qualify()

    def test_case_objective_rewrite_rejected(self):
        self.pack.request['governed_plan']['cases'][0]['objective']='Different objective'
        with self.assertRaises(ValueError):self.qualify()

    def test_node_identity_rewrite_rejected(self):
        self.pack.request['governed_plan']['nodes'][0]['economic_id']='unrelated'
        with self.assertRaises(ValueError):self.qualify()

    def test_dependency_contract_addition_rejected(self):
        self.pack.request['governed_plan']['dependencies'].append(copy.deepcopy(next(iter(self.f['session'].edges.values())).__dict__))
        with self.assertRaises(ValueError):self.qualify()

    def test_observation_snapshot_mutation_rejected(self):
        fixture.correct(self.f);key=self.f['nodes']['match-mismatch'].id
        engine,prepared,pack,_=fixture.replacement_intake(self.f,key,fixture.matching_source(self.f,'mismatch'))
        source=pack.request['governed_plan']['sources'][key];source['decision']['reason']='Invented replacement reason'
        pack.scoped_packs[0].request['source']=copy.deepcopy(source)
        with self.assertRaises(ValueError):qualify_replacement(engine,prepared,pack,self.f['case'],key)
