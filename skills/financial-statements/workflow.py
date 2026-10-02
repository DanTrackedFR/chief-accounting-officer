"""Authorized TB to six-statement/disclosure review pack; not legal filing advice."""
from core_accounting import cash, dec, required, ReviewRequired
from production import flag, nonnegative
from advanced_accounting import gate, unique, event_date, iso, result, ZERO

CATEGORIES={'asset','liability','equity','revenue','expense','oci'}

def statements(tb):
    unique(tb);totals={k:ZERO for k in CATEGORIES};lines={};line_categories={};cash_total=ZERO
    for x in tb:
        required(x,'balance','category','line','source_version','classification_memo','cash_account')
        if x['category'] not in CATEGORIES:raise ReviewRequired('Unknown statement category')
        b=cash(dec(x['balance']));totals[x['category']]+=b
        if x['line'] in line_categories and line_categories[x['line']]!=x['category']:
            raise ReviewRequired('Statement line collision across categories would cause invalid netting')
        line_categories[x['line']]=x['category']
        lines[x['line']]=lines.get(x['line'],ZERO)+b
        if flag(x,'cash_account'):
            if x['category']!='asset':raise ReviewRequired('Cash mapping requires separately assessed asset/cash convention')
            cash_total+=b
    if sum(totals.values())!=0:raise ReviewRequired('Authorized TB does not balance')
    profit=-(totals['revenue']+totals['expense']);oci=-totals['oci'];equity=-totals['equity']+profit+oci
    if totals['asset']!=-totals['liability']+equity:raise ReviewRequired('Statement equation fails')
    return {'assets':totals['asset'],'liabilities':-totals['liability'],'closing_equity':equity,'revenue':-totals['revenue'],
      'expenses':totals['expense'],'profit':profit,'oci':oci,'comprehensive_income':profit+oci,'cash':cash_total,'lines':lines}

