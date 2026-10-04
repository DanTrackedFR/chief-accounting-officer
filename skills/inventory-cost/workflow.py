"""Controlled ordinary inventory and manufacturing cost integrator, never an ERP."""
from final_batch_accounting import *
import re
KEYS=('items','movements','orders','costs','standards','valuation','originals','documents','gl','imports','owner_links','owner_gl_effects','scope','disclosures','accounting_policy','currency','count','cutoff','requested_action')
LIMITS=['Ordinary commercial inventory and controlled manufacturing accounting for 2026 only; supplied ownership, BOM, routing, capacity and valuation judgments remain independently reviewed.', 'Joint/by-products, retail estimation, autonomous forecasts, specialist industry exceptions and borrowing-cost capitalization require separate governed methods. No ERP posting or audit opinion is issued.', 'Upstream owner entries remain with their originating owner; Inventory records eligible cost absorption and inventory relief once.']
ACCOUNTS={'RM':'Raw materials','WIP':'Work in progress','FG':'Finished goods','MERCH':'Merchandise'}

def copy_layers(ls):return [dict(x) for x in ls]

def exact(a,b,label):
    if dec(a)!=dec(b):raise ReviewRequired(label+' exact reconciliation failed')

def frozen(c,d,key):
    rs=pack(c,key,key+'_inventory');p=c['originals'][key];source(c,p);inventory(p,'inventory',p['records'])
    if digest(rs)!=digest(p['records']) or snapshot(c,d,p['source_doc'],c['currency'])!=p['records']:raise ReviewRequired('Independent original '+key+' differs from accounting tracker')
    return rs

def owned(c,d,item):
    r=snapshot(c,d,item['ownership_doc'],c['currency']);texts(r,'rights_memo','ownership_event_id')
    if any(r[k]!=c[k] for k in ('entity','framework','jurisdiction')) or r['checked_on']!=c['execution_date'] or r['item_id']!=item['id']:raise ReviewRequired('Ownership dimensions/currentness mismatch')
    if not flag(r,'owned') or flag(r,'third_party_owned') or flag(r,'consigned_out_without_ownership'):raise ReviewRequired('Inventory economic ownership unresolved')

def scope(c,d):
    p=c['scope'];source(c,p);texts(p,'checked_on','scope_memo','edition','entity_scope')
    enum(c,'requested_action',{'accounting','workpaper'})
    if c.get('package')!='inventory-cost' or not re.fullmatch('[A-Z]{3}',c['currency']):raise ReviewRequired('Inventory package/currency mismatch')
    if not iso('2026-01-01')<=iso(c['period_start'])<=iso(c['reporting_period'])<=iso('2026-12-31'):raise ReviewRequired('Inventory knowledge reviewed 2026 only')
    ed={'IFRS':'IAS2_2026','US_GAAP':'ASC330_2026','UK_GAAP':'FRS102_September2024_2026','AASB':'AASB102_2026_Tier1'}[c['framework']]
    if p['checked_on']!=c['execution_date'] or p['edition']!=ed or ed not in c['applicability_review']['standard_versions']:raise ReviewRequired('Inventory operative edition/currentness unresolved')
    expected_scope={'IFRS':'for_profit_full_ifrs','US_GAAP':'ordinary_us_gaap','UK_GAAP':'frs102_full_commercial','AASB':'aasb_tier1_for_profit'}[c['framework']]
    if p['entity_scope']!=expected_scope:raise ReviewRequired('Inventory entity scope differs from approved claims')
    if c['framework']=='AASB' and c['reporting_tier']!=1:raise ReviewRequired('AASB Tier2 disclosure overlay excluded')
    if c['framework']=='UK_GAAP' and c['uk_standard_edition']!='September2024':raise ReviewRequired('FRS102 edition mismatch')
    for k in ('borrowing_capitalization','joint_products','retail_method','industry_exception','forecast_generation','external_posting','early_adoption'):
        if flag(p,k):raise ReviewRequired('Unsupported Inventory specialist boundary: '+k)
    actual=snapshot(c,d,p['source_doc'],c['currency'])
    if actual!= {k:v for k,v in p.items() if k not in ('id','owner','reviewer','evidence','approved','approval_date','version','approved_version','source_entity','source_framework','source_period','source_doc')}:raise ReviewRequired('Independent scope source contradiction')
    return p

