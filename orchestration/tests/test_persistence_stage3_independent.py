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
    def test_valid_context_consumption_remains_readable(self):
        self.record=self.memory.transition(COMPANY,self.record['record_id'],self.governance(),expected_revision=1,recorded_at=EXACT)
        self.memory.consume_context(COMPANY,self.case.id,self.case.id,self.record['record_id'],self.record['version_id'],expected_revision=2,recorded_at=EXACT)
        audit=self.memory.audit(COMPANY)
        self.assertEqual(audit['revision'],3);self.assertEqual(len(audit['uses']),1)
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
    def test_restored_supersession_must_validate_successor_lineage(self):
        self.record=self.memory.transition(COMPANY,self.record['record_id'],self.governance(),expected_revision=1,recorded_at=EXACT)
        db=self.store.connection
        from orchestration.persistence.codec import loads
        oldevent=loads(db.execute('SELECT payload FROM memory_events WHERE sequence=2').fetchone()[0])
        record=copy.deepcopy(self.record);record['status']='SUPERSEDED';record['superseded_by']=record['record_id']
        g=self.governance('SUPERSEDED');g['prior_status']='DOCUMENTED';record['governance']=g
        record['version_id']=ident('memory-version',{k:v for k,v in record.items() if k!='version_id'})
        event=dict(contract=1,company_id=COMPANY,kind='TRANSITION',record_id=record['record_id'],previous_version=self.record['version_id'],value=record,reason='Hostile rewritten supersession',recorded_at=EXACT)
        wire=dumps(event);checksum=sha(wire)
        previous=db.execute('SELECT sha256 FROM memory_events WHERE sequence=2').fetchone()[0]
        db.execute('INSERT INTO memory_events VALUES(?,?,?,?,?,?)',(COMPANY,3,ident('memory-event',event),wire,checksum,previous))
        db.execute('UPDATE memory_heads SET sequence=3,sha256=?',(checksum,))
        with self.assertRaises(IntegrityError):self.memory.audit(COMPANY)
    def test_supersession_cannot_use_self_as_successor(self):
        self.record=self.memory.transition(COMPANY,self.record['record_id'],self.governance(),expected_revision=1,recorded_at=EXACT)
        g=self.governance('SUPERSEDED');g['prior_status']='DOCUMENTED'
        with self.assertRaises(IntegrityError):self.memory.transition(COMPANY,self.record['record_id'],g,expected_revision=2,recorded_at=EXACT,successor=self.record['record_id'])


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
    def test_actual_competing_promotion_connections_publish_one_approved_position(self):
        import threading
        from orchestration.tests.persistence_stage3_fixtures import build,capture,governance,LEARNED
        other=build(objective='Competing independently observed same system')
        self.store.save(other,self.company,[],0);second=capture(self.store,other)
        barrier=threading.Barrier(2);outcomes=[]
        def writer(record):
            with SQLiteStore(self.path,timeout=20) as store:
                barrier.wait(timeout=20)
                try:
                    store.memory().transition(self.company,record['record_id'],governance(record,'APPROVED'),expected_revision=2,recorded_at=LEARNED);outcomes.append('published')
                except (IntegrityError,ValueError):outcomes.append('refused')
        workers=[threading.Thread(target=writer,args=(record,)) for record in (self.record,second)]
        for worker in workers:worker.start()
        for worker in workers:worker.join(timeout=30);self.assertFalse(worker.is_alive())
        self.assertEqual(sorted(outcomes),['published','refused'])
        self.assertEqual(sum(r['status']=='APPROVED' for r in self.memory.audit(self.company)['company_context']),1)
    def test_sqlite_interruption_rolls_back_entire_conflict_resolution(self):
        import sqlite3
        from orchestration.tests.persistence_stage3_fixtures import build,capture,governance,LEARNED
        old=self.transition();other=build(objective='Atomic reviewed replacement',value='Xero')
        self.store.save(other,self.company,[],0);new=capture(self.store,other,supersedes=[old['record_id']])
        self.store.connection.execute("CREATE TRIGGER interrupt_resolution BEFORE INSERT ON memory_events WHEN NEW.sequence=5 BEGIN SELECT RAISE(ABORT,'Injected durable interruption'); END")
        with self.assertRaises(sqlite3.IntegrityError):self.memory.resolve_conflict(self.company,new['record_id'],governance(new),{old['record_id']:governance(old,'SUPERSEDED')},expected_revision=3,recorded_at=LEARNED)
        self.store.connection.execute('DROP TRIGGER interrupt_resolution')
        audit=self.memory.audit(self.company);self.assertEqual(audit['revision'],3)
        states={r['record_id']:r['status'] for r in audit['company_context']}
        self.assertEqual(states[old['record_id']],'DOCUMENTED');self.assertEqual(states[new['record_id']],'PROPOSED')
    def test_planning_cannot_substitute_valid_other_fiscal_calendar_same_dates(self):
        from dataclasses import asdict
        from orchestration.periods import FiscalCalendar,Period,PeriodRegistry
        from orchestration.intake import Intake,FixturePlanner,StructuredProposal
        from orchestration.tests.intake_fixtures import SCOPE,cl
        self.transition()
        calendar=FiscalCalendar('independent-other-fiscal','Different fiscal year',7,1,('Explicit reviewed alternate calendar',))
        period=Period.create(calendar.calendar_id,'2026-12-01','2026-12-31',2027,'DEC',provenance=('Explicit reviewed alternate Period',))
        registry=copy.deepcopy(self.case.governance.periods.record());registry['calendars'].append(asdict(calendar));registry['periods'].append(dict(period.record(),status='OPEN'));registry['calendars'].sort(key=lambda row:row['calendar_id']);registry['periods'].sort(key=lambda row:row['period_id'])
        restored=PeriodRegistry.from_record(registry);self.assertEqual(restored.get(period.period_id).calendar_id,calendar.calendar_id)
        scope=copy.deepcopy(SCOPE);scope.update(calendar_id=calendar.calendar_id,reporting_calendar=calendar.calendar_id,period_id=period.period_id,period_registry=registry)
        planner=FixturePlanner(StructuredProposal(cl('Different fiscal review',status='USER_STATED'),cl('Context'),cl('REPORTING')))
        with self.assertRaises(IntegrityError):Intake(planner).prepare_with_memory('Different fiscal review',[],[],scope,self.memory,self.company,self.case.id,self.case.id,[('finance','systems')])
    def test_compound_resolution_is_idempotent_after_lost_ack(self):
        from orchestration.tests.persistence_stage3_fixtures import build,capture,governance,LEARNED
        old=self.transition();other=build(objective='Reviewed replacement system position',value='Xero')
        self.store.save(other,self.company,[],0);new=capture(self.store,other,supersedes=[old['record_id']])
        chosen_g=governance(new);alternatives={old['record_id']:governance(old,'SUPERSEDED')}
        chosen=self.memory.resolve_conflict(self.company,new['record_id'],chosen_g,alternatives,expected_revision=3,recorded_at=LEARNED)
        replay=self.memory.resolve_conflict(self.company,new['record_id'],chosen_g,alternatives,expected_revision=3,recorded_at=LEARNED)
        self.assertEqual(chosen,replay);self.assertEqual(self.memory.audit(self.company)['revision'],5)
    def test_restored_use_cannot_bypass_effective_period(self):
        from orchestration.tests.persistence_stage3_fixtures import capture,governance,LEARNED
        r=capture(self.store,self.case,subject='partial-period',effective_from=dict(value='2026-12-15',precision='exact'))
        r=self.memory.transition(self.company,r['record_id'],governance(r),expected_revision=2,recorded_at=LEARNED)
        self.assertEqual(self.memory.retrieve(self.company,self.case.id,self.case.id,'partial-period','systems')['qualified'],[])
        _,checksum=self.store._read(self.company,self.case.id,1)
        use=dict(root_case=self.case.id,case_id=self.case.id,case_revision=1,case_sha256=checksum,memory_version=r['version_id'],use='CONTEXT_ONLY',source_revision=1,source_sha256=checksum)
        event=dict(contract=1,company_id=self.company,kind='USE',record_id=r['record_id'],previous_version=r['version_id'],value=use,reason='Hostile partial-period use',recorded_at=LEARNED)
        db=self.store.connection;wire=dumps(event);checksum=sha(wire);previous=db.execute('SELECT sha256 FROM memory_events WHERE sequence=3').fetchone()[0]
        db.execute('INSERT INTO memory_events VALUES(?,?,?,?,?,?)',(self.company,4,ident('memory-event',event),wire,checksum,previous));db.execute('UPDATE memory_heads SET sequence=4,sha256=?',(checksum,))
        with self.assertRaises(IntegrityError):self.memory.audit(self.company)
    def test_restored_decision_cannot_claim_approval_on_documented_position(self):
        from orchestration.tests.persistence_stage3_fixtures import governance,LEARNED
        record=self.transition()
        changed=copy.deepcopy(record);changed['decision']['status']='approved';changed['governance']=governance(record)
        changed['version_id']=ident('memory-version',{k:v for k,v in changed.items() if k!='version_id'})
        event=dict(contract=1,company_id=self.company,kind='DECISION',record_id=record['record_id'],previous_version=record['version_id'],value=changed,reason='Hostile approved decision',recorded_at=LEARNED)
        db=self.store.connection;wire=dumps(event);checksum=sha(wire);previous=db.execute('SELECT sha256 FROM memory_events WHERE sequence=2').fetchone()[0]
        db.execute('INSERT INTO memory_events VALUES(?,?,?,?,?,?)',(self.company,3,ident('memory-event',event),wire,checksum,previous));db.execute('UPDATE memory_heads SET sequence=3,sha256=?',(checksum,))
        with self.assertRaises(IntegrityError):self.memory.audit(self.company)
    def test_planning_memory_use_cannot_substitute_equal_value_wrong_provenance(self):
        from orchestration.tests.persistence_stage3_fixtures import build,capture,governance,LEARNED
        old=self.transition()
        inherited=build(objective='Case planned from exact original system memory',memory=dict(memory=self.memory,company_id=self.company,qualification_root=self.case.id,qualification_case=self.case.id,subjects=[('finance','systems')]))
        self.store.save(inherited,self.company,[],0)
        replacement=build(objective='Independent equal-value system evidence')
        self.store.save(replacement,self.company,[],0);new=capture(self.store,replacement)
        self.memory.transition(self.company,old['record_id'],governance(old,'RETRACTED'),expected_revision=self.memory.audit(self.company)['revision'],recorded_at=LEARNED)
        new=self.memory.transition(self.company,new['record_id'],governance(new),expected_revision=self.memory.audit(self.company)['revision'],recorded_at=LEARNED)
        self.assertEqual(old['value'],new['value']);self.assertNotEqual(old['record_id'],new['record_id'])
        with self.assertRaises(IntegrityError):self.memory.consume_context(self.company,inherited.id,inherited.id,new['record_id'],new['version_id'],expected_revision=self.memory.audit(self.company)['revision'],recorded_at=LEARNED)
    def test_memory_derived_context_cannot_launder_into_independent_documented_truth(self):
        from orchestration.tests.persistence_stage3_fixtures import build,capture,governance,LEARNED
        old=self.transition()
        inherited=build(objective='Case inherits systems solely from qualified memory',memory=dict(memory=self.memory,company_id=self.company,qualification_root=self.case.id,qualification_case=self.case.id,subjects=[('finance','systems')]))
        self.store.save(inherited,self.company,[],0)
        # The new source archive contains AP evidence, no independent systems document.
        import json
        for bundle in inherited.governance.evidence_bundles.values():
            self.assertNotIn('system-policy',[json.loads(raw)['id'] for raw in bundle['raw_sources']])
        with self.assertRaises(IntegrityError):
            copied=capture(self.store,inherited,assertion='USER_STATED')
            self.memory.transition(self.company,copied['record_id'],governance(copied,kind='DOCUMENTARY'),expected_revision=self.memory.audit(self.company)['revision'],recorded_at=LEARNED)
        self.memory.transition(self.company,old['record_id'],governance(old,'RETRACTED'),expected_revision=self.memory.audit(self.company)['revision'],recorded_at=LEARNED)
        self.assertEqual(self.memory.retrieve(self.company,inherited.id,inherited.id,'finance','systems')['qualified'],[])
    def test_linked_decision_new_position_cannot_contradict_context_value(self):
        from orchestration.tests.persistence_stage3_fixtures import capture
        decision=copy.deepcopy(self.record['decision']);decision['new_position']='Different unsupported position'
        with self.assertRaises(IntegrityError):capture(self.store,self.case,subject='contradictory-decision',decision=decision)
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

