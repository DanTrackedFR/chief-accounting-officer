import concurrent.futures
import http.client
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
from hosted_cao.service import Service, Server
from local_cao.adapter import ExecutionInterface
from local_cao.tests.test_authored import context, evidence
from orchestration.runtime import CAO

TOKEN='synthetic-test-credential-'+('x'*32)
COMPANY='synthetic-demo-001'

class Authored(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.workspace=self.root/'company';self.workspace.mkdir()
        (self.workspace/'company-context.md').write_text(context())
        self.other=self.root/'other';self.other.mkdir();(self.other/'company-context.md').write_text(context().replace(COMPANY,'other-company'))
        self.service=Service(self.root/'jobs',{COMPANY:self.workspace,'other-company':self.other},[{'caller_id':'express-test','token':TOKEN,'companies':[COMPANY]},{'caller_id':'other-express','token':'y'*40,'companies':['other-company']}])
        self.server=Server(('127.0.0.1',0),self.service);self.thread=threading.Thread(target=self.server.serve_forever);self.thread.start()
        self.addCleanup(self.close)
        self.assertEqual(self.call('initialize')[0],200)
    def close(self):
        self.server.shutdown();self.server.server_close();self.thread.join();self.service.close()
    def http(self,path,body=None,headers=None,method=None):
        c=http.client.HTTPConnection(*self.server.server_address,timeout=60)
        h={'Authorization':'Bearer '+TOKEN,'X-CAO-Company':COMPANY,'Content-Type':'application/json'};h.update(headers or {})
        c.request(method or ('POST' if body is not None else 'GET'),path,json.dumps(body) if isinstance(body,dict) else body,h)
        r=c.getresponse();data=json.loads(r.read());status=r.status;c.close();return status,data
    def envelope(self,op,**kw):return dict(contract_version='1.0',operation=op,company_id=COMPANY,**kw)
    def call(self,op,**kw):return self.http('/v1/operations',self.envelope(op,**kw))
    def start(self,pkg='fixed-assets',rid='case'):
        family={'fixed-assets':'machinery','accounts-payable':'supplier_cost'}.get(pkg,pkg)
        status,r=self.call('start',request_id=rid,objective='Calculate supported '+pkg+' accounting',target_family=family)
        self.assertEqual(status,200,r);return r['case_id']
    def stage(self,pkg='fixed-assets',rid='case'):
        cid=self.start(pkg,rid);self.assertEqual(self.call('submit',case_id=cid,evidence=evidence(pkg))[0],200);return cid
    def job(self,cid,key='retry'):
        return self.http('/v1/jobs',self.envelope('execute',case_id=cid),{'Idempotency-Key':key})
    def test_health_readiness_version(self):
        for path in ('health','readiness','version'):
            s,r=self.http('/v1/'+path);self.assertEqual(s,200);self.assertEqual(r['api_version'],'1.0')
        self.assertEqual(self.http('/v2/version')[0],404)
    def test_authentication(self):
        for token in ('','wrong'):
            self.assertEqual(self.http('/v1/operations',self.envelope('list'),{'Authorization':token})[0],401)
    def test_company_scope(self):
        self.assertEqual(self.http('/v1/operations',self.envelope('list'),{'X-CAO-Company':'other-company'})[0],403)
        self.assertEqual(self.http('/v1/operations',{**self.envelope('list'),'company_id':'other-company'})[0],400)
    def test_invalid_fields_version(self):
        for request in (self.envelope('list',extra=True),{**self.envelope('list'),'contract_version':'2.0'},self.envelope('execute',case_id='foo')):
            self.assertEqual(self.http('/v1/operations',request)[0],400)
    def test_payload_limit(self):
        self.assertEqual(self.http('/v1/operations','x'*(2_000_001))[0],413)
    def test_malformed(self):
        for data in ('[]','{"operation":"a","operation":"b"}','{"x":NaN}'):
            self.assertEqual(self.http('/v1/operations',data)[0],400)
    def execute(self,pkg):
        cid=self.stage(pkg);status,j=self.job(cid);self.assertEqual(status,202,j)
        self.assertEqual(j['state'],'ACCEPTED');self.assertTrue(self.service.run_one())
        status,j=self.http('/v1/jobs/'+j['id']);self.assertEqual(status,200,j);self.assertEqual(j['state'],'SUCCEEDED')
        r=j['accounting'];self.assertEqual(r['execution_state'],'complete',r)
        local=ExecutionInterface(self.workspace).call(self.envelope('resume',case_id=cid));self.assertEqual(local['public_result'],r['public_result'])
        self.assertEqual(r['checkpoint_revision'],1);return cid,j
    def test_native_fixed_assets_exact_parity(self):
        _,j=self.execute('fixed-assets');self.assertIn('90000',json.dumps(j['accounting']['public_result']))
    def test_native_ap_exact_parity(self):
        _,j=self.execute('accounts-payable');self.assertIn('9600',json.dumps(j['accounting']['public_result']))
    def test_missing_evidence_job_outcome(self):
        cid=self.start('customer_contract');_,j=self.job(cid);self.service.run_one();_,r=self.http('/v1/jobs/'+j['id'])
        self.assertEqual(r['state'],'SUCCEEDED');self.assertEqual(r['accounting']['execution_state'],'blocked');self.assertFalse(r['accounting']['durable'])
        self.assertFalse(r['accounting']['public_result'].get('journals'))
    def test_retry_no_duplicate_economics(self):
        cid,j=self.execute('fixed-assets')
        with patch.object(CAO,'run',side_effect=AssertionError('owner rerun')):
            _,retry=self.job(cid);self.assertEqual(retry['id'],j['id']);self.assertEqual(retry['accounting']['public_result'],j['accounting']['public_result'])
            _,other=self.job(cid,'new-key');self.service.run_one();result=self.service.job(COMPANY,other['id']);self.assertEqual(result['accounting']['checkpoint_revision'],1)
    def test_concurrent_duplicates(self):
        cid=self.stage()
        with concurrent.futures.ThreadPoolExecutor(8) as pool:results=list(pool.map(lambda _:self.job(cid),range(8)))
        self.assertEqual({s for s,r in results},{202});self.assertEqual(len({r['id'] for s,r in results}),1)
        self.service.run_one();self.assertFalse(self.service.run_one())
    def test_idempotency_conflict(self):
        cid=self.stage();self.job(cid);cid2=self.start(rid='second');self.assertEqual(self.job(cid2)[0],409)
    def test_restore_new_service(self):
        cid,j=self.execute('accounts-payable');other=Service(self.root/'jobs',self.service.companies,self.service.credentials)
        self.assertEqual(other.job(COMPANY,j['id'])['accounting']['public_result'],j['accounting']['public_result'])
    def test_crash_before_native_execution(self):
        cid=self.stage();_,j=self.job(cid)
        with self.service.db() as c:c.execute("UPDATE jobs SET state='EXECUTING' WHERE id=?",(j['id'],))
        other=Service(self.root/'jobs',self.service.companies,self.service.credentials);other.run_one()
        self.assertEqual(other.job(COMPANY,j['id'])['accounting']['execution_state'],'complete')
    def test_lost_native_ack(self):
        cid=self.stage();_,j=self.job(cid)
        native=ExecutionInterface(self.workspace).call(self.envelope('execute',case_id=cid));self.assertTrue(native['ok'])
        with self.service.db() as c:c.execute("UPDATE jobs SET state='EXECUTING' WHERE id=?",(j['id'],))
        with patch.object(CAO,'run',side_effect=AssertionError('rerun')):self.service.run_one()
        self.assertEqual(self.service.job(COMPANY,j['id'])['accounting']['checkpoint_revision'],1)
    def test_input_change_after_acceptance_refuses(self):
        cid=self.start();_,j=self.job(cid);self.call('submit',case_id=cid,evidence=evidence('fixed-assets'));self.service.run_one()
        self.assertEqual(self.service.job(COMPANY,j['id'])['state'],'FAILED')
        self.assertFalse(self.call('resume',case_id=cid)[1]['ok'])
    def test_staged_file(self):
        cid=self.start();folder=self.workspace/'staged';folder.mkdir();(folder/'reviewed.json').write_text(json.dumps(evidence('fixed-assets')))
        self.assertEqual(self.call('submit',case_id=cid,staged_file_id='reviewed')[0],200)
    def test_path_symlink_rejection(self):
        cid=self.start()
        for value in ('../secret','/tmp/file','https://example.com','a/b'):
            self.assertEqual(self.call('submit',case_id=cid,staged_file_id=value)[0],400)
        folder=self.workspace/'staged';folder.mkdir();(folder/'link.json').symlink_to('/etc/passwd')
        self.assertEqual(self.call('submit',case_id=cid,staged_file_id='link')[0],422)
        self.assertEqual(self.call('submit',case_id=cid,evidence_file='/etc/passwd')[0],400)
    def test_unsupported_remains_blocked(self):
        for family in ('borrowing_costs','investment_property','government_grants'):
            self.assertNotEqual(self.call('start',request_id=family,objective='Calculate',target_family=family)[0],200)
    def test_confidential_errors_logs(self):
        with self.assertLogs('hosted_cao',level='INFO') as logs:
            status,r=self.http('/v1/operations','SECRET-invalid')
        self.assertNotIn('SECRET',json.dumps(r));self.assertNotIn(TOKEN,str(logs.output));self.assertNotIn('SECRET',str(logs.output))
    def test_cross_company_job(self):
        cid=self.stage();_,j=self.job(cid)
        self.assertEqual(self.http('/v1/jobs/'+j['id'],headers={'Authorization':'Bearer '+'y'*40,'X-CAO-Company':'other-company'})[0],404)

if __name__=='__main__':unittest.main()
