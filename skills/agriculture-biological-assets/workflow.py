"""Bounded agricultural accounting; quantities and valuations are supplied evidence."""
from final_batch_accounting import *
import re

KEYS=('assets','asset_source','movements','movement_source','opening_population',
      'closing_population','documents','gl','classification','disclosures','imports',
      'currency','requested_action','accounting_policy','applicability_review')
BOUNDARY_LIMITS=[
    'Qualified current valuation and control evidence are required; this workpaper does not value a farm or establish legal rights.',
    'Harvest transfers establish the entry amount only. Post-harvest Inventory & Cost Accounting is unavailable.',
    'Government assistance, foreign currency, cost-model exceptions and sales recognition require separate accounting owners.',
]

def bounded_scope(c):
    if c['package']!='agriculture-biological-assets':raise ReviewRequired('Wrong Agriculture package')
    if iso(c['period_start'])<iso('2026-01-01') or iso(c['reporting_period'])>iso('2026-12-31'):
        raise ReviewRequired('Agriculture operative-period scope is 2026; other editions require specialist review')
    enum(c,'requested_action',{'classification','accounting'})
    texts(c,'currency')
    if not re.fullmatch(r'[A-Z]{3}',c['currency']):raise ReviewRequired('Currency must be an ISO-style three-letter unit')
    p=c['classification'];source(c,p)
    texts(p,'checked_on','scope_memo','legal_control_memo','biological_transformation_memo','source_system','subledger','entity','jurisdiction')
    if p['checked_on']!=c['execution_date'] or p['entity']!=c['entity'] or p['jurisdiction']!=c['jurisdiction']:
        raise ReviewRequired('Current actual-entity Agriculture scope review required')
    if p['framework']!=c['framework'] or p['effective_period']!=[c['period_start'],c['reporting_period']]:
        raise ReviewRequired('Agriculture classification framework/period mismatch')
    if p['reporting_basis']!={'IFRS':'full_IFRS','AASB':'Tier1_for_profit','UK_GAAP':'full_FRS102','US_GAAP':'ASC905_producer'}[c['framework']]:
        raise ReviewRequired('Unsupported Agriculture reporting basis/entity overlay')
    edition={'IFRS':'IAS41_2026_no_IFRS18','AASB':'AASB141_compilation2022_2026','UK_GAAP':'FRS102_September2024_2026','US_GAAP':'ASC905_2026'}[c['framework']]
    if p['operative_edition']!=edition or edition not in c['applicability_review']['standard_versions']:
        raise ReviewRequired('Agriculture operative standard edition review contradicts governed scope')
    if c['framework']=='UK_GAAP' and c['uk_standard_edition']!='September2024':raise ReviewRequired('Unsupported FRS 102 edition')
    if c['framework']=='AASB' and c['aasb_compilation']!=edition:raise ReviewRequired('Unsupported AASB 141 compilation')
    if flag(p,'early_presentation_adoption'):raise ReviewRequired('Early presentation-standard adoption is outside Agriculture scope')
    for k in ('government_assistance','fx','valuation_requested','post_harvest_accounting','external_posting','unsupported_contract_rights'):
        if flag(p,k):raise ReviewRequired('Unsupported Agriculture dependency: '+k)
    if c['framework']=='AASB' and c['reporting_tier']!=1:
        raise ReviewRequired('AASB Tier 2 and NFP overlays require separately scoped disclosure support')
    return p

def original_population(c,key,rs):
    p=c[key];source(c,p);texts(p,'population_memo','extract_version','source_doc')
    inventory(p,'inventory',rows(p['records']))
    if digest(rs)!=digest(p['records']):raise ReviewRequired('Agriculture tracker contradicts original source population')
    return p