class IndependentFreshProcessReuse(unittest.TestCase):
    def test_separate_case_reuses_exact_memory_after_two_process_restarts(self):
        import json
        import subprocess
        import sys
        from orchestration.tests.persistence_stage3_fixtures import build,capture,governance,COMPANY,LEARNED
        first=build(approval=True);second=build(objective='Separate unrelated closing review')
        self.assertNotEqual(first.id,second.id)
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'memory.db'
            with SQLiteStore(path) as store:
                store.save(first,COMPANY,[],0);r=capture(store,first)
                r=store.memory().transition(COMPANY,r['record_id'],governance(r,'APPROVED','DOCUMENTARY'),expected_revision=1,recorded_at=LEARNED)
                store.save(second,COMPANY,[],0)
            script='''import json,sys
from unittest.mock import patch
from orchestration.persistence import SQLiteStore
from orchestration.runtime import CAO
from orchestration.tests.persistence_stage3_fixtures import LEARNED
with patch.object(CAO,'run',side_effect=AssertionError('Case rerun')),patch.object(CAO,'execute_versioned_owner',side_effect=AssertionError('Native rerun')):
 with SQLiteStore(sys.argv[1]) as store:
  result=store.memory().retrieve(sys.argv[2],sys.argv[3],sys.argv[3],'finance','systems')
  r=result['qualified'][0]['record']
  store.memory().consume_context(sys.argv[2],sys.argv[3],sys.argv[3],r['record_id'],r['version_id'],expected_revision=2,recorded_at=LEARNED)
  print(json.dumps(dict(record=r['record_id'],version=r['version_id'],source=r['source']['case_id'],revision=store.memory().audit(sys.argv[2])['revision'])))
'''
            result=subprocess.run([sys.executable,'-c',script,str(path),COMPANY,second.id],capture_output=True,text=True,timeout=60)
            self.assertEqual(result.returncode,0,result.stderr);proof=json.loads(result.stdout)
            self.assertEqual(proof,dict(record=r['record_id'],version=r['version_id'],source=first.id,revision=3))
            final=subprocess.run([sys.executable,'-c','import json,sys;from orchestration.persistence import SQLiteStore;s=SQLiteStore(sys.argv[1]);a=s.memory().audit(sys.argv[2]);print(json.dumps({"revision":a["revision"],"uses":len(a["uses"])}));s.close()',str(path),COMPANY],capture_output=True,text=True,timeout=60)
            self.assertEqual(final.returncode,0,final.stderr);self.assertEqual(json.loads(final.stdout),dict(revision=3,uses=1))


