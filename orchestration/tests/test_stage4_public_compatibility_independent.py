"""Independent inherited blocked-public compatibility regressions.

These assert required behavior directly; no expected failure or bypass.
"""
import sys
import unittest
from pathlib import Path
sys.path[:0] = [str(Path(__file__).resolve().parents[2] / 'skills'),
               str(Path(__file__).resolve().parents[2] / 'skills/tests')]
from production import assess_case, to_public
from agriculture_cases import case, ready, PACKAGE
from interfaces.public_output import ROUTES, public_record


class IndependentPublicCompatibility(unittest.TestCase):
    def test_missing_native_identity_is_curated_without_losing_blocked_reason(self):
        for framework in ('IFRS','US_GAAP','UK_GAAP','AASB'):
            result = assess_case('income-taxes', {'framework':framework,'reviewer_signoff':{'approved':True}})
            self.assertEqual(result['status'], 'blocked')
            for route in ROUTES:
                with self.subTest(framework=framework, route=route):
                    public = to_public(result, route)
                    self.assertEqual(public['citations'], [])
                    self.assertIn('Missing required facts', public['guidance'])
                    self.assertTrue(public['uncertainties'])
                    self.assertNotIn('case_id', str(public))
                    self.assertNotIn('reviewer_signoff', str(public))

    def test_unsupported_agriculture_dependency_remains_publicly_blocked(self):
        source = ready(c=case('IFRS','livestock'), release=True)
        source.pop('reviewer_signoff')
        source['classification']['post_harvest_accounting'] = True
        result = assess_case(PACKAGE, source)
        self.assertEqual(result['status'], 'blocked')
        for route in ROUTES:
            with self.subTest(route=route):
                public = to_public(result, route)
                self.assertIn('Unsupported Agriculture', public['guidance'])
                self.assertIn('post_harvest_accounting', str(public['uncertainties']))
                self.assertTrue(public['limitations'])

    def test_natural_dependency_caveat_is_not_an_internal_identifier(self):
        caveat = 'Outstanding dependency: obtain separately reviewed harvest-cost evidence.'
        for route in ROUTES:
            with self.subTest(route=route):
                result = public_record({'guidance':'Accounting remains blocked.','limitations':[caveat]}, route=route)
                self.assertEqual(result['limitations'], [caveat])

    def test_actual_internal_dependency_identifiers_still_fail_closed(self):
        for token in ('dependency_id', 'case_id', 'result_version', 'source_fingerprint', 'reviewer_signoff'):
            with self.subTest(token=token):
                with self.assertRaises(ValueError):
                    public_record({'guidance':'Internal '+token+' details'}, route='answer')

    def test_concrete_typed_identifiers_still_fail_closed_every_route(self):
        for prefix in ('exec','version','period','case','dependency','ic-side','ic-relationship','fingerprint'):
            for route in ROUTES:
                with self.subTest(prefix=prefix, route=route):
                    with self.assertRaises(ValueError):
                        public_record({'limitations':['Blocked by '+prefix+':secret']}, route=route)

    def test_whitespace_cannot_hide_other_internal_tokens_or_hashes(self):
        for token in ('dependency: case_id', 'dependency:\tresult_version',
                      'dependency:\nsource_fingerprint', ' Source \t: internal note',
                      'dependency: '+('a'*64), 'reviewer_signoff', 'approval_track',
                      'ChatGPT training data', 'source_note'):
            for route in ROUTES:
                with self.subTest(token=token, route=route):
                    with self.assertRaises(ValueError):
                        public_record({'guidance':'Blocked.','uncertainties':[token]}, route=route)

    def test_adapter_does_not_curate_arbitrary_contaminated_reason(self):
        result = assess_case('income-taxes', {'framework':'IFRS','reviewer_signoff':{'approved':True}})
        result['conclusion'] = 'Unreviewed case_id cannot be disclosed'
        with self.assertRaises(ValueError): to_public(result)

    def test_adapter_does_not_drop_unknown_missing_fact_provenance(self):
        result = assess_case('income-taxes', {'framework':'IFRS','reviewer_signoff':{'approved':True}})
        result['conclusion'] = 'Accounting case cannot be completed: Missing required facts: source_note'
        with self.assertRaises(ValueError): to_public(result)

    def test_missing_fact_curation_preserves_every_substantive_requirement(self):
        result = assess_case('income-taxes', {'framework':'IFRS','reviewer_signoff':{'approved':True}})
        required = 'Missing required facts: case_id, node_id, period_id, result_version, dependency_id, source_fingerprint, reviewer_signoff, entity, jurisdiction'
        result['conclusion'] = 'Accounting case cannot be completed: '+required
        result['uncertainties'] = [required]
        result['open_items'] = [required]
        public = to_public(result)
        expected = 'Missing required facts: accounting case identity, accounting execution identity, governed accounting period, current accounting result, qualified accounting dependency, qualified source identity, independent accounting review, entity, jurisdiction'
        self.assertEqual(public['limitations'], [expected])
        self.assertEqual(public['uncertainties'], [expected])
        self.assertIn(expected, public['guidance'])
