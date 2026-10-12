"""Bounded subprocess suites with actual distinct test IDs and durable evidence."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest
from concurrent.futures import ThreadPoolExecutor

ROOT=Path(__file__).resolve().parents[1]
ATTEMPT=os.environ.get('CAO_BUILD4_ATTEMPT','attempt-001')
if not ATTEMPT.replace('-','').isalnum():raise ValueError('Invalid release attempt')
OUT=ROOT/'build4/release'/ATTEMPT

def one_suite(directory,pattern,index):
    OUT.mkdir(parents=True,exist_ok=True)
    if directory=='orchestration/tests' and pattern=='test_*.py':
        # Same discovery population, isolated module subprocesses; no tests skipped.
        started=time.monotonic();modules=sorted((ROOT/directory).glob(pattern))
        def shard(entry):
            i,path=entry;label=str(index)+'-module-'+str(i);log=OUT/(label+'.log');started_ns=time.time_ns()
            with log.open('w') as f:
                try:code=subprocess.run([sys.executable,'-m','build4.run_release','suite',directory,path.name,label],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,timeout=14400).returncode
                except subprocess.TimeoutExpired:code=124
            file=OUT/('suite-'+label+'.json')
            r=json.loads(file.read_text()) if file.exists() and file.stat().st_mtime_ns>=started_ns else dict(tests=0,errors=1,failures=0,skipped=0,distinct_ids=[],passed=False)
            r.update(exit_code=code,log=str(log.relative_to(ROOT)),log_sha256=hashlib.sha256(log.read_bytes()).hexdigest())
            print(json.dumps(dict(module=path.name,tests=r['tests'],exit_code=code)),flush=True)
            return r
        with ThreadPoolExecutor(max_workers=7) as pool:records=list(pool.map(shard,enumerate(modules)))
        ids=[i for r in records for i in r['distinct_ids']]
        loader=unittest.TestLoader();suite=loader.discover(directory,pattern=pattern)
        def cases(s):
            for t in s:
                if isinstance(t,unittest.TestSuite):yield from cases(t)
                else:yield t
        expected=sorted(directory+'::'+t.id() for t in cases(suite))
        complete=sorted(ids)==expected and len(ids)==len(set(ids))
        value=dict(suite=directory,pattern=pattern,distinct_ids=sorted(ids),tests=sum(r['tests'] for r in records),errors=sum(r['errors'] for r in records),failures=sum(r['failures'] for r in records),skipped=sum(r['skipped'] for r in records),seconds=round(time.monotonic()-started,3),passed=complete and all(r['exit_code']==0 and r['passed'] for r in records),module_results=records,exact_discovery_population=complete)
        (OUT/f'suite-{index}.json').write_text(json.dumps(value,indent=2)+'\n')
        return 0 if value['passed'] else 1
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
    if OUT.exists():raise SystemExit('Preserve prior attempt; select a new CAO_BUILD4_ATTEMPT')
    OUT.mkdir(parents=True)
    (OUT/'start-source-hashes.json').write_text(json.dumps(source_hashes(),sort_keys=True,indent=2)+'\n')
    (OUT/'start-input-hashes.json').write_text(json.dumps(input_hashes(),sort_keys=True,indent=2)+'\n')
    prior=json.loads((ROOT/'local_cao/release/release-regression.json').read_text())
    suites=[(x['suite'],x['pattern']) for x in prior['suite_results']]+[('knowledge/borrowing-costs','test*.py'),('hosted_cao/tests','test_*.py'),('intelligence/tests','test_*.py'),('build4/tests','test_*.py')]
    records=[];logs=[]
    def run(args,name,timeout=14400):
        path=OUT/(name+'.log');started=time.monotonic()
        with path.open('w') as f:
            try:r=subprocess.run(args,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,timeout=timeout,env={**os.environ,'PYTHONHASHSEED':'19'});code=r.returncode
            except subprocess.TimeoutExpired:code=124
        logs.append({'path':str(path.relative_to(ROOT)),'exit_code':code,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size,'seconds':round(time.monotonic()-started,3)})
        return code
    for i,(directory,pattern) in enumerate(suites):
        started_ns=time.time_ns()
        code=run([sys.executable,'-m','build4.run_release','suite',directory,pattern,str(i)],f'suite-{i}')
        record=json.loads((OUT/f'suite-{i}.json').read_text()) if (OUT/f'suite-{i}.json').exists() and (OUT/f'suite-{i}.json').stat().st_mtime_ns>=started_ns else {'passed':False,'tests':0,'distinct_ids':[]}
        record['exit_code']=code;records.append(record)
        print(json.dumps({'suite':directory,'tests':record['tests'],'exit_code':code}),flush=True)
        save(records,logs)
        if code:raise SystemExit(code)
    validators=prior['validators']+[{'command':'knowledge/borrowing-costs/validate_supplement.py'}]
    for i,v in enumerate(validators):
        code=run([sys.executable,v['command']],f'validator-{i}',600);save(records,logs)
        if code:raise SystemExit(code)
    code=run(['git','diff','--check'],'diff-check',30);save(records,logs)
    if code:raise SystemExit(code)
    if not json.loads((OUT/'release-regression.json').read_text())['complete']:raise SystemExit('Release source changed or population incomplete')

def source_hashes():
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*.py') if '.git' not in p.parts}

def input_hashes():
    folders=['build4','intelligence','hosted_cao','local_cao','orchestration','skills','interfaces','knowledge','.github']
    paths=[p for folder in folders for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in {'.py','.json','.md','.csv','.yml','.yaml','.txt'} and '/release/' not in str(p.relative_to(ROOT)) and '/examples/' not in str(p.relative_to(ROOT))]
    paths += list(ROOT.glob('*.py'))
    recovery=subprocess.check_output(['git','ls-files','recovery/borrowing-costs-pr42'],cwd=ROOT,text=True).splitlines()
    paths += [ROOT/name for name in recovery if Path(name).suffix in {'.py','.json'} or '.tar.xz.part' in name]
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths))}

def save(records,logs):
    ids=sorted({i for r in records for i in r['distinct_ids']})
    sources=source_hashes()
    start=json.loads((OUT/'start-source-hashes.json').read_text())
    inputs=input_hashes()
    unchanged=sources==start and inputs==json.loads((OUT/'start-input-hashes.json').read_text())
    value={'baseline':'495d4e7fccd5863c971423a5fb130f82e37b9604','executed_distinct_tests':len(ids),'attempt':ATTEMPT,'source_unchanged':unchanged,'suite_results':records,'logs':logs,'tested_python_sha256':sources,'tested_execution_inputs_sha256':inputs,'complete':len(records)==15 and len(logs)==24 and unchanged and all(x['exit_code']==0 for x in logs) and all(r['passed'] and not r['skipped'] for r in records),'historical_artifacts_regenerated':False}
    (OUT/'release-regression.json').write_text(json.dumps(value,indent=2)+'\n')

if __name__=='__main__':
    if len(sys.argv)>1:sys.exit(one_suite(sys.argv[2],sys.argv[3],sys.argv[4]))
    release()
