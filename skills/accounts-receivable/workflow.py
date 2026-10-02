from operations_accounting import *

def assess(c,claims):
    proof(c,'invoices','receipts','credits','opening_customers','closing_customers','gl_ar','gl_unapplied','collections','bank_total','handoffs')
    handoff(c,'revenue','Revenue Recognition');handoff(c,'ecl','ECL')
    inv=rows(c['invoices'],False);receipts=rows(c['receipts']);credits=rows(c['credits']);cust=rows(c['opening_customers'],False);closing=rows(c['closing_customers'],False)
    balances={r['id']:nonnegative(r['balance']) for r in cust};opening=sum(balances.values(),ZERO);entries=[];invs={};billed=ZERO;credit=ZERO;applied=ZERO;unapplied=ZERO;cash_total=ZERO
    for i in inv:
        approval(i,c);required(i,'customer','amount','due_date','invoice_date','opening','entitlement_supported','offset','disputed','currency')
        if not flag(i,'entitlement_supported') or i['customer'] not in balances or i['currency']!=c['functional_currency']:raise ReviewRequired('Invoice right, customer or currency unsupported')
        amount=positive(i['amount']);iso(i['due_date']);date=iso(i['invoice_date'])
        if date>iso(c['reporting_period']):raise ReviewRequired('Future invoice')
        invs[i['id']]={'row':i,'balance':amount}
        if not flag(i,'opening'):
            inperiod(c,i['invoice_date']);balances[i['customer']]+=amount;billed+=amount
            # Offset classification is supplied by the reviewed revenue memo.
            entries.append(journal(('Dr','accounts receivable',amount),('Cr',i['offset'],amount)))
    for customer in balances:
        agree(sum((x['balance'] for x in invs.values() if x['row']['customer']==customer and x['row']['opening']),ZERO),next(r['balance'] for r in cust if r['id']==customer),'Opening invoice detail')
    for cr in credits:
        approval(cr,c);required(cr,'invoice_id','amount','date','offset','reason','revenue_reviewed')
        inperiod(c,cr['date'])
        if cr['invoice_id'] not in invs or not flag(cr,'revenue_reviewed') or cr['reason'] not in ['billing_error','commercial_concession','return']:raise ReviewRequired('Credit needs approved revenue classification')
        target=invs[cr['invoice_id']];n=positive(cr['amount'])
        if n>target['balance']:raise ReviewRequired('Credit exceeds outstanding right')
        target['balance']-=n;balances[target['row']['customer']]-=n;credit+=n
        entries.append(journal(('Dr',cr['offset'],n),('Cr','accounts receivable',n)))
    for r in receipts:
        approval(r,c);required(r,'customer','amount','date','allocations','bank_id','bank_confirmed','currency')
        if r['customer'] not in balances or not flag(r,'bank_confirmed') or r['currency']!=c['functional_currency']:raise ReviewRequired('Receipt is not supported bank cash in the book currency')
        inperiod(c,r['date']);n=positive(r['amount']);alloc=rows(r['allocations']);allocated=ZERO
        for a in alloc:
            required(a,'invoice_id','amount')
            if a['invoice_id'] not in invs:raise ReviewRequired('Cash allocation invoice missing')
            target=invs[a['invoice_id']];v=positive(a['amount'])
            if target['row']['customer']!=r['customer'] or v>target['balance']:raise ReviewRequired('Cross-customer or excessive cash allocation')
            allocated+=v;target['balance']-=v;balances[r['customer']]-=v
        if allocated>n:raise ReviewRequired('Allocations exceed receipt')
        applied+=allocated;unapplied+=n-allocated;cash_total+=n
        entries.append(journal(('Dr','cash',n),('Cr','accounts receivable',allocated),('Cr','customer unapplied liability',n-allocated)))
    if len({r['bank_id'] for r in receipts})!=len(receipts):raise ReviewRequired('Duplicate bank receipt')
    agree(c['bank_total'],cash_total,'Bank receipt population');agree(c['gl_unapplied'],unapplied,'Unapplied liability')
    if {r['id'] for r in closing}!=set(balances):raise ReviewRequired('Customer confirmation inventory incomplete')
    for r in closing:approval(r,c);agree(r['balance'],balances[r['id']],'Customer confirmation')
    total=sum(balances.values(),ZERO);agree(c['gl_ar'],total,'AR subledger to GL');agree(total,opening+billed-credit-applied,'AR movement')
    population(c,inv,[positive(i['amount']) for i in inv]);aging={'current':ZERO,'1_30':ZERO,'31_60':ZERO,'61_90':ZERO,'over90':ZERO};actions=rows(c['collections'])
    actionmap={r['invoice_id']:r for r in actions}
    if len(actionmap)!=len(actions):raise ReviewRequired('Duplicate invoice collection action')
    for id,x in invs.items():
        age=max(0,(iso(c['reporting_period'])-iso(x['row']['due_date'])).days);n=x['balance'];bucket='current' if not age else '1_30' if age<=30 else '31_60' if age<=60 else '61_90' if age<=90 else 'over90';aging[bucket]+=n
        if n and (age or flag(x['row'],'disputed')):
            if id not in actionmap:raise ReviewRequired('Past due/disputed invoice lacks collection ownership')
            a=actionmap[id];approval(a,c);required(a,'next_action','next_date','dispute_evidence','status')
            if a['status'] not in ['follow_up','dispute_review','promise_to_pay']:raise ReviewRequired('Unsupported collection closure without bank/credit evidence')
            if iso(a['next_date'])<iso(c['reporting_period']):raise ReviewRequired('Collection next action is stale')
    agree(sum(aging.values(),ZERO),total,'Ageing to GL')
    return finish('Customer balances, bank allocations, credits and collection exceptions reconciled.',{'opening_ar':opening,'billed':billed,'credits':credit,'applied_cash':applied,'closing_ar':total,'unapplied_liability':unapplied,'ageing':aging},entries,
      ['Billing and bank cash do not establish revenue. Disputes are not automatic credits or write-offs.','Unidentified cash remains a customer liability; no ageing-only release or cross-customer netting.'],
      ['Receivable/contract/customer liabilities, credit loss and material dispute disclosures require Revenue Recognition and ECL review.'])
