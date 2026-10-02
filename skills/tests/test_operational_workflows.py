import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path
from decimal import Decimal
sys.path.insert(0,str(Path(__file__).resolve().parent))
from operational_cases import PACKAGES,operational,certified,approved
from additional_cases import certify
from production import assess_case,to_public,case_fingerprint,canonical_knowledge,PACKAGES as REGISTRY
from core_accounting import balance

class OperationalTests(unittest.TestCase):
    def test_saved_public_CLI_examples(self):
        root=Path(__file__).resolve().parents[2]
        for p in PACKAGES:
            for fw in ['IFRS','US_GAAP','UK_GAAP','AASB']:
                folder=root/'skills'/p/'examples';case=folder/(fw+'.case.json')
                proc=subprocess.run([sys.executable,str(root/'skills/run_skill.py'),p,str(case),'--route','export'],capture_output=True,text=True,check=True)
                self.assertEqual(json.loads(proc.stdout),json.loads((folder/(fw+'.public.json')).read_text()))
                self.assertNotIn('reviewer_signoff',json.loads(case.read_text()))

    def check(self,p,c):
        r=assess_case(p,certify(p,c));self.assertEqual(r['status'],'complete',r['conclusion'])
        for j in r['journal_entry_implications']:balance(j)
        return r

    def test_all_frameworks_and_public_routes(self):
        for p in PACKAGES:
            for fw in ['IFRS','US_GAAP','UK_GAAP','AASB']:
                with self.subTest(p=p,fw=fw):
                    c=certified(p,fw);snapshot=copy.deepcopy(c);r=assess_case(p,c);self.assertEqual(r['status'],'complete',r['conclusion']);self.assertEqual(c,snapshot)
                    for j in r['journal_entry_implications']:balance(j)
                    for route in ['answer','answer_context','retrieval_snippet','citation','tool_output','user_log','export']:
                        public=json.dumps(to_public(r,route),default=str);self.assertNotIn('synthetic independent reviewer',public);self.assertNotIn('knowledge_documents',public)

    def test_exact_numerics(self):
        expectations={'month-end-close':('close_day','6'),'balance-sheet-reconciliations':('gross_reconciling_items','0'),'accounts-receivable':('closing_ar','120'),'accounts-payable':('closing_accruals','9600'),'fixed-assets':('depreciation','90000'),'intercompany-accounting':('recharges','0')}
        for p,(k,n) in expectations.items():self.assertEqual(self.check(p,operational(p))['calculations'][k],Decimal(n))

    def test_common_control_adverse_matrix(self):
        changes=[('complete',False),('as_of','2026-11-30'),('population_count',999),('population_amount','999'),('reviewer','synthetic source owner')]
        for p in PACKAGES:
            for fw in ['IFRS','US_GAAP','UK_GAAP','AASB']:
                for k,v in changes:
                    with self.subTest(p=p,fw=fw,k=k):
                        c=operational(p,fw);c['controls'][k]=v;self.assertEqual(assess_case(p,certify(p,c))['status'],'blocked')

    def test_missing_stale_and_self_approval(self):
        rows={'month-end-close':'tasks','balance-sheet-reconciliations':'reconciliations','accounts-receivable':'invoices','accounts-payable':'invoices','fixed-assets':'assets','intercompany-accounting':'pairs'}
        for p in PACKAGES:
            for mutation in ['stale','self','missing','late']:
                c=operational(p);r=c[rows[p]][0]
                if mutation=='stale':r['approved_version']='old'
                elif mutation=='self':r['reviewer']=r['owner']
                elif mutation=='missing':r['evidence']=''
                else:r['approval_date']='2027-01-06'
                self.assertEqual(assess_case(p,certify(p,c))['status'],'blocked',(p,mutation))
            c=certified(p);c.pop('reviewer_signoff');self.assertEqual(assess_case(p,c)['status'],'partial')
            c=certified(p);c['judgment_memo']+=' modified';self.assertEqual(assess_case(p,c)['status'],'partial')
            c=certified(p);c['knowledge_review']['documents'][0]['sha256']='stale';self.assertEqual(assess_case(p,c)['status'],'blocked')

    def test_close_adverse(self):
        for mutation in ['cycle','reject','lock','reopen','duplicate','late_approval','overaccrue']:
            c=operational('month-end-close')
            if mutation=='cycle':c['tasks'][0]['predecessors']=['statements']
            elif mutation=='reject':c['tasks'][0]['unresolved_count']=1
            elif mutation=='lock':c['close']['exceptions']=['unresolved']
            elif mutation=='reopen':c['close']['reopened']=True
            elif mutation=='duplicate':c['journals'].append(copy.deepcopy(c['journals'][0]))
            elif mutation=='late_approval':c['journals'][0]['posted_at']='2026-12-30'
            else:c['accruals'][0]['gl_adjustment']='75000'
            self.assertEqual(assess_case('month-end-close',certify('month-end-close',c))['status'],'blocked',mutation)

    def test_reconciliation_gross_and_coverage(self):
        c=operational('balance-sheet-reconciliations');r=c['reconciliations'][0]
        r['items']=[approved('a',amount='5000',opened='2026-12-31',resolution='timing',source_id='X',gl_id='Y',status='supported_timing'),approved('b',amount='-5000',opened='2026-12-31',resolution='timing',source_id='Y',gl_id='X',status='supported_timing')]
        self.assertEqual(assess_case('balance-sheet-reconciliations',certify('balance-sheet-reconciliations',c))['status'],'blocked')
        r['threshold']='10000';r['relative_threshold']='0.1';self.assertEqual(self.check('balance-sheet-reconciliations',c)['calculations']['gross_reconciling_items'],Decimal('10000'))
        r['items'][0]['opened']='2025-01-01';self.assertEqual(assess_case('balance-sheet-reconciliations',certify('balance-sheet-reconciliations',c))['status'],'blocked')

    def test_receivable_bad_cash_credit_dispute(self):
        for route in ['excess','other_customer','credit','bank','dispute','handoff']:
            c=operational('accounts-receivable')
            if route=='excess':c['receipts'][0]['allocations'][0]['amount']='151'
            elif route=='other_customer':c['receipts'][0]['customer']='OTHER'
            elif route=='credit':c['credits'][0]['reason']='writeoff'
            elif route=='bank':c['bank_total']='201'
            elif route=='dispute':c['invoices'][0]['disputed']=True
            else:c['handoffs']['ecl']['resolved']=False
            self.assertEqual(assess_case('accounts-receivable',certify('accounts-receivable',c))['status'],'blocked',route)

    def test_payable_duplicate_match_payment_accrual(self):
        for route in ['duplicate','match','payment','unreceived','reversal','gl']:
            c=operational('accounts-payable')
            if route=='duplicate':r=copy.deepcopy(c['invoices'][0]);r['id']='new';c['invoices'].append(r)
            elif route=='match':c['invoices'][0]['po_amount']='119'
            elif route=='payment':c['payments'][0]['payment_releaser']=c['payments'][0]['payment_preparer']
            elif route=='unreceived':c['accruals'][0]['received_supported']=False
            elif route=='reversal':c['accruals'][0]['reversal_date']='2026-12-31'
            else:c['gl_ap']='21'
            self.assertEqual(assess_case('accounts-payable',certify('accounts-payable',c))['status'],'blocked',route)

    def test_asset_revision_disposal_and_units(self):
        p='fixed-assets';c=operational(p);a=c['assets'][0];a['change']={'enabled':True,'date':'2026-01-01','new_remaining_life':'7','new_residual':'60000','new_information':True,'evidence':'engineering','units_before':'0','units_after':'0'};a['expected_depreciation']='51428.57';a['gl_accumulated']='231428.57';c['gl']['accumulated']='231428.57'
        self.assertEqual(self.check(p,c)['calculations']['depreciation'],Decimal('51428.57'))
        a['disposal']={'enabled':True,'date':'2026-12-31','proceeds':'400000','ordinary_sale':True,'evidence':'sale/bank'};a['gl_cost']='0';a['gl_accumulated']='0';c['gl'].update(cost='0',accumulated='0')
        self.assertEqual(self.check(p,c)['calculations']['assets'][0]['disposal_gain'],Decimal('31428.57'))
        c=operational(p);a=c['assets'][0];a.update(method='units_of_production',remaining_units='70000',period_units='10000',expected_depreciation='51428.57',gl_accumulated='231428.57');c['gl']['accumulated']='231428.57';self.check(p,c)

    def test_asset_ready_cip_and_gross_net(self):
        p='fixed-assets';c=operational(p);c['gl']['cost']='650000';c['gl']['accumulated']='320000';self.assertEqual(assess_case(p,certify(p,c))['status'],'blocked')
        c=operational(p);c['cip']=[approved('project',opening='100',transfer='0',asset_id='machine',ready_date='2026-12-31',ready=True,impairment_reviewed=True,gl_closing='100')];c['gl']['cip']='100';self.assertEqual(assess_case(p,certify(p,c))['status'],'blocked')

    def test_intercompany_mismatch_and_rates(self):
        p='intercompany-accounting'
        for mutation in ['principal','rate','gl','confirmation','specialist']:
            c=operational(p)
            if mutation=='principal':c['pairs'][0]['opening_b']='95'
            elif mutation=='rate':c['pairs'][0]['rate_a']='0'
            elif mutation=='gl':c['pairs'][0]['gl_a']='121'
            elif mutation=='confirmation':c['pairs'][0]['confirmed_b']='95'
            else:c['handoffs']['transfer_pricing']['resolved']=False
            self.assertEqual(assess_case(p,certify(p,c))['status'],'blocked',mutation)

    def test_framework_and_period_scopes(self):
        for p in PACKAGES:
            for fw in ['UK_GAAP','AASB','US_GAAP','IFRS']:
                c=operational(p,fw);c['applicability_review']['effective_period'][0]='2025-01-01';self.assertEqual(assess_case(p,certify(p,c))['status'],'blocked')
        c=operational('fixed-assets','US_GAAP');c['asset_policy']['model']='revaluation';self.assertEqual(assess_case('fixed-assets',certify('fixed-assets',c))['status'],'blocked')

if __name__=='__main__':unittest.main()
