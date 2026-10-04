"""Synthetic controlled factory source fixtures; approvals are test records only."""
import copy
from decimal import Decimal
from governance_cases import case as prior,row,document,source_index
from governance_accounting import digest
from production import canonical_knowledge,PACKAGES,case_fingerprint,load_workflow
PACKAGE='inventory-cost'

def content(c,id):return next(x['content'] for x in c['documents'] if x['id']==id)
def replace_doc(c,id,value):
    for d in c['documents']:
        if d['id']==id:d['content']=copy.deepcopy(value);return
    document(c,id,value)
def sources(c):
    c['originals']={}
    for key in ('items','movements','orders','costs','standards','valuation'):
        c[key+'_inventory']=[r['id'] for r in c[key]];p=source_index(c,key+'-source',c[key]);p['source_doc']=key+'-original';c['originals'][key]=p;replace_doc(c,p['source_doc'],c[key])
    c['source_inventory']=c['items_inventory'];c['controls'].update(population_count=len(c['items']),population_amount=str(sum(abs(Decimal(i['closing_cost'])) for i in c['items'])))
    return refresh(c)
def refresh(c):
    c['document_inventory']=[d['id'] for d in c['documents']]
    for d in c['documents']:d['content_hash']=digest(d['content'])
    c['release_review']=row(c,'release',review_memo='Synthetic independent exact original source release',payload_fingerprint=digest({k:c[k] for k in load_workflow(PACKAGE).KEYS}))
    return c

