"""Whole-operation positive control, preserving the original bounded controls."""
import copy
from decimal import Decimal
from dataclasses import asdict
from orchestration.tests import stage4_closing_fixtures as closing, stage4_correction_fixtures as prior, stage4_fixtures as s4, stage3_fixtures as s3
from orchestration.runtime import CAO
from orchestration.governed_plan import observation
from additional_cases import fx, certify
from operational_cases import operational
from cases import consolidation


def build():
    f=prior.build();e=f['session'];root=f['containers']['GROUP-EUR-OCT']
    # Replace only incoming translated populations BEFORE any result publication.
    # Bounded transaction translations remain evidence for their reassessments;
    # one complete operation per entity supplies Group accounting.
    remove=[key for key,edge in e.edges.items() if edge.consumer_node==f['nodes']['elimination'].id and e.graph.nodes[edge.producer_node].selected_skill=='foreign-currency']
    for key in remove:
        edge=e.edges.pop(key);f['basis'].contracts.pop(key,None)
        for label,value in list(f['edges'].items()):
            if value==key:del f['edges'][label]
    e.graph.nodes[f['nodes']['elimination'].id].dependencies=sorted({v.producer_node for v in e.edges.values() if v.consumer_node==f['nodes']['elimination'].id})
    s3.add_node(f,'timing-translation-ENTITY-UK','foreign-currency',f['containers']['ENTITY-UK-OCT'],'timing')
    s3.add_edge(f,'timing-ENTITY-UK','timing-translation-ENTITY-UK',('calculations','pairs',0,'b_functional'))
    s3.add_node(f,'timing-reassessment','intercompany-accounting',root,'timing')
    s3.add_edge(f,'timing-current-ENTITY-NL','timing-reassessment',('calculations','pairs',0,'a_functional'))
    s3.add_edge(f,'timing-translation-ENTITY-UK','timing-reassessment',('calculations','translation','translated_tb','timing payable'))
    s3.add_edge(f,'match-timing-current','timing-reassessment',('matching','classification'))
    s3.add_edge(f,'timing-reassessment','elimination',('calculations','pairs',0,'a_functional'))
    s3.add_edge(f,'match-timing-current','elimination',('matching','classification'))
    s3.add_edge(f,'timing-current-ENTITY-NL','elimination',('calculations','pairs',0,'a_functional'))
    for scope,labels in [('ENTITY-US',[('clean-ENTITY-US','a_functional'),('fx-ENTITY-US','b_functional')]),('ENTITY-UK',[('mismatch-ENTITY-UK','a_functional'),('timing-ENTITY-UK','b_functional'),('fx-ENTITY-UK','a_functional')])]:
        label='whole-translation-'+scope
        s3.add_node(f,label,'foreign-currency',f['containers'][scope+'-OCT'],None)
        for legal,metric in labels:
            s3.add_edge(f,legal,label,('calculations','pairs',0,metric))
            s3.add_edge(f,legal,label,('calculations','pairs',0,'a_fx_gain' if metric=='a_functional' else 'b_fx_loss'))
        for metric in ('translated_tb','closing_cta','cta_movement'):s3.add_edge(f,label,'elimination',('calculations','translation',metric))
    s3.add_edge(f,'mismatch-ENTITY-NL','elimination',('calculations','pairs',0,'b_fx_loss'))
    f['reviewed_parent_opening_ledger']=dict(cash='300',investment='258',clean_payable='90',mismatch_payable='11',timing_receivable='30',capital='487',provenance='Separately reviewed parent opening ledger: gross legal balances, investments and capital; current corrections are noncash')
    return f


def timing_translation(f):
    label='timing-translation-ENTITY-UK';n=f['nodes'][label];c=s3.native_context(f,label,fx('UK_GAAP'));c['items']=[]
    c['currency'].update(functional='GBP',ledger='GBP',presentation='EUR')
    c['translation'].update(operation_id='timing',valuation_date=n.period[1],functional_currency='GBP',presentation_currency='EUR',tb=[dict(id='timing cash',balance='100',category='asset',rate='1',memo='Reviewed closing cash'),dict(id='timing payable',balance='-30',category='liability',rate='1',memo='Exact current legal timing payable'),dict(id='timing capital',balance='-70',category='equity',rate='1',memo='Reviewed capital')],opening_net_assets='70',opening_rate='1',closing_rate='1',profit='0',profit_rate='1',reported_closing_net_assets='70',other_oci='0',other_oci_rate='1',ownership='1')
    s3.bind(f,c,'timing-ENTITY-UK',label,('translation','tb',1,'balance'),-1)
    c['versioned_dependency_receipts']=s3.receipts(f,n.id);return certify('foreign-currency',c)


