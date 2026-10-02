"""Recognition/disclosure, range measurement and provision movement accounting."""
from decimal import Decimal
from core_accounting import cash, dec, required, ReviewRequired, journal
from production import flag, fraction, nonnegative

def assess(c,claims):
    required(c,'obligation','estimate','movements','reimbursement','specialist_items')
    if c['specialist_items']:raise ReviewRequired('Unresolved provision specialist matters: '+', '.join(c['specialist_items']))
    o=c['obligation'];required(o,'type','basis','probability','obligation_memo','past_event','present_obligation','estimable')
    past=flag(o,'past_event'); present=flag(o,'present_obligation'); estimable=flag(o,'estimable')
    if o['basis'] not in ('legal','constructive','possible'):raise ReviewRequired('Unresolved obligation basis')
    if o['type'] not in ('litigation','warranty','onerous','restructuring','decommissioning','other_provision','contingent_asset'):raise ReviewRequired('Unknown provision scope')
    if o['basis']=='possible' and present:raise ReviewRequired('Possible obligation cannot also be an established present obligation')
    us=c['framework']=='US_GAAP'
    if us and o['basis']=='constructive':raise ReviewRequired('ASC450 obligation cannot be inferred from IAS37 constructive-obligation route')
    if us:
        if o['probability'] not in ('probable','reasonably_possible','remote'):raise ReviewRequired('ASC450 qualitative probability categories required')
        probable=o['probability']=='probable';disclose=o['probability']!='remote'
    else:
        if o['probability'] not in ('more_likely_than_not','possible','remote'):raise ReviewRequired('IAS37/FRS102 qualitative probability categories required')
        probable=o['probability']=='more_likely_than_not';disclose=o['probability']!='remote'
    recognize=past and present and probable and estimable
    if o['type']=='restructuring':
        required(o,'detailed_plan','valid_expectation','direct_expenditures_only')
        if us:raise ReviewRequired('US restructuring/exit costs require ASC420/712 event-specific handoff, not ASC450 generic accrual')
        if not (flag(o,'detailed_plan') and flag(o,'valid_expectation') and flag(o,'direct_expenditures_only')):
            recognize=False
    if o['type']=='decommissioning' and us:raise ReviewRequired('US asset retirement obligation requires ASC410 specialist, not ASC450')
    e=c['estimate'];required(e,'basis','outcomes','discount_rate','years','risk_memo','estimate_memo')
    amount=Decimal(0)
    if recognize:
        if o['type']=='onerous':
            if us:raise ReviewRequired('US contract-specific loss model required; no general IAS37 onerous provision')
            required(e,'fulfilment_cost','benefits','exit_cost','asset_impairment_first','no_double_count_memo')
            if not flag(e,'asset_impairment_first'):raise ReviewRequired('Perform contract asset impairment before onerous measurement')
            amount=min(max(Decimal(0),nonnegative(e['fulfilment_cost'])-nonnegative(e['benefits'])),nonnegative(e['exit_cost']))
        elif us:
            if e['basis']!='asc450_range':raise ReviewRequired('Use ASC450 best estimate or minimum-of-range route')
            required(e,'low','high')
            if 'best_estimate' not in e:raise ReviewRequired('Best estimate decision must explicitly be supplied, including null for none')
            low=nonnegative(e['low']);high=nonnegative(e['high'])
            if low>high:raise ReviewRequired('Range is reversed')
            if e['best_estimate'] is None:amount=low
            else:
                amount=nonnegative(e['best_estimate'])
                if not low<=amount<=high:raise ReviewRequired('Best estimate is outside supportable range')
        elif e['basis']=='expected_value':
            if not e['outcomes'] or sum(fraction(x['probability']) for x in e['outcomes'])!=1:raise ReviewRequired('Outcome probabilities must total one')
            amount=sum(nonnegative(x['amount'])*fraction(x['probability']) for x in e['outcomes'])
        elif e['basis']=='most_likely':
            required(e,'selected_amount','other_outcomes_memo')
            amount=nonnegative(e['selected_amount'])
        elif e['basis']=='continuous_equal_range':
            low=nonnegative(e['low']);high=nonnegative(e['high'])
            if low>high:raise ReviewRequired('Range is reversed')
            amount=(low+high)/2
        else:raise ReviewRequired('Unsupported best-estimate method')
    rate=dec(e['discount_rate']);years=dec(e['years'])
    if rate<=-1 or years<0:raise ReviewRequired('Invalid discount rate/timing')
    if us and rate!=0 and not c['policy_elections'].get('us_discounting_exception_memo'):
        raise ReviewRequired('ASC450 does not generally discount; specific exception required')
    provision=cash(amount/(1+rate)**years)
    m=c['movements'];required(m,'opening','settlements','unwind','fx','other','movement_evidence')
    opening=nonnegative(m['opening']);settled=nonnegative(m['settlements']);unwind=nonnegative(m['unwind']);fx=dec(m['fx']);other=dec(m['other'])
    if fx!=0 or other!=0:raise ReviewRequired('FX/other provision movements require supported balanced event journals; this workpaper cannot use unexplained bridge amounts')
    reestimate=cash(provision-opening+settled-unwind-fx-other)
    entries=[]
    destination='restoration asset' if o['type']=='decommissioning' else 'provision expense'
    if reestimate>=0:entries.append(journal(('Dr',destination,reestimate),('Cr','provision',reestimate)))
    else:entries.append(journal(('Dr','provision',-reestimate),('Cr',destination,-reestimate)))
    if settled:entries.append(journal(('Dr','provision',settled),('Cr','cash',settled)))
    if unwind:entries.append(journal(('Dr','finance cost',unwind),('Cr','provision',unwind)))
    r=c['reimbursement'];required(r,'claimed','recognition_threshold_met','reimbursement_memo','opening_asset','cash_received')
    asset=min(nonnegative(r['claimed']),provision) if flag(r,'recognition_threshold_met') else Decimal(0)
    if us and asset and not c['policy_elections'].get('us_recovery_recognition_memo'):
        raise ReviewRequired('US recovery recognition assessed independently from liability')
    receipts=nonnegative(r['cash_received']);change=cash(asset-nonnegative(r['opening_asset'])+receipts)
    if change>=0:entries.append(journal(('Dr','reimbursement receivable',change),('Cr','reimbursement income',change)))
    else:entries.append(journal(('Dr','reimbursement impairment',-change),('Cr','reimbursement receivable',-change)))
    if receipts:entries.append(journal(('Dr','cash',receipts),('Cr','reimbursement receivable',receipts)))
    decision='recognize' if recognize else 'disclose_contingency' if disclose else 'no_recognition_or_disclosure'
    if o['type']=='contingent_asset':
        raise ReviewRequired('Contingent assets require separate virtually-certain/probable gain route; do not recognize as negative provisions')
    if not recognize and opening:
        required(o,'release_memo')
    return {'conclusion':f'Provision decision {decision}; closing liability {provision}; estimate movement {reestimate}; separate reimbursement asset {cash(asset)}.',
      'method':{'decision':decision,'estimate_basis':e['basis'],'framework_threshold':o['probability']},
      'calculations':{'undiscounted_estimate':cash(amount),'provision':provision,'reimbursement':cash(asset),
       'provision_bridge':{'opening':opening,'estimate_change':reestimate,'settlements':settled,'unwind':unwind,'fx':fx,'other':other,'closing':provision}},
      'journal_entry_implications':entries,'judgments':[o['obligation_memo'],e['estimate_memo'],e['risk_memo'],r['reimbursement_memo']],
      'uncertainties':['Probability and legal outcome are supported judgments, not statistical thresholds inferred by the calculator. Reimbursements are separate assets; no balance-sheet netting is implied.'],
      'open_items':[],'disclosures_impacted':['Provision opening-to-closing movements by class','Nature, timing and uncertainty of obligations','Assumptions, expected reimbursements and recognized reimbursement assets','Contingent liability description and financial effect or why not practicable','ASC450 additional reasonably possible exposure beyond accrued amount','Apply framework-specific prejudicial-information exception with reviewer support']}
