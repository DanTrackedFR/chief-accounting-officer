"""Exact temporal qualification for inert facts and separately reviewed inputs.

Legacy bounded requests retain their date contracts. Explicit Period registries
require stable calendar-qualified identity; evidence never chooses a calendar.
"""
from .periods import PeriodRegistry
from .scopes import scope_registry


def registry(context):
    row=context.get('period_registry')
    if not row:return None
    return PeriodRegistry.from_record(row) if 'history' in row else PeriodRegistry(row['calendars'],row['periods'],row.get('relationships',[]))


def qualify(context,dimensions):
    periods=registry(context)
    if periods is None:return None
    p=periods.get(dimensions.get('period_id'))
    s=scope_registry(context).get(dimensions.get('scope_id',dimensions.get('entity')))
    if dimensions.get('calendar_id')!=p.calendar_id or (s.reporting_calendar and s.reporting_calendar!=p.calendar_id):raise ValueError('Exact Period/calendar identity required')
    if dimensions.get('period')!=[p.start,p.end]:raise ValueError('Exact Period evidence dates differ')
    role=dimensions.get('period_role')
    if role not in ('CURRENT','PRIOR','OPENING','COMPARATIVE','PARTIAL_INCLUDED_PERIOD'):raise ValueError('Explicit Period relationship role required')
    relationship=dimensions.get('relationship_id')
    if role=='CURRENT':
        if relationship is not None:raise ValueError('Current Period cannot substitute relationship evidence')
    elif relationship not in periods.relationships or periods.relationships[relationship].source_period!=p.period_id or periods.relationships[relationship].relationship!=role:raise ValueError('Exact Period relationship identity required')
    return p


def validate_fact(context,dimensions,metadata):
    p=qualify(context,dimensions)
    if p is None:return
    for source in metadata:
        for key in ('period_id','calendar_id','period_role','relationship_id','period'):
            if source.get(key)!=dimensions.get(key):raise ValueError('Fact source Period/calendar/relationship differs')


def validate_pack(context,pack,natives):
    periods=registry(context)
    if periods is None:return
    for native in natives:
        p=periods.get(native.get('period_id'))
        if pack.scoped_packs:continue  # exact qualification belongs to each child
        if (pack.scope_id,pack.period_id,pack.calendar_id)!=(native.get('scope_id',native.get('entity')),p.period_id,p.calendar_id) or pack.relationship_id is not None:raise ValueError('ReviewedInputPack exact Scope/Period/calendar required')


def validate_binding(context,native,binding,dimensions):
    p=qualify(context,dimensions)
    if p is None:return
    periods=registry(context);target=periods.get(native.get('period_id'))
    if (binding.period_id,binding.calendar_id)!=(target.period_id,target.calendar_id):raise ValueError('Binding target Period/calendar differs')
    if binding.kind in ('current','owner_result'):
        if p.period_id!=target.period_id or dimensions['period_role']!='CURRENT' or binding.relationship_id is not None:raise ValueError('Opening/comparative evidence cannot certify current execution')
    else:
        key=binding.relationship_id
        edge=periods.relationships.get(key)
        if edge is None or key!=dimensions.get('relationship_id') or (edge.source_period,edge.target_period)!=(p.period_id,target.period_id):raise ValueError('Binding Period relationship differs')


def validate_source(context,native,metadata,binding):
    periods=registry(context)
    if periods is None:return
    qualify(context,metadata)
    p=periods.get(native.get('period_id'))
    if (binding.period_id,binding.calendar_id)!=(p.period_id,p.calendar_id) or binding.relationship_id is not None:raise ValueError('Auxiliary binding exact target Period/calendar required')
    if metadata.get('period_id')!=p.period_id or metadata.get('period_role')!='CURRENT' or metadata.get('relationship_id') is not None:raise ValueError('Reviewed source cannot certify another Period or relationship')


def validate_native_sources(context,node,source):
    """Apply the same qualification at ordinary/correction production entry."""
    periods=registry(context)
    if periods is None:return
    target=periods.get(node.period_id)
    for row in source.get('qualified_scope_sources',[]):
        meta=row.get('metadata',{})
        qualify(context,meta)
        if meta.get('scope_id',meta.get('entity'))!=node.scope_id or meta.get('period_id')!=target.period_id or meta.get('period_role')!='CURRENT' or meta.get('relationship_id') is not None:raise ValueError('Native source manifest cannot certify another Scope/Period/relationship')
