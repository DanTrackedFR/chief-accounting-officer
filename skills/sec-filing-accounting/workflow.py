"""US filer accounting readiness controls, never a legal or technical filing certificate."""
from special_reporting import *

ALLOWED={'financial-statements','alternative-performance-measures','accounting-changes','earnings-per-share','segment-reporting','subsequent-events'}
PAYLOAD=('filer','rule','calendar','statements','statement_inventory','filing_lines','filing_line_inventory','tags','tag_inventory','issues','issue_inventory','queries','query_inventory','changes','change_inventory','imports')

def release_fingerprint(c):
    return hashlib.sha256(json.dumps({k:c[k] for k in PAYLOAD},sort_keys=True,default=str).encode()).hexdigest()

def assess(c,claims):
    rs=start(c,'filing_lines',ALLOWED)
    if c['jurisdiction']!='US' or c['framework'] not in {'US_GAAP','IFRS'}:raise ReviewRequired('US SEC accounting-support scope only')
    f=c['filer'];approval(f,c);texts(f,'registration_evidence','filer_classification_evidence','status_memo','form','issuer_type','filing_kind')
    if not flag(f,'registrant') or not flag(f,'qualified_status_reviewed'):raise ReviewRequired('Actual registrant/form determination required')
    issuer=enum(f,'issuer_type',{'domestic','fpi'});kind=enum(f,'filing_kind',{'annual','interim'})
    expected={'domestic':{'annual':'10-K','interim':'10-Q'},'fpi':{'annual':'20-F','interim':'6-K'}}[issuer][kind]
    if f['form']!=expected or (issuer=='domestic' and c['framework']!='US_GAAP'):raise ReviewRequired('Filer/form/framework confusion; no automatic domestic route for FPI')
    if any(flag(f,k) for k in ('amended_filing','special_form','compliance_certification','officer_certification','audit_opinion_requested','edgar_submission_requested')):raise ReviewRequired('Legal/filing/certification or special-form route is not executable')
    r=c['rule'];checked_rule(c,r,{'www.sec.gov','sec.gov'})
    if any(r[k]!=f[k] for k in ('issuer_type','form','filing_kind')):raise ReviewRequired('Current authoritative form/filer rule mismatch')
    texts(r,'deadline_evidence','taxonomy_version','entry_point','form_instructions_memo','annual_interim_memo','statement_requirements_memo')
    cal=c['calendar'];approval(cal,c);texts(cal,'deadline_memo','audit_dependency_memo','board_dependency_memo')
    if iso(cal['due_date'])!=iso(r['verified_due_date']):raise ReviewRequired('Calendar cannot invent statutory deadline')
    if not iso(c['reporting_period'])<=iso(cal['internal_ready_date'])<=iso(cal['due_date']):raise ReviewRequired('Internal readiness/date sequence invalid')
    # A qualified 6-K case remains disclosure support; never impose 10-Q or a
    # mechanical quarterly deadline on the FPI.
    if issuer=='fpi' and kind=='interim' and not flag(r,'fpi_interim_basis_verified'):raise ReviewRequired('Actual 6-K obligation facts/current instructions required')
    if issuer=='domestic' and kind=='interim' and enum(f,'quarter',{'Q1','Q2','Q3'}) not in {'Q1','Q2','Q3'}:raise ReviewRequired('10-Q annual fourth-quarter confusion')
    sources=rows(c['statements'],False);inventory(c,'statement_inventory',sources);by={s['id']:s for s in sources};values={}
    for s in sources:values[s['id']]=typed_statement(c,s,flag(s,'current'))
    for s in sources:
        basis={'profit':'duration','revenue':'duration','expenses':'duration','oci':'duration','cash':'instant','assets':'instant','liabilities':'instant','closing_equity':'instant'}
        if s['metric'] not in basis or s['period_kind']!=basis[s['metric']]:raise ReviewRequired('Unsupported source metric or temporal semantics')
        if not flag(s,'current'):comparable_spans([c['period_start'],c['reporting_period']],s['source_period'])
    if not any(flag(s,'current') for s in sources) or not any(not flag(s,'current') for s in sources):raise ReviewRequired('Current and comparative statement populations required')
    seen=set();filing={}
    for a in rs:
        id=a['statement_id']
        if id not in by or id in seen:raise ReviewRequired('Missing/duplicated statement-to-filing source')
        s=by[id];texts(a,'metric','units','form_section','tieout_memo')
        if a['source_period']!=s['source_period'] or a['metric']!=s['metric'] or a['units']!=s['units']:raise ReviewRequired('Source-to-filing semantic/period mismatch')
        exact(a['amount'],values[id],'Human filing/source value');seen.add(id);filing[a['id']]=a
    if seen!=set(by):raise ReviewRequired('Complete source-to-filing population required')
    population(c,rs,[abs(dec(a['amount'])) for a in rs])
    tags=rows(c['tags']);inventory(c,'tag_inventory',tags);tagged=set()
    if flag(r,'inline_xbrl_required') and not tags:raise ReviewRequired('Required Inline XBRL accounting review absent')
    for t in tags:
        approval(t,c);texts(t,'filing_line_id','taxonomy_version','entry_point','concept','expected_concept','context_entity','unit','expected_unit','extension_memo','dimension_memo')
        id=t['filing_line_id']
        if id not in filing or id in tagged:raise ReviewRequired('Missing/duplicate tag source')
        a=filing[id]
        if t['taxonomy_version']!=r['taxonomy_version'] or t['entry_point']!=r['entry_point'] or t['concept']!=t['expected_concept']:raise ReviewRequired('Wrong taxonomy/concept mapping')
        if t['context_entity']!=c['entity'] or t['context_period']!=a['source_period'] or t['unit']!=t['expected_unit'] or t['unit']!=a['units']:raise ReviewRequired('XBRL context/entity/unit mismatch')
        if t['dimensions']!=t['expected_dimensions'] or t['period_kind']!=t['expected_period_kind'] or t['period_kind']!=by[a['statement_id']]['period_kind']:raise ReviewRequired('XBRL period/dimension mismatch')
        if not flag(t,'mapping_reviewed') or not flag(t,'extension_reviewed'):raise ReviewRequired('Unresolved taxonomy/extension accounting mapping')
        scale=t['scale'];sign=t['sign']
        if type(scale) is not int or not -12<=scale<=12 or type(sign) is not int or sign not in (-1,1):raise ReviewRequired('Invalid reviewed tag scale/sign')
        if scale!=t['expected_scale'] or sign!=t['expected_sign']:raise ReviewRequired('Scale/sign differ from qualified mapping')
        exact(t['display_amount'],a['amount'],'Rendered filing amount');exact(dec(t['raw_value'])*Decimal(10)**scale*sign,a['amount'],'Machine tag amount')
        tagged.add(id)
    if flag(r,'inline_xbrl_required') and tagged!=set(filing):raise ReviewRequired('Tag source population incomplete')
    review=c['filing_review'];approval(review,c)
    for k in ('disclosure_controls_complete','annual_interim_checklist_complete','source_completeness_reviewed','narrative_consistency_reviewed','validation_errors_resolved','warnings_resolved','legal_ir_auditor_review_complete','apm_scope_reviewed'):
        if not flag(review,k):raise ReviewRequired('Filing-accounting control unresolved: '+k)
    if flag(review,'apm_present'):
        apms=[i for i in c['imports'] if i['package']=='alternative-performance-measures']
        if len(apms)!=1:raise ReviewRequired('Exact completed APM owner required for published alternative measures')
        for k,v in apms[0]['result']['calculations']['measures'].items():exact(review['apm_amounts'][k],v['adjusted_measure'],'Filing/APM owner')
    elif any(i['package']=='alternative-performance-measures' for i in c['imports']):raise ReviewRequired('APM import contradicts filing scope')
    issues=rows(c['issues']);inventory(c,'issue_inventory',issues)
    for i in issues:
        approval(i,c);texts(i,'accounting_owner','resolution_memo')
        if not flag(i,'closed') or not flag(i,'dependent_outputs_refreshed'):raise ReviewRequired('Open filing accounting issue')
    queries=rows(c['queries']);inventory(c,'query_inventory',queries)
    for q in queries:
        approval(q,c);texts(q,'original_filing_evidence','original_period_memo','question_memo','response_workpaper','correction_assessment','legal_review','response_due_evidence')
        if not flag(q,'evidence_reproduced') or not flag(q,'accounting_owner_reviewed') or flag(q,'submission_requested'):raise ReviewRequired('Query evidence/ownership incomplete or unauthorized submission')
    changes=rows(c['changes']);inventory(c,'change_inventory',changes)
    for x in changes:
        approval(x,c);texts(x,'change_memo','impacted_line_id','reapproval_memo')
        if x['impacted_line_id'] not in filing or not all(flag(x,k) for k in ('source_refreshed','rendering_refreshed','tags_refreshed','approvals_reopened')):raise ReviewRequired('Late change invalidates filing/accounting sign-off')
    if review['reviewed_release_fingerprint']!=release_fingerprint(c):raise ReviewRequired('Source/filing/tags changed after release review; reopen controls')
    return no_posting(c,'US registrant filing-accounting support workpaper reconciled',dict(statement_line_count=len(rs),tag_count=len(tags),resolved_issue_count=len(issues),query_workpaper_count=len(queries),statutory_deadline_calculated=False,regulator_validation_certified=False),['Actual qualified domestic/FPI and annual/interim workpaper; current authoritative rule/taxonomy check remains case-specific'],['Accounting support only: no securities-law advice, EDGAR filing, officer certification, audit opinion, regulatory compliance or regulator-valid XBRL assertion. Verified calendar dates are supplied rule evidence, not computed obligations.'])
