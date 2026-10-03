import copy,json,unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from decimal import Decimal
from production import assess_case,to_public,canonical_knowledge,PACKAGES,case_fingerprint
from core_accounting import balance
from financing_cases import case,ready,PACKAGES as NEW,FRAMEWORKS

class FinancingControls(unittest.TestCase):
    def each(self,fn):
        for p in NEW:
            for fw in FRAMEWORKS:
                with self.subTest(package=p,framework=fw):fn(p,fw)
    def test_four_framework_complete(self):
        self.each(lambda p,f:self.assertEqual(assess_case(p,ready(p,f))['status'],'complete'))
    def test_unsigned_partial(self):
        def run(p,f):
            c=ready(p,f);c.pop('reviewer_signoff');self.assertEqual(assess_case(p,c)['status'],'partial')
        self.each(run)
    def test_stale_certification(self):
        def run(p,f):
            c=ready(p,f);c['judgment_memo']+=' changed';self.assertEqual(assess_case(p,c)['status'],'partial')
        self.each(run)
    def test_reviewer_independence(self):
        def run(p,f):
            c=ready(p,f);c['reviewer_signoff']['reviewer']=c['preparer'];self.assertEqual(assess_case(p,c)['status'],'partial')
        self.each(run)
    def test_knowledge_hash_change(self):
        def run(p,f):
            c=ready(p,f);c['knowledge_review']['documents'][0]['sha256']='stale';self.assertEqual(assess_case(p,c)['status'],'blocked')
        self.each(run)
    def test_missing_source_evidence(self):
        def run(p,f):
            c=case(p,f);c['accounting_policy'].pop('evidence');self.assertEqual(assess_case(p,ready(p,f,c))['status'],'blocked')
        self.each(run)
    def test_stale_approval(self):
        def run(p,f):
            c=case(p,f);c['accounting_policy']['approved_version']='stale';self.assertEqual(assess_case(p,ready(p,f,c))['status'],'blocked')
        self.each(run)
    def test_population_omission(self):
        def run(p,f):
            c=case(p,f);c['source_inventory']=[];self.assertEqual(assess_case(p,ready(p,f,c))['status'],'blocked')
        self.each(run)
    def test_population_amount(self):
        def run(p,f):
            c=case(p,f);c['controls']['population_amount']='0';self.assertEqual(assess_case(p,ready(p,f,c))['status'],'blocked')
        self.each(run)
    def test_gl_offset_omission(self):
        def run(p,f):
            c=case(p,f);c['gl']=c['gl'][:-1];c['gl_inventory']=c['gl_inventory'][:-1];self.assertEqual(assess_case(p,ready(p,f,c))['status'],'blocked')
        self.each(run)
    def test_statement_tie(self):
        def run(p,f):
            c=case(p,f);c['gl'][0]['statement']='12345';self.assertEqual(assess_case(p,ready(p,f,c))['status'],'blocked')
        self.each(run)
    def test_policy_framework_mismatch(self):
        def run(p,f):
            c=case(p,f);c['accounting_policy']['framework']='wrong';self.assertEqual(assess_case(p,ready(p,f,c))['status'],'blocked')
        self.each(run)
    def test_entity_scope_mismatch(self):
        def run(p,f):
            c=case(p,f);c['accounting_policy']['entity_scope']='wrong';self.assertEqual(assess_case(p,ready(p,f,c))['status'],'blocked')
        self.each(run)
    def test_period_mismatch(self):
        def run(p,f):
            c=case(p,f);c['accounting_policy']['effective_period'][0]='2025-01-01';self.assertEqual(assess_case(p,ready(p,f,c))['status'],'blocked')
        self.each(run)
    def test_malformed(self):
        for p in NEW:
            for c in [None,[],{},'bad',{'framework':'BOGUS'}]:self.assertEqual(assess_case(p,c)['status'],'blocked')
    def test_privacy_all_routes(self):
        def run(p,f):
            c=ready(p,f);c['internal_payload']={'reviewer':'secret-reviewer','hash':'secret-hash','source_note':'Source: private'};c=ready(p,f,c);r=assess_case(p,c)
            self.assertEqual(r['status'],'complete')
            for route in ['answer_context','answer','retrieval_snippet','citation','tool_output','user_log','export']:
                s=json.dumps(to_public(r,route));self.assertNotIn('secret',s);self.assertNotIn('source_note',s);self.assertNotIn('case_fingerprint',s)
        self.each(run)
    def test_journals_balanced(self):
        def run(p,f):
            r=assess_case(p,ready(p,f));self.assertEqual(r['status'],'complete')
            for j in r['journal_entry_implications']:self.assertTrue(balance(j))
        self.each(run)
    def test_case_immutable(self):
        def run(p,f):
            c=ready(p,f);original=copy.deepcopy(c);assess_case(p,c);self.assertEqual(c,original)
        self.each(run)
    def test_inventory_all_frameworks_blocked(self):
        for f in FRAMEWORKS:self.assertEqual(assess_case('inventory-cost',case('inventory-cost',f))['status'],'blocked')
    def test_tax_evidence_preserved(self):
        for f in FRAMEWORKS:
            claims,docs=canonical_knowledge(PACKAGES['income-taxes'][1],f);self.assertEqual(len(claims),16)
            self.assertTrue(all(x['evidence_status']=='MODEL_DERIVED_AUDIT_REQUIRED' and x['audit_required'] for x in claims))
    def test_numerical_results(self):
        self.assertEqual(assess_case('income-taxes',ready('income-taxes'))['calculations']['total_tax_expense'],Decimal('275'))
        self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll'))['calculations']['net_cash'],Decimal('4000'))
        self.assertEqual(assess_case('debt-financing',ready('debt-financing'))['calculations']['debt'][0]['closing'],Decimal('1008.4'))
        self.assertEqual(assess_case('intangible-assets',ready('intangible-assets'))['calculations']['assets'][0]['amortization'],Decimal('100000'))
        self.assertEqual(assess_case('fair-value-measurement',ready('fair-value-measurement'))['calculations']['measurements'][0]['value'],Decimal('120'))
    def test_tax_us_enactment(self):
        c=case('income-taxes','US_GAAP');c['jurisdictions'][0]['rate_status']='substantively_enacted';self.assertEqual(assess_case('income-taxes',ready('income-taxes',c=c))['status'],'blocked')
    def test_tax_wrong_uk_model(self):
        c=case('income-taxes','UK_GAAP');c['jurisdictions'][0]['difference_model']='temporary_difference';self.assertEqual(assess_case('income-taxes',ready('income-taxes',c=c))['status'],'blocked')
    def test_tax_omitted_decision_area(self):
        c=case('income-taxes');c['tax_area_reviews'].pop();self.assertEqual(assess_case('income-taxes',ready('income-taxes',c=c))['status'],'blocked')
    def test_tax_sign_error(self):
        c=case('income-taxes');c['jurisdictions'][0]['differences'][1]['kind']='taxable';self.assertEqual(assess_case('income-taxes',ready('income-taxes',c=c))['status'],'blocked')
    def test_tax_offset_without_right(self):
        c=case('income-taxes');c['jurisdictions'][0].update(offset_permitted=True,same_tax_authority=True,same_tax_entity=True,enforceable_offset_right=False,settlement_conditions_met=True);self.assertEqual(assess_case('income-taxes',ready('income-taxes',c=c))['status'],'blocked')
    def test_tax_recovery_boundary(self):
        c=case('income-taxes');c['jurisdictions'][0]['differences'][1]['recoverable_tax_amount']='51';self.assertEqual(assess_case('income-taxes',ready('income-taxes',c=c))['status'],'blocked')
    def test_payroll_withholding_not_extra_cost(self):
        c=case('employee-benefits-payroll');c['register_expense']='11800';self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll',c=c))['status'],'blocked')
    def test_payroll_nonaccumulating_leave(self):
        c=case('employee-benefits-payroll');c['benefits'][0].update(kind='leave',accumulating=False);self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll',c=c))['status'],'blocked')
    def test_payroll_actuarial_block(self):
        c=case('employee-benefits-payroll');c['benefits'][0]['kind']='defined_benefit';self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll',c=c))['status'],'blocked')
    def test_debt_schedule_gap(self):
        c=case('debt-financing');c['debt'][0]['schedule'][0]['start']='2026-02-01';self.assertEqual(assess_case('debt-financing',ready('debt-financing',c=c))['status'],'blocked')
    def test_debt_nominal_not_eir(self):
        c=case('debt-financing');c['debt'][0]['schedule'][0]['expected_interest']='50';self.assertEqual(assess_case('debt-financing',ready('debt-financing',c=c))['status'],'blocked')
    def test_debt_modification_block(self):
        c=case('debt-financing');c['debt'][0]['modified']=True;self.assertEqual(assess_case('debt-financing',ready('debt-financing',c=c))['status'],'blocked')
    def test_debt_maturity_omission(self):
        c=case('debt-financing');c['debt'][0]['maturities']=[];c['debt'][0]['maturity_inventory']=[];self.assertEqual(assess_case('debt-financing',ready('debt-financing',c=c))['status'],'blocked')
    def test_intangible_uk_indefinite(self):
        c=case('intangible-assets','UK_GAAP');c['assets'][0]['life']='indefinite';self.assertEqual(assess_case('intangible-assets',ready('intangible-assets',c=c))['status'],'blocked')
    def test_intangible_preavailable(self):
        c=case('intangible-assets');c['assets'][0]['available_date']='2027-01-01';self.assertEqual(assess_case('intangible-assets',ready('intangible-assets',c=c))['status'],'blocked')
    def test_intangible_excess_fraction(self):
        c=case('intangible-assets');c['assets'][0]['period_fraction']='1.01';self.assertEqual(assess_case('intangible-assets',ready('intangible-assets',c=c))['status'],'blocked')
    def test_fv_lowest_significant_level(self):
        c=case('fair-value-measurement');c['measurements'][0]['inputs'].append(copy.deepcopy(c['measurements'][0]['inputs'][0]));c['measurements'][0]['inputs'][-1].update(id='unobservable',level='3');c['measurements'][0]['input_inventory'].append('unobservable');self.assertEqual(assess_case('fair-value-measurement',ready('fair-value-measurement',c=c))['status'],'blocked')
    def test_fv_transaction_cost_excluded(self):
        c=case('fair-value-measurement');c['measurements'][0]['expected_value']='119';self.assertEqual(assess_case('fair-value-measurement',ready('fair-value-measurement',c=c))['status'],'blocked')
    def test_fv_stale_date(self):
        c=case('fair-value-measurement');c['measurements'][0]['measurement_date']='2025-12-31';self.assertEqual(assess_case('fair-value-measurement',ready('fair-value-measurement',c=c))['status'],'blocked')
    def test_fv_pre2026_uk(self):
        c=case('fair-value-measurement','UK_GAAP');c['period_start']='2025-01-01';c['applicability_review']['effective_period'][0]=c['period_start'];c['accounting_policy']['effective_period'][0]=c['period_start'];self.assertEqual(assess_case('fair-value-measurement',ready('fair-value-measurement',c=c))['status'],'blocked')

    def test_source_entity_mismatch(self):
        def run(p,f):
            c=case(p,f);key=next(k for k in ['jurisdictions','benefits','debt','assets','measurements'] if k in c);c[key][0]['source_entity']='Other entity';self.assertEqual(assess_case(p,ready(p,f,c))['status'],'blocked')
        self.each(run)
    def test_source_framework_mismatch(self):
        def run(p,f):
            c=case(p,f);key=next(k for k in ['jurisdictions','benefits','debt','assets','measurements'] if k in c);c[key][0]['source_framework']='Wrong';self.assertEqual(assess_case(p,ready(p,f,c))['status'],'blocked')
        self.each(run)
    def test_source_period_mismatch(self):
        def run(p,f):
            c=case(p,f);key=next(k for k in ['jurisdictions','benefits','debt','assets','measurements'] if k in c);c[key][0]['source_period']=['2025-01-01','2025-12-31'];self.assertEqual(assess_case(p,ready(p,f,c))['status'],'blocked')
        self.each(run)
    def test_implementation_fingerprint_change(self):
        from unittest.mock import patch
        def run(p,f):
            c=ready(p,f)
            if p=='fair-value-measurement':return
            with patch('production.case_fingerprint',return_value='changed implementation'):
                self.assertEqual(assess_case(p,c)['status'],'partial')
        self.each(run)
    def test_zero_activity(self):
        def run(p,f):
            c=case(p,f);key=next(k for k in ['jurisdictions','benefits','debt','assets','measurements'] if k in c);c[key]=[];c['source_inventory']=[];c['gl']=[];c['gl_inventory']=[];c['controls'].update(population_count=0,population_amount='0')
            for k in ['cash_total','register_expense','register_closing','register_withholding','statement_tax_expense','statement_pretax']:
                if k in c:c[k]='0'
            self.assertEqual(assess_case(p,ready(p,f,c))['status'],'complete')
        self.each(run)
    def test_debt_current_maturity_QA(self):
        for f in FRAMEWORKS:
            c=case('debt-financing',f);r=c['debt'][0];r['maturities'][0]['date']='2027-06-30';self.assertEqual(assess_case('debt-financing',ready('debt-financing',f,c))['status'],'blocked')
            r.update(current_carrying='1008.40',noncurrent_carrying='0');r['maturities'][0]['date']='2027-12-31';v=r['yield_validation'];v['cashflows']=v['cashflows'][:1]+[dict(v['cashflows'][-1],date='2027-12-31',amount='1089.072')];v['flow_inventory']=['coupon1','redemption'];self.assertEqual(assess_case('debt-financing',ready('debt-financing',f,c))['status'],'complete')
    def test_intangible_zero_amortization_QA(self):
        c=case('intangible-assets');c['assets'][0].update(period_fraction='0',expected_amortization='0',gl_accumulated='0')
        for r in c['gl']:
            if r['id'] in ['Amortization expense','Accumulated amortization']:r.update(closing='0',statement='0')
        self.assertEqual(assess_case('intangible-assets',ready('intangible-assets',c=c))['status'],'blocked')
    def test_intangible_quarter_QA(self):
        for f in FRAMEWORKS:
            c=case('intangible-assets',f);c['reporting_period']='2026-03-31';c['controls']['as_of']=c['reporting_period'];c['applicability_review']['effective_period'][1]=c['reporting_period'];c['accounting_policy']['effective_period'][1]=c['reporting_period'];c['assets'][0]['source_period'][1]=c['reporting_period']
            self.assertEqual(assess_case('intangible-assets',ready('intangible-assets',f,c))['status'],'blocked')
            c['assets'][0].update(period_fraction=str(Decimal(90)/Decimal(365)),expected_amortization='24657.53',gl_accumulated='24657.53')
            for r in c['gl']:
                if r['id']=='Amortization expense':r.update(closing='24657.53',statement='24657.53')
                if r['id']=='Accumulated amortization':r.update(closing='-24657.53',statement='-24657.53')
            self.assertEqual(assess_case('intangible-assets',ready('intangible-assets',f,c))['status'],'complete')
    def test_credit_cannot_be_DTL_QA(self):
        c=case('income-taxes');c['jurisdictions'][0]['differences'][1].update(kind='taxable',source='credit');self.assertEqual(assess_case('income-taxes',ready('income-taxes',c=c))['status'],'blocked')
    def test_exception_recovery_contradiction(self):
        c=case('income-taxes');c['jurisdictions'][0]['differences'][1]['recognition_exception']=True;self.assertEqual(assess_case('income-taxes',ready('income-taxes',c=c))['status'],'blocked')
    def test_opening_stock_GL_QA(self):
        def run(p,f):
            c=case(p,f);r=c['gl'][0];r['opening']=str(Decimal(r['opening'])+100);r['closing']=str(Decimal(r['closing'])+100);r['statement']=r['closing']
            # Choose owned stock rather than expense/cash.
            owned={'income-taxes':'Deferred tax asset','employee-benefits-payroll':'Employee benefit payable','debt-financing':'Debt carrying liability','intangible-assets':'Intangible asset','fair-value-measurement':'Fair value asset'}[p]
            c=case(p,f);r=next(x for x in c['gl'] if x['id']==owned);r['opening']=str(Decimal(r['opening'])+100);r['closing']=str(Decimal(r['closing'])+100);r['statement']=r['closing'];self.assertEqual(assess_case(p,ready(p,f,c))['status'],'blocked')
        self.each(run)
    def test_fv_uncertified_underlying(self):
        c=case('fair-value-measurement');c['handoffs']['instrument'].pop('result');self.assertEqual(assess_case('fair-value-measurement',ready('fair-value-measurement',c=c))['status'],'blocked')
    def test_fv_stale_underlying_certification(self):
        c=case('fair-value-measurement');c['handoffs']['instrument']['case']['judgment_memo']='changed';self.assertEqual(assess_case('fair-value-measurement',ready('fair-value-measurement',c=c))['status'],'blocked')
    def test_fv_altered_journal_offsets(self):
        c=case('fair-value-measurement');c['handoffs']['instrument']['journals'][1][1]['account']='Fair value OCI';self.assertEqual(assess_case('fair-value-measurement',ready('fair-value-measurement',c=c))['status'],'blocked')
    def test_fv_nested_account_metadata(self):
        c=case('fair-value-measurement');c['handoffs']['instrument']['journals'][1][1]['account']={'reviewer':'secret','hash':'secret'};self.assertEqual(assess_case('fair-value-measurement',ready('fair-value-measurement',c=c))['status'],'blocked')
    def test_fv_specialist_levels(self):
        from reporting_cases import pol
        from operational_cases import approved
        for f in FRAMEWORKS:
            for level in [2,3]:
                c=case('fair-value-measurement',f);r=c['measurements'][0];r.update(method='specialist',expected_level=level);r['inputs'][0]['level']=str(level);r['valuation']=pol(c,'valuation',measurement_date=c['reporting_period'],market_exit_value='120',model_validation='Qualified independent model review',calibration='Observed transactions independently checked',input_change_memo='Change analysis reviewed');r['transfer']=approved('transfer',reason_memo='Input significance changed',timing_memo='Reviewed consistent transfer-date policy')
                self.assertEqual(assess_case('fair-value-measurement',ready('fair-value-measurement',f,c))['status'],'complete')
    def test_decimal_malformed_boundaries(self):
        for value in ['NaN','Infinity',True,.1,'bad']:
            for p,key,field in [('income-taxes','jurisdictions','current_rate'),('employee-benefits-payroll','benefits','units'),('debt-financing','debt','draws'),('intangible-assets','assets','residual'),('fair-value-measurement','measurements','quote')]:
                c=case(p);c[key][0][field]=value;self.assertEqual(assess_case(p,ready(p,c=c))['status'],'blocked')
    def test_duplicate_source_ids(self):
        def run(p,f):
            c=case(p,f);key=next(k for k in ['jurisdictions','benefits','debt','assets','measurements'] if k in c);c[key].append(copy.deepcopy(c[key][0]));self.assertEqual(assess_case(p,ready(p,f,c))['status'],'blocked')
        self.each(run)
    def test_imports_evidence_only_exact_once(self):
        from operational_cases import approved
        from reporting_cases import certified
        from additional_cases import award
        from production import execute
        for f in FRAMEWORKS:
            source=certified('share-based-compensation',f,case=award(f));r=execute('share-based-compensation',source)
            c=case('employee-benefits-payroll',f);c['imports']=[approved('sbc',package='share-based-compensation',case=source,result=r,mode='evidence_only')]
            self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll',f,c))['status'],'complete')
            c['imports'][0]['mode']='post_journals';self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll',f,c))['status'],'blocked')
            c['imports'][0]['mode']='evidence_only';dupe=copy.deepcopy(c['imports'][0]);dupe['id']='sbc_duplicate';c['imports'].append(dupe);self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll',f,c))['status'],'blocked')

    def test_fv_duplicate_underlying_result(self):
        c=case('fair-value-measurement');r=copy.deepcopy(c['measurements'][0]);r['id']='duplicate';c['measurements'].append(r);c['source_inventory'].append('duplicate');c['controls'].update(population_count=2,population_amount='240');self.assertEqual(assess_case('fair-value-measurement',ready('fair-value-measurement',c=c))['status'],'blocked')
    def test_payroll_bonus_current_vs_cumulative(self):
        for f in FRAMEWORKS:
            c=case('employee-benefits-payroll',f);r=c['benefits'][0];r.update(kind='bonus',units='600',rate='.1',employer_rate='0',measurement_basis='cumulative_entitlement',prior_service_expense='30',opening='30',payment='0',withholding='0',expected_charge='30',gl_closing='60');c.update(cash_total='0',register_expense='30',register_closing='60',register_withholding='0');c['controls']['population_amount']='30'
            c['gl']=[dict(x,opening='-30' if x['id']=='Employee benefit payable' else '0',closing='-60' if x['id']=='Employee benefit payable' else '30' if x['id']=='Employee benefit expense' else '0',statement='-60' if x['id']=='Employee benefit payable' else '30' if x['id']=='Employee benefit expense' else '0') for x in c['gl']]
            self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll',f,c))['status'],'complete')
            r['expected_charge']='60';self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll',f,c))['status'],'blocked')
    def test_payroll_other_supported_benefits(self):
        for f in FRAMEWORKS:
            for kind in ['bonus','commission','leave','defined_contribution','employer_tax']:
                c=case('employee-benefits-payroll',f);r=c['benefits'][0];r['kind']=kind
                if kind=='leave':r['accumulating']=True
                if kind in ['defined_contribution','employer_tax']:
                    r.update(units='54',payment_service_units='54',employer_rate='0')
                self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll',f,c))['status'],'complete')
    def test_payroll_termination_framework_routes(self):
        from reporting_cases import pol
        from operational_cases import handoffs
        for f in FRAMEWORKS:
            c=case('employee-benefits-payroll',f);r=c['benefits'][0];r['kind']='termination';r['termination_review']=pol(c,'termination',withdrawal_memo='Actual signed inability-to-withdraw evidence',future_service_memo='No service retention condition',framework_trigger_memo='Independently verified actual framework event',recognition_date='2026-12-01',future_service_required=False,cannot_withdraw=True,linked_restructuring_recognized=False,handoff='termination')
            if f in ['US_GAAP','UK_GAAP']:
                c['handoffs']=handoffs(c,{'termination':'Termination benefit accounting'});c['handoffs']['termination']['amount']='10800'
            self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll',f,c))['status'],'complete')
            r['termination_review']['future_service_required']=True;self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll',f,c))['status'],'blocked')
    def test_payroll_long_term_settlement(self):
        c=case('employee-benefits-payroll');c['benefits'][0]['settlement_date']='2028-01-01';self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll',c=c))['status'],'blocked')
    def test_tax_us_allowance_vs_probable_asset(self):
        for f in FRAMEWORKS:
            c=case('income-taxes',f);r=c['jurisdictions'][0];d=r['differences'][1];d['recoverable_tax_amount']='30';d['expected_gross']='50' if f=='US_GAAP' else '30';d['expected_allowance']='20' if f=='US_GAAP' else '0';r['closing_dta']=d['expected_gross'];r['closing_allowance']=d['expected_allowance'];r['etr_adjustments'][0]['amount']='45';c['statement_tax_expense']='295'
            for g in c['gl']:
                if g['id']=='Deferred tax asset':g.update(closing=d['expected_gross'],statement=d['expected_gross'])
                if g['id']=='Deferred tax expense':g.update(closing='45',statement='45')
            if f=='US_GAAP':
                from operational_cases import approved
                c['gl'].append(approved('Deferred tax valuation allowance',opening='0',closing='-20',statement='-20'));c['gl_inventory'].append('Deferred tax valuation allowance')
            result=assess_case('income-taxes',ready('income-taxes',f,c));self.assertEqual(result['status'],'complete');self.assertEqual(result['calculations']['jurisdictions'][0]['dta_net'],Decimal('30'))
    def test_tax_rate_change_is_movement(self):
        from operational_cases import approved
        for f in FRAMEWORKS:
            c=case('income-taxes',f);r=c['jurisdictions'][0];d=r['differences'][0];d.update(opening_gross='75',reversal_rate='.30',expected_gross='90');r.update(closing_dtl='90');r['etr_adjustments'][0]['amount']='-35';c['statement_tax_expense']='215'
            for g in c['gl']:
                if g['id']=='Deferred tax liability':g.update(opening='-75',closing='-90',statement='-90')
                if g['id']=='Deferred tax expense':g.update(closing='-35',statement='-35')
            self.assertEqual(assess_case('income-taxes',ready('income-taxes',f,c))['status'],'complete')
    def test_intangible_disposal_gain(self):
        from financing_cases import gl
        for f in FRAMEWORKS:
            c=case('intangible-assets',f);r=c['assets'][0];r.update(disposed=True,proceeds='550000',gl_cost='0',gl_accumulated='0');gl(c,{'Intangible asset':'0','Cash':'-50000','Amortization expense':'100000','Accumulated amortization':'0','Disposal gain':'-50000'})
            self.assertEqual(assess_case('intangible-assets',ready('intangible-assets',f,c))['status'],'complete')
    def test_intangible_indefinite_routes(self):
        from financing_cases import gl
        for f in ['IFRS','US_GAAP','AASB']:
            c=case('intangible-assets',f);r=c['assets'][0];r.update(life='indefinite',annual_impairment_complete=True,expected_amortization='0',gl_accumulated='0');gl(c,{'Intangible asset':'600000','Cash':'-600000'})
            self.assertEqual(assess_case('intangible-assets',ready('intangible-assets',f,c))['status'],'complete')
            r['annual_impairment_complete']=False;self.assertEqual(assess_case('intangible-assets',ready('intangible-assets',f,c))['status'],'blocked')
    def test_intangible_development_pre_gate_cost(self):
        from operational_cases import approved
        from financing_cases import gl
        for f in ['IFRS','UK_GAAP','AASB']:
            c=case('intangible-assets',f);r=c['assets'][0];r.update(origin='development',gate_date='2026-01-01',feasible=True,intention=True,ability=True,benefits=True,resources=True,reliable_measurement=True);r['costs'][0]['kind']='eligible_development'
            self.assertEqual(assess_case('intangible-assets',ready('intangible-assets',f,c))['status'],'complete')
            r['gate_date']='2026-02-01';self.assertEqual(assess_case('intangible-assets',ready('intangible-assets',f,c))['status'],'blocked')
    def test_intangible_us_development_not_IFRS(self):
        c=case('intangible-assets','US_GAAP');c['assets'][0].update(origin='development',gate_date='2026-01-01');self.assertEqual(assess_case('intangible-assets',ready('intangible-assets',c=c))['status'],'blocked')
    def test_tax_credit_not_multiplied_by_rate(self):
        c=case('income-taxes');r=c['jurisdictions'][0];d=r['differences'][1];d.update(source='credit',difference='50');self.assertEqual(assess_case('income-taxes',ready('income-taxes',c=c))['status'],'complete')
    def test_inventory_fabricated_approval_no_bypass(self):
        c=case('inventory-cost');c['knowledge_review']={'claim_ids':['INVENTED-INVENTORY'], 'documents':[], 'reviewer':'fake'};c['reviewer_signoff']={'approved':True,'reviewer':'fake','case_fingerprint':case_fingerprint(c)};self.assertEqual(assess_case('inventory-cost',c)['status'],'blocked')
    def test_intangible_purchase_chronology_QA(self):
        c=case('intangible-assets');c['assets'][0]['costs'][0]['date']='2026-12-31';self.assertEqual(assess_case('intangible-assets',ready('intangible-assets',c=c))['status'],'blocked')
    def test_intangible_short_life_floor_QA(self):
        for f in FRAMEWORKS:
            c=case('intangible-assets',f);r=c['assets'][0];r.update(remaining_years='.5',expected_amortization='600000',gl_accumulated='600000')
            for g in c['gl']:
                if g['id']=='Amortization expense':g.update(closing='600000',statement='600000')
                if g['id']=='Accumulated amortization':g.update(closing='-600000',statement='-600000')
            self.assertEqual(assess_case('intangible-assets',ready('intangible-assets',f,c))['status'],'complete')
            r.update(expected_amortization='1200000',gl_accumulated='1200000');self.assertEqual(assess_case('intangible-assets',ready('intangible-assets',f,c))['status'],'blocked')
    def test_intangible_disposal_cutoff_QA(self):
        c=case('intangible-assets');c['assets'][0].update(disposed=True,disposal_date='2026-06-30');self.assertEqual(assess_case('intangible-assets',ready('intangible-assets',c=c))['status'],'blocked')
    def test_tax_prepayment_specialist(self):
        c=case('income-taxes');c['jurisdictions'][0].update(tax_paid='300',closing_current='-50');self.assertEqual(assess_case('income-taxes',ready('income-taxes',c=c))['status'],'blocked')
    def test_framework_overlay_boundaries(self):
        for p in NEW:
            c=case(p,'AASB');c['entity_type']='not_for_profit';c['applicability_review']['entity_scope']='not_for_profit';self.assertEqual(assess_case(p,ready(p,c=c))['status'],'blocked')
            c=case(p,'UK_GAAP');c['uk_standard']='FRS_101';self.assertEqual(assess_case(p,ready(p,c=c))['status'],'blocked')
    def test_disclosure_incomplete(self):
        def run(p,f):
            c=case(p,f);c['disclosure_review']['complete']=False;self.assertEqual(assess_case(p,ready(p,f,c))['status'],'blocked')
        self.each(run)
    def test_intangible_unreliable_uk_life(self):
        c=case('intangible-assets','UK_GAAP');c['assets'][0].update(life_reliably_estimated=False,remaining_years='11');self.assertEqual(assess_case('intangible-assets',ready('intangible-assets',c=c))['status'],'blocked')
    def test_fv_underlying_result_entity_mismatch(self):
        c=case('fair-value-measurement');c['handoffs']['instrument']['case']['entity']='Other';self.assertEqual(assess_case('fair-value-measurement',ready('fair-value-measurement',c=c))['status'],'blocked')
    def test_fv_underlying_result_partial(self):
        c=case('fair-value-measurement');c['handoffs']['instrument']['result']['status']='partial';self.assertEqual(assess_case('fair-value-measurement',ready('fair-value-measurement',c=c))['status'],'blocked')
    def test_fv_underlying_zero_quote(self):
        c=case('fair-value-measurement');c['measurements'][0]['quote']='0';self.assertEqual(assess_case('fair-value-measurement',ready('fair-value-measurement',c=c))['status'],'blocked')
    def test_immutable_map_actual_registers(self):
        import hashlib
        root=Path(__file__).resolve().parents[2];m=json.loads((root/'skills/FINANCING-KNOWLEDGE-MAP.json').read_text())
        self.assertEqual((m['canonical_topics'],m['capabilities']),(157,347))
        for p in m['packages'].values():
            for t in p['topics']:
                source=root/t['register'];self.assertEqual(t['sha256'],hashlib.sha256(source.read_bytes()).hexdigest());self.assertEqual({x['claim_id'] for x in t['claims']},{x['claim_id'] for x in json.loads(source.read_text())['claims']})
    def test_debt_fictitious_tail_QA(self):
        from operational_cases import approved
        c=case('debt-financing');r=c['debt'][0];r['maturities'][0].update(date='2027-06-30',carrying='0');r['maturities'].append(approved('tail',date='2028-12-31',principal='0',carrying='1008.4'));r['maturity_inventory'].append('tail');self.assertEqual(assess_case('debt-financing',ready('debt-financing',c=c))['status'],'blocked')
    def test_fv_extra_journal_metadata_never_public_QA(self):
        c=case('fair-value-measurement');c['handoffs']['instrument']['journals'][1][0].update(reviewer='secret-person',sha256='secret-hash',private={'reviewer':'secret'});r=assess_case('fair-value-measurement',ready('fair-value-measurement',c=c));self.assertEqual(r['status'],'complete')
        for route in ['answer_context','answer','retrieval_snippet','citation','tool_output','user_log','export']:self.assertNotIn('secret',json.dumps(to_public(r,route)))
    def test_debt_eir_not_contractually_supported(self):
        c=case('debt-financing');c['debt'][0]['yield_validation']['cashflows'][-1]['amount']='1050';self.assertEqual(assess_case('debt-financing',ready('debt-financing',c=c))['status'],'blocked')
    def test_missing_preparer_cannot_prove_independence(self):
        def run(p,f):
            c=case(p,f);c.pop('preparer');self.assertEqual(assess_case(p,ready(p,f,c))['status'],'blocked')
        self.each(run)
    def test_payroll_future_payment_and_service(self):
        c=case('employee-benefits-payroll');c['benefits'][0]['payment_date']='2027-01-01';self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll',c=c))['status'],'blocked')
        c=case('employee-benefits-payroll');c['benefits'][0]['service_end']='2027-01-01';self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll',c=c))['status'],'blocked')
    def test_completed_underlying_JSON_roundtrip(self):
        from production import serializable
        for f in FRAMEWORKS:
            c=json.loads(json.dumps(ready('fair-value-measurement',f),default=serializable));self.assertEqual(assess_case('fair-value-measurement',c)['status'],'complete')
    def test_archived_four_framework_examples(self):
        from reporting_cases import certified
        from production import execute
        root=Path(__file__).resolve().parents[1]
        for p in NEW:
            for f in FRAMEWORKS:
                original=json.loads((root/p/'examples'/f'{f}.case.json').read_text());self.assertNotIn('reviewer_signoff',original)
                # Reissue ONLY these labeled synthetic nested examples against
                # current bytes; never copy a real human approval to new code.
                for h in original.get('handoffs',{}).values():
                    if 'case' in h:
                        h['case']=certified(h['package'],f,case=h['case']);h['result']=execute(h['package'],h['case'])
                c=ready(p,f,original);r=assess_case(p,c);self.assertEqual(r['status'],'complete');self.assertEqual(to_public(r),json.loads((root/p/'examples'/f'{f}.complete.public.json').read_text()))
                c.pop('reviewer_signoff');r=assess_case(p,c);self.assertEqual(r['status'],'partial');self.assertEqual(to_public(r),json.loads((root/p/'examples'/f'{f}.partial.public.json').read_text()))
    def test_debt_intra_interval_cash_omission_QA(self):
        from operational_cases import approved
        from financing_accounting import year_fraction
        from datetime import date
        c=case('debt-financing');v=c['debt'][0]['yield_validation'];v['cashflows'].append(approved('mid',date='2026-06-30',amount='20',principal='0'));v['flow_inventory'].append('mid');shift=Decimal(20)*Decimal('1.08')**(year_fraction(date(2026,1,1),date(2028,12,31))-year_fraction(date(2026,1,1),date(2026,6,30)));v['cashflows'][2]['amount']=str(Decimal(v['cashflows'][2]['amount'])-shift)
        self.assertEqual(assess_case('debt-financing',ready('debt-financing',c=c))['status'],'blocked')
    def test_payroll_pre_service_settlement_QA(self):
        c=case('employee-benefits-payroll');c['benefits'][0].update(service_start='2026-12-01',payment_date='2026-01-01');self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll',c=c))['status'],'blocked')
    def test_payroll_unearned_payment_prefix(self):
        c=case('employee-benefits-payroll');c['benefits'][0]['payment_service_units']='10';self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll',c=c))['status'],'blocked')
    def test_payroll_withholding_opening_and_remittance(self):
        from operational_cases import approved
        for f in FRAMEWORKS:
            c=case('employee-benefits-payroll',f);c.update(opening_withholding='200',withholding_remittances=[approved('remit',date='2026-12-31',amount='600',bank_evidence='Independent bank settlement',authority_evidence='Actual withholding remittance')],withholding_inventory=['remit'],withholding_bank_total='600',register_withholding='600',cash_total='4600')
            for g in c['gl']:
                if g['id']=='Cash':g.update(closing='-4600',statement='-4600')
                if g['id']=='Employee withholding payable':g.update(opening='-200',closing='-600',statement='-600')
            self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll',f,c))['status'],'complete')
            c['withholding_remittances'][0]['date']='2027-01-01';self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll',f,c))['status'],'blocked')
    def test_linked_only_termination_requires_specialist_adapter_QA(self):
        from financing_cases import pol
        for f in ('IFRS','AASB'):
            c=case('employee-benefits-payroll',f);r=c['benefits'][0];r['kind']='termination';r['termination_review']=pol(c,'termination',withdrawal_memo='Reviewed',future_service_memo='No future service',framework_trigger_memo='Reviewed linkage',recognition_date='2026-12-01',future_service_required=False,cannot_withdraw=False,linked_restructuring_recognized=True)
            self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll',f,c))['status'],'blocked')
    def test_withholding_cannot_settle_future_deductions_QA(self):
        from operational_cases import approved
        for f in FRAMEWORKS:
            c=case('employee-benefits-payroll',f);c.update(withholding_remittances=[approved('early',date='2026-01-01',amount='600',bank_evidence='Actual bank payment',authority_evidence='Reviewed remittance')],withholding_inventory=['early'],withholding_bank_total='600',register_withholding='400',cash_total='4600')
            for g in c['gl']:
                if g['id']=='Cash':g.update(closing='-4600',statement='-4600')
                if g['id']=='Employee withholding payable':g.update(closing='-400',statement='-400')
            self.assertEqual(assess_case('employee-benefits-payroll',ready('employee-benefits-payroll',f,c))['status'],'blocked')
    def test_public_CLI_four_framework_roundtrip(self):
        import subprocess,tempfile
        from production import serializable
        root=Path(__file__).resolve().parents[2]
        for p in NEW:
            for f in FRAMEWORKS:
                path=root/'skills'/p/'examples'/f'{f}.case.json'
                with tempfile.TemporaryDirectory() as temp:
                    # Archives are synthetic, not live approvals. Shared implementation
                    # changes invalidate nested certifications; refresh only in scratch.
                    archived=json.loads(path.read_text())
                    if p=='fair-value-measurement':
                        from reporting_cases import certified
                        from production import execute
                        for row in archived['measurements']:
                            h=archived['handoffs'][row['underlying_handoff']];h['case']=certified(h['package'],f,h['case']);h['result']=execute(h['package'],h['case'])
                    unsigned=Path(temp)/'unsigned.json';unsigned.write_text(json.dumps(archived,default=serializable))
                    output=subprocess.check_output([sys.executable,str(root/'skills/run_skill.py'),p,str(unsigned)],text=True)
                    self.assertIn('Review status: partial',json.loads(output)['guidance'])
                    signed=Path(temp)/'synthetic.json';signed.write_text(json.dumps(ready(p,f),default=serializable))
                    output=subprocess.check_output([sys.executable,str(root/'skills/run_skill.py'),p,str(signed)],text=True)
                    self.assertIn('Review status: complete',json.loads(output)['guidance']);self.assertNotIn('case_fingerprint',output);self.assertNotIn('source_note',output)

if __name__=='__main__':unittest.main()
