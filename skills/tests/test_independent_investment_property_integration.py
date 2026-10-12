"""Separate AI reviewer challenges actual native/durable/local/HTTP IP adapters."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from investment_property_cases import case, ready, capture
from orchestration import CAO
from orchestration.persistence import SQLiteStore, snapshot
from orchestration.persistence.codec import dumps
from local_cao.adapter import ExecutionInterface, VERSION
from local_cao.tests.test_authored import context


def source():
    c=case()
    def rebind(v):
        if isinstance(v,dict):
            for k,x in v.items():
                if k in ('entity','source_entity','legal_entity','legal_owner'):v[k]='ENTITY-DEMO'
                else:rebind(x)
        elif isinstance(v,list):
            for x in v:rebind(x)
    rebind(c);capture(c);return ready(c=c)


def request(c):
    return dict(objective='How should we account for our rental investment property?',scope=dict(entity=c['entity'],framework=c['framework'],jurisdiction=c['jurisdiction'],period_start=c['period_start'],reporting_period=c['reporting_period'],currency='EUR'),facts={'rental_investment':c})


class IndependentInvestmentIntegrationQA(unittest.TestCase):
    def test_native_property_owner_and_no_other_owner_execution(self):
        r=CAO().run(request(source()));self.assertEqual('complete',r.outcome,r.open_questions);self.assertEqual(['investment-property'],r.skills_invoked)
        n=r.graph.nodes['investment-property'];self.assertEqual('complete',n.status);self.assertEqual('50000',str(n.result['calculations']['fair_value_movement']))
        self.assertEqual('CLOSED',r.status)

    def test_missing_property_evidence_preserves_unrelated_ap(self):
        from orchestration.tests.test_independent_qa import IndependentQA
        h=IndependentQA();h.setUpClass();req=h.request();req['objective']='Review supplier and rental property accounting';req['facts']['rental_investment']={'properties':[{'asset_id':'unresolved-title'}],'material':True}
        r=CAO().run(req);self.assertEqual('partial',r.outcome);self.assertEqual('complete',r.graph.nodes['accounts-payable'].status);self.assertEqual('blocked',r.graph.nodes['investment-property'].status);self.assertFalse(r.graph.nodes['investment-property'].result)

    def test_durable_case_history_exact_restore_without_owner_execution(self):
        r=CAO().run(request(source()));self.assertEqual('complete',r.outcome,r.open_questions)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'property.db'
            with SQLiteStore(path) as store:self.assertEqual(1,store.save(r,'company-property',[],0))
            original=dumps(snapshot(r,'company-property',[]))
            with patch.object(CAO,'run',side_effect=AssertionError('unexpected accounting replay')):
                with SQLiteStore(path) as store:
                    restored,revision,ctx=store.load('company-property',r.id)
                    again,revision2,ctx2=store.load('company-property',r.id)
            self.assertEqual(1,revision);self.assertEqual(revision,revision2)
            self.assertEqual(original,dumps(snapshot(restored,'company-property',ctx)))
            self.assertEqual(original,dumps(snapshot(again,'company-property',ctx2)))
            self.assertEqual(CAO().public(r),CAO().public(restored))

    def test_local_execute_restart_and_repeated_read_do_not_replay(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'company-context.md').write_text(context());api=ExecutionInterface(p)
            def call(op,**kw):return api.call(dict(contract_version=VERSION,operation=op,company_id='synthetic-demo-001',**kw))
            self.assertTrue(call('initialize')['ok']);r=call('start',request_id='property',objective='How should we account for our rental investment property?',target_family='rental_investment');self.assertTrue(r['ok'],r);cid=r['case_id']
            self.assertTrue(call('submit',case_id=cid,evidence={'facts':{'rental_investment':source()}})['ok']);out=call('execute',case_id=cid);self.assertEqual('complete',out['execution_state'],out)
            api=ExecutionInterface(p)
            with patch.object(CAO,'run',side_effect=AssertionError('unexpected accounting replay')):
                self.assertEqual(out['public_result'],call('resume',case_id=cid)['public_result'])
                self.assertEqual(out,call('execute',case_id=cid))

    def test_local_source_changes_cannot_overwrite_committed_case_history(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'company-context.md').write_text(context());api=ExecutionInterface(p)
            def call(op,**kw):return api.call(dict(contract_version=VERSION,operation=op,company_id='synthetic-demo-001',**kw))
            self.assertTrue(call('initialize')['ok']);r=call('start',request_id='property-history',objective='How should we account for our rental investment property?',target_family='rental_investment');cid=r['case_id']
            c=source();self.assertTrue(call('submit',case_id=cid,evidence={'facts':{'rental_investment':c}})['ok']);out=call('execute',case_id=cid);self.assertEqual('complete',out['execution_state'],out)
            c['valuation']['amount']='700000';capture(c);c=ready(c=c)
            rejected=call('submit',case_id=cid,evidence={'facts':{'rental_investment':c}});self.assertFalse(rejected['ok']);self.assertEqual('immutable_submission',rejected['error']['code'])
            self.assertEqual(out['public_result'],call('resume',case_id=cid)['public_result'])

    def test_hosted_job_and_local_restart_share_exact_accounting_result(self):
        from hosted_cao.tests.test_authored import Authored
        h=Authored();h.setUp();self.addCleanup(h.doCleanups)
        cid=h.start('rental_investment');status,_=h.call('submit',case_id=cid,evidence={'facts':{'rental_investment':source()}});self.assertEqual(200,status)
        status,j=h.job(cid);self.assertEqual(202,status);self.assertTrue(h.service.run_one());status,j=h.http('/v1/jobs/'+j['id']);self.assertEqual(200,status);self.assertEqual('complete',j['accounting']['execution_state'],j)
        api=ExecutionInterface(h.workspace);local=api.call(h.envelope('resume',case_id=cid));self.assertEqual(local['public_result'],j['accounting']['public_result'])


if __name__=='__main__':unittest.main()
