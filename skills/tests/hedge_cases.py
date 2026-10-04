"""Synthetic evidence and journal fixtures; no approvals represent real people."""
import copy,json
from pathlib import Path
from cases import base
from production import canonical_knowledge,case_fingerprint,PACKAGES
from core_accounting import dec
PACKAGE='derivatives-hedge-accounting'

def workflow():
    from production import load_workflow
    return load_workflow(PACKAGE)

def sources(c):
    w=workflow();c['documents']=[]
    c['population_review']['id']='population';c['disclosure_review']['id']='disclosures'
    records=c['contracts']+c['valuations']+c['owner_links']+[c['population_review'],c['disclosure_review']]+c['gl']
    for r in c['relationships']:
        records.append(r['risk_measurement']);records.append(r)
    for r in records:
        r['document_id']='doc-'+r['id']
    for r in records:
        content=copy.deepcopy({k:v for k,v in r.items() if k!='document_id'})
        c['documents'].append(dict(id=r['document_id'],reviewer='Synthetic independent source reviewer',source_system='Synthetic frozen source',version='1',entity=c['entity'],framework=c['framework'],currency=c['currency'],as_of=c['reporting_period'],content=content,content_hash=w.digest(content)))
    return c

def case(fw='IFRS',route='standalone',outcome='pending'):
    c=base(PACKAGE,fw);c.update(package=PACKAGE,execution_date='2027-02-01',currency='EUR',requested_action='accounting_workpaper',model={'IFRS':'IFRS9_Chapter6','AASB':'AASB9_Chapter6','US_GAAP':'ASC815_2017_12','UK_GAAP':'FRS102_Section12_2026'}[fw],documents=[],imports=[],owner_links=[],relationships=[])
    if fw=='US_GAAP':c['policy_elections'].update(asu_2025_07_early_adopted=False,asu_2025_09_early_adopted=False)
    contract=dict(id='forward1',kind='forward',underlying='Commodity index',underlying_type='commodity',comparable_investment='1000',notional='1000',payment_provision=True,initial_net_investment='0',small_initial_investment=True,future_settlement=True,net_settlement=True,exception_applies=False,exception_assessed=True,embedded_feature=False,financial_asset_host=False,closely_related=True,separation_required=False,contract_memo='Actual synthetic contractual terms reviewed',scope_memo='Independent scope analysis',embedded_memo='Reviewed none',maturity='2027-12-31')
    val=dict(id='valuation1',instrument_id='forward1',qualified_valuer='Synthetic independent derivative valuation specialist',valuation_method='Independently qualified external curve and market valuation',market_evidence='Synthetic frozen independent market workpaper',credit_adjustment_memo='Independent bilateral credit assessment',measurement_date=c['reporting_period'],opening_date=c['period_start'],currency='EUR',entity=c['entity'],notional='1000',opening='0',change='100',settlement='0',closing='100')
    if route=='standalone':contract.update(underlying='EUR/USD',underlying_type='fx')
    c.update(contracts=[contract],valuations=[val],population_review=dict(reviewer='Synthetic independent completeness reviewer',complete=True,completeness_memo='Independent signed contract register completeness',source_system='Synthetic contract register',contract_ids=['forward1'],notional_total='1000'))
    gl={'Derivative balance forward1':('0','100'),'Derivative P&L forward1':('0','-100')}
    if route=='cash_flow':
        risk=dict(id='risk1',instrument_valuation_id='independent-hypothetical1',qualified_reviewer='Synthetic independent hedged-risk valuation reviewer',method='Separately measured hypothetical instrument for designated risk',market_evidence='Independent hypothetical risk source',assessment_date=c['reporting_period'],item_id='purchase1',risk_id='commodity_price',currency='EUR',quantity='1000',current_change='-90',instrument_cumulative='100',risk_cumulative='-90',opening_instrument_cumulative='0',opening_risk_cumulative='0')
        eff='100' if fw=='US_GAAP' else '90';ineff='0' if fw=='US_GAAP' else '-10'
        r=dict(id='relationship1',instrument_id='forward1',type=route,objective='Documented management commodity purchase price protection',designation_memo='Frozen designation at qualification',instrument_eligibility_memo='Eligible whole forward',item_eligibility_memo='Highly probable commodity purchase',risk_component_memo='Whole supported commodity risk',effectiveness_memo='Documented independent assessment',risk_id='commodity_price',hedged_item_id='purchase1',designation_date='2026-01-01',documentation_date='2026-01-01',inception_date='2026-01-01',advanced_route='none',excluded_components='none',instrument_eligible=True,item_eligible=True,risk_eligible=True,objective_unchanged=True,economic_relationship=True,credit_dominates=False,highly_effective=True,external_group_exposure=True,assessment_date=c['reporting_period'],effectiveness_method={'IFRS':'economic_relationship','AASB':'economic_relationship','US_GAAP':'documented_high_effectiveness','UK_GAAP':'economic_relationship'}[fw],ratio='1',actual_instrument_quantity='1000',actual_item_quantity='1000',status='active',risk_measurement=risk,item_type='forecast_purchase',opening_reserve='0',reserve_source_opening='0',opening_effective='0',earnings_release='0',basis_release='0',forecast_memo='Actual approved purchase plan independent probability and volumes',forecast_date='2027-03-31',forecast_probability='probable' if fw=='US_GAAP' else 'highly_probable',forecast_quantity='1000',designated_start='2026-01-01',designated_end='2027-12-31',forecast_outcome=outcome)
        gl={'Derivative balance forward1':('0','100'),'Hedge P&L relationship1':('0',ineff),'Hedge reserve relationship1':('0','-'+eff)}
        if outcome=='no_longer_expected':
            r.update(status='discontinued',discontinuation_date=c['reporting_period'],discontinuation_reason='forecast cancelled',earnings_release=eff)
            gl['Hedge reserve relationship1']=('0','0');gl['Hedge P&L relationship1']=('0','-100')
        elif outcome=='occurred':
            r.update(forecast_date=c['reporting_period'],transaction_date=c['reporting_period'])
            gl['Hedge reserve relationship1']=('0','0')
            if fw=='US_GAAP':
                r.update(earnings_release=eff,earnings_date=c['reporting_period'],earnings_period_memo='Actual purchased inventory consumed in earnings this period');gl['Hedge P&L relationship1']=('0','-100')
            else:
                r.update(basis_release=eff,acquisition_id='receipt1',sku='SKU1',acquired_quantity='1000');gl['Nonfinancial asset basis adjustment']=('0','-'+eff)
        if fw=='UK_GAAP':r.update(instrument_external=True,instrument_fvtpl=True,written_option=False,documented_ineffectiveness_causes='Current native documented commodity mismatch and credit causes')
        c['relationships']=[r]
    c['gl']=[dict(id=k,opening=op,closing=cl,statement=cl) for k,(op,cl) in gl.items()]
    c['disclosure_review']=dict(reviewer='Synthetic independent disclosure reviewer',framework_checklist=fw+' actual operative disclosure requirements',strategy_memo='Documented objective disclosures',timing_profile_memo='Actual notional maturity/settlement disclosures',framework=fw,complete=True,contract_ids=['forward1'],relationship_ids=[r['id'] for r in c['relationships']])
    return sources(c)

