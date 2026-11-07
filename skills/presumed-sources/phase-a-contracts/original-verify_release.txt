"""Verify current Presumed-source acceptance without rewriting historical Build4 evidence."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

# Mandatory assertions below are intentionally unavailable under optimization.
# Refuse at import, including runpy/direct function callers, before any success.
if sys.flags.optimize:
    raise RuntimeError("Optimized Python is not supported for mandatory release integrity verification")
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from receipt_integrity import verify_inventory, artifact, require


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()



from release_population import (SUPPORTED_SUITES, VALIDATOR_COMMANDS, gate_plan,
                                discover, release_input_hashes)


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
    expected_plan = gate_plan(manifest['attempt'], manifest['source_commit'])
    assert manifest['gate_plan'] == expected_plan, 'Mandatory release gate plan differs'
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
    environments = [slot['environment'] for slot in expected_plan] + [{'PYTHONHASHSEED': '19'} for _ in VALIDATOR_COMMANDS] + [{}]
    assert [row.get('environment') for row in manifest['logs']] == environments, 'Mandatory release environment differs'
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


def verify(pointer_path='build4/release/presumed-sources-accepted-release.json'):
    from build4.run_release import source_hashes,input_hashes
    pointer_file=artifact(ROOT,pointer_path)
    require(pointer_file.is_relative_to(ROOT/'build4/release'), 'Acceptance pointer outside release namespace')
    pointer=json.loads(pointer_file.read_text())
    manifest_path=artifact(ROOT,pointer['manifest'])
    assert manifest_path.resolve().is_relative_to(ROOT/'build4/release'),'Acceptance outside release namespace'
    assert digest(manifest_path)==pointer['sha256'],'Presumed-source regression manifest hash differs'
    manifest=json.loads(manifest_path.read_text())
    assert manifest['complete'] and manifest['source_unchanged'],'Incomplete Presumed-source release'
    verify_inventory(ROOT,pointer,manifest_path,manifest,'release')
    validate_population(manifest)
    assert source_hashes()==manifest['tested_python_sha256'],'Presumed-source Python changed after regression'
    assert release_input_hashes()==manifest['tested_execution_inputs_sha256'],'Presumed-source execution inputs changed after regression'
    all_ids=[]
    inventory=discover(manifest['attempt'],manifest['source_commit'])
    for r, discovered in zip(manifest['suite_results'],inventory['suite_results']):
        expected=discovered['distinct_ids']
        assert expected==r['distinct_ids'] and r['passed'] and not r['skipped'] and not r['failures'] and not r['errors'] and r['exit_code']==0,('Presumed-source test receipt differs',r['suite'])
        all_ids.extend(expected)
        for shard in r.get('module_results',[]):assert shard['passed'] and shard['exit_code']==0 and digest(ROOT/shard['log'])==shard['log_sha256']
    assert len(all_ids)==len(set(all_ids))==manifest['executed_distinct_tests'],'Presumed-source test count differs'
    assert len(manifest['suite_results'])==len(SUPPORTED_SUITES) and len(manifest['logs'])==len(SUPPORTED_SUITES)+len(VALIDATOR_COMMANDS)+1,'Presumed-source release population incomplete'
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

def verify_focused(pointer_path):
    """Explicit diagnostic mode; cannot issue or satisfy release acceptance."""
    from build4.run_release import source_hashes, input_hashes
    pointer = json.loads(artifact(ROOT, pointer_path).read_bytes())
    path = artifact(ROOT, pointer['manifest'])
    require(path.is_relative_to(ROOT/'diagnostics/profile12/remediation'), 'Focused evidence outside diagnostic namespace')
    require(digest(path) == pointer['sha256'], 'Focused manifest digest differs')
    manifest = json.loads(path.read_bytes())
    require(manifest.get('scope') == 'focused-governance-qa-v1', 'Not a focused governance receipt')
    require(manifest['complete'] is True and manifest['source_unchanged'] is True, 'Incomplete focused execution')
    rows = manifest['suite_results']
    require(len(rows) == 1 and (rows[0]['suite'], rows[0]['pattern']) ==
            ('diagnostics/profile12', 'regressions.py'), 'Focused suite population differs')
    _counted_pass(rows[0])
    script = '''import json,unittest
suite=unittest.TestLoader().discover('diagnostics/profile12',pattern='regressions.py')
def cases(s):
 for t in s:
  if isinstance(t,unittest.TestSuite):yield from cases(t)
  else:yield t
print(json.dumps(sorted('diagnostics/profile12::'+t.id() for t in cases(suite))))
'''
    discovered = json.loads(subprocess.check_output([sys.executable,'-c',script],cwd=ROOT,text=True))
    require(rows[0]['distinct_ids'] == discovered, 'Focused discovery population differs')
    require(rows[0]['tests'] == 19 and manifest['executed_distinct_tests'] == 19, 'Focused test population differs')
    require(len(manifest['logs']) == 1, 'Focused command population differs')
    log = manifest['logs'][0]
    require(_command_shape(log['command']) == ['python', '-m', 'build4.run_release', 'suite',
            'diagnostics/profile12', 'regressions.py', '0'], 'Focused command differs')
    require(log['exit_code'] == 0 and digest(artifact(ROOT,log['path'])) == log['sha256'], 'Presumed-source log changed')
    inventory = verify_inventory(ROOT, pointer, path, manifest, 'focused-governance-qa-v1')
    require(source_hashes() == manifest['tested_python_sha256'], 'Focused Python changed after execution')
    require(input_hashes() == manifest['tested_execution_inputs_sha256'], 'Focused execution inputs changed')
    return dict(status='PASS', scope='focused-governance-qa-v1', release_accepted=False,
                distinct_tests=19, inventory_files=inventory, historical_files=verify_historical())


if __name__=='__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--focused':
        result = verify_focused(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == '--pointer':
        result = verify(sys.argv[2])
    elif len(sys.argv) == 1:
        result = verify()
    else:
        raise SystemExit('Usage: verify_release.py [--pointer release-pointer | --focused diagnostic-pointer]')
    print(json.dumps(result,sort_keys=True))
