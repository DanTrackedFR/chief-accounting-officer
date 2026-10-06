"""Governed temporal dimensions; dates establish no accounting treatment."""
from dataclasses import dataclass, asdict
from datetime import date, timedelta
import hashlib
import json


def identity(kind, value):
    return kind+':'+hashlib.sha256(json.dumps(value, sort_keys=True, default=str, separators=(',', ':')).encode()).hexdigest()


def day(value):
    if not isinstance(value, str): raise ValueError('ISO date required')
    try: parsed=date.fromisoformat(value)
    except (ValueError, TypeError): raise ValueError('ISO date required') from None
    if parsed.isoformat()!=value: raise ValueError('Canonical ISO date required')
    return parsed


@dataclass(frozen=True)
class FiscalCalendar:
    calendar_id: str
    description: str
    year_start_month: int
    year_start_day: int
    provenance: tuple

    def validate(self):
        if not self.calendar_id or not self.description or not self.provenance: raise ValueError('Governed calendar required')
        if self.year_start_month is None and self.year_start_day is None:return self
        if type(self.year_start_month)!=int or type(self.year_start_day)!=int: raise ValueError('Calendar date required')
        try: date(2001,self.year_start_month,self.year_start_day)
        except ValueError: raise ValueError('Invalid fiscal calendar') from None
        return self


@dataclass(frozen=True)
class Period:
    period_id: str
    calendar_id: str
    start: str
    end: str
    fiscal_year: int
    fiscal_period: str
    period_type: str
    as_of: str
    provenance: tuple

    @classmethod
    def create(cls,calendar_id,start,end,fiscal_year,fiscal_period,period_type='REPORTING',as_of=None,provenance=()):
        values=dict(calendar_id=calendar_id,start=start,end=end,fiscal_year=fiscal_year,fiscal_period=fiscal_period,period_type=period_type,as_of=as_of or end)
        return cls(identity('period',values),**values,provenance=tuple(provenance)).validate()

    def validate(self):
        if day(self.end)<day(self.start) or day(self.as_of)<day(self.start): raise ValueError('Invalid reporting interval')
        if type(self.fiscal_year)!=int or not self.calendar_id or not self.fiscal_period or not self.provenance: raise ValueError('Governed Period required')
        if self.period_type not in ('REPORTING','OPENING','PARTIAL_INCLUDED_PERIOD'): raise ValueError('Invalid Period type')
        values={k:v for k,v in asdict(self).items() if k not in ('period_id','provenance')}
        if self.period_id!=identity('period',values): raise ValueError('Period identity substituted')
        if self.period_type=='OPENING' and self.start!=self.end: raise ValueError('Opening must be an as-of interval')
        return self

    def record(self): return asdict(self)


@dataclass(frozen=True)
class PeriodRelationship:
    source_period: str
    target_period: str
    relationship: str
    provenance: tuple

    @property
    def id(self): return identity('period-edge',[self.source_period,self.target_period,self.relationship])


@dataclass(frozen=True)
class EffectiveInterval:
    scope_id: str
    owner: str
    source_period: str
    included_period: str
    effective_event: str
    effective_date: str
    provenance: tuple

    def validate(self,periods,scopes):
        scope=scopes.get(self.scope_id)
        source=periods.get(self.source_period); included=periods.get(self.included_period)
        if scope.reporting_calendar and scope.reporting_calendar!=source.calendar_id:raise ValueError('Effective interval Scope fiscal calendar differs')
        if not self.owner or not self.provenance or self.effective_event not in ('ACQUISITION','DISPOSAL','BOUNDED_INCLUSION'): raise ValueError('Governed effective event required')
        effective=day(self.effective_date)
        if included.period_type!='PARTIAL_INCLUDED_PERIOD' or source.calendar_id!=included.calendar_id or not day(source.start)<=day(included.start)<=day(included.end)<=day(source.end): raise ValueError('Impossible included interval')
        if self.effective_event=='ACQUISITION' and included.start!=self.effective_date: raise ValueError('Acquisition interval mismatch')
        if self.effective_event=='DISPOSAL' and included.end!=self.effective_date: raise ValueError('Disposal interval mismatch')
        if not day(source.start)<=effective<=day(source.end): raise ValueError('Effective event outside source Period')
        return self


