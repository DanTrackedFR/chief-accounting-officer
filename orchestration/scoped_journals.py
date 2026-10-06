"""Accounting-layer qualification around the inherited gross-line allocator."""
from .scopes import scope_registry,execution_scopes,execution_identity,scoped_context


def qualify_journal(context,source_scope,posting_scope,layer):
    registry=scope_registry(context);source=registry.get(source_scope);target=registry.get(posting_scope)
    scoped_context(context,{'entity':source_scope});scoped_context(context,{'entity':posting_scope})
    if layer not in ('LEGAL_ENTITY','SUBGROUP','GROUP') or target.scope_type!=layer: raise ValueError('Journal posting layer differs from Scope')
    if source.scope_type!=layer or source_scope!=posting_scope: raise ValueError('Journal source/posting Scope contamination; explicit accounting conversion owner required')
    return dict(source_scope=source_scope,posting_scope=posting_scope,accounting_layer=layer)


def allocate_scoped(native,context,ownership):
    """Same allocator, scoped node keys and event keys; no separate dedup engine."""
    from .runtime import CAO,digest
    rows=[]
    for row in native:
        if not row.get('node') or not row.get('owner') or not row.get('currency') or len(row.get('period',[]))!=2: raise ValueError('Scoped native journal dimensions required')
        scope=scoped_context(context,dict(entity=row['posting_scope'],period_start=row['period'][0],reporting_period=row['period'][1],**({'period_id':row['period_id']} if 'period_id' in row else {})))
        qualification=qualify_journal(scope,row['source_scope'],row['posting_scope'],row['accounting_layer'])
        if row['node']!=execution_identity(row['owner'],scope):raise ValueError('Journal node owner/Scope identity differs')
        if row['currency']!=scope['currency'] or row['period']!=[scope['period_start'],scope['reporting_period']]:raise ValueError('Native journal differs from governed Scope currency/period')
        rows.append(dict(owner=row['node'],journals=row['journals']))
    events=[]
    for event in ownership:
        if set(event)-{'period_id','result_version'}!={'economic_id','posting_scope','period','currency','primary','witnesses','evidence'}: raise ValueError('Scoped economic event required')
        target=scope_registry(context).get(event['posting_scope'])
        refs=event['primary']+[r for witness in event['witnesses'] for r in witness]
        matches=[]
        for ref in refs:
            match=[r for r in native if r['node']==ref['owner']]
            if len(match)!=1: raise ValueError('Exact journal producing node required')
            row=match[0]
            if row.get('period_id')!=event.get('period_id') or row.get('result_version')!=event.get('result_version'):raise ValueError('Journal event Period/version differs')
            if (row['posting_scope'],row['period'],row['currency'])!=(event['posting_scope'],event['period'],event['currency']): raise ValueError('Event scope/currency/period contamination')
            matches.append(row)
        events.append(dict(economic_id=digest([event['posting_scope'],event.get('period_id',event['period']),event['economic_id']]),primary=event['primary'],witnesses=event['witnesses'],evidence=event['evidence']))
    selected,ledger=CAO._qualified_journals(rows,{},events)
    return selected,[dict(event,allocated_identity=actual['economic_id']) for event,actual in zip(ownership,ledger)]
