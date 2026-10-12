"""Two separately certified US Revenue inputs in September and October."""
import copy
from orchestration.tests.stage2_fixtures import build
from orchestration.intake import *
from orchestration.tests.intake_fixtures import cl,cell
from cases import finalize

OBJECTIVE='Review revenue for September and October.'

def fixture():
    f=build();e=f['coordinator'];n=f['nodes']['US-SEP']
    scope=dict(entity=n.scope_id,framework=n.framework,jurisdiction=n.jurisdiction,currency=n.functional_currency,period_start=n.period[0],reporting_period=n.period[1],period_id=n.period_id,scopes=e.cases.scopes.record(),period_registry=e.periods.record())
    sources=[];natives=[];bindings=[];children=[]
    p=StructuredProposal(cl(OBJECTIVE,status='USER_STATED',confidence=1),cl('Period qualified revenue review'),cl('CLOSE_REVIEW'))
    for label in ('US-SEP','US-OCT'):
        node=f['nodes'][label];period=e.periods.get(node.period_id)
        dims=dict(scope_id=node.scope_id,entity=node.scope_id,framework=node.framework,jurisdiction=node.jurisdiction,currency=node.functional_currency,unit='currency',period=node.period,period_id=node.period_id,calendar_id=period.calendar_id,period_role='CURRENT',comparator='actual')
        meta=dict(dims,controlled_export=True,version='v1')
        raw=RawSource('source-'+label,'revenue.csv','csv','record_id,recognised_revenue\ncontract-1,800\n',meta);sources.append(raw)
        inventory=Inventory([raw]);ref=cell(inventory,raw.id,'recognised_revenue')
        fact=FactCandidate('fact-'+label,'customer_contract','recognised_revenue',cl('800',[ref],'EXTRACTED',.99),dims,'revenue-recognition',economic_id='contract-1',confirmation_required=False,transformation='decimal')
        p.facts.append(fact);p.issues.append(cl(dict(id='issue-'+label,owner='revenue-recognition',family='customer_contract',scope_id=node.scope_id,period_id=node.period_id,fact_ids=[fact.id],dependencies=[],required_fields=['recognised_revenue']),[ref]))
        native=copy.deepcopy(f['sources'][node.id]);actual=inventory.extractions[raw.id].source
        native['source_population']=[raw.id];native['qualified_scope_sources']=[dict(source_id=raw.id,fingerprint=actual['fingerprint'],metadata=actual['metadata'])]
        native=finalize('revenue-recognition',native);natives.append(native)
        binding=Binding(fact.id,'revenue-recognition',('period_revenue',),'owner_result',node.scope_id,node.period_id,period.calendar_id);bindings.append(binding)
        children.append(ReviewedInputPack(dict(objective=OBJECTIVE,facts=dict(customer_contract=native)),[binding],scope_id=node.scope_id,period_id=node.period_id,calendar_id=period.calendar_id))
    request=dict(objective=OBJECTIVE,scope=scope,facts=dict(customer_contract=natives))
    pack=ReviewedInputPack(request,bindings,scoped_packs=children)
    return sources,p,scope,pack
