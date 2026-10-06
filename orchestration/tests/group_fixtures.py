"""Controlled two-entity evidence and separate synthetic reviewer workpapers.

These approvals are test evidence, never real people or runtime authorization.
"""
import copy
from decimal import Decimal
from orchestration.tests.fixtures import completed
from additional_cases import acquisition, fx, impairment, reporting, certify
from cases import consolidation
from financing_cases import case as financing_case, gl
from operational_cases import operational, handoffs
from orchestration.runtime import dimensions, at, digest
from orchestration.planning import FACT_ADAPTERS
from orchestration.intake import RawSource, Inventory, StructuredProposal, FactCandidate, FixturePlanner, Intake, Binding, ReviewedInputPack, DocumentBinding, TextAssertion, PopulationBinding
from orchestration.tests.intake_fixtures import cl, cell
from orchestration.intake.semantic import transform
from governance_cases import case as governance_case, ready as governance_ready, refresh_release, document, row, source_index

PARENT='Parent'; SUB='Subsidiary-US'; GROUP='Group'
SPAN=['2026-01-01','2026-12-31']; ACQUIRED='2026-07-01'
from orchestration.scopes import Scope
SCOPE=dict(entity=GROUP,framework='IFRS',jurisdiction='NL',period_start=SPAN[0],reporting_period=SPAN[1],currency='EUR',materiality='1',
    scopes=[Scope(GROUP,'GROUP',GROUP,jurisdiction='NL',framework='IFRS',presentation_currency='EUR',provenance=('reviewed-group-profile',)).record()]+[
        Scope(e,'LEGAL_ENTITY',e,e,GROUP,j,'IFRS',cur,provenance=('reviewed-legal-profile',)).record() for e,j,cur in [(PARENT,'NL','EUR'),(SUB,'US','USD')]])
OBJECTIVE="Can you review our year-end group accounts? We acquired 80% of a US business on 1 July, the subsidiary reports in USD, there are intercompany balances, goodwill looks high, and I want to know whether the consolidated accounts are right. I've attached the acquisition model, entity trial balances, intercompany schedules, FX rates, tax workpapers, impairment model and consolidation pack. Please test management's claim that the acquisition added the full-year subsidiary profit."


def context(c,entity,currency,jurisdiction):
    c.update(entity=entity,jurisdiction=jurisdiction,period_start=SPAN[0],reporting_period=SPAN[1])
    c['applicability_review']['effective_period']=SPAN
    if isinstance(c.get('currency'),dict):c['currency'].update(functional=currency,ledger=currency)
    else:c['functional_currency']=currency
    for row in c.get('jurisdictions',[]):
        row.update(source_entity=entity,source_framework='IFRS',source_period=SPAN)
    for h in c.get('handoffs',{}).values():h.update(entity=entity,framework='IFRS',reporting_period=SPAN[1])
    return c


def receipt(owners,producer,consumer,semantic):
    return dict(producer=producer,semantic=semantic,result=completed(producer,owners[producer]),
        source_dimensions=list(dimensions(owners[producer])),consumer_dimensions=list(dimensions(owners[consumer])),
        evidence='Separate synthetic reviewer tied current native source and specialist result')


