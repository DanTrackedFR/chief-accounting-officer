"""Certification dependency isolation and fail-closed legacy coverage."""
import copy
import unittest
from pathlib import Path
from unittest.mock import patch
from cases import revenue
from production import ROOT, PACKAGES, case_fingerprint, assess_case
from implementation_scope import fingerprint_files, owners


class ImplementationScope(unittest.TestCase):
    def setUp(self):
        self.case = revenue()

    def changed(self, relative):
        original = Path.read_bytes
        target = ROOT / relative
        def read(path):
            value = original(path)
            return value + b'\n# independently simulated mutation' if path == target else value
        with patch.object(Path, 'read_bytes', read):
            return case_fingerprint(self.case)

    def test_other_owner_workflow_does_not_invalidate_revenue(self):
        self.assertEqual(case_fingerprint(self.case), self.changed('skills/borrowing-costs/workflow.py'))

    def test_owner_workflow_invalidates(self):
        self.assertNotEqual(case_fingerprint(self.case), self.changed('skills/revenue-recognition/workflow.py'))

    def test_owner_engine_invalidates(self):
        self.assertNotEqual(case_fingerprint(self.case), self.changed('skills/revenue-recognition/engine.py'))

    def test_shared_boundary_invalidates(self):
        self.assertNotEqual(case_fingerprint(self.case), self.changed('skills/production.py'))

    def test_case_changes_invalidate(self):
        altered = copy.deepcopy(self.case)
        altered['price_components']['fixed'] = '999'
        self.assertNotEqual(case_fingerprint(self.case), case_fingerprint(altered))

    def test_signoff_cannot_change_identity(self):
        altered = copy.deepcopy(self.case)
        altered['reviewer_signoff'] = {'approved': False}
        self.assertEqual(case_fingerprint(self.case), case_fingerprint(altered))

    def test_legacy_unknown_binds_all_owners(self):
        self.assertEqual(set(PACKAGES), set(owners({}, PACKAGES)))
        self.assertIn(ROOT/'skills/borrowing-costs/workflow.py', fingerprint_files({}, ROOT, PACKAGES))

    def test_ambiguous_topics_bind_both_owners(self):
        case = {'knowledge_review': {'documents': [{'topic_id': 'TOPIC-08-007'}]}}
        self.assertEqual(['alternative-performance-measures', 'earnings-per-share'], owners(case, PACKAGES))

    def test_borrowing_scope_has_helpers_and_supplement(self):
        files = fingerprint_files({'package': 'borrowing-costs'}, ROOT, PACKAGES)
        for name in ('skills/advanced_accounting.py', 'skills/financing_accounting.py',
                     'skills/borrowing_knowledge.py', 'knowledge/borrowing-costs/retrieval.py'):
            self.assertIn(ROOT/name, files)

    def test_forged_owner_cannot_certify_another_workflow(self):
        altered = copy.deepcopy(self.case)
        altered['package'] = 'inventory-cost'
        altered['reviewer_signoff']['case_fingerprint'] = case_fingerprint(altered)
        result = assess_case('revenue-recognition', altered)
        self.assertEqual('blocked', result['status'])
        self.assertFalse(result['journal_entry_implications'])
