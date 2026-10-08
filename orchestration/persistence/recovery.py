"""Durable intents around native deterministic operations, never accounting authority.

Uncommitted owner execution is replayed from a *fresh* prepared native checkpoint.
No executable callback, inferred source, external posting or new ledger is stored.
"""
import copy
import sqlite3
from .codec import dumps, loads, IntegrityError
from .state import snapshot, restore
from .store import sha, RevisionConflict, StorageError
from .evidence import validate as validate_evidence
from orchestration.periods import identity
from orchestration.versions import fingerprint
from orchestration.runtime import CAO


class RecoveryBlocked(ValueError): pass


FIELDS = {
    'CORRECT': {'kind', 'node_id', 'source', 'reason'},
    'REWORK': {'kind', 'plan', 'reviewed_sources'},
    'REOPEN': {'kind', 'period_id', 'reason', 'approval', 'case_ids', 'node_ids'},
    'CLOSE_PERIOD': {'kind', 'period_id'},
    'SELECT_JOURNALS': {'kind', 'context', 'events'},
    'UNCERTAIN_EXTERNAL': {'kind', 'selection_operation', 'evidence'},
}
TERMINAL = {'COMMITTED', 'ABORTED'}


def _phase(name, store, operation_id):
    """Fault-test seam; no runtime callback is deserialized or accepted in intents."""


def validate_intent(case, intent, read_only=False):
    if not isinstance(intent, dict) or intent.get('kind') not in FIELDS or set(intent) != FIELDS[intent['kind']]:
        raise IntegrityError('Unknown/incomplete durable operation intent')
    e = case.governance; kind = intent['kind']
    sources = {}
    if kind == 'CORRECT':
        n = e.graph.nodes.get(intent['node_id'])
        if n is None or not isinstance(intent['reason'], str) or not intent['reason'].strip():
            raise IntegrityError('Exact correction target/reason required')
        e.versions.require_current(e.versions.current(n.id).version_id)
        e.periods.authorize_execution(n.period_id, n.case_id, n.id)
        sources[n.id] = intent['source']
    elif kind == 'REWORK':
        plan = intent['plan']
        if not e.rework_history or plan != e.rework_history[-1]: raise IntegrityError('Exact latest native rework plan required')
        stale = {n for n, v in e.versions.active.items() if e.versions.state(v) == 'STALE'}
        if plan['execution_order'] != e.topological(stale): raise IntegrityError('Exact native stale topology required')
        sources = intent['reviewed_sources']
        if not isinstance(sources, dict) or set(sources) != stale: raise IntegrityError('Complete selected reviewed rework population required')
        for key in sources:
            n = e.graph.nodes[key]; e.periods.authorize_execution(n.period_id, n.case_id, n.id)
    elif kind in ('REOPEN', 'CLOSE_PERIOD'):
        e.periods.get(intent['period_id'])
        if kind == 'REOPEN':
            # Replay on a copy validates the existing synthetic governance contract.
            periods = copy.deepcopy(e.periods)
            periods.reopen(intent['period_id'], intent['reason'], intent['approval'], intent['case_ids'], intent['node_ids'])
            for key in intent['node_ids']:
                n = e.graph.nodes.get(key)
                if n is None or n.period_id != intent['period_id'] or n.case_id not in intent['case_ids']:
                    raise IntegrityError('Reopening authorization dimensions differ')
            if any(key not in e.cases.cases for key in intent['case_ids']): raise IntegrityError('Unknown reopening Case')
    elif kind == 'SELECT_JOURNALS':
        # Actual native gross-line qualification, not a competing journal engine.
        if not read_only: e.current_journals(intent['context'], intent['events'])
    elif kind == 'UNCERTAIN_EXTERNAL':
        if not isinstance(intent['selection_operation'], str) or not intent['selection_operation'] or not isinstance(intent['evidence'], list) or not intent['evidence']:
            raise IntegrityError('Uncertain action requires exact selection and reconciliation evidence')
    if sources:
        qualified = {}
        for key, bundle in getattr(e, 'evidence_bundles', {}).items(): qualified.update(validate_evidence(key, bundle, e))
        for key, source in sources.items():
            n = e.graph.nodes[key]
            if not isinstance(source, dict) or (source.get('scope_id', source.get('entity')), source.get('period_id')) != (n.scope_id, n.period_id):
                raise IntegrityError('Durable reviewed source dimensions differ')
            if not source.get('qualified_input_snapshot') or fingerprint(source) not in qualified:
                raise IntegrityError('Reviewed operation source absent from actual sealed session')


