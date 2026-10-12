"""Fresh reviewed closing treasury/ledger evidence, unchanged native owners.

Synthetic treasury sheet is supplied before execution. No residual-dependent
rate selection and no change to the original conflict or opening control.
"""
import copy
from dataclasses import asdict
from decimal import Decimal
from orchestration.tests import stage4_correction_fixtures as prior, stage4_fixtures as s4, stage3_fixtures as s3
from orchestration.runtime import CAO
from orchestration.governed_plan import observation
from additional_cases import certify

CLOSE=dict(source_id='TREASURY-CLOSE-2026-10-31-03',valuation_date='2026-10-31',
    reviewed=True,synthetic=True,gbp_per_usd='0.90',eur_per_usd='0.90',eur_per_gbp='1.00',
    original_quote_date='2026-09-30',original_gbp_per_usd='0.80',
    provenance='Separately supplied controlled treasury closing quote sheet; stale September UK quote found in October export',
    uk_gl='18.00',uk_opening_book='16',uk_opening_operation=dict(cash='100',receivable='16',capital='116',memo='Separately retained opening operation ledger; closing quote changes no opening capital'),
    reporting_books=dict(a='18.00',b='18.00',provenance='Separately reviewed current EUR carrying ledger after native legal close and translation'))


def correction(f,evidence=None):
    evidence=copy.deepcopy(CLOSE if evidence is None else evidence)
    n=f['nodes']['fx-ENTITY-UK'];c=copy.deepcopy(f['session'].sources[n.id])
    for k in ('reviewer_signoff','source_population','qualified_scope_sources','qualified_input_snapshot'):c.pop(k,None)
    p=c['pairs'][0]
    from orchestration.closing_evidence import validate_quote_sheet
    validate_quote_sheet(evidence, n.period[1], {'eur_per_gbp': f['session'].sources[f['nodes']['fx-translation-ENTITY-UK'].id]['translation']['closing_rate'], 'eur_per_usd': f['session'].sources[f['nodes']['fx-translation-ENTITY-US'].id]['translation']['closing_rate']})
    if evidence.get('reviewed') is not True or evidence.get('synthetic') is not True or evidence['valuation_date']!=n.period[1]:
        raise ValueError('Separate reviewed closing-date evidence required')
    if evidence['source_id']==c['intercompany_transactions'][0]['source_id'] or not evidence.get('provenance'):
        raise ValueError('Fresh closing quote source provenance required')
    # GL/book values are separately supplied, never solved from a desired EUR result.
    p.update(rate_a=evidence['gbp_per_usd'],gl_a=evidence['uk_gl'],
        opening_book_a=evidence['uk_opening_book'],book_a=evidence['uk_opening_book'],
        rate_evidence=evidence['provenance'],version=evidence['source_id'],approved_version=evidence['source_id'])
    c['intercompany_transactions'][0].update(source_id=evidence['source_id']+'-UK-LEDGER',functional_amount=evidence['uk_gl'])
    c['correction_evidence']=dict(evidence,original_source_id='source-fx-ENTITY-UK',
        opening_operation=copy.deepcopy(evidence['uk_opening_operation']),reviewed_opening_book=evidence['uk_opening_book'],
        scope_id=n.scope_id,case_id=n.case_id,period_id=n.period_id,framework=n.framework,
        counterparty_scope='ENTITY-US',economic_id='fx',agreement_id='agreement-fx',book_entry_id='book-fx-ENTITY-UK',
        transaction_currency='USD',functional_currency='GBP',legal_side='receivable',reason='October closing export used an obsolete September quote')
    return certify('intercompany-accounting',c)


