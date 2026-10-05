"""Raw-ish sources + simulated model proposals, separate fixture-only review packs.

The user never supplies skill IDs or native schemas. Model fixtures operate on
extracted cells. Native reviewer scaffolds are injected only after preparation;
all mapped fields must equal independently certified workpaper inputs. No runtime
certification is created. This is bounded source-to-reviewed-workpaper integration,
not automated production workpaper certification.
"""
import copy
from orchestration.intake import *
from orchestration.intake.semantic import transform
from orchestration.planning import FACT_ADAPTERS

SCOPE=dict(entity='Synthetic Group',framework='IFRS',jurisdiction='NL',period_start='2026-12-01',reporting_period='2026-12-31',currency='USD',industry='manufacturing',materiality='1000')
OBJECTIVE='Our factory margins look terrible this month. Can you review the close and figure out what’s going on? I have attached the P&L, production/inventory report, payroll export, AP accruals, fixed asset register, FX report and close checklist.'

def metadata(**kwargs):return dict(entity=SCOPE['entity'],period=[SCOPE['period_start'],SCOPE['reporting_period']],currency='USD',comparator='actual',version='v1',source_system='Synthetic controlled export',controlled_export=True,as_of='2026-12-31',extracted_at='2027-01-02',**kwargs)

def factory_sources():
    return [
        RawSource('pnl','December management.csv','csv','metric,amount\nrevenue,40000\ncogs,11304\nunallocated_overhead,45000\ngross_profit,-16304\nfactory_labour,11000\n',metadata()),
        RawSource('production','final_final_v7.xlsx','normalized_workbook',{'sheets':[{'name':'Stock','rows':[{'record_id':'RM','closing_cost':'510'},{'record_id':'WIP','closing_cost':'11304'},{'record_id':'FG','closing_cost':'33912'}]},{'name':'Production','rows':[{'record_id':'order-1','normal_capacity':'200','actual_output':'100','fixed_overhead':'90000'}]}]},metadata()),
        RawSource('payroll','Pay export.csv','csv','employee_id,gross_pay,rate,units,expected_charge,factory_labour\nE01,10000,200,50,10800,10800\n',metadata()),
        RawSource('ap','Accrual export.tsv','tsv','supplier\tamount\tunits\tunit_price\nS1\t120\t12\t10\n',metadata()),
        RawSource('assets','Asset register.json','json',[{'record_id':'machine','opening_cost':'600000','period_units':'100','expected_depreciation':'90000'}],metadata()),
        RawSource('fx','FX export.csv','csv','record_id,foreign_amount,initial_rate,opening_book\ninventory-purchase,100,1.10,110\n',metadata()),
        RawSource('close','Close evidence.json','json',[{'record_id':'ap','duration':'2','finished_goods':'33912.00','interface_balance':'45726.00','control_threshold':'10','profit':'-16304.00','ppe':'600000'}],metadata()),
        RawSource('billing','Billing.csv','csv','product_id,ssp,delivered_units\ndelivery,40000,20\n',metadata()),
        RawSource('prior','November actual.csv','csv','metric,amount\ngross_profit,15000\n',dict(metadata(),period=['2026-11-01','2026-11-30'],comparator='prior_actual',as_of='2026-11-30')),
        RawSource('commentary','CEO notes.md','markdown','FX is the main reason margin is down.\n\nThis inventory should all be capitalized.',dict(metadata(),controlled_export=False)),
    ]

def cell(inventory,source,column,row=None,table=None):
    found=[f for f in inventory.fields().values() if f['source_id']==source and f['location'].get('column')==column and (row is None or f['location'].get('row')==row) and (table is None or f['location'].get('table')==table)]
    if len(found)!=1:raise AssertionError(('ambiguous fixture field',source,column,row,table))
    return found[0]['id']

def cl(value,evidence=(),status='INFERRED',confidence=.9):return Claim(value,status,confidence,'Deterministic simulated semantic interpretation',list(evidence))

def numeric(inventory,id,family,attribute,source,column,row=None,table=None,dimensions=None):
    e=cell(inventory,source,column,row,table);v=transform(inventory.fields()[e]['value'],'decimal')
    dims=dict(entity=SCOPE['entity'],period=[SCOPE['period_start'],SCOPE['reporting_period']],currency='USD',unit='currency',comparator='actual')
    if dimensions:dims.update(dimensions)
    return FactCandidate(id,family,attribute,cl(v,[e],'EXTRACTED',.99),dims,FACT_ADAPTERS[family][0],confirmation_required=False,transformation='decimal')

