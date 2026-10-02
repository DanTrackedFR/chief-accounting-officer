"""Measurement governance: supplied market evidence, never autonomous valuations."""
from financing_accounting import *

def assess(c,claims):
    rs=begin(c,'measurements');entries=[];out=[];gross=[]
    if c['imports']:raise ReviewRequired('FV imports belong to explicit underlying measurement source, not duplicate journal imports')
    if c['framework']=='UK_GAAP' and iso(c['period_start'])<iso('2026-01-01'):
        raise ReviewRequired('Pre2026 UK fair-value edition requires separate operative-method specialist')
    op_total=cl_total=ZERO
    for r in rs:
        reviewed(r,c,'basis_memo','unit_memo','market_memo','market_participant_memo','disclosure_memo','valuation_memo')
        if iso(r['measurement_date'])!=iso(c['reporting_period']):raise ReviewRequired('Stale fair value measurement date')
        if not flag(r,'required_or_permitted') or not flag(r,'accessible_market'):raise ReviewRequired('Underlying standard/market access unresolved')
        enum(r,'recurrence',{'recurring','nonrecurring'});method=enum(r,'method',{'quoted','specialist'})
        inputs=rows(r['inputs'],False);inventory(r,'input_inventory',inputs);levels=[]
        for p in inputs:
            approval(p,c);level=enum(p,'level',{'1','2','3'})
            if flag(p,'significant'):levels.append(int(level))
        if not levels:raise ReviewRequired('Significant input population unresolved')
        hierarchy=max(levels);transport=nonnegative(r['transport']);transaction=nonnegative(r['transaction_cost'])
        if method=='quoted':
            if hierarchy!=1 or not flag(r,'identical_active_unadjusted') or transport:
                raise ReviewRequired('Adjusted/nonactive quote cannot be Level1 bounded measurement')
            value=cash(nonnegative(r['quantity'])*nonnegative(r['quote']))
        else:
            v=r['valuation'];policy(c,v);reviewed(v,c,'model_validation','calibration','input_change_memo')
            if iso(v['measurement_date'])!=iso(c['reporting_period']):raise ReviewRequired('Valuation date mismatch')
            if transport and not flag(v,'location_characteristic'):raise ReviewRequired('Transport adjustment requires asset-location characteristic')
            value=cash(nonnegative(v['market_exit_value'])-transport)
            if value<0:raise ReviewRequired('Transport exceeds supplied exit value')
        if type(r['expected_level']) is not int or r['expected_level']!=hierarchy:raise ReviewRequired('Hierarchy must reflect lowest significant input')
        agree(r['expected_value'],value,'Reviewed valuation');opening=nonnegative(r['opening_value']);purchases=nonnegative(r['purchases']);sales=nonnegative(r['sales_at_carrying']);fx=dec(r['fx'])
        movement=cash(value-opening-purchases+sales-fx);agree(r['remeasurement'],movement,'FV stock/flow bridge')
        if type(r['prior_level']) is not int or r['prior_level'] not in (1,2,3):raise ReviewRequired('Prior hierarchy unresolved')
        if r['prior_level']!=hierarchy:reviewed(r['transfer'],c,'reason_memo','timing_memo')
        # The underlying recognition owner supplies journals. Every offset and movement is independently tied.
        h=handoff(c,r['underlying_handoff'],'Underlying fair-value accounting');required(h,'measurement_value','journals','opening_account','closing_account')
        from production import execute
        required(h,'package','case','result')
        if h['package']!='financial-instruments-ecl':raise ReviewRequired('Non-equity underlying measurement requires a qualified specific integration adapter')
        source=h['case']
        if source.get('entity')!=c['entity'] or source.get('framework')!=c['framework'] or source.get('period_start')!=c['period_start'] or source.get('reporting_period')!=c['reporting_period']:raise ReviewRequired('Underlying case dimensions mismatch')
        fresh=execute(h['package'],source)
        if fresh['status']!='complete' or fresh!=h['result'] or source['instrument']['kind']!='equity_asset':raise ReviewRequired('Underlying fair-value recognition must be complete, current and unaltered')
        agree(fresh['calculations']['closing'],value,'Certified underlying carrying value');agree(fresh['calculations']['opening'],opening,'Certified underlying opening')
        agree(fresh['calculations']['additions'],purchases,'Certified underlying purchases')
        if sales or fx or transport:raise ReviewRequired('Disposal, FX or transport requires a qualified separate integration adapter')
        mapping={'equity investment':'Fair value asset','fair value gain/loss':'Fair value gain','OCI equity reserve (no recycling)':'Fair value OCI','cash':'Cash'}
        mapped=[]
        for j in fresh['journal_entry_implications']:
            if any(l['account'] not in mapping for l in j):raise ReviewRequired('Underlying account mapping unresolved')
            mapped.append([dict(side=l['side'],account=mapping[l['account']],amount=l['amount']) for l in j])
        normalized=[[dict(side=l['side'],account=l['account'],amount=cash(l['amount'])) for l in j] for j in h['journals']]
        if normalized!=mapped:raise ReviewRequired('Underlying journals differ from certified recognition result')
        agree(h['measurement_value'],value,'Underlying measured value');agree(h['opening_account'],opening,'Underlying opening');agree(h['closing_account'],value,'Underlying closing')
        journal_rows=h['journals']
        if not isinstance(journal_rows,list):raise ReviewRequired('Underlying journal array required')
        asset=flag(r,'asset');account=enum(r,'account',{'Fair value asset','Fair value liability'})
        if (account=='Fair value asset')!=asset:raise ReviewRequired('FV asset/liability journal classification mismatch')
        delta=sum((line_delta(j,account,credit=not asset) for j in journal_rows),ZERO)
        agree(delta,value-opening,'Underlying all-movement accounting journal bridge')
        entries+=journal_rows;agree(r['gl_value'],value,'FV source/GL');gross.append(value)
        op_total+=opening;cl_total+=value
        out.append(dict(level=hierarchy,value=value,remeasurement=movement,transaction_cost_excluded=transaction,transport=transport))
    population(c,rs,gross)
    stocks(c,{'Fair value asset':(op_total,cl_total)})
    return complete(c,'Fair value evidence, hierarchy and underlying accounting reconciled',dict(measurements=out),entries,
        ['Fair-value standard does not supply recognition or unit of account; underlying owner determines journal/OCI classification',
         'Complex models, rates, option pricing, appraisals and private-company values require qualified independently reviewed valuation evidence'])
