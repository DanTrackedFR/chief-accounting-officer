"""Complete distinct release discovery, isolated suites, immutable source receipts."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

ROOT=Path(__file__).resolve().parents[2]
ATTEMPT=os.environ.get('CAO_IP_ATTEMPT','investment-property-pr43-attempt-001')
if not ATTEMPT.replace('-','').isalnum():raise ValueError('Invalid release attempt')
os.environ['CAO_BUILD4_ATTEMPT']=ATTEMPT
sys.path.insert(0,str(ROOT))
from build4.run_release import source_hashes,input_hashes
OUT=ROOT/'build4/release'/ATTEMPT


def release():
    if OUT.exists():raise SystemExit('Preserve prior attempt; choose new CAO_IP_ATTEMPT')
    OUT.mkdir(parents=True)
    before_source=source_hashes();before_input=input_hashes()
    (OUT/'start-source-hashes.json').write_text(json.dumps(before_source,sort_keys=True,indent=2)+'\n')
    (OUT/'start-input-hashes.json').write_text(json.dumps(before_input,sort_keys=True,indent=2)+'\n')
    prior=json.loads((ROOT/'local_cao/release/release-regression.json').read_text())
    suites=[(x['suite'],x['pattern']) for x in prior['suite_results']]+[('knowledge/borrowing-costs','test*.py'),('hosted_cao/tests','test_*.py'),('intelligence/tests','test_*.py'),('build4/tests','test_*.py'),('knowledge/government-grants','test_*.py'),('knowledge/investment-property','test_*.py')]
    validators=[x['command'] for x in prior['validators']]+['knowledge/borrowing-costs/validate_supplement.py','knowledge/government-grants/validate_supplement.py','knowledge/investment-property/validate_supplement.py']
    def run(args,name,timeout=14400):
        log=OUT/(name+'.log');started=time.monotonic()
        with log.open('w') as f:
            try:code=subprocess.run(args,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,timeout=timeout,env={**os.environ,'PYTHONHASHSEED':'19'}).returncode
            except subprocess.TimeoutExpired:code=124
        return dict(command=args,exit_code=code,path=str(log.relative_to(ROOT)),sha256=hashlib.sha256(log.read_bytes()).hexdigest(),seconds=round(time.monotonic()-started,3))
    def suite(item):
        i,(directory,pattern)=item
        receipt=run([sys.executable,'-m','build4.run_release','suite',directory,pattern,str(i)],'suite-'+str(i))
        path=OUT/('suite-'+str(i)+'.json')
        data=json.loads(path.read_text()) if path.exists() else dict(suite=directory,pattern=pattern,tests=0,distinct_ids=[],errors=1,failures=0,skipped=0,passed=False)
        data['exit_code']=receipt['exit_code']
        print(json.dumps(dict(suite=directory,tests=data['tests'],exit_code=data['exit_code'])),flush=True)
        return data,receipt
    with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(suite,enumerate(suites)))
    records=[r[0] for r in results];logs=[r[1] for r in results]
    for i,cmd in enumerate(validators):
        logs.append(run([sys.executable,cmd],'validator-'+str(i),600))
        print(json.dumps(dict(validator=cmd,exit_code=logs[-1]['exit_code'])),flush=True)
    logs.append(run(['git','diff','--check'],'diff-check',30))
    ids=[i for r in records for i in r['distinct_ids']]
    unchanged=before_source==source_hashes() and before_input==input_hashes()
    complete=unchanged and len(ids)==len(set(ids)) and len(records)==len(suites) and all(r['passed'] and not r['skipped'] and not r['errors'] and not r['failures'] and r['exit_code']==0 for r in records) and all(l['exit_code']==0 for l in logs)
    value=dict(baseline_main='e75375b84813b9d584db12aa692b2f4d16baf052',baseline_pr='a66a43b54f1c72a9eea686589173d94c5138384d',attempt=ATTEMPT,complete=complete,source_unchanged=unchanged,executed_distinct_tests=len(set(ids)),suite_results=records,logs=logs,tested_python_sha256=before_source,tested_execution_inputs_sha256=before_input,historical_artifacts_regenerated=False)
    (OUT/'release-regression.json').write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(complete=complete,tests=len(set(ids)),source_unchanged=unchanged)),flush=True)
    return 0 if complete else 1

if __name__=='__main__':sys.exit(release())
