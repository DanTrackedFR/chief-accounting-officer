"""Bounded actual-process QA. Temporary synthetic contract, never CAO acceptance.

All runner/verifier algorithms are real. Only the fixture's historical population
and digest constants differ, because the real pinned historical test files cannot
be replaced with 17 cheap canaries. Real preservation is checked separately.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / 'skills/presumed-sources'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def put(root, name, contents):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents)
    return path


def json_put(root, name, value):
    return put(root, name, json.dumps(value, indent=2, sort_keys=True) + '\n')


class IndependentRunnerContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.storage = tempfile.TemporaryDirectory()
        cls.base = Path(cls.storage.name) / 'base'
        cls.base.mkdir()
        objects = subprocess.check_output(['git', 'rev-parse', '--path-format=absolute',
                                           '--git-path', 'objects'], cwd=ROOT, text=True).strip()
        cls.env = {**os.environ, 'GIT_ALTERNATE_OBJECT_DIRECTORIES': objects}
        subprocess.run(['git', 'init', '-q'], cwd=cls.base, check=True)
        for name in ('execute_release.py', 'run_release.py', 'verify_release.py', 'receipt_integrity.py'):
            put(cls.base, 'skills/presumed-sources/' + name, (SOURCE / name).read_text())
        for name in ('build4/run_release.py', 'orchestration/history_references.py'):
            put(cls.base, name, (ROOT / name).read_text())
        spec = importlib.util.spec_from_file_location('qa_real_verifier', SOURCE / 'verify_release.py')
        verifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(verifier)
        cls.suites = verifier.SUPPORTED_SUITES
        cls.validators = verifier.VALIDATOR_COMMANDS
        for i, (directory, pattern) in enumerate(cls.suites):
            filename = 'independent_review_tests.py' if pattern == 'independent_review_tests.py' else 'test_canary.py'
            put(cls.base, directory + '/' + filename,
                'import unittest\nclass Canary(unittest.TestCase):\n'
                '    def test_executed(self): self.assertEqual(2 + 2, 4)\n')
        for name in cls.validators:
            put(cls.base, name, 'print("synthetic validator executed")\n')
        json_put(cls.base, 'local_cao/release/release-regression.json', dict(
            suite_results=[dict(suite=s, pattern=p) for s, p in cls.suites[:11]],
            validators=[dict(command=c) for c in cls.validators[:7]]))
        canary = put(cls.base, 'historical-canary.txt', 'immutable synthetic historical evidence\n')
        preservation = json_put(cls.base, 'skills/presumed-sources/release/historical-preservation.json',
            dict(baseline='7146eaeca6a28d17d9183d0f9431fd9b9663f1fe',
                 files={'historical-canary.txt': sha(canary)}))
        vpath = cls.base / 'skills/presumed-sources/verify_release.py'
        vpath.write_text(vpath.read_text().replace(verifier.PRESERVATION_SHA256, sha(preservation))
                         .replace('PRESERVATION_COUNT = 8912', 'PRESERVATION_COUNT = 1'))
        json_put(cls.base, 'build4/release/investment-property-historical-preservation.json',
                 dict(files={'historical-canary.txt': sha(canary)}))
        for name in ('specialist-migration.json', 'orchestration-migration.json', 'main-proof-migration.json'):
            json_put(cls.base, 'skills/government-grants/release-evidence/historical-qa/' + name,
                     dict(status='PASS', errors=[], files={}))
        put(cls.base, 'build4/release/presumed-sources-accepted-release.json',
            '{"historical": "deliberately stale, untouched"}\n')
        result = cls.invoke(cls.base, 'qa-seed')
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr +
                (cls.base / 'skills/presumed-sources/release/full-regression-qa-seed.log').read_text())
        manifest = json.loads((cls.base / 'build4/release/qa-seed/release-regression.json').read_text())
        if manifest['executed_distinct_tests'] != 17 or len(manifest['logs']) != 28:
            raise AssertionError('Synthetic real execution population differs')
        put(cls.base, 'build4/release/qa-seed/receipt-review.md',
            'SYNTHETIC FIXTURE ONLY: 17 actual trivial tests, not CAO accounting acceptance.\n')
        seal = '''import json,sys
from pathlib import Path
sys.path.insert(0,'skills/presumed-sources')
from receipt_integrity import seal_inventory
root=Path.cwd()
p=seal_inventory(root,root/'build4/release/qa-seed/release-regression.json',
 'skills/presumed-sources/release/full-regression-qa-seed.log',
 'build4/release/qa-seed/receipt-review.md',root/'build4/release/qa-inventory.json','release')
(root/'build4/release/qa-pointer.json').write_text(json.dumps(p))
'''
        subprocess.run([sys.executable, '-c', seal], cwd=cls.base, env=cls.env, check=True)
        result = cls.invoke(cls.base, 'qa-control', '--reuse', 'build4/release/qa-pointer.json')
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)

    @classmethod
    def tearDownClass(cls):
        cls.storage.cleanup()

    @classmethod
    def invoke(cls, root, attempt, *args, optimize=False):
        return subprocess.run([sys.executable] + (['-O'] if optimize else []) +
            ['skills/presumed-sources/execute_release.py', *args], cwd=root,
            env={**cls.env, 'CAO_SOURCES_ATTEMPT': attempt, 'PYTHONPATH': str(root)},
            capture_output=True, text=True, timeout=60)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'fixture'
        shutil.copytree(self.base, self.root)
        self.before = self.snapshot()

    def tearDown(self):
        self.temp.cleanup()

    def snapshot(self):
        return {str(p.relative_to(self.root)): sha(p) for p in self.root.rglob('*')
                if p.is_file() and (str(p.relative_to(self.root)).startswith('build4/release/')
                   or str(p.relative_to(self.root)).startswith('skills/presumed-sources/release/')
                   or p.name == 'historical-canary.txt')}

    def unchanged(self):
        after = self.snapshot()
        self.assertTrue(self.before.items() <= after.items())

    def rejected(self, *args, optimize=False):
        result = self.invoke(self.root, 'qa-rejected', *args, optimize=optimize)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((self.root / 'build4/release/qa-rejected').exists())
        self.assertFalse((self.root / 'skills/presumed-sources/release/full-regression-qa-rejected.log').exists())
        return result

    def test_valid_explicit_reuse_uses_full_verifier_without_regression(self):
        r = self.invoke(self.root, 'qa-reuse', '--reuse', 'build4/release/qa-pointer.json')
        self.assertEqual(r.returncode, 0, r.stderr)
        value = json.loads(r.stdout)
        self.assertEqual(value['status'], 'ACCEPTANCE_REUSED')
        self.assertEqual(value['verification']['distinct_tests'], 17)
        self.assertEqual(value['verification']['historical_files'], 1)
        self.assertFalse((self.root / 'build4/release/qa-reuse/release-regression.json').exists())
        self.assertFalse((self.root / 'skills/presumed-sources/release/full-regression-qa-reuse.log').exists())
        self.unchanged()

    def test_default_runs_despite_historical_pointer_and_matching_acceptance(self):
        r = self.invoke(self.root, 'qa-fresh')
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse(json.loads(r.stdout)['release_accepted'])
        manifest = json.loads((self.root / 'build4/release/qa-fresh/release-regression.json').read_text())
        self.assertTrue(manifest['complete'])
        self.assertEqual(manifest['executed_distinct_tests'], 17)
        self.unchanged()

    def test_malformed_explicit_pointer_rejected(self):
        put(self.root, 'build4/release/broken.json', '{')
        self.rejected('--reuse', 'build4/release/broken.json')
        self.unchanged()

    def test_historical_explicit_pointer_rejected(self):
        self.rejected('--reuse', 'build4/release/presumed-sources-accepted-release.json')
        self.unchanged()

    def test_missing_explicit_pointer_rejected(self):
        self.rejected('--reuse', 'build4/release/missing.json')
        self.unchanged()

    def test_changed_python_identity_rejected(self):
        p = self.root / 'skills/tests/test_canary.py'
        p.write_text(p.read_text() + '# source differs\n')
        r = self.rejected('--reuse', 'build4/release/qa-pointer.json')
        self.assertIn('Python changed', r.stderr)
        self.unchanged()

    def test_changed_execution_input_identity_rejected(self):
        put(self.root, 'interfaces/changed.json', '{}\n')
        r = self.rejected('--reuse', 'build4/release/qa-pointer.json')
        self.assertIn('execution inputs changed', r.stderr)
        self.unchanged()

    def test_inventory_artifact_corruption_rejected(self):
        put(self.root, 'build4/release/qa-seed/suite-0.log', 'tampered\n')
        r = self.rejected('--reuse', 'build4/release/qa-pointer.json')
        self.assertIn('artifact changed', r.stderr)

    def test_pointer_escape_and_symlink_rejected(self):
        self.rejected('--reuse', '../outside.json')
        (self.root / 'build4/release/link.json').symlink_to(self.root / 'build4/release/qa-pointer.json')
        self.rejected('--reuse', 'build4/release/link.json')
        self.unchanged()

    def test_optimized_wrapper_cannot_reuse(self):
        r = self.rejected('--reuse', 'build4/release/qa-pointer.json', optimize=True)
        self.assertIn('Optimized Python', r.stderr)
        self.unchanged()

    def test_prior_attempt_collision_preserves_bytes(self):
        r = self.invoke(self.root, 'qa-seed')
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('Preserve prior attempt', r.stderr)
        self.unchanged()

    def test_outer_log_collision_preserves_bytes(self):
        put(self.root, 'skills/presumed-sources/release/full-regression-qa-rejected.log', 'old log\n')
        before = self.snapshot()
        r = self.invoke(self.root, 'qa-rejected')
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(before, self.snapshot())
        self.assertFalse((self.root / 'build4/release/qa-rejected').exists())

    def test_output_symlink_rejected(self):
        (self.root / 'build4/release/qa-rejected').symlink_to(self.root / 'build4/release/qa-seed', target_is_directory=True)
        r = self.invoke(self.root, 'qa-rejected')
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('redirected', r.stderr)
        self.unchanged()

    def test_invalid_attempt_labels_rejected(self):
        for attempt in ('', '../escape', '-bad', 'with space', 'bad/slash'):
            with self.subTest(attempt=attempt):
                r = self.invoke(self.root, attempt)
                self.assertNotEqual(r.returncode, 0)
                self.assertIn('unique CAO_SOURCES_ATTEMPT', r.stderr)
        self.unchanged()

    def test_unsuccessful_actual_regression_never_claims_acceptance(self):
        put(self.root, 'skills/tests/test_canary.py',
            'import unittest\nclass Canary(unittest.TestCase):\n'
            '    def test_failed(self): self.fail("intentional synthetic failure")\n')
        r = self.invoke(self.root, 'qa-failed')
        self.assertNotEqual(r.returncode, 0)
        manifest = json.loads((self.root / 'build4/release/qa-failed/release-regression.json').read_text())
        self.assertFalse(manifest['complete'])
        self.assertFalse((self.root / 'build4/release/qa-failed/execution.json').exists())
        self.unchanged()

    def test_actual_workflow_final_gate_rejects_pending_and_accepts_verified_reuse(self):
        workflow = (ROOT / '.github/workflows/cao-presumed-sources.yml').read_text()
        step = workflow.split('      - name: Report execution scope (fresh regression is not release acceptance)\n', 1)[1]
        body = step.split('      - name:', 1)[0].split('        run: |\n', 1)[1]
        command = textwrap.dedent(body)
        for attempt, expected_code in (('qa-seed', 1), ('qa-control', 0)):
            with self.subTest(attempt=attempt):
                r = subprocess.run(['bash', '-e', '-c', command], cwd=self.root,
                    env={**self.env, 'CAO_SOURCES_ATTEMPT': attempt,
                         'GITHUB_STEP_SUMMARY': str(self.root / 'step-summary.md')},
                    capture_output=True, text=True, timeout=10)
                self.assertEqual(r.returncode, expected_code, r.stdout + r.stderr)
        self.unchanged()


if __name__ == '__main__':
    unittest.main(verbosity=2)
