"""Batch 30/48/49/50 helpers on the existing governed production envelope."""
from governance_accounting import *
import governance_accounting as prior

BATCH=('defined-benefit-opeb','accounting-controls-icfr','accounting-systems-data-integrity','accounting-operating-model')
PRACTICE=BATCH[1:]
def mapped_knowledge(package,framework):
    m=json.loads((ROOT/'skills/FINAL-BATCH-KNOWLEDGE-MAP.json').read_text())['packages'][package]
    manifest=json.loads((ROOT/'knowledge/phase-2d-topic-manifest.json').read_text())['topics'];claims=[];docs=[]
    for t in m['topics']:
        actual=next(x for x in manifest if x['topic_id']==t['topic_id'])
        if actual['status']!='APPROVED' or not set(t['capability_ids'])<=set(actual['capability_ids']):raise ReviewRequired('Frozen approval/capability changed')
        register=ROOT/t['register']
        if hashlib.sha256(register.read_bytes()).hexdigest()!=t['sha256']:raise ReviewRequired('Frozen claim register changed')
        for x in json.loads(register.read_text())['claims']:
            if x['framework'] not in {framework,'OTHER'}:continue
            if x.get('approval_review',{}).get('result')!='PASS':raise ReviewRequired('Mapped claim lacks approval')
            claims.append(dict(topic_id=t['topic_id'],claim_id=x['claim_id'],proposition=x['proposition'],references=x.get('paragraph_references',[]),reference_confidence=x['reference_confidence'],evidence_status=x['evidence_status'],audit_required=x['audit_required'],limitations=x['limitations'],effective_period=x['effective_period'],entity_scope=x['entity_scope']))
        for d in t['knowledge_documents']+[dict(path=t['register'],sha256=t['sha256'])]:
            if hashlib.sha256((ROOT/d['path']).read_bytes()).hexdigest()!=d['sha256']:raise ReviewRequired('Frozen canonical document changed')
            docs.append(dict(topic_id=t['topic_id'],**d))
    return claims,docs

