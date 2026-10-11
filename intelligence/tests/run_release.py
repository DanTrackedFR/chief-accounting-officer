"""Bounded subprocess suites with actual distinct test IDs and durable evidence."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'intelligence/release'

def one_suite(directory,pattern,index):
    loader=unittest.TestLoader();suite=loader.discover(directory,pattern=pattern)
    def cases(s):
        for t in s:
            if isinstance(t,unittest.TestSuite):yield from cases(t)
            else:yield t
    ids=sorted(directory+'::'+t.id() for t in cases(suite))
    started=time.monotonic();result=unittest.TextTestRunner(verbosity=2).run(suite)
    record={'suite':directory,'pattern':pattern,'distinct_ids':ids,'tests':result.testsRun,'errors':len(result.errors),'failures':len(result.failures),'skipped':len(result.skipped),'seconds':round(time.monotonic()-started,3),'passed':result.wasSuccessful()}
    (OUT/f'suite-{index}.json').write_text(json.dumps(record,indent=2)+'\n')
    return 0 if result.wasSuccessful() else 1

def release():
    OUT.mkdir(exist_ok=True)
    prior=json.loads((ROOT/'local_cao/release/release-regression.json').read_text())
    suites=[(x['suite'],x['pattern']) for x in prior['suite_results']]+[('hosted_cao/tests','test_*.py'),('intelligence/tests','test_*.py')]
    records=[];logs=[]
    def run(args,name,timeout=14400):
        path=OUT/(name+'.log');started=time.monotonic()
        with path.open('w') as f:
            try:r=subprocess.run(args,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,timeout=timeout,env={**os.environ,'PYTHONHASHSEED':'19'});code=r.returncode
            except subprocess.TimeoutExpired:code=124
        logs.append({'path':str(path.relative_to(ROOT)),'exit_code':code,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size,'seconds':round(time.monotonic()-started,3)})
        return code
    for i,(directory,pattern) in enumerate(suites):
        code=run([sys.executable,'-m','intelligence.tests.run_release','suite',directory,pattern,str(i)],f'suite-{i}')
        record=json.loads((OUT/f'suite-{i}.json').read_text()) if (OUT/f'suite-{i}.json').exists() else {'passed':False,'tests':0,'distinct_ids':[]}
        record['exit_code']=code;records.append(record)
        print(json.dumps({'suite':directory,'tests':record['tests'],'exit_code':code}),flush=True)
        save(records,logs)
        if code:raise SystemExit(code)
    for i,v in enumerate(prior['validators']):
        code=run([sys.executable,v['command']],f'validator-{i}',600);save(records,logs)
        if code:raise SystemExit(code)
    code=run(['git','diff','--check'],'diff-check',30);save(records,logs)
    if code:raise SystemExit(code)

def save(records,logs):
    ids=sorted({i for r in records for i in r['distinct_ids']})
    sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['intelligence','hosted_cao','local_cao','orchestration','skills','interfaces'] for p in (ROOT/folder).rglob('*.py')}
    value={'baseline':'0523543fb1da0e8b8d05f05e93148ffc3b29cd70','executed_distinct_tests':len(ids),'suite_results':records,'logs':logs,'tested_python_sha256':sources,'complete':len(records)==13 and len(logs)==21 and all(x['exit_code']==0 for x in logs),'historical_artifacts_regenerated':False}
    (OUT/'release-regression.json').write_text(json.dumps(value,indent=2)+'\n')

if __name__=='__main__':
    if len(sys.argv)>1:sys.exit(one_suite(sys.argv[2],sys.argv[3],sys.argv[4]))
    release()
