"""Explicit current-result observations across Scopes, without conversion authority."""
import copy
from .runtime import digest, number
from .scopes import execution_scopes, execution_identity,scoped_context
from .planning import Node


def validate_scoped_receipt(receipt,graph,inputs,target,context):
    required={'source_owner','source_node','source_scope','target_node','target_scope','semantic_metric',
        'framework','currency','functional_currency','presentation_currency','result_fingerprint',
        'exact_case_fingerprint','currentness','economic_identity','result','evidence','consumption_type'}
    if not isinstance(receipt,dict) or set(receipt)!=required or not receipt['evidence']: raise ValueError('Explicit typed scoped receipt required')
    node=graph.nodes.get(receipt['source_node'])
    if not node or receipt['source_node']!=node.id or node.status!='complete': raise ValueError('Current producing execution node required')
    if receipt['target_node']!=target.id or receipt['target_scope']!=target.scope_id or node.id not in target.dependencies: raise ValueError('Receipt target execution differs')
    if receipt['source_scope']!=node.scope_id or receipt['source_owner']!=node.selected_skill: raise ValueError('Wrong-Scope result substitution')
    if receipt['framework']!=node.framework or receipt['currency']!=(node.functional_currency or node.presentation_currency): raise ValueError('Framework/currency contamination')
    if receipt['functional_currency']!=node.functional_currency or receipt['presentation_currency']!=node.presentation_currency: raise ValueError('Currency dimension relabelled')
    if receipt['currentness']!='CURRENT' or receipt['result_fingerprint']!=digest(node.result) or digest(receipt['result'])!=digest(node.result): raise ValueError('Stale or substituted scoped result')
    if receipt['exact_case_fingerprint']!=node.result['case_fingerprint']: raise ValueError('Exact execution fingerprint differs')
    actual_context=execution_scopes(context)[node.scope_id]
    source=inputs[node.id]
    from .runtime import dimensions
    if dimensions(source)!=(node.scope_id,node.framework,node.jurisdiction,*node.period,actual_context['currency']): raise ValueError('Producer source dimensions contaminated')
    if receipt['economic_identity']!=[node.scope_id,node.id,'period_revenue',node.result['case_fingerprint']]: raise ValueError('Receipt economic identity differs')
    if receipt['source_owner']!='revenue-recognition' or receipt['semantic_metric']!='period_revenue': raise ValueError('Unregistered observation semantic')
    if receipt['consumption_type']!='LOCAL_RESULT_OBSERVATION' or target.scope_type not in ('GROUP','SUBGROUP') or node.scope_type!='LEGAL_ENTITY': raise ValueError('Unqualified cross-Scope consumption')
    return node


def consume_group(contract,graph,inputs,context,case):
    if not isinstance(contract,dict) or set(contract)-{'qualified_context_fingerprint'}!={'scope_id','expected_producers','receipts','context_source'}: raise ValueError('Explicit Group observation contract required')
    scopes=execution_scopes(context);scope=scopes.get(contract['scope_id'])
    if not scope or scope['scope_type'] not in ('GROUP','SUBGROUP'): raise ValueError('Group consumer needs reporting Scope')
    scope=scoped_context(context,{'entity':contract['scope_id']})
    source=contract['context_source']
    if not isinstance(source,dict) or set(source)!={'source_id','scope_id','framework','currency','evidence'} or not source['source_id'] or not source['evidence']: raise ValueError('Group context source required')
    if (source['scope_id'],source['framework'],source['currency'])!=(scope['scope_id'],scope['framework'],scope['currency']): raise ValueError('Group context source contamination')
    key=execution_identity('orchestration-group-observation',scope)
    target=Node(key,'scoped local-result observation','orchestration-group-observation','Explicit Group observation',scope['scope_id'],scope['framework'],[scope['period_start'],scope['reporting_period']],
        logical_id='group-observation',scope_id=scope['scope_id'],scope_type=scope['scope_type'],jurisdiction=scope['jurisdiction'],functional_currency=scope['functional_currency'],presentation_currency=scope['presentation_currency'])
    producers=contract['expected_producers']
    if not isinstance(producers,list) or not producers or len(set(producers))!=len(producers): raise ValueError('Distinct exact producers required')
    if any(id not in graph.nodes or graph.nodes[id].id!=id for id in producers): raise ValueError('Exact producer identity required')
    target.dependencies=list(producers)
    seen=set();observations=[];limits=[]
    for receipt in contract['receipts']:
        node=validate_scoped_receipt(receipt,graph,inputs,target,context)
        if node.id in seen: raise ValueError('Duplicate scoped receipt')
        seen.add(node.id)
        boundary=[]
        if node.framework!=scope['framework']: boundary.append('framework conversion unresolved')
        if receipt['currency']!=scope['currency']: boundary.append('currency translation unresolved')
        amount=str(number(node.result['calculations']['period_revenue']))
        observations.append(dict(scope_id=node.scope_id,producing_node=node.id,owner=node.selected_skill,
            amount=amount,framework=node.framework,currency=receipt['currency'],conversion_boundary=boundary,
            exact_case_fingerprint=node.result['case_fingerprint'],result_fingerprint=digest(node.result)))
        if boundary: limits.append(node.scope_id+': '+', '.join(boundary)+'.')
        case.handoff_ledger.append(copy.deepcopy({k:v for k,v in receipt.items() if k!='result'}))
    if seen!=set(producers): raise ValueError('Scoped result observation population omitted or added')
    observations.sort(key=lambda r:r['scope_id'])
    summary='Revenue reviewed separately: '+'; '.join(r['scope_id']+' '+r['amount']+' '+r['currency']+' ('+r['framework']+')' for r in observations)+'. No consolidated '+scope['framework']+'/'+scope['currency']+' total is established; local results retain their original accounting basis.'
    target.status='complete';target.result=dict(observations=observations,accounting_authority=False,currentness='CURRENT')
    graph.add(target);graph.validate()
    return dict(scope_id=scope['scope_id'],node=key,observations=observations,summary=summary,limitations=limits,
        consolidated_total=None,accounting_authority=False,context_lineage=dict(copy.deepcopy(source),qualified_context_fingerprint=contract.get('qualified_context_fingerprint')))
