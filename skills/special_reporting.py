"""Bounded special-reporting controls; governed workpapers, never filings or valuation."""
from presentation_accounting import *
from urllib.parse import urlparse
import hashlib,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def mapped_knowledge(package,framework=None):
    m=json.loads((ROOT/'skills/SPECIAL-REPORTING-KNOWLEDGE-MAP.json').read_text())['packages'][package]
    claims=[];documents=[]
    manifest=json.loads((ROOT/'knowledge/phase-2d-topic-manifest.json').read_text())['topics']
    for t in m['topics']:
        current=next(x for x in manifest if x['topic_id']==t['topic_id'])
        if current['status']!='APPROVED':raise ReviewRequired('Canonical approval changed')
        p=ROOT/t['register']
        if hashlib.sha256(p.read_bytes()).hexdigest()!=t['sha256']:raise ReviewRequired('Immutable canonical register changed')
        actual=json.loads(p.read_text())['claims']
        for x in actual:
            if framework is not None and x['framework']!=framework:continue
            if x.get('approval_review',{}).get('result')!='PASS':raise ReviewRequired('Mapped claim lacks individual approval')
            claims.append(dict(topic_id=t['topic_id'],claim_id=x['claim_id'],proposition=x['proposition'],references=x.get('paragraph_references',[]),reference_confidence=x['reference_confidence'],evidence_status=x['evidence_status'],audit_required=x['audit_required'],limitations=x['limitations'],effective_period=x['effective_period'],entity_scope=x['entity_scope']))
        for d in t['knowledge_documents']+[{'path':t['register'],'sha256':t['sha256']}]:
            if hashlib.sha256((ROOT/d['path']).read_bytes()).hexdigest()!=d['sha256']:raise ReviewRequired('Immutable governed document changed')
            documents.append(dict(topic_id=t['topic_id'],**d))
    return claims,documents

def start(c,key,allowed=()):
    if key in {'adjustments','filing_lines'}:
        common(c,key,'accounting_policy','gl','imports');policy(c,c['accounting_policy']);texts(c,'preparer','entity','jurisdiction','case_id')
        if c['applicability_review']['exceptions']:raise ReviewRequired('Unresolved applicability overlay')
        rs=rows(c[key]);inventory(c,'source_inventory',rs)
        for r in rs:
            approval(r,c)
            if r['source_entity']!=c['entity'] or r['source_framework']!=c['framework']:raise ReviewRequired('Source identity/framework mismatch')
    else:rs=begin(c,key)
    imports(c,allowed)
    if c.get('requested_action','workpaper')!='workpaper':raise ReviewRequired('Only accounting workpaper support is executable')
    return rs

def method(c,key,target):
    return qualified(c,c[key],target)

def no_posting(c,title,calcs,judgments,limitations):
    r=complete(c,title,calcs,[],judgments);r['uncertainties']=limitations
    return r

def checked_rule(c,r,authority):
    policy(c,r);texts(r,'authority_url','rule_version','checked_on','jurisdiction','issuer_type','rule_memo')
    u=urlparse(r['authority_url'])
    if u.scheme!='https' or u.hostname not in authority:raise ReviewRequired('Current authoritative issuer-rule evidence required')
    if r['jurisdiction']!=c['jurisdiction'] or not iso(c['reporting_period'])<=iso(r['checked_on'])<=iso(c['execution_date']):raise ReviewRequired('Rule jurisdiction or current-check date mismatch')
    if r['checked_on']!=c['execution_date']:raise ReviewRequired('Current-rule review must be refreshed for execution date')
    if r.get('case_id')!=c['case_id']:raise ReviewRequired('Current rule evidence must cover exact case')
    if not flag(r,'current_authority_verified'):raise ReviewRequired('Authoritative actual-case rule check unresolved')


def exact(a,b,label):
    if dec(a)!=dec(b):raise ReviewRequired(label+' exact reconciliation failed')


def typed_statement(c,r,current=True,full_entity=True):
    """Controlled supplied statement population, independently bound to its own GL."""
    approval(r,c);texts(r,'source_entity','source_framework','source_version','metric','definition','units')
    if r['source_entity']!=c['entity'] or r['source_framework']!=c['framework']:raise ReviewRequired('Statement identity/framework mismatch')
    span=r['source_period']
    if not isinstance(span,list) or len(span)!=2 or iso(span[0])>iso(span[1]):raise ReviewRequired('Invalid statement period')
    if current and span!=[c['period_start'],c['reporting_period']]:raise ReviewRequired('Current source span mismatch')
    if not current and iso(span[1])>=iso(c['period_start']):raise ReviewRequired('Comparative source overlaps current period')
    lines=rows(r['lines'],False);inventory(r,'line_inventory',lines);total=ZERO
    for l in lines:
        approval(l,c);texts(l,'account','source_memo')
        total+=dec(l['gl_amount'])*(-1 if flag(l,'credit_nature') else 1)
        exact(l['amount'],dec(l['gl_amount'])*(-1 if l['credit_nature'] else 1),'Statement source line')
    exact(r['amount'],total,'Statement subtotal to independently approved GL lines')
    for imp in c['imports']:
        if imp['package']=='financial-statements' and current and full_entity:
            values=imp['result']['calculations']['current']
            if r['metric'] not in values:raise ReviewRequired('Statement owner metric unavailable in bounded adapter')
            exact(r['amount'],values[r['metric']],'Actual completed statement owner')
    return dec(r['amount'])


def comparable_spans(current,prior):
    a,b=map(iso,current);x,y=map(iso,prior)
    if (a.month,a.day,b.month,b.day)!=(x.month,x.day,y.month,y.day) or a.year-x.year!=1 or b.year-y.year!=1:
        raise ReviewRequired('Comparative period must use same prior-year calendar span; other fiscal/transition bases need separate method')
