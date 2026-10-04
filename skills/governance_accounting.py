"""Bounded management governance reuses the governed accounting runtime."""
from special_reporting import *
from production import PACKAGES

BATCH=('ipo-accounting-readiness','audit-support-pbc','accounting-policy-memo-governance','disclosure-management','management-accounting-analytics')

def mapped_knowledge(package,framework):
    m=json.loads((ROOT/'skills/GOVERNANCE-KNOWLEDGE-MAP.json').read_text())['packages'][package]
    manifest=json.loads((ROOT/'knowledge/phase-2d-topic-manifest.json').read_text())['topics'];claims=[];docs=[]
    for t in m['topics']:
        actual=next(x for x in manifest if x['topic_id']==t['topic_id'])
        if actual['status']!='APPROVED' or not set(t['capability_ids'])<=set(actual['capability_ids']):raise ReviewRequired('Mapped canonical approval/capability changed')
        register=ROOT/t['register']
        if hashlib.sha256(register.read_bytes()).hexdigest()!=t['sha256']:raise ReviewRequired('Frozen canonical register changed')
        for x in json.loads(register.read_text())['claims']:
            if x['framework'] not in {framework,'OTHER'}:continue
            if x.get('approval_review',{}).get('result')!='PASS':raise ReviewRequired('Mapped claim not independently approved')
            claims.append(dict(topic_id=t['topic_id'],claim_id=x['claim_id'],proposition=x['proposition'],references=x.get('paragraph_references',[]),reference_confidence=x['reference_confidence'],evidence_status=x['evidence_status'],audit_required=x['audit_required'],limitations=x['limitations'],effective_period=x['effective_period'],entity_scope=x['entity_scope']))
        for d in t['knowledge_documents']+[dict(path=t['register'],sha256=t['sha256'])]:
            if hashlib.sha256((ROOT/d['path']).read_bytes()).hexdigest()!=d['sha256']:raise ReviewRequired('Frozen knowledge document changed')
            docs.append(dict(topic_id=t['topic_id'],**d))
    return claims,docs

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()

def pack(c,key,inv,empty=True):
    rs=rows(c[key],empty);inventory(c,inv,rs)
    for r in rs:source(c,r)
    return rs

def evidence(c):
    rs=pack(c,'documents','document_inventory');out={}
    for r in rs:
        texts(r,'source_system','query_version','parameters','snapshot_version','currency')
        if r['snapshot_version']!=r['version'] or r['as_of']!=c['reporting_period']:raise ReviewRequired('Evidence source snapshot is stale')
        if r['content_hash']!=digest(r['content']):raise ReviewRequired('Evidence bytes differ from reviewed source digest')
        if not isinstance(r['content'],(dict,list,str)):raise ReviewRequired('Unsupported evidence content')
        out[r['id']]=r
    return out

def doc(d,id):
    if id not in d:raise ReviewRequired('Evidence source missing from independent population')
    return d[id]

def actual_owner(c,id):
    matches=[i for i in c['imports'] if i['id']==id]
    if len(matches)!=1:raise ReviewRequired('Actual completed accounting owner required')
    return matches[0]

def accounting_owner(c,id):
    imp=actual_owner(c,id)
    if imp['package'] in set(BATCH)|{'sec-filing-accounting','alternative-performance-measures','accounting-controls-icfr','accounting-systems-data-integrity','accounting-operating-model'}:raise ReviewRequired('Governance/filing/control facts cannot authorize substantive accounting assertions')
    return imp

def owner_assertion(c,r):
    imp=accounting_owner(c,r['owner_import']);path=r['result_path']
    if not isinstance(path,list) or not path or any(not isinstance(x,str) or not x for x in path):raise ReviewRequired('Controlled owner result path required')
    value=imp['result']['calculations']
    for k in path:
        if not isinstance(value,dict) or k not in value:raise ReviewRequired('Owner result assertion is not available')
        value=value[k]
    if isinstance(value,(dict,list,bool)) or value is None:raise ReviewRequired('Only actual numeric owner facts may be imported')
    exact(r['amount'],value,'Completed accounting owner fact')
    return dec(value)

def start(c,key):
    rs=begin(c,key);population(c,rs,[abs(dec(r['amount'])) for r in rs])
    if c.get('requested_action')!='workpaper':raise ReviewRequired('Only bounded management workpaper support is executable')
    for imp in rows(c['imports']):
        if imp.get('case',{}).get('jurisdiction')!=c['jurisdiction']:raise ReviewRequired('Imported owner jurisdiction mismatch')
    blocked={'government-grants','borrowing-costs','investment-property'}
    # Inventory now has governed production authority. Actual complete current
    # imports still reexecute the native owner and retain all certification gates.
    allowed=set(PACKAGES)-blocked-{c['package']}
    imports(c,allowed)
    p=qualified(c,c['governance_method'],'Bounded management governance')
    if any(flag(p,k) for k in ('posting_requested','legal_certification','audit_opinion','regulatory_compliance','forecast_requested','authority_override')):raise ReviewRequired('Unsupported accounting/legal/audit/FP&A assertion')
    texts(p,'scope_memo','boundary_memo','current_requirements_memo','qualification_memo')
    if p['entity']!=c['entity'] or p['jurisdiction']!=c['jurisdiction'] or p['checked_on']!=c['execution_date']:raise ReviewRequired('Actual-case current governance method required')
    return rs,evidence(c)

def independent_population(c,key,rs,fields):
    p=c[key];source(c,p);texts(p,'population_memo','extract_version')
    inventory(p,'inventory',rows(p['records']))
    original={r['id']:r for r in p['records']}
    if set(original)!={r['id'] for r in rs}:raise ReviewRequired('Tracker differs from actual independently frozen source population')
    for r in rs:
        frozen=set(fields)|({'amount'} if 'amount' in r else set())|({'accountable_owner'} if 'accountable_owner' in r else set())
        if any(r[k]!=original[r['id']][k] for k in frozen):raise ReviewRequired('Source identity/content changed in tracker')
    return original

def review_release(c,keys):
    r=c['release_review'];source(c,r);texts(r,'review_memo')
    if r['payload_fingerprint']!=digest({k:c[k] for k in keys}):raise ReviewRequired('Source/artifact changed after release review')

def output(c,title,calcs,limits,open_items=()):
    r=no_posting(c,title,calcs,['Qualified management judgments remain distinct from calculated facts'],limits)
    r['open_items']=list(open_items)
    return r

def comparison(c,span):comparable_spans([c['period_start'],c['reporting_period']],span)
