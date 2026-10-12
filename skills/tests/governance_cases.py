"""Clearly synthetic governed management workpapers; not real case certification."""
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from cases import base
from operational_cases import approved
from reporting_cases import pol
from additional_cases import reporting,certify
from governance_accounting import BATCH,digest
from production import canonical_knowledge,case_fingerprint,execute,PACKAGES,load_workflow
FRAMEWORKS=('IFRS','US_GAAP','UK_GAAP','AASB')

def row(c,id,**kw):return approved(id,source_entity=c['entity'],source_framework=c['framework'],source_period=[c['period_start'],c['reporting_period']],**kw)
def document(c,id,content,currency='USD'):
    d=row(c,id,source_system='Synthetic controlled source',query_version='synthetic-query-v1',parameters='Actual fixed case filter',snapshot_version='v1',currency=currency,as_of=c['reporting_period'],content=copy.deepcopy(content),content_hash=digest(content));c['documents'].append(d);c['document_inventory'].append(id);return d

def source_index(c,id,rs):return row(c,id,records=copy.deepcopy(rs),inventory=[r['id'] for r in rs],population_memo='Independent original source control population, not inferred from tracker',extract_version='v1')
def owner(c,pkg='financial-statements'):
    s=reporting(c['framework']);s['jurisdiction']=c['jurisdiction'];s=certify(pkg,s);r=execute(pkg,s)
    assert r['status']=='complete',r['conclusion']
    imp=approved('completed-owner',package=pkg,case=s,result=r,mode='evidence_only');c['imports'].append(imp);return imp

def refresh_release(c):
    keys=load_workflow(c['package']).KEYS
    c['release_review']=row(c,'release',review_memo='Independent exact source/artifact release review',payload_fingerprint=digest({k:c[k] for k in keys}))
    return c

