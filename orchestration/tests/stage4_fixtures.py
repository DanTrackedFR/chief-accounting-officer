"""Controlled finance-holding Group sources; review is synthetic, never runtime authority.

The company has ordinary loans, cash and wholly owned subsidiaries. General
commercial revenue conversion is deliberately absent because no qualified owner
contract exists. The material residual is EUR1m (figures expressed in millions).
"""
import copy
from dataclasses import asdict
from decimal import Decimal
from orchestration.tests import stage3_fixtures as s3
from orchestration import stage3 as governed_stage3
from orchestration.periods import Period, PeriodRelationship, EffectiveInterval
from orchestration.runtime import CAO, Case
from orchestration.cases import case_identity
from orchestration.versions import Dependency
from orchestration.governed_plan import observation
from additional_cases import fx, reporting, certify
from cases import consolidation

OBJECTIVE='Review the Group close across our Netherlands, US and UK finance-holding businesses, investigate the material movements and intercompany differences, determine whether the Group reporting is supportable, and give me the final Group accounting/reporting conclusion.'
EVIDENCE=s3.EVIDENCE


def build():
    f=s3.build();e=f['session']
    # Replace only the fixture's initial Group objective, not runtime identity.
    old=f['containers']['GROUP-EUR-OCT'];old.objective=OBJECTIVE
    key=case_identity(old.scope_id,old.period_id,OBJECTIVE,old.cycle)
    del e.cases.cases[old.id];previous=old.id;old.id=key;e.cases.cases[key]=old
    for c in e.cases.cases.values():
        if c.parent_case_id==previous:c.parent_case_id=key
    for n in e.graph.nodes.values():
        if n.case_id==previous:n.case_id=key
    # Rebuild explicit dependency identities following the changed Case.
    rows=[asdict(edge) for edge in e.edges.values()]
    e.edges.clear();f['edges'].clear()
    for n in e.graph.nodes.values():n.dependencies=[]
    for row in rows:
        if row['producer_case']==previous:row['producer_case']=key
        if row['consumer_case']==previous:row['consumer_case']=key
        edge=Dependency(**row);edge_key=e.add_dependency(edge)
        a=e.graph.nodes[edge.producer_node].logical_id;b=e.graph.nodes[edge.consumer_node].logical_id
        f['edges'][(a,b) if (a,b) not in f['edges'] else (a,b,edge.metric_path[-1])]=edge_key
    f['basis'].contracts.clear();s3.declare_basis(f)
    # Consolidation consumes a population, rather than one transaction. Preserve
    # node identity by rebuilding just this fixture node before any publication.
    rebuild_population_node(f,'elimination')
    root=f['containers']['GROUP-EUR-OCT']
    s3.add_node(f,'uk-translation','foreign-currency',f['containers']['ENTITY-UK-OCT'],'mismatch')
    s3.add_node(f,'uk-conversion','intercompany-accounting',root,'mismatch')
    for a,b,path in [
        ('mismatch-ENTITY-UK','uk-translation',('calculations','pairs',0,'a_functional')),
        ('uk-translation','uk-conversion',('calculations','translation','translated_tb','ic loan')),
        ('mismatch-ENTITY-NL','uk-conversion',('calculations','pairs',0,'b_functional')),
        ('match-mismatch','uk-conversion',('matching','classification')),
        ('uk-conversion','elimination',('calculations','pairs',0,'a_functional')),
        ('uk-translation','elimination',('calculations','translation','translated_tb')),
        ('uk-translation','elimination',('calculations','translation','closing_cta')),
        ('uk-translation','elimination',('calculations','translation','cta_movement')),
        ('mismatch-ENTITY-NL','elimination',('calculations','pairs',0,'b_functional')),
        ('match-mismatch','elimination',('matching','classification'))]:s3.add_edge(f,a,b,path)
    p=f['periods'];e.periods.add_relationship(PeriodRelationship(p['CALENDAR-SEP'].period_id,p['CALENDAR-OCT'].period_id,'OPENING',EVIDENCE))
    e.periods.add_relationship(PeriodRelationship(p['CALENDAR-SEP'].period_id,p['CALENDAR-OCT'].period_id,'COMPARATIVE',EVIDENCE))
    partial=Period.create('CALENDAR','2026-09-20','2026-09-30',2026,'SEP-DRAWDOWN','PARTIAL_INCLUDED_PERIOD',provenance=EVIDENCE)
    # Canonical registry reconstruction includes a dated loan agreement interval.
    from orchestration.periods import PeriodRegistry
    e.periods=PeriodRegistry(e.periods.calendars.values(),[*e.periods.periods.values(),partial],e.periods.relationships.values());e.cases.periods=e.periods
    e.periods.add_relationship(PeriodRelationship(p['CALENDAR-SEP'].period_id,partial.period_id,'PARTIAL_INCLUDED_PERIOD',EVIDENCE))
    f['effective_interval']=EffectiveInterval('ENTITY-NL','intercompany-accounting',p['CALENDAR-SEP'].period_id,partial.period_id,'BOUNDED_INCLUSION','2026-09-20',EVIDENCE).validate(e.periods,e.cases.scopes)
    s3.add_node(f,'nl-opening','orchestration-opening-observation',f['containers']['ENTITY-NL-OCT'],None)
    a=f['nodes']['timing-ENTITY-NL'];b=f['nodes']['nl-opening']
    edge=Dependency(a.id,b.id,a.case_id,b.case_id,a.scope_id,b.scope_id,a.period_id,b.period_id,'OPENING','EXPLICIT_CROSS_CASE',('calculations','pairs',0,'a_functional'),EVIDENCE)
    f['edges'][('timing-ENTITY-NL','nl-opening')]=e.add_dependency(edge)
    s3.add_node(f,'analytics','management-accounting-analytics',root,None)
    s3.add_edge(f,'reporting','analytics',('calculations','current','cash'))
    s3.add_node(f,'nl-comparative','orchestration-comparative-observation',f['containers']['ENTITY-NL-OCT'],None)
    a=f['nodes']['timing-ENTITY-NL'];b=f['nodes']['nl-comparative']
    edge=Dependency(a.id,b.id,a.case_id,b.case_id,a.scope_id,b.scope_id,a.period_id,b.period_id,'COMPARATIVE','EXPLICIT_CROSS_CASE',('calculations','pairs',0,'a_functional'),EVIDENCE)
    f['edges'][('timing-ENTITY-NL','nl-comparative')]=e.add_dependency(edge)
    s3.add_edge(f,'nl-opening','group',('observed_amount',))
    s3.add_edge(f,'nl-comparative','group',('observed_amount',))
    # Prior closing is not itself an October legal balance. A separately
    # reviewed current native owner consumes the exact opening carrying value.
    s3.add_node(f,'timing-current-ENTITY-NL','intercompany-accounting',f['containers']['ENTITY-NL-OCT'],'timing')
    a=f['nodes']['timing-ENTITY-NL'];b=f['nodes']['timing-current-ENTITY-NL']
    edge=Dependency(a.id,b.id,a.case_id,b.case_id,a.scope_id,b.scope_id,a.period_id,b.period_id,'OPENING','EXPLICIT_CROSS_CASE',('calculations','pairs',0,'a_functional'),EVIDENCE)
    f['edges'][('timing-ENTITY-NL','timing-current-ENTITY-NL')]=e.add_dependency(edge)
    objective='Review the supplied loan closing balance within the governed September effective interval'
    effective_case=Case(case_identity('ENTITY-NL',partial.period_id,objective,old.cycle),objective)
    e.cases.register(effective_case,'ENTITY-NL',partial.period_id,old.cycle,root.id,EVIDENCE)
    f['containers']['ENTITY-NL-EFFECTIVE']=effective_case
    s3.add_node(f,'timing-effective-ENTITY-NL','intercompany-accounting',effective_case,'timing')
    a=f['nodes']['timing-ENTITY-NL'];b=f['nodes']['timing-effective-ENTITY-NL']
    edge=Dependency(a.id,b.id,a.case_id,b.case_id,a.scope_id,b.scope_id,a.period_id,b.period_id,'PARTIAL_INCLUDED_PERIOD','EXPLICIT_CROSS_CASE',('calculations','pairs',0,'a_functional'),EVIDENCE)
    f['edges'][('timing-ENTITY-NL','timing-effective-ENTITY-NL')]=e.add_dependency(edge)
    s3.add_edge(f,'timing-effective-ENTITY-NL','group',('calculations','pairs',0,'a_functional'))
    # A fresh October relationship consumes the actual October legal owners.
    # The September/October timing observation remains a separate immutable
    # execution; equal principal amounts alone never select either side.
    s3.add_node(f,'match-timing-current','orchestration-current-match',root,'timing')
    s3.add_edge(f,'timing-current-ENTITY-NL','match-timing-current',('calculations','pairs',0,'a_functional'))
    s3.add_edge(f,'timing-ENTITY-UK','match-timing-current',('calculations','pairs',0,'b_functional'))
    return f


