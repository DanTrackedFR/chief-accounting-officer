"""Entirely synthetic four-framework cases; approvals never authenticate a person."""
from decimal import Decimal
from cases import base
from operational_cases import approved,handoffs
from reporting_cases import pol,certified

PACKAGES=['income-taxes','employee-benefits-payroll','debt-financing','intangible-assets','fair-value-measurement']
FRAMEWORKS=['IFRS','US_GAAP','UK_GAAP','AASB']

def gl(c,balances,opening=None):
    c['gl']=[approved(k,opening=str((opening or {}).get(k,0)),closing=str(v),statement=str(v)) for k,v in balances.items()]
    c['gl_inventory']=list(balances)

def case(package,fw='IFRS'):
    c=base(package,fw);c['execution_date']='2027-02-01';c['imports']=[];c['handoffs']={}
    c['controls']=dict(source_version='v1',as_of=c['reporting_period'],population_count=1,population_amount='0',owner='synthetic source owner',reviewer='synthetic completeness reviewer',complete=True,policy_version='v1',cutoff_memo='Synthetic independently frozen population')
    c['disclosure_review']=approved('disclosure',checklist_version='v1',period_entity_memo='Actual operative framework/tier checklist',complete=True)
    c['accounting_policy']=pol(c,'policy',development_election='capitalize',time_basis='actual_actual')
    if package=='income-taxes':
        areas=['current_tax','tax_bases','differences','losses_credits','recoverability','uncertainty','rates','acquisitions','share_based','outside_basis','allocation','etr','disclosures','transition','offsetting','scope']
        c['tax_area_reviews']=[pol(c,k,scope_memo='Synthetic independently evaluated scope',exception_memo='No unsupported exception',disposition='applicable') for k in areas]
        ds=[]
        for id,kind,source,carrying,taxbase,difference,recovery,closing in [('equipment','taxable','asset','1000','700','300','0','75'),('accrual','deductible','liability','200','0','200','50','50')]:
            ds.append(approved(id,kind=kind,source=source,carrying=carrying,tax_base=taxbase,difference=difference,reversal_rate='.25',rate_status='enacted',recognition_exception=False,recoverable_tax_amount=recovery,opening_gross='0',opening_allowance='0',allocation='profit',expected_gross=closing,expected_allowance='0',basis_evidence='Supplied legal tax base or UK timing-difference evidence',reversal_memo='Verified reversal type/rate',recovery_memo='Supported jurisdictional forecast and expiry review',exception_memo='Independent exception review'))
        r=approved('jurisdiction',difference_model='timing_difference_plus' if fw=='UK_GAAP' else 'temporary_difference',rate_status='enacted',current_rate='.25',pretax_profit='1000',permanent_adjustment='0',taxable_adjustment='0',taxable_income='1000',credits_used='0',prior_trueup='0',expected_current='250',opening_current='0',tax_paid='0',closing_current='250',differences=ds,difference_inventory=['equipment','accrual'],uncertain_position=approved('utp',framework=fw,opening='0',closing='0',settled='0',recognition_memo='Reviewed nil exposure',measurement_memo='Qualified framework method, not IFRIC23/ASC740 equivalence',framework_memo='Actual operative framework',interest_penalty_memo='Nil supported'),etr_adjustments=[approved('deferred',amount='25',cause_memo='Current period net deferred charge')],etr_inventory=['deferred'],offset_permitted=False,closing_dta='50',closing_dtl='75',closing_allowance='0',tax_law_memo='Supplied enacted tax law, not model facts',return_to_provision_memo='Verified current tax population',rate_evidence='Supplied hypothetical 25 percent, not jurisdiction law',filing_scope_memo='Actual taxpayer/jurisdiction',uncertainty_memo='Reviewed UTP census',allocation_memo='P&L ordinary tax only')
        c.update(jurisdictions=[r],source_inventory=['jurisdiction'],statement_tax_expense='275',statement_pretax='1000');c['controls']['population_amount']='1000'
        gl(c,{'Current tax expense':'250','Current tax payable':'-250','Deferred tax asset':'50','Deferred tax liability':'-75','Deferred tax expense':'25'})
    elif package=='employee-benefits-payroll':
        r=approved('salary',kind='salary',earned_obligation=True,short_term=True,capitalized=False,units='50',rate='200',employer_rate='.08',opening='0',payment='5000',withholding='1000',expected_charge='10800',gl_closing='5800',entitlement_memo='Fifty earned employee service days',classification_memo='Ordinary short-term liability, separate from DB',cutoff_memo='Actual unpaid days excluded from later duplicate payroll',settlement_memo='Approved gross payment/deductions')
        c.update(benefits=[r],source_inventory=['salary'],cash_total='4000',register_expense='10800',register_closing='5800',register_withholding='1000');c['controls']['population_amount']='10800'
        gl(c,{'Employee benefit expense':'10800','Employee benefit payable':'-5800','Cash':'-4000','Employee withholding payable':'-1000'})
    elif package=='debt-financing':
        p=approved('annual',start=c['period_start'],end=c['reporting_period'],effective_period_rate='.08',cash_interest='50',principal_payment='0',expected_interest='78.40',expected_closing='1008.40')
        r=approved('loan',measurement='amortized_cost',complex_features=False,modified=False,opening_carrying='0',opening_principal='0',draws='1000',eligible_cost='20',service_cost='0',directly_attributable=True,schedule=[p],schedule_inventory=['annual'],lender_principal='1000',gl_closing='1008.40',rights_at_reporting_date=True,current_carrying='0',noncurrent_carrying='1008.40',maturities=[approved('maturity',date='2028-12-31',principal='1000')],maturity_inventory=['maturity'],terms_memo='Executed synthetic term-loan',fee_memo='Verified eligible lender issue costs',yield_memo='Supplied contract-supported periodic yield',classification_memo='Independent actual framework rights review',covenant_memo='All testing dates/rights reviewed')
        r['maturities'][0]['carrying']='1008.40'
        c.update(debt=[r],source_inventory=['loan']);c['controls']['population_amount']='1000'
        gl(c,{'Cash':'930','Interest expense':'78.40','Debt carrying liability':'-1008.40'})
    elif package=='intangible-assets':
        r=approved('licence',origin='purchased',life='finite',rights_memo='Verified controlled identifiable licence',recognition_memo='Separate purchase gate',life_memo='Supported six-year life',annual_review='Annual method/life/residual review',impairment_memo='No indicators independently reviewed',recognition_supported=True,model='cost',costs=[approved('purchase',date=c['period_start'],amount='600000',kind='purchase',capitalize=True)],cost_inventory=['purchase'],available_date=c['period_start'],opening_cost='0',opening_accumulated='0',residual='0',remaining_years='6',period_fraction='1',life_reliably_estimated=True,expected_amortization='100000',disposed=False,proceeds='0',gl_cost='600000',gl_accumulated='100000')
        c.update(assets=[r],source_inventory=['licence']);c['controls']['population_amount']='600000'
        gl(c,{'Intangible asset':'600000','Cash':'-600000','Amortization expense':'100000','Accumulated amortization':'-100000'})
    elif package=='fair-value-measurement':
        r=approved('listed',basis_memo='Underlying standard requires market fair value',unit_memo='Ten identical ordinary shares',market_memo='Accessible principal active market',market_participant_memo='Unadjusted market-participant exit quote',disclosure_memo='Actual hierarchy/recurring requirements',valuation_memo='Independent quote validation',measurement_date=c['reporting_period'],required_or_permitted=True,accessible_market=True,recurrence='recurring',method='quoted',inputs=[approved('quote',level='1',significant=True)],input_inventory=['quote'],transport='0',transaction_cost='1',identical_active_unadjusted=True,quantity='10',quote='12',expected_level=1,prior_level=1,expected_value='120',opening_value='100',purchases='0',sales_at_carrying='0',fx='0',remeasurement='20',underlying_handoff='instrument',asset=True,account='Fair value asset',gl_value='120')
        c.update(measurements=[r],source_inventory=['listed']);c['controls']['population_amount']='120'
        c['handoffs']=handoffs(c,{'instrument':'Underlying fair-value accounting'});c['handoffs']['instrument'].update(measurement_value='120',opening_account='100',closing_account='120',journals=[[dict(side='Dr',account='Fair value asset',amount='20'),dict(side='Cr',account='Fair value gain',amount='20')]])
        from cases import ecl
        from additional_cases import certify
        from production import execute
        source=ecl(fw);source['instrument'].update(kind='equity_asset',measurement='FVTPL',impairment_model='none')
        source['measurement_schedule'].update(opening_gross='100',fair_value='120',additions='0',eir='0',cash_flows='0',writeoffs='0',fx='0')
        source=certified('financial-instruments-ecl',fw,case=source);result=execute('financial-instruments-ecl',source)
        c['handoffs']['instrument'].update(package='financial-instruments-ecl',case=source,result=result)
        c['handoffs']['instrument']['journals']=[[],[dict(side='Dr',account='Fair value asset',amount='20'),dict(side='Cr',account='Fair value gain',amount='20')]]
        gl(c,{'Fair value asset':'120','Fair value gain':'-20'},{'Fair value asset':'100'})
    key={'income-taxes':'jurisdictions','employee-benefits-payroll':'benefits','debt-financing':'debt','intangible-assets':'assets','fair-value-measurement':'measurements'}.get(package,'unmapped')
    for r in c.get(key,[]):r.update(source_entity=c['entity'],source_framework=c['framework'],source_period=[c['period_start'],c['reporting_period']])
    return c

def ready(package,fw='IFRS',c=None):
    return certified(package,fw,case=c or case(package,fw))
