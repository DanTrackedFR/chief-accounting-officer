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
PRIOR_CONTRACT = NAMESPACE + '/contract-v1.json'
CONTRACT = NAMESPACE + '/contract-v2.json'
AMENDMENT = NAMESPACE + '/amendment-001.json'
AMENDMENT_SCHEMA = NAMESPACE + '/amendment-001.schema.json'
AMENDMENT_REVIEW = NAMESPACE + '/amendment-001-review.md'
AMENDMENT_RECORDS = (PRIOR_CONTRACT, AMENDMENT, AMENDMENT_SCHEMA, AMENDMENT_REVIEW)
REVIEWED_IMPLEMENTATION = '1589734065b4a534276062f97b32288d6c03f761'
REVIEWED_TREE = 'f3f747aa241583d1564cb210e99cd2cd18ca4765'
REVIEW_REPORT_MARKER = b'## Complete published standalone G4C-3 report\n\n'
# Exact published provenance; final sealing bytes require future external review.
IMPLEMENTATION_REVIEW = {'conditions': ['Obtain separate owner authorisation to publish the exact local candidate to existing PR #54. Recheck remote head/PR Draft state and source/tree before writing. This review itself authorises only its report comment, not a source push or recreated Git commit.', 'Preserve the eight-file hashes, original sealed records and all historical evidence. Any source/pin/approval-record change creates a successor requiring fresh bounded verification and exact-byte review; this report does not preapprove it.', 'Disclose that amendment-001 remains PENDING_INDEPENDENT_REVIEW and contract-v2 remains PENDING_G3. Publication alone does not open production acceptance. Prior G3B-2 review applies to its old source, not automatic approval of the new helper.', 'Before fresh full regression, separately authorise and complete the required governance sealing/approval-evidence successor and independently review its final hashes/tree. Do not merely relabel the original historical scope review. Preserve the acyclic external trust anchor and separate map checks.', 'After that gate, obtain explicit renewed regression execution authority. Fresh discovery/maps, full mandatory methods, durable retrieved Actions artifacts, source-bound reviewed acceptance receipt and independent final acceptance remain required. Do not reuse F2 acceptance, claim skipped/pending exact-head CI passed, mark Ready, merge or deploy.'], 'disposition': 'APPROVE WITH EXPLICIT CONDITIONS', 'final_byte_attestation': 'PENDING_INDEPENDENT_FINAL_BYTE_REVIEW', 'path': 'skills/presumed-sources/release/ci-governance-v1/amendment-001-review.md', 'publication': 'https://github.com/DanTrackedFR/chief-accounting-officer/pull/54#issuecomment-6836464616', 'release_accepted': False, 'report_sha256': 'ad85901b6a58c247d233e22f239cf2aac59280cdbff6ecc1aa0914d4f0deb8fe', 'review_id': 'G4C3-15897340-20261112', 'reviewed_commit': '1589734065b4a534276062f97b32288d6c03f761', 'reviewed_tree': 'f3f747aa241583d1564cb210e99cd2cd18ca4765', 'scope': ['skills/presumed-sources/ci_governance.py', 'skills/presumed-sources/release/ci-governance-v1/amendment-001.json', 'skills/presumed-sources/release/ci-governance-v1/amendment-001.schema.json', 'skills/presumed-sources/release/ci-governance-v1/contract-v2.json', 'tests/fixtures/phase_a_v1/runner.py', 'tests/phase_a_release_infra/test_infrastructure.py', 'tests/test_ci_governance_migration.py', 'tests/test_presumed_release.py'], 'session_reference': '01a1d1a0-6cc7-7cf1-8779-3e580adf1af0', 'sha256': '970eff3e719eb54f78874add4a5a67c1021f01da1810b8bac26c7db69dbfb470'}
AMENDMENT_SHA256 = 'eacee145d63748c53007c6ab96e0d4e7bf76d14957c084ddf7c9736c8a88786c'
PRIOR_COMMIT = '3fc1efd56506ad465ca959324644ac903130e321'
PRIOR_TREE = 'b5227359df39804dc887fab9b22ac15931cee18e'
PRIOR_CONTRACT_SHA256 = 'e7695c46551a9457040dade644a6de5f94f85a3670a9b81248eef74794fad94a'
CONTRACT_SHA256 = 'b676056ff2e6cfc1a62567c56a03972f012e155f70b8af433cf55b7802bb6495'
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


