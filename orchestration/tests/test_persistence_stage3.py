"""Permanent real native/storage Company Memory authority attacks."""
import copy
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from orchestration.persistence import SQLiteStore,IntegrityError,RevisionConflict
from orchestration.persistence.memory import applicability,ident
from orchestration.persistence.codec import dumps,loads
from orchestration.persistence.store import sha,DDL_V2
from orchestration.tests.persistence_stage3_fixtures import *

class CompanyMemoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.path=Path(cls.tmp.name)/'template.db';cls.case=build(approval=True)
        with SQLiteStore(cls.path) as s:s.save(cls.case,COMPANY,[],0)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def setUp(self):
        self.local=tempfile.TemporaryDirectory();self.path=Path(self.local.name)/'test.db';shutil.copyfile(type(self).path,self.path)
        self.s=SQLiteStore(self.path);self.m=self.s.memory();self.c=self.s.load(COMPANY,self.case.id)[0];self.r=capture(self.s,self.c)
    def tearDown(self):self.s.close();self.local.cleanup()
    def promote(self,status='DOCUMENTED',kind='SYNTHETIC'):
        self.r=self.m.transition(COMPANY,self.r['record_id'],governance(self.r,status,kind),expected_revision=self.m.audit(COMPANY)['revision'],recorded_at=LEARNED);return self.r
    def query(self):return self.m.retrieve(COMPANY,self.c.id,self.c.id,'finance','systems')
    def bad_capture(self,**changes):
        with self.assertRaises(ValueError):capture(self.s,self.c,**changes)
    def bad_governance(self,**changes):
        g=governance(self.r,'APPROVED');g.update(changes)
        with self.assertRaises(ValueError):self.m.transition(COMPANY,self.r['record_id'],g,expected_revision=1,recorded_at=LEARNED)
    def test_proposed_restart_is_not_approved(self):
        self.s.close();self.s=SQLiteStore(self.path);self.m=self.s.memory();self.assertFalse(self.query()['qualified']);self.assertEqual(self.m.audit(COMPANY)['company_context'][0]['status'],'PROPOSED')
    def test_documentary_approval_requires_exact_source_envelope(self):
        r=self.promote('APPROVED','DOCUMENTARY');self.assertFalse(r['governance']['authenticated']);self.assertEqual(len(self.query()['qualified']),1)
    def test_unknown_company(self):
        with self.assertRaises(ValueError):self.m.retrieve('company:unknown',self.c.id,self.c.id,'finance','systems')
    def test_cross_company_record(self):
        with self.assertRaises(ValueError):self.m.transition('company:other',self.r['record_id'],governance(self.r),expected_revision=0,recorded_at=LEARNED)
    def test_same_display_name_distinct_company(self):
        self.s.save(self.c,'company:same-display',[],0);self.assertFalse(self.m.retrieve('company:same-display',self.c.id,self.c.id,'finance','systems')['qualified'])
    def test_missing_source(self):self.bad_capture(bundle_ids=[])
    def test_changed_sealed_payload(self):
        self.s.connection.execute("UPDATE checkpoints SET payload=payload||' ' WHERE revision=1")
        with self.assertRaises(ValueError):self.query()
    def test_wrong_reviewed_bundle(self):self.bad_capture(bundle_ids=['missing-bundle'])
    def test_no_explicit_intent(self):self.bad_governance(intent='MODEL_PROMOTION')
    def test_model_approval_claim(self):self.bad_governance(authority='MODEL_GENERATED')
    def test_synthetic_authentication(self):self.bad_governance(authenticated=True)
    def test_unreviewed_approval(self):self.bad_governance(bundle_ids=[])
    def test_inferred_assertion_cannot_be_relabelled(self):self.bad_capture(assertion='INFERRED')
    def test_conflicting_candidate_preserved_and_blocks(self):
        self.promote();other=build('Different close Case',value='Xero');self.s.save(other,COMPANY,[],0);r=capture(self.s,other)
        self.assertFalse(self.query()['qualified']);self.assertTrue(self.query()['conflicts'])
        with self.assertRaises(ValueError):self.m.transition(COMPANY,r['record_id'],governance(r),expected_revision=3,recorded_at=LEARNED)
        self.assertEqual(len(self.m.audit(COMPANY)['company_context']),2)
    def test_duplicate_current_approval(self):
        self.promote('APPROVED');other=build('Independent same policy');self.s.save(other,COMPANY,[],0);r=capture(self.s,other)
        with self.assertRaises(ValueError):self.m.transition(COMPANY,r['record_id'],governance(r,'APPROVED'),expected_revision=3,recorded_at=LEARNED)
    def test_duplicate_event_sql_identity(self):
        row=self.s.connection.execute('SELECT * FROM memory_events').fetchone()
        with self.assertRaises(sqlite3.IntegrityError):self.s.connection.execute('INSERT INTO memory_events VALUES(?,?,?,?,?,?)',row)
    def test_missing_historical_event(self):
        self.promote();self.s.connection.execute('PRAGMA foreign_keys=OFF');self.s.connection.execute('DELETE FROM memory_events WHERE sequence=1')
        with self.assertRaises(ValueError):self.m.audit(COMPANY)
    def test_deleted_memory_record(self):
        self.s.connection.execute('PRAGMA foreign_keys=OFF');self.s.connection.execute('DELETE FROM memory_events')
        with self.assertRaises(ValueError):self.query()
    def test_rewritten_immutable_lineage(self):
        self.promote();row=self.s.connection.execute('SELECT payload FROM memory_events WHERE sequence=2').fetchone();e=loads(row[0]);e['value']['source']['case_id']='another';e['value']['version_id']=ident('memory-version',{k:v for k,v in e['value'].items() if k!='version_id'});wire=dumps(e);checksum=sha(wire)
        self.s.connection.execute('UPDATE memory_events SET payload=?,sha256=?,event_id=? WHERE sequence=2',(wire,checksum,ident('memory-event',e)));self.s.connection.execute('UPDATE memory_heads SET sha256=?',(checksum,))
        with self.assertRaises(ValueError):self.m.audit(COMPANY)
    def test_superseded_result_refused(self):
        self.promote();correction(self.c)
        self.s.save(self.c,COMPANY,[],1);self.assertFalse(self.query()['qualified'])
    def test_retracted_record_refused(self):self.promote('RETRACTED');self.assertFalse(self.query()['qualified'])
    def test_old_retracted_record_cannot_reapprove(self):
        self.promote('RETRACTED')
        with self.assertRaises(ValueError):self.promote('APPROVED')
    def test_wrong_scope(self):
        d=copy.deepcopy(self.r['applicability']);d['scope_id']='other';self.bad_capture(dimensions=d)
    def test_wrong_period(self):
        d=copy.deepcopy(self.r['applicability']);d['period_ids']=['period:missing'];self.bad_capture(dimensions=d)
    def test_wrong_calendar(self):
        d=copy.deepcopy(self.r['applicability']);d['calendar_id']='other';self.bad_capture(dimensions=d)
    def test_wrong_framework(self):
        d=copy.deepcopy(self.r['applicability']);d['framework']='US_GAAP';self.bad_capture(dimensions=d)
    def test_wrong_currency(self):
        d=copy.deepcopy(self.r['applicability']);d['currency']='EUR';self.bad_capture(dimensions=d)
    def test_wrong_jurisdiction(self):
        d=copy.deepcopy(self.r['applicability']);d['jurisdiction']='US';self.bad_capture(dimensions=d)
    def test_invalid_effective_interval(self):self.bad_capture(effective_from=dict(value='2027-02-01',precision='exact'))
    def test_effective_is_not_learned(self):self.assertNotEqual(self.r['effective_from'],self.r['learned_at'])
    def test_unknown_date_not_fabricated(self):self.bad_capture(learned_at=dict(value='2026-12-01',precision='unknown'))
    def test_opening_comparative_substitution(self):
        d=copy.deepcopy(self.r['applicability']);d['relationship_id']='COMPARATIVE';self.bad_capture(dimensions=d)
    def test_equal_value_wrong_provenance(self):self.bad_capture(result_versions=['version:unknown'])
    def test_transient_fact_gate(self):self.bad_capture(material=False)
    def test_reusability_gate(self):self.bad_capture(reusable=False)
    def test_candidate_cannot_supply_native_inputs(self):
        with self.assertRaises(ValueError):self.m.consume_context(COMPANY,self.c.id,self.c.id,self.r['record_id'],self.r['version_id'],expected_revision=1,recorded_at=LEARNED)
    def test_native_owners_not_invoked(self):
        self.promote()
        from orchestration.runtime import CAO
        with patch.object(CAO,'execute_versioned_owner',side_effect=AssertionError('owner execution')):self.assertTrue(self.query()['qualified'])
    def test_memory_does_not_override_owner(self):
        from orchestration.runtime import CAO
        before=CAO().public(self.c);self.promote();self.query();self.assertEqual(before,CAO().public(self.c))
    def test_no_journal_action(self):
        self.promote()
        with patch('orchestration.scoped_journals.allocate_scoped',side_effect=AssertionError('posting')):self.query()
    def test_lost_ack_retry_same_event(self):
        g=governance(self.r);r=self.m.transition(COMPANY,self.r['record_id'],g,expected_revision=1,recorded_at=LEARNED);self.assertEqual(r,self.m.transition(COMPANY,self.r['record_id'],g,expected_revision=1,recorded_at=LEARNED));self.assertEqual(self.m.audit(COMPANY)['revision'],2)
    def test_competing_connections_stale_revision(self):
        with SQLiteStore(self.path) as other:
            self.promote()
            g=governance(self.r,'RETRACTED')
            with self.assertRaises(RevisionConflict):other.memory().transition(COMPANY,self.r['record_id'],g,expected_revision=1,recorded_at=LEARNED)
    def test_interrupted_publication_rolls_back(self):
        original=self.m._append
        def fail(*a,**k):original(*a,**k);raise RuntimeError('interrupted before COMMIT')
        with patch.object(self.m,'_append',side_effect=fail):
            with self.assertRaises(RuntimeError):self.promote()
        self.assertEqual(self.m.audit(COMPANY)['revision'],1);self.assertFalse(self.query()['qualified'])
    def test_exact_case_consumption_snapshot(self):
        self.promote();u=self.m.consume_context(COMPANY,self.c.id,self.c.id,self.r['record_id'],self.r['version_id'],expected_revision=2,recorded_at=LEARNED);self.assertEqual(u['case_revision'],1);self.assertEqual(u['use'],'CONTEXT_ONLY')
    def test_corrupt_memory_hash(self):
        self.s.connection.execute("UPDATE memory_events SET sha256='bad'")
        with self.assertRaises(ValueError):self.m.audit(COMPANY)
    def test_future_memory_contract(self):
        e=loads(self.s.connection.execute('SELECT payload FROM memory_events').fetchone()[0]);e['contract']=2;wire=dumps(e);checksum=sha(wire);self.s.connection.execute('UPDATE memory_events SET payload=?,sha256=?,event_id=?',(wire,checksum,ident('memory-event',e)));self.s.connection.execute('UPDATE memory_heads SET sha256=?',(checksum,))
        with self.assertRaises(ValueError):self.m.audit(COMPANY)
    def test_material_decision_requires_rationale(self):
        d=copy.deepcopy(self.r['decision']);d['reason']='';self.bad_capture(decision=d)
    def test_private_memory_excluded_public(self):
        from orchestration.runtime import CAO
        self.promote('APPROVED');wire=json.dumps(CAO().public(self.c))
        for item in ['memory-event:','TRUSTED_CALLER_ASSERTION','memory_governance','bundle_ids','synthetic governance']:self.assertNotIn(item,wire)
    def test_unknown_stored_type(self):self.bad_capture(uncertainty=lambda:None)
    def test_historical_context_separate(self):
        self.promote('RETRACTED');r=self.m.retrieve(COMPANY,self.c.id,self.c.id,'finance','systems',historical=True);self.assertEqual(r['qualified'][0]['qualification'],'HISTORICAL')
    def test_five_linked_projections(self):
        a=self.m.audit(COMPANY)
        for key in ['company_context','case_library','artifact_library','provenance','decision_register']:self.assertTrue(a[key])

    def test_nonoverlapping_historical_positions_not_conflict(self):
        # Both are actual sealed source/native Case candidates; exact dates are
        # explicit contextual applicability, not accounting result authority.
        a=capture(self.s,self.c,subject='consecutive-policy',effective_to=dict(value='2026-12-15',precision='exact'))
        self.m.transition(COMPANY,a['record_id'],governance(a),expected_revision=self.m.audit(COMPANY)['revision'],recorded_at=LEARNED)
        c=build('Successive December policy',value='Xero');self.s.save(c,COMPANY,[],0)
        b=capture(self.s,c,subject='consecutive-policy',effective_from=dict(value='2026-12-16',precision='exact'))
        self.m.transition(COMPANY,b['record_id'],governance(b),expected_revision=self.m.audit(COMPANY)['revision'],recorded_at=LEARNED)
        result=self.m.retrieve(COMPANY,self.c.id,self.c.id,'consecutive-policy','systems');self.assertFalse(result['conflicts'])
    def test_different_framework_positions_are_not_combined(self):
        self.promote()
        other=build('Different framework policy',value='Xero',framework='US_GAAP');self.s.save(other,COMPANY,[],0)
        r=capture(self.s,other);r=self.m.transition(COMPANY,r['record_id'],governance(r),expected_revision=self.m.audit(COMPANY)['revision'],recorded_at=LEARNED)
        a=self.query();b=self.m.retrieve(COMPANY,other.id,other.id,'finance','systems')
        self.assertFalse(a['conflicts']);self.assertFalse(b['conflicts'])
        self.assertEqual([v['record']['value'] for v in a['qualified']],['NetSuite']);self.assertEqual([v['record']['value'] for v in b['qualified']],['Xero'])
    def test_case_checkpoint_without_memory_publication_grants_no_authority(self):
        other=build('Case published before interrupted memory',value='Xero');self.s.save(other,COMPANY,[],0)
        original=self.m._append
        def fail(*a,**k):original(*a,**k);raise RuntimeError('memory publication interrupted')
        with patch.object(type(self.m),'_append',side_effect=fail),self.assertRaises(RuntimeError):capture(self.s,other,subject='orphan-policy')
        self.assertEqual(self.s.load(COMPANY,other.id)[0].id,other.id)
        self.assertEqual(self.m.retrieve(COMPANY,other.id,other.id,'orphan-policy','systems')['qualified'],[])
    def test_governed_decision_lifecycle(self):
        self.promote();r=self.r
        for status in ['documented','implemented','reversed']:
            decision=copy.deepcopy(r['decision']);decision['status']=status
            g=governance(r);g['target_status']=r['status'];g['prior_status']=r['status']
            r=self.m.decide(COMPANY,r['record_id'],decision,g,expected_revision=self.m.audit(COMPANY)['revision'],recorded_at=LEARNED)
        self.assertEqual(self.m.audit(COMPANY)['decision_register'][0]['decision']['status'],'reversed')
        self.assertEqual(len([e for e in self.m.history(COMPANY,r['record_id']) if e['kind']=='DECISION']),3)
    def test_decision_new_position_must_match_context(self):
        d=copy.deepcopy(self.r['decision']);d['new_position']='Invented alternative';self.bad_capture(decision=d)
    def test_candidate_cannot_approve_decision(self):
        d=copy.deepcopy(self.r['decision']);d['status']='approved';self.bad_capture(decision=d)
    def test_decision_language_is_only_an_unresolved_proposal(self):
        for phrase in ['we decided','going forward','from next month','we changed','instead of','management approved','audit asked','implemented']:
            with self.subTest(phrase=phrase):
                c=build('Decision signal '+phrase,value=phrase+' NetSuite');self.s.save(c,COMPANY,[],0)
                r=capture(self.s,c,subject='decision-signal:'+phrase,decision=None)
                self.assertEqual(r['status'],'PROPOSED');self.assertEqual(r['decision']['status'],'proposed');self.assertEqual(r['decision']['decision_date'],UNKNOWN)
                with self.assertRaises(IntegrityError):self.m.transition(COMPANY,r['record_id'],governance(r),expected_revision=self.m.audit(COMPANY)['revision'],recorded_at=LEARNED)
    def test_qualified_intake_context_suppresses_question(self):
        self.promote()
        b=build('Independent context-informed Case',memory=dict(memory=self.m,company_id=COMPANY,qualification_root=self.c.id,qualification_case=self.c.id,subjects=[('finance','systems')]))
        self.assertEqual(b.governance.context['systems'],'NetSuite');self.assertNotEqual(b.id,self.c.id)
    def test_partial_effective_period_does_not_reuse(self):
        r=capture(self.s,self.c,subject='partial-context',effective_from=dict(value='2026-12-15',precision='exact'))
        self.m.transition(COMPANY,r['record_id'],governance(r),expected_revision=self.m.audit(COMPANY)['revision'],recorded_at=LEARNED)
        result=self.m.retrieve(COMPANY,self.c.id,self.c.id,'partial-context','systems');self.assertFalse(result['qualified'])

