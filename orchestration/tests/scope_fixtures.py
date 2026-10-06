"""Independent synthetic source populations and fixture-only owner certification."""
import copy
from dataclasses import asdict
from orchestration.scopes import Scope,execution_scopes,execution_identity
from orchestration.runtime import digest,CAO
from orchestration.intake import *
from orchestration.tests.intake_fixtures import cl,cell
from orchestration.tests.fixtures import revenue,certify,completed

OBJECTIVE='Review revenue for our Netherlands, US and UK businesses and give me a Group summary.'
ROWS=[Scope('GROUP-EUR','GROUP','European reporting Group',jurisdiction='NL',framework='IFRS',presentation_currency='EUR',provenance=('reviewed-group-profile',)),
    Scope('ENTITY-NL','LEGAL_ENTITY','Netherlands business','NL-001','GROUP-EUR','NL','IFRS','EUR',provenance=('reviewed-NL-profile',)),
    Scope('ENTITY-US','LEGAL_ENTITY','US business','US-001','GROUP-EUR','US','US_GAAP','USD',provenance=('reviewed-US-profile',)),
    Scope('ENTITY-UK','LEGAL_ENTITY','UK business','UK-001','GROUP-EUR','UK','UK_GAAP','GBP',provenance=('reviewed-UK-profile',))]
SCOPE=dict(entity='GROUP-EUR',framework='IFRS',jurisdiction='NL',currency='EUR',period_start='2026-01-01',reporting_period='2026-12-31',scopes=[s.record() for s in ROWS])


def source_pack():
    out=[]
    for key,s in execution_scopes(SCOPE).items():
        metadata=dict(scope_id=key,entity=key,period=[s['period_start'],s['reporting_period']],currency=s['currency'],framework=s['framework'],jurisdiction=s['jurisdiction'],comparator='actual',controlled_export=True,version='v1')
        if s['scope_type']=='LEGAL_ENTITY':
            out.append(RawSource('source-'+key,'revenue-export.csv','csv','record_id,recognised_revenue\ncontract-1,800\n',metadata))
        else:out.append(RawSource('source-'+key,'reporting-profile.csv','csv','reporting_currency\nEUR\n',metadata))
    return out


def semantic_proposal(sources):
    inv=Inventory(sources)
    p=StructuredProposal(cl(OBJECTIVE,status='USER_STATED',confidence=1),cl('Scoped Group revenue review'),cl('CLOSE_REVIEW'))
    for s in ROWS[1:]:
        e=cell(inv,'source-'+s.scope_id,'recognised_revenue')
        dims=dict(scope_id=s.scope_id,entity=s.scope_id,framework=s.framework,jurisdiction=s.jurisdiction,currency=s.functional_currency,unit='currency',period=['2026-01-01','2026-12-31'],comparator='actual')
        f=FactCandidate('fact-'+s.scope_id,'customer_contract','recognised_revenue',cl('800',[e],'EXTRACTED',.99),dims,'revenue-recognition',economic_id='contract-1',confirmation_required=False,transformation='decimal')
        p.facts.append(f)
        p.issues.append(cl(dict(id='revenue-'+s.scope_id,scope_id=s.scope_id,owner='revenue-recognition',family='customer_contract',fact_ids=[f.id],dependencies=[],required_fields=['recognised_revenue']),[e]))
    return p


def native_cases():
    out=[]
    for s in ROWS[1:]:
        native=revenue(s.framework);native.update(scope_id=s.scope_id,entity=s.scope_id,jurisdiction=s.jurisdiction,functional_currency=s.functional_currency,
            case_id='revenue-'+s.scope_id,posting_scope_id=s.scope_id,journal_layer='LEGAL_ENTITY')
        native['evidence']=['independently reviewed source-'+s.scope_id]
        native['obligations'][0]['economic_id']='contract-1'
        native['source_population']=['source-'+s.scope_id]
        actual=Inventory(source_pack()).extractions['source-'+s.scope_id].source
        native['qualified_scope_sources']=[dict(source_id=actual['id'],fingerprint=actual['fingerprint'],metadata=actual['metadata'])]
        native['balance_bridge']['opening_revenue']='0'
        native['balance_bridge']['billings']={'ENTITY-NL':'400','ENTITY-US':'500','ENTITY-UK':'600'}[s.scope_id]
        from cases import finalize
        native=finalize('revenue-recognition',native);completed('revenue-recognition',native)
        out.append(native)
    return out


def reviewed_pack():
    cases=native_cases();scope=execution_scopes(SCOPE);receipts=[]
    target=execution_identity('orchestration-group-observation',scope['GROUP-EUR'])
    for c in cases:
        s=scope[c['entity']];result=completed('revenue-recognition',c);key=execution_identity('revenue-recognition',s)
        receipts.append(dict(source_owner='revenue-recognition',source_node=key,source_scope=s['scope_id'],target_node=target,target_scope='GROUP-EUR',
            semantic_metric='period_revenue',framework=s['framework'],currency=s['currency'],functional_currency=s['functional_currency'],presentation_currency=s['presentation_currency'],
            result_fingerprint=digest(result),exact_case_fingerprint=result['case_fingerprint'],currentness='CURRENT',economic_identity=[s['scope_id'],key,'period_revenue',result['case_fingerprint']],result=result,evidence=['independent current local Revenue workpaper'],consumption_type='LOCAL_RESULT_OBSERVATION'))
    consumer=dict(qualified_context_fingerprint=Inventory(source_pack()).extractions['source-GROUP-EUR'].source['fingerprint'],scope_id='GROUP-EUR',expected_producers=[r['source_node'] for r in receipts],receipts=receipts,
        context_source=dict(source_id='source-GROUP-EUR',scope_id='GROUP-EUR',framework='IFRS',currency='EUR',evidence=['reviewed-group-profile']))
    request=dict(case_id='stage1-scoped-revenue',objective=OBJECTIVE,scope=copy.deepcopy(SCOPE),facts=dict(customer_contract=cases),group_consumer=consumer)
    bindings=[Binding('fact-'+s.scope_id,'revenue-recognition',('period_revenue',),'owner_result',s.scope_id) for s in ROWS[1:]]
    children=[ReviewedInputPack(dict(objective=OBJECTIVE,facts=dict(customer_contract=copy.deepcopy(native))),[bindings[i]],scope_id=native['entity']) for i,native in enumerate(cases)]
    return ReviewedInputPack(request,bindings,scoped_packs=children)


def run():
    sources=source_pack();engine=Intake(FixturePlanner(semantic_proposal(sources)));prepared=engine.prepare(OBJECTIVE,sources,[],SCOPE)
    return engine.execute(prepared,reviewed_pack())
