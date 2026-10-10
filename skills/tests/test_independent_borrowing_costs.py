"""Independent synthetic adversarial QA. Test approvals do not authenticate people.
Local assessor probes are deliberately separate from production release acceptance.
"""
import copy
import importlib.util
import json
import unittest
from unittest.mock import patch
from decimal import Decimal
from pathlib import Path
from borrowing_costs_cases import case, remeasure, ready
from core_accounting import ReviewRequired
from production import assess_case, to_public, serializable
from interfaces.public_output import ROUTES

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('_independent_borrowing_workflow',ROOT/'skills/borrowing-costs/workflow.py')
workflow=importlib.util.module_from_spec(spec);spec.loader.exec_module(workflow)
CLAIMS=[dict(topic_id='SUPPLEMENTAL_BORROWING_COSTS')]

def fresh(fw='IFRS',method='mixed'):
    c=case(fw,method);c['case_id']='Independent synthetic 137 percent borrowing QA '+fw
    p=c['projects'][0];p['opening_expenditure']='137000';p['expenditures'][0]['amount']='137000'
    for b in c['borrowings']:
        b['opening_principal']=str(Decimal(b['opening_principal'])*Decimal('1.37'))
    c=remeasure(c)
    # Source capture is explicit; later adversarial remeasure must preserve it.
    from borrowing_costs_cases import capture_sources
    return capture_sources(c)

def uk_compound(method):
    rate=Decimal('.08')/365;a=1+rate
    first=Decimal('137000')*rate;second=2*first
    if method=='mixed':
        first-=Decimal('68500')*rate;second-=Decimal('68500')*rate
        first+=Decimal('4110')/365;second+=Decimal('4110')/365
    return (first*(a**181-1)/rate*a**184+second*(a**184-1)/rate).quantize(Decimal('.01'))