# A finite path universe, anchored to F2 rather than selected by contract data.
# Production F2 contains all eight. Existing isolated fixtures rewrite the code's
# F2 literal to a sparse synthetic predecessor; they cannot change production F2
# through JSON, environment variables, or a caller-supplied migration selector.
PREDECESSOR_PATHS = (
    'skills/presumed-sources/release/historical-preservation.json',
    'skills/presumed-sources/release/workflow-migration/contract-v2.json',
    'skills/presumed-sources/release/workflow-migration/cao-orchestration.v1.yml',
    'skills/presumed-sources/release/workflow-migration/independent-qa.md',
    'skills/presumed-sources/release/workflow-migration/receipt-review.md',
    'skills/presumed-sources/phase-a-contracts/accepted-main-infrastructure-v1.json',
    'skills/presumed-sources/release/phase-a-v1/proof-contract.json',
    'skills/presumed-sources/release/phase-a-v1/governance-source-v2.json',
)


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


def _safe_name(name):
    require(isinstance(name,str) and bool(name) and not Path(name).is_absolute() and
            '..' not in Path(name).parts and Path(name).as_posix() == name,
            'Unsafe contract path')


def _bound_shape(row):
    _keys(row, ('path','sha256'))
    _safe_name(row['path'])
    _digest(row['sha256'])


def _blob_shape(value):
    require(isinstance(value,str) and re.fullmatch('[0-9a-f]{40}',value) is not None,
            'Malformed Git blob')


def _validate_shape(root, data):
    """Explicit fixed-schema validation, followed by stricter migration rules.

    No JSON Schema package is needed by production. This implements every
    constraint in contract.schema.json; existing semantic checks remain stronger
    for fields whose schema only declares an object. F2_COUNT is the existing
    literal rebound solely in copied synthetic fixture code, never contract data.
    """
    _keys(data, TOP_KEYS)
    for name in ('modified_files','added_source_files','predecessor_commits',
                 'population_extension','preserved_f2_files','workflow_transitions',
                 'proof_input_transitions','compatibility_test'):
        require(isinstance(data[name],dict), 'Contract field must be an object: '+name)
    for key in ('schema','owner_authorization'):
        _bound_shape(data[key])
    _keys(data['scope_review'], ('path','sha256','status'))
    _safe_name(data['scope_review']['path']); _digest(data['scope_review']['sha256'])
    require(data['scope_review']['status'] in ('PENDING_G3','INDEPENDENTLY_REVIEWED'),
            'Invalid review status')
    _keys(data['modified_files'], MODIFIED)
    _keys(data['added_source_files'], ADDED)
    _keys(data['predecessor_commits'], ('f2','f2_tree','frozen','frozen_tree','accepted_baseline'))
    for value in data['predecessor_commits'].values():_blob_shape(value)
    for name,row in data['modified_files'].items():
        _safe_name(name)
        _keys(row, ('archive','before_sha256','before_blob','after_sha256'))
        _safe_name(row['archive']);_digest(row['before_sha256']);_digest(row['after_sha256'])
        _blob_shape(row['before_blob'])
    compatibility=data['compatibility_test']
    _keys(compatibility, ('path','before_sha256','before_blob','after_sha256'))
    _safe_name(compatibility['path']);_digest(compatibility['before_sha256'])
    _digest(compatibility['after_sha256']);_blob_shape(compatibility['before_blob'])
    for key in ('workflow_transitions','proof_input_transitions'):
        _keys(data[key],WORKFLOWS)
        for row in data[key].values():
            _keys(row, ('before','after'));_digest(row['before']);_digest(row['after'])
    population=data['population_extension']
    _keys(population, ('slot','base_count','additional_ids','total'))
    for key in ('slot','base_count','total'):
        require(type(population[key]) is int, 'Population counter must be an integer')
    ids=population['additional_ids']
    require(isinstance(ids,list) and len(ids)==24 and all(isinstance(v,str) for v in ids),
            'Population extension differs: invalid identities')
    require(len(set(ids))==len(ids), 'Duplicate population identities')
    require(len(data['preserved_f2_files'])==F2_COUNT, 'F2 preservation population differs')
    for name,row in data['preserved_f2_files'].items():
        _safe_name(name);_keys(row, ('sha256','blob'));_digest(row['sha256']);_blob_shape(row['blob'])
    records=data['predecessor_contracts']
    require(isinstance(records,list) and bool(records), 'Empty or invalid predecessor contracts')
    for row in records:_bound_shape(row)
    paths=[row['path'] for row in records]
    require(len(paths)==len(set(paths)), 'Duplicate predecessor contract path')
    # Use only the immutable code-pinned Git tree, never a set supplied by JSON.
    # This also supports the existing sparse, explicitly synthetic Git fixture.
    tree={line.split('\t',1)[1] for line in _git(root,'ls-tree','-r',F2).decode().splitlines()}
    expected=set(PREDECESSOR_PATHS) & tree
    require(bool(expected) and set(paths)==expected, 'Unauthorized predecessor contract set')


