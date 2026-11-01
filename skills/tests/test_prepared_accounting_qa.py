"""Independent accounting challenges for the bounded optional-review mode.

Synthetic source approvals below are historical fixture evidence, not generated
execution review or authenticated professional sign-off.
"""
import copy
import json
import sys
import unittest
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from operational_cases import operational, certified
from production import execute, to_public, case_fingerprint
from core_accounting import ReviewRequired, balance
from interfaces.public_output import ROUTES


def prepared(package='fixed-assets', framework='IFRS'):
    case = operational(package, framework)
    for key in ('knowledge_review', 'applicability_review', 'reviewer_signoff'):
        case.pop(key, None)
    # Explicit new-mode qualification tokens; source data and economics remain
    # the existing owner fixture, not generated accounting approval.
    case['policy_elections'] = {}
    if framework == 'UK_GAAP': case['uk_standard_edition'] = '2026'
    elif framework == 'AASB': case['aasb_compilation'] = '2026'
    elif framework == 'US_GAAP': case['us_entity_type'] = 'private_company'
    case['review_mode'] = 'prepared_unreviewed'
    return case


class IndependentPreparedAccountingQA(unittest.TestCase):
    def run_prepared(self, package='fixed-assets', case=None):
        return execute(package, prepared(package) if case is None else case,
                       allow_prepared_unreviewed=True)

    def blocked(self, package, case):
        with self.assertRaises(ReviewRequired):
            self.run_prepared(package, case)

    def test_independent_fixed_asset_economics(self):
        case = prepared()
        snapshot = copy.deepcopy(case)
        result = self.run_prepared(case=case)
        expected = (Decimal('600000') - Decimal('180000') - Decimal('60000')) / Decimal('4')
        self.assertEqual(result['calculations']['depreciation'], expected)
        asset = result['calculations']['assets'][0]
        self.assertEqual(asset['closing_accumulated'], Decimal('180000') + expected)
        self.assertEqual(asset['carrying'], Decimal('330000'))
        self.assertEqual(case, snapshot, 'Execution must not inject review records into source evidence')

    def test_independent_supplier_accrual_economics(self):
        result = self.run_prepared('accounts-payable')
        expected = Decimal('12') * Decimal('800')
        calc = result['calculations']
        self.assertEqual(calc['closing_accruals'], expected)
        self.assertEqual(calc['closing_ap'], Decimal('120') - Decimal('100'))
        self.assertEqual(calc['accrual_backtests'][0]['variance'], Decimal('800'))
        self.assertNotEqual(calc['closing_accruals'], Decimal('10400'),
                            'January service cost must not be silently accrued in December')

    def test_review_is_separate_from_supported_accounting(self):
        for package in ('fixed-assets', 'accounts-payable'):
            with self.subTest(package=package):
                result = self.run_prepared(package)
                self.assertEqual(result['status'], 'partial')
                self.assertEqual(result['accounting_determination'], 'SUPPORTED')
                self.assertEqual(result['evidence_sufficiency'], 'SUFFICIENT')
                self.assertEqual(result['review_provenance'], 'SYSTEM_PREPARED')
                self.assertFalse(any('reviewer must approve' in item.lower()
                                     for item in result.get('open_items', [])))
                self.assertFalse(result['journal_entry_implications'])
                self.assertTrue(result['proposed_journal_workpaper'])
                for journal in result['proposed_journal_workpaper']:
                    self.assertTrue(balance(journal))

    def test_disabled_by_default(self):
        with self.assertRaises(ReviewRequired):
            execute('fixed-assets', prepared())

    def test_reviewer_injection_cannot_upgrade(self):
        for package in ('fixed-assets', 'accounts-payable'):
            for key in ('knowledge_review', 'applicability_review', 'reviewer_signoff'):
                for injected in (None, {}, {'reviewer': 'Injected approver', 'approved': True}):
                    with self.subTest(package=package, field=key, injected=injected):
                        case = prepared(package)
                        case[key] = injected
                        self.blocked(package, case)

    def test_missing_material_evidence_blocks(self):
        for package, field in [('fixed-assets', 'evidence'), ('fixed-assets', 'judgment_memo'),
                               ('fixed-assets', 'assets'), ('fixed-assets', 'asset_inventory'),
                               ('accounts-payable', 'accruals'), ('accounts-payable', 'handoffs')]:
            with self.subTest(package=package, field=field):
                case = prepared(package)
                case.pop(field)
                self.blocked(package, case)

    def test_source_controls_remain_substantive(self):
        for package in ('fixed-assets', 'accounts-payable'):
            for key, value in [('complete', False), ('as_of', '2026-11-30'),
                               ('population_count', 999), ('population_amount', '999'),
                               ('reviewer', 'synthetic source owner')]:
                with self.subTest(package=package, field=key):
                    case = prepared(package)
                    case['controls'][key] = value
                    self.blocked(package, case)

    def test_source_row_stale_and_self_approval_block(self):
        for package, rows in [('fixed-assets', 'assets'), ('accounts-payable', 'accruals')]:
            for mutation in ('missing', 'stale', 'self', 'late', 'unapproved'):
                with self.subTest(package=package, mutation=mutation):
                    case = prepared(package)
                    row = case[rows][0]
                    if mutation == 'missing': row['evidence'] = ''
                    elif mutation == 'stale': row['approved_version'] = 'old'
                    elif mutation == 'self': row['reviewer'] = row['owner']
                    elif mutation == 'late': row['approval_date'] = '2027-01-06'
                    else: row['approved'] = False
                    self.blocked(package, case)

    def test_applicability_mismatch_and_unresolved_specialist_block(self):
        for package, key in [('fixed-assets', 'impairment'), ('accounts-payable', 'recognition')]:
            for dimension, wrong in [('entity', 'OTHER'), ('framework', 'US_GAAP'),
                                     ('reporting_period', '2025-12-31'), ('resolved', False)]:
                with self.subTest(package=package, dimension=dimension):
                    case = prepared(package)
                    case['handoffs'][key][dimension] = wrong
                    self.blocked(package, case)
            case = prepared(package)
            case['specialist_items'] = ['Unresolved material classification']
            self.blocked(package, case)

    def test_unsupported_framework_period_and_policy_block(self):
        for package in ('fixed-assets', 'accounts-payable'):
            for field, value in [('framework', 'OTHER'), ('period_start', '2027-01-01'),
                                 ('period_start', '2025-01-01'), ('reporting_period', '2027-12-31'),
                                 ('entity_type', 'not_for_profit'),
                                 ('policy_elections', {'unsupported_model': 'fair_value'})]:
                with self.subTest(package=package, field=field, value=value):
                    case = prepared(package)
                    case[field] = value
                    self.blocked(package, case)

    def test_australian_tier_and_sector_boundaries(self):
        for package in ('fixed-assets', 'accounts-payable'):
            for field, value in [('reporting_tier', 3), ('reporting_tier', True),
                                 ('entity_type', 'not_for_profit'), ('entity_type', 'public_sector'),
                                 ('aasb_compilation', 'unqualified future edition')]:
                with self.subTest(package=package, field=field, value=value):
                    case = prepared(package, 'AASB')
                    case[field] = value
                    self.blocked(package, case)

    def test_qualified_frameworks_preserve_owner_economics(self):
        for package, key, expected in [('fixed-assets', 'depreciation', Decimal('90000')),
                                       ('accounts-payable', 'closing_accruals', Decimal('9600'))]:
            for framework in ('IFRS', 'US_GAAP', 'UK_GAAP', 'AASB'):
                with self.subTest(package=package, framework=framework):
                    result = self.run_prepared(package, prepared(package, framework))
                    self.assertEqual(result['calculations'][key], expected)
                    self.assertEqual(result['accounting_determination'], 'SUPPORTED')
            tier2 = prepared(package, 'AASB')
            tier2['reporting_tier'] = 2
            self.assertEqual(self.run_prepared(package, tier2)['calculations'][key], expected)

    def test_regulated_and_public_us_routes_are_not_inferred(self):
        for package in ('fixed-assets', 'accounts-payable'):
            for value in ('public', 'insurance', 'bank', 'private_nonprofit'):
                case = prepared(package, 'US_GAAP')
                case['us_entity_type'] = value
                self.blocked(package, case)
            case = prepared(package, 'US_GAAP')
            case['regulatory_overlays'] = ['SEC registrant']
            self.blocked(package, case)

    def test_supplier_profile_is_neutral_background_without_claim_application(self):
        from production import canonical_knowledge, PACKAGES
        for framework in ('IFRS', 'US_GAAP', 'UK_GAAP', 'AASB'):
            with self.subTest(framework=framework):
                claims, documents = canonical_knowledge(PACKAGES['accounts-payable'][1], framework,
                                                        package='accounts-payable')
                snapshot = copy.deepcopy((claims, documents))
                result = self.run_prepared('accounts-payable', prepared('accounts-payable', framework))
                self.assertEqual(result['applicability_provenance']['standard_versions'],
                                 ['Governed ordinary supplier-cost reconciliation profile, 2026'])
                self.assertEqual(result['applicability_provenance']['framework'], framework)
                self.assertEqual(result['applicability_provenance']['origin'], 'SYSTEM_DERIVED')
                self.assertEqual(result['knowledge_population'], snapshot[0])
                self.assertEqual(result['knowledge_documents'], snapshot[1])
                self.assertEqual(canonical_knowledge(PACKAGES['accounts-payable'][1], framework,
                                                    package='accounts-payable'), snapshot)
                self.assertEqual(result['evidence'], [])
                self.assertNotIn('applied_claim_ids', result)
                self.assertNotIn('knowledge_review', result['facts_used'])

    def test_uk_framework_and_edition_boundaries(self):
        for package in ('fixed-assets', 'accounts-payable'):
            for field, value in [('uk_standard', 'FRS_101'), ('uk_standard', 'FRS_105'),
                                 ('uk_standard_edition', 'January2019')]:
                with self.subTest(package=package, field=field, value=value):
                    case = prepared(package, 'UK_GAAP')
                    case[field] = value
                    self.blocked(package, case)

    def test_fixed_assets_unsupported_methods_and_elections(self):
        for mutation in ('revaluation', 'unsupported_method', 'not_ready', 'software', 'no_life_review'):
            with self.subTest(mutation=mutation):
                case = prepared()
                if mutation == 'revaluation': case['asset_policy']['model'] = 'revaluation'
                elif mutation == 'unsupported_method': case['assets'][0]['method'] = 'accelerated_unspecified'
                elif mutation == 'not_ready': case['assets'][0]['ready_date'] = '2027-01-01'
                elif mutation == 'software': case['assets'][0]['scope'] = 'software'
                else: case['asset_policy']['life_review'] = False
                self.blocked('fixed-assets', case)

    def test_ap_missing_receipt_currency_cutoff_and_segregation(self):
        for mutation in ('receipt', 'future_receipt', 'future_reversal', 'currency', 'segregation'):
            with self.subTest(mutation=mutation):
                case = prepared('accounts-payable')
                if mutation == 'receipt': case['accruals'][0]['received_supported'] = False
                elif mutation == 'future_receipt': case['accruals'][0]['received_date'] = '2027-01-01'
                elif mutation == 'future_reversal': case['accruals'][0]['reversal_date'] = '2026-12-31'
                elif mutation == 'currency': case['invoices'][0]['currency'] = 'USD'
                else: case['payments'][0]['payment_releaser'] = case['payments'][0]['payment_preparer']
                self.blocked('accounts-payable', case)

    def test_public_provenance_and_citations_do_not_overstate_authority(self):
        banned = ('knowledge_documents', 'claim_ids', 'claim_register', 'reviewer_signoff',
                  'synthetic independent reviewer', 'SOURCE_VERIFIED', 'evidence_status',
                  'Source: ChatGPT', 'consult a qualified accountant', 'AI-generated accounting advice')
        for package in ('fixed-assets', 'accounts-payable'):
            result = self.run_prepared(package)
            for route in ROUTES:
                with self.subTest(package=package, route=route):
                    public = to_public(result, route=route)
                    encoded = json.dumps(public, default=str)
                    for token in banned:
                        self.assertNotIn(token, encoded)
                    self.assertIn('90000' if package == 'fixed-assets' else '9600', encoded)
                    self.assertFalse(any(c.get('locator') for c in public.get('citations', [])),
                                     'Background guidance must not manufacture claim-level application')

    def test_mode_changes_fingerprint(self):
        case = prepared()
        prepared_fingerprint = case_fingerprint(case)
        case.pop('review_mode')
        self.assertNotEqual(case_fingerprint(case), prepared_fingerprint)

    def test_public_treatment_assumptions_and_proposed_journals(self):
        for package in ('fixed-assets', 'accounts-payable'):
            case = prepared(package)
            case['assumptions'] = ['No unrecorded material amendments affect the supplied evidence.']
            public = to_public(self.run_prepared(package, case))
            encoded = json.dumps(public, default=str)
            self.assertIn(case['assumptions'][0], encoded)
            for account in (('depreciation expense', 'accumulated depreciation') if package == 'fixed-assets'
                            else ('professional services expense', 'accrued expenses')):
                self.assertIn(account, encoded)
            self.assertIn('propos', encoded.lower())
            self.assertTrue(any(word in encoded.lower() for word in
                                ('systematic', 'available for use', 'ready for use', 'received services', 'obligation')),
                            'Public accounting result must explain the relevant requirements')

    def test_formal_economics_unchanged(self):
        for package, key, expected in [('fixed-assets', 'depreciation', Decimal('90000')),
                                       ('accounts-payable', 'closing_accruals', Decimal('9600'))]:
            result = execute(package, certified(package))
            self.assertEqual(result['status'], 'complete')
            self.assertEqual(result['calculations'][key], expected)

    def test_selected_owner_must_match_immutable_case_owner(self):
        for package, wrong in [('fixed-assets', 'accounts-payable'), ('accounts-payable', 'fixed-assets')]:
            case = prepared(package)
            case['package'] = wrong
            self.blocked(package, case)

    def test_other_packages_are_not_opted_in(self):
        for package in ('month-end-close', 'revenue-recognition', 'investment-property', 'borrowing-costs'):
            self.blocked(package, prepared())

    def test_system_record_cannot_certify_formal_result(self):
        from prepared_execution import SYSTEM
        for package in ('fixed-assets', 'accounts-payable'):
            for key in ('knowledge_review', 'applicability_review', 'reviewer_signoff'):
                case = certified(package)
                case[key]['reviewer'] = SYSTEM
                if key == 'reviewer_signoff':
                    case[key]['case_fingerprint'] = case_fingerprint(case)
                with self.assertRaises(ReviewRequired):
                    execute(package, case)

    def test_unresolved_canonical_assurance_blocks(self):
        from unittest.mock import patch
        import production
        for status in ('CONFLICTED', 'NOT_RESEARCHED'):
            claims, docs = production.canonical_knowledge(production.PACKAGES['fixed-assets'][1], 'IFRS', package='fixed-assets')
            claims[0]['evidence_status'] = status
            with patch.object(production, 'canonical_knowledge', return_value=(claims, docs)):
                self.blocked('fixed-assets', prepared())

    def test_relabelled_system_records_cannot_certify_formal_result(self):
        for package in ('fixed-assets', 'accounts-payable'):
            for key in ('knowledge_review', 'applicability_review', 'reviewer_signoff'):
                for field, tag in [('provenance', 'SYSTEM_DERIVED'), ('origin', 'SYSTEM_PREPARED')]:
                    with self.subTest(package=package, record=key, field=field):
                        case = certified(package)
                        case[key]['reviewer'] = 'non-human worker'
                        case[key][field] = tag
                        # Fresh fingerprint prevents an unrelated stale-signoff
                        # refusal from masking the actual provenance gate.
                        case['reviewer_signoff']['case_fingerprint'] = case_fingerprint(case)
                        with self.assertRaisesRegex(ReviewRequired, 'System provenance'):
                            execute(package, case)

    def test_public_boundary_rejects_private_provenance_in_assumptions(self):
        for text in ('Source: ChatGPT training data', 'synthetic independent reviewer',
                     '0123456789abcdef' * 4):
            case = prepared()
            case['assumptions'] = [text]
            with self.assertRaises((ReviewRequired, ValueError)):
                self.run_prepared(case=case)

    def test_insufficient_evidence_is_unresolved_with_specific_public_issue(self):
        from production import assess_case
        for package in ('fixed-assets', 'accounts-payable'):
            case = prepared(package)
            case['evidence'] = []
            result = assess_case(package, case, allow_prepared_unreviewed=True)
            self.assertEqual(result['status'], 'blocked')
            self.assertEqual(result['accounting_determination'], 'UNRESOLVED')
            self.assertEqual(result['evidence_sufficiency'], 'INSUFFICIENT')
            self.assertFalse(result['calculations'])
            public = to_public(result)
            self.assertTrue(public['open_items'])
            self.assertIn('Evidence population', json.dumps(public))
            self.assertNotIn('90000' if package == 'fixed-assets' else '9600', json.dumps(public))

    def test_all_public_refusals_preserve_issue_without_invented_scope(self):
        from production import assess_case
        scenarios = []
        scenarios.append(('month-end-close', prepared(), 'unavailable for this accounting package'))
        scenarios.append(('investment-property', prepared(), 'unavailable for this accounting package'))
        for package in ('fixed-assets', 'accounts-payable'):
            missing = prepared(package)
            missing['evidence'] = []
            scenarios.append((package, missing, 'Evidence population'))
            future = prepared(package)
            future.update(period_start='2027-01-01', reporting_period='2027-12-31')
            scenarios.append((package, future, 'wholly within 2026'))
        for package, case, reason in scenarios:
            result = assess_case(package, case, allow_prepared_unreviewed=True)
            self.assertEqual(result['status'], 'blocked')
            self.assertFalse(result['calculations'])
            for route in ROUTES:
                with self.subTest(package=package, reason=reason, route=route):
                    public = to_public(result, route=route)
                    encoded = json.dumps(public)
                    self.assertEqual(public['accounting_determination'], 'UNRESOLVED')
                    self.assertEqual(public['evidence_sufficiency'], 'INSUFFICIENT')
                    self.assertEqual(public['review_provenance'], 'SYSTEM_PREPARED')
                    self.assertIn(reason, public['guidance'])
                    self.assertTrue(public['open_items'])
                    self.assertEqual(public.get('citations', []), [])
                    for invented in ('Qualifying ordinary machinery', 'Recognize supplier obligations',
                                     'governed knowledge package', 'background guidance',
                                     'Proposed journal implications', 'Calculations:', '90000', '9600'):
                        self.assertNotIn(invented, encoded)


if __name__ == '__main__':
    unittest.main()
