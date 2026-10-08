"""Real SQLite and fresh-process interrupted/resumed native accounting proof."""
import hashlib
import base64
import gzip
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from orchestration.persistence.codec import dumps, loads

TARGET=Path(__file__).resolve().parents[1]/'examples/durable-rework-recovery'


def worker(path, action):
    from orchestration.persistence import SQLiteStore, snapshot
    from orchestration.tests.persistence_stage2_fixtures import baseline, correction_intent, rework_intent, journal_intent, reopening, attach, COMPANY, CONTEXT
    from orchestration.runtime import CAO
    from unittest.mock import patch
    with SQLiteStore(path) as store:
        if action=='baseline':
            f=baseline();case=f['case'];store.save(case,COMPANY,CONTEXT,0)
            return dict(checkpoint=snapshot(case,COMPANY,CONTEXT),public=CAO().public(case))
        case_id=store.connection.execute('SELECT case_id FROM heads WHERE company_id=?',(COMPANY,)).fetchone()[0]
        case,revision,context=store.load(COMPANY,case_id)
        if action=='correction':
            intent=correction_intent(case);key=store.prepare(case,COMPANY,context,revision,intent)
            case,record=store.recover(COMPANY,case_id,key)
            return dict(checkpoint=snapshot(case,COMPANY,context),operation=record)
        if action in ('interrupt','rework'):
            row=store.connection.execute('SELECT operation_id FROM operations WHERE company_id=? ORDER BY prepared_revision DESC',(COMPANY,)).fetchone()
            plan=store.operation(COMPANY,case_id,row[0])['events'][-1]['value']['result']
            intent=rework_intent(case,plan);key=store.prepare(case,COMPANY,context,revision,intent)
            # Native owners really execute, then process death occurs before the
            # outcome SQLite COMMIT. OS closes the writer; SQLite rolls back.
            def die(name,*args):
                if name=='after_native':
                    import os
                    os._exit(73)
            if action=='rework':
                case,record=store.recover(COMPANY,case_id,key)
                return dict(operation=record,checkpoint=snapshot(case,COMPANY,context),public=CAO().public(case))
            with patch('orchestration.persistence.recovery._phase',side_effect=die):store.recover(COMPANY,case_id,key)
            raise AssertionError('Controlled death did not occur')
        if action=='resume':
            key=store.connection.execute('SELECT operation_id FROM operations ORDER BY prepared_revision DESC').fetchone()[0]
            before=store.operation(COMPANY,case_id,key)
            case,record=store.recover(COMPANY,case_id,key)
            return dict(before_recovery=before,operation=record,checkpoint=snapshot(case,COMPANY,context),public=CAO().public(case))
        if action=='selection':
            key=store.prepare(case,COMPANY,context,revision,journal_intent(case))
            case,record=store.recover(COMPANY,case_id,key)
            return dict(operation=record,public=CAO().public(case),checkpoint=snapshot(case,COMPANY,context))
        if action=='repeat':
            key=store.connection.execute('SELECT operation_id FROM operations ORDER BY prepared_revision DESC').fetchone()[0]
            before=dumps(snapshot(case,COMPANY,context))
            with patch.object(CAO,'execute_versioned_owner',side_effect=AssertionError('Committed retry reexecuted accounting')):
                case,record=store.recover(COMPANY,case_id,key)
            if before!=dumps(snapshot(case,COMPANY,context)):raise AssertionError('Committed repeat changed governed state')
            return dict(operation=record,public=CAO().public(case),checkpoint=snapshot(case,COMPANY,context),no_repeat_execution=True)
        if action=='reclose':
            period=attach(case)['nodes']['adjacent-closing'].period_id
            key=store.prepare(case,COMPANY,context,revision,dict(kind='CLOSE_PERIOD',period_id=period))
            case,record=store.recover(COMPANY,case_id,key)
            return dict(operation=record,checkpoint=snapshot(case,COMPANY,context),public=CAO().public(case))
        if action=='periods':
            f=attach(case);period=f['nodes']['adjacent-closing'].period_id
            key=store.prepare(case,COMPANY,context,revision,dict(kind='CLOSE_PERIOD',period_id=period));case,r=store.recover(COMPANY,case_id,key)
            try:correction_intent(case)
            except ValueError:refused=True
            else:
                # Native intake does not execute. Native operation preparation
                # must refuse unauthorized closed-Period owner work.
                try:store.prepare(case,COMPANY,context,r['head_revision'],correction_intent(case))
                except ValueError:refused=True
                else:raise AssertionError('Closed period correction accepted')
            key=store.prepare(case,COMPANY,context,r['head_revision'],reopening(case,period));case,r=store.recover(COMPANY,case_id,key)
            return dict(operation=r,unauthorized_closed_correction_refused=refused,checkpoint=snapshot(case,COMPANY,context))
        raise ValueError(action)


