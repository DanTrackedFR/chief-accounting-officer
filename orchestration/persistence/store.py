"""Transactional local durable repository. SQLite is an adapter, not accounting."""
import hashlib
import os
from pathlib import Path
import sqlite3
from typing import Protocol
from .codec import dumps, loads, IntegrityError
from .state import snapshot, restore

SCHEMA_VERSION = 3


def _current_schema(connection):
    """Exact schema3 read-only no-op; unknown or mixed schemas fail closed."""
    actual = dict(connection.execute("SELECT name,sql FROM sqlite_master WHERE type='table'"))
    expected = {statement.split('(')[0].split()[-1]: statement for statement in DDL}
    if connection.execute('PRAGMA user_version').fetchone()[0] != SCHEMA_VERSION or actual != expected:
        raise IntegrityError('Partial/unknown current schema rejected')
    return SCHEMA_VERSION


def _migrate_v1(connection):
    actual = dict(connection.execute("SELECT name,sql FROM sqlite_master WHERE type='table'"))
    expected = {statement.split('(')[0].split()[-1]: statement for statement in DDL_V1}
    if actual != expected: raise IntegrityError('Partial/unknown schema1 rejected')
    for statement in OPERATION_DDL: connection.execute(statement)
    connection.execute('ALTER TABLE checkpoints ADD COLUMN '+OPERATION_COLUMN)
    connection.execute('PRAGMA user_version=2')
    return _migrate_v2(connection)


def _migrate_v2(connection):
    actual = dict(connection.execute("SELECT name,sql FROM sqlite_master WHERE type='table'"))
    expected = {statement.split('(')[0].split()[-1]: statement for statement in DDL_V2}
    if actual != expected: raise IntegrityError('Partial/unknown schema2 rejected')
    for statement in MEMORY_DDL: connection.execute(statement)
    connection.execute('PRAGMA user_version=3')
    return SCHEMA_VERSION


SCHEMA_HANDLERS = {1: _migrate_v1, 2: _migrate_v2, 3: _current_schema}


class RevisionConflict(ValueError): pass
class StorageError(ValueError): pass


class CheckpointStore(Protocol):
    def save(self, case, company_id, company_context, expected_revision): ...
    def load(self, company_id, case_id, revision=None): ...
    def prepare(self, case, company_id, company_context, expected_revision, intent): ...
    def recover(self, company_id, case_id, operation_id): ...
    def operation(self, company_id, case_id, operation_id): ...
    def abandon(self, company_id, case_id, operation_id, reason): ...
    def close(self): ...


DDL_V1 = (
    'CREATE TABLE checkpoints(company_id TEXT NOT NULL,case_id TEXT NOT NULL,revision INTEGER NOT NULL CHECK(revision>0),payload TEXT NOT NULL,sha256 TEXT NOT NULL,previous_sha256 TEXT,object_count INTEGER NOT NULL,PRIMARY KEY(company_id,case_id,revision))',
    'CREATE TABLE objects(company_id TEXT NOT NULL,case_id TEXT NOT NULL,revision INTEGER NOT NULL,kind TEXT NOT NULL,object_id TEXT NOT NULL,payload TEXT NOT NULL,sha256 TEXT NOT NULL,PRIMARY KEY(company_id,case_id,revision,kind,object_id),FOREIGN KEY(company_id,case_id,revision) REFERENCES checkpoints(company_id,case_id,revision))',
    'CREATE TABLE heads(company_id TEXT NOT NULL,case_id TEXT NOT NULL,revision INTEGER NOT NULL,PRIMARY KEY(company_id,case_id),FOREIGN KEY(company_id,case_id,revision) REFERENCES checkpoints(company_id,case_id,revision))',
)


OPERATION_DDL = (
    'CREATE TABLE operations(company_id TEXT NOT NULL,case_id TEXT NOT NULL,operation_id TEXT NOT NULL,base_revision INTEGER NOT NULL,prepared_revision INTEGER NOT NULL,payload TEXT NOT NULL,sha256 TEXT NOT NULL,PRIMARY KEY(operation_id),FOREIGN KEY(company_id,case_id,prepared_revision) REFERENCES checkpoints(company_id,case_id,revision))',
    'CREATE TABLE operation_events(operation_id TEXT NOT NULL,sequence INTEGER NOT NULL,status TEXT NOT NULL,payload TEXT NOT NULL,sha256 TEXT NOT NULL,PRIMARY KEY(operation_id,sequence),FOREIGN KEY(operation_id) REFERENCES operations(operation_id))',
)
OPERATION_COLUMN = 'operation_id TEXT REFERENCES operations(operation_id) DEFERRABLE INITIALLY DEFERRED'
DDL_V2 = (DDL_V1[0].replace(',PRIMARY KEY', ', '+OPERATION_COLUMN+',PRIMARY KEY', 1),) + DDL_V1[1:] + OPERATION_DDL


