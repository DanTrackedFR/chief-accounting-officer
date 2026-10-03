"""Isolated evidenced index schedule; explicitly not balanced IAS29 statements."""
from special_reporting import *

def assess(c,claims):
    rs=start(c,'items',{'financial-statements'})
    if c['imports']:raise ReviewRequired('No completed hyperinflation statement/FX/consolidation adapter exists in this isolated schedule')
    if c['framework'] not in {'IFRS','AASB'}:raise ReviewRequired('US ASC830 and UK detailed mechanics are outside isolated IAS29/AASB129 index method')
    p=method(c,'inflation_method','Isolated hyperinflation index schedule')
    if enum(p,'scope',{'isolated_schedule'})!='isolated_schedule':raise ReviewRequired('No complete purchasing-power accounting engine')
    texts(p,'functional_currency','economy','economic_evidence','qualitative_indicators','quantitative_indicators','group_consistency_memo','onset_cessation_memo','index_source','index_series','index_revision','classification_memo','equity_memo','income_memo','monetary_result_handoff','translation_handoff','tax_handoff','comparative_memo')
    if not flag(p,'hyperinflation_supported') or flag(p,'threshold_only') or not flag(p,'independent_economic_review'):raise ReviewRequired('Actual period-specific qualitative and quantitative economic assessment required')
    if any(flag(p,k) for k in ('complete_statements_requested','monetary_gain_calculation_requested','translation_requested','consolidation_requested','journal_requested')):raise ReviewRequired('Complete monetary result, statements, translation and journals need separate governed engine')
    indices=rows(c['indices'],False);inventory(c,'index_inventory',indices);by={}
    for r in indices:
        approval(r,c);texts(r,'series','revision','source_url','index_date')
        if r['series']!=p['index_series'] or r['revision']!=p['index_revision']:raise ReviewRequired('Mixed inflation-index series/revisions')
        if iso(r['index_date'])>iso(c['reporting_period']):raise ReviewRequired('Index date after reporting cutoff')
        by[r['id']]=positive(r['value'])
    closing=p['closing_index_id']
    if closing not in by or next(r for r in indices if r['id']==closing)['index_date']!=c['reporting_period']:raise ReviewRequired('Reporting-date general index missing')
    total=ZERO;adjustment=ZERO;summary=[]
    for r in rs:
        texts(r,'classification_evidence','measurement_memo','measurement_date');kind=enum(r,'kind',{'monetary','historical_nonmonetary','current_nonmonetary','equity','income_expense'})
        amount=dec(r['amount']);date=iso(r['measurement_date'])
        if date>iso(c['reporting_period']):raise ReviewRequired('Future measurement population')
        if kind in {'monetary','current_nonmonetary'}:
            if date!=iso(c['reporting_period']):raise ReviewRequired('Earlier current measurement requires a separately qualified schedule')
            value=amount
        else:
            ix=r['index_id']
            if ix not in by or next(i for i in indices if i['id']==ix)['index_date']!=r['measurement_date']:raise ReviewRequired('Index must match exact acquisition/equity/flow measurement date')
            if kind=='income_expense' and not iso(c['period_start'])<=date:raise ReviewRequired('Income/expense source outside reporting period')
            value=amount*by[closing]/by[ix]
        exact(r['expected_restated'],value,'Isolated item index result')
        total+=abs(amount);adjustment+=value-amount
        summary.append(dict(kind=kind,original=amount,index_restated=value,adjustment=value-amount))
    population(c,rs,[abs(dec(r['amount'])) for r in rs])
    return no_posting(c,'Isolated hyperinflation assessment/index workpaper reconciled',dict(items=summary,isolated_adjustment=adjustment,full_statement_result=False),['Actual qualified economy assessment and dated general-index evidence; monetary/current balances not blindly indexed'],['This isolated schedule is not a complete restated trial balance, purchasing-power gain/loss, equity/earnings statement, tax or comparative package. No balancing gain, journal or FX/consolidation result is created. Existing FX and Consolidation hyperinflation boundaries remain intact.'])