def case(fw='IFRS',kind='manufacturing',costing='actual',formula='FIFO'):
    c=prior('ipo-accounting-readiness',fw)
    for k in ('readiness','readiness_source','dependencies','dependency_inventory','governance_method'):c.pop(k,None)
    c.update(package=PACKAGE,case_id='Synthetic Inventory '+fw+' '+kind+' '+costing+' '+formula,currency='USD',requested_action='accounting',documents=[],document_inventory=[],imports=[],owner_links=[],owner_links_inventory=[],owner_gl_effects=[],owner_gl_effects_inventory=[],items=[],movements=[],orders=[],costs=[],standards=[],valuation=[])
    ed={'IFRS':'IAS2_2026','US_GAAP':'ASC330_2026','UK_GAAP':'FRS102_September2024_2026','AASB':'AASB102_2026_Tier1'}[fw];c['applicability_review']['standard_versions']=[ed]
    flags={k:False for k in ('borrowing_capitalization','joint_products','retail_method','industry_exception','forecast_generation','external_posting','early_adoption')}
    payload=dict(checked_on=c['execution_date'],scope_memo='Synthetic ordinary commercial factory entity, reviewed edition and boundaries',edition=ed,entity_scope={'IFRS':'for_profit_full_ifrs','US_GAAP':'ordinary_us_gaap','UK_GAAP':'frs102_full_commercial','AASB':'aasb_tier1_for_profit'}[fw],**flags)
    c['scope']=row(c,'scope',source_doc='scope-source',**payload);document(c,'scope-source',payload)
    c['accounting_policy']['formula_by_group']={'materials':formula,'production':formula,'resale':formula}
    def item(id,cl,oq,oc,cq,cc,location='Factory'):
        i=row(c,id,physical_id='physical-'+id,unit='units',class_=cl,location=location,ownership_doc=id+'-rights',policy_group='materials' if cl=='RM' else ('production' if cl in {'WIP','FG'} else 'resale'),currency='USD',measurement_doc=id+'-measurement',opening_quantity=oq,opening_cost=oc,closing_quantity=cq,closing_cost=cc,formula=formula,interchangeable=formula!='SPECIFIC_IDENTIFICATION',opening_layers=[dict(id=id+'-opening',economic_id=id+'-opening-source',quantity=oq,cost=oc,date='2025-12-31')] if Decimal(oq) else [])
        i['class']=i.pop('class_');c['items'].append(i)
        document(c,i['measurement_doc'],dict(item=id,checked_on=c['execution_date'],population_reviewed=True,impairment_indicator=False,forecast_used=False,forecast_checked_on=c['execution_date'],forecast_reviewed=True,expired=False,discontinued=False,estimate_memo='Synthetic current item value/ageing review',demand_evidence_memo='Synthetic actual recent sales support, no autonomous forecast',ageing_evidence_memo='Synthetic current ageing expiry discontinuation source'))
        document(c,i['ownership_doc'],dict(item_id=id,rights_memo='Synthetic current purchased-title/owned third-party/consignment assessment',ownership_event_id='title-'+id,entity=c['entity'],framework=fw,jurisdiction=c['jurisdiction'],checked_on=c['execution_date'],owned=True,third_party_owned=False,consigned_out_without_ownership=False))
    def move(id,item,kind,q,amt,date='2026-06-30',**kw):
        m=row(c,id,economic_id='economic-'+id,item=item,kind=kind,quantity=q,amount=amt,date=date,currency='USD',unit='units',source_doc=id+'-source',sequence=len(c['movements'])+1,**kw);c['movements'].append(m)
        data=dict(economic_id=m['economic_id'],item=item,quantity=q,date=date,ownership_supported=True,in_period=True)
        if kind=='purchase':data['cost_components']=[dict(id='price',economic_id='price-'+id,kind='price',amount=amt)]
        document(c,m['source_doc'],data);return m
    if kind=='manufacturing':
        item('component','RM','100','1000','40','400');item('order-wip','WIP','0','0','20','200');item('product','FG','0','0','60','600')
        move('issue','component','issue','60','600',order_id='order-1',layer_ids=['component-opening'])
        move('completion','product','complete','80','800',date='2026-09-30',order_id='order-1')
        move('sale','product','sale','20','200',date='2026-10-31',layer_ids=['production-1'])
        o=row(c,'order-1',production_id='production-1',architecture='production_order',bom_doc='bom',routing_doc='routing',capacity_doc='capacity',loss_doc='loss',completion_doc='completion-evidence',completed_quantity='80',closing_equivalent_units='20',scrap_quantity='0',opening_wip='0',wip_item='order-wip',fg_item='product',completion_date='2026-09-30',costing=costing,closing_wip_cost='200',completed_cost='800');c['orders']=[o]
        common=dict(order_id=o['id'],checked_on=c['execution_date'])
        document(c,'bom',dict(**common,effective_from='2026-01-01',effective_to='2026-12-31',substitutions_approved=True,components=[dict(id='bom-component',component_id='component',standard_quantity_per_output='0.6',standard_price='9',maximum_good_output='100')]))
        document(c,'routing',dict(**common,actual_labour_hours='20',actual_driver_units='100',driver='machine_hours'))
        document(c,'capacity',dict(**common,normal_capacity='200',actual_driver_units='100',normal_capacity_memo='Synthetic controlled normal seasonal productive capacity incl planned maintenance',driver='machine_hours',pool_memo='Synthetic complete factory OH pool',reviewed_multi_period=True,pool_complete=True))
        document(c,'loss',dict(**common,reported_loss='0',loss_memo='Synthetic closed mass/yield source register',loss_explained=True,abnormal_excluded=True,abnormal_material_cost='0',net_component_usage={'component':'60'}))
        document(c,'completion-evidence',dict(**common,completed_quantity='80',closing_equivalent_units='20',homogeneous_equivalents_reviewed=True))
        for id,k,amount,extra in [('labour','direct_labour','200',dict(hours='20',rate='10')),('variable','variable_overhead','100',dict(driver_units='100')),('fixed','fixed_overhead','200',{})]:
            x=row(c,id,economic_id='cost-'+id,order_id='order-1',date='2026-06-30',kind=k,amount=amount,currency='USD',source_doc=id+'-source',allocation_memo='Synthetic evidenced factory actual-cost driver',**extra);c['costs'].append(x)
            document(c,x['source_doc'],dict(economic_id=x['economic_id'],order_id=x['order_id'],amount=amount,currency='USD',manufacturing=True,pool_complete=True,**extra))
        if costing=='standard':c['standards']=[row(c,'standards',order_id='order-1',effective_date='2026-01-01',review_memo='Synthetic current regular standard review',approximation_memo='Synthetic material actual deviation reviewed gross',output_quantity='100',current=True,material_deviation_reviewed=True,unsupported_revaluation=False,labour_hours_per_output='0.2',labour_rate='9',driver_units_per_output='1',variable_rate='0.9',fixed_rate='1',fixed_budget='200',disposition=dict(eligible_normal='90',abnormal_idle='100',gross_reviewed=True,inventory_cogs_reviewed=True,components=[dict(id=k,component=k,total=a,inventory=a if k!='fixed_volume' else '0',idle_expense=a if k=='fixed_volume' else '0') for k,a in [('material_price','60'),('material_usage','0'),('labour_rate','20'),('labour_efficiency','0'),('variable_spending','10'),('variable_efficiency','0'),('fixed_spending','0'),('fixed_volume','100')]]))]
        glvals=[('Raw materials','1000','400'),('Work in progress','0','200'),('Finished goods','0','600'),('Labour clearing','0','-200'),('Overhead clearing','0','-300'),('Unallocated overhead expense','0','100'),('Cost of goods sold','0','200')];cogs='200';closing='1200'
    else:
        item('goods','MERCH','10','100','15','225');move('receipt','goods','purchase','10','200')
        relief='75' if formula=='WEIGHTED_AVERAGE' else ('100' if formula=='LIFO' else '50');cc='225' if formula=='WEIGHTED_AVERAGE' else ('200' if formula=='LIFO' else '250');c['items'][0]['closing_cost']=cc
        move('sale','goods','sale','5',relief,date='2026-10-31',layer_ids=['goods-opening'])
        glvals=[('Merchandise','100',cc),('Acquisition clearing','0','-200'),('Cost of goods sold','0',relief)];cogs=relief;closing=cc
    if costing=='standard':glvals+=[('Manufacturing variance clearing','0','0')]+[('Manufacturing '+k+' variance','0','0') for k in ('material_price','material_usage','labour_rate','labour_efficiency','variable_spending','variable_efficiency','fixed_spending','fixed_volume')]
    c['gl']=[row(c,id,currency='USD',opening=op,closing=cl,statement=cl) for id,op,cl in glvals];c['gl_inventory']=[r['id'] for r in c['gl']]
    req=({'policy','formula','classes','carrying','valuation_losses','estimates'} if fw=='US_GAAP' else {'policy','formula','classes','carrying','write_down','pledged','reversal','reversal_circumstances'}|({'expense'} if fw!='UK_GAAP' else set()));requirements={x:'Synthetic controlled current '+x+' source conclusion' for x in req};document(c,'disclosures-source',requirements)
    c['disclosures']=row(c,'disclosures',source_doc='disclosures-source',checked_on=c['execution_date'],requirements=requirements,closing_inventory=closing,cogs=cogs,write_down='0',reversal='0')
    counts=[dict(id=i['id'],item=i['id'],location=i['location'],quantity=i['closing_quantity']) for i in c['items']];document(c,'count-source',counts);c['count']=row(c,'count',source_doc='count-source',records=counts)
    cutoff=[dict(id=m['id'],economic_id=m['economic_id'],ownership_supported=True,date_reviewed=True) for m in c['movements']];document(c,'cutoff-source',cutoff);c['cutoff']=row(c,'cutoff',source_doc='cutoff-source',records=cutoff)
    disclosure_support(c)
    return sources(c)

