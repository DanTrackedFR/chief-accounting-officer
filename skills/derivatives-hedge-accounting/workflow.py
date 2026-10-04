"""Evidence-bound accounting owner; valuation and economic strategy stay external."""
from core_accounting import ReviewRequired, required, dec, cash, journal, balance
from datetime import date
from decimal import Decimal
import hashlib,json
ZERO=Decimal(0)

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()
def check(ok,message):
    if not ok:raise ReviewRequired(message)
def iso(v):
    try:return date.fromisoformat(v)
    except (ValueError,TypeError):raise ReviewRequired('ISO date required')
def text(r,*ks):
    for k in ks:check(isinstance(r.get(k),str) and bool(r[k].strip()),'Actual evidenced '+k+' required')
def boolean(r,k):
    check(type(r.get(k)) is bool,k+' requires evidenced boolean');return r[k]
def exact(a,b,label):check(cash(a)==cash(b),label+' does not reconcile')
def population(rs,label):
    check(isinstance(rs,list),label+' must be list')
    check(all(isinstance(r,dict) and isinstance(r.get('id'),str) and r['id'] for r in rs),'Invalid '+label)
    check(len({r['id'] for r in rs})==len(rs),'Duplicate '+label)
    return rs

def source(c,r,docs):
    text(r,'id','document_id');check(r['document_id'] in docs,'Missing actual source document')
    d=docs[r['document_id']]
    check(d['content']=={k:v for k,v in r.items() if k!='document_id'},'Source record differs from frozen independent evidence')
    return r

def signed_entry(account,amount,counter):
    amount=cash(amount)
    return journal(('Dr' if amount>=0 else 'Cr',account,abs(amount)),('Cr' if amount>=0 else 'Dr',counter,abs(amount)))

def lower(instrument,risk):
    i=dec(instrument);r=dec(risk)
    check(i*r<=0,'Hedging instrument and independently measured hedged risk do not offset')
    return (1 if i>=0 else -1)*min(abs(i),abs(r))

def ledger(c,entries,stocks):
    rs=population(c['gl'],'GL');by={r['id']:r for r in rs};delta={}
    for j in entries:
        balance(j)
        for l in j:delta[l['account']]=delta.get(l['account'],ZERO)+dec(l['amount'])*(1 if l['side']=='Dr' else -1)
    check(set(delta)<=set(by),'Journal account missing from complete GL')
    for a,r in by.items():
        exact(r['opening']+ZERO if isinstance(r['opening'],Decimal) else dec(r['opening']),dec(r['closing'])-delta.get(a,ZERO),'GL journal bridge '+a)
        exact(r['closing'],r['statement'],'GL/statement '+a)
    for a,(op,cl) in stocks.items():
        check(a in by,'Source balance missing from GL '+a);exact(by[a]['opening'],op,'Opening '+a);exact(by[a]['closing'],cl,'Closing '+a)
    return delta

def owner_links(c,docs):
    from production import execute
    seen=set();values={}
    allowed={'debt-financing','foreign-currency','consolidation','financial-instruments-ecl','financial-statements','equity-capital','revenue-recognition','fair-value-measurement'}
    for imp in population(c['imports'],'owner imports'):
        check(imp['package'] in allowed,'Unsupported owner or hedge/inventory cycle')
        cc=imp['case'];check(all(cc.get(k)==c[k] for k in ('entity','framework','jurisdiction','period_start','reporting_period')),'Owner context differs')
        rr=execute(imp['package'],cc);check(rr['status']=='complete','Owner result not currently complete')
        check(digest(rr)==digest(imp['result']),'Owner result differs from current executable owner')
    for l in population(c['owner_links'],'owner links'):
        source(c,l,docs);matches=[i for i in c['imports'] if i['id']==l['owner_import']];check(len(matches)==1,'Missing owner')
        imp=matches[0];value=imp['result']['calculations'];path=l['result_path']
        check(isinstance(path,list) and bool(path),'Owner numeric result path required')
        for key in path:
            if isinstance(value,list):value=value[key] if isinstance(key,int) and 0<=key<len(value) else next((r for r in value if r.get('id')==key),None)
            else:value=value.get(key) if isinstance(value,dict) else None
            check(value is not None,'Owner result fact missing')
        check(not isinstance(value,(list,dict,bool)),'Numeric owner assertion required');exact(value,l['amount'],'Actual owner bound fact')
        check(l['id'] not in values,'Duplicate owner fact');values[l['id']]=(imp['package'],dec(value));seen.add(imp['id'])
    seen.update(r['consolidation_import'] for r in c['relationships'] if r.get('type')=='net_investment' and r.get('consolidation_import'))
    check(seen=={i['id'] for i in c['imports']},'Unused owner import could duplicate accounting')
    return values

