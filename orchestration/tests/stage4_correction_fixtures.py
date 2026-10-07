"""Reviewed opening-book transcription correction; deliberately Outcome B.

This controlled evidence is synthetic, not authenticated company approval.
The closing rate is unchanged. No target EUR amount is an input or criterion.
Existing Intercompany owns ordinary monetary remeasurement; Foreign Currency
owns the separately reconciled presentation translation. No new methodology.
"""
import copy
from dataclasses import asdict
from decimal import Decimal
from orchestration.tests import stage4_fixtures as s4, stage3_fixtures as s3
from orchestration.governed_plan import observation
from orchestration.runtime import CAO
from additional_cases import fx, certify
from operational_cases import operational


def build():
    f=s4.build();root=f['containers']['GROUP-EUR-OCT']
    s3.add_node(f,'match-fx-current','orchestration-current-match',root,'fx')
    for scope,role in [('ENTITY-UK','a'),('ENTITY-US','b')]:
        label='fx-translation-'+scope
        s3.add_node(f,label,'foreign-currency',f['containers'][scope+'-OCT'],'fx')
        s3.add_edge(f,'fx-'+scope,label,('calculations','pairs',0,role+'_functional'))
        s3.add_edge(f,'fx-'+scope,label,('calculations','pairs',0,'a_fx_gain' if role=='a' else 'b_fx_loss'))
        s3.add_edge(f,'fx-'+scope,'match-fx-current',('calculations','pairs',0,role+'_functional'))
    s3.add_node(f,'fx-reassessment','intercompany-accounting',root,'fx')
    for scope,account in [('ENTITY-UK','ic loan'),('ENTITY-US','fx payable')]:
        label='fx-translation-'+scope
        s3.add_edge(f,label,'fx-reassessment',('calculations','translation','translated_tb',account))
        for metric in ('translated_tb','closing_cta','cta_movement'):
            s3.add_edge(f,label,'elimination',('calculations','translation',metric))
    s3.add_edge(f,'match-fx-current','fx-reassessment',('matching','classification'))
    edge=s3.add_edge(f,'fx-reassessment','elimination',('calculations','pairs',0,'a_functional'))
    s3.add_edge(f,'match-fx-current','elimination',('matching','classification'))
    f['basis'].declare(edge,producer_layer='FRAMEWORK_ADJUSTMENT',consumer_layer='GROUP_ELIMINATION',framework='IFRS',currency='EUR',semantic_metric='ordinary_reciprocal_balance',economic_id='fx',required_framework='IFRS',required_currency='EUR',evidence=s3.EVIDENCE)
    f['fx_group_edge']=edge
    f['fx_operation_ledgers']={'ENTITY-UK':dict(cash='100',receivable='16',capital='116',memo='Separately reviewed original opening operation ledger'), 'ENTITY-US':dict(cash='100',payable='20',capital='80',memo='Separately reviewed original US opening operation ledger')}
    return f


def reviewed_correction(f):
    c=copy.deepcopy(f['session'].sources[f['nodes']['fx-ENTITY-UK'].id])
    for key in ('reviewer_signoff','source_population','qualified_scope_sources','qualified_input_snapshot'):c.pop(key,None)
    p=c['pairs'][0]
    # The new evidence corrects the pre-remeasurement ledger transcription,
    # NOT the principal, closing carrying value, currency or closing quote.
    p.update(opening_book_a='15',book_a='15',version='opening-review-v2',approved_version='opening-review-v2',
             opening_book_evidence='Separate reviewed opening ledger UK-IC-OPEN-02: USD20 receivable, GBP15 pre-remeasurement carrying; original export incorrectly transcribed GBP16')
    c['correction_evidence']=dict(reviewed=True,synthetic=True,source_id='UK-IC-OPEN-02',
        original_source_id='source-fx-ENTITY-UK',original_opening_book='16',reviewed_opening_book='15',
        reason='Opening book export transcription corrected against separately reviewed ledger and confirmation',
        opening_operation=dict(cash='100',receivable='15',capital='115',memo='Separately supplied opening operation ledger; not an inferred CTA or balancing capital adjustment'),
        unchanged=['USD20 principal','USD transaction currency','GBP functional currency','0.8 GBP per USD closing quote','GBP16 closing receivable','agreement-fx','book-fx-ENTITY-UK','ENTITY-US counterparty'])
    return certify('intercompany-accounting',c)


