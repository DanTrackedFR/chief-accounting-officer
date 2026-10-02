"""Plain amortized-cost debt schedules, separate principal and reporting-date rights."""
from financing_accounting import *

def assess(c,claims):
    rs=begin(c,'debt');entries=imports(c,{'financial-instruments-ecl','foreign-currency','accounting-changes'});out=[];gross=[]
    op_total=cl_total=ZERO
    for r in rs:
        if enum(r,'measurement',{'amortized_cost'})!='amortized_cost':raise ReviewRequired('Instrument specialist required')
        reviewed(r,c,'terms_memo','fee_memo','yield_memo','classification_memo','covenant_memo')
        if flag(r,'complex_features') or flag(r,'modified'):raise ReviewRequired('Derivative/convertible or modification/extinguishment requires qualified instrument conclusion; old EIR cannot continue automatically')
        opening=nonnegative(r['opening_carrying']);op_principal=nonnegative(r['opening_principal'])
        draws=nonnegative(r['draws']);fees=nonnegative(r['eligible_cost']);service=nonnegative(r['service_cost'])
        if fees>draws or (fees and not flag(r,'directly_attributable')):raise ReviewRequired('Ineligible or undrawn-facility cost cannot reduce term debt')
        # Each full interest interval is independently dated and uses its actual opening stock.
        carrying=cash(opening+draws-fees);principal=op_principal+draws;total_interest=total_cash_interest=repayments=ZERO
        periods=rows(r['schedule']);inventory(r,'schedule_inventory',periods);last=iso(c['period_start'])
        for p in periods:
            approval(p,c);start=iso(p['start']);end=iso(p['end'])
            if start!=last or end<=start or end>iso(c['reporting_period']):raise ReviewRequired('EIR schedule gap/overlap or future period')
            interest=cash(carrying*fraction(p['effective_period_rate']));cash_interest=nonnegative(p['cash_interest']);repay=nonnegative(p['principal_payment'])
            if repay>principal:raise ReviewRequired('Repayment exceeds legal principal')
            carrying=cash(carrying+interest-cash_interest-repay);principal-=repay
            if carrying<0:raise ReviewRequired('Debt carrying balance below zero')
            agree(p['expected_interest'],interest,'Effective interest');agree(p['expected_closing'],carrying,'EIR interval')
            total_interest+=interest;total_cash_interest+=cash_interest;repayments+=repay;last=end
        if last!=iso(c['reporting_period']) and (carrying or periods):raise ReviewRequired('EIR schedule must cover reporting cutoff')
        agree(r['lender_principal'],principal,'Lender principal');agree(r['gl_closing'],carrying,'Debt source/GL')
        if not flag(r,'rights_at_reporting_date'):raise ReviewRequired('Current/noncurrent rights, covenant waiver or refinancing requires legal/framework evidence')
        current=nonnegative(r['current_carrying']);noncurrent=nonnegative(r['noncurrent_carrying']);agree(current+noncurrent,carrying,'Maturity presentation')
        maturities=rows(r['maturities']);inventory(r,'maturity_inventory',maturities)
        due=due_carrying=due_current=ZERO
        for m in maturities:
            approval(m,c);d=iso(m['date'])
            if d<=iso(c['reporting_period']):raise ReviewRequired('Overdue debt requires default/current classification specialist')
            due+=nonnegative(m['principal'])
            due_carrying+=nonnegative(m['carrying'])
            if d<=anniversary(iso(c['reporting_period'])):due_current+=nonnegative(m['carrying'])
        agree(due,principal,'Complete debt maturity population')
        agree(due_carrying,carrying,'Maturity carrying population');agree(current,due_current,'Current maturity classification')
        entries += [journal(('Dr','Cash',draws-fees-service),('Dr','Financing service expense',service),('Cr','Debt carrying liability',draws-fees)),
            journal(('Dr','Interest expense',total_interest),('Cr','Debt carrying liability',total_interest)),
            journal(('Dr','Debt carrying liability',total_cash_interest+repayments),('Cr','Cash',total_cash_interest+repayments))]
        gross.append(op_principal+draws);out.append(dict(opening=opening,draws=draws,eligible_cost=fees,effective_interest=total_interest,cash_interest=total_cash_interest,repayments=repayments,closing=carrying,principal=principal,current=current,noncurrent=noncurrent))
        op_total+=opening;cl_total+=carrying
    population(c,rs,gross)
    stocks(c,{'Debt carrying liability':(-op_total,-cl_total)})
    return complete(c,'Plain debt effective-interest and lender/GL bridges reconciled',dict(debt=out),entries,
        ['Actual periodic yields and eligible cost classifications require independent contract evidence; no yield guessed',
         'Modification, extinguishment, revolvers, debt-for-equity, FVTPL, derivatives, covenant/default and legal validity remain instrument/legal specialists'])
