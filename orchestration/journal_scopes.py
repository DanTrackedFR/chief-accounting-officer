"""Scoped source-assembly journal bridge using the existing event allocator.

Legal-entity source snapshots and consolidation-only journals are separate.
Specialist implications embedded in qualified source populations are retained as
evidence, never reposted. This is not a legal-entity posting engine.
"""
from decimal import Decimal
from .runtime import at, digest, number, dimensions


def validate_assembly(c,graph,inputs,request,native):
    contract=request.get('source_assembly_journals')
    if not isinstance(contract,dict) or set(contract)!={'assembly_owner','target_entity','posting_owner','evidence_journals','ownership','review'}:
        raise ValueError('Explicit scoped source-assembly journal contract required')
    owner=contract['assembly_owner'];target=contract['target_entity']
    from .scopes import execution_scopes
    if execution_scopes(request['scope'])[target]['level']!='group':raise ValueError('Consolidation posting target must be a governed group scope')
    # This adapter validates the existing governed full-consolidation result.
    # General assembly-owner contracts belong in the next workstream.
    if owner!='consolidation' or contract['posting_owner']!=owner or owner not in inputs:
        raise ValueError('Unsupported scoped assembly contract')
    node=next(n for n in graph.nodes.values() if n.selected_skill==owner)
    source=inputs[owner]
    if source['entity']!=target or target!=c.entities[0] or node.status!='complete':raise ValueError('Group journal target differs from qualified assembly')
    if not source.get('qualified_owner_results'):raise ValueError('Scoped assembly requires governed specialist receipts')
    payload=dict(native=native,assembly_case_fingerprint=node.result['case_fingerprint'],target_entity=target,
        posting_owner=owner,evidence_journals=contract['evidence_journals'],ownership=contract['ownership'])
    review=contract['review']
    if review.get('payload_fingerprint')!=digest(payload) or review.get('approved') is not True or not review.get('reviewer') or review.get('reviewer')==review.get('preparer'):
        raise ValueError('Scoped journal bridge needs independent exact-payload review')
    journals={(r['owner'],i):j for r in native for i,j in enumerate(r['journals'])}
    seen=set();evidence=[]
    for witness in contract['evidence_journals']:
        if set(witness)!={'owner','index','source_entity','source_currency','target_entity','level','mode','receipt_consumer','semantic'}:
            raise ValueError('Scoped journal evidence dimensions required')
        key=(witness['owner'],witness['index']);producer=inputs.get(witness['owner'])
        if key not in journals or key in seen or witness['owner']==owner:raise ValueError('Journal implication omitted, duplicated or reposted')
        if witness['source_entity']!=producer['entity'] or witness['source_currency']!=dimensions(producer)[-1] or witness['target_entity']!=target or witness['level']!='group' or witness['mode']!='included_in_qualified_source':
            raise ValueError('Legal-entity/group journal scope contamination')
        consumers=[n for n in graph.nodes.values() if n.selected_skill==witness['receipt_consumer'] and n.status=='complete']
        if len(consumers)!=1 or not any(r.get('producer')==witness['owner'] and r.get('semantic')==witness['semantic'] for r in inputs[witness['receipt_consumer']].get('qualified_owner_results',[])):
            raise ValueError('Evidence-only implication lacks current actual specialist receipt')
        seen.add(key);evidence.append(dict(witness,posting=False,native_journal_fingerprint=digest(journals[key])))
    if seen!={key for key in journals if key[0]!=owner}:raise ValueError('Native specialist journal population not accounted for')
    # Keep the inherited gross line-grain event allocator: it detects omitted,
    # duplicated and relabelled allocations independently of account totals.
    from .runtime import CAO
    selected,ledger=CAO._qualified_journals([r for r in native if r['owner']==owner],{},contract['ownership'])
    assembled={}
    for entity in source['entities']:
        if entity['id'] not in node.result['calculations']['perimeter']:continue
        if entity['translation'] is not None:raise ValueError('Scoped source bridge requires owner-qualified presentation balances')
        for account,value in entity['balances'].items():assembled[account]=assembled.get(account,Decimal(0))+number(value)
    for journal in selected:
        for line in journal['lines']:
            assembled[line['account']]=assembled.get(line['account'],Decimal(0))+number(line['amount'])*(1 if line['side']=='Dr' else -1)
    final=node.result['calculations']['consolidated_balances']
    if any(assembled.get(k,Decimal(0))!=number(final.get(k,0)) for k in set(assembled)|set(final)):
        raise ValueError('Scoped source plus exactly-once journals differs from governed assembly')
    c.journal_ownership_ledger=[dict(r,source_entity=target,target_entity=target,level='group',posting=True,source_scope=target,posting_scope=target,accounting_layer='GROUP',node=node.id,owner=owner,currency=dimensions(source)[-1],period=node.period) for r in ledger]+[dict(r,source_scope=r['source_entity'],posting_scope=target,accounting_layer='GROUP') for r in evidence]
    c._scoped_postings=selected;c._journal_mapping={}
    c.execution_ledger.append(dict(node=node.id,status='qualified_source_assembly',target_entity=target,level='group',residual='0'))
