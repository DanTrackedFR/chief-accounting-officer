"""Small real intake/accounting fixture; synthetic governance stays synthetic."""
import copy
from orchestration.intake import Intake, FixturePlanner, StructuredProposal, ReviewedInputPack, Binding, RawSource, Inventory
from orchestration.tests.intake_fixtures import SCOPE, metadata, numeric, cl
from orchestration.tests.diagnostic_fixtures import monthly_manufacturing
from orchestration.persistence.memory import applicability
COMPANY='company:memory-fixture'
UNKNOWN=dict(value=None,precision='unknown')
LEARNED=dict(value='2027-01-02',precision='exact')
FROM=dict(value='2026-12-01',precision='exact')
TO=dict(value='2026-12-31',precision='exact')

def build(objective='Document our recurring close control',value='NetSuite',semantic='EXTRACTED',approval=False,source_version='v1',memory=None):
    scope=copy.deepcopy(SCOPE)
    raws=[RawSource('ap-simple','invoice_export.csv','csv','supplier,amount\nS1,120\n',dict(metadata(),version=source_version)),
          RawSource('system-policy','Finance system.json','json',[dict(record_id='system',systems=value)],metadata())]
    if approval:
        raws.append(RawSource('governance','Documented decision.json','json',[dict(record_id='decision',memory_governance=__import__('json').dumps(dict(subject='finance',attribute='systems',value=value,status='APPROVED',scope_id=scope['entity'],framework=scope['framework'],period=[scope['period_start'],scope['reporting_period']],currency=scope['currency'],jurisdiction=scope['jurisdiction'],convention='DOCUMENTARY_ASSERTION'),sort_keys=True,separators=(',',':')))],metadata()))
    inv=Inventory(raws);fact=numeric(inv,'invoice-amount','supplier_cost','amount','ap-simple','amount')
    from orchestration.tests.intake_fixtures import cell
    field=cell(inv,'system-policy','systems')
    p=StructuredProposal(cl(objective,status='USER_STATED',confidence=1),cl('Closing balance'),cl('REPORTING'),bounded_owner=cl('accounts-payable'),facts=[fact],issues=[cl(dict(id='ap-node',owner='accounts-payable',family='supplier_cost',fact_ids=[fact.id],dependencies=[],required_fields=['amount']),fact.claim.evidence)],context_candidates={'systems':cl(value,[field],semantic)})
    intake=Intake(FixturePlanner(p))
    if memory is None:prepared=intake.prepare(objective,raws,[],scope)
    else:
        p.context_candidates={}
        p.missing_facts=[cl(dict(attribute='systems',owner='',kind='confirmation'),status='UNRESOLVED',confidence=0)]
        intake=Intake(FixturePlanner(p))
        prepared,refs=intake.prepare_with_memory(objective,raws,[],scope,**memory)
        assert not any(q.get('attribute')=='systems' for q in prepared.questions)
        assert prepared._current['systems']==value
    source=monthly_manufacturing()['facts']['supplier_cost']
    pack=ReviewedInputPack(dict(objective=objective,scope=prepared._current,facts={'supplier_cost':source}),[Binding(fact.id,'accounts-payable',('invoices','I1','amount'))])
    intake.execute(prepared,pack);return prepared.case

def capture(store,case,company=COMPANY,**overrides):
    m=store.memory();options=dict(category='systems_data',subject='finance',assertion='EXTRACTED',bundle_ids=sorted(case.governance.evidence_bundles),result_versions=sorted(k for k in case.governance.versions.versions if case.governance.versions.states[k]=='CURRENT'),dimensions=applicability(case,case.scope_id,[case.period_id]),effective_from=FROM,effective_to=TO,learned_at=LEARNED,expected_revision=m.audit(company)['revision'],material=True,reusable=True,decision=dict(previous_position=None,new_position='NetSuite',reason='Recurring controlled finance-system documentation',decision_date=UNKNOWN,status='proposed',implications=['Recurring close context']))
    options.update(overrides)
    index=next(i for i,c in enumerate(case.memory_candidates) if c['attribute']=='systems')
    return m.capture(company,case.id,case.id,index,**options)

def governance(r,target='DOCUMENTED',kind='SYNTHETIC',reason='Explicit bounded review of retained system evidence'):
    return dict(intent='EXPLICIT_MEMORY_TRANSITION',prior_status=r['status'],target_status=target,record_id=r['record_id'],applicability=r['applicability'],authority='TRUSTED_CALLER_ASSERTION',evidence_kind=kind,bundle_ids=r['source']['bundle_ids'],reason=reason,decision_date=UNKNOWN,approval_date=UNKNOWN,authenticated=False)

