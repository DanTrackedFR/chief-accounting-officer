"""Success and hostile alternative routes, independently specified numerical expectations."""
import copy,unittest
from decimal import Decimal
import test_reporting_workflows as workflows
from reporting_cases import reporting,approved,handoffs

class ReportingRouteTests(unittest.TestCase):
    run_case=workflows.ReportingTests.run_case
    block=workflows.ReportingTests.block
    def flow(self,c,id,kind,n,category):
        c['transactions'].append(approved(id,date='2026-12-31',amount=str(n),kind=kind,category=category,cash=True,source_id=id,bank_id=id,classification_memo='Independently approved underlying nature',specifically_identified=kind=='income_taxes'))
        c['controls']['population_count']+=1;c['controls']['population_amount']=str(Decimal(c['controls']['population_amount'])+abs(Decimal(n)))
        s=c['statement'];s[category]=str(Decimal(s[category])+Decimal(n));s['closing']=str(Decimal(s['closing'])+Decimal(n));s['balance_sheet_closing']=s['closing'];c['cash_accounts'][0]['closing']=s['closing'];c['cash_accounts'][0]['gl_closing']=s['closing']
        if category=='operating':
            c['indirect']['adjustments'].append(approved(id,amount=str(n),basis_memo='Independent subtotal-to-cash adjustment',noncash_acquisition_fx_excluded=True));c['indirect']['adjustment_inventory'].append(id)
    def test_cash_interest_dividend_tax_lease_four_frameworks(self):
        for f in ['IFRS','US_GAAP','UK_GAAP','AASB']:
            c=reporting('cash-flow-reporting',f)
            for id,kind,n,cat in [('interest','interest_paid',-4,'operating'),('yield','interest_received',3,'operating'),('divreceived','dividends_received',2,'operating'),('divpaid','dividends_paid',-5,'financing'),('tax','income_taxes',-6,'operating'),('lease','lease_principal',-7,'financing'),('rental','lease_operating',-8,'operating')]:self.flow(c,id,kind,n,cat)
            r=self.run_case('cash-flow-reporting',c);self.assertEqual(r['calculations']['closing'],Decimal('265'))
    def test_cash_tax_refund_and_trace_to_investing(self):
        c=reporting('cash-flow-reporting');self.flow(c,'tax_refund','income_taxes',6,'investing');self.run_case('cash-flow-reporting',c)
        c=reporting('cash-flow-reporting','US_GAAP');self.flow(c,'tax_refund','income_taxes',6,'investing');self.run_case('cash-flow-reporting',c,'blocked')
    def test_cash_acquisition_net_inflow_and_disposal(self):
        c=reporting('cash-flow-reporting');self.flow(c,'acquire','business_acquisition',5,'investing');self.flow(c,'dispose','business_disposal',10,'investing');c['handoffs'].update(handoffs(c,{'business_acquisition':'Consolidation','business_disposal':'Consolidation'}));c['handoffs']['business_acquisition']['amount']='5';c['handoffs']['business_disposal']['amount']='10';self.run_case('cash-flow-reporting',c)
    def test_cash_noncash_omission_and_future_date(self):
        self.block('cash-flow-reporting',lambda c:c.update(noncash=[]))
        self.block('cash-flow-reporting',lambda c:c['noncash'][0].update(date='2027-01-01'))
        self.block('cash-flow-reporting',lambda c:c.update(noncash_source_total='21'))
    def test_cash_use_only_restriction_cannot_exclude_demand_cash(self):
        for f in ['IFRS','UK_GAAP','AASB']:
            c=reporting('cash-flow-reporting',f);c['cash_accounts'].append(approved('restricted',opening='100',closing='100',gl_opening='100',gl_closing='100',type='restricted',cf_included=False,balance_sheet_cash=True,fx='0',withdrawable_demand=True,definition_memo='Qualifying demand deposit',restriction_evidence='Use restriction only, withdrawable',bank_gl_evidence='Supported bank GL tie'));c['cash_inventory'].append('restricted');c['statement'].update(balance_sheet_opening='200',balance_sheet_closing='390');self.run_case('cash-flow-reporting',c,'blocked')
    def test_cash_ifrs18_lease_rent_operating_and_interest_financing(self):
        c=reporting('cash-flow-reporting');c['cash_policy'].update(early_adoption=True,interest_paid='financing',interest_received='investing',dividends_received='investing');c['indirect']['starting_subtotal']='operating_profit';self.flow(c,'interest','lease_interest',-4,'financing');self.flow(c,'rent','lease_operating',-8,'operating');self.run_case('cash-flow-reporting',c)
    def test_equity_treasury_reissue_loss_equity_only(self):
        c=reporting('equity-capital');c['events']+=[approved('buy',kind='treasury_buy',date='2026-04-01',amount='30',shares='3',cost_method_memo='Reviewed cost method',equity_classified=True,accounting_memo='Supported purchase',legal_evidence='Approved'),approved('reissue',kind='treasury_reissue',date='2026-05-01',amount='25',shares='3',carrying_cost='30',cost_method_memo='Reviewed cost method',loss_allocation=[{'id':'loss','component':'premium','amount':'5'}],equity_classified=True,accounting_memo='Supported reissue',legal_evidence='Approved')];c['components'][1].update(closing='167',gl_closing='167');c['statement']['closing_equity']='327';c['controls'].update(population_count=4,population_amount='265');self.run_case('equity-capital',c)
    def test_equity_capital_reduction_internal_and_cash(self):
        for cash in [False,True]:
            c=reporting('equity-capital');c['events'].append(approved('reduce',kind='capital_reduction',date='2026-12-31',amount='10',equity_classified=True,accounting_memo='Reviewed reduction',legal_evidence='Reviewed qualified legal opinion',from_component='share_capital',to_component='retained_earnings',cash_settlement=cash,shares_cancelled='10',court_or_legal_approval='Authorized supported legal capital action'));c['components'][0].update(closing='110',gl_closing='110');c['share_register']['closing_issued']='110'
            if cash:c['statement']['closing_equity']='322'
            else:c['components'][2].update(closing='50',gl_closing='50')
            c['controls'].update(population_count=3,population_amount='220');self.run_case('equity-capital',c)
    def test_equity_imported_reclass_offsets_and_exact_once(self):
        c=reporting('equity-capital');c['events'].append(approved('reclass',kind='retrospective_adjustment',component='oci',date='2026-12-31',amount='10',signed_amount='10',source_entries=[[{'side':'Dr','account':'retained_earnings','amount':'10'},{'side':'Cr','account':'oci','amount':'10'}]],source_journal_ids=['prior_reclass'],handoff_key='change',equity_classified=True,accounting_memo='Reviewed reclassification',legal_evidence='Approved'));c['handoffs'].update(handoffs(c,{'change':'Accounting Changes'}));c['handoffs']['change']['amount']='10';c['components'][2].update(closing='30',gl_closing='30');c['components'][4].update(closing='10',gl_closing='10');c['controls'].update(population_count=3,population_amount='220');self.run_case('equity-capital',c)
        c['components'][2].update(closing='40',gl_closing='40');c['statement']['closing_equity']='342';self.run_case('equity-capital',c,'blocked')
    def test_equity_profit_oci_sbc_group_imports(self):
        for kind,component,target,n in [('profit','retained_earnings','Financial Statements','10'),('oci','oci','Financial Statements','5'),('sbc','premium','Share-Based Compensation','6'),('group_change','premium','Consolidation','7')]:
            c=reporting('equity-capital');source=[] if kind in ['profit','oci'] else [[{'side':'Dr','account':'expense' if kind=='sbc' else 'investment','amount':n},{'side':'Cr','account':component,'amount':n}]];c['events'].append(approved('import',kind=kind,component=component,date='2026-12-31',amount=n,signed_amount=n,source_entries=source,source_journal_ids=['source'] if source else [],handoff_key='import',equity_classified=True,accounting_memo='Reviewed source',legal_evidence='Approved'));c['handoffs'].update(handoffs(c,{'import':target}));c['handoffs']['import']['amount']=n
            r=next(r for r in c['components'] if r['id']==component);r['closing']=str(Decimal(r['closing'])+Decimal(n));r['gl_closing']=r['closing'];c['statement']['closing_equity']=str(332+Decimal(n));c['controls'].update(population_count=3,population_amount=str(210+Decimal(n)));self.run_case('equity-capital',c)
    def test_changes_modified_transition_opening(self):
        c=reporting('accounting-changes');c['change'].update(kind='policy',mandatory=True,specific_transition=True,transition_route='modified_retrospective');c['affected_periods'][0].update(period_start='2026-01-01',period_end='2026-01-01',opening_equity_effect=True,lines=[{'id':'cash','balance':'100','category':'asset'},{'id':'retained_earnings','balance':'-100','category':'equity'},{'id':'payable','balance':'0','category':'liability'}],expected_corrected={'cash':'100','retained_earnings':'-80','payable':'-20'},eps_applicable=False);c['adjustments'][0].update(layer='transition_opening',lines=[{'side':'Dr','account':'retained_earnings','amount':'20'},{'side':'Cr','account':'payable','amount':'20'}]);c['handoffs'].update(handoffs(c,{'transition':'Transaction standard transition'}));r=self.run_case('accounting-changes',c);self.assertEqual(r['calculations']['opening_equity_change'],Decimal('-20'))
    def test_changes_impracticability_supported_ifrs_boundary(self):
        c=reporting('accounting-changes');c['change'].update(impracticable=True,impracticability_memo='Exhaustive source reconstruction unavailable, independent technical review',earliest_practicable='2025-01-01');c['handoffs'].update(handoffs(c,{'practicability':'Technical accounting practicability'}));self.run_case('accounting-changes',c);c['change']['earliest_practicable']='2026-01-01';self.run_case('accounting-changes',c,'blocked')
    def test_changes_material_error_cannot_be_uncorrected(self):
        c=reporting('accounting-changes');c['adjustments']=[];p=c['affected_periods'][0];p['expected_corrected']={l['id']:l['balance'] for l in p['lines']};p['corrected_eps']='10';c['opening_equity_bridge']['corrected']='100';c['controls'].update(population_count=0,population_amount='0');self.run_case('accounting-changes',c,'blocked')
    def debt_case(self):
        c=reporting('going-concern');c['debt']=[approved('loan',agreement='Supported loan agreement',classification_memo='Debt maturity January31',covenant_memo='Only January test in forecast window',maturity='2027-01-31',principal='100',breach=False,waiver_effective='not_applicable',payable_on_demand=False,coverage_by_scenario={'base':['ratio'],'downside':['ratio']})];c['debt_inventory']=['loan'];c['controls']['population_amount']='4760'
        for s in c['scenarios']:
            for i,r in enumerate(s['periods']):
                r['expected_before']=str(900 if s['id']=='base' else 880-i*20);r['expected_after']=r['expected_before'];r['intra_period_min_before']=r['expected_before'];r['intra_period_min_after']=r['expected_after']
            s['expected_min_before']=s['expected_min_after']='900' if s['id']=='base' else '660';s['periods'][0]['debt_payments']=[{'id':'payment','debt_id':'loan','amount':'100','date':'2027-01-31'}];s['periods'][0]['covenants']=[{'id':'ratio','debt_id':'loan','numerator':'100','denominator':'50','limit':'2','comparison':'minimum','compliant':True,'waiver_memo':'No waiver required'}]
        return c
    def test_gc_debt_paid_and_covenant_boundary(self):
        c=self.debt_case();self.run_case('going-concern',c);c['scenarios'][0]['periods'][0]['covenants'][0]['denominator']='0';self.run_case('going-concern',c,'blocked')
    def test_gc_debt_payment_late_or_duplicate_principal(self):
        c=self.debt_case();c['debt'][0]['maturity']='2027-01-15';self.run_case('going-concern',c,'blocked')
        c=self.debt_case();c['scenarios'][0]['periods'][0]['debt_payments'][0]['amount']='101';self.run_case('going-concern',c,'blocked')
    def test_gc_demand_overdue_liquidity_method_boundary(self):
        for demand,maturity in [(True,'2027-01-31'),(True,'2026-12-31'),(False,'2026-12-30')]:
            c=self.debt_case();c['debt'][0].update(payable_on_demand=demand,maturity=maturity);r=self.run_case('going-concern',c,'blocked');self.assertIn('immediate-call/default',r['conclusion'])
    def test_gc_committed_plan_and_missing_covenant(self):
        c=self.debt_case();c['plans']=[approved('facility',amount='50',available_date='2027-01-20',committed=True,within_control=True,probable_implementation=True,probable_mitigation=True,management_intent='Actual documented board intent',feasibility_memo='Independent implementation and mitigation review',commitment_evidence='Signed binding available facility')]
        for s in c['scenarios']:
            s['periods'][0]['plan_draws']=[{'id':'draw','plan_id':'facility','amount':'50','date':'2027-01-25'}]
            for r in s['periods']:r['expected_after']=str(Decimal(r['expected_after'])+50);r['intra_period_min_after']=r['expected_after']
            s['expected_min_after']=str(Decimal(s['expected_min_after'])+50)
        self.run_case('going-concern',c);c['scenarios'][0]['periods'][0]['covenants']=[];self.run_case('going-concern',c,'blocked')
    def test_commitment_realized_gain_supported_external_journal(self):
        c=reporting('commitments-contingencies');r=c['register'][0];r.update(kind='gain_contingency',route='realized_gain',charge='10',closing_recognized='10',gl_closing='10',recognized_account='receivable',measurement_handoff='gain',source_journals=[approved('gainjournal',source_case_id='realized-gain-case',account='receivable',lines=[{'side':'Dr','account':'receivable','amount':'10'},{'side':'Cr','account':'gain','amount':'10'}])]);c['handoffs'].update(handoffs(c,{'gain':'Provisions & Contingencies'}));c['handoffs']['gain']['amount']='10';c['gl_recognized']='10';c['disclosure'][0]['recognized_amount']='10';self.run_case('commitments-contingencies',c)
    def test_commitment_no_gl_offset_hiding_between_registered_accounts(self):
        c=reporting('commitments-contingencies');r=c['register'][0];r.update(kind='litigation',route='provision',charge='10',closing_recognized='10',gl_closing='10',recognized_account='provision',measurement_handoff='provision',source_journals=[approved('journal',source_case_id='provision-case',account='provision',lines=[{'side':'Dr','account':'other_provision','amount':'10'},{'side':'Cr','account':'provision','amount':'10'}])]);other=copy.deepcopy(r);other.update(id='other',opening_recognized='20',charge='0',closing_recognized='20',gl_closing='20',recognized_account='other_provision',measurement_handoff='other',source_journals=[]);c['register'].append(other);c['contract_inventory'].append('other');d=copy.deepcopy(c['disclosure'][0]);d.update(id='other',recognized_amount='20');c['disclosure'].append(d);c['disclosure'][0]['recognized_amount']='10';c['gl_recognized']='30';c['controls'].update(population_count=2,population_amount='300');c['handoffs'].update(handoffs(c,{'provision':'Provisions & Contingencies','other':'Provisions & Contingencies'}));c['handoffs']['provision']['amount']='10';c['handoffs']['other']['amount']='20';self.run_case('commitments-contingencies',c,'blocked')
    def test_related_pricing_and_supported_exemption(self):
        c=reporting('related-parties');c['relationships'][0].update(arm_length_asserted=True,pricing_evidence='Reviewed comparable-market pricing study',arm_length_approved=True);self.run_case('related-parties',c);c['transactions'][0].update(exemption=True,exemption_memo='Qualified applicable disclosure exemption');c['handoffs'].update(handoffs(c,{'exemption':'Related-party disclosure specialist'}));c['disclosure'][0].update(included=False,amount='0');c['statement_totals']['sales']='0';self.run_case('related-parties',c)
    def test_related_commitment_population_separate_from_payable(self):
        c=reporting('related-parties');x=copy.deepcopy(c['balances'][0]);x.update(id='commitment',amount='50',gl_amount='50',type='guarantee');c['commitments'].append(x);c['disclosure'].append(approved('commitment',included=True,amount='50',requirement_memo='Maximum related guarantee exposure, not payable'));c['statement_totals']['commitments']='50';c['controls'].update(population_count=3,population_amount='170');r=self.run_case('related-parties',c);self.assertEqual(r['calculations']['receivables'],Decimal('20'));self.assertEqual(r['calculations']['commitments'],Decimal('50'))

if __name__=='__main__':unittest.main()