def assess(c,claims):
    gate(c,'presentation','current_tb','comparative_tb','comparative','cash_flow','equity_bridge','notes','checklist','coverage')
    p=c['presentation'];required(p,'model','early_adoption','adoption_memo','business_activity','entity_overlay','classification_review_complete','offsetting_review_complete')
    if not flag(p,'classification_review_complete') or not flag(p,'offsetting_review_complete'):
        raise ReviewRequired('Complete covenant/maturity/current-noncurrent and offsetting-rights review')
    start=iso(c['period_start']);early=flag(p,'early_adoption');fw=c['framework']
    if fw in ('IFRS','AASB'):
        effective=start>=iso('2027-01-01') or early
        expected=('IFRS18' if effective else 'IAS1') if fw=='IFRS' else ('AASB18' if effective else 'AASB101')
        if p['model']!=expected:raise ReviewRequired('Presentation model conflicts with reporting-period/adoption gate')
        if effective:
            required(p,'transition_comparatives_reconciled','mdp_review_complete','category_map_reviewed')
            if not all(flag(p,k) for k in ('transition_comparatives_reconciled','mdp_review_complete','category_map_reviewed')):
                raise ReviewRequired('IFRS18/AASB18 transition, management performance measures and category mapping incomplete')
            if p['business_activity']!='ordinary':raise ReviewRequired('Specified main business activities require IFRS18 category/cash-flow specialist mapping')
    else:
        expected='US_GAAP' if fw=='US_GAAP' else 'FRS102'
        if p['model']!=expected or early:raise ReviewRequired('IFRS18 adoption must not be imported into US/UK GAAP')
        if fw=='UK_GAAP':
            required(p,'statutory_format_version','small_entity_scope','periodic_review_adopted')
            if start>=iso('2026-01-01') and not flag(p,'periodic_review_adopted'):
                raise ReviewRequired('FRS102 2026 Periodic Review adoption unresolved')
            if start>=iso('2027-01-01'):
                required(p,'adapted_formats_2027_review_complete')
                if not flag(p,'adapted_formats_2027_review_complete'):raise ReviewRequired('UK 2027 adapted-format changes not assessed')
    current=statements(c['current_tb']);prior=statements(c['comparative_tb'])
    q=c['comparative'];required(q,'period_end','issued_version','restated_version','adjustments_memo','opening_equity_tie','tax_effects_reviewed')
    if iso(q['period_end'])>=start:raise ReviewRequired('Comparative reporting period must precede current period')
    if not flag(q,'opening_equity_tie') or not flag(q,'tax_effects_reviewed'):
        raise ReviewRequired('Comparative issued-to-restated and tax effects review incomplete')
    eq=c['equity_bridge'];unique(eq);closing_eq=ZERO;eq_profit=ZERO;eq_oci=ZERO;opening_eq=ZERO
    for e in eq:
        required(e,'opening','profit','oci','owner_transactions','retrospective_adjustments','other','closing','memo')
        opening=dec(e['opening']);profit=dec(e['profit']);oci=dec(e['oci']);owner=dec(e['owner_transactions']);adjustment=dec(e['retrospective_adjustments']);other=dec(e['other'])
        if cash(opening+profit+oci+owner+adjustment+other)!=cash(dec(e['closing'])):raise ReviewRequired('Equity component rollforward fails')
        closing_eq+=dec(e['closing']);eq_profit+=profit;eq_oci+=oci;opening_eq+=opening+adjustment
    if cash(closing_eq)!=current['closing_equity'] or cash(eq_profit)!=current['profit'] or cash(eq_oci)!=current['oci']:
        raise ReviewRequired('Equity bridge fails primary-statement income/OCI/closing tie')
    if cash(opening_eq)!=prior['closing_equity']:raise ReviewRequired('Restated comparative equity differs from opening current equity')
    cf=c['cash_flow'];required(cf,'start_subtotal','start_amount','adjustments','investing','financing','fx','opening','closing','balance_sheet_bridge','population_memo','classifications')
    modern=p['model'] in ('IFRS18','AASB18')
    if modern and cf['start_subtotal']!='operating_profit':raise ReviewRequired('IFRS18 indirect method starts with operating profit')
    if cf['start_subtotal'] not in ('profit','profit_before_tax','operating_profit'):raise ReviewRequired('Unknown indirect starting subtotal')
    if fw=='US_GAAP' and cf['start_subtotal']!='profit':raise ReviewRequired('US indirect cash flow starts with net income')
    if cf['start_subtotal']=='profit' and cash(dec(cf['start_amount']))!=current['profit']:raise ReviewRequired('Cash flow starting profit fails P&L tie')
    if cf['start_subtotal']!='profit':
        required(cf,'subtotal_reconciliation','subtotal_memo')
        if cash(dec(cf['start_amount'])+dec(cf['subtotal_reconciliation']))!=current['profit']:
            raise ReviewRequired('Operating/pre-tax subtotal does not reconcile to net profit')
    operating=dec(cf['start_amount'])
    for x in cf['adjustments']:
        required(x,'id','amount','source','noncash_acquisition_fx_excluded','memo')
        if not flag(x,'noncash_acquisition_fx_excluded'):raise ReviewRequired('Working capital/noncash population double-counts acquisition or FX')
        operating+=dec(x['amount'])
    unique(cf['classifications'])
    classified={k:ZERO for k in ('operating','investing','financing')}
    for x in cf['classifications']:
        required(x,'kind','class','amount','memo')
        if x['class'] not in ('operating','investing','financing'):raise ReviewRequired('Cash flow classification unknown')
        classified[x['class']]+=dec(x['amount'])
        if fw=='US_GAAP':
            expected='financing' if x['kind']=='dividends_paid' else 'operating' if x['kind'] in ('interest_paid','interest_received','dividends_received') else x['class']
            if x['class']!=expected:raise ReviewRequired('US interest/dividend cash flow classification mismatch')
        elif modern:
            expected={'interest_paid':'financing','dividends_paid':'financing','interest_received':'investing','dividends_received':'investing'}.get(x['kind'],x['class'])
            if x['class']!=expected:raise ReviewRequired('IFRS18 ordinary-activity interest/dividend classification mismatch')
    if cash(classified['operating'])!=cash(operating) or cash(classified['investing'])!=cash(dec(cf['investing'])) or cash(classified['financing'])!=cash(dec(cf['financing'])):
        raise ReviewRequired('Dated classified cash population does not reconcile to cash flow totals')
    opening=dec(cf['opening']);closing=dec(cf['closing']);bridge=dec(cf['balance_sheet_bridge'])
    if cash(opening+operating+dec(cf['investing'])+dec(cf['financing'])+dec(cf['fx']))!=cash(closing):raise ReviewRequired('Cash flow rollforward fails')
    if cash(closing+bridge)!=current['cash']:raise ReviewRequired('Closing cash-flow/balance-sheet cash bridge fails')
    required(cf,'opening_balance_sheet_bridge')
    if cash(opening+dec(cf['opening_balance_sheet_bridge']))!=prior['cash']:raise ReviewRequired('Opening cash does not tie to comparative cash')
    coverage=c['coverage'];required(coverage,'requirement_population_reviewed','checklist_version','narrative_reviewed','special_topics','complete_sets')
    if not flag(coverage,'requirement_population_reviewed') or not flag(coverage,'narrative_reviewed'):
        raise ReviewRequired('Disclosure/narrative population has not been independently assessed')
    if set(coverage['complete_sets'])!={'balance_sheet','income','comprehensive_income','cash_flow','equity','notes'}:
        raise ReviewRequired('All six statement/note sets must be present')
    needed={'going_concern','subsequent_events','related_parties','segments','eps','tax','leases','acquisitions','financial_instruments','contingencies','share_awards'}
    if set(coverage['special_topics'])!=needed:raise ReviewRequired('Disclosure-only specialist topic population incomplete')
    for topic,x in coverage['special_topics'].items():
        required(x,'decision','memo','evidence')
        if x['decision'] not in ('reviewed','not_applicable'):raise ReviewRequired('Unresolved specialist disclosure: '+topic)
    unique(c['checklist']);required_groups={'balance_sheet','income','comprehensive_income','cash_flow','equity','notes'}
    if not required_groups.issubset({x['group'] for x in c['checklist']}):raise ReviewRequired('Checklist does not cover statement populations')
    for x in c['checklist']:
        required(x,'group','requirement','effective_version','decision','memo','evidence','owner')
        if x['decision'] not in ('satisfied','not_applicable'):raise ReviewRequired('Open disclosure checklist item')
    unique(c['notes'])
    totals={k:v for k,v in current.items() if k!='lines'}
    for n in c['notes']:
        required(n,'target','amount','population_evidence','memo')
        if n['target'] not in totals or cash(dec(n['amount']))!=totals[n['target']]:raise ReviewRequired('Note amount does not tie to primary statement')
    return result('Primary statements, comparatives, equity, cash and disclosure populations reconcile for the reviewed presentation regime.',
      {'framework':fw,'presentation':p['model'],'entity_overlay':p['entity_overlay'],'checklist_version':coverage['checklist_version']},
      {'current':current,'comparative':prior,'equity_components':[{k:e[k] for k in ('id','opening','profit','oci','owner_transactions','retrospective_adjustments','other','closing')} for e in eq],'cash_flow':{'operating':cash(operating),'investing':cash(dec(cf['investing'])),
       'financing':cash(dec(cf['financing'])),'fx':cash(dec(cf['fx'])),'opening':cash(opening),'closing':cash(closing),'bs_cash_bridge':cash(bridge)},'note_tieouts':[{k:n[k] for k in ('id','target','amount')} for n in c['notes']]},[],
      [p['adoption_memo'],q['adjustments_memo'],cf['population_memo']],
      ['Complete period/entity-specific requirement register','Accounting policies and significant judgments/estimation uncertainty',
       'Current/noncurrent, covenant, cash restriction and offsetting assessments','Income/OCI disaggregation and equity components',
       'Cash flow classification and noncash financing movements','Comparative/restatement and adoption reconciliation','Topic-specific notes, events, going concern and filing overlays'],
      ['This is a governed reporting/tie-out pack, not an autonomous legal filing or a complete universal checklist. Tax conclusions and specialist note scopes require approved external workpapers. A numeric tie-out alone does not certify disclosure completeness.'])