def ready(c=None,fw='IFRS',kind='manufacturing',costing='actual',formula='FIFO'):
    c=copy.deepcopy(c or case(fw,kind,costing,formula));refresh(c)
    claims,docs=canonical_knowledge(PACKAGES[PACKAGE][1],c['framework'],package=PACKAGE)
    c['knowledge_review']=dict(reviewer='Synthetic independent inventory knowledge reviewer',claim_ids=[x['claim_id'] for x in claims],documents=docs,applied_claim_ids=[x['claim_id'] for x in claims],selection_memo='Synthetic ordinary inventory manufacturing scope and framework decisions reviewed individually',public_caveats=['Controlled actual source facts and current framework-specific standards determine cost, capacity, ownership and valuation.'])
    c['reviewer_signoff']=dict(reviewer='Synthetic independent inventory accounting reviewer',approved=True,case_fingerprint=case_fingerprint(c));return c

def return_case(costing='actual'):
    c=case(costing=costing);m=c['movements'][0];m.update(quantity='70',amount='700');content(c,m['source_doc'])['quantity']='70'
    ret=row(c,'return',economic_id='economic-return',item='component',kind='return',quantity='10',amount='100',date='2026-07-30',currency='USD',unit='units',source_doc='return-source',sequence=2,order_id='order-1',original_issue='economic-issue',return_layer_id='component-opening')
    c['movements'].insert(1,ret)
    for n,m in enumerate(c['movements']):m['sequence']=n+1
    document(c,'return-source',dict(economic_id='economic-return',item='component',quantity='10',date='2026-07-30',ownership_supported=True,in_period=True))
    cutoff=[dict(id=m['id'],economic_id=m['economic_id'],ownership_supported=True,date_reviewed=True) for m in c['movements']];c['cutoff']['records']=cutoff;replace_doc(c,'cutoff-source',cutoff)
    return sources(c)

