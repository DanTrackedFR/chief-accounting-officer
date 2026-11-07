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


class ClientValidation(ValueError):
    def __init__(self, requirements): self.requirements = requirements


class ExecutionInterface:
    """Caller supplies a trusted host-selected workspace, never a wire-level path."""
    def __init__(self, workspace, model_provider=None, *, allow_prepared_unreviewed=False, allow_presumed_user_sources=False):
        if type(allow_prepared_unreviewed) is not bool: raise ValueError('Host enablement must be boolean')
        if type(allow_presumed_user_sources) is not bool: raise ValueError('Host enablement must be boolean')
        if allow_presumed_user_sources and not allow_prepared_unreviewed: raise ValueError('Presumed sources require prepared execution')
        self.allow_presumed_user_sources = allow_presumed_user_sources
        self.allow_prepared_unreviewed = allow_prepared_unreviewed
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
        company = None; operation = None; requirements = []
        try:
            if sys.version_info < (3, 12) or sys.platform == 'win32': raise Failure('runtime_installation')
            from local_cao.validation import requirements as request_requirements
            needs = request_requirements(request) if self.allow_presumed_user_sources else []
            if needs: raise ClientValidation(needs)
            bounded(request)
            if len(canonical(request).encode()) > MAX_BYTES: raise Failure('invalid_request')
            if not isinstance(request, dict): raise Failure('invalid_request')
            operation = request.get('operation'); company = identity(request.get('company_id'))
            if request.get('contract_version') != VERSION or operation not in OPERATIONS:
                raise Failure('invalid_request')
            allowed = {'contract_version', 'operation', 'company_id', 'case_id', 'objective',
                       'request_id', 'target_family', 'evidence', 'evidence_file', 'route',
                       'context', 'interpretation', 'document', 'event_id', 'node_id', 'reason', 'review_mode', 'source_assurance'}
            if set(request)-allowed: raise Failure('invalid_request')
            if 'review_mode' in request:
                if request['review_mode'] not in ('formal', 'prepared_unreviewed'): raise Failure('invalid_request')
                if operation not in ('start', 'submit', 'execute', 'status', 'questions', 'result', 'resume'): raise Failure('invalid_request')
                if request['review_mode'] == 'prepared_unreviewed' and not self.allow_prepared_unreviewed: raise Failure('invalid_request')
            if 'source_assurance' in request:
                if request['source_assurance'] != 'presumed_user_provided' or not self.allow_presumed_user_sources or operation not in ('start','submit','execute','status','questions','result','resume'): raise Failure('invalid_request')
            from intelligence.contracts import validate as validate_intelligence_request
            validate_intelligence_request(request)
            with self._lock(): result = self._call(request, company, operation)
            return dict(contract_version=VERSION, operation=operation, company_id=company,
                        ok=True, **result)
        except ClientValidation as exc: code = 'invalid_request'; requirements = exc.requirements
        except Failure as exc: code = exc.code
        except ImportError: code = 'runtime_installation'
        except FileNotFoundError: code = 'not_found'
        except (ValueError, TypeError, KeyError, ArithmeticError, RecursionError): code = 'invalid_request'
        except (OSError, sqlite3.Error): code = 'storage_failure'
        if self.allow_presumed_user_sources and code == 'invalid_request' and not requirements:
            requirements = [dict(identifier='request.shape',field_path='$',explanation='Check the submitted fields and types against the execution contract.',category='invalid_shape')]
        return dict(contract_version=VERSION, operation=operation if operation in OPERATIONS else None,
                    ok=False, error={'code': code, 'message': ERRORS[code], **({'requirements': requirements} if requirements else {})},
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
        mode = d.get('review_mode', 'formal')
        if r.get('review_mode', mode) != mode: raise Failure('identity_conflict')
        assurance = d.get('source_assurance')
        if r.get('source_assurance', assurance) != assurance: raise Failure('identity_conflict')
        if assurance is not None and (assurance != 'presumed_user_provided' or not self.allow_presumed_user_sources or mode != 'prepared_unreviewed'): raise Failure('invalid_request')
        if mode == 'prepared_unreviewed' and not self.allow_prepared_unreviewed: raise Failure('invalid_request')
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
            if operation == 'execute':
                if mode == 'prepared_unreviewed' and evidence: self._evidence(evidence, d)
                native.update(evidence)
                if mode == 'prepared_unreviewed':
                    for value in native.get('facts', {}).values():
                        for row in value if isinstance(value, list) else [value]:
                            row['review_mode'] = mode
                            row['package'] = FACT_ADAPTERS[d['target_family']][0]
                            if assurance is not None: row['source_assurance'] = assurance
            elif evidence:
                return dict(case_id=d['case_id'], lifecycle_state='OPEN', execution_state='blocked',
                    checkpoint_revision=None, durable=False, currentness='NOT_EXECUTED', workplan=[],
                    public_result=public_record(dict(status='blocked', guidance='Reviewed workpaper is staged; accounting has not executed.',
                        open_items=['Invoke execute for the staged workpaper before requesting an accounting result.']), route=r.get('route', 'tool_output')))
            case = CAO(allow_prepared_unreviewed=self.allow_prepared_unreviewed,allow_presumed_user_sources=self.allow_presumed_user_sources).run(native)
            if case.outcome == 'complete':
                owner = FACT_ADAPTERS[d['target_family']][0]
                targets = [n for n in case.graph.nodes.values() if n.selected_skill == owner]
                if not targets or any(n.status != 'complete' for n in targets):
                    raise Failure('invalid_request')
            if hasattr(case, 'governance') and case.id != d['case_id']: raise Failure('identity_conflict')
            if operation == 'execute' and hasattr(case, 'governance') and (case.governance.versions.active or mode == 'prepared_unreviewed'):
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
        mode = r.get('review_mode', 'formal')
        if mode == 'prepared_unreviewed':
            if not self.allow_prepared_unreviewed or family not in ('machinery', 'supplier_cost'): raise Failure('invalid_request')
        s = scope(config); p = compatibility_period(s)
        # A structured private cycle cannot alias a legal formal request ID.
        # Keep historical formal cycles byte-for-byte unchanged.
        assurance = r.get('source_assurance')
        if assurance is not None and (mode != 'prepared_unreviewed' or not self.allow_presumed_user_sources): raise Failure('invalid_request')
        if mode == 'prepared_unreviewed': cycle = canonical([cycle, mode] if assurance is None else [cycle, mode, assurance])
        cid = case_identity(s['entity'], p.period_id, objective, cycle)
        native = dict(case_id=cycle, objective=objective, scope=s, company_context=[], facts={})
        d = dict(company_id=config['company']['company_id'], case_id=cid,
                 target_family=family, native_request=native)
        if mode == 'prepared_unreviewed': d['review_mode'] = mode
        if assurance is not None: d['source_assurance'] = assurance
        requests = self._path('requests'); requests.mkdir(mode=0o700, exist_ok=True)
        # Request identity also prevents a changed objective from becoming a retry.
        immutable(requests / (identity(r.get('request_id'))+'.json'), d)
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
        if 'context_snapshot' not in d:
            mode=d.get('review_mode','formal');assurance=d.get('source_assurance')
            if mode=='formal':
                identity(n['case_id'])
                if assurance is not None:raise Failure('identity_conflict')
            elif mode=='prepared_unreviewed':
                try:cycle=decode(n['case_id'])
                except ValueError:raise Failure('identity_conflict') from None
                if not isinstance(cycle,list) or len(cycle)!=(3 if assurance is not None else 2) or cycle[1]!=mode or (assurance is not None and (assurance!='presumed_user_provided' or cycle[2]!=assurance)):
                    raise Failure('identity_conflict')
                identity(cycle[0])
            else:raise Failure('identity_conflict')
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
        if d.get('review_mode') == 'prepared_unreviewed':
            if set(e) != {'facts'} or set(e['facts']) != {d['target_family']}: raise Failure('invalid_request')
            from prepared_execution import reject_records
            reject_records(e)
            for row in rows:
                if row.get('review_mode', 'prepared_unreviewed') != 'prepared_unreviewed' or row.get('package', FACT_ADAPTERS[d['target_family']][0]) != FACT_ADAPTERS[d['target_family']][0]: raise Failure('invalid_request')
                if 'imports' in row: raise Failure('invalid_request')
        else:
            if any(row.get('review_mode', 'formal') != 'formal' for row in rows): raise Failure('invalid_request')
        for row in rows:
            if row.get('source_assurance', d.get('source_assurance')) != d.get('source_assurance'): raise Failure('invalid_request')
            if d.get('source_assurance') is not None and (not isinstance(row.get('case_id'),str) or not row['case_id'].strip() or len(row['case_id'])>256):
                raise ClientValidation([dict(identifier='missing.source_case',field_path='evidence.facts.'+d['target_family']+'.case_id',explanation='Supply the source accounting Case binding.',category='missing_fact')])
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
        try:
            output = CAO().public(case, route)
            prepared = [n.result for n in case.graph.nodes.values() if n.result and n.result.get('review_mode') == 'prepared_unreviewed']
            if prepared:
                from production import to_public
                if len(prepared) != 1: raise Failure('invalid_request')
                native_output = output
                result = prepared[0]
                output = to_public(result, route)
                unresolved = [n for n in case.graph.nodes.values() if n.result is not result and n.status in ('blocked', 'partial') and (n.required or n.material is not False)]
                if unresolved or case.open_questions:
                    output['accounting_determination'] = 'UNRESOLVED'
                    output['evidence_sufficiency'] = 'INSUFFICIENT'
                    output['open_items'] = list(native_output.get('open_items', []))
                    output['guidance'] += '\nThe calculations above are supported within the accounting owner scope. Resolve the listed evidence or investigation gaps to complete the wider objective.'
                metrics = ('depreciation', 'closing_cost', 'closing_accumulated', 'closing_cip') if result['skill_id'] == 'SKILL-FA-001' else ('opening_ap', 'invoices', 'payments', 'closing_ap', 'closing_accruals')
                output['calculations'] = [dict(label=k.replace('_', ' '), amount=str(result['calculations'][k])) for k in metrics if k in result['calculations']]
                output = public_record(output, route=route)
        except (ValueError, TypeError, KeyError): raise Failure('public_boundary') from None
        if d and not revision:
            requirements = ['Supply controlled structured evidence before execution.'] if d.get('review_mode') == 'prepared_unreviewed' else ['Supply controlled structured evidence and independently reviewed native workpapers before execution.']
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
