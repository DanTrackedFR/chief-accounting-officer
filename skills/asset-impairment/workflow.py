"""Framework-specific recoverability, allocation and reversal workpaper."""
from decimal import Decimal
from core_accounting import cash, dec, required, ReviewRequired, journal
from production import flag, fraction, nonnegative
from advanced_accounting import gate, unique, positive, result, ZERO

def allocate(loss,assets):
    """Pro-rata allocation with floors; repeat after a floor binds, residual explicit."""
    remaining=cash(loss);out={a['id']:ZERO for a in assets}
    active=[a for a in assets if a['carrying']>a['floor']]
    while remaining and active:
        weights=sum((a['carrying'] for a in active),ZERO)
        if not weights:
            if len(active)!=1:raise ReviewRequired('Zero-carrying unit needs a specialist allocation basis')
            a=active[0];assigned=min(remaining,a['carrying']-a['floor']-out[a['id']]);out[a['id']]+=assigned;remaining-=assigned
            break
        budget=remaining;used=ZERO
        for index,a in enumerate(active):
            capacity=a['carrying']-a['floor']-out[a['id']]
            proposed=cash(budget*a['carrying']/weights) if index<len(active)-1 else budget-used
            assigned=min(capacity,max(proposed,ZERO));out[a['id']]+=assigned;used+=assigned
        if not used:break
        remaining-=used
        active=[a for a in active if out[a['id']]<a['carrying']-a['floor']]
    return out,remaining