def owner_cases():
    out={}
    tax=context(financing_case('income-taxes'),SUB,'USD','US')
    r=tax['jurisdictions'][0]
    r.update(pretax_profit='0',taxable_income='0',expected_current='0',closing_current='0',tax_paid='0',closing_dta='0',closing_dtl='25',
        etr_adjustments=[],etr_inventory=[],difference_inventory=['land-uplift'])
    d=r['differences'][0];r['differences']=[d]
    d.update(id='land-uplift',asset_identity='LAND-1',carrying='100',tax_base='0',difference='100',allocation='acquisition',allocation_handoff='ppa',expected_gross='25')
    tax['acquisition_effective_date']=ACQUIRED
    tax['handoffs']=handoffs(tax,{'ppa':'Tax allocation specialist'});tax['handoffs']['ppa']['tax_movement']='25'
    tax.update(statement_tax_expense='0',statement_pretax='0');tax['controls']['population_amount']='0'
    gl(tax,{'Deferred tax liability':'-25','Acquisition tax clearing':'25','Current tax expense':'0','Current tax payable':'0','Deferred tax expense':'0','Uncertain tax liability':'0'})
    out['income-taxes']=certify('income-taxes',tax)

    bc=context(acquisition(),SUB,'USD','US');bc['acquisition'].update(date=ACQUIRED,acquirer=PARENT)
    bc['assets'][0].update(id='cash',account='cash',amount='900')
    uplift=copy.deepcopy(bc['assets'][0]);uplift.update(id='land-uplift',asset_identity='LAND-1',account='land uplift',amount='100',valuation_evidence='Independent acquisition-date land appraisal, USD100 incremental FV')
    bc['assets'].append(uplift);bc['liabilities'][0].update(account='debt',amount='200')
    dtl=copy.deepcopy(bc['liabilities'][0]);dtl.update(id='dtl',account='Deferred tax liability',amount='25',measurement_basis='reviewed_exception',valuation_evidence='Qualified acquisition-date tax workpaper')
    bc['liabilities'].append(dtl);bc['nci'].update(method='fair_value',fair_value='200',memo='Independently qualified full-goodwill NCI valuation USD200')
    bc['qualified_nci_election']='Full-goodwill fair-value'
    bc['qualified_legal_extract']='Signed completion 1 July 2026. Ordinary operating business acquired by Parent. Transferred experienced operating team, service-delivery systems and substantive documented processes with recurring customer outputs. 80% voting rights; substantive board appointment and operating decision rights; no participating rights held by minority. Price USD800; independent NCI fair value USD200. No earnout, prior interest or ownership change.'
    bc['costs'].update(direct='0',other='0');out['business-combinations']=bc
    bc['qualified_owner_results']=[receipt(out,'income-taxes','business-combinations','acquisition_dtl')]
    out['business-combinations']=certify('business-combinations',bc)

    fc=context(fx(),SUB,'USD','US');fc['items']=[];fc['currency']['presentation']='EUR'
    t=fc['translation'];t.update(operation_id=SUB,opening_net_assets='1000',opening_rate='.9',closing_rate='.8',profit='100',profit_rate='.85',reported_closing_net_assets='1100')
    local=[('cash','1125','asset','.8'),('debt','-200','liability','.8'),('IC payable','-125','liability','.8'),
        ('sub equity','-700','equity','.9'),('sub revenue','-250','profit','.85'),('sub expense','150','profit','.85'),
        ('land uplift','100','asset','.8'),('Deferred tax liability','-25','liability','.8'),('goodwill','225','asset','.8'),('acquisition adjustment equity','-300','equity','.9')]
    t['tb']=[dict(id=i,balance=b,category=k,rate=rate,memo='Independent rate schedule: closing assets/liabilities; acquisition equity; supported post-acquisition weighted transactions') for i,b,k,rate in local]
    fc['activity_selection']=dict(source_start=SPAN[0],source_end=SPAN[1],effective_date=ACQUIRED,
        records=[dict(id='pre',entity=SUB,currency='USD',start=SPAN[0],end='2026-06-30',revenue='200',expense='50'),
                 dict(id='post',entity=SUB,currency='USD',start=ACQUIRED,end=SPAN[1],revenue='250',expense='150')],
        full_year_balances={'cash':'1125','debt':'-200','IC payable':'-125','sub equity':'-550','sub revenue':'-450','sub expense':'200'},equity_account='sub equity',
        inventory=['pre','post'],included_ids=['post'],included_profit='100',revenue_account='sub revenue',expense_account='sub expense',evidence='Complete pre/post acquisition activity export and signed completion date')
    fc['qualified_acquisition']=copy.deepcopy(completed('business-combinations',out['business-combinations'])['calculations'])
    out['foreign-currency']=fc;fc['qualified_owner_results']=[receipt(out,'business-combinations','foreign-currency',s) for s in ('acquisition_goodwill','acquisition_basis')]
    out['foreign-currency']=certify('foreign-currency',fc)

    ic=context(operational('intercompany-accounting'),PARENT,'EUR','NL');p=ic['pairs'][0]
    p.update(entity_a=PARENT,entity_b=SUB,currency='USD',transaction_id='IC-LOAN-1',date='2026-09-01',opening_book_evidence='Already posted demand loan at start of September-to-year-end reconciliation window; not a January opening balance',opening_a='125',opening_b='125',
        confirmed_a='125',confirmed_b='125',initial_rate_a='.8',initial_rate_b='1',rate_a='.8',rate_b='1',
        opening_book_a='100',opening_book_b='125',book_a='100',book_b='125',gl_a='100',gl_b='125')
    ic['controls']['population_amount']='125';out['intercompany-accounting']=certify('intercompany-accounting',ic)

    imp=context(impairment(),GROUP,'EUR','NL');imp['assets']=[dict(id='gw',account='goodwill',type='goodwill',carrying='180',floor='0',no_impairment_ceiling='180',valuation_evidence='Completed acquisition and foreign-operation translation'),
        dict(id='net-assets',account='CGU net assets',type='finite',carrying='700',floor='0',no_impairment_ceiling='700',valuation_evidence='Qualified group CGU carrying perimeter')]
    imp['valuation'].update(cash_flows=[dict(year='1',amount='990')],discount_rate='0.1',terminal_value='0',fv_less_costs='900',fair_value='900',undiscounted='900',memo='Independent EUR900 recoverable amount valuation for US-operation CGU; no forecast generated')
    imp['unit']['source_entity']=SUB;imp['qualified_unit_carrying']='880'
    out['asset-impairment']=imp;imp['qualified_owner_results']=[receipt(out,'foreign-currency','asset-impairment',s) for s in ('unit_carrying','goodwill_carrying')]
    out['asset-impairment']=certify('asset-impairment',imp)

    cons=context(consolidation(),GROUP,'EUR','NL');ctrl=cons['entities'][0]['control']
    pb={'parent cash':'1380','investment':'720','IC receivable':'100','parent equity':'-2000','parent revenue':'-300','parent expense':'100'}
    sb={k:str(v) for k,v in completed('foreign-currency',out['foreign-currency'])['calculations']['translation']['translated_tb'].items()};sb['translation reserve']='105'
    cons['entities']=[dict(id=PARENT,parent=True,balances=pb,control=copy.deepcopy(ctrl),translation=None,policy_alignment=True,date_alignment=True),
        dict(id=SUB,parent=False,balances=sb,control=copy.deepcopy(ctrl),translation=None,policy_alignment=True,date_alignment=True)]
    cons['investments']=[dict(subsidiary=SUB,parent_entity=PARENT,investment_account='investment',investment='720',
        acquisition_equity={'sub equity':'630','acquisition adjustment equity':'270'},fair_value_adjustments={},goodwill='0',nci_at_acquisition='180',
        acquisition_memo='Completed PPA already translated into qualified subsidiary assembly; eliminate investment/equity only')]
    cons['intercompany']=[dict(seller=SUB,buyer=PARENT,debit_account='IC payable',credit_account='IC receivable',amount='100',matched=True,family='balance',source_id='IC-LOAN-1')]
    cons['nci']=[dict(subsidiary=SUB,ownership='.8',opening='180',adjusted_profit='85',adjusted_oci='-105',dividends='0',other='0',allocation_memo='Full-goodwill 80/20 ordinary rights, post-acquisition profit and OCI only')]
    cons['nci_attribution_account']='parent equity';cons['specialist_receipts']=dict(nci_oci='-21',impairment='0')
    mapping={k:('assets' if k in ('parent cash','investment','IC receivable','cash','land uplift','goodwill') else 'liabilities' if k in ('debt','IC payable','Deferred tax liability') else 'income' if 'revenue' in k else 'expenses' if 'expense' in k else 'equity') for k in set(pb)|set(sb)|{'noncontrolling interest'}}
    cons['statement_mapping']=mapping
    cons['equity_bridge']=dict(opening='2000',profit='285',oci='-105',owner_transactions='180',other='0',closing='2360',memo='Parent opening plus post-acquisition group results, CTA and NCI acquisition')
    cons['cta_bridge']=dict(opening='0',translation='105',disposals='0',other='0',closing='105',cta_accounts=['translation reserve'],memo='Debit balance represents EUR105 translation loss in OCI')
    cons['cash_flow_bridge']=dict(opening_cash='2000',operating='285',investing='90',financing='0',fx='-95',closing_cash='2280',cash_accounts=['parent cash','cash'],memo='Reviewed acquired cash810 less consideration720; post-acquisition cash85; Parent cash200; closing translation cash-95')
    out['consolidation']=cons
    cons['qualified_acquisition']=copy.deepcopy(completed('business-combinations',out['business-combinations'])['calculations'])
    cons['qualified_owner_results']=[receipt(out,p,'consolidation',s) for p,s in [('business-combinations','acquisition_basis'),('foreign-currency','translated_population'),('foreign-currency','post_acquisition_profit'),('foreign-currency','nci_oci'),('intercompany-accounting','matched_intercompany'),('asset-impairment','impairment')]]
    out['consolidation']=certify('consolidation',cons)
    fs=context(reporting(),GROUP,'EUR','NL')
    balances=completed('consolidation',out['consolidation'])['calculations']['consolidated_balances']
    def tb(rows):return [dict(id=k,balance=str(v),category=cat,line=k,source_version='qualified-group-v1',classification_memo='Reviewed consolidated population classification',cash_account=k in ('cash','parent cash')) for k,v,cat in rows]
    cats={'assets':'asset','liabilities':'liability','equity':'equity','income':'revenue','expenses':'expense'}
    fs['current_tb']=tb([(k,v,'oci' if k=='translation reserve' else cats[mapping[k]]) for k,v in balances.items()])
    fs['comparative_tb']=tb([('parent cash','2000','asset'),('parent equity','-2000','equity')])
    fs['qualified_consolidated_balances']={k:str(v) for k,v in balances.items()}
    fs['equity_bridge']=[dict(id='owners',opening='2000',profit='268',oci='-84',owner_transactions='0',retrospective_adjustments='0',other='0',closing='2184',memo='Qualified group result less NCI attribution'),
        dict(id='nci',opening='0',profit='17',oci='-21',owner_transactions='180',retrospective_adjustments='0',other='0',closing='176',memo='Completed consolidated NCI rollforward')]
    fs['cash_flow'].update(start_amount='285',adjustments=[],opening='2000',closing='2280',investing='90',financing='0',fx='-95',classifications=[dict(id='op',date=SPAN[1],kind='net_operating',**{'class':'operating'},amount='285',memo='Complete group operating cash population'),dict(id='acq',date=ACQUIRED,kind='acquisition_net_cash',**{'class':'investing'},amount='90',memo='Acquired cash810 less consideration720')])
    fs['notes'][0].update(amount='2280')
    out['financial-statements']=fs
    fs['qualified_owner_results']=[receipt(out,'consolidation','financial-statements',s) for s in ('consolidated_population','nci_closing','nci_profit','nci_oci')]
    out['financial-statements']=certify('financial-statements',fs)
    def governance_context(c):
        def adapt(v):
            if isinstance(v,dict):return {k:adapt(x) for k,x in v.items()}
            if isinstance(v,list):return [adapt(x) for x in v]
            if v=='Synthetic Group':return GROUP
            if v=='USD':return 'EUR'
            return v
        c=adapt(c);c['functional_currency']='EUR';return c
    a=governance_context(governance_case('management-accounting-analytics'))
    a['accounts'][0].update(amount='285',management_amount='285',account='group result')
    a['account_source']['records']=copy.deepcopy(a['accounts']);a['controls']['population_amount']='285'
    for d in a['documents']:
        data=d['content']
        if d['id'] in ('current-books','prior-books'):
            n='285' if d['id']=='current-books' else '0';data.update(account='group result',statutory_amount=n,management_amount=n,gross_amount=n);data['records'][0].update(account='group result',amount=n)
        if d['id']=='actual-drivers':data.update(account='group result',drivers=[dict(id='parent',amount='200'),dict(id='post-acquisition',amount='85')],driver_inventory=['parent','post-acquisition'])
    a['explanations'][0].update(account='group result',amount='285')
    a['imports']=[row(a,'group-result',package='financial-statements',case=out['financial-statements'],result=completed('financial-statements',out['financial-statements']),mode='evidence_only')]
    ref=dict(owner_import='group-result',result_path=['current','profit'],amount='285')
    prior=['2025-01-01','2025-12-31'];base=dict(entity=GROUP,currency='EUR',unit='EUR',metric='account_balance',presentation_basis='signed_balance')
    for id,n,span,components in [('group-current','285',SPAN,[dict(sign=1,ref=ref)]),('group-prior','0',prior,[])]:
        document(a,id,dict(base,period=span,kind='actual',posted_only=True,amount=n,records=[dict(id=id+'-posted',amount=n)],inventory=[id+'-posted'],version='actual-v1',approved=True,supplied=True,approved_on='2025-12-31',owner_components=components,profit=n),currency='EUR')
    document(a,'group-drivers',dict(base,period=SPAN,baseline_period=prior,comparator_version='actual-v1',method='source_flux',source_owner='financial-statements',source_metric='group profit',category='mixed',evidence_class='bridge_attribution',confidence='high',population_complete=True,
        records=[dict(id='group',baseline_amount='0',current_amount='285',current_owner=ref,posted_only=True,economic_components=['parent-result','post-acquisition-result'])],inventory=['group'],supported_post_profit='85',parent_profit='200'),currency='EUR')
    a['diagnostic']=dict(component_ties=[dict(groups=['contribution'],current_owner=ref,baseline_field='profit',sign=1)],unit='EUR',metric='account_balance',presentation_basis='signed_balance',current={'doc':'group-current'},comparator=dict(doc='group-prior',kind='actual',version='actual-v1',period=prior,frozen_on='2025-12-31'),
        groups=[dict(id='contribution',doc='group-drivers',method='source_flux',sign=1,labels=dict(movement='Standalone and supported post-acquisition contribution'),accounting_check=dict(**ref,issue='Group acquisition contribution',reason='Confirm analytical contribution against qualified consolidated statement result'))],group_inventory=['contribution'],tolerance='.01',materiality='1',
        hypotheses=[dict(id='full-year-contribution',observation='Acquisition completed midyear',hypothesis='Full-year subsidiary profit is acquisition contribution',evidence_class='bridge_attribution',tests=[dict(doc='group-drivers',field='supported_post_profit',operator='equal',value='212.5')])],signals=[],revenue=None)
    for d in a['documents']:d['content_hash']=digest(d['content'])
    a['qualified_contribution_population']=copy.deepcopy(completed('consolidation',out['consolidation'])['calculations']['consolidated_balances'])
    a['entity_contribution']=dict(entity=PARENT,document='group-drivers',field='parent_profit')
    out['management-accounting-analytics']=a
    a['qualified_owner_results']=[receipt(out,p,'management-accounting-analytics',s) for p,s in [('foreign-currency','post_acquisition_contribution'),('financial-statements','group_profit'),('consolidation','entity_contribution_population')]]
    out['management-accounting-analytics']=governance_ready('management-accounting-analytics',c=refresh_release(a))

    disc=governance_context(governance_case('disclosure-management'))
    imp=disc['imports'][0];imp.update(case=out['financial-statements'],result=completed('financial-statements',out['financial-statements']))
    dby={d['id']:d for d in disc['documents']}
    dby['statement']['content'].update(amount='285');dby['issued-prior']['content'].update(amount='0')
    disc['requirements'][0].update(amount='285',owner_requirement=imp['result']['disclosures_impacted'][0]);disc['notes'][0].update(amount='285',prior_amount='0',narrative=imp['result']['conclusion'])
    # Five scoped group statement notes, each tied to an actual completed FS
    # assertion. No universal filing checklist or cross-currency owner import.
    for key,path,amount in [('goodwill',['current','lines','goodwill'],'180'),('nci',['equity_components',1,'closing'],'176'),('translation-oci',['current','oci'],'-105'),('deferred-tax',['current','lines','Deferred tax liability'],'-20')]:
        req=copy.deepcopy(disc['requirements'][0]);rid='requirement-'+key
        req.update(id=rid,requirement_key=key+'-support',requirement_text='Qualified consolidated '+key+' statement support',amount=amount,metric=path[-1],result_path=path,applicability_doc='applicability-'+key)
        disc['requirements'].append(req)
        note=copy.deepcopy(disc['notes'][0]);note.update(id='note-'+key,requirement_id=rid,amount=amount,note_location='Controlled group '+key+' note',issued_prior_doc='issued-prior-'+key,statement_doc='statement-'+key)
        disc['notes'].append(note)
        for source_id,target_id,changes in [('applicability','applicability-'+key,dict(requirement_id=rid)),('issued-prior','issued-prior-'+key,dict(requirement_key=key+'-support',amount='0')),('statement','statement-'+key,dict(metric=path[-1],amount=amount))]:
            d=copy.deepcopy(dby[source_id]);d['id']=target_id;d['content'].update(changes);disc['documents'].append(d);disc['document_inventory'].append(target_id)
    disc['note_inventory']=[r['id'] for r in disc['notes']]
    disc['requirement_source']['records']=copy.deepcopy(disc['requirements']);disc['requirement_source']['inventory']=[r['id'] for r in disc['requirements']]
    disc['source_inventory']=[r['id'] for r in disc['requirements']]
    disc['controls'].update(population_count=5,population_amount='766')
    for d in disc['documents']:d['content_hash']=digest(d['content'])
    out['disclosure-management']=governance_ready('disclosure-management',c=refresh_release(disc))
    for pkg,c in out.items():completed(pkg,c)
    return out


