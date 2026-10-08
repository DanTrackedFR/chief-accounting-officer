"""Native governed checkpoint contract v1; restoration executes no accounting."""
import copy
from dataclasses import asdict, fields
from orchestration.runtime import Case, CAO, digest
from orchestration.scopes import ScopeRegistry, execution_identity
from orchestration.periods import PeriodRegistry, identity
from orchestration.cases import CaseRegistry
from orchestration.planning import Graph, Node
from orchestration.versions import VersionedExecution, ResultVersion, Dependency, fingerprint
from .codec import dumps, loads, IntegrityError
from .evidence import validate as validate_evidence

CONTRACT_VERSION = 1
CASE_PRIVATE = {'_synthesis_currentness', '_journal_mapping', '_scoped_postings', '_public_calculation_order', '_source_qualification_refs'}
SESSION_DATA = {'context', 'request', 'sources', 'evidence_bundles'}
ROOT_FIELDS = {'contract_version', 'company_id', 'root_case', 'company_context', 'scopes', 'periods', 'cases', 'case_private', 'nodes', 'graph_history', 'dependencies', 'versions', 'source_snapshots', 'active', 'states', 'supersession', 'version_history', 'receipts', 'rework_history', 'session'}


def exact_fields(row, cls):
    if not isinstance(row, dict) or set(row) != {f.name for f in fields(cls)}:
        raise IntegrityError('Unsupported/incomplete '+cls.__name__+' fields')


def snapshot(root, company_id, company_context):
    """Complete governed session, including all sibling/history objects.

    company_id is a supplied stable namespace, never inferred from display names.
    Company Context is the runtime's governed record population, not approved memory.
    """
    if not isinstance(company_id, str) or not company_id.strip(): raise IntegrityError('Company identity required')
    if not isinstance(company_context, list) or any(not isinstance(r, dict) for r in company_context):
        raise IntegrityError('Governed Company Context records required')
    e = root.governance
    if e.cases.get(root.id) is not root or getattr(root, 'graph', None) is not e.graph: raise IntegrityError('Root runtime object differs')
    unknown = set(vars(e)) - {'cao', 'graph', 'cases', 'periods', 'edges', 'versions', 'receipts', 'rework_history'} - SESSION_DATA
    if unknown: raise IntegrityError('Unregistered session metadata: '+','.join(sorted(unknown)))
    private = {}
    for key, case in e.cases.cases.items():
        unknown = set(vars(case)) - set(Case.__dataclass_fields__) - CASE_PRIVATE - {'graph', 'governance'}
        if unknown: raise IntegrityError('Unregistered Case metadata: '+','.join(sorted(unknown)))
        private[key] = {k: copy.deepcopy(getattr(case, k)) for k in sorted(CASE_PRIVATE) if hasattr(case, k)}
        # Native public calculations are an ordered row list derived from this
        # mapping. Preserve that delivery provenance separately from sorted JSON.
        private[key]['_public_calculation_order'] = [list(s.get('calculations', {})) for s in case.conclusions]
    doc = dict(contract_version=CONTRACT_VERSION, company_id=company_id, root_case=root.id,
        company_context=copy.deepcopy(company_context), scopes=e.cases.scopes.record(), periods=e.periods.record(),
        cases=[asdict(e.cases.cases[k]) for k in sorted(e.cases.cases)], case_private=private,
        nodes=[asdict(e.graph.nodes[k]) for k in sorted(e.graph.nodes)], graph_history=copy.deepcopy(e.graph.history),
        dependencies={k: asdict(e.edges[k]) for k in sorted(e.edges)},
        versions={k: asdict(e.versions.versions[k]) for k in sorted(e.versions.versions)},
        source_snapshots=copy.deepcopy(e.versions.source_snapshots), active=copy.deepcopy(e.versions.active),
        states=copy.deepcopy(e.versions.states), supersession=copy.deepcopy(e.versions.supersession),
        version_history=copy.deepcopy(e.versions.history), receipts=copy.deepcopy(e.receipts),
        rework_history=copy.deepcopy(e.rework_history),
        session={k: copy.deepcopy(dict(getattr(e, k))) for k in sorted(SESSION_DATA) if hasattr(e, k)})
    # Validate the same wire contract before storage, on an independent object graph.
    doc = loads(dumps(doc))
    restore(doc, company_id, root.id)
    return doc


