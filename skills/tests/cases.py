"""Synthetic examples; never company facts. Fixtures are reviewer inputs."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from production import canonical_knowledge,case_fingerprint

def base(package,framework='IFRS',start='2026-01-01'):
    c={'case_id':'synthetic-'+package,'framework':framework,'period_start':start,'reporting_period':start[:4]+'-12-31',
       'entity':'Synthetic Group','jurisdiction':'NL','entity_type':'for_profit','policy_elections':{},'evidence':['synthetic evidence set'],
       'judgment_memo':'Reviewed synthetic alternative routes and assumptions','assumptions':['Synthetic amounts and assumptions for regression only'],
       'preparer':'synthetic preparer','specialist_items':[]}
    if framework=='UK_GAAP':c.update(uk_standard='FRS_102',uk_standard_edition='September2024');c['policy_elections'].update(section23_model='legacy' if start<'2026-01-01' else 'revised_2026',financial_instruments='sections11_12')
    if framework=='US_GAAP':c['us_entity_type']='public'
    if framework=='AASB':c.update(aasb_compilation='2026 effective compilation',reporting_tier=1)
    c['applicability_review']={'reviewer':'synthetic accounting reviewer','standard_versions':['selected effective edition'],
      'effective_period':[c['period_start'],c['reporting_period']],'entity_scope':c['entity_type'],'exceptions':[]}
    return c

def finalize(package,c):
    from production import PACKAGES
    claims,docs=canonical_knowledge(PACKAGES[package][1],c['framework'])
    c['knowledge_review']={'reviewer':'synthetic accounting reviewer','claim_ids':[x['claim_id'] for x in claims],'documents':docs}
    c['reviewer_signoff']={'reviewer':'synthetic independent reviewer','approved':True,'case_fingerprint':case_fingerprint(c)}
    return c

def revenue(fw='IFRS',start='2026-01-01'):
    c=base('revenue-recognition',fw,start)
    c.update(contract={k:True for k in ['customer_in_scope','approved_committed','rights_identified','payment_terms_identified','commercial_substance','collectibility_met']},
      price_components={'fixed':'1000','noncash':'0','customer_payments':'0','financing_adjustment':'0','variable':[]},
      obligations=[{'id':'delivery','ssp':'600','distinct_memo':'Distinct delivered product','ssp_evidence':'Price list','role':'principal','role_memo':'Controls product',
       'timing':'point_in_time','timing_evidence':'Signed delivery','control_transferred':True,'legacy_route':'goods','risks_rewards_transferred':True},
       {'id':'service','ssp':'400','distinct_memo':'Independent stand-ready service','ssp_evidence':'Price list','role':'principal','role_memo':'Controls service',
        'timing':'over_time','timing_evidence':'Certified six of twelve months','simultaneous_receipt':True,'customer_controls_asset':False,
        'no_alternative_use':False,'right_to_payment_with_margin':False,'progress_reliable':True,'progress':'0.5','legacy_route':'service','reliable_completion':True}],
      balance_bridge={'opening_revenue':'300','opening_contract_net':'-200','opening_receivable':'200','billings':'400','cash_received':'300','opening_cost_asset':'50'},
      contract_costs=[{'amount':'100','capitalization_memo':'Incremental recoverable commission','recoverable':True,'qualifying':True,'amortization':'25','impairment':'5'}])
    c['contract'].update(combination_memo='Single contract',scope_memo='Customer product/service arrangement')
    return finalize('revenue-recognition',c)

def ecl(fw='IFRS'):
    c=base('financial-instruments-ecl',fw)
    model='CECL' if fw=='US_GAAP' else 'incurred_loss' if fw=='UK_GAAP' else 'general'
    c.update(instrument={'kind':'debt_asset','classification_memo':'Hold to collect SPPI debt','measurement':'amortized_cost','impairment_model':model,
         'business_model':'hold_collect','sppi':True,'basic_instrument_assessment':'Basic fixed rate debt'},
      credit={'method':'pd_lgd','assumptions_memo':'Forward looking marginal PD/LGD','overlay':'0','overlay_memo':'No overlay',
         'credit_impaired':False,'sicr':True,'origination_risk_evidence':'Origination rating','current_risk_evidence':'Risk deterioration',
         'default_definition':'Default reviewed','horizon':'lifetime_default_events','objective_impairment_evidence':True,
         'scenarios':[{'weight':'0.75','terms':[{'ead':'1000','marginal_pd':'0.10','lgd':'0.5','discount_factor':'1'}]},
                      {'weight':'0.25','terms':[{'ead':'1000','marginal_pd':'0.20','lgd':'0.5','discount_factor':'1'}]}]},
      measurement_schedule={'opening_gross':'1000','eir':'0','cash_flows':'0','additions':'0','writeoffs':'20','fx':'0','fair_value':'980'},
      allowance_bridge={'opening':'100','writeoffs':'20','recoveries':'5','fx':'0'})
    return finalize('financial-instruments-ecl',c)

def provision(fw='IFRS'):
    c=base('provisions-contingencies',fw)
    c.update(obligation={'type':'litigation','basis':'legal','probability':'probable' if fw=='US_GAAP' else 'more_likely_than_not',
      'obligation_memo':'Counsel evidence reviewed','past_event':True,'present_obligation':True,'estimable':True},
      estimate={'basis':'asc450_range' if fw=='US_GAAP' else 'expected_value','outcomes':[{'amount':'40','probability':'0.5'},{'amount':'50','probability':'0.5'}],
       'low':'40','high':'50','best_estimate':'45','discount_rate':'0','years':'1','risk_memo':'No discount materiality adjustment','estimate_memo':'Reviewed outcomes'},
      movements={'opening':'50','settlements':'20','unwind':'0','fx':'0','other':'0','movement_evidence':'Cash claims settled'},
      reimbursement={'claimed':'0','recognition_threshold_met':False,'reimbursement_memo':'No reimbursement','opening_asset':'0','cash_received':'0'})
    return finalize('provisions-contingencies',c)

def consolidation(fw='IFRS'):
    c=base('consolidation',fw)
    ctrl={'model':'power_returns_link','substantive_power':True,'variable_returns':True,'power_returns_link':True,'control_memo':'Substantive voting rights control','excluded':False}
    if fw=='US_GAAP':ctrl.update(model='voting',vie_scope_memo='Not VIE',controlling_financial_interest=True,substantive_participating_rights_preclude=False)
    if fw=='UK_GAAP':ctrl.update(model='section9',power_to_govern_policies=True)
    c.update(entities=[{'id':'P','parent':True,'balances':{'cash':'300','investment':'80','equity':'-380'},'control':ctrl,'translation':None,'policy_alignment':True,'date_alignment':True},
         {'id':'S','parent':False,'balances':{'cash':'100','sub equity':'-100'},'control':ctrl,'translation':None,'policy_alignment':True,'date_alignment':True}],
      intercompany=[],investments=[{'subsidiary':'S','parent_entity':'P','investment_account':'investment','investment':'80','acquisition_equity':{'sub equity':'100'},
        'fair_value_adjustments':{},'goodwill':'0','nci_at_acquisition':'20','acquisition_memo':'80% acquisition of net assets100'}],
      profit_eliminations=[],nci=[{'subsidiary':'S','ownership':'0.8','opening':'20','adjusted_profit':'0','adjusted_oci':'0','dividends':'0','other':'0','allocation_memo':'80/20 rights'}],
      ownership_changes=[],nci_attribution_account='equity',statement_mapping={'cash':'assets','investment':'assets','equity':'equity','sub equity':'equity','goodwill':'assets','noncontrolling interest':'equity'},
      cash_flow_bridge={'opening_cash':'400','operating':'0','investing':'0','financing':'0','fx':'0','closing_cash':'400','cash_accounts':['cash'],'memo':'Cash flow population tie'},
      disclosure_tieout='Group TB and NCI note bridge')
    return finalize('consolidation',c)