# Exact owner-authorised successor. No independent attestation is asserted here.
MAINTENANCE = NAMESPACE + '/amendment-002.json'
MAINTENANCE_SCHEMA = NAMESPACE + '/amendment-002.schema.json'
MAINTENANCE_REVIEW = NAMESPACE + '/amendment-002-review.md'
DIAGNOSTIC_TEST = 'diagnostics/profile12/governance.py'
DIAGNOSTIC_ARCHIVE = NAMESPACE + '/predecessors/' + DIAGNOSTIC_TEST + '.txt'
MAINTENANCE_PREDECESSOR = '1feef2f93f2b5d9d017dc55449912c9cfd8bf7a7'
MAINTENANCE_TREE = 'e9adf0d767198ba7593361126980296bb070d20a'
MAINTENANCE_SHA256 = '2a217840838a66ec0c59688396eab7510d45c9e2b0b78de8ab40df439cc78984'
MAINTENANCE_STATE = 'OWNER_AUTHORISED_MAINTENANCE_PENDING_FINAL_REVIEW'
MAINTENANCE_PATHS = (DIAGNOSTIC_TEST, 'skills/presumed-sources/accepted_history.py',
                     'tests/fixtures/phase_a_v1/runner.py',
                     'tests/phase_a_release_infra/test_infrastructure.py',
                     'tests/test_ci_governance_migration.py')
MAINTENANCE_RECORDS = (MAINTENANCE, MAINTENANCE_SCHEMA, MAINTENANCE_REVIEW, DIAGNOSTIC_ARCHIVE)
AMENDMENT_RECORDS += MAINTENANCE_RECORDS


