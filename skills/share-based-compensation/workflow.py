"""Award/tranche service attribution; external valuations and legal classification."""
from core_accounting import cash, dec, required, ReviewRequired, journal
from production import flag, fraction, nonnegative
from advanced_accounting import gate, unique, positive, event_date, movement, result, ZERO

def assess(c,claims):
    gate(c,'award','tranches','schedule','event')
    a=c['award'];required(a,'classification','grant_date','grant_date_memo','valuation_inputs','valuation_review','conditions_memo',
      'conditions','forfeiture_policy','classification_memo','ordinary_employee_award','group_arrangement','withholding_feature')
    event_date(c,a['grant_date'])
    if not flag(a,'ordinary_employee_award') or flag(a,'group_arrangement') or flag(a,'withholding_feature'):
        raise ReviewRequired('Profits interests, nonemployee/group awards and withholding classification require specialist scope method')
    if a['classification'] not in ('equity','cash'):raise ReviewRequired('Settlement obligation/classification unresolved')
    if a['conditions'] not in ('service','service_nonmarket','service_market'):
        raise ReviewRequired('Nonvesting or mixed conditions require specialist valuation/vesting analysis')
    if a['forfeiture_policy'] not in ('estimate','actual'):raise ReviewRequired('Forfeiture policy unresolved')
    if c['framework']!='US_GAAP' and a['forfeiture_policy']!='estimate':raise ReviewRequired('US actual-forfeiture election is not a global policy')
    for k in ('model','share_price','exercise_price','volatility','risk_free_rate','expected_term','dividend_yield','market_condition_treatment'):
        required(a['valuation_inputs'],k)
    if not flag(a,'valuation_review_complete'):raise ReviewRequired('Grant/current fair values need reviewed valuation support')
    unique(c['tranches']);tranches={t['id']:t for t in c['tranches']}
    for t in tranches.values():
        required(t,'granted','grant_fair_value','vesting_date','service_attribution_memo')
        positive(t['granted']);nonnegative(t['grant_fair_value']);event_date(c,t['vesting_date']) if t['vesting_date']<=c['reporting_period'] else None
        if t['vesting_date']<a['grant_date']:raise ReviewRequired('Vesting precedes grant')
    required(a,'opening_cumulative','opening_balance_memo')
    unique(c['schedule'],'date');previous_date=max(a['grant_date'],c['period_start']);previous=cash(nonnegative(a['opening_cumulative']));rows=[];entries=[];last_quantities={}
    for row in c['schedule']:
        required(row,'tranches','opening_booked','memo')
        event_date(c,row['date'])
        if row['date']<previous_date:raise ReviewRequired('Award schedule is not chronological')
        if cash(nonnegative(row['opening_booked']))!=previous:raise ReviewRequired('Opening award expense/liability does not tie to preceding schedule')
        if set(row['tranches'])!=set(tranches):raise ReviewRequired('Tranche population incomplete')
        cumulative=ZERO;parts={}
        for tid,t in tranches.items():
            x=row['tranches'][tid];required(x,'expected_vesting','actual_forfeited','progress','nonmarket_met','market_met','current_fair_value')
            granted=nonnegative(t['granted']);expected=nonnegative(x['expected_vesting']);forfeited=nonnegative(x['actual_forfeited'])
            if max(expected,forfeited)>granted:raise ReviewRequired('Vesting/forfeitures exceed grants')
            if expected>granted-forfeited:raise ReviewRequired('Expected vesting exceeds nonforfeited grants')
            progress=fraction(x['progress'])
            if row['date']>=t['vesting_date'] and progress!=1:raise ReviewRequired('Vesting-date service progress must be complete')
            if row['date']>=t['vesting_date'] and expected!=granted-forfeited:raise ReviewRequired('Final vesting count must reconcile to actual forfeitures')
            if row['date']<t['vesting_date'] and progress==1:raise ReviewRequired('Early complete service requires separately reviewed acceleration')
            # Market conditions are in value; failure alone does not reverse earned service.
            flag(x,'market_met');met=flag(x,'nonmarket_met')
            count=granted-forfeited if a['forfeiture_policy']=='actual' else expected
            if a['conditions']=='service_nonmarket' and not met:count=ZERO
            value=nonnegative(t['grant_fair_value']) if a['classification']=='equity' else nonnegative(x['current_fair_value'])
            cost=cash(count*value*progress);cumulative+=cost;parts[tid]=cost;last_quantities[tid]=count
        delta=cumulative-previous
        entries.append(movement('share compensation expense','award equity' if a['classification']=='equity' else 'award liability',delta))
        rows.append({'date':row['date'],'by_tranche':parts,'cumulative':cumulative,'period_expense':delta})
        previous=cumulative;previous_date=row['date']
    e=c['event'];required(e,'kind','date','memo')
    kind=e['kind'];incremental=ZERO;settlement=ZERO;closing=previous
    if kind!='none':
        event_date(c,e['date'])
        if e['date']<previous_date:raise ReviewRequired('Event precedes final schedule row; use event-specific chronological schedule')
        if kind=='beneficial_modification':
            if a['classification']!='equity':raise ReviewRequired('Cash modifications require settlement-date liability valuation')
            required(e,'before_fair_value','after_fair_value','eligible_count','remaining_service_progress','conditions_unchanged','original_probable')
            if not flag(e,'conditions_unchanged') or not flag(e,'original_probable'):
                raise ReviewRequired('Modified vesting/probability requires framework-specific modification analysis')
            count=nonnegative(e['eligible_count'])
            if count>sum(last_quantities.values()):raise ReviewRequired('Modification population exceeds eligible awards')
            incremental=cash(count*max(nonnegative(e['after_fair_value'])-nonnegative(e['before_fair_value']),ZERO)*fraction(e['remaining_service_progress']))
            entries.append(journal(('Dr','share compensation expense',incremental),('Cr','award equity',incremental)))
            closing+=incremental
        elif kind=='cash_settlement':
            if a['classification']!='cash':raise ReviewRequired('Cash settlement of equity award is a repurchase/cancellation, not liability clearing')
            required(e,'amount','settlement_fair_value','fully_vested')
            if not flag(e,'fully_vested'):raise ReviewRequired('Unvested cash settlement needs acceleration analysis')
            if any(e['date']<t['vesting_date'] for t in tranches.values()):raise ReviewRequired('Cash settlement precedes vesting; acceleration method required')
            settlement=cash(nonnegative(e['amount']))
            fv=nonnegative(e['settlement_fair_value']);target=cash(sum(last_quantities.values())*fv)
            if settlement!=target:raise ReviewRequired('Settlement amount differs from reviewed settlement-date valuation')
            entries.append(movement('share compensation expense','award liability',target-previous))
            entries.append(journal(('Dr','award liability',settlement),('Cr','cash',settlement)));closing=ZERO
        elif kind=='cancellation':
            if a['classification']!='equity':raise ReviewRequired('Cash cancellation needs liability/event classification method')
            required(e,'unrecognized_original','payment','repurchase_fair_value','not_forfeiture','remaining_cost_memo')
            if not flag(e,'not_forfeiture'):raise ReviewRequired('Vesting failure is not cancellation acceleration')
            acceleration=cash(nonnegative(e['unrecognized_original']));payment=cash(nonnegative(e['payment']))
            original_total=sum((cash(last_quantities[tid]*nonnegative(t['grant_fair_value'])) for tid,t in tranches.items()),ZERO)
            if acceleration!=max(original_total-previous,ZERO):raise ReviewRequired('Cancellation acceleration does not reconcile to remaining original cost')
            entries.append(journal(('Dr','share compensation expense',acceleration),('Cr','award equity',acceleration)))
            deducted=min(payment,cash(nonnegative(e['repurchase_fair_value'])))
            entries.append(journal(('Dr','award equity',deducted),('Dr','settlement compensation expense',payment-deducted),('Cr','cash',payment)))
            closing+=acceleration-deducted;settlement=payment
        else:raise ReviewRequired('Replacement, cash/equity conversion or settlement alternatives require specialist method')
    return result('Reviewed award classification, tranche expense and event journals reconcile.',
      {'framework':c['framework'],'classification':a['classification'],'forfeiture_policy':a['forfeiture_policy'],'conditions':a['conditions']},
      {'schedule':rows,'incremental_modification_expense':incremental,'settlement_cash':settlement,'closing_equity_or_liability':closing},
      entries,[a['classification_memo'],a['grant_date_memo'],a['valuation_review'],a['conditions_memo'],e['memo']],
      ['Award terms, classification and vesting conditions','Grant/forfeiture/exercise/expiry populations and weighted values','Valuation model inputs and measurement dates',
       'Expense and equity/liability movements','Unrecognized compensation and remaining service','Modification/cancellation/settlement effects'],
      ['Fair values are external reviewed inputs, not inferred option values. Market conditions do not override service eligibility. Group, profits-interest, withholding, nonemployee and classification-changing awards require specialists.'])
