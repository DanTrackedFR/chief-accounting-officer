"""Instrument classification, EIR measurement and framework-specific impairment."""
from decimal import Decimal
from core_accounting import cash, dec, required, ReviewRequired, journal
from production import flag, fraction, nonnegative

def discount(value):
    n=fraction(value)
    if n<=0:raise ReviewRequired('Discount factor must be positive')
    return n

def classify(c):
    i=c['instrument'];required(i,'kind','classification_memo','measurement','impairment_model')
    fw=c['framework']; model=i['impairment_model']
    if i['kind'] in ('guarantee','commitment'):raise ReviewRequired('Liability/equity/guarantee/commitment requires instrument-specific measurement and journals; do not use asset ECL workpaper')
    if i['kind'] not in ('debt_asset','trade_receivable','contract_asset','equity_asset','debt_liability','commitment','guarantee','lease_receivable'):
        raise ReviewRequired('Derivatives, compound instruments or other instruments require specialist classification')
    if fw=='UK_GAAP':
        election=c['policy_elections'].get('financial_instruments')
        if election not in ('sections11_12','IFRS9','IAS39'): raise ReviewRequired('Resolve permitted UK financial instrument election and edition')
        if election=='IAS39': raise ReviewRequired('IAS39 elected measurement requires its specialist workflow')
        if election=='sections11_12':
            if model not in ('incurred_loss','none'):raise ReviewRequired('FRS102 own model does not import IFRS9 staging')
            if c['credit']['method'] != 'cash_shortfall':raise ReviewRequired('UK incurred loss uses evidenced discounted recoverable cash flows, not an unconditioned expected-loss portfolio')
            required(i,'basic_instrument_assessment')
            if i['measurement']!='amortized_cost' or model!='incurred_loss':raise ReviewRequired('Own UK model workpaper supports basic amortized-cost assets and incurred-loss only')
            return i['measurement'],model
        fw='IFRS'
    if fw in ('IFRS','AASB'):
        if i['kind'] in ('debt_asset','trade_receivable','contract_asset'):
            required(i,'business_model','sppi')
            sppi=flag(i,'sppi')
            category='amortized_cost' if sppi and i['business_model']=='hold_collect' else 'FVOCI' if sppi and i['business_model']=='collect_sell' else 'FVTPL'
            if i['measurement']!=category:raise ReviewRequired('Business-model/SPPI classification mismatch')
            if category=='FVTPL' and model!='none':raise ReviewRequired('FVTPL credit effects are in fair value, not an ECL allowance')
            if category!='FVTPL' and model=='none':raise ReviewRequired('Applicable debt assets require impairment assessment')
        elif i['kind']=='lease_receivable':
            if i['measurement']!='lease_net_investment':raise ReviewRequired('Lease receivable impairment requires reviewed lease net investment')
        elif i['kind']=='equity_asset' and model!='none':raise ReviewRequired('Equity investments have no ECL allowance')
        if model not in ('general','simplified','poci','none'):raise ReviewRequired('IFRS9 model required')
        if model=='simplified' and i['kind'] not in ('trade_receivable','contract_asset','lease_receivable'):
            raise ReviewRequired('Simplified ECL is not available for ordinary loans')
    elif fw=='US_GAAP':
        if 'stage' in i:raise ReviewRequired('USCECL does not use IFRS staging')
        if model not in ('CECL','AFS','none'):raise ReviewRequired('US instrument-specific CECL/AFS scope required')
        if model=='none' and i['measurement'] not in ('FVTPL',):raise ReviewRequired('US debt assets require CECL/AFS or documented out-of-scope specialist assessment')
        if model=='AFS' and i['measurement']!='AFS':raise ReviewRequired('AFS model requires AFS debt security')
        if model=='CECL' and i['measurement'] not in ('amortized_cost','lease_net_investment','off_balance'):
            raise ReviewRequired('CECL measurement scope mismatch')
    return i['measurement'],model

