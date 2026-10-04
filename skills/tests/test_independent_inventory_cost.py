"""Independent adversarial Inventory QA; synthetic test approval is not production approval."""
import copy
import json
import unittest
from decimal import Decimal
from unittest.mock import patch
from inventory_cases import case,ready,refresh,sources,content,replace_doc,row,document,PACKAGE,return_case,valuation_case,over_recovery_case,high_capacity_case,grouped_standard_case,purchase_standard_case,raw_context_case
from production import assess_case,to_public,serializable,case_fingerprint
from interfaces.public_output import ROUTES

MONEY={'opening_cost','closing_cost','cost','amount','opening','closing','statement','population_amount','rate','standard_price','opening_wip','closing_wip_cost','completed_cost','labour_rate','variable_rate','fixed_rate','fixed_budget','eligible_normal','abnormal_idle','closing_inventory','cogs','write_down','reversal','prior_write_down','adjustment','selling_price','completion_cost','selling_cost','total','inventory','idle_expense','carrying_cost_before_measurement','original_cost','replacement_cost','normal_profit','manufacturing_other','abnormal_material_cost','valuation_losses','standard_unit_cost','ppv_inventory_adjustment','reporting_gross_adverse','reporting_gross_favorable','unit_cost'}
def specimen(fw='IFRS',kind='manufacturing',costing='actual',formula='FIFO'):
    c=case(fw,kind,costing,formula)
    return scale_case(c)

def scale_case(c):
    fw=c['framework'];kind=c['case_id']
    seen=set()
    def scale(o):
        if isinstance(o,(dict,list)):
            if id(o) in seen:return
            seen.add(id(o))
        if isinstance(o,dict):
            for k,v in list(o.items()):
                if k=='carrying' and isinstance(v,dict):
                    for a,n in list(v.items()):
                        if isinstance(n,str):v[a]=str(Decimal(n)*Decimal('1.37'))
                elif k in MONEY and isinstance(v,str):
                    try:o[k]=str(Decimal(v)*Decimal('1.37'))
                    except Exception:pass
                else:scale(v)
        elif isinstance(o,list):
            for v in o:scale(v)
    scale(c);c['case_id']='Independent inventory source cost ×1.37 '+fw+' '+kind
    return sources(c)

def repair_disclosure_sources(c):
    d=c['disclosures'];req=d['requirements'];accounts={'RM':'Raw materials','WIP':'Work in progress','FG':'Finished goods','MERCH':'Merchandise'}
    req['carrying']={accounts[k]:str(sum(Decimal(i['closing_cost']) for i in c['items'] if i['class']==k)) for k in {i['class'] for i in c['items']}}
    req['classes']=sorted({i['class'] for i in c['items']})
    expense=sum((Decimal(g['closing'])-Decimal(g['opening']) for g in c['gl'] if g['id'] in {'Abnormal manufacturing expense','Unallocated overhead expense','Inventory count expense','Inventory disposal expense'}),Decimal(0))
    if 'expense' in req:req['expense']=dict(cogs=d['cogs'],manufacturing_other=str(expense),write_down=d['write_down'],reversal=d['reversal'])
    for k in ('write_down','valuation_losses','reversal'):
        if k in req:req[k]=d['write_down'] if k=='valuation_losses' else d[k]
    replace_doc(c,d['source_doc'],req);return c

def owner_case(package):
    from operational_cases import operational
    from additional_cases import certify,fx
    from financing_cases import case as payroll_case,ready as payroll_ready
    from production import execute
    if package in {'fixed-assets','accounts-payable'}:
        upstream=operational(package);upstream['functional_currency']='USD'
        for key in ('invoices','payments'):
            for r in upstream.get(key,[]):r['currency']='USD'
        upstream=certify(package,upstream)
    elif package=='employee-benefits-payroll':
        upstream=payroll_case(package);upstream['functional_currency']='USD';upstream=payroll_ready(package,c=upstream)
    else:
        upstream=fx();upstream['currency'].update(functional='USD',presentation='USD',ledger='USD');upstream['translation']['enabled']=False
        upstream['items'][0].update(id='inventory-purchase',type='historical_nonmonetary',settled_foreign='0',settlement_date=None,account='Inventory acquisition',memo='Independent controlled historical nonmonetary inventory purchase basis')
        upstream=certify(package,upstream)
    result=execute(package,upstream)
    c=specimen(kind='resale' if package=='foreign-currency' else 'manufacturing')
    path,owner_kind={'fixed-assets':(['depreciation'],'depreciation'),'employee-benefits-payroll':(['expense'],'labour'),'accounts-payable':(['invoices'],'ap'),'foreign-currency':(['transactions','inventory-purchase','initial'],'fx')}[package]
    value={'fixed-assets':Decimal('90000'),'employee-benefits-payroll':Decimal('10800'),'accounts-payable':Decimal('120'),'foreign-currency':Decimal('110')}[package]
    if package=='foreign-currency':
        target=c['movements'][0];target['amount']=str(value);content(c,target['source_doc'])['cost_components'][0]['amount']=str(value)
        closing=Decimal('137')+value-Decimal('68.5');c['items'][0]['closing_cost']=str(closing);c['gl'][0].update(closing=str(closing),statement=str(closing));c['gl'][1].update(closing=str(-value),statement=str(-value));c['disclosures']['closing_inventory']=str(closing)
    else:
        index={'employee-benefits-payroll':0,'accounts-payable':1,'fixed-assets':2}[package];target=c['costs'][index];target['amount']=str(value);b=content(c,target['source_doc']);b['amount']=str(value)
        if index==0:target['rate']=str(value/Decimal('20'));b['rate']=target['rate']
        material=Decimal('822');lab=Decimal(c['costs'][0]['amount']);variable=Decimal(c['costs'][1]['amount']);fixed=Decimal(c['costs'][2]['amount']);absorbed=fixed/2;total=material+lab+variable+absorbed;wip=total/5;fg=total*Decimal('.8');cogs=total/5
        c['orders'][0].update(closing_wip_cost=str(wip),completed_cost=str(fg));c['movements'][1]['amount']=str(fg);c['movements'][2]['amount']=str(cogs);c['items'][1]['closing_cost']=str(wip);c['items'][2]['closing_cost']=str(fg-cogs)
        changes={'Work in progress':wip,'Finished goods':fg-cogs,'Labour clearing':-lab,'Overhead clearing':-(variable+fixed),'Unallocated overhead expense':fixed-absorbed,'Cost of goods sold':cogs}
        for r in c['gl']:
            if r['id'] in changes:r.update(closing=str(changes[r['id']]),statement=str(changes[r['id']]))
        c['disclosures'].update(closing_inventory=str(Decimal('548')+wip+fg-cogs),cogs=str(cogs))
    target.update(owner_import='actual-'+package,owner_kind=owner_kind)
    b=content(c,target['source_doc']);b.update(amount=str(value),currency='USD',eligible_manufacturing=True,production_mapping_memo='Independent factory cell source allocation',cost_qualification_memo='Independent actual source conversion cost review')
    c['imports']=[row(c,'actual-'+package,package=package,case=upstream,result=result,mode='evidence_only')]
    c['owner_links']=[row(c,'link-'+package,owner_import='actual-'+package,result_path=path,economic_id=target['economic_id'],target_id=target['id'],amount=str(value),source_doc=target['source_doc'],source_field='amount')];c['owner_links_inventory']=[r['id'] for r in c['owner_links']]
    return sources(repair_disclosure_sources(c))

