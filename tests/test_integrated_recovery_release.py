"""Verify both immutable baselines and current integrated synthetic proofs."""
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT/'recovery/borrowing-costs-pr42'
SPEC = importlib.util.spec_from_file_location('integrated_identity_review', HERE/'check_identity_transition.py')
REVIEW = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REVIEW)


class IntegratedRecoveryRelease(unittest.TestCase):
    def test_original_pr_examples_are_immutable(self):
        baseline = json.loads((HERE/'published-head-manifest.json').read_text())['files']
        for name, checksum in baseline.items():
            if '/examples/' in name:
                self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(), checksum, name)

    def test_main_historical_authorities_and_pr_versions_are_preserved(self):
        manifest = json.loads((HERE/'main-historical-preservation.json').read_text())
        main = json.loads((ROOT/'build4/release/historical-inventory.json').read_text())['files']
        original = json.loads((HERE/'published-head-manifest.json').read_text())['files']
        review = REVIEW.Transition()
        for name, record in manifest['files'].items():
            old = ROOT/record['main_original_path']
            self.assertTrue(old.resolve().is_relative_to(HERE/'main-original'))
            self.assertEqual(hashlib.sha256(old.read_bytes()).hexdigest(), main[name])
            self.assertEqual(record['pr42_original_sha256'], original[name])
            current = ROOT/name
            self.assertEqual(hashlib.sha256(current.read_bytes()).hexdigest(), original[name])
            review.compare(REVIEW.expand(json.loads(old.read_bytes())), REVIEW.expand(json.loads(current.read_bytes())), name)
        self.assertFalse(review.errors, str(review.errors[:3]))

    def test_current_integrated_proofs_change_only_consistent_identities(self):
        manifest = json.loads((HERE/'main-proof-migration.json').read_text())
        review = REVIEW.Transition()
        pairs = []
        for name, record in manifest['files'].items():
            old = ROOT/name
            current = ROOT/record['current_path']
            self.assertTrue(current.resolve().is_relative_to(HERE/'integration-fresh'))
            self.assertEqual(hashlib.sha256(old.read_bytes()).hexdigest(), record['original_sha256'])
            self.assertEqual(hashlib.sha256(current.read_bytes()).hexdigest(), record['current_sha256'])
            pairs.append((name, REVIEW.expand(json.loads(old.read_bytes())), REVIEW.expand(json.loads(current.read_bytes()))))
        # Anchor all native versions before inspecting hash-keyed receipt maps.
        # Set iteration order must never decide whether an authority is known.
        for phase in ('versions', 'bundles'):
            review.phase = phase
            for name, old, current in pairs:
                review.seed(old, current, name)
        for name, old, current in pairs:
            review.compare(old, current, name)
        self.assertFalse(review.errors, str(review.errors[:3]))


if __name__ == '__main__':
    unittest.main()
