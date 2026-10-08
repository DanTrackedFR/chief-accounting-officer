"""Durable lifecycle attacks at actual SQLite/native qualification boundaries."""
import copy
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from orchestration.persistence import SQLiteStore, snapshot, restore, IntegrityError, RevisionConflict
from orchestration.persistence.recovery import RecoveryBlocked
from orchestration.persistence.store import DDL_V1, sha
from orchestration.persistence.codec import dumps
from orchestration.tests.persistence_stage2_fixtures import baseline, correction_intent, rework_intent, journal_intent, reopening, COMPANY, CONTEXT
from orchestration.runtime import CAO


class DurableLifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.template=Path(cls.tmp.name)/'template.db'
        f=baseline();cls.doc=snapshot(f['case'],COMPANY,CONTEXT);cls.case_id=f['case'].id
        with SQLiteStore(cls.template) as s:s.save(f['case'],COMPANY,CONTEXT,0)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def setUp(self):
        self.tmpcase=tempfile.TemporaryDirectory();self.path=Path(self.tmpcase.name)/'state.db'
        src=sqlite3.connect(self.template);dest=sqlite3.connect(self.path);src.backup(dest);src.close();dest.close()
        self.store=SQLiteStore(self.path);self.case,self.rev,self.ctx=self.store.load(COMPANY,self.case_id)
    def tearDown(self):self.store.close();self.tmpcase.cleanup()
    def prepared(self):
        i=correction_intent(self.case);key=self.store.prepare(self.case,COMPANY,self.ctx,self.rev,i)
        return key,i
    def corrected(self):
        key,_=self.prepared();c,r=self.store.recover(COMPANY,self.case_id,key)
        return c,r,r['events'][-1]['value']['result']
    def tampered_load(self, change):
        # Deliberately update only raw payload (not hashes); actual store must
        # reject corruption before runtime authority can be consulted.
        self.store.connection.execute("UPDATE checkpoints SET payload=? WHERE revision=1",(dumps(change(copy.deepcopy(self.doc))),))
        with self.assertRaises(IntegrityError):self.store.load(COMPANY,self.case_id)
    def native_attack(self, change):
        doc=copy.deepcopy(self.doc);change(doc)
        with self.assertRaises(IntegrityError):restore(doc,COMPANY,self.case_id)
    def test_prepare_exact_semantics_and_retry(self):
        key,i=self.prepared();again=self.store.prepare(self.case,COMPANY,self.ctx,1,i)
        self.assertEqual(key,again);self.assertEqual(self.store.load(COMPANY,self.case_id)[1],2)
        self.assertEqual(self.store.operation(COMPANY,self.case_id,key)['status'],'PREPARED')
    def test_failure_before_preparation_keeps_baseline(self):
        i=correction_intent(self.case);i['source']['qualified_input_snapshot']['fingerprint']='wrong'
        with self.assertRaises(IntegrityError):self.store.prepare(self.case,COMPANY,self.ctx,1,i)
        self.assertEqual(self.store.load(COMPANY,self.case_id)[1],1)
    def test_preparation_transaction_rolls_back(self):
        i=correction_intent(self.case)
        with patch('orchestration.persistence.recovery._phase',side_effect=OSError('interrupt')):
            with self.assertRaises(OSError):self.store.prepare(self.case,COMPANY,self.ctx,1,i)
        self.assertEqual(self.store.load(COMPANY,self.case_id)[1],1)
        self.assertEqual(self.store.connection.execute('SELECT count(*) FROM operations').fetchone()[0],0)
    def test_after_preparation_can_recover(self):
        key,_=self.prepared();c,r=self.store.recover(COMPANY,self.case_id,key)
        self.assertEqual(r['status'],'COMMITTED');self.assertEqual(c.status,'IN_PROGRESS')
    def test_failure_during_owner_replays_from_prepared(self):
        key,_=self.prepared()
        with patch.object(CAO,'execute_versioned_owner',side_effect=RuntimeError('death')):
            with self.assertRaises(RuntimeError):self.store.recover(COMPANY,self.case_id,key)
        self.assertEqual(self.store.operation(COMPANY,self.case_id,key)['status'],'EXECUTING')
        c,r=self.store.recover(COMPANY,self.case_id,key);self.assertEqual(r['status'],'COMMITTED')
    def test_after_native_before_checkpoint_discards_partial_state(self):
        key,_=self.prepared()
        def fault(name,*args):
            if name=='after_native':raise RuntimeError('death')
        with patch('orchestration.persistence.recovery._phase',side_effect=fault):
            with self.assertRaises(RuntimeError):self.store.recover(COMPANY,self.case_id,key)
        c,rev,_=self.store.load(COMPANY,self.case_id);self.assertEqual(rev,2);self.assertEqual(c.governance.versions.active,self.doc['active'])
        c,r=self.store.recover(COMPANY,self.case_id,key);self.assertEqual(r['status'],'COMMITTED')
    def test_failure_while_invalidating_is_not_committed(self):
        from orchestration.versions import VersionedExecution
        key,_=self.prepared();original=VersionedExecution.invalidate
        def partial(session,*args):original(session,*args);raise RuntimeError('after invalidation')
        with patch.object(VersionedExecution,'invalidate',partial):
            with self.assertRaises(RuntimeError):self.store.recover(COMPANY,self.case_id,key)
        self.assertEqual(self.store.load(COMPANY,self.case_id)[0].governance.versions.active,self.doc['active'])
        self.assertEqual(self.store.recover(COMPANY,self.case_id,key)[1]['status'],'COMMITTED')
    def test_actual_sqlite_outcome_transaction_failure(self):
        key,_=self.prepared()
        self.store.connection.execute("CREATE TEMP TRIGGER fail_commit BEFORE INSERT ON operation_events WHEN NEW.status='COMMITTED' BEGIN SELECT RAISE(ABORT,'fault'); END")
        with self.assertRaises(ValueError):self.store.recover(COMPANY,self.case_id,key)
        self.assertEqual(self.store.load(COMPANY,self.case_id)[1],2)
        self.store.connection.execute('DROP TRIGGER fail_commit')
        self.assertEqual(self.store.recover(COMPANY,self.case_id,key)[1]['status'],'COMMITTED')
    def test_lost_ack_does_not_publish_again(self):
        key,_=self.prepared()
        def fault(name,*args):
            if name=='after_commit':raise RuntimeError('lost acknowledgement')
        with patch('orchestration.persistence.recovery._phase',side_effect=fault):
            with self.assertRaises(RuntimeError):self.store.recover(COMPANY,self.case_id,key)
        before=self.store.load(COMPANY,self.case_id)[0]
        with patch.object(CAO,'execute_versioned_owner',side_effect=AssertionError('duplicate')):c,r=self.store.recover(COMPANY,self.case_id,key)
        self.assertEqual(r['head_revision'],3);self.assertEqual(snapshot(c,COMPANY,CONTEXT),snapshot(before,COMPANY,CONTEXT))
    def test_pending_operation_blocks_uncoordinated_writer(self):
        key,_=self.prepared();c,rev,ctx=self.store.load(COMPANY,self.case_id)
        with self.assertRaises(RecoveryBlocked):self.store.save(c,COMPANY,ctx,rev)
    def test_separate_connection_obsolete_writer(self):
        with SQLiteStore(self.path) as second:
            c,rev,ctx=second.load(COMPANY,self.case_id);key,_=self.prepared();self.store.recover(COMPANY,self.case_id,key)
            with self.assertRaises(RevisionConflict):second.save(c,COMPANY,ctx,rev)
    def test_wrong_company_operation_refused(self):
        key,_=self.prepared()
        with self.assertRaises(IntegrityError):self.store.recover('company:other',self.case_id,key)
    def test_wrong_root_case_operation_refused(self):
        key,_=self.prepared()
        with self.assertRaises(IntegrityError):self.store.recover(COMPANY,'case:wrong',key)
    def test_missing_actual_sealed_correction_evidence(self):
        i=correction_intent(self.case);self.case.governance.evidence_bundles={}
        with self.assertRaises(IntegrityError):self.store.prepare(self.case,COMPANY,self.ctx,1,i)
    def test_changed_reviewed_pack_refused(self):
        i=correction_intent(self.case);b=next(iter(self.case.governance.evidence_bundles.values()));b['pack']['scope_id']='wrong'
        with self.assertRaises(IntegrityError):self.store.prepare(self.case,COMPANY,self.ctx,1,i)
    def test_preview_only_rework_evidence_refused(self):
        c,r,p=self.corrected();preview=copy.deepcopy(c);i=rework_intent(preview,p)
        with self.assertRaises(IntegrityError):self.store.prepare(c,COMPANY,self.ctx,r['head_revision'],i)
    def test_prepare_cannot_smuggle_uncommitted_accounting(self):
        i=correction_intent(self.case);CAO().correct(self.case,i['node_id'],i['source'],i['reason'])
        with self.assertRaises(IntegrityError):self.store.prepare(self.case,COMPANY,self.ctx,1,i)
    def test_no_false_closure_after_correction_or_interrupt(self):
        c,r,p=self.corrected();self.assertNotEqual(c.status,'CLOSED');self.assertNotEqual(CAO().public(c)['status'],'complete')
        i=rework_intent(c,p);key=self.store.prepare(c,COMPANY,self.ctx,r['head_revision'],i)
        def fault(name,*args):
            if name=='after_native':raise RuntimeError('death')
        with patch('orchestration.persistence.recovery._phase',side_effect=fault):
            with self.assertRaises(RuntimeError):self.store.recover(COMPANY,self.case_id,key)
        c,_,_=self.store.load(COMPANY,self.case_id);self.assertNotEqual(c.status,'CLOSED')
    def test_native_rework_exact_order_and_unaffected_versions(self):
        c,r,p=self.corrected();i=rework_intent(c,p);key=self.store.prepare(c,COMPANY,self.ctx,r['head_revision'],i);c,r=self.store.recover(COMPANY,self.case_id,key)
        self.assertEqual([row['node'] for row in r['events'][-1]['value']['result']],p['execution_order'])
        self.assertEqual(c.status,'CLOSED');self.assertEqual(CAO().public(c)['status'],'complete')
        for n in p['unaffected']:self.assertEqual(c.governance.versions.active[n],self.doc['active'][n])
    def test_wrong_rework_order_refused(self):
        c,r,p=self.corrected();i=rework_intent(c,p);i['plan']['execution_order'].reverse()
        with self.assertRaises(IntegrityError):self.store.prepare(c,COMPANY,self.ctx,r['head_revision'],i)
    def test_closed_period_without_authorization_refused(self):
        i=correction_intent(self.case);n=self.case.governance.graph.nodes[i['node_id']]
        key=self.store.prepare(self.case,COMPANY,self.ctx,1,dict(kind='CLOSE_PERIOD',period_id=n.period_id));c,r=self.store.recover(COMPANY,self.case_id,key)
        with self.assertRaises(ValueError):self.store.prepare(c,COMPANY,self.ctx,r['head_revision'],correction_intent(c))
    def test_reopening_exact_authorization_survives_restart(self):
        n=next(n for n in self.case.graph.nodes.values() if n.logical_id=='adjacent-closing');period=n.period_id
        key=self.store.prepare(self.case,COMPANY,self.ctx,1,dict(kind='CLOSE_PERIOD',period_id=period));c,r=self.store.recover(COMPANY,self.case_id,key)
        key=self.store.prepare(c,COMPANY,self.ctx,r['head_revision'],reopening(c,period));c,r=self.store.recover(COMPANY,self.case_id,key)
        with SQLiteStore(self.path) as fresh:c,rev,ctx=fresh.load(COMPANY,self.case_id)
        key=self.store.prepare(c,COMPANY,ctx,rev,correction_intent(c));c,r=self.store.recover(COMPANY,self.case_id,key)
        self.assertEqual(c.governance.periods.status[period],'REOPENED');self.assertEqual(c.status,'IN_PROGRESS')
    def test_stale_case_cannot_reclose_period(self):
        c,r,p=self.corrected();key=self.store.prepare(c,COMPANY,self.ctx,r['head_revision'],dict(kind='CLOSE_PERIOD',period_id=c.period_id))
        with self.assertRaises(RecoveryBlocked):self.store.recover(COMPANY,self.case_id,key)
        self.assertEqual(self.store.operation(COMPANY,self.case_id,key)['status'],'BLOCKED')
    def test_same_value_superseded_receipts_remain_historical(self):
        c,r,p=self.corrected();e=c.governance
        stale=[x for x in e.receipts if e.versions.state(x['result_version'])!='CURRENT'];self.assertTrue(stale)
        for receipt in stale:
            with self.assertRaises(ValueError):e.validate_receipt(receipt,receipt['consumer_node'])
    def test_journal_selection_repeated_without_duplicate(self):
        key=self.store.prepare(self.case,COMPANY,self.ctx,1,journal_intent(self.case));c,r=self.store.recover(COMPANY,self.case_id,key)
        self.assertEqual(len(r['events'][-1]['value']['result']['selected']),8)
        with patch('orchestration.scoped_journals.allocate_scoped',side_effect=AssertionError('reallocated')):after,again=self.store.recover(COMPANY,self.case_id,key)
        self.assertEqual(r,again);self.assertEqual(snapshot(c,COMPANY,CONTEXT),snapshot(after,COMPANY,CONTEXT))
    def test_duplicate_legal_selection_native_refusal(self):
        i=journal_intent(self.case);legal=next(ev for ev in i['events'] if ev['posting_scope']=='ENTITY-NL');i['events'].append(copy.deepcopy(legal))
        with self.assertRaises(ValueError):self.store.prepare(self.case,COMPANY,self.ctx,1,i)
    def test_duplicate_group_elimination_native_refusal(self):
        i=journal_intent(self.case);group=next(ev for ev in i['events'] if ev['posting_scope']=='GROUP-EUR');i['events'].append(copy.deepcopy(group))
        with self.assertRaises(ValueError):self.store.prepare(self.case,COMPANY,self.ctx,1,i)
    def test_legal_group_layer_substitution_refused(self):
        i=journal_intent(self.case);i['events'][0]['posting_scope']='GROUP-EUR'
        with self.assertRaises(ValueError):self.store.prepare(self.case,COMPANY,self.ctx,1,i)
    def test_stale_dependency_cannot_select_journals(self):
        c,r,p=self.corrected()
        with self.assertRaises(ValueError):journal_intent(c)
    def test_uncertain_external_outcome_fails_closed(self):
        key=self.store.prepare(self.case,COMPANY,self.ctx,1,journal_intent(self.case));c,r=self.store.recover(COMPANY,self.case_id,key)
        uncertain=self.store.prepare(c,COMPANY,self.ctx,r['head_revision'],dict(kind='UNCERTAIN_EXTERNAL',selection_operation=key,evidence=['External system may have received this population; acknowledgement absent']))
        with self.assertRaises(RecoveryBlocked):self.store.recover(COMPANY,self.case_id,uncertain)
        self.assertEqual(self.store.operation(COMPANY,self.case_id,uncertain)['status'],'UNCERTAIN')
        with self.assertRaises(RecoveryBlocked):self.store.abandon(COMPANY,self.case_id,uncertain,'repost')
        with self.assertRaises(RecoveryBlocked):self.store.save(c,COMPANY,self.ctx,4)
    def test_duplicate_transition_refused(self):
        key,_=self.prepared();wire=dumps({})
        self.store.connection.execute('INSERT INTO operation_events VALUES(?,?,?,?,?)',(key,1,'PREPARED',wire,sha(wire)))
        with self.assertRaises(IntegrityError):self.store.recover(COMPANY,self.case_id,key)
    def test_operation_payload_corruption_refused(self):
        key,_=self.prepared();self.store.connection.execute("UPDATE operations SET payload='{}'")
        with self.assertRaises(IntegrityError):self.store.recover(COMPANY,self.case_id,key)
    def test_missing_dependency_receipt_refused(self):self.native_attack(lambda d:d.update(receipts=d['receipts'][1:]))
    def test_missing_rework_history_refused(self):self.native_attack(lambda d:d.update(rework_history=[]))
    def test_corrupt_dependency_graph_refused(self):self.native_attack(lambda d:d['nodes'][0]['dependencies'].append('missing'))
    def test_rewritten_immutable_source_refused(self):self.native_attack(lambda d:next(iter(d['source_snapshots'].values())).update(evidence=['rewritten']))
    def test_opening_comparative_substitution_refused(self):
        def change(d):
            edge=next(e for e in d['dependencies'].values() if e['dependency_type']=='OPENING');edge['dependency_type']='COMPARATIVE'
        self.native_attack(change)
    def test_wrong_receipt_dimensions_and_version_refused(self):
        for field in ('producer_scope','consumer_scope','producer_period','consumer_period','producer_framework','consumer_framework','value_currency','result_version'):
            with self.subTest(field=field):self.native_attack(lambda d:d['receipts'][0].update({field:'wrong'}))
    def test_public_output_never_leaks_operation_intents(self):
        c,r,p=self.corrected()
        from interfaces.public_output import ROUTES
        for route in ROUTES:
            public=json.dumps(CAO().public(c,route))
            for token in ('operation:','version:','dependency:','source_fingerprint','reviewer_signoff','evidence_bundles','journal_entry_implications'):self.assertNotIn(token,public)
    def test_abandon_pure_uncommitted_operation_is_explicit(self):
        key,_=self.prepared();self.store.abandon(COMPANY,self.case_id,key,'Reviewed source withdrawn; no native outcome committed')
        with self.assertRaises(RecoveryBlocked):self.store.recover(COMPANY,self.case_id,key)
        c,rev,ctx=self.store.load(COMPANY,self.case_id);self.assertEqual(self.store.save(c,COMPANY,ctx,rev),3)


