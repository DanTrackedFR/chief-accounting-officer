"""Independent agent QA; synthetic approvals are not authenticated people.
Scaffolding comes from shared case shape. All amounts/expected GL below are
independently set without the authored oracle or production-derived expectations.
"""
import importlib.util
import json
import unittest
from copy import deepcopy
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from grant_cases import case, capture, ready
from core_accounting import ReviewRequired
from production import assess_case, to_public

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('_independent_grant_workflow',ROOT/'skills/government-grants/workflow.py')
workflow=importlib.util.module_from_spec(spec);spec.loader.exec_module(workflow)
CLAIMS=[dict(topic_id='SUPPLEMENTAL_GOVERNMENT_GRANTS')]
D=Decimal


def independent_case(fw='IFRS',route='income'):
    c=case(fw,route);c['case_id']='Independent grant 137.03 and 913 cost '+fw+' '+route
    g=c['grants'][0];asset=g['classification']=='asset'
    g.update(agreement_amount='137.03',recognized_addition='137.03',total_eligible_expense_basis='913')
    c['controls']['population_amount']='137.03'
    g['eligible_costs'][0].update(amount='913',owner_gl_amount='913',current_expense='91.3' if asset else '271.11')
    g['asset'].update(cost='913',total_expense_basis='913',current_expense='91.3')
    if g['payments']:g['payments'][0]['amount']='137.03'
    g['valuation']['fair_value']='137.03'
    release=D('137.03') if route in ('performance','past') else D('0') if route in ('deduction','cost_accumulation','advance','repayment') else (D('137.03')*D('91.3' if asset else '271.11')/D('913')).quantize(D('.01'),rounding=ROUND_HALF_UP)
    opening=D('30') if route=='repayment' else D('0');repay=D('70') if route=='repayment' else D('0');expense=max(D(0),repay-opening)
    addition=D('137.03') if route not in ('repayment','advance') else D(0)
    basis=addition if route in ('deduction','cost_accumulation') else D(0)
    closing=opening+addition-release-min(opening,repay) if not basis else D(0)
    adv=D('137.03') if route=='advance' else D(0)
    g['expected']=dict(closing_deferred=str(closing),closing_receivable='0',grant_income=str(release),repayment_expense=str(expense),basis_adjustment=str(basis),closing_advance=str(adv))
    g['disclosure'].update(g['expected'])
    if closing:
        g['release_schedule'][0].update(amount=str(closing),expense_basis=str(D('913')-D('91.3' if asset else '271.11')))
    cash=D('137.03') if g['payments'] else D(0)
    for row in c['gl']:
        account=row['id'];op=D(0);cl=D(0)
        if account=='Deferred grant':op=-opening;cl=-closing
        if account=='Grant cash':cl=cash
        if account=='Grant income':cl=-release
        if account=='Grant repayment expense':cl=expense
        if account=='Grant repayment payable':cl=-repay
        if account=='Grant advance':cl=-adv
        if account=='Grant asset contra-basis':cl=-basis
        if account=='Nonmonetary grant clearing' and route=='nonmonetary':op=-addition
        row.update(opening=str(op),closing=str(cl),statement=str(cl))
    return capture(c)


def gl(c,account,**changes):
    next(r for r in c['gl'] if r['id']==account).update({k:str(v) for k,v in changes.items()})