def links(c,d,costs,movements):
    imports(c,{'derivatives-hedge-accounting','agriculture-biological-assets','fixed-assets','employee-benefits-payroll','accounts-payable','foreign-currency','leases','revenue-recognition','financial-statements','disclosure-management','accounting-controls-icfr','accounting-systems-data-integrity'})
    used=set();economic=set();bindings={}
    signatures=[digest({'package':i['package'],'economic_source':{k:v for k,v in i['case'].items() if k not in {'case_id','knowledge_review','reviewer_signoff','preparer','judgment_memo','assumptions'}}}) for i in c['imports']]
    unique(signatures,'actual owner economic population under case aliases')
    for r in pack(c,'owner_links','owner_links_inventory'):
        imp=actual_owner(c,r['owner_import']);path=r['result_path'];texts(r,'economic_id','target_id')
        if not isinstance(path,list) or not path or any(not isinstance(x,str) or not x for x in path):raise ReviewRequired('Actual owner result assertion path required')
        if r['economic_id'] in economic:raise ReviewRequired('Duplicate economic owner amount')
        value=imp['result']['calculations']
        for k in path:
            if isinstance(value,list):
                matched=[x for x in value if x.get('id')==k]
                if len(matched)!=1:raise ReviewRequired('Actual owner source row absent')
                value=matched[0]
            elif isinstance(value,dict) and k in value:value=value[k]
            else:raise ReviewRequired('Actual numerical owner assertion missing')
        if isinstance(value,(dict,list,bool)) or value is None:raise ReviewRequired('Owner assertion must be numerical')
        b=snapshot(c,d,r['source_doc'],c['currency']);field=r['source_field']
        if not isinstance(b,dict) or field not in b or b.get('economic_id')!=r['economic_id']:raise ReviewRequired('Owner source economic identity missing')
        exact(r['amount'],value,'Owner amount');exact(b[field],value,'Owner source assertion')
        candidates=[x for x in costs+movements if x['id']==r['target_id']]
        if len(candidates)!=1 or candidates[0]['economic_id']!=r['economic_id'] or candidates[0].get('owner_import')!=imp['id']:raise ReviewRequired('Owner assertion not bound to actual consumed source')
        target=candidates[0]
        expected={'labour':'employee-benefits-payroll','depreciation':'fixed-assets','ap':'accounts-payable','fx':'foreign-currency','lease':'leases','harvest':'agriculture-biological-assets','hedge_basis':'derivatives-hedge-accounting'}.get(target.get('owner_kind'))
        if expected!=imp['package']:raise ReviewRequired('Wrong source accounting owner')
        valid_path={'labour':path==['expense'],'depreciation':path==['depreciation'],'ap':path==['invoices'],'fx':len(path)==3 and path[0]=='transactions' and path[2]=='initial','harvest':path==['harvest_entry'],'hedge_basis':len(path)==3 and path[0]=='basis_adjustments' and path[2]=='amount'}.get(target.get('owner_kind'),False)
        if not valid_path:raise ReviewRequired('Owner metric cannot establish manufacturing cost')
        texts(b,'production_mapping_memo','cost_qualification_memo')
        if not flag(b,'eligible_manufacturing') or b['currency']!=c['currency']:raise ReviewRequired('Owner cost qualification/currency mismatch')
        if expected=='agriculture-biological-assets' and (path!=['harvest_entry'] or target.get('kind')!='harvest'):raise ReviewRequired('Agriculture harvest entry boundary only')
        if expected=='derivatives-hedge-accounting':
            if c['framework'] not in {'IFRS','AASB','UK_GAAP'} or target.get('kind')!='purchase' or target.get('hedge_basis_adjustment_id')!=path[1]:raise ReviewRequired('Only governed nonfinancial purchase basis handoff supported')
            adjustment=next((x for x in imp['result']['calculations']['basis_adjustments'] if x['id']==path[1]),None)
            if adjustment is None or any(adjustment[k]!=v for k,v in {'item_id':target['item'],'acquisition_id':target['economic_id'],'currency':c['currency'],'entity':c['entity'],'framework':c['framework'],'date':target['date']}.items()):raise ReviewRequired('Hedge basis SKU/acquisition/dimension mismatch')
            exact(adjustment['quantity'],target['quantity'],'Hedge basis receipt quantity')
        else:exact(target['amount'],value,'Consumed owner amount')
        used.add(imp['id']);economic.add(r['economic_id']);bindings[target['id']]=r
    if used!={i['id'] for i in c['imports']}:raise ReviewRequired('Unused or unbound imported owner result')
    return bindings

