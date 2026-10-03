"""Synthetic bounded workpapers; no real economy, rule, issuer or reviewer assertions."""
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from cases import base
from operational_cases import approved
from reporting_cases import pol
from presentation_cases import dimensions
from production import canonical_knowledge,PACKAGES as REGISTRY,case_fingerprint,execute

PACKAGES=['held-for-sale-discontinued-operations','hyperinflation-accounting','alternative-performance-measures','sec-filing-accounting']
BLOCKED=['investment-property']
FRAMEWORKS=['IFRS','US_GAAP','UK_GAAP','AASB']

def method(c,id,target,**kw):return pol(c,id,target=target,resolved=True,scope_memo='Independently reviewed synthetic bounded scope',boundary_memo='All unsupported routes excluded',**kw)

def statement(c,id,amount='150',prior=False,metric='profit',**kw):
    span=['2025-01-01','2025-12-31'] if prior else [c['period_start'],c['reporting_period']]
    return approved(id,source_entity=c['entity'],source_framework=c['framework'],source_period=span,source_version='v1',metric=metric,definition='Actual controlled GAAP subtotal',units='USD',amount=amount,period_kind='duration',lines=[approved('expense-source',account='controlled net subtotal',source_memo='Independent approved GL population',gl_amount=str(-__import__('decimal').Decimal(amount)),credit_nature=True,amount=amount)],line_inventory=['expense-source'],**kw)

def rule(c,**kw):return pol(c,'current-rule',authority_url='https://www.sec.gov/forms',rule_version='Synthetic exact case rule version',checked_on=c['execution_date'],jurisdiction=c['jurisdiction'],issuer_type='domestic',rule_memo='Synthetic authoritative verification record, not a real verification',case_id=c['case_id'],current_authority_verified=True,**kw)

