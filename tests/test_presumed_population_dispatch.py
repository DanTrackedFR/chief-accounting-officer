"""Actual production CLI negative cases in an explicitly synthetic repository.

The imported fixture executes only 136 trivial synthetic methods. It does not
execute the CAO accounting regression or confer release acceptance.
"""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('population_dispatch_fixture',
    ROOT/'tests/fixtures/phase_a_v1/runner.py')
FIXTURE = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(FIXTURE)


class ProductionPopulationDispatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = FIXTURE.IndependentRunnerContract
        cls.contract.setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.contract.tearDownClass()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)/'candidate'
        shutil.copytree(self.contract.base, self.root)
        self.env = {**self.contract.env, 'PYTHONPATH': str(self.root), 'CAO_SOURCES_ATTEMPT':'bounded-check'}

    def invoke(self, *args):
        return subprocess.run([sys.executable, 'skills/presumed-sources/run_release.py', *args],
                              cwd=self.root, env=self.env, capture_output=True, text=True, timeout=60)

    def test_actual_discovery_rejects_one_missing_required_method(self):
        before = self.invoke('--discover'); self.assertEqual(before.returncode, 0, before.stderr)
        inventory = json.loads(before.stdout)
        self.assertEqual(inventory['discovered_distinct_tests'], 136)
        required = json.loads((self.root/'skills/presumed-sources/required-remediation-tests.json').read_text())['suites'][0]
        method = required['distinct_ids'][0].split('.')[-1]
        path = self.root/required['suite']/required['pattern']
        path.write_text(path.read_text().replace('def '+method+'(', 'def omitted_'+method+'(', 1))
        failed = self.invoke('--discover')
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn('Missing mandatory Phase A/historical methods', failed.stderr)
        self.assertFalse((self.root/'build4/release/bounded-check').exists())

    def test_missing_outcome_dependency_refused_before_execution(self):
        for name in ('../escape', str(self.root.parent/'escaped')):
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'Redirected fixture path'):
                FIXTURE.put(self.root, name, 'invalid')
        link = self.root / 'outside'
        link.symlink_to(self.root.parent, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'Redirected fixture path'):
            FIXTURE.put(self.root, 'outside/escaped', 'invalid')
        link.unlink()
        original = Path.read_bytes
        for filename in ('accepted-main-infrastructure-v1.json', 'proof-contract.json', 'governance-source-v2.json'):
            with self.subTest(contract=filename), patch.object(Path, 'read_bytes',
                    lambda p: b'{}' if p.name == filename else original(p)):
                with self.assertRaisesRegex(ValueError, 'Fixture contract changed'):
                    FIXTURE.bind_fixture_contracts(self.root)
        path = self.root / 'build4/test_outcomes.py'
        path.unlink()
        result = self.invoke('--discover')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("No module named 'build4.test_outcomes'", result.stderr)
        self.assertFalse((self.root / 'build4/release/bounded-check').exists())

    def test_actual_preflight_refuses_dirty_consumed_input(self):
        path = self.root/'skills/presumed-sources/required-remediation-tests.json'
        path.write_bytes(path.read_bytes()+b'\n')
        failed = self.invoke('--preflight')
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn('Commit tracked changes', failed.stderr)
        self.assertFalse((self.root/'build4/release/bounded-check').exists())

    def test_actual_preflight_refuses_ignored_untracked_python(self):
        ignore = self.root/'.git/info/exclude'
        ignore.write_text(ignore.read_text()+'\nignored-input.py\n')
        (self.root/'ignored-input.py').write_text('VALUE=1\n')
        failed = self.invoke('--preflight')
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn('including ignored files', failed.stderr)
        self.assertFalse((self.root/'build4/release/bounded-check').exists())

    def test_actual_preflight_dispatches_all_five_slots_without_release_receipt(self):
        result = self.invoke('--preflight'); self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        attempt = self.root/'build4/release/bounded-check'
        receipt = json.loads((attempt/'bounded-preflight.json').read_text())
        self.assertTrue(receipt['complete'])
        self.assertEqual(receipt['executed_distinct_tests'], 64)
        self.assertEqual(len(receipt['suite_results']), 6)
        self.assertEqual(len(receipt['gate_plan']), 23)
        self.assertFalse(receipt['release_accepted'])
        self.assertFalse(receipt['full_accounting_regression_executed'])
        self.assertFalse((attempt/'release-regression.json').exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
