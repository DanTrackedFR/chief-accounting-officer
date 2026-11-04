"""Verify current Presumed-source acceptance without rewriting historical Build4 evidence."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()



SUPPORTED_SUITES = (
    ('orchestration/tests', 'test_*.py'), ('skills/tests', 'test_*.py'),
    ('skills/lease-accounting/tests', 'test_*.py'), ('tests', 'test_*.py'),
    ('knowledge/income-taxes', 'test*.py'), ('knowledge/agriculture', 'test*.py'),
    ('knowledge/insurance-contracts', 'test*.py'), ('knowledge/derivatives-hedge', 'test*.py'),
    ('knowledge/derivatives-hedge', 'independent_review_tests.py'), ('knowledge/inventory-cost', 'test*.py'),
    ('local_cao/tests', 'test_*.py'), ('knowledge/borrowing-costs', 'test*.py'),
    ('hosted_cao/tests', 'test_*.py'), ('intelligence/tests', 'test_*.py'),
    ('build4/tests', 'test_*.py'), ('knowledge/government-grants', 'test_*.py'),
    ('knowledge/investment-property', 'test_*.py'),
)
VALIDATOR_COMMANDS = (
    'knowledge/income-taxes/validate_supplement.py', 'knowledge/agriculture/validate_supplement.py',
    'knowledge/insurance-contracts/validate_supplement.py', 'knowledge/derivatives-hedge/validate_supplement.py',
    'knowledge/inventory-cost/validate_supplement.py', 'knowledge/standards-evidence/validate_claims.py',
    'knowledge/standards-evidence/validate_approvals.py', 'knowledge/borrowing-costs/validate_supplement.py',
    'knowledge/government-grants/validate_supplement.py', 'knowledge/investment-property/validate_supplement.py',
)


def _counted_pass(row):
    ids = row['distinct_ids']
    assert isinstance(ids, list) and len(ids) == len(set(ids)), 'Duplicate test identities'
    assert type(row['tests']) is int and row['tests'] == len(ids), 'Test receipt count differs'
    assert row['passed'] is True and row['exit_code'] == 0, 'Unsuccessful suite receipt'
    assert all(type(row[k]) is int and row[k] == 0 for k in ('skipped', 'errors', 'failures')), 'Unexecuted or unsuccessful tests'


def _command_shape(command):
    import re
    assert isinstance(command, list) and command, 'Missing executed command'
    if command[0] == 'git': return command
    assert re.fullmatch(r'python(?:3(?:\.12)?)?', Path(command[0]).name), 'Unexpected test interpreter'
    return ['python'] + command[1:]


def validate_population(manifest):
    rows = manifest['suite_results']
    assert [(r['suite'], r['pattern']) for r in rows] == list(SUPPORTED_SUITES), 'Release suite population differs'
    ids = []
    for row in rows:
        _counted_pass(row); ids.extend(row['distinct_ids'])
        if row['suite'] == 'orchestration/tests':
            assert row.get('exact_discovery_population') is True, 'Orchestration discovery incomplete'
            shards = row.get('module_results', [])
            assert shards, 'Missing orchestration shards'
            shard_ids = []
            for shard in shards:
                _counted_pass(shard); shard_ids.extend(shard['distinct_ids'])
            assert sorted(shard_ids) == sorted(row['distinct_ids']) and len(shard_ids) == len(set(shard_ids)), 'Shard test population differs'
    assert len(ids) == len(set(ids)) == manifest['executed_distinct_tests'], 'Distinct release test population differs'
    expected = [['python', '-m', 'build4.run_release', 'suite', directory, pattern, str(i)] for i, (directory, pattern) in enumerate(SUPPORTED_SUITES)]
    expected += [['python', command] for command in VALIDATOR_COMMANDS]
    expected += [['git', 'diff', '--check']]
    assert [_command_shape(row['command']) for row in manifest['logs']] == expected, 'Release validator or command population differs'
    assert all(row['exit_code'] == 0 for row in manifest['logs']), 'Unsuccessful release command'


PRESERVATION_SHA256 = '2c4fcdc1b938a1297acb31080e32c3c6ec388ad756395146028df45c98e70c49'
PRESERVATION_COUNT = 8912


ORCHESTRATION_WORKFLOW = '.github/workflows/cao-orchestration.yml'
MIGRATION_DIRECTORY = Path('skills/presumed-sources/release/workflow-migration')
MIGRATION_SHA256 = 'a1d5672288968069ab5b4c7068ec65116dcacbc9d1f0783e7aace2d1b6520ceb'


def verify_workflow_migration(historical_digest):
    contract_path = ROOT / MIGRATION_DIRECTORY / 'contract-v2.json'
    assert contract_path.resolve() == contract_path, 'Migration contract path redirected'
    assert digest(contract_path) == MIGRATION_SHA256, 'Workflow migration contract changed'
    contract = json.loads(contract_path.read_bytes())
    evidence = contract['independent_verification']
    report = ROOT / evidence['path']
    assert report.resolve() == report and digest(report) == evidence['sha256'], 'Independent migration evidence changed'
    assert evidence['other_entries_verified'] == contract['unchanged_entries'] == PRESERVATION_COUNT - 1
    migration = contract['migration']
    assert contract['predecessor']['sha256'] == PRESERVATION_SHA256
    assert migration['original_path'] == migration['successor_path'] == ORCHESTRATION_WORKFLOW
    assert migration['original_sha256'] == historical_digest
    archive = ROOT / migration['archived_path']
    successor = ROOT / migration['successor_path']
    assert archive.resolve() == archive and successor.resolve() == successor, 'Workflow path redirected'
    assert digest(archive) == historical_digest, 'Archived original workflow changed'
    assert digest(successor) == migration['successor_sha256'], 'Active successor workflow changed'


def verify_historical():
    path=ROOT/'skills/presumed-sources/release/historical-preservation.json'
    assert digest(path)==PRESERVATION_SHA256,'Historical preservation manifest changed'
    historical=json.loads(path.read_bytes())
    assert historical['baseline']=='7146eaeca6a28d17d9183d0f9431fd9b9663f1fe'
    assert len(historical['files'])==PRESERVATION_COUNT,'Historical preservation population differs'
    for name,expected in historical['files'].items():
        assert (ROOT/name).resolve().is_relative_to(ROOT),'Historical path escapes repository'
        if name == ORCHESTRATION_WORKFLOW:
            verify_workflow_migration(expected)
        else:
            assert digest(ROOT/name)==expected,('Main7146 artifact changed',name)
    return len(historical['files'])


def verify():
    from build4.run_release import source_hashes,input_hashes
    pointer=json.loads((ROOT/'build4/release/presumed-sources-accepted-release.json').read_text())
    manifest_path=ROOT/pointer['manifest']
    assert manifest_path.resolve().is_relative_to(ROOT/'build4/release'),'Acceptance outside release namespace'
    assert digest(manifest_path)==pointer['sha256'],'Presumed-source regression manifest hash differs'
    manifest=json.loads(manifest_path.read_text())
    assert manifest['complete'] and manifest['source_unchanged'],'Incomplete Presumed-source release'
    validate_population(manifest)
    assert source_hashes()==manifest['tested_python_sha256'],'Presumed-source Python changed after regression'
    assert input_hashes()==manifest['tested_execution_inputs_sha256'],'Presumed-source execution inputs changed after regression'
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
        assert expected==r['distinct_ids'] and r['passed'] and not r['skipped'] and not r['failures'] and not r['errors'] and r['exit_code']==0,('Presumed-source test receipt differs',r['suite'])
        all_ids.extend(expected)
        for shard in r.get('module_results',[]):assert shard['passed'] and shard['exit_code']==0 and digest(ROOT/shard['log'])==shard['log_sha256']
    assert len(all_ids)==len(set(all_ids))==manifest['executed_distinct_tests'],'Presumed-source test count differs'
    assert len(manifest['suite_results'])==17 and len(manifest['logs'])==28,'Presumed-source release population incomplete'
    for row in manifest['logs']:assert row['exit_code']==0 and digest(ROOT/row['path'])==row['sha256'],('Presumed-source log changed',row['path'])
    # Preserve all merged main files under canonical knowledge and historical
    # accounting namespaces, and every original grants supplement file.
    preserved=json.loads((ROOT/'build4/release/investment-property-historical-preservation.json').read_text())
    for name,h in preserved['files'].items():assert digest(ROOT/name)==h,('Historical accounting evidence changed',name)
    from orchestration.history_references import reference_path
    namespace=ROOT/'skills/government-grants/release-evidence/historical-qa'
    for filename in ('specialist-migration.json','orchestration-migration.json','main-proof-migration.json'):
        report=json.loads((namespace/filename).read_text());assert report['status']=='PASS' and not report['errors']
        for name,row in report['files'].items():assert digest(reference_path(name))==row['current_sha256']
    return dict(status='PASS',distinct_tests=len(all_ids),historical_files=verify_historical())

if __name__=='__main__':print(json.dumps(verify(),sort_keys=True))