def net_investment_source(c,r,owners):
    text(r,'foreign_operation_id','net_investment_eligibility_memo','consolidation_import','translation_owner')
    cons=next((i for i in c['imports'] if i['id']==r['consolidation_import']),None)
    check(cons is not None and cons['package']=='consolidation','Actual Consolidation operation owner required')
    operation=r['foreign_operation_id'];check(operation in cons['result']['calculations']['perimeter'],'Foreign operation outside actual group perimeter')
    es=[e for e in cons['case']['entities'] if e['id']==operation and e['parent'] is False]
    check(len(es)==1 and bool(es[0]['translation']),'Qualifying translated foreign subsidiary evidence required')
    e=es[0];links=[l for l in c['owner_links'] if l['id']==r['translation_owner']];check(len(links)==1,'FX translation source link required')
    link=links[0];check(link['result_path']==['translation','cta_movement'],'Net investment requires actual operation CTA path, not arbitrary owner scalar')
    imp=next(i for i in c['imports'] if i['id']==link['owner_import']);check(imp['package']=='foreign-currency','Actual Foreign Currency translation required')
    tr=imp['case']['translation'];check(tr['enabled'] is True and tr['operation_id']==operation,'Foreign operation identity differs across owners')
    check(tr['presentation_currency']==c['currency'] and tr['functional_currency']!=c['currency'],'Actual foreign-operation currencies required')
    fxrows={b['id']:b for b in tr['tb']};check(set(fxrows)==set(e['balances']),'Operation TB populations differ')
    total=ZERO
    mapping=cons['case']['statement_mapping']
    for account,value in e['balances'].items():
        f=fxrows[account];exact(value,f['balance'],'Operation original TB');exact(e['translation']['account_rates'][account],f['rate'],'Operation applied translation rate')
        if mapping[account] in {'assets','liabilities'}:
            check(f['category'] in {'asset','liability'},'Operation account classification contradicts FX owner');total+=cash(dec(value)*dec(f['rate']))
    exact(total,imp['result']['calculations']['translation']['closing_net_translated'],'Actual operation translated net assets')
    ownerships=[n for n in cons['case']['nci'] if n['subsidiary']==operation];check(len(ownerships)==1,'Actual operation ownership required')
    own=dec(ownerships[0]['ownership']);exact(own,tr['ownership'],'Cross-owner ownership')
    check(type(r.get('disposed')) is bool,'Actual disposal decision required')
    if r['disposed']:
        check(imp['case']['disposal']['kind']=='full' and imp['case']['disposal']['qualifying_disposal_reviewed'] is True,'Actual current FX qualifying disposal result required; unsupported disposal cannot release hedge reserve')
        ev=[x for x in cons['case']['ownership_changes'] if x.get('subsidiary')==operation and x.get('control_retained') is False and x.get('date')==c['reporting_period']]
        check(len(ev)==1 and bool(ev[0]['derecognition_journal']),'Actual qualifying same-operation Consolidation disposal required')
    check(dec(r['net_investment'])>0 and dec(r['net_investment'])<=total*own,'Eligible parent net investment exceeds actual owned operation net assets')
    check(abs(dec(r['actual_item_quantity']))<=dec(r['net_investment']),'Designated exposure exceeds eligible net investment')