def reassessment(f):
    c=prior.reassessment_source(f);p=c['pairs'][0]
    legal=f['session'].sources[f['nodes']['fx-ENTITY-UK'].id]
    evidence=legal.get('correction_evidence')
    if evidence:
        books=evidence['reporting_books']
        p.update(rate_a=evidence['eur_per_usd'],rate_b=evidence['eur_per_usd'],
            opening_book_a=books['a'],book_a=books['a'],gl_a=books['a'],
            opening_book_b=books['b'],book_b=books['b'],gl_b=books['b'],
            rate_evidence=evidence['provenance'],opening_book_evidence=books['provenance'])
        c['reviewed_reporting_basis_ledger']=copy.deepcopy(books)
        c['closing_quote_evidence']=copy.deepcopy(evidence)
    return certify('intercompany-accounting',c)


def source(f,label):
    if label=='fx-reassessment':return reassessment(f)
    return prior.source(f,label)


def run(evidence=None):
    f=prior.initial();e=f['session'];n=f['nodes'];before={k:e.versions.current(v.id) for k,v in n.items()}
    fresh=s4.qualified_replacement(f,n['fx-ENTITY-UK'].id,correction(f,evidence))
    plan=CAO().correct(f['case'],n['fx-ENTITY-UK'].id,fresh,'Separately reviewed October closing treasury quote and legal ledger correction')
    stale={k:dict(version=v.version_id,state=e.versions.state(v.version_id)) for k,v in before.items()}
    preview=copy.deepcopy(f);pe=preview['session'];supplied={}
    for key in plan['execution_order']:
        node=pe.graph.nodes[key]
        blockers=[p for p in node.dependencies if pe.graph.nodes[p].status!='complete' or pe.versions.current(p).payload().get('unresolved_dependencies')]
        c=dict(scope_id=node.scope_id,period_id=node.period_id,evidence=list(s3.EVIDENCE),source_id='blocked-close-'+node.logical_id) if blockers else s4.qualified_replacement(preview,key,source(preview,node.logical_id))
        pe.execute(key,observation,c,'Dependency rework: '+plan['new_version']);supplied[key]=c
    f.setdefault('replacement_intakes',[]).extend(preview.get('replacement_intakes',[])[len(f.get('replacement_intakes',[])):])
    ledger=CAO().selective_reexecute(f['case'],plan,supplied)
    receipt=f['basis'].receipt(f['fx_group_edge']);f['basis'].validate(receipt,n['elimination'].id)
    pair=e.versions.current(n['fx-reassessment'].id).payload()['calculations']['pairs'][0]
    residual=dict(receivable=pair['a_functional'],payable=pair['b_functional'],signed_receivable_minus_payable=str(Decimal(pair['a_functional'])-Decimal(pair['b_functional'])),currency='EUR',unit_scale='million',
        disposition='NO_CARRYING_RESIDUAL' if Decimal(pair['a_functional'])==Decimal(pair['b_functional']) else 'UNRESOLVED')
    return f,dict(before=before,plan=plan,stale=stale,ledger=ledger,qualified_group_dependency=receipt,residual=residual)


def artifacts():
    f,r=run();e=f['session'];n=f['nodes']
    return dict(original={k:asdict(v) for k,v in r['before'].items()},
        reviewed_closing_source=e.sources[n['fx-ENTITY-UK'].id],
        current={k:asdict(e.versions.current(v.id)) for k,v in n.items()},supersession=e.versions.supersession,
        invalidation=r['plan'],stale_before_rework=r['stale'],selective_rework=r['ledger'],residual=r['residual'],
        transformations=prior.transformations(f),qualified_group_dependency=asdict(r['qualified_group_dependency']),
        exact_once=prior.exact_once(f),reviewed_replacements=[dict(node=x['node'],raw_sources=[asdict(v) for v in x['raw_sources']],inventory=x['prepared'].inventory,lineage=x['prepared'].lineage,reviewed_pack=asdict(x['reviewed_pack'])) for x in f['replacement_intakes']],
        case=dict(status=f['case'].status,outcome=f['case'].outcome),public_answer=CAO().public(f['case']),
        scope='Native closing-rate correction resolves bounded FX residual; full Group population/closure remains a separate required gate')
