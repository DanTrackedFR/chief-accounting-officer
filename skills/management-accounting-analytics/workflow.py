"""Reconciled controllership facts, never fabricated FP&A explanations."""
from governance_accounting import *
KEYS=('accounts','account_source','documents','imports','bridge_items','bridge_inventory','explanations','explanation_inventory','reconciliations','reconciliation_inventory','governance_method','diagnostic')
def assess(c,claims):
    rs,docs=start(c,'accounts');p=c['governance_method']
    if any(flag(p,k) for k in ('budgeting','forecasting','investment_analysis','commercial_planning','generic_bi','manufactured_explanations','automatic_gl_correction')):raise ReviewRequired('Accounting analytics cannot become FP&A/BI or manufacture explanations/entries')
    enum(p,'comparison_basis',{'prior_year_calendar_balance','prior_month_calendar_balance'});texts(p,'currency','signed_convention','metric_dictionary','threshold_memo')
    independent_population(c,'account_source',rs,('account','currency','current_source_doc','prior_source_doc'))
    if len({r['account'] for r in rs})!=len(rs):raise ReviewRequired('Duplicate accounting metric/account')
    bridge=pack(c,'bridge_items','bridge_inventory');explanations=pack(c,'explanations','explanation_inventory');rec=pack(c,'reconciliations','reconciliation_inventory')
    bby={};eby={};used_bridge=set();used_explanation=set();totals=dict(current_management=ZERO,current_statutory=ZERO,prior_statutory=ZERO,gross_movement=ZERO,gross_statutory=ZERO)
    for b in bridge:
        if b['account'] not in {r['account'] for r in rs}:raise ReviewRequired('Orphan management/statutory bridge')
        enum(b,'classification',{'owner_accounting_adjustment'})
        sign=b['sign']
        if type(sign) is not int or sign not in (-1,1):raise ReviewRequired('Bridge sign must be actual reviewed accounting mapping')
        imp=accounting_owner(c,b['owner_import']);basis=dict(b,amount=dec(b['amount'])*sign)
        owner_assertion(c,basis);texts(b,'rationale','mapping_memo')
        identity=(b['owner_import'],tuple(b['result_path']))
        if identity in used_bridge:raise ReviewRequired('Actual owner bridge counted twice')
        used_bridge.add(identity);bby[b['account']]=bby.get(b['account'],ZERO)+dec(b['amount'])
    for e in explanations:
        texts(e,'account','interpretation_memo');actual=doc(docs,e['driver_doc'])['content']
        if not isinstance(actual,dict) or actual['account']!=e['account'] or actual['period']!=[c['period_start'],c['reporting_period']]:raise ReviewRequired('Variance explanation source scope mismatch')
        drivers=rows(actual['drivers'],False);inventory(actual,'driver_inventory',drivers)
        if any((e['driver_doc'],x['id']) in used_explanation for x in drivers):raise ReviewRequired('Variance drivers counted twice')
        for x in drivers:used_explanation.add((e['driver_doc'],x['id']))
        exact(e['amount'],sum((dec(x['amount']) for x in drivers),ZERO),'Actual factual driver decomposition')
        if e['account'] in eby:raise ReviewRequired('Duplicate account variance interpretation')
        eby[e['account']]=dec(e['amount'])
    deltas=[]
    for r in rs:
        texts(r,'account','currency','lineage_memo');enum(r,'metric',{'account_balance'})
        if r['currency']!=p['currency']:raise ReviewRequired('Cannot net/aggregate different currencies')
        current_doc=doc(docs,r['current_source_doc']);prior_doc=doc(docs,r['prior_source_doc'])
        if current_doc['currency']!=r['currency'] or prior_doc['currency']!=r['currency']:raise ReviewRequired('Accounting source metadata currency contradiction')
        current=current_doc['content'];prior=prior_doc['content']
        if current['period']!=[c['period_start'],c['reporting_period']]:raise ReviewRequired('Current accounting source period mismatch')
        if p['comparison_basis']=='prior_year_calendar_balance':comparison(c,prior['period'])
        else:
            from datetime import date,timedelta
            a,b=[date.fromisoformat(x) for x in prior['period']];current_start=date.fromisoformat(c['period_start'])
            if a.day!=1 or current_start.day!=1 or b+timedelta(days=1)!=current_start:raise ReviewRequired('Prior-month accounting comparator period mismatch')
        for data in (current,prior):
            if data['account']!=r['account'] or data['currency']!=r['currency'] or data['posted_only'] is not True or data['signed_convention']!=p['signed_convention']:raise ReviewRequired('Accounting source/report semantic or posted-state mismatch')
            lines=rows(data['records'],False);inventory(data,'inventory',lines)
            if any(x['account']!=r['account'] for x in lines):raise ReviewRequired('Source line account mismatch')
            exact(data['statutory_amount'],sum((dec(x['amount']) for x in lines),ZERO),'Accounting record population')
            exact(data['gross_amount'],sum((abs(dec(x['amount'])) for x in lines),ZERO),'Gross accounting population')
        cur=dec(current['statutory_amount']);old=dec(prior['statutory_amount']);management=dec(current['management_amount'])
        exact(r['amount'],cur,'Report to actual statutory source');exact(r['management_amount'],management,'Report to actual management source')
        exact(management+bby.get(r['account'],ZERO),cur,'Management/statutory bridge')
        delta=cur-old
        if delta!=0 and eby.get(r['account'])!=delta:raise ReviewRequired('Nonzero variance requires exact supported factual decomposition')
        if delta==0 and r['account'] in eby:raise ReviewRequired('Unnecessary/contradictory zero-movement explanation')
        totals['current_management']+=management;totals['current_statutory']+=cur;totals['prior_statutory']+=old;totals['gross_movement']+=abs(delta);totals['gross_statutory']+=dec(current['gross_amount'])
        deltas.append(dict(movement=delta,percentage=None if old==0 else delta/abs(old)*100))
    if set(eby)-{r['account'] for r in rs}:raise ReviewRequired('Orphan variance explanation')
    open_items=[];ontime=0;material_open=0
    original=doc(docs,p['reconciliation_source_doc'])['content'];raw=rows(original['records'],False);inventory(original,'inventory',raw)
    if set(x['id'] for x in raw)!={x['id'] for x in rec}:raise ReviewRequired('Accounting KPI denominator population incomplete')
    by={x['id']:x for x in raw}
    for r in rec:
        if any(r[k]!=by[r['id']][k] for k in ('due_date','completed_on','material','amount')):raise ReviewRequired('KPI row differs from actual source event')
        if not iso(c['period_start'])<=iso(r['due_date'])<=iso(c['execution_date']):raise ReviewRequired('KPI due event outside declared accounting cycle')
        if r['completed_on'] is None:
            if flag(r,'material'):material_open+=1
        else:
            if not iso(c['period_start'])<=iso(r['completed_on'])<=iso(c['execution_date']):raise ReviewRequired('Future reconciliation completion cannot be a fact')
            if iso(r['completed_on'])<=iso(r['due_date']):ontime+=1
    if material_open:open_items.append('Material incomplete reconciliation prevents clean accounting-quality review')
    enum(p,'kpi',{'on_time_reconciliation_rate'})
    diagnostic = None
    if c.get('diagnostic') is not None:
        import importlib.util
        spec=importlib.util.spec_from_file_location("accounting_diagnostics",ROOT/"skills/management-accounting-analytics/diagnostics.py")
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        diagnose=module.assess
        try:diagnostic = diagnose(c,docs)
        except (ValueError,KeyError,TypeError,AttributeError,ArithmeticError) as exc:
            raise ReviewRequired('Malformed diagnostic source, dimensions or comparator') from exc
        open_items.extend(diagnostic['open_items'])
    balance_diagnostics=None
    if c.get('balance_diagnostics') is not None:
        import importlib.util
        spec=importlib.util.spec_from_file_location('accounting_balance_diagnostics',ROOT/'skills/management-accounting-analytics/diagnostics.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        balance_diagnostics=module.assess_balances(c,docs)
        open_items.extend(balance_diagnostics['open_items'])
    review_release(c,KEYS)
    return output(c,'Controllership accounting-source, bridge and flux workpaper reconciled',dict(**totals,diagnostic=diagnostic,balance_diagnostics=balance_diagnostics,account_movements=deltas,on_time_reconciliation_count=ontime,reconciliation_population=len(rec),on_time_reconciliation_rate=Decimal(ontime)/len(rec)*100,material_open_reconciliations=material_open),['Calculated accounting movements and reconciled KPI facts only. Factual driver evidence is separate from qualified management interpretation; no invented explanations, autonomous budgets/forecasts, investment advice, BI application, automatic GL correction or statutory filing conclusion. Gross exposures remain visible.'],open_items)