def rebuild_population_node(f,label):
    from orchestration.scopes import execution_identity
    e=f['session'];n=f['nodes'][label];old=n.id
    n.economic_id=None
    scope=e.cases.scopes.get(n.scope_id);p=e.periods.get(n.period_id)
    n.id=execution_identity(n.selected_skill,dict(scope_id=scope.scope_id,scope_type=scope.scope_type,framework=scope.framework,jurisdiction=scope.jurisdiction,functional_currency=scope.functional_currency,presentation_currency=scope.presentation_currency,period_start=p.start,reporting_period=p.end,period_id=p.period_id))
    del e.graph.nodes[old];e.graph.nodes[n.id]=n
    case=e.cases.get(n.case_id);case.node_refs=[n.id if key==old else key for key in case.node_refs]
    rows=[asdict(edge) for edge in e.edges.values()];e.edges.clear();f['edges'].clear()
    for node in e.graph.nodes.values():node.dependencies=[]
    for row in rows:
        for key in ('producer_node','consumer_node'):
            if row[key]==old:row[key]=n.id
        edge=Dependency(**row);key=e.add_dependency(edge)
        a=e.graph.nodes[edge.producer_node].logical_id;b=e.graph.nodes[edge.consumer_node].logical_id
        f['edges'][(a,b) if (a,b) not in f['edges'] else (a,b,edge.metric_path[-1])]=key
    # Cross-layer declarations are recreated against actual new dependency IDs.
    f['basis'].contracts.clear()
    # The source transaction contract stays exact; the population target does
    # not falsely adopt one of its contributing transactions' identities.
    s3.declare_basis(f)


def legal_source(f,relationship,scope,corrected=False):
    c=s3.legal_source(f,relationship,scope)
    if relationship=='mismatch' and scope=='ENTITY-NL' and corrected:
        p=c['pairs'][0]
        p.update(opening_a='10',opening_b='10',confirmed_a='10',confirmed_b='10',
            opening_book_a='10',opening_book_b='11',book_a='10',book_b='11',gl_a='10',gl_b='10',
            version='v2',approved_version='v2')
        c['controls']['population_amount']='10';row=c['intercompany_transactions'][0]
        row.update(source_id='source-mismatch-ENTITY-NL-v2',transaction_amount='10',functional_amount='10.00')
        c['correction_evidence']=dict(original='Original export duplicated EUR1m payable; retained',replacement='Reviewed loan confirmation EUR10m and corrected legal-book closing payable EUR10m',reviewed=True,version='v2')
        c=certify('intercompany-accounting',c)
    c['unit_scale']='million'
    return certify('intercompany-accounting',c)


