import copy,json,subprocess,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from production import assess_case,to_public,case_fingerprint,serializable,PACKAGES as REGISTRY,canonical_knowledge
from reporting_cases import PACKAGES,reporting,certified,approved,handoffs,pol
from decimal import Decimal

FW=['IFRS','US_GAAP','UK_GAAP','AASB']
ROOT=Path(__file__).resolve().parents[2]

class ReportingTests(unittest.TestCase):
    def run_case(self,p,c,status='complete'):
        r=assess_case(p,certified(p,case=c) if c['framework'] in FW else c);self.assertEqual(r['status'],status,r['conclusion']);return r
    def block(self,p,fn,fw='IFRS'):
        c=reporting(p,fw);fn(c);return self.run_case(p,c,'blocked')
    def test_all_four_frameworks_complete_balanced_and_private(self):
        for p in PACKAGES:
            for f in FW:
                with self.subTest(p=p,f=f):
                    r=self.run_case(p,reporting(p,f));pub=json.dumps(to_public(r),default=serializable)
                    for forbidden in ['synthetic independent reviewer','case_fingerprint','sha256','MODEL_DERIVED','audit_required','Synthetic independent complete source register']:
                        self.assertNotIn(forbidden,pub)
                    for j in r['journal_entry_implications']:
                        self.assertEqual(sum(Decimal(l['amount']) for l in j if l['side']=='Dr'),sum(Decimal(l['amount']) for l in j if l['side']=='Cr'))
    def test_missing_reviewer_is_partial_all_frameworks(self):
        for p in PACKAGES:
            for f in FW:self.assertEqual(assess_case(p,{k:v for k,v in certified(p,f).items() if k!='reviewer_signoff'})['status'],'partial')
    def test_stale_certification_every_package(self):
        for p in PACKAGES:
            c=certified(p);c['judgment_memo']+=' changed';self.assertEqual(assess_case(p,c)['status'],'partial')
    def test_independent_reviewer_every_package(self):
        for p in PACKAGES:
            c=certified(p);c['reviewer_signoff']['reviewer']=c['preparer'];self.assertEqual(assess_case(p,c)['status'],'partial')
    def test_knowledge_change_every_package(self):
        for p in PACKAGES:
            c=certified(p);c['knowledge_review']['documents'][0]['sha256']='stale';self.assertEqual(assess_case(p,c)['status'],'blocked')
    def test_implementation_change_invalidates_certification(self):
        c=certified('cash-flow-reporting');original=case_fingerprint(c)
        from unittest.mock import patch
        with patch('production.hashlib.sha256') as h:
            h.return_value.hexdigest.return_value='different';self.assertNotEqual(original,case_fingerprint(c))
    def test_missing_evidence_completeness_stale_approval_all_packages(self):
        for p in PACKAGES:
            for f in FW:
                self.block(p,lambda c:c.update(evidence=[]),f)
                self.block(p,lambda c:c['controls'].update(complete=False),f)
                self.block(p,lambda c:c['disclosure_review'].update(approved_version='stale'),f)
                self.block(p,lambda c:c['controls'].update(population_count=999),f)
    def test_malformed_context_policy_entity_and_framework(self):
        for p in PACKAGES:
            for key,value in [('entity_type','not_for_profit'),('period_start','bad'),('reporting_period','2025-01-01'),('framework','invented')]:
                self.block(p,lambda c,k=key,v=value:c.update({k:v}))
    def test_handoff_dimension_mismatch_and_unresolved(self):
        for p in PACKAGES:
            for key,value in [('resolved',False),('entity','Other'),('framework','US_GAAP'),('reporting_period','2025-12-31')]:
                self.block(p,lambda c,k=key,v=value:next(iter(c['handoffs'].values())).update({k:v}))
    def test_no_internal_source_notes_in_all_public_routes(self):
        from interfaces.public_output import ROUTES as PUBLIC_ROUTES
        for p in PACKAGES:
            c=reporting(p);c['judgment_memo']='INTERNAL SECRET MEMO';c['evidence']=['INTERNAL SECRET SOURCE'];r=self.run_case(p,c)
            for route in PUBLIC_ROUTES:
                text=json.dumps(to_public(r,route),default=serializable);self.assertNotIn('INTERNAL SECRET',text);self.assertNotIn('reviewer_signoff',text)
    def test_provisional_references_are_qualified(self):
        r=self.run_case('cash-flow-reporting',reporting('cash-flow-reporting'));s=json.dumps(to_public(r),default=serializable).lower();self.assertIn('unverified',s)
    def test_cash_numeric_bridge_and_working_capital(self):
        c=reporting('cash-flow-reporting');c['indirect']['start_amount']='220';c['indirect']['net_profit']='220';c['handoffs']['profit']['amount']='220';c['indirect']['working_capital']=[approved('ar',opening='100',closing='135',acquisition='10',fx='5',noncash='0',side='asset',source_bridge='35 change less acquisition10 FX5 =20 operating')]
        r=self.run_case('cash-flow-reporting',c);self.assertEqual(r['calculations']['indirect_operating'],Decimal('240'))
    def test_cash_wrong_indirect_and_sign(self):
        self.block('cash-flow-reporting',lambda c:c['indirect']['adjustments'][0].update(amount='120'))
        self.block('cash-flow-reporting',lambda c:c['transactions'][0].update(amount='-400'))
    def test_cash_noncash_doublecount(self):
        self.block('cash-flow-reporting',lambda c:c['noncash'][0].update(source_id='customers'))
    def test_cash_transfer_pair_and_unpaired_block(self):
        c=reporting('cash-flow-reporting')
        for id,n in [('in','30'),('out','-30')]:c['transactions'].append(approved(id,date='2026-12-31',amount=n,kind='internal_transfer',category='excluded',cash=True,source_id=id,bank_id=id,classification_memo='Both included accounts'))
        c['controls'].update(population_count=6,population_amount='760');self.run_case('cash-flow-reporting',c)
        c['transactions'].pop();c['controls'].update(population_count=5,population_amount='730');self.run_case('cash-flow-reporting',c,'blocked')
    def test_cash_equivalent_original_maturity_boundary(self):
        c=reporting('cash-flow-reporting');a=c['cash_accounts'][0];a.update(type='equivalent',acquisition_date='2026-09-30',maturity_date='2026-12-30',cash_management=True,known_amount=True,insignificant_risk=True);self.run_case('cash-flow-reporting',c);a['maturity_date']='2026-12-31';self.run_case('cash-flow-reporting',c,'blocked')
    def test_cash_restricted_framework_difference(self):
        for f in FW:
            c=reporting('cash-flow-reporting',f);c['cash_accounts'][0].update(type='restricted',withdrawable_demand=f!='US_GAAP');self.run_case('cash-flow-reporting',c)
        self.block('cash-flow-reporting',lambda c:c['cash_accounts'][0].update(type='restricted',withdrawable_demand=False))
    def test_cash_us_overdraft_excluded_and_ifrs_requires_integral(self):
        self.block('cash-flow-reporting',lambda c:c['cash_accounts'][0].update(type='overdraft',integral_cash_management=True),'US_GAAP')
        self.block('cash-flow-reporting',lambda c:c['cash_accounts'][0].update(type='overdraft',integral_cash_management=False))
    def test_cash_ifrs18_and_early_adoption(self):
        for f in ['IFRS','AASB']:
            c=reporting('cash-flow-reporting',f);c['cash_policy'].update(early_adoption=True,interest_paid='financing',interest_received='investing',dividends_received='investing');c['indirect']['starting_subtotal']='operating_profit';self.run_case('cash-flow-reporting',c);c['indirect']['starting_subtotal']='net_profit';self.run_case('cash-flow-reporting',c,'blocked')
        self.block('cash-flow-reporting',lambda c:c['cash_policy'].update(early_adoption=True),'US_GAAP')
    def test_cash_2027_nonadoption_blocks(self):
        c=reporting('cash-flow-reporting');c['period_start']='2027-01-01';c['reporting_period']='2027-12-31';c['execution_date']='2028-01-01';c['applicability_review']['effective_period']=[c['period_start'],c['reporting_period']];c['controls']['as_of']=c['reporting_period'];c['cash_policy']['effective_period']=[c['period_start'],c['reporting_period']];self.run_case('cash-flow-reporting',c,'blocked')
    def test_cash_us_interest_policy_wrong(self):self.block('cash-flow-reporting',lambda c:c['cash_policy'].update(interest_paid='financing'),'US_GAAP')
    def test_cash_bank_duplicate_and_fx_tie(self):
        self.block('cash-flow-reporting',lambda c:c['transactions'][1].update(bank_id='customers'))
        self.block('cash-flow-reporting',lambda c:c['handoffs']['fx'].update(amount='10'))
    def test_equity_ordinary_cost_and_dividend_math(self):
        r=self.run_case('equity-capital',reporting('equity-capital'));self.assertEqual(r['calculations']['closing'],Decimal('332'));self.assertEqual(r['calculations']['components']['premium'],Decimal('172'))
    def test_equity_opening_own_and_positive_treasury_block(self):
        self.block('equity-capital',lambda c:c['share_register'].update(opening_own='101'))
        self.block('equity-capital',lambda c:c['components'][3].update(opening='1'))
    def test_equity_costs_exceed_premium_and_compound_block(self):
        self.block('equity-capital',lambda c:c['events'][0].update(incremental_cost='181'))
        self.block('equity-capital',lambda c:c['events'][0].update(ordinary=False))
    def test_equity_treasury_buy_and_reissue_gain(self):
        c=reporting('equity-capital');c['events']+= [approved('buy',kind='treasury_buy',date='2026-04-01',amount='30',shares='3',cost_method_memo='Reviewed cost method',equity_classified=True,accounting_memo='Approved own-share purchase',legal_evidence='Supported legal rights'),approved('reissue',kind='treasury_reissue',date='2026-05-01',amount='35',shares='3',carrying_cost='30',cost_method_memo='Reviewed carrying cost',loss_allocation=[],equity_classified=True,accounting_memo='Approved reissue',legal_evidence='Supported legal rights')];c['components'][1].update(closing='177',gl_closing='177');c['statement']['closing_equity']='337';c['controls'].update(population_count=4,population_amount='275');self.run_case('equity-capital',c)
    def test_equity_dividend_payment_cannot_exceed_payable(self):
        c=reporting('equity-capital');c['events'].append(approved('pay',kind='dividend_paid',date='2026-12-31',amount='11',equity_classified=True,accounting_memo='Payment',legal_evidence='Support'));self.run_case('equity-capital',c,'blocked')
    def test_equity_nci_profit_separate_component(self):
        c=reporting('equity-capital');c['components'].append(approved('nci_profit',opening='10',closing='14',gl_closing='14',classification_memo='Supported NCI attribution',equity_owner='nci',role='profit'));c['component_inventory'].append('nci_profit');c['events'].append(approved('nci',kind='profit',component='nci_profit',date='2026-12-31',amount='4',signed_amount='4',source_entries=[],handoff_key='nci',equity_classified=True,accounting_memo='Consolidated profit attribution',legal_evidence='Group ownership'));c['handoffs'].update(handoffs(c,{'nci':'Financial Statements'}));c['handoffs']['nci']['amount']='4';c['statement'].update(opening_equity='160',closing_equity='346');c['controls'].update(population_count=3,population_amount='214');self.run_case('equity-capital',c)
    def test_changes_prior_error_profit_eps_opening(self):
        r=self.run_case('accounting-changes',reporting('accounting-changes'));self.assertEqual(r['calculations']['opening_equity_change'],Decimal('-20'));self.assertEqual(r['calculations']['periods'][0]['basic_eps'],Decimal('8'))
    def test_changes_multiperiod_carryforward_not_doublecounted(self):
        c=reporting('accounting-changes');p=copy.deepcopy(c['affected_periods'][0]);p['id']='earlier';p['period_start']='2024-01-01';p['period_end']='2024-12-31';c['affected_periods'].append(p);c['period_inventory'].append('earlier');a=copy.deepcopy(c['adjustments'][0]);a.update(id='earlier',period_id='earlier');c['adjustments'].append(a);c['controls'].update(population_count=2,population_amount='40');r=self.run_case('accounting-changes',c);self.assertEqual(r['calculations']['opening_equity_change'],Decimal('-20'))
    def test_changes_estimate_prospective_and_old_info_rejected(self):
        c=reporting('accounting-changes');c['change'].update(kind='estimate',original_information_available=False,new_information=True,information_date='2026-04-01');p=c['affected_periods'][0];p.update(period_start='2026-01-01',period_end='2026-12-31');c['adjustments'][0]['layer']='current_profit';c['opening_equity_bridge']['corrected']='100';self.run_case('accounting-changes',c);c['change']['original_information_available']=True;self.run_case('accounting-changes',c,'blocked')
    def test_changes_us_hybrid_only(self):
        c=reporting('accounting-changes','US_GAAP');c['change']['kind']='estimate_effected_by_principle';c['affected_periods'][0].update(period_start='2026-01-01',period_end='2026-12-31');c['adjustments'][0]['layer']='current_profit';c['opening_equity_bridge']['corrected']='100';self.run_case('accounting-changes',c)
        self.block('accounting-changes',lambda c:c['change'].update(kind='estimate_effected_by_principle'))
    def test_changes_policy_mandatory_transition_requires_handoff(self):
        c=reporting('accounting-changes');c['change'].update(kind='policy',mandatory=True,specific_transition=True);c['handoffs'].update(handoffs(c,{'transition':'Transaction standard transition'}));self.run_case('accounting-changes',c);c['change']['specific_transition']=False;self.run_case('accounting-changes',c,'blocked')
    def test_changes_us_error_no_impracticability(self):self.block('accounting-changes',lambda c:c['change'].update(impracticable=True),'US_GAAP')
    def test_changes_wrong_period_and_unbalanced(self):
        self.block('accounting-changes',lambda c:c['affected_periods'][0].update(period_end='2030-01-01'))
        self.block('accounting-changes',lambda c:c['adjustments'][0]['lines'][0].update(amount='21'))
        self.block('accounting-changes',lambda c:c.update(error_register=[]))
    def test_changes_sec_big_r_and_little_r(self):
        for prior,expected in [(True,'Big_R_reissuance'),(False,'little_r_revision')]:
            c=reporting('accounting-changes','US_GAAP');c['sec']=approved('sec',registrant=True,auditor_notice=False,filer_type='domestic',counsel_memo='Reviewed accounting and filing consequences',auditor_memo='Reviewed error',authorized_governance_memo='Board authorized analysis',nonreliance_date='2027-01-16',filing_plan='Counsel owns filing timeline and form',icfr_clawback_review='Independent review');c['materiality']['prior_material']=prior;c['handoffs'].update(handoffs(c,{'sec':'SEC securities counsel'}));r=self.run_case('accounting-changes',c);self.assertEqual(r['calculations']['sec_route'],expected);self.assertEqual(r['calculations']['item_402_review'],prior)
    def test_changes_sec_claims_not_nonregistrant(self):
        c=certified('accounting-changes','US_GAAP');claims,_=canonical_knowledge(REGISTRY['accounting-changes'][1],'US_GAAP');c['knowledge_review']['applied_claim_ids']+=[x['claim_id'] for x in claims if '-SEC-' in x['claim_id']];c['reviewer_signoff']['case_fingerprint']=case_fingerprint(c);self.assertEqual(assess_case('accounting-changes',c)['status'],'blocked')
    def test_gc_framework_horizons_and_cash_math(self):
        for f in FW:
            c=reporting('going-concern',f);r=self.run_case('going-concern',c);self.assertEqual(r['calculations']['scenarios'][1]['minimum_after'],Decimal('700' if f in ['US_GAAP','UK_GAAP'] else '760'))
            c['assessment']['horizon_end']='2027-01-01';self.run_case('going-concern',c,'blocked')
    def test_gc_missing_month_and_fabricated_forecast(self):
        self.block('going-concern',lambda c:c['scenarios'][0]['periods'].pop(1))
        self.block('going-concern',lambda c:c['scenarios'][0]['periods'][0].update(expected_after='999'))
    def test_gc_opening_reserve_minimum(self):
        c=reporting('going-concern');c['scenarios'][0]['minimum_reserve']='1100';c['scenarios'][0].update(expected_min_before='-100',expected_min_after='-100');c['management_review']['material_uncertainty']=True;r=self.run_case('going-concern',c);self.assertEqual(r['calculations']['scenarios'][0]['minimum_before'],Decimal('-100'))
    def test_gc_intra_period_minimum_and_uncertainty(self):
        c=reporting('going-concern');c['scenarios'][0]['periods'][0].update(intra_period_min_before='-5',intra_period_min_after='-5');c['scenarios'][0].update(expected_min_before='-5',expected_min_after='-5');self.run_case('going-concern',c,'blocked');c['management_review']['material_uncertainty']=True;self.run_case('going-concern',c)
    def test_gc_debt_maturity_missing_payment_and_covenant_inventory(self):
        c=reporting('going-concern');c['debt']=[approved('loan',agreement='Signed loan',classification_memo='Due within horizon',covenant_memo='Contract tests complete',maturity='2027-01-31',principal='100',breach=False,waiver_effective='not_applicable',payable_on_demand=False,coverage_by_scenario={'base':[],'downside':[]})];c['debt_inventory']=['loan'];self.run_case('going-concern',c,'blocked')
        c['debt'][0].update(maturity='2029-01-31',coverage_by_scenario={'base':['cv'],'downside':[]});self.run_case('going-concern',c,'blocked')
    def test_gc_plan_uncommitted_and_overdrawn(self):
        c=reporting('going-concern');c['plans']=[approved('fund',available_date='2027-01-31',amount='50',committed=False,within_control=True,probable_implementation=True,probable_mitigation=True,management_intent='Actual supported board plan',feasibility_memo='Support',commitment_evidence='No binding agreement')];c['scenarios'][0]['periods'][0]['plan_draws']=[{'id':'draw','plan_id':'fund','amount':'50'}];self.run_case('going-concern',c,'blocked')
        c['plans'][0]['committed']=True;c['scenarios'][0]['periods'][0]['plan_draws'][0]['amount']='51';self.run_case('going-concern',c,'blocked')
    def test_gc_sensitivity_and_cash_availability(self):
        self.block('going-concern',lambda c:c['sensitivities'][0].update(expected_reduction='20'))
        self.block('going-concern',lambda c:c['assessment'].update(unavailable_cash='10'))
    def test_commitment_register_recognition_distinct(self):
        r=self.run_case('commitments-contingencies',reporting('commitments-contingencies'));self.assertEqual(r['calculations']['maximum_contractual_exposure'],Decimal('120'));self.assertEqual(r['calculations']['recognized_balances'],0)
    def test_commitment_guarantee_requires_external_measurement(self):
        c=reporting('commitments-contingencies');c['register'][0].update(kind='guarantee',route='disclosure_only',measurement_handoff='valuation');self.run_case('commitments-contingencies',c,'blocked');c['handoffs'].update(handoffs(c,{'valuation':'Guarantee accounting and valuation'}));c['handoffs']['valuation']['amount']='0';self.run_case('commitments-contingencies',c)
    def test_commitment_provision_import_balanced_journal_all_frameworks(self):
        for f in FW:
            c=reporting('commitments-contingencies',f);n='40' if f=='US_GAAP' else '45';r=c['register'][0];r.update(kind='litigation',route='provision',recognized_account='provision',charge=n,closing_recognized=n,gl_closing=n,measurement_handoff='measure',source_journals=[approved('journal',source_case_id='provision-case',account='provision',lines=[{'side':'Dr','account':'expense','amount':n},{'side':'Cr','account':'provision','amount':n}])]);c['disclosure'][0]['recognized_amount']=n;c['gl_recognized']=n;c['handoffs'].update(handoffs(c,{'measure':'Provisions & Contingencies'}));c['handoffs']['measure']['amount']=n;self.run_case('commitments-contingencies',c)
    def test_commitment_kind_route_bypass_and_excess_fulfillment(self):
        self.block('commitments-contingencies',lambda c:c['register'][0].update(route='financial_guarantee'))
        self.block('commitments-contingencies',lambda c:c['register'][0].update(fulfilled='200'))
    def test_commitment_gain_unrecognized_and_illegal_probability(self):
        c=reporting('commitments-contingencies');c['register'][0].update(kind='gain_contingency',route='gain_unrecognized');self.run_case('commitments-contingencies',c);c['register'][0]['law_probability_supported']=False;self.run_case('commitments-contingencies',c,'blocked')
    def test_related_timeline_and_consolidation(self):
        c=reporting('related-parties');c['relationships'][0]['start']='2026-12-15';c['disclosure'][0].update(included=False,amount='0');c['statement_totals']['sales']='0';self.run_case('related-parties',c)
        c=reporting('related-parties');c['reporting_scope']['level']='consolidated'
        for r in c['transactions']+c['balances']:r['eliminated']=True
        for n in c['disclosure']:n.update(included=False,amount='0')
        c['statement_totals'].update(sales='0',receivables='0');self.run_case('related-parties',c)
    def test_related_false_declaration_and_arm_length(self):
        self.block('related-parties',lambda c:c['declarations'][0].update(related=False,relationship_ids=[]))
        self.block('related-parties',lambda c:c['relationships'][0].update(arm_length_asserted=True))
    def test_related_kmp_categories_inventory_and_gl(self):
        c=reporting('related-parties');c['relationships'][0]['kind']='kmp';c['reporting_scope']['kmp_scope']=True;c['kmp_compensation']=[approved('pay',relationship_id='relation',category='short_term',amount='10',gl_amount='10',included=True,payroll_evidence='Reviewed payroll',period_allocation_memo='Service during KMP relationship')];c['kmp_inventory']=['pay'];c['kmp_categories_review']['totals']['short_term']='10';c['statement_totals']['kmp']='10';self.run_case('related-parties',c)
        for key,value in [('category','invented'),('included',False),('gl_amount','11')]:
            d=copy.deepcopy(c);d['kmp_compensation'][0][key]=value;self.run_case('related-parties',d,'blocked')
        c['kmp_inventory']=[];self.run_case('related-parties',c,'blocked')
    def test_related_uk_2026_disclosure_and_separate_elimination(self):
        self.block('related-parties',lambda c:c['reporting_scope'].update(uk_2026_disclosure_review=False),'UK_GAAP')
        self.block('related-parties',lambda c:c['transactions'][0].update(eliminated=True))
    def test_cross_skill_actual_statement_result(self):
        from additional_cases import reporting as financial,certify
        c=reporting('cash-flow-reporting');result=assess_case('financial-statements',certify('financial-statements',financial()));self.assertEqual(result['status'],'complete');c['handoffs']['statements']['result']=result;self.run_case('cash-flow-reporting',c);result['status']='partial';self.run_case('cash-flow-reporting',c,'blocked')
    def test_cross_skill_actual_provision_and_fx_results(self):
        from cases import provision
        from additional_cases import fx,certify
        for p,key,target,source in [('commitments-contingencies','provisions','provisions-contingencies',provision()),('cash-flow-reporting','fx','foreign-currency',certify('foreign-currency',fx()))]:
            r=assess_case(target,source);self.assertEqual(r['status'],'complete');c=reporting(p);c['handoffs'][key]['result']=r;self.run_case(p,c)
    def test_cli_all_six_and_four_frameworks(self):
        for p in PACKAGES:
            for f in FW:
                with tempfile.TemporaryDirectory() as d:
                    path=Path(d)/'case.json';path.write_text(json.dumps(certified(p,f)));run=subprocess.run([sys.executable,str(ROOT/'skills/run_skill.py'),p,str(path)],capture_output=True,text=True,cwd=ROOT);self.assertEqual(run.returncode,0,run.stderr);self.assertIn('Review status: complete',json.loads(run.stdout)['guidance'])
    def test_blocked_tax_preserved(self):self.assertEqual(assess_case('income-taxes',reporting('accounting-changes'))['status'],'blocked')

if __name__=='__main__':unittest.main()
