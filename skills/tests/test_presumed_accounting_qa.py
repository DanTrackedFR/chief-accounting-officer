"""Independent accounting challenges; no production or authored-fixture imports.

Economics are constructed here from source facts and independently reperformed.
These tests assert accounting outcomes, not internal implementation details.
"""
import copy
import json
import sys
import unittest
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core_accounting import ReviewRequired, balance
from production import execute, to_public


def source_case(package='fixed-assets', framework='IFRS'):
    case = dict(case_id='independent-source-economics', framework=framework,
                jurisdiction='NL', entity='Workshop BV', entity_type='for_profit',
                period_start='2026-01-01', reporting_period='2026-12-31',
                functional_currency='EUR', assumptions=[], review_mode='prepared_unreviewed',
                source_assurance='presumed_user_provided',
                source=dict(id='workshop-register', version='2026-v1', hash='a'*64),
                source_attestation=dict(authenticated_user_reference='private-user-92831',
                    timestamp='2027-01-05T10:00:00+01:00', statement_version='records-v1',
                    represents_company_records=True))
    if framework == 'US_GAAP': case['us_entity_type'] = 'private_company'
    elif framework == 'UK_GAAP': case.update(uk_standard='FRS_102', uk_standard_edition='2026')
    elif framework == 'AASB': case.update(aasb_compilation='2026', reporting_tier=2)
    if package == 'fixed-assets':
        case['assets'] = [dict(id='lathe-1', opening_cost='600000', opening_accumulated='180000',
            residual='60000', remaining_life='4', ready_date='2024-01-01',
            method='straight_line', scope='ordinary_ppe')]
    else:
        case['invoices'] = [dict(id='invoice-1', supplier='Metalwork', invoice_number='MW-102',
            amount='120', invoice_date='2026-12-31', received_date='2026-12-30',
            units='12', unit_price='10', account='consumables expense',
            recognition_basis='goods_received')]
    return case


def run(package='fixed-assets', case=None):
    return execute(package, source_case(package) if case is None else case,
                   allow_prepared_unreviewed=True, allow_presumed_user_sources=True)


def findings(result, check=None, state=None):
    return [r for r in result.get('anomaly_report', {}).get('findings', [])
            if (check is None or r['check_id'] == check) and
               (state is None or r['severity'] == state)]


