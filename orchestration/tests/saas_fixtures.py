"""Controlled source pack and separately qualified synthetic owner workpapers.

No runtime approval creation. Sources look like company exports; semantic model
simulation maps actual extracted fields. Native qualification happens solely in
this regression scaffold, after intake, with explicit exact source bindings.
"""
import copy
from decimal import Decimal
from dataclasses import asdict
from orchestration.intake import *
from orchestration.tests.fixtures import completed
from orchestration.tests.intake_fixtures import cl,cell
from orchestration.intake.semantic import transform
from orchestration.planning import FACT_ADAPTERS
from cases import revenue,ecl
from additional_cases import fx,reporting,certify
from operational_cases import operational,approved
from governance_cases import case as governance_case,ready,refresh_release,document,row,source_index
from governance_accounting import digest

SCOPE=dict(entity='Synthetic Group',framework='IFRS',jurisdiction='NL',period_start='2026-12-01',reporting_period='2026-12-31',currency='USD',industry='software subscriptions',materiality='5')
OBJECTIVE='Can you review our month-end close? Revenue is up, but cash collection looks worse, deferred revenue moved a lot, and I am not sure whether the close is clean. I have attached the P&L, balance sheet, AR ageing, billing export, revenue schedule, FX report and reconciliation pack.'
PRIOR=['2026-11-01','2026-11-30']
OPENING=[('Cash','5000','asset'),('AR','910','asset'),('Allowance','-20','asset'),('Contract liability','-1000','liability'),('Opening equity','-4890','equity')]
CURRENT=[('Cash','5250','asset'),('AR','1520','asset'),('Allowance','-80','asset'),('Contract liability','-1300','liability'),('Unapplied cash','-50','liability'),('Opening equity','-4890','equity'),('Revenue','-500','revenue'),('Credit loss expense','60','expense'),('FX income','-10','expense'),('Manual accrual expense','25','expense'),('Accrued liabilities','-25','liability')]

def metadata(prior=False,controlled=True):
    return dict(entity=SCOPE['entity'],period=PRIOR if prior else [SCOPE['period_start'],SCOPE['reporting_period']],currency='USD',comparator='prior_actual' if prior else 'actual',version='controlled-v1',source_system='Synthetic accounting export',controlled_export=controlled,as_of='2026-11-30' if prior else '2026-12-31',extracted_at='2027-01-05')