# Explicit company export mappings. Schemas/certifications are prepared separately
# after intake; raw sources contain company records, not an internal Case.
MAP=[
 ('tax-asset','tax_temporary_difference','asset_identity','tax','asset_id',('jurisdictions',0,'differences',0,'asset_identity'),'identity'),
 ('bc-asset','acquisition','asset_identity','purchase','asset_id',('assets','land-uplift','asset_identity'),'identity'),
 ('tax-effective','tax_temporary_difference','acquisition_effective_date','tax','effective_date',('acquisition_effective_date',),'iso_date'),
 ('tax','tax_temporary_difference','uplift_tax_base','tax','tax_base',('jurisdictions',0,'differences',0,'tax_base'),'decimal'),
 ('tax-rate','tax_temporary_difference','reversal_rate','tax','rate',('jurisdictions',0,'differences',0,'reversal_rate'),'decimal'),
 ('tax-carrying','tax_temporary_difference','tax_carrying','tax','carrying',('jurisdictions',0,'differences',0,'carrying'),'decimal'),
 ('bc-costs','acquisition','acquisition_costs','purchase','acquisition_costs',('costs','direct'),'decimal'),
 ('bc-date','acquisition','acquisition_date','purchase','completed',('acquisition','date'),'iso_date'),
 ('bc-price','acquisition','consideration','purchase','cash_price',('consideration','cash'),'decimal'),
 ('bc-nci','acquisition','initial_nci','purchase','nci_value',('nci','fair_value'),'decimal'),
 ('bc-owned','acquisition','ownership','purchase','ownership',('nci','ownership'),'decimal'),
 ('bc-cash','acquisition','acquired_cash','purchase','cash_assets',('assets','cash','amount'),'decimal'),
 ('bc-fv','acquisition','fair_value_uplift','purchase','land_uplift',('assets','land-uplift','amount'),'decimal'),
 ('bc-debt','acquisition','assumed_debt','purchase','debt',('liabilities','debt','amount'),'decimal'),
 ('bc-dtl','acquisition','acquisition_dtl','purchase','dtl',('liabilities','dtl','amount'),'decimal'),
 ('fx-close','foreign_operation','closing_rate','rates','closing',('translation','closing_rate'),'decimal'),
 ('fx-open','foreign_operation','acquisition_rate','rates','acquisition',('translation','opening_rate'),'decimal'),
 ('fx-profit-rate','foreign_operation','profit_rate','rates','post_average',('translation','profit_rate'),'decimal'),
 ('fx-post-profit','foreign_operation','included_profit','activity','post_profit',('translation','profit'),'decimal'),
 ('fx-pre-revenue','foreign_operation','pre_revenue','activity','pre_revenue',('activity_selection','records',0,'revenue'),'decimal'),
 ('fx-pre-expense','foreign_operation','pre_expense','activity','pre_expense',('activity_selection','records',0,'expense'),'decimal'),
 ('fx-post-revenue','foreign_operation','post_revenue','activity','post_revenue',('activity_selection','records',1,'revenue'),'decimal'),
 ('fx-post-expense','foreign_operation','post_expense','activity','post_expense',('activity_selection','records',1,'expense'),'decimal'),
 ('ic-date','intercompany','loan_effective_date','ic','originated',('pairs',0,'date'),'iso_date'),
 ('ic-denomination','intercompany','principal_currency','ic','principal_currency',('pairs',0,'currency'),'identity'),
 ('ic-rate-a','intercompany','parent_conversion_rate','ic','parent_rate',('pairs',0,'rate_a'),'decimal'),
 ('ic-rate-b','intercompany','subsidiary_conversion_rate','ic','subsidiary_rate',('pairs',0,'rate_b'),'decimal'),
 ('ic-a','intercompany','parent_principal','ic','principal',('pairs',0,'confirmed_a'),'decimal'),
 ('ic-b','intercompany','sub_principal','ic','reciprocal',('pairs',0,'confirmed_b'),'decimal'),
 ('ic-counterparty','intercompany','counterparty','ic','counterparty',('pairs',0,'entity_b'),'identity'),
 ('ic-id','intercompany','transaction_id','ic','transaction',('pairs',0,'transaction_id'),'identity'),
 ('imp-fv','impairment_valuation','fvlc_value','valuation','fvlc',('valuation','fv_less_costs'),'decimal'),
 ('imp-recoverable','impairment_valuation','recoverable_value','valuation','recoverable',('recoverable',),'decimal'),
 ('imp-cashflow','impairment_valuation','supplied_valuation_cashflow','valuation','cashflow_year1',('valuation','cash_flows',0,'amount'),'decimal'),
 ('imp-rate','impairment_valuation','supplied_discount_rate','valuation','discount_rate',('valuation','discount_rate'),'decimal'),
 ('imp-terminal','impairment_valuation','supplied_terminal_value','valuation','terminal_value',('valuation','terminal_value'),'decimal'),
 ('imp-unit','impairment_valuation','unit_entity','valuation','operation_entity',('unit','source_entity'),'identity'),
 ('imp-fairvalue','impairment_valuation','fair_value','valuation','fair_value',('valuation','fair_value'),'decimal'),
 ('imp-undiscounted','impairment_valuation','undiscounted','valuation','undiscounted',('valuation','undiscounted'),'decimal'),
 ('imp-gw','impairment_valuation','goodwill_carrying','valuation','goodwill',('assets','gw','carrying'),'decimal'),
 ('imp-net','impairment_valuation','unit_net_assets','valuation','net_assets',('assets','net-assets','carrying'),'decimal'),
 ('cons-power','group_structure','substantive_power','rights','power',('entities',SUB,'control','substantive_power'),'boolean'),
 ('cons-link','group_structure','power_returns_link','rights','link',('entities',SUB,'control','power_returns_link'),'boolean'),
 ('cons-returns','group_structure','variable_returns','rights','returns',('entities',SUB,'control','variable_returns'),'boolean'),
 ('fs-profit','statement','group_profit','pack','profit',('cash_flow','start_amount'),'decimal'),
 ('fs-nci','statement','closing_nci','pack','nci',('equity_bridge','nci','closing'),'decimal'),
 ('analytics-post','analytics','supported_acquisition_contribution','analytics-source','post_acquisition',('documents','group-drivers','content','supported_post_profit'),'decimal'),
 ('analytics-parent','analytics','parent_contribution','analytics-source','parent',('documents','group-drivers','content','parent_profit'),'decimal'),
 ('analytics-group','analytics','group_profit','analytics-source','profit',('accounts','cash-metric','amount'),'decimal'),
 ('disclosure-profit','disclosure','profit_support','note-source','profit',('requirements','requirement-1','amount'),'decimal'),
]