def valuation_case(fw='IFRS',reversal=False,formula='FIFO'):
    c=case(fw,'resale',formula=formula);i=c['items'][0];before=Decimal(i['closing_cost']);prior='50' if reversal else '0';selling='20' if reversal else '12';target=before+Decimal(prior) if reversal and fw!='US_GAAP' else (Decimal('180') if not reversal else before)
    if formula=='LIFO' and not reversal:target=Decimal('150')
    adjustment=target-before;i['closing_cost']=str(target)
    a=dict(item=i['id'],checked_on=c['execution_date'],current_market=True,completion_cost_complete=True,selling_cost_complete=True,obsolescence_reviewed=True,grouping='item',forecast_invented=False,expiry_reviewed=True,selling_price=selling,completion_cost='0',selling_cost='0',replacement_cost='10',normal_profit='3',carrying_cost_before_measurement=str(before),prior_write_down=prior,original_cost=str(before+Decimal(prior)),valuation_memo='Synthetic current controlled actual lower-cost estimate',recovery_evidence_memo='Synthetic independently reviewed actual recovery within original reduction',recovery_reviewed=True,forecast_used=False,forecast_checked_on=c['execution_date'],forecast_reviewed=True,expired=False,salvage_supported=False)
    content(c,i['measurement_doc'])['impairment_indicator']=True
    document(c,'valuation-source',a);c['valuation']=[row(c,'lower-cost',item=i['id'],source_doc='valuation-source',prior_write_down=prior,adjustment=str(adjustment))]
    c['gl'][0]['closing']=c['gl'][0]['statement']=str(target);c['gl'].append(row(c,'Inventory measurement expense',currency='USD',opening='0',closing=str(-adjustment),statement=str(-adjustment)));c['gl_inventory']=[r['id'] for r in c['gl']]
    c['disclosures'].update(closing_inventory=str(target),write_down=str(max(-adjustment,0)),reversal=str(max(adjustment,0)))
    disclosure_support(c)
    return sources(c)

def over_recovery_case(fw='IFRS'):
    c=case(fw,costing='standard');s=c['standards'][0];s.update(fixed_rate='3',fixed_budget='600');s['disposition']['eligible_normal']='-110';s['disposition']['components'][6].update(total='-400',inventory='-400');s['disposition']['components'][7].update(total='300',inventory='200',idle_expense='100')
    return sources(c)

def high_capacity_case():
    c=case();content(c,'capacity')['normal_capacity']='50';o=c['orders'][0];o.update(completed_cost='880',closing_wip_cost='220');c['movements'][1]['amount']='880';c['movements'][2]['amount']='220';c['items'][1]['closing_cost']='220';c['items'][2]['closing_cost']='660'
    for r in c['gl']:
        if r['id']=='Work in progress':r['closing']=r['statement']='220'
        elif r['id']=='Finished goods':r['closing']=r['statement']='660'
        elif r['id']=='Unallocated overhead expense':r['closing']=r['statement']='0'
        elif r['id']=='Overhead clearing':r['closing']=r['statement']='-300'
        elif r['id']=='Cost of goods sold':r['closing']=r['statement']='220'
    c['disclosures'].update(closing_inventory='1280',cogs='220');disclosure_support(c,other='0');return sources(c)