def qualified_value(c,d,id,asset,qty,when):
    v=snapshot(c,d,id,c['currency']);texts(v,'qualified_valuer','qualification_memo','independence_memo','report_version','market_evidence','selling_costs_memo','measurement_basis')
    if v['measurement_basis']!='fair_value_less_costs_to_sell':raise ReviewRequired('Agriculture measurement basis must be FV less costs to sell')
    if any(v[k]!=expected for k,expected in [('entity',c['entity']),('framework',c['framework']),('asset_id',asset['id']),('category',asset['category']),('quantity_unit',asset['quantity_unit']),('currency',c['currency']),('measurement_date',when)]):
        raise ReviewRequired('Valuation owner dimensions, identity or measurement date contradict Agriculture')
    if not iso(when)<=iso(v['signed_on'])<=iso(c['execution_date']):raise ReviewRequired('Invalid qualified valuation sign date')
    if not flag(v,'control_supported') or not flag(v,'reliable_measurement') or not flag(v,'current_market_evidence'):
        raise ReviewRequired('Qualified control/current valuation evidence unresolved')
    exact(v['quantity'],qty,'Valuation source quantity')
    gross=nonnegative(v['fair_value']);costs=nonnegative(v['costs_to_sell'])
    for key in ('finance_or_income_tax_included','transport_deducted_again','other_uncertain_costs'):
        if flag(v,key):raise ReviewRequired('Excluded or uncertain valuation cost component')
    components=rows(v['cost_components']);component_total=ZERO
    for component in components:
        enum(component,'kind',{'commission','levy','transfer_tax','exchange_fee','other_incremental'})
        texts(component,'evidence_memo')
        if not flag(component,'incremental_disposal'):raise ReviewRequired('Selling cost is not evidenced incremental disposal cost')
        component_total+=nonnegative(component['amount'])
    exact(costs,component_total,'Qualified costs-to-sell component population')
    # Fair value already incorporates relevant location/condition adjustments;
    # no autonomous price, hierarchy, transport or valuation-model calculation.
    value=gross-costs
    if value<0:raise ReviewRequired('Selling costs exceed value; specialist route required')
    if value!=cash(value):raise ReviewRequired('Monetary valuation must use controlled currency precision')
    exact(v['net_value'],value,'Qualified valuation net amount')
    if 'owner_import' in v:
        imp=actual_owner(c,v['owner_import'])
        if imp['package']!='fair-value-measurement':raise ReviewRequired('Wrong valuation owner')
        # Existing owner has a bounded equity-only adapter. It cannot be
        # relabelled biological authority even when the scalar happens to match.
        raise ReviewRequired('Existing Fair Value owner lacks biological-asset integration; qualified agriculture valuation report required')
    return value