def timing_reassessment(f):
    label='timing-reassessment';n=f['nodes'][label];c=s3.native_context(f,label,operational('intercompany-accounting','IFRS'))
    c['pairs'][0].update(id='timing',transaction_id='timing',entity_a='ENTITY-NL',entity_b='ENTITY-UK',currency='GBP',opening_a='30',opening_b='30',confirmed_a='30',confirmed_b='30',opening_book_a='30',opening_book_b='30',book_a='30',book_b='30',gl_a='30',gl_b='30',rate_a='1',rate_b='1',initial_rate_a='1',initial_rate_b='1',recharge='0',settled_a='0',settled_b='0',date=n.period[1],approval_date=n.period[1])
    c['controls'].update(population_count=1,population_amount='30');c['conversion_economic_id']='timing';c['stage3_contract']='ORDINARY_IC_REASSESSMENT'
    s3.bind(f,c,'timing-current-ENTITY-NL',label,('pairs',0,'gl_a'));s3.bind(f,c,'timing-translation-ENTITY-UK',label,('pairs',0,'gl_b'),-1)
    c['versioned_dependency_receipts']=s3.receipts(f,n.id);return certify('intercompany-accounting',c)


def whole_translation(f,scope):
    label='whole-translation-'+scope;n=f['nodes'][label];e=f['session'];c=s3.native_context(f,label,fx(n.framework));c['items']=[]
    currency='GBP' if scope=='ENTITY-UK' else 'USD';rate='1' if scope=='ENTITY-UK' else '.9';capital='96' if scope=='ENTITY-UK' else '180'
    specs=[('mismatch-ENTITY-UK','a_functional','mismatch loan',1),('timing-ENTITY-UK','b_functional','timing payable',-1),('fx-ENTITY-UK','a_functional','fx loan',1)] if scope=='ENTITY-UK' else [('clean-ENTITY-US','a_functional','clean loan',1),('fx-ENTITY-US','b_functional','fx payable',-1)]
    tb=[dict(id='uk cash' if scope=='ENTITY-UK' else 'cash',balance='100',category='asset',rate=rate,memo='Separately supplied complete operation cash ledger')];bindings=[];net=Decimal('100');profit=Decimal(0)
    for legal,field,account,sign in specs:
        v=e.versions.current(f['nodes'][legal].id);p=v.payload()['calculations']['pairs'][0];value=Decimal(p[field])*sign;net+=value
        index=len(tb);tb.append(dict(id=account,balance=str(value),category='asset' if sign==1 else 'liability',rate=rate,memo='Exact current legal '+legal))
        s3.bind(f,c,legal,label,('translation','tb',index,'balance'),sign)
        gain='a_fx_gain' if sign==1 else 'b_fx_loss';value=Decimal(p[gain])*sign;profit+=value
        index=len(tb);tb.append(dict(id=legal+' profit',balance=str(-value),category='profit',rate=rate,memo='Exact native legal FX profit once'))
        c['stage3_input_bindings'].append(dict(dependency_id=f['edges'][(legal,label,gain)],target_path=['translation','tb',index,'balance'],sign=-sign,evidence=list(s3.EVIDENCE)))
    tb.append(dict(id='uk equity' if scope=='ENTITY-UK' else 'sub equity',balance='-'+capital,category='equity',rate=rate,memo='Separately reviewed acquisition/opening equity ledger'))
    c['currency'].update(functional=currency,ledger=currency,presentation='EUR')
    c['translation'].update(operation_id=scope+'-whole-operation',valuation_date=n.period[1],functional_currency=currency,presentation_currency='EUR',tb=tb,opening_net_assets=capital,opening_rate=rate,closing_rate=rate,profit=str(profit),profit_rate=rate,other_oci='0',other_oci_rate=rate,reported_closing_net_assets=str(net),ownership='1')
    c['reviewed_whole_operation']=dict(source_id=scope+'-COMPLETE-OCT-CLOSE',opening_cash='100',opening_capital=capital,complete_legal_positions=[x[0] for x in specs],provenance='Separately supplied complete finance-holding operation ledger: all governed current loan positions and cash; no other commercial activity')
    c['versioned_dependency_receipts']=s3.receipts(f,n.id);return certify('foreign-currency',c)


