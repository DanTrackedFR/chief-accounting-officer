from reporting_accounting import *

def assess(c,claims):
    common(c,'change','affected_periods','adjustments','materiality','sec','handoffs','period_inventory','error_register')
    ch=c['change'];policy(c,ch);required(ch,'kind','discovery_date','original_information_available','new_information','mandatory','specific_transition','transition_route','permitted_change','impracticable','impracticability_memo','earliest_practicable','original_authorization','information_date')
    discovery=iso(ch['discovery_date']);info=iso(ch['information_date']);auth=iso(ch['original_authorization']);kind=ch['kind'];fw=c['framework']
    if discovery>iso(c['execution_date']) or info>discovery:raise ReviewRequired('Accounting change discovery/information chronology inconsistent')
    old=flag(ch,'original_information_available');new=flag(ch,'new_information');mandatory=flag(ch,'mandatory');impractical=flag(ch,'impracticable')
    if kind=='estimate':
        if old or not new or info<=auth:raise ReviewRequired('Prior available information cannot be recast as a new estimate')
        route='prospective'
    elif kind=='error':
        if not old or info>auth:raise ReviewRequired('Proven prior error requires information available at original authorization')
        route='retrospective'
    elif kind in ['policy','estimate_effected_by_principle']:
        if kind=='estimate_effected_by_principle' and fw!='US_GAAP':raise ReviewRequired('ASC250 hybrid depreciation-method route requires US applicability')
        if not flag(ch,'permitted_change'):raise ReviewRequired('Policy change lacks permitted/preferable basis')
        if kind=='estimate_effected_by_principle':route='prospective'
        elif mandatory:
            if not flag(ch,'specific_transition'):raise ReviewRequired('Mandatory adoption requires specific-standard transition analysis')
            specialist(c,'transition','Transaction standard transition');route=ch['transition_route']
            if route not in ['retrospective','modified_retrospective','prospective']:raise ReviewRequired('Specific transition route unsupported')
        else:route='retrospective'
    else:raise ReviewRequired('Policy/estimate/error classification unresolved')
    if impractical:
        texts(ch,'impracticability_memo');iso(ch['earliest_practicable'])
        if fw=='US_GAAP' and kind=='error':raise ReviewRequired('Do not import IFRS impracticability relief into US error correction')
        specialist(c,'practicability','Technical accounting practicability')
    materiality=c['materiality'];reviewed(materiality,c,'qualitative_memo','aggregation_memo','interim_memo')
    for k in ['prior_material','current_if_corrected_material','current_uncorrected_material','interim_review_complete']:flag(materiality,k)
    if not materiality['interim_review_complete']:raise ReviewRequired('Interim/full-year effects require separate review')
    periods=rows(c['affected_periods'],False);inventory(c,'period_inventory',periods);adjustments=rows(c['adjustments']);error_rows=rows(c['error_register']);sec=c['sec'];required(sec,'registrant','auditor_notice');registrant=flag(sec,'registrant');notice=flag(sec,'auditor_notice')
    if registrant and fw!='US_GAAP':raise ReviewRequired('SEC US-GAAP issuer method requires correct filer framework')
    prior_material=materiality['prior_material'];filing='not_applicable'
    if kind=='error' and registrant:
        reviewed(sec,c,'filer_type','counsel_memo','auditor_memo','authorized_governance_memo');specialist(c,'sec','SEC securities counsel')
        if sec['filer_type']!='domestic':raise ReviewRequired('Foreign-private issuer requires separate form/filing method')
        if prior_material:filing='Big_R_reissuance';route='retrospective'
        elif materiality['current_if_corrected_material'] or materiality['current_uncorrected_material']:filing='little_r_revision';route='retrospective'
        else:filing='out_of_period_review';route='current'
        required(sec,'nonreliance_date','filing_plan','icfr_clawback_review')
        texts(sec,'filing_plan','icfr_clawback_review')
        if prior_material:
            nonreliance=iso(sec['nonreliance_date'])
            if nonreliance>iso(c['execution_date']) or nonreliance<discovery:raise ReviewRequired('Authorized non-reliance chronology requires counsel resolution')
        if notice:specialist(c,'auditor_notice','SEC securities counsel')
    elif kind=='error' and not prior_material:
        specialist(c,'immaterial','Technical accounting materiality');route='current' if not materiality['current_if_corrected_material'] and not materiality['current_uncorrected_material'] else 'retrospective'
    if registrant and kind=='policy':specialist(c,'preferability','SEC securities counsel')
    specialist(c,'tax','Tax and EPS');specialist(c,'underlying','Underlying transaction accounting')
    if kind=='error' and not error_rows:raise ReviewRequired('Error evaluation requires a complete independently reviewed error register')
    entries=[];work=[];equity_change=ZERO;profit_change=ZERO;prior_effects=[];transition_effect=ZERO;current_profits=[]
    byperiod={p['id']:p for p in periods};deltas={id:{} for id in byperiod}
    for a in adjustments:
        reviewed(a,c,'source_memo');required(a,'period_id','lines','layer')
        if a['period_id'] not in byperiod:raise ReviewRequired('Correction period missing from complete population')
        p=byperiod[a['period_id']];end=iso(p['period_end']);start=iso(p['period_start'])
        if start>end or end>iso(c['reporting_period']):raise ReviewRequired('Correction period chronology unresolved')
        if a['layer'] not in ['comparative_profit','earliest_opening','current_profit','transition_opening']:raise ReviewRequired('Correction layer unresolved')
        if (a['layer'] in ['earliest_opening','transition_opening'])!=flag(p,'opening_equity_effect'):raise ReviewRequired('Correction layer conflicts with period opening-equity disposition')
        if route in ['prospective','current'] and end<iso(c['period_start']):raise ReviewRequired('Prospective/current method cannot alter an issued prior period')
        if route=='modified_retrospective' and end!=iso(c['period_start']):raise ReviewRequired('Modified transition adjusts specified opening layer only')
        if impractical and end<iso(ch['earliest_practicable']):raise ReviewRequired('Correction predates supported earliest practicable date')
        if not isinstance(a['lines'],list) or not a['lines']:raise ReviewRequired('Balanced correction lines required')
        balance(a['lines']);entries.append(a['lines'])
        for l in a['lines']:
            id=l['account'];deltas[p['id']][id]=deltas[p['id']].get(id,ZERO)+dec(l['amount'])*(1 if l['side']=='Dr' else -1)
    for p in periods:
        reviewed(p,c,'issued_version','statement_memo','comparative_memo');required(p,'period_start','period_end','lines','expected_corrected','opening_equity_effect','issued')
        orig=rows(p['lines'],False);original={l['id']:dec(l['balance']) for l in orig};types={l['id']:l['category'] for l in orig}
        flag(p,'issued')
        if any(t not in ['asset','liability','equity','revenue','expense'] for t in types.values()):raise ReviewRequired('Correction statement classification unresolved')
        if not set(deltas[p['id']])<=set(original):raise ReviewRequired('Journal offset absent from period statement population')
        agree(sum(original.values(),ZERO),0,'Original TB');corrected={id:original[id]+deltas[p['id']].get(id,ZERO) for id in original};agree(sum(corrected.values(),ZERO),0,'Corrected TB')
        if set(p['expected_corrected'])!=set(corrected):raise ReviewRequired('Corrected line inventory incomplete')
        for id,n in corrected.items():agree(p['expected_corrected'][id],n,'Corrected line '+id)
        profit_before=-sum((n for id,n in original.items() if types[id] in ['revenue','expense']),ZERO);profit_after=-sum((n for id,n in corrected.items() if types[id] in ['revenue','expense']),ZERO)
        net=-sum((delta for id,delta in deltas[p['id']].items() if types[id] in ['revenue','expense','equity']),ZERO)
        if iso(p['period_end'])<iso(c['period_start']):prior_effects.append((iso(p['period_end']),net))
        elif flag(p,'opening_equity_effect'):
            if p['period_start']!=c['period_start'] or p['period_end']!=c['period_start']:raise ReviewRequired('Current opening layer must be a point at period start')
            transition_effect+=net
        else:current_profits.append((iso(p['period_end']),profit_after-profit_before))
        if flag(p,'opening_equity_effect'):
            if any(types[id] in ['revenue','expense'] and delta for id,delta in deltas[p['id']].items()):raise ReviewRequired('Earliest-opening correction cannot also charge comparative P&L')
        if route=='prospective' and p['opening_equity_effect']:raise ReviewRequired('Estimate change cannot adjust opening equity')
        required(p,'weighted_shares','original_eps','corrected_eps','eps_applicable')
        eps=None
        if flag(p,'eps_applicable'):
            shares=positive(p['weighted_shares']);eps=cash(profit_after/shares);agree(p['original_eps'],profit_before/shares,'Original basic EPS');agree(p['corrected_eps'],eps,'Corrected basic EPS')
        work.append({'id':p['id'],'period_end':p['period_end'],'original':original,'corrected':corrected,'original_profit':profit_before,'corrected_profit':profit_after,'equity_effect':net,'basic_eps':eps})
    if prior_effects:
        latest=max(d for d,n in prior_effects);values={n for d,n in prior_effects if d==latest}
        if len(values)!=1:raise ReviewRequired('Annual/interim corrected closing equity disagrees')
        equity_change=next(iter(values))
    equity_change+=transition_effect
    if current_profits:
        latest=max(d for d,n in current_profits);values={n for d,n in current_profits if d==latest}
        if len(values)!=1:raise ReviewRequired('Current annual/interim profit correction conflicts')
        profit_change=next(iter(values))
    required(c,'opening_equity_bridge');eq=c['opening_equity_bridge'];agree(dec(eq['original'])+equity_change,eq['corrected'],'Corrected prior close to current opening equity')
    rollover=ZERO;iron=ZERO;gross=ZERO
    for e in error_rows:
        reviewed(e,c,'qualitative_memo');required(e,'current_earnings_effect','ending_balance_effect');rollover+=dec(e['current_earnings_effect']);iron+=dec(e['ending_balance_effect']);gross+=abs(dec(e['ending_balance_effect']))
    population(c,adjustments,[sum((dec(l['amount']) for l in a['lines'] if l['side']=='Dr'),ZERO) for a in adjustments])
    return finish('Accounting change route and original-to-corrected periods reconcile.',{'route':route,'periods':work,'opening_equity_change':equity_change,'current_profit_change':profit_change,'rollover':rollover,'iron_curtain':iron,'gross_balance_error':gross,'sec_route':filing,'item_402_review':registrant and kind=='error' and (prior_material or notice)},entries,
      ['Materiality is a reviewed quantitative/qualitative and aggregate judgment, never an automatic percentage.','Counsel owns Item4.02/non-reliance, deadlines and filings; accounting workflow does not file or make legal determinations.'],
      ['Nature/reason, by-period lines/tax/basic and diluted EPS, earliest equity, impracticability/transition, interim effects, SEC revisions/restatements and ICFR/clawback review.'])