def _case_lifecycle(case):
    history = case.transitions
    if not isinstance(history, list) or not history or history[0] != 'OPEN': raise IntegrityError('Missing Case transition history')
    replay = Case(case.id, case.objective)
    replay.challenge_results = copy.deepcopy(case.challenge_results)
    replay.artifacts = copy.deepcopy(case.artifacts); replay.observer_ran = case.observer_ran
    # Past complete closure may precede a legitimate current partial REWORK.
    replay.outcome = 'complete'
    reworks = 0
    for event in history[1:]:
        if event == 'REWORK':
            if replay.status not in ('CLOSED', 'DOCUMENTED', 'CONCLUDED'): raise IntegrityError('Invalid Case rework transition')
            replay.status = 'IN_PROGRESS'; reworks += 1
        else: replay.transition(event)
    if replay.status != case.status: raise IntegrityError('Stored Case status differs from transition history')
    if reworks > sum(r.get('reason') == 'Material dependencies require governed rework' for r in case.governance_history):
        raise IntegrityError('Missing rework history')
    if case.outcome not in ('blocked', 'partial', 'complete'): raise IntegrityError('Unknown Case outcome')
    if case.status == 'CLOSED' and case.outcome != 'complete': raise IntegrityError('False Case closure')
    if case.status in ('CONCLUDED', 'DOCUMENTED', 'CLOSED') and not case.challenge_results: raise IntegrityError('Missing challenge state')
    if case.status in ('DOCUMENTED', 'CLOSED') and not case.artifacts: raise IntegrityError('Missing Case documentation')