MEMORY_DDL = (
    'CREATE TABLE memory_events(company_id TEXT NOT NULL,sequence INTEGER NOT NULL,event_id TEXT NOT NULL UNIQUE,payload TEXT NOT NULL,sha256 TEXT NOT NULL,previous_sha256 TEXT,PRIMARY KEY(company_id,sequence))',
    'CREATE TABLE memory_heads(company_id TEXT NOT NULL,sequence INTEGER NOT NULL,sha256 TEXT NOT NULL,PRIMARY KEY(company_id),FOREIGN KEY(company_id,sequence) REFERENCES memory_events(company_id,sequence))',
)
DDL = DDL_V2 + MEMORY_DDL


def sha(text): return hashlib.sha256(text.encode('utf-8')).hexdigest()


def objects(doc):
    rows = [('company', doc['company_id'], doc['company_context'])]
    rows += [('scope', r['scope_id'], r) for r in doc['scopes']]
    rows += [('case', r['id'], r) for r in doc['cases']]
    rows += [('node', r['id'], r) for r in doc['nodes']]
    for kind, key in [('version', 'versions'), ('source', 'source_snapshots'), ('dependency', 'dependencies')]:
        rows += [(kind, k, v) for k, v in doc[key].items()]
    for kind, key, id_key in [('calendar', 'calendars', 'calendar_id'), ('period', 'periods', 'period_id'), ('period_relationship', 'relationships', 'id')]:
        rows += [(kind, r[id_key], r) for r in doc['periods'][key]]
    rows += [('evidence_bundle', k, v) for k, v in doc['session'].get('evidence_bundles', {}).items()]
    return sorted((kind, key, dumps(value), sha(dumps(value))) for kind, key, value in rows)


def validate_extension(previous, current):
    """A new revision cannot erase/overwrite previously committed history."""
    for name in ('versions', 'source_snapshots', 'dependencies'):
        if any(k not in current[name] or current[name][k] != v for k, v in previous[name].items()):
            raise IntegrityError('Committed immutable history removed/changed: '+name)
    for name in ('version_history', 'graph_history', 'rework_history', 'receipts'):
        if current[name][:len(previous[name])] != previous[name]:
            raise IntegrityError('Committed history is not an extension: '+name)
    for key, bundle in previous['session'].get('evidence_bundles', {}).items():
        if current['session'].get('evidence_bundles', {}).get(key) != bundle:
            raise IntegrityError('Committed source qualification removed')
    for key in ('calendars', 'relationships'):
        old = previous['periods'][key]
        new = current['periods'][key]
        if any(row not in new for row in old): raise IntegrityError('Committed Period identity history changed')
    old_periods = {r['period_id']: {k:v for k,v in r.items() if k != 'status'} for r in previous['periods']['periods']}
    new_periods = {r['period_id']: {k:v for k,v in r.items() if k != 'status'} for r in current['periods']['periods']}
    if any(new_periods.get(k) != v for k,v in old_periods.items()): raise IntegrityError('Committed Period identity changed')
    if current['periods']['history'][:len(previous['periods']['history'])] != previous['periods']['history']:
        raise IntegrityError('Committed Period governance history changed')
    old_cases = {c['id']: c for c in previous['cases']}
    new_cases = {c['id']: c for c in current['cases']}
    for key, old in old_cases.items():
        new = new_cases.get(key)
        if new is None: raise IntegrityError('Committed Case removed')
        for name in ('objective', 'scope_id', 'period_id', 'case_type', 'cycle', 'parent_case_id', 'provenance'):
            if new[name] != old[name]: raise IntegrityError('Committed Case identity changed')
        for name in ('transitions', 'governance_history'):
            if new[name][:len(old[name])] != old[name]: raise IntegrityError('Committed Case history removed')


