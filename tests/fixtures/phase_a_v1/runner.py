"""Bounded actual-process QA. Temporary synthetic contract, never CAO acceptance.

All runner/verifier algorithms are real. Only the fixture's historical population
and digest constants differ, because the real pinned historical test files cannot
be replaced with 136 cheap canaries (18 suite probes plus 118 required identities). Real preservation is checked separately.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
FROZEN = 'e025098beb849484e49d27f005adbcd30d508dc4'
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


# Every imported release implementation must still match its frozen Git blob.
DEPENDENCIES = (
    'build4/run_release.py', 'build4/verify_release.py', 'build4/test_outcomes.py',
    'orchestration/history_references.py', 'intelligence/tests/run_release.py',
    *('skills/presumed-sources/' + name for name in (
        'execute_release.py', 'run_release.py', 'suite_runner.py', 'verify_release.py',
        'receipt_integrity.py', 'release_population.py', 'proof_selection.py', 'accepted_history.py',
        'required-remediation-tests.json', 'phase-a-contracts/required-tests-v1.json',
        'release/http-proof.json', 'release/phase-a-v1/http-proof.json')),
)


def copy_dependency(root, name):
    data = (ROOT / name).read_bytes()
    if name == 'skills/presumed-sources/proof_selection.py':
        if hashlib.sha256(data).hexdigest() != '19dbe5411bdb03dd33d4247b38ee6d68732318229680c1d53fad1e59f14a9c5b':
            raise ValueError('Fixture successor selector changed')
    elif data != subprocess.check_output(['git', 'show', FROZEN + ':' + name], cwd=ROOT):
        raise ValueError('Fixture dependency differs from frozen source: ' + name)
    dest = root / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)


def substitute(path, before, after):
    text = path.read_text()
    if text.count(before) != 1:
        raise ValueError('Unexpected fixture constant in ' + str(path))
    path.write_text(text.replace(before, after))


def bind_fixture_contracts(root):
    # Scope only the fixture data and trusted digests to this isolated checkout.
    # The preservation and proof validators continue to run in the child process.
    directory = root / 'skills/presumed-sources'
    relative = 'skills/presumed-sources/'
    live = json.loads((SOURCE / 'phase-a-contracts/accepted-main-infrastructure-v1.json').read_bytes())
    files = {}
    for name, row in live['source_migrations'].items():
        copy_dependency(root, row['archive_path'])
        if not (root / name).exists():
            copy_dependency(root, name)
        row['successor_sha256'] = sha(root / name)
        files[name] = live['files'][name]
    canary = 'historical-canary.txt'
    files[canary] = subprocess.check_output(['git', 'hash-object', canary], cwd=root, text=True).strip()
    live['files'] = files
    path = json_put(root, relative + 'phase-a-contracts/accepted-main-infrastructure-v1.json', live)
    history = directory / 'accepted_history.py'
    substitute(history, 'b2c6a8d435095a82ae63d1d4f8ec5ed2e62dba4e4222e5adb5843914b3e4bfac', sha(path))
    substitute(history, "len(data['files'])==7963", "len(data['files'])==5")
    proof = json.loads((SOURCE / 'release/phase-a-v1/proof-contract.json').read_bytes())
    # The fixture emitter calculates its totals separately from its pinned expected values.
    expected = {'executions': [
        {'package': 'fixed-assets', 'calculations': [
            {'label': 'closing cost', 'amount': 648000}, {'label': 'depreciation', 'amount': 64800}]},
        {'package': 'accounts-payable', 'calculations': [{'label': 'invoices', 'amount': 1550}]}]}
    proof_path = json_put(root, proof['successor_proof']['path'], expected)
    proof['successor_proof']['sha256'] = sha(proof_path)
    put(root, 'hosted_cao/tests/prove_presumed_http.py', """
