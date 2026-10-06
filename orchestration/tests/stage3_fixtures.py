"""Bounded synthetic Stage 3 proof; approvals are fixture-only review records."""
import copy
from dataclasses import asdict, replace
from decimal import Decimal
from orchestration.scopes import ScopeRegistry, execution_identity
from orchestration.periods import FiscalCalendar, Period, PeriodRegistry
from orchestration.cases import CaseRegistry, case_identity
from orchestration.planning import Graph, Node
from orchestration.runtime import Case, CAO, production
from orchestration.versions import VersionedExecution, Dependency, fingerprint
from orchestration.intercompany_network import TransactionSide, MatchingDecision, IntercompanyNetwork
from orchestration.cross_layer_receipts import ReportingBasis
from orchestration.tests.scope_fixtures import ROWS
from operational_cases import operational, handoffs
from additional_cases import fx, reporting, certify
from cases import finalize, consolidation

EVIDENCE = ('Independent synthetic source, rate and accounting review; not authenticated approval',)


def build():
    scopes = ScopeRegistry([replace(s, reporting_calendar='US-FISCAL' if s.scope_id == 'ENTITY-US' else 'CALENDAR') for s in ROWS])
    calendars = [FiscalCalendar('CALENDAR', 'Calendar', 1, 1, EVIDENCE), FiscalCalendar('US-FISCAL', 'July year', 7, 1, EVIDENCE)]
    periods = {}
    for cal in ('CALENDAR', 'US-FISCAL'):
        for label, start, end in [('SEP', '2026-09-01', '2026-09-30'), ('OCT', '2026-10-01', '2026-10-31')]:
            periods[cal + '-' + label] = Period.create(cal, start, end, 2027 if cal == 'US-FISCAL' else 2026, label, provenance=EVIDENCE)
    registry = PeriodRegistry(calendars, periods.values())
    cases = CaseRegistry(scopes, registry)
    containers = {}
    for scope, label in [('GROUP-EUR', 'OCT'), ('ENTITY-NL', 'OCT'), ('ENTITY-US', 'OCT'), ('ENTITY-UK', 'OCT'), ('ENTITY-NL', 'SEP')]:
        p = periods[('US-FISCAL' if scope == 'ENTITY-US' else 'CALENDAR') + '-' + label]
        objective = 'Bounded intercompany review ' + scope + ' ' + label
        c = Case(case_identity(scope, p.period_id, objective, 'stage3-proof'), objective)
        cases.register(c, scope, p.period_id, 'stage3-proof', None if scope == 'GROUP-EUR' else containers['GROUP-EUR-OCT'].id, EVIDENCE)
        containers[scope + '-' + label] = c
    session = VersionedExecution(Graph(), cases, registry)
    session.sources = {}
    f = dict(session=session, nodes={}, containers=containers, periods=periods, source_specs={}, edges={}, basis=ReportingBasis(session))
    for relationship, a, b, ca, cb in [
        ('clean', 'ENTITY-US', 'ENTITY-NL', 'OCT', 'OCT'),
        ('timing', 'ENTITY-NL', 'ENTITY-UK', 'SEP', 'OCT'),
        ('fx', 'ENTITY-UK', 'ENTITY-US', 'OCT', 'OCT'),
        ('mismatch', 'ENTITY-UK', 'ENTITY-NL', 'OCT', 'OCT')]:
        for scope, period, role in [(a, ca, 'receivable'), (b, cb, 'payable')]:
            add_node(f, relationship + '-' + scope, 'intercompany-accounting', containers[scope + '-' + period], relationship)
        add_node(f, 'match-' + relationship, 'orchestration-stage3-match', containers['GROUP-EUR-OCT'], relationship)
        for scope in (a, b):
            add_edge(f, relationship + '-' + scope, 'match-' + relationship, ('calculations', 'pairs', 0, 'a_functional' if scope == a else 'b_functional'))
        f['source_specs'][relationship] = dict(a=a, b=b, pa=ca, pb=cb)
    add_node(f, 'translation', 'foreign-currency', containers['ENTITY-US-OCT'], 'clean')
    add_node(f, 'conversion', 'intercompany-accounting', containers['GROUP-EUR-OCT'], 'clean')
    add_node(f, 'elimination', 'consolidation', containers['GROUP-EUR-OCT'], 'clean')
    add_node(f, 'reporting', 'financial-statements', containers['GROUP-EUR-OCT'], 'clean')
    add_node(f, 'group', 'orchestration-stage3-group', containers['GROUP-EUR-OCT'], 'clean')
    for a, b, path in [
        ('clean-ENTITY-US', 'translation', ('calculations', 'pairs', 0, 'a_functional')),
        ('match-clean', 'translation', ('matching', 'classification')),
        ('translation', 'conversion', ('calculations', 'translation', 'translated_tb', 'ic loan')),
        ('clean-ENTITY-NL', 'conversion', ('calculations', 'pairs', 0, 'b_functional')),
        ('match-clean', 'conversion', ('matching', 'classification')),
        ('conversion', 'elimination', ('calculations', 'pairs', 0, 'a_functional')),
        ('translation', 'elimination', ('calculations', 'translation', 'translated_tb')),
        ('translation', 'elimination', ('calculations', 'translation', 'closing_cta')),
        ('translation', 'elimination', ('calculations', 'translation', 'cta_movement')),
        ('clean-ENTITY-NL', 'elimination', ('calculations', 'pairs', 0, 'b_functional')),
        ('match-clean', 'elimination', ('matching', 'classification')),
        ('elimination', 'reporting', ('calculations', 'consolidated_balances')),
        ('reporting', 'group', ('calculations',))]:
        add_edge(f, a, b, path)
    declare_basis(f)
    return f


