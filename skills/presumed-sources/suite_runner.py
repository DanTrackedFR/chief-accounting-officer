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
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from build4.test_outcomes import ObservedResult, observations, aggregate

ROOT=Path(__file__).resolve().parents[2]
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
                try:code=subprocess.run([sys.executable,str(ROOT/'skills/presumed-sources/suite_runner.py'),'suite',directory,path.name,label],cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,timeout=14400).returncode
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
        value.update(aggregate(records))
        (OUT/f'suite-{index}.json').write_text(json.dumps(value,indent=2)+'\n')
        return 0 if value['passed'] else 1
    loader=unittest.TestLoader();suite=loader.discover(directory,pattern=pattern)
    def cases(s):
        for t in s:
            if isinstance(t,unittest.TestSuite):yield from cases(t)
            else:yield t
    ids=sorted(directory+'::'+t.id() for t in cases(suite))
    started=time.monotonic();result=unittest.TextTestRunner(verbosity=2,resultclass=ObservedResult).run(suite)
    record={'suite':directory,'pattern':pattern,'distinct_ids':ids,'tests':result.testsRun,'errors':len(result.errors),'failures':len(result.failures),'skipped':len(result.skipped),'seconds':round(time.monotonic()-started,3),'passed':result.wasSuccessful()}
    record.update(observations(result,directory,ids))
    (OUT/f'suite-{index}.json').write_text(json.dumps(record,indent=2)+'\n')
    return 0 if result.wasSuccessful() else 1

if __name__=='__main__':
    if len(sys.argv)!=5 or sys.argv[1]!='suite':raise SystemExit('Only one bounded suite per invocation')
    sys.exit(one_suite(sys.argv[2],sys.argv[3],sys.argv[4]))
