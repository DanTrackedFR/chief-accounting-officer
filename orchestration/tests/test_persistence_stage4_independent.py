"""Fresh reviewer: connected Group/native SQLite memory boundaries, no owner rewrites."""
import copy
from decimal import Decimal
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from orchestration.persistence import SQLiteStore, snapshot, IntegrityError
from orchestration.persistence.codec import dumps
from orchestration.runtime import CAO
from orchestration.tests import persistence_stage4_fixtures as f
from orchestration.tests import stage4_closing_population as population
from orchestration.reporting_temporal import validate_reporting_temporal
from interfaces.public_output import ROUTES

class DurableIntegrationIndependent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.template=Path(cls.tmp.name)/'native.db'
        initial=f.initial(systems='NetSuite');cls.blocked=copy.deepcopy(initial)
        accepted,cls.acceptance=f.finish(initial);cls.root=accepted['case'].id
        with SQLiteStore(cls.template) as store:
            store.save(accepted['case'],f.COMPANY,f.CONTEXT,0)
            cls.candidate=f.capture(store,accepted['case'])
            cls.record=store.memory().transition(f.COMPANY,cls.candidate['record_id'],f.governance(cls.candidate),expected_revision=1,recorded_at=f.LEARNED)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'attack.db';shutil.copyfile(self.template,self.path)
        self.s=SQLiteStore(self.path);self.c,self.rev,self.ctx=self.s.load(f.COMPANY,self.root);self.m=self.s.memory()
        self.nodes={n.logical_id:n for n in self.c.graph.nodes.values()}
    def tearDown(self):self.s.close();self.tmp.cleanup()
    def test_sealed_governed_intake_preserves_exact_proposed_candidate(self):
        prepared=self.blocked['intake'];native=self.blocked['case']
        original=next(x for x in prepared.memory_candidates if x['attribute']=='systems')
        retained=next(x for x in native.memory_candidates if x.get('semantic_status')=='EXTRACTED' and x['attribute']=='systems')
        self.assertEqual(dumps(original),dumps(retained));self.assertEqual(self.candidate['status'],'PROPOSED')
        self.assertEqual(self.candidate['value'],'NetSuite');self.assertFalse(self.record['governance']['authenticated'])
    def test_original_conflict_and_correction_remain_immutable(self):
        self.assertEqual(CAO().public(self.blocked['case'])['status'],'partial')
        old=self.acceptance['before']['fx-ENTITY-UK'];current=self.c.governance.versions.current(self.nodes['fx-ENTITY-UK'].id)
        self.assertEqual(Decimal(old.payload()['calculations']['pairs'][0]['a_functional']),16)
        self.assertEqual(Decimal(current.payload()['calculations']['pairs'][0]['a_functional']),18)
        self.assertEqual(Decimal(current.payload()['calculations']['pairs'][0]['a_fx_gain']),2)
        for v in self.acceptance['before'].values():self.assertEqual(self.c.governance.versions.versions[v.version_id],v)
    def test_native_reporting_temporal_and_journal_invariants(self):
        r=f.current_results(self.c);self.assertEqual(r['reporting']['calculations']['current']['cash'],'490.00');self.assertEqual(r['reporting']['calculations']['current']['profit'],'3.00')
        self.assertEqual(r['current-opening']['calculations']['current']['closing_equity'],'487.00')
        self.assertEqual(r['prior-year-comparative']['calculations']['current']['cash'],'489.00')
        inventory=population.exact_once(f.attach(self.c));self.assertEqual(len(inventory['selected']),8)
        self.assertEqual(len(r['elimination']['journal_entry_implications']),6)
    def test_current_memory_is_exact_root_owned_native_support(self):
        r=self.m.retrieve(f.COMPANY,self.root,self.root,'finance','systems')['qualified'][0]['record']
        self.assertTrue(r['source']['result_versions'])
        for key in r['source']['result_versions']:
            v=self.c.governance.versions.require_current(key);self.assertEqual((v.case_id,v.scope_id),(self.root,'GROUP-EUR'))
        for name in ('case_library','artifact_library','provenance','decision_register'):self.assertTrue(self.m.audit(f.COMPANY)[name])
    def test_group_memory_does_not_inherit_into_legal_entity(self):
        legal=self.nodes['fx-ENTITY-UK'].case_id
        self.assertFalse(self.m.retrieve(f.COMPANY,self.root,legal,'finance','systems')['qualified'])
    def test_other_company_namespace_refuses_real_checkpoint(self):
        with self.assertRaises(IntegrityError):self.m.retrieve('company:hostile',self.root,self.root,'finance','systems')
    def test_wrong_case_refuses_native_memory_consumption(self):
        with self.assertRaises(ValueError):self.m.consume_context(f.COMPANY,self.root,'case:hostile',self.record['record_id'],self.record['version_id'],expected_revision=2,recorded_at=f.LEARNED)
    def test_documentary_approval_requires_actual_sealed_envelope(self):
        intent=f.governance(self.record,'APPROVED');intent['evidence_kind']='DOCUMENTARY'
        with self.assertRaises(IntegrityError):self.m.transition(f.COMPANY,self.record['record_id'],intent,expected_revision=2,recorded_at=f.LEARNED)
    def test_synthetic_transition_never_authenticates(self):
        intent=f.governance(self.record,'APPROVED');intent['authenticated']=True
        with self.assertRaises(IntegrityError):self.m.transition(f.COMPANY,self.record['record_id'],intent,expected_revision=2,recorded_at=f.LEARNED)
    def test_context_reference_cannot_replace_native_receipt(self):
        e=self.c.governance;edge=next(x for x in e.edges.values() if x.consumer_node==self.nodes['group'].id)
        with self.assertRaises(ValueError):e.validate_receipt(dict(record_id=self.record['record_id'],version_id=self.record['version_id'],use='CONTEXT_ONLY'),edge.consumer_node)
    def test_context_record_cannot_bypass_native_reviewed_input(self):
        e=self.c.governance;n=self.nodes['adjacent-closing']
        with self.assertRaises(ValueError):CAO().correct(self.c,n.id,dict(memory=self.record),'Hostile memory-only financial input')
        self.assertEqual(self.c.status,'CLOSED')
    def test_actual_source_correction_stales_exact_support_and_only_real_consumers(self):
        before=snapshot(self.c,f.COMPANY,self.ctx);key=self.s.prepare(self.c,f.COMPANY,self.ctx,self.rev,f.correction_intent(self.c));c,outcome=self.s.recover(f.COMPANY,self.root,key)
        plan=outcome['events'][-1]['value']['result'];self.assertEqual({c.graph.nodes[x].logical_id for x in plan['execution_order']},{'current-opening','reporting','analytics','group'})
        query=self.m.retrieve(f.COMPANY,self.root,self.root,'finance','systems');self.assertFalse(query['qualified']);self.assertTrue(any('supporting-result-STALE' in x['reasons'] for x in query['refused']))
        for node in plan['unaffected']:self.assertEqual(before['active'][node],c.governance.versions.active[node])
        self.assertEqual(CAO().public(c)['status'],'partial')
        with self.assertRaises(IntegrityError):self.m.consume_context(f.COMPANY,self.root,self.root,self.record['record_id'],self.record['version_id'],expected_revision=2,recorded_at=f.LEARNED)
    def test_context_only_reuse_never_adds_source_case_financial_edge(self):
        reusable=f.initial(f.REUSE_OBJECTIVE,memory=f.memory_request(self.m,self.root));b,_=f.finish(reusable);self.s.save(b['case'],f.COMPANY,f.CONTEXT,0);self.assertEqual(len(f.native_invariants(b['case'])['journals']['selected']),8)
        self.assertEqual(reusable['memory_references'][0]['version_id'],self.record['version_id'])
        self.assertFalse(any(q.get('attribute')=='systems' for q in reusable['intake'].questions))
        self.assertFalse(any(edge.producer_case==self.root for edge in b['session'].edges.values()))
        use=self.m.consume_context(f.COMPANY,b['case'].id,b['case'].id,self.record['record_id'],self.record['version_id'],expected_revision=2,recorded_at=f.LEARNED)
        self.assertEqual(use['use'],'CONTEXT_ONLY')
        a_before=dumps(snapshot(self.c,f.COMPANY,self.ctx));new=self.m.transition(f.COMPANY,self.record['record_id'],f.governance(self.record,'RETRACTED'),expected_revision=3,recorded_at=f.LEARNED)
        restored,_,_=self.s.load(f.COMPANY,self.root);self.assertEqual(a_before,dumps(snapshot(restored,f.COMPANY,self.ctx)))
        self.assertEqual(self.m.audit(f.COMPANY)['uses'][0]['value']['memory_version'],self.record['version_id']);self.assertEqual(new['status'],'RETRACTED')
    def test_temporal_role_cannot_be_replaced_by_memory_equal_value(self):
        e=self.c.governance;n=self.nodes['reporting'];source=copy.deepcopy(e.sources[n.id])
        opening=source['temporal_reporting']['OPENING']
        receipts=[e.receipt(k) for k,d in e.edges.items() if d.consumer_node==n.id and k!=opening]
        receipts.append(dict(dependency_id=opening,record_id=self.record['record_id'],version_id=self.record['version_id'],use='CONTEXT_ONLY'))
        with self.assertRaises((ValueError,KeyError)):validate_reporting_temporal(e,n,source,receipts)
    def test_concurrent_memory_promotion_and_actual_source_correction_serialize(self):
        import threading
        key=self.s.prepare(self.c,f.COMPANY,self.ctx,self.rev,f.correction_intent(self.c))
        barrier=threading.Barrier(2);results={}
        def promote():
            try:
                with SQLiteStore(self.path) as other:
                    other.connection.execute('PRAGMA busy_timeout=120000')
                    barrier.wait(timeout=30)
                    results['promotion']=other.memory().transition(f.COMPANY,self.record['record_id'],f.governance(self.record,'APPROVED'),expected_revision=2,recorded_at=f.LEARNED)
            except IntegrityError as exc:results['promotion_refused']=str(exc)
            except BaseException as exc:results['promotion_error']=repr(exc)
        def correct():
            try:
                with SQLiteStore(self.path) as other:
                    other.connection.execute('PRAGMA busy_timeout=120000')
                    barrier.wait(timeout=30);results['correction']=dict(status=other.recover(f.COMPANY,self.root,key)[1]['status'])
            except BaseException as exc:results['correction_error']=repr(exc)
        workers=[threading.Thread(target=promote),threading.Thread(target=correct)]
        for worker in workers:worker.start()
        for worker in workers:worker.join(timeout=120);self.assertFalse(worker.is_alive())
        self.assertNotIn('promotion_error',results);self.assertNotIn('correction_error',results)
        self.assertEqual(results['correction']['status'],'COMMITTED')
        self.assertTrue('promotion' in results or 'promotion_refused' in results)
        q=self.m.retrieve(f.COMPANY,self.root,self.root,'finance','systems');self.assertFalse(q['qualified'])
        self.assertTrue(any('supporting-result-STALE' in x['reasons'] for x in q['refused']))

    def test_warm_memory_lookup_cannot_hide_later_operation_history_corruption(self):
        key=self.s.prepare(self.c,f.COMPANY,self.ctx,self.rev,f.correction_intent(self.c))
        self.assertTrue(self.m.retrieve(f.COMPANY,self.root,self.root,'finance','systems')['qualified'])
        self.s.connection.execute('DELETE FROM operation_events WHERE operation_id=?',(key,))
        with self.assertRaises(IntegrityError):self.m.retrieve(f.COMPANY,self.root,self.root,'finance','systems')
        self.assertIsNone(self.m._native_cache)
    def test_failed_sqlite_transition_clears_cache_without_promoting_memory(self):
        import sqlite3
        self.assertTrue(self.m.retrieve(f.COMPANY,self.root,self.root,'finance','systems')['qualified'])
        self.s.connection.execute("CREATE TRIGGER reviewer_abort BEFORE INSERT ON memory_events BEGIN SELECT RAISE(ABORT,'independent interrupted transition'); END")
        with self.assertRaises(sqlite3.IntegrityError):self.m.transition(f.COMPANY,self.record['record_id'],f.governance(self.record,'APPROVED'),expected_revision=2,recorded_at=f.LEARNED)
        self.assertIsNone(self.m._native_cache);self.s.connection.execute('DROP TRIGGER reviewer_abort')
        audit=self.m.audit(f.COMPANY);self.assertEqual(audit['revision'],2);self.assertEqual(audit['company_context'][0]['status'],'DOCUMENTED')
        self.assertIsNone(self.m._native_cache)
    def test_cached_native_read_never_survives_commit_to_later_corrupt_checkpoint(self):
        self.assertTrue(self.m.retrieve(f.COMPANY,self.root,self.root,'finance','systems')['qualified'])
        self.assertIsNone(self.m._native_cache)
        self.s.connection.execute("UPDATE checkpoints SET payload=payload||' ' WHERE company_id=? AND case_id=?",(f.COMPANY,self.root))
        with self.assertRaises(IntegrityError):self.m.retrieve(f.COMPANY,self.root,self.root,'finance','systems')
        self.assertIsNone(self.m._native_cache)

    def test_current_unresolved_company_case_remains_partial_after_restart(self):
        negative=f.initial(f.OBJECTIVE+' Evaluate an unresolved current negative reporting control.',systems='Xero')['case']
        self.s.save(negative,f.COMPANY,f.CONTEXT,0)
        with patch.object(CAO,'run',side_effect=AssertionError('Restoration ran accounting')),patch.object(CAO,'execute_versioned_owner',side_effect=AssertionError('Restoration ran owner')):
            restored,_,_=self.s.load(f.COMPANY,negative.id)
        self.assertNotEqual(restored.status,'CLOSED');self.assertEqual(CAO().public(restored)['status'],'partial')
        self.assertTrue(CAO().public(restored)['open_items'])
        self.assertEqual(CAO().public(self.c)['status'],'complete')
        first=f.capture(self.s,self.c,subject='negative-systems')
        self.m.transition(f.COMPANY,first['record_id'],f.governance(first),expected_revision=3,recorded_at=f.LEARNED)
        other=f.capture(self.s,restored,subject='negative-systems')
        self.assertEqual(other['status'],'PROPOSED')
        refusal=self.m.retrieve(f.COMPANY,self.root,self.root,'negative-systems','systems')
        self.assertTrue(refusal['conflicts']);self.assertFalse(refusal['qualified'])
        self.assertEqual(CAO().public(self.c)['status'],'complete')
        historical=[v.payload() for v in restored.governance.versions.versions.values() if v.node_id==next(n.id for n in restored.graph.nodes.values() if n.logical_id=='fx-ENTITY-UK')]
        self.assertTrue(any(Decimal(v['calculations']['pairs'][0]['a_functional'])==16 for v in historical))

    def test_governed_successor_can_be_reused_without_historical_position_substitution(self):
        newer,_=f.finish(f.initial(f.OBJECTIVE+' Independently review corrected systems context.',systems='Xero'))
        case=newer['case'];self.s.save(case,f.COMPANY,f.CONTEXT,0)
        candidate=f.capture(self.s,case,supersedes=[self.record['record_id']])
        successor=self.m.resolve_conflict(f.COMPANY,candidate['record_id'],f.governance(candidate),{self.record['record_id']:f.governance(self.record,'SUPERSEDED')},expected_revision=3,recorded_at=f.LEARNED)
        retrieval=self.m.retrieve(f.COMPANY,case.id,case.id,'finance','systems')
        self.assertEqual([v['record']['value'] for v in retrieval['qualified']],['Xero'])
        self.assertTrue(any(r['record']['status']=='SUPERSEDED' for r in retrieval['refused']))
        separate=f.initial(f.REUSE_OBJECTIVE+' Use qualified successor in separate Case.',memory=f.memory_request(self.m,case.id))
        self.assertEqual(separate['session'].context['systems'],'Xero')
        self.assertEqual(separate['memory_references'][0]['version_id'],successor['version_id'])
        self.assertNotEqual(separate['memory_references'][0]['version_id'],self.record['version_id'])

    def test_equal_value_unapproved_active_alternative_still_blocks_intake(self):
        newer,_=f.finish(f.initial(f.OBJECTIVE+' Review equal-value unapproved alternative.',systems='NetSuite'))
        case=newer['case'];self.s.save(case,f.COMPANY,f.CONTEXT,0);candidate=f.capture(self.s,case)
        self.assertEqual(candidate['status'],'PROPOSED')
        retrieval=self.m.retrieve(f.COMPANY,self.root,self.root,'finance','systems')
        self.assertTrue(retrieval['qualified']);self.assertTrue(any(v['record']['status']=='PROPOSED' for v in retrieval['refused']))
        with self.assertRaises(IntegrityError):f.initial(f.REUSE_OBJECTIVE+' Reject unapproved active alternative.',memory=f.memory_request(self.m,self.root))
    def test_retracted_alternative_cannot_veto_or_substitute_current_exact_version(self):
        newer,_=f.finish(f.initial(f.OBJECTIVE+' Review then retract erroneous systems source.',systems='Xero'))
        case=newer['case'];self.s.save(case,f.COMPANY,f.CONTEXT,0);candidate=f.capture(self.s,case)
        retracted=self.m.transition(f.COMPANY,candidate['record_id'],f.governance(candidate,'RETRACTED'),expected_revision=3,recorded_at=f.LEARNED)
        retrieval=self.m.retrieve(f.COMPANY,self.root,self.root,'finance','systems')
        self.assertFalse(retrieval['conflicts']);self.assertEqual([x['record']['version_id'] for x in retrieval['qualified']],[self.record['version_id']])
        separate=f.initial(f.REUSE_OBJECTIVE+' Retain qualified current context after retraction.',memory=f.memory_request(self.m,self.root))
        self.assertEqual(separate['session'].context['systems'],'NetSuite')
        self.assertEqual(separate['memory_references'][0]['version_id'],self.record['version_id'])
        with self.assertRaises(IntegrityError):self.m.consume_context(f.COMPANY,self.root,self.root,retracted['record_id'],retracted['version_id'],expected_revision=4,recorded_at=f.LEARNED)

    def test_active_stale_support_cannot_be_hidden_by_new_equal_value_position(self):
        key=self.s.prepare(self.c,f.COMPANY,self.ctx,self.rev,f.correction_intent(self.c));self.s.recover(f.COMPANY,self.root,key)
        newer,_=f.finish(f.initial(f.OBJECTIVE+' Review independently qualified same-value context.',systems='NetSuite'))
        case=newer['case'];self.s.save(case,f.COMPANY,f.CONTEXT,0);candidate=f.capture(self.s,case)
        current=self.m.transition(f.COMPANY,candidate['record_id'],f.governance(candidate),expected_revision=3,recorded_at=f.LEARNED)
        retrieval=self.m.retrieve(f.COMPANY,case.id,case.id,'finance','systems')
        self.assertEqual([x['record']['version_id'] for x in retrieval['qualified']],[current['version_id']])
        self.assertTrue(any(x['record']['status']=='DOCUMENTED' and 'supporting-result-STALE' in x['reasons'] for x in retrieval['refused']))
        with self.assertRaises(IntegrityError):f.initial(f.REUSE_OBJECTIVE+' Refuse active stale support.',memory=f.memory_request(self.m,case.id))

    def test_restore_and_current_retrieval_are_read_only(self):
        before=dumps(snapshot(self.c,f.COMPANY,self.ctx))
        with patch.object(CAO,'run',side_effect=AssertionError('Native run on read')),patch.object(CAO,'execute_versioned_owner',side_effect=AssertionError('Native owner on read')):
            restored,rev,ctx=self.s.load(f.COMPANY,self.root);self.assertTrue(self.m.retrieve(f.COMPANY,self.root,self.root,'finance','systems')['qualified'])
        self.assertEqual(before,dumps(snapshot(restored,f.COMPANY,ctx)));self.assertEqual(rev,self.rev)
    def test_public_routes_exclude_private_memory_and_storage(self):
        for route in ROUTES:
            public=CAO().public(self.c,route);self.assertEqual(public['status'],'complete')
            for token in ('memory-version:','memory-event:','record_id','source_snapshots','checkpoint_sha256','reviewer_signoff','operations','Company finance system.json'):
                self.assertNotIn(token,str(public))

if __name__=='__main__':unittest.main()