def artifacts():
    def run(path,action,code=0):
        r=subprocess.run([sys.executable,'-m','orchestration.tests.generate_persistence_stage2_examples',path,action],capture_output=True,text=True)
        if r.returncode!=code:raise RuntimeError(action+': '+r.stderr)
        return loads(r.stdout.strip()) if code==0 else None
    with tempfile.TemporaryDirectory() as p:
        path=str(Path(p)/'proof.db');original=run(path,'baseline');corrected=run(path,'correction')
        run(path,'interrupt',73);resumed=run(path,'resume');selected=run(path,'selection');repeat=run(path,'repeat')
        periods=run(path,'periods');after_reopen=run(path,'correction');reclosed_work=run(path,'rework');reclosed=run(path,'reclose');reclosure_repeat=run(path,'repeat')
    if reclosed['checkpoint']!=reclosure_repeat['checkpoint'] or reclosed['public']!=reclosure_repeat['public']:raise AssertionError('Repeated reclosure recovery changed state')
    plan=corrected['operation']['events'][-1]['value']['result']
    old=original['checkpoint'];new=resumed['checkpoint']
    for key in plan['unaffected']:
        if old['active'][key]!=new['active'][key]:raise AssertionError('Unaffected owner reexecuted')
    for key,value in old['versions'].items():
        if new['versions'][key]!=value or new['source_snapshots'][key]!=old['source_snapshots'][key]:raise AssertionError('Immutable history changed')
    if resumed['public']['status']!='complete' or next(c for c in new['cases'] if c['id']==new['root_case'])['status']!='CLOSED':raise AssertionError('Native completion missing')
    if selected['public']!=repeat['public'] or selected['checkpoint']!=repeat['checkpoint']:raise AssertionError('Repeat recovery changed economics/output')
    if len(selected['operation']['events'][-1]['value']['result']['selected'])!=8:raise AssertionError('Native eight-journal inventory changed')
    # Separate genuinely unresolved accepted conflict, no overridden success.
    from orchestration.tests import stage4_temporal_fixtures as t
    from orchestration.persistence import SQLiteStore, snapshot
    from orchestration.tests.persistence_stage2_fixtures import COMPANY,CONTEXT
    from orchestration.runtime import CAO
    negative=t.intake_initial();c=negative['case']
    with tempfile.TemporaryDirectory() as p,SQLiteStore(Path(p)/'blocked.db') as s:
        s.save(c,COMPANY,CONTEXT,0);c,_,_=s.load(COMPANY,c.id)
        if c.outcome=='complete' or c.status=='CLOSED':raise AssertionError('Unresolved conflict manufactured success')
        blocked=dict(public=CAO().public(c),checkpoint=snapshot(c,COMPANY,CONTEXT))
    summary=dict(result='PASS',producer_terminated=True,fresh_processes=11,controlled_process_exit=73,
        interrupted_boundary='native selective rework executed, before durable outcome commit',
        recovery_unit='replay exact authorized native unit from prepared checkpoint; no partial owner state committed',
        exact_selective_order=plan['execution_order'],unaffected_versions_preserved=True,immutable_history_preserved=True,
        current_journal_count=8,closed_period_reopened_then_corrected_reworked_reclosed=True,internal_selection_only=True,external_posting_proved=False,
        resumed_public_complete=True,resumed_case_closed=True,repeat_recovery_identical=True,
        unresolved_control_outcome=c.outcome,synthetic_review=True,schema_version=2,checkpoint_contract=1)
    def archived(doc):
        wire=dumps(doc).encode();compressed=gzip.compress(wire,mtime=0)
        # Canonical platform-independent gzip OS header; no filename/time metadata.
        compressed=compressed[:9]+bytes([255])+compressed[10:]
        return dict(encoding='gzip-base64 canonical checkpoint JSON',sha256=hashlib.sha256(wire).hexdigest(),payload=base64.b64encode(compressed).decode('ascii'))
    values = {'full-native-checkpoints.json':dict(original=archived(old),resumed=archived(new)), 'restart-recovery-proof.json':summary,'original-checkpoint.json':old,'corrected-interrupted-checkpoint.json':corrected,
            'resumed-checkpoint.json':resumed,'current-journals-and-repeat.json':dict(selection=selected,repeat=repeat),
            'closed-reopened-period.json':dict(reopening=periods,correction_after_restart=after_reopen,rework=reclosed_work,reclosure=reclosed,repeat_reclosure=reclosure_repeat),'blocked-control.json':blocked,'public-answer.json':reclosure_repeat['public']}
    result = {}
    for name, value in values.items():
        view = project(value)
        # Lossless packaging only: retain every audit field without publishing
        # repeated multi-megabyte histories as oversized connector requests.
        if name != 'full-native-checkpoints.json' and len(dumps(view).encode()) > 1_000_000:
            view = archived(view)
            view['encoding'] = 'gzip-base64 canonical audit JSON'
        result[name] = view
    return result


