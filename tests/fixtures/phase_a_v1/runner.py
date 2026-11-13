"""Bounded actual-process QA. Temporary synthetic contract, never CAO acceptance.

All runner/verifier algorithms are real. Only the fixture's historical population
and digest constants differ, because the real pinned historical test files cannot
be replaced with 136 cheap canaries (18 suite probes plus 118 required identities). Real preservation is checked separately.
"""
import hashlib
import contextlib
import copy
from unittest.mock import patch
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
sys.path.insert(0,str(SOURCE))


def git_environment():
    """Real-checkout reads must not inherit repository-selection overrides."""
    return {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def child_path(root, name):
    relative = Path(name)
    path = root / relative
    if relative.is_absolute() or '..' in relative.parts or path.resolve() != path:
        raise ValueError('Redirected fixture path: ' + str(name))
    return path


def read_contract(name, expected):
    data = child_path(SOURCE, name).read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError('Fixture contract changed: ' + name)
    return json.loads(data)


def put(root, name, contents):
    path = child_path(root, name)
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
        'receipt_integrity.py', 'release_population.py', 'proof_selection.py', 'accepted_history.py', 'ci_governance.py',
        'required-remediation-tests.json', 'phase-a-contracts/required-tests-v1.json',
        'release/http-proof.json', 'release/phase-a-v1/http-proof.json')),
)


def copy_dependency(root, name):
    dest = child_path(root, name)
    data = child_path(ROOT, name).read_bytes()
    from ci_governance import load_contract, MODIFIED, ADDED
    transition = load_contract(ROOT)
    if name in MODIFIED:
        expected = transition['modified_files'][name]['after_sha256']
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError('Fixture successor dependency changed: ' + name)
    elif name == ADDED[0]:
        import ci_governance
        if data != Path(ci_governance.__file__).read_bytes():
            raise ValueError('Fixture anchor differs from loaded test trust root')
    elif data != subprocess.check_output(['git', 'show', FROZEN + ':' + name], cwd=ROOT, env=git_environment()):
        raise ValueError('Fixture dependency differs from frozen source: ' + name)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)


def substitute(path, before, after):
    text = path.read_text()
    if text.count(before) != 1:
        raise ValueError('Unexpected fixture constant in ' + str(path))
    path.write_text(text.replace(before, after))


def bind_fixture_contracts(root, env=None):
    # Scope only the fixture data and trusted digests to this isolated checkout.
    # The preservation and proof validators continue to run in the child process.
    directory = root / 'skills/presumed-sources'
    relative = 'skills/presumed-sources/'
    live = read_contract('phase-a-contracts/accepted-main-infrastructure-v1.json',
                         'b2c6a8d435095a82ae63d1d4f8ec5ed2e62dba4e4222e5adb5843914b3e4bfac')
    proof = read_contract('release/phase-a-v1/proof-contract.json',
                          '0cfd93e3d75f3bd9d781422bbbf97129607fe07253a09dba6d80f911de673694')
    transition = read_contract('release/phase-a-v1/governance-source-v2.json',
                               '1ec5e6f00421cd4948a23a1db6ac22f17128d6b63511544ac267c0d4e466d836')
    migrations = {'diagnostics/profile12/remediation/issue_focused_receipt.py',
                  *(relative + name for name in ('release_population.py', 'run_release.py', 'verify_release.py'))}
    if set(live['source_migrations']) != migrations or transition['path'] != 'skills/tests/test_independent_ip_main_reconciliation.py':
        raise ValueError('Unexpected synthetic migration population')
    files = {}
    for name, row in live['source_migrations'].items():
        copy_dependency(root, row['archive_path'])
        if not (root / name).exists():
            copy_dependency(root, name)
        row['successor_sha256'] = sha(root / name)
        files[name] = live['files'][name]
    canary = 'historical-canary.txt'
    files[canary] = subprocess.check_output(['git', 'hash-object', canary], cwd=root, env=git_environment() if env is None else env, text=True).strip()
    live['files'] = files
    path = json_put(root, relative + 'phase-a-contracts/accepted-main-infrastructure-v1.json', live)
    history = directory / 'accepted_history.py'
    substitute(history, 'b2c6a8d435095a82ae63d1d4f8ec5ed2e62dba4e4222e5adb5843914b3e4bfac', sha(path))
    substitute(history, "len(data['files'])==7963", "len(data['files'])==5")
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



@contextlib.contextmanager
def synthetic_review_context():
    """Check the real overlay before a caller's independent synthetic history.

    This compatibility context does not fabricate review authority or change
    production pins. Fabricated-source checks use bind_ci_fixture's separate
    disposable records instead; genuine evidence stays byte-for-byte intact.
    """
    import ci_governance as governance
    governance.verify_transition(ROOT)
    yield