for key,column in [('goodwill','goodwill'),('nci','nci'),('translation-oci','oci'),('deferred-tax','tax')]:
    MAP.append(('note-'+key,'disclosure',column+'_support','note-source',column,('requirements','requirement-'+key,'amount'),'decimal'))
for i,account in enumerate(('parent cash','investment','IC receivable','parent equity','parent revenue','parent expense'),2):
    MAP.append(('parent-tb-'+str(i),'group_structure','parent_'+account.lower().replace(' ','_'),'parent-tb','balance',('entities',PARENT,'balances',account),'decimal',i))
for i,account in enumerate(('cash','debt','IC payable','sub equity','sub revenue','sub expense'),2):
    MAP.append(('sub-tb-'+str(i),'foreign_operation','full_year_'+account.lower().replace(' ','_'),'sub-tb','balance',('activity_selection','full_year_balances',account),'decimal',i))


def mappings():
    return [tuple(row)+((None,) if len(row)==7 else ()) for row in MAP]


def group_sources(clean=False):
    def raw(id,name,entity,cur,text,kind='accounting_records',controlled=True):
        return RawSource(id,name,'csv',text,dict(entity=entity,period=SPAN,currency=cur,comparator='actual',version='corrected-v2' if clean else 'v1',
            source_system='Controlled synthetic company export',controlled_export=controlled,as_of=SPAN[1],extracted_at='2027-02-01',source_type=kind,approval_status='reviewed_test_evidence'))
    sources=[
        raw('purchase','Acquisition completion and purchase model.csv',SUB,'USD','completed,cash_price,nci_value,ownership,cash_assets,land_uplift,debt,dtl,asset_id,acquisition_costs\n2026-07-01,800,200,0.8,900,100,200,25,LAND-1,0\n','acquisition_model'),
        raw('tax','Reviewed acquisition tax workpaper.csv',SUB,'USD','tax_base,rate,carrying,effective_date,asset_id\n0,0.25,100,2026-07-01,LAND-1\n','tax_evidence'),
        raw('rates','Approved foreign operation rates.csv',SUB,'USD','closing,acquisition,post_average\n0.8,0.9,0.85\n','approved_rates'),
        raw('activity','Full year subsidiary activity split.csv',SUB,'USD','pre_revenue,pre_expense,post_revenue,post_expense,post_profit\n200,50,250,150,100\n'),
        raw('ic','Bilateral loan confirmation.csv',PARENT,'EUR','principal,reciprocal,counterparty,transaction,principal_currency,parent_rate,subsidiary_rate,originated,terms\n125,125,Subsidiary-US,IC-LOAN-1,USD,0.8,1,2026-09-01,Repayable on demand; already posted before this reconciliation\n'),
        raw('valuation','Independent goodwill CGU valuation.csv',GROUP,'EUR','recoverable,goodwill,net_assets,fvlc,cashflow_year1,discount_rate,terminal_value,fair_value,undiscounted,operation_entity\n900,180,700,900,990,0.1,0,900,900,Subsidiary-US\n','independent_valuation'),
        raw('rights','Group rights and perimeter review.csv',GROUP,'EUR','power,returns,link\ntrue,true,true\n','legal_entity_evidence'),
        raw('pack','final_consolidation_v9.csv',GROUP,'EUR','profit,nci\n285,176\n','management_workpaper'),
        raw('analytics-source','Group contribution support.csv',GROUP,'EUR','profit,parent,post_acquisition\n285,200,85\n'),
        raw('note-source','Group note support.csv',GROUP,'EUR','profit,goodwill,nci,oci,tax,note\n285,180,176,-105,-20,Group performance\n'),
        raw('ic-parent','Parent IC ledger closing.csv',PARENT,'EUR','ic_closing\n'+('100' if clean else '105')+'\n'),
        raw('ic-confirmed','Bilateral FX reconciliation.csv',PARENT,'EUR','ic_closing,confirmed_by\n100,bilateral-source\n'),
    ]
    for id,name,entity,cur,text,kind in [
        ('spa','SPA and completion extract',SUB,'USD','Signed completion 1 July 2026. Ordinary operating business acquired by Parent. Transferred experienced operating team, service-delivery systems and substantive documented processes with recurring customer outputs. 80% voting rights; substantive board appointment and operating decision rights; no participating rights held by minority. Price USD800; independent NCI fair value USD200. No earnout, prior interest or ownership change.','legal_entity_evidence'),
        ('appraisal','Qualified acquisition appraisal',SUB,'USD','Asset LAND-1. Independent acquisition-date incremental land fair value USD100, supported by an approved valuation report. No depreciable FV uplift. Acquired cash USD900 and debt USD200. Independently valued non-controlling 20% equity interest fair value USD200.','independent_valuation'),
        ('policy','Group and currency policy',GROUP,'EUR','Parent functional/presentation EUR; Subsidiary functional USD. Full-goodwill fair-value NCI election approved for this IFRS acquisition. Group adjustments only. Year-end goodwill CGU test consumes independently supplied valuation. Tax rate25% and zero uplift tax base are independently reviewed synthetic inputs, not law inferred from jurisdiction.','accounting_policy'),
        ('commentary','Management commentary',GROUP,'EUR','The acquisition contributed the subsidiary full-year profit of USD250 this year.','management_commentary'),
    ]:
        sources.append(RawSource(id,name+'.md','markdown',text,dict(entity=entity,period=SPAN,currency=cur,comparator='actual',version='v1',source_type=kind,controlled_export=False,approval_status='qualified_test_source')))
    # Independently frozen balanced legal-entity TB exports, distinct from PPA
    # and translated consolidation workpapers.
    sources.append(raw('parent-tb','Parent trial balance.csv',PARENT,'EUR','account,balance\nparent cash,1380\ninvestment,720\nIC receivable,100\nparent equity,-2000\nparent revenue,-300\nparent expense,100\n'))
    sources.append(raw('sub-tb','Subsidiary USD trial balance.csv',SUB,'USD','account,balance\ncash,1125\ndebt,-200\nIC payable,-125\nsub equity,-550\nsub revenue,-450\nsub expense,200\n'))
    from dataclasses import replace
    sources=[replace(s,metadata=dict(s.metadata,amount_currency='USD')) if s.id=='ic' else s for s in sources]
    return sources


