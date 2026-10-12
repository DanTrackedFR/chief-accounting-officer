"""Bounded domestic tangible-construction allocation; underlying debt stays with its owner."""
from financing_accounting import *

EDITIONS={'IFRS':'IAS23_2026','AASB':'AASB123_MAR2020','US_GAAP':'ASC835_20_2026','UK_GAAP':'FRS102_SEP2024_2026'}

def day_fraction(d,basis):
    if basis=='actual_actual':return Decimal(1)/Decimal((date(d.year+1,1,1)-date(d.year,1,1)).days)
    if basis=='actual_365':return Decimal(1)/Decimal(365)
    if basis=='actual_360':return Decimal(1)/Decimal(360)
    raise ReviewRequired('Contractual dated interest convention unavailable')

def ifrs_day(expenditure,specific,general,period_daily_rate=None):
    """Actual directly attributable specific cost; residual spend uses general pool."""
    cost=sum((r['interest']-r['income'] for r in specific),ZERO)
    residual=max(ZERO,expenditure-sum((r['principal'] for r in specific),ZERO))
    principal=sum((r['principal'] for r in general),ZERO)
    rate=period_daily_rate if period_daily_rate is not None else (sum((r['interest'] for r in general),ZERO)/principal if principal else ZERO)
    return cost+residual*rate,rate

def us_day(expenditure,specific,general,period_daily_rate=None):
    """ASC avoidable interest: specific rate on actual spend, other debt on excess."""
    remaining=expenditure;cost=ZERO
    for r in specific:
        allocated=min(remaining,r['principal']);remaining-=allocated
        cost+=allocated*(r['interest']/r['principal'] if r['principal'] else ZERO)
    principal=sum((r['principal'] for r in general),ZERO)
    rate=period_daily_rate if period_daily_rate is not None else (sum((r['interest'] for r in general),ZERO)/principal if principal else ZERO)
    return cost+remaining*rate,rate