def declare_basis(f):
    b=f['basis']
    for a,c,pl,cl,fw,cur,semantic in [
        ('clean-ENTITY-US','translation','LEGAL_ENTITY','TRANSLATION','US_GAAP','USD','ordinary_reciprocal_balance'),
        ('translation','conversion','TRANSLATION','FRAMEWORK_ADJUSTMENT','US_GAAP','EUR','translated_intercompany_balance'),
        ('conversion','elimination','FRAMEWORK_ADJUSTMENT','GROUP_ELIMINATION','IFRS','EUR','ordinary_reciprocal_balance'),
        ('elimination','reporting','GROUP_ELIMINATION','GROUP_REPORTING','IFRS','EUR','consolidated_population'),
        ('reporting','group','GROUP_REPORTING','GROUP_REPORTING','IFRS','EUR','group_statements')]:
        b.declare(f['edges'][(a,c)],producer_layer=pl,consumer_layer=cl,framework=fw,currency=cur,
            semantic_metric=semantic,economic_id='clean',required_framework=fw,required_currency=cur,evidence=EVIDENCE)


def add_node(f, label, owner, case, economic):
    e = f['session']; s = e.cases.scopes.get(case.scope_id); p = e.periods.get(case.period_id)
    context = dict(scope_id=s.scope_id, scope_type=s.scope_type, framework=s.framework, jurisdiction=s.jurisdiction,
        functional_currency=s.functional_currency, presentation_currency=s.presentation_currency,
        period_start=p.start, reporting_period=p.end, period_id=p.period_id, economic_id=economic)
    n = Node(execution_identity(owner, context), label, owner, 'Bounded Stage 3 production route', s.scope_id,
        s.framework, [p.start, p.end], scope_id=s.scope_id, scope_type=s.scope_type, jurisdiction=s.jurisdiction,
        functional_currency=s.functional_currency, presentation_currency=s.presentation_currency,
        period_id=p.period_id, case_id=case.id, logical_id=label, economic_id=economic)
    e.graph.add(n);e.cases.bind_node(case.id,n);f['nodes'][label]=n
    return n


def add_edge(f, a, b, path):
    e=f['session'];p=f['nodes'][a];c=f['nodes'][b]
    typ='CURRENT' if p.period_id==c.period_id else 'QUALIFIED_ALIGNMENT'
    edge=Dependency(p.id,c.id,p.case_id,c.case_id,p.scope_id,c.scope_id,p.period_id,c.period_id,
        typ,'EXPLICIT_CROSS_CASE',path,EVIDENCE,alignment_evidence=EVIDENCE if typ=='QUALIFIED_ALIGNMENT' else ())
    key=e.add_dependency(edge);f['edges'][(a,b) if (a,b) not in f['edges'] else (a,b,path[-1])]=key
    return key


def native_context(f, label, source):
    n=f['nodes'][label];source.update(entity=n.scope_id,scope_id=n.scope_id,framework=n.framework,
        jurisdiction=n.jurisdiction,period_start=n.period[0],reporting_period=n.period[1],
        period_id=n.period_id,economic_id=n.economic_id,case_id='stage3-'+label,functional_currency=n.functional_currency or n.presentation_currency)
    source['applicability_review']['effective_period']=n.period
    if source.get('framework')=='US_GAAP':source['us_entity_type']='public'
    if 'execution_date' in source:source['execution_date']=n.period[1]
    for h in source.get('handoffs',{}).values():h.update(entity=n.scope_id,framework=n.framework,reporting_period=n.period[1])
    if 'controls' in source:source['controls']['as_of']=n.period[1]
    return source


