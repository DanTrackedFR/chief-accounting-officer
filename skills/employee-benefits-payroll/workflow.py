"""Service-earned short-term/DC accounting; payroll processing is out of scope."""
from financing_accounting import *

def assess(c,claims):
    rs=begin(c,'benefits');entries=imports(c,{'share-based-compensation','revenue-recognition','accounting-changes'});out=[];gross=[]
    required(c,'cash_total','register_expense','register_closing','register_withholding')
    expense=liability=withholding=paid=opening_total=ZERO
    for r in rs:
        kind=enum(r,'kind',{'salary','bonus','commission','leave','defined_contribution','employer_tax'})
        reviewed(r,c,'entitlement_memo','classification_memo','cutoff_memo','settlement_memo')
        if not flag(r,'earned_obligation') or not flag(r,'short_term'):
            raise ReviewRequired('Benefit recognition/settlement is unresolved or requires long-term/actuarial method')
        if kind=='leave' and not flag(r,'accumulating'):raise ReviewRequired('Nonaccumulating leave cannot use unused-day accrual')
        if flag(r,'capitalized'):raise ReviewRequired('Benefit asset classification requires complete underlying asset/contract-cost workflow')
        amount=cash(nonnegative(r['units'])*nonnegative(r['rate']))
        burden=cash(amount*fraction(r['employer_rate']))
        if kind in {'defined_contribution','employer_tax'} and burden:raise ReviewRequired('Do not apply employer burden to contribution/tax again')
        charge=amount+burden;opening=nonnegative(r['opening']);payment=nonnegative(r['payment']);deduction=nonnegative(r['withholding'])
        if deduction>payment or payment>opening+charge:raise ReviewRequired('Payroll payment/withholding exceeds earned available liability')
        closing=cash(opening+charge-payment);agree(r['expected_charge'],charge,'Benefit measurement');agree(r['gl_closing'],closing,'Benefit source/GL')
        entries.append(journal(('Dr','Employee benefit expense',charge),('Cr','Employee benefit payable',charge)))
        entries.append(journal(('Dr','Employee benefit payable',payment),('Cr','Cash',payment-deduction),('Cr','Employee withholding payable',deduction)))
        expense+=charge;liability+=closing;opening_total+=opening;withholding+=deduction;paid+=payment-deduction;gross.append(charge)
        out.append(dict(kind=kind,charge=charge,closing=closing,net_payment=payment-deduction))
    population(c,rs,gross);agree(c['cash_total'],paid,'Payroll cash');agree(c['register_expense'],expense,'Payroll register expense');agree(c['register_closing'],liability,'Payroll register liability');agree(c['register_withholding'],withholding,'Employee deductions')
    stocks(c,{'Employee benefit payable':(-opening_total,-liability),'Employee withholding payable':(ZERO,-withholding)})
    return complete(c,'Earned employee benefits and payroll clearing reconciled',dict(benefits=out,expense=expense,closing_liability=liability,withholding=withholding,net_cash=paid),entries,
        ['Framework-specific entitlement and service obligation are evidenced, not inferred from target payout',
         'Defined benefit, other long-term, termination, employment law and contribution/tax entitlement require specialists; no payroll processing'])
