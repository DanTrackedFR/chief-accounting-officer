from operations_accounting import *

def assess(c,claims):
    proof(c,'invoices','accruals','payments','opening_ap','gl_ap','supplier_balances','gl_accrual','handoffs','bank_total')
    handoff(c,'recognition','Expense and asset recognition')
    inv=rows(c['invoices']);acs=[dict(a) for a in rows(c['accruals'])];payments=rows(c['payments']);opening=rows(c['opening_ap'],False);confirm=rows(c['supplier_balances'],False)
    balances={r['id']:nonnegative(r['balance']) for r in opening};start=sum(balances.values(),ZERO);entries=[];billed=ZERO;paid=ZERO;acc=ZERO;keys=set();acmap={a['id']:a for a in acs};cleared={a['id']:ZERO for a in acs}
    for a in acs:
        approval(a,c);required(a,'supplier','units','rate','received_supported','received_date','invoiced_received','opening_accrual','account','reversal_date','clearing_plan','subsequent_actual','backtest_memo','gl_closing')
        if a['supplier'] not in balances or not flag(a,'received_supported'):raise ReviewRequired('Unbilled receipt/obligation unsupported')
        inperiod(c,a['received_date']);received=cash(nonnegative(a['units'])*nonnegative(a['rate']));prior=nonnegative(a['opening_accrual']);unbilled=received-nonnegative(a['invoiced_received'])
        if unbilled<0:raise ReviewRequired('Invoiced receipt exceeds complete source service')
        if iso(a['reversal_date'])<=iso(c['reporting_period']) or not a['clearing_plan']:raise ReviewRequired('Accrual reversal lacks future monitored clearing plan')
        nonnegative(a['subsequent_actual']);a['_received']=received;a['_unbilled']=unbilled
        delta=unbilled-prior;entries.append(movement(a['account'],'accrued expenses',delta));acc+=unbilled
    for i in inv:
        approval(i,c);required(i,'supplier','invoice_number','amount','units','unit_price','po_amount','received_amount','received_date','invoice_date','account','match_approved','bank_master_review','currency')
        if 'accrual_id' not in i:raise ReviewRequired('Explicit accrual link or empty none required')
        texts(i,'bank_master_review','invoice_number')
        key=(i['supplier'],i['invoice_number'].strip().casefold())
        if key in keys:raise ReviewRequired('Duplicate supplier invoice')
        keys.add(key)
        if i['supplier'] not in balances or i['currency']!=c['functional_currency'] or not flag(i,'match_approved'):raise ReviewRequired('Invoice match, supplier or book currency unresolved')
        if iso(i['received_date'])>iso(c['reporting_period']):raise ReviewRequired('Future invoice receipt')
        inperiod(c,i['invoice_date']);n=positive(i['amount'])
        agree(n,nonnegative(i['units'])*nonnegative(i['unit_price']),'Invoice units/rate');agree(n,i['po_amount'],'PO match');agree(n,i['received_amount'],'Receipt match')
        used=ZERO
        if i['accrual_id']:
            if i['accrual_id'] not in acmap:raise ReviewRequired('Missing prior accrual link')
            a=acmap[i['accrual_id']];used=min(n,nonnegative(a['opening_accrual'])-cleared[a['id']]);cleared[a['id']]+=used
            if a['supplier']!=i['supplier']:raise ReviewRequired('Cross-supplier accrual clearing')
        balances[i['supplier']]+=n;billed+=n;entries.append(journal(('Dr','accrued expenses',used),('Dr',i['account'],n-used),('Cr','accounts payable',n)))
    # Opening accrual is consumed by invoices before the closing estimate is
    # computed: remove the duplicate portion of any earlier release entry.
    if acs:
        entries=entries[len(acs):]
        for a in acs:
            remaining=nonnegative(a['opening_accrual'])-cleared[a['id']]
            entries.append(movement(a['account'],'accrued expenses',a['_unbilled']-remaining));agree(a['gl_closing'],a['_unbilled'],'Accrual final GL')
    bankids=set()
    for p in payments:
        approval(p,c);required(p,'supplier','amount','date','bank_id','bank_confirmed','bank_master_approved','payment_preparer','payment_releaser')
        texts(p,'bank_id','payment_preparer','payment_releaser')
        if p['supplier'] not in balances or p['bank_id'] in bankids or not flag(p,'bank_confirmed') or not flag(p,'bank_master_approved') or p['payment_preparer']==p['payment_releaser']:raise ReviewRequired('Payment segregation, bank master or duplicate payment failure')
        bankids.add(p['bank_id']);inperiod(c,p['date']);n=positive(p['amount'])
        if n>balances[p['supplier']]:raise ReviewRequired('Payment exceeds supported supplier debt')
        balances[p['supplier']]-=n;paid+=n;entries.append(journal(('Dr','accounts payable',n),('Cr','cash',n)))
    if {r['id'] for r in confirm}!=set(balances):raise ReviewRequired('Supplier confirmation coverage failed')
    for r in confirm:approval(r,c);agree(r['balance'],balances[r['id']],'Supplier confirmation')
    closing=sum(balances.values(),ZERO);agree(c['gl_ap'],closing,'AP subledger/GL');agree(c['bank_total'],paid,'Payment bank total');agree(c['gl_accrual'],acc,'Accrual total GL');agree(closing,start+billed-paid,'AP movement')
    population(c,inv+acs,[positive(i['amount']) for i in inv]+[a['_received'] for a in acs])
    return finish('Supplier invoices, payments and independently received unbilled liabilities reconciled.',{'opening_ap':start,'invoices':billed,'payments':paid,'closing_ap':closing,'closing_accruals':acc,'accrual_backtests':[{'id':a['id'],'estimate':a['_unbilled'],'subsequent_actual':nonnegative(a['subsequent_actual']),'variance':cash(nonnegative(a['subsequent_actual'])-a['_unbilled'])} for a in acs]},entries,
      ['PO approval or invoice date alone does not prove receipt or asset/expense recognition.','Subsequent invoice differences require estimate/error and cutoff review before posting; reversal cannot erase an unsettled obligation.'],
      ['Material accrual uncertainty, expense/asset classification, related parties and supplier financing require separate disclosure review.'])
