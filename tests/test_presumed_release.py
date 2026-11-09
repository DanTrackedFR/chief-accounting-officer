"""Independent acceptance-population and historical-preservation adversarial QA.

The established independent 17-suite/10-validator assertions are reused against
the original 17 slots, extended here by five mandatory remediation slots. All history
mutation tests use synthetic isolated files, never real accounting artifacts.
"""
import csv
import gzip
import subprocess
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import shutil
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
PROFILE12 = '97d0621331c6ad2a66b12ed09c0ec40c05c626b9'
PHASE_A_SUITES = [*BASELINE.EXPECTED_SUITES, *REMEDIATION,
                  ('tests/phase_a_release_infra', 'test_*.py')]
LEDGER = 'docs/phase-a/failed-regression-42466932475-1/identity-ledger.tsv.gz'
LEDGER_SHA256 = '9d05d7c782169398060fb49bab1735b731f0a337a66b9c880542af34801983df'
ADDITIONAL_ID = ('tests::test_presumed_population_dispatch.ProductionPopulationDispatch.'
                 'test_missing_outcome_dependency_refused_before_execution')
ROUTING_ID = ('tests::test_presumed_ci_evidence.IndependentCIEvidenceIsolationQA.'
              'test_event_routing_with_executed_synthetic_receipt')


def check_phase_a_inventory(inventory, commit, expected):
    if inventory['source_commit'] != commit:
        raise ValueError('Incorrect inventory source')
    rows = inventory['suite_results']
    if [(r['suite'], r['pattern']) for r in rows] != PHASE_A_SUITES:
        raise ValueError('Incorrect suite population')
    actual_total = 0
    for slot, row in enumerate(rows):
        # Production discovery publishes sorted lists and the runner compares them in order.
        identities = row['distinct_ids']
        if identities != expected[slot]:
            raise ValueError('Incorrect identities at slot ' + str(slot))
        if type(row.get('tests')) is not int or row['tests'] != len(identities):
            raise ValueError('Incorrect discovery count at slot ' + str(slot))
        actual_total += len(identities)
    reported = inventory.get('discovered_distinct_tests')
    if type(reported) is not int or reported != actual_total or actual_total != sum(map(len, expected)):
        raise ValueError('Incorrect discovered total')



FIXTURE = module('phase_a_receipt_fixture', ROOT/'tests/fixtures/phase_a_v1/runner.py')