def group_proposal(sources):
    inventory=Inventory(sources)
    p=StructuredProposal(cl(OBJECTIVE,status='USER_STATED',confidence=1),cl('Year-end group accounting review'),cl('CLOSE_REVIEW'),
        secondary_modes=[cl('ACCOUNTING_DETERMINATION'),cl('RECONCILIATION_INVESTIGATION'),cl('REPORTING')])
    for id,family,attribute,source,column,path,method,row in mappings():
        ref=cell(inventory,source,column,row);field=inventory.fields()[ref];meta=inventory.extractions[source].source['metadata']
        dims=dict(entity=meta['entity'],currency=meta['currency'],period=SPAN,comparator='actual',unit='currency' if method=='decimal' else 'text')
        if id in ('ic-a','ic-b'):dims['amount_currency']=meta['amount_currency']
        p.facts.append(FactCandidate(id,family,attribute,cl(transform(field['value'],method),[ref],'EXTRACTED',.99),dims,
            FACT_ADAPTERS[family][0],confirmation_required=False,transformation=method))
    for source in ('ic-parent','ic-confirmed'):
        ref=cell(inventory,source,'ic_closing')
        p.facts.append(FactCandidate(source,'intercompany','ic_closing',cl(transform(inventory.fields()[ref]['value'],'decimal'),[ref],'EXTRACTED',.99),
            dict(entity=PARENT,currency='EUR',period=SPAN,comparator='actual',unit='currency'),confirmation_required=False,transformation='decimal'))
    dependencies={'business-combinations':['income-taxes'],'foreign-currency':['business-combinations'],
        'asset-impairment':['foreign-currency'],'consolidation':['foreign-currency','intercompany-accounting','asset-impairment'],'financial-statements':['consolidation'],
        'management-accounting-analytics':['financial-statements'],'disclosure-management':['financial-statements']}
    for family in dict.fromkeys(f.family for f in p.facts):
        fs=[f for f in p.facts if f.family==family];owner=FACT_ADAPTERS[family][0]
        p.issues.append(cl(dict(id=owner,scope_id=GROUP if owner in ('consolidation','asset-impairment','financial-statements','disclosure-management','management-accounting-analytics') else PARENT if owner=='intercompany-accounting' else SUB,owner=owner,family=family,fact_ids=[f.id for f in fs],dependencies=dependencies.get(owner,[]),required_fields=[]),[e for f in fs for e in f.claim.evidence]))
    return p