def _blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def _maintenance(root):
    """Validate mandatory successor authority without granting review/acceptance.

    Historical source/review bindings stay in their original records. The helper
    successor is externally reviewed at its final Git tree, avoiding a self-hash.
    """
    root = Path(root)
    raw = artifact(root, MAINTENANCE).read_bytes()
    require(sha(raw) == MAINTENANCE_SHA256, 'Maintenance amendment changed')
    record = _json(raw)
    _keys(record, ('schema_version','amendment_id','state','independent_review',
                   'release_accepted','predecessor','evidence','authorization','successors',
                   'helper','schema','review','accepted_main_extension'))
    require(type(record['schema_version']) is int and record['schema_version'] == 2 and
            record['amendment_id'] == 'phase-a-ci-governance-v1-amendment-002' and
            record['state'] == MAINTENANCE_STATE and record['independent_review'] is None and
            record['release_accepted'] is False, 'Invalid maintenance identity/state')
    require(isinstance(record['authorization'],str) and bool(record['authorization']),
            'Missing maintenance owner authority')
    for key, name in (('schema',MAINTENANCE_SCHEMA), ('review',MAINTENANCE_REVIEW)):
        _bound_shape(record[key]); require(record[key]['path'] == name, 'Maintenance record redirected')
        _bound(root,record[key])
    _keys(record['evidence'], ('failed_run','g4d1_sha256','g4d2_sha256','g4d3_sha256'))
    for key in ('g4d1_sha256','g4d2_sha256','g4d3_sha256'): _digest(record['evidence'][key])
    failure = record['evidence']['failed_run']
    _keys(failure, ('run_id','attempt','method','checkpoint','archive_sha256','manifest_sha256'))
    require(type(failure['run_id']) is int and failure['run_id'] == 43501747483 and
            type(failure['attempt']) is int and failure['attempt'] == 1 and
            failure['method'] == 'diagnostics/profile12::governance.Governance.test_GOV_02' and
            failure['checkpoint'] == 'https://github.com/DanTrackedFR/chief-accounting-officer/pull/54#issuecomment-6865295726',
            'Maintenance failure provenance differs')
    _digest(failure['archive_sha256']); _digest(failure['manifest_sha256'])
    prior = record['predecessor']
    _keys(prior, ('commit','tree','records'))
    require(prior['commit'] == MAINTENANCE_PREDECESSOR and prior['tree'] == MAINTENANCE_TREE and
            _git(root,'rev-parse',MAINTENANCE_PREDECESSOR+'^{tree}').decode().strip() == MAINTENANCE_TREE,
            'Maintenance predecessor identity differs')
    names = tuple(NAMESPACE+'/'+n for n in ('contract-v1.json','scope-review.md','contract-v2.json',
                  'amendment-001.json','amendment-001.schema.json','amendment-001-review.md'))
    _keys(prior['records'],names)
    for name,row in prior['records'].items():
        _keys(row, ('sha256','blob')); _digest(row['sha256']); _blob_shape(row['blob'])
        before = _git(root,'show',MAINTENANCE_PREDECESSOR+':'+name)
        require(sha(before) == row['sha256'] and _blob(before) == row['blob'],
                'Maintenance predecessor record differs: '+name)
    _keys(record['successors'],MAINTENANCE_PATHS)
    for name,row in record['successors'].items():
        _keys(row, ('before_sha256','before_blob','after_sha256','after_blob'))
        for key in ('before_sha256','after_sha256'): _digest(row[key])
        for key in ('before_blob','after_blob'): _blob_shape(row[key])
        before = _git(root,'show',MAINTENANCE_PREDECESSOR+':'+name)
        require(sha(before) == row['before_sha256'] and _blob(before) == row['before_blob'],
                'Maintenance source predecessor differs: '+name)
    helper = record['helper']
    _keys(helper, ('path','before_sha256','before_blob','successor_identity'))
    require(helper['path'] == ADDED[0] and helper['successor_identity'] == 'EXTERNAL_FINAL_GIT_REVIEW',
            'Maintenance helper must retain external review anchor')
    before = _git(root,'show',MAINTENANCE_PREDECESSOR+':'+ADDED[0])
    require(sha(before) == helper['before_sha256'] and _blob(before) == helper['before_blob'],
            'Maintenance helper predecessor differs')
    extension = record['accepted_main_extension']
    _keys(extension, ('contract','baseline','migrations'))
    _bound_shape(extension['contract'])
    require(extension['contract']['path'] == 'skills/presumed-sources/phase-a-contracts/accepted-main-infrastructure-v1.json'
            and extension['baseline'] == BASELINE, 'Accepted-main extension predecessor differs')
    _bound(root,extension['contract'])
    _keys(extension['migrations'], (DIAGNOSTIC_TEST,))
    row = extension['migrations'][DIAGNOSTIC_TEST]
    _keys(row, ('archive_path','original_sha256','original_blob','successor_sha256','successor_blob'))
    source = record['successors'][DIAGNOSTIC_TEST]
    require(row == dict(archive_path=DIAGNOSTIC_ARCHIVE, original_sha256=source['before_sha256'],
            original_blob=source['before_blob'], successor_sha256=source['after_sha256'],
            successor_blob=source['after_blob']), 'Accepted-main extension source binding differs')
    original = artifact(root,DIAGNOSTIC_ARCHIVE).read_bytes()
    require(sha(original) == row['original_sha256'] and _blob(original) == row['original_blob'],
            'Accepted-main diagnostic archive changed')
    return record