def _versions(e, doc):
    registry = e.versions
    if set(doc['versions']) != set(doc['states']) or set(doc['versions']) != set(doc['source_snapshots']):
        raise IntegrityError('Missing result version/source/state')
    for key, row in doc['versions'].items():
        exact_fields(row, ResultVersion)
        v = ResultVersion(**row)
        if key != v.version_id or v.node_id not in e.graph.nodes: raise IntegrityError('Wrong result identity')
        n = e.graph.nodes[v.node_id]
        if (v.case_id, v.scope_id, v.period_id) != (n.case_id, n.scope_id, n.period_id): raise IntegrityError('Result dimensions differ')
        if v.result_id != identity('result', [n.id, n.case_id, n.scope_id, n.period_id]): raise IntegrityError('Substituted result ID')
        payload = v.payload(); source = doc['source_snapshots'][key]
        if fingerprint(payload) != v.result_fingerprint or fingerprint(source) != v.source_fingerprint or payload.get('case_fingerprint') != v.exact_case_fingerprint:
            raise IntegrityError('Source/result fingerprint mismatch')
        if payload.get('status') not in ('complete', 'blocked') or not v.reason: raise IntegrityError('Unqualified result payload')
        content = [v.result_id, v.predecessor, v.exact_case_fingerprint, v.source_fingerprint, v.result_fingerprint, sorted(v.dependency_bindings), v.reason]
        if identity('version', content) != key: raise IntegrityError('Substituted immutable version')
        if source.get('scope_id', source.get('entity')) != v.scope_id: raise IntegrityError('Source Scope differs')
        if 'period_id' in source:
            if source['period_id'] != v.period_id: raise IntegrityError('Source Period differs')
        elif (source.get('period_start'), source.get('reporting_period')) != tuple(n.period):
            raise IntegrityError('Legacy source execution interval differs')
        native_currency = n.functional_currency or n.presentation_currency
        if source.get('framework', n.framework) != n.framework or source.get('functional_currency', native_currency) != native_currency:
            raise IntegrityError('Source framework/currency differs')
        registry.versions[key] = v
    # Replay governance events, not accounting owners or result publication.
    states = {}; active = {}; supersession = {}; published = set()
    for event in doc['version_history']:
        kind = event.get('event')
        if kind == 'PUBLISH':
            if set(event) != {'event', 'version', 'predecessor', 'reason'}: raise IntegrityError('Unknown publication history fields')
            key = event['version']
            if key in published or key not in registry.versions: raise IntegrityError('Missing/duplicated publication')
            v = registry.versions[key]
            if event['reason'] != v.reason or event['predecessor'] != v.predecessor or active.get(v.node_id) != v.predecessor:
                raise IntegrityError('Inconsistent supersession history')
            incoming = {k for k, edge in e.edges.items() if edge.consumer_node == v.node_id}
            if {k for k, _ in v.dependency_bindings} != incoming or len(v.dependency_bindings) != len(incoming):
                raise IntegrityError('Incomplete result dependency bindings')
            for dep, bound in v.dependency_bindings:
                edge = e.edges[dep]; producer = registry.versions.get(bound)
                if producer is None or bound not in published or producer.node_id != edge.producer_node or states[bound] != 'CURRENT' or active.get(producer.node_id) != bound:
                    raise IntegrityError('Wrong-version dependency at publication')
            if v.predecessor:
                states[v.predecessor] = 'SUPERSEDED'; supersession[v.predecessor] = key
            states[key] = 'CURRENT'; active[v.node_id] = key; published.add(key)
        elif kind == 'STALE':
            if set(event) != {'event', 'version', 'dependency', 'upstream'} or states.get(event['version']) != 'CURRENT': raise IntegrityError('Invalid stale history')
            v = registry.versions[event['version']]
            if event['dependency'] != 'CHALLENGE' and (event['dependency'], event['upstream']) not in v.dependency_bindings:
                raise IntegrityError('Stale cause differs from exact binding')
            states[event['version']] = 'STALE'
        elif kind == 'RESTATEMENT_LINEAGE':
            if set(event) != {'event', 'original_version', 'restated_version', 'approval', 'accounting_authority'} or event['accounting_authority'] is not False:
                raise IntegrityError('Invalid correction history')
            old, new = event['original_version'], event['restated_version']
            if old not in published or new not in published or registry.versions[new].predecessor != old:
                raise IntegrityError('Broken restatement lineage')
            approval = event['approval']
            if set(approval) != {'status', 'evidence', 'convention'} or approval['status'] != 'APPROVED' or not approval['evidence'] or approval['convention'] != 'SYNTHETIC_GOVERNED':
                raise IntegrityError('Missing existing synthetic approval')
        else: raise IntegrityError('Unknown version history event')
    if published != set(registry.versions) or (states, active, supersession) != (doc['states'], doc['active'], doc['supersession']):
        raise IntegrityError('Registry currentness contradicts immutable history')
    registry.states = copy.deepcopy(states); registry.active = copy.deepcopy(active)
    registry.supersession = copy.deepcopy(supersession); registry.history = copy.deepcopy(doc['version_history'])
    registry.source_snapshots = copy.deepcopy(doc['source_snapshots'])
    for key in registry.active.values():
        v = registry.versions[key]; n = e.graph.nodes[v.node_id]
        if states[key] == 'CURRENT': registry.require_current(key)
        if (n.status == 'complete' and n.result is None) or (n.result is not None and fingerprint(n.result) != v.result_fingerprint): raise IntegrityError('Node/current result differs')
        if n.status == 'complete' and states[key] != 'CURRENT': raise IntegrityError('Stale result claims complete execution')
        if n.execution_receipt.get('result_version') != key or n.execution_receipt.get('currentness') not in ('CURRENT', 'STALE') or (states[key] == 'CURRENT' and n.execution_receipt.get('currentness') != 'CURRENT'):
            raise IntegrityError('Node receipt/result currentness differs')
        if fingerprint(e.sources.get(n.id)) != v.source_fingerprint: raise IntegrityError('Latest source differs from active version')


