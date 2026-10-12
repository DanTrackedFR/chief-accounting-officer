"""Transaction remeasurement and independently reconciled foreign-operation CTA."""
from core_accounting import cash, dec, required, ReviewRequired, journal
from production import flag, fraction, nonnegative
from advanced_accounting import gate, positive, event_date, unique, movement, result, ZERO

def assess(c,claims):
    gate(c,'currency','items','translation','disposal')
    cur=c['currency'];required(cur,'functional','presentation','ledger','functional_memo','rate_source','rate_convention',
      'functional_review_complete','hyperinflation','exchangeability','functional_change','net_investment_items')
    if not flag(cur,'functional_review_complete'):raise ReviewRequired('Functional currency needs economic indicator assessment')
    if cur['rate_convention']!='functional_per_foreign':raise ReviewRequired('Transaction rate quote convention must be functional currency per foreign unit')
    if flag(cur,'hyperinflation') or not flag(cur,'exchangeability') or flag(cur,'functional_change') or flag(cur,'net_investment_items'):
        raise ReviewRequired('Hyperinflation, exchangeability, currency changes or net investment need separate framework specialist method')
    if cur['ledger']!=cur['functional']:raise ReviewRequired('Full ledger-to-functional remeasurement must precede transaction/translation workflow')
    if c['items']:
        unique(c['items'])
    elif not isinstance(c['items'],list) or c.get('translation',{}).get('enabled') is not True:
        raise ReviewRequired('Empty transaction population requires an explicit foreign-operation translation')
    entries=[];remeasure=ZERO;schedules=[]
    for x in c['items']:
        required(x,'type','side','account','foreign_amount','initial_rate','closing_rate','settled_foreign','settlement_rate',
          'initial_date','memo','opening_book','opening_route','opening_rate')
        if 'settlement_date' not in x:raise ReviewRequired('Settlement date must be explicit, including null for none')
        event_date(c,x['initial_date'])
        if x['settlement_date'] is not None:
            event_date(c,x['settlement_date'])
            if x['settlement_date']<x['initial_date']:raise ReviewRequired('Settlement precedes recognition')
        if x['side'] not in ('asset','liability') or x['type'] not in ('monetary','historical_nonmonetary','fair_value_nonmonetary'):
            raise ReviewRequired('Item classification unresolved')
        foreign=nonnegative(x['foreign_amount']);settled=nonnegative(x['settled_foreign'])
        if settled>foreign:raise ReviewRequired('Settlement exceeds foreign position')
        initial=cash(foreign*positive(x['initial_rate']));opening=cash(nonnegative(x['opening_book']))
        if x['opening_route']=='initial':
            if x['initial_date']<c['period_start'] or opening!=initial:raise ReviewRequired('Opening recognition amount/rate/period does not reconcile')
        elif x['opening_route']=='carried_monetary':
            if x['type']!='monetary' or x['initial_date']>=c['period_start'] or opening!=cash(foreign*positive(x['opening_rate'])):
                raise ReviewRequired('Carried monetary opening balance/rate does not reconcile')
        else:raise ReviewRequired('Unknown transaction opening route')
        settlement=cash(settled*positive(x['settlement_rate']));closing_rate=positive(x['closing_rate'])
        if settled and x['settlement_date'] is None:raise ReviewRequired('Dated settlement required')
        remaining=foreign-settled
        if x['type']=='monetary':closing=cash(remaining*closing_rate);origin='FX income'
        elif x['type']=='historical_nonmonetary':
            if settled:raise ReviewRequired('Disposal of nonmonetary asset requires disposal method')
            closing=initial;origin='FX income'
        else:
            required(x,'fair_value_foreign','fair_value_rate','fair_value_date','measurement_origin')
            event_date(c,x['fair_value_date'])
            if settled or x['measurement_origin'] not in ('P&L','OCI'):raise ReviewRequired('Fair-value nonmonetary disposal/origin unresolved')
            closing=cash(nonnegative(x['fair_value_foreign'])*positive(x['fair_value_rate']))
            origin='fair value income' if x['measurement_origin']=='P&L' else 'fair value OCI'
        change=cash(closing+settlement-opening);gain=change if x['side']=='asset' else -change
        if x['side']=='asset':
            entries.append(movement(x['account'],origin,change))
            entries.append(journal(('Dr','cash',settlement),('Cr',x['account'],settlement)))
        else:
            entries.append(movement(origin,x['account'],change))
            entries.append(journal(('Dr',x['account'],settlement),('Cr','cash',settlement)))
        if x['type']=='monetary':remeasure+=gain
        schedules.append({'id':x['id'],'initial':initial,'settlement':settlement,'closing':closing,'gain':gain,'origin':origin})
    t=c['translation'];required(t,'enabled')
    calcs={'transactions':schedules,'monetary_fx_profit':remeasure}
    if flag(t,'enabled'):
        required(t,'operation_id','valuation_date','functional_currency','presentation_currency','quote','tb','opening_net_assets','opening_rate','closing_rate',
          'profit','profit_rate','flows','other_oci','other_oci_rate','opening_cta','reported_closing_net_assets','ownership','memo','rates_approximate_dates')
        if t['quote']!='presentation_per_functional' or t['functional_currency']==t['presentation_currency']:
            raise ReviewRequired('Translation layer currencies/quote convention invalid')
        if t['presentation_currency']!=cur['presentation']:raise ReviewRequired('Foreign operation must translate to reporting presentation currency')
        event_date(c,t['valuation_date'])
        if not flag(t,'rates_approximate_dates'):raise ReviewRequired('Average rate cannot approximate transaction dates; use dated transaction population')
        unique(t['tb']);tb=t['tb']
        if cash(sum((dec(x['balance']) for x in tb),ZERO))!=0:raise ReviewRequired('Foreign-operation functional TB does not balance')
        close_rate=positive(t['closing_rate']);profit=cash(dec(t['profit']));profit_trans=cash(profit*positive(t['profit_rate']))
        local_net=ZERO;translated_net=ZERO;translated_tb={};mapped_profit=ZERO
        for x in tb:
            required(x,'category','rate','memo')
            b=dec(x['balance']);r=positive(x['rate'])
            if x['category'] in ('asset','liability'):
                if r!=close_rate:raise ReviewRequired('Translate assets/liabilities at closing rate')
                local_net+=b;translated_net+=cash(b*r)
            elif x['category']=='profit':
                if r!=dec(t['profit_rate']):raise ReviewRequired('Profit rate differs from reviewed transaction approximation')
                mapped_profit-=b
            elif x['category']!='equity':raise ReviewRequired('Unknown translation TB category')
            translated_tb[x['id']]=cash(b*r)
        if cash(mapped_profit)!=profit or cash(local_net)!=cash(dec(t['reported_closing_net_assets'])):
            raise ReviewRequired('TB profit or closing net assets does not tie to bridge')
        opening=cash(dec(t['opening_net_assets']));flows=ZERO;translated_flows=ZERO
        for f in t['flows']:
            required(f,'amount','rate','date','memo');event_date(c,f['date'])
            flows+=dec(f['amount']);translated_flows+=cash(dec(f['amount'])*positive(f['rate']))
        other_oci=cash(dec(t['other_oci']));oci_trans=cash(other_oci*positive(t['other_oci_rate']))
        if cash(opening+profit+flows+other_oci)!=cash(local_net):raise ReviewRequired('Local net-asset rollforward incomplete')
        translated_open=cash(opening*positive(t['opening_rate']))
        cta=cash(translated_net-translated_open-profit_trans-translated_flows-oci_trans)
        # Independent bridge must agree with translated TB; not an arbitrary reserve plug.
        opening_cta=cash(dec(t['opening_cta']))
        if cash(sum(translated_tb.values()))!=opening_cta+cta:raise ReviewRequired('CTA bridge differs from translated historical equity/TB')
        owned=fraction(t['ownership']);nci=cash(cta*(1-owned));owners=cta-nci
        entries.extend([movement('translation clearing','owners translation OCI',owners),movement('translation clearing','NCI translation OCI',nci)])
        total=opening_cta+cta
        d=c['disposal'];required(d,'kind','memo')
        recycled=ZERO
        if d['kind']=='full':
            required(d,'date','qualifying_disposal_reviewed','owners_cta','nci_cta')
            event_date(c,d['date'])
            if t['valuation_date']!=d['date']:raise ReviewRequired('Disposal translation TB and rate must be measured at disposal date')
            if not flag(d,'qualifying_disposal_reviewed'):raise ReviewRequired('Disposal trigger requires rights/control review')
            owner_balance=cash(dec(d['owners_cta']));nci_balance=cash(dec(d['nci_cta']))
            if owner_balance+nci_balance!=total:raise ReviewRequired('Owner/NCI accumulated CTA does not tie')
            recycled=owner_balance
            entries.append(movement('owners translation reserve','disposal gain',owner_balance))
            entries.append(movement('NCI translation reserve','NCI derecognition clearing',nci_balance))
            closing_cta=ZERO
        elif d['kind']=='none':
            if t['valuation_date']!=c['reporting_period']:raise ReviewRequired('Continuing operation translation must use reporting-date TB/rate')
            closing_cta=total
        else:raise ReviewRequired('Partial disposal or retained-control transfer requires framework-specific specialist method')
        calcs['translation']={'translated_tb':translated_tb,'opening_net_translated':translated_open,'profit_translated':profit_trans,
          'closing_net_translated':translated_net,'cta_movement':cta,'owners_movement':owners,'nci_movement':nci,
          'opening_cta':opening_cta,'recycled_owners':recycled,'closing_cta':closing_cta}
    elif c['disposal'].get('kind')!='none':raise ReviewRequired('Disposal needs translated-operation reserve history')
    return result('Functional-currency transaction schedule and separate presentation-currency bridge reconcile.',
      {'framework':c['framework'],'functional':cur['functional'],'presentation':cur['presentation'],'layers':'remeasurement then translation'},
      calcs,entries,[cur['functional_memo'],cur['rate_source']]+[x['memo'] for x in c['items']],
      ['Functional/presentation currencies and changes','Transaction FX gains/losses separate from translation OCI','Translation reserve and NCI rollforwards',
       'Disposal reclassification and ownership changes','Rate-source uncertainty and lack-of-exchangeability disclosures where relevant'],
      ['Rates and functional currency are reviewed inputs. Monetary FX is not eliminated merely because an intragroup balance is eliminated. Hyperinflation, exchangeability, net investments and hedges require specialist methods.'])
