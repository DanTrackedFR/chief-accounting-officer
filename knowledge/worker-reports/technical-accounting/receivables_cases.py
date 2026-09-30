"""Hand-authored adverse cases for 006–010; serialization is mechanical."""
import json
from pathlib import Path
from completion_tools import TOPICS

def post(event, *rows):
    return {'event': event, 'lines': [{'side': s, 'account': a, 'amount': v} for s,a,v in rows]}

def make(n, name, frameworks, keys, facts, calculations, expected, route, choice,
         journals, balances, evidence, control, data, notes, opening=None):
    return {'id': name, 'frameworks': frameworks,
            'claim_ids': [f'TOPIC-03-{n:03d}-{k}' for k in keys],
            'facts': facts, 'calculations': calculations, 'expected_calculations': expected,
            'route': route, 'expected_route': choice, 'journals': journals,
            'opening_balances': opening or {}, 'expected_balances': balances,
            'workpaper_outcome': evidence, 'control_outcome': control,
            'data_outcome': data, 'presentation_disclosure_outcome': notes}

ALL=['IFRS','US_GAAP','UK_GAAP','AASB']
cases={n:[] for n in range(6,11)}
cases[6].append(make(6,'CC-asset-amortization-impairment',['IFRS','US_GAAP','UK_GAAP','AASB'],
 ['IFRS-R002','US-R003','UK-R005','AASB-R002','IFRS-R013','US-R015','UK-R017','AASB-R013'],
 dict(commission=90,years=3,consideration=200,future_cost=155,incremental=True,recoverable=True,uk_capitalize=True),
 dict(amortization='commission/years',before_loss='commission-amortization',cap='consideration-future_cost',loss='max(0,before_loss-cap)',closing='before_loss-loss'),
 dict(amortization=30,before_loss=60,cap=45,loss=15,closing=45),
 'incremental and recoverable and uk_capitalize',True,
 [post('successful contract commission',('Dr','cost_asset','commission'),('Cr','commission_payable','commission')),
  post('year-one amortization',('Dr','amortization','amortization'),('Cr','cost_asset','amortization')),
  post('recoverability shortfall',('Dr','impairment','loss'),('Cr','cost_asset','loss'))],
 dict(cost_asset=45,commission_payable=-90,amortization=30,impairment=15),
 'CC-006 ties success-only90 to plan/payroll and supports three-year renewal benefit; approved remaining consideration200 and direct cost155 support cap45.',
 'Asset rollforward90-30-15=45 rejects salary capitalization and a revenue-offset impairment plug; UK capitalization policy must be approved.',
 'Cost ID links successful contract, payroll payable90, amortization30 and loss15; policy version gates UK asset route.',
 'Closing cost asset45, amortization30 and impairment15 feed the applicable cost-asset notes; payable remains90 until settlement.'))
for capitalize in [False,True]:
 cases[6].append(make(6,'CC-UK-policy-'+str(capitalize),['UK_GAAP'],['UK-R005','UK-R006'],
  dict(cost=90,capitalize=capitalize),dict(asset='cost if capitalize else 0',expense='cost-asset'),
  dict(asset=90 if capitalize else 0,expense=0 if capitalize else 90),'capitalize',capitalize,
  [post('selected UK acquisition-cost policy',('Dr','cost_asset','asset'),('Dr','commission_expense','expense'),('Cr','payable','cost'))],
  dict(cost_asset=90 if capitalize else 0,commission_expense=0 if capitalize else 90,payable=-90),
  'CC-006 records FRS102 revised adoption and a consistently applied policy; neither choice is selected from desired quarterly profit.',
  'Policy approval rejects contradictory expense90 plus asset90 and produces exactly one90 debit destination.',
  'Entity/period policy selects acquisition-cost classification; commission90 remains linked to the same payable and contract.',
  'Asset90 or current expense90 differs by election; disclose policy and separately assess subsequent asset amortization when capitalized.'))
for us in [False,True]:
 cases[6].append(make(6,'CC-reversal-US-'+str(us),['US_GAAP'] if us else ['IFRS','AASB'],
  ['US-R016'] if us else ['IFRS-R014','AASB-R014'],
  dict(opening_asset=45,new_cap=55,no_loss_cap=60,us=us),
  dict(reversal='0 if us else min(new_cap,no_loss_cap)-opening_asset',closing='opening_asset+reversal'),
  dict(reversal=0 if us else 10,closing=45 if us else 55),'not us',not us,
  [post('supported improvement before further amortization',('Dr','cost_asset','reversal'),('Cr','impairment_reversal','reversal'))],
  dict(cost_asset=45 if us else 55,impairment_reversal=0 if us else -10),
  'CC-006 retains improved remaining recovery55 and no-loss cap60; there has been no intervening amortization in these stated facts.',
  'Framework control rejects a10 US reversal and rejects IFRS/AASB reversal beyond the no-loss carrying amount.',
  'Prior impairment ID and new estimate version remain linked; US reversal flag stays disabled.',
  'IFRS/AASB asset55 and gain10 versus US asset45 and no gain are independently reconciled.',dict(cost_asset=45)))