def ready(c=None):
    c=copy.deepcopy(c or case());claims,docs=canonical_knowledge(PACKAGES[PACKAGE][1],c['framework'],package=PACKAGE)
    c['knowledge_review']=dict(reviewer='Synthetic independent knowledge reviewer',claim_ids=[r['claim_id'] for r in claims],documents=docs,applied_claim_ids=[r['claim_id'] for r in claims],selection_memo='Synthetic reviewed decision-specific scope and hedge method claims',public_caveats=['Qualified current evidence and the operative accounting model are required; source confidence remains bounded.'])
    c['reviewer_signoff']=dict(reviewer='Synthetic independent implementation reviewer',approved=True,case_fingerprint=case_fingerprint(c));return c

def fair_value_case(fw='IFRS'):
    c=case(fw,'cash_flow');r=c['relationships'][0];r.update(type='fair_value',item_type='firm_commitment',opening_basis='0',basis_amortization='0')
    c['gl']=[dict(id=k,opening='0',closing=v,statement=v) for k,v in {'Derivative balance forward1':'100','Hedge P&L relationship1':'-10','Hedged item basis adjustment relationship1':'-90'}.items()]
    return sources(c)

def net_investment_case(fw='IFRS',disposed=False):
    from cases import consolidation
    from additional_cases import fx,certify
    from production import execute
    co=consolidation(fw);co.pop('reviewer_signoff',None)
    co['entities'][0]['balances']={'cash':'300','investment':'72','equity':'-372'}
    co['entities'][1].update(id='ForeignS',balances={'cash':'100','sub equity':'-100'},translation=dict(account_rates={'cash':'0.8','sub equity':'0.9'},rate_evidence='Qualified actual operation source rates',cta_account='translation reserve'))
    co['investments'][0].update(subsidiary='ForeignS',investment='72',acquisition_equity={'sub equity':'90'},nci_at_acquisition='18')
    co['nci'][0].update(subsidiary='ForeignS',opening='18');co['statement_mapping']['translation reserve']='equity'
    co['cash_flow_bridge'].update(opening_cash='380',closing_cash='380');co['equity_bridge'].update(opening='380',closing='380')
    co['cta_bridge'].update(opening='0',translation='10',closing='10',cta_accounts=['translation reserve'])
    co=certify('consolidation',co);cr=execute('consolidation',co)
    fc=fx(fw);fc['translation'].update(operation_id='ForeignS',tb=[dict(id='cash',balance='100',category='asset',rate='0.8',memo='Current closing'),dict(id='sub equity',balance='-100',category='equity',rate='0.9',memo='Historical')],opening_net_assets='100',opening_rate='0.9',closing_rate='0.8',profit='0',profit_rate='0.85',reported_closing_net_assets='100')
    fc=certify('foreign-currency',fc);fr=execute('foreign-currency',fc)
    c=case(fw,'cash_flow');r=c['relationships'][0];r.update(risk_id='FX',type='net_investment',item_type='net_investment',group_perspective=True,consolidation_import='cons1',foreign_operation_id='ForeignS',net_investment_eligibility_memo='Actual parent owned net assets in foreign operation qualifies; FX/group scopes reviewed',translation_owner='translation-link',net_investment='64',translation_change='-10',actual_instrument_quantity='64',actual_item_quantity='64',disposed=disposed)
    c['contracts'][0]['notional']='64';c['valuations'][0]['notional']='64';c['population_review']['notional_total']='64';r['risk_measurement'].update(risk_id='FX',quantity='64',current_change='-10',risk_cumulative='-10')
    if disposed and fw!='UK_GAAP':r['earnings_release']='10'
    c['imports']=[dict(id='cons1',package='consolidation',case=co,result=cr),dict(id='fx1',package='foreign-currency',case=fc,result=fr)]
    c['owner_links']=[dict(id='translation-link',owner_import='fx1',result_path=['translation','cta_movement'],amount='-10')]
    close='0' if disposed and fw!='UK_GAAP' else '-10';pnl='-100' if disposed and fw!='UK_GAAP' else '-90'
    c['gl']=[dict(id=k,opening='0',closing=v,statement=v) for k,v in {'Derivative balance forward1':'100','Hedge P&L relationship1':pnl,'Hedge reserve relationship1':close}.items()]
    return sources(c)

