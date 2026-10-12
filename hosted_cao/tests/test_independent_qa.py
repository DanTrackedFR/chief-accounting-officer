"""Independent reviewer-owned HTTP and durable operational boundary tests."""
import concurrent.futures
import http.client
import json
import logging
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
from hosted_cao.service import Service, Server
from local_cao.adapter import ExecutionInterface
from orchestration.persistence import SQLiteStore
from orchestration.runtime import CAO
from orchestration.tests.fixtures import operational, certify

ROOT=Path(__file__).resolve().parents[2]
class IndependentHTTPQA(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.company='synthetic-demo-001';self.token='a'*48
        self.work=self.root/'company';self.other=self.root/'other';self.work.mkdir();self.other.mkdir()
        text=(ROOT/'company-context.example.md').read_text()
        (self.work/'company-context.md').write_text(text)
        (self.other/'company-context.md').write_text(text.replace(self.company,'other-company'))
        self.service=Service(self.root/'jobs',{self.company:self.work,'other-company':self.other},[{'caller_id':'express','token':self.token,'companies':[self.company]}])
        self.server=Server(('127.0.0.1',0),self.service);self.thread=threading.Thread(target=self.server.serve_forever);self.thread.start()
        self.addCleanup(self.shutdown)
        self.assertEqual(self.op('initialize')[0],200)
    def shutdown(self):
        self.server.shutdown();self.server.server_close();self.thread.join();self.service.close()
    def wire(self,path='/v1/operations',body=None,company=None,token=None,extra=None,raw=None,method='POST'):
        h={'Authorization':'Bearer '+(self.token if token is None else token),'X-CAO-Company':company or self.company,'Content-Type':'application/json'}
        h.update(extra or {});conn=http.client.HTTPConnection(*self.server.server_address,timeout=20)
        conn.request(method,path,body=raw if raw is not None else json.dumps(body) if body is not None else None,headers=h)
        r=conn.getresponse(); data=r.read();conn.close();return r.status,json.loads(data)
    def req(self,op,**kw):return dict(contract_version='1.0',company_id=self.company,operation=op,**kw)
    def op(self,op,**kw):return self.wire(body=self.req(op,**kw))
    def start(self,rid='qa',family='machinery'):
        status,r=self.op('start',request_id=rid,objective='Calculate reviewed accounting',target_family=family);self.assertEqual(status,200,r);return r['case_id']
    def evidence(self,package):
        c=operational(package);c.update(entity='ENTITY-DEMO',scope_id='ENTITY-DEMO')
        for h in c.get('handoffs',{}).values():h['entity']='ENTITY-DEMO'
        return {'facts':{{'fixed-assets':'machinery','accounts-payable':'supplier_cost'}[package]:certify(package,c)}}
    def job(self,cid,key='qa'):
        status,r=self.wire('/v1/jobs',self.req('execute',case_id=cid),extra={'Idempotency-Key':key});self.assertEqual(status,202,r);return r
    def poll(self,jid):return self.wire('/v1/jobs/'+jid,method='GET')[1]
    def test_two_real_owners_exact_local_parity_and_checkpoint_recovery(self):
        for package,family in [('fixed-assets','machinery'),('accounts-payable','supplier_cost')]:
            cid=self.start(package,family);self.assertEqual(self.op('submit',case_id=cid,evidence=self.evidence(package))[0],200)
            j=self.job(cid,package);self.assertTrue(self.service.run_one());r=self.poll(j['id'])
            self.assertEqual(r['state'],'SUCCEEDED');native=ExecutionInterface(self.work).call(self.req('resume',case_id=cid))
            self.assertEqual(r['accounting'],native);self.assertEqual(native['execution_state'],'complete')
            with self.service.db() as c:c.execute("UPDATE jobs SET state='EXECUTING' WHERE id=?",(j['id'],))
            with patch.object(CAO,'run',side_effect=AssertionError('Lost acknowledgment reran economics')):self.service.run_one()
            self.assertEqual(self.poll(j['id'])['accounting'],native)
            with SQLiteStore(self.work/'accounting.sqlite3') as store:self.assertEqual(store.load(self.company,cid)[1],1)
    def test_nondurable_blocked_job_explicit_accounting_outcome(self):
        cid=self.start();j=self.job(cid);self.service.run_one();r=self.poll(j['id'])
        self.assertEqual(r['state'],'SUCCEEDED');self.assertIn('accounting',r)
        self.assertNotEqual(r['accounting']['execution_state'],'complete');self.assertFalse(r['accounting']['durable'])
    def test_company_credentials_and_known_case_job_isolation(self):
        cid=self.start();j=self.job(cid)
        for token in ('', 'b'*48):self.assertEqual(self.wire(body=self.req('list'),token=token)[0],401)
        self.assertEqual(self.wire('/v1/jobs/'+j['id'],method='GET',company='other-company')[0],403)
        self.assertEqual(self.wire(body=self.req('result',case_id=cid),company='other-company')[0],403)
        self.assertEqual(self.wire(body={**self.req('list'),'company_id':'other-company'})[0],400)
    def test_duplicate_acceptance_concurrent_and_changed_fingerprint(self):
        cid=self.start()
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:rows=list(pool.map(lambda _:self.job(cid),range(8)))
        self.assertEqual(len({r['id'] for r in rows}),1)
        with self.service.db() as c:self.assertEqual(c.execute('SELECT count(*) FROM jobs').fetchone()[0],1)
        changed=self.req('execute',case_id=cid,route='answer')
        self.assertEqual(self.wire('/v1/jobs',changed,extra={'Idempotency-Key':'qa'})[0],409)
    def test_staged_paths_symlinks_and_untrusted_authority_rejected(self):
        cid=self.start();(self.work/'staged').mkdir();(self.work/'staged/link.json').symlink_to('/etc/passwd')
        for value in ('../escape','/etc/passwd','https://example.com/x'):
            self.assertEqual(self.op('submit',case_id=cid,staged_file_id=value)[0],400)
        status,r=self.op('submit',case_id=cid,staged_file_id='link');self.assertEqual(status,422);self.assertEqual(r['error']['code'],'workspace_boundary')
        for field,value in [('evidence_file','/etc/passwd'),('authenticated',True),('approved',True)]:self.assertEqual(self.wire(body={**self.req('execute',case_id=cid),field:value})[0],400)
    def test_malformed_json_and_private_exception_hygiene(self):
        for raw in ('{"operation":"list","operation":"execute"}','{"value":NaN}','[]'):
            status,r=self.wire(raw=raw);self.assertEqual(status,400);self.assertNotIn('Traceback',json.dumps(r))
        with patch.object(CAO,'run',side_effect=ValueError('CONFIDENTIAL SECRET')):
            status,r=self.op('start',request_id='error',objective='Test confidential failure',target_family='machinery')
        self.assertNotIn('SECRET',json.dumps(r));self.assertNotIn('CONFIDENTIAL',json.dumps(r))
    def test_changed_evidence_after_acceptance_fails_closed(self):
        cid=self.start();j=self.job(cid)
        self.assertEqual(self.op('submit',case_id=cid,evidence=self.evidence('fixed-assets'))[0],200)
        self.service.run_one();r=self.poll(j['id']);self.assertEqual(r['state'],'FAILED')
        with SQLiteStore(self.work/'accounting.sqlite3') as store:self.assertEqual(store.connection.execute('SELECT count(*) FROM checkpoints').fetchone()[0],0)
    def test_concurrent_workers_same_service_create_one_checkpoint(self):
        cid=self.start();self.op('submit',case_id=cid,evidence=self.evidence('fixed-assets'));j=self.job(cid)
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(lambda _:self.service.run_one(),range(6)))
        with SQLiteStore(self.work/'accounting.sqlite3') as store:self.assertEqual(store.load(self.company,cid)[1],1)
        self.assertEqual(self.poll(j['id'])['accounting']['execution_state'],'complete')
    def test_polling_preserves_native_stale_checkpoint(self):
        cid=self.start();self.op('submit',case_id=cid,evidence=self.evidence('fixed-assets'));j=self.job(cid);self.service.run_one()
        with SQLiteStore(self.work/'accounting.sqlite3') as store:
            case,revision,_=store.load(self.company,cid)
            version=next(iter(case.governance.versions.active.values()));case.governance.versions.mark_stale(version,'CHALLENGE','independent-review')
            node=case.governance.graph.nodes[case.governance.versions.versions[version].node_id];node.status='blocked'
            CAO()._refresh_versioned(case,False)
            store.save(case,self.company,[],revision)
        r=self.poll(j['id']);self.assertEqual(r['accounting']['currentness'],'STALE')
        self.assertNotEqual(r['accounting']['execution_state'],'complete')
    def test_malformed_staged_duplicate_json_and_regular_file_boundary(self):
        cid=self.start();stage=self.work/'staged';stage.mkdir()
        (stage/'duplicate.json').write_text('{"facts":{},"facts":{}}')
        (stage/'directory.json').mkdir()
        for ident in ('duplicate','directory'):
            status,r=self.op('submit',case_id=cid,staged_file_id=ident);self.assertEqual(status,422);self.assertFalse(r['ok'])
    def test_logs_contain_only_operational_metadata(self):
        with self.assertLogs('hosted_cao',level=logging.INFO) as captured:
            cid=self.start('log-check');j=self.job(cid);self.service.run_one()
        output=' '.join(captured.output)
        self.assertNotIn(self.token,output);self.assertNotIn('Calculate reviewed accounting',output)
        self.assertNotIn('assets',output);self.assertIn('job_finished',output)

    def test_single_worker_lock_across_instances(self):
        self.service.start_worker()
        other=Service(self.root/'jobs',{self.company:self.work},[{'caller_id':'express','token':self.token,'companies':[self.company]}])
        with self.assertRaises(BlockingIOError):other.start_worker()
        other.close()

if __name__=='__main__':unittest.main()
