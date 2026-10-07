"""Separately reviewed boundary stocks; no intervening-year movement is inferred.

September closing / October opening retain unresolved gross loan economics.
October corrections belong solely to current accounting. The prior-year issued
comparative remains the original cash/equity489 source population.
"""
import copy
from dataclasses import asdict
from orchestration.tests import stage4_closing_population as whole, stage4_fixtures as s4, stage3_fixtures as s3
from orchestration.periods import Period, PeriodRegistry, PeriodRelationship
from orchestration.cases import case_identity
from orchestration.runtime import CAO, Case
from orchestration.versions import Dependency
from orchestration.governed_plan import observation
from additional_cases import reporting, certify

EVIDENCE = ('Separately reviewed synthetic authorized boundary TB: cash ledgers NL300/US100x0.9/UK100; opening capital487; unresolved original loans retained gross. No year-long movement assertion.',)
BOUNDARY = [('cash','490','asset',True), ('mismatch receivable','10','asset',False),
            ('mismatch payable','-11','liability',False), ('fx receivable','16','asset',False),
            ('fx payable','-18','liability',False), ('equity','-487','equity',False)]
COMPARATIVE = [('cash','489','asset',True),('equity','-489','equity',False)]


def rows(specs, version):
    return [dict(id=k,balance=v,category=cat,performance_category='operating',line=k,
                 source_version=version,classification_memo='Separately reviewed authorized stock; unresolved balances remain gross',cash_account=cash)
            for k,v,cat,cash in specs]


def build():
    f=whole.build();e=f['session'];root=f['containers']['GROUP-EUR-OCT']
    p=Period.create('CALENDAR','2025-10-01','2025-10-31',2025,'OCT',provenance=s3.EVIDENCE)
    opening=Period.create('CALENDAR','2026-10-01','2026-10-01',2026,'OCT-OPENING','OPENING',provenance=EVIDENCE)
    e.periods=PeriodRegistry(e.periods.calendars.values(),[*e.periods.periods.values(),p,opening],e.periods.relationships.values());e.cases.periods=e.periods
    f['periods']['CALENDAR-COMPARATIVE']=p
    f['periods']['CALENDAR-OPENING']=opening
    e.periods.add_relationship(PeriodRelationship(f['periods']['CALENDAR-SEP'].period_id,opening.period_id,'OPENING',EVIDENCE))
    e.periods.add_relationship(PeriodRelationship(p.period_id,root.period_id,'COMPARATIVE',s3.EVIDENCE))
    for label,period in [('adjacent-closing',f['periods']['CALENDAR-SEP']),('current-opening',opening),('prior-year-comparative',p)]:
        objective='Review supplied authorized historical Group stock '+period.end
        c=Case(case_identity(root.scope_id,period.period_id,objective,root.cycle),objective)
        e.cases.register(c,root.scope_id,period.period_id,root.cycle,None,EVIDENCE)
        f['containers'][label]=c;s3.add_node(f,label,'financial-statements',c,None)
        if label=='adjacent-closing':continue
        a=f['nodes'][label];b=f['nodes']['reporting'];kind='QUALIFIED_ALIGNMENT' if label=='current-opening' else 'COMPARATIVE'
        edge=Dependency(a.id,b.id,a.case_id,b.case_id,a.scope_id,b.scope_id,a.period_id,b.period_id,kind,'EXPLICIT_CROSS_CASE',('calculations','current'),EVIDENCE,alignment_evidence=EVIDENCE if kind=='QUALIFIED_ALIGNMENT' else ())
        f['edges'][(label,'reporting')]=e.add_dependency(edge)
    a=f['nodes']['adjacent-closing'];b=f['nodes']['current-opening']
    edge=Dependency(a.id,b.id,a.case_id,b.case_id,a.scope_id,b.scope_id,a.period_id,b.period_id,'OPENING','EXPLICIT_CROSS_CASE',('calculations','current'),EVIDENCE)
    f['edges'][('adjacent-closing','current-opening')]=e.add_dependency(edge)
    s3.add_edge(f,'analytics','group',('calculations','diagnostic','bridge'))
    return f