class IndependentPresumedReleasePopulationQA(BASELINE.IndependentPreparedReleaseQA):
    @classmethod
    def setUpClass(cls):
        cls.fixture = FIXTURE.IndependentRunnerContract
        cls.fixture.setUpClass()
        cls.addClassCleanup(cls.fixture.tearDownClass)
        cls.seed = json.loads((cls.fixture.base/'build4/release/qa-seed/release-regression.json').read_bytes())

    def receipt(self):
        return copy.deepcopy(self.seed)

    def setUp(self):
        patcher = patch.object(BASELINE, 'receipt', self.receipt)
        patcher.start()
        self.addCleanup(patcher.stop)

    def validate(self, value):
        program = """
import json, sys
sys.path.insert(0, 'skills/presumed-sources')
from verify_release import validate_population, verify_source_binding
value = json.load(sys.stdin)
validate_population(value)
verify_source_binding(value['source_commit'], value['tested_python_sha256'], value['tested_execution_inputs_sha256'])
"""
        proc = subprocess.run([sys.executable, '-c', program], cwd=self.fixture.base,
                              input=json.dumps(value), text=True, capture_output=True, timeout=30)
        if proc.returncode:
            raise ValueError(proc.stderr)

    def test_interpreter_location_can_change_without_changing_command(self):
        value = self.receipt()
        self.verify_sealed(value)
        self.validate(value)
        for key, changed, reason in (
                ('outcome_schema_version', None, 'Missing actual execution receipt semantics'),
                ('outcome_schema_version', 2, 'Missing actual execution receipt semantics'),
                ('tested_execution_inputs_sha256', None, 'tested_execution_inputs_sha256'),
                ('source_commit', PROFILE12, 'Mandatory release gate plan differs')):
            bad = self.receipt()
            if changed is None:
                del bad[key]
            else:
                bad[key] = changed
            with self.subTest(key=key, changed=changed), self.assertRaisesRegex(ValueError, reason):
                self.validate(bad)
        for key in ('tested_python_sha256', 'tested_execution_inputs_sha256'):
            bad = self.receipt()
            bad[key][next(iter(bad[key]))] = '0'*64
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'Start/test source evidence differs'):
                self.verify_sealed(bad)
        bad = self.receipt()
        bad['logs'][0]['command'][1] = 'different-script.py'
        with self.assertRaisesRegex(ValueError, 'command population differs'):
            self.validate(bad)
        for row in value['logs'][:-1]:
            row['command'][0] = '/different/host/bin/python3'
        self.validate(value)
        self.verify_sealed(value)

    def verify_sealed(self, value):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)/'relocated'
            shutil.copytree(self.fixture.base, root)
            manifest = root/'build4/release/qa-seed/release-regression.json'
            manifest.write_text(json.dumps(value))
            from receipt_integrity import seal_inventory
            pointer = seal_inventory(root, manifest, 'skills/presumed-sources/release/full-regression-qa-seed.log',
                                     'build4/release/qa-seed/receipt-review.md',
                                     root/'build4/release/relocated-inventory.json', 'release')
            dest = root/'build4/release/relocated-pointer.json'
            dest.write_text(json.dumps(pointer))
            result = subprocess.run([sys.executable,'-m','build4.verify_release','--pointer',
                                     str(dest.relative_to(root))],cwd=root,env=self.fixture.env,
                                    capture_output=True,text=True,timeout=60)
            if result.returncode:
                raise ValueError(result.stderr)
            self.assertEqual(json.loads(result.stdout)['distinct_tests'], 136)

    def test_missing_replaced_or_reordered_validator_refused(self):
        for mutation in ('missing', 'replace', 'reorder'):
            value = self.receipt()
            index = len(PHASE_A_SUITES)
            if mutation == 'missing':
                value['logs'].pop(index)
            elif mutation == 'replace':
                value['logs'][index]['command'] = ['python', '-c', 'pass']
            else:
                value['logs'][index:index+2] = reversed(value['logs'][index:index+2])
            with self.subTest(mutation=mutation), self.assertRaisesRegex(ValueError, 'command population differs'):
                self.validate(value)

    def test_exact_independently_pinned_release_population(self):
        from release_population import discover, source_commit, verify_source_binding
        original = subprocess.check_output(['git','show',PROFILE12 + ':tests/test_presumed_release.py'], cwd=ROOT)
        self.assertEqual(hashlib.sha256(original).hexdigest(),
                         'faf8231c16dfe12d033dbef427fbf969dd93c91370099f7776512424132ea8bc')
        self.assertEqual(len(BASELINE.EXPECTED_SUITES + REMEDIATION), 22)
        self.assertEqual(list(VERIFIER.SUPPORTED_SUITES), PHASE_A_SUITES)
        self.assertEqual(list(VERIFIER.VALIDATOR_COMMANDS), BASELINE.EXPECTED_VALIDATORS)
        commit = source_commit()
        self.assertTrue(verify_source_binding(commit, {}, {LEDGER: LEDGER_SHA256}))
        rows = list(csv.DictReader(gzip.decompress((ROOT/LEDGER).read_bytes()).decode().splitlines(),
                                   delimiter='\t'))
        expected = [sorted(r['identity'] for r in rows if int(r['slot']) == slot)
                    for slot in range(23)]
        self.assertEqual(len(expected[22]), 16)
        expected[3] = sorted([*expected[3], ADDITIONAL_ID, ROUTING_ID])
        self.assertEqual(len(expected[3]), 142)
        self.assertEqual(expected[3][89], ROUTING_ID)
        self.assertEqual(sum(map(len, expected)), 4013)
        inventory = discover('governance-population', commit)
        check_phase_a_inventory(inventory, commit, expected)
        for delta in (-1, 1):
            bad = dict(inventory, discovered_distinct_tests=inventory['discovered_distinct_tests'] + delta)
            with self.subTest(total_delta=delta), self.assertRaisesRegex(ValueError, 'Incorrect discovered total'):
                check_phase_a_inventory(bad, commit, expected)
        bad = copy.deepcopy(inventory)
        bad['suite_results'][3]['tests'] -= 1
        with self.assertRaisesRegex(ValueError, 'Incorrect discovery count at slot 3'):
            check_phase_a_inventory(bad, commit, expected)
        bad = copy.deepcopy(inventory)
        identities = bad['suite_results'][3]['distinct_ids']
        identities.remove(ROUTING_ID)
        identities.append(ROUTING_ID)
        with self.assertRaisesRegex(ValueError, 'Incorrect identities at slot 3'):
            check_phase_a_inventory(bad, commit, expected)
        for group in ('Phase A', 'historical'):
            target = next(r for r in rows if group.lower() in r['mandatory population'].lower())
            bad = copy.deepcopy(inventory)
            bad['suite_results'][int(target['slot'])]['distinct_ids'].remove(target['identity'])
            with self.subTest(group=group), self.assertRaisesRegex(ValueError, 'Incorrect identities'):
                check_phase_a_inventory(bad, commit, expected)
        bad = copy.deepcopy(inventory)
        bad['suite_results'][22]['distinct_ids'].append(expected[22][0])
        with self.assertRaisesRegex(ValueError, 'Incorrect identities'):
            check_phase_a_inventory(bad, commit, expected)
        for replacement in ([], [dict(inventory['suite_results'][22], suite='tests/unauthorized')]):
            bad = dict(inventory, suite_results=inventory['suite_results'][:22] + replacement)
            with self.assertRaisesRegex(ValueError, 'Incorrect suite population'):
                check_phase_a_inventory(bad, commit, expected)
        with self.assertRaisesRegex(ValueError, 'Incorrect inventory source'):
            check_phase_a_inventory(dict(inventory, source_commit=PROFILE12), commit, expected)

    def test_every_remediation_slot_is_mandatory(self):
        for index in range(17, 22):
            value=self.receipt(); value['suite_results'].pop(index)
            self.refuses(value)

    def test_governance_environment_and_plan_are_mandatory(self):
        for key in ('CAO_GOV_REF', 'CAO_GOV_FOCUSED', 'CAO_ENGINEERING_REF', 'CAO_DIAGNOSTIC_OUT'):
            value=self.receipt(); value['logs'][18]['environment']=dict(value['logs'][18]['environment'])
            value['logs'][18]['environment'].pop(key)
            self.refuses(value)
        value=self.receipt(); value['gate_plan'].pop(); self.refuses(value)

    def test_all_ten_validators_still_required(self):
        for index in range(len(PHASE_A_SUITES), len(PHASE_A_SUITES) + 10):
            value=self.receipt(); value['logs'].pop(index); self.refuses(value)


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