def group_source(f):
    e=f['session'];label='elimination';n=f['nodes'][label];c=s3.native_context(f,label,consolidation('IFRS'));control=copy.deepcopy(c['entities'][0]['control'])
    opening=f['reviewed_parent_opening_ledger']
    native=e.sources[f['nodes']['mismatch-ENTITY-NL'].id]['pairs'][0]
    if Decimal(opening['mismatch_payable'])!=Decimal(native['opening_book_b']) or Decimal(opening['capital'])!=Decimal(opening['cash'])+Decimal(opening['investment'])-Decimal(opening['clean_payable'])-Decimal(opening['mismatch_payable'])+Decimal(opening['timing_receivable']):raise ValueError('Reviewed parent ledger differs from native opening source')
    nl={'cash':'300','investment':'258','ic payable':'-90','uk payable':'-10','timing loan':'30','equity':'-487','correction income':'-1'}
    us=e.versions.current(f['nodes']['whole-translation-ENTITY-US'].id).payload()['calculations']['translation']['translated_tb'];uk=e.versions.current(f['nodes']['whole-translation-ENTITY-UK'].id).payload()['calculations']['translation']['translated_tb']
    c['entities']=[dict(id='ENTITY-NL',parent=True,balances=nl,control=control,translation=None,policy_alignment=True,date_alignment=True),dict(id='ENTITY-US',parent=False,balances=dict(us,CTA='0'),control=copy.deepcopy(control),translation=None,policy_alignment=True,date_alignment=True),dict(id='ENTITY-UK',parent=False,balances=dict(uk,CTA='0'),control=copy.deepcopy(control),translation=None,policy_alignment=True,date_alignment=True)]
    inv=copy.deepcopy(c['investments'][0]);nc=copy.deepcopy(c['nci'][0]);c['investments']=[];c['nci']=[]
    for entity,equity,amount in [('ENTITY-US','sub equity','162'),('ENTITY-UK','uk equity','96')]:
        row=copy.deepcopy(inv);row.update(subsidiary=entity,parent_entity='ENTITY-NL',investment=amount,acquisition_equity={equity:amount},nci_at_acquisition='0');c['investments'].append(row)
        row=copy.deepcopy(nc);row.update(subsidiary=entity,ownership='1',opening='0',adjusted_profit='0',adjusted_oci='0');c['nci'].append(row)
    c['intercompany']=[]
    for economic,seller,buyer,debit,credit,producer,amount in [('clean','ENTITY-NL','ENTITY-US','ic payable','clean loan','conversion','90'),('mismatch','ENTITY-NL','ENTITY-UK','uk payable','mismatch loan','uk-conversion','10'),('timing','ENTITY-UK','ENTITY-NL','timing payable','timing loan','timing-reassessment','30'),('fx','ENTITY-US','ENTITY-UK','fx payable','fx loan','fx-reassessment','18')]:
        index=len(c['intercompany']);c['intercompany'].append(dict(id=economic,transaction_id=economic,family='receivable_payable',source_id='reviewed-complete-'+economic,seller=seller,buyer=buyer,amount=amount,debit_account=debit,credit_account=credit,matched=True,source_memo='Separately reviewed full-population reciprocal ledger; exact current transformations'))
        s3.bind(f,c,producer,label,('intercompany',index,'amount'))
    keys=set(nl)|set(us)|set(uk)|{'CTA','goodwill','noncontrolling interest'}
    c['statement_mapping']={k:'assets' if k in ('cash','uk cash','investment','clean loan','mismatch loan','fx loan','timing loan','goodwill') else 'liabilities' if k in ('ic payable','uk payable','timing payable','fx payable') else 'income' if k.endswith(' profit') or k=='correction income' else 'equity' for k in keys}
    c['cash_flow_bridge'].update(opening_cash='490',closing_cash='490',operating='0',investing='0',financing='0',fx='0',cash_accounts=['cash','uk cash'])
    c['equity_bridge'].update(opening='487',profit='3',oci='0',closing='490');c['cta_bridge'].update(translation='0',closing='0',cta_accounts=['CTA'])
    for producer,account,sign in [('clean-ENTITY-NL','ic payable',-1),('mismatch-ENTITY-NL','uk payable',-1),('timing-current-ENTITY-NL','timing loan',1)]:s3.bind(f,c,producer,label,('entities',0,'balances',account),sign)
    for index,scope in [(1,'ENTITY-US'),(2,'ENTITY-UK')]:
        producer='whole-translation-'+scope
        c.setdefault('stage3_input_bindings',[]).append(dict(dependency_id=f['edges'][(producer,label,'closing_cta')],target_path=['entities',index,'balances','CTA'],sign=-1,evidence=list(s3.EVIDENCE)))
    c['stage3_input_bindings'].append(dict(dependency_id=f['edges'][('mismatch-ENTITY-NL',label,'b_fx_loss')],target_path=['entities',0,'balances','correction income'],sign=1,evidence=list(s3.EVIDENCE)))
    c['reviewed_parent_opening_ledger']=copy.deepcopy(opening)
    c['versioned_dependency_receipts']=s3.receipts(f,n.id)
    from orchestration.stage3 import current_legal_loan_versions
    c['group_population_coverage']=dict(mode='ALL_CURRENT_LOAN_SIDES',required_legal_result_versions=current_legal_loan_versions(e,n,{'ENTITY-NL','ENTITY-US','ENTITY-UK'}))
    return certify('consolidation',c)