def translation_source(f,scope):
    label='fx-translation-'+scope;n=f['nodes'][label];e=f['session']
    c=s3.native_context(f,label,fx(n.framework));c['items']=[]
    currency='GBP' if scope=='ENTITY-UK' else 'USD';sign=1 if scope=='ENTITY-UK' else -1
    rate='1' if scope=='ENTITY-UK' else '.9'
    legal=e.versions.current(f['nodes']['fx-'+scope].id);pair=legal.payload()['calculations']['pairs'][0]
    native=e.sources[legal.node_id]
    reviewed=native.get('correction_evidence',{}).get('opening_operation',f['fx_operation_ledgers'][scope])
    opening=reviewed['capital'];cash=reviewed['cash'];field='receivable' if sign==1 else 'payable'
    opening_book=native['pairs'][0]['opening_book_a' if sign==1 else 'opening_book_b']
    if Decimal(reviewed[field])!=Decimal(opening_book) or Decimal(opening)!=Decimal(cash)+sign*Decimal(opening_book):
        raise ValueError('Reviewed opening operation ledger differs from exact legal opening book/capital')
    if native.get('correction_evidence') and Decimal(native['correction_evidence']['reviewed_opening_book'])!=Decimal(opening_book):
        raise ValueError('Correction evidence differs from native legal opening book')
    profit=str(Decimal(pair['a_fx_gain' if sign==1 else 'b_fx_loss'])*sign)
    amount=pair['a_functional' if sign==1 else 'b_functional']
    close=str(Decimal(cash)+sign*Decimal(amount))
    c['currency'].update(functional=currency,ledger=currency,presentation='EUR')
    c['translation'].update(operation_id='fx',valuation_date=n.period[1],functional_currency=currency,presentation_currency='EUR',
        tb=[dict(id='cash',balance=cash,category='asset',rate=rate,memo=reviewed['memo']),
            dict(id='ic loan' if sign==1 else 'fx payable',balance=str(Decimal(amount)*sign),category='asset' if sign==1 else 'liability',rate=rate,memo='Exact signed current native legal result'),
            dict(id='equity',balance='-'+opening,category='equity',rate=rate,memo='Reviewed opening capital ledger'),
            dict(id='FX income',balance=str(-Decimal(profit)),category='profit',rate=rate,memo='Current native monetary FX once')],
        opening_net_assets=opening,opening_rate=rate,closing_rate=rate,profit=profit,profit_rate=rate,
        other_oci='0',other_oci_rate=rate,reported_closing_net_assets=close,ownership='1')
    c['reviewed_operation_ledger']=copy.deepcopy(reviewed)
    if native.get('correction_evidence'):c['correction_evidence']=copy.deepcopy(native['correction_evidence'])
    s3.bind(f,c,'fx-'+scope,label,('translation','tb',1,'balance'),sign)
    metric='a_fx_gain' if sign==1 else 'b_fx_loss'
    c.setdefault('stage3_input_bindings',[]).append(dict(dependency_id=f['edges'][('fx-'+scope,label,metric)],target_path=['translation','tb',3,'balance'],sign=-sign,evidence=list(s3.EVIDENCE)))
    c['versioned_dependency_receipts']=s3.receipts(f,n.id)
    return certify('foreign-currency',c)


def current_match(f):
    c=s3.match_source(f,'fx');n=f['nodes']['match-fx-current']
    c['decision']['classification']='MATCHED'
    c['decision']['reason']='Reviewed reciprocal USD20 legal principals and exact agreement/book/counterparty identities; qualified principal match does not dispose of presentation carrying residual'
    c['versioned_dependency_receipts']=s3.receipts(f,n.id)
    return c


def reassessment_source(f):
    n=f['nodes']['fx-reassessment'];c=s3.native_context(f,n.logical_id,operational('intercompany-accounting','IFRS'))
    c['pairs'][0].update(id='fx',transaction_id='fx',entity_a='ENTITY-UK',entity_b='ENTITY-US',currency='USD',opening_a='20',opening_b='20',confirmed_a='20',confirmed_b='20',opening_book_a='16',opening_book_b='18',book_a='16',book_b='18',gl_a='16',gl_b='18',rate_a='.8',rate_b='.9',initial_rate_a='.8',initial_rate_b='.9',recharge='0',settled_a='0',settled_b='0',date=n.period[1],approval_date=n.period[1])
    c['controls'].update(population_count=1,population_amount='20');c['conversion_economic_id']='fx';c['stage3_contract']='ORDINARY_IC_REASSESSMENT'
    s3.bind(f,c,'fx-translation-ENTITY-UK',n.logical_id,('pairs',0,'gl_a'))
    s3.bind(f,c,'fx-translation-ENTITY-US',n.logical_id,('pairs',0,'gl_b'),-1)
    c['versioned_dependency_receipts']=s3.receipts(f,n.id)
    return certify('intercompany-accounting',c)


