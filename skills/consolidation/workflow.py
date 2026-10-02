"""Control assessment, consolidated TB, eliminations and NCI bridges.

Acquisition and translation facts must be independently supported; no fair-value,
exchange-rate or legal-control assumptions are manufactured.
"""
from decimal import Decimal
from core_accounting import cash, dec, required, ReviewRequired, journal, balance
from production import flag, fraction, nonnegative

def control(c,a):
    required(a,'control_memo','model','excluded')
    if flag(a,'excluded'):
        required(a,'exclusion_basis');return False
    fw=c['framework']
    if fw in ('IFRS','AASB'):
        if a['model']!='power_returns_link':raise ReviewRequired('IFRS10/AASB10 control model required')
        return flag(a,'substantive_power') and flag(a,'variable_returns') and flag(a,'power_returns_link')
    if fw=='US_GAAP':
        required(a,'vie_scope_memo')
        if a['model']=='VIE':return flag(a,'power_significant_activities') and flag(a,'potentially_significant_losses_benefits')
        if a['model']=='voting':
            return flag(a,'controlling_financial_interest') and not flag(a,'substantive_participating_rights_preclude')
        raise ReviewRequired('ASC810 VIE/voting model required')
    if a['model']!='section9':raise ReviewRequired('FRS102 Section9 control model required')
    return flag(a,'power_to_govern_policies')

def signed_entry(dr,cr,value):
    n=cash(value)
    return journal(('Dr',dr,n),('Cr',cr,n)) if n>=0 else journal(('Dr',cr,-n),('Cr',dr,-n))

