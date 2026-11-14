"""Permanent adversarial release infrastructure controls (no full regression)."""
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'skills/presumed-sources'))
sys.path.insert(0,str(ROOT))
from build4.test_outcomes import ObservedResult, observations, validate_outcomes
import proof_selection as proof
import release_population as population
import ci_governance as governance


def verifier():
    spec=importlib.util.spec_from_file_location('phase_a_verifier',ROOT/'skills/presumed-sources/verify_release.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def candidate_preservation(v):
    """Check immutable candidate bytes, without granting a production seal."""
    data = governance.load_contract(ROOT)
    old = json.loads((ROOT/governance.PRIOR_CONTRACT).read_bytes())
    path = ROOT/'skills/presumed-sources/release/historical-preservation.json'
    assert v.digest(path) == v.PRESERVATION_SHA256
    historical = json.loads(path.read_bytes())
    assert len(historical['files']) == v.PRESERVATION_COUNT == 8912
    for name, expected in historical['files'].items():
        if name in governance.WORKFLOWS:
            assert v.digest(ROOT/name) == data['modified_files'][name]['after_sha256'], ('Active workflow changed', name)
        if name == 'docs/HOSTED-CAO.md':
            v.verify_doc_migration(expected)
            continue
        if name == v.ORCHESTRATION_WORKFLOW:
            contract = ROOT/v.MIGRATION_DIRECTORY/'contract-v2.json'
            assert v.digest(contract) == v.MIGRATION_SHA256
            migration = json.loads(contract.read_bytes())
            review = migration['independent_verification']
            assert v.digest(ROOT/review['path']) == review['sha256']
            assert review['other_entries_verified'] == migration['unchanged_entries'] == 8911
            assert migration['predecessor']['sha256'] == v.PRESERVATION_SHA256
            row = migration['migration']
            assert row['original_path'] == row['successor_path'] == name
            assert row['original_sha256'] == expected
            assert v.digest(ROOT/old['modified_files'][name]['archive']) == row['successor_sha256']
            selected = ROOT/row['archived_path']
        else:
            selected = ROOT/old['modified_files'][name]['archive'] if name in governance.WORKFLOWS else ROOT/name
        assert selected.resolve() == selected and selected.resolve().is_relative_to(ROOT)
        assert v.digest(selected) == expected, ('Historical candidate artifact changed', name)
    import accepted_history
    path = ROOT/accepted_history.CONTRACT
    assert v.digest(path) == accepted_history.CONTRACT_SHA256
    main = json.loads(path.read_bytes())
    assert main['baseline'] == governance.BASELINE and len(main['files']) == 7963
    assert set(main['source_migrations']) == {
        'diagnostics/profile12/remediation/issue_focused_receipt.py',
        'skills/presumed-sources/release_population.py', 'skills/presumed-sources/run_release.py',
        'skills/presumed-sources/verify_release.py'}
    maintenance_path = ROOT/governance.MAINTENANCE
    maintenance_raw = maintenance_path.read_bytes()
    assert hashlib.sha256(maintenance_raw).hexdigest() == governance.MAINTENANCE_SHA256
    extension = json.loads(maintenance_raw)['accepted_main_extension']
    assert extension['contract'] == dict(path=accepted_history.CONTRACT,sha256=accepted_history.CONTRACT_SHA256)
    assert extension['baseline'] == main['baseline']
    assert set(extension['migrations']) == {governance.DIAGNOSTIC_TEST}
    assert not set(extension['migrations']) & set(main['source_migrations'])
    for name, expected in main['files'].items():
        row = main['source_migrations'].get(name)
        if row:
            selected = ROOT/old['modified_files'][name]['archive'] if name == governance.VERIFIER else ROOT/name
            assert v.digest(selected) == row['successor_sha256']
            original = (ROOT/row['archive_path']).read_bytes()
            assert hashlib.sha256(original).hexdigest() == row['original_sha256']
        elif name in extension['migrations']:
            row = extension['migrations'][name]
            assert row['archive_path'] == governance.DIAGNOSTIC_ARCHIVE
            original = (ROOT/row['archive_path']).read_bytes()
            assert hashlib.sha256(original).hexdigest() == row['original_sha256']
            assert row['original_blob'] == expected
            active = (ROOT/name).read_bytes()
            assert hashlib.sha256(active).hexdigest() == row['successor_sha256']
            assert hashlib.sha1(b'blob '+str(len(active)).encode()+b'\0'+active).hexdigest() == row['successor_blob']
        else:
            original = (ROOT/name).read_bytes()
        assert hashlib.sha1(b'blob '+str(len(original)).encode()+b'\0'+original).hexdigest() == expected, name
    for name, row in old['preserved_f2_files'].items():
        raw = (ROOT/name).read_bytes()
        assert v.digest(ROOT/name) == row['sha256']
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == row['blob']
    for row in old['modified_files'].values():
        raw = (ROOT/row['archive']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row['before_sha256']
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == row['before_blob']
    assert len(old['preserved_f2_files']) == 611 and len(old['modified_files']) == 9
    return dict(historical=8912, accepted_main=7963, f2=611, archives=9, state=data['state'],
                unchanged_active_files=len(main['files'])-len(main['source_migrations'])-len(extension['migrations']),
                archived_source_migrations=len(main['source_migrations'])+len(extension['migrations']))


class SyntheticProcesses:
    """Reuse the existing disposable fixture; never seal the real candidate."""
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('infrastructure_fixture',ROOT/'tests/fixtures/phase_a_v1/runner.py')
        fixture=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixture)
        cls.fixture=fixture.IndependentRunnerContract
        cls.fixture.setUpClass()
        cls.addClassCleanup(cls.fixture.doClassCleanups)
    def setUp(self):
        storage=tempfile.TemporaryDirectory();self.addCleanup(storage.cleanup)
        self.synthetic=Path(storage.name)/'fixture'
        shutil.copytree(self.fixture.base,self.synthetic)
    def process(self, program):
        return subprocess.run([sys.executable,'-c',"import sys; sys.path.insert(0,'skills/presumed-sources'); "+program],
                              cwd=self.synthetic,env=self.fixture.env,capture_output=True,text=True,timeout=60)
    def positive(self, program):
        result=self.process(program);self.assertEqual(result.returncode,0,result.stderr);return result
    def negative(self, program, message=None):
        result=self.process(program);self.assertNotEqual(result.returncode,0)
        if message:self.assertIn(message,result.stderr)
        return result


class Infrastructure(SyntheticProcesses, unittest.TestCase):
    def test_proof_positive_version_and_arithmetic(self):
        data=governance.load_contract(ROOT)
        if data['state'] != 'SEALED':
            with self.assertRaises(governance.PendingSealing):proof.selected_proof()
        else:
            path=proof.selected_proof();self.assertEqual(proof.verify_output(path)['proof_version'],'phase-a-v1')
        # Genuine algorithms execute against the already-established synthetic
        # fixture, rather than relabelling the pending candidate as approved.
        self.positive("import proof_selection as p; assert p.verify_output(p.selected_proof())['proof_version']=='phase-a-v1'")
        self.assertEqual(hashlib.sha256((ROOT/'skills/presumed-sources/release/http-proof.json').read_bytes()).hexdigest(),
                         'be06ab1a1ee247bc24159f7ad605eb30c1dc70fccb13c864b50a9da25e88bcb7')
    def test_selector_cli_without_pythonpath(self):
        command=[sys.executable,'skills/presumed-sources/proof_selection.py','--version','phase-a-v1',
                 '--output','skills/presumed-sources/release/phase-a-v1/http-proof.json']
        env={k:v for k,v in os.environ.items() if k!='PYTHONPATH'}
        result=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True)
        if governance.load_contract(ROOT)['state'] != 'SEALED':
            self.assertNotEqual(result.returncode,0);self.assertIn('PendingSealing',result.stderr)
        else:
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(json.loads(result.stdout)['proof_version'],'phase-a-v1')
        env={k:v for k,v in self.fixture.env.items() if k!='PYTHONPATH'}
        control=subprocess.run(command,cwd=self.synthetic,env=env,capture_output=True,text=True)
        self.assertEqual(control.returncode,0,control.stderr)
        self.assertEqual(json.loads(control.stdout)['proof_version'],'phase-a-v1')
    def test_proof_wrong_version(self):
        with self.assertRaises(ValueError):proof.selected_proof('historical')
    def test_proof_missing_stale_tampered_and_contract(self):
        for target in ('http-proof.json','proof-contract.json'):
            with self.subTest(target=target):
                path=self.synthetic/'skills/presumed-sources/release/phase-a-v1'/target
                original=path.read_bytes()
                try:
                    path.write_bytes(b'{}\n')
                    self.negative('import proof_selection as p; p.selected_proof()')
                finally:path.write_bytes(original)
        path=self.synthetic/'skills/presumed-sources/release/phase-a-v1/http-proof.json'
        original=path.read_bytes()
        try:
            path.unlink();self.negative('import proof_selection as p; p.selected_proof()')
        finally:path.write_bytes(original)
        self.negative("import proof_selection as p; p.verify_output('skills/presumed-sources/release/http-proof.json')")
    def test_proof_source_and_execution_input_mismatch(self):
        for key in ('accounting_source_sha256','proof_inputs_sha256'):
            with self.subTest(key=key):
                program="""import json,proof_selection as p
from unittest.mock import patch
data=json.loads((p.ROOT/p.CONTRACT).read_bytes())
target=next(iter(data[KEY])); original=p.digest
def changed(path):return '0'*64 if str(path.relative_to(p.ROOT))==target else original(path)
with patch.object(p,'digest',changed):p.selected_proof()
""".replace('KEY',repr(key))
                self.negative(program,'source/input mismatch')
    def test_unexpected_numerical_divergence(self):
        self.negative("""import json,tempfile,proof_selection as p
from pathlib import Path
data=json.loads(p.selected_proof().read_bytes());data['executions'][0]['calculations'][0]['amount']='64801'
with tempfile.TemporaryDirectory() as d:
 path=Path(d)/'mutated.json';path.write_text(json.dumps(data));p.verify_output(path)
""",'output differs')
    def test_historical_and_explicit_migrations(self):
        result=candidate_preservation(verifier())
        self.assertEqual((result['historical'],result['accepted_main']),(8912,7963))
        self.assertEqual((result['unchanged_active_files'],result['archived_source_migrations']),(7958,5))
        if result['state'] != 'SEALED':
            with self.assertRaises(governance.PendingSealing):verifier().verify_historical()
        else:self.assertEqual(verifier().verify_historical(),8912)
        self.positive('import verify_release as v; assert v.verify_historical()==1')
    def test_doc_migration_missing_wrong_old_new_and_future_doc(self):
        v=verifier();original=v.digest
        historical=json.loads((ROOT/'skills/presumed-sources/release/historical-preservation.json').read_bytes())
        expected=historical['files']['docs/HOSTED-CAO.md']
        targets=[v.DOC_MIGRATION,'docs/HOSTED-CAO.md','skills/presumed-sources/phase-a-contracts/HOSTED-CAO.original.md']
        for target in targets:
            with self.subTest(target=target),patch.object(v,'digest',lambda p:'0'*64 if str(p.relative_to(ROOT))==target else original(p)):
                if target == v.DOC_MIGRATION:
                    with self.assertRaises(ValueError):v.verify_doc_migration(expected)
        read=Path.read_bytes
        for target in targets[1:]:
            with self.subTest(target=target),patch.object(Path,'read_bytes',lambda p:read(p)+b'\n# mutation' if str(p.relative_to(ROOT))==target else read(p)):
                with self.assertRaises(ValueError):v.verify_doc_migration(expected)
        with patch.object(v,'artifact',side_effect=ValueError('Missing migration')):
            with self.assertRaises(ValueError):v.verify_doc_migration(expected)
        with self.assertRaises(ValueError):v.verify_doc_migration('0'*64)
    def test_unrelated_historical_mutation_rejected(self):
        v=verifier();original=v.digest
        manifest=json.loads((ROOT/'skills/presumed-sources/release/historical-preservation.json').read_bytes())
        target=next(n for n in manifest['files'] if n not in ('docs/HOSTED-CAO.md',v.ORCHESTRATION_WORKFLOW))
        with patch.object(v,'digest',lambda p:'0'*64 if str(p.relative_to(ROOT))==target else original(p)):
            with self.assertRaises(AssertionError):candidate_preservation(v)
    def test_optimized_verifier_refuses(self):
        for flag in ('-O','-OO'):
            p=subprocess.run([sys.executable,flag,'-c',"import runpy; runpy.run_path('skills/presumed-sources/verify_release.py')['verify_historical']()"],cwd=ROOT,capture_output=True,text=True)
            self.assertNotEqual(p.returncode,0);self.assertIn('Optimized Python is not supported',p.stderr)
    def test_required_55_and_historical_63_omission_duplicate(self):
        historical=[i for row in population.required_ids() for i in row['distinct_ids']]
        phase=population.phase_a_required_ids();self.assertEqual(len(historical),63);self.assertEqual(len(phase),55)
        ids=sorted(historical+phase);self.assertEqual(population.verify_required_population([{'distinct_ids':ids}]),118)
        for removed in (historical[0],phase[0]):
            with self.subTest(removed=removed),self.assertRaises(ValueError):population.verify_required_population([{'distinct_ids':[i for i in ids if i!=removed]}])
        with self.assertRaises(ValueError):population.verify_required_population([{'distinct_ids':ids+[ids[0]]}])
    def test_original_49_pass_14_setup_unexecuted(self):
        class Good(unittest.TestCase):pass
        for i in range(49):setattr(Good,'test_'+str(i),lambda self:None)
        class Bad(unittest.TestCase):
            @classmethod
            def setUpClass(cls):raise RuntimeError('original preservation setup failure')
        for i in range(14):setattr(Bad,'test_'+str(i),lambda self:None)
        suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(Good),unittest.defaultTestLoader.loadTestsFromTestCase(Bad)])
        scheduled=sorted('synthetic::'+t.id() for group in suite for t in group)
        result=unittest.TextTestRunner(stream=io.StringIO(),resultclass=ObservedResult).run(suite)
        row=dict(distinct_ids=scheduled,tests=result.testsRun,errors=len(result.errors),failures=len(result.failures),skipped=len(result.skipped),passed=result.wasSuccessful(),exit_code=1,**observations(result,'synthetic',scheduled))
        self.assertEqual(len(row['executed_ids']),49);self.assertEqual(len(row['passed_ids']),49);self.assertEqual(len(row['unexecuted_ids']),14)
        validate_outcomes(row,successful=False)
        with self.assertRaises(ValueError):validate_outcomes(row)
        forged=copy.deepcopy(row);forged.update(executed_ids=scheduled,tests=63,passed=True,errors=0,exit_code=0)
        with self.assertRaises(ValueError):validate_outcomes(forged)
    def test_skips_failures_errors_subtests_and_truncation(self):
        class Cases(unittest.TestCase):
            def test_pass(self):pass
            @unittest.skip('required cannot skip')
            def test_skip(self):pass
            def test_failure(self):self.fail('fail')
            def test_error(self):raise RuntimeError('error')
            def test_subtest(self):
                with self.subTest(x=1):self.fail('subtest')
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(Cases);ids=sorted('sample::'+t.id() for t in suite)
        result=unittest.TextTestRunner(stream=io.StringIO(),resultclass=ObservedResult).run(suite)
        row=dict(distinct_ids=ids,tests=result.testsRun,errors=len(result.errors),failures=len(result.failures),skipped=len(result.skipped),passed=False,exit_code=1,**observations(result,'sample',ids))
        validate_outcomes(row,False);self.assertEqual(len(row['executed_ids']),4)
        with self.assertRaises(ValueError):validate_outcomes(row)
        for key in ('executed_ids','passed_ids','scheduled_ids','suite_errors'):
            bad=copy.deepcopy(row);bad.pop(key)
            with self.subTest(key=key),self.assertRaises(ValueError):validate_outcomes(bad)