def _event(store, key, status, value):
    seq = store.connection.execute('SELECT count(*) FROM operation_events WHERE operation_id=?', (key,)).fetchone()[0]
    payload = dumps(value)
    store.connection.execute('INSERT INTO operation_events VALUES(?,?,?,?,?)', (key, seq, status, payload, sha(payload)))


def read_operation(store, company_id, case_id, key):
    row = store.connection.execute('SELECT company_id,case_id,base_revision,prepared_revision,payload,sha256 FROM operations WHERE operation_id=?', (key,)).fetchone()
    if row is None or row[:2] != (company_id, case_id): raise IntegrityError('Unknown/wrong Company/Case operation')
    company, root, base, prepared, payload, checksum = row
    if sha(payload) != checksum: raise IntegrityError('Corrupt durable operation')
    doc = loads(payload)
    if set(doc) != {'company_id', 'case_id', 'base_revision', 'base_sha256', 'prepared_sha256', 'intent'} or (doc['company_id'], doc['case_id'], doc['base_revision']) != (company, root, base):
        raise IntegrityError('Wrong operation identity contract')
    if type(base) is not int or base < 1 or prepared != base + 1 or identity('operation', doc) != key:
        raise IntegrityError('Operation semantics identity differs')
    _, base_sha = store._read(company, root, base)
    prepared_doc, prepared_sha = store._read(company, root, prepared)
    if (base_sha, prepared_sha) != (doc['base_sha256'], doc['prepared_sha256']): raise IntegrityError('Operation checkpoint binding differs')
    native = restore(prepared_doc, company, root)
    validate_intent(native, doc['intent'], read_only=True)
    events = []; state = None
    for seq, status, wire, checksum in store.connection.execute('SELECT sequence,status,payload,sha256 FROM operation_events WHERE operation_id=? ORDER BY sequence', (key,)):
        if seq != len(events) or sha(wire) != checksum: raise IntegrityError('Missing/corrupt operation event')
        value = loads(wire)
        if not isinstance(value, dict): raise IntegrityError('Invalid operation outcome')
        if state is None:
            if status != 'PREPARED' or value != {}: raise IntegrityError('Missing operation preparation')
        elif state == 'PREPARED':
            if status not in ('EXECUTING', 'ABORTED', 'UNCERTAIN'): raise IntegrityError('Invalid operation start')
        elif state == 'EXECUTING':
            if status not in ('COMMITTED', 'BLOCKED', 'ABORTED'): raise IntegrityError('Invalid operation outcome transition')
        elif state == 'BLOCKED':
            if status != 'ABORTED': raise IntegrityError('Blocked evidence cannot silently retry')
        else: raise IntegrityError('Duplicate terminal operation transition')
        if status in ('PREPARED', 'EXECUTING') and value != {}: raise IntegrityError('Invalid preparation/execution data')
        if status == 'COMMITTED':
            if set(value) != {'revision', 'checkpoint_sha256', 'result'} or value['revision'] != prepared + 1:
                raise IntegrityError('Wrong committed operation revision')
            result_doc, result_sha = store._read(company, root, value['revision'])
            if result_sha != value['checkpoint_sha256']: raise IntegrityError('Committed outcome checkpoint differs')
            restore(result_doc, company, root)
        if status == 'UNCERTAIN' and (doc['intent']['kind'] != 'UNCERTAIN_EXTERNAL' or value != {'requires': 'explicit external reconciliation; never automatic repost'}):
            raise IntegrityError('Uncertain external marker differs')
        if status == 'BLOCKED' and set(value) != {'error_type', 'requires'}: raise IntegrityError('Invalid blocked operation')
        if status == 'ABORTED' and (set(value) != {'reason'} or not value['reason']): raise IntegrityError('Missing safe abandonment reason')
        events.append(dict(status=status, value=value)); state = status
    if state is None: raise IntegrityError('Operation has no durable preparation')
    return dict(operation_id=key, prepared_revision=prepared, intent=doc['intent'], status=state, events=events)