# These are simulated semantic mappings, not rules/keyword dispatch in production.
FACTORY_MAPPINGS=[
 ('asset-cost','machinery','opening_cost','assets','opening_cost',None,None,('assets','machine','opening_cost')),
 ('ap-amount','supplier_cost','amount','ap','amount',None,None,('invoices','I1','amount')),
 ('pay-rate','employee_cost','rate','payroll','rate',None,None,('benefits','salary','rate')),
 ('pay-units','employee_cost','units','payroll','units',None,None,('benefits','salary','units')),
 ('pay-charge','employee_cost','expected_charge','payroll','expected_charge',None,None,('benefits','salary','expected_charge')),
 ('fx-opening','currency_exposure','opening_book','fx','opening_book',None,None,('items','inventory-purchase','opening_book')),
 ('stock-rm','inventory','closing_cost','production','closing_cost',1,'Stock',('items','component','closing_cost')),
 ('revenue-ssp','customer_contract','ssp','billing','ssp',None,None,('obligations','delivery','ssp')),
 ('statement-cost','statement','opening_cost','close','ppe',None,None,('current_tb','PPE gross','balance')),
 ('stock-rec','reconciliation','closing_cost','close','finished_goods',None,None,('reconciliations','Finished goods','source_closing')),
 ('close-duration','close_calendar','duration','close','duration',None,None,('tasks','ap','duration')),
 ('interface-balance','interface','amount','close','interface_balance',None,None,('interfaces','interface-1','amount')),
 ('control-threshold','control','threshold','close','control_threshold',None,None,('control_rows','control-1','threshold')),
 ('profit-disclosure','disclosure','profit','close','profit',None,None,('requirements','requirement-1','amount')),
 ('analytic-cogs','analytics','cogs','pnl','amount',3,None,('accounts','cash-metric','amount')),
 ('prior-profit','analytics','prior_profit','prior','amount',None,None,('documents','diagnostic-prior','content','amount')),
]

def factory_proposal(sources):
    inv=Inventory(sources)
    p=StructuredProposal(cl(OBJECTIVE,status='USER_STATED',confidence=1),cl('Diagnostic close workpaper'),cl('DIAGNOSTIC_ANALYTICS'),supporting_modes=[cl('CLOSE_REVIEW'),cl('RECONCILIATION_INVESTIGATION')])
    p.facts=[numeric(inv,*m[:7],dimensions=dict(period=['2026-11-01','2026-11-30'],comparator='prior_actual') if m[0]=='prior-profit' else None) for m in FACTORY_MAPPINGS]
    for id,source in [('labour-export','payroll'),('labour-gl','pnl')]:
        p.facts.append(numeric(inv,id,'employee_cost','factory_labour',source,'factory_labour' if source=='payroll' else 'amount',None if source=='payroll' else 6))
    block=inv.extractions['commentary'].blocks[0]['field']
    p.hypotheses=[cl(dict(id='management-fx',description='FX is the main margin driver',tests=[dict(left_owner='foreign-currency',left_path=['monetary_fx_profit'],right_owner='management-accounting-analytics',right_path=['diagnostic','bridge','change'],factor=.5,operator='magnitude_above')]),[block])]
    families={s:'unknown' for s in inv.extractions}
    families.update(pnl='pnl',production='inventory_report',payroll='payroll_export',ap='ap_export',assets='fixed_asset_register',fx='fx_report',close='close_checklist',billing='revenue_report',prior='pnl',commentary='management_commentary')
    for id,family in families.items():
        p.classifications[id]=cl(dict(family=family,certainty='probable'),list(inv.extractions[id].fields)[:1])
    for family in dict.fromkeys(m[1] for m in FACTORY_MAPPINGS):
        owner=FACT_ADAPTERS[family][0]
        facts=[f for f in p.facts if f.family==family]
        if facts:p.issues.append(cl(dict(id=owner,owner=owner,family=family,fact_ids=[f.id for f in facts],dependencies=[],required_fields=[]),[e for f in facts for e in f.claim.evidence]))
    p.missing_facts=[cl(dict(attribute='framework',owner='',kind='blocking'),status='UNRESOLVED',confidence=0)]
    return p

