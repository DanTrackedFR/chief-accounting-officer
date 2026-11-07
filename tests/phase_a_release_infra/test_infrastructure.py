"""Permanent adversarial release infrastructure controls (no full regression)."""
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
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


def verifier():
    spec=importlib.util.spec_from_file_location('phase_a_verifier',ROOT/'skills/presumed-sources/verify_release.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


class Infrastructure(unittest.TestCase):
    def test_proof_positive_version_and_arithmetic(self):
        path=proof.selected_proof();self.assertEqual(proof.verify_output(path)['proof_version'],'phase-a-v1')
        self.assertEqual(hashlib.sha256((ROOT/'skills/presumed-sources/release/http-proof.json').read_bytes()).hexdigest(),
                         'be06ab1a1ee247bc24159f7ad605eb30c1dc70fccb13c864b50a9da25e88bcb7')
    def test_proof_wrong_version(self):
        with self.assertRaises(ValueError):proof.selected_proof('historical')
    def test_proof_missing_stale_tampered_and_contract(self):
        # In-memory path substitutions avoid mutating the candidate during preflight.
        for target in ('http-proof.json','proof-contract.json'):
            original=Path.read_bytes
            def altered(path):
                if str(path).endswith('phase-a-v1/'+target):return b'{}\n'
                return original(path)
            with self.subTest(target=target),patch.object(Path,'read_bytes',altered):
                with self.assertRaises(ValueError):proof.selected_proof()
        original=proof.artifact
        def missing(root,name):
            if name.endswith('phase-a-v1/http-proof.json'):raise ValueError('Missing successor proof')
            return original(root,name)
        with patch.object(proof,'artifact',missing):
            with self.assertRaises(ValueError):proof.selected_proof()
        with tempfile.TemporaryDirectory() as d:
            stale=Path(d)/'old.json';stale.write_bytes((ROOT/'skills/presumed-sources/release/http-proof.json').read_bytes())
            with self.assertRaises(ValueError):proof.verify_output(stale)
    def test_proof_source_and_execution_input_mismatch(self):
        data=json.loads((ROOT/proof.CONTRACT).read_bytes())
        for key in ('accounting_source_sha256','proof_inputs_sha256'):
            target=next(iter(data[key]));original=proof.digest
            def changed(path):return '0'*64 if str(path.relative_to(ROOT))==target else original(path)
            with self.subTest(key=key),patch.object(proof,'digest',changed):
                with self.assertRaisesRegex(ValueError,'source/input mismatch'):proof.selected_proof()
    def test_unexpected_numerical_divergence(self):
        data=json.loads(proof.selected_proof().read_bytes());data['executions'][0]['calculations'][0]['amount']='64801'
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'mutated.json';path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError,'output differs'):proof.verify_output(path)
    def test_historical_and_explicit_migrations(self):
        self.assertEqual(verifier().verify_historical(),8912)
    def test_doc_migration_missing_wrong_old_new_and_future_doc(self):
        v=verifier();original=v.digest
        targets=[v.DOC_MIGRATION,'docs/HOSTED-CAO.md','skills/presumed-sources/phase-a-contracts/HOSTED-CAO.original.md']
        for target in targets:
            with self.subTest(target=target),patch.object(v,'digest',lambda p:'0'*64 if str(p.relative_to(ROOT))==target else original(p)):
                # Archive and document hash use exact bytes, so exercise actual bytes there.
                if target==v.DOC_MIGRATION:
                    with self.assertRaises(ValueError):v.verify_historical()
        read=Path.read_bytes
        for target in targets[1:]:
            with self.subTest(target=target),patch.object(Path,'read_bytes',lambda p:read(p)+b'\n# mutation' if str(p.relative_to(ROOT))==target else read(p)):
                with self.assertRaises(ValueError):v.verify_historical()
        with patch.object(v,'artifact',side_effect=ValueError('Missing migration')):
            with self.assertRaises(ValueError):v.verify_doc_migration('0'*64)
        with self.assertRaises(ValueError):v.verify_doc_migration('0'*64)
    def test_unrelated_historical_mutation_rejected(self):
        v=verifier();original=v.digest
        manifest=json.loads((ROOT/'skills/presumed-sources/release/historical-preservation.json').read_bytes())
        target=next(n for n in manifest['files'] if n not in ('docs/HOSTED-CAO.md',v.ORCHESTRATION_WORKFLOW))
        with patch.object(v,'digest',lambda p:'0'*64 if str(p.relative_to(ROOT))==target else original(p)):
            with self.assertRaises(AssertionError):v.verify_historical()
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


class ReceiptAdversarial(unittest.TestCase):
    """Simulated rows exercise receipt rejection; never assert execution/acceptance."""
    def model(self):
        from build4.test_outcomes import aggregate
        v=verifier();required=population.phase_a_required_ids()+[i for r in population.required_ids() for i in r['distinct_ids']]
        rows=[]
        for directory,pattern in population.SUPPORTED_SUITES:
            ids=sorted(i for i in required if i.startswith(directory+'::') and
                       __import__('fnmatch').fnmatch(i.split('::')[1].split('.')[0]+'.py',pattern))
            if not ids:ids=[directory+'::simulation.'+pattern+'.method']
            row=dict(suite=directory,pattern=pattern,tests=len(ids),distinct_ids=ids,discovered_ids=ids,scheduled_ids=ids,
                     executed_ids=ids,passed_ids=ids,failed_ids=[],errored_ids=[],skipped_ids=[],unexecuted_ids=[],suite_errors=[],
                     outcome_schema_version=1,passed=True,exit_code=0,skipped=0,errors=0,failures=0)
            if directory=='orchestration/tests':row.update(exact_discovery_population=True,module_results=[dict(row)])
            rows.append(row)
        plan=population.gate_plan('simulation','1'*40)
        logs=[dict(command=r['command'],environment=r['environment'],exit_code=0) for r in plan]
        logs += [dict(command=['python',c],environment={'PYTHONHASHSEED':'19'},exit_code=0) for c in population.VALIDATOR_COMMANDS]
        logs += [dict(command=['git','diff','--check'],environment={},exit_code=0)]
        outcomes=aggregate(rows)
        d=dict(source_commit='1'*40,attempt='simulation',suite_results=rows,logs=logs,gate_plan=plan,
               outcome_schema_version=1,outcomes=outcomes,proof_version=proof.VERSION,proof_contract_sha256=proof.CONTRACT_SHA256,
               proof_sha256=hashlib.sha256(proof.selected_proof().read_bytes()).hexdigest())
        for k in ('scheduled','executed','passed','failed','errored','skipped','unexecuted','discovered'):d[k+'_distinct_tests']=len(outcomes[k+'_ids'])
        return v,d
    def test_population_semantics_positive_and_negative(self):
        v,d=self.model();v.validate_population(d)
        bad=copy.deepcopy(d);bad.pop('discovered_distinct_tests')
        with self.assertRaises(ValueError):v.validate_population(bad)
        for kind in ('executed_ids','passed_ids','scheduled_ids'):
            bad=copy.deepcopy(d);bad['suite_results'][1][kind]=[]
            with self.subTest(kind=kind),self.assertRaises(ValueError):v.validate_population(bad)
        for field in ('discovered_distinct_tests','executed_distinct_tests','passed_distinct_tests','proof_version','proof_sha256','proof_contract_sha256'):
            bad=copy.deepcopy(d);bad[field]='tampered'
            with self.subTest(field=field),self.assertRaises(ValueError):v.validate_population(bad)
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