def assess(c,claims):
    required(c,'package','execution_date','currency','requested_action','documents','contracts','population_review','valuations','relationships','imports','owner_links','gl','disclosure_review','model')
    check(c['package']=='derivatives-hedge-accounting','Wrong specialist package')
    check(c['requested_action']=='accounting_workpaper','Accounting workpaper only; no trading or posting')
    check(iso(c['period_start'])>=iso('2026-01-01') and iso(c['reporting_period'])<=iso('2026-12-31'),'Operative 2026 editions only')
    check(iso(c['execution_date'])>=iso(c['reporting_period']),'Execution predates reporting date')
    check(isinstance(c['currency'],str) and len(c['currency'])==3 and c['currency'].isupper(),'Single supported currency required')
    fw=c['framework'];models={'IFRS':'IFRS9_Chapter6','AASB':'AASB9_Chapter6','US_GAAP':'ASC815_2017_12','UK_GAAP':'FRS102_Section12_2026'}
    check(c['model']==models[fw],'Unsupported hedge model, retained IAS39 or amendment adoption')
    if fw=='UK_GAAP':check(c['policy_elections'].get('financial_instruments')=='sections11_12','FRS102 native Section12 policy required')
    if fw=='US_GAAP':
        check(iso(c['period_start'])<=iso('2026-12-15'),'ASU2025-07 mandatory for annual periods beginning after December15 2026: amended route unsupported')
        check(c['policy_elections'].get('asu_2025_07_early_adopted') is False and c['policy_elections'].get('asu_2025_09_early_adopted') is False,'Resolve effective amended US scope/hedge model; early adoption unsupported')
    docs={}
    for d in population(c['documents'],'documents'):
        text(d,'reviewer','source_system','version');check(d['reviewer']!=c['preparer'],'Independent source qualification required')
        check(d['entity']==c['entity'] and d['framework']==fw and d['currency']==c['currency'] and d['as_of']==c['reporting_period'],'Source context/date/currency differs')
        check(d['content_hash']==digest(d['content']),'Source bytes changed');docs[d['id']]=d
    owners=owner_links(c,docs);consumed_owner_facts=set()
    def bound(r,key,packages,amount):
        id=r.get(key);check(id in owners,'Completed '+key+' owner required');check(id not in consumed_owner_facts,'Owner assertion consumed twice');consumed_owner_facts.add(id);pkg,value=owners[id];check(pkg in packages,'Wrong accounting owner');exact(value,amount,key)
        link=next(l for l in c['owner_links'] if l['id']==id)
        if key=='host_owner':
            check(link['result_path']==['gross_carrying_amount'],'Host carrying assertion must use actual gross carrying amount, not ECL or unrelated scalar')
            imp=next(i for i in c['imports'] if i['id']==link['owner_import']);check(r.get('host_item_id')==imp['case']['case_id'],'Actual financial asset host case identity differs')
            instrument=imp['case']['instrument'];check(instrument['kind'] in {'debt_asset','equity_asset'},'Financial asset host cannot borrow liability/other host classification')
            if instrument.get('id') is not None:check(r.get('host_id')==instrument['id'],'Actual original host instrument identity differs')
        if key=='debt_owner':
            check(link['result_path']==['debt',r['debt_result_index'],'closing'],'Debt owner must bind actual debt closing schedule row')
            imp=next(i for i in c['imports'] if i['id']==link['owner_import']);debt=imp['case']['debt'][r['debt_result_index']]
            check(debt['id']==r['hedged_item_id'],'Wrong underlying debt item')
            expected_rate='fixed' if r['type']=='fair_value' else 'variable';check(debt.get('contractual_rate_type')==expected_rate and r['underlying_rate_type']==expected_rate,'Actual underlying debt fixed/variable contractual rate differs from hedge route')
            text(debt,'contractual_rate_terms_memo')
            if expected_rate=='variable':text(debt,'contractual_benchmark')
            exact(debt['lender_principal'],r['actual_item_quantity'],'Actual debt principal');check(max(m['date'] for m in debt['maturities'])==r['debt_maturity'],'Actual debt maturity')
    check(c['entity_type']=='for_profit','Entity overlay unsupported')
    if fw=='AASB':check(c['reporting_tier']==1,'AASB Tier1 full hedge disclosure scope only')
    contracts=population(c['contracts'],'contract population');check(bool(contracts),'Nonempty actual contract completeness population required')
    pr=c['population_review'];source(c,pr,docs);text(pr,'reviewer','completeness_memo','source_system');check(pr['reviewer']!=c['preparer'],'Independent completeness review')
    check(pr['complete'] is True and pr['contract_ids']==[r['id'] for r in contracts],'Derivative completeness population differs')
    exact(pr['notional_total'],sum((dec(r['notional']) for r in contracts),ZERO),'Complete notional population')
    valuations=population(c['valuations'],'valuations');relationships=population(c['relationships'],'relationships')
    check(len({r['instrument_id'] for r in relationships})==len(relationships),'Instrument allocated twice; partial designations unsupported')
    usedv=set();usedr=set();entries=[];results=[];reserves=[];basis=[];stocks={};qualifications=[]
    for contract in contracts:
        source(c,contract,docs);id=contract['id'];text(contract,'contract_memo','scope_memo','embedded_memo','underlying','maturity')
        check(iso(contract['maturity'])>=iso(c['period_start']),'Expired contract needs settlement evidence scope')
        check(dec(contract['notional'])>0,'Positive evidenced notional required')
        check(contract['kind'] in {'forward','swap','future','purchase_contract','option'},'Unsupported actual contract kind')
        check(contract['underlying_type'] in {'price','rate','index','fx','commodity','credit'},'Actual qualifying underlying behavior required')
        initial=dec(contract['initial_net_investment']);comparable=dec(contract['comparable_investment'])
        check(initial>=0 and comparable>0,'Independent comparable initial-investment evidence required')
        check(contract['small_initial_investment']==(initial<comparable),'Initial investment conclusion contradicts comparable similar market-factor response')
        for key in ('payment_provision','small_initial_investment','future_settlement','net_settlement','exception_applies','exception_assessed','embedded_feature','financial_asset_host','closely_related','separation_required'):
            boolean(contract,key)
        check(contract['exception_assessed'],'Scope exceptions not actually assessed')
        if contract['exception_applies']:
            text(contract,'exception_memo','exception_contract_rights');check(contract['exception_route'] in {'own_use','normal_purchase_normal_sale'},'Own equity/guarantee exception requires separate governed classification')
            check(contract['kind']=='purchase_contract' and contract['physical_delivery_expected'] is True and contract['own_requirements'] is True and contract['past_net_settlement'] is False,'Actual physical delivery/usage and settlement-practice evidence required')
            if fw=='US_GAAP':check(contract['normal_purchase_election_documented'] is True,'US NPNS documented election required')
            if fw=='UK_GAAP':check(contract['atypical_risks'] is False and contract['continuous_own_requirements'] is True,'FRS102 atypical risk/continuous own needs scope assessment required')
            if fw=='US_GAAP':check(contract['exception_route']!='own_use','IFRS own use cannot replace US normal purchase election')
            if fw in {'IFRS','AASB'}:check(contract['exception_route']!='normal_purchase_normal_sale','US exception cannot replace IFRS own use')
            check(not any(r['instrument_id']==id for r in relationships),'Scope-excluded instrument cannot designate hedge')
            results.append(dict(id=id,route='scope_exception',exception=contract['exception_route']));continue
        if contract['embedded_feature']:
            if fw in {'IFRS','AASB'} and contract['financial_asset_host']:
                check(not contract['separation_required'],'IFRS financial asset host uses whole instrument classification');bound(contract,'host_owner',{'financial-instruments-ecl'},contract['host_carrying'])
                results.append(dict(id=id,route='financial_asset_whole_instrument_owner'));continue
            check(not contract['separation_required'] and contract['closely_related'],'Embedded separation valuation/host allocation needs specialized governed assessment')
        derivative=contract['payment_provision'] and contract['small_initial_investment'] and contract['future_settlement'] and (contract['net_settlement'] if fw=='US_GAAP' else True)
        if not derivative:
            check(not any(r['instrument_id']==id for r in relationships),'Nonderivative hedge instruments outside bounded executable route')
            results.append(dict(id=id,route='not_derivative'));continue
        check(initial==0,'Nonzero initial investment/premium requires governed inception recognition and framework comparison; unsupported monetary route')
        vs=[v for v in valuations if v['instrument_id']==id];check(len(vs)==1,'One independently qualified current valuation required');v=vs[0];source(c,v,docs)
        check(v['id'] not in usedv,'Valuation reused');usedv.add(v['id'])
        text(v,'qualified_valuer','valuation_method','market_evidence','credit_adjustment_memo');check(v['qualified_valuer']!=c['preparer'],'Independent qualified valuation required')
        check(v['measurement_date']==c['reporting_period'] and v['opening_date']==c['period_start'],'Stale valuation dates')
        check(v['currency']==c['currency'] and v['entity']==c['entity'],'Valuation scope mismatch');exact(v['notional'],contract['notional'],'Valuation notional')
        opening=dec(v['opening']);change=dec(v['change']);settlement=dec(v['settlement']);closing=dec(v['closing']);exact(opening+change-settlement,closing,'Signed valuation/settlement bridge')
        account='Derivative balance '+id;stocks[account]=(opening,closing)
        rs=[r for r in relationships if r['instrument_id']==id];r=rs[0] if rs else None
        if r and (iso(r['documentation_date'])>iso(r['designation_date']) or (fw!='UK_GAAP' and r['designation_date']!=r['inception_date'])):
            source(c,r,docs);usedr.add(r['id']);qualifications.append(dict(id=r['id'],status='failed_designation',reason='Documentation or designation timing failed; standalone derivative earnings accounting'))
            r=None
        pnl=change;effective=ZERO;item_change=ZERO;release=basis_release=ZERO;route='standalone';openreserve=closereserve=ZERO
        if r:
            source(c,r,docs);usedr.add(r['id']);text(r,'objective','designation_memo','instrument_eligibility_memo','item_eligibility_memo','risk_component_memo','effectiveness_memo','risk_id','hedged_item_id','designation_date','documentation_date','inception_date')
            check(r['advanced_route']=='none' and r['excluded_components']=='none','Advanced options/forward points/basis/portfolio elections unsupported')
            check(contract['kind'] in {'forward','swap','future'},'Option/excluded component advanced route unsupported')
            for key in ('instrument_eligible','item_eligible','risk_eligible','objective_unchanged','economic_relationship','credit_dominates','highly_effective','external_group_exposure'):
                boolean(r,key)
            check(r['instrument_eligible'] and r['item_eligible'] and r['risk_eligible'],'Instrument/item/risk eligibility not established')
            if fw=='UK_GAAP':
                check(r['instrument_external'] is True and r['instrument_fvtpl'] is True and r['written_option'] is False,'Current FRS102 eligible external FVTPL non-written instrument required');text(r,'documented_ineffectiveness_causes')
            check(r['external_group_exposure'],'Intragroup exceptional qualification unsupported')
            check(iso(r['designation_date'])<=iso(c['period_start']),'Midperiod designation needs independently split valuations')
            check(iso(r['documentation_date'])<=iso(r['designation_date']),'Late documentation: ordinary derivative accounting required')
            if fw!='UK_GAAP':check(r['designation_date']==r['inception_date'],'Retrospective/inception designation failure')
            else:check(iso(r['designation_date'])>=iso(r['inception_date']),'FRS conditions date cannot predate economic hedge')
            check(r['assessment_date']==c['reporting_period'],'Stale effectiveness assessment')
            expected={'IFRS':'economic_relationship','AASB':'economic_relationship','US_GAAP':'documented_high_effectiveness','UK_GAAP':'economic_relationship'}[fw]
            check(r['effectiveness_method']==expected,'Framework effectiveness method differs')
            if fw in {'IFRS','AASB'}:check(r['economic_relationship'] and not r['credit_dominates'],'Economic relationship/credit dominance fails')
            elif fw=='UK_GAAP':check(r['economic_relationship'],'Current native FRS102 economic relationship required')
            else:check(r['highly_effective'],'Framework high effectiveness not established')
            check(dec(r['ratio'])>0 and dec(r['actual_instrument_quantity'])>0 and dec(r['actual_item_quantity'])>0,'Actual documented quantities required')
            exact(dec(r['actual_instrument_quantity'])/dec(r['actual_item_quantity']),r['ratio'],'Actual management hedge ratio')
            exact(r['actual_instrument_quantity'],contract['notional'],'Designated whole instrument quantity')
            status=r['status'];check(status in {'active','discontinued','rebalanced'},'Unknown hedge lifecycle')
            if status=='rebalanced':
                check(fw in {'IFRS','AASB'} and r['objective_unchanged'],'Rebalancing only continuing IFRS/AASB objective');text(r,'rebalancing_memo')
                check(r['rebalancing_date']==c['reporting_period'],'Only end-period prospective rebalancing supported');exact(r['historical_effective'],r['opening_effective'],'Historical effectiveness cannot be rewritten')
                check(dec(r['new_ratio'])>0,'Prospective ratio positive');exact(dec(r['new_instrument_quantity'])/dec(r['new_item_quantity']),r['new_ratio'],'Prospective actual quantities')
            if status=='discontinued':
                text(r,'discontinuation_reason');check(r['discontinuation_date']==c['reporting_period'],'Midperiod discontinuation requires split independently measured periods')
                if fw in {'IFRS','AASB'}:check(r['discontinuation_reason']!='voluntary','Qualifying continuing objective cannot voluntarily dedesignate')
            else:check(iso(contract['maturity'])>=iso(c['reporting_period']),'Expired instrument remains in active hedge')
            risk=r['risk_measurement'];source(c,risk,docs);check(risk['instrument_valuation_id']!=v['id'],'Hedged risk cannot copy instrument valuation source');text(risk,'qualified_reviewer','method','market_evidence')
            check(risk['qualified_reviewer']!=c['preparer'] and risk['assessment_date']==c['reporting_period'],'Current independently measured risk required')
            check(risk['item_id']==r['hedged_item_id'] and risk['risk_id']==r['risk_id'],'Wrong measured item/risk');check(risk['currency']==c['currency'],'Risk measurement currency')
            exact(risk['quantity'],r['actual_item_quantity'],'Risk quantity')
            route=r['type'];check(route in {'fair_value','cash_flow','net_investment'},'Unsupported relationship type')
            if r['item_type']=='debt':bound(r,'debt_owner',{'debt-financing'},r['underlying_carrying']);text(r,'debt_terms_memo');exact(r['debt_notional'],r['actual_item_quantity'],'Debt notional');check(r['debt_maturity']==contract['maturity'],'Debt maturity mismatch')
            if r['risk_id']=='FX' and route!='net_investment':
                bound(r,'fx_owner',{'foreign-currency'},r['fx_exposure']);check(r['functional_currency']==c['currency'],'Wrong functional currency')
                link=next(l for l in c['owner_links'] if l['id']==r['fx_owner']);check(link['result_path']==['transactions',r['hedged_item_id'],'closing'],'FX exposure must be actual same hedged transaction, not unrelated owner amount')
                imp=next(i for i in c['imports'] if i['id']==link['owner_import']);items=[i for i in imp['case']['items'] if i['id']==r['hedged_item_id']]
                check(len(items)==1 and imp['case']['currency']['functional']==c['currency'],'Actual FX transaction scope and functional currency required');exact(items[0]['foreign_amount'],r['actual_item_quantity'],'Actual FX foreign exposure quantity')
            if route=='fair_value':
                check(r['item_type'] in {'debt','firm_commitment'},'Bounded FV debt or supported firm commitment only')
                item_change=dec(risk['current_change']);check(change*item_change<=0,'FV risk offset sign');pnl=change+item_change
                entries.append(signed_entry('Hedged item basis adjustment '+r['id'],item_change,'Hedge P&L '+r['id']))
                stocks['Hedged item basis adjustment '+r['id']]=(dec(r['opening_basis']),dec(r['opening_basis'])+item_change)
                check(dec(r['basis_amortization'])==0,'Post-discontinuation EIR basis amortization requires underlying owner recomputation; unsupported here')
            else:
                openreserve=dec(r['opening_reserve']);release=dec(r['earnings_release']);basis_release=dec(r['basis_release']);exact(r['reserve_source_opening'],openreserve,'Opening equity reserve')
                if route=='cash_flow':
                    check(r['item_type'] in {'forecast_purchase','forecast_sale','variable_debt'},'Unsupported CF item type')
                    if r['item_type']=='variable_debt':bound(r,'debt_owner',{'debt-financing'},r['underlying_carrying'])
                    else:
                        text(r,'forecast_memo','forecast_date');check(iso(r['forecast_date'])>=iso(r['designation_date']),'Forecast date before designation');expected_probability='probable' if fw=='US_GAAP' else 'highly_probable'
                        if r['forecast_probability']!=expected_probability:
                            check(r['forecast_probability']=='expected' and status=='discontinued' and r['discontinuation_reason']=='probability_lost' and r['probability_before_cessation']==expected_probability and r['measurement_through_qualification_date']==c['reporting_period'],'Actual threshold loss must have qualified through endperiod; forecast merely expected retains prior reserve')
                        exact(r['forecast_quantity'],r['actual_item_quantity'],'Actual forecast quantity');check(iso(r['forecast_date'])<=iso(r['designated_end']) and iso(r['forecast_date'])>=iso(r['designated_start']),'Forecast outside designated window')
                    if fw=='US_GAAP':effective=change;pnl=ZERO
                    else:
                        current=lower(risk['instrument_cumulative'],risk['risk_cumulative']);prior=lower(risk['opening_instrument_cumulative'],risk['opening_risk_cumulative']);exact(prior,r['opening_effective'],'Opening cumulative effectiveness')
                        exact(dec(risk['instrument_cumulative'])-dec(risk['opening_instrument_cumulative']),change,'Cumulative/current instrument')
                        exact(dec(risk['risk_cumulative'])-dec(risk['opening_risk_cumulative']),risk['current_change'],'Cumulative/current independently measured risk')
                        effective=current-prior;pnl=change-effective
                    outcome=r['forecast_outcome'];check(outcome in {'pending','occurred','no_longer_expected'},'Unknown forecast outcome')
                    if outcome=='no_longer_expected':
                        check(status=='discontinued','Failed forecast must discontinue');exact(release,openreserve+effective,'Failed forecast immediate reserve release');exact(basis_release,0,'Cancelled purchase cannot basis adjust')
                    elif outcome=='pending':exact(release,0,'Pending forecast retain OCI');exact(basis_release,0,'Pending purchase no basis adjustment')
                    else:
                        check(r['transaction_date']==r['forecast_date'] and iso(c['period_start'])<=iso(r['transaction_date'])<=iso(c['reporting_period']),'Actual transaction timing differs')
                        if r['item_type']=='forecast_purchase' and fw in {'IFRS','AASB','UK_GAAP'}:
                            exact(release,0,'Nonfinancial purchase cannot earnings recycle');exact(basis_release,openreserve+effective,'Complete nonfinancial acquisition basis adjustment')
                            text(r,'acquisition_id','sku');check(dec(r['acquired_quantity'])>0,'Acquired quantity required');exact(r['acquired_quantity'],r['forecast_quantity'],'Acquired designated quantity')
                            basis.append(dict(id=r['id']+'-basis',economic_id=r['id']+'-'+r['acquisition_id'],item_id=r['sku'],acquisition_id=r['acquisition_id'],amount=-basis_release,currency=c['currency'],entity=c['entity'],framework=fw,date=r['transaction_date'],quantity=dec(r['acquired_quantity']),relationship_id=r['id'],instrument_id=id))
                        else:
                            exact(basis_release,0,'US CF and forecast sales do not directly basis adjust');text(r,'earnings_period_memo')
                            if r['item_type']=='forecast_sale':
                                bound(r,'revenue_owner',{'revenue-recognition'},r['underlying_period_revenue']);link=next(l for l in c['owner_links'] if l['id']==r['revenue_owner']);check(link['result_path']==['period_revenue'],'Actual current Revenue period required')
                                imp=next(i for i in c['imports'] if i['id']==link['owner_import']);check(imp['case'].get('contract_id')==r['hedged_item_id'] and imp['case'].get('currency')==c['currency'],'Revenue source actual contract/currency differs from designated sale');exact(imp['case']['hedged_contract_quantity'],r['forecast_quantity'],'Actual Revenue contract quantity')
                            check(r['earnings_date']==c['reporting_period'],'Recycle only actual hedged earnings period')
                            exact(release,openreserve+effective,'Whole designated earnings release')
                else:
                    check(r['risk_id']=='FX','Net investment hedge must designate actual FX risk')
                    check(r['item_type']=='net_investment' and r['group_perspective'] is True,'Qualifying actual group net investment required')
                    net_investment_source(c,r,owners);bound(r,'translation_owner',{'foreign-currency'},r['translation_change'])
                    check(abs(dec(risk['risk_cumulative']))<=abs(dec(r['net_investment'])),'Net investment exposure exceeded')
                    effective=lower(change,risk['current_change']);pnl=change-effective;exact(basis_release,0,'NI cannot nonfinancial basis adjust')
                    if fw=='UK_GAAP':exact(release,0,'FRS102 net investment reserve does not recycle on disposal')
                    elif r['disposed'] is True:exact(release,openreserve+effective,'NI qualifying disposal recycle')
                    else:exact(release,0,'NI undisposed reserve retained')
                closereserve=openreserve+effective-release-basis_release
                stocks['Hedge reserve '+r['id']]=(-openreserve,-closereserve)
                if release:entries.append(signed_entry('Hedge reserve '+r['id'],release,'Hedge P&L '+r['id']))
                if basis_release:entries.append(signed_entry('Hedge reserve '+r['id'],basis_release,'Nonfinancial asset basis adjustment'))
                reserves.append(dict(id=r['id'],opening=openreserve,recognized_oci=effective,reclassification=release,basis_adjustment=basis_release,closing=closereserve))
            entries.append(signed_entry(account,change-effective,'Hedge P&L '+r['id']))
            if effective:entries.append(signed_entry(account,effective,'Hedge reserve '+r['id']))
            qualifications.append(dict(id=r['id'],framework_method=r['effectiveness_method'],status=status,ratio=r['ratio'],historical_effective=r['opening_effective']))
        else:entries.append(signed_entry(account,change,'Derivative P&L '+id))
        if settlement:entries.append(signed_entry('Cash',settlement,account))
        results.append(dict(id=id,route=route,opening=opening,change=change,settlement=settlement,closing=closing,effective=effective,ineffectiveness=pnl,hedged_item_change=item_change,earnings_release=release))
    check(consumed_owner_facts==set(owners),'Owner facts must bind an actual used derivative/hedged item; unrelated equity valuation cannot qualify derivative')
    check(usedv=={v['id'] for v in valuations},'Unused/duplicate valuation population')
    check(usedr=={r['id'] for r in relationships},'Unconsumed hedge relationship')
    disclosure=c['disclosure_review'];source(c,disclosure,docs);text(disclosure,'reviewer','framework_checklist','strategy_memo','timing_profile_memo');check(disclosure['framework']==fw and disclosure['complete'] is True,'Actual framework disclosures incomplete')
    check(disclosure['contract_ids']==[r['id'] for r in contracts] and disclosure['relationship_ids']==[r['id'] for r in relationships],'Disclosure completeness differs')
    for row in c['gl']:source(c,row,docs)
    delta=ledger(c,entries,stocks)
    return dict(status='partial',conclusion='Qualified derivative scope, valuation bridges, framework hedge journals and reserves reconcile',method='Bounded actual-relationship accounting; no valuation or dealing',calculations=dict(derivatives=results,hedge_reserves=reserves,basis_adjustments=basis,effectiveness=qualifications,gl_movements=delta),journal_entry_implications=entries,judgments=['Management objective and independently qualified evidence determine eligibility; quantities are not selected by this workflow'],uncertainties=['2026 operative basic full-instrument routes only. Advanced techniques and midperiod measurement splits require a governed specialist method.'],open_items=[],disclosures_impacted=['Framework-specific instrument, risk, reserve and accounting-effect disclosure support'])