def bind_ci_fixture(root, env):
    """Rebind data and literal pins ONLY in an isolated synthetic Git checkout.

    The code-pin-bound provisional closure is checked before copying.
    This synthetic seal never authorises the production candidate.
    All production algorithms remain in the child; synthetic maps and histories
    are separately labelled and cannot leave this temporary fixture as acceptance.
    """
    import ci_governance as governance
    data = json.loads((ROOT / governance.CONTRACT).read_bytes())
    namespace = root / governance.NAMESPACE
    namespace.mkdir(parents=True, exist_ok=True)
    # Keep original sealed records immutable; only temporary successor data is rebound.
    for record in governance.AMENDMENT_RECORDS:
        put(root, record, (ROOT/record).read_text())
    for name in governance.WORKFLOWS:
        put(root, name, (ROOT/name).read_text())
    for name in ('tests/test_presumed_release.py', governance.ADDED[1], governance.COMPATIBILITY_TEST,
                 'tests/phase_a_release_infra/test_infrastructure.py'):
        put(root, name, '# Synthetic closure file; no CAO test body or acceptance.\n')
    put(root, 'tests/fixtures/phase_a_v1/runner.py', Path(__file__).read_text())
    for name in ('contract.schema.json','owner-authorization.json'):
        put(root, governance.NAMESPACE+'/'+name, (ROOT/governance.NAMESPACE/name).read_text())
    # The original review stays immutable even in this disposable history.
    put(root, governance.NAMESPACE+'/scope-review.md',
        (ROOT/governance.NAMESPACE/'scope-review.md').read_text())
    subprocess.run(['git','add','.'],cwd=root,env=env,check=True)
    subprocess.run(['git','commit','-qm','Synthetic predecessor only'],cwd=root,env=env,check=True)
    put(root,'build4/release/synthetic-f2-evidence.txt','synthetic immutable evidence\n')
    subprocess.run(['git','add','.'],cwd=root,env=env,check=True)
    subprocess.run(['git','commit','-qm','Synthetic evidence only'],cwd=root,env=env,check=True)
    f2 = subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,env=env,text=True).strip()
    tree = subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=root,env=env,text=True).strip()
    helper = root / governance.ADDED[0]
    substitute(helper, governance.F2, f2)
    substitute(helper, '2fff8be455b395428ab26de94cc046cc33c8040c', tree)
    substitute(helper, 'F2_COUNT = 611', 'F2_COUNT = 1')
    substitute(helper, governance.FROZEN_MANIFEST, 'build4/release/synthetic-frozen-maps.json')
    data['predecessor_commits']['f2'] = f2
    data['predecessor_commits']['f2_tree'] = tree
    data['state'] = 'SEALED'
    # Separate local synthetic authority; never label it as the published G4C-3.
    report = 'SYNTHETIC COMPONENT REPORT ONLY. No independent CAO review or acceptance.\n'
    review = put(root,governance.AMENDMENT_REVIEW,
        'SYNTHETIC DISPOSABLE FIXTURE. No published review or human signature.\n\n'
        '## Synthetic component report\n\n'+report)
    synthetic = copy.deepcopy(governance.IMPLEMENTATION_REVIEW)
    synthetic.update(sha256=sha(review),review_id='SYNTHETIC_COMPONENT_ONLY',
        publication='synthetic://disposable-fixture/no-published-approval',
        report_sha256=hashlib.sha256(report.encode()).hexdigest(),
        reviewed_commit=f2,reviewed_tree=tree,disposition='SYNTHETIC_COMPONENT_ONLY',
        conditions=['NO CAO APPROVAL; disposable component test only'],
        session_reference='SYNTHETIC_NO_REVIEWER_SESSION')
    # Only copied helper constants are rebound; production has no test-mode branch.
    substitute(helper,'REVIEW_REPORT_MARKER = '+repr(governance.REVIEW_REPORT_MARKER),
               "REVIEW_REPORT_MARKER = b'## Synthetic component report\\n\\n'")
    substitute(helper,'IMPLEMENTATION_REVIEW = '+repr(governance.IMPLEMENTATION_REVIEW),
               'IMPLEMENTATION_REVIEW = '+repr(synthetic))
    substitute(helper,"REVIEWED_IMPLEMENTATION = '"+governance.REVIEWED_IMPLEMENTATION+"'",
               "REVIEWED_IMPLEMENTATION = '"+f2+"'")
    substitute(helper,"REVIEWED_TREE = '"+governance.REVIEWED_TREE+"'",
               "REVIEWED_TREE = '"+tree+"'")
    data['scope_review'] = dict(path=governance.AMENDMENT_REVIEW,
                              sha256=sha(review),status='INDEPENDENTLY_REVIEWED')
    data['schema']['sha256'] = sha(namespace/'contract.schema.json')
    data['owner_authorization']['sha256'] = sha(namespace/'owner-authorization.json')
    data['modified_files'] = {}
    for name in governance.MODIFIED:
        before = subprocess.check_output(['git','show',f2+':'+name],cwd=root,env=env)
        archive = governance.NAMESPACE+'/predecessors/'+name+'.txt'
        put(root,archive,before.decode())
        data['modified_files'][name] = dict(archive=archive,before_sha256=hashlib.sha256(before).hexdigest(),
            before_blob=subprocess.check_output(['git','rev-parse',f2+':'+name],cwd=root,env=env,text=True).strip(),
            after_sha256=sha(root/name))
    name=governance.COMPATIBILITY_TEST
    before=subprocess.check_output(['git','show',f2+':'+name],cwd=root,env=env)
    data['compatibility_test']=dict(path=name,before_sha256=hashlib.sha256(before).hexdigest(),
        before_blob=subprocess.check_output(['git','rev-parse',f2+':'+name],cwd=root,env=env,text=True).strip(),
        after_sha256=sha(root/name))
    data['added_source_files'][governance.ADDED[1]]['sha256'] = sha(root/governance.ADDED[1])
    for key in ('workflow_transitions','proof_input_transitions'):
        data[key] = {name:dict(before=data['modified_files'][name]['before_sha256'],
                              after=data['modified_files'][name]['after_sha256']) for name in governance.WORKFLOWS}
    names = ['skills/presumed-sources/release/historical-preservation.json',
             'skills/presumed-sources/phase-a-contracts/accepted-main-infrastructure-v1.json',
             'skills/presumed-sources/release/phase-a-v1/proof-contract.json',
             'skills/presumed-sources/release/phase-a-v1/governance-source-v2.json']
    data['predecessor_contracts'] = [dict(path=n,sha256=sha(root/n)) for n in names]
    name='build4/release/synthetic-f2-evidence.txt'
    data['preserved_f2_files']={name:dict(sha256=sha(root/name),blob=subprocess.check_output(
        ['git','rev-parse',f2+':'+name],cwd=root,env=env,text=True).strip())}
    # Query the real enumerators in a fresh child; neither executes tests.
    program = "import json; from build4.run_release import source_hashes; from release_population import release_input_hashes; print(json.dumps(dict(tested_python_sha256=source_hashes(),tested_execution_inputs_sha256=release_input_hashes())))"
    child_env={**env,'PYTHONPATH':str(root)+os.pathsep+str(root/'skills/presumed-sources')}
    maps=json.loads(subprocess.check_output([sys.executable,'-c',program],cwd=root,env=child_env,text=True))
    for values in maps.values():
        for name in governance.ADDED: values.pop(name,None)
    json_put(root,'build4/release/synthetic-frozen-maps.json',maps)
    amendment=json.loads((root/governance.AMENDMENT).read_bytes())
    amendment['independent_review'] = synthetic
    for name,row in amendment['successors'].items():
        row['after_sha256'] = row['reviewed_sha256'] = sha(root/name)
        row['reviewed_blob'] = subprocess.check_output(
            ['git','rev-parse',f2+':'+name],cwd=root,env=env,text=True).strip()
        row['change_state'] = 'UNCHANGED_SINCE_IMPLEMENTATION_REVIEW'
    schema=json.loads((root/governance.AMENDMENT_SCHEMA).read_bytes())
    props=schema['properties']['independent_review']['oneOf'][1]['properties']
    for key,value in synthetic.items():props[key]={'const':value}
    schema_path=json_put(root,governance.AMENDMENT_SCHEMA,schema)
    amendment['schema']['sha256'] = sha(schema_path)
    amendment_path=json_put(root,governance.AMENDMENT,amendment)
    substitute(helper,governance.AMENDMENT_SHA256,sha(amendment_path))
    contract=json_put(root,governance.CONTRACT,data)
    substitute(helper,governance.CONTRACT_SHA256,sha(contract))