class SQLiteStore:
    """BEGIN IMMEDIATE writer + revision CAS; deferred read snapshot isolation.

    Retain immutable checkpoint revisions. Readers validate full manifests before
    native reconstruction. Failures roll back, never expose partial governance.
    """
    def __init__(self, path, timeout=5.0):
        self.path = Path(path)
        if str(path) == ':memory:': raise StorageError('Durable file path required')
        if self.path.is_symlink(): raise StorageError('Symlink database rejected')
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.close(fd)
        except FileExistsError: pass
        self.connection = sqlite3.connect(str(self.path), timeout=timeout, isolation_level=None)
        self.connection.execute('PRAGMA foreign_keys=ON')
        self.connection.execute('PRAGMA synchronous=FULL')
        try: self.initialize()
        except Exception:
            self.connection.close(); raise

    def initialize(self):
        try:
            self.connection.execute('BEGIN IMMEDIATE')
            version = self.connection.execute('PRAGMA user_version').fetchone()[0]
            tables = {r[0] for r in self.connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if version == 0 and not tables:
                for statement in DDL: self.connection.execute(statement)
                self.connection.execute('PRAGMA user_version=3')
            else: self.migrate(version)
            self._schema()
            self.connection.execute('COMMIT')
        except (ValueError, sqlite3.Error):
            if self.connection.in_transaction: self.connection.execute('ROLLBACK')
            raise

    def migrate(self, version):
        """Registered compatibility entrypoint; exact schema1/2 migrates to schema3.

        No speculative migrations. Future registered steps must run in the caller's
        transaction and preserve historical checkpoint bytes, not rewrite results.
        """
        if type(version) is not int or version not in SCHEMA_HANDLERS: raise IntegrityError('Unsupported storage schema version')
        if version != self.connection.execute('PRAGMA user_version').fetchone()[0]: raise IntegrityError('Migration version differs from actual schema')
        return SCHEMA_HANDLERS[version](self.connection)

    def _schema(self):
        if self.connection.execute('PRAGMA user_version').fetchone()[0] != SCHEMA_VERSION: raise IntegrityError('Unsupported storage schema')
        expected = {statement.split('(')[0].split()[-1]: statement for statement in DDL}
        actual = dict(self.connection.execute("SELECT name,sql FROM sqlite_master WHERE type='table'"))
        if actual != expected: raise IntegrityError('Storage schema differs from versioned contract')
        if self.connection.execute('PRAGMA quick_check').fetchone()[0] != 'ok': raise IntegrityError('Corrupt database')
        if self.connection.execute('PRAGMA foreign_key_check').fetchall(): raise IntegrityError('Broken storage reference')

    def _head(self, company_id, case_id):
        row = self.connection.execute('SELECT revision FROM heads WHERE company_id=? AND case_id=?', (company_id, case_id)).fetchone()
        latest = self.connection.execute('SELECT max(revision) FROM checkpoints WHERE company_id=? AND case_id=?', (company_id, case_id)).fetchone()[0]
        if (row[0] if row else None) != latest: raise IntegrityError('Checkpoint head contradicts committed history')
        return row[0] if row else 0

    def _write_objects(self, company_id, case_id, revision, manifest):
        # Separate seam supports deterministic interrupted-write testing. A fault
        # at any row is contained by the surrounding actual SQLite transaction.
        for kind, key, payload, checksum in manifest:
            self.connection.execute('INSERT INTO objects VALUES(?,?,?,?,?,?,?)', (company_id, case_id, revision, kind, key, payload, checksum))

    def save(self, case, company_id, company_context, expected_revision):
        if type(expected_revision) is not int or expected_revision < 0: raise RevisionConflict('Explicit expected revision required')
        doc = snapshot(case, company_id, company_context)
        payload = dumps(doc); checksum = sha(payload); manifest = objects(doc)
        try:
            self.connection.execute('BEGIN IMMEDIATE'); self._schema()
            current = self._head(company_id, case.id)
            if current != expected_revision: raise RevisionConflict('Checkpoint revision changed')
            from .recovery import reject_pending
            reject_pending(self, company_id, case.id)
            revision = self._save_doc(doc, expected_revision)
            self.connection.execute('COMMIT')
            return revision
        except (ValueError, sqlite3.Error, OSError) as exc:
            if self.connection.in_transaction: self.connection.execute('ROLLBACK')
            if isinstance(exc, ValueError): raise
            raise StorageError('Checkpoint write failed; previous committed revision retained') from exc
        except BaseException:
            if self.connection.in_transaction: self.connection.execute('ROLLBACK')
            raise

    def _save_doc(self, doc, expected_revision, operation_id=None):
        """Caller owns BEGIN/COMMIT; operation outcome and head publish together."""
        company_id, case_id = doc['company_id'], doc['root_case']
        current = self._head(company_id, case_id)
        if current != expected_revision: raise RevisionConflict('Checkpoint revision changed')
        payload = dumps(doc); checksum = sha(payload); manifest = objects(doc)
        previous = None
        if current:
            # Validate the retained head before extending its immutable chain.
            prior_doc, previous = self._read(company_id, case_id, current)
            restore(prior_doc, company_id, case_id)
            validate_extension(prior_doc, doc)
        revision = current + 1
        self.connection.execute('INSERT INTO checkpoints VALUES(?,?,?,?,?,?,?,?)', (company_id, case_id, revision, payload, checksum, previous, len(manifest), operation_id))
        self._write_objects(company_id, case_id, revision, manifest)
        self.connection.execute('INSERT INTO heads VALUES(?,?,?) ON CONFLICT(company_id,case_id) DO UPDATE SET revision=excluded.revision', (company_id, case_id, revision))
        return revision

    def prepare(self, case, company_id, company_context, expected_revision, intent):
        from .recovery import prepare
        return prepare(self, case, company_id, company_context, expected_revision, intent)

    def recover(self, company_id, case_id, operation_id):
        from .recovery import recover
        return recover(self, company_id, case_id, operation_id)

    def abandon(self, company_id, case_id, operation_id, reason):
        from .recovery import abandon
        return abandon(self, company_id, case_id, operation_id, reason)

    def operation(self, company_id, case_id, operation_id):
        from .recovery import read_operation
        try:
            self.connection.execute('BEGIN'); self._schema()
            value = read_operation(self, company_id, case_id, operation_id)
            self.connection.execute('COMMIT')
            return value
        except BaseException:
            if self.connection.in_transaction: self.connection.execute('ROLLBACK')
            raise

    def _read(self, company_id, case_id, revision):
        row = self.connection.execute('SELECT payload,sha256,previous_sha256,object_count,operation_id FROM checkpoints WHERE company_id=? AND case_id=? AND revision=?', (company_id, case_id, revision)).fetchone()
        if row is None: raise IntegrityError('Missing committed checkpoint')
        payload, checksum, previous, count, operation_id = row
        if operation_id is not None:
            binding = self.connection.execute('SELECT company_id,case_id,base_revision,prepared_revision FROM operations WHERE operation_id=?', (operation_id,)).fetchone()
            if binding is None or binding[:2] != (company_id, case_id) or revision not in (binding[3], binding[3]+1):
                raise IntegrityError('Missing/wrong durable operation checkpoint binding')
            events = self.connection.execute('SELECT sequence,status,payload,sha256 FROM operation_events WHERE operation_id=? ORDER BY sequence', (operation_id,)).fetchall()
            if not events or events[0][:2] != (0, 'PREPARED') or any(seq != i or sha(wire) != checksum for i,(seq,status,wire,checksum) in enumerate(events)):
                raise IntegrityError('Missing/corrupt durable operation event population')
            if revision == binding[3]+1:
                if events[-1][1] != 'COMMITTED': raise IntegrityError('Outcome checkpoint lacks committed operation')
                outcome = loads(events[-1][2])
                if not isinstance(outcome, dict) or outcome.get('revision') != revision or outcome.get('checkpoint_sha256') != checksum:
                    raise IntegrityError('Operation outcome checkpoint hash differs')

        if sha(payload) != checksum: raise IntegrityError('Corrupted checkpoint payload')
        doc = loads(payload)
        if not isinstance(doc, dict) or (doc.get('company_id'), doc.get('root_case')) != (company_id, case_id): raise IntegrityError('Wrong checkpoint namespace')
        manifest = self.connection.execute('SELECT kind,object_id,payload,sha256 FROM objects WHERE company_id=? AND case_id=? AND revision=? ORDER BY kind,object_id', (company_id, case_id, revision)).fetchall()
        if len(manifest) != count or manifest != objects(doc): raise IntegrityError('Missing/changed durable object manifest')
        if revision == 1:
            if previous is not None: raise IntegrityError('Unexpected initial checkpoint predecessor')
        else:
            old = self.connection.execute('SELECT sha256 FROM checkpoints WHERE company_id=? AND case_id=? AND revision=?', (company_id, case_id, revision - 1)).fetchone()
            if old is None or old[0] != previous: raise IntegrityError('Broken checkpoint revision chain')
        return doc, checksum

    def load(self, company_id, case_id, revision=None):
        try:
            self.connection.execute('BEGIN'); self._schema()
            head = self._head(company_id, case_id)
            revision = head if revision is None else revision
            if type(revision) is not int or not 1 <= revision <= head: raise IntegrityError('Unknown checkpoint revision')
            doc, _ = self._read(company_id, case_id, revision)
            root = restore(doc, company_id, case_id)
            # A valid native head alone cannot hide damaged recovery markers.
            # All marker reads share this same SQLite read snapshot.
            from .recovery import read_operation
            for (operation_id,) in self.connection.execute('SELECT operation_id FROM operations WHERE company_id=? AND case_id=? ORDER BY prepared_revision', (company_id, case_id)):
                read_operation(self, company_id, case_id, operation_id)
            self.connection.execute('COMMIT')
            return root, revision, copy_context(doc)
        except (ValueError, sqlite3.Error) as exc:
            if self.connection.in_transaction: self.connection.execute('ROLLBACK')
            if isinstance(exc, ValueError): raise
            raise StorageError('Checkpoint read failed closed') from exc

    def memory(self):
        from .memory import CompanyMemory
        return CompanyMemory(self)

    def close(self): self.connection.close()
    def __enter__(self): return self
    def __exit__(self, *args): self.close()


def copy_context(doc):
    import copy
    return copy.deepcopy(doc['company_context'])