def start(c,key,accounting=False):
    rs=begin(c,key);population(c,rs,[abs(dec(r['amount'])) for r in rs])
    if not rs:raise ReviewRequired('Actual nonempty governed source population required')
    if c['requested_action'] not in ({'workpaper','accounting'} if accounting else {'workpaper'}):raise ReviewRequired('Unsupported external action or certification')
    for imp in rows(c['imports']):
        if imp.get('case',{}).get('jurisdiction')!=c['jurisdiction']:raise ReviewRequired('Imported jurisdiction mismatch')
    imports(c,set(PACKAGES)-{'government-grants','borrowing-costs','investment-property','inventory-cost',c['package']})
    p=qualified(c,c['governance_method'],'Bounded final batch')
    texts(p,'entity','jurisdiction','checked_on','current_requirements_memo','qualification_memo')
    if p['entity']!=c['entity'] or p['jurisdiction']!=c['jurisdiction'] or p['checked_on']!=c['execution_date']:raise ReviewRequired('Current actual-case scope required')
    for k in ('external_write','legal_certification','audit_opinion','regulatory_compliance','authority_override'):
        if flag(p,k):raise ReviewRequired('Unsupported authority or mutation')
    for k in ('posting_requested','forecast_requested','score_requested','benchmark_requested','ipo_timing_prediction','sec_status_determination','filing_mechanics','evidence_sufficiency_asserted','auditor_independence_determined','confirmation_control_requested','audit_adjustments_requested','auditor_signoff_requested','autonomous_policy_selection','transition_calculation_requested','overwrite_history','invented_citations','universal_checklist','compliance_certification','prior_year_rollforward_only','filing_requested','comparative_change_requested','budgeting','forecasting','investment_analysis','commercial_planning','generic_bi','manufactured_explanations','automatic_gl_correction'):
        if k in p and flag(p,k):raise ReviewRequired('Unsupported inherited authority or scope expansion')
    d=evidence(c);links=pack(c,'owner_links','owner_link_inventory')
    used_docs={r[k] for r in rs for k in {'defined-benefit-opeb':('statement_doc',),'accounting-controls-icfr':('design_doc',),'accounting-systems-data-integrity':('target_doc',),'accounting-operating-model':('evidence_doc',)}[c['package']]}
    seen=set();allowed_fields={'defined-benefit-opeb':{'net_liability','gl_net_liability','pnl_expense','oci_loss'},'accounting-controls-icfr':{'threshold'},'accounting-systems-data-integrity':{'gl_amount','statement_amount'},'accounting-operating-model':{'controlled_kpi_rate'}}[c['package']]
    for link in links:
        imp=actual_owner(c,link['owner_import'])
        if imp['id'] in seen:raise ReviewRequired('Owner result must reconcile exactly once')
        seen.add(imp['id']);path=link['result_path']
        if not isinstance(path,list) or not path or any(not isinstance(k,str) or not k for k in path):raise ReviewRequired('Actual numeric owner result path required')
        if c['package']=='accounting-operating-model' and (imp['package']!='management-accounting-analytics' or path!=['on_time_reconciliation_rate'] or not any(r.get('kpi_owner_import')==imp['id'] and r['evidence_doc']==link['evidence_doc'] for r in rs)):raise ReviewRequired('Operating-model KPI must use named actual accounting analytics owner')
        value=imp['result']['calculations']
        for k in path:
            if not isinstance(value,dict) or k not in value:raise ReviewRequired('Owner fact absent')
            value=value[k]
        if isinstance(value,(dict,list,bool)) or value is None:raise ReviewRequired('Numeric owner fact required')
        if link['evidence_doc'] not in used_docs:raise ReviewRequired('Owner must reconcile an actual used source assertion')
        blob=doc(d,link['evidence_doc'])['content'];field=link['evidence_field']
        if field not in allowed_fields or not isinstance(blob,dict) or field not in blob:raise ReviewRequired('Unsupported source-to-owner binding')
        if c['package'] in BATCH[:3] and imp['package'] in set(prior.BATCH)|set(PRACTICE)|{'sec-filing-accounting','alternative-performance-measures'}:raise ReviewRequired('Governance facts cannot become monetary accounting authority')
        exact(link['amount'],value,'Owner assertion');exact(blob[field],value,'Source/owner contradiction')
    if seen!={i['id'] for i in c['imports']}:raise ReviewRequired('Unreconciled imported owner result')
    return rs,d

def original(c,key,rs):
    """Bind all tracker fields to independently frozen original source records."""
    p=c[key];source(c,p);texts(p,'population_memo','extract_version');inventory(p,'inventory',rows(p['records']))
    if digest(rs)!=digest(p['records']):raise ReviewRequired('Original source and tracker population/content differ')

def snapshot(c,d,id,currency=None):
    r=doc(d,id)
    if currency is not None and r['currency']!=currency:raise ReviewRequired('Evidence currency mismatch')
    return r['content']

def exact_fields(a,b,keys,label):
    if any(a[k]!=b[k] for k in keys):raise ReviewRequired(label+' source facts contradict tracker')

def unique(values,label):
    if len(values)!=len(set(values)):raise ReviewRequired('Aliased duplicate '+label)

def period_date(c,value):return inperiod(c,value)

def dated_review(c,r,fields):
    source(c,r);texts(r,*fields)
    if r['checked_on']!=c['execution_date']:raise ReviewRequired('Review is not current at execution')

def retained_owner(c,r,allowed):
    i=actual_owner(c,r['owner_import'])
    if i['package'] not in allowed:raise ReviewRequired('Wrong completed workflow owner')
    return i

def finalize(c,title,calcs,limits,open_items=(),entries=()):
    r=complete(c,title,calcs,list(entries),['Qualified source judgments remain separate from calculations'])
    r['uncertainties']=limits;r['open_items']=list(open_items);return r
