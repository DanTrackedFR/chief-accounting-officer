"""Controlled synthetic comparative diagnostics with current native owners.

No runtime approval generation. Frozen source definitions and comparator editions
are independent fixture inputs, explicitly synthetic.
"""
import copy
from decimal import Decimal
from orchestration.tests.fixtures import manufacturing, completed
from governance_cases import document, ready, refresh_release, row
from governance_accounting import digest


def diagnostic_manufacturing():
    req=monthly_manufacturing();req['case_id']='synthetic-factory-margin-investigation'
    req['objective']='Our factory margins look terrible this month. Can you review the close and figure out what’s going on?'
    c=req['facts']['analytics'];curperiod=[c['period_start'],c['reporting_period']];oldperiod=['2026-11-01','2026-11-30'];basis='inventory_relief_and_manufacturing_expense'
    # Imports are actual complete accounting authority; diagnostic arithmetic never posts.
    for family,pkg in [('customer_contract','revenue-recognition')]:
        source=req['facts'][family];c['imports'].append(row(c,'diagnostic-'+pkg,package=pkg,case=copy.deepcopy(source),result=completed(pkg,source),mode='evidence_only'))
    def ref(owner,path,amount):return dict(owner_import=owner,result_path=path,amount=amount)
    revenue=ref('diagnostic-revenue-recognition',['period_revenue'],'40000')
    relief=ref('inventory-owner',['cogs'],'11304');overhead=ref('inventory-owner',['manufacturing_expense'],'45000')
    def base(metric):return dict(entity=c['entity'],currency='USD',unit='USD',period=curperiod,metric=metric,presentation_basis=basis)
    def metric(id,amount,span,components=None):
        s=base('gross_profit');s.update(kind='actual',posted_only=True,period=span,amount=amount,records=[dict(id=id+'-posted',amount=amount)],inventory=[id+'-posted'],version='actual-v1',approved=True,supplied=True,approved_on='2026-11-30',owner_components=components or [])
        document(c,id,s);return s
    prior=metric('diagnostic-prior','15000',oldperiod);prior.update(revenue='50000',cogs='15000',manufacturing_expense='20000')
    next(x for x in c['documents'] if x['id']=='diagnostic-prior')['content']=copy.deepcopy(prior)
    metric('diagnostic-current','-16304',curperiod,[dict(sign=1,ref=revenue),dict(sign=-1,ref=relief),dict(sign=-1,ref=overhead)])
    groups=[]
    def group(id,method,records,labels,sign,owner,source_metric,category='economic',check=None):
        src=base('gross_profit');src.update(baseline_period=oldperiod,comparator_version='actual-v1',method=method,source_owner=owner,source_metric=source_metric,category=category,evidence_class='bridge_attribution',confidence='high',population_complete=True,records=records,inventory=[r['id'] for r in records])
        document(c,id,src);groups.append(dict(id=id,doc=id,method=method,sign=sign,labels=labels,accounting_check=check))
    # Revenue 50k -> 40k, quantity and price/mix separated by explicit convention.
    sales=[dict(id='product-A',q0='20',p0='1500',q1='15',p1='1400',baseline_amount='30000',current_amount='21000',economic_components=['sales-A']),dict(id='product-B',q0='10',p0='2000',q1='5',p1='3800',baseline_amount='20000',current_amount='19000',economic_components=['sales-B'])]
    group('sales','price_volume_mix',sales,dict(volume='Sales volume',mix='Product mix',price='Selling price'),1,'revenue-recognition','period_revenue')
    # Controlled material/labour source components sum to 11,304 current relief.
    group('material','rate_quantity',[dict(id='material-cost',q0='10',p0='10',q1='12',p1='10',baseline_amount='100',current_amount='120',economic_components=['material-local-ex-FX'])],dict(quantity='Material usage',rate='Material input price'),-1,'inventory-cost','cogs material excluding FX')
    group('labour','rate_quantity',[dict(id='labour-cost',q0='4',p0='500',q1='4',p1='540',baseline_amount='2000',current_amount='2160',economic_components=['labour-direct'])],dict(quantity='Labour hours/efficiency attribution',rate='Labour rate'),-1,'inventory-cost','cogs labour')
    group('other-cost','source_flux',[dict(id='other-cost',baseline_amount='12900',current_amount='9024',posted_only=True,economic_components=['other-conversion-allocated'])],dict(movement='Other identified conversion-cost reduction'),-1,'inventory-cost','remaining COGS: 9000 fixed absorption plus 24 variable overhead')
    # Every cost attribution also binds actual Inventory component outputs and
    # the owner COGS/eligible-cost ratio; this never changes native COGS.
    for gid,metrics in [('material',[('material','600')]),('labour',[('direct_labour','10800')]),('other-cost',[('absorbed_fixed','45000'),('variable_overhead','120')])]:
        source=next(x for x in c['documents'] if x['id']==gid)['content']
        source['component_allocation']=dict(components=[ref('inventory-owner',['order-1',key],amount) for key,amount in metrics],numerator=relief,denominator=ref('inventory-owner',['order-1','actual_eligible_total'],'56520'))
    # Independent component tie prevents invented quantitative attribution.
    tie=base('cogs');tie.update(components=[dict(doc='material',field='current_amount'),dict(doc='labour',field='current_amount'),dict(doc='other-cost',field='current_amount')],owner=relief)
    document(c,'diagnostic-cost-tie',tie)
    check=dict(**overhead,issue='Fixed overhead under-recovery accounting',reason='Significant normal-capacity expense warrants governed accounting treatment recheck')
    group('capacity','rate_quantity',[dict(id='unallocated-fixed',q0='.25',p0='80000',q1='.5',p1='90000',baseline_amount='20000',current_amount='45000',current_owner=overhead,economic_components=['unallocated-fixed-OH'])],dict(quantity='Fixed overhead capacity contribution',rate='Fixed overhead spending contribution'),-1,'inventory-cost','manufacturing_expense',category='mixed',check=check)
    c['diagnostic']=dict(component_ties=[dict(groups=['sales'],current_owner=revenue,baseline_field='revenue',sign=1),dict(groups=['material','labour','other-cost'],current_owner=relief,baseline_field='cogs',sign=-1),dict(groups=['capacity'],current_owner=overhead,baseline_field='manufacturing_expense',sign=-1)],unit='USD',metric='gross_profit',presentation_basis=basis,current={'doc':'diagnostic-current'},comparator=dict(doc='diagnostic-prior',kind='actual',version='actual-v1',period=oldperiod,frozen_on='2026-11-30'),groups=groups,group_inventory=[g['id'] for g in groups],tolerance='.01',materiality='1000',
        hypotheses=[dict(id='capacity',observation='Gross profit deteriorated',hypothesis='Higher unallocated fixed overhead explains part of the deterioration',evidence_class='bridge_attribution',tests=[dict(doc='capacity',field='observed_under_recovery',operator='above',value='20000')])],
        signals=[dict(doc='capacity',field='observed_under_recovery',baseline_field='prior_under_recovery',threshold='10000',question='Inspect production capacity and the completed normal-capacity accounting workpaper')],revenue=dict(current_owner=revenue,baseline_amount='50000'))
    capacity=next(x for x in c['documents'] if x['id']=='capacity')['content'];capacity.update(observed_under_recovery='45000',prior_under_recovery='20000')
    for docrow in c['documents']:docrow['content_hash']=digest(docrow['content'])
    req['facts']['analytics']=ready('management-accounting-analytics',c=refresh_release(c))
    # Exact integrated native journal pack fixture-only approval after diagnostics extension.
    from orchestration.runtime import digest as rdigest
    native=[]
    for family,source in req['facts'].items():
        if family=='task_attributes':continue
        from orchestration.planning import FACT_ADAPTERS
        pkg=FACT_ADAPTERS[family][0];r=completed(pkg,source)
        native.append(dict(owner=pkg,case_fingerprint=r['case_fingerprint'],journals=r.get('journal_entry_implications',[])))
    req['journal_pack_review']['payload_fingerprint']=rdigest(dict(mapping=req['journal_account_mapping'],native_owner_journals=native))
    return req


