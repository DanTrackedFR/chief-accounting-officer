"""Exact CI-governance-v1 succession; provisional records cannot confer acceptance.

The literal contract pin is an external-review trust anchor, not a self-signature.
G3 must approve this complete module and final Git tree independently.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from receipt_integrity import artifact, require, IntegrityError

if sys.flags.optimize:
    raise RuntimeError('Optimized Python is not supported for mandatory release integrity verification')
ROOT = Path(__file__).resolve().parents[2]
NAMESPACE = 'skills/presumed-sources/release/ci-governance-v1'
CONTRACT = NAMESPACE + '/contract-v1.json'
CONTRACT_SHA256 = '1932b9d6c540c5133852bfe9c3eb67bce2e16e93742ec70faa8e0b96531674e5'
F2 = 'b65b6553a1990029c0b6d200c564c4ccac368299'
FROZEN = 'fc33e21153756a0f694590e55fc607c8b0fb30e4'
F2_COUNT = 611
FROZEN_MANIFEST = 'build4/release/presumed-sources-evidence-42700963367-1-successor-1/release-regression.json'
BASELINE = '97d0621331c6ad2a66b12ed09c0ec40c05c626b9'
WORKFLOWS = (
    '.github/workflows/standards-evidence.yml', '.github/workflows/phase3-skills.yml',
    '.github/workflows/cao-build4.yml', '.github/workflows/cao-orchestration.yml',
)
VERIFIER = 'skills/presumed-sources/verify_release.py'
MODIFIED = (*WORKFLOWS, VERIFIER, 'skills/presumed-sources/accepted_history.py',
            'skills/presumed-sources/proof_selection.py', 'tests/test_presumed_release.py',
            'tests/fixtures/phase_a_v1/runner.py')
COMPATIBILITY_TEST = 'tests/test_presumed_workflow_migration.py'
ADDED = ('skills/presumed-sources/ci_governance.py', 'tests/test_ci_governance_migration.py')
RECORDS = ('contract-v1.json', 'contract.schema.json', 'owner-authorization.json', 'scope-review.md')
TOP_KEYS = {'schema_version','migration_id','state','predecessor_commits','predecessor_contracts',
            'owner_authorization','scope_review','schema','modified_files','added_source_files',
            'workflow_transitions','accepted_main_transition','proof_input_transitions',
            'population_extension','preserved_f2_files','compatibility_test'}
METHODS = (
    'approved_transition_passes', 'predecessor_git_binding', 'historical_predecessor_mutation',
    'f2_archive_mutation', 'legacy_archive_mutation', 'contract_mutation', 'scope_review_mutation',
    'unlisted_workflow_change', 'successor_hash_mismatch', 'unapproved_verifier_successor',
    'historical_rollback', 'no_default_receipt_fallback', 'missing_or_malformed_pointer',
    'pointer_sha256_mismatch', 'changed_map_reuse_rejected', 'duplicate_population_identity',
    'omitted_population_identity', 'exact_proof_input_overlay', 'proof_or_accounting_source_mutation',
    'f2_evidence_preserved', 'unsafe_or_duplicate_paths', 'joint_successor_record_forgery',
    'anchor_binding_checked_independently', 'bootstrap_remains_acceptance_pending',
)
ADDITIONAL_IDS = tuple('tests::test_ci_governance_migration.CIGovernanceMigrationQA.test_' + x for x in METHODS)


class PendingSealing(IntegrityError):
    """G2 implementation is not an independently sealed G3 transition."""


def sha(data):
    return hashlib.sha256(data).hexdigest()


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def _json(data):
    return json.loads(data, object_pairs_hook=_pairs)


def _keys(data, keys):
    require(isinstance(data, dict) and set(data) == set(keys), 'Unexpected contract fields')


def _digest(value):
    require(isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None, 'Malformed digest')


def _bound(root, row):
    _keys(row, ('path', 'sha256'))
    _digest(row['sha256'])
    path = artifact(root, row['path'])
    require(sha(path.read_bytes()) == row['sha256'], 'Bound evidence changed: ' + row['path'])
    return path


def _git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root)


def load_contract(root):
    """Validate the pinned record structure; this does NOT approve pending records."""
    root = Path(root)
    raw = artifact(root, CONTRACT).read_bytes()
    require(sha(raw) == CONTRACT_SHA256, 'CI governance contract changed')
    data = _json(raw)
    _keys(data, TOP_KEYS)
    require(type(data['schema_version']) is int and data['schema_version'] == 1 and
            data['migration_id'] == 'phase-a-ci-governance-v1', 'Wrong CI governance version')
    require(data['state'] in ('PENDING_G3', 'SEALED'), 'Invalid sealing state')
    require(set(data['modified_files']) == set(MODIFIED) and
            set(data['added_source_files']) == set(ADDED), 'Unauthorized migration population')
    require(data['added_source_files'][ADDED[0]] == {'trust_anchor': 'EXTERNAL_G3_GIT_REVIEW'},
            'Trust anchor must not self-hash')
    require(set(data['workflow_transitions']) == set(WORKFLOWS) and
            set(data['proof_input_transitions']) == set(WORKFLOWS), 'Unauthorized workflow transitions')
    require(data['accepted_main_transition'] == VERIFIER, 'Unauthorized accepted-main transition')
    require(data['predecessor_commits'] == {
        'f2': F2, 'f2_tree': '2fff8be455b395428ab26de94cc046cc33c8040c',
        'frozen': FROZEN, 'frozen_tree': '768a4768d1e7203cf16c3834939498f78504e052',
        'accepted_baseline': BASELINE}, 'Predecessor identity differs')
    require(data['population_extension'] == {'slot': 3, 'base_count': 4013,
            'additional_ids': sorted(ADDITIONAL_IDS), 'total': 4037}, 'Population extension differs')
    for name, row in data['modified_files'].items():
        _keys(row, ('archive', 'before_sha256', 'before_blob', 'after_sha256'))
        require(row['archive'] == NAMESPACE + '/predecessors/' + name + '.txt', 'Archive redirected')
        _digest(row['before_sha256']); _digest(row['after_sha256'])
        require(re.fullmatch('[0-9a-f]{40}', row['before_blob']) is not None, 'Malformed predecessor blob')
    _keys(data['compatibility_test'], ('path','before_sha256','before_blob','after_sha256'))
    compatibility = data['compatibility_test']
    require(compatibility['path'] == COMPATIBILITY_TEST, 'Unlisted compatibility test')
    _digest(compatibility['before_sha256']); _digest(compatibility['after_sha256'])
    require(re.fullmatch('[0-9a-f]{40}',compatibility['before_blob']) is not None, 'Malformed compatibility blob')
    _keys(data['added_source_files'][ADDED[1]], ('sha256',))
    _digest(data['added_source_files'][ADDED[1]]['sha256'])
    for name in WORKFLOWS:
        row = data['modified_files'][name]
        expected = {'before': row['before_sha256'], 'after': row['after_sha256']}
        require(data['workflow_transitions'][name] == expected and
                data['proof_input_transitions'][name] == expected, 'Workflow transition mismatch')
    require(len(data['preserved_f2_files']) == F2_COUNT, 'F2 preservation population differs')
    return data


def verify_transition(root):
    """Verify sealed exact succession, all predecessor bindings and governed closure."""
    root = Path(root)
    data = load_contract(root)
    if data['state'] != 'SEALED':
        raise PendingSealing('CI governance PENDING_G3: independent review and final sealing required')
    _keys(data['scope_review'], ('path', 'sha256', 'status'))
    require(data['scope_review']['status'] == 'INDEPENDENTLY_REVIEWED', 'Independent review pending')
    require(data['scope_review']['path'] == NAMESPACE + '/scope-review.md', 'Review redirected')
    _bound(root, {k: data['scope_review'][k] for k in ('path','sha256')})
    require(b'PENDING G3' not in artifact(root, data['scope_review']['path']).read_bytes(), 'Pending review cannot seal')
    for key, filename in (('schema','contract.schema.json'), ('owner_authorization','owner-authorization.json')):
        require(data[key]['path'] == NAMESPACE + '/' + filename, 'Record redirected')
        _bound(root, data[key])
    expected_records = {NAMESPACE + '/' + n for n in RECORDS}
    expected_records.update(row['archive'] for row in data['modified_files'].values())
    actual_records = {str(p.relative_to(root)) for p in (root/NAMESPACE).rglob('*') if p.is_file()}
    require(actual_records == expected_records, 'Unlisted governance record')
    require(_git(root, 'rev-parse', F2+'^{tree}').decode().strip() == data['predecessor_commits']['f2_tree'], 'F2 tree differs')
    require(_git(root, 'rev-parse', FROZEN+'^{tree}').decode().strip() == data['predecessor_commits']['frozen_tree'], 'Frozen tree differs')
    tree = {line.split('\t',1)[1]: line.split()[2] for line in _git(root,'ls-tree','-r',F2).decode().splitlines()}
    def blob(data):
        return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    for row in data['predecessor_contracts']:
        path = _bound(root, row)
        require(blob(path.read_bytes()) == tree.get(row['path']), 'Predecessor contract differs from F2')
    for name, row in data['modified_files'].items():
        archive = artifact(root, row['archive']).read_bytes()
        require(blob(archive) == tree.get(name) and sha(archive) == row['before_sha256'], 'Archived predecessor changed: '+name)
        require(tree.get(name) == row['before_blob'], 'Predecessor Git binding differs: '+name)
        require(sha(artifact(root,name).read_bytes()) == row['after_sha256'], 'Active successor changed: '+name)
    require(sha(artifact(root,ADDED[1]).read_bytes()) == data['added_source_files'][ADDED[1]]['sha256'], 'Added test changed')
    compatibility = data['compatibility_test']
    before = _git(root,'show',F2+':'+COMPATIBILITY_TEST)
    require(sha(before) == compatibility['before_sha256'] and tree.get(COMPATIBILITY_TEST) == compatibility['before_blob'], 'Compatibility predecessor differs')
    require(sha(artifact(root,COMPATIBILITY_TEST).read_bytes()) == compatibility['after_sha256'], 'Compatibility successor changed')
    f2_paths = _git(root, 'diff', '--name-only', F2+'^', F2).decode().splitlines()
    require(set(f2_paths) == set(data['preserved_f2_files']), 'F2 inventory paths differ')
    for name,row in data['preserved_f2_files'].items():
        _keys(row, ('sha256','blob'))
        b = artifact(root,name).read_bytes()
        require(sha(b) == row['sha256'] and
                tree.get(name) == row['blob'] and
                hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest() == row['blob'], 'F2 evidence changed: '+name)
    from build4.run_release import source_hashes
    from release_population import release_input_hashes
    frozen = _json(artifact(root, FROZEN_MANIFEST).read_bytes())
    require(root == ROOT, 'Governed maps require actual checkout root')
    for actual, key in ((source_hashes(),'tested_python_sha256'), (release_input_hashes(),'tested_execution_inputs_sha256')):
        original = frozen[key]
        # The unchanged input builder excludes top-level tests/; Python maps do not.
        added = set(ADDED) if key == 'tested_python_sha256' else {ADDED[0]}
        require(set(actual) == set(original) | added, ('Python changed; ' if key == 'tested_python_sha256' else 'execution inputs changed; ')+'Unlisted governed input population')
        for name, expected in original.items():
            if name in MODIFIED:
                expected = data['modified_files'][name]['after_sha256']
            elif name == COMPATIBILITY_TEST:
                expected = data['compatibility_test']['after_sha256']
            require(actual[name] == expected, ('Python changed; ' if name.endswith('.py') else 'execution inputs changed; ')+'Unlisted governed change: '+name)
    return data


def historical_predecessor(root, path):
    require(path in WORKFLOWS, 'Unlisted historical workflow')
    data = verify_transition(root)
    return artifact(Path(root), data['modified_files'][path]['archive'])


def accepted_main_predecessor(root, path):
    require(path == VERIFIER, 'Unlisted accepted-main successor')
    data = verify_transition(root)
    return artifact(Path(root), data['modified_files'][path]['archive'])


def apply_proof_input_transition(root, predecessor_inputs):
    data = verify_transition(root)
    result = dict(predecessor_inputs)
    for name,row in data['proof_input_transitions'].items():
        require(result.get(name) == row['before'], 'Incorrect proof-input predecessor: '+name)
        result[name] = row['after']
    return result


def _check_pointer(root, pointer, digest):
    require(isinstance(pointer,str) and re.fullmatch(r'build4/release/[a-zA-Z0-9_-]+-v2\.json',pointer) is not None,
            'Missing or malformed acceptance pointer')
    _digest(digest)
    require(sha(artifact(Path(root),pointer).read_bytes()) == digest, 'Acceptance pointer SHA-256 mismatch')
    return pointer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    check = commands.add_parser('check-pointer')
    check.add_argument('--pointer', required=True); check.add_argument('--sha256', required=True)
    args = parser.parse_args()
    print(json.dumps({'pointer': _check_pointer(ROOT,args.pointer,args.sha256), 'hash_checked':True,
                      'release_accepted':False}))
