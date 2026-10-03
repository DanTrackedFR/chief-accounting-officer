"""Condition chronology, completed recognition owners and authorization window."""
from presentation_accounting import *

OWNERS={'customer_failure':{'financial-instruments-ecl'},'litigation':{'provisions-contingencies'},'impairment':{'asset-impairment'},'acquisition':{'business-combinations'},'disposal':{'fixed-assets','intangible-assets'},'financing':{'debt-financing'},'covenant':{'debt-financing'},'dividend':{'equity-capital'},'fraud_error':{'accounting-changes'},'tax':{'income-taxes'},'other':set()}

def assess(c,claims):
    rs=begin(c,'events');imports(c,{'going-concern','financial-statements'})
    p=qualified(c,c['event_method'],'Subsequent-event accounting');reviewed(p,c,'authorization_memo','window_memo','filer_memo','basis_memo','aggregate_materiality_memo')
    cutoff=iso(p['cutoff']);end=iso(c['reporting_period'])
    expected='issuance' if c['framework']=='US_GAAP' and c['us_entity_type']=='public' else 'available_to_issue' if c['framework']=='US_GAAP' else 'authorization'
    if p['window_basis']!=expected or not end<=cutoff<=iso(c['execution_date']):raise ReviewRequired('Incorrect framework/entity subsequent-event cutoff')
    if not flag(p,'basis_appropriate'):raise ReviewRequired('Going-concern basis change requires separate framework-specific basis method')
    if flag(p,'post_issuance'):raise ReviewRequired('Post-issuance discovery/reissuance and SEC/legal filing require specialists')
    feeds=rows(c['feeds']);inventory(c,'feed_inventory',feeds)
    required_feeds={'board','legal','treasury','commercial','tax','asset','post_close','management_forecast'}
    if {r['id'] for r in feeds}!=required_feeds:raise ReviewRequired('Subsequent-event independent feed population incomplete')
    fed=[]
    for f in feeds:
        reviewed(f,c,'search_memo');
        if iso(f['reviewed_through'])!=cutoff or not flag(f,'complete'):raise ReviewRequired('Feed review does not reach authorization cutoff')
        if not isinstance(f['event_ids'],list) or len(set(f['event_ids']))!=len(f['event_ids']):raise ReviewRequired('Feed event IDs malformed')
        fed+=f['event_ids']
    if set(fed)!={r['id'] for r in rs}:raise ReviewRequired('Event log omits or invents feed events')
    originals=rows(c['statement_balances']);inventory(c,'statement_inventory',originals);delta={};seen=set();out=[];gross=[];owned_stocks={}
    updates=rows(c['accounting_updates']);inventory(c,'update_inventory',updates);by={r['id']:r for r in updates};used=set()
    for r in rs:
        kind=enum(r,'kind',set(OWNERS));reviewed(r,c,'condition_memo','materiality_memo','disclosure_memo','going_concern_memo')
        occurred=iso(r['event_date']);learned=iso(r['learned_date']);condition=iso(r['condition_date'])
        if not end<occurred<=learned<=cutoff:raise ReviewRequired('Event or discovery outside complete review window')
        existed=flag(r,'existed_at_reporting_date')
        if existed!=(condition<=end) or condition>occurred:raise ReviewRequired('Reporting-date condition chronology contradicts classification')
        adjusts=flag(r,'adjusting')
        if adjusts!=existed:raise ReviewRequired('Later information is not interchangeable with later causation')
        if kind=='dividend' and not existed and adjusts:raise ReviewRequired('Later declared dividend is not a reporting-date liability')
        if flag(r,'going_concern_impact'):
            matches=[i for i in c['imports'] if i['id']==r['going_concern_import'] and i['package']=='going-concern']
            if len(matches)!=1:raise ReviewRequired('Going-concern development requires actual completed matching assessment')
        amount=dec(r['measurement_change']);gross.append(abs(amount));effect=None
        if adjusts:
            uid=r['update_id']
            if uid in used or uid not in by:raise ReviewRequired('Adjusting conclusion missing or double-counted')
            used.add(uid);u=by[uid];source(c,u)
            before=completed(c,u['original'],OWNERS[kind]);after=completed(c,u['revised'],OWNERS[kind])
            if u['revised']['package']!='provisions-contingencies':raise ReviewRequired('Adjusting stock-to-statement adapter currently supports litigation provisions only; other owners require separately qualified integration')
            b=u['original']['case'];a=u['revised']['case']
            if b['obligation']['type']!='litigation' or a['obligation']['type']!='litigation' or not same_result(b['movements'],a['movements']) or not same_result(b['reimbursement'],a['reimbursement']):raise ReviewRequired('Litigation estimate update cannot silently change settlements, opening movements or reimbursement')
            if owned_stocks:raise ReviewRequired('Multiple litigation/account stocks require separately supported aggregate ownership adapter')
            owned_stocks['provision']=(-dec(before['calculations']['provision']),-dec(after['calculations']['provision']))
            if before['calculations']['reimbursement'] or after['calculations']['reimbursement']:raise ReviewRequired('Reimbursement stock change requires separate complete adapter')
            if u['original']['package']!=u['revised']['package'] or u['original']['case']['case_id']!=u['revised']['case']['case_id']:raise ReviewRequired('Adjustment must compare same accounting owner/case')
            key=(u['revised']['package'],u['revised']['case']['case_id'])
            if key in seen:raise ReviewRequired('Accounting owner adjustment imported twice')
            seen.add(key);change={}
            for sign,result in ((-1,before),(1,after)):
                for entry in result['journal_entry_implications']:
                    for l in entry:change[l['account']]=change.get(l['account'],ZERO)+sign*dec(l['amount'])*(1 if l['side']=='Dr' else -1)
            if cash(sum(change.values(),ZERO))!=ZERO:raise ReviewRequired('Underlying adjustment is not balanced')
            if u.get('measured_account')!='provision':raise ReviewRequired('Litigation adapter must measure the primary provision stock, not an arbitrary zero offset')
            agree(amount,dec(after['calculations']['provision'])-dec(before['calculations']['provision']),'Event/primary provision liability change')
            for account,n in change.items():delta[account]=delta.get(account,ZERO)+n
            effect=amount
        elif amount:raise ReviewRequired('Nonadjusting event cannot alter period-end accounting')
        if flag(r,'material') and not flag(r,'disclosed'):raise ReviewRequired('Material event disclosure missing')
        if flag(r,'disclosed'):
            reviewed(r,c,'nature_memo');estimated=flag(r,'effect_estimable')
            if estimated:
                effect=dec(r['financial_effect'])
                if adjusts:agree(effect,amount,'Adjusting-event disclosed measurement effect; other exposure bases need separate adapter')
            else:reviewed(r,c,'inability_to_estimate_memo')
        out.append(dict(kind=kind,adjusting=adjusts,disclosed=r['disclosed'],financial_effect=effect))
    if used!=set(by):raise ReviewRequired('Unlinked accounting update could double count recognition')
    if set(delta)-{r['id'] for r in originals}:raise ReviewRequired('Accounting offset missing from statement population')
    for r in originals:
        approval(r,c);agree(r['revised'],dec(r['original'])+delta.get(r['id'],ZERO),'Original-to-revised statement');agree(r['statement'],r['revised'],'Final statement tie')
        if r['id'] in owned_stocks:
            agree(r['original'],owned_stocks[r['id']][0],'Original accounting-owner stock');agree(r['revised'],owned_stocks[r['id']][1],'Revised accounting-owner stock')
    if set(owned_stocks)-{r['id'] for r in originals}:raise ReviewRequired('Owned stock absent from original/revised statement')
    if cash(sum((dec(r['original']) for r in originals),ZERO)) or cash(sum((dec(r['revised']) for r in originals),ZERO)):raise ReviewRequired('Original or revised statement TB unbalanced')
    population(c,rs,gross)
    return complete(c,'Subsequent-event window, recognition owners and disclosures reconciled',dict(events=out,statement_adjustments=delta,cutoff=str(cutoff)),[],['Underlying completed accounting owners retain journals; this event-register workflow does not post them again','Legal authorization, materiality, condition timing and filing conclusions require actual evidence','Unsupported reserved-specialist measurement is not extended by this event workflow'])