def sources(clean=False):
    def raw(id,name,format,payload,prior=False,controlled=True):return RawSource(id,name,format,payload,metadata(prior,controlled))
    return [
        raw('tb','GL December final.csv','csv','account,balance,category\n'+''.join(','.join(r)+'\n' for r in CURRENT)),
        raw('prior_tb','November GL.csv','csv','account,balance,category\n'+''.join(','.join(r)+'\n' for r in OPENING),True),
        raw('pnl','Monthly P&L.csv','csv','metric,amount\nrevenue,500\ncredit_loss_expense,60\nfx_gain,10\nmanual_accrual,25\nprofit,425\n'),
        raw('balance_sheet','Balance sheet.json','json',[{'line':r[0],'amount':r[1]} for r in CURRENT if r[2] in ('asset','liability','equity')]),
        raw('billing','Invoice download.csv','csv','invoice_id,customer,book_amount,invoice_date,due_date,original_currency,original_amount,opening\nold-domestic,Alpha,800,2026-10-01,2026-11-01,USD,800,true\nold-foreign,Beta,110,2026-10-15,2026-11-15,EUR,100,true\ncurrent,Alpha,800,2026-12-01,2027-01-01,USD,800,false\n'),
        raw('receipts','Bank receipts.csv','csv','bank_id,customer,receipt,applied,unapplied,closing_cash\nBANK-DEC,Alpha,250,200,50,5250\n'),
        raw('ar_detail','Customer ledger.json','json',[dict(customer='Alpha',opening='800',closing='1400'),dict(customer='Beta',opening='110',closing='120')]),
        raw('ar_summary','AR control totals.csv','csv','closing_ar,gl_control_total\n1520,1520\n'),
        raw('ageing','aged debt final_v3.csv','csv','bucket,amount\ncurrent,800\n1_30,0\n31_60,720\n61_90,0\nover90,0\ntotal,'+('1520' if clean else '1515')+'\n'),
        raw('revenue','Revenue schedule.csv','csv','contract,price,progress,opening_revenue,opening_contract_net,opening_ar,billings,cash_applied,period_revenue,closing_contract_liability\nAlpha-platform,12000,0.125,1000,-1000,800,800,200,500,1300\n'),
        raw('contract','Alpha customer order.md','markdown','Customer: Alpha. Hosted API processing services form one distinct series of services received and consumed as supplied.\n\nTerm: 2026-10-01 to 2027-09-30. Fixed consideration USD 12000 for 12000 API processing units supplied over the term; no variable fees, refunds or cancellation rights.\n\nThe customer receives and consumes processing as supplied. Independently reviewed output progress is 1500 delivered units / 12000 contracted units = 0.125. October delivered 600, November 400 and December 500 units. Prior cumulative earned amount is USD 1000. No expiry, breakage or contract modification arises in this close.\n\nBilling records are enforceable billed rights. Revenue is recognised as service is supplied; payment does not establish performance.',controlled=False),
        raw('deferred','Contract balances.csv','csv','contract,opening_liability,billings,recognised,closing_liability,contract_asset\nAlpha-platform,1000,800,500,1300,0\n'),
        raw('loss_rates','Reviewed credit loss assumptions.csv','csv','bucket,exposure,loss_rate,effective_from,reviewed_on,as_of,source_version\ncurrent,800,0.01,2026-12-01,2026-12-31,2026-12-31,controlled-v1\n31_60,720,0.10,2026-12-01,2026-12-31,2026-12-31,controlled-v1\n'),
        raw('allowance','Allowance rollforward.csv','csv','opening,expense,writeoffs,recoveries,fx,closing\n20,60,0,0,0,80\n'),
        raw('fx','Receivable FX.csv','csv','invoice_id,foreign_currency,foreign_amount,opening_book,opening_rate,initial_rate,closing_rate,settled_foreign,closing_book,gain\nold-foreign,EUR,100,110,1.10,1.10,1.20,0,120,10\n'),
        raw('checklist','Close checklist.json','json',[dict(task='billing',duration='4',reconciliation_open_difference='0',state='complete',complete=True),dict(task='reclose',duration='1',state='complete')]),
        raw('rec_pack','Reconciliation review.json','json',[dict(account='AR',qualified_detail_balance='1520',open_difference='0' if clean else '5',reported_ageing='1520' if clean else '1515'),dict(account='Contract liability',qualified_detail_balance='-1300',open_difference='0'),dict(account='Allowance',qualified_detail_balance='-80',open_difference='0')]),
        raw('journals','Posted journals.csv','csv','journal_id,amount,effective_date,approved_at,posted_at,classification\nMANUAL-DEC,25,2026-12-31,2027-01-02,2027-01-02,estimate\n'),
        raw('prior','November management actual.csv','csv','metric,amount\nrevenue,400\nbillings,500\ncash_collections,450\ngross_ar,910\nallowance,20\ncontract_liability,1000\ncontract_asset,0\ncurrent,0\n1_30,910\n31_60,0\n61_90,0\nover90,0\n',True),
        raw('commentary','Management close comments.md','markdown','Collections only look worse because revenue grew.\n\nDeferred revenue is up because invoices were raised before the service was supplied.',controlled=False),
        raw('notes','Monthly note scope.json','json',[dict(topic='credit loss',closing_allowance='80',scope='Internal monthly risk and balance support; not an external filing')]),
    ]