def disclosure_support(c,other=None):
    ds=c['disclosures'];classes=sorted({i['class'] for i in c['items']});accounts={'RM':'Raw materials','WIP':'Work in progress','FG':'Finished goods','MERCH':'Merchandise'}
    carrying={accounts[k]:str(sum((Decimal(i['closing_cost']) for i in c['items'] if i['class']==k),Decimal(0))) for k in classes}
    other=other if other is not None else str(sum((Decimal(g['closing'])-Decimal(g['opening']) for g in c['gl'] if g['id'] in {'Abnormal manufacturing expense','Unallocated overhead expense','Inventory count expense','Inventory disposal expense'}),Decimal(0)))
    data=dict(policy=dict(framework=c['framework'],edition=c['scope']['edition'],measurement_memo='Synthetic actual company cost/measurement policy reviewed'),formula=copy.deepcopy(c['accounting_policy']['formula_by_group']),classes=classes,carrying=carrying,expense=dict(cogs=ds['cogs'],manufacturing_other=other,write_down=ds['write_down'],reversal=ds['reversal']),write_down=ds['write_down'],valuation_losses=ds['write_down'],reversal=ds['reversal'],pledged=dict(amount='0',reviewed=True,evidence_memo='Synthetic actual collateral register none'),reversal_circumstances=dict(reviewed=True,evidence_memo='Synthetic current evidence of value recovery/no reversal'),estimates=dict(model='LCM' if any(i['formula']=='LIFO' for i in c['items']) else 'LCNRV',reviewed=True,evidence_memo='Synthetic actual current lower-cost estimation evidence'))
    ds['requirements']={k:data[k] for k in ds['requirements']};replace_doc(c,ds['source_doc'],ds['requirements']);return c

def count_case():
    c=case(kind='resale');i=c['items'][0];i.update(closing_quantity='14',closing_cost='240')
    m=row(c,'count-shortage',economic_id='economic-count-shortage',item='goods',kind='count',quantity='1',amount='10',date='2026-11-30',currency='USD',unit='units',source_doc='count-adjustment-source',sequence=3,layer_ids=['goods-opening']);c['movements'].append(m)
    document(c,m['source_doc'],dict(economic_id=m['economic_id'],item='goods',quantity='1',date=m['date'],ownership_supported=True,in_period=True))
    c['count']['records'][0]['quantity']='14';replace_doc(c,'count-source',c['count']['records']);c['cutoff']['records'].append(dict(id=m['id'],economic_id=m['economic_id'],ownership_supported=True,date_reviewed=True));replace_doc(c,'cutoff-source',c['cutoff']['records'])
    c['gl'][0]['closing']=c['gl'][0]['statement']='240';c['gl'].append(row(c,'Inventory count expense',currency='USD',opening='0',closing='10',statement='10'));c['gl_inventory']=[g['id'] for g in c['gl']];c['disclosures']['closing_inventory']='240';disclosure_support(c);return sources(c)

def location_case(location='Third-party warehouse'):
    c=case(kind='resale');c['items'][0]['location']=location;c['count']['records'][0]['location']=location;replace_doc(c,'count-source',c['count']['records']);content(c,'goods-rights')['rights_memo']='Synthetic actual title and external custodian/transport document confirms entity-owned goods at '+location;return sources(c)

def loss_case():
    c=case();c['orders'][0]['scrap_quantity']='1';content(c,'loss').update(reported_loss='1',loss_memo='Synthetic supplied normal process yield loss, BOM allowance includes normal waste');return sources(c)