def factory_review_pack(prepared):
    """Existing synthetic reviewer scaffolds qualify mapped inputs after intake.

    The parsed sources are NOT replaced by this scaffold. Changes in source cells
    fail exact binding, and unqualified workpaper changes fail assess_case.
    """
    from orchestration.tests.diagnostic_fixtures import diagnostic_manufacturing
    r=diagnostic_manufacturing();r['objective']=OBJECTIVE
    bindings=[]
    for m in FACTORY_MAPPINGS:
        bindings.append(Binding(m[0],FACT_ADAPTERS[m[1]][0],m[7],'comparator' if m[0]=='prior-profit' else 'current'))
    # Prior comparator uses existing independently controlled Analytics document.
    # Its evidence is separate from current accounting fact promotion.
    return ReviewedInputPack(r,bindings)

def factory():
    sources=factory_sources();planner=FixturePlanner(factory_proposal(sources));intake=Intake(planner)
    result=intake.prepare(OBJECTIVE,sources,[],SCOPE)
    return intake,result

def ap_control():
    objective='What is the closing AP balance?'
    raw=[RawSource('ap-simple','invoice_export.csv','csv','supplier,amount\nS1,120\n',metadata())]
    inv=Inventory(raw);f=numeric(inv,'invoice-amount','supplier_cost','amount','ap-simple','amount')
    p=StructuredProposal(cl(objective,status='USER_STATED',confidence=1),cl('Closing balance'),cl('REPORTING'),bounded_owner=cl('accounts-payable'),facts=[f],issues=[cl(dict(id='ap-node',owner='accounts-payable',family='supplier_cost',fact_ids=[f.id],dependencies=[],required_fields=['amount']),f.claim.evidence)])
    intake=Intake(FixturePlanner(p));prepared=intake.prepare(objective,raw,[],SCOPE)
    from orchestration.tests.diagnostic_fixtures import monthly_manufacturing
    reviewed=monthly_manufacturing()['facts']['supplier_cost']
    pack=ReviewedInputPack(dict(objective=objective,scope=SCOPE,facts={'supplier_cost':reviewed}),[Binding(f.id,'accounts-payable',('invoices','I1','amount'))])
    return intake,intake.execute(prepared,pack)

def contract_control(text=None):
    objective='Can you review this customer contract and tell me how we should account for it?'
    text=text or 'Parties: Synthetic Group and Customer A.\n\nTerm: 12 months.\n\nConsideration: USD 24000.\n\nBilling: monthly.\n\nServices: hosted platform access and onboarding.\n\nCancellation: customer may cancel on 30 days notice.\n\nVariable amounts: service credits for downtime. Refund rights are unspecified.'
    # Simulated semantic model annotations use each source block's content, not
    # a prewritten contract conclusion. New text remains new evidence.
    paragraphs=text.split('\n\n')
    sources=[RawSource('agreement','Customer agreement.docx','normalized_document',{'blocks':[dict(id='block-'+str(i),page=1,section='Commercial terms',text=t) for i,t in enumerate(paragraphs,1)]},dict(metadata(),controlled_export=False))]
    inv=Inventory(sources);facts=[]
    labels={'parties':'parties','term':'term','consideration':'consideration','billing':'billing_timing','services':'services','cancellation':'cancellation','variable amounts':'variable_amounts'}
    for i,b in enumerate(inv.extractions['agreement'].blocks):
        value=inv.fields()[b['field']]['value'];label=value.partition(':')[0].lower()
        attribute=labels.get(label,'contract_block_'+str(i))
        facts.append(FactCandidate('contract-'+str(i),'customer_contract',attribute,cl(value,[b['field']],'EXTRACTED',.99),candidate_owner='revenue-recognition'))
    evidence=[e for f in facts for e in f.claim.evidence]
    p=StructuredProposal(cl(objective,status='USER_STATED',confidence=1),cl('Accounting position'),cl('ACCOUNTING_DETERMINATION'),facts=facts,classifications={'agreement':cl(dict(family='contract',certainty='probable'),evidence)},issues=[cl(dict(id='revenue',owner='revenue-recognition',family='customer_contract',fact_ids=[f.id for f in facts],dependencies=[],required_fields=['refund_rights','performance_obligations']),evidence)],missing_facts=[cl(dict(attribute='refund_rights',owner='revenue-recognition',kind='blocking'),status='UNRESOLVED',confidence=0)])
    intake=Intake(FixturePlanner(p));prepared=intake.prepare(objective,sources,[],SCOPE)
    return intake,intake.execute(prepared)