def _receipts(e):
    # Historical receipts remain inert. Validate them against their original
    # producer version; never change CURRENT labels to authorize current use.
    from orchestration.runtime import at
    from collections import Counter
    expected_bindings = Counter(binding for version in e.versions.versions.values()
        if version.payload().get('status') == 'complete' for binding in version.dependency_bindings)
    actual_bindings = Counter((r.get('dependency_id'), r.get('result_version')) for r in e.receipts)
    if actual_bindings != expected_bindings:
        raise IntegrityError('Typed receipt history population differs')
    for receipt in e.receipts:
        dep = receipt.get('dependency_id'); key = receipt.get('result_version')
        if dep not in e.edges or key not in e.versions.versions: raise IntegrityError('Missing receipt dependency/result')
        edge = e.edges[dep]; v = e.versions.versions[key]
        producer = e.graph.nodes[edge.producer_node]; consumer = e.graph.nodes[edge.consumer_node]
        payload = v.payload(); source = e.versions.source_snapshots[key]
        value_currency = payload.get('currency', producer.functional_currency or producer.presentation_currency)
        if producer.economic_id is not None and producer.selected_skill == 'foreign-currency' and tuple(edge.metric_path)[:2] == ('calculations', 'translation'):
            value_currency = source['translation']['presentation_currency']
        expected = dict(dependency_id=edge.id, result_version=v.version_id, producer_node=edge.producer_node, consumer_node=edge.consumer_node,
            producer_scope=edge.producer_scope, consumer_scope=edge.consumer_scope, producer_period=edge.producer_period, consumer_period=edge.consumer_period,
            producer_framework=payload.get('framework', producer.framework), consumer_framework=consumer.framework,
            producer_functional_currency=producer.functional_currency, producer_presentation_currency=producer.presentation_currency,
            consumer_functional_currency=consumer.functional_currency, consumer_presentation_currency=consumer.presentation_currency,
            value_currency=value_currency, metric_path=list(edge.metric_path), currentness='CURRENT', result_fingerprint=v.result_fingerprint,
            value=copy.deepcopy(at(payload, edge.metric_path)))
        if v.node_id != edge.producer_node or receipt != expected: raise IntegrityError('Receipt dimensions/version/layer/value differ')
        if not any((dep, key) in x.dependency_bindings for x in e.versions.versions.values() if x.node_id == edge.consumer_node):
            raise IntegrityError('Receipt was never consumed by governed version')