class MemoryMigration(unittest.TestCase):
    def test_schema2_migration_retains_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'old.db';c=build()
            with SQLiteStore(p) as s:
                s.save(c,COMPANY,[],0);before=s.connection.execute('SELECT * FROM checkpoints').fetchall();s.connection.execute('DROP TABLE memory_heads');s.connection.execute('DROP TABLE memory_events');s.connection.execute('PRAGMA user_version=2')
            with SQLiteStore(p) as s:self.assertEqual(before,s.connection.execute('SELECT * FROM checkpoints').fetchall());self.assertEqual(s.connection.execute('PRAGMA user_version').fetchone()[0],3)
    def test_migration_failure_rolls_back(self):
        import orchestration.persistence.store as module
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'old.db';db=sqlite3.connect(p)
            for stmt in DDL_V2:db.execute(stmt)
            db.execute('PRAGMA user_version=2');db.commit();db.close()
            with patch.object(module,'MEMORY_DDL',module.MEMORY_DDL+('bad sql',)):
                with self.assertRaises(sqlite3.Error):SQLiteStore(p)
            db=sqlite3.connect(p);self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0],2);self.assertEqual(len(db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()),5);db.close()
    def test_repeated_initialization(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'db'
            for _ in range(2):
                with SQLiteStore(p) as s:self.assertEqual(s.connection.execute('PRAGMA user_version').fetchone()[0],3)

if __name__=='__main__':unittest.main()