def _effective_digest(name, predecessor, maintenance):
    row = maintenance['successors'].get(name)
    if row is None:
        return predecessor
    require(predecessor == row['before_sha256'], 'Maintenance source binding differs: '+name)
    return row['after_sha256']


def effective_source_digest(root, name, predecessor):
    """Explicit content-addressed successor; never a caller-selected allowance."""
    return _effective_digest(name, predecessor, _maintenance(root))


def _legacy_active_digest(root, name, maintenance):
    # The original reviewed hash remains verifiable in frozen Git, while current
    # bytes must satisfy the separately authenticated successor below.
    row = maintenance['successors'].get(name)
    return row['before_sha256'] if row is not None else sha(artifact(root,name).read_bytes())


def accepted_main_extension(root):
    verify_transition(root)
    return _maintenance(root)['accepted_main_extension']


def _verify_amendment(root, data):
    """Exact versioned successor authority; pending bytes never confer a seal.

    Helper successor identity is an external-review anchor, not a cyclic hash.
    The two code pins authenticate this record and the effective contract.
    """
    maintenance = _maintenance(root)
    raw = artifact(root, AMENDMENT).read_bytes()
    require(sha(raw) == AMENDMENT_SHA256, 'CI governance amendment changed')
    record = _json(raw)
    _keys(record, ('schema_version','amendment_id','state','prior_source','diagnosis',
                   'authorization','successors','helper','schema','independent_review'))
    require(type(record['schema_version']) is int and record['schema_version'] == 1 and
            record['amendment_id'] == 'phase-a-ci-governance-v1-amendment-001' and
            record['state'] in ('PENDING_INDEPENDENT_REVIEW', 'INDEPENDENTLY_REVIEWED_IMPLEMENTATION'),
            'Invalid amendment identity/state')
    if record['state'] == 'PENDING_INDEPENDENT_REVIEW':
        require(record['independent_review'] is None and data['state'] == 'PENDING_G3',
                'Unapproved amendment cannot seal')
    else:
        require(record['independent_review'] == IMPLEMENTATION_REVIEW,
                'Incorrect implementation review provenance')
        evidence = _bound(root, {k: record['independent_review'][k] for k in ('path','sha256')})
        raw_review = evidence.read_bytes()
        marker = REVIEW_REPORT_MARKER
        require(raw_review.count(marker) == 1 and sha(raw_review.split(marker,1)[1]) ==
                IMPLEMENTATION_REVIEW['report_sha256'], 'Published review report bytes differ')
        require(_git(root,'rev-parse',REVIEWED_IMPLEMENTATION+'^{tree}').decode().strip() ==
                REVIEWED_TREE, 'Reviewed implementation tree differs')
    require(record['prior_source'] == dict(commit=PRIOR_COMMIT, tree=PRIOR_TREE,
            contract_sha256=PRIOR_CONTRACT_SHA256,
            attestation='https://github.com/DanTrackedFR/chief-accounting-officer/pull/54#issuecomment-6834058611',
            publication='https://github.com/DanTrackedFR/chief-accounting-officer/pull/54#issuecomment-6834471586'),
            'Incorrect amendment predecessor')
    require(record['diagnosis'] == dict(
            url='https://github.com/DanTrackedFR/chief-accounting-officer/pull/54#issuecomment-6835042772',
            sha256='1f1851a262e4d98d469bd47382a5a092ef20ee26c6d6e9ff8f1e5216d06171f5'),
            'Incorrect amendment diagnosis')
    require(isinstance(record['authorization'],str) and bool(record['authorization']),
            'Missing amendment implementation authority')
    _bound_shape(record['schema'])
    require(record['schema']['path'] == AMENDMENT_SCHEMA, 'Amendment schema redirected')
    _bound(root,record['schema'])
    require(sha(artifact(root,PRIOR_CONTRACT).read_bytes()) == PRIOR_CONTRACT_SHA256,
            'Original sealed contract changed')
    require(_git(root,'rev-parse',PRIOR_COMMIT+'^{tree}').decode().strip() == PRIOR_TREE,
            'Published amendment predecessor tree differs')
    require(sha(_git(root,'show',PRIOR_COMMIT+':'+PRIOR_CONTRACT)) == PRIOR_CONTRACT_SHA256,
            'Original contract Git binding differs')
    names = ('tests/fixtures/phase_a_v1/runner.py', 'tests/test_ci_governance_migration.py',
             'tests/test_presumed_release.py', 'tests/phase_a_release_infra/test_infrastructure.py',
             COMPATIBILITY_TEST)
    _keys(record['successors'], names)
    for name,row in record['successors'].items():
        _keys(row, ('before_sha256','before_blob','after_sha256','reason',
                    'reviewed_sha256','reviewed_blob','change_state'))
        _digest(row['reviewed_sha256']); _blob_shape(row['reviewed_blob'])
        maintenance_paths = ('tests/fixtures/phase_a_v1/runner.py','tests/test_ci_governance_migration.py',
                       COMPATIBILITY_TEST)
        expected_state = ('OWNER_AUTHORISED_TEST_MAINTENANCE_PENDING_FINAL_REVIEW'
                          if row['after_sha256'] != row['reviewed_sha256'] else
                          'UNCHANGED_SINCE_IMPLEMENTATION_REVIEW')
        require(row['change_state'] == expected_state and
                (expected_state == 'UNCHANGED_SINCE_IMPLEMENTATION_REVIEW' or name in maintenance_paths),
                'Unapproved implementation successor: '+name)
        _digest(row['before_sha256']); _digest(row['after_sha256']); _blob_shape(row['before_blob'])
        require(isinstance(row['reason'],str) and bool(row['reason']), 'Missing successor reason')
        before = _git(root,'show',PRIOR_COMMIT+':'+name)
        require(sha(before) == row['before_sha256'] and
                _git(root,'rev-parse',PRIOR_COMMIT+':'+name).decode().strip() == row['before_blob'],
                'Amendment predecessor Git binding differs: '+name)
        effective = (data['modified_files'][name]['after_sha256'] if name in MODIFIED
                     else data['added_source_files'][name]['sha256'] if name in ADDED
                     else _legacy_active_digest(root,name,maintenance))
        require(effective == row['after_sha256'] and sha(artifact(root,name).read_bytes()) ==
                _effective_digest(name,row['after_sha256'],maintenance),
                'Amendment successor differs: '+name)
        if record['state'] == 'INDEPENDENTLY_REVIEWED_IMPLEMENTATION':
            require(sha(_git(root,'show',REVIEWED_IMPLEMENTATION+':'+name)) == row['reviewed_sha256'] and
                    _git(root,'rev-parse',REVIEWED_IMPLEMENTATION+':'+name).decode().strip() == row['reviewed_blob'],
                    'Reviewed implementation successor differs: '+name)
    helper = record['helper']
    _keys(helper, ('path','before_sha256','before_blob','successor_identity','reason'))
    require(helper['path'] == ADDED[0] and helper['successor_identity'] == 'EXTERNAL_FINAL_GIT_REVIEW',
            'Helper must retain external final-byte review anchor')
    _digest(helper['before_sha256']); _blob_shape(helper['before_blob'])
    require(isinstance(helper['reason'],str) and bool(helper['reason']), 'Missing helper reason')
    require(sha(_git(root,'show',PRIOR_COMMIT+':'+ADDED[0])) == helper['before_sha256'] and
            _git(root,'rev-parse',PRIOR_COMMIT+':'+ADDED[0]).decode().strip() == helper['before_blob'],
            'Helper predecessor binding differs')
    return record


