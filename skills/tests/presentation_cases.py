"""Wholly synthetic fixtures; no company facts or real reviewer approvals."""
from decimal import Decimal
from cases import base
from operational_cases import approved
from reporting_cases import pol,certified
from production import execute,case_fingerprint

PACKAGES=['earnings-per-share','segment-reporting','subsequent-events']
BLOCKED=['government-grants','borrowing-costs']
FRAMEWORKS=['IFRS','US_GAAP','UK_GAAP','AASB']

def method(c,id,target,**kw):
    return pol(c,id,target=target,resolved=True,scope_memo='Actual hypothetical framework/entity/period scope independently reviewed',boundary_memo='No unsupported exception in synthetic route',**kw)

def dimensions(c,rs):
    for r in rs:r.update(source_entity=c['entity'],source_framework=c['framework'],source_period=[c['period_start'],c['reporting_period']])

def case(pkg,fw='IFRS'):
    c=base(pkg,fw);c.update(execution_date='2027-03-31',imports=[],gl=[],gl_inventory=[])
    c['accounting_policy']=pol(c,'policy');c['disclosure_review']=approved('disclosure',checklist_version='Actual operative period/tier',period_entity_memo='Synthetic completed scope/checklist',complete=True)
    c['controls']=dict(source_version='v1',as_of=c['reporting_period'],population_count=0,population_amount='0',owner='synthetic source owner',reviewer='synthetic independent completeness reviewer',complete=True,policy_version='v1',cutoff_memo='Synthetic complete source population')
    if pkg=='earnings-per-share':
        c['eps_method']=method(c,'eps','EPS accounting',in_scope=True,multiple_class=False,participating_securities=False,additional_per_share=False,uk_scope='specified_ias33',authorization_date='2027-03-31',continuing_control_memo='Continuing operations control',comparative_memo='Complete comparative population',legal_rights_memo='Supplied hypothetical rights',framework_method_memo='Independent operative IAS33/ASC260/specifiedUK/AASB133 method')
        c['share_intervals']=[approved('year',start=c['period_start'],end=c['reporting_period'],issued='100',treasury='0')];c.update(opening_issued='100',closing_issued='100',opening_treasury='0',closing_treasury='0',expected_weighted_shares='100',retrospective_actions=[],retrospective_inventory=[])
        c['numerator']=pol(c,'numerator',profit='120',nci='0',preferred='20',other='0',continuing_profit='120',continuing_nci='0',continuing_preferred='20',continuing_other='0',ordinary_total='100',ordinary_continuing='100',ordinary_discontinued='0',attribution_memo='Statement profit attributable',preference_memo='Qualified cumulative preference amount20',adjustment_memo='No other adjustments',financial_statement_memo='GL/statement/note tie')
        c['potential_shares']=[approved('convertible',method=method(c,'convertible-method','EPS instrument accounting',kind='if_converted',incremental_weighted_shares='10',total_numerator_adjustment='6',continuing_numerator_adjustment='6',terms_memo='Actual supplied conversion terms',tax_memo='Qualified after-tax six',timing_memo='Full period',measurement_memo='Qualified instrument-specific method'))];c['instrument_inventory']=['convertible']
        c['comparatives']=[];c['comparative_inventory']=[]
        c['statement']=dict(basic_total='1',basic_continuing='1',basic_discontinued='0',diluted_total=str(Decimal(106)/110),diluted_continuing=str(Decimal(106)/110),diluted_discontinued='0')
        c['source_inventory']=['year'];c['controls'].update(population_count=1,population_amount='100');dimensions(c,c['share_intervals']+c['potential_shares'])
    elif pkg=='segment-reporting':
        c['segment_method']=method(c,'segments','Segment accounting',in_scope=True,uk_scope='separately_reviewed_obligation',codm_identity='Hypothetical actual executive committee',codm_pack_memo='Actual monthly resource/profit package',aggregation_memo='Two separate components',transition_memo='Actual operative edition',comparative_memo='Unchanged structure',entity_wide_memo='Full external revenue population',significant_expense_memo='Actual ASC280 annual/interim required expenses',annual_interim_adoption_memo='Reviewed actual reporting period and adoption',single_segment_memo='Multiple components',asset_test=True,structure_changed=False,comparatives_reconciled=True,thresholds=method(c,'thresholds','Segment reportability thresholds',revenue='.1',profit='.1',assets='.1',external_coverage='.75',major_customer='.1'))
        c['components']=[approved(id,external_revenue=ext,intersegment_revenue=inter,profit=profit,assets=assets,liabilities=liabilities,business_activity=True,discrete_information=True,regular_codm_review=True,operating=True,business_memo='Evidenced operation',discrete_information_memo='Complete discrete records',regular_review_memo='Actual recurring CODM pack',resource_allocation_memo='Documented allocation process') for id,ext,inter,profit,assets,liabilities in [('A','600','100','180','1000','400'),('B','400','0','40','600','200')]]
        c['groups']=[approved(id,members=[id],label='Segment '+id,qualitative_required=False,reported=True) for id in ('A','B')];c['group_inventory']=['A','B']
        c['reconciliations']=[approved(k,segment_total=total,consolidated=final,statement=final,items=[approved('bridge',amount=adjust,cause_memo='Actual signed intersegment/corporate bridge')],item_inventory=['bridge']) for k,total,adjust,final in [('revenue','1100','-100','1000'),('profit','220','-20','200'),('assets','1600','0','1600'),('liabilities','600','0','600')]];c['reconciliation_inventory']=['revenue','profit','assets','liabilities']
        c['entity_wide']=pol(c,'wide',geographic=[approved('local',external_revenue='1000',noncurrent_assets='800',source_memo='Full actual geography')],geographic_inventory=['local'],products_services=[approved('product',external_revenue='1000',source_memo='Full product source')],products_services_inventory=['product'],customers=[approved('customer',external_revenue='1000',source_memo='Complete hypothetical single customer',major=True,segment_attribution_memo='Both segments actual customer sales')],customers_inventory=['customer'],geographic_asset_memo='Independent noncurrent asset population',statement_noncurrent_assets='800')
        c['source_inventory']=['A','B'];c['controls'].update(population_count=2,population_amount='1100');dimensions(c,c['components'])
    elif pkg=='subsequent-events':
        c['event_method']=method(c,'window','Subsequent-event accounting',cutoff='2027-03-31',window_basis='issuance' if fw=='US_GAAP' else 'authorization',basis_appropriate=True,post_issuance=False,authorization_memo='Actual legal authorizer and date',window_memo='Framework-specific actual window',filer_memo='Actual public entity',basis_memo='Continued appropriate basis',aggregate_materiality_memo='Complete individual and aggregate assessment')
        c['events']=[approved('financing',kind='financing',event_date='2027-01-10',learned_date='2027-01-15',condition_date='2027-01-10',existed_at_reporting_date=False,adjusting=False,going_concern_impact=False,measurement_change='0',material=True,disclosed=True,effect_estimable=True,financial_effect='100',condition_memo='Executed new financing after report',materiality_memo='Qualified material event',disclosure_memo='Approved nature/effect',going_concern_memo='Separately reviewed nil adverse impact',nature_memo='Material new financing')]
        c['feeds']=[approved(id,search_memo='Independent source search through exact cutoff',reviewed_through='2027-03-31',complete=True,event_ids=['financing'] if id=='treasury' else []) for id in ('board','legal','treasury','commercial','tax','asset','post_close','management_forecast')];c['feed_inventory']=[r['id'] for r in c['feeds']]
        c['accounting_updates']=[];c['update_inventory']=[];c['statement_balances']=[approved('Cash',original='100',revised='100',statement='100'),approved('Equity',original='-100',revised='-100',statement='-100')];c['statement_inventory']=['Cash','Equity'];c['source_inventory']=['financing'];c['controls'].update(population_count=1,population_amount='0');dimensions(c,c['events'])
    if pkg in {'earnings-per-share','segment-reporting'}:
        values={k:c['numerator'][k] for k in ('profit','nci','preferred','other','continuing_profit','continuing_nci','continuing_preferred','continuing_other')} if pkg=='earnings-per-share' else dict(revenue='1000',profit='200',assets='1600',liabilities='600',geographic_noncurrent_assets='800')
        bind_statement(c,values)
        if pkg=='segment-reporting':c['segment_method'].update(profit_definition_adjustment='0',profit_definition_memo='Same independently supported net profit definition')
    return c

