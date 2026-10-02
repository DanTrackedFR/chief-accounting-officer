from calendar import isleap
from operations_accounting import *

def charge(start,end,basis,life,method,units=ZERO):
    if end<start:return ZERO
    if method=='units_of_production':return cash(min(basis,basis*units/positive(life)))
    if method!='straight_line':raise ReviewRequired('Unsupported depreciation method')
    fraction_year=ZERO;d=start
    while d<=end:
        yend=min(end,iso(str(d.year)+'-12-31'));fraction_year+=Decimal((yend-d).days+1)/Decimal(366 if isleap(d.year) else 365);d=yend+timedelta(days=1)
    return cash(min(basis,basis/positive(life)*fraction_year))

def assess(c,claims):
    proof(c,'assets','costs','cip','gl','handoffs','asset_policy')
    handoff(c,'impairment','Impairment');handoff(c,'leases','Lease Accounting')
    policy=c['asset_policy'];required(policy,'model','component_review','life_review','review_memo')
    if policy['model']!='cost' or not flag(policy,'component_review') or not flag(policy,'life_review'):raise ReviewRequired('Cost model, component and life review required')
    assets=rows(c['assets'],False);costs=rows(c['costs']);projects=rows(c['cip']);inventory(c,'asset_inventory',assets);inventory(c,'project_inventory',projects);amap={a['id']:a for a in assets};pmap={p['id']:p for p in projects};adds={id:ZERO for id in amap};padds={id:ZERO for id in pmap};entries=[];expenses=ZERO
    if set(amap)&set(pmap):raise ReviewRequired('Asset and project destination IDs overlap')
    for x in costs:
        approval(x,c);required(x,'amount','date','eligible','eligibility_memo','kind','destination','account','offset','recognition_reviewed')
        inperiod(c,x['date']);n=positive(x['amount'])
        if not flag(x,'recognition_reviewed') or x['kind'] not in ['purchase','freight','installation','training','general_overhead','abnormal_waste']:raise ReviewRequired('Specialized cost requires separate technical review')
        if flag(x,'eligible'):
            if x['kind'] in ['training','general_overhead','abnormal_waste']:raise ReviewRequired('Ineligible cost cannot be capitalized')
            if x['destination'] in amap:
                a=amap[x['destination']]
                if iso(x['date'])>iso(a['ready_date']):raise ReviewRequired('Post-readiness cost needs separately approved improvement/component route')
                adds[x['destination']]+=n;entries.append(journal(('Dr','PPE cost',n),('Cr',x['offset'],n)))
            elif x['destination'] in pmap:padds[x['destination']]+=n;entries.append(journal(('Dr','construction in progress',n),('Cr',x['offset'],n)))
            else:raise ReviewRequired('Cost destination not in register')
        else:expenses+=n;entries.append(journal(('Dr',x['account'],n),('Cr',x['offset'],n)))
    cipend=ZERO;cipwork=[]
    for p in projects:
        approval(p,c);required(p,'opening','transfer','asset_id','ready_date','ready','impairment_reviewed','gl_closing')
        if not flag(p,'impairment_reviewed'):raise ReviewRequired('CIP impairment/abandonment review missing')
        opening=nonnegative(p['opening']);transfer=nonnegative(p['transfer']);end=opening+padds[p['id']]-transfer
        if end<0:raise ReviewRequired('CIP transfer exceeds supported costs')
        if transfer:
            if not flag(p,'ready') or p['asset_id'] not in amap:raise ReviewRequired('CIP transfer not commissioned to a registered asset')
            inperiod(c,p['ready_date'])
            if p['ready_date']!=amap[p['asset_id']]['ready_date']:raise ReviewRequired('CIP commissioning and asset readiness differ')
            adds[p['asset_id']]+=transfer;entries.append(journal(('Dr','PPE cost',transfer),('Cr','construction in progress',transfer)))
        elif flag(p,'ready'):raise ReviewRequired('Ready CIP portion must transfer and start depreciation')
        agree(p['gl_closing'],end,'CIP project GL');cipend+=end;cipwork.append({'id':p['id'],'opening':opening,'additions':padds[p['id']],'transfer':transfer,'closing':end})
    gross=ZERO;acc=ZERO;dep=ZERO;work=[]
    start=iso(c['period_start']);end=iso(c['reporting_period'])
    for a in assets:
        approval(a,c);required(a,'opening_cost','opening_accumulated','residual','remaining_life','ready_date','method','remaining_units','period_units','change','disposal','expected_depreciation','gl_cost','gl_accumulated','scope','component_id','consumption_memo')
        if a['scope']!='ordinary_ppe':raise ReviewRequired('Software, ROU, revaluation, held-for-sale and specialized assets require owning specialist')
        cost=nonnegative(a['opening_cost'])+adds[a['id']];openingacc=nonnegative(a['opening_accumulated']);residual=nonnegative(a['residual']);carrying=cost-openingacc
        if openingacc>cost:raise ReviewRequired('Accumulation exceeds register cost')
        ready=iso(a['ready_date']);begin=max(start,ready);last=end;disp=a['disposal'];required(disp,'enabled')
        if ready>end:raise ReviewRequired('Asset not ready at period end must remain in CIP')
        if flag(disp,'enabled'):required(disp,'date','proceeds','ordinary_sale','evidence');last=inperiod(c,disp['date'])
        if flag(disp,'enabled') and last<ready:raise ReviewRequired('Pre-readiness disposal must use the CIP/uncommissioned asset route')
        change=a['change'];required(change,'enabled');basis=max(carrying-residual,ZERO);life=positive(a['remaining_units'] if a['method']=='units_of_production' else a['remaining_life'])
        if flag(change,'enabled'):
            required(change,'date','new_remaining_life','new_residual','new_information','evidence','units_before','units_after')
            d=inperiod(c,change['date'])
            if d<begin or d>last or not flag(change,'new_information'):raise ReviewRequired('Estimate revision chronology or error assessment unresolved')
            first=charge(begin,d-timedelta(days=1),basis,life,a['method'],nonnegative(change['units_before']));newres=nonnegative(change['new_residual']);newbasis=max(carrying-first-newres,ZERO)
            afterunits=nonnegative(change['units_after'])
            if a['method']=='units_of_production' and nonnegative(change['units_before'])+afterunits!=nonnegative(a['period_units']):raise ReviewRequired('Production before/after revision does not reconcile to complete output')
            if a['method']=='units_of_production' and (nonnegative(change['units_before'])>life or afterunits>positive(change['new_remaining_life'])):raise ReviewRequired('Revised production exceeds supported remaining units')
            amount=first+charge(d,last,newbasis,positive(change['new_remaining_life']),a['method'],afterunits)
        else:
            units=nonnegative(a['period_units'])
            if a['method']=='units_of_production' and units>life:raise ReviewRequired('Production exceeds approved remaining units')
            amount=charge(begin,last,basis,life,a['method'],units)
        agree(a['expected_depreciation'],amount,'Reviewed depreciation expectation');entries.append(journal(('Dr','depreciation expense',amount),('Cr','accumulated depreciation',amount)));dep+=amount;closingacc=openingacc+amount;closingcost=cost;gain=ZERO
        if flag(disp,'enabled'):
            if not flag(disp,'ordinary_sale'):raise ReviewRequired('Disposal requires specialized held-for-sale/sale-leaseback route')
            proceeds=nonnegative(disp['proceeds']);gain=cash(proceeds-(cost-closingacc));entries.append(journal(('Dr','cash',proceeds),('Dr','accumulated depreciation',closingacc),('Dr','disposal loss',max(-gain,ZERO)),('Cr','PPE cost',cost),('Cr','disposal gain',max(gain,ZERO))));closingcost=ZERO;closingacc=ZERO
        agree(a['gl_cost'],closingcost,'Register gross cost GL');agree(a['gl_accumulated'],closingacc,'Register accumulated GL');gross+=closingcost;acc+=closingacc;work.append({'id':a['id'],'cost':cost,'depreciation':amount,'closing_cost':closingcost,'closing_accumulated':closingacc,'carrying':closingcost-closingacc,'disposal_gain':gain})
    agree(c['gl']['cost'],gross,'Class gross GL');agree(c['gl']['accumulated'],acc,'Class accumulated GL');agree(c['gl']['cip'],cipend,'Class CIP GL');population(c,costs,[positive(x['amount']) for x in costs])
    return finish('Qualifying costs, components, depreciation, disposals and CIP reconcile to gross ledgers.',{'assets':work,'cip':cipwork,'depreciation':dep,'excluded_expense':expenses,'closing_cost':gross,'closing_accumulated':acc,'closing_cip':cipend},entries,
      ['Readiness starts depreciation independently of project budget closure; idleness does not automatically stop depreciation.','US component policy and estimate/method changes differ from IAS16; FRS102 significant-change reviews must not be described as an automatic IAS16 annual requirement.'],
      ['Class gross/accumulated rollforwards, depreciation methods/lives, impairment, disposals and CIP commitments; AASB Tier2 disclosures use applicable reduced-disclosure requirements.'])
