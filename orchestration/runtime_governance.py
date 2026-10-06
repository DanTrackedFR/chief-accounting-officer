"""Case/Period/version normalization for the existing CAO graph.

Native inputs are never re-certified or rewritten by normalization. Compatibility
calendars explicitly retain unknown fiscal starts; supplied registries are replayed.
"""
from dataclasses import asdict
from .periods import PeriodRegistry,FiscalCalendar,compatibility_period,Period
from .cases import CaseRegistry,case_identity
from .scopes import scope_registry
from .versions import VersionedExecution,Dependency


def attach(c,graph,context,inputs,request):
    scopes=scope_registry(context)
    explicit=context.get('period_registry')
    if explicit:
        periods=PeriodRegistry.from_record(explicit) if 'history' in explicit else PeriodRegistry(explicit['calendars'],explicit['periods'],explicit.get('relationships',[]))
    else:
        normalized={}
        for n in graph.nodes.values():
            s=scopes.get(n.scope_id)
            ctx=dict(scope_id=n.scope_id,period_start=n.period[0],reporting_period=n.period[1],reporting_calendar=s.reporting_calendar)
            p=compatibility_period(ctx);normalized[p.period_id]=p
        primary=compatibility_period(dict(context,scope_id=context['entity']))
        normalized[primary.period_id]=primary
        calendars=[FiscalCalendar(key,'Unspecified fiscal start in supplied bounded context',None,None,('supplied-governed-context',)) for key in sorted({p.calendar_id for p in normalized.values()})]
        periods=PeriodRegistry(calendars,normalized.values())
    cases=CaseRegistry(scopes,periods)
    cycle=c.id
    def period_for(scope,start,end,key=None):
        if key:
            p=periods.get(key)
            if (p.start,p.end)!=(start,end):raise ValueError('Case Period dates differ')
            return p
        matches=[p for p in periods.periods.values() if (p.start,p.end)==(start,end) and (not scopes.get(scope).reporting_calendar or p.calendar_id==scopes.get(scope).reporting_calendar)]
        if not explicit:
            key=compatibility_period(dict(scope_id=scope,period_start=start,reporting_period=end,reporting_calendar=scopes.get(scope).reporting_calendar)).period_id
            return periods.get(key)
        if len(matches)!=1:raise ValueError('Resolve exact Case Period/calendar identity')
        return matches[0]
    primary=period_for(context['entity'],context['period_start'],context['reporting_period'],context.get('period_id'))
    c.id=case_identity(context['entity'],primary.period_id,c.objective,cycle)
    cases.register(c,context['entity'],primary.period_id,cycle,provenance=('supplied-governed-objective',))
    by={(c.scope_id,c.period_id):c}
    for n in graph.nodes.values():
        p=period_for(n.scope_id,*n.period,n.period_id or None);n.period_id=p.period_id
        if (n.scope_id,p.period_id) not in by:
            from .runtime import Case
            child=Case(case_identity(n.scope_id,p.period_id,c.objective,cycle),c.objective)
            # Compatibility creates work containers, never infers Case parentage
            # from the organizational Scope graph.
            cases.register(child,n.scope_id,p.period_id,cycle,provenance=('supplied-governed-workplan',))
            by[(n.scope_id,p.period_id)]=child
        n.case_id=by[(n.scope_id,p.period_id)].id;cases.bind_node(n.case_id,n)
    session=VersionedExecution(graph,cases,periods);c.governance=session
    session.sources=inputs;session.context=context;session.request=request
    explicit_edges={}
    for row in request.get('temporal_dependencies',[]):
        edge=Dependency(**row);explicit_edges[(edge.producer_node,edge.consumer_node)]=edge
    for n in graph.nodes.values():
        for upstream in list(n.dependencies):
            producer=graph.nodes[upstream];edge=explicit_edges.get((upstream,n.id))
            if edge is None:
                if producer.period_id==n.period_id:kind='CURRENT';alignment=()
                elif explicit:raise ValueError('Explicit cross-Period dependency contract required')
                else:kind='QUALIFIED_ALIGNMENT';alignment=('Existing separately reviewed native dependency; checked before result publication',)
                edge=Dependency(upstream,n.id,producer.case_id,n.case_id,producer.scope_id,n.scope_id,producer.period_id,n.period_id,kind,'SAME_CASE' if producer.case_id==n.case_id else 'EXPLICIT_CROSS_CASE',('case_fingerprint',),('Native exact-result dependency',),required=n.required,material=n.material,alignment_evidence=alignment)
            session.add_dependency(edge)
    return session