# Explicit source field -> reviewed native field mappings; no implicit intake sums.
MAPPINGS=[
 ('rev-period-result','customer_contract','recognised_revenue','revenue','period_revenue',2,('__result__','period_revenue')),
 ('rev-price','customer_contract','consideration','revenue','price',2,('price_components','fixed')),
 ('rev-progress','customer_contract','progress','revenue','progress',2,('obligations','platform','progress')),
 ('rev-opening','customer_contract','opening_revenue','revenue','opening_revenue',2,('balance_bridge','opening_revenue')),
 ('rev-contract-opening','customer_contract','contract_opening','revenue','opening_contract_net',2,('balance_bridge','opening_contract_net')),
 ('rev-billings','customer_contract','contract_billings','revenue','billings',2,('balance_bridge','billings')),
 ('ar-opening-domestic','receivable_population','domestic_invoice','billing','book_amount',2,('invoices','old-domestic','amount')),
 ('ar-opening-foreign','receivable_population','foreign_invoice_book','billing','book_amount',3,('invoices','old-foreign','amount')),
 ('ar-billings','receivable_population','new_invoice','billing','book_amount',4,('invoices','current','amount')),
 ('ar-receipt','receivable_population','cash_receipt','receipts','receipt',2,('receipts','cash','amount')),
 ('ar-applied','receivable_population','cash_applied','receipts','applied',2,('receipts','cash','allocations','allocation','amount')),
 ('ar-gl','receivable_population','closing_ar','ar_summary','closing_ar',2,('gl_ar',)),
 ('ecl-current-exposure','credit_exposure','current_exposure','loss_rates','exposure',2,('credit','scenarios','base','terms','current','exposure')),
 ('ecl-aged-exposure','credit_exposure','aged_exposure','loss_rates','exposure',3,('credit','scenarios','base','terms','31_60','exposure')),
 ('ecl-current-rate','credit_exposure','current_loss_rate','loss_rates','loss_rate',2,('credit','scenarios','base','terms','current','loss_rate')),
 ('ecl-aged-rate','credit_exposure','aged_loss_rate','loss_rates','loss_rate',3,('credit','scenarios','base','terms','31_60','loss_rate')),
 ('ecl-opening','credit_exposure','opening_allowance','allowance','opening',2,('allowance_bridge','opening')),
 ('fx-opening','currency_exposure','opening_book','fx','opening_book',2,('items','old-foreign','opening_book')),
 ('fx-initial-rate','currency_exposure','initial_rate','fx','initial_rate',2,('items','old-foreign','initial_rate')),
 ('fx-closing-rate','currency_exposure','closing_rate','fx','closing_rate',2,('items','old-foreign','closing_rate')),
 ('rec-ar','reconciliation','ar_balance','rec_pack','qualified_detail_balance',1,('reconciliations','AR','source_closing')),
 ('rec-contract','reconciliation','contract_balance','rec_pack','qualified_detail_balance',2,('reconciliations','Contract liability','source_closing')),
 ('rec-allowance','reconciliation','allowance','rec_pack','qualified_detail_balance',3,('reconciliations','Allowance','source_closing')),
 ('close-task-complete','close_calendar','billing_complete','checklist','complete',1,('tasks','billing','complete')),
 ('close-duration','close_calendar','billing_duration','checklist','duration',1,('tasks','billing','duration')),
 ('close-journal','close_calendar','manual_accrual','journals','amount',2,('accruals','A1','received')),
 ('fs-revenue','statement','revenue','tb','balance',8,('current_tb','Revenue','balance')),
 ('fs-ar','statement','gross_ar','tb','balance',3,('current_tb','AR','balance')),
 ('fs-liability','statement','contract_liability','tb','balance',5,('current_tb','Contract liability','balance')),
 ('fs-allowance','statement','allowance','tb','balance',4,('current_tb','Allowance','balance')),
 ('disc-allowance','disclosure','allowance','notes','closing_allowance',1,('requirements','requirement-1','amount')),
 ('analytics-cash','analytics','closing_cash','receipts','closing_cash',2,('accounts','cash-metric','amount')),
]
for column,target in [('journal_id','id'),('effective_date','posting_date'),('approved_at','approval_date'),('posted_at','posted_at')]:
    MAPPINGS.append(('close-journal-'+column,'close_calendar','journal_'+column,'journals',column,2,('journals','MANUAL-DEC',target)))
for i,k in enumerate(['revenue','billings','cash_collections','gross_ar','allowance','contract_liability','contract_asset'],2):
    MAPPINGS.append(('prior-'+k,'analytics','prior_'+k,'prior','amount',i,('documents','balance-source','content','prior',k)))
for i,invoice in enumerate(['old-domestic','old-foreign','current'],2):
    for column,target in [('invoice_id','id'),('customer','customer'),('invoice_date','invoice_date'),('due_date','due_date'),('original_currency','currency'),('opening','opening')]:
        MAPPINGS.append(('ar-'+invoice+'-'+column,'receivable_population',column+'_'+invoice.replace('-','_'),'billing',column,i,('invoices',invoice,target)))
MAPPINGS.append(('ar-foreign-original','receivable_population','original_foreign_amount','billing','original_amount',3,('invoices','old-foreign','foreign_amount')))

def method(id):
    if id=='close-task-complete':return 'boolean'
    if id=='ecl-review-source_version' or id=='close-journal-journal_id':return 'identity'
    if id.startswith('close-journal-') and id.endswith(('effective_date','approved_at','posted_at')):return 'iso_date'
    if id.startswith('ecl-review-') or id.endswith(('invoice_date','due_date')):return 'iso_date'
    if id.startswith('ar-') and id.endswith('-opening'):return 'boolean'
    if id.endswith(('invoice_id','customer','original_currency')):return 'identity'
    return 'decimal'

for key in ['effective_from','reviewed_on','as_of','source_version']:
    MAPPINGS.append(('ecl-review-'+key,'credit_exposure','review_'+key,'loss_rates',key,2,('credit','loss_rate_review',key)))
for i,k in enumerate(['current','1_30','31_60','61_90','over90'],9):
    MAPPINGS.append(('prior-age-'+k,'analytics','prior_age_'+k,'prior','amount',i,('documents','balance-source','content','prior','ageing',k)))