def agriculture_intake_case():
    from agriculture_cases import ready as agriculture_ready,case as agriculture_case
    from production import execute
    upstream=agriculture_ready(c=agriculture_case());result=execute('agriculture-biological-assets',upstream)
    c=specimen(kind='resale');i=c['items'][0];i.update(unit='kg',opening_quantity='0',opening_cost='0',opening_layers=[],closing_quantity='80',closing_cost='56')
    m=c['movements'][0];m.update(kind='harvest',quantity='100',amount='70',unit='kg',owner_import='actual-agriculture',owner_kind='harvest',date='2026-09-30')
    b=content(c,m['source_doc']);b.update(quantity='100',date=m['date'],amount='70',currency='USD',harvest_gain_duplicate=False,biological_remeasurement=False,eligible_manufacturing=True,production_mapping_memo='Independent actual harvest lot intake',cost_qualification_memo='Actual completed harvest owner basis retained exactly once');b.pop('cost_components',None)
    c['movements'][1].update(quantity='20',amount='14',unit='kg');b=content(c,c['movements'][1]['source_doc']);b['quantity']='20'
    c['imports']=[row(c,'actual-agriculture',package='agriculture-biological-assets',case=upstream,result=result,mode='evidence_only')]
    c['owner_links']=[row(c,'agriculture-link',owner_import='actual-agriculture',result_path=['harvest_entry'],economic_id=m['economic_id'],target_id=m['id'],amount='70',source_doc=m['source_doc'],source_field='amount')];c['owner_links_inventory']=['agriculture-link']
    c['gl']=[row(c,'Merchandise',currency='USD',opening='0',closing='56',statement='56'),row(c,'Cost of goods sold',currency='USD',opening='0',closing='14',statement='14')];c['gl_inventory']=[g['id'] for g in c['gl']];c['disclosures'].update(closing_inventory='56',cogs='14');c['count']['records'][0]['quantity']='80';replace_doc(c,'count-source',c['count']['records'])
    mapping=dict(movement_id=m['id'],owner_import='actual-agriculture',owner_account='Harvest inventory entry',account='Merchandise',amount='70')
    document(c,'retained-harvest',mapping);c['owner_gl_effects']=[row(c,'retained-harvest-effect',source_doc='retained-harvest',**mapping)];c['owner_gl_effects_inventory']=['retained-harvest-effect']
    return sources(repair_disclosure_sources(c))

