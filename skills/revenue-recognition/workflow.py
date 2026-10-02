"""Five-step assessment and cumulative-to-period revenue accounting.

Rules are grounded in TOPIC-03-001–006/012; framework-specific judgments
are evidenced inputs. No legal conclusion is inferred from arithmetic.
"""
from decimal import Decimal
from core_accounting import cash, dec, required, ReviewRequired, journal
from production import flag, fraction, nonnegative
from pathlib import Path
import importlib.util
_spec=importlib.util.spec_from_file_location('rev_math',Path(__file__).with_name('engine.py'))
_math=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_math)

def movement(dr,cr,amount):
    n=cash(amount)
    return journal(('Dr',dr,n),('Cr',cr,n)) if n>=0 else journal(('Dr',cr,-n),('Cr',dr,-n))

def transaction_price(c):
    required(c,'price_components')
    p=c['price_components']; required(p,'fixed','noncash','customer_payments','financing_adjustment','variable')
    fixed=nonnegative(p['fixed']); variable=Decimal(0)
    for v in p['variable']:
        required(v,'method','outcomes','constraint_memo','included_amount','royalty_exception')
        outcomes=v['outcomes']
        if not outcomes: raise ReviewRequired('Variable price needs supported outcomes')
        if v['method']=='expected_value':
            if sum(fraction(x['probability']) for x in outcomes)!=1: raise ReviewRequired('Variable probabilities must total one')
            estimate=sum(dec(x['amount'])*fraction(x['probability']) for x in outcomes)
        elif v['method']=='most_likely':
            estimate=dec(max(outcomes,key=lambda x:fraction(x['probability']))['amount'])
        else: raise ReviewRequired('Unsupported variable estimate method')
        included=dec(v['included_amount'])
        if included>max(dec(x['amount']) for x in outcomes) or included<min(Decimal(0),min(dec(x['amount']) for x in outcomes)):
            raise ReviewRequired('Constrained amount is outside supported outcomes')
        if flag(v,'royalty_exception') and not flag(v,'royalty_event_and_satisfaction_met') and included!=0:
            raise ReviewRequired('IP royalty accelerated before event/satisfaction')
        variable+=included
    price=cash(fixed+variable+dec(p['noncash'])-nonnegative(p['customer_payments'])+dec(p['financing_adjustment']))
    if price<0: raise ReviewRequired('Negative consideration requires customer-payment specialist route')
    return price

def timing(c,o,legacy):
    required(o,'timing','timing_evidence')
    if legacy:
        required(o,'legacy_route')
        if o['legacy_route']=='goods': return Decimal(1) if flag(o,'risks_rewards_transferred') else Decimal(0)
        if o['legacy_route']=='service':
            if not flag(o,'reliable_completion'):
                required(o,'recoverable_cost_revenue'); return None
            return fraction(o['progress'])
        raise ReviewRequired('Legacy UK construction/other route needs specialist schedule')
    if o['timing']=='point_in_time': return Decimal(1) if flag(o,'control_transferred') else Decimal(0)
    if o['timing']!='over_time': raise ReviewRequired('Unknown satisfaction pattern')
    a=flag(o,'simultaneous_receipt'); b=flag(o,'customer_controls_asset')
    d=flag(o,'no_alternative_use'); e=flag(o,'right_to_payment_with_margin')
    if not (a or b or (d and e)): raise ReviewRequired('Over-time criteria fail; apply control-transfer route')
    if not flag(o,'progress_reliable'):
        required(o,'recoverable_cost_revenue')
        return None
    return fraction(o['progress'])

