"""Accounting-function readiness evidence monitor, never an IPO score."""
from governance_accounting import *
AREAS={'historical_reporting','close','policy','technical_accounting','controls','audit','systems_data','calendar','ownership_resources'}
KEYS=('readiness','readiness_source','documents','imports','governance_method','dependencies','dependency_inventory')
def assess(c,claims):
    rs,docs=start(c,'readiness')
    p=c['governance_method']
    if any(flag(p,k) for k in ('score_requested','benchmark_requested','ipo_timing_prediction','sec_status_determination','filing_mechanics')):raise ReviewRequired('Readiness tracking cannot score/predict IPO or determine regulatory obligations')
    texts(p,'venue','issuer_assumptions','adviser_scope_memo')
    if len(rs)!=len(AREAS) or {r['area'] for r in rs}!=AREAS:raise ReviewRequired('Accounting readiness diagnostic areas incomplete')
    independent_population(c,'readiness_source',rs,('area','criterion','evidence_doc','due_date'))
    deps=pack(c,'dependencies','dependency_inventory');by={r['id']:r for r in deps}
    open_items=[];closed=0
    for r in rs:
        enum(r,'area',AREAS);texts(r,'criterion','accountable_owner','assessment_memo','remediation_memo')
        state=enum(r,'state',{'supported','gap','remediated'})
        observed=doc(docs,r['evidence_doc'])['content']
        if not isinstance(observed,dict) or observed['area']!=r['area'] or observed['criterion']!=r['criterion'] or observed['state']!=state:raise ReviewRequired('Readiness observation contradicts controlled source')
        if dec(r['amount'])!=0:raise ReviewRequired('No arbitrary readiness score or monetary proxy')
        if iso(r['due_date'])<iso(c['period_start']):raise ReviewRequired('Readiness planning date outside actual assessed horizon')
        if not isinstance(r['dependency_ids'],list) or len(set(r['dependency_ids']))!=len(r['dependency_ids']):raise ReviewRequired('Duplicate readiness dependencies')
        for id in r['dependency_ids']:
            if id not in by:raise ReviewRequired('Missing readiness dependency')
        if state=='gap':open_items.append('Unresolved accounting readiness gap; qualified owner remediation required')
        elif not flag(observed,'criterion_evidenced'):raise ReviewRequired('Unsupported staffing/system/control readiness conclusion')
        else:closed+=1
        if state=='remediated' and not flag(observed,'remediation_retested'):raise ReviewRequired('Remediation requires repeatable evidence')
    if set(by)!={id for r in rs for id in r['dependency_ids']}:raise ReviewRequired('Orphan/unreviewed readiness dependency')
    for d in deps:
        texts(d,'scope_memo','accountable_owner','dependency_kind')
        enum(d,'dependency_kind',{'accounting_owner','qualified_external'})
        if d['dependency_kind']=='accounting_owner':actual_owner(c,d['owner_import'])
        else:
            e=doc(docs,d['evidence_doc'])['content']
            if not isinstance(e,dict) or e.get('dependency_resolved') is not True:open_items.append('Qualified external readiness dependency remains unresolved')
    review_release(c,KEYS)
    return output(c,'Accounting-function readiness evidence workpaper reviewed',dict(area_count=len(rs),supported_area_count=closed,unresolved_gap_count=len(open_items),ipo_readiness_score_produced=False),['Qualified accounting-function assessment only. No IPO success/timetable, SEC compliance, generic staffing target, audit opinion or filing conclusion. Actual market/jurisdiction obligations remain separately verified.'],open_items)
