"""Synthetic grant agreements and independent arithmetic oracle; no real approval."""
from copy import deepcopy
from decimal import Decimal
from cases import base,finalize
from operational_cases import approved
from reporting_cases import pol
from production import case_fingerprint

EDITIONS={'IFRS':'IAS20_2026','AASB':'AASB120_2021_2026','UK_GAAP':'FRS102_SEP2024_2026','US_GAAP':'ASU2025_10_ADOPTED_2026'}

def case(fw='IFRS',route='income'):
    c=base('government-grants',fw);c['jurisdiction']={'IFRS':'NL','AASB':'AU','UK_GAAP':'GB','US_GAAP':'US'}[fw];c.update(package='government-grants',execution_date='2027-02-01',functional_currency='EUR',imports=[])
    c['applicability_review']['standard_versions']=[EDITIONS[fw]]
    if fw=='AASB':c['aasb_compilation']='2021 compilation applicable 2026'
    model={'IFRS':'IAS20_ACCRUAL','AASB':'AASB120_ACCRUAL','UK_GAAP':'FRS102_ACCRUAL','US_GAAP':'ASC832_ASU2025_10_ADOPTED'}[fw]
    if route=='performance':model='FRS102_PERFORMANCE'
    p='asset_deduction' if route=='deduction' else 'cost_accumulation' if route=='cost_accumulation' else 'deferred_income'
    c['accounting_policy']=pol(c,'policy',grant_model=model,early_presentation_adoption=False,presentation_by_class={'income':'deferred_income','asset':p},nonmonetary_measurement='fair_value')
    c['accounting_policy']['effective_standard']=EDITIONS[fw]
    c['controls']=dict(source_version='v1',as_of=c['reporting_period'],population_count=1,population_amount='100',owner='synthetic grant census owner',reviewer='synthetic grant census reviewer',complete=True,policy_version='v1',cutoff_memo='Independent award census and source completeness')
    c['disclosure_review']=approved('disclosure',checklist_version='v1',period_entity_memo='Framework policy, amounts, grant nature, assistance, conditions and clawback terms inspected',complete=True)
    def b(id,**kw):return approved(id,source_entity=c['entity'],source_framework=fw,source_period=[c['period_start'],c['reporting_period']],currency='EUR',**kw)
    asset=route in ('asset','deduction','nonmonetary','cost_accumulation')
    g=b('award',agreement_memo='Executed award 100',grantor_memo='Government grantor verified',conditions_memo='Terms independently inspected',classification_memo='Long-term plant' if asset else 'Eligible wages',rights_memo='Award and reimbursement right current',agreement_id='signed-award',economic_id='government-award-1',grantor='Synthetic government',grantor_identity_evidence='Official grantor legal identity',government_confirmed=True,substance='grant',classification='asset' if asset else 'income',event='repayment' if route=='repayment' else 'advance' if route=='advance' else 'recognition',transfer='nonmonetary' if route=='nonmonetary' else 'monetary',presentation=p,agreement_amount='100',opening_deferred='30' if route=='repayment' else '0',opening_receivable='0',opening_advance='0',receivable_right_supported=True,recognition_date='2026-06-30',recognized_addition='100',total_eligible_expense_basis='500',past_cost_compensation=route=='past',no_future_costs=True)
    g['opening_history']=b('grant-history',history_memo='Independent opening award, cash, recognized income and basis history',recognized_total='100' if route=='repayment' else '0',cash_total='100' if route=='repayment' else '0',income_total='70' if route=='repayment' else '0',basis_total='0',prior_repayments='0',prior_advances='0')
    g['recognition_review']=b('recognition',receipt_memo='Award receipt likely with executed terms',compliance_memo='Independent inspection of qualifying costs and retention plan',threshold='probable' if fw=='US_GAAP' else 'reasonable_assurance',receipt_supported=True,compliance_supported=route!='advance')
    g['conditions']=[b('retention',kind='performance',due_date='2027-12-31',as_of=c['reporting_period'],compliance_memo='Supported actual milestone and ongoing retention',compliance_evidenced=True,met=route!='advance')];g['condition_inventory']=['retention']
    g['eligible_costs']=[b('cost',economic_id='payroll-or-plant-1',accounting_owner='fixed-assets' if asset else 'employee-benefits-payroll',grant_id='award',cost_memo='Original cost register and invoice',classification_memo='Asset owner determines plant basis' if asset else 'Payroll owner determines wages',amount='500',current_expense='50' if asset else '200',owner_gl_amount='500',incurred_date='2026-06-30')];g['cost_inventory']=['cost']
    g['asset']=b('plant',asset_id='plant-1',accounting_owner='fixed-assets',grant_id='award',asset_memo='Cost 500 in original owner register',expense_pattern_memo='Depreciable cost500 expense50 supplied by asset owner',grant_adjustment_memo='Grant adjustment distinct from original acquisition and depreciation',cost='500',available_for_use_date='2026-01-01',expense_model='depreciation',useful_life_years='10',residual_value='0',total_expense_basis='500',current_expense='50',disposed=False,impaired=False,life_changed=False,basis_adjustment_not_posted=True,owner_clearing_entry_supported=True)
    g['payments']=[] if route in ('nonmonetary','repayment') else [b('receipt',bank_id='bank-grant-1',grant_id='award',bank_memo='Actual receipt independently matched to award',date='2026-06-30',amount='100')];g['payment_inventory']=[x['id'] for x in g['payments']]
    g['repayment']=b('clawback',obligation_memo='Present enforceable repayment obligation',trigger_memo='New condition failure in current period',estimate_memo='New estimate not prior error',trigger_date='2026-12-01',obligation_supported=True,error_vs_estimate='new_estimate',amount='70',simple_model_conclusion=True)
    g['measurement']='fair_value';g['valuation']=b('value',asset_id='plant-1',valuation_date='2026-06-30',valuation_memo='Qualified independent actual fair value',qualified=True,fair_value='100',nominal='1',cost_to_entity='0')
    c['grants']=[g];c['source_inventory']=['award']
    c['journal_ownership']=[b('ownership',economic_id=g['economic_id'],accounting_owner='government-grants',already_posted=False,ownership_memo='Distinct grant economic accounting; owner costs remain original')];c['ownership_inventory']=['ownership']
    if fw=='US_GAAP':c['us_adoption']=b('adoption',standard='ASU2025-10',annual_period_start='2026-01-01',financial_statements_unissued_at_adoption=True,transition_reviewed=True,evidence_id='actual-adoption-memo',adoption_date='2026-03-01',transition_memo='Retrospective adoption across presented years inspected',unissued_memo='Financial statements unissued at adoption')
    oracle(c);capture(c);return c