def stock_source(f,label):
    c=s3.native_context(f,label,reporting());n=f['nodes'][label]
    specs=BOUNDARY if label in ('adjacent-closing','current-opening') else COMPARATIVE
    equity='487' if label in ('adjacent-closing','current-opening') else '489';cash='490' if label in ('adjacent-closing','current-opening') else '489'
    c['current_tb']=rows(specs,'reviewed-boundary-2026-09-30' if label in ('adjacent-closing','current-opening') else 'reviewed-prior-v1')
    c['comparative_tb']=copy.deepcopy(c['current_tb']);c['opening_tb']=copy.deepcopy(c['current_tb'])
    from datetime import date,timedelta
    end=(date.fromisoformat(n.period[0])-timedelta(days=1)).isoformat()
    c['opening']=dict(period_end=end,review_memo='Independently supplied same-period opening stock and zero historical period activity; no intervening-year rollforward')
    c['comparative'].update(period_end=end,adjustments_memo='Reviewed bounded stock workpaper; no restatement or intervening accounting inferred')
    c['equity_bridge'][0].update(opening=equity,profit='0',oci='0',closing=equity)
    c['cash_flow'].update(start_amount='0',adjustments=[],investing='0',financing='0',fx='0',opening=cash,closing=cash,balance_sheet_bridge='0',opening_balance_sheet_bridge='0',classifications=[],zero_movement_review=dict(complete=True,movement_count=0,evidence=list(EVIDENCE)))
    c['notes'][0]['amount']=cash;c['unit_scale']='million'
    c['boundary_evidence']=dict(provenance=list(EVIDENCE),stock_date=n.period[1],source_inventory=['NL-CASH-300','US-CASH-100','UK-CASH-100','ORIGINAL-MISMATCH-10-11','ORIGINAL-FX-16-18'] if label in ('adjacent-closing','current-opening') else ['ORIGINAL-2025-10-31-CASH-EQUITY-489'],reviewed=True)
    if label=='current-opening':
        c['opening_stock_dependency']=f['edges'][('adjacent-closing','current-opening')]
        c['opening_stock_summary']=copy.deepcopy(f['session'].versions.current(f['nodes']['adjacent-closing'].id).payload()['calculations']['current'])
        s3.bind(f,c,'adjacent-closing','current-opening',('opening_stock_summary',))
        c['versioned_dependency_receipts']=s3.receipts(f,n.id)
    return certify('financial-statements',c)


def source(f,label):
    if label in ('adjacent-closing','current-opening','prior-year-comparative'):return stock_source(f,label)
    if label=='reporting':
        c=whole.source(f,label);e=f['session'];c['temporal_reporting']={};c['temporal_summaries']={}
        for producer,kind,field in [('current-opening','OPENING','opening_tb'),('prior-year-comparative','COMPARATIVE','comparative_tb')]:
            n=f['nodes'][producer];v=e.versions.current(n.id);c[field]=copy.deepcopy(e.sources[n.id]['current_tb'])
            c['temporal_reporting'][kind]=f['edges'][(producer,'reporting')]
            c['temporal_summaries'][kind]=copy.deepcopy(v.payload()['calculations']['current'])
            s3.bind(f,c,producer,'reporting',('temporal_summaries',kind))
        c['opening']=dict(period_end='2026-09-30',review_memo='Exact adjacent reviewed closing stock; no comparative substitution')
        c['cash_flow'].update(opening_balance_sheet_bridge='0',zero_movement_review=dict(complete=True,movement_count=0,evidence=list(EVIDENCE)))
        c['versioned_dependency_receipts']=s3.receipts(f,f['nodes'][label].id)
        return certify('financial-statements',c)
    c=whole.source(f,label)
    if label=='analytics':
        from governance_cases import ready, refresh_release
        from orchestration.runtime import digest
        # Diagnose the observed prior-year stock difference only. No financing
        # event or intervening-year cash movement is established by these stocks.
        for doc in c['documents']:
            content=doc['content']
            if doc['id']=='actual-drivers':
                content['drivers']=[dict(id='observed-stock-comparison',amount='1')]
                content['driver_inventory']=['observed-stock-comparison']
            if doc['id']=='cash-drivers':
                content['records'][0]['id']='observed-stock-comparison'
                content['records'][0]['economic_components']=['qualified-comparative-and-current-stock']
                content['inventory']=['observed-stock-comparison']
            doc['content_hash']=digest(content)
        c['explanations'][0]['interpretation_memo']='Observed prior-year cash stock difference only; no intervening cash transaction or causal financing attribution is inferred'
        c['diagnostic']['groups'][0]['labels']['movement']='Observed prior-year cash stock difference; intervening movements not inferred'
        c=refresh_release(c);c['release_review']['approval_date']=f['nodes'][label].period[1];c=ready('management-accounting-analytics',c=c)
    if f['nodes'][label].selected_skill.startswith('orchestration-'):
        c['versioned_dependency_receipts']=s3.receipts(f,f['nodes'][label].id)
    return c


def initial():
    f=build();e=f['session'];plan=s4.serialize(f)
    for key in e.topological(e.graph.nodes):
        n=e.graph.nodes[key];blocked=any(e.graph.nodes[p].status!='complete' or e.versions.current(p).payload().get('unresolved_dependencies') for p in n.dependencies)
        c=dict(scope_id=n.scope_id,period_id=n.period_id,evidence=list(s3.EVIDENCE)) if blocked else source(f,n.logical_id)
        e.execute(key,observation,c,'Initial governed CAO execution')
    plan['sources']=copy.deepcopy(e.sources);case=CAO().run(dict(objective=s4.OBJECTIVE,governed_plan=plan));f['case']=case;f['session']=case.governance;f['basis'].session=case.governance
    f['nodes']={k:case.graph.nodes[v.id] for k,v in f['nodes'].items()};f['containers']={k:case.governance.cases.get(v.id) for k,v in f['containers'].items()};return f


