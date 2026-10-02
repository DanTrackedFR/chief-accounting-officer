from operations_accounting import *

def assess(c,claims):
    proof(c,'pairs','recharges','handoffs')
    handoff(c,'consolidation','Consolidation');handoff(c,'transfer_pricing','Transfer Pricing');handoff(c,'fx','Foreign Currency')
    pairs=rows(c['pairs'],False);recharges=rows(c['recharges']);work=[];journals=[];transactions=set();recharge_total=ZERO
    for r in recharges:
        approval(r,c);required(r,'cost_pool','allocations','markup','agreement','tax_review','date','provider','currency','source_complete')
        inperiod(c,r['date'])
        if not flag(r,'source_complete'):raise ReviewRequired('Recharge cost population incomplete')
        alloc=rows(r['allocations'],False);agree(sum((fraction(a['share']) for a in alloc),ZERO),1,'Recharge allocation weights');pool=nonnegative(r['cost_pool']);markup=nonnegative(r['markup'])
        if markup>1:raise ReviewRequired('Exceptional markup requires separate transfer pricing review')
        target=cash(pool*(1+markup));distributed=ZERO
        for index,a in enumerate(alloc):
            required(a,'entity','pair_id','share')
            if a['entity']==r['provider'] or a['pair_id'] not in {p['id'] for p in pairs}:raise ReviewRequired('Recharge bilateral entity/pair invalid')
            amount=target-distributed if index==len(alloc)-1 else cash(target*fraction(a['share']));distributed+=amount
            p=next(p for p in pairs if p['id']==a['pair_id'])
            if p['entity_a']!=r['provider'] or p['entity_b']!=a['entity'] or p['currency']!=r['currency']:raise ReviewRequired('Recharge agreement differs from bilateral pair')
            agree(p['recharge'],amount,'Recharge to bilateral transaction');recharge_total+=amount
            # Local book currency remeasurement is separate below.
            journals.append({'entity':r['provider'],'lines':journal(('Dr','intercompany receivable',cash(amount*positive(p['initial_rate_a']))),('Cr','recharge income',cash(amount*positive(p['initial_rate_a']))))})
            journals.append({'entity':a['entity'],'lines':journal(('Dr','recharge expense',cash(amount*positive(p['initial_rate_b']))),('Cr','intercompany payable',cash(amount*positive(p['initial_rate_b']))))})
    for p in pairs:
        approval(p,c);required(p,'entity_a','entity_b','currency','transaction_id','opening_a','opening_b','recharge','settled_a','settled_b','settlement_evidence','confirmed_a','confirmed_b','rate_a','rate_b','initial_rate_a','initial_rate_b','book_a','book_b','gl_a','gl_b','rate_evidence','mismatch_items','date')
        inperiod(c,p['date'])
        if p['entity_a']==p['entity_b'] or p['transaction_id'] in transactions:raise ReviewRequired('Bilateral entity or duplicate transaction invalid')
        transactions.add(p['transaction_id'])
        a=nonnegative(p['opening_a'])+nonnegative(p['recharge'])-nonnegative(p['settled_a']);b=nonnegative(p['opening_b'])+nonnegative(p['recharge'])-nonnegative(p['settled_b'])
        if a<0 or b<0 or p['mismatch_items']:raise ReviewRequired('Unresolved timing, principal, tax or FX intercompany mismatch')
        agree(a,b,'Reciprocal foreign principal');agree(p['confirmed_a'],a,'A bilateral confirmation');agree(p['confirmed_b'],b,'B bilateral confirmation')
        local_a=cash(a*positive(p['rate_a']));local_b=cash(b*positive(p['rate_b']));fxa=local_a-nonnegative(p['book_a']);fxb=local_b-nonnegative(p['book_b'])
        agree(p['gl_a'],local_a,'A monetary GL');agree(p['gl_b'],local_b,'B monetary GL')
        if nonnegative(p['settled_a']):journals.append({'entity':p['entity_a'],'lines':journal(('Dr','cash',cash(nonnegative(p['settled_a'])*positive(p['settlement_rate_a']))),('Cr','intercompany receivable',cash(nonnegative(p['settled_a'])*positive(p['settlement_rate_a']))))})
        if nonnegative(p['settled_b']):journals.append({'entity':p['entity_b'],'lines':journal(('Dr','intercompany payable',cash(nonnegative(p['settled_b'])*positive(p['settlement_rate_b']))),('Cr','cash',cash(nonnegative(p['settled_b'])*positive(p['settlement_rate_b']))))})
        journals.append({'entity':p['entity_a'],'lines':movement('intercompany receivable','FX gain or loss',fxa)});journals.append({'entity':p['entity_b'],'lines':movement('FX gain or loss','intercompany payable',fxb)})
        work.append({'pair':p['id'],'foreign_principal':a,'a_functional':local_a,'b_functional':local_b,'a_fx_gain':fxa,'b_fx_loss':fxb})
    population(c,pairs,[nonnegative(p['opening_a'])+nonnegative(p['recharge']) for p in pairs])
    # Standard journal envelope stays balanced; entity ownership is preserved
    # in the numeric workpaper and journal index, never netted across books.
    return finish('Bilateral principal, approved recharge allocations and local monetary balances reconciled.',{'pairs':work,'recharges':recharge_total,'journal_entities':[j['entity'] for j in journals]},[j['lines'] for j in journals],
      ['Settlement cutoff and transaction FX require source evidence; balanced group totals do not prove reciprocal principal.','No arm\'s-length conclusion, group elimination or unrealized-profit plug is generated.'],
      ['Related-party transactions/balances, FX and recharge policies require entity and group presentation review.'])
