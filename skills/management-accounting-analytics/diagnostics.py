"""Deterministic diagnostic methods over reviewed sources; no accounting authority.

Sources are independently frozen document contents under the native skill's
source/release/case review gates. Current numeric owner references are reexecuted
by governance_accounting.start. All attribution keys come from those documents,
not caller driver aliases. No network, forecast generation or GL correction.
"""
from decimal import Decimal
from datetime import date
from governance_accounting import ReviewRequired, doc, accounting_owner, owner_assertion

ZERO=Decimal(0)
CATEGORIES={'economic','accounting_close','data_reliability','mixed'}
EVIDENCE={'bridge_attribution','direct_operational_evidence','statistical_association','management_explanation','model_hypothesis'}

def num(v):
    if isinstance(v,bool):raise ReviewRequired('Boolean is not a diagnostic amount')
    try:n=Decimal(str(v))
    except Exception as e:raise ReviewRequired('Invalid diagnostic number') from e
    if not n.is_finite():raise ReviewRequired('Nonfinite diagnostic number')
    return n

def require(condition, message):
    if not condition:raise ReviewRequired(message)

def exact(a,b, message):require(num(a)==num(b), message)

def population(rows, inventory):
    require(isinstance(rows,list) and rows, 'Diagnostic source population required')
    ids=[r['id'] for r in rows]
    require(len(ids)==len(set(ids)) and len(inventory)==len(set(inventory)) and set(ids)==set(inventory), 'Incomplete/duplicate diagnostic population')

def period(span):
    require(isinstance(span,list) and len(span)==2, 'Diagnostic period required')
    a,b=[date.fromisoformat(x) for x in span]
    require(a<=b,'Invalid diagnostic period')
    return a,b

def scope(c, s, expected_period):
    require(s['entity']==c['entity'] and s['currency']==c['governance_method']['currency'] and s['unit']==c['diagnostic']['unit'], 'Diagnostic entity/currency/unit mismatch')
    require(s['period']==expected_period, 'Diagnostic source/comparator period mismatch')
    period(s['period'])

def owner_value(c, ref):
    require(set(ref)=={'owner_import','result_path','amount'}, 'Only numeric evidence owner reference allowed')
    return owner_assertion(c,ref)

def actual(c, docs, selector, expected_period, current=False):
    require(set(selector)=={'doc'}, 'Diagnostic source selector must identify frozen document')
    s=doc(docs,selector['doc'])['content'];scope(c,s,expected_period)
    require(s['kind']=='actual' and s['posted_only'] is True,'Budget/forecast cannot be accounting actual')
    population(s['records'],s['inventory'])
    total=sum((num(r['amount']) for r in s['records']),ZERO)
    exact(s['amount'],total,'Diagnostic source records do not reconcile')
    if current:
        refs=s['owner_components'];require(refs,'Current accounting metric needs actual owner lineage')
        total_owner=ZERO;identities=set()
        for r in refs:
            require(r['sign'] in (-1,1) and type(r['sign']) is int,'Owner component sign required')
            imp=accounting_owner(c,r['ref']['owner_import']);key=(imp['package'],tuple(r['ref']['result_path']))
            require(key not in identities,'Current metric repeats accounting component');identities.add(key)
            if s['metric']=='gross_profit':
                allowed={('revenue-recognition',('period_revenue',)):1,('inventory-cost',('cogs',)):-1}
                if s['presentation_basis']=='inventory_relief_and_manufacturing_expense':allowed[('inventory-cost',('manufacturing_expense',))]=-1
                require(key in allowed and r['sign']==allowed[key],'Gross-profit component sign/owner contradicts presentation basis')
            total_owner+=owner_value(c,r['ref'])*r['sign']
        if s['metric']=='gross_profit':require(identities==set(allowed),'Gross-profit owner components incomplete')
        exact(total,total_owner,'Diagnostic metric differs from actual completed accounting owners')
    return s

