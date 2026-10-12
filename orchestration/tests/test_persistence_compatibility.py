"""Bounded compatibility probes against existing accepted Stage4, not a new flagship."""
import copy
import json
import tempfile
import unittest
from unittest.mock import patch
from orchestration.tests import stage4_temporal_fixtures as t, stage4_closing_population as whole
from orchestration.persistence import snapshot, restore, SQLiteStore, IntegrityError
from orchestration.persistence.evidence import retain
from orchestration.persistence.codec import dumps
from orchestration.runtime import CAO
from orchestration.tests.persistence_fixtures import COMPANY, CONTEXT


class Stage4CheckpointCompatibility(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f,cls.record=t.run();cls.case=cls.f['case']
        # Existing Stage4 assembles reviewed rework in preview contexts. Retain
        # that same evidence in the committed session; never rebuild approvals.
        for row in cls.f['replacement_intakes']:retain(cls.case.governance,row['prepared'],row['reviewed_pack'])
        cls.doc=snapshot(cls.case,COMPANY,CONTEXT)

    def restored(self):return restore(copy.deepcopy(self.doc),COMPANY,self.case.id)
    def attack(self,fn):
        d=copy.deepcopy(self.doc);fn(d)
        with self.assertRaises(IntegrityError):restore(d,COMPANY,self.case.id)

    def test_accepted_stage4_roundtrip(self):
        c=self.restored();self.assertEqual((c.status,c.outcome),('CLOSED','complete'))
        self.assertEqual(dumps(snapshot(c,COMPANY,CONTEXT)),dumps(self.doc))
        self.assertEqual(CAO().public(c),CAO().public(self.case))
    def test_exact_once_group_and_legal_inventory(self):
        c=self.restored();f=dict(self.f,case=c,session=c.governance)
        before=whole.exact_once(self.f);after=whole.exact_once(f)
        self.assertEqual(before,after);self.assertEqual(len(after['selected']),8)
    def test_no_accounting_execution_or_release_during_restore(self):
        with patch.object(CAO,'run',side_effect=AssertionError('rerun')),patch.object(CAO,'execute_versioned_owner',side_effect=AssertionError('owner')),patch('orchestration.scoped_journals.allocate_scoped',side_effect=AssertionError('journal release')):
            self.restored()
    def test_missing_sealed_evidence_rejected(self):
        self.attack(lambda d:d['session'].update(evidence_bundles={}))
    def test_wrong_reviewed_pack(self):
        def mutate(d):
            b=next(iter(d['session']['evidence_bundles'].values()));b['pack']['scoped_packs'][0]['request']['source']['evidence']=['changed review']
        self.attack(mutate)
    def test_unreviewed_evidence_cannot_be_restored_as_reviewed(self):
        def mutate(d):
            b=next(iter(d['session']['evidence_bundles'].values()));b['fields']['validation']['accepted']=False
        self.attack(mutate)
    def test_changed_raw_source_old_fingerprint(self):
        def mutate(d):
            b=next(iter(d['session']['evidence_bundles'].values()));raw=json.loads(b['raw_sources'][0]);raw['payload']=[dict(record_id='tampered',amount='0')];b['raw_sources'][0]=json.dumps(raw)
        self.attack(mutate)
    def test_duplicate_group_elimination_rejected(self):
        def mutate(d):
            n=next(n for n in d['nodes'] if n['selected_skill']=='consolidation');n['result']['journal_entry_implications']*=2
        self.attack(mutate)
    def test_superseded_legal_journal_not_current(self):
        c=self.restored();e=c.governance
        old=[v for k,v in e.versions.versions.items() if e.versions.states[k]=='SUPERSEDED']
        self.assertTrue(old)
        for v in old:
            with self.assertRaises(ValueError):e.versions.require_current(v.version_id)
    def test_opening_and_comparative_stay_distinct(self):
        e=self.restored().governance
        kinds={edge.dependency_type for edge in e.edges.values()}
        self.assertTrue({'OPENING','COMPARATIVE'}<=kinds)
        self.assertEqual(e.periods.record(),self.case.governance.periods.record())
    def test_restore_source_population_exact(self):
        e=self.restored().governance
        self.assertEqual(e.evidence_bundles,self.case.governance.evidence_bundles)
        self.assertEqual(e.versions.source_snapshots,self.case.governance.versions.source_snapshots)
    def test_current_private_public_boundary(self):
        from interfaces.public_output import ROUTES
        c=self.restored()
        for route in ROUTES:
            public=json.dumps(CAO().public(c,route))
            for token in ('version:','dependency:','source_fingerprint','reviewer_signoff','evidence_tier','routing_metadata','governance_history'):
                self.assertNotIn(token,public)
    def test_fresh_store_reconstructs_native_stage4(self):
        with tempfile.TemporaryDirectory() as p:
            with SQLiteStore(p+'/state.db') as store:store.save(self.case,COMPANY,CONTEXT,0)
            with SQLiteStore(p+'/state.db') as store:c,rev,ctx=store.load(COMPANY,self.case.id)
            self.assertEqual(rev,1);self.assertEqual(dumps(snapshot(c,COMPANY,ctx)),dumps(self.doc))

if __name__=='__main__':unittest.main()
