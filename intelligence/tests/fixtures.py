"""Unfamiliar synthetic inputs and explicitly synthetic independent review packs.

Approval creation is test-only. Production adapters never import this module.
"""
import base64
import copy
from dataclasses import asdict
from pathlib import Path
import io
import json
import zipfile
from docx import Document
from local_cao.tests.test_authored import context
from orchestration.intake import Claim,StructuredProposal,RawSource,Inventory,ReviewedInputPack,DocumentBinding,TextAssertion,FactCandidate,Binding
from orchestration.tests.fixtures import revenue,certify
from orchestration.periods import compatibility_period
from orchestration.intake.sources import fingerprint

COMPANY='synthetic-demo-001'
OBJECTIVE='How should we account for the Halcyon telemetry contract and service?'

def cl(v,e=(),status='INFERRED',confidence=.9):return Claim(v,status,confidence,'Synthetic controlled interpretation',list(e))

def proposal(objective,family,scope,refs):
    from orchestration.planning import FACT_ADAPTERS
    owner=FACT_ADAPTERS[family][0]
    p=StructuredProposal(cl(objective,status='USER_STATED',confidence=1),cl('Accounting determination'),cl('ACCOUNTING_DETERMINATION'))
    p.issues=[cl(dict(id='reviewed-owner',owner=owner,family=family,fact_ids=[],dependencies=[],required_fields=[],scope_id=scope['entity'],period_id=scope['period_id']),refs,'EXTRACTED',.99)]
    return p

def doc(scope,text=None,format='docx',role='contract',id='halcyon-agreement',version='v1',supersedes=None,**meta):
    text=text or 'Halcyon telemetry contract. Fixed price EUR 17350. Product and service are distinct. No refund terms supplied. Service term twelve months.'
    if format=='docx':
        d=Document();d.add_paragraph(text);b=io.BytesIO();d.save(b);raw=b.getvalue();stable=io.BytesIO()
        with zipfile.ZipFile(io.BytesIO(raw)) as src,zipfile.ZipFile(stable,'w',compression=zipfile.ZIP_DEFLATED) as dst:
            for name in sorted(src.namelist()):
                entry=zipfile.ZipInfo(name,(2026,1,1,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED;dst.writestr(entry,src.read(name))
        data=stable.getvalue()
    else:data=text.encode()
    p=compatibility_period(scope)
    m=dict(company_id=COMPANY,entity=scope['entity'],currency=scope['currency'],framework=scope['framework'],period=[scope['period_start'],scope['reporting_period']],scope_id=scope['entity'],period_id=p.period_id,calendar_id=p.calendar_id,period_role='CURRENT',relationship_id=None,**meta)
    out=dict(id=id,version=version,format=format,role=role,metadata=m,content_base64=base64.b64encode(data).decode())
    if supersedes:out['supersedes']=supersedes
    return out

def setup(api):
    api.workspace.mkdir(exist_ok=True);(api.workspace/'company-context.md').write_text(context())
    r=api.call(dict(contract_version='1.0',operation='initialize',company_id=COMPANY));assert r['ok'],r

def wire(op,**kw):return dict(contract_version='1.0',operation=op,company_id=COMPANY,**kw)

def revenue_evidence(api,cid,price="17350",replacement=False):
    with api._store() as store:case,_,_=store.load(COMPANY,cid)
    state=case._investigation;s=state['snapshot']['scope'];obs=state['documents'][-1]
    source=RawSource(**obs['raw_source']);inv=Inventory([source]);refs=list(inv.fields())
    p=proposal(OBJECTIVE,'customer_contract',s,refs)
    supplemental=RawSource('reviewed-price-export','Synthetic independent price export','json',[{'fixed':price}],dict(entity=s['entity'],scope_id=s['entity'],period=[s['period_start'],s['reporting_period']],period_id=s['period_id'],calendar_id=compatibility_period(s).calendar_id,period_role='CURRENT',relationship_id=None,currency=s['currency'],comparator='actual',controlled_export=True))
    sf=Inventory([supplemental]).fields();ref=next(iter(sf))
    p.facts=[FactCandidate('fixed-price','customer_contract','fixed',cl(price,[ref],'EXTRACTED',.99),dict(entity=s['entity'],scope_id=s['entity'],period=[s['period_start'],s['reporting_period']],period_id=s['period_id'],calendar_id=compatibility_period(s).calendar_id,period_role='CURRENT',currency=s['currency'],unit='currency',comparator='actual'),'revenue-recognition',confirmation_required=False,transformation='decimal')]
    p.issues[0].value['fact_ids']=['fixed-price']
    c=revenue();c.update(entity=s['entity'],scope_id=s['entity'],functional_currency=s['currency'],period_id=case.period_id)
    c['applicability_review']['entity_scope']='for_profit'
    c['price_components']['fixed']=price;c['obligations'][0]['ssp']='11000';c['obligations'][1]['ssp']='9000';c['obligations'][1]['progress']='0.25'
    c['balance_bridge'].update(opening_revenue='0',opening_contract_net='0',opening_receivable='0',billings='0',cash_received='0',opening_cost_asset='0');c['contract_costs']=[]
    c['qualified_source_documents']={source.id:dict(fingerprint=inv.extractions[source.id].source['fingerprint'],metadata=source.metadata)}
    assertion=TextAssertion(source.id,'revenue-recognition',r'Fixed price EUR (\d+)',('price_components','fixed'),'decimal',scope_id=s['entity'],period_id=s['period_id'],calendar_id=compatibility_period(s).calendar_id)
    c['source_semantic_controls']=dict(text_assertions=[asdict(assertion)],populations=[])
    c=certify('revenue-recognition',c);c.pop('reviewer_signoff',None)
    extra=[supplemental]
    if replacement:
        node=next(iter(case.graph.nodes))
        snapshot=RawSource('reviewed-native-input-v2','Synthetic complete independent source snapshot','json',[dict(record_id=node,reviewed_input=__import__('orchestration.intake.sources',fromlist=['canonical']).canonical(c))],dict(source.metadata))
        extra.append(snapshot);all_inv=Inventory([source]+extra)
        c['source_population']=list(all_inv.extractions)
        c['qualified_scope_sources']=[dict(source_id=k,fingerprint=v.source['fingerprint'],metadata=v.source['metadata']) for k,v in all_inv.extractions.items()]
        c['qualified_input_snapshot']=dict(source_id=snapshot.id,fingerprint=all_inv.extractions[snapshot.id].source['fingerprint'])
    c=certify('revenue-recognition',c)
    pack=ReviewedInputPack(dict(case_id=case.cycle,objective=OBJECTIVE,scope=s,facts={'customer_contract':c}),[Binding('fixed-price','revenue-recognition',('price_components','fixed'),scope_id=s['entity'],period_id=s['period_id'],calendar_id=compatibility_period(s).calendar_id)],documents=[DocumentBinding(source.id,'revenue-recognition',('qualified_source_documents',source.id),scope_id=s['entity'],period_id=s['period_id'],calendar_id=compatibility_period(s).calendar_id)],text_assertions=[assertion],scope_id=s['entity'],period_id=s['period_id'],calendar_id=compatibility_period(s).calendar_id)
    return json.loads(json.dumps(dict(proposal=p.record(),pack=asdict(pack),sources=[asdict(x) for x in extra])))
