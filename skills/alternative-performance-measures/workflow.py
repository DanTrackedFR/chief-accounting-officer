"""Controlled statement-to-APM lineage and jurisdictional review, no invented addbacks."""
from special_reporting import *

def assess(c,claims):
    rs=start(c,'adjustments',{'financial-statements','accounting-changes'})
    p=method(c,'apm_method','APM reconciliation and publication governance')
    texts(p,'label','definition','rationale','metric','units','jurisdictional_memo','prominence_memo','tax_nci_memo','recurrence_memo','mpm_memo')
    if any(flag(p,k) for k in ('invented_adjustments','compliance_certification_requested','per_share_requested','definition_changed')):raise ReviewRequired('Invented adjustments, certification, per-share and definition changes need separate governed method')
    for k in ('not_misleading_reviewed','prominence_reviewed','comparative_consistent','adjustment_population_complete','tax_nci_reviewed','publication_draft_reviewed'):
        if not flag(p,k):raise ReviewRequired('APM publication-control prerequisite unresolved: '+k)
    r=c['regulatory_method']
    authorities={'US':{'www.sec.gov','sec.gov'},'EU':{'www.esma.europa.eu','esma.europa.eu'},'UK':{'www.fca.org.uk','www.frc.org.uk'},'AU':{'www.asic.gov.au','asic.gov.au'}}
    jurisdiction=enum(c,'jurisdiction',set(authorities));checked_rule(c,r,authorities[jurisdiction])
    if r['issuer_type']!=p['issuer_type'] or r['regime']!=p['regime']:raise ReviewRequired('Actual issuer/regulatory regime mismatch')
    if jurisdiction=='US' and r['regime']!='SEC_RegG_Item10e_review':raise ReviewRequired('SEC APM regime cannot be replaced by ESMA/IFRS18')
    expected={'EU':'EU_APM_review','UK':'UK_APM_review','AU':'AU_APM_review'}
    if jurisdiction in expected and r['regime']!=expected[jurisdiction]:raise ReviewRequired('Jurisdictional APM rules are not interchangeable')
    modern=c['framework'] in {'IFRS','AASB'} and (iso(c['period_start'])>=iso('2027-01-01') or flag(p,'early_adoption'))
    if c['framework'] not in {'IFRS','AASB'} and flag(p,'early_adoption'):raise ReviewRequired('IFRS18 cannot be imported into US/UK accounting')
    if flag(p,'mpm_effective')!=modern:raise ReviewRequired('MPM effective period/adoption mismatch')
    if modern and (not flag(p,'mpm_scope_reviewed') or (flag(p,'mpm_in_scope') and not flag(p,'mpm_disclosures_complete'))):raise ReviewRequired('Separate effective MPM scope/disclosure review incomplete')
    if not modern and flag(p,'mpm_in_scope'):raise ReviewRequired('Do not backdate IFRS18 MPM scope to non-early 2026')
    statements=rows(c['statements'],False);inventory(c,'statement_inventory',statements)
    if len(statements)!=2 or {s['id'] for s in statements}!={'current','prior'}:raise ReviewRequired('Exactly current and comparative controlled sources required')
    values={}
    for s in statements:
        if s['metric']!=p['metric'] or s['units']!=p['units']:raise ReviewRequired('GAAP subtotal label/units mismatch')
        values[s['id']]=typed_statement(c,s,s['id']=='current')
    comparable_spans(next(s for s in statements if s['id']=='current')['source_period'],next(s for s in statements if s['id']=='prior')['source_period'])
    sources=rows(c['adjustment_journals']);inventory(c,'journal_inventory',sources);by={s['id']:s for s in sources};used=set();totals={k:ZERO for k in values};tax={k:ZERO for k in values};nci={k:ZERO for k in values};definitions={k:{} for k in values}
    for a in rs:
        period=enum(a,'period',set(values));texts(a,'label','definition_key','rationale','tax_nci_memo','classification_memo')
        if a['source_period']!=next(s for s in statements if s['id']==period)['source_period']:raise ReviewRequired('Adjustment/GAAP period mismatch')
        if flag(a,'recurring') and flag(a,'described_nonrecurring'):raise ReviewRequired('Recurring adjustment mischaracterized as nonrecurring')
        if not flag(a,'in_gaap_subtotal') or not flag(a,'regulatory_treatment_reviewed'):raise ReviewRequired('Unsupported adjustment eligibility')
        ids=a['journal_ids']
        if not isinstance(ids,list) or not ids or len(ids)!=len(set(ids)):raise ReviewRequired('Adjustment journal population incomplete')
        amount=ZERO
        for id in ids:
            if id not in by or id in used:raise ReviewRequired('Missing or double-counted adjustment journal')
            j=by[id];approval(j,c);texts(j,'expense_account','source_memo')
            if j['period']!=period or j['source_period']!=a['source_period']:raise ReviewRequired('Adjustment journal period mismatch')
            parent=next(s for s in statements if s['id']==period)
            matching=[l for l in parent['lines'] if l['account']==j['expense_account']]
            if len(matching)!=1 or id not in matching[0]['journal_ids']:raise ReviewRequired('Adjustment journal not in actual GAAP subtotal ledger population')
            population_journals=[z for z in sources if z['id'] in matching[0]['journal_ids']]
            if {z['id'] for z in population_journals}!=set(matching[0]['journal_ids']):raise ReviewRequired('GAAP expense journal source union incomplete')
            full_amount=sum((dec(z['included_expense']) for z in population_journals),ZERO)
            exact(matching[0]['gl_amount'],full_amount,'GAAP ledger expense/journal source population')
            if not matching[0]['credit_nature']:raise ReviewRequired('Expense addback must reduce the original profit subtotal')
            balance(j['lines']);expense=sum((dec(l['amount'])*(1 if l['side']=='Dr' else -1) for l in j['lines'] if l['account']==j['expense_account']),ZERO)
            exact(j['included_expense'],expense,'Actual expense journal lineage');amount+=expense;used.add(id)
        exact(a['amount'],amount,'Source journal APM addback')
        totals[period]+=amount;tax[period]+=dec(a['tax_effect']);nci[period]+=dec(a['nci_effect']);key=a['definition_key']
        if key in definitions[period]:raise ReviewRequired('Duplicate adjustment definition in period')
        definitions[period][key]=(a['label'],flag(a,'recurring'),flag(a,'described_nonrecurring'))
    if used!=set(by):raise ReviewRequired('Adjustment journal source union incomplete')
    if definitions['current']!=definitions['prior']:raise ReviewRequired('Comparative adjustment definitions are inconsistent')
    population(c,rs,[abs(dec(a['amount'])) for a in rs])
    out={}
    for period,gaap in values.items():
        pub=c['publication'][period];approval(pub,c)
        if pub['label']!=p['label'] or pub['definition']!=p['definition'] or pub['units']!=p['units']:raise ReviewRequired('Published APM dictionary differs across communications/periods')
        value=gaap+totals[period]
        exact(pub['gaap_amount'],gaap,'Published GAAP subtotal');exact(pub['adjusted_amount'],value,'Published APM reconciliation')
        exact(pub['tax_effect'],tax[period],'Published tax effect');exact(pub['nci_effect'],nci[period],'Published NCI effect')
        out[period]=dict(gaap_subtotal=gaap,adjustments=totals[period],adjusted_measure=value,tax_effect=tax[period],nci_effect=nci[period])
    return no_posting(c,'Bounded APM reconciliation and publication-review workpaper reconciled',dict(measures=out,mpm_scope=flag(p,'mpm_in_scope')),['Management-defined labels and adjustments remain actual independently reviewed inputs; GAAP recognition stays with accounting owners'],['This is accounting governance support, not regulatory clearance. Actual issuer/jurisdiction rules and separate effective IFRS18/AASB18 MPM disclosure obligations require current qualified review; no adjustment is invented or posted.'])