class IndependentNativeSupportingCaseBoundary(unittest.TestCase):
    def test_existing_current_result_of_other_native_case_cannot_support_memory(self):
        from orchestration.tests.persistence_stage2_fixtures import baseline,COMPANY,CONTEXT
        f=baseline();case=f['case'];e=case.governance
        from orchestration.runtime import CAO
        e.context.update(entity=case.scope_id,framework=e.cases.scopes.get(case.scope_id).framework)
        CAO()._observe(case,e.context,{})
        candidate_index=next(i for i,c in enumerate(case.memory_candidates) if c['attribute']=='framework')
        foreign=next(k for k,v in e.versions.versions.items() if v.case_id!=case.id and e.versions.states[k]=='CURRENT')
        with tempfile.TemporaryDirectory() as folder,SQLiteStore(Path(folder)/'memory.db') as store:
            store.save(case,COMPANY,CONTEXT,0)
            with self.assertRaises(IntegrityError):store.memory().capture(COMPANY,case.id,case.id,candidate_index,category='reporting_profile',subject='reporting',assertion='USER_STATED',bundle_ids=list(e.evidence_bundles),result_versions=[foreign],dimensions=applicability(case,case.scope_id,[case.period_id]),effective_from=dict(value='2026-10-01',precision='exact'),effective_to=dict(value='2026-10-31',precision='exact'),learned_at=dict(value='2026-11-01',precision='exact'),expected_revision=0,material=True,reusable=True)

    def test_registered_relationship_of_other_period_cannot_qualify_memory(self):
        from orchestration.tests.persistence_stage2_fixtures import baseline,COMPANY,CONTEXT
        from orchestration.runtime import CAO
        f=baseline();case=f['case'];e=case.governance
        e.context.update(entity=case.scope_id,framework=e.cases.scopes.get(case.scope_id).framework);CAO()._observe(case,e.context,{})
        relation=next(r for r in e.periods.record()['relationships'] if case.period_id not in {r['source_period'],r['target_period']})
        candidate_index=next(i for i,c in enumerate(case.memory_candidates) if c['attribute']=='framework')
        with tempfile.TemporaryDirectory() as folder,SQLiteStore(Path(folder)/'memory.db') as store:
            store.save(case,COMPANY,CONTEXT,0)
            with self.assertRaises(IntegrityError):
                dims=applicability(case,case.scope_id,[case.period_id],relation['id'])
                store.memory().capture(COMPANY,case.id,case.id,candidate_index,category='reporting_profile',subject='reporting',assertion='USER_STATED',bundle_ids=list(e.evidence_bundles),result_versions=[],dimensions=dims,effective_from=dict(value='2026-10-01',precision='exact'),effective_to=dict(value='2026-10-31',precision='exact'),learned_at=dict(value='2026-11-01',precision='exact'),expected_revision=0,material=True,reusable=True)

    def test_registered_period_of_wrong_scope_calendar_cannot_qualify_memory(self):
        from orchestration.tests.persistence_stage2_fixtures import baseline,COMPANY,CONTEXT
        from orchestration.runtime import CAO
        f=baseline();case=f['case'];e=case.governance;scope=e.cases.scopes.get(case.scope_id)
        self.assertTrue(scope.reporting_calendar)
        wrong=next(p for p in e.periods.periods.values() if p.calendar_id!=scope.reporting_calendar)
        e.context.update(entity=case.scope_id,framework=scope.framework);CAO()._observe(case,e.context,{})
        candidate_index=next(i for i,c in enumerate(case.memory_candidates) if c['attribute']=='framework')
        with tempfile.TemporaryDirectory() as folder,SQLiteStore(Path(folder)/'memory.db') as store:
            store.save(case,COMPANY,CONTEXT,0)
            with self.assertRaises(IntegrityError):
                dims=applicability(case,case.scope_id,[wrong.period_id])
                store.memory().capture(COMPANY,case.id,case.id,candidate_index,category='reporting_profile',subject='reporting',assertion='USER_STATED',bundle_ids=list(e.evidence_bundles),result_versions=[],dimensions=dims,effective_from=dict(value=wrong.start,precision='exact'),effective_to=dict(value=wrong.end,precision='exact'),learned_at=dict(value='2026-11-01',precision='exact'),expected_revision=0,material=True,reusable=True)

if __name__=='__main__':unittest.main()