def source(f,label):
    if label=='timing-translation-ENTITY-UK':return timing_translation(f)
    if label=='timing-reassessment':return timing_reassessment(f)
    if label.startswith('whole-translation-'):return whole_translation(f,label[len('whole-translation-'):])
    if label=='elimination':return group_source(f)
    if label=='reporting':
        c=s4.reporting_source(f);c['equity_bridge'][0].update(opening='487',profit='3',closing='490');c['cash_flow']['start_amount']='3';c['cash_flow']['adjustments'][0]['amount']='-3';c['cash_flow']['adjustments'][0]['source']='Reviewed noncash payable correction and native monetary FX profit';c['cash_flow'].update(opening='490',financing='0',classifications=[]);return certify('financial-statements',c)
    return closing.source(f,label)


def initial():
    f=build();e=f['session'];plan=s4.serialize(f)
    for key in e.topological(e.graph.nodes):
        n=e.graph.nodes[key];blockers=[p for p in n.dependencies if e.graph.nodes[p].status!='complete' or e.versions.current(p).payload().get('unresolved_dependencies')]
        c=dict(scope_id=n.scope_id,period_id=n.period_id,evidence=list(s3.EVIDENCE),source_id='pending-'+n.logical_id) if blockers else source(f,n.logical_id)
        e.execute(key,observation,c,'Initial governed CAO execution')
    plan['sources']=copy.deepcopy(e.sources);case=CAO().run(dict(objective=s4.OBJECTIVE,governed_plan=plan));f['case']=case;f['session']=case.governance;f['basis'].session=case.governance
    f['nodes']={k:case.graph.nodes[v.id] for k,v in f['nodes'].items()};f['containers']={k:case.governance.cases.get(v.id) for k,v in f['containers'].items()};return f


def refresh(f,plan):
    preview=copy.deepcopy(f);e=preview['session'];supplied={};preparation_refusal=None
    for key in plan['execution_order']:
        n=e.graph.nodes[key];blockers=[p for p in n.dependencies if e.graph.nodes[p].status!='complete' or e.versions.current(p).payload().get('unresolved_dependencies')]
        c=dict(scope_id=n.scope_id,period_id=n.period_id,evidence=list(s3.EVIDENCE),source_id='blocked-close-'+n.logical_id) if blockers else s4.qualified_replacement(preview,key,source(preview,n.logical_id))
        supplied[key]=c
        try:e.execute(key,observation,c,'Dependency rework: '+plan['new_version'])
        except ValueError as error:
            if n.logical_id!='reporting' or str(error)!='Versioned native accounting result not qualified':raise
            preparation_refusal=dict(node=n.logical_id,error=str(error));break
    f.setdefault('replacement_intakes',[]).extend(preview.get('replacement_intakes',[])[len(f.get('replacement_intakes',[])):])
    try:
        ledger=CAO().selective_reexecute(f['case'],plan,supplied)
        if preparation_refusal:raise AssertionError('Native refusal was not reproduced')
        return dict(ledger=ledger)
    except ValueError as error:
        if not preparation_refusal or str(error)!=preparation_refusal['error']:raise
        from orchestration.runtime import production
        node=f['nodes']['reporting'];result=production.assess_case(node.selected_skill,supplied[node.id])
        if result.get('status')!='blocked':raise AssertionError('Refusal must be native accounting evidence failure')
        return dict(refusal=preparation_refusal,native_refusal=result,
            executed=[dict(node=f['session'].graph.nodes[key].logical_id,version=f['session'].versions.current(key).version_id) for key in plan['execution_order'] if f['session'].versions.current(key,allow_stale=True) and f['session'].versions.state(f['session'].versions.current(key,allow_stale=True).version_id)=='CURRENT'])