def matching_source(f,relationship):
    source=s3.match_source(f,relationship)
    if relationship=='mismatch':
        amounts={side['transaction_amount'] for side in source['sides']}
        source['decision']['classification']='MATCHED' if len(amounts)==1 else 'UNRESOLVED_MISMATCH'
    return source


def current_timing_match(f):
    from orchestration.intercompany_network import TransactionSide, MatchingDecision
    from orchestration.versions import fingerprint
    e=f['session'];node=f['nodes']['match-timing-current'];sides=[]
    labels=('timing-current-ENTITY-NL','timing-ENTITY-UK')
    for index,label in enumerate(labels):
        n=f['nodes'][label];other=f['nodes'][labels[1-index]]
        version=e.versions.current(n.id);row=e.sources[n.id]['intercompany_transactions'][0]
        sides.append(TransactionSide(**row,case_id=n.case_id,owner_node=n.id,
            result_version=version.version_id,metric_path=('calculations','pairs',0,'a_functional' if index==0 else 'b_functional'),
            source_path=('intercompany_transactions',0),source_fingerprint=fingerprint(row),evidence=EVIDENCE,
            counterparty_case=other.case_id,counterparty_period=other.period_id))
    decision=MatchingDecision(sides[0].relationship_id,tuple(s.side_id for s in sides),'MATCHED',
        EVIDENCE,tuple(s.result_version for s in sides),'synthetic independent October timing reviewer',
        'Separately reviewed October confirmations under agreement-timing: exact current NL receivable and UK payable, GBP30 principal; September timing difference is retained history')
    return dict(scope_id=node.scope_id,period_id=node.period_id,method='STAGE3_MATCH',network_id='STAGE3-NETWORK',
        sides=[asdict(s) for s in sides],decision=asdict(decision),evidence=list(EVIDENCE),
        versioned_dependency_receipts=s3.receipts(f,node.id))


def uk_translation(f):
    n=f['nodes']['uk-translation'];c=s3.native_context(f,'uk-translation',fx('UK_GAAP'));c['items']=[]
    c['currency'].update(functional='GBP',ledger='GBP',presentation='EUR')
    # Independently supplied parity rate, not an orchestration FX calculation.
    t=c['translation'];t.update(operation_id='mismatch',valuation_date=n.period[1],functional_currency='GBP',presentation_currency='EUR',
        tb=[dict(id='uk cash',balance='100',category='asset',rate='1',memo='Supplied reviewed closing rate'),dict(id='ic loan',balance='10.00',category='asset',rate='1',memo='Exact UK native legal loan'),dict(id='uk equity',balance='-110',category='equity',rate='1',memo='Supplied historical rate')],
        opening_net_assets='110',opening_rate='1',closing_rate='1',profit='0',profit_rate='1',other_oci='0',other_oci_rate='1',reported_closing_net_assets='110',ownership='1')
    s3.bind(f,c,'mismatch-ENTITY-UK','uk-translation',('translation','tb',1,'balance'))
    c['versioned_dependency_receipts']=s3.receipts(f,n.id)
    return certify('foreign-currency',c)


def uk_conversion(f):
    from operational_cases import operational
    n=f['nodes']['uk-conversion'];c=s3.native_context(f,'uk-conversion',operational('intercompany-accounting','IFRS'))
    p=c['pairs'][0];p.update(id='mismatch',transaction_id='mismatch',entity_a='ENTITY-UK',entity_b='ENTITY-NL',currency='EUR',
        opening_a='10',opening_b='10',opening_book_a='10',opening_book_b='10',book_a='10',book_b='10',gl_a='10',gl_b='10',confirmed_a='10',confirmed_b='10',rate_a='1',rate_b='1',initial_rate_a='1',initial_rate_b='1',date=n.period[1],approval_date=n.period[1])
    c['controls'].update(population_count=1,population_amount='10');c['conversion_economic_id']='mismatch';c['stage3_contract']='ORDINARY_IC_REASSESSMENT'
    s3.bind(f,c,'uk-translation','uk-conversion',('pairs',0,'gl_a'));s3.bind(f,c,'mismatch-ENTITY-NL','uk-conversion',('pairs',0,'gl_b'))
    c['versioned_dependency_receipts']=s3.receipts(f,n.id)
    return certify('intercompany-accounting',c)


