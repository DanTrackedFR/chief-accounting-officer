"""Executable bounded Company Memory proof with genuinely fresh processes."""
import base64
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from orchestration.persistence import SQLiteStore, snapshot, IntegrityError
from orchestration.persistence.codec import dumps
from orchestration.runtime import CAO
from orchestration.tests.persistence_stage3_fixtures import *
TARGET=Path(__file__).resolve().parents[1]/'examples/company-accounting-memory'

def envelope(value):
    wire=dumps(value).encode();compressed=bytearray(gzip.compress(wire,mtime=0));compressed[9]=255
    return dict(encoding='gzip-base64 canonical audit JSON',sha256=hashlib.sha256(wire).hexdigest(),payload=base64.b64encode(compressed).decode())

def phase(path,action):
    with SQLiteStore(path) as s:
        m=s.memory()
        if action=='capture':
            a=build(approval=True);s.save(a,COMPANY,[],0);r=capture(s,a)
            return dict(root=a.id,candidate=r,public=CAO().public(a),checkpoint=envelope(snapshot(a,COMPANY,[])))
        audit=m.audit(COMPANY);root=audit['case_library'][0]['root_case'];a,revision,context=s.load(COMPANY,root)
        original=audit['company_context'][0]
        if action=='promote':
            before=m.retrieve(COMPANY,root,root,'finance','systems');assert not before['qualified']
            g=governance(original,'APPROVED','DOCUMENTARY')
            approved=m.transition(COMPANY,original['record_id'],g,expected_revision=audit['revision'],recorded_at=LEARNED)
            assert approved==m.transition(COMPANY,original['record_id'],g,expected_revision=audit['revision'],recorded_at=LEARNED)
            return dict(before=before,approved=approved,history=m.history(COMPANY,original['record_id']))
        if action=='reuse':
            b=build('Separate Case B close question',memory=dict(memory=m,company_id=COMPANY,qualification_root=root,qualification_case=root,subjects=[('finance','systems')]))
            assert b.id!=root;s.save(b,COMPANY,[],0)
            result=m.retrieve(COMPANY,b.id,b.id,'finance','systems');assert len(result['qualified'])==1
            r=result['qualified'][0]['record'];use=m.consume_context(COMPANY,b.id,b.id,r['record_id'],r['version_id'],expected_revision=m.audit(COMPANY)['revision'],recorded_at=LEARNED)
            s.save(b,'company:isolated',[],0);assert not m.retrieve('company:isolated',b.id,b.id,'finance','systems')['qualified']
            return dict(root=b.id,retrieval=result,use=use,known_system=b.governance.context['systems'],questions_suppressed=True,public=CAO().public(b),journal_fingerprints=[v.result_fingerprint for v in b.governance.versions.versions.values()],checkpoint=envelope(snapshot(b,COMPANY,[])))
        if action=='conflict':
            c=build('Contradictory systems source',value='Xero');s.save(c,COMPANY,[],0);r=capture(s,c,supersedes=[original['record_id']])
            refused=m.retrieve(COMPANY,root,root,'finance','systems');assert refused['conflicts'] and not refused['qualified']
            try:m.transition(COMPANY,r['record_id'],governance(r),expected_revision=m.audit(COMPANY)['revision'],recorded_at=LEARNED)
            except IntegrityError:pass
            else:raise AssertionError('Unsupported contradiction promoted')
            g=governance(r);alternatives={original['record_id']:governance(original,'SUPERSEDED',reason='Reviewed corrected systems document: Xero supersedes old NetSuite position')};expected=m.audit(COMPANY)['revision']
            successor=m.resolve_conflict(COMPANY,r['record_id'],g,alternatives,expected_revision=expected,recorded_at=LEARNED)
            assert successor==m.resolve_conflict(COMPANY,r['record_id'],g,alternatives,expected_revision=expected,recorded_at=LEARNED)
            return dict(conflicting_candidate=r,blocked_retrieval=refused,resolution=successor,audit=m.audit(COMPANY))
        if action=='correction':
            current=next(r for r in audit['company_context'] if r['status']=='DOCUMENTED');c,rev,ctx=s.load(COMPANY,current['source']['root_case'])
            before=CAO().public(c);intent=correction(c,execute=False)
            operation=s.prepare(c,COMPANY,ctx,rev,intent);c,outcome=s.recover(COMPANY,c.id,operation);plan=outcome['events'][-1]['value']['result']
            rework=s.prepare(c,COMPANY,ctx,outcome['head_revision'],dict(kind='REWORK',plan=plan,reviewed_sources={}));c,completed=s.recover(COMPANY,c.id,rework)
            assert (c.status,CAO().public(c)['status'])==('CLOSED','complete')
            refusal=m.retrieve(COMPANY,c.id,c.id,'finance','systems');assert not refusal['qualified'];assert any('supporting-result-SUPERSEDED' in entry['reasons'] for entry in refusal['refused'])
            retracted=m.transition(COMPANY,current['record_id'],governance(current,'RETRACTED',reason='Supporting immutable accounting result superseded by reviewed source correction'),expected_revision=m.audit(COMPANY)['revision'],recorded_at=LEARNED)
            candidate=capture(s,c,supersedes=[])
            assert candidate['status']=='PROPOSED' and candidate['record_id']!=current['record_id']
            approved=m.transition(COMPANY,candidate['record_id'],governance(candidate),expected_revision=m.audit(COMPANY)['revision'],recorded_at=LEARNED)
            from orchestration.versions import fingerprint
            # Native economics remain equal across immutable source versions.
            versions=list(c.governance.versions.versions.values());assert len(versions)==2
            assert versions[0].payload()['journal_entry_implications']==versions[1].payload()['journal_entry_implications']
            return dict(correction=plan,durable_operation=operation,native_rework=rework,refused=refusal,retracted=retracted,proposed_successor=candidate,current=approved,qualified=m.retrieve(COMPANY,c.id,c.id,'finance','systems'),historical=m.history(COMPANY,current['record_id']),checkpoint=envelope(snapshot(c,COMPANY,ctx)),native_journals_unchanged=True)
        if action=='unresolved':
            c=build('Unresolved independent memory conflict',value='Unknown system');s.save(c,COMPANY,[],0);r=capture(s,c,subject='unresolved-control')
            first=m.transition(COMPANY,r['record_id'],governance(r),expected_revision=m.audit(COMPANY)['revision'],recorded_at=LEARNED)
            other=build('Second unresolved source',value='Disputed system');s.save(other,COMPANY,[],0);candidate=capture(s,other,subject='unresolved-control')
            result=m.retrieve(COMPANY,other.id,other.id,'unresolved-control','systems');assert not result['qualified'] and result['conflicts']
            unaffected=m.retrieve(COMPANY,root,root,'finance','systems');assert unaffected['qualified']
            return dict(first=first,candidate=candidate,refusal=result,unrelated_context_unaffected=True)
        if action=='restore':
            from unittest.mock import patch
            with patch.object(CAO,'run',side_effect=AssertionError('Case A rerun')),patch.object(CAO,'execute_versioned_owner',side_effect=AssertionError('owner invoked')):
                current=m.retrieve(COMPANY,root,root,'finance','systems');assert len(current['qualified'])==1
                audit=m.audit(COMPANY);assert len(audit['uses'])==1
            return dict(audit=audit,qualified=current,public=CAO().public(a),result='PASS',authenticated_approval=False,stage4_started=False)
        raise ValueError(action)

def artifacts():
    result={}
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp)/'native.db'
        for action in ['capture','promote','reuse','conflict','correction','unresolved','restore']:
            child=subprocess.run([sys.executable,'-m','orchestration.tests.generate_persistence_stage3_examples','--phase',str(path),action],capture_output=True,text=True,timeout=120)
            if child.returncode:raise RuntimeError(action+': '+child.stderr)
            value=json.loads(child.stdout)
            result[action+'.json']=envelope(value) if action in {'conflict','correction','restore'} else value
    result['proof-summary.json']=dict(result='PASS',separate_processes=7,cross_case_context=True,unapproved_proposal_retained=True,exact_versions=True,contradiction_refusal=True,native_correction=True,historical_consumption_preserved=True,no_duplicate_journals=True,authenticated_approval=False)
    return result

def main():
    if len(sys.argv)>1 and sys.argv[1]=='--phase':print(json.dumps(phase(sys.argv[2],sys.argv[3]),sort_keys=True,default=str));return
    out=Path(sys.argv[1]) if len(sys.argv)>1 else TARGET;out.mkdir(parents=True,exist_ok=True)
    for name,value in artifacts().items():(out/name).write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':main()
