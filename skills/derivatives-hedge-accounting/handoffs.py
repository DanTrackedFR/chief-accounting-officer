"""Bounded source-to-current-reporting receipt, separate from statement production.

Only first-year continuing cash-flow hedge results are supported. Both owners
must currently execute complete; mappings bind actual source economics to their
own distinct TB and equity component rows. This module never chooses statement
classification, changes owner cases, or invents a baseline business balance.
"""
from core_accounting import ReviewRequired,dec,cash
from production import execute
import hashlib,json

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()
def require(ok,message):
    if not ok:raise ReviewRequired(message)
def exact(a,b,label):require(cash(a)==cash(b),label+' differs from current actual Hedge result')
def unique_rows(rs,label):
    require(isinstance(rs,list) and bool(rs),label+' requires nonempty actual population')
    require(all(isinstance(r,dict) and isinstance(r.get('id'),str) and r['id'] for r in rs),'Malformed '+label)
    require(len({r['id'] for r in rs})==len(rs),'Duplicate '+label)
    return {r['id']:r for r in rs}
def run_owner(package,imp):
    require(isinstance(imp,dict) and isinstance(imp.get('case'),dict) and isinstance(imp.get('result'),dict),'Actual case/result owner import required')
    current=execute(package,imp['case'])
    require(current['status']=='complete','Current completed '+package+' owner required')
    require(digest(current)==digest(imp['result']),'Imported '+package+' result differs from fresh native owner execution')
    return current