class IndependentInventory(unittest.TestCase):
    def result(self,c,certify=True):return assess_case(PACKAGE,ready(c=c) if certify else c)
    def blocked(self,c):
        r=self.result(c);self.assertEqual('blocked',r['status'],r['conclusion']);return r
    def complete(self,c):
        r=self.result(c);self.assertEqual('complete',r['status'],r['conclusion']);return r
    def test_valid_four_frameworks_independent_manufacturing(self):
        for fw in ('IFRS','US_GAAP','UK_GAAP','AASB'):
            r=self.complete(specimen(fw));a=r['calculations']['order-1']
            for key,value in {'material':'822','direct_labour':'274','variable_overhead':'137','fixed_overhead':'274','absorbed_fixed':'137','under_recovery':'137','actual_eligible_total':'1370','completed_cost':'1096','closing_wip':'274'}.items():self.assertEqual(Decimal(value),a[key],key)
            self.assertEqual(Decimal('1644'),r['calculations']['closing_inventory']);self.assertEqual(Decimal('274'),r['calculations']['cogs'])
            for j in r['journal_entry_implications']:self.assertEqual(sum(x['amount'] for x in j if x['side']=='Dr'),sum(x['amount'] for x in j if x['side']=='Cr'))
    def test_valid_standard_gross_decomposition(self):
        r=self.complete(specimen(costing='standard'));v=r['calculations']['order-1']['variances'];self.assertEqual(Decimal('260.30'),sum(v.values()))
        for key,value in {'material_price':'82.2','material_usage':'0','labour_rate':'27.4','labour_efficiency':'0','variable_spending':'13.7','variable_efficiency':'0','fixed_spending':'0','fixed_volume':'137'}.items():self.assertEqual(Decimal(value),v[key])
    def test_valid_multilayer_fifo_and_weighted_average(self):
        for formula,closing,relief in [('FIFO','342.5','68.5'),('WEIGHTED_AVERAGE','308.25','102.75')]:
            r=self.complete(specimen(kind='resale',formula=formula));self.assertEqual(Decimal(closing),r['calculations']['closing_inventory']);self.assertEqual(Decimal(relief),r['calculations']['cogs'])
    def test_duplicate_item_physical_alias(self):
        c=specimen();c['items'][1]['physical_id']=c['items'][0]['physical_id'];self.blocked(sources(c))
    def test_duplicate_production_economic_identity(self):
        c=specimen();m=copy.deepcopy(c['movements'][0]);m['id']='alias-issue';c['movements'].append(m);self.blocked(sources(c))
    def test_duplicate_cost_economic_identity(self):
        c=specimen();x=copy.deepcopy(c['costs'][0]);x['id']='alias-payroll';c['costs'].append(x);self.blocked(sources(c))
    def test_duplicate_order_production_identity(self):
        c=specimen();o=copy.deepcopy(c['orders'][0]);o['id']='alias-order';c['orders'].append(o);self.blocked(sources(c))
    def test_opening_closing_bridges_unexplained_negative(self):
        for k,val in [('opening_quantity','0'),('closing_quantity','41'),('closing_cost','1'),('opening_cost','99')]:
            c=specimen();c['items'][0][k]=val;self.blocked(sources(c))
    def test_stock_gl_statement_and_cogs_mismatch(self):
        for which in ('stock','statement','cogs'):
            c=specimen()
            if which=='stock':c['gl'][0]['closing']='1'
            elif which=='statement':c['gl'][0]['statement']='1'
            else:c['disclosures']['cogs']='1'
            self.blocked(refresh(c))
    def test_nonfactory_and_incomplete_cost_pool(self):
        for key in ('manufacturing','pool_complete'):
            c=specimen();content(c,'labour-source')[key]=False;self.blocked(refresh(c))
    def test_wrong_labour_source_hours_and_rate(self):
        for key in ('hours','rate','amount'):
            c=specimen();content(c,'labour-source')[key]='999';self.blocked(refresh(c))
    def test_wrong_routing_hours_and_driver(self):
        for key in ('actual_labour_hours','actual_driver_units','driver'):
            c=specimen();content(c,'routing')[key]='999';self.blocked(refresh(c))
    def test_capacity_unknown_invented_or_wrong_denominator(self):
        for key,val in [('reviewed_multi_period',False),('pool_complete',False),('normal_capacity','0'),('actual_driver_units','200'),('driver','unknown'),('normal_capacity_memo','')]:
            c=specimen();content(c,'capacity')[key]=val;self.blocked(refresh(c))
    def test_source_wrong_currency_or_dimensions(self):
        for key,val in [('source_entity','Other factory'),('source_framework','UK_GAAP'),('source_period',['2025-01-01','2025-12-31'])]:
            c=specimen();c['costs'][0][key]=val;self.blocked(sources(c))
        c=specimen();c['costs'][0]['currency']='EUR';self.blocked(sources(c))
    def test_bom_and_loss_source_invalid(self):
        for doc,key,val in [('bom','substitutions_approved',False),('bom','effective_to','2025-12-31'),('loss','loss_explained',False),('loss','abnormal_excluded',False),('loss','reported_loss','1')]:
            c=specimen();content(c,doc)[key]=val;self.blocked(refresh(c))
    def test_completion_cutoff_and_equivalent_unit_contradiction(self):
        for key,val in [('completion_date','2027-01-01'),('completed_quantity','81'),('closing_equivalent_units','99')]:
            c=specimen();c['orders'][0][key]=val;self.blocked(sources(c))
    def test_stale_unreviewed_standards_and_revaluation(self):
        for key,val in [('current',False),('material_deviation_reviewed',False),('unsupported_revaluation',True),('effective_date','2025-01-01'),('review_memo',''),('approximation_memo',''),('output_quantity','101')]:
            c=specimen(costing='standard');c['standards'][0][key]=val;self.blocked(sources(c))
    def test_variance_disposition_and_denominator(self):
        for key,val in [('eligible_normal','0'),('abnormal_idle','0'),('gross_reviewed',False),('inventory_cogs_reviewed',False)]:
            c=specimen(costing='standard');c['standards'][0]['disposition'][key]=val;self.blocked(sources(c))
        c=specimen(costing='standard');c['standards'][0]['fixed_rate']='4';self.blocked(sources(c))
    def test_ownership_possession_not_title(self):
        for key,val in [('owned',False),('third_party_owned',True),('consigned_out_without_ownership',True),('rights_memo',''),('checked_on','2025-12-31')]:
            c=specimen();content(c,'component-rights')[key]=val;self.blocked(refresh(c))
    def test_economic_date_not_invoice_date(self):
        for key,val in [('date','2027-01-01'),('ownership_supported',False),('in_period',False)]:
            c=specimen();content(c,'issue-source')[key]=val;self.blocked(refresh(c))
    def test_count_and_cutoff_incomplete(self):
        for key,doc in [('count','count-source'),('cutoff','cutoff-source')]:
            c=specimen();c[key]['records'].pop();replace_doc(c,doc,c[key]['records']);self.blocked(refresh(c))
    def test_formula_policy_and_specific_interchangeability(self):
        c=specimen();c['accounting_policy']['formula_by_group']['materials']='WEIGHTED_AVERAGE';self.blocked(refresh(c))
        c=specimen();c['items'][0]['formula']='SPECIFIC_IDENTIFICATION';c['accounting_policy']['formula_by_group']['materials']='SPECIFIC_IDENTIFICATION';self.blocked(sources(c))
    def test_lifo_cannot_leak_across_frameworks(self):
        for fw in ('IFRS','AASB','UK_GAAP'):self.blocked(specimen(fw,formula='LIFO'))
    def test_disclosure_population_complete(self):
        c=specimen();c['disclosures']['requirements'].pop('pledged');replace_doc(c,'disclosures-source',c['disclosures']['requirements']);self.blocked(refresh(c))
    def test_specialist_and_borrowing_scope_fail_closed(self):
        for key in ('borrowing_capitalization','joint_products','retail_method','industry_exception','forecast_generation','external_posting','early_adoption'):
            c=specimen();c['scope'][key]=True;content(c,'scope-source')[key]=True;self.blocked(refresh(c))
    def test_malformed_units_money_quantities_currency(self):
        for val in ('NaN','Infinity',True,3.7,None,{},[]):
            c=specimen();c['items'][0]['opening_quantity']=val;self.blocked(sources(c))
        for key,val in [('unit','Private reviewer NAME_ABC'),('currency','EUR')]:
            c=specimen();c['items'][0][key]=val;self.blocked(sources(c))
    def test_stale_source_hash(self):
        c=ready(c=specimen());content(c,'bom')['components'][0]['standard_price']='99';self.assertEqual('blocked',self.result(c,False)['status'])
    def test_stale_knowledge_and_release_hash(self):
        for key in ('documents','claim_ids','applied_claim_ids'):
            c=ready(c=specimen());c['knowledge_review'][key]=[];self.assertEqual('blocked',self.result(c,False)['status'])
        c=ready(c=specimen());c['release_review']['payload_fingerprint']='0'*64;self.assertEqual('blocked',self.result(c,False)['status'])
    def test_stale_case_and_implementation_certification(self):
        c=ready(c=specimen());c['reviewer_signoff']['case_fingerprint']='stale';self.assertEqual('partial',self.result(c,False)['status'])
        c=ready(c=specimen())
        with patch('production.case_fingerprint',return_value='changed-executable-fingerprint'):self.assertEqual('partial',self.result(c,False)['status'])
    def test_public_private_source_all_seven_routes(self):
        r=self.complete(specimen());r['facts_used']['private_reviewer']='PRIVATE_NAME_927';r['evidence'][0].update(source_note='Source: ChatGPT training data',approval_track='TRAINING_DATA_CHECKED',approval_review={'reviewer':'PRIVATE_NAME_927'})
        for route in ROUTES:
            output=json.dumps(to_public(r,route),default=serializable)
            for secret in ('PRIVATE_NAME_927','Source:','source_note','approval_track','case_fingerprint','sha256','evidence_status','audit_required'):self.assertNotIn(secret,output)
    def test_duplicate_bom_component_under_alias(self):
        c=specimen();b=copy.deepcopy(content(c,'bom')['components'][0]);b['id']='component-alias';content(c,'bom')['components'].append(b);self.blocked(refresh(c))
    def test_duplicate_count_or_cutoff_economic_population(self):
        for key,doc in [('count','count-source'),('cutoff','cutoff-source')]:
            c=specimen();r=copy.deepcopy(c[key]['records'][0]);r['id']='alias';c[key]['records'].append(r);replace_doc(c,doc,c[key]['records']);self.blocked(refresh(c))
    def test_actual_fixed_assets_payroll_ap_fx_owner_consumption(self):
        for package in ('fixed-assets','employee-benefits-payroll','accounts-payable','foreign-currency'):
            r=self.complete(owner_case(package));self.assertEqual(Decimal({'fixed-assets':'37534.4','employee-benefits-payroll':'10064.8','accounts-payable':'1630.4','foreign-currency':'178.5'}[package]),r['calculations']['closing_inventory'])
    def test_owner_wrong_metric_not_cost(self):
        for package,path in [('fixed-assets',['closing_cost']),('employee-benefits-payroll',['closing_liability']),('accounts-payable',['closing_ap']),('foreign-currency',['monetary_fx_profit'])]:
            c=owner_case(package);c['owner_links'][0]['result_path']=path;self.blocked(refresh(c))
    def test_owner_stale_entity_period_duplicate_and_unbound(self):
        for key,val in [('entity','Other factory'),('framework','US_GAAP'),('reporting_period','2025-12-31')]:
            c=owner_case('employee-benefits-payroll');c['imports'][0]['case'][key]=val;self.blocked(refresh(c))
        c=owner_case('fixed-assets');c['imports'][0]['result']['calculations']['depreciation']='1';self.blocked(refresh(c))
        c=owner_case('accounts-payable');x=copy.deepcopy(c['owner_links'][0]);x['id']='duplicate-link';c['owner_links'].append(x);c['owner_links_inventory'].append(x['id']);self.blocked(refresh(c))
    def test_owner_qualification_and_numeric_source_binding(self):
        for key,val in [('eligible_manufacturing',False),('amount','1'),('currency','EUR'),('production_mapping_memo',''),('cost_qualification_memo','')]:
            c=owner_case('fixed-assets');content(c,c['owner_links'][0]['source_doc'])[key]=val;self.blocked(refresh(c))
    def test_valid_net_bom_return_actual_and_standard(self):
        for costing in ('actual','standard'):
            r=self.complete(scale_case(return_case(costing)));self.assertEqual(Decimal('822'),r['calculations']['order-1']['material']);self.assertEqual(Decimal('1644'),r['calculations']['closing_inventory'])
    def test_valid_under_over_and_high_capacity_recovery(self):
        r=self.complete(scale_case(over_recovery_case()));a=r['calculations']['order-1'];self.assertEqual(Decimal('-137'),a['standard_recovery']);self.assertEqual(Decimal('137'),a['under_recovery']);self.assertEqual(Decimal('-150.7'),a['actual_eligible_total']-a['standard_total'])
        r=self.complete(scale_case(high_capacity_case()));a=r['calculations']['order-1'];self.assertEqual(Decimal('274'),a['absorbed_fixed']);self.assertEqual(0,a['under_recovery']);self.assertEqual(Decimal('1753.6'),r['calculations']['closing_inventory'])
    def test_valid_nrv_write_down_reversals_and_us_lcm(self):
        for fw in ('IFRS','UK_GAAP','AASB','US_GAAP'):
            r=self.complete(scale_case(valuation_case(fw)));self.assertEqual(Decimal('246.6'),r['calculations']['closing_inventory']);self.assertEqual(Decimal('95.9'),r['calculations']['write_down'])
            r=self.complete(scale_case(valuation_case(fw,True)));self.assertEqual(Decimal('0' if fw=='US_GAAP' else '68.5'),r['calculations']['reversal'])
        r=self.complete(scale_case(valuation_case('US_GAAP',formula='LIFO')));self.assertEqual(Decimal('205.5'),r['calculations']['closing_inventory'])
    def test_measurement_stale_omitted_cost_grouping_sign(self):
        for key,val in [('checked_on','2025-12-31'),('current_market',False),('completion_cost_complete',False),('selling_cost_complete',False),('obsolescence_reviewed',False),('grouping','portfolio'),('forecast_invented',True),('expiry_reviewed',False)]:
            c=valuation_case();content(c,'valuation-source')[key]=val;self.blocked(refresh(c))
        for key in ('completion_cost','selling_cost'):
            c=valuation_case();content(c,'valuation-source').pop(key);self.blocked(refresh(c))
        c=valuation_case();c['valuation'][0]['adjustment']='70';self.blocked(sources(c))
    def test_duplicate_write_down_measurement_same_item(self):
        c=valuation_case();v=copy.deepcopy(c['valuation'][0]);v.update(id='valuation-alias',adjustment='0');c['valuation'].append(v);self.blocked(sources(c))
    def test_unbound_prior_write_down_cannot_create_reversal(self):
        c=valuation_case(reversal=True);c['valuation'][0]['prior_write_down']='500';c['valuation'][0]['adjustment']='50';self.blocked(sources(c))
    def test_scrap_output_yield_and_unreported_loss(self):
        c=specimen();content(c,'bom')['components'][0]['maximum_good_output']='99';self.blocked(refresh(c))
        c=specimen();content(c,'loss')['net_component_usage']['component']='59';self.blocked(refresh(c))
        c=specimen();c['orders'][0]['scrap_quantity']='1';self.blocked(sources(c))
    def test_variance_components_duplicated_mislabeled_sign_and_netting(self):
        for mode in ('duplicate','missing','mislabeled','sign','net'):
            c=specimen(costing='standard');a=c['standards'][0]['disposition']['components']
            if mode=='duplicate':r=copy.deepcopy(a[0]);r['id']='ppv-alias';a.append(r)
            elif mode=='missing':a.pop(1)
            elif mode=='mislabeled':a[0]['component']='yield'
            elif mode=='sign':a[0]['total']='-82.2'
            else:a[0].update(inventory='0',idle_expense=a[0]['total'])
            self.blocked(sources(c))
    def test_returns_cannot_double_issue_or_cross_order(self):
        for key,val in [('original_issue','missing-issue'),('order_id','missing-order'),('quantity','80'),('amount','1')]:
            c=return_case();c['movements'][1][key]=val;self.blocked(sources(c))
    def test_stale_edition_entity_tier_and_period(self):
        for fw in ('IFRS','US_GAAP','UK_GAAP','AASB'):
            c=specimen(fw);c['scope']['edition']='superseded';content(c,'scope-source')['edition']='superseded';self.blocked(refresh(c))
        c=specimen('AASB');c['reporting_tier']=2;self.blocked(refresh(c))
        c=specimen();c['reporting_period']='2027-12-31';self.blocked(refresh(c))
    def test_nonfinite_cost_and_mixed_gl_currency(self):
        for key,val in [('amount','Infinity'),('rate','NaN'),('hours',True)]:
            c=specimen();c['costs'][0][key]=val;self.blocked(sources(c))
        c=specimen();c['gl'][0]['currency']='EUR';self.blocked(refresh(c))
    def test_same_actual_payroll_source_under_distinct_case_alias(self):
        from financing_cases import ready as payroll_ready
        from production import execute
        c=owner_case('employee-benefits-payroll');imp=copy.deepcopy(c['imports'][0]);imp['id']='payroll-result-alias';imp['case']['case_id']='New name same economic payroll source';imp['case']=payroll_ready('employee-benefits-payroll',c=imp['case']);imp['result']=execute('employee-benefits-payroll',imp['case']);c['imports'].append(imp)
        x=copy.deepcopy(c['costs'][0]);x.update(id='labour-source-alias',economic_id='cost-labour-alias',owner_import=imp['id'],source_doc='labour-doc-alias');c['costs'].append(x)
        b=copy.deepcopy(content(c,'labour-source'));b['economic_id']=x['economic_id'];document(c,x['source_doc'],b)
        link=copy.deepcopy(c['owner_links'][0]);link.update(id='alias-link',owner_import=imp['id'],economic_id=x['economic_id'],target_id=x['id'],source_doc=x['source_doc']);c['owner_links'].append(link);c['owner_links_inventory'].append(link['id'])
        content(c,'routing')['actual_labour_hours']='40';c['orders'][0].update(closing_wip_cost='4539.2',completed_cost='18156.8');c['movements'][1]['amount']='18156.8';c['movements'][2]['amount']='4539.2';c['items'][1]['closing_cost']='4539.2';c['items'][2]['closing_cost']='13617.6'
        updates={'Work in progress':'4539.2','Finished goods':'13617.6','Labour clearing':'-21600','Cost of goods sold':'4539.2'}
        for g in c['gl']:
            if g['id'] in updates:g['closing']=g['statement']=updates[g['id']]
        c['disclosures'].update(closing_inventory='18704.8',cogs='4539.2');self.blocked(sources(c))
    def test_expiry_discontinuation_stale_forecast_population(self):
        for key,val in [('impairment_indicator',True),('expired',True),('discontinued',True),('population_reviewed',False),('estimate_memo',''),('demand_evidence_memo',''),('ageing_evidence_memo','')]:
            c=specimen();content(c,'component-measurement')[key]=val;self.blocked(refresh(c))
        c=specimen();a=content(c,'component-measurement');a.update(forecast_used=True,forecast_checked_on='2025-12-31');self.blocked(refresh(c))
        c=valuation_case();a=content(c,'valuation-source');a.update(forecast_used=True,forecast_checked_on='2025-12-31');self.blocked(refresh(c))
        c=valuation_case();content(c,'valuation-source').update(expired=True,salvage_supported=False);self.blocked(refresh(c))
    def test_abnormal_material_loss_cannot_remain_in_inventory(self):
        c=specimen();content(c,'loss')['abnormal_material_cost']='137';self.blocked(refresh(c))
    def test_valid_actual_agriculture_harvest_once(self):
        r=self.complete(agriculture_intake_case());self.assertEqual(Decimal('56'),r['calculations']['closing_inventory']);self.assertEqual(Decimal('14'),r['calculations']['cogs']);self.assertEqual(1,len(r['journal_entry_implications']))
    def test_agriculture_stale_duplicate_wrong_owner_and_biology(self):
        for key,val in [('harvest_gain_duplicate',True),('biological_remeasurement',True)]:
            c=agriculture_intake_case();content(c,c['movements'][0]['source_doc'])[key]=val;self.blocked(refresh(c))
        for key,val in [('entity','Other farm'),('framework','AASB'),('reporting_period','2025-12-31')]:
            c=agriculture_intake_case();c['imports'][0]['case'][key]=val;self.blocked(refresh(c))
        c=agriculture_intake_case();c['imports'][0]['result']['calculations']['harvest_entry']='999';self.blocked(refresh(c))
        c=agriculture_intake_case();m=copy.deepcopy(c['movements'][0]);m['id']='alias-harvest';c['movements'].insert(1,m);self.blocked(sources(c))
        c=agriculture_intake_case();c['owner_links'][0]['result_path']=['biological_measurement_gain'];self.blocked(refresh(c))
    def test_post_harvest_is_inventory_not_biological_remeasurement(self):
        c=agriculture_intake_case();c['scope']['industry_exception']=True;content(c,'scope-source')['industry_exception']=True;self.blocked(refresh(c))
    def test_framework_entity_namespace_source_restriction(self):
        for value in ('IFRS_for_SMEs','UK1A','Tier2','ASC905_producer'):
            c=specimen();c['scope']['entity_scope']=value;content(c,'scope-source')['entity_scope']=value;self.blocked(refresh(c))
    def test_disclosure_carrying_classes_formula_contradictions(self):
        for key,value in [('formula','Unsupported LIFO in ordinary IFRS'),('classes','Only merchandise; exclude raw materials WIP finished goods'),('carrying','Inventory carrying amount 999999 unsupported'),('pledged','No pledge source but asserted nil')]:
            c=specimen();c['disclosures']['requirements'][key]=value;replace_doc(c,'disclosures-source',c['disclosures']['requirements']);self.blocked(refresh(c))
    def test_valid_actual_usage_differs_from_bom_standard(self):
        c=case(costing='standard');content(c,'bom')['components'][0]['standard_quantity_per_output']='0.5';d=c['standards'][0]['disposition'];d['eligible_normal']='180';d['components'][1].update(total='90',inventory='90');r=self.complete(scale_case(sources(c)));self.assertEqual(Decimal('123.3'),r['calculations']['order-1']['variances']['material_usage']);self.assertEqual(Decimal('822'),r['calculations']['order-1']['material'])
    def test_valid_job_batch_process_source_dimensions(self):
        for architecture in ('job','batch','process'):
            c=specimen();c['orders'][0]['architecture']=architecture;r=self.complete(sources(c));self.assertEqual(Decimal('1644'),r['calculations']['closing_inventory'])
    def test_valid_normal_scrap_source_and_abnormal_material_expense(self):
        c=specimen();c['orders'][0]['scrap_quantity']='5';content(c,'loss')['reported_loss']='5';r=self.complete(sources(c));self.assertEqual(Decimal('1370'),r['calculations']['order-1']['actual_eligible_total'])
        c=specimen();content(c,'loss')['abnormal_material_cost']='137';c['orders'][0].update(closing_wip_cost='246.6',completed_cost='986.4');c['items'][1]['closing_cost']='246.6';c['items'][2]['closing_cost']='739.8';c['movements'][1]['amount']='986.4';c['movements'][2]['amount']='246.6'
        for g in c['gl']:
            if g['id']=='Work in progress':g['closing']=g['statement']='246.6'
            elif g['id']=='Finished goods':g['closing']=g['statement']='739.8'
            elif g['id']=='Cost of goods sold':g['closing']=g['statement']='246.6'
        c['gl'].append(row(c,'Abnormal manufacturing expense',currency='USD',opening='0',closing='137',statement='137'));c['gl_inventory'].append('Abnormal manufacturing expense');c['disclosures'].update(closing_inventory='1534.4',cogs='246.6')
        r=self.complete(sources(repair_disclosure_sources(c)));self.assertEqual(Decimal('274'),r['calculations']['manufacturing_expense']);self.assertEqual(Decimal('1233'),r['calculations']['order-1']['actual_eligible_total'])
    def test_positive_completion_duplicate_alias_even_reconciled(self):
        c=specimen();m=copy.deepcopy(c['movements'][1]);m.update(id='second-completion',economic_id='different-completion-alias',sequence=99,source_doc='second-completion-source');document(c,m['source_doc'],dict(economic_id=m['economic_id'],item=m['item'],quantity=m['quantity'],date=m['date'],ownership_supported=True,in_period=True));c['movements'].insert(2,m);self.blocked(sources(c))
    def test_opening_layers_duplicate_alias_and_wrong_chronology(self):
        c=specimen();a=c['items'][0]['opening_layers'];x=copy.deepcopy(a[0]);x['id']='alias-layer';a.append(x);self.blocked(sources(c))
        c=specimen();c['items'][0]['opening_layers'][0]['date']='2027-01-01';self.blocked(sources(c))
        c=specimen();c['movements'][0]['sequence']=True;self.blocked(sources(c))
    def test_single_claim_selection_cannot_omit_manufacturing_knowledge(self):
        c=ready(c=specimen());c['knowledge_review']['applied_claim_ids']=c['knowledge_review']['applied_claim_ids'][:1];c['reviewer_signoff']['case_fingerprint']=case_fingerprint(c);self.assertEqual('blocked',self.result(c,False)['status'])
    def test_iqa10_return_restores_original_fifo_position(self):
        c=return_case();purchase=row(c,'new-rm-purchase',economic_id='new-rm-economic',item='component',kind='purchase',quantity='10',amount='200',date='2026-07-01',currency='USD',unit='units',source_doc='new-rm-source',sequence=2)
        document(c,'new-rm-source',dict(economic_id=purchase['economic_id'],item='component',quantity='10',date=purchase['date'],ownership_supported=True,in_period=True,cost_components=[dict(id='price-new',economic_id='new-price-identity',kind='price',amount='200')]))
        issue=row(c,'second-issue',economic_id='new-second-issue',item='component',kind='issue',quantity='40',amount='400',date='2026-08-30',currency='USD',unit='units',source_doc='second-issue-source',sequence=4,order_id='order-1')
        document(c,'second-issue-source',dict(economic_id=issue['economic_id'],item='component',quantity='40',date=issue['date'],ownership_supported=True,in_period=True))
        c['movements'].insert(1,purchase);c['movements'].insert(3,issue)
        for n,m in enumerate(c['movements']):m['sequence']=n+1
        content(c,'loss')['net_component_usage']['component']='100';c['orders'][0].update(closing_wip_cost='280',completed_cost='1120');c['movements'][-2]['amount']='1120';c['movements'][-1]['amount']='280';c['items'][0].update(closing_quantity='10',closing_cost='200');c['items'][1]['closing_cost']='280';c['items'][2]['closing_cost']='840'
        changes={'Raw materials':'200','Work in progress':'280','Finished goods':'840','Cost of goods sold':'280'}
        for g in c['gl']:
            if g['id'] in changes:g['closing']=g['statement']=changes[g['id']]
        c['gl'].append(row(c,'Acquisition clearing',currency='USD',opening='0',closing='-200',statement='-200'));c['gl_inventory'].append('Acquisition clearing');c['disclosures'].update(closing_inventory='1320',cogs='280')
        c['count']['records'][0]['quantity']='10';replace_doc(c,'count-source',c['count']['records']);c['cutoff']['records']=[dict(id=m['id'],economic_id=m['economic_id'],ownership_supported=True,date_reviewed=True) for m in c['movements']];replace_doc(c,'cutoff-source',c['cutoff']['records'])
        r=self.complete(sources(repair_disclosure_sources(c)));self.assertEqual(Decimal('1000'),r['calculations']['order-1']['material']);self.assertEqual(Decimal('1320'),r['calculations']['closing_inventory'])
    def test_valid_distinct_labour_rate_efficiency_variable_fixed_variances(self):
        c=case(costing='standard');s=c['standards'][0];s.update(labour_hours_per_output='0.18',driver_units_per_output='0.8');d=s['disposition'];d['eligible_normal']='146';d['components'][3].update(total='18',inventory='18');d['components'][5].update(total='18',inventory='18');d['components'][7].update(total='120',inventory='20',idle_expense='100')
        r=self.complete(scale_case(sources(c)));v=r['calculations']['order-1']['variances'];self.assertEqual(Decimal('27.4'),v['labour_rate']);self.assertEqual(Decimal('24.66'),v['labour_efficiency']);self.assertEqual(Decimal('24.66'),v['variable_efficiency']);self.assertEqual(Decimal('164.4'),v['fixed_volume']);self.assertEqual(Decimal('1644'),r['calculations']['closing_inventory'])
    def test_valid_multilayer_issue_returns_exact_original_cost(self):
        for returned_layer,return_cost,material,rm,wip,completed,cogs,fg,total in [('component-opening','100','800','700','240','960','240','720','1660'),('component-expensive','200','700','800','220','880','220','660','1680')]:
            c=return_case();c['items'][0].update(opening_cost='1500',closing_cost=rm);c['items'][0]['opening_layers']=[dict(id='component-opening',economic_id='old-cheap-layer',quantity='50',cost='500',date='2025-11-30'),dict(id='component-expensive',economic_id='old-expensive-layer',quantity='50',cost='1000',date='2025-12-31')];c['movements'][0]['amount']='900';c['movements'][1].update(amount=return_cost,return_layer_id=returned_layer);c['movements'][2]['amount']=completed;c['movements'][3]['amount']=cogs;c['orders'][0].update(closing_wip_cost=wip,completed_cost=completed);c['items'][1]['closing_cost']=wip;c['items'][2]['closing_cost']=fg
            for g in c['gl']:
                if g['id']=='Raw materials':g.update(opening='1500',closing=rm,statement=rm)
                elif g['id']=='Work in progress':g['closing']=g['statement']=wip
                elif g['id']=='Finished goods':g['closing']=g['statement']=fg
                elif g['id']=='Cost of goods sold':g['closing']=g['statement']=cogs
            c['disclosures'].update(closing_inventory=total,cogs=cogs);r=self.complete(sources(repair_disclosure_sources(c)));self.assertEqual(Decimal(material),r['calculations']['order-1']['material']);self.assertEqual(Decimal(total),r['calculations']['closing_inventory'])
    def test_mixed_layer_return_unknown_layer_or_unsupported_blended_cost(self):
        for key,val in [('return_layer_id','unknown-source-layer'),('amount','125'),('quantity','71')]:
            c=return_case();c['movements'][1][key]=val;self.blocked(sources(c))
    def test_valid_count_adjustment_and_disposal_expense_not_revenue(self):
        for kind,account in [('count','Inventory count expense'),('writeoff','Inventory disposal expense')]:
            c=specimen(kind='resale');c['movements'][1]['kind']=kind;g=c['gl'][-1];g['id']=account;c['gl_inventory']=[g['id'] for g in c['gl']];c['disclosures']['cogs']='0';r=self.complete(sources(repair_disclosure_sources(c)));self.assertEqual(Decimal('342.5'),r['calculations']['closing_inventory']);self.assertEqual(0,r['calculations']['cogs']);self.assertEqual(Decimal('68.5'),r['calculations']['manufacturing_expense'])
    def test_owned_goods_in_transit_and_third_party_custody(self):
        for location in ('Independent carrier goods in transit','Independent supplier custody owned materials','Independent third-party warehouse'):
            c=specimen(kind='resale');c['items'][0]['location']=location;c['count']['records'][0]['location']=location;replace_doc(c,'count-source',c['count']['records']);r=self.complete(sources(c));self.assertEqual(Decimal('342.5'),r['calculations']['closing_inventory'])
    def test_downstream_handoff_interfaces_exact_inventory_owned_facts(self):
        r=self.complete(specimen());h=r['calculations']['owner_handoffs'];self.assertEqual({'financial_statements':Decimal('1644'),'revenue_cogs':Decimal('274'),'disclosure_inventory':Decimal('1644'),'systems_item_count':3,'controls_movement_count':3},h)
        self.assertEqual(Decimal('1644'),sum(r['calculations']['inventory_by_class'].values()));self.assertEqual(Decimal('1644'),r['calculations']['opening_inventory']+r['calculations']['retained_owner_intake']+r['calculations']['inventory_own_movement'])
        r=self.complete(agriculture_intake_case());a=r['calculations'];self.assertEqual(0,a['opening_inventory']);self.assertEqual(Decimal('70'),a['retained_owner_intake']);self.assertEqual(Decimal('-14'),a['inventory_own_movement']);self.assertEqual(Decimal('56'),a['owner_handoffs']['financial_statements'])
    def test_agriculture_retained_original_gl_effect_missing_or_duplicated(self):
        c=agriculture_intake_case();c['owner_gl_effects']=[];c['owner_gl_effects_inventory']=[];self.blocked(refresh(c))
        c=agriculture_intake_case();r=copy.deepcopy(c['owner_gl_effects'][0]);r['id']='same-retained-alias';c['owner_gl_effects'].append(r);c['owner_gl_effects_inventory'].append(r['id']);self.blocked(refresh(c))
        c=agriculture_intake_case();c['owner_gl_effects'][0]['amount']='140';self.blocked(refresh(c))
    def test_valid_company_grouped_standard_architecture_adverse_favorable(self):
        r=self.complete(scale_case(grouped_standard_case()));self.assertEqual(Decimal('1644'),r['calculations']['closing_inventory'])
        c=grouped_standard_case();s=c['standards'][0];s.update(fixed_rate='3',fixed_budget='600',reporting_gross_adverse='390',reporting_gross_favorable='-400');s['disposition']['eligible_normal']='-110';s['disposition']['components'][3].update(total='-100',inventory='-200',idle_expense='100');r=self.complete(scale_case(sources(c)));self.assertEqual(Decimal('-137'),r['calculations']['order-1']['standard_recovery']);self.assertEqual(Decimal('1644'),r['calculations']['closing_inventory'])
    def test_grouped_variance_duplicate_unsupported_group_and_netting(self):
        for mode in ('duplicate','unsupported','netted','gross_favorable_omitted','source_memo_absent'):
            c=grouped_standard_case();s=c['standards'][0]
            if mode=='duplicate':s['disposition']['components'][0]['members'].append('labour_rate')
            elif mode=='unsupported':s['disposition']['components'][0]['members'].append('invented_yield_split')
            elif mode=='netted':s['reporting_gross_adverse']='90'
            elif mode=='gross_favorable_omitted':s.pop('reporting_gross_favorable')
            else:s['company_reporting_memo']=''
            self.blocked(sources(c))
    def test_valid_purchase_standard_ppv_trace_once(self):
        r=self.complete(scale_case(purchase_standard_case()));self.assertEqual(Decimal('342.5'),r['calculations']['closing_inventory']);self.assertEqual(Decimal('68.5'),r['calculations']['cogs']);j=r['journal_entry_implications'];self.assertTrue(any(x['account']=='Purchase price variance' for e in j for x in e))
    def test_ppv_duplicate_stale_unbound_or_overlap_manufacturing(self):
        for key,val in [('standard_checked_on','2025-12-31'),('standards_reviewed',False),('ppv_inventory_adjustment','1'),('standard_unit_cost','99')]:
            c=purchase_standard_case();content(c,'receipt-source')[key]=val;self.blocked(refresh(c))
        c=specimen();content(c,'issue-source').update(purchase_standard=True,standard_unit_cost='1',ppv_inventory_adjustment='100');c['movements'][0]['kind']='purchase';self.blocked(sources(c))
    def test_typed_disclosure_actual_values_contradict_reconciled_results(self):
        for key in ('formula','classes','carrying','policy','expense','pledged','reversal_circumstances'):
            c=specimen();req=c['disclosures']['requirements']
            if key=='formula':req[key]['materials']='LIFO'
            elif key=='classes':req[key]=['MERCH']
            elif key=='carrying':req[key]['Raw materials']='99999'
            elif key=='policy':req[key]['framework']='US_GAAP'
            elif key=='expense':req[key]['manufacturing_other']='0'
            elif key=='pledged':req[key]['amount']='99999'
            else:req[key]['reviewed']=False
            replace_doc(c,'disclosures-source',req);self.blocked(refresh(c))
    def test_unowned_external_action_not_complete_accounting(self):
        for action in ('erp_posting','audit_opinion','forecast','autonomous_standard_setting'):
            c=specimen();c['requested_action']=action;self.blocked(refresh(c))
    def test_zero_realizable_value_and_us_reversal_cannot_cross_framework(self):
        for fw in ('IFRS','US_GAAP'):
            c=valuation_case(fw);a=content(c,'valuation-source');a.update(selling_price='0',completion_cost='0',selling_cost='0');c['valuation'][0]['adjustment']='-250';c['items'][0]['closing_cost']='0';c['gl'][0]['closing']=c['gl'][0]['statement']='0';c['gl'][-1]['closing']=c['gl'][-1]['statement']='250';c['disclosures'].update(closing_inventory='0',write_down='250');r=self.complete(sources(repair_disclosure_sources(c)));self.assertEqual(0,r['calculations']['closing_inventory']);self.assertEqual(Decimal('250'),r['calculations']['write_down'])
        c=valuation_case('US_GAAP',True);c['valuation'][0]['adjustment']='50';c['items'][0]['closing_cost']='300';c['gl'][0]['closing']=c['gl'][0]['statement']='300';c['gl'][-1]['closing']=c['gl'][-1]['statement']='-50';c['disclosures'].update(closing_inventory='300',reversal='50');self.blocked(sources(repair_disclosure_sources(c)))
    def test_balanced_class_transfer_eliminates_entity_inventory_movement(self):
        c=specimen(kind='resale');i=copy.deepcopy(c['items'][0]);i.update(id='second-location-stock',physical_id='distinct-controlled-transferred-lot',location='Second controlled warehouse',opening_quantity='0',opening_cost='0',opening_layers=[],closing_quantity='5',closing_cost='68.5',ownership_doc='second-location-rights',measurement_doc='second-location-measurement');c['items'].append(i);c['items'][0].update(closing_quantity='10',closing_cost='274')
        b=copy.deepcopy(content(c,'goods-rights'));b['item_id']=i['id'];b['ownership_event_id']='independent-title-second-lot';document(c,i['ownership_doc'],b);b=copy.deepcopy(content(c,'goods-measurement'));b['item']=i['id'];document(c,i['measurement_doc'],b)
        m=row(c,'internal-transfer',economic_id='unique-internal-transfer',item='goods',destination_item=i['id'],kind='transfer',quantity='5',amount='68.5',date='2026-11-30',currency='USD',unit='units',source_doc='internal-transfer-doc',sequence=3);c['movements'].append(m);document(c,m['source_doc'],dict(economic_id=m['economic_id'],item=m['item'],quantity='5',date=m['date'],ownership_supported=True,in_period=True));c['count']['records'][0]['quantity']='10';c['count']['records'].append(dict(id=i['id'],item=i['id'],location=i['location'],quantity='5'));replace_doc(c,'count-source',c['count']['records']);c['cutoff']['records'].append(dict(id=m['id'],economic_id=m['economic_id'],ownership_supported=True,date_reviewed=True));replace_doc(c,'cutoff-source',c['cutoff']['records']);r=self.complete(sources(repair_disclosure_sources(c)));self.assertEqual(Decimal('342.5'),r['calculations']['closing_inventory']);self.assertEqual(Decimal('68.5'),r['calculations']['cogs'])
    def test_internal_transfer_wrong_location_or_duplicate_economic_event(self):
        c=specimen();c['count']['records'][0]['location']='Omitted actual factory';replace_doc(c,'count-source',c['count']['records']);self.blocked(refresh(c))
        c=specimen();c['movements'][0]['kind']='transfer';c['movements'][0]['destination_item']='order-wip';self.blocked(sources(c))
    def test_unreviewed_yield_mix_revaluation_or_complex_wip(self):
        c=specimen();content(c,'completion-evidence')['homogeneous_equivalents_reviewed']=False;self.blocked(refresh(c))
        c=specimen(costing='standard');c['standards'][0]['unsupported_revaluation']=True;self.blocked(sources(c))
    def test_iqa12_raw_material_decline_not_write_down_when_fg_recoverable(self):
        c=case();c['items'][0]['closing_cost']='320';content(c,'component-measurement')['impairment_indicator']=True
        a=dict(item='component',checked_on=c['execution_date'],current_market=True,completion_cost_complete=True,selling_cost_complete=True,obsolescence_reviewed=True,grouping='item',forecast_invented=False,expiry_reviewed=True,selling_price='8',completion_cost='0',selling_cost='0',carrying_cost_before_measurement='400',prior_write_down='0',original_cost='400',valuation_memo='Independent raw material market decline assessment',recovery_evidence_memo='Independent finished goods incorporating this RM recover their full10 cost at15 selling price',recovery_reviewed=True,forecast_used=False,forecast_checked_on=c['execution_date'],forecast_reviewed=True,expired=False,salvage_supported=False,finished_goods_recoverable=True,finished_goods_recovery_doc='fg-recovery-source')
        document(c,'fg-recovery-source',dict(item='product',component='component',checked_on=c['execution_date'],current_market=True,selling_price='15',completion_cost='0',selling_cost='0',unit_cost='10',recovery_reviewed=True));document(c,'raw-recovery-source',a);c['valuation']=[row(c,'raw-decline-test',item='component',source_doc='raw-recovery-source',prior_write_down='0',adjustment='-80')]
        c['gl'][0]['closing']=c['gl'][0]['statement']='320';c['gl'].append(row(c,'Inventory measurement expense',currency='USD',opening='0',closing='80',statement='80'));c['gl_inventory'].append('Inventory measurement expense');c['disclosures'].update(closing_inventory='1120',write_down='80');self.blocked(sources(repair_disclosure_sources(c)))
    def test_valid_raw_context_eight_framework_recovery_cases(self):
        for fw in ('IFRS','AASB','US_GAAP','UK_GAAP'):
            for recoverable in (True,False):
                r=self.complete(scale_case(raw_context_case(fw,recoverable)));exempt=fw in {'IFRS','AASB'} and recoverable;self.assertEqual(Decimal('1644' if exempt else '1534.4'),r['calculations']['closing_inventory']);self.assertEqual(Decimal('0' if exempt else '109.6'),r['calculations']['write_down'])
    def test_raw_recovery_current_cost_market_component_and_method(self):
        for key,val in [('checked_on','2025-12-31'),('current_market',False),('unit_cost','9'),('item','missing-fg'),('component','different-rm'),('recovery_reviewed',False),('cost_basis_memo',''),('net_sales_estimate_memo','')]:
            c=raw_context_case();content(c,'fg-recovery-source')[key]=val;self.blocked(refresh(c))
        for key,val in [('raw_measurement_method','LCNRV'),('finished_goods_recoverable',False),('raw_context_memo','')]:
            c=raw_context_case();content(c,'raw-recovery-source')[key]=val;self.blocked(refresh(c))
    def test_us_uk_do_not_inherit_ifrs_raw_recovery_method(self):
        for fw in ('US_GAAP','UK_GAAP'):
            c=raw_context_case(fw);content(c,'raw-recovery-source')['raw_measurement_method']='finished_goods_recoverability';self.blocked(refresh(c))
            c=raw_context_case(fw);content(c,'raw-recovery-source')['framework_raw_method_reviewed']=False;self.blocked(refresh(c))
    def test_ifrs_replacement_cost_only_when_fg_not_recoverable(self):
        c=raw_context_case(recoverable=False);content(c,'raw-recovery-source')['replacement_cost_appropriate']=False;self.blocked(refresh(c))
        c=raw_context_case(recoverable=True);content(c,'raw-recovery-source')['raw_measurement_method']='replacement_cost';self.blocked(refresh(c))
    def test_production_unit_cost_and_real_class_bridges(self):
        r=self.complete(specimen());a=r['calculations'];self.assertEqual(Decimal('13.7'),a['order-1']['finished_unit_cost']);self.assertEqual(Decimal('80'),a['order-1']['completed_quantity']);self.assertEqual(Decimal('20'),a['order-1']['closing_equivalent_units'])
        for cl,b in a['class_bridges'].items():self.assertEqual(b['closing'],b['opening']+b['own_movement']+b['retained_owner_intake'])
    def test_malformed_payloads(self):
        for c in (None,[],{},dict(framework='unknown')):self.assertEqual('blocked',assess_case(PACKAGE,c)['status'])

if __name__=='__main__':unittest.main()