import json
assets = [10000 + 1000 * i for i in range(1, 28)]
rows = [
    dict(package='fixed-assets', calculations=[
        dict(label='closing cost', amount=sum(assets)),
        dict(label='depreciation', amount=sum(cost // 10 for cost in assets))]),
    dict(package='accounts-payable', calculations=[
        dict(label='invoices', amount=sum(100 + 10 * i for i in range(1, 11)))])]
print(json.dumps(dict(executions=rows), sort_keys=True, indent=2))
""")
    proof['accounting_source_sha256'] = {
        str(p.relative_to(root)): sha(p) for folder in ('orchestration','local_cao','hosted_cao','intelligence','skills')
        for p in (root / folder).rglob('*.py') if not p.is_relative_to(directory)}
    proof['proof_inputs_sha256'] = {
        str(p.relative_to(root)): sha(p)
        for folder in ('build4','intelligence','hosted_cao','local_cao','orchestration','skills','interfaces','knowledge','.github')
        for p in (root / folder).rglob('*') if p.suffix in {'.json','.md','.csv','.yml','.yaml','.txt'}
        and 'release' not in p.relative_to(root).parts and 'examples' not in p.relative_to(root).parts}
    transition = json.loads((SOURCE / 'release/phase-a-v1/governance-source-v2.json').read_bytes())
    fixture_test = put(root, transition['path'], '# synthetic successor governance module\n')
    transition['before'] = hashlib.sha256(b'# synthetic predecessor governance module\n').hexdigest()
    transition['after'] = sha(fixture_test)
    proof['accounting_source_sha256'][transition['path']] = transition['before']
    path = json_put(root, relative + 'release/phase-a-v1/proof-contract.json', proof)
    substitute(directory / 'proof_selection.py',
               '0cfd93e3d75f3bd9d781422bbbf97129607fe07253a09dba6d80f911de673694', sha(path))
    transition['parent_sha256'] = sha(path)
    path = json_put(root, relative + 'release/phase-a-v1/governance-source-v2.json', transition)
    substitute(directory / 'proof_selection.py',
               '1ec5e6f00421cd4948a23a1db6ac22f17128d6b63511544ac267c0d4e466d836', sha(path))



HISTORICAL_FIXTURE = 'diagnostics/profile12/runner-recovery/independent-qa/test_runner_contract.py'
spec = importlib.util.spec_from_file_location('profile12_historical_runner', ROOT / HISTORICAL_FIXTURE)
historical = importlib.util.module_from_spec(spec)
spec.loader.exec_module(historical)


class IndependentRunnerContract(historical.IndependentRunnerContract):
    @classmethod
    def setUpClass(cls):
        cls.storage = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.storage.cleanup)
        cls.base = Path(cls.storage.name) / 'base'
        cls.base.mkdir()
        objects = subprocess.check_output(['git', 'rev-parse', '--path-format=absolute',
                                           '--git-path', 'objects'], cwd=ROOT, text=True).strip()
        cls.env = {**os.environ, 'GIT_ALTERNATE_OBJECT_DIRECTORIES': objects}
        subprocess.run(['git', 'init', '-q'], cwd=cls.base, check=True)
        for name in DEPENDENCIES:
            copy_dependency(cls.base, name)
        spec = importlib.util.spec_from_file_location('qa_real_verifier', SOURCE / 'verify_release.py')
        verifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(verifier)
        cls.suites = verifier.SUPPORTED_SUITES
        cls.validators = verifier.VALIDATOR_COMMANDS
        for i, (directory, pattern) in enumerate(cls.suites[:17] + cls.suites[22:]):
            filename = 'independent_review_tests.py' if pattern == 'independent_review_tests.py' else 'test_canary.py'
            put(cls.base, directory + '/' + filename,
                'import unittest\nclass Canary(unittest.TestCase):\n'
                '    def test_executed(self): self.assertEqual(2 + 2, 4)\n')
        # Keep the immutable required identities; substitute only their bodies in
        # this explicitly synthetic fixture. Production never changes its contract.
        required = json.loads((SOURCE/'required-remediation-tests.json').read_text())
        for row in required['suites']:
            classes = {}
            for identity in row['distinct_ids']:
                module, klass, method = identity.split('::')[1].split('.')
                classes.setdefault(klass, []).append(method)
            text = 'import unittest\n'
            for klass, methods in classes.items():
                text += 'class '+klass+'(unittest.TestCase):\n'
                for method in methods:
                    text += '    def '+method+'(self): self.assertTrue(True)\n'
            put(cls.base, row['suite']+'/'+row['pattern'], text)
        phase_ids = json.loads((cls.base / 'skills/presumed-sources/phase-a-contracts/required-tests-v1.json').read_bytes())['required_ids']
        modules = {}
        for identity in phase_ids:
            directory, case = identity.split('::')
            module, klass, method = case.split('.')
            modules.setdefault(directory + '/' + module + '.py', {}).setdefault(klass, []).append(method)
        for name, classes in modules.items():
            lines = ['import unittest']
            for klass, methods in classes.items():
                lines.append('class ' + klass + '(unittest.TestCase):')
                lines.extend('    def ' + method + '(self): self.assertEqual(1, 1)' for method in methods)
            put(cls.base, name, '\n'.join(lines) + '\n')
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
        bind_fixture_contracts(cls.base)
        subprocess.run(['git', 'add', '.'], cwd=cls.base, check=True)
        subprocess.run(['git', '-c', 'user.name=Synthetic QA', '-c', 'user.email=synthetic@example.invalid', 'commit', '-qm', 'Synthetic fixture only'], cwd=cls.base, check=True)
        result = cls.invoke(cls.base, 'qa-seed')
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr +
                (cls.base / 'skills/presumed-sources/release/full-regression-qa-seed.log').read_text())
        manifest = json.loads((cls.base / 'build4/release/qa-seed/release-regression.json').read_text())
        if manifest['executed_distinct_tests'] != 136 or len(manifest['logs']) != 34:
            raise AssertionError('Synthetic real execution population differs')
        put(cls.base, 'build4/release/qa-seed/receipt-review.md',
            'SYNTHETIC FIXTURE ONLY: 136 actual trivial tests, not CAO accounting acceptance.\n')
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


    def test_valid_explicit_reuse_uses_full_verifier_without_regression(self):
        r = self.invoke(self.root, 'qa-reuse', '--reuse', 'build4/release/qa-pointer.json')
        self.assertEqual(r.returncode, 0, r.stderr)
        value = json.loads(r.stdout)
        self.assertEqual(value['status'], 'ACCEPTANCE_REUSED')
        self.assertEqual(value['verification']['distinct_tests'], 136)
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
        self.assertEqual(manifest['executed_distinct_tests'], 136)
        self.unchanged()


    def test_changed_python_identity_rejected(self):
        p = self.root / 'tests/test_canary.py'
        p.write_text(p.read_text() + '# source differs\n')
        r = self.rejected('--reuse', 'build4/release/qa-pointer.json')
        self.assertIn('Python changed', r.stderr)
        self.unchanged()

    def test_changed_execution_input_identity_rejected(self):
        put(self.root, 'diagnostics/profile12/fixtures/changed.json', '{}\n')
        r = self.rejected('--reuse', 'build4/release/qa-pointer.json')
        self.assertIn('execution inputs changed', r.stderr)
        self.unchanged()


    def test_unsuccessful_actual_regression_never_claims_acceptance(self):
        put(self.root, 'tests/test_canary.py',
            'import unittest\nclass Canary(unittest.TestCase):\n'
            '    def test_failed(self): self.fail("intentional synthetic failure")\n')
        subprocess.run(['git', 'add', 'tests/test_canary.py'], cwd=self.root, check=True)
        subprocess.run(['git', '-c', 'user.name=Synthetic QA', '-c', 'user.email=synthetic@example.invalid', 'commit', '-qm', 'Intentional failure fixture'], cwd=self.root, check=True)
        r = self.invoke(self.root, 'qa-failed')
        self.assertNotEqual(r.returncode, 0)
        manifest = json.loads((self.root / 'build4/release/qa-failed/release-regression.json').read_text())
        self.assertFalse(manifest['complete'])
        self.assertFalse((self.root / 'build4/release/qa-failed/execution.json').exists())
        self.unchanged()