cases[6].append(make(6,'CC-billing-interface-duplicate-revenue',ALL,['IFRS-R001','US-R001','UK-R001','AASB-R001'],
 dict(usage_count=10,invoiced_usage=9,usage_price=12,milestones=2,milestone_price=40,revenue_already_recorded=True),
 dict(eligible='usage_count*usage_price+milestones*milestone_price',billed='invoiced_usage*usage_price+milestones*milestone_price',missing='eligible-billed',new_revenue='0 if revenue_already_recorded else missing'),
 dict(eligible=200,billed=188,missing=12,new_revenue=0),'revenue_already_recorded',True,
 [post('recover invoice for previously recognized event',('Dr','receivable','missing'),('Cr','contract_asset','missing'))],
 dict(receivable=12,contract_asset=0,revenue=-12),
 'Billing workpaper independently matches10 approved usage events and2 milestones to invoices; the missing12 already exists in revenue/contract asset.',
 'Control detects200-188=12 missing billing and rejects second revenue credit12 during invoice recovery.',
 'Recovered invoice references original performance event and contract-asset ID; replayed event is idempotent.',
 'AR12 replaces conditional asset12 without changing revenue12; billing defect is reported as a control exception.',dict(contract_asset=12,revenue=-12)))

cases[7].append(make(7,'RF-return-estimate-and-settlement',ALL,
 [f'{f}-R005' for f in ['IFRS','US','UK','AASB']],
 dict(cash_sale=1000,cost=600,original_rate=.2,final_rate=.1,initial_recovery_cost=10,final_recovery_cost=10),
 dict(initial_refund='cash_sale*original_rate',revenue='cash_sale-initial_refund',initial_recovery='cost*original_rate-initial_recovery_cost',initial_cogs='cost-initial_recovery',refund='cash_sale*final_rate',release='initial_refund-refund',final_recovery='cost*final_rate-final_recovery_cost',recovery_reduction='initial_recovery-final_recovery'),
 dict(initial_refund=200,revenue=800,initial_recovery=110,initial_cogs=490,refund=100,release=100,final_recovery=50,recovery_reduction=60),'final_rate<original_rate',True,
 [post('sale',('Dr','cash','cash_sale'),('Cr','revenue','revenue'),('Cr','refund_liability','initial_refund')),
  post('derecognize inventory and recognize recovery',('Dr','cost_of_sales','initial_cogs'),('Dr','recovery_asset','initial_recovery'),('Cr','inventory','cost')),
  post('re-estimate refunds',('Dr','refund_liability','release'),('Cr','revenue','release')),
  post('re-estimate recovery costs',('Dr','cost_of_sales','recovery_reduction'),('Cr','recovery_asset','recovery_reduction')),
  post('cash refund',('Dr','refund_liability','refund'),('Cr','cash','refund')),
  post('net recovered inventory',('Dr','inventory','final_recovery'),('Cr','recovery_asset','final_recovery'))],
 dict(cash=900,revenue=-900,refund_liability=0,recovery_asset=0,cost_of_sales=550,inventory=-550),
 'RF-007 retains revised return cohort and recovery cost10; physical net inventory50 and cash100 settle separately after re-estimation.',
 'Refund rollforward200-100-100=0 and recovery110-60-50=0 reject double revenue reversal at settlement.',
 'Return/refund/inventory receipt IDs are separate; estimate versions20%->10% preserve original sale lineage.',
 'Final revenue900 and cost550 reconcile to cash900 and net inventory derecognition550; no residual recovery asset or refund liability.'))
for concession in [False,True]:
 cases[7].append(make(7,'RF-price-versus-credit-'+str(concession),ALL,[f'{f}-R009' for f in ['IFRS','US','UK','AASB']],
  dict(balance=50,concession=concession),{}, {},'concession',concession,
  [post('commercial concession' if concession else 'supported credit loss',('Dr','revenue' if concession else 'credit_loss',50),('Cr','receivable' if concession else 'allowance',50))],
  dict(receivable=0 if concession else 50,revenue=0 if concession else -50,allowance=0 if concession else -50,credit_loss=0 if concession else 50),
  'RF-007 records legal reduction of entitlement or insolvency of an unchanged claim; UK objective evidence is provided for the loss branch.',
  'Reason-code review rejects a50 allowance and a50 price credit for the same surrendered entitlement.',
  'Commercial credit references price version and invoice; impairment references exposure and allowance model.',
  'Commercial concession changes revenue/grossAR; impairment retains gross revenue50 and AR50 with allowance50.',dict(receivable=50,revenue=-50)))

