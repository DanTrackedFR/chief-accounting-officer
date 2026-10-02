"""New six-skill synthetic inputs; no real entities or approvals."""
from cases import base

def acquisition(fw='IFRS'):
    c=base('business-combinations',fw)
    c.update(acquisition={'date':'2026-01-01','acquirer':'Synthetic parent','business_definition_memo':'Input/process/output business reviewed',
      'control_memo':'Substantive ordinary control','scope':'ordinary_business','business_definition_met':True,'control_obtained':True,
      'tax_review':'Tax specialist supported amounts including nil additional tax','tax_review_complete':True,
      'exceptions_review':'Recognition exceptions reviewed','exceptions_resolved':True,'bargain_reassessment_complete':True},
      assets=[{'id':'cash','account':'acquired cash','amount':'900','recognition_memo':'Complete acquired assets','valuation_evidence':'Synthetic valuation',
      'measurement_basis':'fair_value','recognition_approved':True}],
      liabilities=[{'id':'debt','account':'assumed liabilities','amount':'200','recognition_memo':'Complete assumed liabilities','valuation_evidence':'Synthetic valuation',
      'measurement_basis':'fair_value','recognition_approved':True}],
      consideration={'cash':'800','equity':'0','other':'0','prior_interest':'0','prior_carrying':'0','memo':'Reviewed SPA',
      'contingent':{'class':'none','acquisition_amount':'0','classification_memo':'No earnout','probable_reliable':True}},
      nci={'ownership':'0.8','method':'proportionate' if fw=='UK_GAAP' else 'fair_value','fair_value':'180','memo':'Reviewed qualifying NCI'},
      costs={'direct':'20','other':'0','issuance':'0','memo':'Supported service costs'},events=[],
      subsequent={'goodwill_amortization':'26' if fw=='UK_GAAP' else '0','goodwill_impairment':'0','memo':'Supported goodwill life and impairment review',
      'impairment_review_complete':True,'useful_life':'10','amortization_fraction':'1','amortization_basis':'Supported ten-year useful life'})
    return c

def impairment(fw='IFRS'):
    c=base('asset-impairment',fw)
    c.update(unit={'model':'asc350_goodwill' if fw=='US_GAAP' else 'recoverable_amount','perimeter_memo':'Single independent unit',
      'indicator_memo':'Test indicators reviewed','sequence_memo':'Other asset tests completed before unit','annual_test':True,'indicator':True,
      'carrying_alignment':True,'other_tests_complete':True,'uk_amortization_complete':True},
      assets=[{'id':'gw','account':'goodwill','type':'goodwill','carrying':'1500','floor':'0','no_impairment_ceiling':'1500','valuation_evidence':'PPA'},
      {'id':'plant','account':'plant','type':'finite','carrying':'10500','floor':'0','no_impairment_ceiling':'10500','valuation_evidence':'Asset ledger'}],
      valuation={'cash_flows':[{'year':'1','amount':'10800'}],'discount_rate':'0','terminal_value':'0','fv_less_costs':'11000',
      'fair_value':'11000','undiscounted':'10800','memo':'Forecast and market value inputs supported','inputs_reviewed':True},
      reversal={'requested':False,'amounts':{},'change_memo':'No reversal'})
    return c

def fx(fw='IFRS'):
    c=base('foreign-currency',fw)
    c.update(currency={'functional':'EUR','presentation':'EUR','ledger':'EUR','functional_memo':'Primary price/cost economics reviewed',
      'rate_source':'Synthetic approved spot feed','rate_convention':'functional_per_foreign','functional_review_complete':True,
      'hyperinflation':False,'exchangeability':True,'functional_change':False,'net_investment_items':False},
      items=[{'id':'AR','type':'monetary','side':'asset','account':'receivable','foreign_amount':'100','initial_rate':'1.10',
        'closing_rate':'1.20','settled_foreign':'40','settlement_rate':'1.15','initial_date':'2026-01-01','settlement_date':'2026-06-30',
        'opening_book':'110','opening_route':'initial','opening_rate':'1.10','memo':'Supported customer receivable'}],
      translation={'enabled':True,'operation_id':'Synthetic USD subsidiary','valuation_date':'2026-12-31','functional_currency':'USD','presentation_currency':'EUR','quote':'presentation_per_functional',
      'tb':[{'id':'cash','balance':'120','category':'asset','rate':'0.80','memo':'Closing rate'},
        {'id':'capital','balance':'-100','category':'equity','rate':'0.90','memo':'Historical equity'},
        {'id':'profit','balance':'-20','category':'profit','rate':'0.85','memo':'Supported average'}],
      'opening_net_assets':'100','opening_rate':'0.90','closing_rate':'0.80','profit':'20','profit_rate':'0.85','flows':[],
      'other_oci':'0','other_oci_rate':'0.85','opening_cta':'0','reported_closing_net_assets':'120','ownership':'0.8',
      'memo':'Separate foreign operation synthetic bridge','rates_approximate_dates':True},disposal={'kind':'none','memo':'No disposal'})
    return c