def monthly_manufacturing():
    """Matching December native workpapers, generated/reviewed only in fixture code.

    Machinery uses supplied units-of-production consumption, not twelve months of
    straight-line depreciation relabelled as one month. Original numerical source
    schedules remain controlled; dates and evidence/release fingerprints refresh.
    """
    r=manufacturing()
    def dates(o):
        if isinstance(o,dict):return {k:dates(v) for k,v in o.items()}
        if isinstance(o,list):return [dates(v) for v in o]
        if isinstance(o,str) and len(o)==10 and o[:5]=='2026-' and o[7]=='-':
            return o if o.startswith('2026-12-') else '2026-12-01'
        if isinstance(o,str) and len(o)==10 and o[:5]=='2025-' and o[7]=='-':
            # Preserve genuine prior-year dates, using comparable December scope.
            return '2025-12-'+o[8:]
        return o
    r=dates(r)
    asset=r['facts']['machinery']['assets'][0]
    basis=Decimal(asset['opening_cost'])-Decimal(asset['opening_accumulated'])-Decimal(asset['residual'])
    asset.update(method='units_of_production',period_units='100',remaining_units=str(basis/Decimal('900')),consumption_memo='Synthetic reviewed December factory consumption; 100 units consumed from supplied remaining production capacity')
    controls=r['facts']['control']
    controls['occurrences']=[o for o in controls['occurrences'] if o['period_date']=='2026-12-31']
    controls['occurrence_inventory']=[o['id'] for o in controls['occurrences']]
    controls['occurrence_source']['records']=copy.deepcopy(controls['occurrences']);controls['occurrence_source']['inventory']=list(controls['occurrence_inventory'])
    for d in controls['documents']:
        if isinstance(d['content'],dict) and 'expected_occurrence_ids' in d['content']:d['content']['expected_occurrence_ids']=list(controls['occurrence_inventory'])
    from orchestration.planning import FACT_ADAPTERS
    from production import case_fingerprint, load_workflow
    owners={FACT_ADAPTERS[f][0]:c for f,c in r['facts'].items() if f!='task_attributes'}
    results={};processing=set()
    def recertify(pkg):
        if pkg in results:return results[pkg]
        if pkg in processing:raise AssertionError('Fixture owner cycle')
        processing.add(pkg);c=owners[pkg]
        for imp in c.get('imports',[]):
            imp['result']=copy.deepcopy(recertify(imp['package']));imp['case']=copy.deepcopy(owners[imp['package']])
        for d in c.get('documents',[]):d['content_hash']=digest(d['content'])
        if 'release_review' in c:
            keys=load_workflow(pkg).KEYS;c['release_review']['payload_fingerprint']=digest({k:c[k] for k in keys})
        c['reviewer_signoff']['case_fingerprint']=case_fingerprint(c)
        result=completed(pkg,c);results[pkg]=result;processing.remove(pkg);return result
    for pkg in owners:recertify(pkg)
    from orchestration.runtime import digest as rdigest
    native=[dict(owner=p,case_fingerprint=results[p]['case_fingerprint'],journals=results[p].get('journal_entry_implications',[])) for p in owners]
    r['journal_pack_review']['payload_fingerprint']=rdigest(dict(mapping=r['journal_account_mapping'],native_owner_journals=native))
    return r
