"""Synthetic proof only. Each CLI operation runs in a separate process."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from local_cao.tests.test_authored import ROOT, context, evidence
from local_cao.adapter import VERSION


def prove():
    with tempfile.TemporaryDirectory() as directory:
        p=Path(directory);(p/'company-context.md').write_text(context())
        def call(op, **kw):
            request=dict(contract_version=VERSION,operation=op,company_id='synthetic-demo-001',**kw)
            process=subprocess.run([sys.executable,'-m','local_cao','--workspace',directory],input=json.dumps(request),capture_output=True,text=True,cwd=ROOT,timeout=60)
            assert process.returncode==0,(op,process.stdout,process.stderr)
            response=json.loads(process.stdout);assert response['ok'],response
            return response
        call('initialize');call('diagnose')
        scenarios=[]
        for pkg,family in [('fixed-assets','machinery'),('accounts-payable','supplier_cost')]:
            start=call('start',request_id=pkg,objective='Calculate supported '+pkg+' accounting',target_family=family)
            c=start['case_id'];e=evidence(pkg)
            call('submit',case_id=c,evidence=e)
            executed=call('execute',case_id=c); resumed=call('resume',case_id=c);retry=call('execute',case_id=c)
            assert executed['public_result']==resumed['public_result']==retry['public_result']
            assert executed['execution_state']=='complete'
            assert executed['checkpoint_revision']==resumed['checkpoint_revision']==retry['checkpoint_revision']==1
            expected='90000' if pkg=='fixed-assets' else '9600'
            assert expected in json.dumps(executed['public_result'])
            scenarios.append(dict(package=pkg,response=executed,resumed_identical=True,retry_identical=True,
                input_sha256=hashlib.sha256(json.dumps(e,sort_keys=True,separators=(',',':')).encode()).hexdigest()))
        for family,question in [('customer_contract','How should we recognize revenue from this new customer agreement?'),('reconciliation','Our prepayments have jumped this month. Investigate.')]:
            start=call('start',request_id=family,objective=question,target_family=family)
            executed=call('execute',case_id=start['case_id'])
            assert executed['execution_state']!='complete' and not executed['durable']
            assert not executed['public_result'].get('calculations')
            scenarios.append(dict(question=question,response=executed))
        return dict(contract_version=VERSION,claude_code_executed=False,live_claude_requires_owner_validation=True,
            fresh_process_operations=True,scenarios=scenarios)


if __name__=='__main__':print(json.dumps(prove(),sort_keys=True,indent=2))