def purchase_standard_case():
    c=case(kind='resale');content(c,'receipt-source').update(purchase_standard=True,standard_checked_on=c['execution_date'],standards_reviewed=True,standard_unit_cost='15',ppv_inventory_adjustment='50');c['gl'].append(row(c,'Purchase price variance',currency='USD',opening='0',closing='0',statement='0'));c['gl_inventory']=[g['id'] for g in c['gl']];return sources(c)


def grouped_standard_case():
    c=case(costing='standard');s=c['standards'][0];s.update(company_reporting_memo='Synthetic actual company four variance-account architecture with underlying nonnetted measurements retained',reporting_gross_adverse='190',reporting_gross_favorable='0')
    s['disposition']['components']=[dict(id=k,component=k,members=members,total=a,inventory=i,idle_expense=e) for k,members,a,i,e in [('material',['material_price','material_usage'],'60','60','0'),('labour',['labour_rate','labour_efficiency'],'20','20','0'),('variable',['variable_spending','variable_efficiency'],'10','10','0'),('fixed',['fixed_spending','fixed_volume'],'100','0','100')]]
    c['gl']=[g for g in c['gl'] if not any(g['id']=='Manufacturing '+k+' variance' for k in ('material_price','material_usage','labour_rate','labour_efficiency','variable_spending','variable_efficiency','fixed_spending','fixed_volume'))]
    c['gl'] += [row(c,'Manufacturing '+k+' variance',currency='USD',opening='0',closing='0',statement='0') for k in ('material','labour','variable','fixed')];c['gl_inventory']=[g['id'] for g in c['gl']];return sources(c)

def raw_context_case(fw='IFRS',recoverable=True):
    c=case(fw);i=c['items'][0];content(c,i['measurement_doc'])['impairment_indicator']=True
    method='finished_goods_recoverability' if fw in {'IFRS','AASB'} and recoverable else ('replacement_cost' if fw in {'IFRS','AASB'} else 'LCNRV')
    target='400' if fw in {'IFRS','AASB'} and recoverable else '320';adjustment='0' if target=='400' else '-80';i['closing_cost']=target
    fg=dict(item='product',component='component',checked_on=c['execution_date'],current_market=True,selling_price='15' if recoverable else '9',completion_cost='0',selling_cost='0',unit_cost='10',recovery_reviewed=True,cost_basis_memo='Synthetic completed factory order actual cost10 per controlled good unit',net_sales_estimate_memo='Synthetic current reviewed actual finished-goods market evidence')
    document(c,'fg-recovery-source',fg)
    a=dict(item='component',checked_on=c['execution_date'],current_market=True,completion_cost_complete=True,selling_cost_complete=True,obsolescence_reviewed=True,grouping='item',forecast_invented=False,expiry_reviewed=True,selling_price='8',completion_cost='0',selling_cost='0',carrying_cost_before_measurement='400',prior_write_down='0',original_cost='400',valuation_memo='Synthetic raw material decline/context assessment',recovery_evidence_memo='Synthetic actual completed finished-goods cost and selling support',recovery_reviewed=True,forecast_used=False,forecast_checked_on=c['execution_date'],forecast_reviewed=True,expired=False,salvage_supported=False,finished_goods_recoverable=recoverable,finished_goods_recovery_doc='fg-recovery-source',raw_measurement_method=method,raw_context_memo='Synthetic framework-specific raw lower-cost context independently reviewed',replacement_cost='8',replacement_cost_appropriate=True,framework_raw_method_reviewed=True)
    document(c,'raw-recovery-source',a);c['valuation']=[row(c,'raw-context',item='component',source_doc='raw-recovery-source',prior_write_down='0',adjustment=adjustment)]
    c['gl'][0]['closing']=c['gl'][0]['statement']=target;c['gl'].append(row(c,'Inventory measurement expense',currency='USD',opening='0',closing=str(-Decimal(adjustment)),statement=str(-Decimal(adjustment))));c['gl_inventory']=[g['id'] for g in c['gl']];c['disclosures'].update(closing_inventory=str(Decimal('800')+Decimal(target)),write_down=str(-Decimal(adjustment)));disclosure_support(c);return sources(c)