def reviewed_rework(f,plan):
    preview=copy.deepcopy(f);out={}
    for key in plan['execution_order']:
        e=preview['session'];n=e.graph.nodes[key];c=s4.qualified_replacement(preview,key,source(preview,n.logical_id));out[key]=c
        e.execute(key,observation,c,'Dependency rework: '+plan['new_version'])
    f.setdefault('replacement_intakes',[]).extend(preview.get('replacement_intakes',[])[len(f.get('replacement_intakes',[])):]);return out


def finish(f, first_plan=None):
    from orchestration.tests import stage4_closing_fixtures as closing
    e=f['session'];before={k:e.versions.current(n.id,allow_stale=True) for k,n in f['nodes'].items()}
    p=first_plan or s4.correct(f)
    # Before reviewed FX correction, only producers supported by current evidence
    # can refresh. Original residual and blocked downstream history are retained.
    for key in p['execution_order']:
        n=e.graph.nodes[key]
        try:e.execute(key,observation,s4.qualified_replacement(f,key,source(f,n.logical_id)),'Dependency rework: '+p['new_version'])
        except ValueError as error:
            if n.logical_id!='elimination' or 'Native input differs from exact producer metric' not in str(error):raise
            break
    before_closing={key:(e.versions.current(key,allow_stale=True),e.graph.nodes[key].iterations) for key in e.graph.nodes}
    n=f['nodes']['fx-ENTITY-UK'];p2=CAO().correct(f['case'],n.id,s4.qualified_replacement(f,n.id,closing.correction(f)),'Separately reviewed October closing treasury quote and legal ledger')
    ledger=CAO().selective_reexecute(f['case'],p2,reviewed_rework(f,p2))
    return f,dict(before=before,before_closing=before_closing,payable_correction=p,closing_correction=p2,ledger=ledger)


def run():
    return finish(intake_initial())


def intake_initial():
    return s4.intake_initial(build,source)


def lineages(f,record):
    e=f['session'];out=[]
    chains=[('NL legal source to Group',['clean-ENTITY-NL','elimination','reporting']),
            ('US legal source through native translation to Group',['clean-ENTITY-US','whole-translation-ENTITY-US','elimination','reporting']),
            ('UK legal source through native translation to Group',['fx-ENTITY-UK','whole-translation-ENTITY-UK','elimination','reporting']),
            ('First reciprocal side through match to elimination',['clean-ENTITY-US','match-clean','elimination']),
            ('Second reciprocal side through match to elimination',['clean-ENTITY-NL','match-clean','elimination']),
            ('Adjacent closing through native opening to Financial Statements',['adjacent-closing','current-opening','reporting']),
            ('Prior-year comparative to current reporting',['prior-year-comparative','reporting']),
            ('Reviewed correction through rematch reporting analytics and observation',['fx-ENTITY-UK','match-fx-current','fx-reassessment','elimination','reporting','analytics','group'])]
    for title,labels in chains:
        versions=[e.versions.require_current(e.versions.current(f['nodes'][label].id).version_id) for label in labels]
        edges=[]
        for a,b in zip(versions,versions[1:]):
            exact=[key for key,edge in e.edges.items() if (edge.producer_node,edge.consumer_node)==(a.node_id,b.node_id)]
            if not exact:raise ValueError('Accepted lineage lacks explicit dependency')
            for key in exact:
                receipt=e.receipt(key);e.validate_receipt(receipt,b.node_id)
                if dict(b.dependency_bindings).get(key)!=a.version_id:raise ValueError('Accepted lineage wrong immutable version')
                edges.append(receipt)
        source=e.sources[versions[0].node_id]
        if not source.get('qualified_input_snapshot'):raise ValueError('Accepted lineage lacks independently sealed full source')
        out.append(dict(title=title,nodes=labels,result_versions=[v.version_id for v in versions],source_snapshot=source['qualified_input_snapshot'],receipts=edges,status='ACCEPTED'))
    old=record['before']['fx-ENTITY-UK'];current=versions[0]
    out[-1]['correction']=dict(original_version=old.version_id,current_version=e.versions.current(old.node_id).version_id,original_state=e.versions.state(old.version_id),reviewed_source=e.sources[old.node_id]['correction_evidence'],invalidation=record['closing_correction'],rework=record['ledger'],case_status=f['case'].status,public_answer=CAO().public(f['case']))
    if len(out)!=8 or f['case'].status!='CLOSED':raise ValueError('Eight accepted complete lineages required')
    return out
