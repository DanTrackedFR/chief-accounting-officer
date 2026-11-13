"""Actual verifier subprocesses in disposable clones; never mutate original evidence."""
import json,os,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(os.environ.get('CAO_DIAGNOSTIC_OUT','/tmp/cao-profile12-diagnostic'));OUT.mkdir(parents=True,exist_ok=True)
REF=os.environ.get('CAO_GOV_REF','36acb611142bc8bedd214622f1ecac539c290056')
SIDECARS=[
 'build4/release/presumed-sources-attempt-ci-41779799873-1/start-source-hashes.json',
 'build4/release/presumed-sources-attempt-ci-41779799873-1/suite-1.json',
 'skills/presumed-sources/release/full-regression-presumed-sources-attempt-ci-41779799873-1.log',
 'skills/presumed-sources/release/workflow-migration/receipt-review.md']
class Governance(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory();cls.addClassCleanup(cls.tmp.cleanup);cls.repo=Path(cls.tmp.name)/'repo'
  subprocess.run(['git','clone','--shared','--no-checkout',str(ROOT),str(cls.repo)],check=True,capture_output=True)
  subprocess.run(['git','checkout','--detach',REF],cwd=cls.repo,check=True,capture_output=True)
  cls.focused=os.environ.get('CAO_GOV_FOCUSED') == '1'
  cls.pointer=None
  if cls.focused:
   receipt=subprocess.run([sys.executable,'diagnostics/profile12/remediation/issue_focused_receipt.py','governance-positive-v1'],cwd=cls.repo,text=True,capture_output=True,check=True,timeout=120)
   cls.pointer=receipt.stdout.strip().splitlines()[-1]
   # The positive control must succeed BEFORE any mutation, not just later by test name.
   valid=subprocess.run([sys.executable,'skills/presumed-sources/verify_release.py','--focused',cls.pointer],cwd=cls.repo,text=True,capture_output=True,timeout=120)
   if valid.returncode:raise RuntimeError('Invalid focused positive control: '+valid.stderr)
   (OUT/'GOV-candidate-positive.json').write_text(json.dumps(dict(source=REF,stdout=valid.stdout,stderr=valid.stderr,exit_code=valid.returncode),indent=2)+'\n')
   import shutil
   shutil.copytree(cls.repo/'diagnostics/profile12/remediation/governance-positive-v1',OUT/'focused-receipt',dirs_exist_ok=True)
   for suffix in ('inventory','pointer'):shutil.copyfile(cls.repo/('diagnostics/profile12/remediation/governance-positive-v1-'+suffix+'.json'),OUT/('focused-'+suffix+'.json'))
  cls.source=subprocess.check_output(['git','rev-parse','HEAD'],cwd=cls.repo,text=True).strip()
 def run_verify(self,label,optimized=False,historical=False):
  command=[sys.executable]+(['-O'] if optimized else [])
  command+=['-c',"import runpy; v=runpy.run_path('skills/presumed-sources/verify_release.py'); print(v['verify_historical']())"] if historical else ['skills/presumed-sources/verify_release.py']
  if self.focused and not historical:command+=['--focused',self.pointer]
  p=subprocess.run(command,cwd=self.repo,text=True,capture_output=True,timeout=120,env={**os.environ,'PYTHONPATH':str(self.repo)})
  (OUT/(label+'.json')).write_text(json.dumps(dict(source=self.source,command=command,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr),indent=2)+'\n')
  return p
 def test_control_intact(self):
  p=self.run_verify('GOV-control-intact');self.assertEqual(p.returncode,0,p.stderr);self.assertIn('focused-governance-qa-v1' if self.focused else '3844',p.stdout)
 def test_GOV_01(self):
  for i,name in enumerate(SIDECARS):
   path=self.repo/name;original=path.read_bytes()
   try:
    path.write_bytes(b'{}\n');p=self.run_verify('GOV-01-'+str(i))
    with self.subTest(sidecar=name):self.assertNotEqual(p.returncode,0,'Tampered sidecar accepted: '+name)
   finally:path.write_bytes(original)
 def test_GOV_02(self):
  path=self.repo/'.github/workflows/cao-orchestration.yml';original=path.read_bytes()
  try:
   path.write_bytes(original+b'\n# unauthorized diagnostic-only mutation\n')
   ordinary=self.run_verify('GOV-02-normal',historical=True)
   self.assertNotEqual(ordinary.returncode,0);self.assertIn('Active successor workflow changed',ordinary.stderr)
   optimized=self.run_verify('GOV-02-optimized',optimized=True,historical=True)
   self.assertNotEqual(optimized.returncode,0,'Optimized Python accepted unauthorized workflow')
  finally:path.write_bytes(original)
 def test_control_bound_log(self):
  pointer=json.loads((self.repo/(self.pointer if self.focused else 'build4/release/presumed-sources-accepted-release.json')).read_text())
  receipt=json.loads((self.repo/pointer['manifest']).read_text());path=self.repo/receipt['logs'][0]['path'];original=path.read_bytes()
  try:
   path.write_bytes(b'{}\n');p=self.run_verify('GOV-control-bound-log');self.assertNotEqual(p.returncode,0);self.assertIn('Presumed-source log changed',p.stderr)
  finally:path.write_bytes(original)
if __name__=='__main__':unittest.main(verbosity=2)
