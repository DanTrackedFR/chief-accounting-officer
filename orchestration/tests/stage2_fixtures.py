"""Bounded dependency proof, never consolidated accounting authority."""
import copy
from dataclasses import replace
from orchestration.periods import FiscalCalendar,Period,PeriodRegistry,PeriodRelationship,EffectiveInterval
from orchestration.scopes import ScopeRegistry,execution_identity
from orchestration.runtime import Case,CAO,digest
from orchestration.cases import CaseRegistry,case_identity
from orchestration.planning import Graph,Node
from orchestration.versions import VersionedExecution,Dependency
from orchestration.tests.scope_fixtures import ROWS
from orchestration.tests.fixtures import revenue
from cases import finalize
from interfaces.public_output import public_record


def build():
    calendars=[FiscalCalendar('CALENDAR','Calendar year',1,1,('reviewed-calendar',)),FiscalCalendar('US-FISCAL','US July fiscal year',7,1,('reviewed-US-calendar',))]
    scopes=ScopeRegistry([replace(s,reporting_calendar='US-FISCAL' if s.scope_id=='ENTITY-US' else 'CALENDAR') for s in ROWS])
    periods={}
    for calendar in ('CALENDAR','US-FISCAL'):
        for label,start,end in [('AUG','2026-08-01','2026-08-31'),('SEP','2026-09-01','2026-09-30'),('OCT','2026-10-01','2026-10-31'),('NOV','2026-11-01','2026-11-30')]:
            fiscal={'AUG':'02','SEP':'03','OCT':'04','NOV':'05'}[label] if calendar=='US-FISCAL' else label
            periods[calendar+'-'+label]=Period.create(calendar,start,end,2027 if calendar=='US-FISCAL' else 2026,fiscal,provenance=('reviewed-periods',))
    partial=Period.create('CALENDAR','2026-10-15','2026-10-31',2026,'OCT-INCLUSION','PARTIAL_INCLUDED_PERIOD',provenance=('qualified-acquisition-date',))
    periods['PARTIAL']=partial
    registry=PeriodRegistry(calendars,periods.values())
    for calendar in ('CALENDAR','US-FISCAL'):
        registry.add_relationship(PeriodRelationship(periods[calendar+'-SEP'].period_id,periods[calendar+'-OCT'].period_id,'OPENING',('qualified-closing-opening',)))
        registry.add_relationship(PeriodRelationship(periods[calendar+'-AUG'].period_id,periods[calendar+'-OCT'].period_id,'COMPARATIVE',('qualified-comparative',)))
    registry.add_relationship(PeriodRelationship(periods['CALENDAR-OCT'].period_id,partial.period_id,'PARTIAL_INCLUDED_PERIOD',('qualified-cutoff',)))
    interval=EffectiveInterval('ENTITY-NL','business-combinations',periods['CALENDAR-OCT'].period_id,partial.period_id,'ACQUISITION','2026-10-15',('qualified-specialist-date',)).validate(registry,scopes)
    cases=CaseRegistry(scopes,registry)
    def case(scope,label,objective,parent=None):
        period=periods[('US-FISCAL' if scope=='ENTITY-US' else 'CALENDAR')+'-'+label]
        key=case_identity(scope,period.period_id,objective,'controlled-close')
        return cases.register(Case(key,objective),scope,period.period_id,'controlled-close',parent,('reviewed-objective',))
    group=case('GROUP-EUR','OCT','October local-result reporting')
    nl=case('ENTITY-NL','OCT','Netherlands October review',group.id)
    us_sep=case('ENTITY-US','SEP','US September revenue review',group.id)
    us_oct=case('ENTITY-US','OCT','US October opening lineage',group.id)
    uk=case('ENTITY-UK','SEP','UK September independent review',group.id)
    graph=Graph(); nodes={};sources={};executors={}
    def node(label,owner,c):
        s=scopes.get(c.scope_id);p=registry.get(c.period_id)
        context=dict(scope_id=s.scope_id,scope_type=s.scope_type,framework=s.framework,jurisdiction=s.jurisdiction,functional_currency=s.functional_currency,presentation_currency=s.presentation_currency,period_start=p.start,reporting_period=p.end,period_id=p.period_id)
        key=execution_identity(owner,context)
        n=Node(key,label,owner,'Controlled dependency proof',s.scope_id,s.framework,[p.start,p.end],scope_id=s.scope_id,scope_type=s.scope_type,jurisdiction=s.jurisdiction,functional_currency=s.functional_currency,presentation_currency=s.presentation_currency,period_id=p.period_id,case_id=c.id,logical_id=label)
        graph.add(n);cases.bind_node(c.id,n);nodes[label]=n
        return n
    for label,owner,c in [('US-SEP','revenue-recognition',us_sep),('US-OCT','revenue-recognition',us_oct),('US-REPORT','orchestration-entity-observation',us_sep),('US-OPEN','orchestration-opening-observation',us_oct),('GROUP','orchestration-group-observation',group),('ANALYTICS','orchestration-local-analytics',group),('UK-SEP','revenue-recognition',uk),('UK-CONTROL','orchestration-process-observation',uk),('NL-CONTROL','orchestration-process-observation',nl)]:node(label,owner,c)
    coordinator=VersionedExecution(graph,cases,registry)
    for a,b,typ in [('US-SEP','US-REPORT','CURRENT'),('US-REPORT','US-OPEN','OPENING'),('US-OPEN','GROUP','QUALIFIED_ALIGNMENT'),('GROUP','ANALYTICS','CURRENT')]:
        producer,consumer=nodes[a],nodes[b]
        coordinator.add_dependency(Dependency(producer.id,consumer.id,producer.case_id,consumer.case_id,producer.scope_id,consumer.scope_id,producer.period_id,consumer.period_id,typ,'DECLARED_CHILD' if b=='GROUP' else 'EXPLICIT_CROSS_CASE' if producer.case_id!=consumer.case_id else 'SAME_CASE',('calculations','period_revenue') if a=='US-SEP' else ('observed_amount',),('explicit-reviewed-dependency',),alignment_evidence=('Reviewed local USD observation across calendars; no EUR translation',) if typ=='QUALIFIED_ALIGNMENT' else ()))
    def observation(n,source,receipts):
        return dict(status='complete',case_fingerprint=digest([source,receipts]),observed_amount=receipts[0]['value'] if receipts else source['value'],accounting_authority=False,currency='USD' if n.scope_id=='GROUP-EUR' else n.functional_currency,limitations=['Local observation only; no framework/currency conversion or consolidated total.'])
    for label,n in nodes.items():
        if n.selected_skill=='revenue-recognition':
            s=scopes.get(n.scope_id);c=revenue(s.framework,n.period[0]);c.update(entity=s.scope_id,scope_id=s.scope_id,jurisdiction=s.jurisdiction,reporting_period=n.period[1],period_id=n.period_id,functional_currency=s.functional_currency,case_id=label)
            c['applicability_review']['effective_period']=n.period; c['balance_bridge']['opening_revenue']='0';c['source_population']=['source-'+label+'-v1'];c['evidence']=['synthetically reviewed contract source '+label]
            sources[n.id]=finalize('revenue-recognition',c);executors[n.id]=CAO().execute_versioned_owner
        else:sources[n.id]=dict(value='0',scope_id=n.scope_id,period_id=n.period_id,source_id='source-'+label);executors[n.id]=observation
    return dict(coordinator=coordinator,nodes=nodes,sources=sources,executors=executors,periods=periods,interval=interval)


