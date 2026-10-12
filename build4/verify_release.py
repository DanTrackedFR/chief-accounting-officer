"""Read-only exact-tree release witness; never regenerates accounting references."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def verify():
    grants_pointer=ROOT/'build4/release/grants-pr27-accepted-release.json'
    if grants_pointer.exists():
        import importlib.util
        spec=importlib.util.spec_from_file_location('grants_release_verifier',ROOT/'skills/government-grants/verify_release.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        return module.verify()
    historical=json.loads((ROOT/'build4/release/historical-inventory.json').read_text())
    preserved=json.loads((ROOT/'recovery/borrowing-costs-pr42/main-historical-preservation.json').read_text())
    assert preserved['status']=='PASS' and not preserved['errors']
    pr42=json.loads((ROOT/'recovery/borrowing-costs-pr42/published-head-manifest.json').read_text())['files']
    for name,expected in historical['files'].items():
        path=ROOT/name
        if name in preserved['files']:
            record=preserved['files'][name]
            assert record['pr42_original_sha256']==pr42[name] and (ROOT/record['main_original_path']).resolve().is_relative_to(ROOT/'recovery/borrowing-costs-pr42/main-original')
            assert record['main_sha256']==expected and digest(path)==record['pr42_original_sha256'],('PR42 original changed',name)
            path=ROOT/record['main_original_path']
        assert digest(path)==expected,('Historical artifact changed',name)
    pointer=json.loads((ROOT/'build4/release/accepted-release.json').read_text())
    manifest_path=ROOT/pointer['manifest']
    assert digest(manifest_path)==pointer['sha256'],'Release manifest hash differs'
    manifest=json.loads(manifest_path.read_text())
    assert manifest['complete'] and manifest['source_unchanged'],'Incomplete final-tree regression'
    sources=manifest['tested_python_sha256']
    from build4.run_release import source_hashes,input_hashes
    actual=source_hashes()
    assert input_hashes()==manifest['tested_execution_inputs_sha256'],'Execution inputs changed since full regression'
    assert actual==sources,'Python population/content changed since full regression'
    all_ids=[]
    for row in manifest['suite_results']:
        # Each release suite runs in a fresh process: identical short module
        # names across directories must not alias during verification either.
        script="""import json,sys,unittest
suite=unittest.TestLoader().discover(sys.argv[1],pattern=sys.argv[2])
def cases(s):
 for t in s:
  if isinstance(t,unittest.TestSuite):yield from cases(t)
  else:yield t
print(json.dumps(sorted(sys.argv[1]+'::'+t.id() for t in cases(suite))))
"""
        expected=json.loads(subprocess.check_output([sys.executable,'-c',script,row['suite'],row['pattern']],cwd=ROOT,text=True))
        assert expected==row['distinct_ids'],('Discovery population differs',row['suite'])
        assert row['passed'] and not row['errors'] and not row['failures'] and not row['skipped'] and row['exit_code']==0
        all_ids.extend(expected)
        for shard in row.get('module_results',[]):
            assert shard['passed'] and shard['exit_code']==0
            assert digest(ROOT/shard['log'])==shard['log_sha256']
    assert len(all_ids)==len(set(all_ids))==manifest['executed_distinct_tests'],'Distinct count differs'
    for row in manifest['logs']:
        assert row['exit_code']==0 and digest(ROOT/row['path'])==row['sha256'],('Gate log mismatch',row['path'])
    proofs=json.loads((ROOT/'build4/release/proof-seeds.json').read_text())
    for row in proofs['proofs']:
        assert row['seeds']==[283,1709] and row['exit_codes']==[0,0] and row['byte_identical']
        assert digest(ROOT/row['reference'])==row['sha256'],'Proof hash mismatch'
    inventory=json.loads((ROOT/'build4/release/artifact-inventory.json').read_text())
    for name,checksum in inventory['files'].items():assert digest(ROOT/name)==checksum,('Artifact hash mismatch',name)
    return dict(status='PASS',distinct_tests=len(all_ids),historical_files=len(historical['files']),python_files=len(actual),proofs=len(proofs['proofs']))

if __name__=='__main__':print(json.dumps(verify(),sort_keys=True))
