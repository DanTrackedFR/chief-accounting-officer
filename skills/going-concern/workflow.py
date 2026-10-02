from reporting_accounting import *

def assess(c,claims):
    common(c,'assessment','scenarios','debt','plans','sensitivities','management_review','handoffs','scenario_inventory','debt_inventory')
    a=c['assessment'];policy(c,a);required(a,'authorization_date','issuance_date','horizon_end','opening_available_cash','unavailable_cash','cash_gl','basis','liquidation_intent','realistic_alternative','conditions_memo')
    auth=iso(a['authorization_date']);issue=iso(a['issuance_date']);end=iso(a['horizon_end']);report=iso(c['reporting_period']);fw=c['framework']
    if auth<report or issue<report or auth>iso(c['execution_date']) or issue>iso(c['execution_date']):raise ReviewRequired('Authorization/issuance window inconsistent with evidence cutoff')
    anchor=issue if fw=='US_GAAP' else auth if fw=='UK_GAAP' else report
    if end<anniversary(anchor):raise ReviewRequired('Forecast horizon shorter than applicable framework minimum')
    if a['basis']!='going_concern' or flag(a,'liquidation_intent') or not flag(a,'realistic_alternative'):raise ReviewRequired('Non-going-concern/liquidation basis requires separate specialist accounting')
    cash_available=nonnegative(a['opening_available_cash']);unavailable=nonnegative(a['unavailable_cash']);agree(cash_available+unavailable,a['cash_gl'],'Cash availability to GL')
    specialist(c,'cash','Cash reporting',cash_available);specialist(c,'debt','Debt and covenants');specialist(c,'subsequent_events','Financial Statements')
    scenarios=rows(c['scenarios'],False);inventory(c,'scenario_inventory',scenarios);debt=rows(c['debt']);inventory(c,'debt_inventory',debt);plans=rows(c['plans']);sens=rows(c['sensitivities'])
    if sum(1 for s in scenarios if s['kind']=='base')!=1 or not any(s['kind']=='downside' for s in scenarios):raise ReviewRequired('Independent base and downside scenarios required')
    debt_dates={}
    for d in debt:
        reviewed(d,c,'agreement','classification_memo','covenant_memo');required(d,'maturity','principal','breach','waiver_effective','payable_on_demand','coverage_by_scenario')
        due=iso(d['maturity']);principal=nonnegative(d['principal']);breach=flag(d,'breach');demand=flag(d,'payable_on_demand')
        if principal and (demand or due<=report):raise ReviewRequired('Positive opening on-demand/overdue debt requires specialist immediate-call/default liquidity method; monthly term-debt route cannot infer settlement timing')
        if breach:
            if not d['waiver_effective']:raise ReviewRequired('Breach requires documented covenant/waiver specialist assessment')
            iso(d['waiver_effective'])
        if not isinstance(d['coverage_by_scenario'],dict) or set(d['coverage_by_scenario'])!={s['id'] for s in scenarios}:raise ReviewRequired('Complete scenario covenant inventory required for every debt')
        for ids in d['coverage_by_scenario'].values():
            if not isinstance(ids,list) or len(ids)!=len(set(ids)):raise ReviewRequired('Covenant test inventory malformed')
        debt_dates[d['id']]=(due,principal,demand)
        if demand and due>report:raise ReviewRequired('Demand debt liquidity date cannot be deferred to contractual maturity')
    pmap={p['id']:p for p in plans}
    for p in plans:
        reviewed(p,c,'management_intent','feasibility_memo','commitment_evidence');required(p,'available_date','amount','committed','within_control','probable_implementation','probable_mitigation')
        iso(p['available_date']);nonnegative(p['amount'])
        for k in ['committed','within_control','probable_implementation','probable_mitigation']:flag(p,k)
    schedule=[];source=[];base_min=None;stress_min=None
    for s in scenarios:
        reviewed(s,c,'forecast_source','assumption_memo','board_review');required(s,'kind','periods','minimum_reserve','gl_opening_cash','expected_min_before','expected_min_after')
        if s['kind'] not in ['base','downside']:raise ReviewRequired('Unsupported scenario kind')
        agree(s['gl_opening_cash'],cash_available,'Scenario opening cash');periods=rows(s['periods'],False);dates=[iso(p['date']) for p in periods]
        if dates!=sorted(set(dates)) or dates[0]<=report or dates[-1]<end:raise ReviewRequired('Forecast timing/population does not cover complete horizon')
        # Forecast rows are end-of-month; prohibit skipped liquidity months.
        previous=report
        for d in dates:
            if (d.year*12+d.month)-(previous.year*12+previous.month)!=1 or d.day!=monthrange(d.year,d.month)[1]:raise ReviewRequired('Forecast must cover each consecutive month end')
            previous=d
        before=cash_available;after=cash_available;res=nonnegative(s['minimum_reserve']);minbefore=before-res;minafter=after-res;usedplans=set();debt_paid={id:ZERO for id in debt_dates};trace=[];first_exhaustion=None;tested={id:set() for id in debt_dates};cash_date=report
        for r in periods:
            reviewed(r,c,'source_memo','intra_period_timing_memo');required(r,'date','receipts','payments','debt_payments','plan_draws','expected_before','expected_after','covenants','intra_period_min_before','intra_period_min_after')
            receipt=nonnegative(r['receipts']);payment=nonnegative(r['payments']);dt=iso(r['date']);dps=rows(r['debt_payments']);draws=rows(r['plan_draws']);debtcash=ZERO;plancash=ZERO
            for dp in dps:
                required(dp,'debt_id','amount','date')
                if dp['debt_id'] not in debt_dates:raise ReviewRequired('Forecast debt payment absent from debt register')
                paid_date=iso(dp['date'])
                if not cash_date<paid_date<=dt or paid_date>debt_dates[dp['debt_id']][0]:raise ReviewRequired('Debt payment timing misses forecast interval or contractual due date')
                n=nonnegative(dp['amount']);debt_paid[dp['debt_id']]+=n;debtcash+=n
                if debt_paid[dp['debt_id']]>debt_dates[dp['debt_id']][1]:raise ReviewRequired('Debt principal cash exceeds confirmed register')
            for id,(due,n,demand) in debt_dates.items():
                if due<=dt and debt_paid[id]<n:raise ReviewRequired('Debt maturity/on-demand cash omitted from forecast')
            for dr in draws:
                required(dr,'plan_id','amount','date')
                if dr['plan_id'] not in pmap or dr['plan_id'] in usedplans:raise ReviewRequired('Missing or repeated mitigation draw')
                p=pmap[dr['plan_id']];n=nonnegative(dr['amount']);usedplans.add(p['id'])
                draw_date=iso(dr['date'])
                if not cash_date<draw_date<=dt or draw_date<iso(p['available_date']) or n>nonnegative(p['amount']):raise ReviewRequired('Mitigation amount/timing exceeds evidence')
                if not p['committed'] or not p['within_control'] or fw=='US_GAAP' and not (p['probable_implementation'] and p['probable_mitigation']):raise ReviewRequired('Uncommitted/infeasible plan cannot supply assumed funding')
                plancash+=n
            opening_before=before;opening_after=after
            before+=receipt-payment-debtcash;after+=receipt-payment-debtcash+plancash;agree(r['expected_before'],before,'Pre-plan liquidity');agree(r['expected_after'],after,'Post-plan liquidity')
            intrab=dec(r['intra_period_min_before']);intraa=dec(r['intra_period_min_after'])
            if intrab>min(opening_before,before) or intraa>min(opening_after,after):raise ReviewRequired('Intra-period cash minimum cannot exceed opening/closing cash')
            minbefore=min(minbefore,intrab-res);minafter=min(minafter,intraa-res)
            if intrab<res and first_exhaustion is None:first_exhaustion=r['date']
            cvs=rows(r['covenants'])
            for cv in cvs:
                required(cv,'debt_id','numerator','denominator','limit','comparison','compliant','waiver_memo')
                if cv['debt_id'] not in debt_dates:raise ReviewRequired('Covenant lacks debt reference')
                if cv['id'] in tested[cv['debt_id']]:raise ReviewRequired('Duplicate covenant test')
                tested[cv['debt_id']].add(cv['id'])
                ratio=dec(cv['numerator'])/positive(cv['denominator']);limit=dec(cv['limit']);comparison=cv['comparison']
                if comparison not in ['minimum','maximum']:raise ReviewRequired('Covenant inequality unresolved')
                actual=ratio>=limit if comparison=='minimum' else ratio<=limit
                if flag(cv,'compliant')!=actual:raise ReviewRequired('Covenant ratio conclusion conflicts with calculation')
                if not actual:texts(cv,'waiver_memo');specialist(c,'covenant_breach','Debt and covenants')
            trace.append({'date':r['date'],'before_plans':cash(before),'after_plans':cash(after),'plan_funding':cash(plancash),'headroom':cash(after-res)})
            source.append(r)
            cash_date=dt
        for d in debt:
            if tested[d['id']]!=set(d['coverage_by_scenario'][s['id']]):raise ReviewRequired('Forecast omits required covenant tests')
        agree(s['expected_min_before'],minbefore,'Minimum pre-plan headroom');agree(s['expected_min_after'],minafter,'Minimum post-plan headroom')
        if s['kind']=='base':base_min=minbefore
        else:stress_min=minafter if stress_min is None else min(stress_min,minafter)
        schedule.append({'id':s['id'],'kind':s['kind'],'minimum_before':cash(minbefore),'minimum_after':cash(minafter),'first_reserve_shortfall_period_before_plans':first_exhaustion,'forecast':trace})
    for x in sens:
        reviewed(x,c,'basis_memo');required(x,'base_receipts','reduction_fraction','incremental_cost','expected_reduction')
        loss=cash(nonnegative(x['base_receipts'])*fraction(x['reduction_fraction'])+nonnegative(x['incremental_cost']));agree(x['expected_reduction'],loss,'Forecast sensitivity')
    review=c['management_review'];reviewed(review,c,'basis_memo','uncertainty_memo','plan_evaluation');required(review,'material_uncertainty','substantial_doubt_before','substantial_doubt_alleviated','significant_judgment')
    for k in ['material_uncertainty','substantial_doubt_before','substantial_doubt_alleviated','significant_judgment']:flag(review,k)
    if fw=='US_GAAP':
        if base_min<0 and not review['substantial_doubt_before']:raise ReviewRequired('Negative pre-plan cash needs substantial-doubt evaluation')
        if review['substantial_doubt_alleviated'] and (not review['substantial_doubt_before'] or any(s['minimum_after']<0 for s in schedule)):raise ReviewRequired('Substantial doubt alleviation conflicts with supported plan cash')
        tier='substantial_doubt_unalleviated' if review['substantial_doubt_before'] and not review['substantial_doubt_alleviated'] else 'substantial_doubt_alleviated' if review['substantial_doubt_before'] else 'ordinary_review'
    else:
        if any(s['minimum_after']<0 for s in schedule) and not review['material_uncertainty']:raise ReviewRequired('Unfunded downside requires material-uncertainty assessment')
        tier='material_uncertainty' if review['material_uncertainty'] else 'significant_judgment' if review['significant_judgment'] else 'ordinary_review'
    population(c,source,[nonnegative(r['receipts'])+nonnegative(r['payments'])+sum((nonnegative(d['amount']) for d in r['debt_payments']),ZERO) for r in source])
    return finish('Framework horizon, forecasts, maturities and supported management plans assessed.',{'horizon_end':a['horizon_end'],'available_cash':cash_available,'scenarios':schedule,'disclosure_tier':tier,'sensitivity_reductions':[cash(x['expected_reduction']) for x in sens]},[],
      ['Forecasts, commitments and management intent are supplied independently evidenced judgments, not generated predictions.','Later waiver can affect liquidity without curing reporting-date debt classification.'],
      ['Basis, significant judgment/material uncertainty or ASC205-40 substantial doubt, plans and dependencies, debt covenants and subsequent events.'])
