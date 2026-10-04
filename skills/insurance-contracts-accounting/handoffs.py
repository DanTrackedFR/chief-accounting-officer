"""Exact-once Insurance receipts into native statement and disclosure owners.

These validators reexecute both actual owners. They do not prepare statements,
select actuarial assumptions, certify checklist compliance or copy postings.
"""
import hashlib
import json
from core_accounting import ReviewRequired, cash, dec
from production import execute

PACKAGE='insurance-contracts-accounting'
NAMESPACE='SUPPLEMENTAL_INSURANCE_CONTRACTS'

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()

def require(condition, message):
    if not condition:raise ReviewRequired(message)

def exact(left,right,label):
    require(cash(left)==cash(right),label+' differs from actual Insurance accounting source')

def rows(values,label):
    require(isinstance(values,list) and bool(values),label+' needs actual nonempty population')
    require(all(isinstance(v,dict) and isinstance(v.get('id'),str) and v['id'] for v in values),'Malformed '+label)
    require(len({v['id'] for v in values})==len(values),'Duplicate '+label)
    return {v['id']:v for v in values}

def owner(package, imp):
    require(isinstance(imp,dict) and isinstance(imp.get('case'),dict) and isinstance(imp.get('result'),dict),'Actual owner case/result required')
    if 'package' in imp:require(imp['package']==package,'Wrong imported accounting owner')
    result=execute(package,imp['case'])
    require(result['status']=='complete','Current independent certification required for '+package)
    require(digest(result)==digest(imp['result']),'Imported result differs from fresh '+package+' execution')
    return result

def same_context(left,right):
    require(all(left.get(k)==right.get(k) for k in ('entity','framework','jurisdiction','period_start','reporting_period','currency')),'Owner entity/framework/period/currency differs')
    require(isinstance(left.get('currency'),str) and bool(left['currency']),'Actual Insurance monetary unit required')

def validate_reporting_handoff(insurance_import, reporting_import, explicit_mapping):
    source=owner(PACKAGE,insurance_import)
    target=owner('financial-statements',reporting_import)
    ic,rc=insurance_import['case'],reporting_import['case'];same_context(ic,rc)
    support=rows(source['calculations']['statement_support'],'Insurance statement support')
    tb=rows(rc['current_tb'],'actual reporting TB');mapping=rows(explicit_mapping,'explicit statement mappings')
    mapped=set();targets=set();line_sums={};source_fingerprint=source['case_fingerprint']
    economics=set()
    for m in mapping.values():
        sid,tid=m.get('source_id'),m.get('tb_id')
        require(sid in support and tid in tb,'Actual source/statement account absent')
        require(sid not in mapped and tid not in targets,'Insurance accounting mapped twice')
        mapped.add(sid);targets.add(tid);s,t=support[sid],tb[tid]
        require(s['currency']==ic['currency'],'Statement source currency differs')
        identity=(s['economic_id'],s['account'])
        require(identity not in economics,'Duplicate Insurance economic balance');economics.add(identity)
        require(t['source_version']==source_fingerprint,'Statement source lineage is stale or wrong owner')
        require(t.get('insurance_source_id')==sid and t.get('insurance_economic_id')==s['economic_id'],'Statement economic source identity differs')
        require(t['category']==s['category'],'Insurance statement classification differs')
        exact(t['balance'],s['signed_balance'],'Insurance TB amount')
        line_sums[t['line']]=line_sums.get(t['line'],dec(0))+dec(s['signed_balance'])
    require(mapped==set(support),'Insurance source population incompletely mapped')
    require(all(r['source_version']!=source_fingerprint or id in targets for id,r in tb.items()),'Additional unbound Insurance source posting')
    require(all(id in targets or not any(k in r for k in ('insurance_source_id','insurance_economic_id')) for id,r in tb.items()),'Additional identified Insurance posting under another owner or source version')
    for line,amount in line_sums.items():
        require(all(id in targets for id,r in tb.items() if r['line']==line),'Unbound posting shares Insurance statement line')
        exact(target['calculations']['current']['lines'][line],amount,'Native statement line')
    return {'status':'validated','source_case_fingerprint':source_fingerprint,'target_case_fingerprint':target['case_fingerprint'],
            'mapping_hash':digest(explicit_mapping),'account_count':len(mapped),'line_amounts':line_sums}

def validate_disclosure_handoff(insurance_import, disclosure_import):
    source=owner(PACKAGE,insurance_import)
    target=owner('disclosure-management',disclosure_import)
    ic,dc=insurance_import['case'],disclosure_import['case'];same_context(ic,dc)
    requirements=rows(dc['requirements'],'actual disclosure requirements')
    imports=rows(dc['imports'],'actual disclosure source owners')
    bound=[];paths=set()
    for r in requirements.values():
        if r['topic_id']!=NAMESPACE:continue
        require(r['owner_import'] in imports,'Disclosure Insurance owner absent')
        imp=imports[r['owner_import']]
        require(imp['package']==PACKAGE,'Insurance requirement routed to another accounting owner')
        require(digest(imp['case'])==digest(ic) and digest(imp['result'])==digest(source),'Disclosure source is different actual Insurance case')
        require(r['owner_requirement'] in source['disclosures_impacted'],'Disclosure requirement not supplied by Insurance owner')
        path=r['result_path'];require(isinstance(path,list) and len(path)>=2 and path[0]=='disclosure_support','Disclosure metric must bind Insurance-specific disclosure schedule')
        key=tuple(path);require(key not in paths,'Duplicate insurance disclosure metric');paths.add(key)
        value=source['calculations']
        for k in path:
            require(isinstance(value,dict) and k in value,'Actual Insurance disclosure metric absent');value=value[k]
        require(not isinstance(value,(dict,list,bool)),'Disclosure requires actual numeric Insurance metric')
        exact(r['amount'],value,'Insurance requirement amount');bound.append(r['id'])
    require(bool(bound),'No actual Insurance disclosure handoff')
    metrics={'premium','acquisition','revenue','service_expense','finance','remaining_coverage','incurred_claims','csm','risk_adjustment','loss_component','premium_deficiency_liability'}
    expected={('disclosure_support','amounts_by_group',gid,k) for gid,g in source['calculations']['disclosure_support']['amounts_by_group'].items() for k in metrics if k in g}
    expected.update(('disclosure_support','amounts_by_group',gid,'rollforwards',name,key) for gid,g in source['calculations']['disclosure_support']['amounts_by_group'].items() for name,bridge in g['rollforwards'].items() for key in bridge)
    require(paths==expected,'Insurance disclosure amount/rollforward population incompletely mapped')
    # A receipt validates the actual qualified requirement population, not a
    # universal Insurance disclosure checklist or regulatory compliance.
    return {'status':'validated','source_case_fingerprint':source['case_fingerprint'],'target_case_fingerprint':target['case_fingerprint'],
            'requirement_ids':bound,'final_checklist_owned_by':'Disclosure Management','compliance_certified':False}