def group_source(f):
    e=f['session'];n=f['nodes']['elimination'];c=s3.native_context(f,'elimination',consolidation('IFRS'))
    control=copy.deepcopy(c['entities'][0]['control'])
    nl={'cash':'300','investment':'290','ic payable':'-90','uk payable':'-10','equity':'-489','correction income':'-1'}
    us=e.versions.current(f['nodes']['translation'].id).payload()['calculations']['translation']['translated_tb']
    uk=e.versions.current(f['nodes']['uk-translation'].id).payload()['calculations']['translation']['translated_tb']
    c['entities']=[dict(id='ENTITY-NL',parent=True,balances=nl,control=control,translation=None,policy_alignment=True,date_alignment=True),
        dict(id='ENTITY-US',parent=False,balances=dict(us,CTA='0'),control=copy.deepcopy(control),translation=None,policy_alignment=True,date_alignment=True),
        dict(id='ENTITY-UK',parent=False,balances=dict(uk,CTA='0'),control=copy.deepcopy(control),translation=None,policy_alignment=True,date_alignment=True)]
    template=copy.deepcopy(c['investments'][0]);nt=copy.deepcopy(c['nci'][0])
    c['investments']=[];c['nci']=[];c['intercompany']=[]
    for entity,relationship,amount,equity,investment,payable in [('ENTITY-US','clean','90','sub equity','180','ic payable'),('ENTITY-UK','mismatch','10','uk equity','110','uk payable')]:
        inv=copy.deepcopy(template);inv.update(subsidiary=entity,parent_entity='ENTITY-NL',investment=investment,acquisition_equity={equity:investment},nci_at_acquisition='0');c['investments'].append(inv)
        nc=copy.deepcopy(nt);nc.update(subsidiary=entity,ownership='1',opening='0',adjusted_profit='0',adjusted_oci='0');c['nci'].append(nc)
        c['intercompany'].append(dict(id=relationship,transaction_id=relationship,family='receivable_payable',source_id='reviewed-'+relationship,seller='ENTITY-NL',buyer=entity,amount=amount,debit_account=payable,credit_account='ic loan',matched=True,source_memo='Qualified exact match/translation/ordinary-loan framework reassessment'))
    c['statement_mapping']={k:'assets' if k in ('cash','uk cash','investment','ic loan','goodwill') else 'liabilities' if k in ('ic payable','uk payable') else 'income' if k in ('FX income','correction income') else 'equity' for k in set(nl)|set(us)|set(uk)|{'CTA','noncontrolling interest','goodwill'}}
    c['cash_flow_bridge'].update(opening_cash='489',closing_cash='490',operating='0',investing='0',financing='1',fx='0',cash_accounts=['cash','uk cash'])
    c['equity_bridge'].update(opening='489',profit='1',oci='0',closing='490');c['cta_bridge'].update(translation='0',closing='0',cta_accounts=['CTA'])
    for producer,target in [('clean-ENTITY-NL',('entities',0,'balances','ic payable')),('mismatch-ENTITY-NL',('entities',0,'balances','uk payable'))]:s3.bind(f,c,producer,'elimination',target,-1)
    for index,producer in [(0,'conversion'),(1,'uk-conversion')]:s3.bind(f,c,producer,'elimination',('intercompany',index,'amount'))
    # Each actual entity reserve is independently bound; shared bridges are
    # validated against the complete qualified owner population by the runtime.
    for index,label in [(1,'translation'),(2,'uk-translation')]:
        c.setdefault('stage3_input_bindings',[]).append(dict(dependency_id=f['edges'][(label,'elimination','closing_cta')],target_path=['entities',index,'balances','CTA'],sign=-1,evidence=list(EVIDENCE)))
    c['versioned_dependency_receipts']=s3.receipts(f,n.id)
    c['group_population_coverage']=dict(mode='ALL_CURRENT_LOAN_SIDES',required_legal_result_versions=governed_stage3.current_legal_loan_versions(e,n,{entity['id'] for entity in c['entities']}))
    return certify('consolidation',c)


def reporting_source(f):
    e=f['session'];n=f['nodes']['reporting'];c=s3.native_context(f,'reporting',reporting())
    balances=e.versions.current(f['nodes']['elimination'].id).payload()['calculations']['consolidated_balances'];mapping=e.sources[f['nodes']['elimination'].id]['statement_mapping']
    categories={'assets':'asset','liabilities':'liability','equity':'equity','income':'revenue','expenses':'expense'}
    c['current_tb']=[dict(id=k,balance=v,category='oci' if k=='CTA' else categories[mapping[k]],performance_category='operating',line=k,source_version=e.versions.current(f['nodes']['elimination'].id).version_id,classification_memo='Exact qualified Consolidation account',cash_account=k in ('cash','uk cash')) for k,v in sorted(balances.items())]
    c['comparative_tb']=[dict(id='cash',balance='489',category='asset',performance_category='operating',line='cash',source_version='reviewed-prior-v1',classification_memo='Reviewed prior issued books',cash_account=True),dict(id='equity',balance='-489',category='equity',performance_category='operating',line='equity',source_version='reviewed-prior-v1',classification_memo='Reviewed prior issued equity',cash_account=False)]
    c['equity_bridge'][0].update(opening='489',profit='1',oci='0',closing='490')
    c['cash_flow'].update(start_amount='1',adjustments=[dict(id='noncash',amount='-1',source='Qualified noncash payable correction',noncash_acquisition_fx_excluded=True,memo='Exclude noncash correction from operating cash')],investing='0',financing='1',fx='0',opening='489',closing='490',classifications=[dict(id='fin',date=n.period[1],kind='capital_receipt',**{'class':'financing'},amount='1',memo='Reviewed financing cash movement')])
    c['unit_scale']='million'
    c['comparative']['period_end']='2025-10-31'
    c['notes'][0]['amount']='490';c['stage3_balances']=copy.deepcopy(balances)
    s3.bind(f,c,'elimination','reporting',('stage3_balances',));c['versioned_dependency_receipts']=s3.receipts(f,n.id)
    return certify('financial-statements',c)


