"""Independent acceptance-population and historical-preservation adversarial QA.

The established independent 17-suite/10-validator assertions are reused against
this new verifier; they remain unchanged in their original module. All history
mutation tests use synthetic isolated files, never real accounting artifacts.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec); spec.loader.exec_module(value)
    return value


BASELINE = module('presumed_release_independent_baseline_tests', ROOT/'tests/test_prepared_release.py')
VERIFIER = module('independent_presumed_source_release_verifier', ROOT/'skills/presumed-sources/verify_release.py')


class IndependentPresumedReleasePopulationQA(BASELINE.IndependentPreparedReleaseQA):
    def validate(self, value):
        return VERIFIER.validate_population(value)

    def test_exact_independently_pinned_release_population(self):
        self.assertEqual(list(VERIFIER.SUPPORTED_SUITES), BASELINE.EXPECTED_SUITES)
        self.assertEqual(list(VERIFIER.VALIDATOR_COMMANDS), BASELINE.EXPECTED_VALIDATORS)
        self.validate(BASELINE.receipt())


class IndependentPresumedHistoricalPreservationQA(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)/'repository'; self.root.mkdir()
        self.paths = {'knowledge/synthetic-history.json': b'{"historical": "original"}\n',
                      'skills/synthetic-history/release/proof.json': b'{"proof": "original"}\n'}
        for name, data in self.paths.items():
            target = self.root/name; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
        self.data = dict(baseline='7146eaeca6a28d17d9183d0f9431fd9b9663f1fe',
                         files={name: hashlib.sha256(data).hexdigest() for name, data in self.paths.items()})
        self.manifest = self.root/'skills/presumed-sources/release/historical-preservation.json'
        self.manifest.parent.mkdir(parents=True); self.write(self.data)
        self.original_hash = hashlib.sha256(self.manifest.read_bytes()).hexdigest()
        self.assertEqual(self.verify(), 2, 'Valid independent fixture must qualify before adverse mutation')

    def write(self, data):
        self.manifest.write_text(json.dumps(data, sort_keys=True, indent=2)+'\n')

    def verify(self, expected_hash=None):
        with patch.object(VERIFIER, 'ROOT', self.root), \
             patch.object(VERIFIER, 'PRESERVATION_SHA256', expected_hash or self.original_hash), \
             patch.object(VERIFIER, 'PRESERVATION_COUNT', 2):
            return VERIFIER.verify_historical()

    def test_valid_exact_manifest_and_population_are_accepted(self):
        self.assertEqual(self.verify(), 2)

    def test_manifest_byte_change_invalidates_pinned_receipt(self):
        self.manifest.write_bytes(self.manifest.read_bytes()+b'\n')
        with self.assertRaises(AssertionError): self.verify()

    def test_empty_manifest_population_cannot_pass_even_with_matching_digest(self):
        altered = copy.deepcopy(self.data); altered['files'] = {}; self.write(altered)
        changed_hash = hashlib.sha256(self.manifest.read_bytes()).hexdigest()
        with self.assertRaises(AssertionError): self.verify(changed_hash)

    def test_deleted_mapping_entry_cannot_pass_even_with_matching_digest(self):
        altered = copy.deepcopy(self.data); altered['files'].pop(next(iter(altered['files']))); self.write(altered)
        changed_hash = hashlib.sha256(self.manifest.read_bytes()).hexdigest()
        with self.assertRaises(AssertionError): self.verify(changed_hash)

    def test_deleted_original_artifact_invalidates_preservation(self):
        (self.root/next(iter(self.paths))).unlink()
        with self.assertRaises((AssertionError, FileNotFoundError)): self.verify()

    def test_changed_original_artifact_invalidates_preservation(self):
        (self.root/next(iter(self.paths))).write_bytes(b'changed historic content')
        with self.assertRaises(AssertionError): self.verify()

    def test_original_mapping_cannot_escape_repository(self):
        external = self.root.parent/'outside-proof.json'; external.write_bytes(b'outside')
        altered = copy.deepcopy(self.data)
        altered['files'].pop(next(iter(altered['files'])))
        altered['files']['../outside-proof.json'] = hashlib.sha256(external.read_bytes()).hexdigest()
        self.write(altered)
        changed_hash = hashlib.sha256(self.manifest.read_bytes()).hexdigest()
        with self.assertRaises(AssertionError): self.verify(changed_hash)

    def test_real_preservation_manifest_matches_exact_pinned_hash_and_count(self):
        manifest = ROOT/'skills/presumed-sources/release/historical-preservation.json'
        raw = manifest.read_bytes(); data = json.loads(raw)
        self.assertRegex(VERIFIER.PRESERVATION_SHA256, r'^[0-9a-f]{64}$')
        self.assertEqual(hashlib.sha256(raw).hexdigest(), VERIFIER.PRESERVATION_SHA256)
        self.assertEqual(len(data['files']), VERIFIER.PRESERVATION_COUNT)
        self.assertGreater(VERIFIER.PRESERVATION_COUNT, 8900)
        self.assertEqual(VERIFIER.verify_historical(), VERIFIER.PRESERVATION_COUNT)


if __name__ == '__main__':
    unittest.main()
