#!/usr/bin/env python3
"""Bounded release supervisor with retained logs, exit codes and distinct method IDs."""
import hashlib,inspect,json,os,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
EVIDENCE=ROOT/'skills/borrowing-costs/release-evidence'
SUITES=[('skills','skills/tests','test_*.py'),('leases','skills/lease-accounting/tests','test_*.py'),('repository','tests','test_*.py'),('orchestration','orchestration/tests','test_*.py'),('tax','knowledge/income-taxes','test_supplement.py'),('agriculture','knowledge/agriculture','test*.py'),('insurance','knowledge/insurance-contracts','test*.py'),('derivatives','knowledge/derivatives-hedge','test*.py'),('derivatives-independent','knowledge/derivatives-hedge','independent_review_tests.py'),('inventory','knowledge/inventory-cost','test*.py'),('borrowing-knowledge','knowledge/borrowing-costs','test*.py')]
VALIDATORS=[('claims',['knowledge/standards-evidence/validate_claims.py']),('approvals',['knowledge/standards-evidence/validate_approvals.py'])]+[(name+'-validation',['knowledge/'+name+'/validate_supplement.py']) for name in ('income-taxes','agriculture','insurance-contracts','derivatives-hedge','inventory-cost','borrowing-costs')]+[('whitespace',None)]

def leaves(s):
 for t in s:
  if isinstance(t,unittest.TestSuite):yield from leaves(t)
  else:yield t

def suite(name,path,pattern):
 sys.path.insert(0,str(ROOT));loader=unittest.TestLoader();s=loader.discover(str(ROOT/path),pattern=pattern)
 ids=[]
 for t in leaves(s):
  source=Path(inspect.getfile(type(t))).resolve()
  try:source=str(source.relative_to(ROOT))
  except ValueError:source=str(source.name)
  ids.append(source+'::'+type(t).__qualname__+'.'+t._testMethodName)
 result=unittest.TextTestRunner(verbosity=1).run(s)
 payload=dict(name=name,tests_run=result.testsRun,distinct_method_ids=sorted(set(ids)),failures=len(result.failures),errors=len(result.errors),skipped=len(result.skipped),status='PASS' if result.wasSuccessful() else 'FAIL')
 (EVIDENCE/(name+'.tests.json')).write_text(json.dumps(payload,indent=2)+'\n')
 return 0 if result.wasSuccessful() else 1

def main():
 os.chdir(ROOT);EVIDENCE.mkdir(parents=True,exist_ok=True)
 if len(sys.argv)>1 and sys.argv[1]=='--suite':return suite(*sys.argv[2:5])
 commands=[(name,[sys.executable,str(Path(__file__).resolve()),'--suite',name,path,pattern]) for name,path,pattern in SUITES]+[(name,[sys.executable]+args if args else ['git','diff','--check']) for name,args in VALIDATORS]
 outcomes=[];distinct=set()
 for name,cmd in commands:
  logfile=EVIDENCE/(name+'.log')
  with logfile.open('wb') as log:
   try:exitcode=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,timeout=1800).returncode
   except subprocess.TimeoutExpired:exitcode=124;log.write(b'\nUNVERIFIED: bounded execution timeout\n')
  row=dict(gate=name,command=cmd[1:] if cmd[0]==sys.executable else cmd,exit_code=exitcode,status='PASS' if exitcode==0 else 'FAIL' if exitcode!=124 else 'UNVERIFIED',log=str(logfile.relative_to(ROOT)),log_sha256=hashlib.sha256(logfile.read_bytes()).hexdigest())
  resultfile=EVIDENCE/(name+'.tests.json')
  if any(s[0]==name for s in SUITES) and resultfile.exists():
   d=json.loads(resultfile.read_text());row['tests_run']=d['tests_run'];row['distinct_tests']=len(d['distinct_method_ids']);row['skipped']=d['skipped'];distinct.update(d['distinct_method_ids'])
  outcomes.append(row)
  summary=dict(status='PASS' if all(r['exit_code']==0 for r in outcomes) and len(outcomes)==len(commands) else 'INCOMPLETE',gates=outcomes,distinct_test_count=len(distinct),distinct_method_ids=sorted(distinct),completed_gates=len(outcomes),required_gates=len(commands))
  (EVIDENCE/'full-regression.json').write_text(json.dumps(summary,indent=2)+'\n')
  print(name,row['status'],row.get('distinct_tests','validator'),flush=True)
 return 0 if summary['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
