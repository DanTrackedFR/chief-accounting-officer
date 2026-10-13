"""Verify current Investment Property acceptance without rewriting historical Build4 evidence."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def verify():
    from build4.run_release import source_hashes,input_hashes
    pointer=json.loads((ROOT/'build4/release/investment-property-pr43-accepted-release.json').read_text())
    manifest_path=ROOT/pointer['manifest']
    assert manifest_path.resolve().is_relative_to(ROOT/'build4/release'),'Acceptance outside release namespace'
    assert digest(manifest_path)==pointer['sha256'],'Investment Property regression manifest hash differs'
    manifest=json.loads(manifest_path.read_text())
    assert manifest['complete'] and manifest['source_unchanged'],'Incomplete Investment Property release'
    assert source_hashes()==manifest['tested_python_sha256'],'Investment Property Python changed after regression'
    assert input_hashes()==manifest['tested_execution_inputs_sha256'],'Investment Property execution inputs changed after regression'
    all_ids=[]
    script='''import json,sys,unittest
suite=unittest.TestLoader().discover(sys.argv[1],pattern=sys.argv[2])
def cases(s):
 for t in s:
  if isinstance(t,unittest.TestSuite):yield from cases(t)
  else:yield t
print(json.dumps(sorted(sys.argv[1]+'::'+t.id() for t in cases(suite))))
'''
    for r in manifest['suite_results']:
        expected=json.loads(subprocess.check_output([sys.executable,'-c',script,r['suite'],r['pattern']],cwd=ROOT,text=True))
        assert expected==r['distinct_ids'] and r['passed'] and not r['skipped'] and not r['failures'] and not r['errors'] and r['exit_code']==0,('Investment Property test receipt differs',r['suite'])
        all_ids.extend(expected)
        for shard in r.get('module_results',[]):assert shard['passed'] and shard['exit_code']==0 and digest(ROOT/shard['log'])==shard['log_sha256']
    assert len(all_ids)==len(set(all_ids))==manifest['executed_distinct_tests'],'Investment Property test count differs'
    assert len(manifest['suite_results'])==17 and len(manifest['logs'])==28,'Investment Property release population incomplete'
    for row in manifest['logs']:assert row['exit_code']==0 and digest(ROOT/row['path'])==row['sha256'],('Investment Property log changed',row['path'])
    # Preserve all merged main files under canonical knowledge and historical
    # accounting namespaces, and every original grants supplement file.
    preserved=json.loads((ROOT/'build4/release/investment-property-historical-preservation.json').read_text())
    for name,h in preserved['files'].items():assert digest(ROOT/name)==h,('Historical accounting evidence changed',name)
    from orchestration.history_references import reference_path
    namespace=ROOT/'skills/government-grants/release-evidence/historical-qa'
    for filename in ('specialist-migration.json','orchestration-migration.json','main-proof-migration.json'):
        report=json.loads((namespace/filename).read_text());assert report['status']=='PASS' and not report['errors']
        for name,row in report['files'].items():assert digest(reference_path(name))==row['current_sha256']
    return dict(status='PASS',distinct_tests=len(all_ids),historical_files=len(preserved['files']))

if __name__=='__main__':print(json.dumps(verify(),sort_keys=True))