def oracle(c):
    """Independent expected movements and source GL, not a production call."""
    g=c['grants'][0];asset=g['classification']=='asset';event=g['event'];basis=g['presentation']!='deferred_income'
    release=Decimal(0) if event!='recognition' or basis else Decimal(100) if c['accounting_policy']['grant_model']=='FRS102_PERFORMANCE' or g['past_cost_compensation'] else Decimal(10 if asset else 40)
    closing=Decimal(0) if basis or event!='recognition' else Decimal(100)-release
    repayment=Decimal(70) if event=='repayment' else Decimal(0);expense=Decimal(40) if event=='repayment' else Decimal(0)
    advance=Decimal(100) if event=='advance' else Decimal(0);adjustment=Decimal(100) if basis and event=='recognition' else Decimal(0)
    g['expected']={k:str(v) for k,v in dict(closing_deferred=closing,closing_receivable=0,grant_income=release,repayment_expense=expense,basis_adjustment=adjustment,closing_advance=advance).items()}
    def b(id,**kw):return approved(id,source_entity=c['entity'],source_framework=c['framework'],source_period=[c['period_start'],c['reporting_period']],currency='EUR',**kw)
    g['disclosure']=b('grant-disclosure',nature_memo='Actual award and monetary/nonmonetary extent',conditions_contingencies_memo='Actual retention and repayment terms',assistance_memo='No other assistance in complete source register',policy_memo='Actual selected class policy and model',grant_model=c['accounting_policy']['grant_model'],presentation=g['presentation'],**g['expected'])
    g['release_schedule']=[b('future',date='2027-12-31',amount=str(closing),expense_basis=str(closing/Decimal(g['agreement_amount'])*Decimal(g['total_eligible_expense_basis'])),schedule_memo='Supported full future eligible expense/asset pattern')] if closing else [];g['schedule_inventory']=[r['id'] for r in g['release_schedule']]
    nonmon=g['transfer']=='nonmonetary';d={'Grant receivable':(0,0),'Grant cash':(0,0 if nonmon or repayment else 100),'Deferred grant':(-30 if repayment else 0,-closing),'Grant income':(0,-release),'Grant repayment expense':(0,expense),'Grant repayment payable':(0,-repayment),'Grant advance':(0,-advance),'Grant asset contra-basis':(0,-adjustment),'Nonmonetary grant clearing':(-100 if nonmon else 0,0)}
    c['gl']=[approved(k,opening=str(op),closing=str(cl),statement=str(cl)) for k,(op,cl) in d.items()];c['gl_inventory']=list(d)
    return c


def capture(c):
    c['original_source_snapshot']=approved('original-grant-sources',capture_memo='Synthetic independently frozen originals before accounting calculation',records=deepcopy({k:c[k] for k in ('grants','gl','journal_ownership','functional_currency')}));return c


def ready(fw='IFRS',route='income',c=None):
    c=deepcopy(c) if c is not None else case(fw,route)
    c=finalize('government-grants',c)
    c['knowledge_review']['applied_claim_ids']=c['knowledge_review']['claim_ids'][:]
    c['reviewer_signoff']['case_fingerprint']=case_fingerprint(c)
    return c