def bind_statement(c,values):
    lines=[];c['gl']=[]
    for metric,v in values.items():
        credit=metric in {'profit','revenue','continuing_profit','liabilities','nci','continuing_nci'};balance=-Decimal(v) if credit else Decimal(v)
        c['gl'].append(approved(metric,opening=str(balance),closing=str(balance),statement=str(balance)))
        lines.append(approved(metric,metric=metric,account=metric,credit_nature=credit,amount=str(v)))
    dimensions(c,lines);c['gl_inventory']=[r['id'] for r in c['gl']];c['financial_statement_source']=pol(c,'statement-source',mapping_memo='Independent source/GL/statement complete metric mapping',full_period_memo='Exact full reporting period, not ending interim quarter',lines=lines,line_inventory=[r['id'] for r in lines])

def ready(pkg,fw='IFRS',c=None):
    return certified(pkg,fw,c or case(pkg,fw))

def adjusting(fw='IFRS'):
    from cases import provision
    import copy
    c=case('subsequent-events',fw);r=c['events'][0];r.update(id='litigation',kind='litigation',condition_date='2026-12-01',existed_at_reporting_date=True,adjusting=True,measurement_change='10',financial_effect='10',update_id='claim')
    c['source_inventory']=['litigation'];c['controls']['population_amount']='10'
    for f in c['feeds']:f['event_ids']=['litigation'] if f['id']=='legal' else []
    before=certified('provisions-contingencies',fw,provision(fw));after=copy.deepcopy(before)
    after['estimate']['outcomes']=[{'amount':'50','probability':'.5'},{'amount':'60','probability':'.5'}];after['estimate'].update(low='50',high='60',best_estimate='55');after=certified('provisions-contingencies',fw,after)
    original=execute('provisions-contingencies',before);revised=execute('provisions-contingencies',after)
    delta={}
    for sign,result in ((-1,original),(1,revised)):
        for e in result['journal_entry_implications']:
            for l in e:delta[l['account']]=delta.get(l['account'],Decimal(0))+sign*Decimal(l['amount'])*(1 if l['side']=='Dr' else -1)
    account='provision'
    u=approved('claim',measured_account=account,original=approved('original',package='provisions-contingencies',case=before,result=original),revised=approved('revised',package='provisions-contingencies',case=after,result=revised));dimensions(c,[u]);c['accounting_updates']=[u];c['update_inventory']=['claim']
    baseline={'provision expense':str(original['calculations']['provision_bridge']['estimate_change']),'provision':str(-original['calculations']['provision']),'cash':'-20','opening equity':'50'}
    c['statement_balances']=[approved(k,original=v,revised=str(Decimal(v)+delta.get(k,Decimal(0))),statement=str(Decimal(v)+delta.get(k,Decimal(0)))) for k,v in baseline.items()];c['statement_inventory']=list(baseline)
    return c
