"""Owned 2026 property adapter; valuation and other owners remain evidence providers."""
from financing_accounting import *

EDITIONS={'IFRS':'IAS40_2026','AASB':'AASB140_DEC2022','UK_GAAP':'FRS102_SEP2024_2026','US_GAAP':'ASC360_2026'}
OWNERS={'depreciation':'Fixed Assets','impairment':'Asset Impairment','borrowing':'Borrowing Costs','leases':'Lease Accounting','tax':'Income Taxes','financing':'Debt Financing','consolidation':'Consolidation'}

def exact_amount(value):
    if not isinstance(value,str):raise ReviewRequired('Source amount must be an exact decimal string')
    n=dec(value)
    if n!=cash(n):raise ReviewRequired('Source amount requires exact cents')
    return n

def bound(r,c,p,*memos):
    reviewed(r,c,*memos)
    if (r.get('asset_id'),r.get('legal_entity'),r.get('framework'),r.get('currency'),r.get('period'))!=(p['asset_id'],c['entity'],c['framework'],c['functional_currency'],[c['period_start'],c['reporting_period']]):
        raise ReviewRequired('Property evidence asset/entity/framework/currency/period mismatch')
    texts(r,'document_id')

def valuation(c,p,day):
    v=c['valuation'];bound(v,c,p,'methodology_memo','rights_memo','market_participant_memo','uncertainty_memo')
    texts(v,'valuer','qualified_reviewer','report_hash','valuation_standard','valuation_method')
    if v['valuer']==v['qualified_reviewer'] or len(v['report_hash'])!=64 or any(x not in '0123456789abcdef' for x in v['report_hash']):raise ReviewRequired('Independent qualified valuation report identity required')
    if v['valuation_date']!=day or v['basis']!='market_participant_exit_price' or v['valuation_standard']!=('FRS102_SECTION2A' if c['framework']=='UK_GAAP' else 'AASB13' if c['framework']=='AASB' else 'IFRS13'):
        raise ReviewRequired('Incorrect valuation date or framework-specific basis')
    if v['valuation_method'] not in {'income','market','cost'} or not flag(v,'reliable') or flag(v,'material_unresolved_uncertainty') or flag(v,'transaction_costs_deducted'):
        raise ReviewRequired('Unsupported or unresolved property valuation')
    if v['recognized_by_other_owner'] is not False:raise ReviewRequired('Fair-value movement already owned elsewhere')
    return nonnegative(exact_amount(v['amount']))

def assert_snapshot(c):
    s=c['original_source_snapshot'];reviewed(s,c,'capture_memo');required(s,'records')
    keys=['properties','accounting_policy','valuation','cost_owner','impairment_owner','events','gl','ownership_register','disclosure_review','functional_currency']
    if not same_result(s['records'],{k:c[k] for k in keys}):raise ReviewRequired('Independently captured original source population contradicts current records')

