from operations_accounting import *

def qualified_fx(c, invoices):
    """Consume current FX-owner monetary results; never compute a rate in AR."""
    from production import assess_case
    def dimensions(native):
        cur=native.get('currency',native.get('functional_currency'))
        if isinstance(cur,dict):cur=cur.get('functional')
        return tuple(native.get(k) for k in ('entity','framework','jurisdiction','period_start','reporting_period'))+(cur,)
    imports=rows(c.get('imports', [])); by={}; used=set(); out={}
    for imp in imports:
        approval(imp,c)
        if imp.get('package')!='foreign-currency' or imp.get('mode')!='evidence_only':
            raise ReviewRequired('AR imports only qualified evidence-only FX owner work')
        native=imp.get('case',{}); actual=assess_case('foreign-currency',native)
        if dimensions(native)!=dimensions(c) or actual.get('status')!='complete' or actual!=imp.get('result'):
            raise ReviewRequired('AR FX owner is stale, incomplete or dimensionally mismatched')
        by[imp['id']]=imp
    for invoice in invoices:
        foreign=invoice['currency']!=c['functional_currency']
        if not foreign:
            if invoice.get('fx_import'):raise ReviewRequired('Foreign invoice cannot be relabelled as functional currency')
            continue
        required(invoice,'fx_import','fx_item','foreign_amount')
        if invoice['fx_import'] not in by:raise ReviewRequired('Foreign invoice currency unsupported without qualified FX owner')
        imp=by[invoice['fx_import']];matches=[x for x in imp['case']['items'] if x['id']==invoice['fx_item']]
        if len(matches)!=1:raise ReviewRequired('Foreign invoice needs one exact FX position')
        x=matches[0];required(x,'foreign_currency')
        if x['type']!='monetary' or x['side']!='asset' or x['foreign_currency']!=invoice['currency'] or x['initial_date']!=invoice['invoice_date'] or x['account']!='accounts receivable':
            raise ReviewRequired('Foreign invoice and FX position semantics differ')
        agree(invoice['foreign_amount'],x['foreign_amount'],'Original foreign invoice')
        agree(invoice['amount'],x['opening_book'],'Foreign invoice functional opening')
        if bool(invoice['opening'])!=(x['opening_route']=='carried_monetary'):
            raise ReviewRequired('Foreign invoice recognition/opening route differs')
        key=(imp['id'],x['id'])
        if key in used:raise ReviewRequired('FX position imported twice')
        used.add(key)
        value=next(v for v in imp['result']['calculations']['transactions'] if v['id']==x['id'])
        out[invoice['id']]=value
    expected={(imp['id'],x['id']) for imp in imports for x in imp['case']['items']}
    if used!=expected:raise ReviewRequired('AR FX position population incomplete')
    return out


