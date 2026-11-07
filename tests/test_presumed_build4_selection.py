"""Actual Build 4 entrypoint against executed synthetic receipts, never release evidence."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
path = ROOT/'diagnostics/profile12/runner-recovery/independent-qa/test_runner_contract.py'
spec = importlib.util.spec_from_file_location('build4_selection_fixture', path)
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


class Build4Selection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture.IndependentRunnerContract.setUpClass()

    @classmethod
    def tearDownClass(cls):
        fixture.IndependentRunnerContract.tearDownClass()

    def setUp(self):
        self.helper = fixture.IndependentRunnerContract()
        self.helper.setUp()
        self.addCleanup(self.helper.tearDown)
        self.root = self.helper.root

    def invoke(self, *args, pointer=None, optimize=False):
        env = {**self.helper.env, 'PYTHONPATH': str(self.root)}
        env.pop('CAO_ACCEPTANCE_POINTER', None)
        if pointer is not None:
            env['CAO_ACCEPTANCE_POINTER'] = pointer
        return subprocess.run([sys.executable] + (['-OO' if optimize == 2 else '-O'] if optimize else []) +
                              ['-m', 'build4.verify_release', *args], cwd=self.root,
                              env=env, text=True, capture_output=True, timeout=120)

    def test_matching_explicit_receipt_repeat_and_restart(self):
        for _ in range(2):
            result = self.invoke('--pointer', 'build4/release/qa-pointer.json')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['status'], 'PASS')
        result = self.invoke(pointer='build4/release/qa-pointer.json')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.helper.unchanged()

    def test_new_default_selects_matching_current_receipt(self):
        current = self.root/'build4/release/presumed-sources-current-release.json'
        current.write_bytes((self.root/'build4/release/qa-pointer.json').read_bytes())
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_tampered_receipt_rejected(self):
        fixture.put(self.root, 'build4/release/qa-seed/release-regression.json', '{}\n')
        result = self.invoke('--pointer', 'build4/release/qa-pointer.json')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('manifest hash differs', result.stderr)

    def test_missing_default_does_not_select_historical(self):
        result = self.invoke()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('presumed-sources-current-release.json', result.stderr)
        self.helper.unchanged()

    def test_explicit_missing_malformed_historical_and_conflict_rejected(self):
        fixture.put(self.root, 'build4/release/malformed.json', '{')
        for pointer in ('build4/release/absent.json', 'build4/release/malformed.json',
                        'build4/release/presumed-sources-accepted-release.json'):
            with self.subTest(pointer=pointer):
                self.assertNotEqual(self.invoke('--pointer', pointer).returncode, 0)
        result = self.invoke('--pointer', 'build4/release/qa-pointer.json', pointer='other.json')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Conflicting explicit', result.stderr)

    def test_changed_source_and_tampered_sidecar_rejected(self):
        path = self.root/'skills/tests/test_canary.py'
        original = path.read_bytes()
        path.write_bytes(original + b'\n# mismatched source\n')
        result = self.invoke('--pointer', 'build4/release/qa-pointer.json')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Python changed', result.stderr)
        path.write_bytes(original)
        fixture.put(self.root, 'build4/release/qa-seed/suite-0.json', '{}\n')
        self.assertNotEqual(self.invoke('--pointer', 'build4/release/qa-pointer.json').returncode, 0)

    def test_stale_current_and_redirected_pointer_fail_without_fallback(self):
        fixture.put(self.root, 'build4/release/presumed-sources-current-release.json', '{}\n')
        self.assertNotEqual(self.invoke().returncode, 0)
        link = self.root/'build4/release/redirected.json'
        link.symlink_to(self.root/'build4/release/qa-pointer.json')
        self.assertNotEqual(self.invoke('--pointer', 'build4/release/redirected.json').returncode, 0)

    def test_optimized_execution_refuses_before_selection(self):
        for flags in (1, 2):
            for args in ((), ('--pointer', 'build4/release/qa-pointer.json')):
                result = self.invoke(*args, optimize=flags)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Optimized Python is not supported', result.stderr)
