"""Clearly synthetic cases; approvals are not authenticated company signoffs."""
import copy
from governance_cases import row,document,source_index,FRAMEWORKS
from governance_cases import case as previous_case
from final_batch_accounting import BATCH,digest
from production import canonical_knowledge,case_fingerprint,PACKAGES,load_workflow

def refresh_release(c):
    c['release_review']=row(c,'release',review_memo='Synthetic independently reperformed payload',payload_fingerprint=digest({k:c[k] for k in load_workflow(c['package']).KEYS}));return c

def case(pkg,fw='IFRS',accounting=False):
    c=previous_case('ipo-accounting-readiness',fw)
    for k in ('readiness','readiness_source','dependencies','dependency_inventory'):c.pop(k,None)
    c.update(package=pkg,case_id='Synthetic '+pkg,documents=[],document_inventory=[],imports=[],owner_links=[],owner_link_inventory=[],gl=[],gl_inventory=[])
    c['governance_method'].update(target='Bounded final batch',external_write=False,legal_certification=False,audit_opinion=False,regulatory_compliance=False,authority_override=False)
    if pkg=='defined-benefit-opeb':
        key='plans';p=row(c,'pension-source',amount='210',plan_id='Actual synthetic plan',classification='defined_benefit_pension',currency='USD',single_employer=True,opening_obligation='1000',service_cost='60',interest_cost='40',benefits_paid='50',actuarial_loss='30',closing_obligation='1080',opening_assets='800',asset_interest='32',contributions='70',asset_remeasurement_gain='18',closing_assets='870',terms_doc='terms',census_doc='census',hr_doc='hr',report_doc='actuary',assets_doc='custody',statement_doc='statement',contributions_doc='funding',**{k:False for k in ('amendment','settlement','curtailment','minimum_funding','asset_ceiling_issue','fx','contributions_already_expensed','assumption_selection_requested')})
        document(c,'terms',{k:p[k] for k in ('plan_id','classification','single_employer','amendment','settlement','curtailment','minimum_funding','asset_ceiling_issue','fx','contributions_already_expensed','assumption_selection_requested')})
        census=dict(employees=[dict(id='employee-1',service_history='Actual synthetic service record',salary_history='Actual qualified input, never valued by software')],inventory=['employee-1'])
        document(c,'census',census);document(c,'hr',census)
        from production import load_workflow
        report={k:p[k] for k in load_workflow(pkg).OBL+load_workflow(pkg).ASSET+('classification','plan_id','currency')}
        report.update({k:p[k] for k in ('amendment','settlement','curtailment','minimum_funding','asset_ceiling_issue','fx','assumption_selection_requested')})
        report.update(actuary='Synthetic qualified actuary',qualifications_memo='Reviewed specialist competence',objectivity_memo='Reviewed independence',assumption_review_memo='Actuary-supplied assumptions; no model selection',signed_on='2027-01-05',report_id='Actual source report v1',method={'IFRS':'IAS19_qualified','US_GAAP':'ASC715_qualified','UK_GAAP':'FRS102_28_qualified','AASB':'AASB119_qualified'}[fw],measurement_date=c['reporting_period'],period=[c['period_start'],c['reporting_period']],entity=c['entity'],framework=fw,census_hash=digest(census),assumptions=dict(qualified_opening_discount_rate='0.04',mortality='Qualified source only'))
        document(c,'actuary',report);document(c,'custody',{k:report[k] for k in load_workflow(pkg).ASSET+('plan_id','currency','measurement_date')})
        document(c,'statement',dict(plan_id=p['plan_id'],currency='USD',net_liability='210',gl_net_liability='210',pnl_expense='68',oci_loss='12'));document(c,'funding',dict(plan_id=p['plan_id'],currency='USD',contributions='70'))
        c[key]=[p];c['plan_source']=source_index(c,'original-plan-register',c[key])
        if accounting:
            c['requested_action']='accounting'
            c['gl']=[row(c,'DB net liability',opening='-200',closing='-210',statement='-210'),row(c,'Pension expense',opening='0',closing='68',statement='68'),row(c,'Pension OCI',opening='0',closing='12',statement='12'),row(c,'Cash',opening='1000',closing='930',statement='930')];c['gl_inventory']=[r['id'] for r in c['gl']]
    elif pkg=='accounting-controls-icfr':
        key='control_rows';r=row(c,'control-1',amount='0',control_key='Actual cash completeness control',objective='Actual population completeness',assertion='completeness',risk_id='risk-cash',process='cash-reconciliation',accountable_owner='Controller',owner_person='preparer-person',review_person='review-person',precision_memo='Current independently qualified precision',exception_route='Actual documented escalation',test_attributes='Population, reviewed attributes and exceptions',frequency='monthly',kind='management_review',timing='detective',threshold='10',design_doc='design',rcm_version='v1')
        c[key]=[r];c['control_source']=source_index(c,'original-controls',c[key]);risk=dict(id='risk-cash',misstatement='Omitted cash population',assertion='completeness',process='cash-reconciliation',fraud_rationale='Qualified actual fraud scope')
        c['risk_source']=source_index(c,'original-risks',[risk]);c['risk_source']['source_doc']='risk-scope';document(c,'risk-scope',dict(records=[risk],inventory=['risk-cash']))
        e={k:r[k] for k in ('control_key','objective','assertion','risk_id','owner_person','review_person','kind','timing','frequency','threshold','rcm_version')};e.update(period=[c['period_start'],c['reporting_period']],precision_evidenced=True,independent_expectation=True,ipe_reconciled=True,expectation_set_on='2026-01-01',data_available_on='2026-12-31',expected_occurrence_ids=['occurrence-'+str(i) for i in range(1,13)],sod_conflict=False,independent_compensating_population_reviewed=False)
        document(c,'design',e);c['occurrences']=[]
        from calendar import monthrange
        for month in range(1,13):
            dt='2026-'+str(month).zfill(2)+'-'+str(monthrange(2026,month)[1]);oid='occurrence-'+str(month)
            o=row(c,oid,control_id='control-1',state='ready',due_date=dt,period_date=dt,evidence_doc='evidence-'+oid);c['occurrences'].append(o)
            document(c,o['evidence_doc'],dict(control_id=o['control_id'],state=o['state'],due_date=o['due_date'],period_date=o['period_date'],attributes_present=True,exceptions_followed_up=True))
        c['occurrence_inventory']=[o['id'] for o in c['occurrences']];c['occurrence_source']=source_index(c,'original-all-occurrences',c['occurrences'])
        c['deficiencies']=[];c['deficiency_inventory']=[];c['governance_method']['applicability_doc']='regime';document(c,'regime',dict(entity=c['entity'],jurisdiction=c['jurisdiction'],period=[c['period_start'],c['reporting_period']],checked_on=c['execution_date'],issuer_facts='Actual separately qualified issuer facts',qualified_applicability_memo='No automatic SOX inference',operative_requirements='Actual scoped management controls',regime='Qualified voluntary design readiness',requested_conclusion='design_evidence_readiness'))
    elif pkg=='accounting-systems-data-integrity':
        key='interfaces';r=row(c,'interface-1',amount='140',source_system='Actual source ledger',target_system='Actual target book',interface_key='cash-interface',entity=c['entity'],book='main-book',currency='USD',mapping_version='v1',lineage_memo='Exact supplied original accounting lineage',source_doc='source',target_doc='target',control_doc='data-control')
        c[key]=[r];c['interface_source']=source_index(c,'original-interfaces',c[key])
        c['books']=[row(c,'main-book',entity=c['entity'],book='main-book',framework=fw,currency='USD')];c['book_inventory']=['main-book'];m=row(c,'cash-mapping',source_system=r['source_system'],source_account='cash',entity=c['entity'],book='main-book',target_account='cash',allowed_source_dimensions=['HQ'],dimension_map=dict(HQ='HQ'),mapping_memo='Approved actual chart/dimension mapping')
        c['account_mapping']=[m];c['mapping_inventory']=[m['id']];c['access']=[row(c,'access-'+str(i),system=r[k],prepare_and_approve=False,unapproved_access=False,responsibility_consistent=True) for i,k in enumerate(('source_system','target_system'),1)];c['access_inventory']=[a['id'] for a in c['access']]
        c['governance_method']['registry_doc']='registry';document(c,'registry',dict(entity=c['entity'],jurisdiction=c['jurisdiction'],books=c['books'],account_mapping=c['account_mapping'],access=c['access']))
        src=dict(system=r['source_system'],entity=c['entity'],book='main-book',currency='USD',mapping_version='v1',period=[c['period_start'],c['reporting_period']],records=[dict(id='source-1',account='cash',dimension='HQ',amount='120'),dict(id='source-2',account='cash',dimension='HQ',amount='-20')],inventory=['source-1','source-2'],signed_total='100',gross_total='140')
        dst=dict(system=r['target_system'],entity=c['entity'],book='main-book',currency='USD',mapping_version='v1',period=src['period'],records=[dict(id='target-'+s['id'],source_id=s['id'],target_account='cash',dimension='HQ',entity=c['entity'],book='main-book',currency='USD',amount=s['amount'],state='posted') for s in src['records']],signed_total='100',gross_total='140',gl_amount='100',statement_amount='100');dst['inventory']=[t['id'] for t in dst['records']]
        document(c,'source',src);document(c,'target',dst);document(c,'data-control',dict(approved_threshold='0',threshold_basis_memo='Exact complete-population ties, not assumed materiality',access_memo='Actual role review',change_memo='Reviewed change evidence',quality_test_memo='Independently tested mapping',fallback_memo='Retained fallback',accounting_owner_reviewed=True,negative_tests_passed=True,exceptions_visible=True,euc_used=False,ai_used=False,migration=False))
    else:
        key='processes';r=row(c,'process-1',amount='40',process_key='Actual cash preparation service',entity=c['entity'],accountable_person='review-person',preparer_person='preparer-person',review_person='review-person',service_level_memo='Actual observed service target',maturity_memo='Evidence-qualified practice, no arbitrary score',calendar_date='2026-12-31',sla='Actual agreed close calendar',maturity_class='RECOMMENDED',execution_model='retained',peak_hours='40',evidence_doc='service')
        c[key]=[r];c['process_source']=source_index(c,'original-accounting-services',c[key]);c['team']=[row(c,'team-'+p,person_id=p,role='Actual accounting role',employment_evidence='Actual supplied team roster',capacity_basis_memo='Measured peak capacity',fte='1',productive_peak_hours='80',reserved_peak_hours='10',retained=True) for p in ('preparer-person','review-person')];c['team_inventory']=[t['id'] for t in c['team']];c['team_source']=source_index(c,'actual-original-team',c['team'])
        e={k:r[k] for k in ('process_key','entity','accountable_person','preparer_person','review_person','maturity_class','calendar_date','sla','execution_model','peak_hours')};e.update(maturity_basis='Actual source maturity evidence',sla_basis='Actual qualified agreement',governance_minutes='Recorded governance decision',acceptance_memo='Actual controlled process acceptance',peak_measurement_memo='Measured workload including actual review',checked_on=c['execution_date'],period=[c['period_start'],c['reporting_period']],maturity_evidenced=True,sla_evidenced=True,headcount_prescription=None,ipo_readiness_score=None,automation_roi=None,review_peak_hours='10',automated=False,critical_dependencies_resolved=True)
        document(c,'service',e);c['roadmap']=[];c['roadmap_inventory']=[]
    c['source_inventory']=[r['id'] for r in c[key]];c['controls'].update(population_count=len(c[key]),population_amount=str(sum(abs(__import__('decimal').Decimal(r['amount'])) for r in c[key])))
    return refresh_release(c)

def ready(pkg,fw='IFRS',c=None,release=False,accounting=False):
    c=copy.deepcopy(c if c is not None else case(pkg,fw,accounting))
    if release:refresh_release(c)
    claims,docs=canonical_knowledge(PACKAGES[pkg][1],c['framework'],package=pkg)
    c['knowledge_review']=dict(reviewer='Synthetic independent knowledge reviewer',claim_ids=[x['claim_id'] for x in claims],documents=docs,applied_claim_ids=[x['claim_id'] for x in claims] if pkg=='defined-benefit-opeb' else [],selection_memo='Actual bounded claim/method applicability, practice never invents authority',public_caveats=['Qualified actual sources and current framework/period review required. No actuarial, legal, audit or external compliance certification.'])
    c['reviewer_signoff']=dict(reviewer='Synthetic independent exact-case reviewer',approved=True,case_fingerprint=case_fingerprint(c));return c