def _history_references(e):
    """Validate persisted history references, without resuming any rework."""
    def consumed(node, dep, upstream):
        edge = e.edges.get(dep)
        if edge is None or edge.consumer_node != node or upstream not in e.versions.versions:
            return False
        return any(v.node_id == node and (dep, upstream) in v.dependency_bindings for v in e.versions.versions.values())
    for event in e.graph.history:
        node = event.get('node')
        if node not in e.graph.nodes: raise IntegrityError('Graph history node absent')
        kind = event.get('event')
        if kind == 'version-invalidation':
            if set(event) != {'node', 'event', 'upstream', 'dependencies'} or not event['dependencies'] or any(not consumed(node, dep, event['upstream']) for dep in event['dependencies']):
                raise IntegrityError('Graph invalidation references differ')
        elif kind == 'invalidate':
            if set(event) != {'node', 'event', 'reason'} or not event['reason']: raise IntegrityError('Invalid graph challenge history')
        elif kind == 'reopen':
            if set(event) != {'node', 'event'}: raise IntegrityError('Invalid graph reopening history')
        else: raise IntegrityError('Unknown graph history event')
    for plan in e.rework_history:
        required = {'changed_upstream', 'old_version', 'new_version', 'direct', 'transitive', 'unaffected', 'execution_order', 'affected_cases', 'affected_periods', 'causes'}
        if set(plan) != required: raise IntegrityError('Unknown rework history contract')
        old = e.versions.versions.get(plan['old_version']); new = e.versions.versions.get(plan['new_version'])
        if old is None or new is None or new.predecessor != old.version_id or new.node_id != old.node_id or plan['changed_upstream'] != new.node_id:
            raise IntegrityError('Broken correction/rework lineage')
        affected = set(plan['direct']) | set(plan['transitive'])
        if set(plan['direct']) & set(plan['transitive']) or not affected <= set(e.graph.nodes) or set(plan['unaffected']) & (affected | {new.node_id}) or not set(plan['unaffected']) <= set(e.graph.nodes):
            raise IntegrityError('Rework partition references differ')
        if plan['execution_order'] != e.topological(affected): raise IntegrityError('Rework topology differs')
        if plan['affected_cases'] != sorted({e.graph.nodes[k].case_id for k in affected}) or plan['affected_periods'] != sorted({e.graph.nodes[k].period_id for k in affected}):
            raise IntegrityError('Rework Case/Period references differ')
        for cause in plan['causes']:
            if set(cause) != {'node', 'dependency', 'upstream_version'} or cause['node'] not in affected or not consumed(cause['node'], cause['dependency'], cause['upstream_version']):
                raise IntegrityError('Rework cause references differ')
        if {c['node'] for c in plan['causes']} != affected: raise IntegrityError('Missing rework causes')
    for case in e.cases.cases.values():
        for event in case.governance_history:
            if set(event) != {'previous_status', 'previous_outcome', 'result_versions', 'reason'} or event['previous_status'] not in ('OPEN', 'SCOPED', 'IN_PROGRESS', 'CHALLENGE', 'CONCLUDED', 'DOCUMENTED', 'CLOSED') or event['previous_outcome'] not in ('complete', 'partial', 'blocked'):
                raise IntegrityError('Invalid Case governance history')
            if any(key not in e.versions.versions or e.versions.versions[key].case_id != case.id for key in event['result_versions']):
                raise IntegrityError('Case governance history version absent/contaminated')
    for event in e.periods.reopenings:
        if any(k not in e.cases.cases for k in event['case_ids']) or any(k not in e.graph.nodes for k in event['node_ids']):
            raise IntegrityError('Period authorization reference absent')
        if any(e.graph.nodes[k].period_id != event['period_id'] or e.graph.nodes[k].case_id not in event['case_ids'] for k in event['node_ids']):
            raise IntegrityError('Period authorization dimensions differ')


def restore(doc, expected_company_id, expected_case_id):
    """Construct native registries and objects, validate all references, no execution."""
    try:
        return _restore(doc, expected_company_id, expected_case_id)
    except (ValueError, KeyError, TypeError, AttributeError, ArithmeticError, StopIteration, RecursionError) as exc:
        raise IntegrityError('Governed checkpoint rejected: '+str(exc)) from exc