def initial(f):
    e=f['coordinator']
    for key in e.topological(e.graph.nodes):e.execute(key,f['executors'][key],f['sources'][key],'Initial qualified execution')
    for c in e.cases.cases.values():
        c.challenge_results.append(dict(status='PASS',kind='qualified-controlled-observations'))
        c.observer_ran=True;c.artifacts=[dict(type='controlled-proof')]
        for status in ('SCOPED','IN_PROGRESS','CHALLENGE','CONCLUDED','DOCUMENTED','CLOSED'):c.transition(status)
    return f


def correction(f):
    e=f['coordinator'];n=f['nodes']['US-SEP'];e.periods.close(n.period_id)
    e.periods.reopen(n.period_id,'Correct reviewed US contract progress',dict(status='APPROVED',evidence=['synthetic independent reopening review'],convention='SYNTHETIC_GOVERNED'),[n.case_id],[n.id,f['nodes']['US-REPORT'].id])
    source=copy.deepcopy(f['sources'][n.id]);source['obligations'][1]['progress']='0.75';source['source_population']=['source-US-SEP-v2'];source['evidence']=['synthetically reviewed corrected contract progress']
    f['sources'][n.id]=finalize('revenue-recognition',source)
    e.execute(n.id,f['executors'][n.id],f['sources'][n.id],'Qualified source correction after governed reopening')
    return e.rework_history[-1]


def public(f):
    e=f['coordinator'];group=e.versions.current(f['nodes']['GROUP'].id).payload()
    return public_record(dict(guidance='The corrected US September result refreshed its October downstream reporting and analytics observations. UK work remains current and did not require rerun.',status='complete',calculations=[dict(label='US local revenue observation (USD)',amount=group['observed_amount'])],limitations=group['limitations']),route='answer')