def source(f,label):
    n=f['nodes'][label]
    if label in ('timing-current-ENTITY-NL','timing-effective-ENTITY-NL'):
        c=s3.native_context(f,label,s3.legal_source(f,'timing','ENTITY-NL'))
        pair=c['pairs'][0];pair.update(date=n.period[1],approval_date=n.period[1])
        row=c['intercompany_transactions'][0]
        row.update(source_id='source-'+label,book_entry_id='book-'+label,period_id=n.period_id)
        c['opening_lineage_evidence']='Separately reviewed October loan rollforward; exact September legal closing carrying value EUR30m supplies October opening book, independently confirmed GBP30m principal and unchanged reviewed rate remain separate source facts'
        s3.bind(f,c,'timing-ENTITY-NL',label,('pairs',0,'opening_book_a'))
        if label=='timing-effective-ENTITY-NL':
            c['governed_effective_interval']=asdict(f['effective_interval'])
            c['opening_lineage_evidence']='Supplied loan book EUR30m and independently confirmed GBP30m closing principal within the reviewed included interval; no drawdown, recognition or allocation treatment inferred from dates'
        c['versioned_dependency_receipts']=s3.receipts(f,n.id);c['unit_scale']='million'
        return certify('intercompany-accounting',c)
    if label=='match-timing-current':return current_timing_match(f)
    if label.startswith('match-'):return matching_source(f,label[6:])
    if label=='uk-translation':return uk_translation(f)
    if label=='uk-conversion':return uk_conversion(f)
    if label=='elimination':return group_source(f)
    if label=='reporting':return reporting_source(f)
    if label=='analytics':return analytics_source(f)
    if label in ('nl-opening','nl-comparative'):return dict(scope_id=n.scope_id,period_id=n.period_id,method='QUALIFIED_LOCAL_OBSERVATION',evidence=list(EVIDENCE),observation_currency='EUR')
    if label in ('translation','conversion','group'):return s3.downstream_source(f,label)
    return legal_source(f,n.economic_id,n.scope_id)


def initial():
    f=build();e=f['session'];plan=serialize(f)
    # Prepare reviewed initial packs in an isolated source qualification session.
    # Materially blocked consumers retain only source identity, not fabricated
    # prospective accounting or certified inputs.
    for key in e.topological(e.graph.nodes):
        label=e.graph.nodes[key].logical_id
        blockers=[e.graph.nodes[p] for p in e.graph.nodes[key].dependencies if e.graph.nodes[p].status!='complete' or e.versions.current(p).payload().get('unresolved_dependencies')]
        c=dict(scope_id=e.graph.nodes[key].scope_id,period_id=e.graph.nodes[key].period_id,source_id='pending-'+label,evidence=list(EVIDENCE)) if blockers else source(f,label)
        e.execute(key,observation,c,'Initial governed CAO execution')
    plan['sources']=copy.deepcopy(e.sources)
    case=CAO().run(dict(objective=OBJECTIVE,governed_plan=plan));f['case']=case;f['session']=case.governance;f['basis'].session=case.governance
    f['nodes']={label:case.graph.nodes[n.id] for label,n in f['nodes'].items()}
    f['containers']={label:case.governance.cases.get(c.id) for label,c in f['containers'].items()}
    return f


def serialize(f):
    e=f['session'];root=f['containers']['GROUP-EUR-OCT']
    return dict(scopes=e.cases.scopes.record(),periods=e.periods.record(),cases=[dict(case_id=c.id,objective=c.objective,scope_id=c.scope_id,period_id=c.period_id,cycle=c.cycle,parent_id=c.parent_case_id,provenance=c.provenance) for c in e.cases.cases.values()],root_case=root.id,nodes=e.graph.record(),dependencies=[asdict(edge) for edge in e.edges.values()],sources={})


def correct(f):
    n=f['nodes']['mismatch-ENTITY-NL']
    c=qualified_replacement(f,n.id,legal_source(f,'mismatch','ENTITY-NL',True))
    return CAO().correct(f['case'],n.id,c,'Qualified reciprocal confirmation and legal source correction')


def reviewed_rework(f,plan):
    preview=copy.deepcopy(f);e=preview['session'];out={}
    try:
        for key in plan['execution_order']:
            label=e.graph.nodes[key].logical_id;c=qualified_replacement(preview,key,source(preview,label))
            e.execute(key,observation,c,'Dependency rework: '+plan['new_version']);out[key]=c
    finally:
        # Source qualification is review evidence, not successful accounting
        # publication. Retain it even when the actual native guard refuses.
        f.setdefault('replacement_intakes',[]).extend(preview.get('replacement_intakes',[])[len(f.get('replacement_intakes',[])):])
    return out


def rework(f,plan):return CAO().selective_reexecute(f['case'],plan,reviewed_rework(f,plan))