def source(f,label):
    if label=='match-fx-current':return current_match(f)
    if label.startswith('fx-translation-'):return translation_source(f,label[len('fx-translation-'):])
    if label=='fx-reassessment':return reassessment_source(f)
    return s4.source(f,label)


def initial():
    f=build();e=f['session'];plan=s4.serialize(f)
    for key in e.topological(e.graph.nodes):
        n=e.graph.nodes[key]
        blockers=[p for p in n.dependencies if e.graph.nodes[p].status!='complete' or e.versions.current(p).payload().get('unresolved_dependencies')]
        c=dict(scope_id=n.scope_id,period_id=n.period_id,evidence=list(s3.EVIDENCE),source_id='pending-'+n.logical_id) if blockers else source(f,n.logical_id)
        e.execute(key,observation,c,'Initial governed CAO execution')
    plan['sources']=copy.deepcopy(e.sources)
    case=CAO().run(dict(objective=s4.OBJECTIVE,governed_plan=plan));f['case']=case;f['session']=case.governance;f['basis'].session=case.governance
    f['nodes']={label:case.graph.nodes[n.id] for label,n in f['nodes'].items()}
    f['containers']={label:case.governance.cases.get(c.id) for label,c in f['containers'].items()}
    return f


def run():
    f=initial();e=f['session'];n=f['nodes'];before={label:e.versions.current(node.id) for label,node in n.items()}
    fresh=s4.qualified_replacement(f,n['fx-ENTITY-UK'].id,reviewed_correction(f))
    plan=CAO().correct(f['case'],n['fx-ENTITY-UK'].id,fresh,'Reviewed UK opening-book transcription evidence; unchanged principal and closing rate')
    stale={label:dict(version=v.version_id,state=e.versions.state(v.version_id)) for label,v in before.items()}
    preview=copy.deepcopy(f);pe=preview['session'];supplied={}
    for key in plan['execution_order']:
        node=pe.graph.nodes[key]
        blockers=[p for p in node.dependencies if pe.graph.nodes[p].status!='complete' or pe.versions.current(p).payload().get('unresolved_dependencies')]
        c=dict(scope_id=node.scope_id,period_id=node.period_id,evidence=list(s3.EVIDENCE),source_id='blocked-correction-'+node.logical_id) if blockers else s4.qualified_replacement(preview,key,source(preview,node.logical_id))
        pe.execute(key,observation,c,'Dependency rework: '+plan['new_version']);supplied[key]=c
    f.setdefault('replacement_intakes',[]).extend(preview.get('replacement_intakes',[])[len(f.get('replacement_intakes',[])):])
    ledger=CAO().selective_reexecute(f['case'],plan,supplied)
    qualified=f['basis'].receipt(f['fx_group_edge']);f['basis'].validate(qualified,n['elimination'].id)
    result=e.versions.current(n['fx-reassessment'].id).payload()['calculations']['pairs'][0]
    residual=dict(receivable=result['a_functional'],payable=result['b_functional'],signed_receivable_minus_payable=str(Decimal(result['a_functional'])-Decimal(result['b_functional'])),currency='EUR',unit_scale='million',material=True,disposition='UNRESOLVED',authority='No supported asymmetric ordinary-loan elimination; opening correction does not change closing carrying amounts')
    return f,dict(before=before,plan=plan,stale=stale,ledger=ledger,qualified_group_dependency=qualified,residual=residual)