def comparator(c,docs, spec):
    s=doc(docs,spec['doc'])['content'];scope(c,s,spec['period'])
    require(s['kind']==spec['kind'] and s['version']==spec['version'],'Comparator kind/version mismatch')
    require(spec['kind'] in {'actual','budget','forecast','standard','target','approved_baseline'},'Unsupported comparator kind')
    require(s['approved'] is True and s['supplied'] is True,'Comparator must be independently supplied/approved')
    require(date.fromisoformat(s['approved_on'])<=date.fromisoformat(spec['frozen_on'])<=date.fromisoformat(c['reporting_period']),'Comparator approved after frozen analytical baseline')
    if spec['kind']=='actual':
        actual(c,docs,{'doc':spec['doc']},spec['period'])
        require(period(spec['period'])[1]<period([c['period_start'],c['reporting_period']])[0],'Actual comparator must precede current period')
    else:
        # Explicit current target period; never an accounting-truth substitution.
        require(spec['period']==[c['period_start'],c['reporting_period']],'Wrong budget/forecast/standard target period')
        population(s['records'],s['inventory'])
        exact(s['amount'],sum((num(r['amount']) for r in s['records']),ZERO),'Comparator records do not reconcile')
    return s

def rate_quantity(rows):
    """Baseline rate; quantity first; rate at current quantity absorbs interaction."""
    volume=sum(((num(r['q1'])-num(r['q0']))*num(r['p0']) for r in rows),ZERO)
    rate=sum((num(r['q1'])*(num(r['p1'])-num(r['p0'])) for r in rows),ZERO)
    return [('quantity',volume),('rate',rate)]

def price_volume_mix(rows):
    """Total-volume at baseline weighted price; mix at baseline prices; current price."""
    q0=sum((num(r['q0']) for r in rows),ZERO);q1=sum((num(r['q1']) for r in rows),ZERO)
    require(q0>0,'Mix requires positive baseline quantity')
    base=sum((num(r['q0'])*num(r['p0']) for r in rows),ZERO)
    volume=(q1-q0)*base/q0
    mix=sum(((num(r['q1'])-q1*num(r['q0'])/q0)*num(r['p0']) for r in rows),ZERO)
    price=sum((num(r['q1'])*(num(r['p1'])-num(r['p0'])) for r in rows),ZERO)
    return [('volume',volume),('mix',mix),('price',price)]

