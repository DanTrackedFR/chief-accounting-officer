"""Dated classification and presentation controls; no disposal-group measurement."""
from special_reporting import *

def assess(c,claims):
    rs=start(c,'assets',{'fixed-assets','asset-impairment','financial-statements','accounting-changes','business-combinations','consolidation'})
    p=method(c,'disposal_method','Disposal classification and presentation')
    if c['framework'] not in {'IFRS','AASB'}:raise ReviewRequired('US/UK held-for-sale measurement/presentation requires a separate governed method')
    if enum(p,'route',{'classification_presentation'})!='classification_presentation':raise ReviewRequired('Unsupported disposal route')
    if any(flag(p,k) for k in ('allocation_required','reversal_requested','completed_disposal','retained_interest','oci_recycling','measurement_requested')):raise ReviewRequired('Measurement/allocation/reversal/disposal ownership exceeds bounded classification workpaper')
    texts(p,'perimeter_memo','sale_plan_memo','criteria_memo','premeasurement_memo','discontinued_memo','cash_flow_memo','comparative_memo','impairment_memo')
    d=inperiod(c,p['classification_date'])
    for k in ('available_immediately','highly_probable','committed_plan','active_marketing','sale_within_year','premeasurement_complete','scope_exceptions_reviewed','group_complete','tax_review_complete'):
        if not flag(p,k):raise ReviewRequired('Classification/sequence prerequisite unresolved: '+k)
    if iso(p['criteria_met_date'])!=d or iso(p['approval_evidence_date'])>d:raise ReviewRequired('Classification cannot precede actual date-specific criteria/evidence')
    if not d<iso(p['expected_sale_date'])<=d.replace(year=d.year+1,day=min(d.day,28) if d.month==2 else d.day):raise ReviewRequired('Sale timing exception requires separate classification method')
    perimeter=c['perimeter'];approval(perimeter,c);texts(perimeter,'legal_memo','book_memo')
    inventory(perimeter,'legal_asset_ids',rs);inventory(perimeter,'book_asset_ids',rs)
    depreciation=rows(c['depreciation_sources']);inventory(c,'depreciation_inventory',depreciation)
    for dep in depreciation:
        source(c,dep)
        if dep['asset_id'] not in {a['id'] for a in rs}:raise ReviewRequired('Depreciation asset outside disposal perimeter')
        if d<=iso(dep['date'])<=iso(c['reporting_period']) and nonnegative(dep['amount'])!=0:raise ReviewRequired('Actual depreciation source contradicts cessation')
    carrying=ZERO;included=set()
    for a in rs:
        texts(a,'measurement_owner','premeasurement_evidence','scope_memo','depreciation_memo')
        if not flag(a,'in_scope') or not flag(a,'premeasurement_complete'):raise ReviewRequired('Unsupported asset/scope in disposal population')
        kind=enum(a,'stock_kind',{'asset','liability'})
        exact(a['carrying_at_classification'],a['book_carrying'],'Disposal perimeter/approved books')
        carrying+=nonnegative(a['carrying_at_classification'])*(1 if kind=='asset' else -1)
        exact(a['depreciation_after_classification'],'0','Depreciation cessation')
        # Amounts are frozen premeasurement-owner facts; this workpaper cannot
        # certify an HFS measurement or invent an asset write-down.
        if a['id'] in included:raise ReviewRequired('Duplicate disposal asset')
        included.add(a['id'])
    population(c,rs,[nonnegative(a['carrying_at_classification']) for a in rs])
    for imp in c['imports']:
        if imp['package']=='asset-impairment':
            assets=imp['case']['assets']
            for a in rs:
                matched=[x for x in assets if x['id']==a['owner_asset_id']]
                if len(matched)!=1:raise ReviewRequired('Impairment-owner perimeter contradiction')
                if d!=iso(c['reporting_period']):raise ReviewRequired('Period-end owner cannot authorize earlier classification stock')
                after=imp['result']['calculations'].get('closing',{})
                if not after:raise ReviewRequired('No supported impairment stock adapter; do not assert measurement ownership')
                exact(a['carrying_at_classification'],after[matched[0]['id']],'Actual owner premeasurement stock')
        if imp['package'] in {'fixed-assets','business-combinations','consolidation'}:
            raise ReviewRequired('Underlying owner supplied without supported stock/perimeter adapter')
    q=c['component'];approval(q,c);texts(q,'qualification_memo','continuing_involvement_memo')
    qualifies=flag(q,'separable_component') and (flag(q,'major_line') or flag(q,'major_geography') or flag(q,'coordinated_major_plan'))
    if flag(q,'discontinued')!=qualifies:raise ReviewRequired('Held-for-sale and discontinued qualification are separate decisions')
    s=c['current_statement'];profit=typed_statement(c,s)
    if s['metric']!='profit':raise ReviewRequired('Profit-after-tax statement required')
    full_lines={x['id']:x for x in s['lines']};used_lines=set();used_statements=set()
    amounts=rows(c['results']);inventory(c,'result_inventory',amounts)
    total=discontinued=ZERO
    for a in amounts:
        source(c,a);texts(a,'allocation_memo','source_population_memo')
        st=a['source_statement']
        if st['metric']!='profit' or st['units']!=s['units'] or st['id'] in used_statements:raise ReviewRequired('Duplicate or incompatible profit source')
        used_statements.add(st['id'])
        for line in st['lines']:
            if line['id'] in used_lines or line['id'] not in full_lines or line!=full_lines[line['id']]:raise ReviewRequired('Component ledger must partition actual full-entity source exactly once')
            used_lines.add(line['id'])
        n=dec(a['profit_after_tax']);exact(n,typed_statement(c,a['source_statement'],full_entity=False),'Component/continuing profit source');total+=n
        if flag(a,'belongs_to_component'):discontinued+=n
        if dec(a['disposal_gain'])!=0:raise ReviewRequired('Completed disposal results need separate exact ownership method')
    if used_lines!=set(full_lines):raise ReviewRequired('Incomplete component/continuing source partition')
    exact(total,profit,'Operating results source statement')
    expected=discontinued if qualifies else ZERO
    exact(c['presentation']['discontinued_profit'],expected,'Discontinued presentation')
    exact(c['presentation']['continuing_profit'],profit-expected,'Continuing presentation')
    cf=rows(c['cash_flows']);inventory(c,'cash_flow_inventory',cf)
    cf_totals={k:ZERO for k in ('operating','investing','financing')}
    bank=rows(c['bank_sources']);inventory(c,'bank_inventory',bank);bank_map={b['id']:b for b in bank};used_bank=set()
    for a in cf:
        source(c,a);k=enum(a,'category',set(cf_totals));texts(a,'bank_source_memo')
        b=a['bank_source'];approval(b,c)
        if b['id'] in used_bank or bank_map.get(b['id'])!=b:raise ReviewRequired('Bank transactions must reconcile exactly once to independent population')
        used_bank.add(b['id'])
        if b['source_period']!=a['source_period'] or b['category']!=k or b['entity']!=c['entity']:raise ReviewRequired('Component bank-source context mismatch')
        exact(a['amount'],b['amount'],'Component cash flow/bank source');cf_totals[k]+=dec(a['amount'])
    if used_bank!=set(bank_map):raise ReviewRequired('Incomplete bank transaction population')
    for k,v in cf_totals.items():exact(c['presentation']['component_cash_flows'][k],v if qualifies else ZERO,'Separate cash-flow support')
    comps=rows(c['comparatives']);inventory(c,'comparative_inventory',comps)
    if not comps:raise ReviewRequired('Comparative presentation evidence required')
    for r in comps:
        approval(r,c);texts(r,'recast_memo');prior=typed_statement(c,r['statement'],False)
        comparable_spans(s['source_period'],r['statement']['source_period'])
        component=typed_statement(c,r['component_statement'],False,full_entity=False)
        ps=r['statement'];cs=r['component_statement']
        if ps['metric']!='profit' or cs['metric']!='profit' or ps['units']!=s['units'] or cs['units']!=s['units']:raise ReviewRequired('Comparative profit metric/units mismatch')
        prior_lines={x['id']:x for x in ps['lines']}
        if any(prior_lines.get(x['id'])!=x for x in cs['lines']):raise ReviewRequired('Prior component source must be actual prior full-entity ledger subset')
        if r['component_statement']['source_period']!=r['statement']['source_period']:raise ReviewRequired('Prior component source span mismatch')
        exact(r['component_profit'],component,'Prior component source ledger')
        exact(dec(r['continuing_profit'])+dec(r['discontinued_profit']),prior,'Comparative total')
        exact(r['discontinued_profit'],r['component_profit'] if qualifies else ZERO,'Comparative component recast')
        if flag(r,'balance_sheet_reclassified'):raise ReviewRequired('Do not automatically reclassify prior balance sheet held-for-sale')
    return no_posting(c,'Bounded held-for-sale classification and discontinued presentation workpaper reconciled',dict(carrying_population=carrying,classification_supported=True,discontinued=qualifies,continuing_profit=profit-expected,discontinued_profit=expected,component_cash_flows=cf_totals if qualifies else {k:ZERO for k in cf_totals}),['Date-specific supported classification; independent major-component assessment'],['No disposal-group measurement, allocation, reversal, disposal gain, OCI recycling or new journals are produced. Asset impairment and recognition remain with their accounting owners. US and UK detailed routes require separate governed methods.'])