def assess(c,claims):
    if not claims or any(x['topic_id']!='SUPPLEMENTAL_INVESTMENT_PROPERTY' for x in claims):raise ReviewRequired('Substantive Investment Property authority absent')
    rs=begin(c,'properties')
    required(c,'original_source_snapshot','events','ownership_register','functional_currency','skill_version')
    if any(k not in c for k in ['valuation','cost_owner','impairment_owner']):raise ReviewRequired('Explicit valuation and owner applicability population required')
    if c['package']!='investment-property' or c['skill_version']!='1.0.0':raise ReviewRequired('Unsupported Investment Property case/version')
    if [c['period_start'],c['reporting_period']]!=['2026-01-01','2026-12-31']:raise ReviewRequired('Only independently reviewed calendar annual 2026 is supported')
    if c['applicability_review']['standard_versions']!=[EDITIONS[c['framework']]] or c['accounting_policy']['effective_standard']!=EDITIONS[c['framework']]:raise ReviewRequired('Incorrect operative Investment Property edition')
    if c['framework'] in {'AASB','UK_GAAP','US_GAAP'} and c['jurisdiction'] not in {'AASB':{'AU'},'UK_GAAP':{'GB','IE'},'US_GAAP':{'US'}}[c['framework']]:
        raise ReviewRequired('Unsupported framework jurisdiction or unresolved local overlay')
    if c['framework']=='AASB' and c['reporting_tier']!=1:raise ReviewRequired('Tier2 and noncommercial Australian overlays unsupported')
    if c['framework']=='AASB' and c['aasb_compilation']!='AASB140_DEC2022':raise ReviewRequired('Incorrect Australian operative compilation')
    if c['framework']=='UK_GAAP' and c['uk_standard_edition']!='September2024':raise ReviewRequired('Incorrect full FRS102 operative edition')
    if c['framework']=='US_GAAP' and c.get('us_property_scope')!='ordinary_held_and_used':raise ReviewRequired('US investment-company and industry models unsupported')
    if flag(c['accounting_policy'],'early_adoption') or flag(c['accounting_policy'],'policy_change'):raise ReviewRequired('Early adoption or policy changes require existing owner')
    if c['imports']:raise ReviewRequired('Native owner imports require an independently bound adapter; no imported journals authorized here')
    if len(rs)!=1:raise ReviewRequired('One exact legal property interest per case required')
    p=rs[0];texts(p,'asset_id','legal_owner','title_document','rights_memo','classification_memo','source_currency')
    if p['legal_owner']!=c['entity'] or p['source_currency']!=c['functional_currency'] or not flag(p,'owned') or not flag(p,'recognition_criteria_met'):raise ReviewRequired('Owned property recognition rights or currency unresolved')
    for key in ['right_of_use','finance_lessor','business_combination','construction','inventory','held_for_sale','sale_leaseback','complex_consideration','foreign_operation']:
        if flag(p,key):raise ReviewRequired('Unsupported property feature requires original accounting owner: '+key)
    enum(p,'purpose',{'rental','capital_appreciation','both'})
    if flag(p,'significant_services'):raise ReviewRequired('Significant services require owner-occupied classification')
    mixed=enum(p,'mixed_use',{'none','separable','inseparable'})
    if mixed=='separable':
        bound(p['segregation'],c,p,'segregation_memo');g=p['segregation']
        if not flag(g,'separately_saleable') and not flag(g,'separately_finance_leasable'):raise ReviewRequired('Mixed-use separation requires actual disposal or finance-lease ability')
        parts=rows(g['parts'],False);inventory(g,'part_inventory',parts)
        for r in parts:approval(r,c);enum(r,'use',{'rental','owner'});texts(r,'component_id')
        if len({r['component_id'] for r in parts})!=len(parts) or sum(r['component_id']==p['asset_id'] and r['use']=='rental' for r in parts)!=1:raise ReviewRequired('Segregated property component is missing or duplicated')
        agree(g['whole_cost'],sum((nonnegative(exact_amount(r['cost'])) for r in parts),ZERO),'Whole-property segregation')
        selected=next(r for r in parts if r['component_id']==p['asset_id'])
        agree(selected['cost'],p['gross_cost'],'Segregated rental cost')
    if mixed=='inseparable':
        if c['framework'] not in {'IFRS','AASB'} or not flag(p,'owner_use_insignificant'):raise ReviewRequired('Unsupported inseparable mixed-use property')
        texts(p,'insignificance_memo')
    model=enum(c['accounting_policy'],'measurement_model',{'cost','fair_value','group_cost'})
    if c['framework']=='US_GAAP' and model!='cost':raise ReviewRequired('No ordinary US property recurring fair-value election')
    if model=='group_cost':
        if c['framework']!='UK_GAAP' or not flag(p,'group_rental') or not flag(p,'separate_statements') or p['group_lessee']==c['entity']:raise ReviewRequired('FRS102 group-rental cost election requires separate lessor scope')
        texts(p,'group_relationship_memo','group_lessee');flag(c['accounting_policy'],'class_consistent')
    elif c['framework']=='UK_GAAP' and model!='fair_value':raise ReviewRequired('FRS102 2026 ordinary Investment Property requires fair value; deleted cost exception unsupported')
    elif model=='group_cost':raise ReviewRequired('Group cost route is specific to FRS102')
    if not flag(c['accounting_policy'],'class_consistent'):raise ReviewRequired('Property-class policy inconsistent')
    if flag(p,'group_rental') and model!='group_cost':raise ReviewRequired('Group-use accounting requires consolidation perimeter owner; ordinary external rental scope only')
    os=rows(c['ownership_register'],False);inventory(c,'ownership_inventory',os)
    for r in os:bound(r,c,p,'ownership_memo');texts(r,'economic_id','accounting_owner');enum(r,'movement',{'initial','fair_value','transfer','disposal','depreciation','impairment'})
    if len({(r['economic_id'],r['movement']) for r in os})!=len(os):raise ReviewRequired('Duplicate journal economic ownership')
    events=rows(c['events'],False);inventory(c,'event_inventory',events)
    if len(events)!=1:raise ReviewRequired('One bounded annual event route required; compound activity requires separate qualified cases')
    e=events[0];bound(e,c,p,'event_memo');route=enum(e,'kind',{'initial','hold','transfer_in_cost','transfer_out_cost','transfer_out_fv','disposal'})
    applied=set(c['knowledge_review']['applied_claim_ids'])
    decisions={x['decision'] for x in claims if x['claim_id'] in applied}
    required_decisions={'definition','owner_use','subsequent_policy','owner_boundaries','lineage','disclosures'}
    required_decisions|={'fair_value','fv_movement','fv_disclosure'} if model=='fair_value' else {'cost_model','cost_disclosure'}
    if route=='initial':required_decisions|={'initial_recognition','initial_cost'}
    if route=='disposal':required_decisions|={'disposal'}
    if route.startswith('transfer'):required_decisions|={'change_use','fv_transfer_out' if route=='transfer_out_fv' else 'cost_transfer'}
    if mixed!='none':required_decisions|={'mixed_use'}
    if not required_decisions<=decisions:raise ReviewRequired('Applied claim selection omits substantive route authority')
    inperiod(c,e['date']);day=e['date'];texts(e,'economic_id')
    if day!=c['reporting_period']:raise ReviewRequired('First release supports reporting-cutoff events only; intra-year ownership and post-event measurement require further qualification')
    acquired=iso(p['acquisition_date'])
    if acquired>iso(day) or (route!='initial' and acquired>=iso(c['period_start'])):
        raise ReviewRequired('Unsupported acquisition chronology or missing annual opening asset')
    if route=='initial' and p['acquisition_date']!=day:raise ReviewRequired('Initial recognition date differs from acquired rights')
    opening_history=p['opening_history'];bound(opening_history,c,p,'opening_memo')
    if opening_history['previous_reporting_date']!='2025-12-31' or opening_history['measurement_model']!=model:
        raise ReviewRequired('Opening accounting model or prior-period evidence mismatch')
    opening=nonnegative(exact_amount(p['opening_carrying']));gross=nonnegative(exact_amount(p['gross_cost']));accdep=nonnegative(exact_amount(p['opening_accumulated_depreciation']));accimp=nonnegative(exact_amount(p['opening_accumulated_impairment']))
    if model!='fair_value' and route!='initial':agree(gross-accdep-accimp,opening,'Historical gross/accumulated opening bridge')
    elif accdep or accimp:raise ReviewRequired('Fair-value model cannot simultaneously carry cost-model accumulated deductions')
    if route=='initial' and opening:raise ReviewRequired('Initial recognition requires zero opening asset')
    agree(opening_history['carrying'],opening,'Original prior-period carrying basis')
    if model!='fair_value' and accimp:raise ReviewRequired('Prior impairment changes prospective depreciation basis; qualified Fixed Assets method required')
    if route.startswith('transfer'):
        if c['framework']=='US_GAAP':raise ReviewRequired('US use changes remain with the PPE owner; no distinct investment-property transfer method is governed')
        if not flag(e,'actual_change_of_use') or e['change_use_date']!=day:raise ReviewRequired('Actual change-of-use evidence required')
        texts(e,'actual_use_evidence','previous_use','new_use','ppe_owner_document')
        expected=('owner','rental') if route=='transfer_in_cost' else ('rental','owner')
        if (e['previous_use'],e['new_use'])!=expected:raise ReviewRequired('Transfer direction contradicts actual use')
        if c['framework']=='UK_GAAP':raise ReviewRequired('FRS102 group election and revaluation transfers require separately governed PPE owner route')
        if route.endswith('cost') and model!='cost' or route=='transfer_out_fv' and (model!='fair_value' or c['framework']=='US_GAAP'):raise ReviewRequired('Unsupported model/transfer route')
    assert_snapshot(c)
    entries=[];cost=ZERO;dep=ZERO;imp=ZERO;gain=ZERO;disposal_gain=ZERO;proceeds=ZERO;disposed=ZERO;transferred=ZERO
    account='Property plant and equipment' if c['framework']=='US_GAAP' or model=='group_cost' else 'Investment property'
    before=opening
    if route=='initial':
        enum(e,'acquisition_nature',{'cash_purchase'})
        if flag(p,'gifted'):raise ReviewRequired('Gifted or nonexchange property requires separately governed original-owner accounting, not the cash-purchase adapter')
        items=rows(e['cost_items'],False);inventory(e,'cost_inventory',items)
        purchase_price=ZERO
        if len({r['economic_id'] for r in items})!=len(items):raise ReviewRequired('Duplicate acquisition cost economics')
        for r in items:
            bound(r,c,p,'eligibility_memo');kind=enum(r,'kind',{'purchase_price','direct_transaction'});texts(r,'economic_id');inperiod(c,r['date'])
            if r['date']>day or r['accounting_owner']!='Investment Property':raise ReviewRequired('Cost cutoff or duplicate acquisition ownership')
            amount=nonnegative(exact_amount(r['amount']));cost+=amount
            if kind=='purchase_price':purchase_price+=amount
        if purchase_price<=ZERO:raise ReviewRequired('Actual positive cash property-price consideration required; fee-only, zero-price and nonexchange acquisitions are unsupported')
        agree(e['purchase_cost'],cost,'Acquisition-source amount');agree(gross,cost,'Recognized gross cost')
        if not flag(e,'paid') or e['cash_date']!=day:raise ReviewRequired('Cash asset acquisition only; AP/financing liability belongs to original owner')
        before=cost;entries.append(journal(('Dr',account,cost),('Cr','Cash',cost)))
    if model in {'cost','group_cost'}:
        if c['valuation'] is not None and flag(c['valuation'],'recognized_by_other_owner'):raise ReviewRequired('Cost model cannot recognize external fair-value movements')
        if route=='initial':
            if c['cost_owner'] is not None or c['impairment_owner'] is not None:raise ReviewRequired('Initial adapter excludes post-event owner measurement; use subsequent holding case')
        else:
            o=c['cost_owner'];bound(o,c,p,'basis_memo','estimate_memo','owner_memo');
            if o['accounting_owner']!='Fixed Assets' or not flag(o,'already_recognized'):raise ReviewRequired('Depreciation must remain with Fixed Assets owner')
            land=nonnegative(exact_amount(o['land_cost']));residual=nonnegative(exact_amount(o['building_residual']));building=gross-land;life=positive(o['building_life_years'])
            if land>gross or residual>building or life>Decimal('1000') or o['method']!='straight_line' or flag(o,'estimate_change'):raise ReviewRequired('Unsupported supplied depreciation estimate/model')
            service=iso(o['available_for_use']);charge_start=max(service,iso(c['period_start']));charge_end=iso(day)
            if service>charge_end:raise ReviewRequired('Asset not yet available for use in holding route')
            dep=cash(min(max(ZERO,opening-land-residual),((building-residual)/life)*year_fraction(charge_start,charge_end)))
            agree(o['depreciation'],dep,'Independent depreciation owner reperformance');agree(o['opening_carrying'],opening,'Depreciation owner opening');agree(o['closing_before_impairment'],opening-dep,'Depreciation owner carrying bridge')
            if o['charge_end']!=day or o['charge_start']!=charge_start.isoformat():raise ReviewRequired('Cost-owner charge dates mismatch')
            before-=dep
            h=c['impairment_owner'];bound(h,c,p,'screening_memo','owner_memo')
            if h['accounting_owner']!='Asset Impairment' or not flag(h,'already_recognized') or flag(h,'reversal'):raise ReviewRequired('Impairment recognition/reversal remains with impairment owner')
            imp=nonnegative(exact_amount(h['loss']));
            if imp>before or (not flag(h,'indicators_present') and imp):raise ReviewRequired('Unsupported impairment owner conclusion')
            agree(h['opening_carrying'],before,'Impairment owner preloss');agree(h['closing_carrying'],before-imp,'Impairment owner result');before-=imp
    elif c['cost_owner'] is not None or c['impairment_owner'] is not None:raise ReviewRequired('Fair-value model cannot duplicate depreciation or impairment effects')
    if model=='fair_value':
        value=valuation(c,p,day);gain=value-before
        if gain:entries.append(signed_entry(account,'Property fair value profit or loss',gain))
        before=value
    if route=='transfer_in_cost':
        agree(e['ppe_carrying'],before,'PPE transfer carrying basis');entries.append(journal(('Dr',account,before),('Cr','Property plant and equipment',before)));transferred=before
    if route in {'transfer_out_cost','transfer_out_fv'}:
        agree(e['ppe_carrying'],before,'PPE deemed/historical cost');entries.append(journal(('Dr','Property plant and equipment',before),('Cr',account,before)));transferred=-before
    if route=='disposal':
        if not flag(e,'sale_recognition_met') or not flag(e,'paid') or e['cash_date']!=day or flag(e,'continuing_involvement'):raise ReviewRequired('Unsupported disposal recognition or continuing involvement')
        texts(e,'sale_contract','derecognition_memo','sale_criteria_owner_memo')
        gross_proceeds=nonnegative(exact_amount(e['gross_proceeds']));selling_costs=nonnegative(exact_amount(e['selling_costs']));proceeds=gross_proceeds-selling_costs
        if proceeds<0:raise ReviewRequired('Disposal proceeds cannot be negative in supported cash route')
        agree(e['net_cash_received'],proceeds,'Disposal net proceeds');agree(e['derecognized_carrying'],before,'Disposal carrying basis');disposed=before;disposal_gain=proceeds-before
        lines=[('Dr','Cash',proceeds),('Cr',account,before)]
        if disposal_gain:lines.append(('Cr' if disposal_gain>0 else 'Dr','Property disposal profit or loss',abs(disposal_gain)))
        entries.append(journal(*lines))
    closing=ZERO if route in {'disposal','transfer_out_cost','transfer_out_fv'} else before
    agree(p['closing_carrying'],closing,'Property closing rollforward')
    # A closing cost-model property still needs a qualified reporting-date FV note.
    # Initial recognition and transfers into the class are not exemptions.
    disclosure_fv=valuation(c,p,day) if model=='cost' and c['framework'] in {'IFRS','AASB'} and closing else ZERO
    # Owners' charges are already in the pre-adapter GL. This adapter never posts them.
    ledger_opening=ZERO if route in {'initial','transfer_in_cost'} else opening-dep-imp
    if route=='transfer_in_cost' and account=='Property plant and equipment':raise ReviewRequired('US use change has no distinct IP account; use PPE presentation owner')
    stocks(c,{account:(ledger_opening,closing)})
    required_moves=[]
    if route in {'initial','disposal'}:required_moves.append((e['economic_id'],route,'Investment Property'))
    if route.startswith('transfer'):required_moves.append((e['economic_id'],'transfer','Investment Property'))
    if model=='fair_value':required_moves.append((e['economic_id'],'fair_value','Investment Property'))
    if c['cost_owner'] is not None:required_moves.append((c['cost_owner']['economic_id'],'depreciation','Fixed Assets'))
    if c['impairment_owner'] is not None:required_moves.append((c['impairment_owner']['economic_id'],'impairment','Asset Impairment'))
    if sorted((r['economic_id'],r['movement'],r['accounting_owner']) for r in os)!=sorted(required_moves):raise ReviewRequired('Exact-once owner population does not match actual movements')
    dr=c['disclosure_review'];bound(dr,c,p,'period_entity_memo');required(dr,'requirements','amounts','presentation','rental_owner_document','statement_owner_document')
    texts(dr,'rental_owner_document','statement_owner_document','restrictions_memo','commitments_memo')
    for key in ['rental_income','direct_expenses_generating_income','direct_expenses_not_generating_income','commitments_amount']:
        nonnegative(exact_amount(dr[key]))
    required_disclosures={'policy','classification','restrictions','commitments','rollforward','rental_income','direct_expenses'}
    required_disclosures|={'valuation_method','valuer','fair_value'} if model=='fair_value' else {'depreciation_method','useful_lives','gross_accumulated'}
    if model=='cost' and c['framework'] in {'IFRS','AASB'}:required_disclosures|={'fair_value'}
    if model=='group_cost':required_disclosures|={'group_rental_carrying'}
    if not required_disclosures<=set(dr['requirements']):raise ReviewRequired('Framework/model-specific disclosure population incomplete')
    if dr['presentation']!=account:raise ReviewRequired('Framework-specific financial statement presentation mismatch')
    class_opening=ZERO if route=='transfer_in_cost' else opening
    class_dep=ZERO if route=='transfer_in_cost' else dep
    class_imp=ZERO if route=='transfer_in_cost' else imp
    agree(class_opening+cost-class_dep-class_imp+gain+transferred-disposed,closing,'Complete property-class rollforward')
    calc={'measurement_model':model,'opening_carrying':class_opening,'additions':cost,'depreciation_owned_elsewhere':class_dep,'impairment_owned_elsewhere':class_imp,'fair_value_movement':gain,'transfers':transferred,'disposal_carrying':disposed,'net_proceeds':proceeds,'disposal_gain':disposal_gain,'closing_carrying':closing}
    if route=='transfer_in_cost':
        calc.update(pre_transfer_depreciation_owned_elsewhere=dep,pre_transfer_impairment_owned_elsewhere=imp)
    if model=='cost' and c['framework'] in {'IFRS','AASB'}:
        calc['fair_value_disclosure']=disclosure_fv
    for k,n in calc.items():
        if k!='measurement_model':agree(dr['amounts'][k],n,'Disclosure movement '+k)
    population(c,rs,[gross])
    return complete(c,'Owned property accounting reconciled within its qualified framework and measurement model',calc,entries,[
        'Depreciation and impairment effects remain with their original owners and are not posted again',
        'Qualified valuation evidence supports the selected accounting route; it does not authorize an unsupported framework method',
        'Initial recognition, movement, transfer and cash disposal journals require exact-once independent ownership and posting review'])
