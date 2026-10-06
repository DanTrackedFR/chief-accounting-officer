"""Governed dimensional Scope registry. Hierarchy conveys no accounting authority."""
from dataclasses import dataclass, asdict
from datetime import date
import re
import json
import hashlib

TYPES = {'LEGAL_ENTITY', 'SUBGROUP', 'GROUP'}
FRAMEWORKS = {'IFRS', 'US_GAAP', 'UK_GAAP', 'AASB'}


def _text(value, name):
    if not isinstance(value, str) or not value.strip() or len(value) > 120:
        raise ValueError('Explicit '+name+' required')
    return value


@dataclass(frozen=True)
class Scope:
    scope_id: str
    scope_type: str
    display_name: str
    legal_entity_id: str | None = None
    parent_scope_id: str | None = None
    jurisdiction: str | None = None
    framework: str | None = None
    functional_currency: str | None = None
    presentation_currency: str | None = None
    reporting_calendar: str | None = None
    status: str = 'CURRENT'
    effective_from: str | None = None
    effective_to: str | None = None
    provenance: tuple = ()

    def validate(self):
        _text(self.scope_id, 'stable Scope ID'); _text(self.display_name, 'display name')
        if self.scope_type not in TYPES: raise ValueError('Invalid Scope type')
        if self.scope_type == 'LEGAL_ENTITY': _text(self.legal_entity_id, 'legal entity identifier')
        elif self.legal_entity_id is not None: raise ValueError('Group/Subgroup cannot masquerade as legal entity')
        if self.framework is not None and self.framework not in FRAMEWORKS: raise ValueError('Invalid Scope framework')
        for value in (self.functional_currency, self.presentation_currency):
            if value is not None and (not isinstance(value, str) or not re.fullmatch('[A-Z]{3}', value)): raise ValueError('Invalid Scope currency')
        for value in (self.jurisdiction, self.reporting_calendar, self.parent_scope_id):
            if value is not None: _text(value, 'Scope metadata')
        if self.status not in ('CURRENT', 'INACTIVE'): raise ValueError('Unapproved Scope status')
        for value in (self.effective_from, self.effective_to):
            if value is not None and date.fromisoformat(value).isoformat() != value: raise ValueError('Invalid Scope date')
        if self.effective_from and self.effective_to and self.effective_from > self.effective_to: raise ValueError('Invalid Scope effective interval')
        if not isinstance(self.provenance, (list, tuple)) or not self.provenance or any(not isinstance(x,str) or not x.strip() for x in self.provenance): raise ValueError('Scope provenance required')
        return self

    def record(self): return asdict(self)


class ScopeRegistry:
    def __init__(self, scopes):
        self._scopes = {}
        for scope in scopes:
            if isinstance(scope, dict): scope = Scope(**scope)
            if not isinstance(scope, Scope): raise ValueError('Governed Scope required')
            scope.validate()
            if scope.scope_id in self._scopes: raise ValueError('Duplicate Scope ID')
            self._scopes[scope.scope_id] = scope
        if not self._scopes: raise ValueError('Scope registry cannot be empty')
        for scope in self._scopes.values():
            parent = scope.parent_scope_id
            if parent is None: continue
            if parent == scope.scope_id: raise ValueError('Self-parent Scope')
            if parent not in self._scopes: raise ValueError('Missing parent Scope')
            if self._scopes[parent].scope_type == 'LEGAL_ENTITY' or scope.scope_type == 'GROUP': raise ValueError('Illegal Scope type transition')
        active=set(); done=set()
        def walk(key):
            if key in active: raise ValueError('Scope hierarchy cycle')
            if key in done: return
            active.add(key)
            if self._scopes[key].parent_scope_id: walk(self._scopes[key].parent_scope_id)
            active.remove(key); done.add(key)
        for key in self._scopes: walk(key)

    def get(self, scope_id):
        if scope_id not in self._scopes: raise ValueError('Unknown Scope; unresolved Scope Candidate required')
        return self._scopes[scope_id]

    def record(self): return [self._scopes[key].record() for key in sorted(self._scopes)]
    def hierarchy(self): return [{'scope_id':s['scope_id'], 'parent_scope_id':s['parent_scope_id']} for s in self.record()]