def debt_case(fw='IFRS',route='fair_value'):
    from financing_cases import ready as debt_ready
    from production import execute
    d=debt_ready('debt-financing',fw);d['debt'][0].update(contractual_rate_type='fixed' if route=='fair_value' else 'variable',contractual_rate_terms_memo='Independently reviewed actual debt terms',contractual_benchmark='Documented synthetic benchmark')
    from additional_cases import certify
    d=certify('debt-financing',d);rr=execute('debt-financing',d)
    c=fair_value_case(fw) if route=='fair_value' else case(fw,'cash_flow')
    r=c['relationships'][0];r.update(item_type='debt' if route=='fair_value' else 'variable_debt',hedged_item_id='loan',debt_owner='debt-link',underlying_carrying='1008.40',debt_terms_memo='Current completed debt contractual schedule',debt_notional='1000',debt_maturity='2028-12-31',debt_result_index=0,underlying_rate_type='fixed' if route=='fair_value' else 'variable')
    r['risk_measurement']['item_id']='loan';c['contracts'][0]['maturity']='2028-12-31'
    c['imports']=[dict(id='debt1',package='debt-financing',case=d,result=rr)]
    c['owner_links']=[dict(id='debt-link',owner_import='debt1',result_path=['debt',0,'closing'],amount='1008.40')]
    return sources(c)