def assess(c,claims):
    required(c,'instrument','credit','allowance_bridge','measurement_schedule','specialist_items')
    if c['specialist_items']:raise ReviewRequired('Unresolved instrument specialists: '+', '.join(c['specialist_items']))
    i=c['instrument'];required(i,'kind')
    if i['kind'] in ('debt_liability','equity_asset'):return non_credit_instrument(c,claims)
    category,model=classify(c);i=c['instrument']; cr=c['credit'];required(cr,'method','assumptions_memo','scenarios','overlay','overlay_memo')
    stage=None
    if model=='general':
        stage=3 if flag(cr,'credit_impaired') else 2 if flag(cr,'sicr') else 1
        required(cr,'origination_risk_evidence','current_risk_evidence','default_definition','horizon')
        expected='12_month_default_events' if stage==1 else 'lifetime_default_events'
        if cr['horizon']!=expected:raise ReviewRequired('Default-event horizon conflicts with stage')
    elif model in ('simplified','CECL'):
        if cr.get('horizon')!='lifetime_default_events':raise ReviewRequired('Lifetime expected loss horizon required')
    elif model=='poci':
        raise ReviewRequired('POCI needs credit-adjusted EIR and cumulative lifetime-ECL change schedule; no ordinary day-one allowance')
    ms=c['measurement_schedule'];required(ms,'opening_gross','eir','cash_flows','additions','writeoffs','fx','fair_value')
    opening=nonnegative(ms['opening_gross']);rate=dec(ms['eir'])
    if ms.get('fx_journals') or dec(ms['fx'])!=0 or dec(c['allowance_bridge']['fx'])!=0:
        required(ms,'fx_journals','fx_memo')
        from core_accounting import balance
        for j in ms['fx_journals']:balance(j)
        delta=sum(dec(l['amount'])*(1 if l['side']=='Dr' else -1) for j in ms['fx_journals'] for l in j if l['account']=='instrument gross carrying amount')
        allowance_delta=sum(dec(l['amount'])*(1 if l['side']=='Cr' else -1) for j in ms['fx_journals'] for l in j if l['account']==('loss allowance (OCI)' if category=='FVOCI' else 'loss allowance'))
        if cash(delta)!=cash(ms['fx']) or cash(allowance_delta)!=cash(c['allowance_bridge']['fx']):raise ReviewRequired('FX journals do not reconcile gross/allowance movements')
    if rate<0:raise ReviewRequired('Negative yield needs separately reviewed signed-interest mechanics')
    interestbase=opening
    if stage==3: interestbase=opening-nonnegative(c['allowance_bridge']['opening'])
    interest=cash(interestbase*rate)
    gross_interest=cash(opening*rate)
    flows=nonnegative(ms['cash_flows']); gross=cash(opening+gross_interest+dec(ms['additions'])-flows-nonnegative(ms['writeoffs'])+dec(ms['fx']))
    if gross<0:raise ReviewRequired('Gross instrument rollforward is negative')
    entries=[]
    if stage==3 and category=='FVOCI':raise ReviewRequired('Credit-impaired FVOCI interest/OCI reconciliation requires its specialist schedule')
    if gross_interest:entries.append(journal(('Dr','instrument gross carrying amount',gross_interest),('Cr','interest revenue',interest),('Cr','loss allowance',gross_interest-interest)))
    if flows:entries.append(journal(('Dr','cash',flows),('Cr','instrument gross carrying amount',flows)))
    if dec(ms['additions']):entries.append(journal(('Dr','instrument gross carrying amount',nonnegative(ms['additions'])),('Cr','cash / payable',nonnegative(ms['additions']))))
    allowance=Decimal(0);scenario_rows=[]
    if model!='none':
        if model=='incurred_loss' and not flag(cr,'objective_impairment_evidence'):
            allowance=Decimal(0)
        else:
            scenarios=cr['scenarios']
            if not scenarios or sum(fraction(s['weight']) for s in scenarios)!=1:raise ReviewRequired('Scenario weights must total one')
            for s in scenarios:
                required(s,'weight','terms');loss=Decimal(0)
                terms=s['terms']
                if not terms:raise ReviewRequired('Missing credit term structure')
                sum_pd=Decimal(0)
                for term in terms:
                    if cr['method']=='pd_lgd':
                        required(term,'ead','marginal_pd','lgd','discount_factor')
                        pd=fraction(term['marginal_pd']);sum_pd+=pd
                        loss+=nonnegative(term['ead'])*pd*fraction(term['lgd'])*discount(term['discount_factor'])
                    elif cr['method']=='cash_shortfall':
                        required(term,'contractual_cash','expected_cash','discount_factor')
                        shortfall=nonnegative(term['contractual_cash'])-nonnegative(term['expected_cash'])
                        if shortfall<0:raise ReviewRequired('Recoveries exceeding cash due require separate gain analysis')
                        loss+=shortfall*discount(term['discount_factor'])
                    elif cr['method']=='loss_rate':
                        loss+=nonnegative(term['exposure'])*fraction(term['loss_rate'])
                    else:raise ReviewRequired('Unsupported credit-loss method')
                if sum_pd>1:raise ReviewRequired('Marginal default probabilities exceed one; use survival-adjusted PDs')
                weighted=loss*fraction(s['weight']);allowance+=weighted;scenario_rows.append({'loss':cash(loss),'weighted':cash(weighted)})
            allowance=cash(allowance+dec(cr['overlay']))
    if allowance<0:raise ReviewRequired('Negative closing allowance')
    if category!='off_balance' and allowance>gross:raise ReviewRequired('Allowance exceeds gross balance')
    if model=='AFS':
        required(i,'intent_to_sell','required_to_sell_before_recovery')
        if flag(i,'intent_to_sell') or flag(i,'required_to_sell_before_recovery'):
            raise ReviewRequired('AFS required/intent sale: write down amortized cost to FV rather than ordinary allowance')
        allowance=min(allowance,max(Decimal(0),gross-nonnegative(ms['fair_value'])))
    bridge=c['allowance_bridge'];required(bridge,'opening','writeoffs','recoveries','fx')
    if nonnegative(bridge['writeoffs'])!=nonnegative(ms['writeoffs']):raise ReviewRequired('Gross and allowance write-offs mismatch')
    openingallowance=nonnegative(bridge['opening']);wo=nonnegative(bridge['writeoffs']);rec=nonnegative(bridge['recoveries']);fx=dec(bridge['fx'])
    net_interest_adjustment=cash(gross_interest-interest)
    expense=cash(allowance-openingallowance+wo-rec-fx-net_interest_adjustment)
    account='commitment provision' if category=='off_balance' else 'loss allowance (OCI)' if category=='FVOCI' else 'loss allowance'
    if expense>=0:entries.append(journal(('Dr','credit loss expense',expense),('Cr',account,expense)))
    else:entries.append(journal(('Dr',account,-expense),('Cr','credit loss reversal',-expense)))
    if wo:entries.append(journal(('Dr',account,wo),('Cr','instrument gross carrying amount',wo)))
    if rec:entries.append(journal(('Dr','cash',rec),('Cr',account,rec)))
    entries.extend(ms.get('fx_journals',[]))
    fair_value_adjustment=Decimal(0)
    if category in ('FVOCI','FVTPL','AFS'):
        required(ms,'opening_fair_value_adjustment')
        fair_value_adjustment=cash(nonnegative(ms['fair_value'])-gross+(allowance if model=='AFS' else 0))
        period_fair_value_change=cash(fair_value_adjustment-dec(ms['opening_fair_value_adjustment']))
        # FVOCI debt credit losses affect OCI without reducing FV carrying value.
        other_side='fair value gain/loss' if category=='FVTPL' else 'OCI fair value reserve'
        if period_fair_value_change>=0:entries.append(journal(('Dr','instrument fair value adjustment',period_fair_value_change),('Cr',other_side,period_fair_value_change)))
        else:entries.append(journal(('Dr',other_side,-period_fair_value_change),('Cr','instrument fair value adjustment',-period_fair_value_change)))
    return {'conclusion':f'Instrument {category}; impairment {model}; closing allowance {allowance}, period credit loss expense {expense}.',
        'method':{'classification':category,'impairment':model,'stage':stage,'credit_method':cr['method']},
        'calculations':{'gross_carrying_amount':gross,'interest_revenue':interest,'allowance':allowance,'expense':expense,'scenarios':scenario_rows,
         'allowance_bridge':{'opening':openingallowance,'expense':expense,'writeoffs':wo,'recoveries':rec,'fx':fx,'net_interest_adjustment':net_interest_adjustment,'closing':allowance},'fair_value_adjustment':fair_value_adjustment},
        'journal_entry_implications':entries,'judgments':[i['classification_memo'],cr['assumptions_memo'],cr['overlay_memo']],
        'uncertainties':['EIR, credit horizon, collateral recoveries and forecast assumptions are reviewed inputs; source forecast uncertainty remains.'],
        'open_items':[], 'disclosures_impacted':['Instrument classes and measurement categories','Credit concentrations, collateral and maximum exposure','Default/SICR definitions, segmentation and forward-looking assumptions','Allowance movements by class/stage and gross exposure changes','Write-offs, modifications, recoveries and credit-impaired balances','Liquidity maturities, market risk and fair value hierarchy','Apply UK elected-model disclosure and AASB tier requirements independently']}


