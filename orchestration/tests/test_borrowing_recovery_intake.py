"""Adversarial source-intake probes for PR42 recovery."""
import copy
import unittest
from orchestration.runtime import CAO
from orchestration.tests.fixtures import manufacturing


class MissingOwnerEvidence(unittest.TestCase):
    def test_missing_workpaper_retains_owner_and_completed_work(self):
        request = manufacturing()
        request['facts']['qualifying_interest'] = {'project': 'factory', 'required_for_objective': False}
        original = copy.deepcopy(request)
        result = CAO().run(request)
        self.assertEqual(request, original)
        self.assertEqual(result.outcome, 'partial')
        node = result.graph.nodes['borrowing-costs']
        self.assertEqual(node.status, 'blocked')
        self.assertIsNone(node.result)
        self.assertTrue(any('Missing reviewed source' in item for item in node.open_items))
        self.assertEqual(result.graph.nodes['inventory-cost'].status, 'complete')

    def test_explicit_unknown_scope_is_never_defaulted(self):
        request = manufacturing()
        request['facts']['qualifying_interest'] = {'project': 'factory', 'entity': 'Unregistered company'}
        result = CAO().run(request)
        self.assertEqual(result.outcome, 'blocked')
        self.assertTrue(any('Owner outside registered Scopes' in row['question'] for row in result.open_questions))

    def test_explicit_scope_without_entity_is_never_certified(self):
        request = manufacturing()
        request['facts']['qualifying_interest'] = {'project': 'factory', 'scope_id': request['scope']['entity']}
        result = CAO().run(request)
        self.assertEqual(result.outcome, 'blocked')
        self.assertTrue(any('Owner entity differs' in row['question'] for row in result.open_questions))