def project(value):
    """Compact audit views, not restorable wire snapshots or hand-edited outcomes.

    Exact full checkpoint hashes bind source/archive populations; actual native
    source snapshots, version payloads, receipts and lifecycle histories remain.
    Repeated bulky intake proposals/requests are represented by exact hashes.
    """
    if isinstance(value,list):return [project(v) for v in value]
    if not isinstance(value,dict):return value
    if 'contract_version' in value and 'source_snapshots' in value:
        doc=value
        result={k:doc[k] for k in ('contract_version','company_id','root_case','company_context','scopes','periods','dependencies','versions','source_snapshots','active','states','supersession','version_history','receipts','rework_history','graph_history')}
        result['checkpoint_sha256']=hashlib.sha256(dumps(doc).encode()).hexdigest()
        result['cases']=[{k:c[k] for k in ('id','objective','scope_id','period_id','case_type','status','outcome','transitions','governance_history','result_version_refs','parent_case_id','child_case_ids','rework_state')} for c in doc['cases']]
        result['nodes']=[{k:n[k] for k in ('id','logical_id','selected_skill','scope_id','case_id','period_id','framework','functional_currency','presentation_currency','economic_id','status','dependencies','execution_receipt')} for n in doc['nodes']]
        result['retained_evidence']={key:dict(seal=b['seal'],archive_sha256=hashlib.sha256(dumps(b).encode()).hexdigest(),reviewed_pack_sha256=hashlib.sha256(dumps(b['pack']).encode()).hexdigest(),raw_source_sha256=[hashlib.sha256(raw.encode()).hexdigest() for raw in b['raw_sources']]) for key,b in doc['session'].get('evidence_bundles',{}).items()}
        result['session_sha256']=hashlib.sha256(dumps(doc['session']).encode()).hexdigest()
        result['artifact_boundary']='Generated audit view of exact checkpoint; full sealed archives remain in SQLite'
        return result
    return {k:project(v) for k,v in value.items()}


def main():
    if len(sys.argv)==3:print(dumps(worker(sys.argv[1],sys.argv[2])));return
    TARGET.mkdir(parents=True,exist_ok=True)
    for name,value in artifacts().items():(TARGET/name).write_text(json.dumps(value,sort_keys=True,indent=2,ensure_ascii=False)+'\n')

if __name__=='__main__':main()