def assess(c,claims):
    rs=begin(c,'assets');p=bounded_scope(c);d=evidence(c)
    ed=snapshot(c,d,p['edition_doc'],c['currency']);texts(ed,'edition_memo')
    for key in ('operative_edition','entity','framework','effective_period','checked_on','reporting_basis','early_presentation_adoption'):
        if ed[key]!=p[key]:raise ReviewRequired('Independent operative-edition source contradicts Agriculture review')
    if c['imports']:
        imports(c,{'fixed-assets','fair-value-measurement','foreign-currency','financial-statements','disclosure-management'})
        raise ReviewRequired('Owner results require a supported exact Agriculture assertion binding; qualified source reports remain the executable route')
    review_release(c,KEYS)
    src=original_population(c,'asset_source',rs)
    if snapshot(c,d,src['source_doc'],c['currency'])!=src['records']:raise ReviewRequired('Asset source records differ from independent snapshot')
    movements=pack(c,'movements','movement_inventory');ms=original_population(c,'movement_source',movements)
    if snapshot(c,d,ms['source_doc'],c['currency'])!=ms['records']:raise ReviewRequired('Movement source records differ from independent snapshot')
    # Physical population is independently sourced, not reconstructed by summing money.
    op=pack(c,'opening_population','opening_inventory');cl=pack(c,'closing_population','closing_inventory')
    for key,pop in [('opening',op),('closing',cl)]:
        if snapshot(c,d,p[key+'_population_doc'],c['currency'])!=pop:raise ReviewRequired('Physical '+key+' population differs from source')
    ids={r['id'] for r in rs};opening={r['id']:r for r in op};closing={r['id']:r for r in cl}
    if (set(opening)|set(closing)) - ids:raise ReviewRequired('Physical source asset omitted from accounting register')
    physical_ids=[]
    for r in rs:
        texts(r,'physical_id','category','control_doc','classification_doc','quantity_unit')
        enum(r,'quantity_unit',{'biological_units','head','trees','plants','lots','kg','litres','tonnes'})
        physical_ids.append(r['physical_id']);enum(r,'state',{'opening','purchase','birth'})
        if r['currency']!=c['currency']:raise ReviewRequired('Multi-currency Agriculture aggregation requires FX owner')
        law=snapshot(c,d,r['control_doc'],c['currency']);scope=snapshot(c,d,r['classification_doc'],c['currency'])
        if law.get('asset_id')!=r['id'] or law.get('physical_id')!=r['physical_id'] or not flag(law,'control_supported'):
            raise ReviewRequired('Current legal/control evidence does not support asset identity')
        texts(law,'rights_memo');texts(scope,'scope_memo')
        if any(law[k]!=c[k] for k in ('entity','framework','jurisdiction')) or law['checked_on']!=c['execution_date'] or not flag(law,'probable_benefits'):
            raise ReviewRequired('Current rights and probable economic benefit evidence required')
        if scope['asset_id']!=r['id'] or scope['category']!=r['category'] or scope['framework']!=c['framework']:
            raise ReviewRequired('Qualified classification source contradicts register')
        route=enum(scope,'route',{'agriculture','fixed-assets','inventory','land','intangible','outside_scope'})
        if route!='agriculture':
            raise ReviewRequired('Classified '+route+'; route to existing accounting owner, do not recognize inside Agriculture')
        if not flag(scope,'living') or not flag(scope,'agricultural_activity'):
            raise ReviewRequired('Biological asset requires living asset and agricultural activity evidence')
        if r['category']=='bearer_plant' and c['framework'] in {'IFRS','AASB'}:
            raise ReviewRequired('Bearer plant belongs to Fixed Assets; separately identified growing produce may remain Agriculture')
        if c['framework']=='UK_GAAP' and r['category']=='growing_produce':
            raise ReviewRequired('FRS 102 does not separate produce from related biological asset before harvest')
        enum(r,'category',{'consumable_livestock','consumable_crop','growing_produce','bearer_livestock','bearer_plant'})
        if c['framework']=='US_GAAP':raise ReviewRequired('US Agriculture uses ASC 905 asset-specific cost/PPE/inventory routes; IFRS fair-value execution is unavailable')
        if c['requested_action']=='accounting':
            if scope['agriculture_model']!='fair_value_less_costs_to_sell' or c['accounting_policy']['class_models'].get(r['category'])!=scope['agriculture_model']:
                raise ReviewRequired('Biological class policy source contradicts executable fair-value model')
    unique(physical_ids,'physical biological asset')
    if c['requested_action']=='classification':
        population(c,rs,[abs(dec(r['amount'])) for r in rs])
        if movements or c['gl']:raise ReviewRequired('Classification workpaper cannot execute monetary movements')
        return finalize(c,'Agriculture classification supported; measurement and recognition require a separate accounting case',
            dict(classified_assets=len(rs)),BOUNDARY_LIMITS)
    if c['accounting_policy'].get('agriculture_model')!='fair_value_less_costs_to_sell':
        raise ReviewRequired('UK cost policy or reliability exception needs a separate governed accounting method')
    used=set(c['knowledge_review']['applied_claim_ids'])
    applied={x['decision'] for x in claims if x['claim_id'] in used}
    need={'scope','recognition','initial','subsequent','selling-costs','gain-loss','harvest','harvest-event','disclosure-gain','disclosure-risks','disclosure-roll'} if c['framework'] in {'IFRS','AASB'} else {'recognition','election','preharvest','fv','harvest-fv','valuation','disclosure-fv','disclosure-harvest','edition'}
    if not need<=applied:raise ReviewRequired('Agriculture applied knowledge selection omits material accounting decisions')
    by={r['id']:r for r in rs};events={};event_physical=[]
    for m in movements:
        if m['asset_id'] not in by:raise ReviewRequired('Movement references missing biological asset')
        if m['asset_id'] in events:raise ReviewRequired('Multiple whole-unit terminal movements double count harvest/death')
        enum(m,'kind',{'harvest','death'});inperiod(c,m['date'])
        if m['currency']!=c['currency']:raise ReviewRequired('Movement currency mismatch')
        events[m['asset_id']]=m;event_physical.append(m['event_source_id'])
    unique(event_physical,'physical movement source')
    entries=[];schedule=[];harvests=[];produce_ids=[];opv=clv=gain=additions=harvest_total=death_total=ZERO;opqty=clqty=buyqty=birthqty=harvestqty=deadqty=ZERO
    for r in rs:
        qty=positive(r['quantity']);expected_qty=qty
        terminal=events.get(r['id']);opening_value=nonnegative(r['opening_value']);consideration=nonnegative(r['purchase_cost'])
        if r['state']=='opening':
            if r['id'] not in opening or consideration:raise ReviewRequired('Opening biological asset or acquisition evidence inconsistent')
            exact(opening[r['id']]['quantity'],qty,'Opening physical quantity');exact(opening[r['id']]['carrying_value'],opening_value,'Opening source carrying amount');opqty+=qty;opv+=opening_value
            if opening[r['id']]['physical_id']!=r['physical_id']:raise ReviewRequired('Opening physical identity contradiction')
            texts(r,'opening_valuation_memo');base=opening_value
        else:
            if r['id'] in opening or opening_value:raise ReviewRequired('Birth/purchase cannot duplicate an opening asset')
            inperiod(c,r['recognition_date']);v=qualified_value(c,d,r['initial_value_doc'],r,qty,r['recognition_date']);base=v;additions+=v
            if r['state']=='purchase':
                buyqty+=qty;entries+= [journal(('Dr','Biological assets',consideration),('Cr','Cash',consideration))]
                evidence_doc=snapshot(c,d,r['purchase_doc'],c['currency'])
                if evidence_doc['asset_id']!=r['id'] or evidence_doc['date']!=r['recognition_date']:raise ReviewRequired('Purchase source identity/date mismatch')
                exact(evidence_doc['quantity'],qty,'Purchase quantity');exact(evidence_doc['cost'],consideration,'Purchase consideration')
            else:
                birthqty+=qty
                if consideration:raise ReviewRequired('Birth cannot have purchase consideration')
                b=snapshot(c,d,r['birth_doc'],c['currency'])
                texts(b,'event_source_id','evidence_memo')
                if b['asset_id']!=r['id'] or b['physical_id']!=r['physical_id'] or b['date']!=r['recognition_date'] or not flag(b,'control_supported'):
                    raise ReviewRequired('Independent birth source identity/date/control contradiction')
                exact(b['quantity'],qty,'Independent birth population quantity')
                if b['event_source_id'] in event_physical:raise ReviewRequired('Aliased birth/terminal event source')
                event_physical.append(b['event_source_id'])
            delta=v-consideration;gain+=delta;entries+=[signed_entry('Biological assets','Agriculture measurement gain',delta)]
        if terminal:
            exact(terminal['quantity'],qty,'Whole-unit terminal quantity')
            if r['id'] in closing:raise ReviewRequired('Harvested/dead asset remains in closing population')
            if r['state']!='opening' and iso(terminal['date'])<iso(r['recognition_date']):raise ReviewRequired('Harvest/death precedes initial recognition')
            if terminal['kind']=='harvest':
                measured=qualified_value(c,d,terminal['valuation_doc'],r,qty,terminal['date'])
                delta=measured-base;gain+=delta;entries+=[signed_entry('Biological assets','Agriculture measurement gain',delta)]
                h=snapshot(c,d,terminal['harvest_doc'],c['currency'])
                if h['asset_id']!=r['id'] or h['date']!=terminal['date']:raise ReviewRequired('Harvest source identity/date mismatch')
                exact(h['harvest_quantity'],terminal['harvest_quantity'],'Harvest produce quantity');positive(h['harvest_quantity']);enum(h,'produce_unit',{'head','kg','litres','tonnes','units'})
                if not flag(h,'entire_asset_harvested') or not flag(h,'boundary_only'):raise ReviewRequired('Partial harvest/continuing bearer asset or postharvest costing needs specialist method')
                texts(h,'produce_id','produce_valuation_doc');enum(h,'produce_category',{'meat','grain','timber','fruit','vegetable','other_produce'})
                if h['produce_id'] in ids or h['produce_id'] in produce_ids:raise ReviewRequired('Harvest produce identity aliases biological or other harvested population')
                produce_ids.append(h['produce_id'])
                produce=dict(id=h['produce_id'],category=h['produce_category'],quantity_unit=h['produce_unit'])
                qualified=snapshot(c,d,h['produce_valuation_doc'],c['currency'])
                if not flag(qualified,'point_at_harvest') or qualified['origin_asset_id']!=r['id']:
                    raise ReviewRequired('Qualified produce measurement must cover harvest point and original biological unit')
                harvested_value=qualified_value(c,d,h['produce_valuation_doc'],produce,h['harvest_quantity'],terminal['date'])
                exact(h['qualified_produce_fvcts'],harvested_value,'Harvest source qualified produce measurement')
                exact(h['inventory_entry_value'],harvested_value,'Harvest boundary inventory entry')
                conversion=harvested_value-measured
                if c['framework']=='UK_GAAP' and conversion:
                    raise ReviewRequired('UK unequal biological-to-produce harvest conversion requires separately governed accounting support')
                gain+=conversion;harvest_total+=harvested_value;harvestqty+=qty
                entries+=[journal(('Dr','Harvest inventory entry',harvested_value),('Cr','Biological assets',measured),
                    ('Cr' if conversion>=0 else 'Dr','Agriculture measurement gain',abs(conversion)))]
                harvests.append(dict(entry_value=harvested_value,biological_carrying_removed=measured,harvest_conversion_gain=conversion,quantity=dec(h['harvest_quantity']),unit=h['produce_unit'],downstream_owner='Inventory & Cost Accounting unavailable; no subsequent measurement performed'))
            else:
                loss=snapshot(c,d,terminal['death_doc'],c['currency'])
                if loss['asset_id']!=r['id'] or loss['date']!=terminal['date']:raise ReviewRequired('Death source identity/date mismatch')
                exact(loss['quantity'],qty,'Death quantity')
                if nonnegative(loss['recoveries']) or not flag(loss,'zero_salvage'):raise ReviewRequired('Recoveries/sale proceeds require separate owners')
                death_total+=base;deadqty+=qty;entries+=[journal(('Dr','Agriculture mortality loss',base),('Cr','Biological assets',base))]
            value=ZERO
        else:
            if r['id'] not in closing:raise ReviewRequired('Living source asset missing from closing population')
            if closing[r['id']]['physical_id']!=r['physical_id']:raise ReviewRequired('Closing physical identity contradiction')
            exact(closing[r['id']]['quantity'],qty,'Closing physical quantity');value=qualified_value(c,d,r['closing_value_doc'],r,qty,c['reporting_period'])
            exact(closing[r['id']]['carrying_value'],value,'Closing population carrying amount');exact(r['amount'],value,'Source/GL carrying assertion')
            delta=value-base;gain+=delta;entries+=[signed_entry('Biological assets','Agriculture measurement gain',delta)];clv+=value;clqty+=qty
        if terminal:exact(r['amount'],ZERO,'Terminal asset closing carrying assertion')
        schedule.append(dict(opening=opening_value,closing=value,quantity=qty,terminal=terminal['kind'] if terminal else 'living'))
    if {r['id'] for r in rs if r['state']=='opening'}!=set(opening):raise ReviewRequired('Opening asset population omitted or relabelled')
    # Initial fair value differences are included in gain, so additions below
    # use cash consideration, not fair-value initial amount, in the monetary bridge.
    purchase_total=sum((nonnegative(r['purchase_cost']) for r in rs),ZERO)
    exact(clv,opv+purchase_total+gain-harvest_total-death_total,'Agriculture opening-to-closing monetary rollforward')
    units={r['quantity_unit'] for r in rs}
    if len(units)!=1:raise ReviewRequired('Mixed quantity units require separately controlled schedules')
    exact(clqty,opqty+buyqty+birthqty-harvestqty-deadqty,'Agriculture quantity rollforward')
    population(c,rs,[nonnegative(r['amount']) for r in rs]);stocks(c,{'Biological assets':(opv,clv)})
    for g in c['gl']:
        if g['currency']!=c['currency']:raise ReviewRequired('GL currency/unit contradiction')
    dis=c['disclosures'];source(c,dis);texts(dis,'requirements_memo','checked_on','scope_memo','requirements_doc')
    if dis['checked_on']!=c['execution_date']:raise ReviewRequired('Stale Agriculture disclosure requirements review')
    if snapshot(c,d,dis['requirements_doc'],c['currency'])!=dis['requirements']:raise ReviewRequired('Disclosure population differs from qualified requirements source')
    req=rows(dis['requirements'],False);inventory(dis,'requirement_inventory',req)
    if any(not flag(x,'supported') for x in req):raise ReviewRequired('Agriculture disclosure population incomplete')
    needed={'classes','policies','gain_loss','quantities','rollforward','harvest','valuation','restrictions','commitments','risk'} if c['framework'] in {'IFRS','AASB'} else {'classes','policies','gain_loss','valuation','rollforward'}
    if {x['id'] for x in req}!=needed:raise ReviewRequired('Framework-specific Agriculture disclosure coverage unresolved')
    expected_support=dict(classes=sorted({r['category'] for r in rs}),policies='fair_value_less_costs_to_sell',gain_loss=gain,
        rollforward=dict(opening=opv,purchases=purchase_total,measurement_gain=gain,harvest_entry=harvest_total,mortality_loss=death_total,closing=clv),
        quantities=dict(opening=opqty,purchases=buyqty,births=birthqty,harvest=harvestqty,deaths=deadqty,closing=clqty),harvest=harvest_total)
    used_values=[]
    for r in rs:
        if r['state']!='opening':used_values.append(r['initial_value_doc'])
        if r['id'] not in events:used_values.append(r['closing_value_doc'])
        elif events[r['id']]['kind']=='harvest':
            used_values.append(events[r['id']]['valuation_doc'])
            used_values.append(snapshot(c,d,events[r['id']]['harvest_doc'],c['currency'])['produce_valuation_doc'])
    expected_support['valuation']=sorted(used_values)
    support_ids=[]
    for requirement in req:
        texts(requirement,'evidence_memo','support_doc');support_ids.append(requirement['support_doc'])
        supporting=snapshot(c,d,requirement['support_doc'],c['currency'])
        texts(supporting,'support_memo')
        if any(supporting[k]!=v for k,v in [('requirement_id',requirement['id']),('entity',c['entity']),('framework',c['framework']),('checked_on',c['execution_date'])]):
            raise ReviewRequired('Agriculture disclosure supporting source scope mismatch')
        key=requirement['id']
        if key in expected_support:
            expected=expected_support[key];actual=supporting['value']
            if isinstance(expected,dict):
                if not isinstance(actual,dict) or set(actual)!=set(expected):raise ReviewRequired('Disclosure bridge field population incomplete')
                for field in expected:exact(actual[field],expected[field],'Disclosure '+key+' '+field)
            elif isinstance(expected,(str,list)):
                if actual!=expected:raise ReviewRequired('Disclosure '+key+' support contradicts accounting schedule')
            else:exact(actual,expected,'Disclosure '+key+' amount')
    unique(support_ids,'disclosure supporting source')
    exact(dis['closing_carrying_value'],clv,'Disclosure closing');exact(dis['pnl_measurement_gain'],gain,'Disclosure gain/loss sign');exact(dis['harvest_entry'],harvest_total,'Disclosure harvest boundary')
    if dis['presentation']!='asset_and_profit_or_loss':raise ReviewRequired('Agriculture gain/loss must not be placed in OCI/equity')
    if 'price_change' in dis or 'physical_change' in dis:
        raise ReviewRequired('Price/physical decomposition requires separately qualified bridge; total gain only is executable')
    calcs=dict(currency=c['currency'],quantity_unit=next(iter(units)),opening=opv,purchases=purchase_total,measurement_gain=gain,harvest_entry=harvest_total,mortality_loss=death_total,closing=clv,
        quantity_bridge=dict(opening=opqty,purchases=buyqty,births=birthqty,harvest=harvestqty,deaths=deadqty,closing=clqty),assets=schedule,harvest=harvests)
    r=finalize(c,'Biological asset FV less costs to sell, quantity/GL bridge and harvest boundary reconciled',calcs,BOUNDARY_LIMITS,entries=entries)
    r['disclosures_impacted']=['Class and policy-specific disclosure support reconciled; use Financial Statements and Disclosure Management owners for final reporting']
    return r
