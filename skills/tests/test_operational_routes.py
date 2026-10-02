"""Route, boundary, integration and independent-QA defect regressions."""
import copy,json,sys,unittest
from decimal import Decimal
from pathlib import Path
from operational_cases import PACKAGES,operational,approved,certified,handoffs
from additional_cases import certify,impairment,fx
from cases import revenue,ecl,consolidation
from production import assess_case,to_public

class RouteTests(unittest.TestCase):
    def run_case(self,p,c,status='complete'):
        # Select only FRS102 propositions while retaining full reviewed register.
        c=certify(p,c)
        if c['framework']=='UK_GAAP':
            from production import canonical_knowledge,PACKAGES as R,case_fingerprint
            claims,_=canonical_knowledge(R[p][1],c['framework']);c['knowledge_review']['applied_claim_ids']=[x['claim_id'] for x in claims if not any(z in x['proposition'].replace(' ','') for z in ['FRS101','FRS105'])];c['reviewer_signoff']['case_fingerprint']=case_fingerprint(c)
        r=assess_case(p,c);self.assertEqual(r['status'],status,r['conclusion']);return r

    def test_postperiod_approval_and_reopen(self):
        p='month-end-close';c=operational(p)
        for t in c['tasks']+c['journals']+c['accruals']+[c['close']]:t['approval_date']='2027-01-03'
        c['journals'][0]['posted_at']='2027-01-03';self.run_case(p,c)
        c['close'].update(reopened=True,reopen_authorization='Authorized actual reopen',reclose_evidence='Full recertification');self.run_case(p,c)
        c['tasks'][0]['actual_finish_day']='3';self.run_case(p,c,'blocked')

    def test_no_boolean_memos_or_identities(self):
        for p in PACKAGES:
            c=operational(p);c['controls']['owner']=True;self.run_case(p,c,'blocked')
        for p in ['accounts-receivable','accounts-payable','fixed-assets','intercompany-accounting']:
            c=operational(p);next(iter(c['handoffs'].values()))['evidence']=False;self.run_case(p,c,'blocked')

    def test_cross_account_correction_cannot_hide_offset(self):
        p='balance-sheet-reconciliations';c=operational(p);c['reconciliations'][0]['adjustments'][0]['offset']='equity';self.run_case(p,c,'blocked')
        c=operational(p);c['inventory'].pop();c['reconciliations'].pop();c['controls'].update(population_count=1,population_amount='130000');self.run_case(p,c,'blocked')

    def test_supported_collection_and_empty_cash(self):
        p='accounts-receivable';c=operational(p);c['invoices'][0]['due_date']='2026-11-01';c['collections']=[approved('COL',invoice_id='opening',next_action='follow_up',next_date='2027-01-06',dispute_evidence='No commercial dispute',status='follow_up')];r=self.run_case(p,c);self.assertEqual(r['calculations']['ageing']['31_60'],Decimal('30'))
        c=operational(p);c['receipts']=[];c['bank_total']='0';c['gl_ar']='240';c['gl_unapplied']='0';c['closing_customers'][0]['balance']='240';self.run_case(p,c)

    def test_accrual_invoice_clear_without_double_expense(self):
        p='accounts-payable';c=operational(p);a=c['accruals'][0];a.update(opening_accrual='120',units='0',invoiced_received='0',gl_closing='0',subsequent_actual='0');c['invoices'][0]['accrual_id']='A1';c['gl_accrual']='0';c['controls']['population_amount']='120';r=self.run_case(p,c)
        expense=sum((x['amount'] if x['side']=='Dr' else -x['amount'] for j in r['journal_entry_implications'] for x in j if x['account'] in ['expense','professional services expense']),Decimal(0));self.assertEqual(expense,0)

    def test_asset_capitalization_cip_transfer_and_training(self):
        p='fixed-assets';c=operational(p);a=c['assets'][0];a.update(opening_cost='0',opening_accumulated='0',residual='0',remaining_life='10',ready_date='2026-12-31',expected_depreciation='0.03',gl_cost='100',gl_accumulated='0.03');c['costs']=[approved('cap',amount='100',date='2026-12-30',eligible=True,eligibility_memo='Installation before readiness',kind='installation',destination='project',account='expense',offset='AP',recognition_reviewed=True),approved('training',amount='20',date='2026-12-30',eligible=False,eligibility_memo='Training excluded',kind='training',destination='machine',account='training expense',offset='AP',recognition_reviewed=True)];c['cip']=[approved('project',opening='0',transfer='100',asset_id='machine',ready_date='2026-12-31',ready=True,impairment_reviewed=True,gl_closing='0')];c['project_inventory']=['project'];c['gl'].update(cost='100',accumulated='0.03');c['controls'].update(population_count=2,population_amount='120');r=self.run_case(p,c);self.assertEqual(r['calculations']['excluded_expense'],20)
        c['costs'][1]['eligible']=True;self.run_case(p,c,'blocked')

    def test_half_year_and_leap_day_depreciation(self):
        p='fixed-assets';c=operational(p);c['assets'][0]['ready_date']='2026-07-01';c['assets'][0]['expected_depreciation']='45369.86';c['assets'][0]['gl_accumulated']='225369.86';c['gl']['accumulated']='225369.86';self.run_case(p,c)
        from production import load_workflow
        from datetime import date
        calc=load_workflow(p).charge;self.assertEqual(calc(date(2024,2,29),date(2024,2,29),Decimal('36600'),Decimal('1'),'straight_line'),Decimal('100.00'))

    def test_recharge_rounding_and_entity_journals(self):
        p='intercompany-accounting';c=operational(p);pair=c['pairs'][0];pair.update(opening_a='0',opening_b='0',opening_book_a='0',opening_book_b='0',recharge='1050',confirmed_a='1050',confirmed_b='1050',book_a='1050',book_b='1050',gl_a='1260',gl_b='1155');c['recharges']=[approved('R1',cost_pool='1000',allocations=[{'id':'B','entity':'Synthetic Sub','pair_id':'AB','share':'1'}],markup='0.05',agreement='Reviewed signed agreement',tax_review='Specialist supported pricing policy',date='2026-12-31',provider='Synthetic Group',currency='USD',source_complete=True)];c['controls']['population_amount']='1050';r=self.run_case(p,c);self.assertEqual(r['calculations']['recharges'],Decimal('1050'));self.assertEqual(r['calculations']['journal_entities'][:2],['Synthetic Group','Synthetic Sub'])
        c['recharges']=[];self.run_case(p,c,'blocked')

    def test_settlement_fx_and_invalid_book(self):
        p='intercompany-accounting';c=operational(p);r=c['pairs'][0];r.update(settled_a='100',settled_b='100',settlement_rate_a='1.2',settlement_rate_b='1.1',confirmed_a='0',confirmed_b='0',book_a='-20',book_b='-10',gl_a='0',gl_b='0');out=self.run_case(p,c);self.assertEqual(out['calculations']['pairs'][0]['a_fx_gain'],Decimal('20'));r['book_a']='0';self.run_case(p,c,'blocked')

    def test_existing_skill_result_integration(self):
        for fw in ['IFRS','US_GAAP','UK_GAAP','AASB']:
            p='accounts-receivable';c=operational(p,fw)
            for key,target,other in [('revenue','Revenue Recognition','revenue-recognition'),('ecl','ECL','financial-instruments-ecl')]:
                downstream=revenue(fw) if key=='revenue' else ecl(fw);r=assess_case(other,downstream);self.assertEqual(r['status'],'complete',r['conclusion']);c['handoffs'][key]['result']=r
            self.run_case(p,c);c['handoffs']['ecl']['result']['status']='partial';self.run_case(p,c,'blocked')
        p='fixed-assets';c=operational(p);r=assess_case('asset-impairment',certify('asset-impairment',impairment()));self.assertEqual(r['status'],'complete');c['handoffs']['impairment']['result']=r;self.run_case(p,c)
        p='intercompany-accounting';c=operational(p);c['handoffs']['fx']['result']=assess_case('foreign-currency',certify('foreign-currency',fx()));c['handoffs']['consolidation']['result']=assess_case('consolidation',consolidation());self.run_case(p,c)

    def test_numeric_boundaries_and_public_contamination(self):
        for p in PACKAGES:
            for n in ['NaN','Infinity',True,0.1,'-1']:
                c=operational(p);c['controls']['population_amount']=n;self.run_case(p,c,'blocked')
        p='accounts-receivable';c=operational(p);c['invoices'][1]['offset']='Source: ChatGPT training data';self.run_case(p,c,'blocked')

    def test_unsupported_scope_and_prior_edition(self):
        for p in PACKAGES:
            for fw in ['UK_GAAP','AASB']:
                c=operational(p,fw)
                if fw=='UK_GAAP':c['uk_standard']='FRS_105'
                else:c['entity_type']='not_for_profit'
                self.run_case(p,c,'blocked')
        # Operational mechanics use the supplied historical edition; they do
        # not silently replace pre-2026 FRS102 recognition with revised revenue.
        c=operational('accounts-receivable','UK_GAAP');c['period_start']='2025-01-01';c['invoices'][0]['invoice_date']='2024-12-01';c['policy_elections']['section23_model']='legacy';c['applicability_review']['effective_period'][0]='2025-01-01';self.run_case('accounts-receivable',c)

if __name__=='__main__':unittest.main()
