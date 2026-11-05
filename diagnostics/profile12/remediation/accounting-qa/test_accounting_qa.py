"""Independent, freshly authored accounting challenges through hosted HTTP and reopened Cases."""
import copy, gzip, hashlib, json, os, subprocess, sys, unittest
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from hosted_cao.tests import test_presumed_engineering_qa as support
OUT=Path(os.environ.get('CAO_ACCOUNTING_QA_OUT',str(Path(__file__).parent/'evidence')))
OUT.mkdir(parents=True,exist_ok=True)

def fresh(package='fixed-assets'):
    c=support.synthetic_case(package,1)
    c['case_id']='accounting-qa-fresh-source'
    c['source']['id']='accounting-qa-fresh-upload'
    if package=='fixed-assets':
        c['assets'][0].update(id='MACHINE-QA',opening_cost='24000',opening_accumulated='6000')
        c['class_assumptions']['machinery']['remaining_life']='6'
    else:
        c['invoices'][0].update(id='BILL-QA',supplier='QA vendor',invoice_number='QA-778',amount='360')
    return c

def disposal(c,**kw):
    c['assets'][0]['disposal']=dict(enabled=True,ordinary_sale=True,date='2026-12-31',proceeds='18000',cash_received=True,payment_terms='cash',**kw)
    return c

