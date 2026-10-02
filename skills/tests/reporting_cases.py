"""Synthetic reporting cases. Every approval is a regression assertion, never a human signoff."""
from calendar import monthrange
from cases import base
from operational_cases import approved, handoffs
from additional_cases import certify

PACKAGES=['cash-flow-reporting','equity-capital','accounting-changes','going-concern','commitments-contingencies','related-parties']

def pol(c,id,**kw):
    return approved(id,framework=c['framework'],effective_period=[c['period_start'],c['reporting_period']],entity_scope=c['entity_type'],method_memo='Synthetic reviewed operative method',effective_standard='Actual effective edition reviewed',**kw)

def reporting(package,fw='IFRS'):
    c=base(package,fw);c['execution_date']='2027-03-31';c['functional_currency']='EUR'
    c['controls']=dict(source_version='v1',as_of=c['reporting_period'],population_count=0,population_amount='0',owner='synthetic owner',reviewer='synthetic independent reviewer',complete=True,policy_version='v1',cutoff_memo='Synthetic independent complete source register')
    c['disclosure_review']=approved('disclosures',checklist_version='v1',period_entity_memo='Actual entity/period requirements independently reviewed',complete=True)
    if package=='cash-flow-reporting':
        c['cash_policy']=pol(c,'policy',early_adoption=False,business_activity='ordinary',interest_paid='operating',interest_received='operating',dividends_received='operating',dividends_paid='financing',restricted_memo='No restrictions')
        c['cash_inventory']=['bank'];c['cash_accounts']=[approved('bank',opening='100',closing='290',gl_opening='100',gl_closing='290',type='demand',cf_included=True,balance_sheet_cash=True,fx='-10',definition_memo='Demand deposit',restriction_evidence='Unrestricted',bank_gl_evidence='Independent bank/GL tie')]
        c['transactions']=[approved(id,date='2026-12-31',amount=n,kind=kind,category=cat,cash=True,source_id=id,bank_id=id,classification_memo='Reviewed cash classification') for id,n,kind,cat in [('customers','400','customer_receipts','operating'),('suppliers','-160','suppliers_employees','operating'),('capex','-90','capital_purchase','investing'),('debt','50','debt_proceeds','financing')]]
        c['indirect']=dict(starting_subtotal='net_profit',start_amount='200',net_profit='200',subtotal_to_profit='0',adjustments=[approved('depreciation',amount='40',basis_memo='Supported noncash depreciation',noncash_acquisition_fx_excluded=True)],working_capital=[])
        c['noncash']=[approved('lease',source_id='lease_non_cash',amount='20',type='new lease',accounting_memo='Reviewed Lease Accounting result')]
        c['statement']=dict(opening='100',closing='290',balance_sheet_opening='100',balance_sheet_closing='290',operating='240',investing='-90',financing='50',fx='-10')
        c['handoffs']=handoffs(c,dict(fx='Foreign Currency',statements='Financial Statements',leases='Lease Accounting',consolidation='Consolidation',profit='Financial Statements'));c['handoffs']['fx']['amount']='-10';c['handoffs']['profit']['amount']='200'
        c['controls'].update(population_count=4,population_amount='700')
    elif package=='equity-capital':
        c['components']=[approved(id,opening=op,closing=cl,gl_closing=cl,classification_memo='Reviewed parent component',equity_owner='parent',role='profit' if id=='retained_earnings' else 'oci' if id=='oci' else 'capital') for id,op,cl in [('share_capital','100','120'),('premium','0','172'),('retained_earnings','50','40'),('treasury','0','0'),('oci','0','0')]]
        c['component_inventory']=[r['id'] for r in c['components']]
        c['events']=[approved('issue',kind='issue',date='2026-03-01',amount='200',equity_classified=True,shares='20',par_value='1',issue_price='10',incremental_cost='8',nonqualifying_cost='0',cost_basis='Incremental direct issue cost',ordinary=True,accounting_memo='Ordinary equity issue',legal_evidence='Reviewed ordinary lawful issue'),approved('dividend',kind='dividend_declared',date='2026-12-31',amount='10',equity_classified=True,accounting_memo='Authorized dividend',legal_evidence='Reviewed declaration')]
        c['share_register']=dict(opening_issued='100',closing_issued='120',opening_own='0',closing_own='0')
        c['statement']=dict(opening_equity='150',closing_equity='332',opening_dividend_payable='0',closing_dividend_payable='10')
        c['handoffs']=handoffs(c,dict(legal='Legal capital',instruments='Financial Instruments',sbc='Share-Based Compensation',group='Consolidation'));c['controls'].update(population_count=2,population_amount='210')
    elif package=='accounting-changes':
        c['change']=pol(c,'error',kind='error',discovery_date='2027-01-15',original_information_available=True,new_information=False,mandatory=False,specific_transition=False,transition_route='retrospective',permitted_change=True,impracticable=False,impracticability_memo='Not invoked',earliest_practicable='2025-01-01',original_authorization='2026-03-01',information_date='2025-12-01')
        c['affected_periods']=[approved('prior',period_start='2025-01-01',period_end='2025-12-31',issued_version='v1',statement_memo='Comparative-year expense was omitted',comparative_memo='Separately reviewed annual comparative',lines=[dict(id='cash',balance='100',category='asset'),dict(id='payable',balance='0',category='liability'),dict(id='revenue',balance='-100',category='revenue'),dict(id='expense',balance='0',category='expense')],expected_corrected={'cash':'100','payable':'-20','revenue':'-100','expense':'20'},opening_equity_effect=False,issued=True,weighted_shares='10',original_eps='10',corrected_eps='8',eps_applicable=True)]
        c['period_inventory']=['prior'];c['adjustments']=[approved('correct',period_id='prior',layer='comparative_profit',source_memo='Original invoice proves original information available',lines=[dict(side='Dr',account='expense',amount='20'),dict(side='Cr',account='payable',amount='20')])]
        c['materiality']=approved('materiality',qualitative_memo='Material to issued comparative',aggregation_memo='Complete cumulative error review',interim_memo='All interims separately reviewed',prior_material=True,current_if_corrected_material=True,current_uncorrected_material=True,interim_review_complete=True)
        c['sec']=dict(registrant=False,auditor_notice=False)
        c['error_register']=[approved('error',current_earnings_effect='0',ending_balance_effect='20',qualitative_memo='Prior expense liability error')]
        c['opening_equity_bridge']=dict(original='100',corrected='80');c['handoffs']=handoffs(c,dict(tax='Tax and EPS',underlying='Underlying transaction accounting'));c['controls'].update(population_count=1,population_amount='20')
    elif package=='going-concern':
        c['assessment']=pol(c,'assessment',authorization_date='2027-03-01',issuance_date='2027-03-01',horizon_end='2028-03-01' if fw in ['US_GAAP','UK_GAAP'] else '2027-12-31',opening_available_cash='1000',unavailable_cash='0',cash_gl='1000',basis='going_concern',liquidation_intent=False,realistic_alternative=True,conditions_memo='Reviewed operating business and financing obligations')
        c['debt']=[];c['debt_inventory']=[];c['plans']=[];c['scenarios']=[]
        for id,kind,receipt in [('base','base',100),('downside','downside',80)]:
            ps=[];cash=1000
            for index in range(12 if fw in ['IFRS','AASB'] else 15):
                yr=2027+index//12;mo=index%12+1;d=f'{yr}-{mo:02}-{monthrange(yr,mo)[1]:02}';opening=cash;cash+=receipt-100
                ps.append(approved(d,date=d,receipts=str(receipt),payments='100',debt_payments=[],plan_draws=[],expected_before=str(cash),expected_after=str(cash),covenants=[],source_memo='Synthetic board-reviewed dated forecast',intra_period_timing_memo='Daily forecast checked, payments after collections',intra_period_min_before=str(min(opening,cash)),intra_period_min_after=str(min(opening,cash))))
            c['scenarios'].append(approved(id,kind=kind,periods=ps,minimum_reserve='0',gl_opening_cash='1000',expected_min_before=str(cash),expected_min_after=str(cash),forecast_source='Synthetic approved forecast',assumption_memo='Synthetic evidenced inputs',board_review='Independent plan review'))
        c['scenario_inventory']=['base','downside'];c['sensitivities']=[approved('sensitivity',base_receipts='100',reduction_fraction='0.2',incremental_cost='5',expected_reduction='25',basis_memo='Approved adverse demand/cost scenario')]
        c['management_review']=approved('conclusion',basis_memo='Reviewed going-concern basis',uncertainty_memo='No material uncertainty in synthetic case',plan_evaluation='No assumed mitigation',material_uncertainty=False,substantial_doubt_before=False,substantial_doubt_alleviated=False,significant_judgment=False)
        c['handoffs']=handoffs(c,dict(cash='Cash reporting',debt='Debt and covenants',subsequent_events='Financial Statements'));c['handoffs']['cash']['amount']='1000';count=sum(len(s['periods']) for s in c['scenarios']);c['controls'].update(population_count=count,population_amount=str((100+100+80+100)*(count//2)))
    elif package=='commitments-contingencies':
        c['register']=[approved('purchase',kind='purchase',opening_commitment='100',new_commitment='50',fulfilled='20',cancelled='10',fx_commitment='0',closing_commitment='120',opening_recognized='0',charge='0',unwind='0',settled='0',fx_recognized='0',closing_recognized='0',gl_closing='0',route='ordinary_commitment',disclose=True,source_journals=[],measurement_handoff='',law_probability_supported=True,contract_evidence='Reviewed signed purchase agreement',completeness_memo='All signed contracts searched',legal_probability_memo='Executable ordinary commitment',recognition_memo='Not yet delivered, no onerous obligation',measurement_memo='Nominal contract exposure')]
        c['register'][0]['measurement_handoff']='not_applicable';c['register'][0]['recognized_account']='not_applicable'
        c['contract_inventory']=['purchase'];c['disclosure']=[approved('purchase',requirements_memo='Required capital/purchase commitment note',exclusion_memo='No exclusion',included=True,amount='120',recognized_amount='0')];c['gl_recognized']='0';c['handoffs']=handoffs(c,dict(legal='Legal contingencies',provisions='Provisions & Contingencies',instruments='Financial Instruments'));c['controls'].update(population_count=1,population_amount='150')
    elif package=='related-parties':
        c['reporting_scope']=pol(c,'scope',level='separate',exemptions_review='None used',kmp_scope=False,small_entity=False,uk_2026_disclosure_review=True)
        c['relationships']=[approved('relation',counterparty='parent',kind='parent',start='2020-01-01',end='2099-12-31',related=True,internal_group=True,arm_length_asserted=False,pricing_evidence='No arm-length assertion',arm_length_approved=False,relationship_evidence='Synthetic ownership register',identification_memo='Documented controlling parent')];c['relationship_inventory']=['relation'];c['counterparty_inventory']=['parent'];c['declarations']=[approved('parent',related=True,relationship_ids=['relation'],declaration_evidence='Signed synthetic declaration',search_memo='Ownership and GL populations searched')]
        c['transactions']=[approved('sale',relationship_id='relation',counterparty='parent',date='2026-12-01',amount='100',gl_amount='100',type='sale',eliminated=False,exemption=False,exemption_memo='No exemption',source_evidence='Reviewed invoice',terms_memo='Unsecured normal terms',governance_approval='Independent transaction approval')];c['balances']=[approved('receivable',relationship_id='relation',counterparty='parent',amount='20',gl_amount='20',type='receivable',eliminated=False,exemption=False,exemption_memo='No exemption',source_evidence='Reviewed customer ledger',terms_memo='Unsecured normal terms',governance_approval='Independent balance confirmation')];c['commitments']=[]
        c['disclosure']=[approved(id,included=True,amount=n,requirement_memo='Applicable related-party disclosure') for id,n in [('sale','100'),('receivable','20')]];c['kmp_compensation']=[];c['statement_totals']=dict(sales='100',purchases='0',receivables='20',payables='0',commitments='0',kmp='0');c['handoffs']=handoffs(c,dict(legal='Related-party legal assessment',group='Consolidation',pricing='Transfer Pricing'));c['controls'].update(population_count=2,population_amount='120')
    if package=='related-parties':
        c['kmp_inventory']=[];c['kmp_categories_review']=approved('kmp_categories',completeness_memo='All KMP pay categories nil/not applicable, independent payroll review',totals={k:'0' for k in ['short_term','post_employment','other_long_term','termination','share_based']})
    return c

def certified(package,fw='IFRS',case=None):
    from production import canonical_knowledge, PACKAGES as REGISTRY, case_fingerprint
    c=certify(package,case or reporting(package,fw))
    claims,_=canonical_knowledge(REGISTRY[package][1],c['framework'])
    c['knowledge_review']['applied_claim_ids']=[x['claim_id'] for x in claims if not any(s in x['proposition'].replace(' ','') for s in ['FRS101','FRS105']) and ('-SEC-' not in x['claim_id'] or c.get('sec',{}).get('registrant',False))]
    c['reviewer_signoff']['case_fingerprint']=case_fingerprint(c)
    return c
