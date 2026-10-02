from reporting_accounting import *

def assess(c,claims):
    common(c,'components','events','share_register','statement','handoffs','component_inventory')
    specialist(c,'legal','Legal capital');specialist(c,'instruments','Financial Instruments');specialist(c,'sbc','Share-Based Compensation');specialist(c,'group','Consolidation')
    components=rows(c['components'],False);inventory(c,'component_inventory',components);byid={r['id']:r for r in components};balances={r['id']:dec(r['opening']) for r in components};effects={id:ZERO for id in byid};entries=[];work=[]
    for r in components:
        reviewed(r,c,'classification_memo');required(r,'opening','closing','gl_closing','equity_owner','role')
        if r['equity_owner'] not in ['parent','nci'] or r['role'] not in ['capital','profit','oci']:raise ReviewRequired('Equity owner/component role unresolved')
        roles={'share_capital':'capital','premium':'capital','treasury':'capital','retained_earnings':'profit','oci':'oci'}
        if r['id'] in roles and (r['equity_owner']!='parent' or r['role']!=roles[r['id']]):raise ReviewRequired('Ordinary parent equity component mapping contradicts accounting journals')
        if r['id']=='treasury' and dec(r['opening'])>0:raise ReviewRequired('Treasury opening must be contra-equity')
    def shift(id,n):
        if id not in byid:raise ReviewRequired('Missing equity component')
        balances[id]+=n;effects[id]+=n
    issued=ZERO;repurchased=ZERO;reissued=ZERO;events=rows(c['events']);dividend_payable=nonnegative(c['statement']['opening_dividend_payable']);shares=nonnegative(c['share_register']['opening_issued']);ownshares=nonnegative(c['share_register']['opening_own']);import_ids=set()
    if ownshares>shares:raise ReviewRequired('Opening own-share register exceeds issued shares')
    for e in sorted(events,key=lambda e:(iso(e['date']),e['id'])):
        reviewed(e,c,'accounting_memo','legal_evidence');required(e,'kind','date','amount','equity_classified');inperiod(c,e['date']);kind=e['kind'];n=nonnegative(e['amount']);lines=[]
        if not flag(e,'equity_classified'):raise ReviewRequired('Liability/compound/redeemable instrument requires classification specialist')
        if kind=='issue':
            required(e,'shares','par_value','issue_price','incremental_cost','nonqualifying_cost','cost_basis','ordinary')
            if not flag(e,'ordinary'):raise ReviewRequired('Convertible/warrant/share issue requires specialist allocation')
            count=positive(e['shares']);par=nonnegative(e['par_value']);price=positive(e['issue_price']);cost=nonnegative(e['incremental_cost']);expense=nonnegative(e['nonqualifying_cost']);gross=cash(count*price);capital=cash(count*par)
            if capital>gross or cost>gross-capital:raise ReviewRequired('Par or issue costs require legal capital allocation review')
            agree(n,gross,'Issue cash');shift('share_capital',capital);shift('premium',gross-capital-cost);shares+=count;issued+=count
            lines=journal(('Dr','cash',gross),('Cr','share_capital',capital),('Cr','premium',gross-capital));entries.append(lines);entries.append(journal(('Dr','premium',cost),('Dr','issue cost expense',expense),('Cr','cash',cost+expense)));lines=[]
        elif kind=='treasury_buy':
            required(e,'shares','cost_method_memo');count=positive(e['shares'])
            if ownshares+count>shares:raise ReviewRequired('Own shares exceed issued register')
            shift('treasury',-n);ownshares+=count;repurchased+=count;lines=journal(('Dr','treasury',n),('Cr','cash',n))
        elif kind=='treasury_reissue':
            required(e,'shares','carrying_cost','cost_method_memo','loss_allocation')
            count=positive(e['shares']);book=nonnegative(e['carrying_cost']);loss=max(book-n,ZERO);gain=max(n-book,ZERO)
            if count>ownshares or book>-balances.get('treasury',ZERO):raise ReviewRequired('Treasury disposal exceeds cost/share inventory')
            gain_component='premium';allowed_loss=['premium','retained_earnings'];method=None
            if c['framework']=='US_GAAP':
                required(e,'treasury_handoff');method=specialist(c,e['treasury_handoff'],'Treasury Shares Accounting',n);policy(c,method);required(method,'method','gain_component','loss_capacity','allocation_memo','allocation_rule')
                texts(method,'allocation_memo')
                if method['method']!='cost' or method['allocation_rule']!='reserve_first':raise ReviewRequired('US treasury par-value/other allocation method lacks approved executable route')
                gain_component=method['gain_component']
                if gain_component!='treasury_apic' or gain_component not in byid or byid[gain_component]['equity_owner']!='parent' or byid[gain_component]['role']!='capital':raise ReviewRequired('US treasury gains require separately substantiated treasury APIC component')
                if not isinstance(method['loss_capacity'],dict) or set(method['loss_capacity'])!={'treasury_apic'}:raise ReviewRequired('Qualified treasury APIC loss-capacity source required')
                capacity=nonnegative(method['loss_capacity']['treasury_apic'])
                if capacity>balances['treasury_apic']:raise ReviewRequired('Treasury APIC capacity exceeds substantiated reserve')
                allowed_loss=['treasury_apic','retained_earnings']
            allocation=rows(e['loss_allocation']);agree(sum((nonnegative(a['amount']) for a in allocation),ZERO),loss,'Treasury loss allocation')
            for a in allocation:
                required(a,'component','amount');v=nonnegative(a['amount'])
                if a['component'] not in allowed_loss:raise ReviewRequired('Treasury loss cannot enter P&L, ordinary US issuance premium or arbitrary reserve')
                shift(a['component'],-v)
            if method:
                allocated=sum((nonnegative(a['amount']) for a in allocation if a['component']=='treasury_apic'),ZERO)
                agree(allocated,min(loss,capacity),'Treasury reserve-first loss allocation')
            shift('treasury',book);shift(gain_component,gain);ownshares-=count;reissued+=count;lines=journal(('Dr','cash',n),('Dr',gain_component,sum((nonnegative(a['amount']) for a in allocation if a['component']==gain_component),ZERO)),('Dr','retained_earnings',sum((nonnegative(a['amount']) for a in allocation if a['component']=='retained_earnings'),ZERO)),('Cr','treasury',book),('Cr',gain_component,gain))
            if method:
                required(e,'source_entries','source_journal_ids');src=e['source_entries'];sourceids=e['source_journal_ids']
                if not isinstance(src,list) or not src or not isinstance(sourceids,list) or len(src)!=len(sourceids) or len(sourceids)!=len(set(sourceids)) or any(not isinstance(i,str) or not i or i in import_ids for i in sourceids):raise ReviewRequired('Qualified US treasury source journals require exact-once identifiers')
                for j in src:balance(j)
                def aggregate(js):
                    out={}
                    for j in js:
                        for l in j:
                            key=(l['account'],l['side']);out[key]=out.get(key,ZERO)+dec(l['amount'])
                    return out
                if aggregate(src)!=aggregate([lines]):raise ReviewRequired('Qualified US treasury journals differ from complete calculated allocation')
                import_ids.update(sourceids)
        elif kind=='dividend_declared':shift('retained_earnings',-n);dividend_payable+=n;lines=journal(('Dr','retained_earnings',n),('Cr','dividends payable',n))
        elif kind=='dividend_paid':
            if n>dividend_payable:raise ReviewRequired('Distribution payment exceeds approved declared payable')
            dividend_payable-=n;lines=journal(('Dr','dividends payable',n),('Cr','cash',n))
        elif kind=='capital_reduction':
            required(e,'from_component','to_component','cash_settlement','shares_cancelled','court_or_legal_approval')
            texts(e,'court_or_legal_approval')
            if e['from_component'] not in ['share_capital','premium'] or n>balances[e['from_component']]:raise ReviewRequired('Capital reduction exceeds authorized component')
            shift(e['from_component'],-n);cancel=nonnegative(e['shares_cancelled'])
            if cancel>shares-ownshares:raise ReviewRequired('Capital reduction cancellation exceeds outstanding shares')
            shares-=cancel
            if flag(e,'cash_settlement'):lines=journal(('Dr',e['from_component'],n),('Cr','cash',n))
            else:shift(e['to_component'],n);lines=journal(('Dr',e['from_component'],n),('Cr',e['to_component'],n))
        elif kind in ['profit','oci','sbc','group_change','retrospective_adjustment']:
            required(e,'component','signed_amount','source_entries','handoff_key')
            amount=dec(e['signed_amount']);agree(n,abs(amount),'Imported equity amount');specialist(c,e['handoff_key'],{'profit':'Financial Statements','oci':'Financial Statements','sbc':'Share-Based Compensation','group_change':'Consolidation','retrospective_adjustment':'Accounting Changes'}[kind],amount)
            src=e['source_entries']
            if not isinstance(src,list):raise ReviewRequired('Imported source entries array required')
            for j in src:balance(j)
            if src:
                required(e,'source_journal_ids');sourceids=e['source_journal_ids']
                if not isinstance(sourceids,list) or len(sourceids)!=len(src) or len(sourceids)!=len(set(sourceids)) or any(not isinstance(i,str) or not i or i in import_ids for i in sourceids):raise ReviewRequired('Imported equity source journals require unique exact-once identifiers')
                import_ids.update(sourceids)
            if kind not in ['profit','oci'] and not src:raise ReviewRequired('Accounting movement requires supported source journals')
            if src:agree(sum((line_delta(j,e['component']) for j in src),ZERO),amount,'Imported journal equity effect')
            if e['component'] not in byid:raise ReviewRequired('Imported equity component absent from inventory')
            if kind in ['profit','oci'] and byid[e['component']]['role']!=kind:raise ReviewRequired('Profit and OCI component classification mismatch')
            if byid[e['component']]['equity_owner']=='nci':specialist(c,'group','Consolidation')
            if src:
                for component in byid:shift(component,sum((line_delta(j,component) for j in src),ZERO))
            else:shift(e['component'],amount)
            entries.extend(src)
        else:raise ReviewRequired('Equity event scope unsupported')
        if lines:entries.append(lines)
        work.append({'id':e['id'],'kind':kind,'amount':n})
    for id,r in byid.items():agree(r['closing'],balances[id],'Equity component movement');agree(r['gl_closing'],balances[id],'Equity component GL')
    if balances.get('treasury',ZERO)>0:raise ReviewRequired('Closing treasury cannot become positive equity')
    total=sum(balances.values(),ZERO);s=c['statement'];agree(s['closing_equity'],total,'Statement equity');agree(s['opening_equity'],sum((dec(r['opening']) for r in components),ZERO),'Opening equity');agree(s['closing_dividend_payable'],dividend_payable,'Dividend payable GL');agree(c['share_register']['closing_issued'],shares,'Issued cap table');agree(c['share_register']['closing_own'],ownshares,'Own-share cap table')
    population(c,events,[nonnegative(e['amount']) for e in events])
    return finish('Capital register, owner transactions and every equity component reconcile.',{'components':balances,'movements':effects,'opening':dec(s['opening_equity']),'closing':total,'issued_shares':shares,'own_shares':ownshares,'dividend_payable':dividend_payable,'events':work},entries,
      ['Credit-positive equity and negative treasury contra-equity are separate components. Legal capital, equity classification, tax and NCI conclusions are externally reviewed inputs.'],
      ['Capital/share counts, premium/treasury costs, owner/nonowner changes, parent/NCI reserves, OCI and retrospective comparatives.'])
