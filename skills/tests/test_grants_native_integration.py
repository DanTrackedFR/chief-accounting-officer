"""Actual grants through existing native, durable, local and HTTP boundaries."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from grant_cases import case,ready,capture
from orchestration import CAO
from orchestration.persistence import SQLiteStore,snapshot
from orchestration.persistence.codec import dumps
from local_cao.adapter import ExecutionInterface,VERSION
from local_cao.tests.test_authored import context


def source():
    c=case()
    def rebind(v):
        if isinstance(v,dict):
            for k,x in v.items():
                if k in ('entity','source_entity'):v[k]='ENTITY-DEMO'
                else:rebind(x)
        elif isinstance(v,list):
            for x in v:rebind(x)
    rebind(c);capture(c);return ready(c=c)


def request(c):return dict(objective='How should we account for this government grant?',scope=dict(entity=c['entity'],framework=c['framework'],jurisdiction=c['jurisdiction'],period_start=c['period_start'],reporting_period=c['reporting_period'],currency='EUR'),facts={'grant':c})

class NativeGrants(unittest.TestCase):
    def test_existing_native_accounting_owner(self):
        r=CAO().run(request(source()));self.assertEqual('complete',r.outcome,r.open_questions);self.assertEqual(['government-grants'],r.skills_invoked)
        n=r.graph.nodes['government-grants'];self.assertEqual('complete',n.status);self.assertEqual('40.00',str(n.result['calculations']['grants'][0]['current_income']))
    def test_missing_grant_keeps_ap_complete(self):
        from orchestration.tests.test_independent_qa import IndependentQA
        h=IndependentQA();h.setUpClass();req=h.request();req['objective']='Review supplier and government grant accounting';req['facts']['grant']={'agreement':'Actual but incomplete agreement','material':True}
        r=CAO().run(req);self.assertEqual('partial',r.outcome);self.assertEqual('complete',r.graph.nodes['accounts-payable'].status);self.assertEqual('blocked',r.graph.nodes['government-grants'].status);self.assertFalse(r.graph.nodes['government-grants'].result)
    def test_restart_preserves_exact_grant_result(self):
        r=CAO().run(request(source()));self.assertEqual('complete',r.outcome)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'grant.db'
            with SQLiteStore(path) as store:self.assertEqual(1,store.save(r,'company-grant',[],0))
            with patch.object(CAO,'run',side_effect=AssertionError('owner replay during restore')):
                with SQLiteStore(path) as store:restored,revision,ctx=store.load('company-grant',r.id)
            self.assertEqual(1,revision);self.assertEqual(dumps(snapshot(r,'company-grant',[])),dumps(snapshot(restored,'company-grant',ctx)));self.assertEqual(CAO().public(r),CAO().public(restored))
    def test_local_and_restart(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'company-context.md').write_text(context());api=ExecutionInterface(p)
            def call(op,**kw):return api.call(dict(contract_version=VERSION,operation=op,company_id='synthetic-demo-001',**kw))
            self.assertTrue(call('initialize')['ok']);r=call('start',request_id='grants',objective='How should we account for this government grant?',target_family='grant');cid=r['case_id']
            self.assertTrue(call('submit',case_id=cid,evidence={'facts':{'grant':source()}})['ok']);out=call('execute',case_id=cid);self.assertEqual('complete',out['execution_state'],out)
            api=ExecutionInterface(p);self.assertEqual(out['public_result'],call('resume',case_id=cid)['public_result'])
    def test_http_and_local_exact_parity(self):
        from hosted_cao.tests.test_authored import Authored
        h=Authored();h.setUp();self.addCleanup(h.doCleanups)
        cid=h.start('grant');status,_=h.call('submit',case_id=cid,evidence={'facts':{'grant':source()}});self.assertEqual(200,status)
        status,j=h.job(cid);self.assertEqual(202,status);self.assertTrue(h.service.run_one());status,j=h.http('/v1/jobs/'+j['id']);self.assertEqual(200,status);self.assertEqual('complete',j['accounting']['execution_state'],j)
        api=ExecutionInterface(h.workspace);local=api.call(h.envelope('resume',case_id=cid));self.assertEqual(local['public_result'],j['accounting']['public_result'])

if __name__=='__main__':unittest.main()
