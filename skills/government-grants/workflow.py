"""Evidence-bound 2026 single-currency grant accounting; no underlying-owner reposting."""
from financing_accounting import *
from grant_knowledge import retrieval_module
from copy import deepcopy

EDITIONS={'IFRS':'IAS20_2026','AASB':'AASB120_2021_2026','UK_GAAP':'FRS102_SEP2024_2026','US_GAAP':'ASU2025_10_ADOPTED_2026'}
OWNERS={'income':{'employee-benefits-payroll','inventory-cost','intangible-assets','accounts-payable'},'asset':{'fixed-assets','inventory-cost','intangible-assets'}}
ACCOUNTS={'receivable':'Grant receivable','cash':'Grant cash','deferred':'Deferred grant','income':'Grant income','expense':'Grant repayment expense','payable':'Grant repayment payable','advance':'Grant advance','basis':'Grant asset contra-basis','clearing':'Nonmonetary grant clearing'}

def bound(r,c,*memo):
    reviewed(r,c,*memo)
    if r.get('source_entity')!=c['entity'] or r.get('source_framework')!=c['framework'] or r.get('source_period')!=[c['period_start'],c['reporting_period']] or r.get('currency')!=c['functional_currency']:
        raise ReviewRequired('Grant source entity, framework, period or currency mismatch')


def scope(c,claims):
    if c.get('package')!='government-grants' or not claims or any(r['topic_id']!='SUPPLEMENTAL_GOVERNMENT_GRANTS' for r in claims):
        raise ReviewRequired('Qualified Grants owner and knowledge required')
    fw=c['framework'];p=c['accounting_policy'];edition=EDITIONS[fw]
    jurisdictions={'IFRS':{'NL','GB','AU','US'},'AASB':{'AU'},'UK_GAAP':{'GB'},'US_GAAP':{'US'}}
    if c['jurisdiction'] not in jurisdictions[fw]:raise ReviewRequired('Unreviewed grant jurisdiction overlay')
    if p['effective_standard']!=edition or c['applicability_review']['standard_versions']!=[edition]:
        raise ReviewRequired('Grant operative edition mismatch')
    if fw=='AASB' and (c['reporting_tier']!=1 or c['aasb_compilation']!='2021 compilation applicable 2026'):
        raise ReviewRequired('Grant AASB Tier 1 for-profit operative compilation required')
    if fw=='UK_GAAP' and c['uk_standard_edition']!='September2024':raise ReviewRequired('Qualified FRS 102 edition required')
    if fw=='US_GAAP' and c['us_entity_type'] not in ('public','private_business'):
        raise ReviewRequired('US business entity scope required')
    m=retrieval_module()
    if fw=='US_GAAP':
        bound(c.get('us_adoption',{}),c,'transition_memo','unissued_memo')
    try:
        m.retrieve(fw,c['reporting_period'],m.SCOPES[fw],period_start=c['period_start'],
                   grant_model=p['grant_model'],us_adoption=c.get('us_adoption'),execution_date=c['execution_date'],
                   early_presentation_adoption=p['early_presentation_adoption'])
    except ValueError as exc:raise ReviewRequired(str(exc)) from exc
    if c['imports']:raise ReviewRequired('Imported journals require an economic adapter; reviewed original owner evidence is supported')
    required(c,'original_source_snapshot','journal_ownership','ownership_inventory')
    original=c['original_source_snapshot'];reviewed(original,c,'capture_memo')
    projection={key:c[key] for key in ('grants','gl','journal_ownership','functional_currency')}
    if not same_result(original['records'],projection):raise ReviewRequired('Grant source records differ from independently captured originals')
    records=rows(c['journal_ownership']);inventory(c,'ownership_inventory',records)
    seen=set()
    for r in records:
        bound(r,c,'ownership_memo');texts(r,'economic_id','accounting_owner')
        if flag(r,'already_posted'):raise ReviewRequired('Grant journal component already posted; qualified reconciliation route required')
        if r['economic_id'] in seen:raise ReviewRequired('Duplicate economic journal ownership')
        seen.add(r['economic_id'])
    return {r['economic_id']:r['accounting_owner'] for r in records}


