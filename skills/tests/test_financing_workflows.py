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
            r.update(current_carrying='1008.40',noncurrent_carrying='0');self.assertEqual(assess_case('debt-financing',ready('debt-financing',f,c))['status'],'complete')
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

if __name__=='__main__':unittest.main()
