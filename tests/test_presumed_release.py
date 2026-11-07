"""Independent acceptance-population and historical-preservation adversarial QA.

The established independent 17-suite/10-validator assertions are reused against
the original 17 slots, extended here by five mandatory remediation slots. All history
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


REMEDIATION = [
    ('diagnostics/profile12', 'regressions.py'),
    ('diagnostics/profile12', 'governance.py'),
    ('diagnostics/profile12/remediation/accounting-qa', 'test_accounting_qa.py'),
    ('diagnostics/profile12/remediation/engineering-qa', 'test_boundaries.py'),
    ('diagnostics/profile12/remediation/engineering-qa', 'test_governance.py'),
]
ORIGINAL_RECEIPT = BASELINE.receipt


def extended_receipt():
    value = ORIGINAL_RECEIPT()
    for index, (suite, pattern) in enumerate(REMEDIATION, 17):
        value['suite_results'].append(dict(suite=suite, pattern=pattern,
            distinct_ids=[suite+'::synthetic_'+str(index)+'.test_checked'], tests=1,
            errors=0, failures=0, skipped=0, passed=True, exit_code=0))
    value.update(attempt='synthetic-population', source_commit='a'*40, executed_distinct_tests=22)
    value['gate_plan'] = VERIFIER.gate_plan(value['attempt'], value['source_commit'])
    extra = [dict(command=list(slot['command']), exit_code=0, path='synthetic/log-'+str(slot['index'])+'.log', sha256='0'*64)
             for slot in value['gate_plan'][17:]]
    value['logs'][17:17] = extra
    envs = [slot['environment'] for slot in value['gate_plan']] + [{'PYTHONHASHSEED':'19'}]*10 + [{}]
    for row, env in zip(value['logs'], envs): row['environment'] = env
    return value


class IndependentPresumedReleasePopulationQA(BASELINE.IndependentPreparedReleaseQA):
    def setUp(self):
        patcher = patch.object(BASELINE, 'receipt', extended_receipt)
        patcher.start(); self.addCleanup(patcher.stop)

    def validate(self, value):
        return VERIFIER.validate_population(value)

    def test_exact_independently_pinned_release_population(self):
        self.assertEqual(list(VERIFIER.SUPPORTED_SUITES), BASELINE.EXPECTED_SUITES + REMEDIATION)
        self.assertEqual(list(VERIFIER.VALIDATOR_COMMANDS), BASELINE.EXPECTED_VALIDATORS)
        self.validate(extended_receipt())

    def test_every_remediation_slot_is_mandatory(self):
        for index in range(17, 22):
            value=extended_receipt(); value['suite_results'].pop(index)
            self.refuses(value)

    def test_governance_environment_and_plan_are_mandatory(self):
        for key in ('CAO_GOV_REF', 'CAO_GOV_FOCUSED', 'CAO_ENGINEERING_REF', 'CAO_DIAGNOSTIC_OUT'):
            value=extended_receipt(); value['logs'][18]['environment']=dict(value['logs'][18]['environment'])
            value['logs'][18]['environment'].pop(key)
            self.refuses(value)
        value=extended_receipt(); value['gate_plan'].pop(); self.refuses(value)

    def test_all_ten_validators_still_required(self):
        for index in range(22, 32):
            value=extended_receipt(); value['logs'].pop(index); self.refuses(value)


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