def assess(c,claims):
    if not claims or not all(r.get('topic_id')=='SUPPLEMENTAL_BORROWING_COSTS' for r in claims):
        raise ReviewRequired('NONPRODUCTION: incidental CIP routing cannot authorize capitalization')
    rs=begin(c,'projects');
    required(c,'original_source_snapshot')
    original=c['original_source_snapshot'];reviewed(original,c,'capture_memo')
    projection={key:c[key] for key in ('projects','borrowings','gl','financing_gl_interest','functional_currency')}
    if not same_result(original['records'],projection):raise ReviewRequired('Current amounts or source populations differ from independently captured originals')
    if c['imports']:raise ReviewRequired('Imported debt results require an economic-population binding adapter; independently reviewed original financing evidence is supported')
    if c.get('package')!='borrowing-costs':raise ReviewRequired('Borrowing Costs case identity mismatch')
    fw=c['framework'];edition=EDITIONS[fw]
    if [c['period_start'],c['reporting_period']]!=['2026-01-01','2026-12-31']:
        raise ReviewRequired('Only independently approved 2026 annual reporting period supported')
    if c['accounting_policy']['effective_standard']!=edition or c['applicability_review']['standard_versions']!=[edition]:
        raise ReviewRequired('Incorrect operative borrowing-cost standard edition')
    if fw=='AASB' and c['reporting_tier']!=1:raise ReviewRequired('AASB Tier2/NFP disclosure overlay not supported')
    if len(rs)!=1:raise ReviewRequired('One independently scoped construction object required; shared multi-project allocation unsupported')
    election=enum(c['accounting_policy'],'borrowing_costs',{'capitalize','expense'})
    if fw!='UK_GAAP' and election!='capitalize':raise ReviewRequired('Expense election not permitted for supported qualifying construction scope')
    reviewed(c['accounting_policy'],c,'consistency_memo','interest_basis_memo')
    p=rs[0];reviewed(p,c,'authorization_memo','qualifying_asset_memo','readiness_memo','progress_memo','expenditure_memo')
    enum(p,'asset_type',{'tangible_construction'});enum(p,'purpose',{'own_use'})
    if not flag(p,'qualifying_asset') or not flag(p,'substantial_period') or flag(p,'abandoned'):
        raise ReviewRequired('Nonqualifying or abandoned project requires expense/impairment owner assessment')
    if flag(p,'shared_components'):raise ReviewRequired('Shared component expenditures require separately scoped cessation and allocation')
    start=iso(c['period_start']);end=iso(c['reporting_period'])
    activity=iso(p['activity_start']);authorized=iso(p['authorized_date'])
    if activity<authorized or activity>end:raise ReviewRequired('Invalid project authorization or commencement')
    ready=iso(p['ready_date']) if p.get('ready_date') else end+timedelta(days=1)
    if ready<activity:raise ReviewRequired('Invalid project completion/cessation')
    opening=nonnegative(p['opening_expenditure']);prior_cost=nonnegative(p['opening_capitalized'])
    basis=enum(c['accounting_policy'],'expenditure_basis',{'actual_cash','carrying_cost'})
    if (fw=='UK_GAAP')!=(basis=='carrying_cost'):raise ReviewRequired('Incorrect framework expenditure basis')
    if fw!='UK_GAAP' and prior_cost:raise ReviewRequired('Previously capitalized costs require separately reviewed accumulated expenditure method')
    xs=rows(p['expenditures']);inventory(p,'expenditure_inventory',xs)
    economic=set();changes={};net=ZERO
    for x in xs:
        approval(x,c);texts(x,'economic_id','payment_memo');d=inperiod(c,x['date'])
        if x['economic_id'] in economic:raise ReviewRequired('Duplicate project expenditure economics')
        economic.add(x['economic_id']);n=dec(x['amount']);net+=n
        enum(x,'basis',{'cash_paid'})
        if x.get('project_id')!=p['id'] or x.get('currency')!=c['functional_currency']:raise ReviewRequired('Expenditure project/currency mismatch')
        if iso(x['cash_date'])!=d:raise ReviewRequired('Later cash payment cannot be backdated')
        changes[d]=changes.get(d,ZERO)+n
    agree(p['actual_net_expenditure'],net,'Actual expenditure source bridge')
    timelines=rows(p['timeline'],False);inventory(p,'timeline_inventory',timelines)
    days={};last=start
    for t in timelines:
        reviewed(t,c,'activity_memo','suspension_memo');lo=iso(t['start']);hi=iso(t['end'])
        state=enum(t,'state',{'pre','active','temporary','suspended','complete'})
        if lo!=last or hi<lo or hi>end:raise ReviewRequired('Capitalization timeline gap/overlap/cutoff')
        if state=='suspended' and (not flag(t,'extended') or flag(t,'necessary_delay') or flag(t,'substantial_technical_activity')):
            raise ReviewRequired('Suspension requires extended ceased development, not necessary delay or technical activity')
        if state=='temporary' and not (flag(t,'necessary_delay') or flag(t,'substantial_technical_activity')):
            raise ReviewRequired('Temporary interruption continuation lacks supported necessity/activity')
        for offset in range((hi-lo).days+1):
            d=lo+timedelta(days=offset)
            expected='pre' if d<activity else 'complete' if d>=ready else None
            if expected and state!=expected or not expected and state in {'pre','complete'}:
                raise ReviewRequired('Timeline inconsistent with evidenced commencement/readiness')
            days[d]=state
        last=hi+timedelta(days=1)
    if last!=end+timedelta(days=1):raise ReviewRequired('Complete temporal source population required')
    loans=rows(c['borrowings'],False);inventory(c,'borrowing_inventory',loans)
    debt_ids=set();borrowed={d:[] for d in days};actual_interest=ZERO;income_total=ZERO
    for b in loans:
        reviewed(b,c,'contract_memo','yield_memo','population_memo','cashflow_memo');texts(b,'economic_id','lender','currency')
        if b['economic_id'] in debt_ids:raise ReviewRequired('Duplicate debt economic identity')
        debt_ids.add(b['economic_id'])
        if b['currency']!=c['functional_currency'] or b.get('source_entity')!=c['entity'] or b.get('source_framework')!=fw or b.get('source_period')!=[c['period_start'],c['reporting_period']]:
            raise ReviewRequired('Borrowing entity/framework/period/currency mismatch')
        role=enum(b,'role',{'specific','general'})
        if role=='specific' and b.get('project_id')!=p['id']:raise ReviewRequired('Specific borrowing is not designated to actual project')
        if flag(b,'complex_features') or flag(b,'tax_exempt') or nonnegative(b['fees']) or nonnegative(b['fx_adjustment']):
            raise ReviewRequired('FX, fees, complex or tax-exempt financing needs separately governed method')
        principal=nonnegative(b['opening_principal']);events=rows(b['events']);inventory(b,'event_inventory',events);flows={}
        for e in events:
            approval(e,c);d=inperiod(c,e['date']);enum(e,'kind',{'draw','repayment'})
            amount=nonnegative(e['amount']);flows[d]=flows.get(d,ZERO)+(amount if e['kind']=='draw' else -amount)
        segs=rows(b['segments'],False);inventory(b,'segment_inventory',segs);last=start;loan_total=ZERO;loan_income=ZERO
        for s in segs:
            reviewed(s,c,'rate_memo');lo=iso(s['start']);hi=iso(s['end']);rate=fraction(s['annual_rate']);basis=enum(s,'day_basis',{'actual_actual','actual_365','actual_360'})
            if lo!=last or hi<lo or hi>end:raise ReviewRequired('Financing segments gap/overlap/cutoff')
            if dec(s['effective_annual_rate'])!=rate:raise ReviewRequired('Coupon/EIR difference requires financing-owner eligible-cost method')
            subtotal=ZERO;inc=nonnegative(s['investment_income'])
            if fw=='US_GAAP' and inc:raise ReviewRequired('US investment income separately owned; no deduction supported in this route')
            for offset in range((hi-lo).days+1):
                d=lo+timedelta(days=offset);principal+=flows.get(d,ZERO)
                if principal<0:raise ReviewRequired('Repayment exceeds outstanding borrowing')
                interest=principal*rate*day_fraction(d,basis);subtotal+=interest
                daily_income=inc/Decimal((hi-lo).days+1)
                if daily_income>interest:raise ReviewRequired('Unsupported investment income exceeds specific financing cost')
                if inc and role!='specific':raise ReviewRequired('Only specific temporary investment income supported')
                borrowed[d].append(dict(role=role,principal=principal,interest=interest,income=daily_income))
            agree(s['actual_interest'],subtotal,'Dated contract interest accrual')
            loan_total+=subtotal;loan_income+=inc;last=hi+timedelta(days=1)
        if last!=end+timedelta(days=1):raise ReviewRequired('Complete annual financing segments required')
        agree(b['closing_principal'],principal,'Draw/repayment/lender closing bridge')
        agree(b['interest_source_total'],loan_total,'Complete financing source interest')
        agree(b['cashflow_interest_total'],loan_total,'Actual financing interest cash-flow/accrual source')
        actual_interest+=loan_total;income_total+=loan_income
    if sum(b['role']=='specific' for b in loans)>1:raise ReviewRequired('Multiple specific loans require independently governed allocation ordering')
    general_total=sum((r['interest'] for values in borrowed.values() for r in values if r['role']=='general'),ZERO)
    general_weighted_principal=sum((r['principal']*day_fraction(d,'actual_actual') for d,values in borrowed.items() for r in values if r['role']=='general'),ZERO)
    period_general_rate=general_total/general_weighted_principal if general_weighted_principal else ZERO
    expenditure=opening;capital=ZERO;schedule=[];eligible_interest=ZERO;general_numerator=ZERO;general_denominator=ZERO
    for d,state in days.items():
        expenditure+=changes.get(d,ZERO)
        if expenditure<0:raise ReviewRequired('Refund exceeds supported project expenditure')
        specific=[r for r in borrowed[d] if r['role']=='specific'];general=[r for r in borrowed[d] if r['role']=='general']
        incurred=sum((r['interest'] for r in borrowed[d]),ZERO)
        general_numerator+=sum((r['interest'] for r in general),ZERO);general_denominator+=sum((r['principal'] for r in general),ZERO)
        value=ZERO;rate=ZERO
        if state in {'active','temporary'} and expenditure>0 and incurred>0 and election=='capitalize':
            base=expenditure+prior_cost+capital if fw=='UK_GAAP' else expenditure
            value,rate=(us_day(base,specific,general,period_general_rate*day_fraction(d,'actual_actual')) if fw=='US_GAAP' else ifrs_day(base,specific,general,period_general_rate*day_fraction(d,'actual_actual')))
            eligible_interest+=incurred
        capital+=value
        schedule.append(dict(date=d.isoformat(),expenditure=expenditure,state=state,interest=incurred,capitalized=value,general_daily_rate=rate))
    uncapped=capital;capital=cash(min(capital,actual_interest));actual_interest=cash(actual_interest);expense=actual_interest-capital
    agree(c['financing_gl_interest'],actual_interest,'Underlying financing expense source/GL')
    agree(p['expected_capitalized'],capital,'Capitalization workpaper')
    agree(c['expected_expense'],expense,'Borrowing cost expense bridge')
    agree(p['closing_expenditure'],opening+net,'Closing actual asset expenditure')
    agree(p['asset_opening'],opening+prior_cost,'Opening CIP/source')
    agree(p['asset_closing'],opening+prior_cost+net+capital,'CIP capitalized cost rollforward')
    stocks(c,{'Construction asset':(opening+prior_cost+net,opening+prior_cost+net+capital),'Interest expense':(actual_interest,expense)})
    population(c,rs,[opening+net])
    entries=[journal(('Dr','Construction asset',capital),('Cr','Interest expense',capital))] if capital else []
    calcs=dict(method='US avoidable interest' if fw=='US_GAAP' else 'UK elected cost model' if fw=='UK_GAAP' else 'Direct attribution',borrowing_cost_incurred=actual_interest,capitalized=capital,expense=expense,investment_income=cash(income_total),unrounded_capitalization=uncapped,period_constraint_or_rounding=capital-uncapped,opening_capitalized=prior_cost,closing_capitalized=prior_cost+capital,expenditure_additions=cash(net),timeline=schedule,capitalization_rate=period_general_rate)
    return complete(c,'Reviewed borrowing costs allocated and reconciled to construction asset and finance expense',calcs,entries,
        ['Single independently scoped domestic tangible construction object; capitalization begins only with actual expenditure, borrowing cost and development activity',
         'Financing recognition remains with the financing owner; only the expense-to-asset allocation is proposed here',
         'FX, fee/EIR differences, tax-exempt financing, shared components, non-PPE assets, abandonment and other periods require qualified specialist methods'])
