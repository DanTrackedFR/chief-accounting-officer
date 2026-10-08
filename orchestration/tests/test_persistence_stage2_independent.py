"""Fresh-reviewer attacks; accepted native fixture, real SQLite/process boundaries."""
import copy
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from orchestration.persistence import SQLiteStore, snapshot, IntegrityError
from orchestration.persistence.codec import dumps
from orchestration.persistence.recovery import RecoveryBlocked
from orchestration.persistence.evidence import retain
from orchestration.runtime import CAO
from orchestration.tests import stage4_temporal_fixtures as temporal, stage4_fixtures as stage4, stage4_closing_population as population
from orchestration.tests.persistence_fixtures import COMPANY, CONTEXT


def attach(case):
    f=temporal.build();e=case.governance;f.update(case=case,session=e)
    f['basis'].session=e;f['nodes']={n.logical_id:n for n in e.graph.nodes.values()}
    f['containers']={k:e.cases.get(c.id) for k,c in f['containers'].items()}
    return f


def correction(case):
    f=attach(case);n=f['nodes']['adjacent-closing']
    c=stage4.qualified_replacement(f,n.id,temporal.stock_source(f,'adjacent-closing'))
    return dict(kind='CORRECT',node_id=n.id,source=c,reason='Independent reviewed replacement closing-stock lineage')


def selection(case):
    f=attach(case);e=case.governance
    events=population.exact_once(f)['events']
    context=dict(entity='GROUP-EUR',framework='IFRS',jurisdiction='NL',currency='EUR',period_start='2026-10-01',reporting_period='2026-10-31',scopes=e.cases.scopes.record(),period_registry=e.periods.record())
    return dict(kind='SELECT_JOURNALS',context=context,events=events)


class IndependentRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root=tempfile.TemporaryDirectory();cls.template=Path(cls.root.name)/'accepted.db'
        f,_=temporal.run()
        for row in f['replacement_intakes']:retain(f['case'].governance,row['prepared'],row['reviewed_pack'])
        f['session'].context.update(company_id=COMPANY,company_context=copy.deepcopy(CONTEXT))
        cls.case_id=f['case'].id
        with SQLiteStore(cls.template) as s:s.save(f['case'],COMPANY,CONTEXT,0)
    @classmethod
    def tearDownClass(cls):cls.root.cleanup()
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'attack.db';shutil.copyfile(self.template,self.path)
        self.store=SQLiteStore(self.path);self.case,self.revision,self.context=self.store.load(COMPANY,self.case_id)
    def tearDown(self):self.store.close();self.tmp.cleanup()
    def prepare(self):return self.store.prepare(self.case,COMPANY,self.context,self.revision,correction(self.case))
    def remove_operation(self,key):
        # FK refusal OR corruption refusal is correct; no payload/hash rewriting.
        try:
            self.store.connection.execute('DELETE FROM operation_events WHERE operation_id=?',(key,))
            self.store.connection.execute('DELETE FROM operations WHERE operation_id=?',(key,))
        except sqlite3.IntegrityError:return True
        return False
    def test_prepared_operation_cannot_disappear_from_durable_history(self):
        key=self.prepare()
        if self.remove_operation(key):return
        with self.assertRaises(IntegrityError):
            case,revision,context=self.store.load(COMPANY,self.case_id)
            self.store.save(case,COMPANY,context,revision)
    def test_uncertain_external_marker_cannot_disappear(self):
        key=self.store.prepare(self.case,COMPANY,self.context,1,selection(self.case));c,r=self.store.recover(COMPANY,self.case_id,key)
        u=self.store.prepare(c,COMPANY,self.context,r['head_revision'],dict(kind='UNCERTAIN_EXTERNAL',selection_operation=key,evidence=['Synthetic external delivery outcome cannot be established']))
        with self.assertRaises(RecoveryBlocked):self.store.recover(COMPANY,self.case_id,u)
        if self.remove_operation(u):return
        with self.assertRaises(IntegrityError):
            c,revision,context=self.store.load(COMPANY,self.case_id);self.store.save(c,COMPANY,context,revision)
    def test_deleted_marker_detected_even_with_foreign_keys_disabled(self):
        key=self.prepare();self.store.connection.execute('PRAGMA foreign_keys=OFF')
        self.store.connection.execute('DELETE FROM operation_events WHERE operation_id=?',(key,));self.store.connection.execute('DELETE FROM operations WHERE operation_id=?',(key,))
        with self.assertRaises(IntegrityError):self.store.load(COMPANY,self.case_id)
    def test_committed_outcome_event_cannot_disappear_on_plain_load(self):
        key=self.prepare();self.store.recover(COMPANY,self.case_id,key)
        self.store.connection.execute("DELETE FROM operation_events WHERE operation_id=? AND status='COMMITTED'",(key,))
        with self.assertRaises(IntegrityError):self.store.load(COMPANY,self.case_id)
    def test_prepared_event_cannot_disappear_on_plain_load(self):
        key=self.prepare();self.store.connection.execute('DELETE FROM operation_events WHERE operation_id=?',(key,))
        with self.assertRaises(IntegrityError):self.store.load(COMPANY,self.case_id)
    def test_committed_journal_receipt_must_match_native_outcome_checkpoint(self):
        key=self.store.prepare(self.case,COMPANY,self.context,1,selection(self.case));self.store.recover(COMPANY,self.case_id,key)
        from orchestration.persistence.codec import loads
        from orchestration.persistence.store import sha
        row=self.store.connection.execute("SELECT sequence,payload FROM operation_events WHERE operation_id=? AND status='COMMITTED'",(key,)).fetchone()
        value=loads(row[1]);value['result']['selected'][0]['lines'][0]['amount']='999999999999'
        payload=dumps(value)
        self.store.connection.execute('UPDATE operation_events SET payload=?,sha256=? WHERE operation_id=? AND sequence=?',(payload,sha(payload),key,row[0]))
        with self.assertRaises(IntegrityError):self.store.recover(COMPANY,self.case_id,key)
    def test_committed_correction_plan_must_match_native_rework_history(self):
        key=self.prepare();self.store.recover(COMPANY,self.case_id,key)
        from orchestration.persistence.codec import loads
        from orchestration.persistence.store import sha
        row=self.store.connection.execute("SELECT sequence,payload FROM operation_events WHERE operation_id=? AND status='COMMITTED'",(key,)).fetchone()
        value=loads(row[1]);value['result']['new_version']='version:missing-authority'
        payload=dumps(value)
        self.store.connection.execute('UPDATE operation_events SET payload=?,sha256=? WHERE operation_id=? AND sequence=?',(payload,sha(payload),key,row[0]))
        with self.assertRaises(IntegrityError):self.store.recover(COMPANY,self.case_id,key)
    def test_duplicate_preparation_transition_refused_on_plain_load(self):
        key=self.prepare();self.store.recover(COMPANY,self.case_id,key)
        self.store.connection.execute("UPDATE operation_events SET status='PREPARED' WHERE operation_id=? AND sequence=1",(key,))
        with self.assertRaises(IntegrityError):self.store.load(COMPANY,self.case_id)
    def test_old_current_receipt_cannot_qualify_equal_value_new_lineage(self):
        old=copy.deepcopy(self.case.governance.receipts);key=self.prepare();c,r=self.store.recover(COMPANY,self.case_id,key)
        replaced=r['events'][-1]['value']['result']['old_version'];seen=0
        for receipt in old:
            if receipt['result_version']!=replaced:continue
            seen+=1
            with self.assertRaises(ValueError):c.governance.validate_receipt(receipt,receipt['consumer_node'])
        self.assertGreater(seen,0)
    def test_prepared_source_cannot_change_after_identity_binding(self):
        key=self.prepare();row=self.store.connection.execute('SELECT payload FROM operations WHERE operation_id=?',(key,)).fetchone()[0]
        from orchestration.persistence.codec import loads
        wire=loads(row);wire['intent']['source']['evidence']=['changed raw evidence']
        self.store.connection.execute('UPDATE operations SET payload=? WHERE operation_id=?',(dumps(wire),key))
        with self.assertRaises(IntegrityError):self.store.recover(COMPANY,self.case_id,key)
    def test_lost_ack_retry_no_owner_execution_or_new_revision(self):
        key=self.prepare()
        def death(name,*args):
            if name=='after_commit':raise RuntimeError('acknowledgement lost')
        with patch('orchestration.persistence.recovery._phase',side_effect=death):
            with self.assertRaises(RuntimeError):self.store.recover(COMPANY,self.case_id,key)
        before,rev,ctx=self.store.load(COMPANY,self.case_id)
        with patch.object(CAO,'execute_versioned_owner',side_effect=AssertionError('duplicate native execution')):after,r=self.store.recover(COMPANY,self.case_id,key)
        self.assertEqual(rev,r['head_revision']);self.assertEqual(snapshot(before,COMPANY,ctx),snapshot(after,COMPANY,ctx))
    def test_two_real_processes_recover_one_operation_once(self):
        key=self.prepare()
        code="from orchestration.persistence import SQLiteStore;import sys,json;\ns=SQLiteStore(sys.argv[1],timeout=120);c,r=s.recover(sys.argv[2],sys.argv[3],sys.argv[4]);print(json.dumps({'head':r['head_revision'],'versions':sorted(c.governance.versions.active.items())}));s.close()"
        args=[sys.executable,'-c',code,str(self.path),COMPANY,self.case_id,key]
        a=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);b=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        outa,erra=a.communicate(timeout=180);outb,errb=b.communicate(timeout=180)
        self.assertEqual(a.returncode,0,erra);self.assertEqual(b.returncode,0,errb);self.assertEqual(json.loads(outa),json.loads(outb))
        self.assertEqual(self.store.connection.execute("SELECT count(*) FROM operation_events WHERE status='COMMITTED'").fetchone()[0],1)
    def test_same_result_journals_no_duplicate_after_new_selection_operation(self):
        i=selection(self.case);key=self.store.prepare(self.case,COMPANY,self.context,1,i);c,r=self.store.recover(COMPANY,self.case_id,key)
        first=r['events'][-1]['value']['result'];k2=self.store.prepare(c,COMPANY,self.context,r['head_revision'],selection(c));c,r2=self.store.recover(COMPANY,self.case_id,k2)
        self.assertEqual(first,r2['events'][-1]['value']['result']);self.assertEqual(len(first['selected']),8)
    def test_group_population_cannot_be_legal_relabelled(self):
        i=selection(self.case);group=next(e for e in i['events'] if e['posting_scope']=='GROUP-EUR');group['posting_scope']='ENTITY-NL'
        with self.assertRaises(ValueError):self.store.prepare(self.case,COMPANY,self.context,1,i)
    def test_pending_correction_does_not_execute_on_restore(self):
        key=self.prepare()
        with patch.object(CAO,'execute_versioned_owner',side_effect=AssertionError('load executed native owner')):
            c,revision,_=self.store.load(COMPANY,self.case_id)
        self.assertEqual(revision,2);self.assertEqual(c.governance.versions.active,self.case.governance.versions.active)
        self.assertEqual(self.store.operation(COMPANY,self.case_id,key)['status'],'PREPARED')
    def test_blocked_closure_cannot_retry_without_new_reviewed_intent(self):
        key=self.prepare();c,r=self.store.recover(COMPANY,self.case_id,key)
        k=self.store.prepare(c,COMPANY,self.context,r['head_revision'],dict(kind='CLOSE_PERIOD',period_id=c.period_id))
        with self.assertRaises(RecoveryBlocked):self.store.recover(COMPANY,self.case_id,k)
        with self.assertRaises(RecoveryBlocked):self.store.recover(COMPANY,self.case_id,k)
        self.assertNotEqual(self.store.load(COMPANY,self.case_id)[0].status,'CLOSED')
    def test_all_public_routes_exclude_private_recovery_provenance(self):
        key=self.prepare();c,r=self.store.recover(COMPANY,self.case_id,key)
        from interfaces.public_output import ROUTES
        for route in ROUTES:
            wire=json.dumps(CAO().public(c,route))
            for value in ('operation:','dependency:','version:','evidence_bundles','reviewer_signoff','journal_entry_implications','prepared_revision','source_fingerprint'):
                self.assertNotIn(value,wire)

if __name__=='__main__':unittest.main()