for uk_ifrs9 in [False,True]:
 cases[8].append(make(8,'ECL-UK-policy-'+str(uk_ifrs9),['UK_GAAP'],['UK-R014','UK-R015','UK-R018'],
  dict(current=1000,late=500,very_late=100,rate_current=.01,rate_late=.05,rate_very_late=.145,individual_loss=30,opening_allowance=20,uk_ifrs9=uk_ifrs9,objective_evidence=True),
  dict(matrix='current*rate_current+late*rate_late+very_late*rate_very_late',required='matrix if uk_ifrs9 else individual_loss',charge='required-opening_allowance',gross='current+late+very_late',net='gross-required'),
  dict(matrix=49.5,required=49.5 if uk_ifrs9 else 30,charge=29.5 if uk_ifrs9 else 10,gross=1600,net=1550.5 if uk_ifrs9 else 1570),'uk_ifrs9',uk_ifrs9,
  [post('selected loss model',('Dr','credit_loss','charge'),('Cr','allowance','charge'))],
  dict(receivable=1600,allowance=-49.5 if uk_ifrs9 else -30,credit_loss=29.5 if uk_ifrs9 else 10),
  'ECL-008 validates invoice population1600, lifetime rate/cohort support and individual objective evidence30; approved UK measurement policy selects method.',
  'Control prevents a forecast-only49.5 matrix being imposed on Sections11/12 and ensures the same exposure is not pooled and individual twice.',
  'UK policy version, evidence flag and model output persist; loss journal never changes revenue.',
  'Closing net1550.5 or1570 follows independently selected policy; Sections11/12 disclosures remain applicable to the IFRS9 measurement election.',dict(receivable=1600,allowance=-20)))
cases[8].append(make(8,'ECL-pool-individual-overlap',['IFRS','US_GAAP','AASB'],['IFRS-R006','US-R011','AASB-R006'],
 dict(gross=1000,individual_exposure=100,pool_rate=.02,individual_loss=30),
 dict(pool='gross-individual_exposure',collective='pool*pool_rate',required='collective+individual_loss',wrong='gross*pool_rate+individual_loss',overstatement='wrong-required'),
 dict(pool=900,collective=18,required=48,wrong=50,overstatement=2),'individual_exposure>0',True,
 [post('nonoverlapping loss assessment',('Dr','credit_loss','required'),('Cr','allowance','required'))],
 dict(receivable=1000,allowance=-48,credit_loss=48),
 'ECL-008 identifies the individual100 before pool construction; collective lifetime2% is independently supported under each selected loss framework.',
 'Overlap control detects the wrong50 calculation overstates losses2; pooled plus individual exposure must equal gross1000.',
 'Exposure ID100 is removed from pool membership and retained in individual assessment; membership versions are auditable.',
 'Allowance48/net952 with method and concentration notes; US lifetime support is documented separately from IFRS stage terminology.',dict(receivable=1000)))
for private in [False,True]:
 cases[8].append(make(8,'ECL-US-subsequent-cash-eligibility-'+str(private),['US_GAAP'],['US-R012','US-R013'],
  dict(exposure=100,subsequent_collection=60,remaining_rate=.1,non_pbe=private,current_606=True,expedient_adopted=True),
  dict(eligible='non_pbe and current_606 and expedient_adopted',basis='exposure-subsequent_collection if eligible else exposure',required='basis*remaining_rate'),
  dict(basis=40 if private else 100,required=4 if private else 10),
  'non_pbe and current_606 and expedient_adopted',private,
  [post('independently selected current-balance estimate',('Dr','credit_loss','required'),('Cr','allowance','required'))],
  dict(receivable=100,allowance=-4 if private else -10,credit_loss=4 if private else 10),
  'ECL-008 records 2026 effective adoption, current606 scope and collection60 before statements available for issuance; remaining10% is supported, not an automatic zero loss.',
  'Election gate rejects additional subsequent-cash relief for a PBE and rejects it without the underlying current-conditions expedient.',
  'Subsequent-cash evidence date and entity status enter election engine; reporting-date gross100 is not reduced by later cash in this estimate journal.',
  'Non-PBE allowance4 versus independently supported PBE10 illustrate eligibility rather than mandatory identical forecasts; note elected methodology.',dict(receivable=100)))

