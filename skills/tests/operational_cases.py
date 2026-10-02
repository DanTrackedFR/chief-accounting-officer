"""Entirely synthetic source populations and approvals for regression only."""
from cases import base
from additional_cases import certify

PACKAGES=['month-end-close','balance-sheet-reconciliations','accounts-receivable','accounts-payable','fixed-assets','intercompany-accounting']

def approved(id,**kw):
    return dict(id=id,owner='synthetic owner',reviewer='synthetic independent reviewer',evidence='synthetic source',approved=True,
                approval_date='2026-12-31',version='v1',approved_version='v1',**kw)

def handoffs(c,targets):
    return {k:dict(target=v,entity=c['entity'],framework=c['framework'],reporting_period=c['reporting_period'],evidence='synthetic specialist memo',reviewer='synthetic technical reviewer',resolved=True,scope_memo='Reviewed ordinary supported scope') for k,v in targets.items()}

def operational(package,fw='IFRS'):
    c=base(package,fw);c['functional_currency']='EUR';c['execution_date']='2027-01-05'
    c['controls']=dict(source_version='v1',as_of=c['reporting_period'],population_count=0,population_amount='0',owner='synthetic source owner',reviewer='synthetic completeness reviewer',complete=True,policy_version='v1',cutoff_memo='Synthetic complete period end independent source')
    if package=='month-end-close':
        c['calendar']={'working_dates':['2026-12-23','2026-12-24','2026-12-25','2026-12-28','2026-12-29','2026-12-30','2026-12-31'],'timezone':'UTC','holiday_review':'Synthetic local operating calendar; no real holiday assertion'}
        c.update(tasks=[approved('ap',predecessors=[],duration='2',due_day='2',complete=True,timezone='UTC',unresolved_count=0),approved('aprec',predecessors=['ap'],duration='2',due_day='4',complete=True,timezone='UTC',unresolved_count=0),approved('billing',predecessors=[],duration='4',due_day='4',complete=True,timezone='UTC',unresolved_count=0),approved('group',predecessors=['aprec','billing'],duration='1',due_day='5',complete=True,timezone='UTC',unresolved_count=0),approved('statements',predecessors=['group'],duration='1',due_day='6',complete=True,timezone='UTC',unresolved_count=0)],
          journals=[approved('J1',**{'class':'estimate'},source_ids=['A1'],posting_date='2026-12-31',posted_at='2026-12-31',posting_id='P1',lines=[{'side':'Dr','account':'expense','amount':'25000'},{'side':'Cr','account':'accrued liabilities','amount':'25000'}],rule_version='v1',cutoff_supported=True,posted=True,reversal_plan='January monitored invoice')],
          accruals=[approved('A1',received='75000',posted='50000',opening_accrual='0',recognition_supported=True,account='expense',reversal_plan='January monitored invoice',gl_adjustment='25000')],
          close=approved('lock',state='locked',account_certifications_complete=True,exceptions=[],reopened=False,reopen_authorization='',reclose_evidence='',journal_population_reconciled=True,recognition_error_review='No prior errors',recognition_errors_resolved=True))
        for t in c['tasks']:
            t['actual_finish_day']=t['due_day'];t['actual_start_day']=str(int(t['due_day'])-int(t['duration']))
        c['controls'].update(population_count=1,population_amount='25000')
    elif package=='balance-sheet-reconciliations':
        c.update(trial_balance=[{'id':'prepaid','balance':'130000'},{'id':'equity','balance':'-130000'}],inventory=[{'id':'prepaid'}],reconciliations=[approved('prepaid',opening='100000',additions='40000',reductions='15000',source_closing='125000',gl_closing='130000',source_ids=['S1'],gl_ids=['S1'],items=[],adjustments=[approved('fix',amount='-5000',offset='expense',error_vs_estimate_memo='Supported duplicated asset correction',posted=True,source_id='S1')],threshold='100',relative_threshold='0.01',max_age_days=30,risk_tier='high',movement_memo='Approved additions/consumption')])
        for t in c['trial_balance']:t['category']='balance_sheet'
        c['trial_balance'].append({'id':'expense','balance':'0','category':'profit_loss'})
        c['inventory'].append({'id':'equity'})
        c['reconciliations'].append(approved('equity',opening='-130000',additions='0',reductions='0',source_closing='-130000',gl_closing='-130000',source_ids=['EQ'],gl_ids=['EQ'],items=[],adjustments=[],threshold='100',relative_threshold='0.01',max_age_days=30,risk_tier='high',movement_memo='Supported opening equity'))
        c['controls'].update(population_count=2,population_amount='260000')
    elif package=='accounts-receivable':
        c.update(invoices=[approved('opening',customer='C1',amount='150',due_date='2026-12-31',invoice_date='2025-12-01',opening=True,entitlement_supported=True,offset='contract balance',disputed=False,currency='EUR'),approved('new',customer='C1',amount='100',due_date='2027-01-31',invoice_date='2026-12-31',opening=False,entitlement_supported=True,offset='contract balance',disputed=False,currency='EUR')],receipts=[approved('cash',customer='C1',amount='200',date='2026-12-31',allocations=[{'id':'alloc','invoice_id':'opening','amount':'120'}],bank_id='BANK1',bank_confirmed=True,currency='EUR')],credits=[approved('credit',invoice_id='new',amount='10',date='2026-12-31',offset='contract balance',reason='billing_error',revenue_reviewed=True)],opening_customers=[{'id':'C1','balance':'150'}],closing_customers=[approved('C1',balance='120')],gl_ar='120',gl_unapplied='80',collections=[],bank_total='200')
        c['opening_unapplied']=[{'id':'C1','balance':'0'}];c['liability_applications']=[];c['refunds']=[];c['refund_bank_total']='0';c['handoffs']=handoffs(c,{'revenue':'Revenue Recognition','ecl':'ECL'});c['controls'].update(population_count=2,population_amount='250')
    elif package=='accounts-payable':
        c.update(invoices=[approved('I1',supplier='S1',invoice_number='N1',amount='120',units='12',unit_price='10',po_amount='120',received_amount='120',received_date='2026-12-31',invoice_date='2026-12-31',account='expense',match_approved=True,bank_master_review='Independent bank master',accrual_id='',currency='EUR')],accruals=[approved('A1',supplier='S1',units='12',rate='800',received_supported=True,received_date='2026-12-31',invoiced_received='0',opening_accrual='0',account='professional services expense',reversal_date='2027-01-01',clearing_plan='Linked subsequent invoice review',subsequent_actual='10400',backtest_memo='800 relates to supported January services',gl_closing='9600')],payments=[approved('P1',supplier='S1',amount='100',date='2026-12-31',bank_id='B1',bank_confirmed=True,bank_master_approved=True,payment_preparer='synthetic initiator',payment_releaser='synthetic releaser')],opening_ap=[{'id':'S1','balance':'0'}],gl_ap='20',supplier_balances=[approved('S1',balance='20')],gl_accrual='9600',bank_total='100')
        c['handoffs']=handoffs(c,{'recognition':'Expense and asset recognition'});c['controls'].update(population_count=2,population_amount='9720')
    elif package=='fixed-assets':
        c.update(asset_policy={'model':'cost','component_review':True,'life_review':True,'review_memo':'Reviewed significant components and framework life-review frequency'},assets=[approved('machine',opening_cost='600000',opening_accumulated='180000',residual='60000',remaining_life='4',ready_date='2024-01-01',method='straight_line',remaining_units='0',period_units='0',change={'enabled':False},disposal={'enabled':False},expected_depreciation='90000',gl_cost='600000',gl_accumulated='270000',scope='ordinary_ppe',component_id='machine component',consumption_memo='Straight-line engineering service use')],costs=[],cip=[],gl={'cost':'600000','accumulated':'270000','cip':'0'})
        c['asset_inventory']=['machine'];c['project_inventory']=[];c['handoffs']=handoffs(c,{'impairment':'Impairment','leases':'Lease Accounting'})
    elif package=='intercompany-accounting':
        c.update(pairs=[approved('AB',entity_a='Synthetic Group',entity_b='Synthetic Sub',currency='USD',transaction_id='IC1',opening_a='100',opening_b='100',recharge='0',settled_a='0',settled_b='0',settlement_evidence='No settlement',confirmed_a='100',confirmed_b='100',rate_a='1.2',rate_b='1.1',initial_rate_a='1',initial_rate_b='1',book_a='100',book_b='100',gl_a='120',gl_b='110',rate_evidence='Synthetic local closing quotes',mismatch_items=[],date='2026-12-31')],recharges=[])
        c['pairs'][0].update(opening_book_a='100',opening_book_b='100',opening_book_evidence='Certified prior-close local book');c['handoffs']=handoffs(c,{'consolidation':'Consolidation','transfer_pricing':'Transfer Pricing','fx':'Foreign Currency'});c['controls'].update(population_count=1,population_amount='100')
    return c

def certified(package,fw='IFRS'):
    c=certify(package,operational(package,fw))
    if fw=='UK_GAAP':
        from production import canonical_knowledge,PACKAGES as REGISTRY,case_fingerprint
        claims,_=canonical_knowledge(REGISTRY[package][1],fw)
        c['knowledge_review']['applied_claim_ids']=[x['claim_id'] for x in claims if not any(z in x['proposition'].replace(' ','') for z in ['FRS101','FRS105'])]
        c['reviewer_signoff']['case_fingerprint']=case_fingerprint(c)
    return c
