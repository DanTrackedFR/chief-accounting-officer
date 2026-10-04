"""Management design/evidence readiness, never operating-effectiveness opinion."""
from final_batch_accounting import *
KEYS=('control_rows','control_source','risk_source','occurrences','occurrence_inventory','occurrence_source','deficiencies','deficiency_inventory','documents','document_inventory','imports','owner_links','owner_link_inventory','governance_method')
LIMITS=['Control design and evidence readiness only; no operating-effectiveness, audit/ICFR opinion, management certification or SOX compliance conclusion.','Actual legal applicability, risk severity and precision remain qualified judgments; an RCM or test plan is not testing evidence.']
def assess(c,claims):
    rs,d=start(c,'control_rows');original(c,'control_source',rs)
    risks=c['risk_source'];source(c,risks);inventory(risks,'inventory',rows(risks['records'],False));byrisk={r['id']:r for r in risks['records']}
    scope=snapshot(c,d,risks['source_doc'])
    if digest(scope['records'])!=digest(risks['records']) or scope['inventory']!=risks['inventory']:raise ReviewRequired('Reporting/fraud risk scope differs from independent source')
    occurrences=pack(c,'occurrences','occurrence_inventory');original(c,'occurrence_source',occurrences)
    defects=pack(c,'deficiencies','deficiency_inventory');open_items=[];covered=set();semantic=[];seen_occ=set()
    regime=snapshot(c,d,c['governance_method']['applicability_doc'])
    if regime['entity']!=c['entity'] or regime['jurisdiction']!=c['jurisdiction'] or regime['period']!=[c['period_start'],c['reporting_period']] or regime['checked_on']!=c['execution_date']:raise ReviewRequired('Current actual control-regime review required')
    texts(regime,'issuer_facts','qualified_applicability_memo','operative_requirements','regime')
    if regime['requested_conclusion']!='design_evidence_readiness':raise ReviewRequired('Readiness cannot certify applicability or effectiveness')
    for r in rs:
        texts(r,'objective','assertion','risk_id','process','accountable_owner','review_person','owner_person','precision_memo','exception_route','test_attributes','control_key','frequency')
        if r['risk_id'] not in byrisk:raise ReviewRequired('Unmapped reporting risk')
        risk=byrisk[r['risk_id']];texts(risk,'misstatement','assertion','process','fraud_rationale');exact_fields(r,risk,('assertion','process'),'Reporting risk')
        covered.add(r['risk_id']);semantic.append(r['control_key'])
        if r['owner_person']==r['review_person']:raise ReviewRequired('Person-level control self review')
        enum(r,'kind',{'manual','management_review','automated'});enum(r,'timing',{'preventive','detective'})
        e=snapshot(c,d,r['design_doc']);exact_fields(e,r,('control_key','objective','assertion','risk_id','owner_person','review_person','kind','timing','frequency'),'Control design')
        if e['period']!=[c['period_start'],c['reporting_period']] or e['rcm_version']!=r['rcm_version']:raise ReviewRequired('Stale RCM design')
        if not flag(e,'precision_evidenced') or not flag(e,'independent_expectation') or not flag(e,'ipe_reconciled'):raise ReviewRequired('Precision/expectation/IPE not evidenced')
        exact(e['threshold'],r['threshold'],'Approved review precision');nonnegative(r['threshold'])
        if not iso(c['period_start'])<=iso(e['expectation_set_on'])<=iso(e['data_available_on'])<=iso(c['execution_date']):raise ReviewRequired('Expectation chronology outside controlled current period')
        if r['kind']=='automated':
            texts(e,'configuration_version','access_evidence','change_evidence','negative_test_evidence')
            if not flag(e,'system_dependency_validated'):raise ReviewRequired('Automated dependency evidence missing')
        if not isinstance(e['expected_occurrence_ids'],list) or len(e['expected_occurrence_ids'])!=len(set(e['expected_occurrence_ids'])):raise ReviewRequired('Occurrence inventory malformed')
        actual=[o for o in occurrences if o['control_id']==r['id']]
        enum(r,'frequency',{'monthly','quarterly','annual'})
        from calendar import monthrange
        start_date=iso(c['period_start']);end_date=iso(c['reporting_period']);dates_expected=set()
        for year in range(start_date.year,end_date.year+1):
            for month in range(1,13):
                end=date(year,month,monthrange(year,month)[1])
                if start_date<=end<=end_date and (r['frequency']=='monthly' or (r['frequency']=='quarterly' and month%3==0) or (r['frequency']=='annual' and month==12)):dates_expected.add(end.isoformat())
        if {o['period_date'] for o in actual}!=dates_expected or len(actual)!=len(dates_expected):raise ReviewRequired('Control frequency/full-period occurrence coverage failed')
        if set(e['expected_occurrence_ids'])!={o['id'] for o in actual}:raise ReviewRequired('Full expected control occurrence population omitted')
        for o in actual:
            seen_occ.add(o['id']);period_date(c,o['period_date']);enum(o,'state',{'ready','missing','failed'})
            if not iso(o['period_date'])<=iso(o['due_date'])<=iso(c['execution_date']):raise ReviewRequired('Control occurrence deadline chronology invalid')
            oe=snapshot(c,d,o['evidence_doc']);exact_fields(oe,o,('control_id','state','due_date','period_date'),'Occurrence evidence')
            if o['state']=='ready' and (not flag(oe,'attributes_present') or not flag(oe,'exceptions_followed_up')):raise ReviewRequired('Signature is not substantive control evidence')
            if o['state']!='ready':open_items.append('Control occurrence evidence unresolved')
        if flag(e,'sod_conflict') and not flag(e,'independent_compensating_population_reviewed'):open_items.append('Action-level segregation conflict remains unresolved')
    unique(semantic,'control key')
    if seen_occ!={o['id'] for o in occurrences}:raise ReviewRequired('Orphan occurrence')
    if covered!=set(byrisk):open_items.append('Uncovered reporting/fraud risks require control design')
    for r in defects:
        if r['control_id'] not in {x['id'] for x in rs}:raise ReviewRequired('Orphan deficiency')
        e=snapshot(c,d,r['assessment_doc']);exact_fields(e,r,('control_id','severity','status'),'Qualified deficiency')
        texts(e,'regime_memo','severity_rationale','potential_exposure_memo','aggregation_memo','root_cause','remediation_owner')
        enum(r,'status',{'open','closed'})
        if r['status']=='closed' and (not flag(e,'independent_retest_passed') or not flag(e,'historical_exposure_reviewed')):raise ReviewRequired('Ticket closure is not retested remediation')
        if r['status']=='open':open_items.append('Qualified deficiency remediation remains open')
    review_release(c,KEYS)
    return finalize(c,'Accounting control design and evidence-readiness workpaper; no effectiveness conclusion',dict(controls=len(rs),risks=len(byrisk),occurrences=len(occurrences),unresolved_occurrences=sum(o['state']!='ready' for o in occurrences),deficiencies=len(defects)),LIMITS,open_items)
