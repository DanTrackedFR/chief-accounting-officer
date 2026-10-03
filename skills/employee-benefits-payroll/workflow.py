"""Service-earned short-term/DC accounting; payroll processing is out of scope."""
from financing_accounting import *

def assess(c,claims):
    rs=begin(c,'benefits');entries=imports(c,{'share-based-compensation','revenue-recognition','accounting-changes','provisions-contingencies'});out=[];gross=[]
    required(c,'cash_total','register_expense','register_closing','register_withholding','opening_withholding','withholding_remittances','withholding_bank_total')
    expense=liability=withholding=paid=opening_total=ZERO;withholding_events={}
    for r in rs:
        kind=enum(r,'kind',{'salary','bonus','commission','leave','defined_contribution','employer_tax','termination'})
        reviewed(r,c,'entitlement_memo','classification_memo','cutoff_memo','settlement_memo')
        start=inperiod(c,r['service_start']);end=inperiod(c,r['service_end'])
        if end<start:raise ReviewRequired('Employee service interval is reversed')
        if not flag(r,'earned_obligation') or not flag(r,'short_term'):
            raise ReviewRequired('Benefit recognition/settlement is unresolved or requires long-term/actuarial method')
        if kind=='leave' and not flag(r,'accumulating'):raise ReviewRequired('Nonaccumulating leave cannot use unused-day accrual')
        if iso(r['settlement_date'])>anniversary(iso(c['reporting_period'])):raise ReviewRequired('Long-term settlement requires a separately supported measurement method')
        if flag(r,'capitalized'):raise ReviewRequired('Benefit asset classification requires complete underlying asset/contract-cost workflow')
        amount=cash(nonnegative(r['units'])*nonnegative(r['rate']))
        burden=cash(amount*fraction(r['employer_rate']))
        if kind in {'defined_contribution','employer_tax'} and burden:raise ReviewRequired('Do not apply employer burden to contribution/tax again')
        basis=enum(r,'measurement_basis',{'period_earned','cumulative_entitlement'})
        prior=nonnegative(r['prior_service_expense'])
        if basis=='period_earned' and prior:raise ReviewRequired('Period-earned input cannot subtract an unexplained prior expense')
        if basis=='cumulative_entitlement' and kind not in {'bonus','leave','commission'}:raise ReviewRequired('Cumulative entitlement route requires independently supported variable compensation')
        charge=cash(amount+burden-prior);opening=nonnegative(r['opening']);payment=nonnegative(r['payment']);deduction=nonnegative(r['withholding'])
        if payment:
            payment_date=inperiod(c,r['payment_date'])
            if payment>opening:
                if payment_date<start:raise ReviewRequired('Pre-service cash above opening obligation requires separate advance accounting')
                reviewed(r,c,'earned_service_at_payment_memo')
                paid_units=nonnegative(r['payment_service_units'])
                if paid_units>nonnegative(r['units']):raise ReviewRequired('Payment-date earned units exceed complete service population')
                earned_at_payment=cash(paid_units*nonnegative(r['rate'])*(1+fraction(r['employer_rate']))-prior)
                if payment>opening+earned_at_payment:raise ReviewRequired('Payment exceeds independently evidenced obligation earned at payment date')
        if kind=='termination':
            t=r['termination_review'];policy(c,t);reviewed(t,c,'withdrawal_memo','future_service_memo','framework_trigger_memo');inperiod(c,t['recognition_date'])
            if payment>opening and iso(r['payment_date'])<iso(t['recognition_date']):raise ReviewRequired('Termination payment precedes the recognition trigger; separate advance method required')
            if flag(t,'future_service_required'):raise ReviewRequired('Future-service retention payment is not immediate termination benefit')
            if c['framework'] in {'IFRS','AASB'}:
                cannot=flag(t,'cannot_withdraw');linked=flag(t,'linked_restructuring_recognized')
                if not (cannot or linked):raise ReviewRequired('Termination recognition trigger is not met')
                if not cannot and linked:raise ReviewRequired('Linked-only restructuring termination requires specialist plan/obligation linkage and separate adapter; an unrelated completed provision is insufficient')
            else:
                specialist(c,t['handoff'],'Termination benefit accounting',charge)
        if deduction>payment or payment>opening+charge:raise ReviewRequired('Payroll payment/withholding exceeds earned available liability')
        if deduction:withholding_events[payment_date]=withholding_events.get(payment_date,ZERO)+deduction
        closing=cash(opening+charge-payment);agree(r['expected_charge'],charge,'Benefit measurement');agree(r['gl_closing'],closing,'Benefit source/GL')
        entries.append(signed_entry('Employee benefit payable','Employee benefit expense',charge,False))
        entries.append(journal(('Dr','Employee benefit payable',payment),('Cr','Cash',payment-deduction),('Cr','Employee withholding payable',deduction)))
        expense+=charge;liability+=closing;opening_total+=opening;withholding+=deduction;paid+=payment-deduction;gross.append(abs(charge))
        out.append(dict(kind=kind,charge=charge,closing=closing,net_payment=payment-deduction))
    remittances=rows(c['withholding_remittances']);inventory(c,'withholding_inventory',remittances);remitted=ZERO
    for p in remittances:
        reviewed(p,c,'bank_evidence','authority_evidence');remit_date=inperiod(c,p['date']);remit_amount=nonnegative(p['amount']);remitted+=remit_amount
        withholding_events[remit_date]=withholding_events.get(remit_date,ZERO)-remit_amount
    opening_withholding=nonnegative(c['opening_withholding']);closing_withholding=opening_withholding+withholding-remitted
    available=opening_withholding
    for event_date in sorted(withholding_events):
        available+=withholding_events[event_date]
        if available<0:raise ReviewRequired('Dated withholding remittance exceeds liability available at settlement; separate advance accounting required')
    if closing_withholding<0:raise ReviewRequired('Withholding remittance exceeds substantiated liability')
    agree(c['withholding_bank_total'],remitted,'Withholding remittance bank');entries.append(journal(('Dr','Employee withholding payable',remitted),('Cr','Cash',remitted)))
    population(c,rs,gross);agree(c['cash_total'],paid+remitted,'Payroll cash');agree(c['register_expense'],expense,'Payroll register expense');agree(c['register_closing'],liability,'Payroll register liability');agree(c['register_withholding'],closing_withholding,'Employee deductions rollforward')
    stocks(c,{'Employee benefit payable':(-opening_total,-liability),'Employee withholding payable':(-opening_withholding,-closing_withholding)})
    return complete(c,'Earned employee benefits and payroll clearing reconciled',dict(benefits=out,expense=expense,closing_liability=liability,withholding=closing_withholding,withholding_deductions=withholding,withholding_remitted=remitted,net_cash=paid+remitted),entries,
        ['Framework-specific entitlement and service obligation are evidenced, not inferred from target payout',
         'Defined benefit, other long-term, termination, employment law and contribution/tax entitlement require specialists; no payroll processing'])