class ReceiptAdversarial(SyntheticProcesses, unittest.TestCase):
    """Simulated rows exercise receipt rejection; never assert execution/acceptance."""
    def model(self):
        seed=json.loads((self.synthetic/'build4/release/qa-seed/release-regression.json').read_bytes())
        return self,seed
    def validate_population(self, data):
        result=subprocess.run([sys.executable,'-c',
            "import sys,json; sys.path.insert(0,'skills/presumed-sources'); from verify_release import validate_population; validate_population(json.load(sys.stdin))"],
            cwd=self.synthetic,env=self.fixture.env,input=json.dumps(data),capture_output=True,text=True,timeout=60)
        if result.returncode:raise ValueError(result.stderr)
    def test_population_semantics_positive_and_negative(self):
        v,d=self.model()
        if governance.load_contract(ROOT)['state'] != 'SEALED':
            with self.assertRaises(governance.PendingSealing):verifier().validate_population(d)
        v.validate_population(d)
        bad=copy.deepcopy(d);bad.pop('discovered_distinct_tests')
        with self.assertRaises(ValueError):v.validate_population(bad)
        for kind in ('executed_ids','passed_ids','scheduled_ids'):
            bad=copy.deepcopy(d);bad['suite_results'][1][kind]=[]
            with self.subTest(kind=kind),self.assertRaises(ValueError):v.validate_population(bad)
        for field in ('discovered_distinct_tests','executed_distinct_tests','passed_distinct_tests','proof_version','proof_sha256','proof_contract_sha256'):
            bad=copy.deepcopy(d);bad[field]='tampered'
            with self.subTest(field=field),self.assertRaises(ValueError):v.validate_population(bad)
        for key in ('failed','errored','skipped','unexecuted'):
            bad=copy.deepcopy(d);bad[key+'_distinct_tests']=False
            with self.subTest(boolean_counter=key),self.assertRaises(ValueError):v.validate_population(bad)
        for identity in (population.phase_a_required_ids()[0],population.required_ids()[0]['distinct_ids'][0]):
            bad=copy.deepcopy(d)
            for row in bad['suite_results']:
                for key in ('distinct_ids','discovered_ids','scheduled_ids','executed_ids','passed_ids'):
                    row[key]=[i for i in row[key] if i!=identity]
                row['tests']=len(row['executed_ids'])
            from build4.test_outcomes import aggregate
            bad['outcomes']=aggregate(bad['suite_results'])
            for k in ('discovered','scheduled','executed','passed'):bad[k+'_distinct_tests']=len(bad['outcomes'][k+'_ids'])
            with self.subTest(identity=identity),self.assertRaises(ValueError):v.validate_population(bad)
        bad=copy.deepcopy(d);bad.update(scope='bounded-remediation-preflight',release_accepted=False)
        with self.assertRaises(ValueError):v.validate_population(bad)
    def test_source_commit_binding(self):
        commit=population.source_commit();n='docs/HOSTED-CAO.md';h=hashlib.sha256((ROOT/n).read_bytes()).hexdigest()
        self.assertTrue(population.verify_source_binding(commit,{}, {n:h}))
        for revision,expected in (('97d0621331c6ad2a66b12ed09c0ec40c05c626b9',h),(commit,'0'*64)):
            with self.subTest(revision=revision),self.assertRaises(ValueError):population.verify_source_binding(revision,{}, {n:expected})
    def test_build4_rejects_historical_pointer_and_missing_receipt(self):
        for extra in ([],['--pointer','build4/release/presumed-sources-accepted-release.json']):
            p=subprocess.run([sys.executable,'build4/verify_release.py',*extra],cwd=ROOT,text=True,capture_output=True)
            self.assertNotEqual(p.returncode,0)

if __name__=='__main__':unittest.main(verbosity=2)