def analytics_source(f):
    from governance_cases import case as governance_case, ready, refresh_release, row
    from orchestration.runtime import digest
    e=f['session'];n=f['nodes']['analytics'];c=governance_case('management-accounting-analytics')
    def adapt(v):
        if isinstance(v,dict):return {k:adapt(x) for k,x in v.items()}
        if isinstance(v,list):
            if v==['2026-01-01','2026-12-31']:return n.period
            if v==['2025-01-01','2025-12-31']:return ['2025-10-01','2025-10-31']
            return [adapt(x) for x in v]
        if v in ('2026-12-31','2027-03-31'):return n.period[1]
        if v=='2027-01-05':return '2026-10-31'
        if v=='2027-01-04':return '2026-10-30'
        if v=='Synthetic Group':return n.scope_id
        if v=='USD':return 'EUR'
        return v
    c=adapt(c);c=s3.native_context(f,'analytics',c);c['functional_currency']='EUR'
    v=e.versions.current(f['nodes']['reporting'].id);native=e.sources[v.node_id]
    c['imports']=[row(c,'group-statements',package='financial-statements',case=copy.deepcopy(native),result=v.payload(),mode='evidence_only')]
    c['accounts'][0].update(account='cash',amount='490.00',management_amount='490.00')
    c['account_source']['records']=copy.deepcopy(c['accounts']);c['controls']['population_amount']='490.00'
    for d in c['documents']:
        data=d['content']
        if d['id'] in ('current-books','prior-books'):
            amount='490.00' if d['id']=='current-books' else '489.00';data.update(account='cash',statutory_amount=amount,management_amount=amount,gross_amount=amount);data['records'][0].update(account='cash',amount=amount)
        if d['id']=='actual-drivers':data.update(account='cash',drivers=[dict(id='reviewed-financing-receipt',amount='1')],driver_inventory=['reviewed-financing-receipt'])
    c['explanations'][0].update(account='cash',amount='1',interpretation_memo='Cash movement is the separately evidenced financing receipt, not the noncash payable correction')
    # Native diagnostic source-flux analysis; owner accounting conclusion remains
    # solely the current Financial Statements result.
    from governance_cases import document
    prior=['2025-10-01','2025-10-31'];base=dict(entity=n.scope_id,currency='EUR',unit='EUR million',metric='account_balance',presentation_basis='signed_balance')
    ref=dict(owner_import='group-statements',result_path=['current','cash'],amount='490.00')
    for label,amount,span,components in [('cash-current','490.00',n.period,[dict(sign=1,ref=ref)]),('cash-prior','489.00',prior,[])]:
        document(c,label,dict(base,period=span,kind='actual',posted_only=True,amount=amount,records=[dict(id=label+'-posted',amount=amount)],inventory=[label+'-posted'],version='actual-v1',approved=True,supplied=True,approved_on='2026-09-30',owner_components=components,cash=amount),currency='EUR')
    document(c,'cash-drivers',dict(base,period=n.period,baseline_period=prior,comparator_version='actual-v1',method='source_flux',source_owner='financial-statements',source_metric='group cash',category='economic',evidence_class='bridge_attribution',confidence='high',population_complete=True,records=[dict(id='financing-receipt',baseline_amount='489.00',current_amount='490.00',current_owner=ref,posted_only=True,economic_components=['supplied-financing-bank-receipt'])],inventory=['financing-receipt']),currency='EUR')
    c['diagnostic']=dict(component_ties=[dict(groups=['cash-movement'],current_owner=ref,baseline_field='cash',sign=1)],unit='EUR million',metric='account_balance',presentation_basis='signed_balance',current={'doc':'cash-current'},comparator=dict(doc='cash-prior',kind='actual',version='actual-v1',period=prior,frozen_on='2026-09-30'),groups=[dict(id='cash-movement',doc='cash-drivers',method='source_flux',sign=1,labels=dict(movement='Reviewed financing cash receipt'),accounting_check=None)],group_inventory=['cash-movement'],tolerance='.01',materiality='.1',hypotheses=[],signals=[],revenue=None)
    c=adapt(c)
    for d in c['documents']:d['content_hash']=digest(d['content'])
    s3.bind(f,c,'reporting','analytics',('accounts',0,'amount'))
    c['versioned_dependency_receipts']=s3.receipts(f,n.id)
    c=refresh_release(c);c['release_review']['approval_date']=n.period[1]
    return ready('management-accounting-analytics',c=c)