HISTORICAL_FIXTURE = 'diagnostics/profile12/runner-recovery/independent-qa/test_runner_contract.py'
spec = importlib.util.spec_from_file_location('profile12_historical_runner', ROOT / HISTORICAL_FIXTURE)
historical = importlib.util.module_from_spec(spec)
spec.loader.exec_module(historical)


class IndependentRunnerContract(historical.IndependentRunnerContract):
    @classmethod
    def setUpClass(cls):
        from ci_governance import load_contract
        load_contract(ROOT)  # Structural/pin validation, never production acceptance.
        cls.storage = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.storage.cleanup)
        cls.base = Path(cls.storage.name) / 'base'
        cls.base.mkdir()
        objects = subprocess.check_output(['git', 'rev-parse', '--path-format=absolute',
                                           '--git-path', 'objects'], cwd=ROOT, env=git_environment(), text=True).strip()
        # The fixture commit is an execution input. Host clocks and user Git
        # settings must not move its identity. Run/attempt IDs vary separately.
        cls.env = {**git_environment(),
                   'PATH': str(Path(sys.executable).parent)+os.pathsep+os.environ.get('PATH',''),
                   'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONNOUSERSITE': '1', 'PYTHONPATH': '',
                   'GIT_ALTERNATE_OBJECT_DIRECTORIES': objects,
                   'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_NOSYSTEM': '1',
                   'GIT_AUTHOR_NAME': 'Synthetic QA', 'GIT_COMMITTER_NAME': 'Synthetic QA',
                   'GIT_AUTHOR_EMAIL': 'synthetic@example.invalid', 'GIT_COMMITTER_EMAIL': 'synthetic@example.invalid',
                   'GIT_AUTHOR_DATE': '2000-01-01T00:00:00Z', 'GIT_COMMITTER_DATE': '2000-01-01T00:00:00Z'}
        subprocess.run(['git', 'init', '--template=', '--object-format=sha1', '-q'], cwd=cls.base, env=cls.env, check=True)
        for name in DEPENDENCIES:
            copy_dependency(cls.base, name)
        spec = importlib.util.spec_from_file_location('qa_real_verifier', SOURCE / 'verify_release.py')
        verifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(verifier)
        cls.suites = verifier.SUPPORTED_SUITES
        cls.validators = verifier.VALIDATOR_COMMANDS
        for directory, pattern in cls.suites[:17] + cls.suites[22:]:
            filename = 'independent_review_tests.py' if pattern == 'independent_review_tests.py' else 'test_canary.py'
            put(cls.base, directory + '/' + filename,
                'import unittest\nclass Canary(unittest.TestCase):\n'
                '    def test_executed(self): self.assertEqual(2 + 2, 4)\n')
        # Keep the immutable required identities; substitute only their bodies in
        # this explicitly synthetic fixture. Production never changes its contract.
        required = json.loads((cls.base/'skills/presumed-sources/required-remediation-tests.json').read_bytes())
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
        substitute(vpath, verifier.PRESERVATION_SHA256, sha(preservation))
        substitute(vpath, 'PRESERVATION_COUNT = 8912', 'PRESERVATION_COUNT = 1')
        json_put(cls.base, 'build4/release/investment-property-historical-preservation.json',
                 dict(files={'historical-canary.txt': sha(canary)}))
        for name in ('specialist-migration.json', 'orchestration-migration.json', 'main-proof-migration.json'):
            json_put(cls.base, 'skills/government-grants/release-evidence/historical-qa/' + name,
                     dict(status='PASS', errors=[], files={}))
        put(cls.base, 'build4/release/presumed-sources-accepted-release.json',
            '{"historical": "deliberately stale, untouched"}\n')
        from ci_governance import WORKFLOWS
        for name in WORKFLOWS:
            put(cls.base,name,(ROOT/name).read_text())
        bind_fixture_contracts(cls.base, cls.env)
        bind_ci_fixture(cls.base, cls.env)
        subprocess.run(['git', 'add', '.'], cwd=cls.base, env=cls.env, check=True)
        subprocess.run(['git', '-c', 'user.name=Synthetic QA', '-c', 'user.email=synthetic@example.invalid', 'commit', '-qm', 'Synthetic fixture only'], cwd=cls.base, env=cls.env, check=True)
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
        # Authorise only this deliberate synthetic source revision, retaining
        # the seed maps and receipts unchanged for preservation assertions.
        original_maps = 'build4/release/synthetic-frozen-maps.json'
        failure_maps = 'build4/release/synthetic-failure-maps.json'
        maps=json.loads((self.root/original_maps).read_bytes())
        maps['tested_python_sha256']['tests/test_canary.py']=sha(self.root/'tests/test_canary.py')
        json_put(self.root,failure_maps,maps)
        helper='skills/presumed-sources/ci_governance.py'
        substitute(self.root/helper,original_maps,failure_maps)
        subprocess.run(['git', 'add', 'tests/test_canary.py',helper,failure_maps],
                       cwd=self.root, env=self.env, check=True)
        subprocess.run(['git', '-c', 'user.name=Synthetic QA', '-c', 'user.email=synthetic@example.invalid', 'commit', '-qm', 'Intentional failure fixture'], cwd=self.root, env=self.env, check=True)
        r = self.invoke(self.root, 'qa-failed')
        self.assertNotEqual(r.returncode, 0)
        manifest = json.loads((self.root / 'build4/release/qa-failed/release-regression.json').read_text())
        self.assertFalse(manifest['complete'])
        self.assertGreater(manifest['failed_distinct_tests'],0)
        self.assertFalse((self.root / 'build4/release/qa-failed/execution.json').exists())
        self.unchanged()