def full_population_refusal(f):
    """Prove the retained guard independently after correcting the other conflict."""
    trial=copy.deepcopy(f);e=trial['session'];plan=s4.correct(trial);ledger=[]
    for key in plan['execution_order']:
        label=e.graph.nodes[key].logical_id
        try:
            c=s4.qualified_replacement(trial,key,source(trial,label))
            v=e.execute(key,observation,c,'Dependency rework: '+plan['new_version'])
            ledger.append(dict(label=label,version=v.version_id))
        except ValueError as error:
            if 'Full Group accounting omits or duplicates' not in str(error):raise
            return dict(status='REFUSED',error=str(error),other_conflict_correction=plan,completed_rework=ledger,
                        material_fx_residual='-2.00 EUR million',case_status=trial['case'].status,case_outcome=trial['case'].outcome)
    raise ValueError('Incomplete full population unexpectedly accepted')


def exact_once(f):
    e=f['session'];n=f['nodes']['fx-ENTITY-UK'];v=e.versions.current(n.id)
    event=dict(economic_id='fx-opening-correction',posting_scope=v.scope_id,period_id=v.period_id,period=n.period,currency='GBP',result_version=v.version_id,primary=[dict(owner=n.id,index=0)],witnesses=[],evidence='Reviewed current UK ordinary monetary remeasurement')
    context=dict(entity='GROUP-EUR',framework='IFRS',jurisdiction='NL',currency='EUR',period_start='2026-10-01',reporting_period='2026-10-31',scopes=e.cases.scopes.record(),period_registry=e.periods.record())
    selected,allocation=e.current_journals(context,[event])
    return dict(selected=selected,allocation=allocation,current_legal_version=v.version_id,
                excluded_superseded=[key for key,version in e.versions.versions.items() if version.node_id==n.id and e.versions.state(key)=='SUPERSEDED'],
                group_elimination='NOT_PRODUCED',translation='Native presentation population includes FX profit once; no new legal journal')


def transformations(f):
    e=f['session'];out=[];target=e.versions.current(f['nodes']['fx-reassessment'].id)
    for scope,field,account in [('ENTITY-UK','a_functional','ic loan'),('ENTITY-US','b_functional','fx payable')]:
        legal=e.versions.current(f['nodes']['fx-'+scope].id);translated=e.versions.current(f['nodes']['fx-translation-'+scope].id)
        out.append(f['basis'].translation(legal.version_id,translated.version_id,'fx',('calculations','pairs',0,field),('translation','tb',1,'balance'),('calculations','translation','translated_tb',account),s3.EVIDENCE,input_sign=1 if scope=='ENTITY-UK' else -1))
        out.append(f['basis'].intercompany_conversion(translated.version_id,target.version_id,'fx',('calculations','translation','translated_tb',account),s3.EVIDENCE))
    return out


def artifacts():
    f,r=run();e=f['session'];n=f['nodes']
    def current(label):return asdict(e.versions.current(n[label].id))
    return {'correction-path.json':dict(outcome='B',original={label:asdict(r['before'][label]) for label in ('fx-ENTITY-UK','fx-ENTITY-US','match-fx','fx-translation-ENTITY-UK','fx-translation-ENTITY-US','fx-reassessment')},
        reviewed_correction=e.sources[n['fx-ENTITY-UK'].id],fresh_reviewed_input_packs=[dict(node=x['node'],raw_sources=[asdict(v) for v in x['raw_sources']],inventory=x['prepared'].inventory,lineage=x['prepared'].lineage,reviewed_pack=asdict(x['reviewed_pack'])) for x in f['replacement_intakes']],
        current={label:current(label) for label in ('fx-ENTITY-UK','fx-ENTITY-US','match-fx','match-fx-current','fx-translation-ENTITY-UK','fx-translation-ENTITY-US','fx-reassessment','elimination','reporting','analytics','group')},
        supersession=e.versions.supersession,invalidation=r['plan'],stale_before_rework=r['stale'],selective_reexecution=r['ledger'],qualified_group_dependency=asdict(r['qualified_group_dependency']),residual=r['residual'],transformation_receipts=transformations(f),exact_once=exact_once(f),full_population_refusal=full_population_refusal(f),
        case=dict(status=f['case'].status,outcome=f['case'].outcome),public_answer=CAO().public(f['case']),
        remaining=['Material EUR2 million translated carrying residual has no supported asymmetric ordinary-loan disposition; reviewed closing-date legal/rate evidence capable of changing closing accounting has not been supplied',
                   'Bounded fx-operation TBs are not complete US/UK operation TBs; timing/clean/mismatch whole-operation per-row lineage and population integration remain required',
                   'Full Stage4 positive population, independent final QA and release gates remain outstanding'])}