def assess(c,claims):
    items=begin(c,'items');d=evidence(c);scope(c,d);review_release(c,KEYS)
    for g in rows(c['gl']):
        source(c,g)
        if g['currency']!=c['currency']:raise ReviewRequired('Inventory GL/statement currency mismatch')
    if set(c['knowledge_review']['applied_claim_ids'])!={x['claim_id'] for x in claims}:raise ReviewRequired('Inventory integrated workpaper must apply the entire reviewed decision population, including explicit excluded-route boundaries')
    for key in ('items','movements','orders','costs','standards','valuation'):
        frozen(c,d,key)
    movements=c['movements'];orders=c['orders'];costs=c['costs'];standards={s['order_id']:s for s in c['standards']}
    population(c,items,[abs(dec(r['closing_cost'])) for r in items])
    unique([i['physical_id'] for i in items],'physical item alias');unique([m['economic_id'] for m in movements],'movement alias');unique([x['economic_id'] for x in costs],'upstream cost alias')
    unique([x['economic_id'] for x in movements+costs],'cross-population economic alias')
    unique([o['production_id'] for o in orders],'production order alias')
    unique([l['economic_id'] for i in items for l in rows(i['opening_layers'])],'opening inventory economic layer alias')
    purchase_components=[x['economic_id'] for m in movements if m['kind']=='purchase' for x in rows(snapshot(c,d,m['source_doc'],c['currency'])['cost_components'])]
    unique(purchase_components,'purchase component economic source reused across receipts')
    binding=links(c,d,costs,movements)
    by={i['id']:i for i in items};ob={o['id']:o for o in orders};quant={i['id']:nonnegative(i['opening_quantity']) for i in items};values={i['id']:nonnegative(i['opening_cost']) for i in items};opening=dict(values);layers={};entries=[];calcs={};consumed={o['id']:[] for o in orders};complete_orders=set();cost_seen=set();relief=ZERO;write=ZERO;reverse=ZERO;expense=ZERO
    def post(a,b,n):
        if n:entries.append(signed_entry(a,b,n))
    for i in items:
        texts(i,'physical_id','unit','location','ownership_doc','policy_group','currency');enum(i,'class',set(ACCOUNTS));owned(c,d,i)
        if i['currency']!=c['currency'] or i['unit'] not in {'units','kg','litres','tonnes','metres'}:raise ReviewRequired('Unsupported currency or quantity unit')
        formula=enum(i,'formula',{'FIFO','WEIGHTED_AVERAGE','SPECIFIC_IDENTIFICATION','LIFO'})
        if formula=='LIFO' and c['framework']!='US_GAAP':raise ReviewRequired('LIFO prohibited in this framework')
        if formula=='SPECIFIC_IDENTIFICATION' and flag(i,'interchangeable'):raise ReviewRequired('Specific identification for interchangeable items unsupported')
        if c['accounting_policy']['formula_by_group'].get(i['policy_group'])!=formula:raise ReviewRequired('Formula policy group mismatch')
        ls=rows(i['opening_layers']);
        if ls!=sorted(ls,key=lambda l:(l['date'],l['id'])) or any(iso(l['date'])>=iso(c['period_start']) for l in ls):raise ReviewRequired('Opening FIFO/LIFO layer chronology invalid')
        unique([l['economic_id'] for l in ls],'cost layer alias')
        exact(sum((nonnegative(l['quantity']) for l in ls),ZERO),quant[i['id']],'Opening layer quantity');exact(sum((nonnegative(l['cost']) for l in ls),ZERO),values[i['id']],'Opening layer cost')
        layers[i['id']]=[[nonnegative(l['quantity']),nonnegative(l['cost']),l['id']] for l in ls]
    last_taken=[]
    def take(id,qty,layer_ids=None):
        nonlocal last_taken
        last_taken=[]
        qty=positive(qty)
        if qty>quant[id]:raise ReviewRequired('Unexplained negative inventory')
        f=by[id]['formula'];v=ZERO
        if f=='WEIGHTED_AVERAGE':
            v=cash(values[id]*qty/quant[id]);last_taken=[{'id':'weighted-average','quantity':qty,'cost':v}];layers[id]=[[quant[id]-qty,values[id]-v,'weighted-average']]
        else:
            remain=qty
            for l in (list(reversed(layers[id])) if f=='LIFO' else layers[id]):
                if f=='SPECIFIC_IDENTIFICATION' and l[2] not in (layer_ids or []):continue
                q=min(l[0],remain)
                if q:
                    cost=cash(l[1]*q/l[0]);l[0]-=q;l[1]-=cost;v+=cost;remain-=q;last_taken.append({'id':l[2],'quantity':q,'cost':cost})
            if remain:raise ReviewRequired('Insufficient identified cost layers')
        quant[id]-=qty;values[id]-=v
        return v
    def add(id,qty,cost,identity):
        quant[id]+=positive(qty);values[id]+=nonnegative(cost);layers[id].append([dec(qty),dec(cost),identity])
    def order_cost(o):
        nonlocal expense
        if o['id'] in complete_orders:raise ReviewRequired('Production order completed twice')
        enum(o,'architecture',{'job','batch','production_order','process'});texts(o,'bom_doc','routing_doc','capacity_doc','loss_doc','completion_doc')
        bom=snapshot(c,d,o['bom_doc'],c['currency']);routing=snapshot(c,d,o['routing_doc'],c['currency']);capacity=snapshot(c,d,o['capacity_doc'],c['currency']);loss=snapshot(c,d,o['loss_doc'],c['currency']);completion=snapshot(c,d,o['completion_doc'],c['currency'])
        for x in (bom,routing,capacity,loss,completion):
            if x['order_id']!=o['id'] or x['checked_on']!=c['execution_date']:raise ReviewRequired('Production source order/currentness mismatch')
        if bom['effective_from']>o['completion_date'] or bom['effective_to']<o['completion_date']:raise ReviewRequired('BOM outside effective period')
        if not flag(bom,'substitutions_approved'):raise ReviewRequired('Unsupported BOM substitution')
        output=positive(o['completed_quantity']);equiv=nonnegative(o['closing_equivalent_units']);good=output+equiv
        exact(completion['completed_quantity'],output,'Production completion');exact(completion['closing_equivalent_units'],equiv,'Production WIP equivalents')
        exact(loss['reported_loss'],o['scrap_quantity'],'Scrap/yield loss');texts(loss,'loss_memo')
        if not flag(loss,'loss_explained') or not flag(loss,'abnormal_excluded'):raise ReviewRequired('Scrap/yield evidence incomplete')
        mat=sum((x['amount'] for x in consumed[o['id']]),ZERO);lab=ZERO;var=ZERO;fixed=ZERO;hours=ZERO;driver=ZERO
        for x in costs:
            if x['order_id']!=o['id']:continue
            if x['id'] in cost_seen:raise ReviewRequired('Duplicate cost absorption')
            if x['currency']!=c['currency']:raise ReviewRequired('Manufacturing cost currency mismatch')
            cost_seen.add(x['id']);period_date(c,x['date']);enum(x,'kind',{'direct_labour','variable_overhead','fixed_overhead','abnormal'});texts(x,'source_doc','allocation_memo')
            orig=snapshot(c,d,x['source_doc'],c['currency'])
            if orig['economic_id']!=x['economic_id'] or orig['order_id']!=o['id']:raise ReviewRequired('Cost source identity contradiction')
            exact(orig['amount'],x['amount'],'Actual manufacturing cost source')
            if orig['currency']!=c['currency'] or not flag(orig,'manufacturing') or not flag(orig,'pool_complete'):raise ReviewRequired('Nonmanufacturing/incomplete pool cost')
            amount=nonnegative(x['amount'])
            if x.get('owner_import') and x['id'] not in binding:raise ReviewRequired('Unbound owner cost')
            if x['kind']=='direct_labour':
                h=positive(x['hours']);exact(orig['hours'],h,'Labour actual hours');exact(orig['rate'],x['rate'],'Labour actual rate');exact(amount,h*nonnegative(x['rate']),'Actual labour rate');lab+=amount;hours+=h;post(ACCOUNTS['WIP'],'Labour clearing',amount)
            elif x['kind']=='variable_overhead':
                u=positive(x['driver_units']);exact(orig['driver_units'],u,'Actual variable usage driver');var+=amount;driver+=u;post(ACCOUNTS['WIP'],'Overhead clearing',amount)
            elif x['kind']=='fixed_overhead':fixed+=amount
            else:expense+=amount;post('Abnormal manufacturing expense','Manufacturing clearing',amount)
        exact(routing['actual_labour_hours'],hours,'Routing actual labour');exact(routing['actual_driver_units'],driver,'Routing actual driver')
        normal=positive(capacity['normal_capacity']);actual=positive(capacity['actual_driver_units']);texts(capacity,'normal_capacity_memo','driver','pool_memo')
        if not flag(capacity,'reviewed_multi_period') or not flag(capacity,'pool_complete') or capacity['driver']!=routing['driver']:raise ReviewRequired('Unsupported overhead normal capacity/driver')
        exact(actual,driver,'Overhead actual denominator');absorbed=cash(fixed*actual/max(normal,actual));idle=fixed-absorbed;expense+=idle
        post(ACCOUNTS['WIP'],'Overhead clearing',absorbed);post('Unallocated overhead expense','Overhead clearing',idle)
        abnormal_material=nonnegative(loss['abnormal_material_cost']);
        if abnormal_material>mat:raise ReviewRequired('Abnormal material loss exceeds actual materials')
        expense+=abnormal_material;post('Abnormal manufacturing expense',ACCOUNTS['WIP'],abnormal_material)
        actual_total=nonnegative(o['opening_wip'])+mat-abnormal_material+lab+var+absorbed
        exact(o['opening_wip'],opening[o['wip_item']],'Opening production WIP source')
        components=rows(bom['components']);unique([r['component_id'] for r in components],'BOM component alias');allowed={r['component_id']:r for r in components};actual_by={}
        for x in consumed[o['id']]:actual_by.setdefault(x['item'],ZERO);actual_by[x['item']]+=x['quantity']
        if set(actual_by)!=set(allowed):raise ReviewRequired('BOM component usage population mismatch')
        for id,b in allowed.items():
            exact(loss['net_component_usage'][id],actual_by[id],'Production yield/net-input source')
            if good>nonnegative(b['maximum_good_output']):raise ReviewRequired('Production output exceeds controlled input yield')
        variance={};standard_total=actual_total
        if o['costing']=='standard':
            s=standards.get(o['id'])
            if s is None:raise ReviewRequired('Controlled standards missing')
            if any(k in s for k in ('yield_variance','mix_variance','unexplained_variance','standard_revaluation_amount')):raise ReviewRequired('Unsupported separate yield/mix/revaluation architecture requires governed company-specific allocation; cannot be silently netted')
            period_date(c,s['effective_date']);texts(s,'review_memo','approximation_memo');exact(s['output_quantity'],good,'Standard allowed output')
            if not flag(s,'current') or not flag(s,'material_deviation_reviewed') or flag(s,'unsupported_revaluation'):raise ReviewRequired('Stale/unreviewed standards')
            sm=ZERO;price=ZERO;usage=ZERO
            for id,b in allowed.items():
                stdqty=nonnegative(b['standard_quantity_per_output'])*good;stdprice=nonnegative(b['standard_price']);a=actual_by[id];cost=sum((x['amount'] for x in consumed[o['id']] if x['item']==id),ZERO)
                price+=cost-a*stdprice;usage+=(a-stdqty)*stdprice;sm+=stdqty*stdprice
            sh=nonnegative(s['labour_hours_per_output'])*good;lr=nonnegative(s['labour_rate']);su=nonnegative(s['driver_units_per_output'])*good;vr=nonnegative(s['variable_rate']);fr=nonnegative(s['fixed_rate']);budget=nonnegative(s['fixed_budget'])
            exact(budget,normal*fr,'Standard fixed rate normal capacity')
            variance=dict(material_price=price,material_usage=usage,labour_rate=lab-hours*lr,labour_efficiency=(hours-sh)*lr,variable_spending=var-driver*vr,variable_efficiency=(driver-su)*vr,fixed_spending=fixed-budget,fixed_volume=budget-su*fr)
            standard_total=nonnegative(o['opening_wip'])+sm+sh*lr+su*(vr+fr)
            exact(sum(variance.values(),ZERO),mat+lab+var+fixed-(standard_total-dec(o['opening_wip'])),'Gross manufacturing variance decomposition')
            disposition=s['disposition'];exact(disposition['eligible_normal'],actual_total-standard_total,'Eligible actual-versus-standard adjustment');exact(disposition['abnormal_idle'],idle,'Abnormal/idle variance expense')
            if not flag(disposition,'gross_reviewed') or not flag(disposition,'inventory_cogs_reviewed'):raise ReviewRequired('Variance disposition unsupported or netted')
            normal_adjustment=actual_total-standard_total
            post('Manufacturing variance clearing',ACCOUNTS['WIP'],normal_adjustment)
            post('Manufacturing variance clearing','Unallocated overhead expense',idle)
            post('Manufacturing variance clearing','Abnormal manufacturing expense',abnormal_material)
            allocations=rows(disposition['components']);unique([a['component'] for a in allocations],'gross variance disposition')
            members=[key for a in allocations for key in a.get('members',[a['component']])]
            unique(members,'variance reporting member allocation')
            if set(members)!=set(variance):raise ReviewRequired('Company variance reporting architecture omits or duplicates a measured component')
            if any('members' in a for a in allocations):
                texts(s,'company_reporting_memo');exact(s['reporting_gross_adverse'],sum((max(n,ZERO) for n in variance.values()),ZERO),'Company gross adverse variance source');exact(s['reporting_gross_favorable'],sum((min(n,ZERO) for n in variance.values()),ZERO),'Company gross favorable variance source')
            normal_sum=ZERO;idle_sum=ZERO;abnormal_sum=ZERO
            for a in allocations:
                key=a['component'];member_keys=a.get('members',[key]);amount=sum((variance[k] for k in member_keys),ZERO);exact(a['total'],amount,'Gross component variance amount')
                exact(dec(a['inventory'])+dec(a['idle_expense'])+dec(a.get('abnormal_expense','0')),amount,'Gross component disposition')
                # Normal price/usage/rate/spending differences restore actual cost.
                # Fixed idle capacity is separately expensed, never hidden in stock.
                expected_idle=idle if 'fixed_volume' in member_keys else ZERO
                exact(a['idle_expense'],expected_idle,'Idle fixed variance classification')
                abnormal_component=dec(a.get('abnormal_expense','0'));exact(abnormal_component,sum((dec(loss.get('abnormal_variance_by_component',{}).get(k,'0')) for k in member_keys),ZERO),'Abnormal material variance classification')
                normal_sum+=dec(a['inventory']);idle_sum+=dec(a['idle_expense']);abnormal_sum+=abnormal_component
                account='Manufacturing '+key+' variance'
                post(account,'Manufacturing variance clearing',amount)
                post(ACCOUNTS['WIP'],account,dec(a['inventory']))
                post('Unallocated overhead expense',account,dec(a['idle_expense']));post('Abnormal manufacturing expense',account,abnormal_component)
            exact(normal_sum,normal_adjustment,'Normal variance inventory adjustment');exact(idle_sum,idle,'Idle variance disposition');exact(abnormal_sum,abnormal_material,'Abnormal material variance disposition')

        elif o['costing']!='actual':raise ReviewRequired('Unsupported costing method')
        # Supplied component-equivalent-unit architecture is recomputed. Simple
        # homogeneous production uses the same completion share for all costs.
        if not flag(completion,'homogeneous_equivalents_reviewed'):raise ReviewRequired('Unsupported heterogeneous WIP equivalence method')
        closing=cash(actual_total*equiv/good);finished=actual_total-closing
        exact(o['closing_wip_cost'],closing,'Closing WIP');exact(o['completed_cost'],finished,'Completed finished goods cost')
        exact(values[o['wip_item']],dec(o['opening_wip'])+mat,'WIP material ledger before absorption')
        values[o['wip_item']]+=lab+var+absorbed-abnormal_material;values[o['wip_item']]-=finished;quant[o['wip_item']]=equiv
        add(o['fg_item'],output,finished,o['production_id']);post(ACCOUNTS['FG'],ACCOUNTS['WIP'],finished)
        complete_orders.add(o['id']);calcs[o['id']]=dict(material=mat,direct_labour=lab,variable_overhead=var,fixed_overhead=fixed,absorbed_fixed=absorbed,abnormal_material_expense=abnormal_material,under_recovery=idle,standard_recovery=(fixed-su*fr if o['costing']=='standard' else idle),standard_total=standard_total,actual_eligible_total=actual_total,variances=variance,completed_cost=finished,completed_quantity=output,closing_equivalent_units=equiv,finished_unit_cost=finished/output,closing_wip=closing)
    if any(type(m['sequence']) is not int or m['sequence']<1 for m in movements):raise ReviewRequired('Movement sequence must be a positive integer')
    if movements!=sorted(movements,key=lambda m:(m['date'],m['sequence'])):raise ReviewRequired('Movement accounting chronology must match controlled date/sequence')
    unique([(m['date'],m['sequence']) for m in movements],'movement chronology')
    for m in movements:
        texts(m,'economic_id','date','currency');period_date(c,m['date'])
        if m['currency']!=c['currency'] or m['item'] not in by:raise ReviewRequired('Movement item/currency mismatch')
        id=m['item'];i=by[id];qty=positive(m['quantity']);kind=enum(m,'kind',{'purchase','issue','return','complete','sale','writeoff','transfer','count','harvest'})
        if m['unit']!=i['unit']:raise ReviewRequired('Movement unit mismatch')
        movement_source=snapshot(c,d,m['source_doc'],c['currency'])
        if movement_source['economic_id']!=m['economic_id'] or movement_source['date']!=m['date'] or movement_source['item']!=id:raise ReviewRequired('Movement ownership/cutoff source contradiction')
        exact(movement_source['quantity'],qty,'Movement original quantity')
        if not flag(movement_source,'ownership_supported') or not flag(movement_source,'in_period'):raise ReviewRequired('Movement ownership/cutoff unsupported')
        if kind in {'purchase','harvest'}:
            amount=nonnegative(m['amount'])
            if kind=='purchase':
                components=rows(movement_source['cost_components']);unique([x['economic_id'] for x in components],'landed cost alias');eligible=ZERO
                for x in components:
                    enum(x,'kind',{'price','discount','rebate','duty','nonrecoverable_tax','freight','handling','insurance','recoverable_tax','selling','abnormal','admin'})
                    if x['kind'] in {'recoverable_tax','selling','abnormal','admin'} and nonnegative(x['amount']):raise ReviewRequired('Excluded landed cost component')
                    eligible+=nonnegative(x['amount'])*(-1 if x['kind'] in {'discount','rebate'} else 1)
                hedge=ZERO
                if m.get('owner_kind')=='hedge_basis':
                    if m['id'] not in binding:raise ReviewRequired('Actual completed Hedge basis handoff required')
                    hedge=dec(binding[m['id']]['amount'])
                    if movement_source.get('hedge_basis_adjustment_id')!=m.get('hedge_basis_adjustment_id') or movement_source.get('hedge_already_in_components') is not False:raise ReviewRequired('Hedge basis duplication or source identity unresolved')
                    if movement_source.get('purchase_standard') is True:raise ReviewRequired('Hedge basis with purchase standard variance requires separately governed adapter')
                    exact(amount,eligible+hedge,'Purchased cost plus exactly-once hedge basis')
                else:exact(amount,eligible,'Purchased landed cost')
                if movement_source.get('purchase_standard') is True:
                    if i['class']!='MERCH':raise ReviewRequired('Purchase standard PPV route is bounded to resale stock; overlapping manufacturing price variance needs company-specific attribution')
                    if movement_source['standard_checked_on']!=c['execution_date'] or not flag(movement_source,'standards_reviewed'):raise ReviewRequired('Purchased inventory standards stale/unreviewed')
                    standard_purchase=qty*nonnegative(movement_source['standard_unit_cost']);ppv=amount-standard_purchase
                    exact(movement_source['ppv_inventory_adjustment'],ppv,'Purchase price variance normal disposition')
                    post(ACCOUNTS[i['class']],'Acquisition clearing',standard_purchase);post('Purchase price variance','Acquisition clearing',ppv);post(ACCOUNTS[i['class']],'Purchase price variance',ppv)
                    calcs.setdefault('purchase_price_variance',ZERO);calcs['purchase_price_variance']+=ppv
                else:post(ACCOUNTS[i['class']],'Acquisition clearing',eligible)
            else:
                if m['id'] not in binding:raise ReviewRequired('Actual Agriculture completed harvest handoff required')
                # The Agriculture owner already recognized initial inventory;
                # this source is opening/boundary intake, not another journal.
                if movement_source['harvest_gain_duplicate'] or movement_source['biological_remeasurement']:raise ReviewRequired('Duplicate biological/harvest accounting')
                # Current-period upstream recognition is retained separately
                # from the true reporting-period opening inventory.
                pass
            add(id,qty,amount,m['economic_id'])
        elif kind=='issue':
            if i['class']!='RM' or m['order_id'] not in ob or m['order_id'] in complete_orders:raise ReviewRequired('Invalid RM production issue order')
            amount=take(id,qty,m.get('layer_ids'));exact(m['amount'],amount,'Production material relieved cost');o=ob[m['order_id']]
            values[o['wip_item']]+=amount;post(ACCOUNTS['WIP'],ACCOUNTS['RM'],amount);consumed[o['id']].append(dict(item=id,quantity=qty,amount=amount,economic_id=m['economic_id'],taken_layers=copy_layers(last_taken)))
        elif kind=='return':
            order=m['order_id']
            if i['class']!='RM' or order not in consumed or order in complete_orders:raise ReviewRequired('Invalid production return')
            matches=[x for x in consumed[order] if x['economic_id']==m['original_issue']]
            if len(matches)!=1 or matches[0]['item']!=id:raise ReviewRequired('Original material issue source required')
            original=matches[0]
            if qty>original['quantity']:raise ReviewRequired('Return exceeds remaining material issue')
            texts(m,'return_layer_id');selected=[l for l in original['taken_layers'] if l['id']==m['return_layer_id']]
            if len(selected)!=1 or qty>selected[0]['quantity']:raise ReviewRequired('Original returned cost layer is missing or insufficient')
            original_layer=selected[0];amount=cash(original_layer['cost']*qty/original_layer['quantity']);exact(m['amount'],amount,'Original-layer production return');original_layer['quantity']-=qty;original_layer['cost']-=amount
            original['quantity']-=qty;original['amount']-=amount;quant[id]+=qty;values[id]+=amount
            restored=next((l for l in layers[id] if l[2]==m['return_layer_id']),None)
            if restored is None:layers[id].insert(0,[qty,amount,m['return_layer_id']])
            else:restored[0]+=qty;restored[1]+=amount
            values[ob[order]['wip_item']]-=amount
            post(ACCOUNTS['RM'],ACCOUNTS['WIP'],amount)
        elif kind=='complete':
            if m['order_id'] not in ob or id!=ob[m['order_id']]['fg_item']:raise ReviewRequired('Wrong production completion')
            o=ob[m['order_id']];exact(qty,o['completed_quantity'],'Completion movement quantity')
            if m['date']!=o['completion_date']:raise ReviewRequired('Completion period contradiction')
            order_cost(o);exact(m['amount'],o['completed_cost'],'Completion movement cost')
        elif kind in {'sale','writeoff','count'}:
            amount=take(id,qty,m.get('layer_ids'));exact(m['amount'],amount,'Inventory relief source')
            offset='Cost of goods sold' if kind=='sale' else ('Inventory count expense' if kind=='count' else 'Inventory disposal expense');post(offset,ACCOUNTS[i['class']],amount)
            if kind=='sale':relief+=amount
            else:expense+=amount
        else:
            target=m['destination_item']
            if target not in by or by[target]['physical_id']==i['physical_id'] or by[target]['class']!=i['class'] or by[target]['unit']!=i['unit']:raise ReviewRequired('Unsupported class/unit transfer')
            amount=take(id,qty,m.get('layer_ids'));exact(m['amount'],amount,'Transfer cost');add(target,qty,amount,m['economic_id'])
    if complete_orders!=set(ob) or cost_seen!={x['id'] for x in costs}:raise ReviewRequired('Uncompleted production or unabsorbed cost population')
    unique([v['item'] for v in c['valuation']],'valuation item population')
    valued={v['item'] for v in c['valuation']}
    for i in items:
        assessment=snapshot(c,d,i['measurement_doc'],c['currency']);texts(assessment,'estimate_memo','demand_evidence_memo','ageing_evidence_memo')
        if assessment['item']!=i['id'] or assessment['checked_on']!=c['execution_date'] or not flag(assessment,'population_reviewed'):raise ReviewRequired('Current complete item measurement population review required')
        if flag(assessment,'impairment_indicator')!=(i['id'] in valued):raise ReviewRequired('Inventory measurement indicators omitted or contradicted')
        if flag(assessment,'forecast_used') and (assessment['forecast_checked_on']!=c['execution_date'] or not flag(assessment,'forecast_reviewed')):raise ReviewRequired('Stale or unreviewed demand forecast')
        if (flag(assessment,'expired') or flag(assessment,'discontinued')) and not flag(assessment,'impairment_indicator'):raise ReviewRequired('Expiry/discontinuation impairment ignored')
    for v in c['valuation']:
        id=v['item'];texts(v,'source_doc');a=snapshot(c,d,v['source_doc'],c['currency'])
        if a['item']!=id or a['checked_on']!=c['execution_date'] or not flag(a,'current_market') or not flag(a,'completion_cost_complete') or not flag(a,'selling_cost_complete') or not flag(a,'obsolescence_reviewed'):raise ReviewRequired('Stale/incomplete lower-cost estimate evidence')
        if a['grouping']!='item' or flag(a,'forecast_invented') or not flag(a,'expiry_reviewed'):raise ReviewRequired('Unsupported grouping/forecast/expiry')
        texts(a,'valuation_memo','recovery_evidence_memo');exact(a['carrying_cost_before_measurement'],values[id],'Valuation source carrying cost');exact(a['prior_write_down'],v['prior_write_down'],'Original recognized write-down source');exact(a['original_cost'],values[id]+nonnegative(v['prior_write_down']),'Original inventory cost ceiling')
        if not flag(a,'recovery_reviewed') or (flag(a,'forecast_used') and (a['forecast_checked_on']!=c['execution_date'] or not flag(a,'forecast_reviewed'))):raise ReviewRequired('Unreviewed recovery/forecast evidence')
        if flag(a,'expired') and nonnegative(a['selling_price']) and not flag(a,'salvage_supported'):raise ReviewRequired('Expired inventory selling value lacks salvage support')
        nrv=nonnegative(a['selling_price'])-nonnegative(a['completion_cost'])-nonnegative(a['selling_cost'])
        nrv=max(ZERO,nrv)*quant[id];prior=nonnegative(v['prior_write_down']);original_cost=values[id]+prior
        if c['framework']=='US_GAAP' and by[id]['formula']=='LIFO':
            replacement=nonnegative(a['replacement_cost']);floor=max(ZERO,dec(a['selling_price'])-dec(a['completion_cost'])-dec(a['selling_cost'])-nonnegative(a['normal_profit']))
            market=min(max(replacement,floor),nrv/quant[id] if quant[id] else ZERO);nrv=market*quant[id]
        if by[id]['class']=='RM':
            texts(a,'finished_goods_recovery_doc','raw_measurement_method','raw_context_memo')
            fg=snapshot(c,d,a['finished_goods_recovery_doc'],c['currency']);texts(fg,'item','component','cost_basis_memo','net_sales_estimate_memo')
            if fg['component']!=id or fg['item'] not in by or by[fg['item']]['class']!='FG' or fg['checked_on']!=c['execution_date'] or not flag(fg,'current_market') or not flag(fg,'recovery_reviewed'):raise ReviewRequired('Raw material requires current controlled linked finished-goods recovery evidence')
            fg_id=fg['item']
            if quant[fg_id]<=0:raise ReviewRequired('Raw material recovery route requires actual finished-goods cost basis; future-production estimates need separately governed method')
            exact(fg['unit_cost'],values[fg_id]/quant[fg_id],'Finished-goods actual cost context')
            fg_nrv=max(ZERO,nonnegative(fg['selling_price'])-nonnegative(fg['completion_cost'])-nonnegative(fg['selling_cost']))
            recoverable=fg_nrv>=nonnegative(fg['unit_cost'])
            if flag(a,'finished_goods_recoverable')!=recoverable:raise ReviewRequired('Finished-goods recoverability assertion contradicts controlled costs/net selling evidence')
            if c['framework'] in {'IFRS','AASB'}:
                if recoverable:
                    if a['raw_measurement_method']!='finished_goods_recoverability':raise ReviewRequired('Recoverable finished-goods context cannot use stand-alone RM price markdown')
                    nrv=original_cost
                else:
                    if a['raw_measurement_method']!='replacement_cost' or not flag(a,'replacement_cost_appropriate'):raise ReviewRequired('Raw replacement-cost method requires actual nonrecoverable finished-goods context and reviewed approximation')
                    nrv=nonnegative(a['replacement_cost'])*quant[id]
            else:
                expected_raw='LCM' if c['framework']=='US_GAAP' and by[id]['formula']=='LIFO' else 'LCNRV'
                if a['raw_measurement_method']!=expected_raw or not flag(a,'framework_raw_method_reviewed'):raise ReviewRequired('US/UK raw method requires its actual formula-specific lower-cost analysis; no automatic IAS2 exception')
        target=min(original_cost,nrv)
        if c['framework']=='US_GAAP':target=min(values[id],target)
        delta=target-values[id];exact(v['adjustment'],delta,'Write-down/reversal controlled estimate')
        if delta<0:write-=delta
        else:reverse+=delta
        values[id]=target;post(ACCOUNTS[by[id]['class']],'Inventory measurement expense',delta)
    for i in items:
        exact(i['closing_quantity'],quant[i['id']],'Physical RM/WIP/FG closing quantity');exact(i['closing_cost'],values[i['id']],'Subledger closing cost')
    counts=c['count'];source(c,counts);cut=c['cutoff'];source(c,cut)
    if snapshot(c,d,counts['source_doc'],c['currency'])!=counts['records'] or {r['item'] for r in counts['records']}!=set(by):raise ReviewRequired('Count location population incomplete')
    unique([r['item'] for r in counts['records']],'count item population')
    for r in counts['records']:
        if r['location']!=by[r['item']]['location']:raise ReviewRequired('Count location mismatch')
        exact(r['quantity'],quant[r['item']],'Count source')
    if snapshot(c,d,cut['source_doc'],c['currency'])!=cut['records'] or {r['economic_id'] for r in cut['records']}!={m['economic_id'] for m in movements}:raise ReviewRequired('Cutoff source population incomplete')
    unique([r['economic_id'] for r in cut['records']],'cutoff source population')
    for r in cut['records']:
        if not flag(r,'ownership_supported') or not flag(r,'date_reviewed'):raise ReviewRequired('Unresolved cutoff review')
    stock={a:(sum((opening[i['id']] for i in items if ACCOUNTS[i['class']]==a),ZERO),sum((values[i['id']] for i in items if ACCOUNTS[i['class']]==a),ZERO)) for a in set(ACCOUNTS.values())};stocks(c,stock)
    dis=c['disclosures'];source(c,dis);actual=snapshot(c,d,dis['source_doc'],c['currency'])
    required_keys=({'policy','formula','classes','carrying','valuation_losses','estimates'} if c['framework']=='US_GAAP' else {'policy','formula','classes','carrying','write_down','pledged','reversal','reversal_circumstances'}|({'expense'} if c['framework']!='UK_GAAP' else set()))
    if set(dis['requirements'])!=required_keys or actual!=dis['requirements'] or any(x is None or x=='' for x in actual.values()):raise ReviewRequired('Framework disclosure population incomplete')
    exact(dis['closing_inventory'],sum(values.values(),ZERO),'Disclosure inventory');exact(dis['cogs'],relief,'COGS relief');exact(dis['write_down'],write,'Write-down disclosure');exact(dis['reversal'],reverse,'Reversal disclosure')
    if dis['checked_on']!=c['execution_date']:raise ReviewRequired('Stale inventory disclosure review')
    if actual['formula']!=c['accounting_policy']['formula_by_group'] or actual['classes']!=sorted({i['class'] for i in items}):raise ReviewRequired('Disclosure formula/class population contradiction')
    if not isinstance(actual['policy'],dict) or actual['policy']['framework']!=c['framework'] or actual['policy']['edition']!=c['scope']['edition'] or not actual['policy']['measurement_memo']:raise ReviewRequired('Disclosure policy framework/current basis mismatch')
    expected_carrying={a:v[1] for a,v in stock.items() if any(ACCOUNTS[i['class']]==a for i in items)}
    if not isinstance(actual['carrying'],dict) or set(actual['carrying'])!=set(expected_carrying):raise ReviewRequired('Disclosure class balance population incomplete')
    for account,amount in expected_carrying.items():exact(actual['carrying'][account],amount,'Disclosure class carrying amount')
    if 'write_down' in actual:exact(actual['write_down'],write,'Disclosure impairment amount')
    if 'valuation_losses' in actual:exact(actual['valuation_losses'],write,'US disclosure valuation losses')
    if 'reversal' in actual:exact(actual['reversal'],reverse,'Disclosure reversal amount')
    if 'expense' in actual:
        for k,n in {'cogs':relief,'manufacturing_other':expense,'write_down':write,'reversal':reverse}.items():exact(actual['expense'][k],n,'Disclosure inventory expense breakdown')
    if 'pledged' in actual:
        pledge=actual['pledged'];texts(pledge,'evidence_memo')
        if not flag(pledge,'reviewed') or nonnegative(pledge['amount'])>sum(values.values(),ZERO):raise ReviewRequired('Unsupported pledged inventory source')
    if 'reversal_circumstances' in actual:
        circumstances=actual['reversal_circumstances'];texts(circumstances,'evidence_memo')
        if not flag(circumstances,'reviewed'):raise ReviewRequired('Reversal circumstances evidence unresolved')
    if 'estimates' in actual:
        texts(actual['estimates'],'evidence_memo');enum(actual['estimates'],'model',{'LCNRV','LCM'})
        expected_model='LCM' if any(i['formula']=='LIFO' for i in items) else 'LCNRV'
        if actual['estimates']['model']!=expected_model or not flag(actual['estimates'],'reviewed'):raise ReviewRequired('US measurement model disclosure mismatch')

    calcs.update(closing_inventory=sum(values.values(),ZERO),cogs=relief,write_down=write,reversal=reverse,manufacturing_expense=expense,inventory_by_class={a:v[1] for a,v in stock.items()},owner_handoffs={'financial_statements':sum(values.values(),ZERO),'revenue_cogs':relief,'disclosure_inventory':sum(values.values(),ZERO),'systems_item_count':len(items),'controls_movement_count':len(movements)})
    retained=pack(c,'owner_gl_effects','owner_gl_effects_inventory');effect_by={};seen_retained=set()
    expected_harvest={m['id'] for m in movements if m['kind']=='harvest'}
    expected_hedge={m['id'] for m in movements if m.get('owner_kind')=='hedge_basis'}
    for effect in retained:
        texts(effect,'source_doc','movement_id','owner_import','owner_account','account');m=next((m for m in movements if m['id']==effect['movement_id']),None)
        if m is None or m['id'] not in (expected_harvest|expected_hedge) or m['id'] in seen_retained or m['owner_import']!=effect['owner_import']:raise ReviewRequired('Retained upstream movement missing/duplicated/mismatched')
        imp=actual_owner(c,effect['owner_import']);owner_delta=sum((dec(line['amount'])*(1 if line['side']=='Dr' else -1) for entry in imp['result']['journal_entry_implications'] for line in entry if line['account']==effect['owner_account']),ZERO)
        expected_account='Nonfinancial asset basis adjustment' if m['id'] in expected_hedge else 'Harvest inventory entry'
        if effect['account']!=ACCOUNTS[by[m['item']]['class']] or effect['owner_account']!=expected_account:raise ReviewRequired('Unsupported retained owner GL mapping')
        expected_amount=binding[m['id']]['amount'] if m['id'] in expected_hedge else m['amount']
        if m['id'] in expected_hedge:
            if effect.get('hedge_basis_adjustment_id')!=m['hedge_basis_adjustment_id']:raise ReviewRequired('Hedge retained economic adjustment mismatch')
            owner_delta=sum((dec(x['amount']) for x in imp['result']['calculations']['basis_adjustments'] if x['id']==m['hedge_basis_adjustment_id']),ZERO)
            exact(sum((dec(x['amount']) for x in imp['result']['calculations']['basis_adjustments']),ZERO),sum((dec(line['amount'])*(1 if line['side']=='Dr' else -1) for entry in imp['result']['journal_entry_implications'] for line in entry if line['account']==expected_account),ZERO),'Hedge handoffs to originating journal')
        exact(effect['amount'],expected_amount,'Retained owner movement basis');exact(effect['amount'],owner_delta,'Original owner-recognized inventory journal')
        original_effect=snapshot(c,d,effect['source_doc'],c['currency'])
        if original_effect!={k:effect[k] for k in (('movement_id','owner_import','owner_account','account','amount','hedge_basis_adjustment_id') if m['id'] in expected_hedge else ('movement_id','owner_import','owner_account','account','amount'))}:raise ReviewRequired('Original retained owner GL mapping differs')
        effect_by[effect['account']]=effect_by.get(effect['account'],ZERO)+dec(effect['amount']);seen_retained.add(m['id'])
    if seen_retained!=(expected_harvest|expected_hedge):raise ReviewRequired('Harvest owner-recognized movement absent from GL bridge')
    deltas={}
    for entry in entries:
        balance(entry)
        for line in entry:deltas[line['account']]=deltas.get(line['account'],ZERO)+dec(line['amount'])*(1 if line['side']=='Dr' else -1)
    accounts={g['id']:g for g in rows(c['gl'])};inventory(c,'gl_inventory',rows(c['gl']))
    if (set(deltas)|set(effect_by))-set(accounts):raise ReviewRequired('Journal/retained owner account absent from GL')
    for g in c['gl']:
        exact(g['closing'],dec(g['opening'])+deltas.get(g['id'],ZERO)+effect_by.get(g['id'],ZERO),'Original GL opening + own journals + retained owner movement')
        exact(g['statement'],g['closing'],'Original GL-to-statements')
    calcs.update(opening_inventory=sum(opening.values(),ZERO),retained_owner_intake=sum(effect_by.values(),ZERO),inventory_own_movement=sum((amount for account,amount in deltas.items() if account in set(ACCOUNTS.values())),ZERO))
    calcs['class_bridges']={a:dict(opening=op,own_movement=deltas.get(a,ZERO),retained_owner_intake=effect_by.get(a,ZERO),closing=cl) for a,(op,cl) in stock.items() if any(ACCOUNTS[i['class']]==a for i in items)}
    item_flows={i['id']:{'opening_quantity':nonnegative(i['opening_quantity']),'closing_quantity':quant[i['id']],'unit':i['unit'],'quantity_basis':'controlled_equivalent_units' if i['class']=='WIP' else 'controlled_physical_units','inflows':ZERO,'reliefs':ZERO} for i in items}
    for m in movements:
        f=item_flows[m['item']];q=dec(m['quantity'])
        if m['kind'] in {'purchase','harvest','return','complete'}:f['inflows']+=q
        elif m['kind'] in {'issue','sale','writeoff','count','transfer'}:f['reliefs']+=q
        if m['kind']=='transfer':item_flows[m['destination_item']]['inflows']+=q
    calcs['quantity_population']=item_flows

    result=finish('Controlled inventory and manufacturing costs reconcile from supplied source populations through RM, WIP, finished goods and all journal offsets.',calcs,entries,['Qualified source judgments remain separate from deterministic calculations'],['Current framework-specific inventory policy, classes, formula, impairment and pledge requirements tie to supplied statements.'])
    result['uncertainties']=LIMITS;result['open_items']=[];return result
