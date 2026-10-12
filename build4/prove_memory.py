"""Fresh-process Company Memory proof; writes only requested new output path."""
import hashlib
import json
import tempfile
import subprocess
import sys
from pathlib import Path
from local_cao.adapter import ExecutionInterface
from build4.tests.test_memory_journey import onboarding,install,investigate,install_policy
from orchestration.tests import persistence_stage3_fixtures as mf
from intelligence.tests.fixtures import COMPANY,wire,doc,revenue_evidence,OBJECTIVE


def policy_proof():
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp);text=onboarding(start='2026-01-01');(path/'company-context.md').write_text(text);api=ExecutionInterface(path)
        assert api.call(wire('initialize'))['ok']
        old_text='Distinct equipment and monitoring promises require reviewed standalone selling prices and period-specific satisfaction evidence.'
        new_text='Distinct equipment and monitoring promises require reviewed standalone selling prices, acceptance evidence and monitoring service-date evidence.'
        old,record=install_policy(api,text,old_text)
        initial=api.call(wire('investigate',request_id='historic-policy-consumer',objective=OBJECTIVE,target_family='customer_contract'))
        assert initial['ok']
        with api._store() as store:
            consumer=store.load(COMPANY,initial['case_id'])[0];snapshot=consumer._investigation['snapshot']
        assert snapshot['values']['policies']==old_text
        assert api.call(wire('document',case_id=initial['case_id'],event_id='policy-contract',document=doc(snapshot['scope'])))['ok']
        reviewed=revenue_evidence(api,initial['case_id'])
        assert api.call(wire('submit',case_id=initial['case_id'],evidence=reviewed))['ok']
        executed=api.call(wire('execute',case_id=initial['case_id']))
        assert executed['ok'] and executed['execution_state']=='complete'
        with api._store() as store:
            native=store.load(COMPANY,initial['case_id'])[0]
            native_versions=native.governance.versions.record()
            original_source=store.load(COMPANY,old.id)[0].governance.evidence_bundles
        successor,replacement=install_policy(api,text,new_text,record)
        stale=api.call(wire('resume',case_id=initial['case_id']))
        assert 'memory-policies' in stale['investigation']['conflicts']
        current,view=investigate(api,'successor-policy-consumer')
        assert view['values']['policies']==new_text
        with api._store() as store:ledger=store.memory().audit(COMPANY)
        return dict(old_source_case=old.id,new_source_case=successor.id,original_record=record,
                    replacement_record=replacement,original_snapshot=snapshot,stale_consumer=stale,
                    reviewed_revenue_input=reviewed,native_revenue_result=executed,
                    native_revenue_versions=native_versions,original_policy_sources=original_source,
                    current_consumer=current,current_snapshot=view,ledger=ledger)


def proof():
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp);text=onboarding();(path/'company-context.md').write_text(text);api=ExecutionInterface(path)
        assert api.call(wire('initialize'))['ok']
        old,r=install(api,text);result,snapshot=investigate(api)
        assert snapshot['values']['systems']=='Oracle ERP'
        assert snapshot['memory_references'][0]['version_id']==r['version_id']
        assert result['execution_state']=='blocked'
        with api._store() as store:
            case=store.load(COMPANY,old.id)[0]
            audit=store.memory().audit(COMPANY)
            versions=case.governance.versions.record()
        other,foreign=install(api,onboarding('ORION-OTHER'),'Regional Ledger')
        result2,s2=investigate(api,'orion-with-foreign-history')
        assert snapshot['memory_references']==s2['memory_references']
        assert 'systems' not in s2['conflicts']
        root=Path(__file__).resolve().parents[1]
        request=wire('resume',case_id=result['case_id'])
        resumed=subprocess.run([sys.executable,'-m','local_cao','--workspace',str(path)],input=json.dumps(request),text=True,capture_output=True,cwd=root)
        assert resumed.returncode==0,resumed.stderr
        fresh=json.loads(resumed.stdout);assert fresh['public_result']==result['public_result']
        mf.correction(old)
        with api._store() as store:
            store.save(old,COMPANY,[],1)
            corrected_versions=old.governance.versions.record()
        stale_process=subprocess.run([sys.executable,'-m','local_cao','--workspace',str(path)],input=json.dumps(request),text=True,capture_output=True,cwd=root)
        assert stale_process.returncode==0,stale_process.stderr
        stale=json.loads(stale_process.stdout)
        assert stale['ok'] and stale['execution_state']=='blocked' and 'memory-systems' in stale['investigation']['conflicts']
        assert stale['investigation']['context_snapshot_id']==snapshot['snapshot_id']
        return dict(accounting_policy_history=policy_proof(),contract='cao-build4-memory-proof/1',company_id=COMPANY,
                    governance_setup='Native SQLiteStore.memory; synthetic trusted caller, authenticated=false',
                    execution_boundary='ExecutionInterface.call investigate/resume',
                    source_case=old.id,consumer_case=result['case_id'],memory_record=r,
                    source_result_versions=versions,context_snapshot=snapshot,
                    actual_result=result,foreign_record=foreign['record_id'],foreign_case=other.id,
                    cross_entity_result=result2,ledger_uses=audit['uses'],
                    fresh_cli_resume=fresh,corrected_source_versions=corrected_versions,stale_cli_resume=stale,
                    limitation='Context reuse grants no accounting input authority; signed contract and reviewed native pack remain required.')


def main():
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output');a=p.parse_args()
    out=Path(a.output) if a.output else None
    if out is not None and out.exists():raise SystemExit('Refusing to overwrite historical proof')
    wire_text=json.dumps(proof(),sort_keys=True,indent=2)+'\n'
    if out is None:print(wire_text,end='')
    else:
        out.parent.mkdir(parents=True,exist_ok=True);out.write_text(wire_text)
        print(hashlib.sha256(wire_text.encode()).hexdigest())

if __name__=='__main__':main()