def award(fw='IFRS'):
    c=base('share-based-compensation',fw)
    c.update(award={'classification':'equity','grant_date':'2026-01-01','grant_date_memo':'Approvals and employee understanding documented',
      'valuation_inputs':{'model':'external reviewed option valuation','share_price':'20','exercise_price':'20','volatility':'0.3',
        'risk_free_rate':'0.03','expected_term':'5','dividend_yield':'0','market_condition_treatment':'None'},
      'valuation_review':'Independent supported grant fair value12','valuation_review_complete':True,'conditions_memo':'Service only',
      'conditions':'service','forfeiture_policy':'estimate','classification_memo':'Equity-only employee grant',
      'ordinary_employee_award':True,'group_arrangement':False,'withholding_feature':False,'opening_cumulative':'0','opening_balance_memo':'No prior service cost'},
      tranches=[{'id':'T1','granted':'10000','grant_fair_value':'12','vesting_date':'2028-12-31','service_attribution_memo':'Three annual service periods'}],
      schedule=[{'date':'2026-12-31','opening_booked':'0','memo':'Reviewed one-third service and expected9000vesting',
      'tranches':{'T1':{'expected_vesting':'9000','actual_forfeited':'1000','progress':'0.3333333333333333333333333333',
      'nonmarket_met':True,'market_met':True,'current_fair_value':'15'}}}],event={'kind':'none','date':'2026-12-31','memo':'No event'})
    return c

def reporting(fw='IFRS',start='2026-01-01'):
    c=base('financial-statements',fw,start);year=start[:4];modern=fw in ('IFRS','AASB') and start>='2027-01-01'
    def tb(rows):
        return [{'id':i,'balance':b,'category':cat,'performance_category':'operating','line':i,'source_version':'syntheticTBv1','classification_memo':'Reviewed class and population','cash_account':i=='cash'} for i,b,cat in rows]
    c.update(presentation={'model':('IFRS18' if modern else 'IAS1') if fw=='IFRS' else ('AASB18' if modern else 'AASB101') if fw=='AASB' else 'US_GAAP' if fw=='US_GAAP' else 'FRS102',
      'early_adoption':False,'adoption_memo':'Actual period and framework reviewed','business_activity':'ordinary','entity_overlay':'Reviewed for-profit tier/filer scope',
      'classification_review_complete':True,'offsetting_review_complete':True,'transition_comparatives_reconciled':True,'mdp_review_complete':True,'category_map_reviewed':True,
      'statutory_format_version':'Applicable company-law formats','small_entity_scope':False,'periodic_review_adopted':True,'adapted_formats_2027_review_complete':True,
      'mdps':[],'mdp_population_memo':'No management-defined public measure in synthetic case'},
      current_tb=tb([('cash','290','asset'),('other assets','210','asset'),('debt','-200','liability'),('opening equity','-100','equity'),('sales','-400','revenue'),('cost','200','expense')]),
      comparative_tb=tb([('cash','100','asset'),('opening equity','-100','equity')]),
      comparative={'period_end':str(int(year)-1)+'-12-31','issued_version':'Signed prior v1','restated_version':'No restatement','adjustments_memo':'No prior error; source bridge reviewed','opening_equity_tie':True,'tax_effects_reviewed':True},
      equity_bridge=[{'id':'owners','opening':'100','profit':'200','oci':'0','owner_transactions':'0','retrospective_adjustments':'0','other':'0','closing':'300','memo':'Owner equity source'}],
      cash_flow={'start_subtotal':'operating_profit' if modern else 'profit','start_amount':'200','subtotal_reconciliation':'0','subtotal_memo':'Operating profit equals net profit in synthetic case',
      'adjustments':[{'id':'noncash','amount':'40','source':'Reviewed movement ledger','noncash_acquisition_fx_excluded':True,'memo':'Noncash adjustment'}],
      'investing':'-90','financing':'50','fx':'-10','opening':'100','closing':'290','balance_sheet_bridge':'0','opening_balance_sheet_bridge':'0','population_memo':'All cash accounts and classifications reviewed',
      'classifications':[{'id':'op','date':year+'-12-31','kind':'net_customer_supplier','class':'operating','amount':'240','memo':'Complete operating flows'},
        {'id':'inv','date':year+'-12-31','kind':'asset_purchase','class':'investing','amount':'-90','memo':'Investing flows'},
        {'id':'fin','date':year+'-12-31','kind':'borrowing','class':'financing','amount':'50','memo':'Financing flows'}]},
      notes=[{'id':'cash-note','target':'cash','amount':'290','population_evidence':'Bank evidence','memo':'All accounts covered'}],
      checklist=[{'id':g,'group':g,'requirement':'Reviewed '+g+' population','effective_version':'Applicable operative edition','decision':'satisfied',
       'memo':'Scope and disclosure population challenge','evidence':'Complete requirement register','owner':'Synthetic disclosure owner'} for g in ('balance_sheet','income','comprehensive_income','cash_flow','equity','notes')],
      coverage={'requirement_population_reviewed':True,'checklist_version':'Synthetic applicable checklist','narrative_reviewed':True,
        'complete_sets':['balance_sheet','income','comprehensive_income','cash_flow','equity','notes'],
        'special_topics':{t:{'decision':'reviewed','memo':'Specialist scope reviewed for synthetic example','evidence':'External signed workpaper'} for t in ('going_concern','subsequent_events','related_parties','segments','eps','tax','leases','acquisitions','financial_instruments','contingencies','share_awards')}})
    return c

FACTORIES={'business-combinations':acquisition,'asset-impairment':impairment,'foreign-currency':fx,'share-based-compensation':award,'financial-statements':reporting}

def certify(package,c):
    from production import canonical_knowledge,PACKAGES,case_fingerprint
    claims,docs=canonical_knowledge(PACKAGES[package][1],c['framework'])
    c['knowledge_review']={'reviewer':'synthetic accounting reviewer','claim_ids':[x['claim_id'] for x in claims],'documents':docs,
      'applied_claim_ids':[x['claim_id'] for x in claims],'selection_memo':'Synthetic framework-specific selection; all claims in synthetic complete package population reviewed for scope',
      'public_caveats':['Precise authority is not asserted where the governed register has no verified paragraph; apply actual effective edition and entity scope.']}
    c['reviewer_signoff']={'reviewer':'synthetic independent reviewer','approved':True,'case_fingerprint':case_fingerprint(c)}
    return c
