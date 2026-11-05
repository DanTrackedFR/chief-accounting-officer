"""Independent remediation boundary QA. Fresh inputs; production HTTP and durable store."""
import copy, hashlib, json, os, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from hosted_cao.tests import test_presumed_engineering_qa as h
from local_cao.adapter import ExecutionInterface
OUT=Path(os.environ.get('CAO_ENGINEERING_OUT',str(Path(__file__).parent/'evidence')))
OUT.mkdir(parents=True,exist_ok=True)

def case(count=1):
    c=h.synthetic_case(count=count)
    c['case_id']='source-engineering-independent-17'
    c['source']['id']='engineering-independent-input'
    c['source']['hash']=hashlib.sha256(b'engineering-independent-input').hexdigest()
    for i,r in enumerate(c['assets']):
        r.update(id='EQ-'+str(i), opening_cost='17250',opening_accumulated='750')
    return c

class Boundaries(unittest.TestCase):
    def setUp(self):
        self.h=h.IndependentPresumedEngineeringQA();self.h.setUp();self.addCleanup(self.h.doCleanups)
        self.trace=[];http=self.h.http
        def traced(path,body=None,**headers):
            result=http(path,body,**headers)
            self.trace.append(dict(path=path,request=body,status=result[0],response=result[1]))
            return result
        self.h.http=traced
        self.addCleanup(lambda:(OUT/(self._testMethodName+'.json')).write_text(json.dumps(self.trace,indent=2,default=str)+'\n'))
    def assert_rejected(self,result,field):
        status,r=result;self.assertIn(status,(400,422),r)
        self.assertEqual(r['error']['code'],'invalid_request')
        self.assertIn(field,[x['field_path'] for x in r['error']['requirements']])
    def complete(self,c,rid='independent'):
        cid,j=self.h.complete(rid=rid,case=c)
        before=self.h.native(cid)[1]
        reopened=self.h.new_service();self.addCleanup(reopened.close)
        self.assertEqual(reopened.job(h.COMPANY,j['id'])['accounting'],j['accounting'])
        self.assertEqual(self.h.job(cid,rid)[1]['id'],j['id'])
        self.assertEqual(self.h.native(cid)[1]['proposed_journal_workpaper'],before['proposed_journal_workpaper'])
        return j['accounting']['public_result'],before
    def test_inline_case_identifier_types(self):
        cid=self.h.start(rid='id-inline')
        for invalid in (False,17,[],{'nested':'id'},'', '  ', 'I'*257):
            with self.subTest(value=str(invalid)[:20]):
                c=case();c['case_id']=invalid
                self.assert_rejected(self.h.call('submit',case_id=cid,evidence=h.supplied(case=c)),'evidence.facts.machinery.case_id')
    def test_staged_case_identifier_types(self):
        cid=self.h.start(rid='id-file');folder=self.h.workspace/'staged';folder.mkdir()
        for invalid in (True,[],{'id':'fake'},' ', 'S'*257):
            with self.subTest(value=str(invalid)[:20]):
                c=case();c['case_id']=invalid
                (folder/'bad.json').write_text(json.dumps(h.supplied(case=c)))
                self.assert_rejected(self.h.call('submit',case_id=cid,staged_file_id='bad'),'evidence.facts.machinery.case_id')
    def test_replaced_staged_evidence_rejected_before_job_acceptance(self):
        cid=self.h.stage(rid='preaccept',case=case())
        api=ExecutionInterface(self.h.workspace,allow_prepared_unreviewed=True,allow_presumed_user_sources=True)
        _,folder=api._request(cid,api._configuration(h.COMPANY));path=folder/'evidence.json'
        value=json.loads(path.read_text());value['facts']['machinery']['case_id']=['bad']
        path.write_text(json.dumps(value))
        self.assert_rejected(self.h.job(cid,'bad-staged'),'evidence.facts.machinery.case_id')
        with self.h.service.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM jobs').fetchone()[0],0)
    def test_direct_owner_rejects_invalid_case_identifier(self):
        from source_execution import execute
        for invalid in (False,[],{},' ', 'D'*257):
            c=case();c.update(case_id=invalid,review_mode=h.MODE,source_assurance=h.PROFILE,package='fixed-assets')
            with self.subTest(value=str(invalid)[:20]):
                r=execute('fixed-assets',c)
                self.assertEqual(r['accounting_determination'],'UNRESOLVED')
                self.assertFalse(r['proposed_journal_workpaper']);self.assertNotIn('source_lineage',r)
                self.assertIn('case_id',[n['field_path'] for n in r['validation_requirements']])
    def test_valid_boundary_identifier_is_distinct_from_durable_case(self):
        c=case();c['case_id']='V'*256
        p,n=self.complete(c)
        self.assertEqual(n['source_lineage']['case'],c['case_id'])
        self.assertEqual(p['accounting_determination'],'SUPPORTED')
    def test_operation_types_are_structured_client_errors(self):
        for op in (None,False,1,3.5,['execute'],{'operation':'execute'},''):
            for path in ('/v1/operations','/v1/jobs'):
                with self.subTest(op=op,path=path):
                    self.assert_rejected(self.h.http(path,self.h.envelope(op),**{'Idempotency-Key':'invalid-op'}),'operation')
        with self.h.service.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM jobs').fetchone()[0],0)
    def test_invalid_operations_local_boundary(self):
        api=ExecutionInterface(self.h.workspace,allow_prepared_unreviewed=True,allow_presumed_user_sources=True)
        for op in ([1],{'a':1},None,False):
            r=api.call(self.h.envelope(op));self.assertFalse(r['ok']);self.assertEqual(r['error']['code'],'invalid_request')
            self.assertIn('operation',[x['field_path'] for x in r['error']['requirements']])
    def test_source_reference_does_not_multiply_and_keeps_anomalies(self):
        c=case(23);c['source']['id']='Z'*8192;c['assets'][5]['opening_cost']='-22'
        p,n=self.complete(c)
        self.assertNotIn('Z'*8192,json.dumps(p))
        self.assertIn('assets:6',p['anomaly_report']['excluded_rows'])
        self.assertTrue(p['validation_requirements'])
        self.assertTrue(all(len(f['source_reference'])<=256 for f in p['anomaly_report']['findings']))
        self.assertGreater(len(p['anomaly_report']['findings']),23)
        self.assertEqual(n['source_lineage']['source']['id'],c['source']['id'])
    def test_source_reference_over_bound_blocks_safely(self):
        c=case();c['source']['id']='Q'*8193
        p,n=self.complete(c)
        self.assertEqual(p['accounting_determination'],'UNRESOLVED');self.assertFalse(n['proposed_journal_workpaper'])
        self.assertNotIn('Q'*8193,json.dumps(p));self.assertTrue(p['validation_requirements'])
    def test_row_id_bound_retains_independent_row(self):
        c=case(2);c['assets'][0]['id']='A'*257
        p,n=self.complete(c)
        self.assertIn('assets:1',p['anomaly_report']['excluded_rows'])
        self.assertEqual(len(n['calculations']['assets']),1)
        self.assertTrue(n['proposed_journal_workpaper']);self.assertNotIn('A'*257,json.dumps(p))
    def test_population_limit_rejects_before_partial_accounting(self):
        c=case(201);p,n=self.complete(c)
        self.assertEqual(p['accounting_determination'],'UNRESOLVED');self.assertFalse(n['proposed_journal_workpaper'])
        self.assertFalse(p['calculations']);self.assertTrue(any('200' in n['explanation'] for n in p['validation_requirements']))
    def test_boolean_disposal_boundary_direct(self):
        from source_execution import execute
        for invalid in (0,1,None,[],{},'true','false'):
            c=case();c.update(review_mode=h.MODE,source_assurance=h.PROFILE,package='fixed-assets')
            c['assets'][0]['disposal']={'enabled':invalid,'date':'2026-08-03','ordinary_sale':True,'proceeds':'20000'}
            with self.subTest(flag=invalid):
                n=execute('fixed-assets',c)
                self.assertEqual(n['accounting_determination'],'UNRESOLVED');self.assertFalse(n['proposed_journal_workpaper'])

if __name__=='__main__':unittest.main(verbosity=2)