class IndependentGovernmentGrants(unittest.TestCase):
    def local(self,c):return workflow.assess(c,CLAIMS)
    def blocked(self,c):
        with self.assertRaises(ReviewRequired):self.local(c)
    def test_independent_income_amounts_four_frameworks(self):
        for fw in ('IFRS','AASB','UK_GAAP','US_GAAP'):
            r=self.local(independent_case(fw));self.assertEqual(D('40.69'),r['calculations']['grants'][0]['current_income'])
            self.assertEqual(D('96.34'),r['calculations']['grants'][0]['closing_deferred'])
    def test_independent_asset_amount_and_balance(self):
        r=self.local(independent_case(route='asset'));self.assertEqual(D('13.70'),r['calculations']['grants'][0]['current_income'])
        for entry in r['journal_entry_implications']:
            self.assertEqual(sum(x['amount'] for x in entry if x['side']=='Dr'),sum(x['amount'] for x in entry if x['side']=='Cr'))
    def test_uk_performance_distinct_from_accrual(self):
        self.assertEqual(D('137.03'),self.local(independent_case('UK_GAAP','performance'))['calculations']['grants'][0]['current_income'])
        self.assertEqual(D('40.69'),self.local(independent_case('UK_GAAP'))['calculations']['grants'][0]['current_income'])
    def test_independent_basis_has_no_grant_income(self):
        for fw,route in [('IFRS','deduction'),('AASB','deduction'),('US_GAAP','cost_accumulation')]:
            s=self.local(independent_case(fw,route))['calculations']['grants'][0];self.assertEqual(D('137.03'),s['basis_adjustment']);self.assertEqual(0,s['current_income'])
    def test_independent_repayment_consumes_deferral_first(self):
        s=self.local(independent_case(route='repayment'))['calculations']['grants'][0];self.assertEqual(D('40'),s['repayment_expense']);self.assertEqual(0,s['closing_deferred'])
    def test_independent_nonmonetary_clearing(self):
        r=self.local(independent_case(route='nonmonetary'));self.assertEqual('Nonmonetary grant clearing',r['journal_entry_implications'][0][0]['account'])
    def test_advance_has_no_income(self):
        s=self.local(independent_case(route='advance'))['calculations']['grants'][0];self.assertEqual(0,s['current_income']);self.assertEqual(D('137.03'),s['closing_advance'])
    def test_advance_cannot_receive_previously_paid_award_again(self):
        c=independent_case(route='advance');g=c['grants'][0];g['opening_history'].update(recognized_total='137.03',cash_total='137.03',income_total='137.03');capture(c);self.blocked(c)
    def test_source_changed_without_new_original_capture(self):
        c=independent_case();c['grants'][0]['agreement_amount']='138';self.blocked(c)
    def test_gl_parallel_stock_shift_is_not_reconciliation(self):
        c=independent_case();r=next(r for r in c['gl'] if r['id']=='Grant receivable');r.update(opening='500',closing='500',statement='500');capture(c);self.blocked(c)
    def test_parallel_shift_all_grant_owned_stocks_and_pnl_blocks(self):
        routes=[('income','Grant income'),('repayment','Grant repayment expense'),('repayment','Grant repayment payable'),('deduction','Grant asset contra-basis'),('nonmonetary','Nonmonetary grant clearing')]
        for route,account in routes:
            c=independent_case(route=route);r=next(r for r in c['gl'] if r['id']==account)
            for key in ('opening','closing','statement'):r[key]=str(D(r[key])+D('17.37'))
            capture(c)
            with self.assertRaisesRegex(ReviewRequired,'stock/GL'):self.local(c)
    def test_already_posted_grant_component_cannot_execute_again(self):
        c=independent_case();c['journal_ownership'][0]['already_posted']=True;capture(c)
        with self.assertRaisesRegex(ReviewRequired,'already posted'):self.local(c)
    def test_income_pattern_not_supported_by_cost_population(self):
        c=independent_case();g=c['grants'][0];g['total_eligible_expense_basis']='271.11';g['expected'].update(closing_deferred='0',grant_income='137.03');g['release_schedule']=[];g['schedule_inventory']=[];gl(c,'Deferred grant',closing=0,statement=0);gl(c,'Grant income',closing='-137.03',statement='-137.03');capture(c);self.blocked(c)
    def test_opening_receivable_cannot_exceed_total_award(self):
        c=independent_case();g=c['grants'][0];g['opening_receivable']='999';g['expected']['closing_receivable']='999';gl(c,'Grant receivable',opening=999,closing=999,statement=999);capture(c);self.blocked(c)
    def test_us_nonmonetary_cost_accumulation_has_no_qualified_owner_adapter(self):
        for measurement in ('cost_to_entity','fair_value'):
            c=independent_case('US_GAAP','cost_accumulation');g=c['grants'][0];g.update(transfer='nonmonetary',measurement=measurement,payments=[],payment_inventory=[]);g['valuation']['cost_to_entity']='137.03';c['accounting_policy']['nonmonetary_measurement']=measurement
            gl(c,'Grant cash',opening=0,closing=0,statement=0);gl(c,'Nonmonetary grant clearing',opening='-137.03',closing=0,statement=0);capture(c)
            r=assess_case('government-grants',ready(c=c));self.assertNotEqual('complete',r['status']);self.assertEqual([],r['journal_entry_implications']);self.assertIn('qualified original asset-owner adapter',str(r['open_items']))
    def test_us_nonmonetary_fv_deferred_positive_production(self):
        c=ready(c=independent_case('US_GAAP','nonmonetary'));r=assess_case('government-grants',c);self.assertEqual('complete',r['status']);s=r['calculations']['grants'][0];self.assertEqual(D('13.70'),s['current_income']);self.assertEqual(D('123.33'),s['closing_deferred']);self.assertEqual(0,s['basis_adjustment'])
    def test_us_nonmonetary_intangible_excluded(self):
        c=independent_case('US_GAAP','nonmonetary');g=c['grants'][0];g['asset']['accounting_owner']='intangible-assets';g['eligible_costs'][0]['accounting_owner']='intangible-assets';capture(c);self.blocked(c)
    def test_opening_unpaid_prior_grant_plus_addition_exceeds_entitlement(self):
        c=independent_case();g=c['grants'][0];g['opening_receivable']='100';g['opening_history'].update(recognized_total='100',cash_total='0',income_total='100');g['expected']['closing_receivable']='100';g['disclosure']['closing_receivable']='100';gl(c,'Grant receivable',opening=100,closing=100,statement=100);capture(c);self.blocked(c)
    def test_positive_followon_release_without_new_recognition(self):
        c=independent_case();g=c['grants'][0];g.update(opening_deferred='82.22',recognized_addition='0',payments=[],payment_inventory=[])
        g['opening_history'].update(recognized_total='137.03',cash_total='137.03',income_total='54.81')
        g['expected'].update(closing_deferred='41.53',grant_income='40.69');g['disclosure'].update(g['expected']);g['release_schedule'][0].update(amount='41.53',expense_basis='276.69')
        gl(c,'Deferred grant',opening='-82.22',closing='-41.53',statement='-41.53');gl(c,'Grant cash',opening=0,closing=0,statement=0);capture(c)
        s=self.local(c)['calculations']['grants'][0];self.assertEqual(D('40.69'),s['current_income']);self.assertEqual(D('41.53'),s['closing_deferred']);self.assertEqual(0,s['recognized_additions'])
    def test_prior_deferral_in_basis_route_excluded(self):
        c=independent_case(route='deduction');g=c['grants'][0];g['opening_deferred']='1';capture(c);self.blocked(c)
    def test_missing_quantitative_disclosure(self):
        c=independent_case();c['grants'][0]['disclosure']['grant_income']='0';capture(c);self.blocked(c)
    def test_missing_compliance_evidence_blocks_even_with_cash(self):
        c=independent_case();c['grants'][0]['conditions'][0]['compliance_evidenced']=False;capture(c);self.blocked(c)
    def test_due_failed_conditions_override_positive_assurance(self):
        for fw in ('IFRS','AASB','US_GAAP','UK_GAAP'):
            for due in ('2026-06-30','2026-12-31'):
                c=independent_case(fw);r=c['grants'][0]['conditions'][0];r.update(met=False,due_date=due);capture(c)
                with self.assertRaisesRegex(ReviewRequired,'Due grant condition failed'):self.local(c)
    def test_future_compliance_reasonable_assurance_not_automatically_failed(self):
        for fw in ('IFRS','AASB','US_GAAP','UK_GAAP'):
            c=independent_case(fw);r=c['grants'][0]['conditions'][0];r.update(met=False,due_date='2027-01-01');capture(c)
            self.assertEqual(D('40.69'),self.local(c)['calculations']['grants'][0]['current_income'])
    def test_stale_condition_cutoff_blocks_all_supported_events(self):
        for route in ('income','advance','repayment'):
            c=independent_case(route=route);c['grants'][0]['conditions'][0]['as_of']='2026-12-30';capture(c)
            with self.assertRaisesRegex(ReviewRequired,'not current'):self.local(c)
    def test_due_failed_condition_cash_is_unrecognized_advance(self):
        c=independent_case(route='advance');c['grants'][0]['conditions'][0].update(met=False,due_date='2026-12-31');capture(c)
        s=self.local(c)['calculations']['grants'][0];self.assertEqual(0,s['current_income']);self.assertEqual(D('137.03'),s['closing_advance'])
    def test_failed_current_condition_repays_without_grant_income(self):
        c=independent_case(route='repayment');c['grants'][0]['conditions'][0].update(met=False,due_date='2026-12-31');capture(c)
        s=self.local(c)['calculations']['grants'][0];self.assertEqual(0,s['current_income']);self.assertEqual(D('40'),s['repayment_expense'])
    def test_missing_due_date_no_production_journals(self):
        c=independent_case();c['grants'][0]['conditions'][0].pop('due_date');capture(c);r=assess_case('government-grants',ready(c=c));self.assertNotEqual('complete',r['status']);self.assertEqual([],r['journal_entry_implications'])
    def test_uk_unmet_performance_blocks(self):
        c=independent_case('UK_GAAP','performance');c['grants'][0]['conditions'][0]['met']=False;capture(c);self.blocked(c)
    def test_wrong_recognition_threshold(self):
        c=independent_case('US_GAAP');c['grants'][0]['recognition_review']['threshold']='reasonable_assurance';capture(c);self.blocked(c)
    def test_us_missing_early_adoption(self):
        c=independent_case('US_GAAP');c.pop('us_adoption');self.blocked(c)
    def test_aasb_tier_two_excluded(self):
        c=independent_case('AASB');c['reporting_tier']=2;self.blocked(c)
    def test_uk_asset_netting_excluded(self):self.blocked(independent_case('UK_GAAP','deduction'))
    def test_wrong_period_edition(self):
        c=independent_case();c['accounting_policy']['effective_standard']='IAS20_2025';self.blocked(c)
    def test_scope_exclusions(self):
        for substance in ('procurement','shareholder','income_tax','loan','assistance','agriculture_fvlcts'):
            c=independent_case();c['grants'][0]['substance']=substance;capture(c);self.blocked(c)
    def test_duplicate_bank_receipt(self):
        c=independent_case();g=c['grants'][0];g['payments'].append(dict(g['payments'][0],id='receipt-alias'));g['payment_inventory'].append('receipt-alias');capture(c);self.blocked(c)
    def test_wrong_owner(self):
        c=independent_case();c['journal_ownership'][0]['accounting_owner']='revenue-recognition';capture(c);self.blocked(c)
    def test_duplicate_agreement_cannot_alias_distinct_economic_records(self):
        c=independent_case();g=deepcopy(c['grants'][0]);g['id']='alias-award';g['economic_id']='alias-economic'
        def distinct(v):
            if isinstance(v,dict):
                for key,value in list(v.items()):
                    if key=='grant_id':v[key]='alias-award'
                    elif key in ('bank_id','asset_id','economic_id') and key!='grant_id':v[key]=str(value)+'-alias'
                    else:distinct(value)
            elif isinstance(v,list):
                for value in v:distinct(value)
        distinct(g);g['economic_id']='alias-economic';c['grants'].append(g);c['source_inventory'].append(g['id']);c['controls'].update(population_count=2,population_amount='274.06')
        o=deepcopy(c['journal_ownership'][0]);o.update(id='alias-ownership',economic_id=g['economic_id']);c['journal_ownership'].append(o);c['ownership_inventory'].append(o['id'])
        for r in c['gl']:
            for key in ('opening','closing','statement'):r[key]=str(D(r[key])*2)
        capture(c)
        with self.assertRaisesRegex(ReviewRequired,'agreement'):self.local(c)
    def test_duplicate_grant_economic_owner(self):
        c=independent_case();r=deepcopy(c['journal_ownership'][0]);r['id']='alias';c['journal_ownership'].append(r);c['ownership_inventory'].append('alias');capture(c);self.blocked(c)
    def test_entity_period_currency_source_mismatch(self):
        for key,value in [('source_entity','OtherCo'),('source_period',['2025-01-01','2025-12-31']),('currency','USD'),('source_framework','US_GAAP')]:
            c=independent_case();c['grants'][0]['eligible_costs'][0][key]=value;capture(c);self.blocked(c)
    def test_nonmonetary_valuation_must_match_recognition_date(self):
        for fw in ('IFRS','AASB','UK_GAAP','US_GAAP'):
            for date in ('2026-06-29','2026-07-01'):
                c=independent_case(fw,'nonmonetary');c['grants'][0]['valuation']['valuation_date']=date;capture(c);r=assess_case('government-grants',ready(c=c));self.assertNotEqual('complete',r['status']);self.assertEqual([],r['journal_entry_implications']);self.assertIn('date',str(r['open_items']).lower())
            c=ready(c=independent_case(fw,'nonmonetary'));r=assess_case('government-grants',c);self.assertEqual('complete',r['status']);self.assertEqual(D('13.70'),r['calculations']['grants'][0]['current_income'])
    def test_missing_valuation(self):
        c=independent_case(route='nonmonetary');c['grants'][0]['valuation']['qualified']=False;capture(c);self.blocked(c)
    def test_complex_repayment_blocks(self):
        c=independent_case(route='repayment');c['grants'][0]['repayment']['error_vs_estimate']='prior_error';capture(c);self.blocked(c)
    def test_us_unincurred_cost_at_recognition_blocks(self):
        c=independent_case('US_GAAP');c['grants'][0]['eligible_costs'][0]['incurred_date']='2026-07-01';capture(c)
        with self.assertRaisesRegex(ReviewRequired,'incurred'):self.local(c)
    def test_asset_expense_before_available_for_use_blocks(self):
        c=independent_case(route='asset');c['grants'][0]['asset']['available_for_use_date']='2027-01-01';capture(c);self.blocked(c)
    def test_asset_zero_life_blocks(self):
        c=independent_case(route='asset');c['grants'][0]['asset']['useful_life_years']='0';capture(c);self.blocked(c)
    def test_asset_residual_basis_contradiction_blocks(self):
        c=independent_case(route='asset');c['grants'][0]['asset']['residual_value']='100';capture(c);self.blocked(c)
    def test_nonus_inventory_cannot_alias_long_term_asset(self):
        for fw in ('IFRS','AASB','UK_GAAP'):
            c=independent_case(fw,'asset');g=c['grants'][0];g['asset'].update(accounting_owner='inventory-cost',expense_model='inventory_expense');g['eligible_costs'][0]['accounting_owner']='inventory-cost';capture(c)
            with self.assertRaisesRegex(ReviewRequired,'long-term asset'):self.local(c)
    def test_future_schedule_original_expense_basis_required(self):
        c=independent_case();c['grants'][0]['release_schedule'][0]['expense_basis']='0';capture(c)
        with self.assertRaisesRegex(ReviewRequired,'Future eligible expense'):self.local(c)
    def test_future_schedule_first_row_cannot_accelerate_release(self):
        c=independent_case();g=c['grants'][0];r=deepcopy(g['release_schedule'][0]);r.update(id='future-second',date='2028-12-31',amount='46.34',expense_basis='320.945');g['release_schedule'][0].update(amount='50',expense_basis='320.945');g['release_schedule'].append(r);g['schedule_inventory'].append(r['id']);capture(c)
        with self.assertRaisesRegex(ReviewRequired,'Future owner expense'):self.local(c)
    def test_repayment_retaining_deferral_requires_revised_pattern(self):
        c=independent_case(route='repayment');g=c['grants'][0];g['repayment']['amount']='10';g['expected'].update(closing_deferred='20',repayment_expense='0');g['disclosure'].update(g['expected'])
        g['release_schedule']=[dict(g['conditions'][0],id='remaining-pattern',date='2027-12-31',amount='20',expense_basis='133.255',schedule_memo='Original owner pattern requires revision')];g['schedule_inventory']=['remaining-pattern'];gl(c,'Deferred grant',opening='-30',closing='-20',statement='-20');gl(c,'Grant repayment expense',closing=0,statement=0);gl(c,'Grant repayment payable',closing=-10,statement=-10);capture(c)
        with self.assertRaisesRegex(ReviewRequired,'revised owner expense pattern'):self.local(c)
    def test_changed_asset_blocks(self):
        c=independent_case(route='asset');c['grants'][0]['asset']['disposed']=True;capture(c);self.blocked(c)
    def test_production_exact_once_journals_and_determinism(self):
        c=ready(c=independent_case());r=assess_case('government-grants',c);self.assertEqual('complete',r['status']);self.assertEqual(r,assess_case('government-grants',deepcopy(c)))
        delta={}
        for entry in r['journal_entry_implications']:
            for line in entry:delta[line['account']]=delta.get(line['account'],D(0))+line['amount']*(1 if line['side']=='Dr' else -1)
        self.assertEqual({'Grant receivable':D(0),'Deferred grant':D('-96.34'),'Grant income':D('-40.69'),'Grant cash':D('137.03')},delta)
    def test_independent_native_complete_and_missing_compliance_blocks(self):
        from orchestration import CAO
        c=ready(c=independent_case());request=dict(objective='How should we account for this government grant?',scope=dict(entity=c['entity'],framework=c['framework'],jurisdiction=c['jurisdiction'],period_start=c['period_start'],reporting_period=c['reporting_period'],currency='EUR'),facts={'grant':c})
        r=CAO().run(request);self.assertEqual('complete',r.outcome,r.open_questions);self.assertEqual(['government-grants'],r.skills_invoked);n=r.graph.nodes['government-grants'];self.assertEqual('complete',n.status);self.assertEqual(D('40.69'),n.result['calculations']['grants'][0]['current_income'])
        bad=independent_case();bad['grants'][0]['conditions'][0]['compliance_evidenced']=False;capture(bad);request['facts']['grant']=ready(c=bad)
        r=CAO().run(request);self.assertNotEqual('complete',r.outcome);self.assertEqual('blocked',r.graph.nodes['government-grants'].status);self.assertEqual([],r.graph.nodes['government-grants'].result['journal_entry_implications'])
    def test_incomplete_certification_no_production_journals(self):
        c=ready(c=independent_case());c['reviewer_signoff']['approved']=False;r=assess_case('government-grants',c);self.assertNotEqual('complete',r['status']);self.assertEqual([],r['journal_entry_implications'])
    def test_stale_certification_no_production_journals(self):
        c=ready(c=independent_case());c['grants'][0]['grantor']='Changed grantor';r=assess_case('government-grants',c);self.assertNotEqual('complete',r['status']);self.assertEqual([],r['journal_entry_implications'])
    def test_public_private_source_boundary(self):
        c=ready(c=independent_case());r=assess_case('government-grants',c);self.assertEqual('complete',r['status']);public=json.dumps(to_public(r),default=str)
        for secret in ('MODEL_DERIVED_AUDIT_REQUIRED','original_source_snapshot','capture_memo','standards-claims.json','reviewer_signoff'):
            self.assertNotIn(secret,public)

if __name__=='__main__':unittest.main()