class IndependentBorrowingCosts(unittest.TestCase):
    def local(self,c):return workflow.assess(c,CLAIMS)
    def blocked(self,c):
        with self.assertRaises(ReviewRequired):self.local(c)
    def test_fresh_mixed_framework_values(self):
        for fw in ('IFRS','AASB','US_GAAP','UK_GAAP'):
            r=self.local(fresh(fw));expected=uk_compound('mixed') if fw=='UK_GAAP' else Decimal('15115.04');self.assertEqual(expected,r['calculations']['capitalized'])
    def test_specific_framework_difference(self):
        for fw,value in [('IFRS','20550.00'),('AASB','20550.00'),('UK_GAAP','20550.00'),('US_GAAP','12363.78')]:
            self.assertEqual(Decimal(value),self.local(fresh(fw,'specific'))['calculations']['capitalized'])
    def test_general_only_independent_weighting(self):
        for fw in ('IFRS','AASB','US_GAAP','UK_GAAP'):
            expected=uk_compound('general') if fw=='UK_GAAP' else Decimal('16485.04');self.assertEqual(expected,self.local(fresh(fw,'general'))['calculations']['capitalized'])
    def test_journal_allocates_only_existing_expense(self):
        r=self.local(fresh())
        for entry in r['journal_entry_implications']:
            self.assertEqual({'Construction asset','Interest expense'},{x['account'] for x in entry})
            self.assertEqual(sum(x['amount'] for x in entry if x['side']=='Dr'),sum(x['amount'] for x in entry if x['side']=='Cr'))
    def test_uk_expense_policy_positive(self):
        from borrowing_costs_cases import capture_sources
        c=fresh('UK_GAAP');c['accounting_policy']['borrowing_costs']='expense';c=capture_sources(remeasure(c));r=self.local(c)
        self.assertEqual(0,r['calculations']['capitalized']);self.assertEqual([],r['journal_entry_implications']);self.assertEqual(Decimal('58910.00'),r['calculations']['expense'])
    def test_iqa02_annual_ceiling_not_daily(self):
        from borrowing_costs_cases import capture_sources
        c=fresh('US_GAAP','general');p=c['projects'][0];p['opening_expenditure']='1000000';p['expenditures'][0]['amount']='-995000'
        c=capture_sources(remeasure(c));r=self.local(c);self.assertEqual(Decimal('39872.88'),r['calculations']['capitalized'])
    def test_valid_extended_suspension_and_resumption(self):
        from borrowing_costs_cases import capture_sources
        c=fresh('IFRS','specific');p=c['projects'][0];t=p['timeline'][0]
        p['timeline']=[dict(t,id='jan',end='2026-01-31'),dict(t,id='pause',start='2026-02-01',end='2026-02-28',state='suspended',extended=True,substantial_technical_activity=False),dict(t,id='resume',start='2026-03-01')]
        p['timeline_inventory']=[x['id'] for x in p['timeline']];c=capture_sources(remeasure(c));r=self.local(c)
        self.assertEqual((Decimal('20550')*337/365).quantize(Decimal('.01')),r['calculations']['capitalized'])
    def test_valid_cessation_at_readiness(self):
        from borrowing_costs_cases import capture_sources
        c=fresh('AASB','specific');p=c['projects'][0];p['ready_date']='2026-09-01';t=p['timeline'][0]
        p['timeline']=[dict(t,id='active',end='2026-08-31'),dict(t,id='complete',start='2026-09-01',state='complete')];p['timeline_inventory']=['active','complete']
        c=capture_sources(remeasure(c));r=self.local(c);self.assertEqual((Decimal('20550')*243/365).quantize(Decimal('.01')),r['calculations']['capitalized'])
    def test_valid_necessary_delay_continues(self):
        from borrowing_costs_cases import capture_sources
        c=fresh('IFRS','specific');c['projects'][0]['timeline'][0].update(state='temporary',necessary_delay=True,substantial_technical_activity=False)
        c=capture_sources(remeasure(c));self.assertEqual(Decimal('20550'),self.local(c)['calculations']['capitalized'])
    def test_missing_original_snapshot(self):
        c=fresh();c.pop('original_source_snapshot');self.blocked(c)
    def test_iqa01_asset_gl_shift(self):
        c=fresh()
        for k in ('opening','closing','statement'):c['gl'][0][k]=str(Decimal(c['gl'][0][k])+37)
        self.blocked(c)
    def test_iqa01_finance_gl_shift(self):
        c=fresh()
        for k in ('opening','closing','statement'):c['gl'][1][k]=str(Decimal(c['gl'][1][k])+37)
        self.blocked(c)
    def test_source_expenditure_recomputed_contradiction(self):
        c=fresh();c['projects'][0]['expenditures'][0]['amount']='138000';self.blocked(remeasure(c))
    def test_source_financing_recomputed_contradiction(self):
        c=fresh();c['borrowings'][0]['segments'][0]['annual_rate']='.07';c['borrowings'][0]['segments'][0]['effective_annual_rate']='.07';self.blocked(remeasure(c))
    def test_source_policy_contradiction(self):
        c=fresh('UK_GAAP');c['accounting_policy']['borrowing_costs']='expense';self.blocked(remeasure(c))
    def test_source_timeline_contradiction(self):
        c=fresh();c['projects'][0]['timeline'][0]['state']='temporary';self.blocked(c)
    def test_duplicate_debt_economic_identity(self):
        c=fresh();b=copy.deepcopy(c['borrowings'][0]);b['id']='different-id';c['borrowings'].append(b);c['borrowing_inventory'].append(b['id']);self.blocked(c)
    def test_duplicate_expenditure_economics(self):
        c=fresh();p=c['projects'][0];x=copy.deepcopy(p['expenditures'][0]);x['id']='different-id';p['expenditures'].append(x);p['expenditure_inventory'].append(x['id']);self.blocked(c)
    def test_missing_financing_population(self):
        c=fresh();c['borrowings'].pop();c['borrowing_inventory'].pop();self.blocked(c)
    def test_missing_expenditure_population(self):
        c=fresh();c['projects'][0]['expenditures']=[];c['projects'][0]['expenditure_inventory']=[];self.blocked(c)
    def test_missing_timeline_population(self):
        c=fresh();c['projects'][0]['timeline']=[];c['projects'][0]['timeline_inventory']=[];self.blocked(c)
    def test_period_routes(self):
        c=fresh();c['reporting_period']='2027-12-31';self.blocked(c)
    def test_edition_routes(self):
        for fw in ('IFRS','AASB','US_GAAP','UK_GAAP'):
            c=fresh(fw);c['accounting_policy']['effective_standard']='superseded';self.blocked(c)
    def test_aasb_tier2_excluded(self):
        c=fresh('AASB');c['reporting_tier']=2;self.blocked(c)
    def test_nonuk_expense_election_excluded(self):
        for fw in ('IFRS','AASB','US_GAAP'):
            c=fresh(fw);c['accounting_policy']['borrowing_costs']='expense';self.blocked(c)
    def test_foreign_currency_excluded(self):
        c=fresh();c['borrowings'][0]['currency']='USD';self.blocked(c)
    def test_fee_eir_fx_tax_exempt_excluded(self):
        for k,v in [('fees','10'),('fx_adjustment','10'),('tax_exempt',True),('complex_features',True)]:
            c=fresh();c['borrowings'][0][k]=v;self.blocked(c)
    def test_multiple_projects_and_components_excluded(self):
        c=fresh();c['projects'][0]['shared_components']=True;self.blocked(c)
        c=fresh();c['projects'].append(copy.deepcopy(c['projects'][0]));self.blocked(c)
    def test_nonconstruction_abandoned_nonqualifying_excluded(self):
        for k,v in [('asset_type','software'),('abandoned',True),('qualifying_asset',False),('substantial_period',False)]:
            c=fresh();c['projects'][0][k]=v;self.blocked(c)
    def test_backdated_cash_excluded(self):
        c=fresh();c['projects'][0]['expenditures'][0]['cash_date']='2026-08-01';self.blocked(c)
    def test_suspension_requires_extended_ceased_activity(self):
        c=fresh();c['projects'][0]['timeline'][0].update(state='suspended',extended=False,substantial_technical_activity=False);self.blocked(c)
    def test_cessation_conflict(self):
        c=fresh();c['projects'][0]['ready_date']='2026-09-01';self.blocked(c)
    def test_imported_debt_economics_without_crosswalk_excluded(self):
        c=fresh();c['imports']=[dict(package='debt-financing',case={},result={},mode='evidence_only')];self.blocked(c)
    def test_sale_inventory_owner_excluded(self):
        from borrowing_costs_cases import capture_sources
        c=fresh();c['projects'][0]['purpose']='sale';self.blocked(capture_sources(c))
    def test_freshly_captured_adverse_routes(self):
        from borrowing_costs_cases import capture_sources
        for fw,group,key,value in [('IFRS','project','abandoned',True),('IFRS','project','asset_type','software'),('IFRS','project','shared_components',True),('IFRS','loan','fees','10'),('IFRS','loan','fx_adjustment','10'),('IFRS','loan','complex_features',True),('IFRS','loan','tax_exempt',True),('IFRS','loan','currency','USD'),('AASB','case','reporting_tier',2),('IFRS','policy','borrowing_costs','expense'),('IFRS','project','opening_capitalized','10')]:
            c=fresh(fw);r=c if group=='case' else c['projects'][0] if group=='project' else c['borrowings'][0] if group=='loan' else c['accounting_policy'];r[key]=value;self.blocked(capture_sources(c))
    def test_malformed_money(self):
        for value in ('NaN','Infinity',True,1.2,None,{},[]):
            c=fresh();c['projects'][0]['opening_expenditure']=value;self.blocked(c)
    def test_production_fresh_release(self):
        for fw in ('IFRS','AASB','US_GAAP','UK_GAAP'):
            r=assess_case('borrowing-costs',ready(c=fresh(fw)));self.assertEqual('complete',r['status'],r['conclusion'])
    def test_production_stale_certification(self):
        c=ready(c=fresh());c['reviewer_signoff']['case_fingerprint']='stale';r=assess_case('borrowing-costs',c);self.assertEqual('partial',r['status']);self.assertEqual([],r['journal_entry_implications'])
    def test_production_recapture_not_implicit_in_recertification(self):
        c=fresh();c['projects'][0]['expenditures'][0]['amount']='138000';c=ready(c=remeasure(c));self.assertEqual('blocked',assess_case('borrowing-costs',c)['status'])
    def test_stale_knowledge_document(self):
        c=ready(c=fresh());c['knowledge_review']['documents'][0]['sha256']='0'*64;self.assertEqual('blocked',assess_case('borrowing-costs',c)['status'])
    def test_stale_selected_claims(self):
        c=ready(c=fresh());c['knowledge_review']['applied_claim_ids']=[];self.assertEqual('blocked',assess_case('borrowing-costs',c)['status'])
    def test_changed_implementation_certification(self):
        c=ready(c=fresh())
        with patch('production.case_fingerprint',return_value='changed-independent-executable'):
            r=assess_case('borrowing-costs',c);self.assertEqual('partial',r['status']);self.assertEqual([],r['journal_entry_implications'])
    def test_blocked_missing_source_public_no_private_metadata(self):
        c=fresh();c.pop('original_source_snapshot');r=assess_case('borrowing-costs',ready(c=c));self.assertEqual('blocked',r['status'])
        for route in ROUTES:
            s=json.dumps(to_public(r,route),default=serializable)
            for secret in ('original_source_snapshot','synthetic independent reviewer','case_fingerprint','sha256','Source:'):self.assertNotIn(secret,s)
    def test_public_private_provenance_all_routes(self):
        r=assess_case('borrowing-costs',ready(c=fresh()));self.assertEqual('complete',r['status'])
        r['facts_used']['reviewer']='PRIVATE_REVIEW_927';r['evidence'][0]['source_note']='Source: ChatGPT training data';r['evidence'][-1]['source_note']='Source: FRC FRS 102'
        for route in ROUTES:
            s=json.dumps(to_public(r,route),default=serializable)
            for secret in ('PRIVATE_REVIEW_927','Source:','source_note','sha256','case_fingerprint','evidence_status','audit_required'):self.assertNotIn(secret,s)

if __name__=='__main__':unittest.main()
