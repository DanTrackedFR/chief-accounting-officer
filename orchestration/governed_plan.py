"""Serializable governed graph intake for the same CAO execution/version substrate."""
from dataclasses import asdict
from .periods import PeriodRegistry
from .scopes import ScopeRegistry,execution_identity
from .cases import CaseRegistry
from .planning import Graph,Node
from .versions import VersionedExecution,Dependency
from .runtime_governance import finish


def observation(node,source,receipts):
    from .runtime import digest
    if source.get('method')!='QUALIFIED_LOCAL_OBSERVATION' or not source.get('evidence'):raise ValueError('Reviewed bounded observation contract required')
    if len(receipts)>1:raise ValueError('No cross-currency/framework aggregation authority')
    if receipts and source.get('observation_currency')!=receipts[0]['value_currency']:raise ValueError('Observation cannot relabel a qualified receipt currency')
    value=receipts[0]['value'] if receipts else source['value']
    return dict(status='complete',case_fingerprint=digest([source,receipts]),observed_amount=value,accounting_authority=False,currency=source['observation_currency'],framework=receipts[0]['producer_framework'] if receipts else node.framework,restated=source.get('restated',False),limitations=['Local observation only; no framework/currency conversion or consolidated total.'])


def run(c,request):
    from .runtime import Case
    plan=request['governed_plan']
    if set(plan)!={'scopes','periods','cases','root_case','nodes','dependencies','sources'}:raise ValueError('Complete serialized governed plan required')
    scopes=ScopeRegistry(plan['scopes']);periods=PeriodRegistry.from_record(plan['periods']);cases=CaseRegistry(scopes,periods)
    pending=list(plan['cases'])
    while pending:
        ready=[row for row in pending if row['parent_id'] is None or row['parent_id'] in cases.cases]
        if not ready:raise ValueError('Case parent cycle or absent parent')
        for row in sorted(ready,key=lambda r:r['case_id']):
            if row['case_id']==plan['root_case']:
                if row['objective']!=c.objective:raise ValueError('Root Case objective changed')
                candidate=c;c.id=row['case_id']
            else:candidate=Case(row['case_id'],row['objective'])
            cases.register(candidate,row['scope_id'],row['period_id'],row['cycle'],row['parent_id'],row['provenance']);pending.remove(row)
    if plan['root_case'] not in cases.cases or cases.get(plan['root_case']) is not c:raise ValueError('Unknown root Case')
    graph=Graph();c.graph=graph
    for row in plan['nodes']:
        node=Node(**row);scope=scopes.get(node.scope_id);period=periods.get(node.period_id)
        context=dict(scope_id=scope.scope_id,scope_type=scope.scope_type,framework=scope.framework,jurisdiction=scope.jurisdiction,functional_currency=scope.functional_currency,presentation_currency=scope.presentation_currency,period_start=period.start,reporting_period=period.end,period_id=period.period_id)
        if node.id!=execution_identity(node.selected_skill,context) or node.period!=[period.start,period.end] or node.result is not None or node.status!='pending':raise ValueError('Governed execution-node substitution')
        if (node.scope_type,node.entity,node.framework,node.jurisdiction,node.functional_currency,node.presentation_currency)!=(scope.scope_type,scope.scope_id,scope.framework,scope.jurisdiction,scope.functional_currency,scope.presentation_currency):raise ValueError('Governed node framework/currency/Scope substitution')
        graph.add(node);cases.bind_node(node.case_id,node)
    session=VersionedExecution(graph,cases,periods);c.governance=session;session.sources=plan['sources'];session.context=request.get('scope',{})
    for row in plan['dependencies']:session.add_dependency(Dependency(**row))
    graph.validate();c.scope_registry=scopes.record();c.entities=[c.scope_id];root_period=periods.get(c.period_id);c.periods=[root_period.start,root_period.end];c.frameworks=[scopes.get(c.scope_id).framework];c.jurisdictions=[scopes.get(c.scope_id).jurisdiction]
    c.transition('SCOPED');c.transition('IN_PROGRESS')
    for node_id in session.topological(graph.nodes):
        node=graph.nodes[node_id]
        session.execute(node_id,observation,plan['sources'][node_id],'Initial governed CAO execution')
        c.execution_ledger.append(dict(node=node_id,status=node.status,result_version=session.versions.current(node_id).version_id))
    c.workplan_nodes=graph.record();c.owner_results=[n.execution_receipt for n in graph.nodes.values() if n.status=='complete']
    c.challenge_results=[dict(kind='governed-currentness',status='PASS',dependencies=len(session.edges))]
    c.transition('CHALLENGE');c.transition('CONCLUDED')
    session.cao._observe(c,dict(entity=c.scope_id,period_start=root_period.start,reporting_period=root_period.end),request)
    c.artifacts=[dict(type='governed-case-record',source_case=c.id)]
    c.transition('DOCUMENTED')
    if c.outcome=='complete':c.transition('CLOSED')
    finish(c)
