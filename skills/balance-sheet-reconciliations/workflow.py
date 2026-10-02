from operations_accounting import *

def assess(c,claims):
    proof(c,'trial_balance','inventory','reconciliations')
    tb=rows(c['trial_balance'],False);inv=rows(c['inventory'],False);recs=rows(c['reconciliations'],False)
    agree(sum((dec(r['balance']) for r in tb),ZERO),ZERO,'Trial balance')
    ids={r['id'] for r in inv}
    if ids!={r['id'] for r in recs} or not ids<={r['id'] for r in tb}:raise ReviewRequired('Full balance-sheet inventory coverage failed')
    tbmap={r['id']:r for r in tb};work=[];entries=[];gross=ZERO
    for r in recs:
        approval(r,c);required(r,'opening','additions','reductions','source_closing','gl_closing','source_ids','gl_ids','items','adjustments','threshold','relative_threshold','max_age_days','risk_tier','movement_memo')
        opening=dec(r['opening']);expected=opening+nonnegative(r['additions'])-nonnegative(r['reductions']);agree(r['source_closing'],expected,'Independent source rollforward')
        agree(r['gl_closing'],tbmap[r['id']]['balance'],'TB to GL')
        if not isinstance(r['source_ids'],list) or not isinstance(r['gl_ids'],list) or len(set(r['source_ids']))!=len(r['source_ids']) or len(set(r['gl_ids']))!=len(r['gl_ids']):raise ReviewRequired('Bidirectional source identifiers required')
        items=rows(r['items']);adjust=rows(r['adjustments']);itemnet=ZERO;itemgross=ZERO
        for i in items:
            approval(i,c);required(i,'amount','opened','resolution','source_id','gl_id','status')
            age=(iso(c['reporting_period'])-iso(i['opened'])).days
            if age<0 or age>nonnegative(r['max_age_days']) or i['status']!='supported_timing':raise ReviewRequired('Unsupported or aged reconciliation item')
            n=dec(i['amount']);itemnet+=n;itemgross+=abs(n)
        absent=set(r['source_ids'])^set(r['gl_ids'])
        identified={i['source_id'] for i in items}|{i['gl_id'] for i in items}
        if not absent<=identified:raise ReviewRequired('Unexplained source/GL population omission')
        delta=ZERO
        for a in adjust:
            approval(a,c);required(a,'amount','offset','error_vs_estimate_memo','posted','source_id')
            if not flag(a,'posted'):raise ReviewRequired('Correction not posted to reconciled GL')
            n=dec(a['amount']);delta+=n;entries.append(movement(r['id'],a['offset'],n))
        # gl_closing is the pre-adjustment extract; posted adjustments bridge to final GL.
        agree(dec(r['gl_closing'])+delta,expected+itemnet,'Source to adjusted GL')
        absolute=nonnegative(r['threshold']);relative=fraction(r['relative_threshold'])
        if itemgross>absolute or itemgross>abs(expected)*relative:raise ReviewRequired('Gross reconciliation exceptions exceed approved risk thresholds')
        gross+=itemgross;work.append({'account':r['id'],'source':cash(expected),'adjusted_gl':cash(dec(r['gl_closing'])+delta),'gross_items':cash(itemgross),'movement':cash(expected-opening)})
    population(c,inv,[abs(dec(tbmap[r['id']]['balance'])) for r in inv])
    return finish('Trial balance and independently substantiated balance-sheet inventory reconciled.',{'accounts':work,'gross_reconciling_items':cash(gross)},entries,
      ['Balanced TB and zero net variance alone do not prove completeness; gross timing items and inventory coverage remain separate assertions.'],
      ['Material prior errors, estimate changes and unexplained movements require the framework-specific reporting assessment.'])