class PeriodRegistry:
    def __init__(self,calendars,periods,relationships=()):
        self.calendars={}; self.periods={}; self.relationships={}; self.status={}; self.history=[]; self.reopenings=[]
        for calendar in calendars:
            if isinstance(calendar,dict): calendar=FiscalCalendar(**calendar)
            calendar.validate()
            if calendar.calendar_id in self.calendars: raise ValueError('Duplicate calendar')
            self.calendars[calendar.calendar_id]=calendar
        for period in periods:
            if isinstance(period,dict): period=Period(**period)
            period.validate()
            if period.calendar_id not in self.calendars or period.period_id in self.periods: raise ValueError('Unknown calendar or duplicate Period')
            # Fiscal labels or evidence as-of revisions do not create another
            # execution interval. Corrections/restatements belong to versions.
            interval=(period.calendar_id,period.start,period.end,period.period_type)
            if any((p.calendar_id,p.start,p.end,p.period_type)==interval for p in self.periods.values()):raise ValueError('Period interval alias; preserve canonical identity and create a result version')
            self.periods[period.period_id]=period; self.status[period.period_id]='OPEN'
        for relationship in relationships: self.add_relationship(relationship)

    @classmethod
    def from_record(cls,record):
        if set(record)!={'calendars','periods','relationships','history'}:raise ValueError('Canonical Period registry record required')
        periods=[{k:v for k,v in row.items() if k!='status'} for row in record['periods']]
        relationships=[]
        for row in record['relationships']:
            edge=PeriodRelationship(**{k:v for k,v in row.items() if k!='id'})
            if edge.id!=row.get('id'):raise ValueError('Period relationship identity relabelled')
            relationships.append(edge)
        registry=cls(record['calendars'],periods,relationships)
        for event in record['history']:
            if event.get('event')=='CLOSED':registry.close(event['period_id'])
            elif event.get('event')=='REOPENED':registry.reopen(event['period_id'],event['reason'],event['approval'],event['case_ids'],event['node_ids'])
            else:raise ValueError('Unknown governed Period event')
        if json.dumps(registry.record(),sort_keys=True)!=json.dumps(record,sort_keys=True):raise ValueError('Period registry lifecycle/history differs')
        return registry

    def get(self,key):
        if key not in self.periods: raise ValueError('Unknown governed Period')
        return self.periods[key]

    def add_relationship(self,edge):
        if isinstance(edge,dict): edge=PeriodRelationship(**edge)
        source,target=self.get(edge.source_period),self.get(edge.target_period)
        if source.period_id==target.period_id or not edge.provenance: raise ValueError('Self-referential/unqualified Period relationship')
        if edge.relationship not in ('CURRENT','PRIOR','COMPARATIVE','OPENING','PARTIAL_INCLUDED_PERIOD'): raise ValueError('Invalid Period relationship')
        if edge.relationship in ('PRIOR','COMPARATIVE','OPENING') and source.end>=target.start: raise ValueError('Prior/comparative/opening relationship dates differ')
        if edge.relationship=='OPENING' and (source.calendar_id!=target.calendar_id or day(source.end)+timedelta(days=1)!=day(target.start)): raise ValueError('Wrong prior closing Period')
        if edge.relationship=='PARTIAL_INCLUDED_PERIOD' and (target.period_type!='PARTIAL_INCLUDED_PERIOD' or source.calendar_id!=target.calendar_id or not source.start<=target.start<=target.end<=source.end): raise ValueError('Partial outside source Period')
        if edge.id in self.relationships: raise ValueError('Duplicate Period relationship')
        adjacency={p:[] for p in self.periods}
        for r in [*self.relationships.values(),edge]: adjacency[r.source_period].append(r.target_period)
        def walk(key,path):
            if key in path: raise ValueError('Period relationship cycle')
            for child in adjacency[key]: walk(child,path|{key})
        for key in adjacency: walk(key,set())
        self.relationships[edge.id]=edge
        return edge.id

    def require_relationship(self,source,target,kind):
        matches=[e for e in self.relationships.values() if (e.source_period,e.target_period,e.relationship)==(source,target,kind)]
        if len(matches)!=1: raise ValueError('Explicit Period relationship required')
        return matches[0]

    def close(self,key):
        self.get(key)
        if self.status[key] not in ('OPEN','REOPENED'): raise ValueError('Period cannot close')
        self.status[key]='CLOSED'; self.history.append(dict(period_id=key,event='CLOSED'))

    def reopen(self,key,reason,approval,case_ids,node_ids):
        self.get(key)
        if self.status[key]!='CLOSED' or not reason or not case_ids or not node_ids: raise ValueError('Governed closed-period reopening required')
        if not isinstance(approval,dict) or set(approval)!={'status','evidence','convention'} or approval['status']!='APPROVED' or approval['convention']!='SYNTHETIC_GOVERNED' or not approval['evidence']: raise ValueError('Synthetic governed reopening approval required')
        record=dict(period_id=key,reason=reason,approval=approval,case_ids=sorted(set(case_ids)),node_ids=sorted(set(node_ids)),event='REOPENED')
        self.reopenings.append(record); self.history.append(record); self.status[key]='REOPENED'

    def authorize_execution(self,key,case_id,node_id):
        self.get(key)
        if self.status[key]=='CLOSED': raise ValueError('Closed Period requires governed reopening')
        if self.status[key]=='REOPENED':
            record=next(r for r in reversed(self.reopenings) if r['period_id']==key)
            if case_id not in record['case_ids'] or node_id not in record['node_ids']: raise ValueError('Execution outside reopened work authorization')

    def record(self):
        return dict(calendars=[asdict(self.calendars[k]) for k in sorted(self.calendars)],periods=[dict(self.get(k).record(),status=self.status[k]) for k in sorted(self.periods)],relationships=[dict(asdict(self.relationships[k]),id=k) for k in sorted(self.relationships)],history=self.history)


def compatibility_period(context):
    """Safe single-period normalization: unknown calendar stays explicitly unspecified."""
    calendar=context.get('reporting_calendar') or 'UNSPECIFIED:'+context['scope_id']
    p=Period.create(calendar,context['period_start'],context['reporting_period'],day(context['reporting_period']).year,'BOUNDED:'+context['period_start']+':'+context['reporting_period'],provenance=('supplied-governed-context',))
    return p
