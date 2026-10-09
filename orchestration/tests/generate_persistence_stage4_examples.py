"""Connected Group accounting/memory/recovery proof, fresh OS processes throughout."""
import base64
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch
from orchestration.persistence import SQLiteStore, snapshot, IntegrityError
from orchestration.persistence.codec import dumps, loads
from orchestration.runtime import CAO
from orchestration.tests.persistence_stage4_fixtures import *
TARGET=Path(__file__).resolve().parents[1]/'examples/full-durable-cao-integration'


def envelope(value):
    wire=dumps(value).encode();compressed=bytearray(gzip.compress(wire,mtime=0));compressed[9]=255
    return dict(encoding='gzip-base64 canonical audit JSON',sha256=hashlib.sha256(wire).hexdigest(),payload=base64.b64encode(compressed).decode())


def root_id(store):
    return store.connection.execute('SELECT case_id FROM heads WHERE company_id=? ORDER BY case_id',(COMPANY,)).fetchall()


def phase(path,action):
    with SQLiteStore(path) as s:
        m=s.memory()
        if action=='company':
            f=initial(systems='NetSuite');negative=dict(checkpoint=envelope(snapshot(f['case'],COMPANY,CONTEXT)),public=CAO().public(f['case']))
            assert negative['public']['status']!='complete' and f['case'].status!='CLOSED'
            f,record=finish(f);a=f['case'];s.save(a,COMPANY,CONTEXT,0);candidate=capture(s,a)
            assert candidate['status']=='PROPOSED'
            return dict(objective=a.objective,root=a.id,candidate=candidate,initial_negative=negative,corrections=record['closing_correction'],checkpoint=envelope(snapshot(a,COMPANY,CONTEXT)),current=native_invariants(a),intake_candidate_preserved=True)
        audit=m.audit(COMPANY);original=next(r for r in audit['company_context'] if r['subject']=='finance' and r['value']=='NetSuite')
        root=original['source']['root_case'];a,rev,ctx=s.load(COMPANY,root)
        if action=='promote':
            refused=m.retrieve(COMPANY,root,root,'finance','systems');assert not refused['qualified']
            r=m.transition(COMPANY,original['record_id'],governance(original),expected_revision=audit['revision'],recorded_at=LEARNED)
            return dict(proposed_refusal=refused,documented=r,authenticated=False,history=m.history(COMPANY,r['record_id']))
        if action in {'reuse','reuse-successor'}:
            source=original if action=='reuse' else next(r for r in audit['company_context'] if r['subject']=='finance' and r['status']=='DOCUMENTED')
            objective=REUSE_OBJECTIVE if action=='reuse' else REUSE_OBJECTIVE+' Confirm the separately corrected company-system context.'
            f=initial(objective,memory=memory_request(m,source['source']['root_case']));assert not any(q.get('attribute')=='systems' for q in f['intake'].questions)
            f,record=finish(f);b=f['case'];s.save(b,COMPANY,CONTEXT,0)
            use=m.consume_context(COMPANY,b.id,b.id,source['record_id'],source['version_id'],expected_revision=m.audit(COMPANY)['revision'],recorded_at=LEARNED)
            assert f['session'].context['systems']==source['value']
            assert all(edge.producer_case!=root for edge in b.governance.edges.values())
            return dict(root=b.id,context=source['value'],references=f['memory_references'],use=use,no_memory_financial_edge=True,checkpoint=envelope(snapshot(b,COMPANY,CONTEXT)),current=native_invariants(b))
        if action=='periods':
            period=attach(a)['nodes']['adjacent-closing'].period_id
            key=s.prepare(a,COMPANY,ctx,rev,dict(kind='CLOSE_PERIOD',period_id=period));a,r=s.recover(COMPANY,root,key)
            try:s.prepare(a,COMPANY,ctx,r['head_revision'],correction_intent(a))
            except ValueError:pass
            else:raise AssertionError('Unauthorized closed correction accepted')
            key=s.prepare(a,COMPANY,ctx,r['head_revision'],reopening(a,period));a,r=s.recover(COMPANY,root,key)
            return dict(unauthorized_refused=True,reopening=r,checkpoint=envelope(snapshot(a,COMPANY,ctx)))
        if action=='correction':
            before=snapshot(a,COMPANY,ctx);key=s.prepare(a,COMPANY,ctx,rev,correction_intent(a));a,r=s.recover(COMPANY,root,key)
            result=m.retrieve(COMPANY,root,root,'finance','systems');assert not result['qualified'] and any('supporting-result-STALE' in x['reasons'] for x in result['refused'])
            assert CAO().public(a)['status']!='complete'
            return dict(operation=r,before=envelope(before),checkpoint=envelope(snapshot(a,COMPANY,ctx)),memory_refusal=result,public=CAO().public(a))
        if action in {'interrupt','resume'}:
            latest=s.connection.execute('SELECT operation_id FROM operations WHERE company_id=? AND case_id=? ORDER BY prepared_revision DESC',(COMPANY,root)).fetchone()[0]
            operation=s.operation(COMPANY,root,latest)
            if action=='interrupt':
                plan=operation['events'][-1]['value']['result'];key=s.prepare(a,COMPANY,ctx,rev,rework_intent(a,plan))
                def die(name,*args):
                    if name=='after_native':os._exit(73)
                with patch('orchestration.persistence.recovery._phase',side_effect=die):s.recover(COMPANY,root,key)
                raise AssertionError('Producer survived controlled exit')
            before=s.operation(COMPANY,root,latest);assert before['status']=='EXECUTING'
            a,r=s.recover(COMPANY,root,latest);assert a.status=='CLOSED'
            memory=m.retrieve(COMPANY,root,root,'finance','systems');assert not memory['qualified']
            return dict(prepared=before,recovered=r,checkpoint=envelope(snapshot(a,COMPANY,ctx)),current=native_invariants(a),memory_refusal=memory)
        if action=='reclose':
            period=attach(a)['nodes']['adjacent-closing'].period_id
            key=s.prepare(a,COMPANY,ctx,rev,dict(kind='CLOSE_PERIOD',period_id=period));a,r=s.recover(COMPANY,root,key)
            return dict(operation=r,checkpoint=envelope(snapshot(a,COMPANY,ctx)))
        if action=='lost-ack':
            key=s.prepare(a,COMPANY,ctx,rev,journal_intent(a))
            def die(name,*args):
                if name=='after_commit':os._exit(74)
            with patch('orchestration.persistence.recovery._phase',side_effect=die):s.recover(COMPANY,root,key)
            raise AssertionError('Committed producer acknowledgement was not lost')
        if action=='repeat':
            key=s.connection.execute('SELECT operation_id FROM operations WHERE company_id=? AND case_id=? ORDER BY prepared_revision DESC',(COMPANY,root)).fetchone()[0]
            before=dumps(snapshot(a,COMPANY,ctx));r0=s.operation(COMPANY,root,key);assert r0['status']=='COMMITTED'
            with patch.object(CAO,'execute_versioned_owner',side_effect=AssertionError('Committed retry executed owner')):
                a,r=s.recover(COMPANY,root,key)
            assert before==dumps(snapshot(a,COMPANY,ctx));assert len(r['events'][-1]['value']['result']['selected'])==8
            return dict(operation=r,checkpoint=envelope(snapshot(a,COMPANY,ctx)),current=native_invariants(a),no_repeat_execution=True)
        if action=='successor':
            # New independent sealed company evidence; inherited memory is never
            # reclassified as extracted documentary truth.
            f=initial(OBJECTIVE+' Review separately supplied corrected company finance-system evidence.',systems='Xero');f,record=finish(f);c=f['case'];s.save(c,COMPANY,CONTEXT,0)
            candidate=capture(s,c,supersedes=[original['record_id']]);assert candidate['status']=='PROPOSED'
            refused=m.retrieve(COMPANY,c.id,c.id,'finance','systems');assert refused['conflicts'] and not refused['qualified']
            try:m.transition(COMPANY,candidate['record_id'],governance(candidate),expected_revision=m.audit(COMPANY)['revision'],recorded_at=LEARNED)
            except IntegrityError:pass
            else:raise AssertionError('Contradiction silently promoted')
            intent=governance(candidate);alternatives={original['record_id']:governance(original,'SUPERSEDED')};expected=m.audit(COMPANY)['revision']
            r=m.resolve_conflict(COMPANY,candidate['record_id'],intent,alternatives,expected_revision=expected,recorded_at=LEARNED)
            assert r==m.resolve_conflict(COMPANY,candidate['record_id'],intent,alternatives,expected_revision=expected,recorded_at=LEARNED)
            return dict(root=c.id,candidate=candidate,blocked=refused,resolved=r,audit=m.audit(COMPANY),checkpoint=envelope(snapshot(c,COMPANY,CONTEXT)))
        if action=='unresolved':
            successor=next(r for r in audit['company_context'] if r['subject']=='finance' and r['status']=='DOCUMENTED');c,_,_=s.load(COMPANY,successor['source']['root_case'])
            first=capture(s,c,subject='unresolved-control');first=m.transition(COMPANY,first['record_id'],governance(first),expected_revision=m.audit(COMPANY)['revision'],recorded_at=LEARNED)
            candidate=capture(s,a,subject='unresolved-control');refusal=m.retrieve(COMPANY,root,root,'unresolved-control','systems');assert refusal['conflicts'] and not refusal['qualified']
            assert m.retrieve(COMPANY,root,root,'finance','systems')['qualified']
            # The unresolved contextual subject never fabricates accounting closure
            # or invalidates unrelated current native financial dependencies.
            return dict(first=first,candidate=candidate,refusal=refusal,outcome='BLOCKED_CONTEXT',public=CAO().public(a),unrelated_accounting_current=True)
        if action=='restore':
            with patch.object(CAO,'run',side_effect=AssertionError('Restoration executed runtime')),patch.object(CAO,'execute_versioned_owner',side_effect=AssertionError('Restoration executed owner')):
                audit=m.audit(COMPANY);assert len(audit['uses'])==2
                roots=[]
                for (key,) in root_id(s):
                    c,_,context=s.load(COMPANY,key);roots.append(dict(root=key,checkpoint=envelope(snapshot(c,COMPANY,context)),public=CAO().public(c)))
            assert all(x['public']['status']=='complete' for x in roots)
            return dict(result='PASS',audit=audit,roots=roots,current=native_invariants(a),qualified=m.retrieve(COMPANY,root,root,'finance','systems'),historical_original=m.history(COMPANY,original['record_id']),authenticated=False,external_posting=False)
        raise ValueError(action)