def validate_reporting_handoff(hedge_imports,reporting_import,explicit_mapping):
    """Return an internal validated receipt, or fail closed on any source mismatch."""
    imports=unique_rows(hedge_imports,'Hedge owner imports');mapping=unique_rows(explicit_mapping,'source/reporting mappings')
    report=run_owner('financial-statements',reporting_import);rc=reporting_import['case']
    require(isinstance(rc.get('currency'),str) and bool(rc['currency']),'Reporting functional/presentation monetary unit must be evidenced')
    tb=unique_rows(rc['current_tb'],'reporting TB');equity=unique_rows(rc['equity_bridge'],'equity components')
    sources={};expected=set();economics=set();source_reserves={}
    for id,imp in imports.items():
        hc=imp['case'];r=run_owner('derivatives-hedge-accounting',imp)
        require(all(hc.get(k)==rc.get(k) for k in ('entity','framework','jurisdiction','period_start','reporting_period','currency')),'Hedge/reporting monetary context differs')
        contracts={x['id']:x for x in hc['contracts']};relationships={x['instrument_id']:x for x in hc['relationships']}
        reserves={x['id']:x for x in r['calculations']['hedge_reserves']}
        for d in r['calculations']['derivatives']:
            require(d['route']=='cash_flow','Reporting adapter supports continuing first-year cash-flow hedges only')
            require(d['id'] in relationships,'Actual designated source relationship required');rel=relationships[d['id']];reserve=reserves[rel['id']]
            require(rel['status'] in {'active','rebalanced'},'Discontinued reporting relationship needs separate governed source handoff')
            require(dec(reserve['opening'])==0 and dec(reserve['reclassification'])==0 and dec(reserve['basis_adjustment'])==0,'Only first-year continuing OCI/reserve handoff supported')
            require(dec(d['opening'])==0 and dec(d['settlement'])==0,'Prior derivative/settlement reporting handoff requires movement-owner mapping')
            economic=(hc['entity'],hc['currency'],hc['reporting_period'],d['id'])
            require(economic not in economics,'Derivative economic balance mapped twice');economics.add(economic)
            expected.add((id,d['id'],rel['id']));sources[(id,d['id'],rel['id'])]=(d,reserve)
            source_reserves[(id,rel['id'])]=reserve
    target_ids=set();mapped=set();receipt=[]
    for m in mapping.values():
        required=('source_import_id','instrument_id','relationship_id','derivative_tb_id','pnl_tb_id','oci_tb_id','equity_component_id')
        require(all(isinstance(m.get(k),str) and m[k] for k in required),'Explicit semantic mapping fields required')
        key=(m['source_import_id'],m['instrument_id'],m['relationship_id']);require(key in expected,'Mapping names wrong actual source instrument/relationship')
        require(key not in mapped,'Source accounting relationship mapped twice');mapped.add(key)
        d,reserve=sources[key]
        source_fingerprint=imports[m['source_import_id']]['result']['case_fingerprint']
        ids=[m['derivative_tb_id'],m['pnl_tb_id'],m['oci_tb_id']]
        require(len(set(ids))==3 and not set(ids)&target_ids,'Duplicate reporting target causes duplicate/offset posting');target_ids.update(ids)
        require(all(id in tb for id in ids),'Mapped actual TB account absent')
        asset,pnl,oci=(tb[id] for id in ids)
        require(all(row['source_version']==source_fingerprint for row in (asset,pnl,oci)),'Mapped TB source lineage differs from actual current owner')
        require(asset['category']==('asset' if dec(d['closing'])>=0 else 'liability'),'Derivative TB sign/classification mismatch')
        require(pnl['category']==('revenue' if dec(d['ineffectiveness'])>=0 else 'expense'),'Derivative earnings mapping category mismatch')
        require(oci['category']=='oci','Unclosed current OCI must not also be posted to closing equity')
        exact(asset['balance'],d['closing'],'Derivative TB balance');exact(pnl['balance'],-dec(d['ineffectiveness']),'Hedge P&L TB');exact(oci['balance'],-dec(reserve['recognized_oci']),'Hedge OCI TB')
        require(m['equity_component_id'] in equity,'Mapped independent Hedge equity component absent')
        component=equity[m['equity_component_id']]
        require(component.get('source_case_fingerprint')==source_fingerprint,'Equity contribution source lineage differs from current Hedge owner')
        require(m['equity_component_id'] not in target_ids,'Equity component reused');target_ids.add(m['equity_component_id'])
        exact(component['opening'],0,'Hedge equity opening');exact(component['profit'],d['ineffectiveness'],'Hedge component earnings');exact(component['oci'],reserve['recognized_oci'],'Hedge component OCI')
        for k in ('owner_transactions','retrospective_adjustments','other'):exact(component[k],0,'Unsupported hedge equity '+k)
        exact(component['closing'],dec(d['ineffectiveness'])+dec(reserve['closing']),'Hedge current total equity contribution')
        receipt.append(dict(source_import_id=m['source_import_id'],instrument_id=d['id'],relationship_id=m['relationship_id'],derivative_closing=dec(d['closing']),pnl=dec(d['ineffectiveness']),oci=dec(reserve['recognized_oci']),closing_reserve=dec(reserve['closing'])))
    require(mapped==expected,'Actual Hedge derivative/relationship population not completely mapped')
    fingerprints={i['result']['case_fingerprint'] for i in imports.values()}
    require(all(row['source_version'] not in fingerprints or id in target_ids for id,row in tb.items()),'Additional unbound Hedge source posting in actual TB')
    require(all(row.get('source_case_fingerprint') not in fingerprints or id in target_ids for id,row in equity.items()),'Additional unbound Hedge source equity contribution')
    # Bind explicit rows to fresh native output, including no balanced plug in a
    # second line with the same name; source-version labels are never authority.
    lines=report['calculations']['current']['lines']
    for id in (x for m in mapping.values() for x in (m['derivative_tb_id'],m['pnl_tb_id'],m['oci_tb_id'])):
        row=tb[id];exact(lines[row['line']],row['balance'],'Native output mapped statement line')
        require(sum(x['line']==row['line'] for x in tb.values())==1,'Mapped source line contains additional unbound posting')
    return dict(status='validated',route='continuing_first_year_cash_flow',mapping_hash=digest(explicit_mapping),reporting_case_fingerprint=report['case_fingerprint'],source_case_fingerprints={id:i['result']['case_fingerprint'] for id,i in imports.items()},source_ties=receipt)
