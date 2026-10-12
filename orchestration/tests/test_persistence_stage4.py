"""Integration attacks at real native intake/accounting/memory boundaries."""
import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from orchestration.persistence import SQLiteStore, restore, snapshot, IntegrityError
from orchestration.persistence.codec import dumps
from orchestration.tests import persistence_stage4_fixtures as f
from orchestration.intake.governed import qualify
from orchestration.runtime import CAO

class DurableIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=f.initial(systems='NetSuite');cls.initial=copy.deepcopy(cls.fixture['case'])
        cls.fixture,cls.corrected=f.finish(cls.fixture);cls.doc=snapshot(cls.fixture['case'],f.COMPANY,f.CONTEXT)
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.store=SQLiteStore(Path(self.tmp.name)/'company.db');self.addCleanup(self.store.close)
        self.case=restore(copy.deepcopy(self.doc),f.COMPANY,self.doc['root_case'])
        self.store.save(self.case,f.COMPANY,f.CONTEXT,0);self.memory=self.store.memory()
    def capture(self,**kwargs):return f.capture(self.store,self.case,**kwargs)
    def promote(self):
        r=self.capture();return self.memory.transition(f.COMPANY,r['record_id'],f.governance(r),expected_revision=self.memory.audit(f.COMPANY)['revision'],recorded_at=f.LEARNED)
    def test_governed_intake_preserves_exact_sealed_candidates(self):
        candidates=self.fixture['intake'].memory_candidates
        self.assertTrue(candidates);self.assertTrue(all(c in self.case.memory_candidates for c in candidates))
        self.assertTrue(all(c['status']=='PROPOSED' for c in candidates))
    def test_native_original_conflict_remains_partial(self):
        self.assertNotEqual(CAO().public(self.initial)['status'],'complete');self.assertNotEqual(self.initial.status,'CLOSED')
        self.assertTrue(any(v.payload().get('unresolved_dependencies') for v in self.initial.governance.versions.versions.values()))
    def test_native_accounting_is_unchanged(self):
        result=f.native_invariants(self.case);self.assertEqual(len(result['journals']['selected']),8)
        for key,v in self.initial.governance.versions.versions.items():self.assertEqual(v,self.case.governance.versions.versions[key])
    def test_capture_starts_proposed_without_approval(self):
        r=self.capture();self.assertEqual(r['status'],'PROPOSED');self.assertIsNone(r['governance'])
        self.assertFalse(self.memory.retrieve(f.COMPANY,self.case.id,self.case.id,'finance','systems')['qualified'])
    def test_explicit_synthetic_documentation_stays_unauthenticated(self):
        r=self.promote();self.assertFalse(r['governance']['authenticated']);self.assertEqual(r['governance']['evidence_kind'],'SYNTHETIC')
    def test_memory_capture_does_not_publish_accounting_or_journals(self):
        before=dumps(snapshot(self.case,f.COMPANY,f.CONTEXT));self.promote()
        after,_,_=self.store.load(f.COMPANY,self.case.id);self.assertEqual(before,dumps(snapshot(after,f.COMPANY,f.CONTEXT)))
    def test_wrong_company_namespace_refuses(self):
        self.promote()
        with self.assertRaises(IntegrityError):self.memory.retrieve('company:wrong',self.case.id,self.case.id,'finance','systems')
    def test_wrong_native_case_support_refuses(self):
        r=self.capture();bad=copy.deepcopy(r);bad['source']['case_id']='case:missing'
        with self.assertRaises((IntegrityError,ValueError)):self.memory._qualification(bad)
    def test_group_memory_does_not_inherit_to_legal_entity(self):
        self.promote();legal=next(c for c in self.case.governance.cases.cases.values() if c.scope_id=='ENTITY-NL')
        self.assertFalse(self.memory.retrieve(f.COMPANY,self.case.id,legal.id,'finance','systems')['qualified'])
    def test_wrong_period_cannot_reuse_group_context(self):
        self.promote();prior=next(c for c in self.case.governance.cases.cases.values() if c.scope_id=='GROUP-EUR' and c.period_id!=self.case.period_id)
        self.assertFalse(self.memory.retrieve(f.COMPANY,self.case.id,prior.id,'finance','systems')['qualified'])
    def test_model_inference_cannot_be_approved(self):
        r=self.capture();bad=copy.deepcopy(r);bad.update(assertion='INFERRED',status='APPROVED')
        g=f.governance(r,'APPROVED')
        with self.assertRaises(IntegrityError):self.memory._governance(bad,g,r['status'])
    def test_memory_reference_cannot_replace_native_receipt(self):
        r=self.promote();node=next(n for n in self.case.graph.nodes.values() if n.logical_id=='reporting')
        ref=dict(record_id=r['record_id'],version_id=r['version_id'],source_case=r['source']['case_id'],use='CONTEXT_ONLY')
        with self.assertRaises((IntegrityError,ValueError,KeyError)):self.case.governance.validate_receipt(ref,node.id)
    def test_memory_context_cannot_substitute_for_reviewed_input_pack(self):
        intake=self.fixture['intake_engine'];prepared=self.fixture['intake'];r=self.promote()
        with self.assertRaises(ValueError):qualify(intake,prepared,r)
    def test_changed_raw_company_evidence_refuses_sealed_intake(self):
        prepared=copy.deepcopy(self.fixture['intake']);raw=prepared._inventory.raw['company-system'];raw.payload[0]['systems']='Xero'
        with self.assertRaises(ValueError):qualify(self.fixture['intake_engine'],prepared,self.fixture['reviewed_pack'])
    def test_deleted_memory_event_refuses_real_ledger(self):
        self.promote();self.store.connection.execute('DELETE FROM memory_events WHERE company_id=? AND sequence=1',(f.COMPANY,))
        with self.assertRaises(IntegrityError):self.memory.audit(f.COMPANY)
    def test_deleted_source_snapshot_refuses_restore(self):
        doc=copy.deepcopy(self.doc);doc['source_snapshots'].pop(next(iter(doc['source_snapshots'])))
        with self.assertRaises((IntegrityError,ValueError)):restore(doc,f.COMPANY,doc['root_case'])
    def test_retracted_context_is_retained_but_refused(self):
        r=self.promote();self.memory.transition(f.COMPANY,r['record_id'],f.governance(r,'RETRACTED'),expected_revision=self.memory.audit(f.COMPANY)['revision'],recorded_at=f.LEARNED)
        self.assertFalse(self.memory.retrieve(f.COMPANY,self.case.id,self.case.id,'finance','systems')['qualified'])
        self.assertEqual(len(self.memory.history(f.COMPANY,r['record_id'])),3)
    def test_public_routes_hide_memory_and_recovery_archives(self):
        self.promote()
        for route in ('answer','summary','artifact','api'):
            try:public=CAO().public(self.case,route)
            except ValueError:continue
            text=dumps(public)
            for marker in ('memory_events','memory_governance','source_snapshots','memory_context_dependencies','qualified_input_snapshot','raw_sources','Company finance system.json'):
                self.assertNotIn(marker,text)
    def test_warm_memory_does_not_hide_later_checkpoint_corruption(self):
        self.promote()
        self.assertTrue(self.memory.retrieve(f.COMPANY,self.case.id,self.case.id,'finance','systems')['qualified'])
        self.store.connection.execute("UPDATE checkpoints SET payload=payload || ' ' WHERE company_id=? AND case_id=?",(f.COMPANY,self.case.id))
        with self.assertRaises(IntegrityError):self.memory.retrieve(f.COMPANY,self.case.id,self.case.id,'finance','systems')
    def test_memory_write_revalidates_native_state_before_commit(self):
        r=self.capture();append=self.memory._append
        def corrupt_after_append(*args,**kwargs):
            result=append(*args,**kwargs)
            self.store.connection.execute("UPDATE checkpoints SET payload=payload || ' ' WHERE company_id=? AND case_id=?",(f.COMPANY,self.case.id))
            return result
        with patch.object(self.memory,'_append',side_effect=corrupt_after_append):
            with self.assertRaises(IntegrityError):self.memory.transition(f.COMPANY,r['record_id'],f.governance(r),expected_revision=1,recorded_at=f.LEARNED)
        audit=self.memory.audit(f.COMPANY)
        self.assertEqual(audit['revision'],1);self.assertEqual(audit['company_context'][0]['status'],'PROPOSED')
        restored,_,_=self.store.load(f.COMPANY,self.case.id)
        self.assertEqual(dumps(snapshot(restored,f.COMPANY,f.CONTEXT)),dumps(self.doc))
    def successor_source(self,value):
        fixture=f.initial(f.OBJECTIVE+' Review separate governed '+value+' systems evidence.',systems=value)
        fixture,_=f.finish(fixture);case=fixture['case'];self.store.save(case,f.COMPANY,f.CONTEXT,0)
        return case
    def test_governed_successor_reuses_current_context_with_retired_history(self):
        old=self.promote();case=self.successor_source('Xero')
        new=f.capture(self.store,case,supersedes=[old['record_id']])
        self.memory.resolve_conflict(f.COMPANY,new['record_id'],f.governance(new),{old['record_id']:f.governance(old,'SUPERSEDED')},expected_revision=3,recorded_at=f.LEARNED)
        result=self.memory.retrieve(f.COMPANY,case.id,case.id,'finance','systems')
        self.assertEqual(result['conflicts'],[]);self.assertEqual([r['record']['value'] for r in result['qualified']],['Xero'])
        self.assertEqual(result['refused'][0]['record']['status'],'SUPERSEDED')
        reused=f.initial(f.REUSE_OBJECTIVE,memory=f.memory_request(self.memory,case.id))
        self.assertEqual(reused['session'].context['systems'],'Xero')
        self.assertEqual([r['record_id'] for r in reused['memory_references']],[new['record_id']])
    def test_unapproved_equal_value_alternative_still_blocks_intake(self):
        self.promote();case=self.successor_source('NetSuite');f.capture(self.store,case)
        result=self.memory.retrieve(f.COMPANY,case.id,case.id,'finance','systems')
        self.assertTrue(result['qualified']);self.assertEqual(result['refused'][0]['record']['status'],'PROPOSED')
        with self.assertRaises(IntegrityError):f.initial(f.REUSE_OBJECTIVE,memory=f.memory_request(self.memory,case.id))
    def test_retracted_history_cannot_veto_or_substitute_current_context(self):
        old=self.promote();self.memory.transition(f.COMPANY,old['record_id'],f.governance(old,'RETRACTED'),expected_revision=2,recorded_at=f.LEARNED)
        case=self.successor_source('Xero');new=f.capture(self.store,case)
        self.memory.transition(f.COMPANY,new['record_id'],f.governance(new),expected_revision=4,recorded_at=f.LEARNED)
        reused=f.initial(f.REUSE_OBJECTIVE,memory=f.memory_request(self.memory,case.id))
        self.assertEqual(reused['session'].context['systems'],'Xero')
        self.assertEqual([r['record_id'] for r in reused['memory_references']],[new['record_id']])
if __name__=='__main__':unittest.main()