def proposal(raw, objective=OBJECTIVE, bounded=None):
    inv=Inventory(raw)
    selected={bounded} if bounded else None
    if bounded=='accounts-receivable':selected.add('foreign-currency')
    if bounded=='financial-instruments-ecl':selected.update(['accounts-receivable','foreign-currency'])
    mode='REPORTING' if bounded else 'CLOSE_REVIEW'
    p=StructuredProposal(cl(objective,status='USER_STATED',confidence=1),cl('Month-end close review'),cl(mode))
    if bounded:p.bounded_owner=cl(bounded)
    else:p.secondary_modes=[cl('DIAGNOSTIC_ANALYTICS'),cl('RECONCILIATION_INVESTIGATION')];p.supporting_modes=[cl('ACCOUNTING_DETERMINATION'),cl('REPORTING')]
    for id,family,attribute,source,column,source_row,path in MAPPINGS:
        owner=FACT_ADAPTERS[family][0]
        if bounded and owner not in selected:continue
        evidence=cell(inv,source,column,source_row)
        dimensions=dict(entity=SCOPE['entity'],period=PRIOR if id.startswith('prior-') else [SCOPE['period_start'],SCOPE['reporting_period']],currency='USD',unit='currency',comparator='prior_actual' if id.startswith('prior-') else 'actual')
        p.facts.append(FactCandidate(id,family,attribute,cl(transform(inv.fields()[evidence]['value'],method(id)),[evidence],'EXTRACTED',.99),dimensions,owner,confirmation_required=False,transformation=method(id)))
    if not bounded:
        for id,family,attribute,source,column,source_row in [
            ('ageing-file-total','receivable_population','ageing_completeness','ageing','amount',7),
            ('ageing-gl-total','receivable_population','ageing_completeness','ar_summary','gl_control_total',2),
            ('rec-checklist','reconciliation','open_reconciliation_difference','checklist','reconciliation_open_difference',1),
            ('rec-pack-open','reconciliation','open_reconciliation_difference','rec_pack','open_difference',1)]:
            evidence=cell(inv,source,column,source_row)
            p.facts.append(FactCandidate(id,family,attribute,cl(transform(inv.fields()[evidence]['value'],method(id)),[evidence],'EXTRACTED',.99),dict(entity=SCOPE['entity'],period=[SCOPE['period_start'],SCOPE['reporting_period']],currency='USD',unit='currency',comparator='actual'),confirmation_required=False,transformation=method(id)))
        for i,b in enumerate(inv.extractions['contract'].blocks):
            value=inv.fields()[b['field']]['value'];p.facts.append(FactCandidate('contract-wording-'+str(i),'customer_contract','contract_terms_'+str(i),cl(value,[b['field']],'EXTRACTED',.99),candidate_owner='revenue-recognition'))
        evidence=inv.extractions['commentary'].blocks[0]['field']
        p.hypotheses=[cl(dict(id='collection-growth-explanation',description='Collections only look worse because revenue grew',tests=[dict(left_owner='accounts-receivable',left_path=['bank_receipts'],right_owner='management-accounting-analytics',right_path=['balance_diagnostics','cash_collections','prior'],factor=1,operator='magnitude_above')]),[evidence])]
        p.context_candidates={'currency':cl('USD',status='CONTEXT_DERIVED')}
    for family in dict.fromkeys(f.family for f in p.facts):
        owner=FACT_ADAPTERS[family][0];facts=[f for f in p.facts if f.family==family]
        dependencies=[]
        if not bounded or bounded in ('accounts-receivable','financial-instruments-ecl'):
            if owner=='accounts-receivable':dependencies=['foreign-currency']
            if owner=='financial-instruments-ecl':dependencies=['accounts-receivable']
            if owner in ('financial-statements','balance-sheet-reconciliations'):dependencies=['revenue-recognition','accounts-receivable','financial-instruments-ecl','foreign-currency']
            if owner=='disclosure-management':dependencies=['financial-statements','financial-instruments-ecl']
        p.issues.append(cl(dict(id=owner,owner=owner,family=family,fact_ids=[f.id for f in facts],dependencies=dependencies,required_fields=[]),[e for f in facts for e in f.claim.evidence]))
    return p

def scope_case(c):
    c['period_start']=SCOPE['period_start'];c['reporting_period']=SCOPE['reporting_period'];c['functional_currency']='USD';c['execution_date']='2027-01-05';c['applicability_review']['effective_period']=[SCOPE['period_start'],SCOPE['reporting_period']]
    return c

