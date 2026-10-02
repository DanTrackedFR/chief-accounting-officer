from reporting_accounting import *

def assess(c,claims):
    common(c,'cash_accounts','transactions','indirect','noncash','statement','cash_policy','handoffs','cash_inventory')
    p=c['cash_policy'];policy(c,p);required(p,'early_adoption','business_activity','interest_paid','interest_received','dividends_paid','dividends_received','restricted_memo')
    fw=c['framework'];modern=fw in ['IFRS','AASB'] and (iso(c['period_start'])>=iso('2027-01-01') or flag(p,'early_adoption'))
    if fw not in ['IFRS','AASB'] and flag(p,'early_adoption'):raise ReviewRequired('IFRS18 cannot be adopted into US/FRS102 cash flow')
    if modern and (p['business_activity']!='ordinary' or fw=='AASB' and c['reporting_tier']==2):raise ReviewRequired('IFRS18 main-business or Australian Tier2 amendments need specialist route')
    if fw=='US_GAAP':expected={'interest_paid':'operating','interest_received':'operating','dividends_received':'operating','dividends_paid':'financing'}
    elif modern:expected={'interest_paid':'financing','interest_received':'investing','dividends_received':'investing','dividends_paid':'financing'}
    else:expected={}
    for k,v in expected.items():
        if p[k]!=v:raise ReviewRequired('Framework/period interest-dividend classification conflicts with adopted method')
    if not expected:
        for k,allowed in [('interest_paid',['operating','financing']),('interest_received',['operating','investing']),('dividends_received',['operating','investing']),('dividends_paid',['operating','financing'])]:
            if p[k] not in allowed:raise ReviewRequired('Unsupported interest/dividend policy election')
    accounts=rows(c['cash_accounts'],False);inventory(c,'cash_inventory',accounts);opening=ZERO;closing=ZERO;bsopen=ZERO;bsclose=ZERO;fx=ZERO
    for a in accounts:
        reviewed(a,c,'definition_memo','restriction_evidence','bank_gl_evidence');required(a,'opening','closing','gl_opening','gl_closing','type','cf_included','balance_sheet_cash','fx')
        agree(a['opening'],a['gl_opening'],'Opening account GL');agree(a['closing'],a['gl_closing'],'Closing account GL')
        included=flag(a,'cf_included');bstag=flag(a,'balance_sheet_cash')
        if a['type'] not in ['demand','equivalent','restricted','overdraft','excluded']:raise ReviewRequired('Cash definition route unresolved')
        if a['type'] in ['demand','equivalent'] and not included:raise ReviewRequired('Qualifying cash omitted from cash flow population')
        if a['type']=='excluded' and included:raise ReviewRequired('Noncash instrument included in cash flow cash')
        if a['type']=='equivalent':
            required(a,'acquisition_date','maturity_date','cash_management','known_amount','insignificant_risk');d=iso(a['acquisition_date']);m=iso(a['maturity_date']);month=d.month+3;year=d.year+(month-1)//12;month=(month-1)%12+1;limit=d.replace(year=year,month=month,day=min(d.day,monthrange(year,month)[1]))
            if m<d or m>limit or not all(flag(a,k) for k in ['cash_management','known_amount','insignificant_risk']):raise ReviewRequired('Cash-equivalent original maturity/purpose/risk unsupported')
        if a['type']=='restricted':
            if fw=='US_GAAP' and not included:raise ReviewRequired('US cash flow reconciliation includes restricted cash population')
            if fw!='US_GAAP' and included and not flag(a,'withdrawable_demand'):raise ReviewRequired('Restriction alone cannot prove deposit cash eligibility')
        if a['type']=='overdraft':
            if included and (fw=='US_GAAP' or not flag(a,'integral_cash_management') or not flag(a,'repayable_on_demand')):raise ReviewRequired('Overdraft requires distinct framework cash-management assessment')
        elif dec(a['opening'])<0 or dec(a['closing'])<0:raise ReviewRequired('Negative asset cash balance requires overdraft route')
        if included:opening+=dec(a['opening']);closing+=dec(a['closing']);fx+=dec(a['fx'])
        if bstag:bsopen+=dec(a['opening']);bsclose+=dec(a['closing'])
    specialist(c,'fx','Foreign Currency',fx);specialist(c,'statements','Financial Statements');specialist(c,'leases','Lease Accounting');specialist(c,'consolidation','Consolidation')
    tx=rows(c['transactions']);totals={k:ZERO for k in ['operating','investing','financing']};direct={};ids=set()
    fixed={'customer_receipts':'operating','suppliers_employees':'operating','capital_purchase':'investing','business_acquisition':'investing','business_disposal':'investing','debt_proceeds':'financing','debt_repayment':'financing','equity_issue':'financing'}
    transfers=ZERO
    receipts={'customer_receipts','debt_proceeds','equity_issue','interest_received','dividends_received'}
    payments={'suppliers_employees','capital_purchase','debt_repayment','interest_paid','dividends_paid','lease_principal','lease_interest','lease_operating'}
    for t in tx:
        reviewed(t,c,'classification_memo','bank_id');required(t,'date','amount','kind','category','cash','source_id');inperiod(c,t['date']);n=dec(t['amount'])
        if t['bank_id'] in ids:raise ReviewRequired('Duplicate bank flow');
        ids.add(t['bank_id'])
        if not flag(t,'cash'):raise ReviewRequired('Noncash transaction must be outside bank cash flow totals')
        kind=t['kind'];category=t['category']
        if kind=='internal_transfer':
            if category!='excluded':raise ReviewRequired('Cash-to-cash transfer is not an operating/investing/financing flow')
            transfers+=n
            continue
        if kind in receipts and n<0 or kind in payments and n>0:raise ReviewRequired('Receipt/payment cash sign conflicts with transaction classification')
        expected_category=fixed.get(kind,p.get(kind))
        if kind=='income_taxes':
            if fw=='US_GAAP':expected_category='operating'
            else:
                required(t,'specifically_identified');expected_category=category if flag(t,'specifically_identified') else 'operating'
        if kind in ['lease_principal','lease_interest','lease_operating']:
            expected_category='operating' if kind=='lease_operating' else 'financing' if kind=='lease_principal' else p['interest_paid']
        if expected_category is None or category!=expected_category or category not in totals:raise ReviewRequired('Cash flow accounting classification unresolved')
        totals[category]+=n;direct[kind]=direct.get(kind,ZERO)+n
    agree(transfers,0,'Internal cash transfers must cancel within included population')
    for kind in ['business_acquisition','business_disposal']:
        if kind in direct:specialist(c,kind,'Consolidation',direct[kind])
    noncash=rows(c['noncash']);noncashwork=[]
    for n in noncash:
        reviewed(n,c,'accounting_memo','source_id');required(n,'amount','type')
        if n['source_id'] in {t['source_id'] for t in tx}:raise ReviewRequired('Noncash source double counted in bank flows')
        noncashwork.append({'id':n['id'],'amount':nonnegative(n['amount']),'type':n['type']})
    ind=c['indirect'];required(ind,'starting_subtotal','start_amount','net_profit','subtotal_to_profit','adjustments','working_capital')
    if fw=='US_GAAP' and ind['starting_subtotal']!='net_profit' or modern and ind['starting_subtotal']!='operating_profit':raise ReviewRequired('Indirect starting subtotal conflicts with framework/adoption')
    if ind['starting_subtotal'] not in ['net_profit','profit_before_tax','operating_profit']:raise ReviewRequired('Unsupported cash flow starting subtotal')
    agree(dec(ind['start_amount'])+dec(ind['subtotal_to_profit']),ind['net_profit'],'Cash subtotal to net profit');specialist(c,'profit','Financial Statements',dec(ind['start_amount']))
    operating=dec(ind['start_amount']);adjustments=rows(ind['adjustments']);wc=rows(ind['working_capital'])
    for a in adjustments:
        reviewed(a,c,'basis_memo');required(a,'amount','noncash_acquisition_fx_excluded')
        if not flag(a,'noncash_acquisition_fx_excluded'):raise ReviewRequired('Indirect adjustment has acquisition/FX contamination')
        operating+=dec(a['amount'])
    for w in wc:
        reviewed(w,c,'source_bridge');required(w,'opening','closing','acquisition','fx','noncash','side')
        if w['side'] not in ['asset','liability']:raise ReviewRequired('Working capital account sign unresolved')
        delta=dec(w['closing'])-dec(w['opening'])-dec(w['acquisition'])-dec(w['fx'])-dec(w['noncash']);operating+=delta*(-1 if w['side']=='asset' else 1)
    agree(operating,totals['operating'],'Indirect to direct operating cash');s=c['statement'];required(s,'opening','closing','balance_sheet_opening','balance_sheet_closing','operating','investing','financing','fx')
    for k in totals:agree(s[k],totals[k],'Statement cash '+k)
    agree(s['opening'],opening,'Statement opening cash');agree(s['closing'],closing,'Statement closing cash');agree(s['balance_sheet_opening'],bsopen,'BS opening cash');agree(s['balance_sheet_closing'],bsclose,'BS closing cash');agree(s['fx'],fx,'FX cash effect');agree(opening+sum(totals.values(),ZERO)+fx,closing,'Opening/flows/FX/closing cash')
    population(c,tx,[abs(dec(t['amount'])) for t in tx])
    return finish('Cash population, direct and indirect statements and balance-sheet cash reconcile.',{'opening':opening,'closing':closing,'direct_operating':totals['operating'],'indirect_operating':cash(operating),'direct_support':direct,'investing':totals['investing'],'financing':totals['financing'],'fx':fx,'balance_sheet_cash':bsclose,'noncash':noncashwork},[],
      ['Classification is separate from underlying recognition; acquisitions are supplied net-of-acquired-cash amounts and need group source proof.'],
      ['Cash definition/restrictions, FX bridge, financing liability changes, noncash activity, supplier finance and adopted interest/dividend policy.'])
