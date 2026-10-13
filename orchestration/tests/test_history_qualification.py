"""Adversarial checks of identity-only synthetic history qualification."""
import json
import unittest
from pathlib import Path
from orchestration.history_references import ROOT, reference_path, prior_reference_path
from orchestration import history_transition as REVIEW


class HistoryQualification(unittest.TestCase):
    def test_amount_change_is_not_a_hash_migration(self):
        review = REVIEW.Transition()
        review.compare({'amount': '1800'}, {'amount': '1801'})
        self.assertTrue(review.errors)

    def test_64_digit_amount_cannot_masquerade_as_digest(self):
        review = REVIEW.Transition()
        review.compare({'amount': '1'*64}, {'amount': '2'*64})
        self.assertTrue(review.errors)

    def test_receipt_cannot_substitute_equal_amount_wrong_version(self):
        review = REVIEW.Transition()
        review.bind('a'*64, 'b'*64, 'native version anchor')
        review.compare({'result_version': 'version:'+'a'*64, 'value': '18'},
                       {'result_version': 'version:'+'c'*64, 'value': '18'})
        self.assertTrue(review.errors)

    def test_single_old_identity_cannot_split(self):
        review = REVIEW.Transition()
        review.bind('a'*64, 'b'*64, 'first source')
        review.bind('a'*64, 'c'*64, 'second source')
        self.assertTrue(review.errors)

    def test_distinct_old_identities_cannot_collapse(self):
        review = REVIEW.Transition()
        review.bind('a'*64, 'b'*64, 'first source')
        review.bind('c'*64, 'b'*64, 'second source')
        self.assertTrue(review.errors)

    def test_population_and_accounting_status_changes_rejected(self):
        for old, current in [({'sources': ['a', 'b']}, {'sources': ['a']}),
                             ({'status': 'blocked'}, {'status': 'complete'})]:
            review = REVIEW.Transition()
            review.compare(old, current)
            self.assertTrue(review.errors)

    def test_declared_version_inventory_sorting_preserves_exact_members(self):
        review = REVIEW.Transition()
        review.bind('a'*64, 'c'*64, 'first native result')
        review.bind('b'*64, 'a'*64, 'second native result')
        review.compare({'result_versions': ['version:'+'a'*64, 'version:'+'b'*64]},
                       {'result_versions': ['version:'+'a'*64, 'version:'+'c'*64]})
        review.finish()
        self.assertFalse(review.errors)

    def test_recorded_orchestration_transition_reperforms(self):
        manifest = json.loads((ROOT/'recovery/borrowing-costs-pr42/orchestration-migration.json').read_text())
        pairs = [(name, REVIEW.expand(json.loads((ROOT/name).read_text())),
                  REVIEW.expand(json.loads(prior_reference_path(name).read_text())))
                 for name in manifest['files']]
        review = REVIEW.Transition()
        review.stable = set(REVIEW.HEX.findall(json.dumps([a for _, a, _ in pairs]))) & set(REVIEW.HEX.findall(json.dumps([b for _, _, b in pairs])))
        for name, old, current in pairs:
            review.seed(old, current, name)
        review.phase = 'bundles'
        for name, old, current in pairs:
            review.seed(old, current, name)
        for name, old, current in pairs:
            review.compare(old, current, name)
        review.finish()
        self.assertFalse(review.errors, str(review.errors[:5]))