def correction(case,execute=True):
    """Actual reviewed replacement through native governed-plan intake seam."""
    from dataclasses import asdict
    import json
    from orchestration.runtime import CAO,digest
    from orchestration.intake import FactCandidate
    from orchestration.intake.governed import qualify_replacement
    from orchestration.tests.intake_fixtures import cell
    from orchestration.persistence.evidence import retain
    from production import case_fingerprint
    e=case.governance;n=next(iter(e.graph.nodes.values()));p=e.periods.get(n.period_id)
    c=copy.deepcopy(e.sources[n.id]);c.update(scope_id=n.scope_id,period_id=n.period_id)
    for k in ('reviewer_signoff','source_population','qualified_scope_sources','qualified_input_snapshot'):c.pop(k,None)
    dims=dict(scope_id=n.scope_id,entity=n.scope_id,framework=n.framework,jurisdiction=n.jurisdiction,currency=n.functional_currency or n.presentation_currency,unit='currency',period=n.period,period_id=n.period_id,calendar_id=p.calendar_id,period_role='CURRENT',comparator='actual')
    raws=[RawSource('correction-value','Reviewed AP.csv','csv','record_id,amount\nI1,120\n',dict(dims,controlled_export=True,version='v2')),
          RawSource('correction-workpaper','Reviewed AP workpaper.json','json',[dict(record_id=n.logical_id,reviewed_input=json.dumps(c,sort_keys=True,separators=(',',':')))],dict(dims,controlled_export=True,version='v2'))]
    inv=Inventory(raws);ref=cell(inv,'correction-value','amount')
    c['source_population']=[r.id for r in raws];c['qualified_scope_sources']=[dict(source_id=ex.source['id'],fingerprint=ex.source['fingerprint'],metadata=ex.source['metadata']) for ex in inv.extractions.values()]
    c['qualified_input_snapshot']=dict(source_id='correction-workpaper',fingerprint=inv.extractions['correction-workpaper'].source['fingerprint'])
    c['reviewer_signoff']=dict(reviewer='synthetic independent source reviewer',approved=True,case_fingerprint=case_fingerprint(c))
    f=FactCandidate('corrected-ap','supplier_cost','amount',cl('120',[ref],'EXTRACTED',.99),dims,'accounts-payable',confirmation_required=False,transformation='identity')
    proposal=StructuredProposal(cl(case.objective,status='USER_STATED',confidence=1),cl('Corrected reviewed AP source'),cl('REPORTING'),facts=[f],issues=[cl(dict(id='correction-AP',owner='accounts-payable',family='supplier_cost',scope_id=n.scope_id,period_id=n.period_id,fact_ids=[f.id],dependencies=[],required_fields=['amount']),[ref])])
    plan=dict(scopes=e.cases.scopes.record(),periods=e.periods.record(),cases=[dict(case_id=x.id,objective=x.objective,scope_id=x.scope_id,period_id=x.period_id,cycle=x.cycle,parent_id=x.parent_case_id,provenance=x.provenance) for x in e.cases.cases.values()],root_case=case.id,nodes=[row for row in e.graph.record() if row['id']==n.id],dependencies=[],sources={n.id:c})
    context=copy.deepcopy(e.context);context.update(scopes=e.cases.scopes.record(),period_registry=e.periods.record(),period_id=case.period_id)
    intake=Intake(FixturePlanner(proposal));prepared=intake.prepare(case.objective,raws,[],context)
    if not prepared.validation['accepted']:raise ValueError(prepared.validation)
    child=ReviewedInputPack(dict(objective=case.objective,node_id=n.id,source=c),[Binding(f.id,n.selected_skill,('invoices','I1','amount'),'current',n.scope_id,n.period_id,p.calendar_id)],scope_id=n.scope_id,period_id=n.period_id,calendar_id=p.calendar_id)
    pack=ReviewedInputPack(dict(objective=case.objective,scope=prepared._current,governed_plan=plan),[],scoped_packs=[child])
    source=qualify_replacement(intake,prepared,pack,case,n.id);retain(e,prepared,pack)
    if not execute:return dict(kind='CORRECT',node_id=n.id,source=source,reason='Qualified replacement export; same economics and new immutable evidence')
    return CAO().correct(case,n.id,source,'Qualified replacement export; same economics and new immutable evidence')