def assess(c,docs):
    d=c['diagnostic']
    require(isinstance(d,dict), 'Structured diagnostic input required')
    require(set(d)=={'unit','metric','presentation_basis','current','comparator','groups','group_inventory','tolerance','materiality','hypotheses','signals','revenue','component_ties'},'Unsupported diagnostic action/field; Analytics cannot determine accounting or post')
    require(d['presentation_basis'] in {'inventory_relief_only','inventory_relief_and_manufacturing_expense','signed_balance'},'Reviewed diagnostic presentation basis required')
    require(d['metric'] in {'gross_profit','account_balance','expense','revenue'},'Unsupported diagnostic metric')
    if d['metric']=='gross_profit':require(d['presentation_basis']!='signed_balance','Gross profit presentation policy required')
    tolerance=num(d['tolerance']);require(ZERO<=tolerance<=Decimal('.01'),'Deliberate absolute tolerance must be between 0 and .01 units')
    materiality=None if d['materiality'] is None else num(d['materiality'])
    require(materiality is None or materiality>=0,'Negative materiality')
    cur=actual(c,docs,d['current'],[c['period_start'],c['reporting_period']],True)
    old=comparator(c,docs,d['comparator'])
    require(cur['metric']==old['metric']==d['metric'] and cur['presentation_basis']==old['presentation_basis']==d['presentation_basis'],'Incomparable metric/presentation basis')
    population(d['groups'],d['group_inventory'])
    used=set();owner_metrics=set();allocated_metrics=set();drivers=[];questions=[];method_records=[]
    for g in d['groups']:
        require(set(g)=={'id','doc','method','sign','labels','accounting_check'},'Unsupported diagnostic group field')
        src=doc(docs,g['doc'])['content'];scope(c,src,[c['period_start'],c['reporting_period']])
        require(src['baseline_period']==old['period'] and src['comparator_version']==old['version'],'Driver comparator period/version mismatch')
        require(src['presentation_basis']==d['presentation_basis'],'Driver presentation mismatch')
        require(src['category'] in CATEGORIES and src['evidence_class'] in EVIDENCE,'Driver category/evidence classification required')
        require(src['evidence_class'] in {'bridge_attribution','direct_operational_evidence'},'Hypothesis/association/management explanation cannot establish a quantitative cause')
        require(src['confidence'] in {'high','medium','low'},'Driver confidence required')
        require(src['population_complete'] is True,'Incomplete driver population cannot be fully explained')
        population(src['records'],src['inventory'])
        require(type(g['sign']) is int and g['sign'] in (-1,1),'Diagnostic bridge sign convention required')
        require(g['method']==src['method'],'Driver method differs from frozen source convention')
        tokens=[]
        for r in src['records']:
            # Original economic component identities are frozen in reviewed source.
            require(r['economic_components'] and len(r['economic_components'])==len(set(r['economic_components'])),'Disjoint original economic components required')
            for component in r['economic_components']:
                token=(c['entity'],c['governance_method']['currency'],tuple(src['period']),component)
                require(token not in used,'Economic analytical attribution counted twice')
                used.add(token);tokens.append(list(token[:2])+[list(token[2]),token[3]])
            if r.get('current_owner') is not None:
                imp=accounting_owner(c,r['current_owner']['owner_import']);metric_identity=(imp['package'],tuple(r['current_owner']['result_path']))
                require(metric_identity not in owner_metrics,'Accounting owner metric attributed twice under economic aliases')
                owner_metrics.add(metric_identity)
                exact(r['current_amount'],owner_value(c,r['current_owner']),'Driver amount not actual owner metric')
            if g['method'] in {'rate_quantity','price_volume_mix'}:
                for k in ('q0','q1','p0','p1'):require(num(r[k])>=0,'Negative quantity/rate unsupported')
                exact(r['baseline_amount'],num(r['q0'])*num(r['p0']),'Baseline quantity/rate amount mismatch')
                exact(r['current_amount'],num(r['q1'])*num(r['p1']),'Current quantity/rate amount mismatch')
            elif g['method']=='owner_flux':
                require(r.get('current_owner') is not None,'Owner flux needs actual owner metric')
            elif g['method']=='source_flux':
                require(r['posted_only'] is True,'Source flux must bind posted accounting movement')
            else:raise ReviewRequired('Unsupported deterministic diagnostic method')
        rs=src['records']
        if src.get('component_allocation'):
            allocation=src['component_allocation']
            require(set(allocation)=={'components','numerator','denominator'},'Controlled native cost-component allocation required')
            denominator=owner_value(c,allocation['denominator']);require(denominator>0,'Allocation denominator must be positive')
            share=owner_value(c,allocation['numerator'])/denominator
            require(ZERO<=share<=1,'Cost-component allocation outside owner population')
            for ref in allocation['components']:
                imp=accounting_owner(c,ref['owner_import']);key=(imp['package'],tuple(ref['result_path']))
                require(imp['package']==src['source_owner'] and key not in allocated_metrics,'Native cost component attributed twice or wrong owner')
                allocated_metrics.add(key)
            allocated=sum((owner_value(c,ref) for ref in allocation['components']),ZERO)*share
            exact(sum((num(r['current_amount']) for r in rs),ZERO),allocated,'Diagnostic cost subcomponents contradict actual native cost allocation')
        parts=rate_quantity(rs) if g['method']=='rate_quantity' else price_volume_mix(rs) if g['method']=='price_volume_mix' else [('movement',sum((num(r['current_amount'])-num(r['baseline_amount']) for r in rs),ZERO))]
        exact(sum((v for _,v in parts),ZERO),sum((num(r['current_amount'])-num(r['baseline_amount']) for r in rs),ZERO),'Method bridge fails to reconcile')
        require(set(g['labels'])=={k for k,v in parts},'Method labels must cover disjoint effects exactly')
        for k,value in parts:
            drivers.append(dict(id=g['id']+'-'+k,label=g['labels'][k],contribution=str(value*g['sign']),category=src['category'],confidence=src['confidence'],status='SUPPORTED',evidence_class=src['evidence_class'],
                lineage=dict(source_doc=g['doc'],source_owner=src['source_owner'],source_metric=src['source_metric'],period=src['period'],entity=src['entity'],currency=src['currency'],unit=src['unit'],comparator=d['comparator'],method=g['method'],effect=k,economic_components=tokens,native_component_allocation=src.get('component_allocation'))))
        method_records.append(dict(group=g['id'],method=g['method'],sign=g['sign'],baseline='supplied comparator',interaction='current quantity rate effect' if g['method']=='rate_quantity' else 'current quantity price effect' if g['method']=='price_volume_mix' else 'none'))
        if g['accounting_check'] is not None:
            check=g['accounting_check']
            require(set(check)=={'owner_import','result_path','amount','issue','reason'},'Accounting check is an inquiry, never treatment or journal')
            imp=accounting_owner(c,check['owner_import']);value=owner_value(c,{k:check[k] for k in ('owner_import','result_path','amount')})
            # A check may only challenge the very accounting amount underlying its group.
            require(any(r.get('current_owner')=={k:check[k] for k in ('owner_import','result_path','amount')} for r in rs),'Accounting inquiry must bind its actual analytical driver')
            questions.append(dict(id=g['id']+'-accounting',target_owner=imp['package'],issue=check['issue'],reason=check['reason'],amount=str(value),result_path=check['result_path'],source_evidence=[g['doc']],materiality=None if materiality is None else str(materiality),status='REQUIRES_OWNER'))
    covered=set();tie_metrics=set();baseline_tied=ZERO
    component_signs={(accounting_owner(c,r['ref']['owner_import'])['package'],tuple(r['ref']['result_path'])):r['sign'] for r in cur['owner_components']}
    groupby={g['id']:g for g in d['groups']}
    require(d['component_ties'],'Diagnostic drivers require exact owner component ties')
    for tie in d['component_ties']:
        require(set(tie)=={'groups','current_owner','baseline_field','sign'},'Controlled diagnostic component tie required')
        require(type(tie['sign']) is int and tie['sign'] in (-1,1),'Component tie sign required')
        imp=accounting_owner(c,tie['current_owner']['owner_import']);key=(imp['package'],tuple(tie['current_owner']['result_path']))
        require(key in component_signs and tie['sign']==component_signs[key],'Driver tie sign/metric differs from actual accounting presentation')
        require(key not in tie_metrics,'Owner population partitioned more than once');tie_metrics.add(key)
        totals=[ZERO,ZERO]
        for gid in tie['groups']:
            require(gid in groupby and gid not in covered,'Driver component tie omitted/duplicated');covered.add(gid)
            group=groupby[gid];source=doc(docs,group['doc'])['content']
            if len(tie['groups'])>1:
                require(source.get('component_allocation') or all(r.get('current_owner') is not None for r in source['records']),'Partitioned accounting metric requires semantic native component lineage for every group')
            require(group['sign']==tie['sign'] and source['source_owner']==imp['package'],'Driver sign/source owner contradicts its owner component tie')
            for index,field in enumerate(('baseline_amount','current_amount')):totals[index]+=sum((num(r[field]) for r in source['records']),ZERO)
        exact(totals[1],owner_value(c,tie['current_owner']),'Diagnostic component population differs from owner metric')
        baseline_tied+=totals[0]*tie['sign']
        exact(totals[0],old[tie['baseline_field']],'Diagnostic baseline component population mismatch')
    require(covered==set(groupby),'Diagnostic groups lack accounting component lineage')
    start=num(old['amount']);end=num(cur['amount']);explained=sum((num(x['contribution']) for x in drivers),ZERO);residual=end-start-explained
    # Residual is computed and visible, never distributed into driver values.
    bridge=dict(metric=d['metric'],unit=d['unit'],starting=str(start),ending=str(end),change=str(end-start),drivers=drivers,residual=str(residual),tolerance=str(tolerance),
        explained_amount=str(explained),explained_percent=None if end==start else str(explained/(end-start)*100),comparator_kind=old['kind'],comparator_version=old['version'],
        status='RECONCILED' if abs(residual)<=tolerance else 'UNEXPLAINED_RESIDUAL',materiality=None if materiality is None else str(materiality),presentation_basis=d['presentation_basis'])
    exact(start+explained+residual,end,'Diagnostic driver bridge invariant')
    open_items=[]
    if abs(residual)>tolerance and (materiality is None or abs(residual)>=materiality):open_items.append('Unexplained diagnostic residual '+str(residual)+' requires evidence; materiality is unknown' if materiality is None else 'Material unexplained diagnostic residual '+str(residual)+' requires evidence')
    hypotheses=[]
    for h in d['hypotheses']:
        require(set(h)=={'id','observation','hypothesis','tests','evidence_class'},'Unsupported hypothesis assertion')
        require(h['evidence_class'] in EVIDENCE,'Hypothesis evidence class required')
        outcomes=[];evidence=[];classes=[]
        for test in h['tests']:
            require(set(test)=={'doc','field','operator','value'},'Controlled hypothesis test required')
            s=doc(docs,test['doc'])['content'];scope(c,s,[c['period_start'],c['reporting_period']]);evidence.append(test['doc']);classes.append(s.get('evidence_class','model_hypothesis'))
            require(test['operator'] in {'equal','above','below'},'Unsupported hypothesis operator')
            a=num(s[test['field']]);b=num(test['value'])
            outcomes.append(a==b if test['operator']=='equal' else a>b if test['operator']=='above' else a<b)
        supported=h['evidence_class'] in {'bridge_attribution','direct_operational_evidence'} and all(x in {'bridge_attribution','direct_operational_evidence'} for x in classes)
        disposition='UNRESOLVED' if not outcomes or not supported else 'SUPPORTED' if all(outcomes) else 'REJECTED' if not any(outcomes) else 'PARTIALLY_SUPPORTED'
        hypotheses.append(dict(id=h['id'],observation=h['observation'],hypothesis=h['hypothesis'],disposition=disposition,evidence_class=h['evidence_class'],evidence=evidence,confidence='medium' if disposition=='SUPPORTED' else 'low'))
    observations=[]
    for sig in d['signals']:
        require(set(sig)=={'doc','field','baseline_field','threshold','question'},'Controlled anomaly threshold required')
        s=doc(docs,sig['doc'])['content'];scope(c,s,[c['period_start'],c['reporting_period']])
        threshold=num(sig['threshold']);require(threshold>=0,'Negative anomaly threshold')
        delta=num(s[sig['field']])-num(s[sig['baseline_field']])
        if abs(delta)>threshold:observations.append(dict(observation='Observed change '+str(delta),confidence='medium',status='OBSERVATION_ONLY',question=sig['question'],required_evidence=[sig['doc']]))
    if d['revenue'] is not None:
        require(d['metric']=='gross_profit','Percentage-point margin bridge requires gross profit')
        revenue=d['revenue'];require(set(revenue)=={'current_owner','baseline_amount'},'Governed margin denominator required')
        r1=owner_value(c,revenue['current_owner']);r0=num(revenue['baseline_amount'])
        require(r1>0 and r0>0,'Margin denominators must be positive')
        # The prior revenue denominator must be part of the independently frozen baseline.
        exact(r0,old['revenue'],'Baseline revenue denominator differs from frozen comparator')
        points=[dict(id=x['id'],label=x['label'],contribution=str(num(x['contribution'])/r1*100)) for x in drivers]
        denominator=start*(1/r1-1/r0)*100
        bridge['margin_points']=dict(starting=str(start/r0*100),ending=str(end/r1*100),drivers=points,denominator_effect=str(denominator),residual=str(residual/r1*100),convention='driver GP contributions/current revenue; separate baseline-GP denominator effect')
    return dict(bridge=bridge,hypotheses=hypotheses,observations=observations,methods=method_records,accounting_questions=questions,attribution_ledger=sorted([list(x[:2])+[list(x[2]),x[3]] for x in used],key=str),open_items=open_items)
