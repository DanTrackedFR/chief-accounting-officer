"""Finite/indefinite purchased assets and tightly gated development costs."""
from financing_accounting import *

def assess(c,claims):
    rs=begin(c,'assets');entries=imports(c,{'business-combinations','asset-impairment','accounting-changes'});out=[];gross=[]
    op_cost=op_acc=cl_cost=cl_acc=ZERO
    for r in rs:
        origin=enum(r,'origin',{'purchased','development'});life=enum(r,'life',{'finite','indefinite'})
        reviewed(r,c,'rights_memo','recognition_memo','life_memo','annual_review','impairment_memo')
        if not flag(r,'recognition_supported'):raise ReviewRequired('Unsubstantiated intangible recognition')
        if c['framework']=='UK_GAAP' and life=='indefinite':raise ReviewRequired('FRS102 requires finite intangible useful life')
        if enum(r,'model',{'cost'})!='cost':raise ReviewRequired('Active-market revaluation requires specialist')
        costs=rows(r['costs']);inventory(r,'cost_inventory',costs);additions=excluded=ZERO
        gate_date=iso(r['gate_date']) if origin=='development' else None
        if origin=='development':
            if c['framework']=='US_GAAP':raise ReviewRequired('US software/R&D capitalization is specialized; do not import IAS38 development gate')
            if c['framework']=='UK_GAAP' and enum(c['accounting_policy'],'development_election',{'capitalize','expense'})=='expense':gate_date=None
            elif not all(flag(r,k) for k in ['feasible','intention','ability','benefits','resources','reliable_measurement']):raise ReviewRequired('All development recognition conditions must be evidenced')
        available=iso(r['available_date']);recognized=iso(r['recognition_date'])
        if origin=='purchased' and available<recognized:raise ReviewRequired('Asset availability cannot precede acquired control/recognition')
        for p in costs:
            approval(p,c);d=inperiod(c,p['date']);amount=nonnegative(p['amount']);kind=enum(p,'kind',{'purchase','eligible_development','research','training','maintenance'})
            if kind=='purchase' and (d!=recognized or d>available):raise ReviewRequired('Purchase recognition/control date and availability chronology do not reconcile')
            qualifying=(kind=='purchase' and origin=='purchased') or (kind=='eligible_development' and origin=='development' and gate_date is not None and gate_date<=d<=available)
            if flag(p,'capitalize')!=qualifying:raise ReviewRequired('Capitalization conflicts with source type or dated gate; pre-gate expense cannot be reinstated')
            if qualifying:additions+=amount
            else:excluded+=amount
        opening=nonnegative(r['opening_cost']);acc=nonnegative(r['opening_accumulated']);residual=nonnegative(r['residual']);cost=opening+additions
        if opening and additions:raise ReviewRequired('New costs on an existing intangible require separate dated component schedule')
        if opening and recognized>iso(c['period_start']):raise ReviewRequired('Opening intangible stock cannot be recognized after opening date')
        disposed=flag(r,'disposed')
        disposal_date=inperiod(c,r['disposal_date']) if disposed else iso(c['reporting_period'])
        if disposed and disposal_date<max(available,recognized):raise ReviewRequired('Disposal precedes recognition or available-use evidence')
        if acc+residual>cost:raise ReviewRequired('Accumulated amortization/residual exceeds cost')
        if life=='indefinite':
            if not flag(r,'annual_impairment_complete'):raise ReviewRequired('Indefinite asset requires completed impairment evidence')
            amort=ZERO
        else:
            years=positive(r['remaining_years']);use=fraction(r['period_fraction'])
            if c['framework']=='UK_GAAP' and not flag(r,'life_reliably_estimated') and years>10:raise ReviewRequired('Unreliable UK life cannot exceed ten years')
            if available>iso(c['reporting_period']) and use:raise ReviewRequired('Amortization precedes availability')
            if available>iso(c['period_start']) and opening:raise ReviewRequired('Mixed existing/new asset requires separate component schedule')
            enum(c['accounting_policy'],'time_basis',{'actual_actual'})
            start=max(available,recognized,iso(c['period_start']));end=disposal_date;expected=ZERO
            for year in range(start.year,end.year+1):
                lo=max(start,date(year,1,1));hi=min(end,date(year,12,31))
                if hi>=lo:expected+=Decimal((hi-lo).days+1)/Decimal((date(year+1,1,1)-date(year,1,1)).days)
            if use!=expected:raise ReviewRequired('Amortization fraction must equal derived available actual-day/year interval')
            amort=cash(min(cost-acc-residual,(cost-acc-residual)/years*use))
        agree(r['expected_amortization'],amort,'Intangible amortization')
        proceeds=nonnegative(r['proceeds']);net=cost-acc-amort
        if not disposed and proceeds:raise ReviewRequired('Proceeds without disposal')
        end_cost=ZERO if disposed else cost;end_acc=ZERO if disposed else acc+amort
        agree(r['gl_cost'],end_cost,'Intangible gross GL');agree(r['gl_accumulated'],end_acc,'Intangible accumulated GL')
        entries += [journal(('Dr','Intangible asset',additions),('Dr','Intangible excluded expense',excluded),('Cr','Cash',additions+excluded)),journal(('Dr','Amortization expense',amort),('Cr','Accumulated amortization',amort))]
        if disposed:
            gain=proceeds-net
            entries.append(journal(('Dr','Cash',proceeds),('Dr','Accumulated amortization',acc+amort),('Dr','Disposal loss',max(-gain,ZERO)),('Cr','Intangible asset',cost),('Cr','Disposal gain',max(gain,ZERO))))
        gross.append(additions+excluded);out.append(dict(origin=origin,additions=additions,excluded=excluded,amortization=amort,closing_cost=end_cost,closing_accumulated=end_acc,closing_net=end_cost-end_acc))
        op_cost+=opening;op_acc+=acc;cl_cost+=end_cost;cl_acc+=end_acc
    population(c,rs,gross)
    stocks(c,{'Intangible asset':(op_cost,cl_cost),'Accumulated amortization':(-op_acc,-cl_acc)})
    return complete(c,'Intangible register, dated cost gates and amortization reconciled',dict(assets=out),entries,
        ['Purchased rights and economic lives require actual evidence; no internally generated brand/customer list route',
         'US software/hosting, cloud/website/crypto, revaluation, unusual legal rights and complex useful-life changes require underlying specialists'])
