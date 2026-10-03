"""Daily basic EPS and qualified instrument increments; no invented cap-table rights."""
from presentation_accounting import *

def assess(c,claims):
    rs=begin(c,'share_intervals');imports(c,{'equity-capital','share-based-compensation','debt-financing','financial-statements','business-combinations','accounting-changes'})
    p=qualified(c,c['eps_method'],'EPS accounting')
    if not flag(p,'in_scope') or flag(p,'multiple_class') or flag(p,'participating_securities'):raise ReviewRequired('Scope/multiple-class/two-class EPS requires separate method')
    if c['framework']=='UK_GAAP' and p.get('uk_scope') not in {'specified_ias33','voluntary_reviewed'}:raise ReviewRequired('FRS102 is not universal IAS33 scope')
    if flag(p,'additional_per_share'):raise ReviewRequired('Additional/IFRS18 per-share measures require separate operative numerator method')
    reviewed(p,c,'continuing_control_memo','comparative_memo','legal_rights_memo','framework_method_memo')
    start=iso(c['period_start']);end=iso(c['reporting_period']);cutoff=iso(p['authorization_date'])
    if not end<=cutoff<=iso(c['execution_date']):raise ReviewRequired('Unsupported authorization window')
    actions=rows(c['retrospective_actions']);inventory(c,'retrospective_inventory',actions)
    action_dates=[]
    for a in actions:
        source(c,a);enum(a,'kind',{'split','bonus'});reviewed(a,c,'legal_terms','retrospective_memo')
        d=iso(a['date']);f=positive(a['factor'])
        if not start<=d<=cutoff:raise ReviewRequired('Retrospective action outside reviewed period/window')
        action_dates.append((d,f))
    if len({d for d,f in action_dates})!=len(action_dates):raise ReviewRequired('Same-date capital actions need separately resolved ordering')
    cursor=start;weighted=ZERO;last=None;den_days=Decimal((end-start).days+1);gross=[];consumed=set()
    for r in sorted(rs,key=lambda x:x['start']):
        lo=inperiod(c,r['start']);hi=inperiod(c,r['end'])
        if lo!=cursor or hi<lo:raise ReviewRequired('Share schedule must be contiguous and nonoverlapping')
        issued=nonnegative(r['issued']);treasury=nonnegative(r['treasury'])
        if issued!=issued.to_integral_value() or treasury!=treasury.to_integral_value() or treasury>issued:raise ReviewRequired('Invalid whole ordinary/treasury shares')
        if last is None:agree(issued,c['opening_issued'],'Opening legal shares');agree(treasury,c['opening_treasury'],'Opening treasury shares')
        else:
            bridge=r['movement'];policy(c,bridge);reviewed(bridge,c,'legal_memo');enum(bridge,'kind',{'ordinary','split','bonus'})
            if iso(bridge['date'])!=lo:raise ReviewRequired('Movement date must match share interval boundary')
            if bridge['kind'] in {'split','bonus'}:
                match=[f for d,f in action_dates if d==lo]
                if len(match)!=1:raise ReviewRequired('Split/bonus requires exact retrospective action')
                action=next(a for a in actions if iso(a['date'])==lo)
                if bridge['kind']!=action['kind']:raise ReviewRequired('Retrospective action kind differs from legal movement')
                consumed.add(lo)
                agree(issued,last[0]*match[0],'Split issued bridge');agree(treasury,last[1]*match[0],'Split treasury bridge')
            else:
                agree(issued,last[0]+dec(bridge['issued_change']),'Issued share movement');agree(treasury,last[1]+dec(bridge['treasury_change']),'Treasury share movement')
        factor=Decimal(1)
        for d,f in action_dates:
            if lo<d<=hi:raise ReviewRequired('Capital action requires split share intervals')
            if d>hi:factor*=f
        weighted+=(issued-treasury)*factor*Decimal((hi-lo).days+1)/den_days
        last=(issued,treasury);cursor=hi+timedelta(days=1);gross.append(issued)
    if cursor!=end+timedelta(days=1):raise ReviewRequired('Share population does not cover full reporting period')
    if consumed!={d for d,f in action_dates if d<=end}:raise ReviewRequired('Every in-period split/bonus must be consumed by its exact legal share boundary; first-day action needs separate opening adapter')
    agree(last[0],c['closing_issued'],'Closing legal share register');agree(last[1],c['closing_treasury'],'Closing treasury register')
    population(c,rs,gross);agree(c['expected_weighted_shares'],weighted,'Weighted-average shares')
    n=c['numerator'];policy(c,n);reviewed(n,c,'attribution_memo','preference_memo','adjustment_memo','financial_statement_memo')
    source_totals=statement_source(c,('profit','nci','preferred','other','continuing_profit','continuing_nci','continuing_preferred','continuing_other'))
    for key,value in source_totals.items():agree(n[key],value,'EPS numerator/current period GL statement source')
    total=dec(n['profit'])-dec(n['nci'])-dec(n['preferred'])+dec(n['other'])
    continuing=dec(n['continuing_profit'])-dec(n['continuing_nci'])-dec(n['continuing_preferred'])+dec(n['continuing_other'])
    agree(total,n['ordinary_total'],'Attributable numerator');agree(continuing,n['ordinary_continuing'],'Continuing numerator');agree(total-continuing,n['ordinary_discontinued'],'Discontinued numerator')
    potentials=rows(c['potential_shares']);inventory(c,'instrument_inventory',potentials);increments=[]
    for r in potentials:
        source(c,r);method=qualified(c,r['method'],'EPS instrument accounting');enum(method,'kind',{'if_converted','treasury_stock','contingent','share_award'})
        reviewed(method,c,'terms_memo','tax_memo','timing_memo','measurement_memo')
        shares=nonnegative(method['incremental_weighted_shares']);adj=dec(method['total_numerator_adjustment']);ca=dec(method['continuing_numerator_adjustment'])
        if shares==0 and (adj or ca):raise ReviewRequired('Zero incremental shares cannot carry numerator adjustment')
        if method['kind'] in {'treasury_stock','share_award'} and (adj or ca):raise ReviewRequired('Option/award numerator effects require separate method')
        if adj<0 or ca<0:raise ReviewRequired('Negative incremental numerator requires specialist sequencing method')
        if shares:increments.append((ca/shares,r['id'],shares,adj,ca))
    dt=total;dc=continuing;ds=weighted;tests=[]
    for _,id,shares,adj,ca in sorted(increments):
        include=continuing>0 and ratio(dc+ca,ds+shares)<ratio(dc,ds)
        if include:dt+=adj;dc+=ca;ds+=shares
        tests.append(dict(included=include,incremental_shares=shares,total_adjustment=adj,continuing_adjustment=ca))
    calculations=dict(weighted_shares=weighted,basic_total=ratio(total,weighted),basic_continuing=ratio(continuing,weighted),basic_discontinued=ratio(total-continuing,weighted),diluted_total=ratio(dt,ds),diluted_continuing=ratio(dc,ds),diluted_discontinued=ratio(dt-dc,ds),diluted_shares=ds,instrument_tests=tests)
    for key in ('basic_total','basic_continuing','basic_discontinued','diluted_total','diluted_continuing','diluted_discontinued'):agree(c['statement'][key],calculations[key],'EPS statement/note')
    comps=rows(c['comparatives']);inventory(c,'comparative_inventory',comps);out=[]
    cumulative=Decimal(1)
    for d,f in action_dates:cumulative*=f
    for r in comps:
        approval(r,c);qualified(c,r['method'],'EPS comparative accounting')
        if iso(r['period_start'])>iso(r['period_end']) or iso(r['period_end'])>=start:raise ReviewRequired('Comparative must be a valid prior reporting span')
        if r.get('source_entity')!=c['entity'] or r.get('source_framework')!=c['framework'] or r.get('source_period')!=[r['period_start'],r['period_end']]:raise ReviewRequired('Comparative source dimensions mismatch')
        revised=positive(r['original_weighted_shares'])*cumulative;agree(r['restated_weighted_shares'],revised,'Retrospective comparative denominator')
        diluted=positive(r['original_diluted_shares'])*cumulative;agree(r['restated_diluted_shares'],diluted,'Retrospective comparative diluted denominator')
        if positive(r['original_diluted_shares'])<positive(r['original_weighted_shares']) or diluted<revised:raise ReviewRequired('Single-class comparative diluted shares cannot be below basic shares')
        agree(r['basic_eps'],ratio(r['ordinary_profit'],revised),'Comparative EPS');agree(r['diluted_eps'],ratio(r['original_diluted_numerator'],diluted),'Comparative diluted EPS')
        out.append(dict(weighted_shares=revised,basic_eps=ratio(r['ordinary_profit'],revised),diluted_shares=diluted,diluted_eps=ratio(r['original_diluted_numerator'],diluted)))
    calculations['comparatives']=out
    return complete(c,'Basic and diluted EPS reconciled under qualified framework methods',calculations,[],['EPS itself creates no journal; underlying earnings/capital accounting remains with its owner','Rights issues, two-class, participating securities and complex contingencies require separately supported methods; option/convertible increments are qualified inputs, not invented terms'])