def non_credit_instrument(c,claims):
    """Amortized-cost liabilities and fair-value equity investment schedules."""
    i=c['instrument'];m=c['measurement_schedule'];required(i,'classification_memo','measurement','impairment_model')
    if i['impairment_model']!='none':raise ReviewRequired('Debt liability and equity investment do not use asset ECL allowance')
    if c['framework']=='UK_GAAP':
        election=c['policy_elections'].get('financial_instruments')
        if election not in ('sections11_12','IFRS9'):raise ReviewRequired('UK non-credit instrument election unresolved or IAS39 specialist required')
        if election=='sections11_12':required(i,'basic_instrument_assessment')
    required(m,'opening_gross','cash_flows','additions','eir','fair_value','fx','writeoffs')
    if dec(m['fx'])!=0 or dec(m['writeoffs'])!=0:raise ReviewRequired('Modification/derecognition/FX requires instrument event schedule')
    opening=nonnegative(m['opening_gross']);additions=nonnegative(m['additions']);cashflow=nonnegative(m['cash_flows']);entries=[]
    if i['kind']=='debt_liability':
        if i['measurement']!='amortized_cost':raise ReviewRequired('Fair-value option/own-credit liability measurement requires specialist schedule')
        rate=dec(m['eir'])
        if rate<0:raise ReviewRequired('Negative-yield liability requires signed-interest specialist schedule')
        interest=cash(opening*rate);closing=cash(opening+additions+interest-cashflow)
        if closing<0:raise ReviewRequired('Liability repayments exceed carrying amount')
        entries=[journal(('Dr','finance cost',interest),('Cr','debt liability',interest)),
                 journal(('Dr','cash',additions),('Cr','debt liability',additions)),
                 journal(('Dr','debt liability',cashflow),('Cr','cash',cashflow))]
        method='Amortized-cost liability effective-interest rollforward'
    else:
        if i['measurement'] not in ('FVTPL','FVOCI'):raise ReviewRequired('Equity measurement alternative/cost requires specialist route')
        if i['measurement']=='FVOCI':
            if c['framework']=='US_GAAP':raise ReviewRequired('ASC321 equity has no IFRS-style FVOCI election')
            if c['framework']=='UK_GAAP' and c['policy_elections'].get('financial_instruments')!='IFRS9':raise ReviewRequired('UK equity FVOCI requires permitted IFRS9 election')
            if not flag(i,'fvoci_irrevocable_election') or flag(i,'held_for_trading'):raise ReviewRequired('Equity FVOCI election/eligibility not established')
        if cashflow:raise ReviewRequired('Equity disposal needs cost/proceeds and OCI transfer schedule, not debt repayment mechanics')
        closing=cash(nonnegative(m['fair_value']));interest=cash(closing-opening-additions)
        account='OCI equity reserve (no recycling)' if i['measurement']=='FVOCI' else 'fair value gain/loss'
        entries.append(journal(('Dr','equity investment',additions),('Cr','cash',additions)))
        if interest>=0:entries.append(journal(('Dr','equity investment',interest),('Cr',account,interest)))
        else:entries.append(journal(('Dr',account,-interest),('Cr','equity investment',-interest)))
        method='Equity investment fair-value measurement'
    return {'conclusion':f"{method}: closing carrying amount {closing}; period interest/fair-value change {interest}.",
        'method':method,'calculations':{'opening':opening,'additions':additions,'interest_or_fv_change':interest,'cash':cashflow,'closing':closing},
        'journal_entry_implications':entries,'judgments':[i['classification_memo']], 'uncertainties':['Fair-value hierarchy and instrument-specific classification/elections require supporting evidence.'],
        'open_items':[],'disclosures_impacted':['Instrument category and policy/elections','Carrying amount reconciliation','Fair value hierarchy and valuation sensitivity','Debt maturity and covenant/liquidity disclosures as applicable']}
