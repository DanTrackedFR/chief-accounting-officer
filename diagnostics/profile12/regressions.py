"""Diagnostic-only, expected-red regression suite. Run explicitly; never release acceptance."""
import copy,gzip,json,os,sys,unittest
from pathlib import Path
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from hosted_cao.tests import test_presumed_engineering_qa as support
HERE=Path(__file__).resolve().parent
OUT=Path(os.environ.get('CAO_DIAGNOSTIC_OUT','/tmp/cao-profile12-diagnostic'))
OUT.mkdir(parents=True,exist_ok=True)
def fixture(name):return json.loads((HERE/'fixtures'/f'{name}.json').read_text())
def dump(name,value):
 data=(json.dumps(value,indent=2,default=str)+'\n').encode()
 (OUT/(name+'.json.gz')).write_bytes(gzip.compress(data,mtime=0))
class Regressions(unittest.TestCase):
 def setUp(self):
  self.h=support.IndependentPresumedEngineeringQA();self.h.setUp();self.addCleanup(self.h.doCleanups)
  self.trace=[];original=self.h.http
  def traced(path,body=None,**headers):
   result=original(path,body,**headers);self.trace.append(dict(path=path,request=body,status=result[0],response=result[1]));return result
  self.h.http=traced
 def run_case(self,name,package='fixed-assets'):
  c=fixture(name);cid,job=self.h.complete(package,name,c);_,native=self.h.native(cid)
  # Reopen the persisted job store and retry the identical key, checking no duplicate workpaper.
  restarted=self.h.new_service();self.addCleanup(restarted.close)
  self.assertEqual(restarted.job(support.COMPANY,job['id'])['accounting'],job['accounting'])
  self.assertEqual(self.h.job(cid,name)[1]['accounting'],job['accounting'])
  self.assertEqual(self.h.native(cid)[1]['proposed_journal_workpaper'],native['proposed_journal_workpaper'])
  dump(name,dict(trace=self.trace,native=native,source_case_bytes=len(json.dumps(c).encode()),public_bytes=len(json.dumps(job['accounting']['public_result']).encode()),retry_and_restart_equal=True))
  return job['accounting']['public_result'],native
 def amount(self,p,label):return {r['label']:Decimal(r['amount']) for r in p['calculations']}.get(label)
 def test_control_fa(self):
  p,n=self.run_case('control-fa');self.assertEqual(self.amount(p,'depreciation'),1100);self.assertEqual(p['accounting_determination'],'SUPPORTED')
 def test_control_ap(self):
  p,n=self.run_case('control-ap','accounts-payable');self.assertEqual(self.amount(p,'invoices'),110);self.assertEqual(p['accounting_determination'],'SUPPORTED')
 def test_control_disposal(self):
  p,n=self.run_case('control-disposal');self.assertEqual(self.amount(p,'closing cost'),0);self.assertIn('cash',json.dumps(n['proposed_journal_workpaper'],default=str))
 def test_control_no_disposal(self):
  p,n=self.run_case('control-no-disposal');self.assertEqual(self.amount(p,'closing cost'),11000);self.assertNotIn('cash',json.dumps(n['proposed_journal_workpaper'],default=str))
 def test_control_accrual(self):
  p,n=self.run_case('control-accrual','accounts-payable');self.assertEqual(self.amount(p,'closing accruals'),200)
 def test_ENG_01(self):
  p,n=self.run_case('ENG-01');self.assertNotEqual(p['accounting_determination'],'SUPPORTED','Nonboolean disposal authorization must be rejected');self.assertNotIn('cash',json.dumps(n['proposed_journal_workpaper'],default=str))
 def test_ENG_02(self):
  p,n=self.run_case('ENG-02');self.assertFalse(p['calculations']);self.assertIn('assets:1',p['anomaly_report']['excluded_rows']);self.assertEqual(n['proposed_journal_workpaper'],[],'Rejected asset must contribute no persisted journal')
 def test_ENG_02_mixed(self):
  p,n=self.run_case('ENG-02-mixed');self.assertEqual(self.amount(p,'depreciation'),1100)
  debit=sum(Decimal(x['amount']) for entry in n['proposed_journal_workpaper'] for x in entry if x['account']=='depreciation expense' and x['side']=='Dr')
  self.assertEqual(debit,1100,'Only the valid row may contribute to persisted depreciation')
 def test_control_disputed(self):
  p,n=self.run_case('control-disputed','accounts-payable');self.assertIsNone(self.amount(p,'invoices'));self.assertEqual(p['accounting_determination'],'UNRESOLVED');self.assertTrue(p['validation_requirements'])
 def test_control_invalid_opening(self):
  p,n=self.run_case('control-invalid-opening');self.assertEqual(p['accounting_determination'],'UNRESOLVED');self.assertFalse(n['calculations'].get('assets'))
 def test_ENG_03(self):
  c=fixture('ENG-03');cid=self.h.start(rid='ENG-03');status,result=self.h.call('submit',case_id=cid,evidence=support.supplied(case=c))
  if status==200:
   _,job=self.h.job(cid,'ENG-03');self.h.service.run_one();done=self.h.http('/v1/jobs/'+job['id'])[1];_,native=self.h.native(cid)
  else:done=native=None
  dump('ENG-03',dict(trace=self.trace,native=native,done=done))
  self.assertIn(status,(400,422),'Source Case ID object must fail preacceptance');self.assertIn('evidence.facts.machinery.case_id',[x['field_path'] for x in result['error']['requirements']])
 def test_ENG_04(self):
  p,n=self.run_case('ENG-04');encoded=json.dumps(p);self.assertLessEqual(encoded.count('X'*8192),1,'Large source identity must not be replicated per finding')
 def test_ENG_05(self):
  p,n=self.run_case('ENG-05','accounts-payable');self.assertIsNone(self.amount(p,'closing ap'),'Conflicting supplied payments must withhold closing AP');self.assertTrue(p['validation_requirements']);self.assertEqual(self.amount(p,'invoices'),110)
 def test_ENG_06(self):
  for path in ('/v1/operations','/v1/jobs'):
   for op in ([],{}):
    status,result=self.h.http(path,self.h.envelope(op),**{'Idempotency-Key':'malformed'})
    dump('ENG-06-'+path.rsplit('/',1)[-1]+('-array' if isinstance(op,list) else '-object'),dict(trace=self.trace))
    with self.subTest(path=path,operation=op):
     self.assertIn(status,(400,422));self.assertEqual(result['error']['code'],'invalid_request');self.assertIn('operation',[x['field_path'] for x in result['error']['requirements']])
 def test_ACC_01(self):
  p,n=self.run_case('ACC-01');self.assertNotEqual(p['accounting_determination'],'SUPPORTED','Current additions cannot cure invalid opening accumulation');self.assertFalse(n['calculations'].get('assets'))
 def test_ACC_02(self):
  p,n=self.run_case('ACC-02','accounts-payable');self.assertNotIn('administrative expense',json.dumps(n['proposed_journal_workpaper'],default=str),'Refundable deposit conflicts with inherited service-expense default');self.assertNotEqual(p['accounting_determination'],'SUPPORTED')
 def test_ACC_03(self):
  p,n=self.run_case('ACC-03');self.assertNotIn('cash',json.dumps(n['proposed_journal_workpaper'],default=str),'Unpaid credit consideration cannot be debited to cash')
 def test_ACC_04(self):
  p,n=self.run_case('ACC-04','accounts-payable');self.assertEqual(self.amount(p,'invoices'),110,'Explicit negation does not establish a dispute');self.assertEqual(p['accounting_determination'],'SUPPORTED')
 def test_ACC_05(self):
  p,n=self.run_case('ACC-05','accounts-payable');self.assertEqual(self.amount(p,'closing accruals'),200,'Unrelated missing invoice supplier must not erase supported accrual');self.assertTrue(p['validation_requirements'])
if __name__=='__main__':unittest.main(verbosity=2)
