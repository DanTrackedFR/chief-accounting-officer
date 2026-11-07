"""Independent versioned governance QA; real verifier in disposable candidate clone."""
import contextlib, hashlib, json, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(os.environ.get('CAO_ENGINEERING_OUT',str(Path(__file__).parent/'governance-evidence')))
OUT.mkdir(parents=True,exist_ok=True)
REF=os.environ.get('CAO_ENGINEERING_REF','HEAD')

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

class GovernanceBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory();cls.addClassCleanup(cls.temp.cleanup)
        cls.repo=Path(cls.temp.name)/'candidate'
        subprocess.run(['git','clone','--shared','--no-checkout',str(ROOT),str(cls.repo)],capture_output=True,check=True)
        subprocess.run(['git','checkout','--detach',REF],cwd=cls.repo,capture_output=True,check=True)
        cls.source=subprocess.check_output(['git','rev-parse','HEAD'],cwd=cls.repo,text=True).strip()
        p=subprocess.run([sys.executable,'diagnostics/profile12/remediation/issue_focused_receipt.py','independent-eng-qa-v1'],cwd=cls.repo,text=True,capture_output=True,timeout=150)
        if p.returncode:raise RuntimeError(p.stdout+p.stderr)
        cls.pointer_path=cls.repo/p.stdout.strip().splitlines()[-1]
        cls.pointer=json.loads(cls.pointer_path.read_bytes())
        cls.inventory_path=cls.repo/cls.pointer['evidence_inventory']['path']
        cls.inventory=json.loads(cls.inventory_path.read_bytes())
        cls.manifest_path=cls.repo/cls.pointer['manifest'];cls.attempt=cls.manifest_path.parent
        cls.manifest=json.loads(cls.manifest_path.read_bytes())
        p=cls.invoke('positive-before-any-tampering')
        if p.returncode:raise RuntimeError('Invalid positive control: '+p.stderr)
    @classmethod
    def invoke(cls,label,flags=(),historical=False,full=False):
        command=[sys.executable,*flags]
        if historical:command+=['-c',"import runpy; v=runpy.run_path('skills/presumed-sources/verify_release.py'); print(v['verify_historical']())"]
        else:
            command+=['skills/presumed-sources/verify_release.py']
            if not full:command+=['--focused',str(cls.pointer_path.relative_to(cls.repo))]
        p=subprocess.run(command,cwd=cls.repo,text=True,capture_output=True,timeout=120)
        (OUT/(label+'.json')).write_text(json.dumps(dict(source=cls.source,command=command,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr),indent=2)+'\n')
        return p
    @contextlib.contextmanager
    def changing(self,*paths):
        snapshot={p:(p.read_bytes() if p.exists() else None) for p in paths}
        try:yield
        finally:
            for p,data in snapshot.items():
                if p.exists() or p.is_symlink():p.unlink()
                if data is not None:p.write_bytes(data)
    def reseal(self,inventory):
        self.inventory_path.write_text(json.dumps(inventory,sort_keys=True))
        pointer=dict(self.pointer,evidence_inventory=dict(self.pointer['evidence_inventory'],sha256=digest(self.inventory_path)))
        self.pointer_path.write_text(json.dumps(pointer))
    def reject(self,label,**kwargs):
        p=self.invoke(label,**kwargs);self.assertNotEqual(p.returncode,0,p.stdout)
        return p
    def test_01_positive_receipt_and_historical_preservation(self):
        p=self.invoke('positive-repeat');self.assertEqual(p.returncode,0,p.stderr)
        r=json.loads(p.stdout);self.assertEqual(r['historical_files'],8912);self.assertFalse(r['release_accepted']);self.assertEqual(r['distinct_tests'],19)
    def test_02_additional_sidecar_classes_fail_closed(self):
        for name in ('start-input-hashes.json','suite-0.json','outer.log','receipt-review.md'):
            path=self.attempt/name
            with self.subTest(name=name),self.changing(path):
                path.write_text('{}\n');self.reject('tamper-'+name.replace('.','-'))
    def test_03_inventory_digest_and_omission_fail_closed(self):
        with self.changing(self.inventory_path):
            self.inventory_path.write_text('{}\n');self.reject('inventory-root-digest')
        for name in ('suite-0.json','start-input-hashes.json'):
            with self.subTest(name=name),self.changing(self.inventory_path,self.pointer_path):
                inventory=json.loads(json.dumps(self.inventory));inventory['files'].pop(str((self.attempt/name).relative_to(self.repo)))
                self.reseal(inventory);self.reject('rehashed-omission-'+name)
    def test_04_unlisted_attempt_file_and_required_deletion(self):
        path=self.attempt/'unlisted-evidence.json'
        with self.changing(path):path.write_text('{}');self.reject('unlisted-attempt-evidence')
        path=self.attempt/'start-input-hashes.json'
        with self.changing(path,self.inventory_path,self.pointer_path):
            path.unlink();inventory=json.loads(json.dumps(self.inventory));inventory['files'].pop(str(path.relative_to(self.repo)))
            self.reseal(inventory);self.reject('deleted-required-sidecar')
    def test_05_identical_bytes_symlink_is_rejected(self):
        path=self.attempt/'receipt-review.md';target=self.repo/'qa-symlink-target.txt'
        with self.changing(path,target):
            target.write_bytes(path.read_bytes());path.unlink();path.symlink_to(target)
            self.reject('redirected-identical-review')
    def test_06_rehashed_role_substitution_is_rejected(self):
        path=self.attempt/'receipt-review.md';target=self.repo/'substitute-review.md'
        with self.changing(path,target,self.inventory_path,self.pointer_path):
            path.unlink();target.write_text('{}\n')
            inventory=json.loads(json.dumps(self.inventory));inventory['files'].pop(str(path.relative_to(self.repo)))
            inventory['files'][str(target.relative_to(self.repo))]=digest(target)
            inventory['attestations']['receipt_review']=str(target.relative_to(self.repo))
            self.reseal(inventory);self.reject('rehashed-review-role-substitution')
    def test_07_path_escape_rejected(self):
        with self.changing(self.inventory_path,self.pointer_path):
            inventory=json.loads(json.dumps(self.inventory));inventory['files']['../outside']='0'*64
            self.reseal(inventory);self.reject('inventory-path-escape')
    def test_08_optimized_entrypoints_refuse_even_valid_receipt(self):
        for flag in ('-O','-OO'):
            for historical in (False,True):
                with self.subTest(flag=flag,historical=historical):
                    p=self.reject('optimized-'+flag[1:]+('-historical' if historical else '-focused'),flags=[flag],historical=historical)
                    self.assertIn('Optimized Python is not supported',p.stderr)
    def test_09_stale_full_release_is_not_accepted(self):
        p=self.reject('full-release-stays-unaccepted',full=True)
        self.assertIn('version 2 evidence inventory',p.stderr)
    def test_10_invented_discovery_population_rejected(self):
        suite=self.attempt/'suite-0.json'
        with self.changing(suite,self.manifest_path,self.inventory_path,self.pointer_path):
            manifest=json.loads(json.dumps(self.manifest));manifest['suite_results'][0]['distinct_ids']=['fake::case'+str(i) for i in range(19)]
            self.manifest_path.write_text(json.dumps(manifest))
            suite.write_text(json.dumps({k:v for k,v in manifest['suite_results'][0].items() if k!='exit_code'}))
            inventory=json.loads(json.dumps(self.inventory))
            inventory['files'][str(suite.relative_to(self.repo))]=digest(suite)
            inventory['files'][str(self.manifest_path.relative_to(self.repo))]=digest(self.manifest_path)
            self.inventory_path.write_text(json.dumps(inventory))
            pointer=dict(self.pointer,sha256=digest(self.manifest_path),evidence_inventory=dict(self.pointer['evidence_inventory'],sha256=digest(self.inventory_path)))
            self.pointer_path.write_text(json.dumps(pointer))
            self.reject('invented-test-identities')

if __name__=='__main__':unittest.main(verbosity=2)