def load_contract(root):
    """Validate the pinned record structure; this does NOT approve pending records."""
    root = Path(root)
    raw = artifact(root, CONTRACT).read_bytes()
    require(sha(raw) == CONTRACT_SHA256, 'CI governance contract changed')
    data = _json(raw)
    _validate_shape(root, data)
    _verify_amendment(root, data)
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
    amendment = _verify_amendment(root, data)
    maintenance = _maintenance(root)
    if data['state'] != 'SEALED':
        raise PendingSealing('CI governance PENDING_G3: independent review and final sealing required')
    _keys(data['scope_review'], ('path', 'sha256', 'status'))
    require(data['scope_review']['status'] == 'INDEPENDENTLY_REVIEWED', 'Independent review pending')
    require(amendment['state'] == 'INDEPENDENTLY_REVIEWED_IMPLEMENTATION',
            'Independent amendment review pending')
    require(data['scope_review'] == dict(path=AMENDMENT_REVIEW,
            sha256=IMPLEMENTATION_REVIEW['sha256'],status='INDEPENDENTLY_REVIEWED'), 'Review redirected')
    # Retain the complete original review binding as historical evidence.
    prior = _json(artifact(root,PRIOR_CONTRACT).read_bytes())
    _bound(root, {k: prior['scope_review'][k] for k in ('path','sha256')})
    _bound(root, {k: data['scope_review'][k] for k in ('path','sha256')})
    require(b'PENDING G3' not in artifact(root, data['scope_review']['path']).read_bytes(), 'Pending review cannot seal')
    for key, filename in (('schema','contract.schema.json'), ('owner_authorization','owner-authorization.json')):
        require(data[key]['path'] == NAMESPACE + '/' + filename, 'Record redirected')
        _bound(root, data[key])
    expected_records = {NAMESPACE + '/' + n for n in RECORDS}
    expected_records.update((*AMENDMENT_RECORDS, CONTRACT))
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
        require(sha(artifact(root,name).read_bytes()) == _effective_digest(name,row['after_sha256'],maintenance), 'Active successor changed: '+name)
    require(sha(artifact(root,ADDED[1]).read_bytes()) == _effective_digest(ADDED[1],data['added_source_files'][ADDED[1]]['sha256'],maintenance), 'Added test changed')
    compatibility = data['compatibility_test']
    before = _git(root,'show',F2+':'+COMPATIBILITY_TEST)
    require(sha(before) == compatibility['before_sha256'] and tree.get(COMPATIBILITY_TEST) == compatibility['before_blob'], 'Compatibility predecessor differs')
    require(sha(artifact(root,COMPATIBILITY_TEST).read_bytes()) == _effective_digest(COMPATIBILITY_TEST,compatibility['after_sha256'],maintenance), 'Compatibility successor changed')
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
            elif name == 'tests/phase_a_release_infra/test_infrastructure.py':
                expected = amendment['successors'][name]['after_sha256']
            expected = _effective_digest(name,expected,maintenance)
            require(actual[name] == expected, ('Python changed; ' if name.endswith('.py') else 'execution inputs changed; ')+'Unlisted governed change: '+name)
    for name,row in maintenance['successors'].items():
        current = artifact(root,name).read_bytes()
        require(sha(current) == row['after_sha256'] and _blob(current) == row['after_blob'],
                'Maintenance successor changed: '+name)
    return dict(data, maintenance_successor=dict(state=maintenance['state'],
                independent_review=None,release_accepted=False))


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