def scope_registry(context):
    """Normalize compatibility contexts immediately into the same generic model."""
    if 'scopes' in context:
        rows=context['scopes']
        if not isinstance(rows,list): raise ValueError('Scope registry rows required')
        return ScopeRegistry(rows)
    rows=context.get('execution_scopes')
    if rows is None: rows=[{k:context[k] for k in ('entity','framework','jurisdiction','period_start','reporting_period','currency')}]
    if not isinstance(rows,list) or not rows: raise ValueError('Explicit execution scopes required')
    scopes=[]
    for row in rows:
        required={'entity','framework','jurisdiction','period_start','reporting_period','currency'}
        if not isinstance(row,dict) or set(row)-required-{'level'} or not required <= set(row): raise ValueError('Explicit execution scope dimensions required')
        if row.get('level','entity') not in ('entity','group','subgroup'): raise ValueError('Invalid execution Scope type')
        start,end=date.fromisoformat(row['period_start']),date.fromisoformat(row['reporting_period'])
        if start>end or start<date.fromisoformat(context['period_start']) or end>date.fromisoformat(context['reporting_period']): raise ValueError('Execution period outside bounded Case')
        typ={'entity':'LEGAL_ENTITY','group':'GROUP','subgroup':'SUBGROUP'}[row.get('level','entity')]
        scopes.append(Scope(row['entity'],typ,row['entity'],row['entity'] if typ=='LEGAL_ENTITY' else None,
            jurisdiction=row['jurisdiction'],framework=row['framework'],
            functional_currency=row['currency'] if typ=='LEGAL_ENTITY' else None,
            presentation_currency=row['currency'] if typ!='LEGAL_ENTITY' else None,
            provenance=('supplied-governed-context',)))
    return ScopeRegistry(scopes)


def execution_scopes(context):
    registry=scope_registry(context)
    out={}
    periods={r['entity']:r for r in context.get('execution_scopes',[])}
    for row in registry.record():
        s=registry.get(row['scope_id']); period=periods.get(s.scope_id,context)
        execution_currency=s.functional_currency if s.scope_type=='LEGAL_ENTITY' else s.presentation_currency
        if not all((s.framework,s.jurisdiction,execution_currency)): raise ValueError('Resolve missing Scope execution metadata: '+s.scope_id)
        out[s.scope_id]=dict(entity=s.scope_id,scope_id=s.scope_id,scope_type=s.scope_type,
            level={'LEGAL_ENTITY':'entity','SUBGROUP':'subgroup','GROUP':'group'}[s.scope_type],
            framework=s.framework,jurisdiction=s.jurisdiction,currency=execution_currency,
            functional_currency=s.functional_currency,presentation_currency=s.presentation_currency,
            period_start=period['period_start'],reporting_period=period['reporting_period'],reporting_calendar=s.reporting_calendar)
    primary=out.get(context.get('entity'))
    if not primary or any(primary[k]!=context[k] for k in ('entity','framework','jurisdiction','currency','period_start','reporting_period')): raise ValueError('Case reporting Scope absent or contradictory')
    return out


def scoped_context(context, source):
    key=source.get('scope_id',source.get('entity'))
    scope=execution_scopes(context).get(key)
    if scope is None: raise ValueError('Owner outside registered Scopes')
    if source.get('entity')!=key: raise ValueError('Owner entity differs from Scope ID')
    registered=scope_registry(context).get(key)
    if registered.status!='CURRENT':raise ValueError('Inactive Scope cannot execute as current')
    if registered.effective_from and registered.effective_from>scope['period_start']:raise ValueError('Scope not effective for bounded execution')
    if registered.effective_to and registered.effective_to<scope['reporting_period']:raise ValueError('Scope expired for bounded execution')
    if source.get('period_id') is not None:
        from .periods import PeriodRegistry
        temporal=context.get('period_registry')
        if not isinstance(temporal,dict):raise ValueError('Governed Period registry required')
        periods=PeriodRegistry.from_record(temporal) if 'history' in temporal else PeriodRegistry(temporal['calendars'],temporal['periods'],temporal.get('relationships',[]))
        period=periods.get(source['period_id'])
        if registered.reporting_calendar and period.calendar_id!=registered.reporting_calendar:raise ValueError('Wrong Scope fiscal calendar')
        if (source.get('period_start'),source.get('reporting_period'))!=(period.start,period.end):raise ValueError('Owner Period dates differ')
        scope=dict(scope,period_start=period.start,reporting_period=period.end,period_id=period.period_id,reporting_calendar=period.calendar_id)
    return dict(context, **scope)


def execution_identity(owner, context):
    """JSON tuple plus SHA256; no order, display name or filename participates."""
    payload=[owner,context['scope_id'],context['scope_type'],context['framework'],context['jurisdiction'],
        context.get('functional_currency'),context.get('presentation_currency'),context['period_start'],context['reporting_period']]
    if context.get('period_id') is not None:payload.append(context['period_id'])
    key=hashlib.sha256(json.dumps(payload,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    return 'exec:'+owner+':'+context['scope_id']+':'+key