def assess(c,claims):
    required(c,'entities','intercompany','investments','profit_eliminations','nci','ownership_changes','statement_mapping','specialist_items')
    if c['specialist_items']:raise ReviewRequired('Unresolved group specialist schedules: '+', '.join(c['specialist_items']))
    ids=[e['id'] for e in c['entities']]
    if not ids or len(ids)!=len(set(ids)):raise ReviewRequired('Unique group entity IDs required')
    for e in c['entities']:flag(e,'parent')
    if sum(e['parent'] for e in c['entities'])!=1:raise ReviewRequired('Exactly one group reporting parent required')
    totals={};source={};entries=[];perimeter=[];translations=[]
    def post(lines):
        balance(lines);entries.append(lines)
        for l in lines:totals[l['account']]=cash(totals.get(l['account'],Decimal(0))+(l['amount'] if l['side']=='Dr' else -l['amount']))
    for e in c['entities']:
        required(e,'id','parent','balances','policy_alignment','date_alignment','control')
        if 'translation' not in e:raise ReviewRequired('Translation decision must be explicit, including null for common currency')
        if not (flag(e,'policy_alignment') and flag(e,'date_alignment')):raise ReviewRequired('Align policies and dates before aggregation')
        if not e['parent'] and not control(c,e['control']):continue
        balances={k:cash(v) for k,v in e['balances'].items()}
        if sum(balances.values())!=0:raise ReviewRequired('Entity trial balance must balance: '+e['id'])
        tr=e['translation']
        if tr:
            required(tr,'account_rates','rate_evidence','cta_account')
            if set(tr['account_rates'])!=set(balances):raise ReviewRequired('Rate mapping must cover each TB account')
            translated={k:cash(v*nonnegative(tr['account_rates'][k])) for k,v in balances.items()}
            if any(dec(v)<=0 for v in tr['account_rates'].values()):raise ReviewRequired('FX rates must be positive')
            cta=-sum(translated.values());translated[tr['cta_account']]=cash(translated.get(tr['cta_account'],0)+cta)
            balances=translated;translations.append({'entity':e['id'],'cta':cta})
        source[e['id']]=balances;perimeter.append(e['id'])
        for account,value in balances.items():totals[account]=cash(totals.get(account,0)+value)
    if not perimeter:raise ReviewRequired('No consolidation perimeter')
    used={}
    for pair in c['intercompany']:
        required(pair,'seller','buyer','debit_account','credit_account','amount','matched','family','source_id')
        if pair['seller'] not in source or pair['buyer'] not in source or pair['seller']==pair['buyer']:
            raise ReviewRequired('Intercompany pair outside perimeter or same-entity')
        if not flag(pair,'matched'):raise ReviewRequired('Unreconciled intercompany difference; no plug elimination')
        n=cash(nonnegative(pair['amount']));dracc=pair['debit_account'];cracc=pair['credit_account']
        # Source credit balance is eliminated with a debit; source debit with a credit.
        for eid,acc,sign in [(pair['seller'],dracc,-1),(pair['buyer'],cracc,1)]:
            key=(eid,acc);used[key]=used.get(key,Decimal(0))+n
            if source[eid].get(acc,Decimal(0))*sign<used[key]:raise ReviewRequired('Elimination exceeds entity/account source population')
        post(journal(('Dr',dracc,n),('Cr',cracc,n)))
    investment_used={}
    if len({x['subsidiary'] for x in c['investments']})!=len(c['investments']):raise ReviewRequired('Duplicate subsidiary investment schedule')
    for inv in c['investments']:
        required(inv,'subsidiary','parent_entity','investment_account','investment','acquisition_equity','fair_value_adjustments','goodwill','nci_at_acquisition','acquisition_memo')
        if inv['subsidiary'] not in source:raise ReviewRequired('Investment elimination outside perimeter')
        key=(inv['parent_entity'],inv['investment_account'])
        investment_used[key]=investment_used.get(key,Decimal(0))+nonnegative(inv['investment'])
        if inv['parent_entity'] not in source or source[inv['parent_entity']].get(inv['investment_account'],0)<investment_used[key]:raise ReviewRequired('Investment elimination exceeds parent source balance')
        rows=[('Cr',inv['investment_account'],nonnegative(inv['investment']))]
        for acc,v in inv['acquisition_equity'].items():rows.append(('Dr',acc,nonnegative(v)))
        for acc,v in inv['fair_value_adjustments'].items():
            n=dec(v);rows.append(('Dr' if n>=0 else 'Cr',acc,abs(n)))
        rows.extend([('Dr','goodwill',nonnegative(inv['goodwill'])),('Cr','noncontrolling interest',nonnegative(inv['nci_at_acquisition']))])
        post(journal(*rows))
    for (eid,acc),value in investment_used.items():
        if source[eid][acc]!=cash(value):raise ReviewRequired('Investment elimination allocation must reconcile to full source account')
    subs={e['id'] for e in c['entities'] if not e['parent'] and e['id'] in source}
    if {x['subsidiary'] for x in c['investments']}!=subs:raise ReviewRequired('Investment/equity opening schedule must cover every subsidiary')
    for p in c['profit_eliminations']:
        required(p,'type','seller','buyer','profit','remaining_fraction','asset_account','source_memo')
        if p['seller'] not in source or p['buyer'] not in source:raise ReviewRequired('Unrealized profit outside group')
        n=cash(nonnegative(p['profit'])*fraction(p['remaining_fraction']))
        post(journal(('Dr','cost of sales / disposal gain',n),('Cr',p['asset_account'],n)))
        if p['type']=='depreciable_asset':
            required(p,'excess_depreciation');correction=nonnegative(p['excess_depreciation'])
            if correction>n:raise ReviewRequired('Excess depreciation exceeds unrealized gain')
            post(journal(('Dr',p['asset_account'],correction),('Cr','depreciation expense',correction)))
        elif p['type']!='inventory':raise ReviewRequired('Unsupported intragroup profit family')
        required(p,'tax_effect_journal','tax_memo')
        if p['tax_effect_journal']:post(p['tax_effect_journal'])
    if len({x['subsidiary'] for x in c['nci']})!=len(c['nci']):raise ReviewRequired('Duplicate NCI schedule')
    ncirows=[]
    for n in c['nci']:
        required(n,'subsidiary','ownership','opening','adjusted_profit','adjusted_oci','dividends','other','allocation_memo')
        if n['subsidiary'] not in subs:raise ReviewRequired('NCI schedule outside subsidiary perimeter')
        ratio=1-fraction(n['ownership']);profit=cash(dec(n['adjusted_profit'])*ratio);oci=cash(dec(n['adjusted_oci'])*ratio);dividend=cash(nonnegative(n['dividends'])*ratio)
        closing=cash(dec(n['opening'])+profit+oci-dividend+dec(n['other']))
        if ratio==0 and closing!=0:raise ReviewRequired('Wholly owned entity cannot retain unexplained nonzero NCI')
        # Attribution is equity presentation, not additional group expense.
        ncirows.append({'subsidiary':n['subsidiary'],'profit':profit,'oci':oci,'dividends':dividend,'closing':closing})
    if {x['subsidiary'] for x in c['nci']}!=subs:raise ReviewRequired('NCI bridge required for all subsidiaries including wholly owned zero-NCI')
    for event in c['ownership_changes']:
        required(event,'control_retained','memo')
        if flag(event,'control_retained'):
            required(event,'cash_paid','nci_carrying_acquired')
            paid=nonnegative(event['cash_paid']);acquired=nonnegative(event['nci_carrying_acquired'])
            lines=[('Dr','noncontrolling interest',acquired),('Cr','cash',paid)]
            delta=paid-acquired;lines.append(('Dr' if delta>=0 else 'Cr','parent equity',abs(delta)));post(journal(*lines))
        else:
            required(event,'derecognition_journal','gain_memo','oci_recycling_memo','retained_interest_fv_evidence')
            post(event['derecognition_journal'])
    required(c,'nci_attribution_account')
    expected_nci=-sum(x['closing'] for x in ncirows)
    delta=cash(expected_nci-totals.get('noncontrolling interest',Decimal(0)))
    if delta:post(signed_entry('noncontrolling interest',c['nci_attribution_account'],delta))
    if sum(totals.values())!=0:raise ReviewRequired('Consolidated trial balance does not balance')
    mapping=c['statement_mapping']
    if not set(totals)<=set(mapping):raise ReviewRequired('Statement mapping must cover every consolidated account')
    for acc in mapping:totals.setdefault(acc,Decimal(0))
    statements={}
    for acc,val in totals.items():
        if mapping[acc] not in ('assets','liabilities','equity','income','expenses'):raise ReviewRequired('Invalid statement classification')
        statements[mapping[acc]]=cash(statements.get(mapping[acc],0)+val)
    required(c,'cash_flow_bridge','disclosure_tieout','equity_bridge','cta_bridge')
    eq=c['equity_bridge'];required(eq,'opening','profit','oci','owner_transactions','other','closing','memo')
    profit=-statements.get('income',Decimal(0))-statements.get('expenses',Decimal(0))
    if cash(eq['profit'])!=cash(profit):raise ReviewRequired('Equity profit does not tie to group income statement')
    if cash(sum(dec(eq[k]) for k in ('opening','profit','oci','owner_transactions','other')))!=cash(eq['closing']):raise ReviewRequired('Opening-to-closing group equity bridge fails')
    if cash(eq['closing'])!=cash(-statements.get('equity',Decimal(0))+profit):raise ReviewRequired('Closing equity does not tie to TB plus unclosed results')
    ct=c['cta_bridge'];required(ct,'opening','translation','disposals','other','closing','cta_accounts','memo')
    if cash(dec(ct['opening'])+dec(ct['translation'])+dec(ct['disposals'])+dec(ct['other']))!=cash(ct['closing']):raise ReviewRequired('CTA bridge fails')
    if cash(sum(totals.get(k,Decimal(0)) for k in ct['cta_accounts']))!=cash(ct['closing']):raise ReviewRequired('CTA does not tie to consolidated TB')
    cf=c['cash_flow_bridge'];required(cf,'opening_cash','operating','investing','financing','fx','closing_cash','cash_accounts','memo')
    if cash(dec(cf['opening_cash'])+dec(cf['operating'])+dec(cf['investing'])+dec(cf['financing'])+dec(cf['fx']))!=cash(cf['closing_cash']):raise ReviewRequired('Cash-flow bridge does not reconcile')
    if cash(sum(totals.get(k,Decimal(0)) for k in cf['cash_accounts']))!=cash(cf['closing_cash']):raise ReviewRequired('Cash flow closing cash does not tie to consolidated TB')
    return {'conclusion':f'Consolidated {len(perimeter)} entities; balanced group trial balance after {len(entries)} consolidation entries.',
      'method':'Framework control perimeter; aligned/translated source TBs; documented eliminations; NCI and cash-flow bridges',
      'calculations':{'perimeter':perimeter,'consolidated_balances':totals,'statements':statements,'translations':translations,'nci':ncirows,'cash_flow':cf,'equity':eq,'cta':ct},
      'journal_entry_implications':entries,'judgments':[c['judgment_memo'],*[e['control']['control_memo'] for e in c['entities']]],
      'uncertainties':['Acquisition fair values, historical FX, rights-specific NCI allocations, loss-of-control OCI and tax effects are independently reviewed specialist inputs.'],
      'open_items':[],'disclosures_impacted':['Group composition and significant control judgments','NCI interests, restrictions and summarized financial information','Ownership changes and acquisitions/disposals','Foreign operation translation reserves','Associates/joint arrangements and unconsolidated structured entities when applicable','Reconcile consolidated statements, equity and cash-flow disclosures with applicable tier relief']}
