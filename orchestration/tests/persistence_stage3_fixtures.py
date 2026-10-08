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

def build(objective='Document our recurring close control',value='NetSuite',semantic='EXTRACTED',approval=False):
    scope=copy.deepcopy(SCOPE)
    raws=[RawSource('ap-simple','invoice_export.csv','csv','supplier,amount\nS1,120\n',metadata()),
          RawSource('system-policy','Finance system.json','json',[dict(record_id='system',systems=value)],metadata())]
    if approval:
        raws.append(RawSource('governance','Documented decision.json','json',[dict(record_id='decision',memory_governance=__import__('json').dumps(dict(subject='finance',attribute='systems',value=value,status='APPROVED',scope_id=scope['entity'],framework=scope['framework'],period=[scope['period_start'],scope['reporting_period']],currency=scope['currency'],jurisdiction=scope['jurisdiction'],convention='DOCUMENTARY_ASSERTION'),sort_keys=True,separators=(',',':')))],metadata()))
    inv=Inventory(raws);fact=numeric(inv,'invoice-amount','supplier_cost','amount','ap-simple','amount')
    from orchestration.tests.intake_fixtures import cell
    field=cell(inv,'system-policy','systems')
    p=StructuredProposal(cl(objective,status='USER_STATED',confidence=1),cl('Closing balance'),cl('REPORTING'),bounded_owner=cl('accounts-payable'),facts=[fact],issues=[cl(dict(id='ap-node',owner='accounts-payable',family='supplier_cost',fact_ids=[fact.id],dependencies=[],required_fields=['amount']),fact.claim.evidence)],context_candidates={'systems':cl(value,[field],semantic)})
    intake=Intake(FixturePlanner(p));prepared=intake.prepare(objective,raws,[],scope)
    source=monthly_manufacturing()['facts']['supplier_cost']
    pack=ReviewedInputPack(dict(objective=objective,scope=scope,facts={'supplier_cost':source}),[Binding(fact.id,'accounts-payable',('invoices','I1','amount'))])
    intake.execute(prepared,pack);return prepared.case

def capture(store,case,company=COMPANY,**overrides):
    m=store.memory();options=dict(category='systems_data',subject='finance',assertion='EXTRACTED',bundle_ids=sorted(case.governance.evidence_bundles),result_versions=sorted(case.governance.versions.versions),dimensions=applicability(case,case.scope_id,[case.period_id]),effective_from=FROM,effective_to=TO,learned_at=LEARNED,expected_revision=m.audit(company)['revision'],material=True,reusable=True,decision=dict(previous_position=None,new_position='NetSuite',reason='Recurring controlled finance-system documentation',decision_date=UNKNOWN,status='proposed',implications=['Recurring close context']))
    options.update(overrides)
    index=next(i for i,c in enumerate(case.memory_candidates) if c['attribute']=='systems')
    return m.capture(company,case.id,case.id,index,**options)

def governance(r,target='DOCUMENTED',kind='SYNTHETIC',reason='Explicit bounded review of retained system evidence'):
    return dict(intent='EXPLICIT_MEMORY_TRANSITION',prior_status=r['status'],target_status=target,record_id=r['record_id'],applicability=r['applicability'],authority='TRUSTED_CALLER_ASSERTION',evidence_kind=kind,bundle_ids=r['source']['bundle_ids'],reason=reason,decision_date=UNKNOWN,approval_date=UNKNOWN,authenticated=False)