class AccountingQA(unittest.TestCase):
    def setUp(self):
        self.h=support.IndependentPresumedEngineeringQA();self.h.setUp();self.addCleanup(self.h.doCleanups)
    def run_case(self,c,package='fixed-assets',label=None):
        label=label or self._testMethodName
        cid,job=self.h.complete(package,label,c);_,n=self.h.native(cid)
        restart=self.h.new_service();self.addCleanup(restart.close)
        self.assertEqual(restart.job(support.COMPANY,job['id'])['accounting'],job['accounting'])
        self.assertEqual(self.h.job(cid,label)[1]['accounting'],job['accounting'])
        self.assertEqual(self.h.native(cid)[1]['proposed_journal_workpaper'],n['proposed_journal_workpaper'])
        payload=dict(input=c,job=job,native=n,retry_and_restart_equal=True,source=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),production_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'skills/source_execution.py',ROOT/'skills/source_screening.py']})
        (OUT/(label+'.json.gz')).write_bytes(gzip.compress(json.dumps(payload,default=str,indent=2).encode(),mtime=0))
        for entry in n['proposed_journal_workpaper']:
            self.assertEqual(sum(Decimal(x['amount']) for x in entry if x['side']=='Dr'),sum(Decimal(x['amount']) for x in entry if x['side']=='Cr'))
        return job['accounting']['public_result'],n
    def amount(self,p,name):return {r['label']:Decimal(r['amount']) for r in p['calculations']}.get(name)
    def debit(self,n,name):return sum(Decimal(x['amount']) for e in n['proposed_journal_workpaper'] for x in e if x['side']=='Dr' and x['account']==name)
    def test_disposal_boolean_invalid_variants(self):
        for i,value in enumerate([0,1,'true',None,[],{}]):
            c=disposal(fresh());c['assets'][0]['disposal']['enabled']=value
            p,n=self.run_case(c,label=self._testMethodName+str(i))
            self.assertEqual(n['proposed_journal_workpaper'],[]);self.assertEqual(p['accounting_determination'],'UNRESOLVED')
    def test_disposal_false_and_omission_preserve_asset(self):
        for i,value in enumerate([False,'omit']):
            c=fresh()
            if value is False:c['assets'][0]['disposal']={'enabled':False}
            p,n=self.run_case(c,label=self._testMethodName+str(i))
            self.assertEqual(self.amount(p,'closing cost'),24000);self.assertEqual(self.debit(n,'cash'),0);self.assertEqual(self.amount(p,'depreciation'),3000)
    def test_cash_disposal_positive(self):
        p,n=self.run_case(disposal(fresh()))
        self.assertEqual(self.debit(n,'cash'),18000);self.assertEqual(self.amount(p,'closing cost'),0);self.assertEqual(self.amount(p,'depreciation'),3000)
    def test_credit_disposal_positive(self):
        c=disposal(fresh());c['assets'][0]['disposal'].update(cash_received=False,payment_terms='credit')
        p,n=self.run_case(c)
        self.assertEqual(self.debit(n,'cash'),0);self.assertEqual(self.debit(n,'disposal receivable'),18000);self.assertEqual(self.amount(p,'closing cost'),0)
    def test_unknown_or_conflicting_settlement_no_cash(self):
        for i,mutation in enumerate([{'cash_received':False,'payment_terms':'cash'},{'cash_received':True,'payment_terms':'credit'},{'cash_received':'true','payment_terms':'cash'},None]):
            c=disposal(fresh())
            if mutation is None:
                c['assets'][0]['disposal'].pop('cash_received');c['assets'][0]['disposal'].pop('payment_terms')
            else:c['assets'][0]['disposal'].update(mutation)
            p,n=self.run_case(c,label=self._testMethodName+str(i));self.assertEqual(self.debit(n,'cash'),0);self.assertEqual(p['accounting_determination'],'UNRESOLVED');self.assertEqual(n['proposed_journal_workpaper'],[])
    def test_mixed_rejected_disposal_retains_only_valid_asset(self):
        c=disposal(fresh());c['assets'][0]['disposal']['proceeds']='invalid'
        good=copy.deepcopy(fresh()['assets'][0]);good['id']='SECOND-QA';c['assets'].append(good)
        p,n=self.run_case(c);self.assertEqual(self.amount(p,'depreciation'),3000);self.assertEqual(self.debit(n,'depreciation expense'),3000)
    def test_invalid_opening_with_addition_is_atomic(self):
        c=fresh();c['assets'][0].update(opening_cost='1000',opening_accumulated='1100',ready_date='2026-06-01')
        c['costs']=[dict(id='COST-QA',destination='MACHINE-QA',amount='5000',kind='purchase',date='2026-05-01',offset='accounts payable')]
        p,n=self.run_case(c);self.assertEqual(n['proposed_journal_workpaper'],[]);self.assertFalse(n['calculations']['assets']);self.assertFalse(n['calculations']['cost_rows'])
    def test_equal_opening_cost_accumulation_valid(self):
        c=fresh();c['assets'][0]['opening_accumulated']='24000'
        p,n=self.run_case(c);self.assertEqual(self.amount(p,'depreciation'),0);self.assertEqual(p['accounting_determination'],'SUPPORTED')
    def test_refundable_deposit_and_ordinary_service_mixed(self):
        c=fresh('accounts-payable');bad=copy.deepcopy(c['invoices'][0]);bad.update(id='DEPOSIT-QA',invoice_number='QA-DEP',description='Repayable security deposit',amount='900');c['invoices'].append(bad)
        p,n=self.run_case(c,'accounts-payable');self.assertEqual(self.amount(p,'invoices'),360);self.assertEqual(self.debit(n,'administrative expense'),360);self.assertTrue(p['validation_requirements'])
    def test_negated_and_affirmative_dispute_context(self):
        for i,description in enumerate(['This invoice is not currently disputed.','No outstanding dispute exists.','This invoice is not disputed, but the supplier disputes the obligation.']):
            c=fresh('accounts-payable');c['invoices'][0].update(description=description,disputed_obligation=False)
            p,n=self.run_case(c,'accounts-payable',label=self._testMethodName+str(i))
            if i<2:self.assertEqual(self.amount(p,'invoices'),360)
            else:self.assertEqual(p['accounting_determination'],'UNRESOLVED');self.assertEqual(n['proposed_journal_workpaper'],[])
    def test_new_dispute_verb_forms_respect_explicit_negation(self):
        for i,description in enumerate(['The supplier is not disputing this invoice.', 'There are no disputes concerning this invoice.', 'The supplier does not dispute this invoice.']):
            c=fresh('accounts-payable');c['invoices'][0].update(description=description,disputed_obligation=False)
            p,n=self.run_case(c,'accounts-payable',label=self._testMethodName+str(i));self.assertEqual(self.amount(p,'invoices'),360);self.assertEqual(p['accounting_determination'],'SUPPORTED')
    def test_structured_affirmative_overrides_text_negation(self):
        c=fresh('accounts-payable');c['invoices'][0].update(description='No dispute.',disputed_obligation=True)
        p,n=self.run_case(c,'accounts-payable');self.assertEqual(n['proposed_journal_workpaper'],[]);self.assertEqual(p['accounting_determination'],'UNRESOLVED')
    def test_payment_positive_and_conflict_preserve_invoice(self):
        for i,total in enumerate(['120','0']):
            c=fresh('accounts-payable');c.update(opening_ap_total='40',payments_total=total,payments=[dict(id='PAY-QA',amount='120',date='2026-07-01')])
            p,n=self.run_case(c,'accounts-payable',label=self._testMethodName+str(i));self.assertEqual(self.amount(p,'invoices'),360);self.assertEqual(self.debit(n,'administrative expense'),360)
            self.assertEqual(self.amount(p,'closing ap'),280 if i==0 else None)
    def test_invalid_payment_aggregate_retains_invoice(self):
        c=fresh('accounts-payable');c.update(opening_ap_total='0',payments_total='invalid')
        p,n=self.run_case(c,'accounts-payable');self.assertEqual(self.amount(p,'invoices'),360);self.assertEqual(self.debit(n,'administrative expense'),360);self.assertIsNone(self.amount(p,'closing ap'));self.assertTrue(p['validation_requirements'])
    def test_out_of_period_payment_detail_qualifies_balance(self):
        c=fresh('accounts-payable');c.update(opening_ap_total='0',payments_total='120',payments=[dict(id='PAY-QA',amount='120',date='2027-02-01')])
        p,n=self.run_case(c,'accounts-payable');self.assertEqual(self.amount(p,'invoices'),360);self.assertIsNone(self.amount(p,'closing ap'));self.assertTrue(p['validation_requirements'])
    def accrual_case(self):
        c=fresh('accounts-payable');c['invoices'][0]['supplier']=None
        c['accruals']=[dict(id='AC-QA',supplier='Other vendor',units='7',rate='80',received_date='2026-08-01',received_supported=True,invoiced_received='60',opening_accrual='90',account='consulting expense',recognition_basis='services_received',invoice_overlap_resolved=True)]
        return c
    def test_malformed_invoice_preserves_independent_accrual(self):
        p,n=self.run_case(self.accrual_case(),'accounts-payable');self.assertEqual(self.amount(p,'closing accruals'),500);self.assertEqual(self.debit(n,'consulting expense'),410);self.assertTrue(p['validation_requirements'])
    def test_unresolved_overlap_remains_blocked(self):
        c=self.accrual_case();c['accruals'][0].pop('invoice_overlap_resolved')
        p,n=self.run_case(c,'accounts-payable');self.assertIsNone(self.amount(p,'closing accruals'));self.assertEqual(n['proposed_journal_workpaper'],[])
    def test_malformed_accrual_supplier_not_authorized_by_overlap(self):
        c=self.accrual_case();c['accruals'][0]['supplier']={'bad':'reference'}
        p,n=self.run_case(c,'accounts-payable');self.assertIsNone(self.amount(p,'closing accruals'));self.assertEqual(n['proposed_journal_workpaper'],[])

if __name__=='__main__':unittest.main(verbosity=2)