def legal_source(f, relationship, scope, corrected=False):
    spec=f['source_specs'][relationship];label=relationship+'-'+scope;n=f['nodes'][label]
    c=native_context(f,label,operational('intercompany-accounting',n.framework));p=c['pairs'][0]
    principal={'clean':'90','timing':'30','fx':'20','mismatch':'10' if scope=='ENTITY-UK' else '11'}[relationship]
    # Quotes are separately supplied reviewed data; fixture arithmetic prepares
    # independently reviewed native inputs, never runtime-generated FX treatment.
    ra,rb={'clean':('1.2222222222222222222222' if corrected else '1.1111111111111111111111','1'),
           'timing':('1','1'), 'fx':('0.8','1'), 'mismatch':('1','1')}[relationship]
    local_a=str((Decimal(principal)*Decimal(ra)).quantize(Decimal('.01')));local_b=str((Decimal(principal)*Decimal(rb)).quantize(Decimal('.01')))
    opening_a='100.00' if relationship=='clean' else local_a
    p.update(id=relationship,transaction_id=relationship,entity_a=spec['a'],entity_b=spec['b'],
        currency={'clean':'EUR','timing':'GBP','fx':'USD','mismatch':'EUR'}[relationship],
        opening_a=principal,opening_b=principal,confirmed_a=principal,confirmed_b=principal,
        opening_book_a=opening_a,opening_book_b=local_b,book_a=opening_a,book_b=local_b,
        gl_a=local_a,gl_b=local_b,rate_a=ra,rate_b=rb,recharge='0',settled_a='0',settled_b='0',
        date=n.period[1],approval_date=n.period[1],version='v2' if corrected else 'v1',approved_version='v2' if corrected else 'v1')
    c['controls'].update(population_count=1,population_amount=principal)
    role='receivable' if scope==spec['a'] else 'payable'
    row=dict(source_id='source-'+label,economic_id=relationship,book_entry_id='book-'+label,
        agreement_id='agreement-'+relationship,network_id='STAGE3-NETWORK',scope_id=scope,
        counterparty_scope=spec['b'] if scope==spec['a'] else spec['a'],period_id=n.period_id,
        transaction_class='loan',role=role,functional_currency=n.functional_currency,
        functional_amount=local_a if role=='receivable' else local_b,
        transaction_currency=p['currency'],transaction_amount=principal)
    c['intercompany_transactions']=[row]
    return certify('intercompany-accounting',c)


def sides(f, relationship):
    e=f['session'];spec=f['source_specs'][relationship];out=[]
    for scope,other in [(spec['a'],spec['b']),(spec['b'],spec['a'])]:
        n=f['nodes'][relationship+'-'+scope];other_node=f['nodes'][relationship+'-'+other]
        v=e.versions.current(n.id);row=e.sources[n.id]['intercompany_transactions'][0]
        out.append(TransactionSide(**{k:row[k] for k in row if k!='source_id'},source_id=row['source_id'],
            case_id=n.case_id,owner_node=n.id,result_version=v.version_id,
            metric_path=('calculations','pairs',0,'a_functional' if scope==spec['a'] else 'b_functional'),
            source_path=('intercompany_transactions',0),source_fingerprint=fingerprint(row),evidence=EVIDENCE,
            counterparty_case=other_node.case_id,counterparty_period=other_node.period_id))
    return out


def match_source(f, relationship):
    n=f['nodes']['match-'+relationship];ss=sides(f,relationship)
    decision=MatchingDecision(ss[0].relationship_id,tuple(s.side_id for s in ss),
        {'clean':'MATCHED','timing':'TIMING_DIFFERENCE','fx':'FX_DIFFERENCE','mismatch':'UNRESOLVED_MISMATCH'}[relationship],
        EVIDENCE,tuple(s.result_version for s in ss),'synthetic independent residual reviewer','Evidence-backed classification; no generated correction',period_alignment=EVIDENCE)
    return dict(scope_id=n.scope_id,period_id=n.period_id,method='STAGE3_MATCH',network_id='STAGE3-NETWORK',
        sides=[asdict(s) for s in ss],decision=asdict(decision),evidence=list(EVIDENCE),
        versioned_dependency_receipts=receipts(f,n.id))