class IndependentPresumedAccountingQA(unittest.TestCase):
    def test_plain_register_depreciation_and_balanced_proposal(self):
        case = source_case(); original = copy.deepcopy(case)
        result = run(case=case)
        self.assertEqual(case, original)
        self.assertEqual(result['calculations']['depreciation'], Decimal('90000'))
        self.assertEqual(result['calculations']['assets'][0]['carrying'], Decimal('330000'))
        self.assertEqual(result['status'], 'partial')
        self.assertEqual(result['accounting_determination'], 'SUPPORTED')
        self.assertEqual(result['journal_entry_implications'], [])
        for lines in result['proposed_journal_workpaper']: self.assertTrue(balance(lines))
        self.assertNotIn('reviewer_signoff', result['facts_used'])

    def test_class_assumptions_apply_without_row_repetition(self):
        case = source_case(); row = case['assets'][0]; row['class'] = 'lathes'
        policy = {k: row.pop(k) for k in ('remaining_life','residual','method','scope')}
        policy.update(entity=case['entity'], framework='IFRS', effective_from='2026-01-01',
                      effective_to='2026-12-31', policy_version='machinery-v2')
        case['class_assumptions'] = {'lathes': policy}
        result = run(case=case)
        self.assertEqual(result['calculations']['depreciation'], Decimal('90000'))
        self.assertEqual(result['applied_class_assumptions'], case['class_assumptions'])

    def test_class_assumptions_wrong_entity_cannot_supply_missing_life(self):
        case = source_case(); case['assets'][0].update({'class':'lathes'})
        case['assets'][0].pop('remaining_life')
        case['class_assumptions'] = {'lathes':dict(entity='Other BV', framework='IFRS',
            effective_from='2026-01-01', effective_to='2026-12-31', policy_version='v1', remaining_life='4')}
        result = run(case=case)
        self.assertEqual(result['calculations']['assets'], [])
        self.assertEqual(result['accounting_determination'], 'UNRESOLVED')

    def test_good_row_survives_duplicate_ids(self):
        case = source_case(); first = case['assets'][0]
        case['assets'] += [copy.deepcopy(first), {**first, 'id':'lathe-good'}]
        result = run(case=case)
        self.assertEqual([x['id'] for x in result['calculations']['assets']], ['lathe-good'])
        self.assertEqual(result['calculations']['depreciation'], Decimal('90000'))
        self.assertEqual(len(findings(result,'unique_identifiers','BLOCKED')), 2)

    def test_invalid_first_amount_does_not_skip_later_row(self):
        case = source_case(); row = case['assets'][0]
        case['assets'] = [{**row, 'opening_cost':'invalid'}, {**row, 'id':'lathe-good'}]
        result = run(case=case)
        self.assertEqual([x['id'] for x in result['calculations']['assets']], ['lathe-good'])
        self.assertEqual(result['calculations']['depreciation'], Decimal('90000'))

    def test_depreciation_comparison_does_not_replace_calculation(self):
        case = source_case(); case['assets'][0]['expected_depreciation'] = '100000'
        result = run(case=case)
        self.assertEqual(result['calculations']['depreciation'], Decimal('90000'))
        self.assertTrue(findings(result,'depreciation_comparison','WARNING'))

    def test_pre_readiness_disposal_blocks_affected_row(self):
        case = source_case(); row = case['assets'][0]
        case['assets'] += [{**row, 'id':'bad-disposal', 'ready_date':'2026-07-01',
            'disposal':dict(enabled=True,date='2026-06-30',proceeds='100000',ordinary_sale=True)}]
        result = run(case=case)
        self.assertEqual(len(result['calculations']['assets']), 1)
        self.assertTrue(findings(result,'pre_readiness_disposal','BLOCKED'))

    def test_unready_asset_not_depreciated(self):
        case = source_case(); case['assets'][0]['ready_date'] = '2027-01-01'
        result = run(case=case)
        self.assertEqual(result['calculations']['assets'], [])
        self.assertTrue(findings(result,'readiness','BLOCKED'))

    def test_disposal_gain_independently_reperformed(self):
        case = source_case(); case['assets'][0]['disposal'] = dict(enabled=True,
            date='2026-12-31',proceeds='400000',ordinary_sale=True)
        result = run(case=case); asset = result['calculations']['assets'][0]
        self.assertEqual(asset['disposal_gain'], Decimal('70000'))
        self.assertEqual(asset['closing_cost'], Decimal(0))
        self.assertEqual(asset['closing_accumulated'], Decimal(0))

    def test_no_company_life_is_silently_invented(self):
        case = source_case(); case['assets'][0].pop('remaining_life')
        result = run(case=case)
        self.assertEqual(result['calculations']['assets'], [])
        self.assertTrue(result['validation_requirements'])

    def test_residual_above_carrying_has_zero_supported_depreciation(self):
        case=source_case();case['assets'][0]['residual']='500000'
        result=run(case=case)
        self.assertEqual(len(result['calculations']['assets']),1)
        self.assertEqual(result['calculations']['depreciation'],Decimal(0))
        self.assertTrue(any('residual' in f['explanation'].lower() for f in findings(result,state='WARNING')))

    def test_units_of_production_does_not_require_unused_year_life(self):
        case=source_case();row=case['assets'][0];row.pop('remaining_life')
        row.update(method='units_of_production',remaining_units='1000',period_units='250')
        result=run(case=case)
        self.assertEqual(result['calculations']['depreciation'],Decimal('90000'))

    def test_no_norm_is_not_a_pass(self):
        result = run()
        self.assertTrue(findings(result,'qualified_outliers','NOT_PERFORMED'))
        self.assertFalse(findings(result,'qualified_outliers','PASS'))
        self.assertTrue(findings(result,'gl_reconciliation','NOT_PERFORMED'))
        self.assertEqual(result['accounting_determination'],'SUPPORTED')

    def test_qualified_outlier_warns_without_substituting_life(self):
        case = source_case(); case['assets'][0].update({'class':'lathes','remaining_life':'40'})
        case['class_norms'] = {'lathes':dict(entity=case['entity'],framework='IFRS',
            effective_from='2026-01-01',effective_to='2026-12-31',basis='company engineering register',
            version='v1',ranges={'remaining_life':{'min':'2','max':'10'}})}
        result = run(case=case)
        self.assertEqual(result['calculations']['depreciation'], Decimal('9000'))
        self.assertTrue(findings(result,'qualified_outliers','WARNING'))

    def test_stale_optional_asset_norm_does_not_displace_supported_life(self):
        case=source_case();case['assets'][0]['class']='lathes'
        case['class_norms']={'lathes':dict(entity=case['entity'],framework='IFRS',
            effective_from='2025-01-01',effective_to='2025-12-31',basis='historical engineering register',
            version='old',ranges={'remaining_life':{'min':'2','max':'10'}})}
        result=run(case=case)
        self.assertEqual(result['calculations']['depreciation'],Decimal('90000'))
        self.assertEqual(result['accounting_determination'],'SUPPORTED')
        self.assertTrue(findings(result,'qualified_outliers','NOT_PERFORMED'))
        self.assertFalse(findings(result,'qualified_outliers','PASS'))

    def test_malformed_optional_norm_range_does_not_block_good_asset(self):
        case=source_case();case['assets'][0]['class']='lathes'
        case['class_norms']={'lathes':dict(entity=case['entity'],framework='IFRS',
            effective_from='2026-01-01',effective_to='2026-12-31',basis='company range register',
            version='v1',ranges={'remaining_life':{'min':'10','max':'2'}})}
        result=run(case=case)
        self.assertEqual(result['calculations']['depreciation'],Decimal('90000'))
        self.assertTrue(findings(result,'qualified_outliers','NOT_PERFORMED'))
        self.assertFalse(findings(result,'qualified_outliers','PASS'))

    def test_stale_optional_invoice_norm_preserves_supported_invoice(self):
        case=source_case('accounts-payable');case['invoices'][0]['class']='supplies'
        case['class_norms']={'supplies':dict(entity=case['entity'],framework='IFRS',
            effective_from='2025-01-01',effective_to='2025-12-31',basis='historical procurement range',
            version='old',ranges={'amount':{'min':'10','max':'1000'}})}
        result=run('accounts-payable',case)
        self.assertEqual(result['calculations']['invoices'],Decimal('120'))
        self.assertTrue(findings(result,'qualified_outliers','NOT_PERFORMED'))

    def test_training_general_overhead_abnormal_waste_expensed(self):
        case = source_case(); case['costs'] = [dict(id=kind,kind=kind,amount='100',
            account=kind+' expense',offset='accounts payable',date='2026-03-01')
            for kind in ('training','general_overhead','abnormal_waste')]
        result = run(case=case)
        self.assertEqual(result['calculations']['excluded_expense'], Decimal('300'))
        self.assertEqual(result['calculations']['closing_cost'], Decimal('600000'))
        self.assertTrue(findings(result,'classification','PASS'))

    def test_capital_cost_specialist_facts_cannot_disappear_at_destination(self):
        case=source_case();case['assets'][0].update(opening_cost='0',opening_accumulated='0',
            residual='0',remaining_life='5',ready_date='2026-01-01')
        case['costs']=[dict(id='leased-equipment',kind='purchase',amount='10000',
            date='2026-01-01',destination='lathe-1',offset='accounts payable',lease_like=True)]
        result=run(case=case)
        self.assertEqual(result['calculations']['assets'],[])
        self.assertEqual(result['proposed_journal_workpaper'],[])
        self.assertTrue(findings(result,'leases','BLOCKED'))

    def test_unsupported_asset_destination_cannot_receive_ppe_proposal(self):
        case=source_case();case['assets'][0].update(opening_cost='0',opening_accumulated='0',
            residual='0',remaining_life='5',ready_date='2026-01-01',scope='software')
        case['costs']=[dict(id='software-purchase',kind='purchase',amount='10000',
            date='2026-01-01',destination='lathe-1',offset='accounts payable')]
        result=run(case=case)
        self.assertEqual(result['calculations']['assets'],[])
        self.assertFalse(any(line['account']=='PPE cost' for entry in result['proposed_journal_workpaper'] for line in entry))

    def test_capitalization_threshold_uses_asset_cost_not_individual_invoice_lines(self):
        case=source_case();case['assets'][0].update(opening_cost='0',opening_accumulated='0',
            residual='0',remaining_life='5',ready_date='2026-01-01',capitalization_threshold='12000')
        case['costs']=[dict(id='purchase',kind='purchase',amount='10000',
            date='2026-01-01',destination='lathe-1',offset='accounts payable',
            capitalization_threshold='12000',account='equipment expense'),
            dict(id='freight',kind='freight',amount='6000',date='2026-01-01',
            destination='lathe-1',offset='accounts payable',capitalization_threshold='12000',account='freight expense')]
        result=run(case=case)
        self.assertEqual(result['calculations']['closing_cost'],Decimal('16000'))
        self.assertEqual(result['calculations']['depreciation'],Decimal('3200'))
        self.assertEqual(result['calculations']['excluded_expense'],Decimal(0))

    def test_new_below_threshold_unit_is_supported_expense_without_unused_life(self):
        case=source_case();row=case['assets'][0]
        row.update(opening_cost='0',opening_accumulated='0',residual='0',
            ready_date='2026-01-01',capitalization_threshold='5000')
        row.pop('remaining_life')
        case['costs']=[dict(id='small-equipment',kind='purchase',amount='1000',
            date='2026-01-01',destination='lathe-1',offset='accounts payable',
            capitalization_threshold='5000',account='equipment expense')]
        result=run(case=case)
        self.assertEqual(result['calculations']['excluded_expense'],Decimal('1000'))
        self.assertEqual(result['calculations']['closing_cost'],Decimal(0))
        self.assertEqual(result['calculations']['depreciation'],Decimal(0))
        self.assertEqual(result['accounting_determination'],'SUPPORTED')

    def test_destination_class_threshold_is_supplied_once_for_linked_cost(self):
        case=source_case();row=case['assets'][0]
        row.update(opening_cost='0',opening_accumulated='0',residual='0',
            ready_date='2026-01-01',**{'class':'small-equipment'})
        case['class_assumptions']={'small-equipment':dict(entity=case['entity'],framework='IFRS',
            effective_from='2026-01-01',effective_to='2026-12-31',policy_version='threshold-v1',
            capitalization_threshold='5000')}
        case['costs']=[dict(id='small-purchase',kind='purchase',amount='1000',
            date='2026-01-01',destination='lathe-1',offset='accounts payable',account='equipment expense')]
        result=run(case=case)
        self.assertEqual(result['calculations']['excluded_expense'],Decimal('1000'))
        self.assertEqual(result['calculations']['closing_cost'],Decimal(0))
        self.assertEqual(result['calculations']['depreciation'],Decimal(0))
        self.assertEqual(result['accounting_determination'],'SUPPORTED')

    def test_destination_readiness_or_scope_blocks_related_capital_proposal(self):
        for invalid in ({'ready_date':'2027-01-01'},{'currency':'USD'},{'entity':'Other BV'}):
            with self.subTest(invalid=invalid):
                case=source_case();case['assets'][0].update(dict(opening_cost='0',opening_accumulated='0',
                    residual='0',remaining_life='5',ready_date='2026-01-01'))
                case['assets'][0].update(invalid)
                case['costs']=[dict(id='purchase',kind='purchase',amount='10000',
                    date='2026-01-01',destination='lathe-1',offset='accounts payable')]
                result=run(case=case)
                self.assertEqual(result['calculations']['assets'],[])
                self.assertFalse(any(line['account']=='PPE cost' for entry in result['proposed_journal_workpaper'] for line in entry))

    def test_all_blocked_assets_have_no_supported_financial_aggregates(self):
        case=source_case();case['assets'][0]['remaining_life']='0'
        result=run(case=case)
        self.assertEqual(result['calculations']['assets'],[])
        for unsupported in ('depreciation','closing_cost','closing_accumulated'):
            self.assertNotIn(unsupported,result['calculations'])
        self.assertEqual(to_public(result)['calculations'],[])
        zero=source_case();zero['assets'][0]['residual']='500000'
        supported=run(case=zero)
        self.assertEqual(supported['calculations']['depreciation'],Decimal(0))
        self.assertEqual(supported['accounting_determination'],'SUPPORTED')

    def test_plain_invoice_listing_does_not_invent_opening_or_payment_balances(self):
        result = run('accounts-payable')
        self.assertEqual(result['calculations']['invoices'], Decimal('120'))
        self.assertNotIn('closing_ap', result['calculations'])
        self.assertNotIn('opening_ap', result['calculations'])
        self.assertNotIn('payments', result['calculations'])

    def test_invoice_only_source_does_not_invent_zero_accrual_population(self):
        result=run('accounts-payable')
        self.assertNotIn('closing_accruals',result['calculations'])
        self.assertFalse(any(row['label']=='closing accruals' for row in to_public(result)['calculations']))

    def test_invoice_duplicate_normalization_is_selective(self):
        case = source_case('accounts-payable'); row=case['invoices'][0]
        case['invoices'] += [{**row,'id':'duplicate','supplier':' METALWORK ', 'invoice_number':' mw-102 '},
                             {**row,'id':'valid','invoice_number':'MW-103'}]
        result=run('accounts-payable',case)
        self.assertEqual(result['calculations']['invoices'],Decimal('120'))
        self.assertEqual([x['id'] for x in result['calculations']['invoice_rows']],['valid'])
        self.assertEqual(len(findings(result,'duplicate_invoices','BLOCKED')),2)

    def test_invoice_currency_and_arithmetic_errors_are_selective(self):
        case=source_case('accounts-payable'); row=case['invoices'][0]
        case['invoices'] += [{**row,'id':'wrong-currency','invoice_number':'MW-103','currency':'USD'},
                             {**row,'id':'wrong-arithmetic','invoice_number':'MW-104','amount':'130'}]
        result=run('accounts-payable',case)
        self.assertEqual(result['calculations']['invoices'],Decimal('120'))
        self.assertTrue(findings(result,'currency','BLOCKED'))
        self.assertTrue(findings(result,'arithmetic','BLOCKED'))

    def test_future_receipt_blocks_current_invoice_recognition(self):
        case=source_case('accounts-payable');case['invoices'][0]['received_date']='2027-01-01'
        result=run('accounts-payable',case)
        self.assertEqual(result['calculations']['invoice_rows'],[])
        self.assertTrue(findings(result,'cutoff','BLOCKED'))

    def test_received_basis_requires_receipt_date_to_resolve_cutoff(self):
        case=source_case('accounts-payable');case['invoices'][0].pop('received_date')
        result=run('accounts-payable',case)
        self.assertEqual(result['calculations']['invoice_rows'],[])
        self.assertEqual(result['accounting_determination'],'UNRESOLVED')

    def test_prior_period_receipt_needs_opening_or_accrual_route(self):
        case=source_case('accounts-payable');case['invoices'][0]['received_date']='2025-12-31'
        result=run('accounts-payable',case)
        self.assertEqual(result['calculations']['invoice_rows'],[])

    def test_gl_mismatch_preserves_supported_rows_without_reconciliation_claim(self):
        case=source_case('accounts-payable');case.update(opening_ap_total='100',payments_total='20',gl={'closing_ap':'999'})
        result=run('accounts-payable',case)
        self.assertEqual(result['calculations']['closing_ap'],Decimal('200'))
        self.assertTrue(findings(result,'gl_reconciliation','WARNING'))
        self.assertEqual(result['anomaly_report']['population_status'],'UNRECONCILED')

    def test_control_total_mismatch_does_not_block_row_calculation(self):
        case=source_case();case['control_totals']={'record_count':2,'amount':'999999'}
        result=run(case=case)
        self.assertEqual(result['calculations']['depreciation'],Decimal('90000'))
        self.assertEqual(result['anomaly_report']['population_status'],'UNRECONCILED')
        self.assertTrue(findings(result,'control_totals','WARNING'))

    def test_invalid_control_amount_preserves_valid_row_economics(self):
        case=source_case();case['control_totals']={'record_count':1,'amount':'unavailable'}
        result=run(case=case)
        self.assertEqual(result['calculations']['depreciation'],Decimal('90000'))
        self.assertEqual(result['anomaly_report']['population_status'],'UNRECONCILED')

    def test_invalid_gl_value_preserves_valid_row_economics(self):
        case=source_case();case['gl']={'closing_cost':'unavailable'}
        result=run(case=case)
        self.assertEqual(result['calculations']['depreciation'],Decimal('90000'))
        self.assertEqual(result['anomaly_report']['population_status'],'UNRECONCILED')

    def test_supplier_aggregate_difference_is_reported_without_replacing_ap(self):
        case=source_case('accounts-payable')
        case.update(opening_ap_total='100',payments_total='20',supplier_balances=[{'id':'Metalwork','balance':'199'}])
        result=run('accounts-payable',case)
        self.assertEqual(result['calculations']['closing_ap'],Decimal('200'))
        self.assertTrue(findings(result,'supplier_reconciliation','WARNING'))
        self.assertEqual(result['anomaly_report']['population_status'],'UNRECONCILED')

    def test_accrual_quantity_rate_economics(self):
        case=source_case('accounts-payable');case['invoices']=[]
        case['accruals']=[dict(id='service-accrual',supplier='Advisory',units='12',rate='800',
            received_date='2026-12-31',received_supported=True,invoiced_received='0',
            account='professional services expense',recognition_basis='services_received')]
        result=run('accounts-payable',case)
        self.assertEqual(result['calculations']['closing_accruals'],Decimal('9600'))

    def test_missing_opening_accrual_preserves_closing_but_does_not_invent_adjustment(self):
        case=source_case('accounts-payable');case['invoices']=[]
        case['accruals']=[dict(id='service-accrual',supplier='Advisory',units='12',rate='800',
            received_date='2026-12-31',received_supported=True,invoiced_received='0',
            account='professional services expense',recognition_basis='services_received')]
        result=run('accounts-payable',case)
        self.assertEqual(result['calculations']['closing_accruals'],Decimal('9600'))
        self.assertEqual(result['proposed_journal_workpaper'],[])
        self.assertNotIn('opening_accrual',result['calculations']['accrual_rows'][0])
        self.assertTrue(findings(result,'roll_forward','NOT_PERFORMED'))

    def test_accrual_specialist_indicator_remains_unresolved(self):
        case=source_case('accounts-payable');case['invoices']=[]
        case['accruals']=[dict(id='financing-accrual',supplier='Financier',units='12',rate='800',
            received_date='2026-12-31',received_supported=True,invoiced_received='0',
            account='professional services expense',recognition_basis='services_received',supplier_financing=True)]
        result=run('accounts-payable',case)
        self.assertEqual(result['calculations']['accrual_rows'],[])
        self.assertEqual(result['accounting_determination'],'UNRESOLVED')

    def test_known_opening_accrual_never_generates_duplicate_full_obligation(self):
        case=source_case('accounts-payable');case['invoices']=[]
        case['accruals']=[dict(id='service-accrual',supplier='Advisory',units='12',rate='800',
            received_date='2026-12-31',received_supported=True,invoiced_received='0',
            account='professional services expense',recognition_basis='services_received',opening_accrual='9000')]
        result=run('accounts-payable',case)
        # Either a supported 600 adjustment or a precise unsupported-movement
        # refusal is safe; adding 9600 to the known 9000 liability is unsafe.
        if result['calculations']['accrual_rows']:
            net=sum((line['amount'] if line['side']=='Cr' else -line['amount']
                for entry in result['proposed_journal_workpaper'] for line in entry
                if line['account']=='accrued expenses'),Decimal(0))
            self.assertEqual(net,Decimal('600'))
        else:self.assertEqual(result['accounting_determination'],'UNRESOLVED')

    def test_recognizable_lease_description_cannot_silently_take_ppe_route(self):
        case=source_case();case['assets'][0]['description']='Leased machine under a finance lease'
        result=run(case=case)
        self.assertEqual(result['calculations']['assets'],[])
        self.assertTrue(findings(result,'leases','BLOCKED'))

    def test_invoice_accrual_overlap_requires_explicit_resolution(self):
        case=source_case('accounts-payable')
        case['accruals']=[dict(id='overlap',supplier='Metalwork',units='12',rate='10',
            received_date='2026-12-31',received_supported=True,invoiced_received='0',
            account='consumables expense',recognition_basis='goods_received')]
        result=run('accounts-payable',case)
        self.assertEqual(result['calculations']['invoices'],Decimal('120'))
        self.assertEqual(result['calculations']['accrual_rows'],[])

    def test_framework_period_scope_remains_bounded(self):
        for framework in ('IFRS','US_GAAP','UK_GAAP','AASB'):
            with self.subTest(framework=framework):
                self.assertEqual(run(case=source_case(framework=framework))['calculations']['depreciation'],Decimal('90000'))
        case=source_case();case.update(period_start='2027-01-01',reporting_period='2027-12-31')
        self.assertEqual(run(case=case)['status'],'blocked')

    def test_provenance_keeps_client_assertion_separate_from_review(self):
        result=run()
        self.assertEqual(result['review_provenance'],'SYSTEM_PREPARED')
        self.assertEqual(result['source_provenance'],'USER_PROVIDED_SOURCES')
        self.assertEqual(result['source_assertion']['origin'],'CLIENT_ASSERTION_NOT_INDEPENDENT_CERTIFICATION')
        public=json.dumps(to_public(result))
        for private in ('private-user-92831','a'*64,'authenticated_user_reference','reviewer_signoff'):
            self.assertNotIn(private,public)
        self.assertNotIn('consult a qualified accountant',public.lower())
        self.assertIn('Nally calculated',public)

    def test_public_actual_row_assumptions_override_disclosed_class_defaults(self):
        case=source_case();case['assets'][0].update({'class':'lathes','remaining_life':'5'})
        case['class_assumptions']={'lathes':dict(entity=case['entity'],framework='IFRS',
            effective_from='2026-01-01',effective_to='2026-12-31',policy_version='v1',
            remaining_life='10',reviewer='Private assumption reviewer')}
        assumption='The supplied five-year remaining life reflects the current engineering plan.'
        case['assumptions']=[assumption]
        result=run(case=case);public=to_public(result);guidance=public['guidance']
        self.assertEqual(result['calculations']['depreciation'],Decimal('72000'))
        self.assertIn('"remaining_life": "5"',guidance)
        self.assertIn('assets:1',guidance)
        self.assertIn(assumption,guidance)
        self.assertNotIn('Private assumption reviewer',json.dumps(public))

    def test_execution_review_records_cannot_be_injected(self):
        for key in ('knowledge_review','applicability_review','reviewer_signoff'):
            case=source_case();case['assets'][0][key]={'reviewer':'Injected reviewer'}
            with self.subTest(key=key),self.assertRaises(ReviewRequired):run(case=case)

    def test_host_switches_must_both_be_enabled(self):
        for enabled in ({},{'allow_prepared_unreviewed':True},{'allow_presumed_user_sources':True}):
            with self.subTest(enabled=enabled),self.assertRaises(ReviewRequired):
                execute('fixed-assets',source_case(),**enabled)


if __name__=='__main__':unittest.main()