def case(pkg,fw='IFRS'):
    c=base(pkg,fw);c.update(package=pkg,execution_date='2027-03-31',requested_action='workpaper',imports=[],gl=[],gl_inventory=[],documents=[],document_inventory=[])
    c['accounting_policy']=pol(c,'governance-policy');c['disclosure_review']=approved('disclosure',checklist_version='synthetic-v1',period_entity_memo='Actual bounded management scope review',complete=True)
    c['controls']=dict(source_version='v1',as_of=c['reporting_period'],population_count=0,population_amount='0',owner='synthetic source owner',reviewer='synthetic independent completeness reviewer',complete=True,policy_version='v1',cutoff_memo='Synthetic actual cutoff/completeness evidence')
    allflags=['posting_requested','legal_certification','audit_opinion','regulatory_compliance','forecast_requested','authority_override','score_requested','benchmark_requested','ipo_timing_prediction','sec_status_determination','filing_mechanics','evidence_sufficiency_asserted','auditor_independence_determined','confirmation_control_requested','audit_adjustments_requested','auditor_signoff_requested','autonomous_policy_selection','transition_calculation_requested','overwrite_history','invented_citations','universal_checklist','compliance_certification','prior_year_rollforward_only','filing_requested','comparative_change_requested','budgeting','forecasting','investment_analysis','commercial_planning','generic_bi','manufactured_explanations','automatic_gl_correction']
    c['governance_method']=pol(c,'method',target='Bounded management governance',resolved=True,scope_memo='Actual independently bounded management workpaper',boundary_memo='All forbidden claims excluded',current_requirements_memo='Actual separately qualified current case scope',qualification_memo='Actual experienced independent reviewer',entity=c['entity'],jurisdiction=c['jurisdiction'],checked_on=c['execution_date'],**{k:False for k in allflags})
    key=''
    if pkg=='ipo-accounting-readiness':
        key='readiness';c[key]=[];c['dependencies']=[];c['dependency_inventory']=[]
        c['governance_method'].update(venue='Synthetic venue, not an actual IPO',issuer_assumptions='Case-specific qualified assumptions, no status determination',adviser_scope_memo='Separate market/counsel assessment required')
        for area in sorted(load_workflow(pkg).AREAS):
            docid=area+'-evidence';document(c,docid,dict(area=area,criterion='Actual qualified '+area+' criterion',state='supported',criterion_evidenced=True,remediation_retested=False))
            c[key].append(row(c,area,amount='0',area=area,criterion='Actual qualified '+area+' criterion',evidence_doc=docid,due_date='2027-03-31',state='supported',accountable_owner='Actual controller',assessment_memo='Qualified actual-case judgment',remediation_memo='No unresolved gap',dependency_ids=[]))
        c['readiness_source']=source_index(c,'readiness-original',c[key])
    elif pkg=='audit-support-pbc':
        key='requests';c['governance_method'].update(currency='USD',assurance_regime='Actual separately qualified audit regime',engagement_scope_memo='Management-side support only')
        records=[dict(id='original-1',account='expense',amount='120'),dict(id='original-2',account='expense',amount='-20')]
        document(c,'source',dict(records=records,inventory=[x['id'] for x in records]));document(c,'books',dict(records=records,inventory=[x['id'] for x in records]));document(c,'selected-evidence',records[0])
        c[key]=[row(c,'request-1',amount='100',purpose='Actual expense population',account='expense',assertion='Completeness/accuracy',due_date='2027-03-31',source_doc='source',ledger_doc='books',accountable_owner='Actual controller',response_memo='Management evidence response',submission_version='v1',state='released')]
        c['request_source']=source_index(c,'auditor-original-requests',c[key]);c['samples']=[row(c,'auditor-sample-1',request_id='request-1',record_id='original-1',support_doc='selected-evidence',evidence_available=True)];c['sample_inventory']=['auditor-sample-1']
        c['auditor_selection']=approved('actual-selection',records=[dict(id='auditor-sample-1',request_id='request-1',record_id='original-1')],inventory=['auditor-sample-1'],selection_memo='Synthetic exact external auditor selection record',selection_version='v1');c['queries']=[];c['query_inventory']=[]
    elif pkg=='accounting-policy-memo-governance':
        key='policies';imp=owner(c);conclusion=imp['result']['conclusion'];fp=imp['result']['case_fingerprint']
        memo={k:'Independently reviewed synthetic '+k for k in load_workflow(pkg).SECTIONS};memo.update(conclusion=conclusion,owner_result_fingerprint=fp,citations=[])
        memo['citations']=[dict(id='actual-claim-'+str(n),claim_id=x['claim_id'],proposition=x['proposition'],locator=None) for n,x in enumerate(imp['result']['evidence'])]
        d=document(c,'active-memo',memo)
        c[key]=[row(c,'policy-current',amount='200',policy_id='reporting-policy',policy_version=1,effective_from='2026-01-01',effective_to='2026-12-31',owner_import=imp['id'],memo_doc=d['id'],accountable_owner='Actual policy controller',implementation_memo='Actual implementation evidence',exception_memo='No unresolved exception',policy_change=False,owner_result_fingerprint=fp,accounting_conclusion=conclusion,implemented=True,exceptions_resolved=True,result_path=['current','profit'])]
        c['policy_source']=source_index(c,'policy-original-register',c[key]);c['history']=[row(c,'policy-history-1',policy_id='reporting-policy',policy_version=1,policy_memo='Retained approved policy',body_hash=d['content_hash'],memo_doc=d['id'],supersedes=None,effective_from='2026-01-01',effective_to='2026-12-31')];c['history_inventory']=['policy-history-1']
    elif pkg=='disclosure-management':
        key='requirements';imp=owner(c)
        document(c,'applicability',dict(requirement_id='requirement-1',applicable=True,current_source_version='actual-qualified-v1',not_applicable_independently_reviewed=False))
        document(c,'issued-prior',dict(period=['2025-01-01','2025-12-31'],requirement_key='profit-support',units='USD',amount='150'))
        document(c,'statement',dict(metric='profit',units='USD',amount='200'))
        c[key]=[row(c,'requirement-1',amount='200',topic_id='TOPIC-08-001',requirement_key='profit-support',requirement_text='Actual qualified reporting owner profit support',owner_import=imp['id'],applicability_doc='applicability',accountable_owner='Actual disclosure owner',applicability_memo='Actual current facts reviewed',applicable=True,owner_requirement=imp['result']['disclosures_impacted'][0],metric='profit',result_path=['current','profit'])]
        c['requirement_source']=source_index(c,'qualified-requirement-register',c[key]);c['requirement_source'].update(requirement_version='actual-qualified-v1',current_scope_memo='Current actual entity/tier/period',topic_coverage_memo='Independent full case applicable topics',authority_review_memo='Qualified current actual-case requirements review',checked_on=c['execution_date'],effective_period=[c['period_start'],c['reporting_period']],applicable_topic_inventory=['TOPIC-08-001'])
        c['notes']=[row(c,'note-1',requirement_id='requirement-1',note_location='Synthetic controlled note',cross_reference='Actual primary statement reference',narrative=imp['result']['conclusion'],amount='200',prior_amount='150',issued_prior_doc='issued-prior',units='USD',statement_doc='statement',unchanged_comparative=True,review_notes_closed=True)];c['note_inventory']=['note-1']
    elif pkg=='management-accounting-analytics':
        c['diagnostic']=None
        key='accounts';c['governance_method'].update(comparison_basis='prior_year_calendar_balance',currency='USD',signed_convention='Signed ledger debit positive',metric_dictionary='Only account balance and on-time reconciliation rate',threshold_memo='All nonzero movements require evidence; no arbitrary industry threshold',reconciliation_source_doc='reconciliation-source',kpi='on_time_reconciliation_rate')
        current=dict(period=[c['period_start'],c['reporting_period']],account='cash',currency='USD',posted_only=True,signed_convention='Signed ledger debit positive',records=[dict(id='cash-line',account='cash',amount='120')],inventory=['cash-line'],statutory_amount='120',management_amount='120',gross_amount='120')
        prior=copy.deepcopy(current);prior.update(period=['2025-01-01','2025-12-31'],records=[dict(id='cash-line',account='cash',amount='100')],statutory_amount='100',management_amount='100',gross_amount='100')
        document(c,'current-books',current);document(c,'prior-books',prior);document(c,'actual-drivers',dict(account='cash',period=[c['period_start'],c['reporting_period']],drivers=[dict(id='actual-receipt',amount='20')],driver_inventory=['actual-receipt']))
        c[key]=[row(c,'cash-metric',amount='120',account='cash',currency='USD',current_source_doc='current-books',prior_source_doc='prior-books',management_amount='120',lineage_memo='Exact controlled books/report lineage',metric='account_balance')];c['account_source']=source_index(c,'original-account-register',c[key])
        c['bridge_items']=[];c['bridge_inventory']=[];c['explanations']=[row(c,'cash-driver',account='cash',interpretation_memo='Management interpretation is qualified; actual receipt is supplied fact',driver_doc='actual-drivers',amount='20')];c['explanation_inventory']=['cash-driver']
        rec=dict(id='cash-rec',due_date='2027-01-05',completed_on='2027-01-04',material=True,amount='120');document(c,'reconciliation-source',dict(records=[rec],inventory=['cash-rec']))
        c['reconciliations']=[row(c,rec.pop('id'),**rec)];c['reconciliation_inventory']=['cash-rec']
    c['source_inventory']=[r['id'] for r in c[key]];c['controls'].update(population_count=len(c[key]),population_amount=str(sum(abs(__import__('decimal').Decimal(r['amount'])) for r in c[key])))
    return refresh_release(c)

def ready(pkg,fw='IFRS',c=None,release=False):
    c=copy.deepcopy(c if c is not None else case(pkg,fw))
    if release:refresh_release(c)
    claims,docs=canonical_knowledge(PACKAGES[pkg][1],c['framework'])
    c['knowledge_review']=dict(reviewer='Synthetic independent knowledge reviewer',claim_ids=[x['claim_id'] for x in claims],documents=docs,applied_claim_ids=[],selection_memo='Approved practice workflow; normative/auditor claims reviewed as context, no universal recognition or auditor obligation asserted',public_caveats=['Management governance workpaper only; underlying accounting and current actual jurisdictional requirements remain separately qualified.'])
    c['reviewer_signoff']=dict(reviewer='Synthetic independent case reviewer',approved=True,case_fingerprint=case_fingerprint(c));return c