def assess(c,claims):
    required(c,'contract','obligations','balance_bridge','contract_costs','specialist_items')
    contract=c['contract']
    for k in ['customer_in_scope','approved_committed','rights_identified','payment_terms_identified','commercial_substance','collectibility_met']:
        if not flag(contract,k): raise ReviewRequired('Contract criterion failed: '+k+'; received cash remains liability pending framework-specific review')
    required(contract,'combination_memo','scope_memo')
    if c['specialist_items']: raise ReviewRequired('Complete specialist schedules for: '+', '.join(c['specialist_items']))
    legacy=c['framework']=='UK_GAAP' and c['period_start']<'2026-01-01' and not c['policy_elections'].get('early_adopt_revised_section23',False)
    if c['framework']=='UK_GAAP':
        expected='legacy' if legacy else 'revised_2026'
        if c['policy_elections'].get('section23_model')!=expected: raise ReviewRequired('UK Section 23 election/period mismatch')
    price=transaction_price(c)
    obs=c['obligations']; ids=[o['id'] for o in obs]
    if not obs or len(set(ids))!=len(ids): raise ReviewRequired('Unique promise IDs required')
    for o in obs:
        required(o,'distinct_memo','ssp_evidence','role','role_memo')
        if o['role'] not in ('principal','agent'): raise ReviewRequired('Resolve principal/agent control analysis')
    allocation=c.get('specific_allocation')
    if allocation:
        required(allocation,'amounts','objective_memo')
        if set(allocation['amounts'])!=set(ids): raise ReviewRequired('Specific allocation must address every obligation')
        amounts={k:cash(nonnegative(v)) for k,v in allocation['amounts'].items()}
        if sum(amounts.values())!=price: raise ReviewRequired('Specific allocation does not reconcile to price')
    else: amounts={x['obligation']:x['allocation'] for x in _math.allocate(price,obs)}
    modification=c.get('modification')
    route='none'
    if modification:
        for key in ['approved','added_distinct','price_at_adjusted_ssp','remaining_distinct']: flag(modification,key)
        if not modification['approved']: raise ReviewRequired('Unapproved modification; original contract remains operative')
        if modification['added_distinct'] and modification['price_at_adjusted_ssp']:
            route='separate_contract'
            raise ReviewRequired('Run separate added contract case and retain original contract case')
        elif modification['remaining_distinct']:
            route='prospective'
            required(modification,'unrecognized_old_price','new_price','remaining_obligation_ids')
            rem=[o for o in obs if o['id'] in modification['remaining_obligation_ids']]
            if not rem: raise ReviewRequired('Missing remaining promises')
            amounts={x['obligation']:x['allocation'] for x in _math.allocate(dec(modification['unrecognized_old_price'])+dec(modification['new_price']),rem)}
            obs=rem
        else:
            route='cumulative_catch_up' # revised price/progress drive cumulative result below
            required(modification,'integrated_promise_memo')
    rows=[]; cumulative=Decimal(0)
    for o in obs:
        progress=timing(c,o,legacy)
        value=cash(o['recoverable_cost_revenue']) if progress is None else cash(amounts[o['id']]*progress)
        if value<0 or value>amounts[o['id']]: raise ReviewRequired('Revenue outside obligation allocation')
        if o['role']=='agent':
            required(o,'net_fee_basis_memo') # SSP/price must be entity fee, not underlying supplier gross sale
        rows.append({'id':o['id'],'allocation':amounts[o['id']],'cumulative_revenue':value,'role':o['role']})
        cumulative+=value
    b=c['balance_bridge'];required(b,'opening_revenue','opening_contract_net','opening_receivable','billings','cash_received','opening_cost_asset')
    prior=nonnegative(b['opening_revenue']); revenue=cash(cumulative-prior)
    if route=='prospective':
        # Only remaining performance is in this workpaper. Original completed revenue is preserved.
        cumulative=cash(prior+cumulative); revenue=cash(cumulative-prior)
    opening=dec(b['opening_contract_net']); bill=nonnegative(b['billings']); receipts=nonnegative(b['cash_received'])
    closing=cash(opening+revenue-bill); ar=cash(nonnegative(b['opening_receivable'])+bill-receipts)
    if ar<0: raise ReviewRequired('Overpayments require separate customer-credit liability')
    entries=[movement('contract clearing','revenue',revenue)]
    if bill: entries.append(journal(('Dr','receivable',bill),('Cr','contract clearing',bill)))
    if receipts: entries.append(journal(('Dr','cash',receipts),('Cr','receivable',receipts)))
    additions=amortization=impairment=Decimal(0)
    for cost in c['contract_costs']:
        required(cost,'amount','capitalization_memo','recoverable','qualifying','amortization','impairment')
        amount=nonnegative(cost['amount'])
        qualifies=flag(cost,'qualifying') and flag(cost,'recoverable')
        if qualifies:
            additions+=amount; entries.append(journal(('Dr','contract cost asset',amount),('Cr','cash / payable',amount)))
        else: entries.append(journal(('Dr','contract cost expense',amount),('Cr','cash / payable',amount)))
        amortization+=nonnegative(cost['amortization']);impairment+=nonnegative(cost['impairment'])
    costclosing=cash(nonnegative(b['opening_cost_asset'])+additions-amortization-impairment)
    if costclosing<0: raise ReviewRequired('Contract cost amortization/impairment exceeds asset')
    if amortization:entries.append(journal(('Dr','contract cost amortization',amortization),('Cr','contract cost asset',amortization)))
    if impairment:entries.append(journal(('Dr','contract cost impairment',impairment),('Cr','contract cost asset',impairment)))
    return {'conclusion':f'Revenue assessment: period revenue {revenue}; closing contract asset {max(closing,0)} and liability {max(-closing,0)}; receivable {ar}.',
      'method':('Legacy FRS 102 sale/service model' if legacy else 'Five-step contract model')+'; modification '+route,
      'calculations':{'transaction_price':price,'obligations':rows,'cumulative_revenue':cumulative,'period_revenue':revenue,
        'contract_bridge':{'opening':opening,'revenue':revenue,'billings':bill,'closing':closing},'receivable':ar,'contract_cost_asset':costclosing},
      'journal_entry_implications':entries,'judgments':[c['judgment_memo'],contract['collectibility_met'],*[o['timing_evidence'] for o in obs]],
      'uncertainties':['Contract clearing journals require mapping to the contract-specific asset/liability accounts; do not offset different contracts.'],
      'open_items':[],'disclosures_impacted':['Disaggregate revenue by meaningful categories','Reconcile receivables and contract assets/liabilities','Performance obligations, payment terms and remaining obligations','Timing, progress, price constraint and SSP judgments','Contract cost balances, amortization and impairment','Apply US nonpublic, UK small entity and AASB tier relief only when eligible']}
