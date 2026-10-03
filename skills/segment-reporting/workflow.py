"""CODM population and qualified reportability rules, not invented management structure."""
from presentation_accounting import *

def assess(c,claims):
    rs=begin(c,'components');imports(c,{'financial-statements','consolidation','business-combinations','accounting-changes'})
    p=qualified(c,c['segment_method'],'Segment accounting');reviewed(p,c,'scope_memo','codm_identity','codm_pack_memo','aggregation_memo','transition_memo','comparative_memo','entity_wide_memo')
    if not flag(p,'in_scope'):raise ReviewRequired('Out-of-scope reporting requires separately documented nonapplicability, not a segment production result')
    if c['framework']=='UK_GAAP' and p.get('uk_scope')!='separately_reviewed_obligation':raise ReviewRequired('No universal FRS102 segment obligation')
    if c['framework']=='US_GAAP':reviewed(p,c,'significant_expense_memo','annual_interim_adoption_memo','single_segment_memo')
    thresholds=qualified(c,p['thresholds'],'Segment reportability thresholds')
    revenue_limit=positive(thresholds['revenue']);profit_limit=positive(thresholds['profit']);asset_limit=positive(thresholds['assets']);coverage=fraction(thresholds['external_coverage']);customer_limit=fraction(thresholds['major_customer'])
    if max(revenue_limit,profit_limit,asset_limit)>1 or coverage==0 or customer_limit==0:raise ReviewRequired('Invalid qualified threshold parameters')
    ops=[];gross=[]
    for r in rs:
        reviewed(r,c,'business_memo','discrete_information_memo','regular_review_memo','resource_allocation_memo')
        operating=flag(r,'business_activity') and flag(r,'discrete_information') and flag(r,'regular_codm_review')
        if flag(r,'operating')!=operating:raise ReviewRequired('Operating segment does not match evidenced CODM criteria')
        ext=nonnegative(r['external_revenue']);inter=nonnegative(r['intersegment_revenue']);assets=nonnegative(r['assets']);nonnegative(r['liabilities']);gross.append(ext+inter)
        if operating:ops.append(r)
        elif ext or inter:raise ReviewRequired('Revenue-bearing excluded component requires specialist scope adapter')
    population(c,rs,gross)
    groups=rows(c['groups']);inventory(c,'group_inventory',groups);seen=set();g=[]
    for r in groups:
        approval(r,c);members=r['members']
        if not isinstance(members,list) or not members or len(set(members))!=len(members):raise ReviewRequired('Invalid group member population')
        if seen.intersection(members):raise ReviewRequired('Component counted twice')
        if not set(members)<={x['id'] for x in ops}:raise ReviewRequired('Group contains unknown/nonoperating component')
        seen.update(members)
        if len(members)>1:
            a=qualified(c,r['aggregation'],'Segment aggregation');reviewed(a,c,'long_term_economics','products_services','production_process','customers','distribution','regulatory_memo')
            if not flag(a,'criteria_met'):raise ReviewRequired('Aggregation economic criteria unresolved')
        selected=[x for x in ops if x['id'] in members]
        measure={k:sum((dec(x[k]) for x in selected),ZERO) for k in ('external_revenue','intersegment_revenue','profit','assets','liabilities')}
        measure.update(label=public_label(r),required=flag(r,'qualitative_required'),reported=flag(r,'reported'));g.append(measure)
    if seen!={x['id'] for x in ops}:raise ReviewRequired('Operating component missing from reportability population')
    total_revenue=sum((x['external_revenue']+x['intersegment_revenue'] for x in g),ZERO);total_assets=sum((x['assets'] for x in g),ZERO)
    profits=sum((max(x['profit'],ZERO) for x in g),ZERO);losses=sum((max(-x['profit'],ZERO) for x in g),ZERO);basis=max(profits,losses)
    for x in g:
        required=(total_revenue>0 and x['external_revenue']+x['intersegment_revenue']>=total_revenue*revenue_limit) or (basis>0 and abs(x['profit'])>=basis*profit_limit) or (flag(p,'asset_test') and total_assets>0 and x['assets']>=total_assets*asset_limit) or x['required']
        if required and not x['reported']:raise ReviewRequired('Required reportable segment omitted')
    external=sum((x['external_revenue'] for x in g),ZERO);reported=sum((x['external_revenue'] for x in g if x['reported']),ZERO)
    if external and reported<external*coverage:raise ReviewRequired('Insufficient reportable external revenue coverage')
    bridges=rows(c['reconciliations']);inventory(c,'reconciliation_inventory',bridges)
    statement_totals=statement_source(c,('revenue','profit','assets','liabilities'))
    if {r['id'] for r in bridges}!={'revenue','profit','assets','liabilities'}:raise ReviewRequired('Complete revenue/profit/asset/liability bridges required')
    totals={'revenue':total_revenue,'profit':sum((x['profit'] for x in g),ZERO),'assets':total_assets,'liabilities':sum((x['liabilities'] for x in g),ZERO)}
    for r in bridges:
        approval(r,c);items=rows(r['items']);inventory(r,'item_inventory',items)
        for item in items:reviewed(item,c,'cause_memo')
        adjustment=sum((dec(i['amount']) for i in items),ZERO);agree(r['segment_total'],totals[r['id']],'Segment measure');agree(r['consolidated'],totals[r['id']]+adjustment,'Segment/consolidated reconciliation');agree(r['statement'],r['consolidated'],'Financial statement tie')
        if r['id']=='revenue':agree(r['consolidated'],external,'External revenue / elimination')
        offset=dec(p['profit_definition_adjustment']) if r['id']=='profit' else ZERO
        if r['id']=='profit':reviewed(p,c,'profit_definition_memo')
        agree(dec(r['consolidated'])+offset,statement_totals[r['id']],'Segment measure definition to actual statement source')
    wide=c['entity_wide'];policy(c,wide)
    for key in ('geographic','products_services','customers'):
        pop=rows(wide[key]);inventory(wide,key+'_inventory',pop)
        for r in pop:reviewed(r,c,'source_memo');nonnegative(r['external_revenue'])
        agree(sum((dec(r['external_revenue']) for r in pop),ZERO),external,'Complete entity-wide revenue population')
        if key=='geographic':
            reviewed(wide,c,'geographic_asset_memo');agree(sum((nonnegative(r['noncurrent_assets']) for r in pop),ZERO),wide['statement_noncurrent_assets'],'Geographic noncurrent assets')
        if key=='customers':
            for r in pop:
                major=external>0 and dec(r['external_revenue'])>=external*customer_limit
                if flag(r,'major')!=major:raise ReviewRequired('Major customer concentration classification mismatch')
                if major:reviewed(r,c,'segment_attribution_memo')
    if flag(p,'structure_changed') and not flag(p,'comparatives_reconciled'):raise ReviewRequired('Changed segment structure requires reconciled comparatives or separately supported impracticability method')
    return complete(c,'CODM segments and entity-wide disclosures reconciled',dict(segments=g,all_other={k:sum((x[k] for x in g if not x['reported']),ZERO) for k in ('external_revenue','intersegment_revenue','profit','assets','liabilities')},consolidated_external_revenue=external,reportable_external_revenue=reported,profit_threshold_basis=basis),[],['Actual CODM and aggregation judgments are independently supplied','Threshold values and framework/adoption requirements must be qualified; no universal IFRS8 obligation imported into FRS102','Segment disclosure creates no journal; accounting remains with consolidation and transaction owners'])
