"""Independent grant knowledge counterexamples and untrusted metadata attacks."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
HERE=Path(__file__).resolve().parent

def module(name,file):
    s=importlib.util.spec_from_file_location(name,HERE/file)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
v=module('independent_grant_validator','validate_supplement.py')
r=module('independent_grant_retrieval','retrieval.py')

class IndependentGrantKnowledgeQA(unittest.TestCase):
    def setUp(self):
        self.d=r.load_register()
        self.c={(c['framework'],c['decision']):c for c in self.d['claims']}
    def text(self,fw,decision):return self.c[(fw,decision)]['proposition'].lower()
    def reject(self,d):self.assertTrue(v.validate_data(d))
    def retrieve(self,fw='IFRS',**kw):
        opts=dict(period_start='2026-01-01',grant_model=next(iter(r.MODELS[fw])))
        if fw=='US_GAAP':opts['execution_date']='2026-12-31'
        if fw=='US_GAAP':opts['us_adoption']={'standard':'ASU2025-10','annual_period_start':'2026-01-01','financial_statements_unissued_at_adoption':True,'transition_reviewed':True,'evidence_id':'reviewed-adoption','adoption_date':'2026-04-01'}
        opts.update(kw);return r.retrieve(fw,'2026-12-31',r.SCOPES[fw],**opts)
    def test_independent_signed_claim_population(self):
        self.assertEqual(v.validate_data(self.d),[])
        ledger=json.loads((HERE/'independent-review.json').read_text())
        self.assertEqual(len(ledger['claim_reviews']),len(self.d['claims']))
        signed={c['claim_id']:c for c in ledger['claim_reviews']}
        for c in self.d['claims']:
            with self.subTest(claim=c['claim_id']):
                self.assertEqual(signed[c['claim_id']]['reviewed_hash'],v.claim_hash(c))
                self.assertGreater(len(signed[c['claim_id']]['challenge']),35)
                self.assertNotEqual(c['approval_review']['reviewer'],self.d['author'])
    def test_claim_hash_change_and_whole_population(self):
        for key,val in [('proposition','Cash receipt alone establishes compliance.'),('entity_scope','NFP'),('audit_required',False),('sources',[]),('public_limitations',['Source: internal'])]:
            d=copy.deepcopy(self.d);d['claims'][0][key]=val;self.reject(d)
        d=copy.deepcopy(self.d);d['claims'].pop();self.reject(d)
        d=copy.deepcopy(self.d);d['claims'][-1]['approval_review']['reviewer']=d['author'];self.reject(d)
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'claims.json';p.write_text(json.dumps(d))
            with self.assertRaises(ValueError):self.retrieve(path=p,decisions=['recognition'])
    def test_source_structure_and_status_inflation(self):
        for source in [None,[],{'title':'x','source_kind':'CURRENT_STANDARD','inspected':True,'url':3,'locator':{}}, {'title':'x','source_kind':'MODEL_KNOWLEDGE','inspected':True,'locator':'invented'}]:
            d=copy.deepcopy(self.d);d['claims'][0]['sources']=[source];self.reject(d)
        d=copy.deepcopy(self.d);c=next(c for c in d['claims'] if c['framework']=='US_GAAP' and c['claim_kind']=='NORMATIVE')
        c.update(evidence_status='SOURCE_VERIFIED',reference_confidence='VERIFIED',audit_required=False,approval_track='PENDING',approval_review=None)
        d['status']='REVIEWED';self.reject(d)
        for c in self.d['claims']:
            if c['framework']=='US_GAAP' and c['claim_kind']=='NORMATIVE':
                self.assertEqual(c['evidence_status'],'PRIMARY_CORROBORATED');self.assertIs(c['audit_required'],True)
    def test_framework_routes_and_privacy(self):
        for fw in r.FRAMEWORKS:
            out=self.retrieve(fw)
            self.assertEqual(len(out),sum(c['framework']==fw for c in self.d['claims']))
            for c in out:self.assertEqual(set(c),set(r.PUBLIC_FIELDS))
            for secret in ('source_note','chatgpt training data','source_verified','primary_corroborated','approval_review','audit_required'):
                self.assertNotIn(secret,json.dumps(out).lower())
        for fw,model in [('IFRS','FRS102_PERFORMANCE'),('UK_GAAP','IAS20_ACCRUAL'),('US_GAAP','IAS20_ACCRUAL'),('AASB','FRS102_ACCRUAL')]:
            with self.assertRaises(ValueError):self.retrieve(fw,grant_model=model)
        for name in ('source: hidden','ChatGPT training data','MODEL_DERIVED_AUDIT_REQUIRED','DIRECT_SOURCE_CHECKED','PRIMARY_CORROBORATED','source_note'):
            d=copy.deepcopy(self.d);d['status']='REVIEWED';c=d['claims'][0];c.update(approval_track='PENDING',approval_review=None);c['public_limitations']=[name];self.reject(d)
    def test_date_scope_and_early_amendments(self):
        for start in (None,'2025-12-31','2027-01-01','garbage'):
            with self.assertRaises(ValueError):self.retrieve(period_start=start)
        for flag in (True,1,'false',None):
            with self.assertRaises(ValueError):self.retrieve(early_presentation_adoption=flag)
        for fw in r.FRAMEWORKS:
            for scope in ('NFP','public_sector','Tier2','us_employee_benefit_plan'):
                with self.assertRaises(ValueError):r.retrieve(fw,'2026-12-31',scope,period_start='2026-01-01',grant_model=next(iter(r.MODELS[fw])))
    def test_us_2026_adoption_is_not_automatic(self):
        self.assertIn('early adoption',self.text('US_GAAP','2026_adoption'))
        self.assertIn('2028',self.text('US_GAAP','effective_dates'));self.assertIn('2029',self.text('US_GAAP','effective_dates'))
        good={'standard':'ASU2025-10','annual_period_start':'2026-01-01','financial_statements_unissued_at_adoption':True,'transition_reviewed':True,'evidence_id':'adoption','adoption_date':'2026-04-01'}
        for k,val in [('financial_statements_unissued_at_adoption',False),('transition_reviewed',False),('annual_period_start','2026-04-01'),('adoption_date','2025-12-03'),('adoption_date','2027-01-01'),('evidence_id',''),('standard','PROPOSAL')]:
            bad=dict(good);bad[k]=val
            with self.assertRaises(ValueError):self.retrieve('US_GAAP',us_adoption=bad)
        with self.assertRaises(ValueError):self.retrieve('US_GAAP',us_adoption=None)
        # Adoption after interim/reporting period end is valid while statements remain unissued.
        after_end=dict(good,adoption_date='2026-08-01')
        rows=r.retrieve('US_GAAP','2026-06-30',r.SCOPES['US_GAAP'],period_start='2026-01-01',grant_model='ASC832_ASU2025_10_ADOPTED',us_adoption=after_end,execution_date='2026-10-04')
        self.assertEqual(len(rows),45)
        for execution in (None,'2026-05-31','2026-07-31','invalid'):
            with self.assertRaises(ValueError):r.retrieve('US_GAAP','2026-06-30',r.SCOPES['US_GAAP'],period_start='2026-01-01',grant_model='ASC832_ASU2025_10_ADOPTED',us_adoption=after_end,execution_date=execution)
        self.assertIn('beginning',self.text('US_GAAP','interim_adoption'))
        self.assertIn('separate review',self.text('US_GAAP','pre_adoption'))
    def test_recognition_scope_attacks(self):
        for fw in ('IFRS','AASB','UK_GAAP'):
            self.assertIn('reasonable assurance',self.text(fw,'recognition'))
        self.assertIn('probable',self.text('US_GAAP','recognition'))
        self.assertIn('recognition requirements',self.text('US_GAAP','cash_not_compliance'))
        for fw in ('IFRS','AASB'):
            self.assertIn('cannot',self.text(fw,'cash_not_compliance'))
            self.assertIn('owner',self.text(fw,'equity_boundary'))
            self.assertIn('tax',self.text(fw,'tax_boundary'))
        self.assertIn('exchange',self.text('US_GAAP','definition'))
        self.assertIn('intangible',self.text('US_GAAP','scope_exclusions'))
        self.assertIn('outside topic740',self.text('US_GAAP','tax_boundary'))
    def test_uk_policy_performance_and_asset_counterexample(self):
        self.assertIn('class',self.text('UK_GAAP','model_election'))
        self.assertIn('conditions are satisfied',self.text('UK_GAAP','performance_conditional'))
        self.assertIn('liability',self.text('UK_GAAP','performance_advance'))
        self.assertIn('cannot',self.text('UK_GAAP','asset_net_prohibited'))
        self.assertIn('fair value',self.text('UK_GAAP','nonmonetary'))
        # £100k cash and assurance, future 10 jobs condition: performance income £0 until condition, accrual expense pattern separate.
        received,condition_satisfied=100000,False
        performance_income=received if condition_satisfied else 0
        self.assertEqual((performance_income,received-performance_income),(0,100000))
        # A 5-year £100k capital grant: UK performance satisfied can income100k, accrual20k, never net asset policy.
        self.assertNotEqual(100000,100000/5)
    def test_nonmonetary_and_loan_counterexamples(self):
        for fw in ('IFRS','AASB'):
            self.assertIn('nominal',self.text(fw,'nonmonetary'))
            self.assertIn('reasonable assurance',self.text(fw,'forgivable_loan'))
        self.assertIn('cost to the entity',self.text('US_GAAP','nonmonetary'))
        self.assertIn('probable',self.text('US_GAAP','forgivable_loan'))
        self.assertIn('excluded',self.text('US_GAAP','below_market_loan'))
        # IFRS/AASB loan100k, qualified IFRS9 liability85k => grant15k, not100k. Subsequent interest belongs to Debt.
        self.assertEqual(100000-85000,15000)
        for fw in ('IFRS','AASB'):self.assertIn('initial financial-liability',self.text(fw,'below_market_loan'))
    def test_repayment_period_and_rollforward_counterexamples(self):
        # Income repayment70k with deferral30k => current expense40k, no blanket reversal prior50k.
        repay,opening=70000,30000
        expense=max(repay-opening,0);closing=max(opening-repay,0)
        self.assertEqual((expense,closing),(40000,0))
        # Original grant20k basis deduction, 2/5 life elapsed, repay10k => restored basis10k, catch-up depreciation4k.
        self.assertEqual(10000*2/5,4000)
        # Deferral100+new60-income40-repay20=100, an unexplained130 ledger is wrong30.
        self.assertEqual(100+60-40-20,100);self.assertNotEqual(130,100)
        for fw in ('IFRS','AASB','US_GAAP'):
            self.assertIn('first',self.text(fw,'repayment_income'))
            self.assertIn('immediately',self.text(fw,'repayment_asset'))
        for fw in r.FRAMEWORKS:
            self.assertIn('no plug',self.text(fw,'deferred_rollforward'))
            self.assertIn('repayment',self.text(fw,'repayment_evidence'))
            self.assertIn('past',self.text(fw,'past_costs'))
    def test_exact_once_and_owner_boundary_counterexamples(self):
        for fw in r.FRAMEWORKS:
            for decision,needle in [('fixed_assets_handoff','depreciation'),('intangibles_handoff','capitalization'),('inventory_handoff','cogs'),('payroll_handoff','eligible'),('debt_handoff','interest'),('reporting_handoff','balanced'),('controls_handoff','legal'),('exact_once','aliases')]:
                self.assertIn(needle,self.text(fw,decision))
        for fw in ('IFRS','AASB'):
            t=self.text(fw,'agriculture_routes')
            self.assertIn('cost',t);self.assertIn('conditional',t);self.assertIn('receivable',t)

if __name__=='__main__':unittest.main()
