"""Reviewed ordinary acquisition PPA and event accounting, not a valuation engine."""
from decimal import Decimal
from core_accounting import cash, dec, required, ReviewRequired, journal
from production import flag, fraction, nonnegative
from advanced_accounting import gate, event_date, iso, unique, movement, result, ZERO

def assess(c,claims):
    gate(c,'acquisition','assets','liabilities','consideration','nci','costs','events','subsequent')
    a=c['acquisition'];required(a,'date','acquirer','business_definition_memo','control_memo','scope','tax_review','exceptions_review')
    acquired=event_date(c,a['date'])
    if acquired<iso(c['period_start']):raise ReviewRequired('Opening acquisitions need an opening-PPA route, not a repeated current acquisition journal')
    if a['scope']!='ordinary_business' or not flag(a,'business_definition_met') or not flag(a,'control_obtained'):
        raise ReviewRequired('Asset acquisitions, common control, reverse/VIE and unresolved business/control scope require separate method')
    if not flag(a,'exceptions_resolved') or not flag(a,'tax_review_complete'):
        raise ReviewRequired('Resolve recognition exceptions, deferred tax and award/legal effects before PPA')
    fw=c['framework'];uk=fw=='UK_GAAP'
    if fw=='US_GAAP' and c['policy_elections'].get('private_company_alternative',False):
        raise ReviewRequired('Private-company recognition/goodwill alternatives require separate specialist schedule')
    unique(c['assets']);unique(c['liabilities'])
    ids=[r['id'] for r in c['assets']+c['liabilities']]
    if len(ids)!=len(set(ids)):raise ReviewRequired('PPA asset and liability IDs overlap')
    for r in c['assets']+c['liabilities']:
        required(r,'account','amount','recognition_memo','valuation_evidence','measurement_basis')
        if r['measurement_basis'] not in ('fair_value','reviewed_exception'):
            raise ReviewRequired('Unresolved PPA measurement basis')
        if not flag(r,'recognition_approved'):raise ReviewRequired('Unapproved identifiable item')
    assets=sum((cash(nonnegative(r['amount'])) for r in c['assets']),ZERO)
    liabilities=sum((cash(nonnegative(r['amount'])) for r in c['liabilities']),ZERO)
    net=assets-liabilities
    if net<0:raise ReviewRequired('Negative identifiable net assets require specialist PPA/NCI assessment')
    k=c['consideration'];required(k,'cash','equity','other','prior_interest','prior_carrying','memo','contingent')
    contingent=k['contingent'];required(contingent,'class','acquisition_amount','classification_memo','probable_reliable')
    if contingent['class'] not in ('none','liability','equity'):raise ReviewRequired('Consideration classification unresolved')
    contingent_amount=cash(nonnegative(contingent['acquisition_amount']))
    if contingent['class']=='none' and contingent_amount:raise ReviewRequired('None consideration cannot have an amount')
    if uk and contingent_amount and not flag(contingent,'probable_reliable'):
        raise ReviewRequired('UK contingent purchase cost requires probable/reliable estimate; resolve recognition amount')
    prior=cash(nonnegative(k['prior_interest']));prior_book=cash(nonnegative(k['prior_carrying']))
    if prior or prior_book:raise ReviewRequired('Step acquisition requires prior-interest and OCI remeasurement specialist')
    costs=c['costs'];required(costs,'direct','other','issuance','memo')
    direct=cash(nonnegative(costs['direct']));other=cash(nonnegative(costs['other']))
    if nonnegative(costs['issuance']):raise ReviewRequired('Debt/equity issuance costs require financing-specific schedule')
    cash_paid=cash(nonnegative(k['cash']));equity=cash(nonnegative(k['equity']));other_paid=cash(nonnegative(k['other']))
    price=cash_paid+equity+other_paid+contingent_amount+(direct if uk else ZERO)
    n=c['nci'];required(n,'ownership','method','fair_value','memo')
    owned=fraction(n['ownership'])
    if not owned:raise ReviewRequired('Zero ownership/control requires specialist rights analysis')
    if n['method'] not in ('fair_value','proportionate'):raise ReviewRequired('NCI model unresolved')
    if fw=='US_GAAP' and n['method']!='fair_value':raise ReviewRequired('ASC805 NCI is not IFRS proportionate election')
    if uk and n['method']!='proportionate':raise ReviewRequired('FRS102 NCI uses proportionate net assets')
    nci=cash(nonnegative(n['fair_value'])) if n['method']=='fair_value' else cash((1-owned)*net)
    if owned==1 and nci:raise ReviewRequired('Full acquisition cannot recognize NCI')
    residual=price+nci-net;goodwill=max(residual,ZERO);bargain=max(-residual,ZERO)
    if bargain:
        if not flag(a,'bargain_reassessment_complete'):raise ReviewRequired('Reassess PPA and consideration before bargain recognition')
        if uk:raise ReviewRequired('UK negative goodwill recognition/release requires Section19-specific schedule, not immediate IFRS gain')
    entries=[journal(*([('Dr',r['account'],r['amount']) for r in c['assets']]+[('Dr','goodwill',goodwill)]+
        [('Cr',r['account'],r['amount']) for r in c['liabilities']]+[('Cr','cash',cash_paid),('Cr','issued equity',equity),
        ('Cr','other consideration payable',other_paid),('Cr','contingent '+contingent['class'],contingent_amount),
        ('Cr','acquisition costs payable',direct if uk else ZERO),('Cr','noncontrolling interest',nci),('Cr','bargain purchase gain',bargain)]))]
    expense=other+(ZERO if uk else direct)
    entries.append(journal(('Dr','acquisition expense',expense),('Cr','acquisition costs payable',expense)))
    adjustments=[];closing_contingent=contingent_amount;asset_balances={r['account']:cash(nonnegative(r['amount'])) for r in c['assets']}
    for e in c['events']:
        required(e,'kind','date','amount','memo')
        when=event_date(c,e['date']);delta=cash(dec(e['amount']))
        if when<acquired:raise ReviewRequired('Acquisition event precedes acquisition date')
        if e['kind']=='measurement_period_asset':
            required(e,'account','acquisition_date_evidence','provisional_item','catchup_depreciation','remaining_goodwill','tax_nci_effects_zero')
            if not flag(e,'acquisition_date_evidence') or not flag(e,'provisional_item'):
                raise ReviewRequired('Later-event estimate is not a measurement-period correction')
            anniversary=acquired.replace(year=acquired.year+1,day=28 if acquired.month==2 and acquired.day==29 else acquired.day)
            if when>anniversary:raise ReviewRequired('Measurement period exceeds one-year maximum')
            if uk:raise ReviewRequired('UK purchase accounting adjustment needs period-specific Section19 schedule')
            if not flag(e,'tax_nci_effects_zero') or (owned<1 and n['method']=='proportionate'):
                raise ReviewRequired('Measurement adjustment tax/NCI effects require full revised PPA schedule')
            matches=[r for r in c['assets'] if r['account']==e['account']]
            if len(matches)!=1 or asset_balances.get(e['account'],ZERO)+delta<0:
                raise ReviewRequired('Measurement adjustment requires a known asset and nonnegative revised carrying value')
            asset_balances[e['account']]+=delta
            if delta>goodwill:raise ReviewRequired('Adjustment crosses goodwill/bargain boundary; reassessment required')
            goodwill-=delta
            if goodwill<0:raise ReviewRequired('Adjustment produced negative goodwill')
            entries.append(movement(e['account'],'goodwill',delta))
            dep=cash(nonnegative(e['catchup_depreciation']))
            entries.append(journal(('Dr','depreciation catch-up',dep),('Cr','accumulated depreciation',dep)))
            if cash(nonnegative(e['remaining_goodwill']))!=goodwill:raise ReviewRequired('Adjusted goodwill does not tie to reviewed event schedule')
            adjustments.append({'asset_delta':delta,'goodwill':goodwill,'catchup':dep,'presentation':'current_period_catchup' if fw=='US_GAAP' else 'retrospective_acquisition_date'})
        elif e['kind']=='contingent_remeasurement':
            if contingent['class']=='none':raise ReviewRequired('No contingent consideration to remeasure')
            if contingent['class']=='equity':
                if delta:raise ReviewRequired('Equity consideration is not subsequently remeasured')
            elif uk:raise ReviewRequired('UK contingent cost adjustment affects purchase cost; separate goodwill/amortization schedule required')
            else:
                closing_contingent+=delta
                if closing_contingent<0:raise ReviewRequired('Negative contingent liability')
                entries.append(movement('contingent remeasurement expense','contingent liability',delta))
        else:raise ReviewRequired('Unsupported acquisition event')
    s=c['subsequent'];required(s,'goodwill_amortization','goodwill_impairment','memo','impairment_review_complete')
    if not flag(s,'impairment_review_complete'):raise ReviewRequired('Complete subsequent goodwill impairment routing')
    amort=cash(nonnegative(s['goodwill_amortization']));loss=cash(nonnegative(s['goodwill_impairment']))
    if amort and not uk:raise ReviewRequired('Ordinary IFRS/AASB/public US goodwill is not amortized')
    if uk:
        required(s,'useful_life','amortization_fraction','amortization_basis')
        life=nonnegative(s['useful_life'])
        if not life or amort!=cash(goodwill/life*fraction(s['amortization_fraction'])):
            raise ReviewRequired('UK goodwill amortization does not reconcile to reviewed life and elapsed fraction')
    if amort+loss>goodwill:raise ReviewRequired('Goodwill movements exceed carrying value')
    entries.extend([journal(('Dr','goodwill amortization',amort),('Cr','accumulated goodwill amortization',amort)),
      journal(('Dr','goodwill impairment',loss),('Cr','goodwill',loss))])
    return result('Reviewed acquisition PPA and subsequent movements reconcile; specialist valuations and tax bases remain external inputs.',
      {'framework':fw,'nci_method':n['method'],'acquisition_date':a['date'],'cost_model':'UK purchase cost' if uk else 'expense services'},
      {'assets':assets,'liabilities':liabilities,'net_assets':net,'consideration':price,'nci':nci,'initial_goodwill':max(residual,ZERO),
       'bargain_gain':bargain,'acquisition_expense':expense,'measurement_adjustments':adjustments,
       'closing_goodwill':goodwill-amort-loss,'closing_contingent_liability':closing_contingent if contingent['class']=='liability' else ZERO},
      entries,[a['business_definition_memo'],a['control_memo'],a['tax_review'],a['exceptions_review'],k['memo'],n['memo'],costs['memo'],s['memo']],
      ['Acquirer/control date and business definition','Consideration and contingent terms/valuation','Identifiable assets/liabilities and exceptions including tax',
       'Goodwill or bargain gain factors and reassessment','Provisional items and measurement-period changes','NCI basis and subsequent goodwill movements','Acquisition expenses and pro-forma/revenue-profit information when required'],
      ['Tax and valuation conclusions are reviewed specialist inputs, not generated here. Ordinary acquisitions only; common control, asset deals, reverse/VIE acquisitions and private alternatives are separate methods.'])
