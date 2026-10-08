"""Independent review attacks at real SQLite/native Company Memory boundaries."""
import copy
import tempfile
import unittest
from pathlib import Path
from orchestration.tests.intake_fixtures import ap_control
from orchestration.persistence import SQLiteStore, IntegrityError
from orchestration.persistence.memory import CompanyMemory, applicability, ident
from orchestration.persistence.codec import dumps
from orchestration.persistence.store import sha

UNKNOWN={'value':None,'precision':'unknown'}
EXACT={'value':'2026-12-01','precision':'exact'}
COMPANY='company:independent-stage3'

class IndependentMemoryAttacks(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.store=SQLiteStore(Path(self.tmp.name)/'memory.db')
        _,prepared=ap_control();self.case=prepared.case
        self.store.save(self.case,COMPANY,[],0);self.memory=CompanyMemory(self.store)
        self.dim=applicability(self.case,self.case.scope_id,[self.case.period_id])
        self.record=self.memory.capture(COMPANY,self.case.id,self.case.id,0,category='reporting_profile',subject='framework',assertion='USER_STATED',bundle_ids=list(self.case.governance.evidence_bundles),result_versions=list(self.case.governance.versions.versions),dimensions=self.dim,effective_from=EXACT,effective_to=UNKNOWN,learned_at=EXACT,expected_revision=0,material=True,reusable=True)
    def tearDown(self):self.store.close();self.tmp.cleanup()
    def governance(self,target='DOCUMENTED'):
        return dict(intent='EXPLICIT_MEMORY_TRANSITION',prior_status='PROPOSED',target_status=target,record_id=self.record['record_id'],applicability=self.dim,authority='TRUSTED_CALLER_ASSERTION',evidence_kind='SYNTHETIC',bundle_ids=self.record['source']['bundle_ids'],reason='Explicit synthetic documentary assertion, not authentication',decision_date=UNKNOWN,approval_date=UNKNOWN,authenticated=False)
    def test_proposal_not_current_context(self):
        result=self.memory.retrieve(COMPANY,self.case.id,self.case.id,'framework','framework')
        self.assertEqual(result['qualified'],[]);self.assertTrue(result['refused'])
    def test_unknown_company_cannot_retrieve(self):
        with self.assertRaises(IntegrityError):self.memory.retrieve('company:other',self.case.id,self.case.id,'framework','framework')
    def test_unknown_historical_consumption_version_rejected(self):
        self.record=self.memory.transition(COMPANY,self.record['record_id'],self.governance(),expected_revision=1,recorded_at=EXACT)
        self.memory.consume_context(COMPANY,self.case.id,self.case.id,self.record['record_id'],self.record['version_id'],expected_revision=2,recorded_at=EXACT)
        db=self.store.connection
        row=db.execute('SELECT payload,previous_sha256 FROM memory_events WHERE sequence=3').fetchone()
        from orchestration.persistence.codec import loads
        event=loads(row[0]);event['previous_version']='memory-version:never-existed';event['value']['memory_version']=event['previous_version']
        wire=dumps(event);checksum=sha(wire)
        db.execute('UPDATE memory_events SET payload=?,sha256=?,event_id=? WHERE sequence=3',(wire,checksum,ident('memory-event',event)))
        db.execute('UPDATE memory_heads SET sha256=?',(checksum,))
        with self.assertRaises(IntegrityError):self.memory.audit(COMPANY)
    def test_unknown_consuming_case_in_history_rejected(self):
        self.record=self.memory.transition(COMPANY,self.record['record_id'],self.governance(),expected_revision=1,recorded_at=EXACT)
        self.memory.consume_context(COMPANY,self.case.id,self.case.id,self.record['record_id'],self.record['version_id'],expected_revision=2,recorded_at=EXACT)
        db=self.store.connection
        from orchestration.persistence.codec import loads
        event=loads(db.execute('SELECT payload FROM memory_events WHERE sequence=3').fetchone()[0])
        event['value']['root_case']='case:never-existed';event['value']['case_id']='case:never-existed'
        wire=dumps(event);checksum=sha(wire)
        db.execute('UPDATE memory_events SET payload=?,sha256=?,event_id=? WHERE sequence=3',(wire,checksum,ident('memory-event',event)))
        db.execute('UPDATE memory_heads SET sha256=?',(checksum,))
        with self.assertRaises(IntegrityError):self.memory.audit(COMPANY)
    def test_supersession_cannot_use_self_as_successor(self):
        self.record=self.memory.transition(COMPANY,self.record['record_id'],self.governance(),expected_revision=1,recorded_at=EXACT)
        g=self.governance('SUPERSEDED');g['prior_status']='DOCUMENTED'
        with self.assertRaises(IntegrityError):self.memory.transition(COMPANY,self.record['record_id'],g,expected_revision=2,recorded_at=EXACT,successor=self.record['record_id'])

if __name__=='__main__':unittest.main()

class IndependentExtractedMemoryAttacks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from orchestration.tests.persistence_stage3_fixtures import build
        cls.case=build()
    def setUp(self):
        from orchestration.tests.persistence_stage3_fixtures import capture,COMPANY as C
        self.company=C;self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'memory.db';self.store=SQLiteStore(self.path)
        self.store.save(self.case,C,[],0);self.memory=self.store.memory();self.record=capture(self.store,self.case)
    def tearDown(self):self.store.close();self.tmp.cleanup()
    def transition(self,**changes):
        from orchestration.tests.persistence_stage3_fixtures import governance,LEARNED
        g=governance(self.record);g.update(changes)
        return self.memory.transition(self.company,self.record['record_id'],g,expected_revision=1,recorded_at=LEARNED)
    def test_documentary_approval_cannot_use_ordinary_system_source(self):
        with self.assertRaises(IntegrityError):self.transition(target_status='APPROVED',evidence_kind='DOCUMENTARY')
    def test_synthetic_authority_cannot_claim_authentication(self):
        with self.assertRaises(IntegrityError):self.transition(target_status='APPROVED',authenticated=True)
    def test_explicit_intent_required(self):
        with self.assertRaises(IntegrityError):self.transition(intent='MODEL_SAYS_APPROVED')
    def test_empty_governance_sources_refused(self):
        with self.assertRaises(IntegrityError):self.transition(bundle_ids=[])
    def test_candidate_cannot_assert_approved_decision_without_governance(self):
        from orchestration.tests.persistence_stage3_fixtures import capture
        decision=copy.deepcopy(self.record['decision']);decision['status']='approved'
        with self.assertRaises(IntegrityError):capture(self.store,self.case,subject='finance-approved-decision',decision=decision)
    def test_source_semantic_assertion_cannot_be_rewritten(self):
        from orchestration.tests.persistence_stage3_fixtures import capture
        with self.assertRaises(IntegrityError):capture(self.store,self.case,assertion='APPROVED_POLICY')
    def test_wrong_framework_cannot_be_captured(self):
        from orchestration.tests.persistence_stage3_fixtures import capture
        d=copy.deepcopy(self.record['applicability']);d['framework']='US_GAAP'
        with self.assertRaises(IntegrityError):capture(self.store,self.case,dimensions=d)
    def test_wrong_calendar_cannot_be_captured(self):
        from orchestration.tests.persistence_stage3_fixtures import capture
        d=copy.deepcopy(self.record['applicability']);d['calendar_id']='fabricated'
        with self.assertRaises(IntegrityError):capture(self.store,self.case,dimensions=d)
    def test_unknown_date_cannot_carry_fabricated_value(self):
        from orchestration.tests.persistence_stage3_fixtures import capture
        with self.assertRaises(IntegrityError):capture(self.store,self.case,learned_at=dict(value='2026-01-01',precision='unknown'))
    def test_inverted_effective_dates_refused(self):
        from orchestration.tests.persistence_stage3_fixtures import capture
        with self.assertRaises(IntegrityError):capture(self.store,self.case,effective_from=dict(value='2027-01-01',precision='exact'))
    def test_capture_cannot_drop_source_evidence(self):
        from orchestration.tests.persistence_stage3_fixtures import capture
        with self.assertRaises(IntegrityError):capture(self.store,self.case,bundle_ids=[])
    def test_two_connections_stale_writer_cannot_add_transition(self):
        from orchestration.tests.persistence_stage3_fixtures import governance,LEARNED
        from orchestration.persistence import RevisionConflict
        self.transition()
        with SQLiteStore(self.path) as other:
            g=governance(self.record,target='CONFIRMED')
            with self.assertRaises((IntegrityError,RevisionConflict)):other.memory().transition(self.company,self.record['record_id'],g,expected_revision=1,recorded_at=LEARNED)
        self.assertEqual(self.memory.audit(self.company)['revision'],2)
    def test_public_native_answer_does_not_expose_memory_ledger(self):
        from orchestration.runtime import CAO
        self.transition();public=dumps(CAO().public(self.case))
        for key in ('memory_events','memory_governance','TRUSTED_CALLER_ASSERTION',self.record['record_id']):self.assertNotIn(key,public)
    def test_lost_ack_retry_keeps_exact_transition(self):
        from orchestration.tests.persistence_stage3_fixtures import governance,LEARNED
        r=self.transition()
        again=self.memory.transition(self.company,self.record['record_id'],governance(self.record),expected_revision=1,recorded_at=LEARNED)
        self.assertEqual(r,again);self.assertEqual(self.memory.audit(self.company)['revision'],2)

class IndependentApprovalSemantics(unittest.TestCase):
    def test_negative_documentary_wording_never_approves(self):
        from unittest.mock import patch
        from orchestration.intake import RawSource
        from orchestration.tests.persistence_stage3_fixtures import build,capture,governance,COMPANY,LEARNED
        def negative_source(*args,**kwargs):
            raw=RawSource(*args,**kwargs)
            if raw.id=='governance':
                payload=copy.deepcopy(raw.payload)
                payload[0]['memory_governance']='NOT '+payload[0]['memory_governance']
                return RawSource(raw.id,raw.name,raw.format,payload,raw.metadata)
            return raw
        with patch('orchestration.tests.persistence_stage3_fixtures.RawSource',side_effect=negative_source):case=build(approval=True)
        with tempfile.TemporaryDirectory() as path,SQLiteStore(Path(path)/'memory.db') as store:
            store.save(case,COMPANY,[],0);r=capture(store,case)
            with self.assertRaises(IntegrityError):store.memory().transition(COMPANY,r['record_id'],governance(r,'APPROVED','DOCUMENTARY'),expected_revision=1,recorded_at=LEARNED)
    def test_inferred_claim_cannot_be_relabeled_as_source_fact(self):
        from orchestration.tests.persistence_stage3_fixtures import build,capture,COMPANY
        case=build(semantic='INFERRED')
        with tempfile.TemporaryDirectory() as path,SQLiteStore(Path(path)/'memory.db') as store:
            store.save(case,COMPANY,[],0)
            with self.assertRaises(IntegrityError):capture(store,case,assertion='SOURCE_FACT')
    def test_inferred_candidate_retained_but_cannot_be_approved(self):
        from orchestration.tests.persistence_stage3_fixtures import build,capture,governance,COMPANY,LEARNED
        case=build(semantic='INFERRED',approval=True)
        with tempfile.TemporaryDirectory() as path,SQLiteStore(Path(path)/'memory.db') as store:
            store.save(case,COMPANY,[],0);r=capture(store,case,assertion='INFERRED')
            self.assertEqual(r['status'],'PROPOSED')
            with self.assertRaises(IntegrityError):store.memory().transition(COMPANY,r['record_id'],governance(r,'APPROVED','DOCUMENTARY'),expected_revision=1,recorded_at=LEARNED)