def intake_initial(builder=None, source_factory=None):
    """Natural objective -> validated source proposal -> reviewed ordinary graph.

    This milestone binds original source principal/rate input populations. Further
    source coverage and correction evidence inventory gates remain explicit tests.
    """
    import json
    from orchestration.intake import RawSource, Inventory, StructuredProposal, FactCandidate, FixturePlanner, Intake, Binding, ReviewedInputPack
    from orchestration.tests.intake_fixtures import cl,cell
    from orchestration.planning import FACT_ADAPTERS
    from orchestration.runtime import production
    f=(builder or build)();selected_source=source_factory or source;e=f['session'];plan=serialize(f);raw=[];facts=[];bindings={};children=[]
    family={owner:family for family,(owner,_) in FACT_ADAPTERS.items()}
    proposal=StructuredProposal(cl(OBJECTIVE,status='USER_STATED',confidence=1),cl('One supported Group close conclusion'),cl('CLOSE_REVIEW'),secondary_modes=[cl('RECONCILIATION_INVESTIGATION'),cl('REPORTING'),cl('DIAGNOSTIC_ANALYTICS')],supporting_modes=[cl('DOCUMENTATION')])
    for key in e.topological(e.graph.nodes):
        n=e.graph.nodes[key];label=n.logical_id;p=e.periods.get(n.period_id)
        deps=[e.graph.nodes[q] for q in n.dependencies if e.graph.nodes[q].status!='complete' or e.versions.current(q).payload().get('unresolved_dependencies')]
        c=dict(scope_id=n.scope_id,period_id=n.period_id,source_id='pending-'+label,pending_dependency_evidence='Current material dependencies required',evidence=list(EVIDENCE)) if deps else selected_source(f,label)
        dims=dict(scope_id=n.scope_id,entity=n.scope_id,framework=n.framework,jurisdiction=n.jurisdiction,currency=n.functional_currency or n.presentation_currency,unit='currency',period=n.period,period_id=n.period_id,calendar_id=p.calendar_id,period_role='CURRENT',comparator='actual')
        owner=n.selected_skill;native=not owner.startswith('orchestration-');pending=bool(deps)
        if native:
            if pending:path=('pending_dependency_evidence',);value=c['pending_dependency_evidence'];attribute='pending_review';confirmation=True
            elif owner=='intercompany-accounting':
                role='a' if n.scope_id==c['pairs'][0]['entity_a'] or n.scope_type=='GROUP' else 'b';path=('pairs',0,'confirmed_'+role);value=c['pairs'][0]['confirmed_'+role];attribute='confirmed_principal';confirmation=False
            elif owner=='foreign-currency':path=('translation','tb',1,'balance');value=c['translation']['tb'][1]['balance'];attribute='functional_loan';confirmation=False
            elif owner=='financial-statements':path=('current_tb',0,'balance');value=c['current_tb'][0]['balance'];attribute='authorized_stock';confirmation=False
            else:raise ValueError('Fixture needs separately reviewed adapter for initial active owner')
            source_id='source-'+label
            r=RawSource(source_id,label+'-ledger.csv','csv','record_id,amount\n'+label+','+str(value)+'\n',dict(dims,controlled_export=True,version='v1',unit_scale='million',provenance='Independently supplied controlled company close source'))
            raw.append(r);inv=Inventory([r]);ref=cell(inv,r.id,'amount');actual=inv.extractions[r.id].source
            fact=FactCandidate('fact-'+label,family[owner],attribute+'_'+label.lower().replace('-','_'),cl(str(value),[ref],'EXTRACTED',.99),dims,owner,economic_id=n.economic_id if owner=='intercompany-accounting' and n.scope_type=='LEGAL_ENTITY' else '',confirmation_required=confirmation,transformation='identity')
            proposal.facts.append(fact);proposal.issues.append(cl(dict(id='issue-'+label,owner=owner,family=family[owner],scope_id=n.scope_id,period_id=n.period_id,fact_ids=[fact.id],dependencies=[],required_fields=[fact.attribute]),[ref]))
            if not pending:
                snapshot={k:copy.deepcopy(v) for k,v in c.items() if k not in ('reviewer_signoff','source_population','qualified_scope_sources','qualified_input_snapshot')}
                reviewed=RawSource('review-'+label,label+'-reviewed-workpaper.json','json',[dict(record_id=label,reviewed_input=json.dumps(snapshot,sort_keys=True,separators=(',',':')))],dict(dims,controlled_export=True,version='v1',unit_scale='million',provenance='Separately reviewed complete native input population'))
                raw.append(reviewed);reviewed_original=Inventory([reviewed]).extractions[reviewed.id].source
                c['source_population']=[r.id,reviewed.id];c['qualified_scope_sources']=[dict(source_id=v['id'],fingerprint=v['fingerprint'],metadata=v['metadata']) for v in (actual,reviewed_original)]
                c['qualified_input_snapshot']=dict(source_id=reviewed.id,fingerprint=reviewed_original['fingerprint'])
                c=certify(owner,c)
                bindings[key]=[Binding(fact.id,owner,path,'current',n.scope_id,n.period_id,p.calendar_id)]
        e.execute(key,observation,c,'Initial governed CAO execution')
        children.append(ReviewedInputPack(dict(objective=OBJECTIVE,node_id=key,source=copy.deepcopy(c)),bindings.get(key,[]),scope_id=n.scope_id,period_id=n.period_id,calendar_id=p.calendar_id))
    context=dict(entity='GROUP-EUR',framework='IFRS',jurisdiction='NL',currency='EUR',period_start='2026-10-01',reporting_period='2026-10-31',period_id=f['periods']['CALENDAR-OCT'].period_id,scopes=e.cases.scopes.record(),period_registry=e.periods.record(),materiality='.1')
    plan['sources']=copy.deepcopy(e.sources)
    engine=Intake(FixturePlanner(proposal));prepared=engine.prepare(OBJECTIVE,raw,[],context)
    if not prepared.validation['accepted']:raise ValueError(prepared.validation)
    pack=ReviewedInputPack(dict(objective=OBJECTIVE,scope=copy.deepcopy(prepared._current),governed_plan=plan),[],scoped_packs=children)
    result=engine.execute(prepared,pack);case=result.case;f['case']=case;f['session']=case.governance;f['basis'].session=case.governance
    f['nodes']={label:case.graph.nodes[n.id] for label,n in f['nodes'].items()};f['containers']={label:case.governance.cases.get(c.id) for label,c in f['containers'].items()}
    f.update(intake=result,raw_sources=raw,reviewed_pack=pack,intake_engine=engine)
    return f


def journal_ledger(f):
    e=f['session'];events=[]
    for key in sorted(e.versions.active):
        n=e.graph.nodes[key];v=e.versions.current(key)
        if n.selected_skill=='foreign-currency':continue
        for index,j in enumerate(v.payload().get('journal_entry_implications',[])):
            events.append(dict(economic_id=n.logical_id+':journal:'+str(index),posting_scope=n.scope_id,period=n.period,currency=n.functional_currency or n.presentation_currency,period_id=n.period_id,result_version=v.version_id,primary=[dict(owner=key,index=index)],witnesses=[],evidence='Separately reviewed current native posting economics'))
    g=e.versions.current(f['nodes']['elimination'].id)
    dispositions=[dict(translation_version=e.versions.current(f['nodes'][label].id).version_id,group_version=g.version_id,source_path=['entities',index,'balances'],evidence=list(EVIDENCE)) for label,index in ([('whole-translation-ENTITY-US',1),('whole-translation-ENTITY-UK',2)] if 'whole-translation-ENTITY-US' in f['nodes'] else [('translation',1),('uk-translation',2)])]
    context=dict(entity='GROUP-EUR',framework='IFRS',jurisdiction='NL',currency='EUR',period_start='2026-10-01',reporting_period='2026-10-31',scopes=e.cases.scopes.record(),period_registry=e.periods.record())
    selected,allocation=f['basis'].current_journals(context,events,dispositions)
    return dict(events=events,dispositions=dispositions,selected=selected,allocation=allocation)


def transforms(f):
    e=f['session'];b=f['basis'];out=[]
    for legal,label,conversion,economic in [('clean-ENTITY-US','translation','conversion','clean'),('mismatch-ENTITY-UK','uk-translation','uk-conversion','mismatch')]:
        u=e.versions.current(f['nodes'][legal].id);t=e.versions.current(f['nodes'][label].id);c=e.versions.current(f['nodes'][conversion].id)
        out.append(b.translation(u.version_id,t.version_id,economic,('calculations','pairs',0,'a_functional'),('translation','tb',1,'balance'),('calculations','translation','translated_tb','ic loan'),EVIDENCE))
        out.append(b.intercompany_conversion(t.version_id,c.version_id,economic,('calculations','translation','translated_tb','ic loan'),EVIDENCE))
    return out


