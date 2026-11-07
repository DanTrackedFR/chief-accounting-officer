"""Complete production discovery and dispatch; --preflight never runs the full release."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(Path(__file__).resolve().parent)]
from build4.run_release import source_hashes
from receipt_integrity import require
from release_population import (BASE_SUITES, SUPPORTED_SUITES, VALIDATOR_COMMANDS,
                                discover, gate_plan, release_input_hashes, source_commit)


def committed_inputs():
    """Governance clones must execute the same Python and fixture inputs as dispatch."""
    require(subprocess.run(['git', 'diff', '--quiet', 'HEAD'], cwd=ROOT).returncode == 0,
            'Commit tracked changes before isolated governance execution')
    tracked = set(subprocess.check_output(['git', 'ls-files'], cwd=ROOT, text=True).splitlines())
    inputs = set(source_hashes()) | set(release_input_hashes())
    require(inputs <= tracked, 'Commit all execution inputs, including ignored files, before isolated governance execution')


def release(attempt, preflight=False):
    for revision in ('7146eaeca6a28d17d9183d0f9431fd9b9663f1fe', 'e75375b84813b9d584db12aa692b2f4d16baf052'):
        require(subprocess.run(['git', 'cat-file', '-e', revision+'^{commit}'], cwd=ROOT, capture_output=True).returncode == 0,
                'Full historical Git checkout required before release validation')
    committed_inputs()
    commit = source_commit()
    inventory = discover(attempt, commit)
    plan = gate_plan(attempt, commit)
    out = ROOT/'build4/release'/attempt
    require(out.resolve() == out and not out.exists(), 'Preserve prior attempt; choose new CAO_SOURCES_ATTEMPT')
    out.mkdir(parents=True)
    before_source, before_input = source_hashes(), release_input_hashes()
    for name, value in [('start-source-hashes', before_source), ('start-input-hashes', before_input), ('discovery', inventory)]:
        (out/(name+'.json')).write_text(json.dumps(value, sort_keys=True, indent=2)+'\n')

    def run(args, name, environment, timeout=14400):
        log = out/(name+'.log'); started = time.monotonic()
        with log.open('x') as stream:
            try:
                code = subprocess.run(args, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT,
                                      timeout=timeout, env={**os.environ, **environment}).returncode
            except subprocess.TimeoutExpired:
                code = 124
        return dict(command=['python']+args[1:] if args[0] == sys.executable else args,
                    environment=environment, exit_code=code, path=str(log.relative_to(ROOT)),
                    sha256=hashlib.sha256(log.read_bytes()).hexdigest(), seconds=round(time.monotonic()-started, 3))

    def suite(slot):
        index = slot['index']
        receipt = run([sys.executable]+slot['command'][1:], 'suite-'+str(index), slot['environment'])
        path = out/('suite-'+str(index)+'.json')
        data = json.loads(path.read_text()) if path.exists() else dict(suite=slot['suite'], pattern=slot['pattern'], tests=0,
                distinct_ids=[], errors=1, failures=0, skipped=0, passed=False)
        data['exit_code'] = receipt['exit_code']
        require(data['distinct_ids'] == inventory['suite_results'][index]['distinct_ids'],
                'Executed population differs from production discovery: '+str(index))
        print(json.dumps(dict(suite=slot['suite'], pattern=slot['pattern'], tests=data['tests'], exit_code=data['exit_code'])), flush=True)
        return data, receipt

    selected = plan[len(BASE_SUITES):] if preflight else plan
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(suite, selected))
    records, logs = [r[0] for r in results], [r[1] for r in results]
    if not preflight:
        for index, command in enumerate(VALIDATOR_COMMANDS):
            logs.append(run([sys.executable, command], 'validator-'+str(index), {'PYTHONHASHSEED': '19'}, 600))
            print(json.dumps(dict(validator=command, exit_code=logs[-1]['exit_code'])), flush=True)
        logs.append(run(['git', 'diff', '--check'], 'diff-check', {}, 30))
    ids = [identity for record in records for identity in record['distinct_ids']]
    unchanged = before_source == source_hashes() and before_input == release_input_hashes() and commit == source_commit()
    complete = unchanged and len(ids) == len(set(ids)) and len(records) == len(selected) and all(
        r['passed'] and not r['skipped'] and not r['errors'] and not r['failures'] and r['exit_code'] == 0 for r in records
    ) and all(log['exit_code'] == 0 for log in logs)
    value = dict(baseline_main='7146eaeca6a28d17d9183d0f9431fd9b9663f1fe', baseline_pr='48', attempt=attempt,
                 source_commit=commit, complete=complete, source_unchanged=unchanged, executed_distinct_tests=len(set(ids)),
                 suite_results=records, logs=logs, gate_plan=plan, tested_python_sha256=before_source,
                 tested_execution_inputs_sha256=before_input, historical_artifacts_regenerated=False)
    if preflight:
        value.update(scope='bounded-remediation-preflight', release_accepted=False,
                     full_accounting_regression_executed=False, discovered_distinct_tests=inventory['discovered_distinct_tests'])
    filename = 'bounded-preflight.json' if preflight else 'release-regression.json'
    (out/filename).write_text(json.dumps(value, sort_keys=True, indent=2)+'\n')
    print(json.dumps(dict(complete=complete, tests=len(set(ids)), source_unchanged=unchanged,
                         scope='bounded-remediation-preflight' if preflight else 'full-regression')), flush=True)
    return 0 if complete else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--discover', action='store_true', help='Enumerate every production gate without executing tests')
    group.add_argument('--preflight', action='store_true', help='Discover all gates and dispatch only the 63 remediation methods')
    args = parser.parse_args()
    attempt = os.environ.get('CAO_SOURCES_ATTEMPT', 'presumed-sources-attempt-001')
    if args.discover:
        print(json.dumps(discover(attempt, source_commit()), sort_keys=True, indent=2))
        return 0
    return release(attempt, preflight=args.preflight)


if __name__ == '__main__':
    sys.exit(main())
