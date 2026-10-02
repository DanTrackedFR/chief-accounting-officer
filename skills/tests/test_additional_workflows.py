"""Numerical, accounting adverse, four-framework and complete envelope gates."""
import copy
import json
import sys
import unittest
from pathlib import Path
from decimal import Decimal
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from production import assess_case,execute,to_public,case_fingerprint,PACKAGES,canonical_knowledge
from core_accounting import balance,ReviewRequired
from additional_cases import FACTORIES,certify,acquisition,impairment,fx,award,reporting

FRAMEWORKS=('IFRS','US_GAAP','UK_GAAP','AASB')
ROUTES=('answer_context','answer','retrieval_snippet','citation','tool_output','user_log','export')

class AdditionalWorkflowTests(unittest.TestCase):
    def run_case(self,package,c):return assess_case(package,certify(package,c))
    def blocked(self,package,c,fragment=None):
        r=self.run_case(package,c)
        self.assertEqual(r['status'],'blocked',r)
        self.assertEqual(r['journal_entry_implications'],[])
        self.assertIn('specialist_routing',r)
        if fragment:self.assertIn(fragment,r['conclusion'])
        return r

    def test_twenty_framework_end_to_end(self):
        for p,factory in FACTORIES.items():
            for fw in FRAMEWORKS:
                with self.subTest(package=p,framework=fw):
                    r=self.run_case(p,factory(fw));self.assertEqual(r['status'],'complete',r)
                    for entry in r['journal_entry_implications']:self.assertTrue(balance(entry))
                    for route in ROUTES:
                        out=to_public(r,route);s=json.dumps(out,default=str)
                        for forbidden in ('source_note','reviewer_signoff','knowledge_review','MODEL_DERIVED','approval_track','audit_required'):
                            self.assertNotIn(forbidden,s)
                    self.assertTrue(r['evidence']);self.assertTrue(r['disclosures_impacted']);self.assertTrue(r['judgments'])

    def test_contract_fields_and_status(self):
        keys=['id','name','version','status','primary_domain','related_domains','description','triggers','non_triggers',
          'framework_sensitivity','applicable_frameworks','jurisdiction_sensitivity','industry_sensitivity','context_requirements','inputs',
          'outputs','artifacts','dependencies','related_skills','knowledge_sources','risk_level','review_required','completion_criteria']
        root=Path(__file__).resolve().parents[1]
        for p in list(FACTORIES)+['income-taxes']:
            body=(root/p/'SKILL.md').read_text()
            for k in keys:self.assertIn('\n'+k+':',body)
            self.assertTrue((root/p/'methods.md').exists());self.assertTrue((root/p/'workflow.py').exists())

    def test_missing_and_stale_certification(self):
        for p,f in FACTORIES.items():
            c=certify(p,f());c.pop('reviewer_signoff');self.assertEqual(assess_case(p,c)['status'],'partial')
            c=certify(p,f());c['assumptions'].append('Changed premise');self.assertEqual(assess_case(p,c)['status'],'partial')
            c=certify(p,f());c['reviewer_signoff']['reviewer']=c['preparer'];self.assertEqual(assess_case(p,c)['status'],'partial')

    def test_all_framework_context_and_evidence_failures(self):
        for p,f in FACTORIES.items():
            for fw in FRAMEWORKS:
                for key in ('entity','jurisdiction','period_start','evidence','judgment_memo'):
                    c=f(fw);c.pop(key);self.blocked(p,c)
                c=f(fw);c['specialist_items']=['Unresolved expert matter'];self.blocked(p,c)
                c=f(fw);c['applicability_review']['exceptions']=['Not resolved'];self.blocked(p,c)

    def test_knowledge_changed_and_wrong_claims(self):
        for p,f in FACTORIES.items():
            c=certify(p,f());c['knowledge_review']['documents'][0]['sha256']='changed'
            self.assertEqual(assess_case(p,c)['status'],'blocked')
            c=certify(p,f());c['knowledge_review']['applied_claim_ids']=['fabricated']
            self.assertEqual(assess_case(p,c)['status'],'blocked')

    def test_operational_topic_retrieved_without_fabricated_claims(self):
        claims,docs=canonical_knowledge(PACKAGES['financial-statements'][1],'IFRS')
        self.assertFalse(any(x['topic_id']=='TOPIC-08-009' for x in claims))
        self.assertTrue(any(x['topic_id']=='TOPIC-08-009' for x in docs))

    def test_tax_is_blocked_not_false_production(self):
        for fw in FRAMEWORKS:
            r=assess_case('income-taxes',{'framework':fw,'reviewer_signoff':{'approved':True}})
            self.assertEqual(r['status'],'blocked');self.assertEqual(r['calculations'],{});self.assertEqual(r['evidence'],[])
            self.assertIn('No approved canonical income-tax',r['conclusion'])
            for route in ROUTES:self.assertEqual(to_public(r,route)['citations'],[])

    def test_nonobjects_malformed_and_numerical_inputs(self):
        for p,f in FACTORIES.items():
            self.assertEqual(assess_case(p,None)['status'],'blocked')
            c=f();c['specialist_items']=False;self.blocked(p,c)
        for value in ('NaN','Infinity',True,0.5):
            c=acquisition();c['consideration']['cash']=value;self.blocked('business-combinations',c)
            c=impairment();c['valuation']['discount_rate']=value;self.blocked('asset-impairment',c)
            c=fx();c['items'][0]['initial_rate']=value;self.blocked('foreign-currency',c)
            c=award();c['tranches'][0]['grant_fair_value']=value;self.blocked('share-based-compensation',c)
            c=reporting();c['current_tb'][0]['balance']=value;self.blocked('financial-statements',c)

    def test_acquisition_nci_costs_and_goodwill(self):
        for fw,expected in [('IFRS','280'),('US_GAAP','280'),('AASB','280'),('UK_GAAP','260')]:
            r=self.run_case('business-combinations',acquisition(fw));self.assertEqual(r['calculations']['initial_goodwill'],Decimal(expected))
            self.assertEqual(r['calculations']['acquisition_expense'],Decimal('0' if fw=='UK_GAAP' else '20'))
        c=acquisition();c['nci']['method']='proportionate';r=self.run_case('business-combinations',c)
        self.assertEqual(r['calculations']['initial_goodwill'],Decimal('240'))
        r=self.run_case('business-combinations',acquisition('UK_GAAP'));self.assertEqual(r['calculations']['closing_goodwill'],Decimal('234'))

    def test_acquisition_bargain_reassessment(self):
        c=acquisition();c['consideration']['cash']='500';c['nci']['method']='proportionate'
        self.assertEqual(self.run_case('business-combinations',copy.deepcopy(c))['calculations']['bargain_gain'],Decimal('60'))
        c['acquisition']['bargain_reassessment_complete']=False;self.blocked('business-combinations',c)
        c=acquisition('UK_GAAP');c['consideration']['cash']='400';self.blocked('business-combinations',c,'negative goodwill')

    def test_acquisition_wrong_models_and_scope(self):
        for fw,model in [('US_GAAP','proportionate'),('UK_GAAP','fair_value')]:
            c=acquisition(fw);c['nci']['method']=model;self.blocked('business-combinations',c)
        for scope in ('asset_acquisition','common_control','reverse','VIE'):
            c=acquisition();c['acquisition']['scope']=scope;self.blocked('business-combinations',c)
        for key in ('business_definition_met','control_obtained','tax_review_complete','exceptions_resolved'):
            c=acquisition();c['acquisition'][key]=False;self.blocked('business-combinations',c)
        c=acquisition();c['consideration']['prior_interest']='10';self.blocked('business-combinations',c,'Step acquisition')

    def test_contingent_liability_and_equity(self):
        c=acquisition();c['consideration']['contingent'].update({'class':'liability','acquisition_amount':'100'})
        c['events']=[{'kind':'contingent_remeasurement','date':'2026-12-31','amount':'20','memo':'FV rises'}]
        r=self.run_case('business-combinations',copy.deepcopy(c));self.assertEqual(r['calculations']['closing_contingent_liability'],Decimal('120'))
        self.assertEqual(r['calculations']['initial_goodwill'],Decimal('380'))
        c['consideration']['contingent']['class']='equity';self.blocked('business-combinations',c,'not subsequently remeasured')

    def test_measurement_period_accounting(self):
        for fw,presentation in [('IFRS','retrospective_acquisition_date'),('US_GAAP','current_period_catchup'),('AASB','retrospective_acquisition_date')]:
            c=acquisition(fw);c['events']=[{'kind':'measurement_period_asset','date':'2026-06-30','amount':'40','memo':'Original provisional asset',
              'account':'acquired cash','acquisition_date_evidence':True,'provisional_item':True,'tax_nci_effects_zero':True,'catchup_depreciation':'4','remaining_goodwill':'240'}]
            r=self.run_case('business-combinations',copy.deepcopy(c));self.assertEqual(r['status'],'complete',r)
            self.assertEqual(r['calculations']['measurement_adjustments'][0]['presentation'],presentation)
            self.assertEqual(r['calculations']['closing_goodwill'],Decimal('240'))
            c['events'][0]['acquisition_date_evidence']=False;self.blocked('business-combinations',c)
        c=acquisition();c['period_start']='2024-01-01';c['applicability_review']['effective_period'][0]=c['period_start'];c['acquisition']['date']='2024-02-29';c['events']=[{'kind':'measurement_period_asset','date':'2026-01-01','amount':'1','memo':'Late',
          'account':'x','acquisition_date_evidence':True,'provisional_item':True,'tax_nci_effects_zero':True,'catchup_depreciation':'0','remaining_goodwill':'279'}]
        self.blocked('business-combinations',c,'one-year')

    def test_ias36_higher_of_and_goodwill_first(self):
        r=self.run_case('asset-impairment',impairment());a=r['calculations']
        self.assertEqual(a['loss'],Decimal('1000'));self.assertEqual(a['allocation']['gw'],Decimal('1000'));self.assertEqual(a['closing']['gw'],Decimal('500'))
        c=impairment();c['valuation']['fv_less_costs']='9000';r=self.run_case('asset-impairment',c)
        self.assertEqual(r['calculations']['recoverable'],Decimal('10800'))

    def test_asc360_undiscounted_screen(self):
        c=impairment('US_GAAP');c['unit']['model']='asc360';c['assets']=c['assets'][1:];c['assets'][0]['carrying']='12000';c['assets'][0]['no_impairment_ceiling']='12000'
        c['valuation'].update(undiscounted='12100',fair_value='10800')
        self.assertEqual(self.run_case('asset-impairment',copy.deepcopy(c))['calculations']['loss'],Decimal('0'))
        c['valuation']['undiscounted']='11500';self.assertEqual(self.run_case('asset-impairment',c)['calculations']['loss'],Decimal('1200'))

    def test_asc350_cap_and_sequence(self):
        c=impairment('US_GAAP');c['valuation']['fair_value']='5000'
        self.assertEqual(self.run_case('asset-impairment',copy.deepcopy(c))['calculations']['loss'],Decimal('1500'))
        c['unit']['other_tests_complete']=False;self.blocked('asset-impairment',c)

    def test_dcf_discount_and_terminal(self):
        c=impairment();c['valuation'].update(cash_flows=[{'year':'1','amount':'110'},{'year':'2','amount':'121'}],discount_rate='0.10',terminal_value='121')
        self.assertEqual(self.run_case('asset-impairment',c)['calculations']['value_in_use'],Decimal('300'))

    def test_allocation_floors_and_exhaustion(self):
        c=impairment();c['assets']=[{'id':i,'account':i,'type':typ,'carrying':car,'floor':floor,'no_impairment_ceiling':car,'valuation_evidence':'Evidence'}
          for i,typ,car,floor in [('gw','goodwill','100','0'),('A','finite','600','580'),('B','finite','300','0')]]
        c['valuation'].update(cash_flows=[{'year':'1','amount':'700'}],fv_less_costs='700')
        a=self.run_case('asset-impairment',copy.deepcopy(c))['calculations']['allocation'];self.assertEqual(a,{'gw':Decimal('100'),'A':Decimal('20'),'B':Decimal('180')})
        c['assets'][2]['floor']='290';self.blocked('asset-impairment',c,'unallocated')

    def test_reversal_ceiling_and_no_goodwill_reversal(self):
        c=impairment();c['assets']=[{'id':'A','account':'asset','type':'finite','carrying':'70','floor':'0','no_impairment_ceiling':'90','valuation_evidence':'Prior impairment'}]
        c['valuation'].update(cash_flows=[{'year':'1','amount':'100'}],fv_less_costs='100')
        c['reversal'].update(requested=True,amounts={'A':'20'},change_memo='Supported change',allocation_model='individual',individual_recoverable_caps={'A':None},individual_recoverable_memo='No separately determinable limit')
        self.assertEqual(self.run_case('asset-impairment',copy.deepcopy(c))['calculations']['closing']['A'],Decimal('90'))
        c['reversal']['amounts']['A']='30';self.blocked('asset-impairment',c,'ceiling')
        c=impairment();c['valuation']['fv_less_costs']='13000';c['reversal'].update(requested=True,amounts={'gw':'1'},allocation_model='unit_pro_rata',individual_recoverable_caps={'plant':None},individual_recoverable_memo='Reviewed')
        self.blocked('asset-impairment',c,'never reversed')

    def test_impairment_uk_and_invalid_perimeter(self):
        c=impairment('UK_GAAP');c['unit']['uk_amortization_complete']=False;self.blocked('asset-impairment',c,'amortization')
        c=impairment('US_GAAP');c['unit']['model']='asc360';self.blocked('asset-impairment',c,'exclude')
        c=impairment();c['assets'].append(copy.deepcopy(c['assets'][0]));self.blocked('asset-impairment',c,'unique')

    def test_fx_transaction_and_cta(self):
        r=self.run_case('foreign-currency',fx());v=r['calculations']
        self.assertEqual(v['monetary_fx_profit'],Decimal('8'));self.assertEqual(v['transactions'][0]['closing'],Decimal('72'))
        self.assertEqual(v['translation']['cta_movement'],Decimal('-11'));self.assertEqual(v['translation']['owners_movement'],Decimal('-8.8'))
        self.assertEqual(v['translation']['nci_movement'],Decimal('-2.2'))

    def test_fx_liability_historical_and_fair_value(self):
        c=fx();c['items'][0]['side']='liability';self.assertEqual(self.run_case('foreign-currency',c)['calculations']['monetary_fx_profit'],Decimal('-8'))
        c=fx();x=c['items'][0];x.update(type='historical_nonmonetary',settled_foreign='0',settlement_date=None)
        self.assertEqual(self.run_case('foreign-currency',copy.deepcopy(c))['calculations']['transactions'][0]['closing'],Decimal('110'))
        x.update(type='fair_value_nonmonetary',fair_value_foreign='150',fair_value_rate='1.18',fair_value_date='2026-12-01',measurement_origin='OCI')
        r=self.run_case('foreign-currency',c);self.assertEqual(r['calculations']['transactions'][0]['closing'],Decimal('177'))
        self.assertEqual(r['calculations']['transactions'][0]['origin'],'fair value OCI')

    def test_fx_cta_not_plug_and_rates(self):
        for key,value in [('reported_closing_net_assets','121'),('profit','21'),('closing_rate','0.81'),('rates_approximate_dates',False)]:
            c=fx();c['translation'][key]=value;self.blocked('foreign-currency',c)
        c=fx();c['translation']['tb'][1]['rate']='0.80';self.blocked('foreign-currency',c,'CTA bridge')
        c=fx();c['items'][0]['opening_book']='111';self.blocked('foreign-currency',c)

    def test_fx_disposal_owner_vs_nci(self):
        c=fx();c['disposal']={'kind':'full','date':'2026-12-31','memo':'Sold operation','qualifying_disposal_reviewed':True,'owners_cta':'-8.8','nci_cta':'-2.2'}
        r=self.run_case('foreign-currency',c);self.assertEqual(r['calculations']['translation']['closing_cta'],Decimal('0'))
        self.assertEqual(r['calculations']['translation']['recycled_owners'],Decimal('-8.8'))

    def test_fx_specialist_boundaries(self):
        for key,value in [('hyperinflation',True),('exchangeability',False),('functional_change',True),('net_investment_items',True),('ledger','USD')]:
            c=fx();c['currency'][key]=value;self.blocked('foreign-currency',c)
        c=fx();c['disposal']['kind']='partial';self.blocked('foreign-currency',c)

    def test_equity_award_three_year_schedule(self):
        c=award();c['reporting_period']='2028-12-31';c['applicability_review']['effective_period'][1]=c['reporting_period']
        original=c['schedule'][0];row2=copy.deepcopy(original);row2.update(date='2027-12-31',opening_booked='36000')
        row2['tranches']['T1'].update(expected_vesting='8000',progress='0.6666666666666666666666666667')
        row3=copy.deepcopy(original);row3.update(date='2028-12-31',opening_booked='64000');row3['tranches']['T1'].update(expected_vesting='8200',actual_forfeited='1800',progress='1')
        c['schedule']=[original,row2,row3]
        r=self.run_case('share-based-compensation',c);self.assertEqual(r['status'],'complete',r)
        self.assertEqual([x['period_expense'] for x in r['calculations']['schedule']],[Decimal('36000'),Decimal('28000'),Decimal('34400')])

    def test_equity_not_reporting_fv_and_market_failure(self):
        c=award();c['award']['conditions']='service_market';c['schedule'][0]['tranches']['T1'].update(current_fair_value='999',market_met=False)
        self.assertEqual(self.run_case('share-based-compensation',c)['calculations']['schedule'][0]['cumulative'],Decimal('36000'))

    def test_cash_award_remeasurement_settlement(self):
        c=award();c['award']['classification']='cash';c['tranches'][0]['vesting_date']='2026-12-31'
        first=c['schedule'][0];first['date']='2026-06-30';first['tranches']['T1'].update(expected_vesting='10000',actual_forfeited='0',progress='0.5',current_fair_value='8')
        second=copy.deepcopy(first);second.update(date='2026-12-31',opening_booked='40000');second['tranches']['T1'].update(progress='1',current_fair_value='12')
        c['schedule']=[first,second];c['event']={'kind':'cash_settlement','date':'2026-12-31','memo':'Vested settlement','amount':'120000','settlement_fair_value':'12','fully_vested':True}
        r=self.run_case('share-based-compensation',c);self.assertEqual(r['status'],'complete',r)
        self.assertEqual([x['period_expense'] for x in r['calculations']['schedule']],[Decimal('40000'),Decimal('80000')])
        self.assertEqual(r['calculations']['closing_equity_or_liability'],Decimal('0'))

    def test_award_us_forfeiture_election(self):
        c=award('US_GAAP');c['award']['forfeiture_policy']='actual';c['schedule'][0]['tranches']['T1']['expected_vesting']='1'
        self.assertEqual(self.run_case('share-based-compensation',c)['calculations']['schedule'][0]['cumulative'],Decimal('36000'))
        c=award();c['award']['forfeiture_policy']='actual';self.blocked('share-based-compensation',c,'not a global')

    def test_modification_floor(self):
        c=award();c['event']={'kind':'beneficial_modification','date':'2026-12-31','memo':'Supported repricing',
          'before_fair_value':'8','after_fair_value':'11','eligible_count':'9000','remaining_service_progress':'1','conditions_unchanged':True,'original_probable':True}
        r=self.run_case('share-based-compensation',copy.deepcopy(c));self.assertEqual(r['calculations']['incremental_modification_expense'],Decimal('27000'))
        c['event']['after_fair_value']='7';self.assertEqual(self.run_case('share-based-compensation',c)['calculations']['incremental_modification_expense'],Decimal('0'))

    def test_cancellation_remaining_cost_and_payment(self):
        c=award();c['event']={'kind':'cancellation','date':'2026-12-31','memo':'Cancelled not vesting failure','unrecognized_original':'72000',
          'payment':'10000','repurchase_fair_value':'9000','not_forfeiture':True,'remaining_cost_memo':'108000 less36000'}
        r=self.run_case('share-based-compensation',copy.deepcopy(c));self.assertEqual(r['calculations']['closing_equity_or_liability'],Decimal('99000'))
        c['event']['unrecognized_original']='1';self.blocked('share-based-compensation',c,'remaining original')

    def test_award_bad_inputs_and_events(self):
        for key in ('group_arrangement','withholding_feature'):
            c=award();c['award'][key]=True;self.blocked('share-based-compensation',c)
        c=award();c['schedule'][0]['tranches']['T1']['expected_vesting']='10001';self.blocked('share-based-compensation',c)
        c=award();c['event']['kind']='cash_to_equity';self.blocked('share-based-compensation',c)
        c=award();c['schedule'][0]['opening_booked']='1';self.blocked('share-based-compensation',c)

    def test_financial_statement_primary_ties(self):
        r=self.run_case('financial-statements',reporting());v=r['calculations']
        self.assertEqual(v['current']['assets'],Decimal('500'));self.assertEqual(v['current']['closing_equity'],Decimal('300'))
        self.assertEqual(v['cash_flow']['operating'],Decimal('240'));self.assertEqual(v['cash_flow']['closing'],Decimal('290'))
        self.assertEqual(v['current']['comprehensive_income'],Decimal('200'))

    def test_ifrs18_aasb18_2027_and_early_adoption(self):
        for fw in ('IFRS','AASB'):
            c=reporting(fw,'2027-01-01');self.assertEqual(self.run_case('financial-statements',copy.deepcopy(c))['status'],'complete')
            c['presentation']['transition_comparatives_reconciled']=False;self.blocked('financial-statements',c)
            c=reporting(fw);c['presentation']['model']='IFRS18' if fw=='IFRS' else 'AASB18';self.blocked('financial-statements',copy.deepcopy(c))
            c['presentation']['early_adoption']=True;c['cash_flow']['start_subtotal']='operating_profit'
            self.assertEqual(self.run_case('financial-statements',c)['status'],'complete')

    def test_statements_independent_bridges_not_only_tb(self):
        for field,value in [('profit','201'),('oci','1'),('opening','99'),('closing','301')]:
            c=reporting();c['equity_bridge'][0][field]=value;self.blocked('financial-statements',c)
        c=reporting();c['cash_flow']['balance_sheet_bridge']='1';self.blocked('financial-statements',c)
        c=reporting();c['notes'][0]['amount']='291';self.blocked('financial-statements',c)

    def test_statements_cash_classification_framework_forks(self):
        for fw in ('US_GAAP','IFRS'):
            c=reporting(fw,'2027-01-01');c['cash_flow']['classifications'][0]['kind']='interest_received'
            if fw=='US_GAAP':self.assertEqual(self.run_case('financial-statements',c)['status'],'complete')
            else:self.blocked('financial-statements',c,'classification mismatch')
        c=reporting('US_GAAP');c['cash_flow']['classifications'][0]['kind']='dividends_paid';self.blocked('financial-statements',c)

    def test_statements_disclosure_completeness_and_uk_gates(self):
        c=reporting();c['coverage']['narrative_reviewed']=False;self.blocked('financial-statements',c)
        c=reporting();c['coverage']['special_topics'].pop('tax');self.blocked('financial-statements',c)
        c=reporting();c['checklist'].pop();self.blocked('financial-statements',c)
        c=reporting();c['cash_flow']['adjustments'][0]['noncash_acquisition_fx_excluded']=False;self.blocked('financial-statements',c)
        c=reporting('UK_GAAP');c['presentation']['periodic_review_adopted']=False;self.blocked('financial-statements',c)
        c=reporting('UK_GAAP','2027-01-01');c['presentation']['adapted_formats_2027_review_complete']=False;self.blocked('financial-statements',c)

    def test_public_workpapers_omit_internal_memos(self):
        c=reporting();c['notes'][0]['memo']='PRIVATE note memo';c['equity_bridge'][0]['memo']='PRIVATE equity memo'
        s=json.dumps(to_public(self.run_case('financial-statements',c)),default=str)
        self.assertNotIn('PRIVATE',s);self.assertNotIn('population_evidence',s)

    def test_qa_acquisition_prior_period_and_invalid_asset_adjustment(self):
        c=acquisition();c['acquisition']['date']='2025-01-01';self.blocked('business-combinations',c,'Opening acquisitions')
        for account,delta in [('nonexistent','1'),('acquired cash','-1000')]:
            c=acquisition();c['events']=[{'kind':'measurement_period_asset','date':'2026-06-30','amount':delta,'memo':'Correction',
              'account':account,'acquisition_date_evidence':True,'provisional_item':True,'tax_nci_effects_zero':True,'catchup_depreciation':'0','remaining_goodwill':'1280'}]
            self.blocked('business-combinations',c,'known asset')

    def test_qa_indefinite_asset_cannot_use_asc360_screen(self):
        c=impairment('US_GAAP');c['unit']['model']='asc360';c['assets']=c['assets'][1:];c['assets'][0].update(type='indefinite',carrying='100',no_impairment_ceiling='100')
        c['valuation'].update(undiscounted='200',fair_value='20');self.blocked('asset-impairment',copy.deepcopy(c),'indefinite')
        c['unit']['model']='asc350_indefinite';self.assertEqual(self.run_case('asset-impairment',c)['calculations']['loss'],Decimal('80'))

    def test_qa_unit_reversal_is_proportional_with_caps(self):
        c=impairment();c['assets']=[{'id':i,'account':i,'type':'finite','carrying':'50','floor':'0','no_impairment_ceiling':'100','valuation_evidence':'Prior impairment'} for i in ('A','B')]
        c['valuation'].update(cash_flows=[{'year':'1','amount':'150'}],fv_less_costs='150')
        c['reversal'].update(requested=True,allocation_model='unit_pro_rata',amounts={'A':'50','B':'0'},individual_recoverable_caps={'A':None,'B':None},individual_recoverable_memo='No separately determinable individual caps')
        self.blocked('asset-impairment',copy.deepcopy(c),'pro-rata')
        c['reversal']['amounts']={'A':'25','B':'25'};r=self.run_case('asset-impairment',c)
        self.assertEqual(r['calculations']['closing'],{'A':Decimal('75'),'B':Decimal('75')})

    def test_qa_carried_receivable_and_accumulated_cta(self):
        c=fx();c['items'][0].update(initial_date='2025-01-01',opening_route='carried_monetary',opening_rate='1.15',opening_book='115')
        c['translation']['opening_cta']='10';c['translation']['tb'][1]['rate']='0.80'
        r=self.run_case('foreign-currency',c);self.assertEqual(r['status'],'complete',r)
        self.assertEqual(r['calculations']['monetary_fx_profit'],Decimal('3'))
        self.assertEqual(r['calculations']['translation']['cta_movement'],Decimal('-11'))
        self.assertEqual(r['calculations']['translation']['closing_cta'],Decimal('-1'))

    def test_qa_award_current_period_opening_and_invalid_quantities(self):
        c=award();c['award']['grant_date']='2025-01-01';c['award']['opening_cumulative']='36000';c['schedule'][0]['opening_booked']='36000'
        c['schedule'][0]['tranches']['T1']['progress']='0.6666666666666666666666666667'
        r=self.run_case('share-based-compensation',c);self.assertEqual(r['calculations']['schedule'][0]['period_expense'],Decimal('36000'))
        c=award();c['schedule'][0]['date']='2025-12-31';self.blocked('share-based-compensation',c,'chronological')
        c=award();c['schedule'][0]['tranches']['T1']['expected_vesting']='10000';self.blocked('share-based-compensation',c,'nonforfeited')
        c=award();c['award']['classification']='cash';c['event']={'kind':'cash_settlement','date':'2026-12-31','memo':'Too early',
          'amount':'90000','settlement_fair_value':'10','fully_vested':True};self.blocked('share-based-compensation',c,'precedes vesting')

    def test_qa_cross_category_statement_line_collision(self):
        c=reporting();c['current_tb'][2]['line']='cash';self.blocked('financial-statements',c,'line collision')

if __name__=='__main__':unittest.main()