def publish(session,n,source):
    session.periods.authorize_execution(n.period_id,n.case_id,n.id)
    receipts=[session.receipt(k) for k,e in sorted(session.edges.items()) if e.consumer_node==n.id]
    for r in receipts:session.validate_receipt(r,n.id)
    version=session.versions.publish(n,n.result,source,[(r['dependency_id'],r['result_version']) for r in receipts],'Initial native CAO execution')
    n.execution_receipt.update(result_version=version.version_id,period_id=n.period_id,case_id=n.case_id,currentness='CURRENT')
    session.receipts.extend(receipts);session.cases.refresh(session.graph,session.versions,session.edges)


def finish(c):
    session=c.governance
    # Currentness was reconciled before ordinary synthesis. Preserve the public
    # objective outcome, which can include qualified work in independent Cases.
    for child in session.cases.cases.values():
        if child is c:continue
        nodes=[session.graph.nodes[k] for k in child.node_refs]
        child.accounting_issues=[dict(owner=n.selected_skill,scope_id=n.scope_id,period_id=n.period_id) for n in nodes]
        child.evidence_refs=[v for n in nodes for v in n.evidence]
        child.owner_results=[dict(n.execution_receipt) for n in nodes if n.status=='complete']
        child.challenge_results=[dict(node=n.id,status=n.status,open_items=list(n.open_items)) for n in nodes]
        child.observer_ran=True;child.artifacts=[dict(type='governed-case-record',source_case=child.id)]
        for status in ('SCOPED','IN_PROGRESS','CHALLENGE','CONCLUDED','DOCUMENTED'):child.transition(status)
        if child.outcome=='complete':child.transition('CLOSED')


def adopt(session,node,source):
    scopes=session.cases.scopes
    if not node.period_id:
        node.period_id=source.get('period_id') or compatibility_period(dict(scope_id=node.scope_id,period_start=node.period[0],reporting_period=node.period[1],reporting_calendar=scopes.get(node.scope_id).reporting_calendar)).period_id
    session.periods.get(node.period_id)
    matches=[c for c in session.cases.cases.values() if (c.scope_id,c.period_id)==(node.scope_id,node.period_id)]
    if len(matches)!=1:raise ValueError('Supplemental node requires exact governed Case')
    node.case_id=matches[0].id;session.cases.bind_node(node.case_id,node)
    for key in node.dependencies:
        producer=session.graph.nodes[key]
        edge=Dependency(key,node.id,producer.case_id,node.case_id,producer.scope_id,node.scope_id,producer.period_id,node.period_id,'CURRENT' if producer.period_id==node.period_id else 'QUALIFIED_ALIGNMENT','SAME_CASE' if producer.case_id==node.case_id else 'EXPLICIT_CROSS_CASE',('case_fingerprint',),('Existing qualified supplemental result',),alignment_evidence=('Existing scoped receipt contract',) if producer.period_id!=node.period_id else ())
        session.add_dependency(edge)


def reconcile(session):
    changed=[]
    for node_id in session.versions.active:
        node=session.graph.nodes[node_id]
        version=session.versions.current(node_id,allow_stale=True)
        if node.status!='complete' and session.versions.state(version.version_id)=='CURRENT':
            session.versions.mark_stale(version.version_id,'CHALLENGE','Native challenge invalidation');changed.append(version.version_id)
    while changed:
        upstream=changed.pop(0)
        for key in sorted(session.versions.active):
            version=session.versions.current(key,allow_stale=True)
            bindings=[edge for edge,bound in version.dependency_bindings if bound==upstream]
            if bindings and session.versions.state(version.version_id)=='CURRENT':
                session.versions.mark_stale(version.version_id,bindings[0],upstream);changed.append(version.version_id)
    session.cases.refresh(session.graph,session.versions,session.edges)
