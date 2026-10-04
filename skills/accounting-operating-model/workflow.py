"""Actual accounting service/team governance, not headcount or corporate strategy."""
from final_batch_accounting import *
KEYS=('processes','process_source','team','team_inventory','team_source','roadmap','roadmap_inventory','documents','document_inventory','imports','owner_links','owner_link_inventory','governance_method')
LIMITS=['Accounting operating-model workpaper with qualified maturity judgments, not mandatory organization or staffing benchmarks.','No hiring/firing, layoffs, employment-law advice, IPO readiness score, automation ROI or duplicated accounting KPI calculations.','Actual critical dependencies, retained accountability and measured capacity remain distinct from recommended target practices.']
def assess(c,claims):
    rs,d=start(c,'processes');original(c,'process_source',rs)
    team=pack(c,'team','team_inventory',False);original(c,'team_source',team);roadmap=pack(c,'roadmap','roadmap_inventory')
    unique([t['person_id'] for t in team],'person');unique([r['process_key'] for r in rs],'accounting process');people={t['person_id']:t for t in team};open_items=[];assigned={p:ZERO for p in people};classes={k:0 for k in ('REQUIRED','RECOMMENDED','WORLD_CLASS','SHORTCUT_RISK')}
    for t in team:
        texts(t,'role','employment_evidence','capacity_basis_memo');fraction(t['fte']);nonnegative(t['productive_peak_hours']);nonnegative(t['reserved_peak_hours'])
        if dec(t['reserved_peak_hours'])>dec(t['productive_peak_hours']):raise ReviewRequired('Team reserve exceeds actual measured capacity')
    for r in rs:
        texts(r,'process_key','entity','accountable_person','preparer_person','review_person','service_level_memo','maturity_memo','calendar_date')
        if r['entity']!=c['entity'] or any(r[k] not in people for k in ('accountable_person','preparer_person','review_person')):raise ReviewRequired('Actual team/process accountability missing')
        if r['preparer_person']==r['review_person']:raise ReviewRequired('Incompatible preparer/reviewer person assignment')
        if not flag(people[r['accountable_person']],'retained'):raise ReviewRequired('Accounting accountability must remain retained for every process')
        enum(r,'maturity_class',set(classes));classes[r['maturity_class']]+=1
        e=snapshot(c,d,r['evidence_doc']);exact_fields(e,r,('process_key','entity','accountable_person','preparer_person','review_person','maturity_class','calendar_date','sla','execution_model'),'Operating model')
        texts(e,'maturity_basis','sla_basis','governance_minutes','acceptance_memo','peak_measurement_memo')
        if e['checked_on']!=c['execution_date'] or e['period']!=[c['period_start'],c['reporting_period']]:raise ReviewRequired('Stale operating-model judgment')
        if not flag(e,'maturity_evidenced') or not flag(e,'sla_evidenced'):raise ReviewRequired('Arbitrary score or service-level benchmark')
        if e['headcount_prescription'] is not None or e['ipo_readiness_score'] is not None or e['automation_roi'] is not None:raise ReviewRequired('Unsupported staffing/IPO/ROI prescription')
        enum(r,'execution_model',{'retained','shared_services','outsourced'})
        if r['execution_model']!='retained' and (not flag(people[r['accountable_person']],'retained') or not flag(e,'provider_handoff_reconciled')):raise ReviewRequired('Outsourcing/shared service lacks retained accounting governance')
        period_date(c,r['calendar_date']);nonnegative(r['peak_hours']);exact(r['amount'],r['peak_hours'],'Original measured work hours');exact(r['peak_hours'],e['peak_hours'],'Measured peak capacity demand')
        assigned[r['preparer_person']]+=dec(r['peak_hours'])
        review_hours=nonnegative(e['review_peak_hours']);assigned[r['review_person']]+=review_hours
        if flag(e,'automated') and (not flag(e,'control_requirements_preserved') or not flag(e,'ai_governance_present') or not flag(e,'human_judgment_retained')):raise ReviewRequired('Automation/AI bypasses accounting controls or human authority')
        if not flag(e,'critical_dependencies_resolved'):open_items.append('Critical accounting governance dependency remains unresolved')
        if r.get('kpi_owner_import'):
            imp=retained_owner(c,dict(owner_import=r['kpi_owner_import']),{'management-accounting-analytics'})
            exact(e['controlled_kpi_rate'],imp['result']['calculations']['on_time_reconciliation_rate'],'Actual accounting analytics KPI owner')
    for person,hours in assigned.items():
        if hours>dec(people[person]['productive_peak_hours'])-dec(people[person]['reserved_peak_hours']):open_items.append('Measured peak accounting capacity gap; no automatic staffing prescription')
    for r in roadmap:
        if r['process_id'] not in {p['id'] for p in rs}:raise ReviewRequired('Roadmap process orphan')
        e=snapshot(c,d,r['evidence_doc']);exact_fields(e,r,('process_id','status','owner_person'),'Transformation roadmap');enum(r,'status',{'planned','complete'})
        if r['owner_person'] not in people:raise ReviewRequired('Roadmap owner absent')
        if r['status']=='complete' and (not flag(e,'independent_acceptance_passed') or not flag(e,'dependencies_complete') or not flag(e,'transition_control_passed')):raise ReviewRequired('Transformation completion unproven')
        if r['status']=='planned':open_items.append('Accounting operating-model transformation remains open')
    review_release(c,KEYS)
    return finalize(c,'Accounting operating-model ownership, cadence and measured capacity workpaper',dict(processes=len(rs),team_members=len(team),supplied_fte=sum((dec(t['fte']) for t in team),ZERO),peak_demand_hours=sum(assigned.values(),ZERO),qualified_practice_classes=classes,open_capacity_gaps=sum(assigned[p]>dec(t['productive_peak_hours'])-dec(t['reserved_peak_hours']) for p,t in people.items())),LIMITS,open_items)