def assess(c,claims):
    proof(c,'invoices','receipts','credits','opening_customers','closing_customers','opening_unapplied','liability_applications','refunds','gl_ar','gl_unapplied','collections','bank_total','refund_bank_total','handoffs')
    handoff(c,'revenue','Revenue Recognition');handoff(c,'ecl','ECL')
    inv=rows(c['invoices'],False);receipts=rows(c['receipts']);credits=rows(c['credits']);cust=rows(c['opening_customers'],False);closing=rows(c['closing_customers'],False)
    fx_positions=qualified_fx(c, inv);fx_total=ZERO;fx_applied={id:ZERO for id in fx_positions}
    balances={r['id']:nonnegative(r['balance']) for r in cust};opening=sum(balances.values(),ZERO);entries=[];invs={};billed=ZERO;credit=ZERO;applied=ZERO;cash_total=ZERO
    deposits=rows(c['opening_unapplied'],False)
    if {r['id'] for r in deposits}!=set(balances):raise ReviewRequired('Opening customer liability inventory incomplete')
    liabilities={r['id']:nonnegative(r['balance']) for r in deposits};opening_liability=sum(liabilities.values(),ZERO)
    for i in inv:
        approval(i,c);required(i,'customer','amount','due_date','invoice_date','opening','entitlement_supported','offset','disputed','currency')
        if not flag(i,'entitlement_supported') or i['customer'] not in balances or (i['currency']!=c['functional_currency'] and i['id'] not in fx_positions):raise ReviewRequired('Invoice right, customer or currency unsupported')
        amount=positive(i['amount']);iso(i['due_date']);date=iso(i['invoice_date'])
        if date>iso(c['reporting_period']):raise ReviewRequired('Future invoice')
        if flag(i,'opening') and date>=iso(c['period_start']):raise ReviewRequired('Opening invoice must precede current reporting period')
        invs[i['id']]={'row':i,'balance':amount}
        if not flag(i,'opening'):
            inperiod(c,i['invoice_date']);balances[i['customer']]+=amount;billed+=amount
            # Offset classification is supplied by the reviewed revenue memo.
            entries.append(journal(('Dr','accounts receivable',amount),('Cr',i['offset'],amount)))
    for customer in balances:
        agree(sum((x['balance'] for x in invs.values() if x['row']['customer']==customer and x['row']['opening']),ZERO),next(r['balance'] for r in cust if r['id']==customer),'Opening invoice detail')
    for id,value in fx_positions.items():
        gain=dec(value['gain']);fx_total+=gain
        target=invs[id];target['balance']+=gain;balances[target['row']['customer']]+=gain
        if target['balance']<0:raise ReviewRequired('FX-adjusted invoice is negative')
        if gain:entries.append(movement('accounts receivable','FX income',gain))
    for cr in credits:
        approval(cr,c);required(cr,'invoice_id','amount','date','offset','reason','revenue_reviewed')
        inperiod(c,cr['date'])
        if cr['invoice_id'] not in invs or not flag(cr,'revenue_reviewed') or cr['reason'] not in ['billing_error','commercial_concession','return']:raise ReviewRequired('Credit needs approved revenue classification')
        if cr['invoice_id'] in fx_positions:raise ReviewRequired('Foreign invoice credit requires separately qualified event method')
        target=invs[cr['invoice_id']];n=positive(cr['amount'])
        if iso(cr['date'])<iso(target['row']['invoice_date']):raise ReviewRequired('Credit predates invoiced right')
        if n>target['balance']:raise ReviewRequired('Credit exceeds outstanding right')
        target['balance']-=n;balances[target['row']['customer']]-=n;credit+=n
        entries.append(journal(('Dr',cr['offset'],n),('Cr','accounts receivable',n)))
    residual_events=[]
    for r in receipts:
        approval(r,c);required(r,'customer','amount','date','allocations','bank_id','bank_confirmed','currency')
        if r['customer'] not in balances or not flag(r,'bank_confirmed') or r['currency']!=c['functional_currency']:raise ReviewRequired('Receipt is not supported bank cash in the book currency')
        inperiod(c,r['date']);n=positive(r['amount']);alloc=rows(r['allocations']);allocated=ZERO
        for a in alloc:
            required(a,'invoice_id','amount')
            if a['invoice_id'] not in invs:raise ReviewRequired('Cash allocation invoice missing')
            target=invs[a['invoice_id']];v=positive(a['amount'])
            if any(cr['invoice_id']==a['invoice_id'] and iso(cr['date'])>iso(r['date']) for cr in credits):raise ReviewRequired('Credit after customer payment requires paid-invoice credit/refund specialist classification')
            if iso(r['date'])<iso(target['row']['invoice_date']):raise ReviewRequired('Pre-invoice cash must remain a deposit until separately supported application')
            if target['row']['customer']!=r['customer'] or v>target['balance']:raise ReviewRequired('Cross-customer or excessive cash allocation')
            if a['invoice_id'] in fx_applied:fx_applied[a['invoice_id']]+=v
            allocated+=v;target['balance']-=v;balances[r['customer']]-=v
        if allocated>n:raise ReviewRequired('Allocations exceed receipt')
        applied+=allocated;liabilities[r['customer']]+=n-allocated;cash_total+=n
        residual_events.append({'customer':r['customer'],'date':r['date'],'amount':n-allocated})
        entries.append(journal(('Dr','cash',n),('Cr','accounts receivable',allocated),('Cr','customer unapplied liability',n-allocated)))
    if len({r['bank_id'] for r in receipts})!=len(receipts):raise ReviewRequired('Duplicate bank receipt')
    applications=rows(c['liability_applications']);refunds=rows(c['refunds']);events=applications+refunds
    # Check every dated prefix of the liability ledger. Same-day movements may
    # be grouped; no later receipt can finance an earlier application/refund.
    opening_deposits={r['id']:nonnegative(r['balance']) for r in deposits}
    for event in events:
        required(event,'customer','date','amount');inperiod(c,event['date']);positive(event['amount'])
        if event['customer'] not in opening_deposits:raise ReviewRequired('Liability event customer missing')
    for event in sorted(events,key=lambda e:(iso(e['date']),e['id'])):
        day=iso(event['date']);customer=event['customer']
        funding=opening_deposits[customer]+sum((e['amount'] for e in residual_events if e['customer']==customer and iso(e['date'])<=day),ZERO)
        release=sum((positive(e['amount']) for e in events if e['customer']==customer and iso(e['date'])<=day),ZERO)
        if release>funding:raise ReviewRequired('Customer liability application/refund precedes available funding')
    for a in applications:
        approval(a,c);required(a,'customer','invoice_id','amount','date','identification_evidence')
        texts(a,'identification_evidence');inperiod(c,a['date'])
        if a['invoice_id'] not in invs or a['customer'] not in liabilities:raise ReviewRequired('Customer deposit application lacks original right')
        if a['invoice_id'] in fx_positions:raise ReviewRequired('Foreign invoice deposit application requires separate FX event method')
        target=invs[a['invoice_id']];n=positive(a['amount'])
        if a['customer']!=target['row']['customer'] or iso(a['date'])<iso(target['row']['invoice_date']) or n>target['balance'] or n>liabilities[a['customer']]:raise ReviewRequired('Customer liability application exceeds right or available funds')
        liabilities[a['customer']]-=n;target['balance']-=n;balances[a['customer']]-=n;applied+=n
        entries.append(journal(('Dr','customer unapplied liability',n),('Cr','accounts receivable',n)))
    refund_total=ZERO;bankids={r['bank_id'] for r in receipts}
    for r in refunds:
        approval(r,c);required(r,'customer','amount','date','bank_id','bank_confirmed','refund_right_evidence')
        texts(r,'refund_right_evidence','bank_id');inperiod(c,r['date']);n=positive(r['amount'])
        if r['customer'] not in liabilities or n>liabilities[r['customer']] or r['bank_id'] in bankids or not flag(r,'bank_confirmed'):raise ReviewRequired('Refund right, bank evidence or customer liability unresolved')
        bankids.add(r['bank_id']);liabilities[r['customer']]-=n;refund_total+=n;entries.append(journal(('Dr','customer unapplied liability',n),('Cr','cash',n)))
    unapplied=sum(liabilities.values(),ZERO)
    agree(c['bank_total'],cash_total,'Bank receipt population');agree(c['refund_bank_total'],refund_total,'Bank refund population');agree(c['gl_unapplied'],unapplied,'Unapplied liability')
    if {r['id'] for r in closing}!=set(balances):raise ReviewRequired('Customer confirmation inventory incomplete')
    for r in closing:approval(r,c);agree(r['balance'],balances[r['id']],'Customer confirmation')
    for id,value in fx_positions.items():
        agree(fx_applied[id],value['settlement'],'FX settlement to applied bank receipts')
        agree(invs[id]['balance'],value['closing'],'FX closing position to invoice')
    total=sum(balances.values(),ZERO);agree(c['gl_ar'],total,'AR subledger to GL');agree(total,opening+billed-credit-applied+fx_total,'AR movement')
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
    return finish('Customer balances, bank allocations, credits and collection exceptions reconciled.',{'opening_ar':opening,'billed':billed,'credits':credit,'applied_cash_and_deposits':applied,'closing_ar':total,'fx_movement':fx_total,'bank_receipts':cash_total,'opening_unapplied':opening_liability,'unapplied_liability':unapplied,'refunds':refund_total,'ageing':aging},entries,
      ['Billing and bank cash do not establish revenue. Disputes are not automatic credits or write-offs.','Unidentified cash remains a customer liability; no ageing-only release or cross-customer netting.'],
      ['Receivable/contract/customer liabilities, credit loss and material dispute disclosures require Revenue Recognition and ECL review.'])
