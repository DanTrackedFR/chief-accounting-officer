"""Fresh service processes, real HTTP/native owners; synthetic evidence only."""
import hashlib
import http.client
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
from local_cao.adapter import canonical, ExecutionInterface
from local_cao.tests.test_authored import ROOT, context, evidence

COMPANY='synthetic-demo-001';TOKEN='synthetic-proof-'+('x'*40)

def prove():
    with tempfile.TemporaryDirectory() as directory:
        root=Path(directory);work=root/'company';work.mkdir();(work/'company-context.md').write_text(context())
        config=root/'config.json';config.write_text(canonical({'job_root':str(root/'jobs'),'companies':{COMPANY:str(work)},'credentials':[{'caller_id':'proof','token':TOKEN,'companies':[COMPANY]}]}))
        process=None;port=None
        def wire(path,body=None,key=None):
            c=http.client.HTTPConnection('127.0.0.1',port,timeout=30)
            headers={'Authorization':'Bearer '+TOKEN,'X-CAO-Company':COMPANY,'Content-Type':'application/json'}
            if key:headers['Idempotency-Key']=key
            c.request('POST' if body is not None else 'GET',path,canonical(body) if body else None,headers)
            r=c.getresponse();payload=json.loads(r.read());status=r.status;c.close();assert status in (200,202),(status,payload);return payload
        def start():
            nonlocal process,port
            with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
            process=subprocess.Popen([sys.executable,'-m','hosted_cao'],cwd=ROOT,env={**os.environ,'CAO_SERVICE_CONFIG':str(config),'CAO_PORT':str(port)},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            for _ in range(100):
                try:
                    wire('/v1/readiness');return
                except OSError:time.sleep(.05)
            raise AssertionError('Service not ready')
        def stop(hard=False):
            if hard:process.kill()
            else:process.terminate()
            process.wait(timeout=30)
        def env(op,**kw):return dict(contract_version='1.0',operation=op,company_id=COMPANY,**kw)
        def call(op,**kw):return wire('/v1/operations',env(op,**kw))
        records=[]
        try:
            start();call('initialize')
            for package,family in [('fixed-assets','machinery'),('accounts-payable','supplier_cost')]:
                cid=call('start',request_id=package,objective='Calculate supported '+package+' accounting',target_family=family)['case_id']
                e=evidence(package);call('submit',case_id=cid,evidence=e)
                j=wire('/v1/jobs',env('execute',case_id=cid),package)
                for _ in range(200):
                    r=wire('/v1/jobs/'+j['id'])
                    if r['state'] in ('SUCCEEDED','FAILED'):break
                    time.sleep(.02)
                assert r['state']=='SUCCEEDED' and r['accounting']['execution_state']=='complete',r
                local=ExecutionInterface(work).call(env('resume',case_id=cid));assert local==r['accounting']
                stop(hard=True);start()
                restored=wire('/v1/jobs/'+j['id']);retry=wire('/v1/jobs',env('execute',case_id=cid),package)
                assert restored['accounting']==retry['accounting']==r['accounting']
                assert restored['accounting']['checkpoint_revision']==1
                records.append({'package':package,'job_id':j['id'],'accounting':r['accounting'],'input_sha256':hashlib.sha256(canonical(e).encode()).hexdigest(),'fresh_process_restoration':True,'retry_exact':True})
            cid=call('start',request_id='missing-contract',objective='How should we recognize revenue from this new customer agreement?',target_family='customer_contract')['case_id']
            j=wire('/v1/jobs',env('execute',case_id=cid),'missing-contract')
            for _ in range(200):
                r=wire('/v1/jobs/'+j['id'])
                if r['state']=='SUCCEEDED':break
                time.sleep(.02)
            assert r['accounting']['execution_state']=='blocked' and not r['accounting']['durable']
            records.append({'missing_evidence':True,'accounting':r['accounting']})
            return {'api_version':'1.0','fresh_http_processes':True,'synthetic_only':True,'operational_timestamps_excluded':True,'scenarios':records}
        finally:
            if process and process.poll() is None:stop()

if __name__=='__main__':print(json.dumps(prove(),sort_keys=True,indent=2))