def artifacts(log_directory=None):
    actions=['company','promote','reuse','periods','correction','interrupt','resume','reclose','lost-ack','repeat','successor','reuse-successor','unresolved','restore'];out={}
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp)/'company.db'
        for action in actions:
            child=subprocess.run([sys.executable,'-m','orchestration.tests.generate_persistence_stage4_examples','--phase',str(path),action],capture_output=True,text=True,timeout=600)
            expected={'interrupt':73,'lost-ack':74}.get(action,0)
            if log_directory:
                dest=Path(log_directory);dest.mkdir(parents=True,exist_ok=True);(dest/(action+'.stderr')).write_text(child.stderr);(dest/(action+'.exit')).write_text(str(child.returncode)+'\n')
            if child.returncode!=expected:raise RuntimeError(action+': '+child.stderr)
            if expected:out[action+'.json']=dict(actual_exit=child.returncode,producer_terminated=True,boundary='after native before commit' if action=='interrupt' else 'after durable commit before acknowledgement')
            else:out[action+'.json']=envelope(loads(child.stdout.strip()))
            if log_directory:
                # Retain each completed lossless proof before the next expensive
                # process; a later failure cannot erase these successful states.
                (Path(log_directory)/(action+'.envelope.json')).write_text(json.dumps(out[action+'.json'],sort_keys=True,indent=2)+'\n')
    out['proof-summary.json']=dict(result='PASS',fresh_processes=len(actions),schema=3,checkpoint_contract=1,native_group_cash='490',native_group_profit='3',current_journals=8,context_only_no_financial_edges=True,actual_source_dependency_rework=True,producer_exit=73,lost_ack_exit=74,independent_review='separate release gate',authenticated_approval=False,external_erp_posting=False)
    return out


def main():
    if len(sys.argv)>1 and sys.argv[1]=='--phase':print(dumps(phase(sys.argv[2],sys.argv[3])));return
    target=Path(sys.argv[1]) if len(sys.argv)>1 else TARGET;target.mkdir(parents=True,exist_ok=True)
    for name,value in artifacts(os.environ.get('DURABLE_STAGE4_LOG_DIRECTORY')).items():(target/name).write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':main()