def receipts(f, node):
    e=f['session'];return [e.receipt(k) for k,edge in sorted(e.edges.items()) if edge.consumer_node==node]


def bind(f, source, a, b, target_path, sign=1):
    source.setdefault('stage3_input_bindings',[]).append(dict(dependency_id=f['edges'][(a,b)],target_path=list(target_path),sign=sign,evidence=list(EVIDENCE)))


def downstream_source(f, label, corrected=False):
    e=f['session'];n=f['nodes'][label]
    if label=='translation':
        c=native_context(f,label,fx('US_GAAP'));c['items']=[];c['currency'].update(functional='USD',ledger='USD',presentation='EUR')
        value=e.versions.current(f['nodes']['clean-ENTITY-US'].id).payload()['calculations']['pairs'][0]['a_functional']
        rate='0.8181818181818181818182' if corrected else '0.9';profit='10.00' if corrected else '0.00'
        t=c['translation'];t.update(operation_id='clean',valuation_date=n.period[1],functional_currency='USD',presentation_currency='EUR',
            tb=[dict(id='cash',balance='100.00',category='asset',rate=rate,memo='Reviewed cash closing rate'),
                dict(id='ic loan',balance=value,category='asset',rate=rate,memo='Exact native legal loan result'),
                dict(id='sub equity',balance='-200.00',category='equity',rate='0.9',memo='Historical equity'),
                dict(id='FX income',balance='-'+profit,category='profit',rate=rate,memo='Native IC remeasurement result')],
            opening_net_assets='200',opening_rate='0.9',closing_rate=rate,profit=profit,profit_rate=rate,
            other_oci='0',other_oci_rate=rate,reported_closing_net_assets='210' if corrected else '200',ownership='1')
        bind(f,c,'clean-ENTITY-US',label,('translation','tb',1,'balance'))
    elif label=='conversion':
        c=native_context(f,label,operational('intercompany-accounting','IFRS'))
        p=c['pairs'][0];p.update(id='clean',transaction_id='clean',entity_a='ENTITY-US',entity_b='ENTITY-NL',currency='EUR',
            opening_a='90',opening_b='90',opening_book_a='90',opening_book_b='90',book_a='90',book_b='90',
            gl_a='90',gl_b='90',confirmed_a='90',confirmed_b='90',rate_a='1',rate_b='1',
            initial_rate_a='1',initial_rate_b='1',date=n.period[1],approval_date=n.period[1])
        c['controls'].update(population_count=1,population_amount='90');c['conversion_economic_id']='clean';c['stage3_contract']='ORDINARY_IC_REASSESSMENT'
        bind(f,c,'translation',label,('pairs',0,'gl_a'))
        bind(f,c,'clean-ENTITY-NL',label,('pairs',0,'gl_b'))
    elif label=='elimination':
        c=native_context(f,label,consolidation('IFRS'));tb=e.versions.current(f['nodes']['translation'].id).payload()['calculations']['translation']['translated_tb']
        c['entities'][0].update(id='ENTITY-NL',balances={'cash':'300','investment':'180','ic payable':'-90','equity':'-390'})
        c['entities'][1].update(id='ENTITY-US',balances=dict(tb,**{'CTA': '16.36' if corrected else '0'}),translation=None)
        c['intercompany']=[dict(id='clean',transaction_id='clean',family='receivable_payable',source_id='reviewed-clean',seller='ENTITY-NL',buyer='ENTITY-US',amount='90',debit_account='ic payable',credit_account='ic loan',matched=True,source_memo='Exact current matching/conversion/translation')]
        c['investments'][0].update(subsidiary='ENTITY-US',parent_entity='ENTITY-NL',investment='180',acquisition_equity={'sub equity':'180'},nci_at_acquisition='0')
        c['nci'][0].update(subsidiary='ENTITY-US',ownership='1',opening='0',adjusted_profit='8.18' if corrected else '0',adjusted_oci='-16.36' if corrected else '0')
        c['statement_mapping'].update({'ic payable':'liabilities','ic loan':'assets','FX income':'income','CTA':'equity'})
        close='381.82' if corrected else '390';c['cash_flow_bridge'].update(opening_cash='390',closing_cash=close,fx='-8.18' if corrected else '0')
        c['equity_bridge'].update(opening='390',profit='8.18' if corrected else '0',oci='-16.36' if corrected else '0',closing=close)
        c['cta_bridge'].update(translation='16.36' if corrected else '0',closing='16.36' if corrected else '0',cta_accounts=['CTA'])
        for account in list(c['statement_mapping']):
            if account not in {'cash','investment','ic payable','equity','ic loan','sub equity','FX income','CTA','goodwill','noncontrolling interest'}:del c['statement_mapping'][account]
        for semantic,path,sign in [
            ('closing_cta',['entities',1,'balances','CTA'],-1),
            ('closing_cta',['cta_bridge','closing'],-1),
            ('cta_movement',['cta_bridge','translation'],-1),
            ('cta_movement',['equity_bridge','oci'],1)]:
            c.setdefault('stage3_input_bindings',[]).append(dict(dependency_id=f['edges'][('translation',label,semantic)],target_path=path,sign=sign,evidence=list(EVIDENCE)))
        # Population binding plus individual signed legal-side/conversion rows.
        bind(f,c,'conversion',label,('intercompany',0,'amount'))
        bind(f,c,'clean-ENTITY-NL',label,('entities',0,'balances','ic payable'),-1)
    elif label=='reporting':
        c=native_context(f,label,reporting());balances=e.versions.current(f['nodes']['elimination'].id).payload()['calculations']['consolidated_balances']
        mapping=e.sources[f['nodes']['elimination'].id]['statement_mapping']
        categories={'assets':'asset','liabilities':'liability','equity':'equity','income':'revenue','expenses':'expense'}
        c['current_tb']=[dict(id=k,balance=v,category='oci' if k=='CTA' else categories[mapping[k]],performance_category='operating',line=k,
            source_version=e.versions.current(f['nodes']['elimination'].id).version_id,
            classification_memo='Current qualified Consolidation account',cash_account=k=='cash') for k,v in sorted(balances.items())]
        c['comparative_tb']=[dict(id='cash',balance='390',category='asset',performance_category='operating',line='cash',source_version='prior',classification_memo='Reviewed prior',cash_account=True),dict(id='opening equity',balance='-390',category='equity',performance_category='operating',line='opening equity',source_version='prior',classification_memo='Reviewed prior',cash_account=False)]
        close='381.82' if corrected else '390';profit='8.18' if corrected else '0';oci='-16.36' if corrected else '0'
        c['equity_bridge'][0].update(opening='390',profit=profit,oci=oci,closing=close)
        c['cash_flow'].update(start_amount=profit,adjustments=[dict(id='noncash',amount='-'+profit if corrected else '0',source='Qualified FX adjustment',noncash_acquisition_fx_excluded=True,memo='FX income excluded from cash')],investing='0',financing='0',fx='-8.18' if corrected else '0',opening='390',closing=close,classifications=[dict(id='op',date=n.period[1],kind='net_operating',**{'class':'operating'},amount='0',memo='No operational cash movement')])
        c['notes'][0]['amount']=close
        # All accounts are individually mapped; no net-population shortcut.
        for index,row in enumerate(c['current_tb']):
            edge=next(edge for edge in e.edges.values() if edge.consumer_node==n.id)
            c.setdefault('stage3_population_binding',{})[row['id']]=dict(source_version=e.versions.current(edge.producer_node).version_id,value=row['balance'])
        # Generic binding covers a numeric statement total rather than nested
        # account reshaping; the complete population is validated below.
        c['versioned_dependency_receipts']=receipts(f,n.id)
        c['stage3_input_bindings']=[dict(dependency_id=f['edges'][('elimination',label)],target_path=['stage3_balances'],sign=1,evidence=list(EVIDENCE))]
        c['stage3_balances']=copy.deepcopy(balances)
    else:
        return dict(scope_id=n.scope_id,period_id=n.period_id,method='STAGE3_GROUP_OBSERVATION',evidence=list(EVIDENCE))
    c['versioned_dependency_receipts']=receipts(f,n.id)
    return certify(n.selected_skill,c)