def assess(c,claims):
    gate(c,'unit','assets','valuation','reversal')
    u=c['unit'];required(u,'model','perimeter_memo','indicator_memo','sequence_memo','annual_test','indicator','carrying_alignment','other_tests_complete','uk_amortization_complete')
    if not flag(u,'carrying_alignment') or not flag(u,'other_tests_complete'):
        raise ReviewRequired('Align valuation/carrying perimeter and complete preceding asset tests')
    if c['framework']=='UK_GAAP' and not flag(u,'uk_amortization_complete'):
        raise ReviewRequired('UK goodwill amortization must precede impairment')
    us=c['framework']=='US_GAAP'
    if c['policy_elections'].get('private_company_alternative',False):raise ReviewRequired('Private-company impairment/amortization alternatives need separate schedule')
    if u['model'] not in (('asc360','asc350_goodwill','asc350_indefinite') if us else ('recoverable_amount',)):
        raise ReviewRequired('Framework impairment model mismatch or held-for-sale specialist boundary')
    unique(c['assets']);assets=[]
    for a in c['assets']:
        required(a,'account','type','carrying','floor','no_impairment_ceiling','valuation_evidence')
        if a['type'] not in ('goodwill','finite','indefinite'):raise ReviewRequired('Asset type unresolved')
        b=dict(a);b['carrying']=cash(nonnegative(a['carrying']));b['floor']=cash(nonnegative(a['floor']))
        b['ceiling']=cash(nonnegative(a['no_impairment_ceiling']))
        if b['floor']>b['carrying']:raise ReviewRequired('Allocation floor exceeds carrying amount')
        assets.append(b)
    goodwill=[a for a in assets if a['type']=='goodwill'];other=[a for a in assets if a['type']!='goodwill']
    if len(goodwill)>1:raise ReviewRequired('One reconciled goodwill layer per tested unit required')
    if u['model']=='asc360' and goodwill:raise ReviewRequired('ASC360 group must exclude separately tested goodwill')
    if u['model']=='asc360' and any(a['type']!='finite' for a in assets):raise ReviewRequired('ASC360 group must exclude ASC350 indefinite assets')
    if u['model']=='asc350_indefinite' and (len(assets)!=1 or assets[0]['type']!='indefinite'):
        raise ReviewRequired('Indefinite-lived intangible uses its separate test')
    carrying=sum((a['carrying'] for a in assets),ZERO);gw=sum((a['carrying'] for a in goodwill),ZERO)
    annual=flag(u,'annual_test');indicator=flag(u,'indicator')
    if c['framework']=='UK_GAAP' and any(a['type']=='indefinite' for a in assets):raise ReviewRequired('FRS102 intangible useful-life/amortization assessment required; do not import IFRS indefinite life')
    if c['framework']!='UK_GAAP' and (goodwill or any(a['type']=='indefinite' for a in assets)) and not annual:
        raise ReviewRequired('Annual goodwill/indefinite test not completed')
    v=c['valuation'];required(v,'cash_flows','discount_rate','terminal_value','fv_less_costs','fair_value','undiscounted','memo','inputs_reviewed')
    if not flag(v,'inputs_reviewed'):raise ReviewRequired('Unreviewed forecast/market valuation inputs')
    rate=dec(v['discount_rate'])
    if rate<=-1:raise ReviewRequired('Invalid discount rate')
    terms=v['cash_flows'];unique(terms,'year')
    if any(dec(t['year'])<=0 or dec(t['year'])!=int(dec(t['year'])) for t in terms):raise ReviewRequired('DCF years must be positive integers')
    # Cash flows can be negative; terminal value is supplied, never inferred growth.
    viu=cash(sum((dec(t['amount'])/(1+rate)**int(dec(t['year'])) for t in terms),ZERO)+nonnegative(v['terminal_value'])/(1+rate)**max(int(dec(t['year'])) for t in terms))
    fv=cash(nonnegative(v['fair_value']));fvlcd=cash(nonnegative(v['fv_less_costs']));undisc=cash(dec(v['undiscounted']))
    recoverable=max(viu,fvlcd);loss=ZERO
    if annual or indicator:
        if u['model']=='recoverable_amount':loss=max(carrying-recoverable,ZERO)
        elif u['model']=='asc360':loss=max(carrying-fv,ZERO) if carrying>undisc else ZERO
        elif u['model']=='asc350_goodwill':loss=min(gw,max(carrying-fv,ZERO))
        else:loss=max(carrying-fv,ZERO)
    if u['model']=='asc350_goodwill' and not goodwill:raise ReviewRequired('Goodwill model has no goodwill')
    allocation={a['id']:ZERO for a in assets};remaining=loss
    if goodwill:
        assigned=min(gw,remaining);allocation[goodwill[0]['id']]=assigned;remaining-=assigned
    if remaining:
        distribution,residual=allocate(remaining,other)
        if residual:raise ReviewRequired('Allocation floors leave an unallocated loss; specialist liability/perimeter assessment required')
        allocation.update(distribution)
    entries=[];closing={a['id']:a['carrying']-allocation[a['id']] for a in assets}
    for a in assets:entries.append(journal(('Dr','impairment expense',allocation[a['id']]),('Cr',a['account'],allocation[a['id']])))
    r=c['reversal'];required(r,'requested','amounts','change_memo')
    reversals={a['id']:ZERO for a in assets}
    if flag(r,'requested'):
        if us:raise ReviewRequired('ASC350/360 held-and-used impairment is not reversed')
        if loss:raise ReviewRequired('Separate impairment and reversal events to avoid incompatible unit tests')
        if not isinstance(r['amounts'],dict) or set(r['amounts'])-set(closing):raise ReviewRequired('Unknown reversal asset')
        budget=max(recoverable-carrying,ZERO)
        required(r,'allocation_model','individual_recoverable_caps','individual_recoverable_memo')
        if r['allocation_model'] not in ('individual','unit_pro_rata') or (r['allocation_model']=='individual' and len(assets)!=1):
            raise ReviewRequired('Reversal requires individual asset or unit pro-rata method')
        if not isinstance(r['individual_recoverable_caps'],dict) or set(r['individual_recoverable_caps'])!={a['id'] for a in other}:
            raise ReviewRequired('Individual recoverable cap decisions required for every nongoodwill asset')
        for a in other:
            cap=r['individual_recoverable_caps'][a['id']]
            if cap is not None:a['ceiling']=min(a['ceiling'],cash(nonnegative(cap)))
        capacity_assets=[dict(a,floor=a['carrying']-max(a['ceiling']-a['carrying'],ZERO)) for a in other]
        target=min(budget,sum((max(a['ceiling']-a['carrying'],ZERO) for a in other),ZERO))
        expected_reversals,_=allocate(target,capacity_assets)
        for a in assets:
            requested=cash(nonnegative(r['amounts'].get(a['id'],'0')))
            if a['type']=='goodwill' and requested:raise ReviewRequired('Goodwill impairment is never reversed')
            if requested>max(a['ceiling']-a['carrying'],ZERO):raise ReviewRequired('Reversal exceeds no-impairment depreciated ceiling')
            if a['type']!='goodwill' and requested!=expected_reversals.get(a['id'],ZERO):
                raise ReviewRequired('Reversal allocation does not match recoverable headroom and pro-rata ceilings')
            reversals[a['id']]=requested;closing[a['id']]+=requested
            entries.append(journal(('Dr',a['account'],requested),('Cr','impairment reversal income',requested)))
        if sum(reversals.values())>budget:raise ReviewRequired('Reversal exceeds recoverable headroom')
    elif r['amounts']:raise ReviewRequired('Reversal amounts supplied without reversal decision')
    return result('Impairment test, asset allocation and carrying-value bridge reconcile.',
      {'model':u['model'],'indicator':indicator,'annual_test':annual},
      {'carrying':carrying,'value_in_use':viu,'fv_less_costs':fvlcd,'recoverable':recoverable,'fair_value':fv,
       'undiscounted':undisc,'loss':loss,'allocation':allocation,'reversals':reversals,'closing':closing,
       'headroom':recoverable-carrying if not us else fv-carrying},entries,
      [u['perimeter_memo'],u['indicator_memo'],u['sequence_memo'],v['memo'],r['change_memo']],
      ['Events/indicators and unit composition','Loss/reversal by class, segment and statement line','Goodwill allocation and testing frequency',
       'Valuation basis, forecast horizon, discount and growth inputs','Fair-value input hierarchy and uncertainty','Headroom and reasonably possible sensitivity changes'],
      ['Discount and terminal assumptions require valuation support. Ordinary cost-model units only; revaluation OCI, held-for-sale, financial assets and private-company alternatives are specialist methods.'])
