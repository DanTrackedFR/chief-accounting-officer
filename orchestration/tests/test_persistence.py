"""Permanent durable-state, transaction and dimensional attacks."""
import copy
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
from orchestration.tests.persistence_fixtures import proof, COMPANY, CONTEXT, journal_population
from orchestration.persistence import SQLiteStore, snapshot, restore, IntegrityError, RevisionConflict
from orchestration.persistence.codec import dumps, loads
from orchestration.persistence.store import objects, sha
from orchestration.runtime import CAO


class NativeRestart(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.f = proof(); cls.doc = snapshot(cls.f['case'], COMPANY, CONTEXT)

    def restored(self): return restore(copy.deepcopy(self.doc), COMPANY, self.doc['root_case'])

    def test_independent_process_restart(self):
        with tempfile.TemporaryDirectory() as directory:
            path = str(Path(directory)/'checkpoint.db'); original = self.f['case']
            before = dumps(self.doc)
            with SQLiteStore(path) as store: self.assertEqual(store.save(original, COMPANY, CONTEXT, 0), 1)
            script = '''
import sys
from unittest.mock import patch
from orchestration.persistence import SQLiteStore,snapshot
from orchestration.persistence.codec import dumps
from orchestration.runtime import CAO
with patch.object(CAO,'execute_versioned_owner',side_effect=AssertionError('owner reexecuted')), patch.object(CAO,'run',side_effect=AssertionError('case rerun')):
 with SQLiteStore(sys.argv[1]) as store:
  root,revision,context=store.load(sys.argv[2],sys.argv[3])
  assert revision==1
  print(dumps(snapshot(root,sys.argv[2],context)))
'''
            result = subprocess.run([sys.executable, '-c', script, path, COMPANY, original.id], check=True, capture_output=True, text=True)
            self.assertEqual(result.stdout.strip(), before)

    def test_repeat_restore_exact_identities(self):
        a=self.restored(); b=restore(snapshot(a,COMPANY,CONTEXT),COMPANY,a.id)
        self.assertIsNot(a,b);self.assertIsNot(a.governance,b.governance)
        self.assertEqual(dumps(snapshot(b,COMPANY,CONTEXT)),dumps(self.doc))

    def test_partial_and_closed_cases_retained(self):
        root=self.restored();self.assertEqual((root.status,root.outcome),('IN_PROGRESS','partial'))
        self.assertTrue(any(c.status=='CLOSED' and c.outcome=='complete' for c in root.governance.cases.cases.values()))

    def test_restore_has_no_journal_side_effect(self):
        with patch('orchestration.scoped_journals.allocate_scoped',side_effect=AssertionError('journal release during restoration')):
            root=self.restored()
        self.assertEqual(journal_population(root),journal_population(self.f['case']))
        self.assertTrue(journal_population(root))

    def test_historical_stale_superseded_receipts_rejected(self):
        e=self.restored().governance
        historical=[r for r in e.receipts if e.versions.states[r['result_version']]!='CURRENT']
        self.assertTrue(historical)
        for r in historical:
            with self.assertRaises(ValueError):e.validate_receipt(r,r['consumer_node'])

    def test_all_public_routes_keep_private_state(self):
        from interfaces.public_output import ROUTES
        c=self.restored()
        for route in ROUTES:
            answer=json.dumps(CAO().public(c,route))
            for token in ('version:', 'exec:', 'dependency:', 'source_fingerprint', 'reviewer', 'evidence_tier', 'routing_metadata', 'governance_history'):
                self.assertNotIn(token,answer)

    def test_iteration_order_independent(self):
        doc=copy.deepcopy(self.doc)
        for name in ('cases','nodes','scopes'):doc[name].reverse()
        for name in ('versions','states','active','dependencies','source_snapshots','supersession'):
            doc[name]=dict(reversed(list(doc[name].items())))
        c=restore(doc,COMPANY,doc['root_case'])
        self.assertEqual(dumps(snapshot(c,COMPANY,CONTEXT)),dumps(self.doc))

    def test_complete_checkpoint_restores_closed(self):
        f=proof(False);d=snapshot(f['case'],COMPANY,CONTEXT);c=restore(d,COMPANY,d['root_case'])
        self.assertEqual((c.status,c.outcome),('CLOSED','complete'))


class DurableAttacks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.doc=snapshot(proof()['case'],COMPANY,CONTEXT)
    def setUp(self):self.d=copy.deepcopy(self.doc)
    def reject(self):
        with self.assertRaises(IntegrityError):restore(self.d,COMPANY,self.doc['root_case'])
    def node(self):return self.d['nodes'][0]
    def case(self):return next(c for c in self.d['cases'] if c['id']==self.d['root_case'])
    def receipt(self):return self.d['receipts'][0]
    def version(self):return self.d['versions'][next(iter(self.d['versions']))]
    def test_wrong_company(self):self.d['company_id']='company:other';self.reject()
    def test_wrong_scope(self):self.node()['scope_id']='UNKNOWN-SCOPE';self.reject()
    def test_wrong_case(self):self.node()['case_id']=self.d['root_case'];self.reject()
    def test_wrong_period(self):self.node()['period_id']=self.d['periods']['periods'][0]['period_id'];self.reject()
    def test_wrong_calendar(self):self.d['periods']['periods'][0]['calendar_id']='US-FISCAL';self.reject()
    def test_wrong_framework(self):self.node()['framework']='AASB';self.reject()
    def test_wrong_currency(self):self.node()['functional_currency']='JPY';self.reject()
    def test_same_display_different_identity_preserved(self):
        for scope in self.d['scopes']:scope['display_name']='Same display'
        c=restore(self.d,COMPANY,self.d['root_case']);self.assertEqual(len(c.governance.cases.scopes.record()),len(self.d['scopes']))
    def test_partial_to_complete(self):self.case()['outcome']='complete';self.reject()
    def test_blocked_to_closed(self):self.case().update(outcome='blocked',status='CLOSED');self.reject()
    def test_invalid_case_transition(self):self.case()['transitions']=['OPEN','CLOSED'];self.reject()
    def test_missing_transition_history(self):self.case()['transitions']=[];self.reject()
    def test_missing_challenge(self):
        c=next(c for c in self.d['cases'] if c['status']=='CLOSED');c['challenge_results']=[];self.reject()
    def test_missing_documentation(self):
        c=next(c for c in self.d['cases'] if c['status']=='CLOSED');c['artifacts']=[];self.reject()
    def test_parent_child_contamination(self):self.case()['child_case_ids']=[];self.reject()
    def test_source_payload_changed(self):
        key=next(iter(self.d['source_snapshots']));self.d['source_snapshots'][key]['evidence']=['changed'];self.reject()
    def test_wrong_owner_binding(self):self.node()['selected_skill']='accounts-payable';self.reject()
    def test_source_population_shortened(self):
        key=next(k for k,s in self.d['source_snapshots'].items() if s.get('source_population'));self.d['source_snapshots'][key]['source_population']=[];self.reject()
    def test_missing_source(self):self.d['source_snapshots'].pop(next(iter(self.d['source_snapshots'])));self.reject()
    def test_missing_version(self):self.d['versions'].pop(next(iter(self.d['versions'])));self.reject()
    def test_duplicate_current(self):
        old=next(k for k,s in self.d['states'].items() if s=='SUPERSEDED');self.d['states'][old]='CURRENT';self.reject()
    def test_superseded_reactivated(self):
        old=next(k for k,s in self.d['states'].items() if s=='SUPERSEDED');self.d['active'][self.d['versions'][old]['node_id']]=old;self.reject()
    def test_wrong_version_receipt(self):self.receipt()['result_version']=next(iter(self.d['versions']));self.reject()
    def test_wrong_layer_receipt(self):self.receipt()['consumer_presentation_currency']='GBP';self.reject()
    def test_wrong_scope_receipt(self):self.receipt()['producer_scope']='ENTITY-NL';self.reject()
    def test_wrong_period_receipt(self):self.receipt()['producer_period']='period:other';self.reject()
    def test_equal_value_wrong_lineage(self):self.receipt()['producer_node']=self.node()['id'];self.reject()
    def test_broken_dependency(self):self.d['dependencies'].pop(next(iter(self.d['dependencies'])));self.reject()
    def test_duplicate_legal_journal(self):
        v=next(v for v in self.d['versions'].values() if json.loads(v['payload_json']).get('journal_entry_implications'))
        p=json.loads(v['payload_json']);p['journal_entry_implications']*=2;v['payload_json']=json.dumps(p);self.reject()
    def test_legal_group_layer_substitution(self):self.node()['scope_type']='GROUP';self.reject()
    def test_missing_required_approval(self):
        event=next(x for x in self.d['periods']['history'] if x['event']=='REOPENED');event['approval']['evidence']=[];self.reject()
    def test_opening_comparative_substitution(self):
        dep=next(x for x in self.d['dependencies'].values() if x['dependency_type']=='OPENING');dep['dependency_type']='COMPARATIVE';self.reject()
    def test_unknown_field(self):self.d['future_approval']=True;self.reject()
    def test_future_contract(self):self.d['contract_version']=2;self.reject()
    def test_missing_required_object(self):del self.d['periods'];self.reject()
    def test_public_privacy_contamination(self):
        f=proof(False);c=f['case'];c.conclusions=[dict(conclusion='version:secret',calculations={},journals=[],open_items=[],controls=[],reporting=[],limitations=[],required_approvals=[])]
        c._synthesis_currentness=sorted((n,k,c.governance.versions.state(k)) for n,k in c.governance.versions.active.items())
        with self.assertRaises(ValueError):snapshot(c,COMPANY,CONTEXT)


class StorageAttacks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.c=proof()['case']
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'state.db';self.store=SQLiteStore(self.path)
    def tearDown(self):self.store.close();self.tmp.cleanup()
    def save(self,rev=0):return self.store.save(self.c,COMPANY,CONTEXT,rev)
    def load(self):return self.store.load(COMPANY,self.c.id)
    def test_real_file_and_fresh_connection(self):
        self.save();self.assertEqual(self.path.stat().st_mode & 0o777,0o600)
        with SQLiteStore(self.path) as fresh:self.assertEqual(fresh.load(COMPANY,self.c.id)[1],1)
    def test_atomic_interrupted_checkpoint(self):
        self.save();original=self.store._write_objects
        def fail(company,case,rev,manifest):original(company,case,rev,manifest[:2]);raise OSError('simulated disk failure')
        with patch.object(self.store,'_write_objects',side_effect=fail):
            with self.assertRaises(ValueError):self.save(1)
        self.assertEqual(self.load()[1],1)
        self.assertEqual(self.store.connection.execute('SELECT count(*) FROM checkpoints').fetchone()[0],1)
    def test_stale_writer(self):
        self.save()
        with SQLiteStore(self.path) as other:
            self.save(1)
            with self.assertRaises(RevisionConflict):other.save(self.c,COMPANY,CONTEXT,1)
        self.assertEqual(self.load()[1],2)
    def test_concurrent_revision_conflict(self):
        self.save();barrier=threading.Barrier(2);results=[]
        def writer():
            with SQLiteStore(self.path) as store:
                barrier.wait()
                try:results.append(store.save(self.c,COMPANY,CONTEXT,1))
                except RevisionConflict:results.append('conflict')
        threads=[threading.Thread(target=writer) for _ in range(2)]
        for thread in threads:thread.start()
        for thread in threads:thread.join(timeout=15);self.assertFalse(thread.is_alive())
        self.assertCountEqual(results,[2,'conflict']);self.assertEqual(self.load()[1],2)
    def test_corrupted_payload(self):
        self.save();self.store.connection.execute("UPDATE checkpoints SET payload='{}'")
        with self.assertRaises(IntegrityError):self.load()
    def test_partial_object_write(self):
        self.save();self.store.connection.execute("DELETE FROM objects WHERE kind='source'")
        with self.assertRaises(IntegrityError):self.load()
    def test_future_schema(self):
        self.store.connection.execute('PRAGMA user_version=2')
        with self.assertRaises(IntegrityError):self.load()
        with self.assertRaises(IntegrityError):self.store.migrate(2)
    def test_noop_migration_fixture(self):
        self.save();before=self.path.read_bytes();self.assertEqual(self.store.migrate(1),1)
        self.assertEqual(self.path.read_bytes(),before)
    def test_failed_schema_initialization_rollback(self):
        path=Path(self.tmp.name)/'unknown.db';conn=sqlite3.connect(path);conn.execute('CREATE TABLE unrelated(value TEXT)');conn.close()
        with self.assertRaises(IntegrityError):SQLiteStore(path)
        conn=sqlite3.connect(path);self.assertEqual(conn.execute('PRAGMA user_version').fetchone()[0],0);conn.close()
    def test_deterministic_serialization(self):
        self.assertEqual(dumps(dict(b=2,a=1)),dumps(dict(a=1,b=2)))
        with self.assertRaises(IntegrityError):loads('{"a":1,"a":2}')
    def test_missing_root_namespace(self):
        self.save()
        with self.assertRaises(IntegrityError):self.store.load('company:wrong',self.c.id)
    def test_reader_only_committed_checkpoint(self):
        self.save()
        with SQLiteStore(self.path) as reader:
            self.store.connection.execute('BEGIN IMMEDIATE')
            self.store.connection.execute('UPDATE heads SET revision=revision')
            self.assertEqual(reader.load(COMPANY,self.c.id)[1],1)
            self.store.connection.execute('ROLLBACK')
    def test_historical_revisions_immutable(self):
        self.save();self.save(1)
        one=self.store.load(COMPANY,self.c.id,1);two=self.load()
        self.assertEqual(dumps(snapshot(one[0],COMPANY,one[2])),dumps(snapshot(two[0],COMPANY,two[2])))
    def test_correct_revision_cannot_truncate_immutable_history(self):
        early=proof(False);self.store.save(early['case'],COMPANY,CONTEXT,0)
        from orchestration.tests.stage2_fixtures import correction
        correction(early);self.store.save(early['case'],COMPANY,CONTEXT,1)
        old,_,context=self.store.load(COMPANY,early['case'].id,1)
        with self.assertRaises(IntegrityError):self.store.save(old,COMPANY,context,2)
        self.assertEqual(self.store.load(COMPANY,early['case'].id)[1],2)
    def test_process_death_mid_transaction_recovers_last_commit(self):
        self.save()
        script='''
import sqlite3,sys,os
conn=sqlite3.connect(sys.argv[1],isolation_level=None)
conn.execute('BEGIN IMMEDIATE')
conn.execute("UPDATE checkpoints SET payload='partial-uncommitted-state'")
os._exit(17)
'''
        result=subprocess.run([sys.executable,'-c',script,str(self.path)])
        self.assertEqual(result.returncode,17);self.assertEqual(self.load()[1],1)

if __name__=='__main__':unittest.main()