def reject_pending(store, company_id, case_id, except_id=None):
    for (key,) in store.connection.execute('SELECT operation_id FROM operations WHERE company_id=? AND case_id=?', (company_id, case_id)):
        record = read_operation(store, company_id, case_id, key)
        if key != except_id and record['status'] not in TERMINAL: raise RecoveryBlocked('Resolve existing durable operation: '+key)


def _transaction(store, action):
    try:
        store.connection.execute('BEGIN IMMEDIATE'); store._schema()
        value = action()
        store.connection.execute('COMMIT')
        return value
    except BaseException as error:
        if store.connection.in_transaction: store.connection.execute('ROLLBACK')
        if isinstance(error, sqlite3.Error): raise StorageError('Durable operation transaction failed; committed state retained') from error
        raise


def prepare(store, case, company_id, company_context, expected_revision, intent):
    if type(expected_revision) is not int or expected_revision < 1: raise RevisionConflict('Operation needs an exact committed base revision')
    doc = snapshot(case, company_id, company_context)
    intent = loads(dumps(intent)); validate_intent(case, intent)
    def write():
        base, base_sha = store._read(company_id, case.id, expected_revision)
        # Preparation may retain newly qualified evidence, but cannot execute or
        # change any native state. Evidence must be explicitly linked to this root.
        stripped = copy.deepcopy(doc); stripped['session']['evidence_bundles'] = base['session'].get('evidence_bundles', {})
        for key in stripped['case_private']:
            if '_source_qualification_refs' in base['case_private'][key]:
                stripped['case_private'][key]['_source_qualification_refs'] = base['case_private'][key]['_source_qualification_refs']
            else: stripped['case_private'][key].pop('_source_qualification_refs', None)
        if dumps(stripped) != dumps(base): raise IntegrityError('Preparation may retain evidence only, not uncommitted accounting')
        operation = dict(company_id=company_id, case_id=case.id, base_revision=expected_revision, base_sha256=base_sha, prepared_sha256=sha(dumps(doc)), intent=intent)
        key = identity('operation', operation)
        if store.connection.execute('SELECT 1 FROM operations WHERE operation_id=?', (key,)).fetchone():
            read_operation(store, company_id, case.id, key); return key
        reject_pending(store, company_id, case.id)
        if intent['kind'] == 'UNCERTAIN_EXTERNAL':
            selected = read_operation(store, company_id, case.id, intent['selection_operation'])
            if selected['status'] != 'COMMITTED' or selected['intent']['kind'] != 'SELECT_JOURNALS' or selected['events'][-1]['value']['revision'] != expected_revision:
                raise IntegrityError('Uncertain action requires exact latest committed internal selection')
        revision = store._save_doc(doc, expected_revision)
        payload = dumps(operation)
        store.connection.execute('INSERT INTO operations VALUES(?,?,?,?,?,?,?)', (company_id, case.id, key, expected_revision, revision, payload, sha(payload)))
        _event(store, key, 'PREPARED', {})
        _phase('prepared_transaction', store, key)
        return key
    key = _transaction(store, write)
    _phase('after_prepare', store, key)
    return key


def execute_native(case, intent):
    e = case.governance; kind = intent['kind']; cao = CAO()
    if kind == 'CORRECT': return cao.correct(case, intent['node_id'], intent['source'], intent['reason'])
    if kind == 'REWORK': return cao.selective_reexecute(case, intent['plan'], intent['reviewed_sources'])
    if kind == 'REOPEN':
        e.periods.reopen(intent['period_id'], intent['reason'], intent['approval'], intent['case_ids'], intent['node_ids'])
        return copy.deepcopy(e.periods.history[-1])
    if kind == 'CLOSE_PERIOD':
        e.cases.refresh(e.graph, e.versions, e.edges)
        selected = [c for c in e.cases.cases.values() if c.period_id == intent['period_id']]
        if not selected or any((c.status, c.outcome) != ('CLOSED', 'complete') for c in selected):
            raise RecoveryBlocked('Period closure requires ordinary current CLOSED complete Cases')
        for c in selected:
            for key in c.node_refs:
                n = e.graph.nodes[key]
                if n.status == 'not_applicable': continue
                e.versions.require_current(e.versions.current(key).version_id)
                for dep, edge in e.edges.items():
                    if edge.consumer_node == key: e.validate_receipt(e.receipt(dep), key)
        e.periods.close(intent['period_id'])
        return copy.deepcopy(e.periods.history[-1])
    if kind == 'SELECT_JOURNALS':
        selected, allocation = e.current_journals(intent['context'], intent['events'])
        return dict(selected=selected, allocation=allocation, boundary='internal selection only; no external posting')
    raise RecoveryBlocked('Unknown external economic outcome requires reconciliation')


