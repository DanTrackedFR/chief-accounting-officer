"""Process death/restart proof on the native Stage2 accounting contracts."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from orchestration.persistence.codec import dumps

TARGET=Path(__file__).resolve().parents[1]/'examples/durable-case-foundation'

PRODUCER='''
import sys
from orchestration.tests.persistence_fixtures import proof,COMPANY,CONTEXT,journal_population
from orchestration.tests.stage2_fixtures import correction
from orchestration.persistence import SQLiteStore,snapshot
from orchestration.persistence.codec import dumps
f=proof(False)
with SQLiteStore(sys.argv[1]) as store:
 store.save(f['case'],COMPANY,CONTEXT,0)
 correction(f)
 store.save(f['case'],COMPANY,CONTEXT,1)
 print(dumps(snapshot(f['case'],COMPANY,CONTEXT)))
# This process exits. No original runtime survives in the restorer's process.
'''
RESTORER='''
import sys
from unittest.mock import patch
from orchestration.tests.persistence_fixtures import COMPANY,journal_population
from orchestration.persistence import SQLiteStore,snapshot
from orchestration.persistence.codec import dumps
from orchestration.runtime import CAO
with patch.object(CAO,'run',side_effect=AssertionError('Owner runtime reexecuted')),patch.object(CAO,'execute_versioned_owner',side_effect=AssertionError('Owner reexecuted')),patch('orchestration.scoped_journals.allocate_scoped',side_effect=AssertionError('Journals released on restore')):
 with SQLiteStore(sys.argv[1]) as store:
  row=store.connection.execute('SELECT case_id FROM heads WHERE company_id=?',(COMPANY,)).fetchone()
  root,revision,context=store.load(COMPANY,row[0]);assert revision==2
  print(dumps(snapshot(root,COMPANY,context)))
'''


def artifacts():
    from orchestration.persistence.codec import loads
    from orchestration.persistence import restore
    from orchestration.runtime import CAO
    from orchestration.tests.persistence_fixtures import COMPANY,journal_population
    with tempfile.TemporaryDirectory() as directory:
        path=str(Path(directory)/'governed.db')
        before=subprocess.run([sys.executable,'-c',PRODUCER,path],capture_output=True,text=True,check=True).stdout.strip()
        after=subprocess.run([sys.executable,'-c',RESTORER,path],capture_output=True,text=True,check=True).stdout.strip()
    if before!=after:raise ValueError('Native restart changed canonical governed state')
    doc=loads(after);root=restore(doc,COMPANY,doc['root_case']);e=root.governance
    rejected=[]
    for receipt in e.receipts:
        if e.versions.states[receipt['result_version']]=='CURRENT':continue
        try:e.validate_receipt(receipt,receipt['consumer_node'])
        except ValueError:rejected.append(dict(dependency_id=receipt['dependency_id'],result_version=receipt['result_version'],state=e.versions.states[receipt['result_version']]))
        else:raise ValueError('Historical receipt requalified')
    if not rejected:raise ValueError('Restart proof requires historical disqualified receipts')
    if not any(c.status=='CLOSED' for c in e.cases.cases.values()):raise ValueError('Closed independent Case missing')
    checksum=hashlib.sha256(after.encode()).hexdigest()
    summary=dict(contract_version=1,store_schema_version=1,checkpoint_revision=2,producer_process_exited=True,
        independent_restorer_process=True,owner_execution_during_restore=0,journal_release_during_restore=0,
        canonical_pre_sha256=checksum,canonical_post_sha256=checksum,exact_roundtrip=True,
        scopes=len(doc['scopes']),periods=len(doc['periods']['periods']),cases=len(doc['cases']),nodes=len(doc['nodes']),
        versions=len(doc['versions']),current=sum(s=='CURRENT' for s in doc['states'].values()),
        stale=sum(s=='STALE' for s in doc['states'].values()),superseded=sum(s=='SUPERSEDED' for s in doc['states'].values()),
        root_status=root.status,root_outcome=root.outcome,closed_cases=sum(c.status=='CLOSED' for c in e.cases.cases.values()),
        historical_receipts_rejected=rejected,journal_versions_preserved=[k for k,_ in journal_population(root)],
        result='PASS',authority='Native governed runtime; synthetic review conventions remain synthetic')
    return {'restart-proof.json':summary,'governed-checkpoint.json':json.loads(after),'public-answer.json':CAO().public(root)}


def main():
    TARGET.mkdir(parents=True,exist_ok=True)
    for name,value in artifacts().items():(TARGET/name).write_text(json.dumps(value,sort_keys=True,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