def case(pkg,fw='IFRS'):
    c=base(pkg,fw);c.update(execution_date='2027-03-31',imports=[],gl=[],gl_inventory=[],requested_action='workpaper')
    c['jurisdiction']={'IFRS':'EU','US_GAAP':'US','UK_GAAP':'UK','AASB':'AU'}[fw]
    c['accounting_policy']=pol(c,'policy');c['disclosure_review']=approved('disclosure',checklist_version='Synthetic actual version',period_entity_memo='Synthetic complete reporting review',complete=True)
    c['controls']=dict(source_version='v1',as_of=c['reporting_period'],population_count=0,population_amount='0',owner='synthetic source owner',reviewer='synthetic completeness reviewer',complete=True,policy_version='v1',cutoff_memo='Synthetic independent source population')
    if pkg=='held-for-sale-discontinued-operations':
        c['disposal_method']=method(c,'disposal','Disposal classification and presentation',route='classification_presentation',classification_date='2026-09-30',criteria_met_date='2026-09-30',approval_evidence_date='2026-09-30',expected_sale_date='2027-06-30',**{k:False for k in ['allocation_required','reversal_requested','completed_disposal','retained_interest','oci_recycling','measurement_requested']},**{k:True for k in ['available_immediately','highly_probable','committed_plan','active_marketing','sale_within_year','premeasurement_complete','scope_exceptions_reviewed','group_complete','tax_review_complete']},**{k:'Synthetic independently reviewed workpaper' for k in ['perimeter_memo','sale_plan_memo','criteria_memo','premeasurement_memo','discontinued_memo','cash_flow_memo','comparative_memo','impairment_memo']})
        c['assets']=[approved('plant',measurement_owner='Fixed assets preclassification source',owner_asset_id='plant',premeasurement_evidence='Independent source after applicable tests',scope_memo='Actual supported asset',depreciation_memo='No depreciation after valid date',in_scope=True,premeasurement_complete=True,carrying_at_classification='330',book_carrying='330',stock_kind='asset',depreciation_after_classification='0')];dimensions(c,c['assets']);c['source_inventory']=['plant'];c['controls'].update(population_count=1,population_amount='330')
        c['perimeter']=approved('perimeter',legal_asset_ids=['plant'],book_asset_ids=['plant'],legal_memo='Actual independently signed legal disposal inventory',book_memo='Complete separately reviewed stock register');c['depreciation_sources']=[];c['depreciation_inventory']=[]
        c['component']=approved('component',qualification_memo='Separate major geographic operation',continuing_involvement_memo='TSA separately owned, no unsupported measurement',separable_component=True,major_line=False,major_geography=True,coordinated_major_plan=False,discontinued=True)
        c['current_statement']=statement(c,'current',amount='150')
        c['results']=[approved('component-result',profit_after_tax='30',belongs_to_component=True,disposal_gain='0',allocation_memo='Actual component source',source_population_memo='Independent complete component ledger'),approved('continuing-result',profit_after_tax='120',belongs_to_component=False,disposal_gain='0',allocation_memo='Actual continuing source',source_population_memo='Complete continuing ledger')];dimensions(c,c['results']);c['result_inventory']=[a['id'] for a in c['results']]
        for a in c['results']:
            a['source_statement']=statement(c,a['id'],a['profit_after_tax'])
            a['source_statement']['lines'][0]['id']=a['id']
            a['source_statement']['line_inventory']=[a['id']]
        c['current_statement']['lines']=[copy.deepcopy(a['source_statement']['lines'][0]) for a in c['results']]
        c['current_statement']['line_inventory']=[a['id'] for a in c['results']]
        c['cash_flows']=[approved(k,category=k,amount=v,bank_source_memo='Independent component cash population') for k,v in [('operating','20'),('investing','-5'),('financing','0')]];dimensions(c,c['cash_flows']);c['cash_flow_inventory']=[a['id'] for a in c['cash_flows']]
        for a in c['cash_flows']:a['bank_source']=approved(a['id'],source_period=a['source_period'],category=a['category'],entity=c['entity'],amount=a['amount'])
        c['bank_sources']=[copy.deepcopy(a['bank_source']) for a in c['cash_flows']];c['bank_inventory']=[b['id'] for b in c['bank_sources']]
        c['presentation']=dict(discontinued_profit='30',continuing_profit='120',component_cash_flows=dict(operating='20',investing='-5',financing='0'))
        c['comparatives']=[approved('prior',statement=statement(c,'prior',amount='100',prior=True),continuing_profit='80',discontinued_profit='20',component_profit='20',component_statement=statement(c,'prior-component','20',True),balance_sheet_reclassified=False,recast_memo='Controlled prior component/current definition')];c['comparative_inventory']=['prior']
        r=c['comparatives'][0];r['component_statement']['lines'][0]['id']='prior-component';r['component_statement']['line_inventory']=['prior-component']
        continuing=statement(c,'prior-continuing','80',True)['lines'][0];continuing['id']='prior-continuing'
        r['statement']['lines']=[copy.deepcopy(r['component_statement']['lines'][0]),continuing];r['statement']['line_inventory']=['prior-component','prior-continuing']
    elif pkg=='hyperinflation-accounting':
        c['inflation_method']=method(c,'inflation','Isolated hyperinflation index schedule',scope='isolated_schedule',hyperinflation_supported=True,threshold_only=False,independent_economic_review=True,closing_index_id='closing',index_series='synthetic-general-index',index_revision='v1',**{k:'Synthetic actual qualified evidence' for k in ['functional_currency','economy','economic_evidence','qualitative_indicators','quantitative_indicators','group_consistency_memo','onset_cessation_memo','index_source','classification_memo','equity_memo','income_memo','monetary_result_handoff','translation_handoff','tax_handoff','comparative_memo']},**{k:False for k in ['complete_statements_requested','monetary_gain_calculation_requested','translation_requested','consolidation_requested','journal_requested']})
        c['indices']=[approved(id,series='synthetic-general-index',revision='v1',source_url='https://synthetic.invalid/index',index_date=d,value=v) for id,d,v in [('acquisition','2026-01-01','200'),('flow','2026-06-30','225'),('closing','2026-12-31','250')]];c['index_inventory']=[i['id'] for i in c['indices']]
        c['items']=[approved(id,kind=kind,amount=a,measurement_date=d,index_id=ix,expected_restated=value,classification_evidence='Actual independently classified item',measurement_memo='Controlled historical/current basis') for id,kind,a,d,ix,value in [('machine','historical_nonmonetary','100','2026-01-01','acquisition','125'),('cash','monetary','40','2026-12-31','closing','40'),('flow','income_expense','50','2026-06-30','flow',str(__import__('decimal').Decimal(50)*250/225)),('equity','equity','-100','2026-01-01','acquisition','-125')]];dimensions(c,c['items']);c['source_inventory']=[i['id'] for i in c['items']];c['controls'].update(population_count=4,population_amount='290')
    elif pkg=='alternative-performance-measures':
        regime={'US':'SEC_RegG_Item10e_review','EU':'EU_APM_review','UK':'UK_APM_review','AU':'AU_APM_review'}[c['jurisdiction']]
        c['apm_method']=method(c,'apm','APM reconciliation and publication governance',label='Adjusted profit',definition='Profit plus reviewed restructuring and share-compensation expenses',rationale='Actual management rationale independently reviewed',metric='profit',units='USD',issuer_type='domestic',regime=regime,**{k:'Synthetic actual qualified review' for k in ['jurisdictional_memo','prominence_memo','tax_nci_memo','recurrence_memo','mpm_memo']},**{k:False for k in ['invented_adjustments','compliance_certification_requested','per_share_requested','definition_changed','early_adoption','mpm_effective','mpm_in_scope']},**{k:True for k in ['not_misleading_reviewed','prominence_reviewed','comparative_consistent','adjustment_population_complete','tax_nci_reviewed','publication_draft_reviewed','mpm_scope_reviewed','mpm_disclosures_complete']})
        c['regulatory_method']=rule(c,regime=regime);c['regulatory_method']['authority_url']={'US':'https://www.sec.gov/forms','EU':'https://www.esma.europa.eu/issuer-disclosure','UK':'https://www.fca.org.uk/','AU':'https://www.asic.gov.au/'}[c['jurisdiction']]
        c['statements']=[statement(c,'current','150'),statement(c,'prior','100',True)];c['statement_inventory']=['current','prior'];c['adjustments']=[];c['adjustment_journals']=[];c['publication']={}
        for period in ['current','prior']:
            span=next(s for s in c['statements'] if s['id']==period)['source_period']
            for typ,n in [('restructuring','20'),('share_compensation','10')]:
                id=period+'-'+typ
                c['adjustments'].append(approved(id,period=period,label=typ,definition_key=typ,rationale='Actual supported adjustment',tax_nci_memo='Actual separately qualified zero tax/NCI effect',classification_memo='Source expense included in GAAP subtotal',recurring=typ=='share_compensation',described_nonrecurring=False,in_gaap_subtotal=True,regulatory_treatment_reviewed=True,journal_ids=[id],amount=n,tax_effect='0',nci_effect='0',source_entity=c['entity'],source_framework=c['framework'],source_period=span))
                c['adjustment_journals'].append(approved(id,period=period,source_period=span,expense_account=typ,source_memo='Actual journal retained with recognition owner',included_expense=n,lines=[dict(side='Dr',account=typ,amount=n),dict(side='Cr',account='liability',amount=n)]))
            c['publication'][period]=approved(period,label=c['apm_method']['label'],definition=c['apm_method']['definition'],units='USD',gaap_amount='150' if period=='current' else '100',adjusted_amount='180' if period=='current' else '130',tax_effect='0',nci_effect='0')
        for st in c['statements']:
            from decimal import Decimal
            st['lines']=[approved('revenue',account='revenue',source_memo='Full approved revenue source',gl_amount=str(-(Decimal(st['amount'])+30)),credit_nature=True,amount=str(Decimal(st['amount'])+30),journal_ids=[])]
            for typ,n in [('restructuring','20'),('share_compensation','10')]:st['lines'].append(approved(typ,account=typ,source_memo='Exact journal population in GAAP subtotal',gl_amount=n,credit_nature=True,amount=str(-Decimal(n)),journal_ids=[st['id']+'-'+typ]))
            st['line_inventory']=[l['id'] for l in st['lines']]
        c['source_inventory']=[i['id'] for i in c['adjustments']];c['journal_inventory']=c['source_inventory'].copy();c['controls'].update(population_count=4,population_amount='60')
    elif pkg=='sec-filing-accounting':
        c['jurisdiction']='US';issuer='fpi' if fw=='IFRS' else 'domestic';form='20-F' if issuer=='fpi' else '10-K'
        c['filer']=approved('filer',registration_evidence='Actual synthetic securities register',filer_classification_evidence='Actual independently reviewed filer memo',status_memo='Ordinary supported issuer',form=form,issuer_type=issuer,filing_kind='annual',registrant=True,qualified_status_reviewed=True,**{k:False for k in ['amended_filing','special_form','compliance_certification','officer_certification','audit_opinion_requested','edgar_submission_requested']})
        c['rule']=rule(c,form=form,filing_kind='annual',deadline_evidence='Synthetic supplied current verified date, no real deadline assertion',taxonomy_version='synthetic-taxonomy-v1',entry_point='synthetic-entry-point',form_instructions_memo='Actual selected form reviewed',annual_interim_memo='Annual package',statement_requirements_memo='Actual complete statement/notes checklist',verified_due_date='2027-04-30',fpi_interim_basis_verified=True,inline_xbrl_required=True);c['rule']['issuer_type']=issuer
        c['calendar']=approved('calendar',due_date='2027-04-30',internal_ready_date='2027-03-31',deadline_memo='Actual supplied evidence',audit_dependency_memo='Actual approved audit package',board_dependency_memo='Actual approved accounting support')
        c['statements']=[statement(c,'current','150',current=True),statement(c,'prior','100',True,current=False)];c['statement_inventory']=['current','prior'];c['filing_lines']=[];c['tags']=[]
        for s in c['statements']:
            c['filing_lines'].append(approved(s['id'],statement_id=s['id'],metric=s['metric'],units='USD',form_section='Financial statements',tieout_memo='Actual source/rendered consistency',amount=s['amount'],source_entity=c['entity'],source_framework=c['framework'],source_period=s['source_period']))
            c['tags'].append(approved(s['id'],filing_line_id=s['id'],taxonomy_version='synthetic-taxonomy-v1',entry_point='synthetic-entry-point',concept='syntheticProfit',expected_concept='syntheticProfit',context_entity=c['entity'],context_period=s['source_period'],unit='USD',expected_unit='USD',extension_memo='No unsupported extension',dimension_memo='Actual source dimensions',dimensions={},expected_dimensions={},period_kind='duration',expected_period_kind='duration',mapping_reviewed=True,extension_reviewed=True,scale=0,expected_scale=0,sign=1,expected_sign=1,display_amount=s['amount'],raw_value=s['amount']))
        c['source_inventory']=['current','prior'];c['filing_line_inventory']=c['source_inventory'].copy();c['tag_inventory']=c['source_inventory'].copy();c['controls'].update(population_count=2,population_amount='250')
        for k in ['issues','queries','changes']:c[k]=[];c[k[:-1]+'_inventory' if k!='queries' else 'query_inventory']=[]
        c['filing_review']=approved('review',**{k:True for k in ['disclosure_controls_complete','annual_interim_checklist_complete','source_completeness_reviewed','narrative_consistency_reviewed','validation_errors_resolved','warnings_resolved','legal_ir_auditor_review_complete','apm_scope_reviewed']},apm_present=False,apm_amounts={},reviewed_release_fingerprint='pending')
        import importlib.util
        spec=importlib.util.spec_from_file_location('sec_workflow',Path(__file__).resolve().parents[1]/'sec-filing-accounting/workflow.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);c['filing_review']['reviewed_release_fingerprint']=mod.release_fingerprint(c)
    return c

def ready(pkg,fw='IFRS',c=None):
    c=copy.deepcopy(c if c is not None else case(pkg,fw));claims,docs=canonical_knowledge(REGISTRY[pkg][1],c['framework'])
    c['knowledge_review']=dict(reviewer='synthetic knowledge reviewer',claim_ids=[x['claim_id'] for x in claims],documents=docs,applied_claim_ids=[x['claim_id'] for x in claims if 'FCA' not in x['proposition']],selection_memo='Synthetic independent selection of actual scope; no authority upgrade',public_caveats=['Exact accounting and jurisdictional scope is bounded; current actual-case authority remains separately reviewed.'])
    c['reviewer_signoff']=dict(reviewer='synthetic independent reviewer',approved=True,case_fingerprint=case_fingerprint(c));return c
