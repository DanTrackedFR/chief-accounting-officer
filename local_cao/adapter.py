"""Version1 execution facade. No accounting methods, certification or approval here.

Private immutable request files are input staging, not a second Case/memory store.
The existing SQLiteStore is the only durable accounting-state authority.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
from contextlib import contextmanager
from .context import parse, scope, identity
from orchestration.runtime import CAO
from orchestration.registry import Registry
from orchestration.planning import FACT_ADAPTERS
from orchestration.periods import compatibility_period
from orchestration.cases import case_identity
from orchestration.persistence import SQLiteStore
from orchestration.intake.sources import bounded, MAX_BYTES
from interfaces.public_output import public_record

VERSION = '1.0'
OPERATIONS = ('initialize', 'diagnose', 'context', 'capabilities', 'start', 'status',
              'questions', 'submit', 'execute', 'result', 'resume', 'list',
              'investigate', 'document', 'continue_investigation', 'investigation', 'correct_investigation', 'rework_investigation')
ERRORS = {'runtime_installation': 'Use Python 3.12 or newer on Linux/macOS or WSL with POSIX file locking.', 'invalid_request': 'Check contract version, operation and required input fields.',
          'invalid_context': 'Correct missing, duplicate or contradictory company-context fields.',
          'workspace_boundary': 'Use regular files inside the selected private workspace; symlinks are rejected.',
          'identity_conflict': 'Company, entity, period or existing submission identity differs; select the original workspace.',
          'immutable_submission': 'Prior evidence is immutable. Use a separately identified Case for new evidence; governed selective rework remains a native operation.',
          'not_found': 'The selected Case or evidence file is unavailable in this company workspace.',
          'storage_failure': 'Accounting state could not be validated or committed. Preserve files and inspect trusted local storage.',
          'public_boundary': 'Accounting delivery is blocked pending safe output review.'}


class Failure(ValueError):
    def __init__(self, code): self.code = code


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def decode(text):
    def pairs(rows):
        out = {}
        for k, v in rows:
            if k in out: raise Failure('invalid_request')
            out[k] = v
        return out
    return json.loads(text, object_pairs_hook=pairs,
        parse_constant=lambda _: (_ for _ in ()).throw(Failure('invalid_request')))


def checked_path(path):
    path = Path(os.path.abspath(path))
    for p in (path, *path.parents):
        if p.is_symlink(): raise Failure('workspace_boundary')
    return path


def immutable(path, value):
    text = canonical(value)
    if path.exists():
        if canonical(decode(path.read_text())) != text: raise Failure('immutable_submission')
        return
    fd, temporary = tempfile.mkstemp(prefix='.input-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as f:
            f.write(text+'\n'); f.flush(); os.fsync(f.fileno())
        try: os.link(temporary, path)
        except FileExistsError:
            if canonical(decode(path.read_text())) != text: raise Failure('immutable_submission')
        directory = os.open(path.parent, os.O_RDONLY)
        try: os.fsync(directory)
        finally: os.close(directory)
    finally: os.unlink(temporary)


class ExecutionInterface:
    """Caller supplies a trusted host-selected workspace, never a wire-level path."""
    def __init__(self, workspace, model_provider=None):
        self.workspace = Path(workspace); self.model_provider = model_provider

    def _path(self, relative):
        root = checked_path(self.workspace)
        if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
            raise Failure('workspace_boundary')
        path = checked_path(root / relative)
        if not path.is_relative_to(root) or path == root: raise Failure('workspace_boundary')
        return path

    def read_json(self, relative):
        path = self._path(relative)
        if not path.is_file(): raise Failure('workspace_boundary')
        if path.stat().st_size > MAX_BYTES: raise Failure('invalid_request')
        value = decode(path.read_text()); bounded(value)
        return value

    @contextmanager
    def _lock(self):
        # Host-local serialization, not distributed authorization. Kernel releases
        # flock on process termination, including crashes. SQLite owns Case atomicity.
        import fcntl
        root = checked_path(self.workspace)
        root.mkdir(mode=0o700, parents=True, exist_ok=True)
        path = self._path('adapter.lock')
        fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            yield
        finally: os.close(fd)

    def _configuration(self, company):
        marker = self.read_json('workspace.json')
        if marker != {'contract_version': VERSION, 'company_id': company}:
            raise Failure('identity_conflict')
        path = self._path('company-context.md')
        if not path.is_file(): raise Failure('workspace_boundary')
        if path.stat().st_size > 100_000: raise Failure('invalid_context')
        try: context = parse(path.read_text())
        except (ValueError, ArithmeticError): raise Failure('invalid_context') from None
        if context['company']['company_id'] != company: raise Failure('identity_conflict')
        return context

    def call(self, request):
        company = None; operation = None
        try:
            if sys.version_info < (3, 12) or sys.platform == 'win32': raise Failure('runtime_installation')
            bounded(request)
            if len(canonical(request).encode()) > MAX_BYTES: raise Failure('invalid_request')
            if not isinstance(request, dict): raise Failure('invalid_request')
            operation = request.get('operation'); company = identity(request.get('company_id'))
            if request.get('contract_version') != VERSION or operation not in OPERATIONS:
                raise Failure('invalid_request')
            allowed = {'contract_version', 'operation', 'company_id', 'case_id', 'objective',
                       'request_id', 'target_family', 'evidence', 'evidence_file', 'route',
                       'context', 'interpretation', 'document', 'event_id', 'node_id', 'reason'}
            if set(request)-allowed: raise Failure('invalid_request')
            from intelligence.contracts import validate as validate_intelligence_request
            validate_intelligence_request(request)
            with self._lock(): result = self._call(request, company, operation)
            return dict(contract_version=VERSION, operation=operation, company_id=company,
                        ok=True, **result)
        except Failure as exc: code = exc.code
        except ImportError: code = 'runtime_installation'
        except FileNotFoundError: code = 'not_found'
        except (ValueError, TypeError, KeyError, ArithmeticError, RecursionError): code = 'invalid_request'
        except (OSError, sqlite3.Error): code = 'storage_failure'
        return dict(contract_version=VERSION, operation=operation if operation in OPERATIONS else None,
                    ok=False, error={'code': code, 'message': ERRORS[code]},
                    public_result=public_record(dict(status='blocked', guidance=ERRORS[code]), route='tool_output'))

    def _store(self):
        path = self._path('accounting.sqlite3')
        if path.exists() and not path.is_file(): raise Failure('workspace_boundary')
        try: return SQLiteStore(path)
        except (ValueError, sqlite3.Error): raise Failure('storage_failure') from None

    def _call(self, r, company, operation):
        if operation == 'initialize':
            path = self._path('company-context.md')
            if not path.is_file(): raise Failure('workspace_boundary')
            if path.stat().st_size > 100_000: raise Failure('invalid_context')
            try: config = parse(path.read_text())
            except (ValueError, ArithmeticError): raise Failure('invalid_context') from None
            if config['company']['company_id'] != company: raise Failure('identity_conflict')
            immutable(self._path('workspace.json'), dict(contract_version=VERSION, company_id=company))
            with self._store(): pass
            return {'execution_state': 'workspace_ready', 'context_authority': 'user_assertion'}
        config = self._configuration(company)
        from intelligence.engine import OPS, handle
        if operation in OPS: return handle(self, r, company, config)
        if operation == 'context':
            # Only execution configuration, never private narrative/policy contents.
            s = {k: v for k, v in scope(config).items() if k != 'scopes'}
            for value in s.values(): public_record({'guidance': str(value)}, route='tool_output')
            return dict(configuration=s, context_authority='user_assertion',
                        approved_company_memory=False)
        if operation in ('capabilities', 'diagnose'):
            result = self._capabilities()
            if operation == 'diagnose':
                with self._store() as store: store.memory().audit(company)
                public_record(dict(status='blocked', guidance='Installation and public boundary ready; no accounting conclusion requested.'), route='tool_output')
                result.update(execution_state='workspace_ready', python_minimum='3.12',
                    dependencies='Python standard library', context_valid=True, storage_ready=True)
            return result
        if operation == 'start': return self._start(r, config)
        if operation == 'list':
            folder = self._path('requests')
            items = []
            if folder.exists():
                for path in sorted(folder.glob('*.json')):
                    d = self.read_json('requests/'+path.name)
                    if d['company_id'] != company: raise Failure('identity_conflict')
                    # Validate original scope/identity even when no checkpoint exists.
                    self._request(d['case_id'], config)
                    items.append({'case_id': d['case_id']})
            return {'cases': items}
        d, folder = self._request(r.get('case_id'), config)
        if 'context_snapshot' in d:
            if operation == 'submit':
                if 'evidence_file' in r: evidence = self.read_json(r['evidence_file'])
                else: evidence = r.get('evidence')
                if not isinstance(evidence,dict): raise Failure('invalid_request')
                immutable(folder / 'intake.json', evidence)
                return dict(case_id=d['case_id'], execution_state='evidence_staged', evidence_authority='native_intake_required')
            return handle(self,r,company,config)
        with self._store() as store:
            head = store.connection.execute('SELECT revision FROM heads WHERE company_id=? AND case_id=?',
                                             (company, d['case_id'])).fetchone()
            if operation == 'submit':
                if ('evidence' in r) == ('evidence_file' in r): raise Failure('invalid_request')
                evidence = r['evidence'] if 'evidence' in r else self.read_json(r['evidence_file'])
                self._evidence(evidence, d)
                if head and (not (folder / 'evidence.json').exists() or self.read_json(str((folder / 'evidence.json').relative_to(checked_path(self.workspace)))) != evidence):
                    raise Failure('immutable_submission')
                immutable(folder / 'evidence.json', evidence)
                return dict(case_id=d['case_id'], execution_state='evidence_staged',
                            evidence_authority='supplied_native_workpaper_not_adapter_approved')
            if head:
                try: case, revision, _ = store.load(company, d['case_id'])
                except (ValueError, sqlite3.Error): raise Failure('storage_failure') from None
                return self._delivery(case, revision, r.get('route', 'tool_output'))
            if operation in ('result', 'resume'): raise Failure('not_found')
            evidence_path = folder / 'evidence.json'
            evidence = self.read_json(str(evidence_path.relative_to(checked_path(self.workspace)))) if evidence_path.exists() else {}
            native = copy.deepcopy(d['native_request'])
            if operation == 'execute': native.update(evidence)
            elif evidence:
                return dict(case_id=d['case_id'], lifecycle_state='OPEN', execution_state='blocked',
                    checkpoint_revision=None, durable=False, currentness='NOT_EXECUTED', workplan=[],
                    public_result=public_record(dict(status='blocked', guidance='Reviewed workpaper is staged; accounting has not executed.',
                        open_items=['Invoke execute for the staged workpaper before requesting an accounting result.']), route=r.get('route', 'tool_output')))
            case = CAO().run(native)
            if case.outcome == 'complete':
                owner = FACT_ADAPTERS[d['target_family']][0]
                targets = [n for n in case.graph.nodes.values() if n.selected_skill == owner]
                if not targets or any(n.status != 'complete' for n in targets):
                    raise Failure('invalid_request')
            if hasattr(case, 'governance') and case.id != d['case_id']: raise Failure('identity_conflict')
            if operation == 'execute' and hasattr(case, 'governance') and case.governance.versions.active:
                try: revision = store.save(case, company, [], 0)
                except ValueError: raise Failure('storage_failure') from None
                return self._delivery(case, revision, r.get('route', 'tool_output'))
            if operation in ('result', 'resume'): raise Failure('not_found')
            return self._delivery(case, None, r.get('route', 'tool_output'), d)

    def _capabilities(self):
        rows = []
        for s in Registry().snapshot():
            families = [f for f, (p, _) in FACT_ADAPTERS.items() if p == s['package']]
            ready = s['production_available'] and s['execution_available']
            descriptor = public_record(dict(guidance=s['package'], status=s['status'],
                open_items=[str(x) for x in s.get('inputs', [])],
                limitations=['Availability is conditional on native knowledge, applicability and input review gates.']), route='tool_output')
            rows.append(dict(package=s['package'], fact_families=families,
                production_declared=s['production_available'], executor_present=s['execution_available'],
                local_fact_adapter=bool(families) and ready, public_contract=descriptor))
        return {'capabilities': rows}

    def _start(self, r, config):
        cycle = identity(r.get('request_id'))
        objective = r.get('objective')
        if not isinstance(objective, str) or not objective.strip() or len(objective)>4000:
            raise Failure('invalid_request')
        # Reject opaque private tokens before any model-facing preview.
        public_record({'guidance': objective}, route='tool_output')
        family = r.get('target_family')
        if family not in FACT_ADAPTERS: raise Failure('invalid_request')
        s = scope(config); p = compatibility_period(s)
        cid = case_identity(s['entity'], p.period_id, objective, cycle)
        native = dict(case_id=cycle, objective=objective, scope=s, company_context=[], facts={})
        d = dict(company_id=config['company']['company_id'], case_id=cid,
                 target_family=family, native_request=native)
        requests = self._path('requests'); requests.mkdir(mode=0o700, exist_ok=True)
        # Request identity also prevents a changed objective from becoming a retry.
        immutable(requests / (cycle+'.json'), d)
        folder = self._path('submissions/'+hashlib.sha256(cid.encode()).hexdigest())
        folder.mkdir(mode=0o700, parents=True, exist_ok=True)
        case = CAO().run(native)
        return self._delivery(case, None, r.get('route', 'tool_output'), d)

    def _request(self, cid, config):
        identity(cid)
        requests = self._path('requests')
        matches = []
        if requests.exists():
            for path in requests.glob('*.json'):
                d = self.read_json('requests/'+path.name)
                if d.get('case_id') == cid: matches.append(d)
        if len(matches) != 1: raise Failure('not_found')
        d = matches[0]
        if d['company_id'] != config['company']['company_id']: raise Failure('identity_conflict')
        n = d['native_request']; s = n['scope']; p = compatibility_period(s)
        if case_identity(s['entity'], p.period_id, n['objective'], n['case_id']) != cid:
            raise Failure('identity_conflict')
        if 'context_snapshot' not in d and s != scope(config): raise Failure('identity_conflict')
        return d, self._path('submissions/'+hashlib.sha256(cid.encode()).hexdigest())

    def _evidence(self, e, d):
        bounded(e)
        if not isinstance(e, dict) or set(e)-{'facts', 'handoffs', 'challenge_assertions',
                'journal_account_mapping', 'journal_pack_review', 'reviewed_scope_packs'}:
            raise Failure('invalid_request')
        if not isinstance(e.get('facts'), dict): raise Failure('invalid_request')
        if d['target_family'] not in e['facts']: raise Failure('invalid_request')
        target = e['facts'][d['target_family']]
        rows = target if isinstance(target, list) else [target]
        fields = FACT_ADAPTERS[d['target_family']][1]
        if not rows or any(not isinstance(row, dict) or not any(row.get(k) for k in fields) or row.get('required_for_objective') is False for row in rows):
            raise Failure('invalid_request')
        # Native approvals are supplied inert workpaper records. Adapter never
        # creates/refreshes reviewer seals or imports context-policy approvals.
        s = d['native_request']['scope']
        for family, value in e['facts'].items():
            if family == 'task_attributes': continue
            if family not in FACT_ADAPTERS: raise Failure('invalid_request')
            for row in value if isinstance(value, list) else [value]:
                if not isinstance(row, dict): raise Failure('invalid_request')
                for key in ('entity', 'scope_id', 'framework', 'jurisdiction', 'period_start', 'reporting_period', 'functional_currency'):
                    if key in row and row[key] != s[key]: raise Failure('identity_conflict')

    def _delivery(self, case, revision, route, d=None):
        try: output = CAO().public(case, route)
        except (ValueError, TypeError, KeyError): raise Failure('public_boundary') from None
        if d and not revision:
            requirements = ['Supply controlled structured evidence and independently reviewed native workpapers before execution.']
            if d.get('target_family'):
                owner, fields = FACT_ADAPTERS[d['target_family']]
                requirements.append('Provide '+d['target_family'].replace('_', ' ')+' workpaper including '+', '.join(fields)+'.')
                if d['target_family'] == 'reconciliation':
                    requirements.append('Supply the account reconciliation, current and comparative trial balances, additions and consumption support, and investigation thresholds.')
                if d['target_family'] == 'customer_contract':
                    requirements.append('Supply the signed agreement, transaction price, performance obligations, delivery evidence and reviewed revenue workpaper.')
                requirements.append('Consult the '+owner+' input contract and preserve its source and review references.')
            output['open_items'] = output.get('open_items', [])+requirements
            output = public_record(output, route=route)
        currentness = 'NOT_EXECUTED' if not revision else 'CURRENT'
        if hasattr(case, 'governance'):
            g = case.governance
            states = [g.versions.state(v) for v in g.versions.active.values()]
            view = sorted((n, v, g.versions.state(v)) for n, v in g.versions.active.items())
            if any(v != 'CURRENT' for v in states) or (case.conclusions and getattr(case, '_synthesis_currentness', None) != view):
                currentness = 'STALE'
        result = dict(case_id=d['case_id'] if d else case.id, lifecycle_state=case.status,
            execution_state=output['status'], checkpoint_revision=revision,
            durable=revision is not None, currentness=currentness, public_result=output)
        result['workplan'] = [dict(owner=n.selected_skill, state=n.status) for n in case.graph.nodes.values()]
        return result