for us in [False,True]:
 cases[9].append(make(9,'WO-recovery-framework-'+str(us),['US_GAAP'] if us else ['IFRS','AASB'],
  ['US-R005','US-R008'] if us else ['IFRS-R005','IFRS-R007','AASB-R005','AASB-R007'],
  dict(writeoff=80,opening_allowance=70,recovery=15,closing_required=25,us=us),
  dict(topup='writeoff-opening_allowance',additional='closing_required-recovery if us else closing_required'),
  dict(topup=10,additional=10 if us else 25),'us',us,
  [post('allowance sufficient for partial writeoff',('Dr','credit_loss','topup'),('Cr','allowance','topup')),
   post('write off identified exposure',('Dr','allowance','writeoff'),('Cr','receivable','writeoff')),
   post('actual recovery',('Dr','cash','recovery'),('Cr','allowance' if us else 'credit_loss','recovery')),
   post('independent remaining portfolio loss',('Dr','credit_loss','additional'),('Cr','allowance','additional'))],
  dict(receivable=200,allowance=-25,cash=15,credit_loss=20),
  'WO-009 proves invoice80 uncollectible, retains collection rights and later remittance15, with independently measured loss25 on remaining200.',
  'Framework-specific recovery15 appears once; net asset190 versus opening210 reconciles to loss20 in both branches.',
  'Written-off exposure ID survives in recovery register; allowance rollforward distinguishes writeoff80, cash15 and closing25.',
  'GrossAR200/allowance25/cash15 and credit-loss result20 reconcile, while gross recovery display follows applicable regime.',dict(receivable=280,allowance=-70)))
cases[9].append(make(9,'WO-bank-fee-not-customer-default',ALL,[f'{f}-R010' for f in ['IFRS','US','UK','AASB']],
 dict(settlement=60,fee=2),dict(net_cash='settlement-fee'),dict(net_cash=58),'fee>0',True,
 [post('gross customer settlement with bank deduction',('Dr','cash','net_cash'),('Dr','bank_fee','fee'),('Cr','receivable','settlement'))],
 dict(receivable=0,cash=58,bank_fee=2,revenue=-60),
 'WO-009 ties bank statement58 to customer remittance60 and bank fee2; customer debt is fully settled.',
 'Cash-application control rejects a fictitious2 overdue receivable,2 bad-debt expense or2 revenue concession.',
 'Gross settlement and fee are separate bank transaction components with original invoice linkage.',
 'AR0, cash58, bank expense2 and unchanged revenue60; fee follows expense presentation, not bad debt.',dict(receivable=60,revenue=-60)))

for remit in [False,True]:
 cases[10].append(make(10,'UC-identification-and-remittance-'+str(remit),ALL,
  [f'{f}-R002' for f in ['IFRS','US','UK','AASB']]+[f'{f}-R010' for f in ['IFRS','US','UK','AASB']],
  dict(receipt=300,matched=120,future=100,unidentified=80,later_match=30,remit=remit),
  dict(remaining='unidentified-later_match',statutory_payment='remaining if remit else 0'),
  dict(remaining=50,statutory_payment=50 if remit else 0),'remit',remit,
  [post('bank receipt split',('Dr','cash','receipt'),('Cr','receivable','matched'),('Cr','contract_liability','future'),('Cr','unapplied_liability','unidentified')),
   post('later supported allocation',('Dr','unapplied_liability','later_match'),('Cr','receivable','later_match')),
   post('legal remittance obligation only when established',('Dr','unapplied_liability','statutory_payment'),('Cr','government_payable','statutory_payment')),
   post('statutory settlement',('Dr','government_payable','statutory_payment'),('Cr','cash','statutory_payment'))],
  dict(receivable=0,cash=250 if remit else 300,contract_liability=-100,unapplied_liability=0 if remit else -50,government_payable=0,revenue=0),
  'UC-010 evidences original120 invoice match,100 future service, later30 identified debt and governing-law remittance conclusion; absent legal proof,50 remains liability.',
  'Allocation children120+100+80 equal300; later30 reduces both unmatched liability and AR without revenue. Aging alone cannot release50.',
  'Bank receipt is immutable; allocation IDs and legal-review version drive reclassification50 and optional settlement, with no duplicate customer refund.',
  'Future-service liability100 persists; unmatched50 or paid government50 never becomes income; material credits are not buried in netAR.',dict(receivable=150)))

def write_cases():
    for n, rows in cases.items():
        folder=next(p for p in TOPICS.glob(f'TOPIC-03-{n:03d}-*') if (p/'phase-2d-method.md').exists())
        (folder/'phase-2d-scenarios.json').write_text(json.dumps({'cases':rows},indent=2)+'\n')

if __name__=='__main__':
    write_cases()