def recover(store, company_id, case_id, key):
    def start():
        record = read_operation(store, company_id, case_id, key)
        if record['status'] in TERMINAL: return record
        if record['status'] in ('BLOCKED', 'UNCERTAIN'): raise RecoveryBlocked('Explicit evidence/reconciliation required: '+record['status'])
        if store._head(company_id, case_id) != record['prepared_revision']: raise RevisionConflict('Prepared operation cannot overwrite newer checkpoint')
        reject_pending(store, company_id, case_id, key)
        if record['intent']['kind'] == 'UNCERTAIN_EXTERNAL':
            _event(store, key, 'UNCERTAIN', {'requires': 'explicit external reconciliation; never automatic repost'})
        elif record['status'] == 'PREPARED': _event(store, key, 'EXECUTING', {})
        return read_operation(store, company_id, case_id, key)
    record = _transaction(store, start)
    if record['status'] == 'UNCERTAIN': raise RecoveryBlocked('External outcome uncertain; reconcile before any repost')
    if record['status'] == 'ABORTED': raise RecoveryBlocked('Operation safely abandoned; prepare separately qualified new intent')
    _phase('before_execution', store, key)
    def finish():
        actual = read_operation(store, company_id, case_id, key)
        if actual['status'] == 'COMMITTED': return actual
        if store._head(company_id, case_id) != actual['prepared_revision']: raise RevisionConflict('Obsolete recovery worker')
        prepared_doc, _ = store._read(company_id, case_id, actual['prepared_revision'])
        # Fresh state on every attempt. Never continue a half-mutated live object.
        case = restore(prepared_doc, company_id, case_id)
        result = execute_native(case, actual['intent'])
        _phase('after_native', store, key)
        doc = snapshot(case, company_id, prepared_doc['company_context'])
        revision = store._save_doc(doc, actual['prepared_revision'])
        _event(store, key, 'COMMITTED', dict(revision=revision, checkpoint_sha256=sha(dumps(doc)), result=result))
        _phase('outcome_transaction', store, key)
        return read_operation(store, company_id, case_id, key)
    if record['status'] != 'COMMITTED':
        try: record = _transaction(store, finish)
        except (ValueError, KeyError, TypeError, ArithmeticError) as error:
            if not isinstance(error, (RevisionConflict, StorageError, IntegrityError)):
                def block():
                    r = read_operation(store, company_id, case_id, key)
                    if r['status'] == 'EXECUTING': _event(store, key, 'BLOCKED', dict(error_type=type(error).__name__, requires='separately qualified evidence; abandon this uncommitted operation'))
                _transaction(store, block)
            raise
    _phase('after_commit', store, key)
    case, head, _ = store.load(company_id, case_id)
    record['head_revision'] = head
    record['outcome_current'] = head == record['events'][-1]['value']['revision']
    return case, record


def abandon(store, company_id, case_id, key, reason):
    """Only uncommitted pure native operations; never uncertain external outcomes."""
    if not isinstance(reason, str) or not reason.strip(): raise IntegrityError('Explicit abandonment reason required')
    def write():
        r = read_operation(store, company_id, case_id, key)
        if r['status'] == 'ABORTED': return r
        if r['status'] not in ('PREPARED', 'EXECUTING', 'BLOCKED') or r['intent']['kind'] == 'UNCERTAIN_EXTERNAL':
            raise RecoveryBlocked('Cannot abandon committed/uncertain economics')
        _event(store, key, 'ABORTED', dict(reason=reason))
        return read_operation(store, company_id, case_id, key)
    return _transaction(store, write)