def special_case(name,fw='IFRS'):
    if name=='late-documentation':
        c=case(fw,'cash_flow');c['relationships'][0]['documentation_date']='2026-02-01';c['gl']=case(fw)['gl']
    elif name=='swap-liability-settlement':
        c=case(fw);c['contracts'][0].update(kind='swap',underlying='Documented interest benchmark',underlying_type='rate');c['valuations'][0].update(opening='-80',change='-30',settlement='-40',closing='-70')
        c['gl']=[dict(id=k,opening=o,closing=v,statement=v) for k,o,v in [('Derivative balance forward1','-80','-70'),('Derivative P&L forward1','0','30'),('Cash','0','-40')]]
    elif name=='rebalancing':
        c=case(fw,'cash_flow');c['relationships'][0].update(status='rebalanced',rebalancing_memo='Documented objective unchanged; independent new actual management quantities',rebalancing_date=c['reporting_period'],historical_effective='0',new_ratio='2',new_instrument_quantity='2000',new_item_quantity='1000')
    elif name=='discontinue-expected':
        c=case(fw,'cash_flow');c['relationships'][0].update(status='discontinued',discontinuation_date=c['reporting_period'],discontinuation_reason='probability_lost',forecast_probability='expected',probability_before_cessation='probable' if fw=='US_GAAP' else 'highly_probable',measurement_through_qualification_date=c['reporting_period'])
    elif name=='cumulative-reversal':
        c=case(fw,'cash_flow');r=c['relationships'][0];r.update(opening_reserve='160',reserve_source_opening='160',opening_effective='160')
        c['valuations'][0].update(opening='180',change='-27',settlement='0',closing='153');r['risk_measurement'].update(opening_instrument_cumulative='180',opening_risk_cumulative='-160',instrument_cumulative='153',risk_cumulative='-110',current_change='50')
        c['gl']=[dict(id=k,opening=o,closing=v,statement=v) for k,o,v in [('Derivative balance forward1','180','153'),('Hedge P&L relationship1','0','-23'),('Hedge reserve relationship1','-160','-110')]]
    elif name=='forecast-sale':
        from cases import revenue
        from production import execute
        rc=revenue(fw);rc.update(contract_id='sale1',currency='EUR',hedged_contract_quantity='1000')
        from additional_cases import certify
        rc['reviewer_signoff']['case_fingerprint']=case_fingerprint(rc);rr=execute('revenue-recognition',rc);c=case(fw,'cash_flow','occurred');r=c['relationships'][0];r['hedged_item_id']='sale1';r['risk_measurement']['item_id']='sale1'
        r.update(item_type='forecast_sale',basis_release='0',earnings_release='100' if fw=='US_GAAP' else '90',earnings_period_memo='Actual current Revenue output includes hedged transaction earnings',earnings_date=c['reporting_period'],revenue_owner='revenue-link',underlying_period_revenue='500')
        c['imports']=[dict(id='revenue1',package='revenue-recognition',case=rc,result=rr)];c['owner_links']=[dict(id='revenue-link',owner_import='revenue1',result_path=['period_revenue'],amount='500')]
        c['gl']=[dict(id=k,opening='0',closing=v,statement=v) for k,v in {'Derivative balance forward1':'100','Hedge P&L relationship1':'-100','Hedge reserve relationship1':'0'}.items()]
    else:raise ValueError(name)
    return sources(c)