def _restore(doc, company_id, case_id):
    if not isinstance(doc, dict) or set(doc) != ROOT_FIELDS or type(doc['contract_version']) is not int or doc['contract_version'] != CONTRACT_VERSION:
        raise IntegrityError('Unsupported checkpoint contract')
    if doc['company_id'] != company_id or doc['root_case'] != case_id: raise IntegrityError('Wrong Company/Case checkpoint')
    if not isinstance(doc['company_context'], list) or any(not isinstance(r, dict) for r in doc['company_context']): raise IntegrityError('Wrong Company Context population')
    scopes = ScopeRegistry(doc['scopes']); periods = PeriodRegistry.from_record(doc['periods']); cases = CaseRegistry(scopes, periods)
    pending = list(doc['cases']); originals = {}
    while pending:
        ready = [r for r in pending if r['parent_case_id'] is None or r['parent_case_id'] in cases.cases]
        if not ready: raise IntegrityError('Missing/cyclic parent Case')
        for row in sorted(ready, key=lambda r: r['id']):
            exact_fields(row, Case)
            c = Case(**copy.deepcopy(row)); originals[c.id] = copy.deepcopy(row)
            children = list(c.child_case_ids)
            cases.register(c, c.scope_id, c.period_id, c.cycle, c.parent_case_id, c.provenance)
            for name in ('scope_id', 'period_id', 'case_type', 'cycle', 'parent_case_id', 'provenance'):
                if dumps(getattr(c, name)) != dumps(row[name]):
                    raise IntegrityError('Stored Case contract was normalized: '+name)
            c.child_case_ids = []
            _case_lifecycle(c); pending.remove(row)
    if set(doc['case_private']) != set(cases.cases): raise IntegrityError('Missing private Case provenance')
    for key, c in cases.cases.items():
        if sorted(c.child_case_ids) != sorted(originals[key]['child_case_ids']) or len(set(originals[key]['child_case_ids'])) != len(originals[key]['child_case_ids']):
            raise IntegrityError('Parent/child contamination')
        # Retain original governed reference ordering exactly.
        c.child_case_ids = copy.deepcopy(originals[key]['child_case_ids'])
        private = doc['case_private'][key]
        if set(private) - CASE_PRIVATE: raise IntegrityError('Unknown Case private metadata')
        for name, value in private.items(): setattr(c, name, copy.deepcopy(value))
        order = private.get('_public_calculation_order')
        if not isinstance(order, list) or len(order) != len(c.conclusions): raise IntegrityError('Missing public calculation provenance')
        for conclusion, keys in zip(c.conclusions, order):
            values = conclusion.get('calculations', {})
            if len(set(keys)) != len(keys) or set(keys) != set(values): raise IntegrityError('Public calculation provenance differs')
            if 'calculations' in conclusion: conclusion['calculations'] = {k: values[k] for k in keys}
    graph = Graph()
    for row in sorted(doc['nodes'], key=lambda n: n['id']):
        exact_fields(row, Node); n = Node(**copy.deepcopy(row))
        s = scopes.get(n.scope_id); p = periods.get(n.period_id)
        ctx = dict(scope_id=s.scope_id, scope_type=s.scope_type, framework=s.framework, jurisdiction=s.jurisdiction,
            functional_currency=s.functional_currency, presentation_currency=s.presentation_currency, period_start=p.start, reporting_period=p.end, period_id=p.period_id)
        if n.economic_id is not None: ctx['economic_id'] = n.economic_id
        # Legacy runtime normalized Period after computing its original node ID.
        legacy = dict(ctx); legacy.pop('period_id')
        identities = {execution_identity(n.selected_skill, ctx), execution_identity(n.selected_skill, legacy)}
        if n.issue == 'diagnostic accounting follow-up':
            for question in cases.get(n.case_id).accounting_questions:
                if question.get('target_owner') == n.selected_skill and n.logical_id == 'diagnostic-'+question['id']:
                    identities |= {key+':recheck:'+digest(question['id']) for key in tuple(identities)}
        if n.id not in identities:
            raise IntegrityError('Execution identity differs')
        if (n.entity, n.scope_type, n.framework, n.jurisdiction, n.functional_currency, n.presentation_currency, n.period) != (s.scope_id, s.scope_type, s.framework, s.jurisdiction, s.functional_currency, s.presentation_currency, [p.start, p.end]):
            raise IntegrityError('Node Scope/Period/framework/currency differs')
        if n.id not in cases.get(n.case_id).node_refs: raise IntegrityError('Missing Case node binding')
        graph.add(n); cases.bind_node(n.case_id, n)
    before = {k: sorted(n.downstream_consumers) for k, n in graph.nodes.items()}
    graph.validate()
    if before != {k: sorted(n.downstream_consumers) for k, n in graph.nodes.items()}: raise IntegrityError('Broken downstream graph reference')
    graph.history = copy.deepcopy(doc['graph_history'])
    e = VersionedExecution(graph, cases, periods)
    session = doc['session']
    if set(session) - SESSION_DATA or 'sources' not in session: raise IntegrityError('Incomplete/unknown session metadata')
    for name, value in session.items(): setattr(e, name, copy.deepcopy(value))
    context = getattr(e, 'context', {})
    if 'company_id' in context and context['company_id'] != company_id:
        raise IntegrityError('Company identity differs from runtime Context')
    if 'company_context' in context and context['company_context'] != doc['company_context']:
        raise IntegrityError('Company Context record population differs')
    for key, row in sorted(doc['dependencies'].items()):
        exact_fields(row, Dependency); edge = Dependency(**row)
        if edge.id != key: raise IntegrityError('Dependency identity differs')
        e.add_dependency(edge)
    # The graph validates membership independently of input iteration order.
    # Preserve the original native ledger ordering after that validation.
    for row in doc['nodes']:
        graph.nodes[row['id']].downstream_consumers = copy.deepcopy(row['downstream_consumers'])
    if any(set(n.dependencies) != {edge.producer_node for edge in e.edges.values() if edge.consumer_node == n.id} for n in graph.nodes.values()):
        raise IntegrityError('Undeclared execution dependency')
    _versions(e, doc)
    e.receipts = copy.deepcopy(doc['receipts']); _receipts(e)
    e.rework_history = copy.deepcopy(doc['rework_history'])
    _history_references(e)
    qualified = {}
    for key, bundle in getattr(e, 'evidence_bundles', {}).items(): qualified.update(validate_evidence(key, bundle, e))
    linked = set()
    for c in cases.cases.values():
        refs = getattr(c, '_source_qualification_refs', [])
        if not isinstance(refs, list) or len(set(refs)) != len(refs) or any(key not in getattr(e, 'evidence_bundles', {}) for key in refs):
            raise IntegrityError('Missing exact Case intake qualification archive')
        linked.update(refs)
    if linked != set(getattr(e, 'evidence_bundles', {})):
        raise IntegrityError('Unlinked source qualification archive')
    for key, source in e.versions.source_snapshots.items():
        if (source.get('qualified_input_snapshot') or source.get('qualified_scope_sources')) and fingerprint(source) not in qualified: raise IntegrityError('Missing sealed source/ReviewedInputPack')
    for c in cases.cases.values():
        if any(k not in graph.nodes or graph.nodes[k].case_id != c.id for k in c.node_refs) or len(set(c.node_refs)) != len(c.node_refs): raise IntegrityError('Case node contamination')
        expected = [e.versions.active[n] for n in c.node_refs if n in e.versions.active]
        if c.result_version_refs != expected: raise IntegrityError('Case result references differ')
        if c.outcome == 'complete':
            required = [graph.nodes[k] for k in c.node_refs if graph.nodes[k].required or graph.nodes[k].material is not False]
            if not required or any(n.status not in ('complete', 'not_applicable') or (n.status != 'not_applicable' and (n.id not in e.versions.active or e.versions.states[e.versions.active[n.id]] != 'CURRENT' or e.versions.current(n.id).payload().get('unresolved_dependencies'))) for n in required):
                raise IntegrityError('False completed Case prerequisites')
            if any(q.get('kind') in ('blocking', 'confirmation') for q in c.open_questions): raise IntegrityError('Completed Case has material questions')
        if hasattr(c, '_synthesis_currentness'):
            if c.conclusions and c._synthesis_currentness != sorted((n, k, e.versions.state(k)) for n, k in e.versions.active.items()):
                raise IntegrityError('Stale public synthesis provenance')
    root = cases.get(case_id); root.graph = graph; root.governance = e
    # Public output uses the existing allowlist. Persistence never emits internals.
    CAO().public(root)
    return root
