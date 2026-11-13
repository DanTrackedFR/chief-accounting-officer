"""G2 challenges: synthetic seals never authorise the real pending candidate."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'skills/presumed-sources'))
import ci_governance as g


class CIGovernanceMigrationQA(unittest.TestCase):
    def setUp(self):
        self.data = g.load_contract(ROOT)
        self.sealed = copy.deepcopy(self.data)
        self.sealed['state'] = 'SEALED'

    def run_synthetic(self, mutations=None, data=None, action=None):
        """Fault-inject contract bytes; genuine review evidence remains untouched."""
        value = self.sealed if data is None else data
        raw = (json.dumps(value,sort_keys=True,indent=2)+'\n').encode()
        replacements = {ROOT/g.CONTRACT:raw}
        replacements.update(mutations or {})
        original = Path.read_bytes
        def read(path):
            if path in replacements:
                if replacements[path] is None: raise FileNotFoundError(str(path))
                return replacements[path]
            return original(path)
        with patch.object(Path,'read_bytes',read), patch.object(g,'CONTRACT_SHA256',g.sha(raw)):
            return (action or (lambda:g.verify_transition(ROOT)))()

    def assert_invalid_shape(self, data):
        # Re-pin only the in-memory test contract, then call production validation.
        # PendingSealing is not a successful result for any malformed contract.
        raw=(json.dumps(data,sort_keys=True,indent=2)+'\n').encode()
        original=Path.read_bytes
        with patch.object(Path,'read_bytes',lambda p:raw if p==ROOT/g.CONTRACT else original(p)), \
             patch.object(g,'CONTRACT_SHA256',g.sha(raw)):
            with self.assertRaises(g.IntegrityError) as raised:
                g.verify_transition(ROOT)
            self.assertNotIsInstance(raised.exception,g.PendingSealing)

    def rejected(self, name, contents=b'changed\n'):
        with self.assertRaises((ValueError,AssertionError,FileNotFoundError)):
            self.run_synthetic({ROOT/name:contents})

    def test_approved_transition_passes(self):
        if self.data['state'] == 'PENDING_G3':
            with self.assertRaises(g.PendingSealing):g.verify_transition(ROOT)
        else:
            self.assertEqual(g.verify_transition(ROOT)['state'],'SEALED')
        self.assertEqual(self.run_synthetic()['migration_id'],'phase-a-ci-governance-v1')
        pending=copy.deepcopy(self.data);pending['state']='PENDING_G3'
        with self.assertRaises(g.PendingSealing):self.run_synthetic(data=pending)
        # Fake component evidence cannot acquire the genuine published trust root.
        self.rejected(g.AMENDMENT_REVIEW,b'SYNTHETIC COMPONENT EVIDENCE ONLY\n')

    def test_predecessor_git_binding(self):
        data=copy.deepcopy(self.sealed)
        data['modified_files'][g.WORKFLOWS[0]]['before_blob']='0'*40
        with self.assertRaisesRegex(ValueError,'Git binding'):self.run_synthetic(data=data)
        cases=[]
        def variant(label, records):
            value=copy.deepcopy(self.data);value['predecessor_contracts']=records;cases.append((label,value))
        rows=self.data['predecessor_contracts']
        variant('empty',[])
        variant('duplicate path',rows+[rows[0]])
        variant('missing authorised predecessor',rows[1:])
        variant('unexpected predecessor',[*rows,dict(path='docs/HOSTED-CAO.md',sha256='0'*64)])
        variant('not an array',{})
        for label,row in (
            ('missing path',{'sha256':'0'*64}),
            ('missing digest',{'path':rows[0]['path']}),
            ('unknown field',{**rows[0],'authority':'invented'}),
            ('wrong path type',{'path':17,'sha256':'0'*64}),
            ('wrong digest type',{'path':rows[0]['path'],'sha256':17}),
            ('malformed digest',{'path':rows[0]['path'],'sha256':'INVALID'}),
            ('unsafe path',{'path':'../escape','sha256':'0'*64}),
            ('non-object row','not a record')):
            variant(label,[row,*rows[1:]])
        for label,value in cases:
            with self.subTest(predecessor_contracts=label):self.assert_invalid_shape(value)
        wrong=copy.deepcopy(self.sealed);wrong['predecessor_contracts'][0]['sha256']='0'*64
        with self.assertRaisesRegex(g.IntegrityError,'Bound evidence changed'):
            self.run_synthetic(data=wrong)

    def test_historical_predecessor_mutation(self):
        self.rejected('skills/presumed-sources/release/historical-preservation.json')

    def test_f2_archive_mutation(self):
        self.rejected(self.data['modified_files'][g.WORKFLOWS[0]]['archive'])

    def test_legacy_archive_mutation(self):
        self.rejected('skills/presumed-sources/release/workflow-migration/cao-orchestration.v1.yml')

    def test_contract_mutation(self):
        original=Path.read_bytes
        with patch.object(Path,'read_bytes',lambda p:b'{}' if p==ROOT/g.CONTRACT else original(p)):
            with self.assertRaisesRegex(ValueError,'contract changed'):g.load_contract(ROOT)
        # The versioned amendment and original seal are independently pinned.
        for name in (g.AMENDMENT, g.AMENDMENT_SCHEMA, g.PRIOR_CONTRACT):
            self.rejected(name)
        # Fixed schema boundaries beyond predecessor records.
        variants=[]
        for field in ('modified_files','added_source_files','predecessor_commits',
                      'population_extension','preserved_f2_files','workflow_transitions',
                      'proof_input_transitions','compatibility_test'):
            value=copy.deepcopy(self.data);value[field]=[];variants.append((field+' object type',value))
        for field in ('schema','owner_authorization'):
            value=copy.deepcopy(self.data);value[field]['extra']=True;variants.append((field+' unknown field',value))
            value=copy.deepcopy(self.data);value[field]['sha256']='invalid';variants.append((field+' digest',value))
        for field in ('state','schema_version','migration_id'):
            value=copy.deepcopy(self.data);value[field]=None;variants.append((field+' enum/constant',value))
        value=copy.deepcopy(self.data);value['scope_review']['status']='APPROVED';variants.append(('review enum',value))
        value=copy.deepcopy(self.data);value['scope_review']['sha256']='invalid';variants.append(('review digest',value))
        value=copy.deepcopy(self.data);value['scope_review']['extra']=True;variants.append(('review unknown field',value))
        value=copy.deepcopy(self.data);value['population_extension']['additional_ids'].pop();variants.append(('minimum identities',value))
        value=copy.deepcopy(self.data);value['population_extension']['additional_ids'].append('extra');variants.append(('maximum identities',value))
        value=copy.deepcopy(self.data);value['population_extension']['additional_ids'][1]=value['population_extension']['additional_ids'][0];variants.append(('unique identities',value))
        value=copy.deepcopy(self.data);value['preserved_f2_files'].pop(next(iter(value['preserved_f2_files'])));variants.append(('minimum F2 rows',value))
        value=copy.deepcopy(self.data);value['preserved_f2_files']['unexpected']={'sha256':'0'*64,'blob':'0'*40};variants.append(('maximum F2 rows',value))
        value=copy.deepcopy(self.data);value['modified_files'][g.WORKFLOWS[0]]['before_blob']=17;variants.append(('Git blob type',value))
        value=copy.deepcopy(self.data);value['modified_files'][g.WORKFLOWS[0]]['extra']=True;variants.append(('migration unknown field',value))
        for label,value in variants:
            with self.subTest(schema_boundary=label):self.assert_invalid_shape(value)

    def test_scope_review_mutation(self):
        self.rejected(g.NAMESPACE+'/scope-review.md')

    def test_unlisted_workflow_change(self):
        from build4.run_release import source_hashes
        from release_population import release_input_hashes
        values=release_input_hashes();values['.github/workflows/unlisted.yml']='0'*64
        with patch('release_population.release_input_hashes',return_value=values):
            with self.assertRaisesRegex(ValueError,'Unlisted governed'):self.run_synthetic()

    def test_successor_hash_mismatch(self):
        self.rejected(g.WORKFLOWS[0])

    def test_unapproved_verifier_successor(self):
        self.rejected(g.VERIFIER)

    def test_historical_rollback(self):
        for name in g.WORKFLOWS:
            self.rejected(name,(ROOT/self.data['modified_files'][name]['archive']).read_bytes())

    def test_no_default_receipt_fallback(self):
        for name in g.WORKFLOWS[2:]:
            text=(ROOT/name).read_text()
            self.assertIn('check-pointer --pointer "$CAO_PR_POINTER" --sha256 "$CAO_PR_POINTER_SHA256"',text)
            self.assertIn('python -m build4.verify_release --pointer "$CAO_PR_POINTER"',text)
            self.assertNotIn('python -m build4.verify_release\n',text)
            self.assertNotIn('execute_release.py',text)

    def test_missing_or_malformed_pointer(self):
        for name in ('','../escape','build4/release/old.json','/tmp/pointer-v2.json'):
            with self.subTest(name=name),self.assertRaises(ValueError):g._check_pointer(ROOT,name,'0'*64)

    def test_pointer_sha256_mismatch(self):
        path='build4/release/presumed-sources-accepted-42700963367-1-successor-1-v2.json'
        for value in ('','0'*64,'G'*64):
            with self.subTest(value=value),self.assertRaises(ValueError):g._check_pointer(ROOT,path,value)
        self.assertEqual(g._check_pointer(ROOT,path,g.sha((ROOT/path).read_bytes())),path)
        for args in ([],['--pointer',path,'--sha256','0'*64]):
            run=subprocess.run([sys.executable,'skills/presumed-sources/ci_governance.py','check-pointer',*args],cwd=ROOT,capture_output=True,text=True)
            self.assertNotEqual(run.returncode,0)

    def test_changed_map_reuse_rejected(self):
        # Isolate unchanged source-map guards past the deliberately pending proof seal.
        import verify_release as verifier
        path='build4/release/presumed-sources-accepted-42700963367-1-successor-1-v2.json'
        pointer=json.loads((ROOT/path).read_bytes()); manifest=json.loads((ROOT/pointer['manifest']).read_bytes())
        proof=ROOT/'skills/presumed-sources/release/phase-a-v1/http-proof.json'
        with patch.object(verifier,'selected_proof',return_value=proof),patch.object(verifier,'CONTRACT_SHA256',manifest['proof_contract_sha256']):
            with self.assertRaisesRegex(AssertionError,'Python changed after regression'):verifier.verify(path)

    def test_duplicate_population_identity(self):
        from release_population import verify_required_population
        with self.assertRaisesRegex(ValueError,'Duplicate release identities'):
            verify_required_population([{'distinct_ids':['duplicate','duplicate']}])

    def test_omitted_population_identity(self):
        from release_population import verify_required_population,phase_a_required_ids,required_ids
        ids=set(phase_a_required_ids());ids.update(i for r in required_ids() for i in r['distinct_ids'])
        ids.remove(sorted(ids)[0])
        with self.assertRaisesRegex(ValueError,'Missing mandatory'):verify_required_population([{'distinct_ids':sorted(ids)}])
        data=copy.deepcopy(self.sealed);data['population_extension']['additional_ids'].pop()
        with self.assertRaisesRegex(ValueError,'Population extension'):self.run_synthetic(data=data)

    def test_exact_proof_input_overlay(self):
        proof=json.loads((ROOT/'skills/presumed-sources/release/phase-a-v1/proof-contract.json').read_bytes())
        before=proof['proof_inputs_sha256']
        after=self.run_synthetic(action=lambda:g.apply_proof_input_transition(ROOT,before))
        self.assertEqual(set(after),set(before))
        self.assertEqual({n for n in after if after[n]!=before[n]},set(g.WORKFLOWS))
        bad=dict(before);bad[g.WORKFLOWS[0]]='0'*64
        with self.assertRaises(ValueError):self.run_synthetic(action=lambda:g.apply_proof_input_transition(ROOT,bad))
        for field in ('workflow_transitions','proof_input_transitions'):
            value=copy.deepcopy(self.data);value[field][g.WORKFLOWS[0]]['after']='0'*64
            with self.subTest(inconsistent_transition=field):self.assert_invalid_shape(value)
        value=copy.deepcopy(self.data);value['predecessor_commits']['f2']='0'*40
        self.assert_invalid_shape(value)

    def test_proof_or_accounting_source_mutation(self):
        # Full governed closure rejects accounting changes even before proof parsing.
        from build4.run_release import source_hashes
        values=source_hashes();values['skills/source_execution.py']='0'*64
        with patch('build4.run_release.source_hashes',return_value=values):
            with self.assertRaisesRegex(ValueError,'Unlisted governed change'):self.run_synthetic()
        self.rejected('skills/presumed-sources/release/phase-a-v1/proof-contract.json')

    def test_f2_evidence_preserved(self):
        path=next(iter(self.data['preserved_f2_files']))
        self.rejected(path)
        self.assertEqual(len(self.data['preserved_f2_files']),611)

    def test_unsafe_or_duplicate_paths(self):
        with self.assertRaisesRegex(ValueError,'Duplicate JSON'):g._json('{"path":1,"path":2}')
        data=copy.deepcopy(self.sealed)
        data['modified_files'][g.WORKFLOWS[0]]['archive']='../escape'
        with self.assertRaises(ValueError):self.run_synthetic(data=data)
        from receipt_integrity import artifact
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve();(root/'escape').symlink_to(ROOT/g.CONTRACT)
            with self.assertRaises(ValueError):artifact(root,'escape')

    def test_joint_successor_record_forgery(self):
        # Keeping the genuine code pin rejects a jointly rewritten record.
        data=copy.deepcopy(self.data);data['modified_files'][g.WORKFLOWS[0]]['after_sha256']='0'*64
        original=Path.read_bytes;raw=json.dumps(data).encode()
        with patch.object(Path,'read_bytes',lambda p:raw if p==ROOT/g.CONTRACT else original(p)):
            with self.assertRaisesRegex(ValueError,'contract changed'):g.load_contract(ROOT)

    def test_anchor_binding_checked_independently(self):
        # Explicitly synthetic external reviewer snapshot; G3 must provide the real one.
        approved=(ROOT/g.ADDED[0]).read_bytes();expected=hashlib.sha256(approved).hexdigest()
        candidate=approved+b'\n# unauthorized anchor edit\n'
        self.assertNotEqual(hashlib.sha256(candidate).hexdigest(),expected)
        self.assertEqual(self.data['added_source_files'][g.ADDED[0]],{'trust_anchor':'EXTERNAL_G3_GIT_REVIEW'})

    def test_bootstrap_remains_acceptance_pending(self):
        # Execute only 136 trivial methods in the isolated synthetic checkout.
        spec=importlib.util.spec_from_file_location('g2_pending_fixture',ROOT/'tests/fixtures/phase_a_v1/runner.py')
        fixture=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixture)
        # A writable alternate prevents local sandbox permissions from masking
        # borrowed-object reads. All objects/refs below belong to disposable repos.
        storage = tempfile.TemporaryDirectory()
        self.addCleanup(storage.cleanup)
        donor = Path(storage.name)/'donor'; donor.mkdir()
        clean = fixture.git_environment()
        subprocess.run(['git','init','--template=','--object-format=sha1','-q'],cwd=donor,env=clean,check=True)
        name = g.WORKFLOWS[0]
        payload = (ROOT/name).read_bytes()
        blob = subprocess.check_output(['git','hash-object','-w','--stdin'],input=payload,cwd=donor,env=clean).decode().strip()
        objects = donor/'.git/objects'
        original_bind = fixture.bind_ci_fixture
        check_output = subprocess.check_output
        observed = []
        def bind(root, env):
            real_objects = env['GIT_ALTERNATE_OBJECT_DIRECTORIES']
            (objects/'info').mkdir(exist_ok=True)
            alternate = objects/'info/alternates'
            alternate.write_text(real_objects+'\n')
            env['GIT_ALTERNATE_OBJECT_DIRECTORIES'] = str(objects)
            def read(args, *a, **kw):
                if args[0] == 'git' and kw.get('cwd') == root:
                    self.assertIs(kw.get('env'),env, 'Every synthetic Git read must use its explicit environment')
                    if args[:2] == ['git','show'] and args[2].endswith(':'+name):
                        self.assertFalse((root/'.git/objects'/blob[:2]/blob[2:]).exists(),
                                         'Control must borrow the blob rather than mask the defect')
                        missing_context = subprocess.run(args,cwd=root,env=clean,capture_output=True)
                        self.assertNotEqual(missing_context.returncode,0)
                        correct = subprocess.run(args,cwd=root,env=env,capture_output=True)
                        self.assertEqual(correct.returncode,0,correct.stderr)
                        self.assertEqual(correct.stdout,payload)
                        top = check_output(['git','rev-parse','--show-toplevel'],cwd=root,env=env,text=True).strip()
                        self.assertEqual(Path(top),root)
                        object_path = objects/blob[:2]/blob[2:]
                        original = object_path.read_bytes()
                        try:
                            # Withhold both donor blob and fallback store: genuine
                            # missing objects must still reject under the right env.
                            object_path.unlink(); alternate.unlink()
                            absent = subprocess.run(args,cwd=root,env=env,capture_output=True)
                            self.assertNotEqual(absent.returncode,0)
                            object_path.write_bytes(b'corrupt diagnostic object')
                            corrupt = subprocess.run(args,cwd=root,env=env,capture_output=True)
                            self.assertNotEqual(corrupt.returncode,0)
                        finally:
                            object_path.write_bytes(original)
                            alternate.write_text(real_objects+'\n')
                        observed.append(args[2])
                return check_output(args,*a,**kw)
            # Ambient repository overrides must not redirect explicitly isolated
            # reads/writes. Donor deliberately lacks the synthetic predecessor.
            with patch.dict(os.environ, GIT_DIR=str(donor/'.git'), GIT_WORK_TREE=str(donor)), \
                 patch.object(subprocess,'check_output',read):
                original_bind(root,env)
        with patch.object(fixture,'bind_ci_fixture',bind):
            fixture.IndependentRunnerContract.setUpClass()
        self.addCleanup(fixture.IndependentRunnerContract.doClassCleanups)
        self.assertEqual(len(observed),1)
        run=fixture.IndependentRunnerContract.invoke(fixture.IndependentRunnerContract.base,'qa-bootstrap')
        self.assertEqual(run.returncode,0,run.stderr)
        status=json.loads(run.stdout)
        self.assertEqual(status['status'],'REGRESSION_COMPLETE_ACCEPTANCE_PENDING')
        self.assertIs(status['release_accepted'],False)
        if self.data['state'] == 'PENDING_G3':
            with self.assertRaises(g.PendingSealing):g.verify_transition(ROOT)
        source=(ROOT/'skills/presumed-sources/execute_release.py').read_text()
        self.assertIn("status='REGRESSION_COMPLETE_ACCEPTANCE_PENDING', release_accepted=False",source)
        self.assertIn("status='ACCEPTANCE_REUSED'",source)