def execute(f,label,source):
    e=f['session'];n=f['nodes'][label]
    from orchestration.governed_plan import observation
    version=e.execute(n.id,observation,source,'Initial governed CAO execution')
    e.sources[n.id]=copy.deepcopy(source)
    return version


def initial(f):
    e=f['session']
    for label,n in sorted(f['nodes'].items()):
        if not n.dependencies:execute(f,label,legal_source(f,n.economic_id,n.scope_id))
    for relationship in sorted(f['source_specs']):execute(f,'match-'+relationship,match_source(f,relationship))
    for label in ('translation','conversion','elimination','reporting','group'):execute(f,label,downstream_source(f,label))
    return f


def correct(f):
    e=f['session'];execute(f,'clean-ENTITY-US',legal_source(f,'clean','ENTITY-US',True))
    return copy.deepcopy(e.rework_history[-1])


def reviewed_rework_sources(f,plan):
    # A fixture reviewer prepares packs against deterministic prospective
    # versions in an isolated rehearsal. The runtime never manufactures approval.
    preview=copy.deepcopy(f);e=preview['session'];sources={}
    from orchestration.governed_plan import observation
    for key in plan['execution_order']:
        label=e.graph.nodes[key].logical_id
        source=match_source(preview,'clean') if label=='match-clean' else downstream_source(preview,label,True)
        e.execute(key,observation,source,'Dependency rework: '+plan['new_version'])
        e.sources[key]=copy.deepcopy(source);sources[key]=source
    return sources