def source_costs(g,c):
    costs=rows(g['eligible_costs']);inventory(g,'cost_inventory',costs)
    total=ZERO;current=ZERO;seen=set()
    for r in costs:
        bound(r,c,'cost_memo','classification_memo');texts(r,'economic_id','accounting_owner','grant_id')
        if r['grant_id']!=g['id'] or r['economic_id'] in seen or r['accounting_owner'] not in OWNERS[g['classification']]:
            raise ReviewRequired('Unqualified or duplicate underlying eligible cost owner')
        seen.add(r['economic_id'])
        amount=nonnegative(r['amount']);expense=nonnegative(r['current_expense'])
        if expense>amount:raise ReviewRequired('Current expense exceeds supported cost')
        inperiod(c,r['incurred_date'])
        if c['framework']=='US_GAAP' and iso(r['incurred_date'])>iso(g['recognition_date']):raise ReviewRequired('US grant recognition predates compensated incurred cost')
        agree(r['owner_gl_amount'],amount,'Eligible cost owner GL')
        total+=amount;current+=expense
    return total,current,seen


def assess(c,claims):
    grants=begin(c,'grants')
    if not grants:raise ReviewRequired('Actual nonempty grant agreement population required')
    texts(c,'functional_currency')
    owners=scope(c,claims);population(c,grants,[nonnegative(g['agreement_amount']) for g in grants])
    entries=[];schedules=[];stock_open={k:ZERO for k in ('deferred','receivable','advance','basis','payable','clearing','income','expense')};stock_close=dict(stock_open);used=set();cost_ids=set();payment_ids=set();economic_ids=set();agreement_ids=set()
    for g in grants:
        bound(g,c,'agreement_memo','grantor_memo','conditions_memo','classification_memo','rights_memo')
        texts(g,'agreement_id','economic_id','grantor','grantor_identity_evidence')
        if g['economic_id'] in economic_ids or owners.get(g['economic_id'])!='government-grants':
            raise ReviewRequired('Grant economic identity has duplicate or different journal owner')
        if g['agreement_id'] in agreement_ids:raise ReviewRequired('Duplicate source grant agreement')
        agreement_ids.add(g['agreement_id']);economic_ids.add(g['economic_id']);used.add(g['economic_id'])
        if not flag(g,'government_confirmed'):raise ReviewRequired('Government grantor identity unresolved')
        substance=enum(g,'substance',{'grant','procurement','shareholder','income_tax','loan','assistance','agriculture_fvlcts'})
        if substance!='grant':raise ReviewRequired('Grant scope requires separate '+substance+' accounting owner')
        enum(g,'classification',{'income','asset'});event=enum(g,'event',{'recognition','advance','repayment'})
        transfer=enum(g,'transfer',{'monetary','nonmonetary'})
        presentation=enum(g,'presentation',{'deferred_income','asset_deduction','cost_accumulation'})
        fw=c['framework'];model=c['accounting_policy']['grant_model']
        if g['classification']=='income' and presentation!='deferred_income':raise ReviewRequired('Income grant requires income presentation')
        if fw=='UK_GAAP' and presentation!='deferred_income':raise ReviewRequired('FRS 102 does not permit asset netting')
        if presentation=='asset_deduction' and fw not in ('IFRS','AASB'):raise ReviewRequired('Asset deduction outside qualified framework')
        if presentation=='cost_accumulation' and fw!='US_GAAP':raise ReviewRequired('Cost accumulation requires adopted Topic 832')
        if c['accounting_policy']['presentation_by_class'].get(g['classification'])!=presentation:
            raise ReviewRequired('Explicit consistent grant presentation policy required')
        amount=nonnegative(g['agreement_amount']);opening=nonnegative(g['opening_deferred']);opar=nonnegative(g['opening_receivable']);opadv=nonnegative(g['opening_advance'])
        if amount<=ZERO:raise ReviewRequired('Positive source agreement amount required')
        if opar>amount or opening>amount or opadv>amount:raise ReviewRequired('Opening grant stocks exceed agreement entitlement')
        if presentation!='deferred_income' and opening:raise ReviewRequired('Asset basis presentation cannot retain deferred income')
        history=g['opening_history'];bound(history,c,'history_memo')
        prior=nonnegative(history['recognized_total']);paid=nonnegative(history['cash_total']);earned=nonnegative(history['income_total']);deducted=nonnegative(history['basis_total'])
        if prior>amount or paid>prior or earned+deducted>prior:raise ReviewRequired('Opening cumulative grant entitlement exceeds agreement')
        agree(opar,prior-paid,'Opening cumulative grant receivable')
        agree(opening,prior-earned-deducted,'Opening cumulative grant deferral')
        if nonnegative(history['prior_repayments']) or nonnegative(history['prior_advances']):raise ReviewRequired('Prior repayment/advance history requires qualified continuation route')
        if presentation=='deferred_income' and deducted or presentation!='deferred_income' and earned:raise ReviewRequired('Opening grant history contradicts presentation policy')
        for key,value in [('deferred',opening),('receivable',opar),('advance',opadv),('basis',deducted)]:stock_open[key]+=value
        threshold='probable' if fw=='US_GAAP' else 'reasonable_assurance'
        conclusion=g['recognition_review'];bound(conclusion,c,'receipt_memo','compliance_memo')
        if conclusion.get('threshold')!=threshold:raise ReviewRequired('Framework-specific recognition threshold required')
        conditions=rows(g['conditions']);inventory(g,'condition_inventory',conditions)
        met=True
        for condition in conditions:
            bound(condition,c,'compliance_memo');enum(condition,'kind',{'precedent','ongoing','performance'})
            if not flag(condition,'compliance_evidenced'):raise ReviewRequired('Grant condition lacks independent compliance evidence')
            condition_met=flag(condition,'met')
            if condition.get('as_of')!=c['reporting_period']:raise ReviewRequired('Grant condition evidence is not current at reporting cutoff')
            due=iso(condition['due_date'])
            if event=='recognition' and due<=iso(c['reporting_period']) and not condition_met:raise ReviewRequired('Due grant condition failed; current assurance conclusion contradicts evidence')
            met=met and condition_met
        assured=flag(conclusion,'receipt_supported') and flag(conclusion,'compliance_supported')
        payments=rows(g['payments']);inventory(g,'payment_inventory',payments);received=ZERO
        for pay in payments:
            bound(pay,c,'bank_memo');texts(pay,'bank_id');inperiod(c,pay['date'])
            if pay['bank_id'] in payment_ids or pay['grant_id']!=g['id']:raise ReviewRequired('Duplicate or misallocated grant bank receipt')
            payment_ids.add(pay['bank_id']);received+=nonnegative(pay['amount'])
        if paid+received>amount:raise ReviewRequired('Cumulative grant cash exceeds source agreement amount')
        additions=ZERO;release=ZERO;repay=ZERO;expense=ZERO;advance=ZERO;basis=ZERO
        if event=='advance':
            if transfer!='monetary' or received<=ZERO or opening or opar or opadv or prior:raise ReviewRequired('Advance route requires new actual cash and no opening grant stocks')
            if assured and (model!='FRS102_PERFORMANCE' or met):raise ReviewRequired('Grant eligible for recognition cannot be classified as unrecognized advance')
            advance=received
            entries.append(journal(('Dr',ACCOUNTS['cash'],received),('Cr',ACCOUNTS['advance'],received)))
        elif event=='repayment':
            if received or opadv or transfer!='monetary':raise ReviewRequired('Separate repayment route cannot combine receipts or nonmonetary transfer')
            r=g['repayment'];bound(r,c,'obligation_memo','trigger_memo','estimate_memo');inperiod(c,r['trigger_date'])
            if not flag(r,'obligation_supported') or r['error_vs_estimate']!='new_estimate' or presentation!='deferred_income':
                raise ReviewRequired('Complex basis repayment or prior error requires qualified asset/accounting-change owner')
            repay=nonnegative(r['amount'])
            if repay>amount or opening>amount:raise ReviewRequired('Repayment exceeds original grant or deferral')
            consume=min(opening,repay);expense=repay-consume
            if fw=='UK_GAAP' and not flag(r,'simple_model_conclusion'):raise ReviewRequired('Qualified UK repayment model conclusion required')
            entries.append(journal(('Dr',ACCOUNTS['deferred'],consume),('Dr',ACCOUNTS['expense'],expense),('Cr',ACCOUNTS['payable'],repay)))
        else:
            if not assured:raise ReviewRequired('Independent receipt and compliance recognition conclusions unresolved')
            if model=='FRS102_PERFORMANCE' and not met:raise ReviewRequired('FRS 102 performance conditions unmet; receipt is an advance')
            if not flag(g,'receivable_right_supported'):raise ReviewRequired('Grant reimbursement right unresolved')
            inperiod(c,g['recognition_date'])
            total,current,ids=source_costs(g,c)
            if cost_ids & ids:raise ReviewRequired('Underlying cost claimed twice')
            cost_ids.update(ids)
            additions=nonnegative(g['recognized_addition'])
            if prior+additions>amount or opening+additions>amount or received>opar+additions:raise ReviewRequired('Grant addition/cash exceeds evidenced entitlement')
            if opadv:raise ReviewRequired('Conversion of prior advance requires separately reviewed transfer route')
            if fw=='US_GAAP' and total<additions:raise ReviewRequired('Topic 832 requires compensated costs incurred')
            if g['classification']=='asset':
                a=g['asset'];bound(a,c,'asset_memo','expense_pattern_memo','grant_adjustment_memo')
                texts(a,'asset_id','accounting_owner','available_for_use_date')
                model_asset=enum(a,'expense_model',{'depreciation','amortization','inventory_expense'})
                if a['accounting_owner']=='inventory-cost' and fw!='US_GAAP':raise ReviewRequired('Ordinary IFRS/AASB/UK inventory subsidy is not a long-term asset grant')
                if model_asset=='inventory_expense' and a['accounting_owner']!='inventory-cost':raise ReviewRequired('Inventory expense pattern requires Inventory owner')
                if model_asset!='inventory_expense':
                    if nonnegative(a['useful_life_years'])<=ZERO:raise ReviewRequired('Actual asset owner useful life required')
                    agree(a['total_expense_basis'],nonnegative(a['cost'])-nonnegative(a['residual_value']),'Owner depreciable asset basis')
                if nonnegative(a['current_expense']) and iso(a['available_for_use_date'])>iso(c['reporting_period']):raise ReviewRequired('Asset expense precedes owner available-for-use cutoff')
                if a['accounting_owner'] not in OWNERS['asset'] or a['grant_id']!=g['id']:raise ReviewRequired('Asset owner or grant identity mismatch')
                if flag(a,'disposed') or flag(a,'impaired') or flag(a,'life_changed'):raise ReviewRequired('Changed asset requires owner reassessment')
                if nonnegative(a['cost'])!=total:raise ReviewRequired('Grant eligible costs do not tie asset owner')
                pattern=nonnegative(a['total_expense_basis']);current=nonnegative(a['current_expense'])
                if not flag(a,'basis_adjustment_not_posted') and presentation!='deferred_income':raise ReviewRequired('Asset grant adjustment already owned or posted')
                if presentation!='deferred_income':basis=additions
            else:
                pattern=nonnegative(g['total_eligible_expense_basis'])
                agree(pattern,total,'Income eligible expense basis and original costs')
            if transfer=='nonmonetary':
                if fw=='US_GAAP' and presentation=='cost_accumulation':raise ReviewRequired('US nonmonetary cost-to-entity accounting requires a qualified original asset-owner adapter; no grant basis adjustment is generated')
                if payments or opar or opening or additions!=amount:raise ReviewRequired('Nonmonetary route requires new complete separate transfer')
                v=g['valuation'];bound(v,c,'valuation_memo');texts(v,'asset_id');inperiod(c,v['valuation_date'])
                if v['valuation_date']!=g['recognition_date']:raise ReviewRequired('Nonmonetary grant valuation does not cover actual recognition date')
                if fw=='US_GAAP' and g['asset']['accounting_owner']=='intangible-assets':raise ReviewRequired('US Topic 832 excludes nonmonetary intangible transfers')
                if g['classification']!='asset' or v['asset_id']!=g['asset']['asset_id'] or not flag(v,'qualified'):raise ReviewRequired('Qualified matched nonmonetary asset valuation required')
                valuation=nonnegative(v['fair_value']);measurement=enum(g,'measurement',{'fair_value','nominal','cost_to_entity'})
                if measurement=='nominal' and fw not in ('IFRS','AASB'):raise ReviewRequired('Nominal nonmonetary route unavailable')
                if measurement=='cost_to_entity' and (fw!='US_GAAP' or presentation!='cost_accumulation'):raise ReviewRequired('Cost to entity requires US cost accumulation')
                measured=valuation if measurement=='fair_value' else nonnegative(v[measurement])
                agree(amount,measured,'Nonmonetary grant valuation')
                if c['accounting_policy'].get('nonmonetary_measurement')!=measurement:raise ReviewRequired('Explicit nonmonetary measurement election required')
                if not flag(g['asset'],'owner_clearing_entry_supported'):raise ReviewRequired('Underlying asset owner clearing entry required')
                debit=ACCOUNTS['clearing'];stock_open['clearing']+=amount
            else:debit=ACCOUNTS['receivable']
            if basis:
                entries.append(journal(('Dr',debit,additions),('Cr',ACCOUNTS['basis'],basis)))
            else:
                immediate=model=='FRS102_PERFORMANCE' or flag(g,'past_cost_compensation')
                if immediate:
                    if g['past_cost_compensation'] and not flag(g,'no_future_costs'):raise ReviewRequired('Past-cost compensation has unresolved future costs')
                    release=opening+additions
                else:
                    if pattern<=ZERO or current>pattern:raise ReviewRequired('Supported expense release pattern unavailable')
                    release=cash(amount*current/pattern)
                    if release>opening+additions:raise ReviewRequired('Release exceeds remaining evidenced grant')
                entries.append(journal(('Dr',debit,additions),('Cr',ACCOUNTS['deferred'],additions)))
                entries.append(journal(('Dr',ACCOUNTS['deferred'],release),('Cr',ACCOUNTS['income'],release)))
            if received:entries.append(journal(('Dr',ACCOUNTS['cash'],received),('Cr',ACCOUNTS['receivable'],received)))
        closing=opening+additions-release-min(opening,repay) if not basis else opening
        closing_ar=opar+(additions if transfer=='monetary' else ZERO)-received if event=='recognition' else opar
        expected={'closing_deferred':closing,'closing_receivable':closing_ar,'grant_income':release,'repayment_expense':expense,'basis_adjustment':basis,'closing_advance':opadv+advance}
        for key,value in expected.items():agree(g['expected'][key],value,'Grant schedule '+key)
        for key,value in [('deferred',closing),('receivable',closing_ar),('advance',opadv+advance),('basis',deducted+basis),('payable',repay),('income',release),('expense',expense)]:stock_close[key]+=value
        d=g['disclosure'];bound(d,c,'nature_memo','conditions_contingencies_memo','assistance_memo','policy_memo')
        if d.get('grant_model')!=model or d.get('presentation')!=presentation:raise ReviewRequired('Disclosure model or presentation mismatch')
        for key,value in expected.items():agree(d[key],value,'Grant quantitative disclosure '+key)
        schedule=rows(g['release_schedule']);inventory(g,'schedule_inventory',schedule);future=ZERO;future_expenses=ZERO
        if event=='repayment' and closing:raise ReviewRequired('Repayment retaining future deferral requires a separately revised owner expense pattern')
        for item in schedule:
            bound(item,c,'schedule_memo')
            if iso(item['date'])<=iso(c['reporting_period']):raise ReviewRequired('Closing deferral schedule must be future dated')
            value=nonnegative(item['amount'])
            if event=='recognition' and not basis:
                future_expenses+=nonnegative(item['expense_basis'])
                expected_release=cash(amount*nonnegative(item['expense_basis'])/pattern)
                # Final-row cents allocation is deterministic and cannot alter
                # total supported future expense or closing grant entitlement.
                if item is schedule[-1]:expected_release=closing-future
                agree(value,expected_release,'Future owner expense to grant release')
            future+=value
        agree(future,closing,'Closing deferral and future schedule')
        if schedule and event=='recognition' and not basis:agree(cash(amount*future_expenses/pattern),closing,'Future eligible expense pattern and remaining grant')
        schedules.append(dict(classification=g['classification'],presentation=presentation,opening_deferred=opening,recognized_additions=additions,current_income=release,repayment=repay,repayment_expense=expense,closing_deferred=closing,closing_receivable=closing_ar,closing_advance=advance,basis_adjustment=basis,future_release=[dict(date=x['date'],amount=cash(x['amount'])) for x in schedule]))
    stocks(c,{ACCOUNTS[key]:(stock_open[key] if key in ('receivable','expense') else -stock_open[key],stock_close[key] if key in ('receivable','expense') else -stock_close[key]) for key in stock_open})
    if used!=set(owners):raise ReviewRequired('Journal ownership population contains unallocated grant identities')
    return complete(c,'Framework-specific governed grant recognition and matching',{'grants':schedules},entries,['Grant qualification, receipt/compliance threshold and class policy are supplied independent judgments; costs and valuation remain with their owners'])