def group_review_pack(prepared):
    owners=owner_cases();bindings=[]
    selected={x.value['owner'] for x in prepared._proposal.issues}
    fact_ids={f.id for f in prepared._proposal.facts}
    for owner,native in owners.items():
        native['qualified_owner_results']=[r for r in native.get('qualified_owner_results',[]) if r['producer'] in selected]
        if 'business-combinations' not in selected:native.pop('qualified_acquisition',None)
    for id,family,attribute,source,column,path,method,row in mappings():
        if id not in fact_ids:continue
        bindings.append(Binding(id,FACT_ADAPTERS[family][0],path,'owner_result' if id=='imp-recoverable' else 'current'))
        if id=='imp-recoverable':continue
        # Normalize native lexical decimals against the explicitly transformed
        # source candidate; numerical accounting is separately reperformed.
        candidate=next(f for f in prepared._proposal.facts if f.id==id)
        at(owners[FACT_ADAPTERS[family][0]],list(path[:-1]))[path[-1]]=copy.deepcopy(candidate.claim.value)
    documents=[]
    text_assertions=[
        TextAssertion('spa','business-combinations',r'\A([\s\S]+)\Z',('qualified_legal_extract',)),
        TextAssertion('spa','business-combinations',r'Price USD([0-9]+(?:\.[0-9]+)?);',('consideration','cash'),'decimal'),
        TextAssertion('spa','business-combinations',r'NCI fair value USD([0-9]+(?:\.[0-9]+)?)\.',('nci','fair_value'),'decimal'),
        TextAssertion('spa','business-combinations',r'([0-9]+(?:\.[0-9]+)?)% voting rights',('nci','ownership'),'percentage'),
        TextAssertion('spa','business-combinations',r'acquired by ([A-Za-z][A-Za-z0-9-]*)\.',('acquisition','acquirer')),
        TextAssertion('spa','business-combinations',r'Signed completion (\d{1,2} [A-Za-z]+ \d{4})',('acquisition','date'),'calendar_date'),
        TextAssertion('appraisal','business-combinations',r'Asset (LAND-[0-9]+)\.',('assets','land-uplift','asset_identity')),
        TextAssertion('appraisal','business-combinations',r'non-controlling 20% equity interest fair value USD([0-9]+(?:\.[0-9]+)?)\.',('nci','fair_value'),'decimal'),
        TextAssertion('appraisal','business-combinations',r'incremental land fair value USD([0-9]+(?:\.[0-9]+)?), supported by an approved valuation report',('assets','land-uplift','amount'),'decimal'),
        TextAssertion('policy','business-combinations',r'(Full-goodwill fair-value) NCI election approved',('qualified_nci_election',)),
        TextAssertion('policy','foreign-currency',r'Subsidiary functional ([A-Z]{3})',('currency','functional')),
    ]
    for source,owner in [('spa','business-combinations'),('appraisal','business-combinations'),('policy','consolidation'),('parent-tb','consolidation'),('sub-tb','foreign-currency')]:
        if owner not in selected:continue
        extracted=prepared._inventory.extractions[source].source
        owners[owner].setdefault('qualified_source_documents',{})[source]=dict(fingerprint=extracted['fingerprint'],metadata=extracted['metadata'])
        documents.append(DocumentBinding(source,owner,('qualified_source_documents',source)))
    populations=[
        PopulationBinding('parent-tb','account','consolidation',('entities',PARENT,'balances'),value_column='balance'),
        PopulationBinding('sub-tb','account','foreign-currency',('activity_selection','full_year_balances'),value_column='balance')]
    text_assertions=[x for x in text_assertions if x.owner in selected]
    populations=[x for x in populations if x.owner in selected]
    from dataclasses import asdict
    for pkg,native in owners.items():
        native['source_semantic_controls']=dict(text_assertions=[asdict(x) for x in text_assertions if x.owner==pkg],populations=[asdict(x) for x in populations if x.owner==pkg])
    # Requalify only synthetic fixtures; production never manufactures approvals.
    # Downstream receipts are regenerated against those current fixture cases.
    for owner in ['income-taxes','business-combinations','foreign-currency','intercompany-accounting','asset-impairment','consolidation','financial-statements','management-accounting-analytics','disclosure-management']:
        for r in owners[owner].get('qualified_owner_results',[]):
            r.update(result=completed(r['producer'],owners[r['producer']]),source_dimensions=list(dimensions(owners[r['producer']])),consumer_dimensions=list(dimensions(owners[owner])))
        for imp in owners[owner].get('imports',[]):
            imp.update(case=owners[imp['package']],result=completed(imp['package'],owners[imp['package']]))
        for d in owners[owner].get('documents',[]):
            if 'content' in d:d['content_hash']=digest(d['content'])
        owners[owner]=governance_ready(owner,c=refresh_release(owners[owner])) if owner in ('management-accounting-analytics','disclosure-management') else certify(owner,owners[owner])
    request=dict(case_id='group-accounting',objective=prepared._proposal.objective.value,scope=copy.deepcopy(SCOPE),facts={family:owners[owner] for family,(owner,_) in FACT_ADAPTERS.items() if family in {f.family for f in prepared._proposal.facts}})
    native=[dict(owner=issue.value['owner'],case_fingerprint=completed(issue.value['owner'],owners[issue.value['owner']])['case_fingerprint'],
        journals=completed(issue.value['owner'],owners[issue.value['owner']]).get('journal_entry_implications',[])) for issue in prepared._proposal.issues]
    evidence=[]
    routes={'income-taxes':('business-combinations','acquisition_dtl'),'business-combinations':('foreign-currency','acquisition_basis'),'foreign-currency':('consolidation','translated_population')}
    for r in native:
        if r['owner']=='consolidation':continue
        for index,j in enumerate(r['journals']):
            consumer,semantic=routes[r['owner']]
            evidence.append(dict(owner=r['owner'],index=index,source_entity=owners[r['owner']]['entity'],source_currency=dimensions(owners[r['owner']])[-1],
                target_entity=GROUP,level='group',mode='included_in_qualified_source',receipt_consumer=consumer,semantic=semantic))
    journals=completed('consolidation',owners['consolidation'])['journal_entry_implications']
    ownership=[dict(economic_id='consolidation-source-entry-'+str(i),primary=[dict(owner='consolidation',index=i)],witnesses=[],evidence='Qualified consolidation-only source identity '+str(i)) for i in range(len(journals))]
    payload=dict(native=native,assembly_case_fingerprint=completed('consolidation',owners['consolidation'])['case_fingerprint'],target_entity=GROUP,posting_owner='consolidation',evidence_journals=evidence,ownership=ownership)
    if 'consolidation' in selected:request['source_assembly_journals']=dict(assembly_owner='consolidation',target_entity=GROUP,posting_owner='consolidation',evidence_journals=evidence,ownership=ownership,
        review=dict(approved=True,reviewer='Synthetic independent group journal reviewer',preparer='Synthetic group preparer',payload_fingerprint=digest(payload)))
    return ReviewedInputPack(request,bindings,documents=documents,text_assertions=text_assertions,populations=populations)