class SchemaMigrationTests(unittest.TestCase):
    def test_schema1_migration_preserves_original_bytes(self):
        with tempfile.TemporaryDirectory() as p:
            path=Path(p)/'v1.db';f=baseline()
            with SQLiteStore(path) as s:s.save(f['case'],COMPANY,CONTEXT,0);before=s.connection.execute('SELECT * FROM checkpoints').fetchall();s.connection.execute('DROP TABLE operation_events');s.connection.execute('DROP TABLE operations');s.connection.execute('PRAGMA user_version=1')
            with SQLiteStore(path) as s:
                self.assertEqual(s.connection.execute('PRAGMA user_version').fetchone()[0],2);self.assertEqual(before,s.connection.execute('SELECT * FROM checkpoints').fetchall());self.assertEqual(s.load(COMPANY,f['case'].id)[1],1)
    def test_migration_failure_rolls_back(self):
        import orchestration.persistence.store as module
        with tempfile.TemporaryDirectory() as p:
            path=Path(p)/'v1.db';db=sqlite3.connect(path)
            for statement in DDL_V1:db.execute(statement)
            db.execute('PRAGMA user_version=1');db.commit();db.close()
            with patch.object(module,'OPERATION_DDL',module.OPERATION_DDL+('invalid sql',)):
                with self.assertRaises(sqlite3.Error):SQLiteStore(path)
            db=sqlite3.connect(path);self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0],1);self.assertEqual(len(db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()),3);db.close()
    def test_mixed_schema1_rejected(self):
        with tempfile.TemporaryDirectory() as p:
            path=Path(p)/'mixed.db';db=sqlite3.connect(path)
            for statement in DDL_V1:db.execute(statement)
            db.execute('CREATE TABLE operations(value TEXT)');db.execute('PRAGMA user_version=1');db.commit();db.close()
            with self.assertRaises(IntegrityError):SQLiteStore(path)

if __name__=='__main__':unittest.main()