def reviewed_pack(prepared,objective=OBJECTIVE,bounded=None):
    """Qualification of controlled fixtures only, external to the runtime/intake."""
    owners={}
    f=scope_case(fx());f['currency'].update(functional='USD',ledger='USD',presentation='USD');f['translation']['enabled']=False
    f['items'][0].update(id='old-foreign',account='accounts receivable',foreign_currency='EUR',foreign_amount='100',initial_rate='1.10',closing_rate='1.20',opening_rate='1.10',opening_book='110',opening_route='carried_monetary',settled_foreign='0',settlement_rate='1.20',initial_date='2026-10-15',settlement_date=None)
    owners['foreign-currency']=certify('foreign-currency',f);fr=completed('foreign-currency',owners['foreign-currency'])
    r=scope_case(revenue());r['price_components']['fixed']='12000';r['obligations']=[r['obligations'][1]];r['obligations'][0].update(id='platform',ssp='12000',progress='0.125',distinct_memo='One distinct hosted API processing service series',timing_evidence='Reviewed contract and independently verified delivered processing-unit output schedule')
    r['balance_bridge'].update(opening_revenue='1000',opening_contract_net='-1000',opening_receivable='800',billings='800',cash_received='200',opening_cost_asset='0');r['contract_costs']=[]
    owners['revenue-recognition']=certify('revenue-recognition',r);rr=completed('revenue-recognition',owners['revenue-recognition'])
    a=scope_case(operational('accounts-receivable'))
    a['invoices']=[approved('old-domestic',customer='Alpha',amount='800',due_date='2026-11-01',invoice_date='2026-10-01',opening=True,entitlement_supported=True,offset='contract balance',disputed=False,currency='USD'),approved('old-foreign',customer='Beta',amount='110',due_date='2026-11-15',invoice_date='2026-10-15',opening=True,entitlement_supported=True,offset='contract balance',disputed=False,currency='EUR',foreign_amount='100',fx_import='fx-owner',fx_item='old-foreign'),approved('current',customer='Alpha',amount='800',due_date='2027-01-01',invoice_date='2026-12-01',opening=False,entitlement_supported=True,offset='contract balance',disputed=False,currency='USD')]
    a['imports']=[approved('fx-owner',package='foreign-currency',case=f,result=fr,mode='evidence_only')]
    a['receipts']=[approved('cash',customer='Alpha',amount='250',date='2026-12-31',allocations=[dict(id='allocation',invoice_id='old-domestic',amount='200')],bank_id='BANK-DEC',bank_confirmed=True,currency='USD')]
    a.update(credits=[],opening_customers=[dict(id='Alpha',balance='800'),dict(id='Beta',balance='110')],closing_customers=[approved('Alpha',balance='1400'),approved('Beta',balance='120')],opening_unapplied=[dict(id='Alpha',balance='0'),dict(id='Beta',balance='0')],bank_total='250',gl_ar='1520',gl_unapplied='50')
    a['collections']=[approved(id+'-collection',invoice_id=id,next_action='contact_customer',next_date='2027-01-06',dispute_evidence='No dispute or release evidence; follow up outstanding right',status='follow_up') for id in ('old-domestic','old-foreign')]
    a['controls'].update(population_count=3,population_amount='1710')
    owners['accounts-receivable']=certify('accounts-receivable',a);ar=completed('accounts-receivable',owners['accounts-receivable'])
    e=scope_case(ecl());e['instrument'].update(kind='trade_receivable',impairment_model='simplified');e['credit'].update(method='loss_rate',horizon='lifetime_default_events',assumptions_memo='Reviewed controlled lifetime loss-rate table effective December; no invented rates',scenarios=[dict(id='base',weight='1',terms=[dict(id='current',bucket='current',exposure='800',loss_rate='0.01'),dict(id='31_60',bucket='31_60',exposure='720',loss_rate='0.10')])])
    e['credit']['loss_rate_review']=dict(as_of='2026-12-31',effective_from='2026-12-01',reviewed_on='2026-12-31',source_version='controlled-v1',rows=copy.deepcopy(e['credit']['scenarios'][0]['terms']))
    e['measurement_schedule'].update(opening_gross='1520',eir='0',cash_flows='0',additions='0',writeoffs='0',fx='0',fair_value='1520');e['allowance_bridge'].update(opening='20',writeoffs='0',recoveries='0',fx='0')
    owners['financial-instruments-ecl']=certify('financial-instruments-ecl',e);er=completed('financial-instruments-ecl',owners['financial-instruments-ecl'])
    close=scope_case(operational('month-end-close'));close['journals'][0].update(id='MANUAL-DEC',approval_date='2027-01-02',posted_at='2027-01-02',lines=[dict(side='Dr',account='Manual accrual expense',amount='25'),dict(side='Cr',account='accrued liabilities',amount='25')])
    close['accruals'][0].update(received='25',posted='0',account='Manual accrual expense',gl_adjustment='25');close['controls'].update(population_amount='25');close['close'].update(approval_date='2027-01-04',reopened=True,reopen_authorization='Controlled authorised reopen for supported December service invoice',reclose_evidence='Independent reclose after the posted journal')
    owners['month-end-close']=certify('month-end-close',close);completed('month-end-close',owners['month-end-close'])
    fs=scope_case(reporting());
    def tb(rows):return [dict(id=id,balance=n,category=category,line=id,source_version='controlled-v1',classification_memo='Reviewed actual account class and original source line',cash_account=id=='Cash') for id,n,category in rows]
    fs['current_tb']=tb(CURRENT);fs['comparative_tb']=tb(OPENING);fs['comparative']['period_end']='2026-11-30'
    fs['equity_bridge']=[dict(id='owners',opening='4890',profit='425',oci='0',owner_transactions='0',retrospective_adjustments='0',other='0',closing='5315',memo='Reviewed owner results and balance movements')]
    fs['cash_flow'].update(start_amount='425',adjustments=[dict(id=id,amount=n,source='Controlled actual owner bridge',noncash_acquisition_fx_excluded=True,memo='Disjoint reviewed working-capital/noncash movement') for id,n in [('credit-loss','60'),('ar-ex-fx','-600'),('fx-profit','-10'),('contract-liability','300'),('unapplied','50'),('accrual','25')]],investing='0',financing='0',fx='0',opening='5000',closing='5250',classifications=[dict(id='bank-collections',date='2026-12-31',kind='customer_receipts',**{'class':'operating'},amount='250',memo='Complete actual bank receipts')]);fs['notes']=[dict(id='cash-note',target='cash',amount='5250',population_evidence='Controlled bank report',memo='Actual cash tie')]
    owners['financial-statements']=certify('financial-statements',fs);fsr=completed('financial-statements',owners['financial-statements'])
    rec=scope_case(operational('balance-sheet-reconciliations'));rec['trial_balance']=[dict(id=id,balance=n,category='balance_sheet' if cat in ('asset','liability','equity') else 'profit_loss') for id,n,cat in CURRENT];rec['inventory']=[dict(id=id) for id,n,cat in CURRENT if cat in ('asset','liability','equity')];rec['reconciliations']=[]
    old={id:Decimal(n) for id,n,cat in OPENING}
    for id,n,cat in CURRENT:
        if cat not in ('asset','liability','equity'):continue
        additions,reductions={'Cash':('250','0'),'AR':('810','200'),'Allowance':('0','60'),'Contract liability':('500','800'),'Unapplied cash':('0','50'),'Opening equity':('0','0'),'Accrued liabilities':('0','25')}[id];rec['reconciliations'].append(approved(id,opening=str(old.get(id,Decimal(0))),additions=additions,reductions=reductions,source_closing=n,gl_closing=n,source_ids=[id],gl_ids=[id],items=[],adjustments=[],threshold='0',relative_threshold='0',max_age_days=30,risk_tier='high',movement_memo='Independently qualified invoice/contract/allowance/bank/posting detail; supplied ageing export discrepancy remains an intake conflict'))
    rec['controls'].update(population_count=len(rec['inventory']),population_amount=str(sum(abs(Decimal(n)) for id,n,cat in CURRENT if cat in ('asset','liability','equity'))))
    owners['balance-sheet-reconciliations']=certify('balance-sheet-reconciliations',rec);completed('balance-sheet-reconciliations',owners['balance-sheet-reconciliations'])
    disc=scope_case(governance_case('disclosure-management'));disc['governance_method']['checked_on']=disc['execution_date'];disc['requirement_source'].update(checked_on=disc['execution_date'],effective_period=[disc['period_start'],disc['reporting_period']],applicable_topic_inventory=['TOPIC-03-008'])
    disc['imports']=[row(disc,'ecl-owner',package='financial-instruments-ecl',case=e,result=er,mode='evidence_only'),row(disc,'statements-owner',package='financial-statements',case=fs,result=fsr,mode='evidence_only')]
    disc['requirements'][0].update(amount='80',topic_id='TOPIC-03-008',owner_import='ecl-owner',requirement_key='monthly-allowance-support',owner_requirement=er['disclosures_impacted'][0],metric='allowance',result_path=['allowance'])
    disc['requirement_source']['records']=copy.deepcopy(disc['requirements']);disc['notes'][0].update(amount='80',prior_amount='20',narrative=er['conclusion'])
    next(d for d in disc['documents'] if d['id']=='statement')['content'].update(metric='allowance',amount='80')
    next(d for d in disc['documents'] if d['id']=='issued-prior')['content'].update(period=['2025-12-01','2025-12-31'],requirement_key='monthly-allowance-support',amount='20')
    disc['controls'].update(population_amount='80')
    # Rescope original synthetic source/review records, not source company facts.
    def rescope(value):
        if isinstance(value,dict):
            for k,v in value.items():
                if k in ('source_period','effective_period'):value[k]=[SCOPE['period_start'],SCOPE['reporting_period']]
                elif k=='checked_on':value[k]='2027-01-05'
                else:rescope(v)
        elif isinstance(value,list):
            for v in value:rescope(v)
    # Never rescope imported owner cases/results; they already have exact scope.
    for key in ('requirements','requirement_source','notes','documents','governance_method','accounting_policy'):rescope(disc[key])
    for d in disc['documents']:d['content_hash']=digest(d['content'])
    owners['disclosure-management']=ready('disclosure-management',c=refresh_release(disc));completed('disclosure-management',owners['disclosure-management'])
    ana=scope_case(governance_case('management-accounting-analytics'));ana['governance_method'].update(checked_on=ana['execution_date'],comparison_basis='prior_month_calendar_balance')
    for key in ('accounts','account_source','explanations','documents','reconciliations','governance_method','accounting_policy'):rescope(ana[key])
    ana['accounts'][0].update(amount='5250',management_amount='5250');ana['account_source']['records']=copy.deepcopy(ana['accounts']);ana['controls'].update(population_amount='5250')
    for d in ana['documents']:
        data=d['content']
        if d['id'] in ('current-books','prior-books'):
            amount='5250' if d['id']=='current-books' else '5000';data.update(period=[SCOPE['period_start'],SCOPE['reporting_period']] if d['id']=='current-books' else PRIOR,statutory_amount=amount,management_amount=amount,gross_amount=amount);data['records'][0]['amount']=amount
        if d['id']=='actual-drivers':data.update(period=[SCOPE['period_start'],SCOPE['reporting_period']],drivers=[dict(id='actual-bank-collections',amount='250')],driver_inventory=['actual-bank-collections'])
    ana['explanations'][0]['amount']='250'
    ana['imports']=[row(ana,pkg,package=pkg,case=owners[pkg],result=completed(pkg,owners[pkg]),mode='evidence_only') for pkg in ('revenue-recognition','accounts-receivable','financial-instruments-ecl','foreign-currency')]
    refs={}
    def ref(metric,pkg,path,amount):refs[metric]=dict(owner_import=pkg,result_path=path,amount=amount)
    for metric,path,amount in [('revenue',['period_revenue'],'500'),('contract_opening',['contract_bridge','opening'],'-1000'),('contract_closing',['contract_bridge','closing'],'-1300'),('contract_billings',['contract_bridge','billings'],'800')]:ref(metric,'revenue-recognition',path,amount)
    for metric,path,amount in [('billings','billed','800'),('credits','credits','0'),('cash_collections','bank_receipts','250'),('cash_applied','applied_cash_and_deposits','200'),('gross_ar','closing_ar','1520'),('opening_ar','opening_ar','910'),('unapplied_cash','unapplied_liability','50'),('ar_fx','fx_movement','10')]:ref(metric,'accounts-receivable',[path],amount)
    for b,amount in ar['calculations']['ageing'].items():ref('ageing_'+b,'accounts-receivable',['ageing',b],str(amount))
    ref('fx_profit','foreign-currency',['monetary_fx_profit'],'10');ref('allowance','financial-instruments-ecl',['allowance'],'80');ref('allowance_expense','financial-instruments-ecl',['expense'],'60')
    data=dict(entity=SCOPE['entity'],currency='USD',period=[SCOPE['period_start'],SCOPE['reporting_period']],prior_period=PRIOR,prior=dict(revenue='400',billings='500',cash_collections='450',gross_ar='910',allowance='20',contract_liability='1000',contract_asset='0',ageing=dict(current='0',**{'1_30':'910','31_60':'0','61_90':'0','over90':'0'})),prior_kind='actual',prior_posted_only=True,prior_version='controlled-v1',prior_approved_on='2026-11-30',refs=refs,dso=dict(method='snapshot_gross_ar_net_billings',numerator='gross_ar',denominator='net_billings',day_convention='actual_calendar_days',status='bounded_analytical_method'),management_hypothesis='collections_decline_only_revenue_growth',materiality='5')
    document(ana,'balance-source',data);ana['balance_diagnostics']={'doc':'balance-source'}
    for d in ana['documents']:d['content_hash']=digest(d['content'])
    owners['management-accounting-analytics']=ready('management-accounting-analytics',c=refresh_release(ana));completed('management-accounting-analytics',owners['management-accounting-analytics'])
    families={}
    for family,(pkg,_) in FACT_ADAPTERS.items():families.setdefault(pkg,family)
    handoffs=[]
    def link(producer,consumer,semantic,path,target,amount,sign=1,purpose='report'):
        handoffs.append(dict(producer=producer,consumer=consumer,semantic=semantic,metric_path=path,target_path=target,amount=amount,sign=sign,purpose=purpose,economic_id=semantic+'-'+consumer,qualification_evidence='Controlled synthetic exact owner-result to current source field review'))
    link('revenue-recognition','financial-statements','revenue',['period_revenue'],['current_tb','Revenue','balance'],'500',-1)
    for consumer,prefix in [('financial-statements','current_tb'),('balance-sheet-reconciliations','reconciliations')]:
        field='balance' if prefix=='current_tb' else 'source_closing'
        for pkg,semantic,path,account,amount,sign in [('accounts-receivable','ar_balance',['closing_ar'],'AR','1520',1),('financial-instruments-ecl','allowance',['allowance'],'Allowance','80',-1),('revenue-recognition','contract_balance',['contract_bridge','closing'],'Contract liability','-1300',1)]:link(pkg,consumer,semantic,path,[prefix,account,field],amount,sign)
    link('foreign-currency','financial-statements','monetary_fx',['monetary_fx_profit'],['current_tb','FX income','balance'],'10',-1)
    link('accounts-receivable','financial-instruments-ecl','credit_exposure',['closing_ar'],['measurement_schedule','opening_gross'],'1520',purpose='review')
    for bucket,exposure in [('current','800'),('31_60','720')]:link('accounts-receivable','financial-instruments-ecl','ar_ageing_'+bucket,['ageing',bucket],['credit','scenarios','base','terms',bucket,'exposure'],exposure,purpose='review')
    request=dict(case_id='synthetic-saas-close',objective=objective,scope=SCOPE,facts={families[pkg]:c for pkg,c in owners.items()},handoffs=handoffs,assumptions=['Controlled synthetic company exports and separate fixture-only reviewer qualification.'])
    # Exact event-level primary/witness allocation retains all native implications.
    mapping={'receivable':'AR','accounts receivable':'AR','contract clearing':'Contract liability','contract balance':'Contract liability','cash':'Cash','customer unapplied liability':'Unapplied cash','loss allowance':'Allowance','credit loss expense':'Credit loss expense','accrued liabilities':'Accrued liabilities','revenue':'Revenue'}
    native=[dict(owner=pkg,case_fingerprint=completed(pkg,owners[pkg])['case_fingerprint'],journals=completed(pkg,owners[pkg])['journal_entry_implications']) for pkg in [i['value']['owner'] for i in prepared.proposal['issues']]]
    def jr(owner,index):return dict(owner=owner,index=index)
    # Revenue: recognition,billing,applied receipt. AR: invoice,FX,bank receipt.
    ownership=[dict(economic_id='recognised-platform-service',primary=[jr('revenue-recognition',0)],witnesses=[],evidence='Contract satisfaction and revenue schedule'),dict(economic_id='current-enforceable-billing',primary=[jr('accounts-receivable',0)],witnesses=[[jr('revenue-recognition',1)]],evidence='Current invoice right and contract-specific billing bridge'),dict(economic_id='receivable-remeasurement',primary=[jr('foreign-currency',0)],witnesses=[[jr('accounts-receivable',1)]],evidence='Original foreign position and FX owner adjustment')]
    # The AR receipt includes applied cash200 plus unapplied50. Revenue only
    # covers applied200, so split witnesses cannot be netted or discarded. Its
    # journal and AR journal need line-grain allocation (below) rather than false
    # whole-journal equivalence. This is supplied exact native line ownership.
    def line(owner,index,position,amount):return dict(owner=owner,index=index,line=position,amount=amount)
    ownership.extend([
        dict(economic_id='cash-applied-old-invoice',primary=[line('accounts-receivable',2,0,'200'),line('accounts-receivable',2,1,'200')],witnesses=[[jr('revenue-recognition',2)]],evidence='BANK-DEC remittance applied to original Alpha right'),
        dict(economic_id='unapplied-customer-cash',primary=[line('accounts-receivable',2,0,'50'),line('accounts-receivable',2,2,'50')],witnesses=[],evidence='BANK-DEC residual remains identified customer liability'),
        dict(economic_id='lifetime-allowance-movement',primary=[jr('financial-instruments-ecl',0)],witnesses=[],evidence='Reviewed credit-loss assumption and owner allowance bridge'),
        dict(economic_id='late-december-service-accrual',primary=[jr('month-end-close',0)],witnesses=[],evidence='MANUAL-DEC approved journal linked to A1 service receipt'),
    ])
    request['journal_account_mapping']=mapping
    request['journal_ownership']=ownership
    request['journal_pack_review']=dict(preparer='Synthetic close preparer',reviewer='Synthetic independent journal integration reviewer',approved=True,payload_fingerprint=__import__('orchestration.runtime',fromlist=['digest']).digest(dict(mapping=mapping,native_owner_journals=native,journal_ownership=ownership)))
    if bounded:
        selected={bounded}
        if bounded=='accounts-receivable':selected.add('foreign-currency')
        if bounded=='financial-instruments-ecl':selected.update(['accounts-receivable','foreign-currency'])
        request['facts']={families[pkg]:c for pkg,c in owners.items() if pkg in selected};request['handoffs']=[]
        for key in ('journal_account_mapping','journal_ownership','journal_pack_review'):request.pop(key,None)
    bindings=[Binding(id,FACT_ADAPTERS[family][0],path[1:] if path[0]=='__result__' else path,'owner_result' if path[0]=='__result__' else 'comparator' if id.startswith('prior-') else 'current') for id,family,attribute,source,column,source_row,path in MAPPINGS if not bounded or FACT_ADAPTERS[family][0] in selected]
    populations=[PopulationBinding('journals','journal_id','month-end-close',('journals',)),PopulationBinding('billing','invoice_id','accounts-receivable',('invoices',)),PopulationBinding('receipts','bank_id','accounts-receivable',('receipts',),'bank_id')]
    if bounded:populations=[row for row in populations if row.owner in selected]
    return ReviewedInputPack(request,bindings,populations)

def flagship(clean=False):
    raw=sources(clean);engine=Intake(FixturePlanner(proposal(raw)));p=engine.prepare(OBJECTIVE,raw,[],SCOPE)
    pack=reviewed_pack(p);return engine,p,pack


def narrow(owner,objective):
    raw=sources(clean=True);engine=Intake(FixturePlanner(proposal(raw,objective,bounded=owner)))
    prepared=engine.prepare(objective,raw,[],SCOPE)
    return engine,prepared,reviewed_pack(prepared,objective,bounded=owner)
