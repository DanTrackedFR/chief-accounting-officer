"""One production population/dispatch contract for Profile 1.2 release gates.

Independent authorship belongs to the retained review, not to subsequent CI reruns.
All five remediation suites are mandatory regression gates, including isolated
current-commit governance subprocesses. Nested positive-control executions are
not added again to the top-level distinct test count.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from receipt_integrity import require
from build4.run_release import input_hashes

BASE_SUITES = (
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
REMEDIATION_SUITES = (
    ('diagnostics/profile12', 'regressions.py'),
    ('diagnostics/profile12', 'governance.py'),
    ('diagnostics/profile12/remediation/accounting-qa', 'test_accounting_qa.py'),
    ('diagnostics/profile12/remediation/engineering-qa', 'test_boundaries.py'),
    ('diagnostics/profile12/remediation/engineering-qa', 'test_governance.py'),
)
INFRA_SUITES = (('tests/phase_a_release_infra', 'test_*.py'),)
SUPPORTED_SUITES = BASE_SUITES + REMEDIATION_SUITES + INFRA_SUITES
PHASE_A_REQUIRED_PATH = 'skills/presumed-sources/phase-a-contracts/required-tests-v1.json'
PHASE_A_REQUIRED_SHA256 = '2ca2548bbb70d37834f445834f8ef2500d5afb2873d984b5e5e9213a10382603'
VALIDATOR_COMMANDS = (
    'knowledge/income-taxes/validate_supplement.py', 'knowledge/agriculture/validate_supplement.py',
    'knowledge/insurance-contracts/validate_supplement.py', 'knowledge/derivatives-hedge/validate_supplement.py',
    'knowledge/inventory-cost/validate_supplement.py', 'knowledge/standards-evidence/validate_claims.py',
    'knowledge/standards-evidence/validate_approvals.py', 'knowledge/borrowing-costs/validate_supplement.py',
    'knowledge/government-grants/validate_supplement.py', 'knowledge/investment-property/validate_supplement.py',
)
REQUIRED_PATH = 'skills/presumed-sources/required-remediation-tests.json'
DISCOVERY_SCRIPT = '''import json,sys,unittest
loader=unittest.TestLoader(); suite=loader.discover(sys.argv[1],pattern=sys.argv[2])
def cases(s):
 for t in s:
  if isinstance(t,unittest.TestSuite):yield from cases(t)
  else:yield t
ids=sorted(sys.argv[1]+'::'+t.id() for t in cases(suite))
if loader.errors:raise RuntimeError('Discovery errors: '+str(loader.errors))
if len(ids)!=len(set(ids)):raise RuntimeError('Duplicate discovery identities')
print(json.dumps(ids))
'''


def release_input_hashes():
    values = input_hashes()
    paths = list((ROOT/'diagnostics/profile12/fixtures').rglob('*')) + [ROOT/REQUIRED_PATH]
    paths += list((ROOT/'skills/presumed-sources/release/phase-a-v1').glob('*.json'))
    paths += [ROOT/'skills/presumed-sources/release/http-proof.json']
    for path in paths:
        if path.is_file():
            require(path.resolve() == path, 'Diagnostic fixture redirected')
            values[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return dict(sorted(values.items()))


def source_commit():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()


def gate_plan(attempt, commit):
    require(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]*', attempt or '') is not None, 'Invalid release attempt')
    require(re.fullmatch(r'[0-9a-f]{40}', commit or '') is not None, 'Invalid frozen source commit')
    plan = []
    for index, (directory, pattern) in enumerate(SUPPORTED_SUITES):
        environment = {'PYTHONHASHSEED': '19', 'CAO_BUILD4_ATTEMPT': attempt}
        if index >= len(BASE_SUITES):
            trace = f'build4/release/{attempt}/traces/suite-{index}'
            environment.update(CAO_DIAGNOSTIC_OUT=trace, CAO_ACCOUNTING_QA_OUT=trace,
                               CAO_ENGINEERING_OUT=trace, CAO_GOV_REF=commit,
                               CAO_GOV_FOCUSED='1', CAO_ENGINEERING_REF=commit)
        plan.append(dict(index=index, suite=directory, pattern=pattern,
                         gate='accounting-regression' if index < len(BASE_SUITES) else 'mandatory-remediation',
                         command=['python', 'skills/presumed-sources/suite_runner.py', 'suite', directory, pattern, str(index)],
                         environment=environment))
    return plan


def required_ids():
    data = json.loads((ROOT/REQUIRED_PATH).read_text())
    require(data.get('schema_version') == 1 and len(data.get('suites', [])) == 5,
            'Missing mandatory remediation coverage contract')
    require([(r['suite'], r['pattern']) for r in data['suites']] == list(REMEDIATION_SUITES),
            'Required remediation suite contract differs')
    ids = [identity for row in data['suites'] for identity in row['distinct_ids']]
    require(len(ids) == len(set(ids)) == 63, 'Mandatory remediation identity contract differs')
    return data['suites']


def phase_a_required_ids():
    path = ROOT/PHASE_A_REQUIRED_PATH
    require(path.resolve() == path and hashlib.sha256(path.read_bytes()).hexdigest() == PHASE_A_REQUIRED_SHA256,
            'Mandatory Phase A identity contract changed')
    data = json.loads(path.read_bytes())
    ids = data['required_ids']
    require(data['schema_version'] == 1 and len(ids) == len(set(ids)) == 55 and ids == sorted(ids),
            'Mandatory Phase A identity population differs')
    return ids


def verify_required_population(rows, executed=False):
    key = 'executed_ids' if executed else 'distinct_ids'
    ids = [identity for row in rows for identity in row[key]]
    require(len(ids) == len(set(ids)), 'Duplicate release identities')
    mandatory = set(phase_a_required_ids())
    mandatory.update(i for row in required_ids() for i in row['distinct_ids'])
    missing = mandatory - set(ids)
    require(not missing, 'Missing mandatory Phase A/historical methods: '+', '.join(sorted(missing)))
    return len(mandatory)



def discover(attempt, commit):
    rows = []
    with tempfile.TemporaryDirectory(prefix='cao-discovery-') as temporary:
        for slot in gate_plan(attempt, commit):
            env = {**os.environ, **slot['environment']}
            # Importing diagnostic modules creates their output directory. Discovery
            # must never create or mutate an attempt or retained evidence directory.
            for key in ('CAO_DIAGNOSTIC_OUT', 'CAO_ACCOUNTING_QA_OUT', 'CAO_ENGINEERING_OUT'):
                env[key] = str(Path(temporary)/str(slot['index']))
            ids = json.loads(subprocess.check_output(
                [sys.executable, '-c', DISCOVERY_SCRIPT, slot['suite'], slot['pattern']],
                cwd=ROOT, env=env, text=True))
            require(bool(ids), 'Empty mandatory suite: '+slot['suite'])
            rows.append(dict(**slot, distinct_ids=ids, tests=len(ids)))
    ids = [identity for row in rows for identity in row['distinct_ids']]
    require(len(ids) == len(set(ids)), 'Duplicate release discovery identities')
    verify_required_population(rows)
    indexed = {(row['suite'], row['pattern']): set(row['distinct_ids']) for row in rows}
    for required in required_ids():
        missing = set(required['distinct_ids']) - indexed[(required['suite'], required['pattern'])]
        require(not missing, 'Missing mandatory remediation tests: '+', '.join(sorted(missing)))
    return dict(schema_version=1, source_commit=commit, attempt=attempt, suite_results=rows,
                discovered_distinct_tests=len(ids), executed_distinct_tests=0,
                release_accepted=False, scope='discovery-only')


def verify_source_binding(commit, sources, inputs):
    require(re.fullmatch(r'[0-9a-f]{40}', commit or '') is not None, 'Invalid source commit')
    entries = subprocess.check_output(['git','ls-tree','-r',commit], cwd=ROOT, text=True)
    tree = {line.split('\t',1)[1]: line.split()[2] for line in entries.splitlines()}
    for name, expected in {**sources, **inputs}.items():
        path = ROOT/name
        require(path.resolve() == path and path.is_file(), 'Source input redirected or absent: '+name)
        data = path.read_bytes()
        blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(hashlib.sha256(data).hexdigest() == expected and tree.get(name) == blob,
                'Source commit/execution input mismatch: '+name)
    return True
