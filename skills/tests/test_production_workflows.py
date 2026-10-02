import copy,json,sys,unittest
from decimal import Decimal
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from production import execute,assess_case,to_public,case_fingerprint,serializable
from core_accounting import ReviewRequired,dec,balance
from cases import revenue,ecl,provision,consolidation,finalize

class Workflows(unittest.TestCase):
    def test_all_four_frameworks_end_to_end(self):
        for fw in ['IFRS','US_GAAP','UK_GAAP','AASB']:
            for pkg,make in [('revenue-recognition',revenue),('financial-instruments-ecl',ecl),('provisions-contingencies',provision),('consolidation',consolidation)]:
                with self.subTest(fw=fw,pkg=pkg):
                    r=execute(pkg,make(fw));self.assertEqual(r['status'],'complete')
                    for j in r['journal_entry_implications']:self.assertTrue(balance(j))
                    for route in ['answer','answer_context','retrieval_snippet','citation','tool_output','user_log','export']:
                        p=to_public(r,route);text=json.dumps(p,default=serializable)
                        self.assertNotIn('source_note',text);self.assertNotIn('MODEL_DERIVED',text)
                        self.assertNotIn('knowledge_documents',text);self.assertTrue(p['guidance'])
                    json.dumps(r,default=serializable)
    def test_period_revenue_not_cumulative(self):
        r=execute('revenue-recognition',revenue())['calculations']
        self.assertEqual(r['cumulative_revenue'],800);self.assertEqual(r['period_revenue'],500)
        self.assertEqual(r['contract_bridge']['closing'],-100);self.assertEqual(r['receivable'],300)
        self.assertEqual(r['contract_cost_asset'],120)
    def test_revenue_legacy_uk_route(self):
        r=execute('revenue-recognition',revenue('UK_GAAP','2025-01-01'));self.assertIn('Legacy',r['method'])
    def test_uk_period_election_mismatch(self):
        c=revenue('UK_GAAP','2025-01-01');c['policy_elections']['section23_model']='revised_2026'
        with self.assertRaises(ReviewRequired):execute('revenue-recognition',c)
    def test_over_time_payment_right_adversarial(self):
        c=revenue();o=c['obligations'][1];o['simultaneous_receipt']=False;o['no_alternative_use']=True;o['right_to_payment_with_margin']=False
        with self.assertRaises(ReviewRequired):execute('revenue-recognition',c)
    def test_variable_constraint_and_specific_allocation(self):
        c=revenue();c['price_components']['variable']=[{'method':'expected_value','outcomes':[{'amount':'200','probability':'0.8'},{'amount':'0','probability':'0.2'}],
          'constraint_memo':'Supported entitlement only100','included_amount':'100','royalty_exception':False}]
        c['specific_allocation']={'amounts':{'delivery':'600','service':'500'},'objective_memo':'Bonus relates only to service'}
        r=execute('revenue-recognition',c)['calculations'];self.assertEqual(r['transaction_price'],1100);self.assertEqual(r['cumulative_revenue'],850)
    def test_duplicate_promise_and_negative_price(self):
        c=revenue();c['obligations'][1]['id']='delivery'
        with self.assertRaises(ReviewRequired):execute('revenue-recognition',c)
        c=revenue();c['price_components']['fixed']='-1'
        with self.assertRaises(ReviewRequired):execute('revenue-recognition',c)
    def test_catch_up_reversal(self):
        c=revenue();c['balance_bridge']['opening_revenue']='900'
        r=execute('revenue-recognition',c);self.assertEqual(r['calculations']['period_revenue'],-100)
        self.assertEqual(r['journal_entry_implications'][0][0]['account'],'revenue')
    def test_ecl_allowance_rollforward(self):
        r=execute('financial-instruments-ecl',ecl())['calculations']
        self.assertEqual(r['allowance'],Decimal('62.50'));self.assertEqual(r['expense'],Decimal('-22.50'))
        self.assertEqual(r['gross_carrying_amount'],980)
    def test_ecl_stage1_horizon(self):
        c=ecl();c['credit']['sicr']=False
        with self.assertRaises(ReviewRequired):execute('financial-instruments-ecl',c)
        c['credit']['horizon']='12_month_default_events';self.assertEqual(execute('financial-instruments-ecl',c)['method']['stage'],1)
    def test_ecl_us_staging_rejected(self):
        c=ecl('US_GAAP');c['instrument']['stage']=1
        with self.assertRaises(ReviewRequired):execute('financial-instruments-ecl',c)
    def test_ecl_uk_election(self):
        c=ecl('UK_GAAP');c['policy_elections']['financial_instruments']='IFRS9';c['instrument']['impairment_model']='general'
        self.assertEqual(execute('financial-instruments-ecl',c)['method']['stage'],2)
    def test_ecl_survival_and_scope(self):
        c=ecl();terms=c['credit']['scenarios'][0]['terms'];terms[0]['marginal_pd']='0.8';terms.append(copy.deepcopy(terms[0]))
        with self.assertRaises(ReviewRequired):execute('financial-instruments-ecl',c)
        c=ecl();c['instrument']['sppi']=False
        with self.assertRaises(ReviewRequired):execute('financial-instruments-ecl',c)
    def test_provision_movement_not_difference(self):
        r=execute('provisions-contingencies',provision())['calculations'];self.assertEqual(r['provision'],45);self.assertEqual(r['provision_bridge']['estimate_change'],15)
    def test_provision_framework_range_difference(self):
        c=provision('US_GAAP');c['estimate'].update(low='100',high='200',best_estimate=None)
        self.assertEqual(execute('provisions-contingencies',c)['calculations']['provision'],100)
        c=provision();c['estimate'].update(basis='continuous_equal_range',low='100',high='200')
        self.assertEqual(execute('provisions-contingencies',c)['calculations']['provision'],150)
    def test_provision_negative_probability(self):
        c=provision();c['estimate']['outcomes'][0]['probability']='-1';c['estimate']['outcomes'][1]['probability']='2'
        with self.assertRaises(ReviewRequired):execute('provisions-contingencies',c)
    def test_provision_disclosure_route(self):
        c=provision();c['obligation'].update(probability='possible',release_memo='Prior obligation no longer probable')
        r=execute('provisions-contingencies',c);self.assertEqual(r['method']['decision'],'disclose_contingency');self.assertEqual(r['calculations']['provision'],0)
    def test_us_discount_and_constructive_obligation(self):
        c=provision('US_GAAP');c['estimate']['discount_rate']='0.05'
        with self.assertRaises(ReviewRequired):execute('provisions-contingencies',c)
        c=provision('US_GAAP');c['obligation']['basis']='constructive'
        with self.assertRaises(ReviewRequired):execute('provisions-contingencies',c)
    def test_reimbursement_capped_and_separate(self):
        c=provision();c['reimbursement'].update(claimed='100',recognition_threshold_met=True)
        r=execute('provisions-contingencies',c)['calculations'];self.assertEqual(r['reimbursement'],45);self.assertEqual(r['provision'],45)
    def test_consolidation_no_intercompany_valid(self):
        r=execute('consolidation',consolidation())['calculations'];self.assertEqual(sum(r['consolidated_balances'].values()),0)
        self.assertEqual(r['consolidated_balances']['investment'],0);self.assertEqual(r['consolidated_balances']['noncontrolling interest'],-20)
    def test_control_not_ownership(self):
        c=consolidation();c['entities'][1]['control']['substantive_power']=False
        with self.assertRaises(ReviewRequired):execute('consolidation',c)
    def test_vie_primary_beneficiary(self):
        c=consolidation('US_GAAP');ctrl=c['entities'][1]['control'];ctrl.update(model='VIE',power_significant_activities=True,potentially_significant_losses_benefits=True)
        self.assertEqual(execute('consolidation',c)['calculations']['perimeter'],['P','S'])
        ctrl['potentially_significant_losses_benefits']=False
        with self.assertRaises(ReviewRequired):execute('consolidation',c)
    def test_unbalanced_tb_and_cashflow(self):
        c=consolidation();c['entities'][0]['balances']['cash']='301'
        with self.assertRaises(ReviewRequired):execute('consolidation',c)
        c=consolidation();c['cash_flow_bridge']['operating']='1'
        with self.assertRaises(ReviewRequired):execute('consolidation',c)
    def test_nonexistent_intercompany_entities(self):
        c=consolidation();c['intercompany']=[{'seller':'X','buyer':'Y','debit_account':'AP','credit_account':'AR','amount':'10','matched':True,'family':'balances','source_id':'x'}]
        with self.assertRaises(ReviewRequired):execute('consolidation',c)
    def test_review_fingerprint_invalidated(self):
        c=revenue();c['balance_bridge']['cash_received']='100'
        self.assertEqual(execute('revenue-recognition',c)['status'],'partial')
        c['reviewer_signoff']['case_fingerprint']=case_fingerprint(c);self.assertEqual(execute('revenue-recognition',c)['status'],'complete')
    def test_knowledge_and_scope_gate(self):
        c=revenue();c['knowledge_review']['claim_ids']=[]
        with self.assertRaises(ReviewRequired):execute('revenue-recognition',c)
        c=revenue('AASB');c['entity_type']='NFP'
        with self.assertRaises(ReviewRequired):execute('revenue-recognition',c)
    def test_public_contamination_fails_closed(self):
        r=execute('revenue-recognition',revenue());r['conclusion']='Source: private note'
        with self.assertRaises(ValueError):to_public(r)
    def test_afs_credit_not_double_counted(self):
        c=ecl('US_GAAP');c['instrument'].update(impairment_model='AFS',measurement='AFS',intent_to_sell=False,required_to_sell_before_recovery=False)
        c['measurement_schedule'].update(opening_gross='100',writeoffs='0',fair_value='80');c['allowance_bridge'].update(opening='0',writeoffs='0',recoveries='0')
        c['credit']['scenarios']=[{'weight':'1','terms':[{'ead':'100','marginal_pd':'0.1','lgd':'1','discount_factor':'1'}]}]
        r=execute('financial-instruments-ecl',c)['calculations']
        self.assertEqual(r['allowance'],10);self.assertEqual(r['fair_value_adjustment'],-10)
        self.assertEqual(r['gross_carrying_amount']+r['fair_value_adjustment']-r['allowance'],80)
    def test_zero_discount_and_none_model_rejected(self):
        c=ecl();c['credit']['scenarios'][0]['terms'][0]['discount_factor']='0'
        with self.assertRaisesRegex(ReviewRequired,'positive'):execute('financial-instruments-ecl',c)
        c=ecl('US_GAAP');c['instrument']['impairment_model']='none'
        with self.assertRaisesRegex(ReviewRequired,'require CECL'):execute('financial-instruments-ecl',c)
    def test_liability_effective_interest(self):
        c=ecl();c['instrument'].update(kind='debt_liability',impairment_model='none');c['measurement_schedule'].update(eir='0.05',cash_flows='100',writeoffs='0')
        r=execute('financial-instruments-ecl',c);self.assertEqual(r['calculations']['closing'],950)
        self.assertEqual(r['journal_entry_implications'][0][0]['account'],'finance cost')
    def test_equity_fvoci_and_us_rejection(self):
        c=ecl();c['instrument'].update(kind='equity_asset',impairment_model='none',measurement='FVOCI',fvoci_irrevocable_election=True,held_for_trading=False)
        c['measurement_schedule'].update(writeoffs='0',fair_value='1200')
        r=execute('financial-instruments-ecl',c);self.assertEqual(r['calculations']['closing'],1200)
        c=ecl('US_GAAP');c['instrument'].update(kind='equity_asset',impairment_model='none',measurement='FVOCI');c['measurement_schedule']['writeoffs']='0'
        with self.assertRaisesRegex(ReviewRequired,'ASC321'):execute('financial-instruments-ecl',c)
    def test_legacy_uk_cost_recovery_amount(self):
        c=revenue('UK_GAAP','2025-01-01');o=c['obligations'][1];o.update(reliable_completion=False,recoverable_cost_revenue='20')
        r=execute('revenue-recognition',c)['calculations'];self.assertEqual(r['cumulative_revenue'],620)
    def test_discounted_provision_and_unwind(self):
        c=provision();c['estimate'].update(basis='most_likely',selected_amount='121',other_outcomes_memo='Single supported obligation',discount_rate='0.1',years='2')
        c['movements'].update(opening='90',settlements='0',unwind='9')
        r=execute('provisions-contingencies',c)['calculations'];self.assertEqual(r['provision'],100);self.assertEqual(r['provision_bridge']['estimate_change'],1)
    def test_onerous_asset_waterfall_and_us_boundary(self):
        c=provision();c['obligation']['type']='onerous';c['estimate'].update(fulfilment_cost='530',benefits='500',exit_cost='40',asset_impairment_first=True,no_double_count_memo='Post impairment costs reviewed')
        self.assertEqual(execute('provisions-contingencies',c)['calculations']['provision'],30)
        c['estimate']['asset_impairment_first']=False
        with self.assertRaisesRegex(ReviewRequired,'impairment'):execute('provisions-contingencies',c)
        c=provision('US_GAAP');c['obligation']['type']='onerous'
        with self.assertRaisesRegex(ReviewRequired,'US contract-specific'):execute('provisions-contingencies',c)
    def test_group_nci_profit_ties_to_equity(self):
        c=consolidation();c['entities'][1]['balances'].update(cash='110',revenue='-10');c['nci'][0]['adjusted_profit']='10'
        c['statement_mapping']['revenue']='income';c['cash_flow_bridge'].update(operating='10',closing_cash='410');c['equity_bridge'].update(profit='10',closing='410')
        r=execute('consolidation',c)['calculations'];self.assertEqual(r['nci'][0]['closing'],22)
        self.assertEqual(r['consolidated_balances']['noncontrolling interest'],-22)
    def test_group_duplicate_and_parent_type(self):
        c=consolidation();c['investments'].append(copy.deepcopy(c['investments'][0]))
        with self.assertRaisesRegex(ReviewRequired,'Duplicate'):execute('consolidation',c)
        c=consolidation();c['entities'][0]['parent']='false'
        with self.assertRaisesRegex(ReviewRequired,'boolean'):execute('consolidation',c)
    def test_ownership_without_control_loss(self):
        c=consolidation();c['ownership_changes']=[{'control_retained':True,'memo':'Acquire remaining20% for25','cash_paid':'25','nci_carrying_acquired':'20'}]
        c['statement_mapping']['parent equity']='equity'
        c['nci'][0].update(ownership='1',other='-20');c['cash_flow_bridge'].update(financing='-25',closing_cash='375');c['equity_bridge'].update(owner_transactions='-25',closing='375')
        r=execute('consolidation',c)['calculations'];self.assertEqual(r['consolidated_balances']['noncontrolling interest'],0)
        self.assertEqual(r['consolidated_balances']['cash'],375)
    def test_group_equity_failure_is_not_hidden_by_balanced_tb(self):
        c=consolidation();c['equity_bridge']['opening']='401'
        with self.assertRaisesRegex(ReviewRequired,'equity bridge'):execute('consolidation',c)
    def test_case_fingerprint_varprice_stable(self):
        c=revenue();c['price_components']['variable']=[{'method':'expected_value','outcomes':[{'amount':'0','probability':'1'}],'constraint_memo':'No bonus','included_amount':'0','royalty_exception':False}]
        c=finalize('revenue-recognition',c);before=copy.deepcopy(c)
        self.assertEqual(execute('revenue-recognition',c)['status'],'complete');self.assertEqual(c,before)
    def test_qa_cent_allocation_no_negative_residual(self):
        from test_four_core_skills import rev
        r=rev.allocate('0.02',[{'id':str(i),'ssp':'1'} for i in range(4)])
        self.assertEqual(sum(x['allocation'] for x in r),Decimal('0.02'));self.assertTrue(all(x['allocation']>=0 for x in r))
        for n in [3,7,50]:
            r=rev.allocate('0.05',[{'id':str(i),'ssp':'1'} for i in range(n)])
            self.assertEqual(sum(x['allocation'] for x in r),Decimal('0.05'));self.assertTrue(all(x['allocation']>=0 for x in r))
    def test_qa_recurring_fair_value_delta(self):
        c=ecl();c['instrument'].update(business_model='collect_sell',measurement='FVOCI');c['measurement_schedule'].update(opening_gross='100',writeoffs='0',fair_value='90',opening_fair_value_adjustment='-20')
        c['allowance_bridge'].update(opening='0',writeoffs='0',recoveries='0');c['credit']['scenarios']=[{'weight':'1','terms':[{'ead':'100','marginal_pd':'0','lgd':'1','discount_factor':'1'}]}]
        r=execute('financial-instruments-ecl',c);j=r['journal_entry_implications'][-1]
        self.assertEqual(j[0]['account'],'instrument fair value adjustment');self.assertEqual(j[0]['amount'],10)
        self.assertEqual(100-20+j[0]['amount'],90)
    def test_qa_decommission_asset_floor(self):
        c=provision();c['obligation']['type']='decommissioning';c['movements']['settlements']='0';c['restoration_asset']={'carrying_amount':'3','remaining_life':'2','model':'cost','impairment_review_memo':'Reviewed residual carrying amount'}
        r=execute('provisions-contingencies',c);j=r['journal_entry_implications'][0]
        self.assertEqual([x['amount'] for x in j],[5,3,2]);self.assertEqual(j[2]['account'],'restoration remeasurement gain')
    def test_qa_most_likely_bad_probabilities(self):
        c=revenue();c['price_components']['variable']=[{'method':'most_likely','outcomes':[{'amount':'0','probability':'0.8'},{'amount':'100','probability':'0.8'}],'constraint_memo':'Review','included_amount':'0','royalty_exception':False}]
        with self.assertRaisesRegex(ReviewRequired,'total one'):execute('revenue-recognition',c)
    def test_gain_contingency_framework_difference(self):
        c=provision();c['obligation'].update(type='contingent_asset',gain_probability='virtually_certain',gain_memo='Unconditional recovery right');c['estimate']['gain_amount']='100'
        self.assertEqual(execute('provisions-contingencies',c)['calculations']['recognized_asset'],100)
        c=provision('US_GAAP');c['obligation'].update(type='contingent_asset',gain_probability='virtually_certain',gain_memo='Gain not realized',gain_realized=False);c['estimate']['gain_amount']='100'
        self.assertEqual(execute('provisions-contingencies',c)['calculations']['recognized_asset'],0)
    def test_provision_explicit_fx_journal_tie(self):
        c=provision();c['movements'].update(fx='5',event_journals=[[{'side':'Dr','account':'FX loss','amount':'5'},{'side':'Cr','account':'provision','amount':'5'}]])
        r=execute('provisions-contingencies',c)['calculations'];self.assertEqual(r['provision_bridge']['estimate_change'],10)
        c['movements']['fx']='6'
        with self.assertRaisesRegex(ReviewRequired,'do not tie'):execute('provisions-contingencies',c)
    def test_canonical_claim_bytes_are_hashed(self):
        c=revenue();docs=c['knowledge_review']['documents']
        self.assertTrue(any(x['path'].endswith('standards-claims.json') for x in docs))
        c['knowledge_review']['documents'][0]['sha256']='stale'
        with self.assertRaisesRegex(ReviewRequired,'changed'):execute('revenue-recognition',c)
    def test_cli_public_output(self):
        import subprocess,tempfile
        c=revenue()
        with tempfile.NamedTemporaryFile(mode='w',suffix='.json') as f:
            json.dump(c,f);f.flush()
            out=subprocess.check_output([sys.executable,str(Path(__file__).resolve().parents[1]/'run_skill.py'),'revenue-recognition',f.name],text=True)
        public=json.loads(out);self.assertIn('Journals:',public['guidance']);self.assertNotIn('evidence_status',out)
    def test_specialist_blocked_envelope_public(self):
        c=ecl();c['instrument']['impairment_model']='poci'
        r=assess_case('financial-instruments-ecl',c);self.assertEqual(r['status'],'blocked')
        self.assertEqual(r['specialist_routing']['topic_id'],'TOPIC-06-007');self.assertEqual(r['journal_entry_implications'],[])
        self.assertIn('Specialist handoff:',to_public(r)['guidance'])
    def test_unexplained_zero_movement_journals_rejected(self):
        c=provision();c['movements']['event_journals']=[[{'side':'Dr','account':'FX expense','amount':'10'},{'side':'Cr','account':'provision','amount':'10'}]]
        with self.assertRaisesRegex(ReviewRequired,'do not tie'):execute('provisions-contingencies',c)
        c=ecl();c['measurement_schedule']['fx_journals']=[[{'side':'Dr','account':'instrument gross carrying amount','amount':'10'},{'side':'Cr','account':'FX gain','amount':'10'}]];c['measurement_schedule']['fx_memo']='Reviewed FX'
        with self.assertRaisesRegex(ReviewRequired,'do not reconcile'):execute('financial-instruments-ecl',c)
    def test_malformed_case_structured_block(self):
        c=revenue();del c['obligations'][0]['id']
        self.assertEqual(assess_case('revenue-recognition',c)['status'],'blocked')
        c=revenue();c['obligations']='malformed'
        self.assertEqual(assess_case('revenue-recognition',c)['status'],'blocked')
    def test_prospective_modification_canonical_case(self):
        c=revenue();c['obligations']=[c['obligations'][1]];c['obligations'][0].update(ssp='1200',progress=str(Decimal(1)/12))
        c['price_components']['fixed']='1200';c['balance_bridge'].update(opening_revenue='600',opening_contract_net='-900',billings='0',cash_received='0')
        c['modification']={'approved':True,'added_distinct':True,'price_at_adjusted_ssp':False,'remaining_distinct':True,'unrecognized_old_price':'600','new_price':'300','remaining_obligation_ids':['service']}
        r=execute('revenue-recognition',c)['calculations'];self.assertEqual(r['period_revenue'],75);self.assertEqual(r['contract_bridge']['closing'],-825)
    def test_integrated_modification_negative_catch_up(self):
        c=revenue();c['obligations']=[c['obligations'][1]];c['obligations'][0].update(ssp='1400',progress='0.4')
        c['price_components']['fixed']='1400';c['balance_bridge']['opening_revenue']='600'
        c['modification']={'approved':True,'added_distinct':False,'price_at_adjusted_ssp':False,'remaining_distinct':False,'integrated_promise_memo':'Integrated work revised cost forecast'}
        self.assertEqual(execute('revenue-recognition',c)['calculations']['period_revenue'],-40)
    def test_matched_intercompany_balances(self):
        c=consolidation();c['entities'][0]['balances'].update(AR='10',equity='-390');c['entities'][1]['balances'].update(AP='-10',inventory='10')
        c['intercompany']=[{'seller':'S','buyer':'P','debit_account':'AP','credit_account':'AR','amount':'10','matched':True,'family':'balance','source_id':'IC1'}]
        c['statement_mapping'].update(AR='assets',AP='liabilities',inventory='assets');c['equity_bridge'].update(opening='410',closing='410')
        r=execute('consolidation',c)['calculations']['consolidated_balances'];self.assertEqual(r['AR'],0);self.assertEqual(r['AP'],0)
    def test_unrealized_inventory_profit(self):
        c=consolidation();c['entities'][0]['balances'].update(inventory='10',equity='-390');c['statement_mapping'].update(inventory='assets',**{'cost of sales / disposal gain':'expenses'})
        c['profit_eliminations']=[{'type':'inventory','seller':'P','buyer':'S','profit':'20','remaining_fraction':'0.5','asset_account':'inventory','source_memo':'Seller margin and held units','tax_effect_journal':[],'tax_memo':'Supported no current deferred tax effect'}]
        c['equity_bridge'].update(opening='410',profit='-10',closing='400')
        r=execute('consolidation',c)['calculations'];self.assertEqual(r['consolidated_balances']['inventory'],0);self.assertEqual(r['statements']['expenses'],10)
    def test_translation_wholly_owned_case(self):
        c=consolidation();c['entities'][0]['balances'].update(investment='100',equity='-400');c['investments'][0].update(investment='100',nci_at_acquisition='0');c['nci'][0].update(ownership='1',opening='0')
        c['entities'][1]['translation']={'account_rates':{'cash':'2','sub equity':'1'},'rate_evidence':'Closing and historical supported rates','cta_account':'CTA'}
        c['statement_mapping']['CTA']='equity';c['cash_flow_bridge'].update(fx='100',closing_cash='500');c['equity_bridge'].update(oci='100',closing='500')
        c['cta_bridge'].update(translation='-100',closing='-100',cta_accounts=['CTA'])
        r=execute('consolidation',c)['calculations'];self.assertEqual(r['translations'][0]['cta'],-100);self.assertEqual(r['consolidated_balances']['cash'],500)
    def test_finite_decimal_and_journal_side(self):
        for bad in ['NaN','Infinity','-Infinity',True,1.2]:
            with self.assertRaises(ReviewRequired):dec(bad)
        with self.assertRaises(ReviewRequired):balance([{'side':'X','account':'cash','amount':'0'}])

if __name__=='__main__':unittest.main()