def rework(f,plan):
    from orchestration.governed_plan import observation
    e=f['session'];sources=reviewed_rework_sources(f,plan)
    ledger=e.reexecute(plan,{key:observation for key in plan['execution_order']},sources)
    e.sources.update(copy.deepcopy(sources))
    return ledger


def network(f):
    result=IntercompanyNetwork(f['session'],'STAGE3-NETWORK')
    for relationship in sorted(f['source_specs']):
        for side in sides(f,relationship):result.register(side)
        n=f['nodes']['match-'+relationship]
        decision=MatchingDecision(**f['session'].sources[n.id]['decision'])
        result.match(decision)
    return result


def ordinary_initial():
    f=build();e=f['session'];root=f['containers']['GROUP-EUR-OCT']
    plan=dict(scopes=e.cases.scopes.record(),periods=e.periods.record(),
        cases=[dict(case_id=c.id,objective=c.objective,scope_id=c.scope_id,period_id=c.period_id,
            cycle=c.cycle,parent_id=c.parent_case_id,provenance=c.provenance) for c in e.cases.cases.values()],
        root_case=root.id,nodes=e.graph.record(),dependencies=[asdict(edge) for edge in e.edges.values()])
    initial(f)
    plan['sources']=copy.deepcopy(e.sources)
    case=CAO().run(dict(objective=root.objective,governed_plan=plan))
    f['case']=case;f['session']=case.governance
    f['nodes']={label:case.graph.nodes[n.id] for label,n in f['nodes'].items()}
    f['containers']={label:case.governance.cases.get(c.id) for label,c in f['containers'].items()}
    contracts=copy.deepcopy(f['basis'].contracts)
    f['basis']=ReportingBasis(case.governance);f['basis'].contracts=contracts
    return f


def journal_inputs(f):
    e=f['session'];events=[]
    context=dict(entity='GROUP-EUR',framework='IFRS',jurisdiction='NL',currency='EUR',period_start='2026-10-01',
        reporting_period='2026-10-31',scopes=e.cases.scopes.record(),period_registry=e.periods.record())
    for label in ('clean-ENTITY-US','elimination'):
        n=f['nodes'][label];v=e.versions.current(n.id)
        for index,j in enumerate(v.payload().get('journal_entry_implications',[])):
            events.append(dict(economic_id=label+':journal:'+str(index),posting_scope=n.scope_id,period=n.period,
                currency=n.functional_currency or n.presentation_currency,period_id=n.period_id,result_version=v.version_id,
                primary=[dict(owner=n.id,index=index)],witnesses=[],evidence='Independently reviewed native current posting event'))
    dispositions=[dict(translation_version=e.versions.current(f['nodes']['translation'].id).version_id,
        group_version=e.versions.current(f['nodes']['elimination'].id).version_id,
        source_path=['entities',1,'balances'],evidence=list(EVIDENCE))]
    return context,events,dispositions


def transformation_receipts(f):
    e=f['session'];b=f['basis']
    u=e.versions.current(f['nodes']['clean-ENTITY-US'].id);t=e.versions.current(f['nodes']['translation'].id);c=e.versions.current(f['nodes']['conversion'].id)
    return [b.translation(u.version_id,t.version_id,'clean',('calculations','pairs',0,'a_functional'),('translation','tb',1,'balance'),('calculations','translation','translated_tb','ic loan'),EVIDENCE),
        b.intercompany_conversion(t.version_id,c.version_id,'clean',('calculations','translation','translated_tb','ic loan'),EVIDENCE)]