def run(clean=False):
    sources=group_sources(clean);intake=Intake(FixturePlanner(group_proposal(sources)))
    prepared=intake.prepare(OBJECTIVE,sources,[],SCOPE)
    if not prepared.validation['accepted']:raise AssertionError(prepared.validation)
    return intake.execute(prepared,group_review_pack(prepared))


def narrow(owner,objective):
    """Previously qualified specialist evidence supports a separate narrow review.

    This is not the full Case with required dependencies silently removed. These
    independently reviewed specialist-only workpapers concern the requested
    accounting population; no full Group reporting/journal bridge is asserted.
    """
    sources=group_sources(True);proposal=group_proposal(sources)
    proposal.objective=cl(objective,status='USER_STATED',confidence=1)
    family=next(f.family for f in proposal.facts if f.candidate_owner==owner)
    proposal.facts=[f for f in proposal.facts if f.family==family]
    proposal.issues=[i for i in proposal.issues if i.value['owner']==owner]
    for issue in proposal.issues:issue.value['dependencies']=[]
    proposal.primary_mode=cl('REPORTING');proposal.secondary_modes=[];proposal.bounded_owner=cl(owner)
    engine=Intake(FixturePlanner(proposal));prepared=engine.prepare(objective,sources,[],SCOPE)
    pack=group_review_pack(prepared)
    return engine.execute(prepared,pack)