def run():
    f=initial();e=f['session'];before={k:e.versions.current(n.id) for k,n in f['nodes'].items()}
    p=s4.correct(f);first=[]
    for key in p['execution_order']:
        node=e.graph.nodes[key]
        try:
            c=s4.qualified_replacement(f,key,source(f,node.logical_id))
            v=e.execute(key,observation,c,'Dependency rework: '+p['new_version'])
            first.append(dict(node=node.logical_id,version=v.version_id))
        except ValueError as error:
            if node.logical_id!='elimination' or 'Native input differs from exact producer metric' not in str(error):raise
            first.append(dict(node=node.logical_id,status='REFUSED',reason=str(error)))
            break
    n=f['nodes']['fx-ENTITY-UK'];p2=CAO().correct(f['case'],n.id,s4.qualified_replacement(f,n.id,closing.correction(f)),'Separately reviewed October closing treasury quote and legal ledger')
    second=refresh(f,p2)
    return f,dict(before=before,original_payable_correction=p,closing_correction=p2,first_rework=first,closing_rework=second)


def exact_once(f):
    e=f['session'];events=[]
    for key in sorted(e.versions.active):
        v=e.versions.current(key,allow_stale=True);n=e.graph.nodes[key]
        if e.versions.state(v.version_id)!='CURRENT' or n.selected_skill not in ('intercompany-accounting','consolidation'):continue
        for index,journal in enumerate(v.payload().get('journal_entry_implications',[])):
            events.append(dict(economic_id=n.logical_id+':journal:'+str(index),posting_scope=n.scope_id,period_id=n.period_id,period=n.period,currency=n.functional_currency or n.presentation_currency,result_version=v.version_id,primary=[dict(owner=key,index=index)],witnesses=[],evidence='Separately reviewed current native economic posting; exact immutable version'))
    context=dict(entity='GROUP-EUR',framework='IFRS',jurisdiction='NL',currency='EUR',period_start='2026-10-01',reporting_period='2026-10-31',scopes=e.cases.scopes.record(),period_registry=e.periods.record())
    native=[dict(node=e.graph.nodes[x['primary'][0]['owner']].logical_id,result_version=x['result_version'],index=x['primary'][0]['index'],lines=e.versions.versions[x['result_version']].payload()['journal_entry_implications'][x['primary'][0]['index']]) for x in events]
    try:selected,allocation=e.current_journals(context,events)
    except ValueError as error:
        if str(error)!='Stale result cannot satisfy current dependency':raise
        return dict(events=events,native_journal_inventory=native,release_selection='REFUSED',reason=str(error),superseded_excluded=[key for key in sorted(e.versions.versions) if e.versions.state(key)=='SUPERSEDED'])
    return dict(events=events,native_journal_inventory=native,selected=selected,allocation=allocation,superseded_excluded=[key for key in sorted(e.versions.versions) if e.versions.state(key)=='SUPERSEDED'],translation='Only complete operation populations enter Group TB; bounded transaction translations qualify carrying receipts and generate no duplicate postings')


def artifacts():
    f,r=run();e=f['session']
    return dict(original={k:asdict(v) for k,v in r['before'].items()},reviewed_parent_opening_ledger=f['reviewed_parent_opening_ledger'],
        reviewed_closing_source=e.sources[f['nodes']['fx-ENTITY-UK'].id],current=e.versions.record(),
        supersession=e.versions.supersession,invalidation=dict(first=r['original_payable_correction'],closing=r['closing_correction']),
        rework=dict(first=r['first_rework'],closing=r['closing_rework']),
        whole_operation_sources={scope:e.sources[f['nodes']['whole-translation-'+scope].id] for scope in ('ENTITY-US','ENTITY-UK')},
        current_group_source=e.sources[f['nodes']['elimination'].id],current_group_result=asdict(e.versions.current(f['nodes']['elimination'].id)),
        transformations=prior.transformations(f),group_dependency=asdict(f['basis'].receipt(f['fx_group_edge'])),
        exact_once=exact_once(f),reviewed_replacements=[dict(node=x['node'],raw_sources=[asdict(v) for v in x['raw_sources']],inventory=x['prepared'].inventory,lineage=x['prepared'].lineage,reviewed_pack=asdict(x['reviewed_pack'])) for x in f['replacement_intakes']],
        case=dict(status=f['case'].status,outcome=f['case'].outcome),public_answer=CAO().public(f['case']),
        remaining_requirement='Separately reviewed complete comparative/opening Group TB, net-assets and cash history reconciling to native current opening equity487 and cash490; inherited comparative equity489 cannot be overwritten or balanced by an unsupported residual disposition',
        stage4='INCOMPLETE',case_complete=False,case_closed=False)