def replacement_intake(f, key, supplied):
    """Separately supplied correction/workpaper inventory, never original mutation."""
    import json
    from orchestration.intake import RawSource, Inventory, StructuredProposal, FactCandidate, FixturePlanner, Intake, Binding, ReviewedInputPack
    from orchestration.intake.governed import qualify_replacement
    from orchestration.tests.intake_fixtures import cl, cell
    from orchestration.planning import FACT_ADAPTERS
    from orchestration.runtime import digest, at
    e=f['session'];n=e.graph.nodes[key];p=e.periods.get(n.period_id)
    c={k:copy.deepcopy(v) for k,v in supplied.items() if k not in ('reviewer_signoff','source_population','qualified_scope_sources','qualified_input_snapshot')}
    dims=dict(scope_id=n.scope_id,entity=n.scope_id,framework=n.framework,jurisdiction=n.jurisdiction,currency=n.functional_currency or n.presentation_currency,unit='currency',period=n.period,period_id=n.period_id,calendar_id=p.calendar_id,period_role='CURRENT',comparator='actual')
    provenance=dict(dims,controlled_export=True,version='replacement-'+digest(c),unit_scale='million',provenance='Fresh separately reviewed correction/rework evidence; original source inventory retained')
    proposal=StructuredProposal(cl(OBJECTIVE,status='USER_STATED',confidence=1),cl('Source qualification for retained execution'),cl('CLOSE_REVIEW'))
    owner=n.selected_skill;native=not owner.startswith('orchestration-');raw=[];bindings=[]
    if native:
        path={'intercompany-accounting':('pairs',0,'confirmed_a'),'foreign-currency':('translation','tb',1,'balance'),'consolidation':('entities',0,'balances','cash'),'financial-statements':('current_tb',0,'balance'),'management-accounting-analytics':('accounts',0,'amount')}[owner]
        value=at(c,path);source_id='replacement-value-'+digest([key,c])
        r=RawSource(source_id,n.logical_id+'-replacement.csv','csv','record_id,amount\n'+n.logical_id+','+str(value)+'\n',provenance)
        raw.append(r);inv=Inventory([r]);ref=cell(inv,r.id,'amount')
        family=next(family for family,(candidate,_) in FACT_ADAPTERS.items() if candidate==owner)
        fact=FactCandidate('replacement-fact-'+n.logical_id,family,'reviewed_value_'+n.logical_id.lower().replace('-','_'),cl(str(value),[ref],'EXTRACTED',.99),dims,owner,economic_id=n.economic_id if owner=='intercompany-accounting' and n.scope_type=='LEGAL_ENTITY' else '',confirmation_required=False,transformation='identity')
        proposal.facts.append(fact);proposal.issues.append(cl(dict(id='replacement-issue-'+n.logical_id,owner=owner,family=family,scope_id=n.scope_id,period_id=n.period_id,fact_ids=[fact.id],dependencies=[],required_fields=[fact.attribute]),[ref]))
        bindings=[Binding(fact.id,owner,path,'current',n.scope_id,n.period_id,p.calendar_id)]
    snapshot=RawSource('replacement-snapshot-'+digest([key,c]),n.logical_id+'-replacement-workpaper.json','json',[dict(record_id=n.logical_id,reviewed_input=json.dumps(c,sort_keys=True,separators=(',',':')))],provenance)
    raw.append(snapshot);inventory=Inventory(raw)
    c['source_population']=[r.id for r in raw]
    c['qualified_scope_sources']=[dict(source_id=row.source['id'],fingerprint=row.source['fingerprint'],metadata=row.source['metadata']) for row in inventory.extractions.values()]
    c['qualified_input_snapshot']=dict(source_id=snapshot.id,fingerprint=inventory.extractions[snapshot.id].source['fingerprint'])
    if native:
        # Requalify the supplied reviewed workpaper without rewriting its
        # knowledge selection after the complete snapshot has been sealed.
        from production import case_fingerprint
        c['reviewer_signoff']=dict(reviewer='synthetic independent reviewer',approved=True,case_fingerprint=case_fingerprint(c))
    plan=serialize(f);plan['nodes']=[row for row in e.graph.record() if row['id']==key];plan['sources']={key:c}
    plan['dependencies']=[asdict(edge) for edge in e.edges.values() if edge.consumer_node==key]
    context=dict(entity='GROUP-EUR',framework='IFRS',jurisdiction='NL',currency='EUR',period_start='2026-10-01',reporting_period='2026-10-31',period_id=f['periods']['CALENDAR-OCT'].period_id,scopes=e.cases.scopes.record(),period_registry=e.periods.record(),materiality='.1')
    engine=Intake(FixturePlanner(proposal));prepared=engine.prepare(OBJECTIVE,raw,[],context)
    if not prepared.validation['accepted']:raise ValueError(prepared.validation)
    child=ReviewedInputPack(dict(objective=OBJECTIVE,node_id=key,source=copy.deepcopy(c)),bindings,scope_id=n.scope_id,period_id=n.period_id,calendar_id=p.calendar_id)
    pack=ReviewedInputPack(dict(objective=OBJECTIVE,scope=copy.deepcopy(prepared._current),governed_plan=plan),[],scoped_packs=[child])
    return engine,prepared,pack,raw


def qualified_replacement(f,key,source):
    from orchestration.intake.governed import qualify_replacement
    engine,prepared,pack,raw=replacement_intake(f,key,source)
    qualified=qualify_replacement(engine,prepared,pack,f['case'],key)
    f.setdefault('replacement_intakes',[]).append(dict(node=key,raw_sources=raw,prepared=prepared,reviewed_pack=pack))
    return qualified
