"""Approved supplemental decision requirements; no autonomous tax-law conclusions."""
from financing_accounting import *

AREAS={'current_tax','tax_bases','differences','losses_credits','recoverability','uncertainty','rates','acquisitions','share_based','outside_basis','allocation','etr','disclosures','transition','offsetting','scope'}

def assess(c,claims):
    rs=begin(c,'jurisdictions');entries=imports(c,{'business-combinations','share-based-compensation','accounting-changes','provisions-contingencies'});out=[];gross=[]
    checks=rows(c['tax_area_reviews'],False)
    if {r['id'] for r in checks}!=AREAS:raise ReviewRequired('All sixteen supplemental tax decision areas need applicability and evidence disposition')
    for r in checks:
        policy(c,r);reviewed(r,c,'scope_memo','exception_memo');enum(r,'disposition',{'applicable','not_applicable','specialist_resolved'})
    total_tax=profit=ZERO;opening_stocks={};closing_stocks={}
    for r in rs:
        reviewed(r,c,'tax_law_memo','return_to_provision_memo','rate_evidence','filing_scope_memo','uncertainty_memo','allocation_memo')
        basis=enum(r,'difference_model',{'temporary_difference','timing_difference_plus'})
        if (basis=='timing_difference_plus')!=(c['framework']=='UK_GAAP'):raise ReviewRequired('UK timing-difference-plus cannot be substituted by IAS12 tax bases')
        legal_rate=enum(r,'rate_status',{'enacted','substantively_enacted'})
        if c['framework']=='US_GAAP' and legal_rate!='enacted':raise ReviewRequired('US tax measurement requires enacted rates')
        rate=fraction(r['current_rate']);pretax=dec(r['pretax_profit']);permanent=dec(r['permanent_adjustment']);timing=dec(r['taxable_adjustment'])
        taxable=pretax+permanent+timing;agree(r['taxable_income'],taxable,'Source taxable income bridge')
        credit=nonnegative(r['credits_used']);current=cash(max(taxable,ZERO)*rate-credit+dec(r['prior_trueup']))
        if credit>max(taxable,ZERO)*rate:raise ReviewRequired('Refundable/negative current tax requires supported specialist method')
        agree(r['expected_current'],current,'Current tax');payable=dec(r['opening_current'])+current-nonnegative(r['tax_paid']);agree(r['closing_current'],payable,'Current tax rollforward')
        if payable<0:raise ReviewRequired('Current tax receivable/refundable position requires a separately supported specialist method')
        opening_stocks['Current tax payable']=opening_stocks.get('Current tax payable',ZERO)-dec(r['opening_current']);closing_stocks['Current tax payable']=closing_stocks.get('Current tax payable',ZERO)-payable
        entries += [signed_entry('Current tax payable','Current tax expense',current,False),journal(('Dr','Current tax payable',r['tax_paid']),('Cr','Cash',r['tax_paid']))]
        dta=dtl=va=deferred_pl=ZERO;differences=rows(r['differences']);inventory(r,'difference_inventory',differences)
        for d in differences:
            reviewed(d,c,'basis_evidence','reversal_memo','recovery_memo','exception_memo')
            kind=enum(d,'kind',{'taxable','deductible'});allocation=enum(d,'allocation',{'profit','oci','equity','acquisition'})
            source=enum(d,'source',{'asset','liability','loss','credit','outside_basis'})
            if source in {'loss','credit'} and kind!='deductible':raise ReviewRequired('Unused loss or credit cannot create a deferred tax liability')
            if basis=='temporary_difference' and source in {'asset','liability'}:
                raw=dec(d['carrying'])-dec(d['tax_base']) if source=='asset' else dec(d['tax_base'])-dec(d['carrying'])
                if (raw>0 and kind!='taxable') or (raw<0 and kind!='deductible'):raise ReviewRequired('Asset/liability tax-base sign classification failed')
                amount=abs(raw);agree(d['difference'],amount,'Temporary difference source')
            else:amount=nonnegative(d['difference'])
            drate=fraction(d['reversal_rate']);drstatus=enum(d,'rate_status',{'enacted','substantively_enacted'})
            if c['framework']=='US_GAAP' and drstatus!='enacted':raise ReviewRequired('US reversal rates require enactment')
            measured=cash(amount*drate) if source!='credit' else cash(amount)
            exception=flag(d,'recognition_exception');recoverable=nonnegative(d['recoverable_tax_amount'])
            if exception and recoverable:raise ReviewRequired('Recognition exception conflicts with claimed recognized recoverability')
            if recoverable>measured:raise ReviewRequired('DTA recovery exceeds gross measured asset')
            opening=nonnegative(d['opening_gross']);opening_va=nonnegative(d['opening_allowance'])
            if opening_va>opening or (opening_va and c['framework']!='US_GAAP'):raise ReviewRequired('Invalid opening valuation allowance')
            if kind=='taxable':
                if opening_va or recoverable:raise ReviewRequired('DTL cannot use DTA recovery or valuation allowance')
                closing=ZERO if exception else measured;allowance=ZERO;account='Deferred tax liability';asset=False;dtl+=closing
            else:
                closing=ZERO if exception else (measured if c['framework']=='US_GAAP' else recoverable)
                allowance=closing-recoverable if c['framework']=='US_GAAP' and not exception else ZERO
                account='Deferred tax asset';asset=True;dta+=closing;va+=allowance
            change=cash(closing-opening);allowance_change=cash(allowance-opening_va)
            offset={'profit':'Deferred tax expense','oci':'Tax OCI','equity':'Tax equity','acquisition':'Acquisition tax clearing'}[allocation]
            if allocation!='profit':
                h=handoff(c,d['allocation_handoff'],'Tax allocation specialist');required(h,'tax_movement');agree(h['tax_movement'],change-allowance_change if asset else change,'Component tax allocation')
            entries.append(signed_entry(account,offset,change,asset))
            if c['framework']=='US_GAAP' and kind=='deductible':entries.append(signed_entry('Deferred tax valuation allowance',offset,allowance_change,False))
            pl=(allowance_change-change) if asset else change
            if allocation=='profit':deferred_pl+=pl
            agree(d['expected_gross'],closing,'Deferred gross');agree(d['expected_allowance'],allowance,'Deferred valuation allowance')
            opening_stocks[account]=opening_stocks.get(account,ZERO)+opening*(1 if asset else -1);closing_stocks[account]=closing_stocks.get(account,ZERO)+closing*(1 if asset else -1)
            if asset:
                opening_stocks['Deferred tax valuation allowance']=opening_stocks.get('Deferred tax valuation allowance',ZERO)-opening_va;closing_stocks['Deferred tax valuation allowance']=closing_stocks.get('Deferred tax valuation allowance',ZERO)-allowance
        utp=r['uncertain_position'];reviewed(utp,c,'recognition_memo','measurement_memo','framework_memo','interest_penalty_memo')
        if utp.get('framework')!=c['framework']:raise ReviewRequired('Uncertain tax position framework mismatch')
        utp_change=nonnegative(utp['closing'])-nonnegative(utp['opening'])+nonnegative(utp['settled'])
        opening_stocks['Uncertain tax liability']=opening_stocks.get('Uncertain tax liability',ZERO)-dec(utp['opening']);closing_stocks['Uncertain tax liability']=closing_stocks.get('Uncertain tax liability',ZERO)-dec(utp['closing'])
        entries += [signed_entry('Uncertain tax liability','Current tax expense',utp_change,False),journal(('Dr','Uncertain tax liability',utp['settled']),('Cr','Cash',utp['settled']))]
        tax=current+deferred_pl+utp_change;benchmark=cash(pretax*rate)
        adjustments=rows(r['etr_adjustments']);inventory(r,'etr_inventory',adjustments)
        for e in adjustments:reviewed(e,c,'cause_memo')
        agree(benchmark+sum((dec(e['amount']) for e in adjustments),ZERO),tax,'Effective tax rate reconciliation')
        offset=flag(r,'offset_permitted')
        if offset and not all(flag(r,k) for k in ['same_tax_authority','same_tax_entity','enforceable_offset_right','settlement_conditions_met']):raise ReviewRequired('Tax offset lacks evidenced framework conditions')
        agree(r['closing_dta'],dta,'DTA rollforward');agree(r['closing_dtl'],dtl,'DTL rollforward');agree(r['closing_allowance'],va,'Allowance rollforward')
        gross.append(abs(taxable));profit+=pretax;total_tax+=tax
        out.append(dict(current=current,deferred_profit=deferred_pl,uncertainty_charge=utp_change,total_tax_expense=tax,current_payable=payable,dta_gross=dta,valuation_allowance=va,dta_net=dta-va,dtl=dtl,net_deferred_display=(dtl-dta+va) if offset else None,etr=None if pretax==0 else tax/pretax))
    population(c,rs,gross);agree(c['statement_tax_expense'],total_tax,'Tax P&L/statement');agree(c['statement_pretax'],profit,'Tax pretax/statement')
    stocks(c,{k:(v,closing_stocks.get(k,ZERO)) for k,v in opening_stocks.items()})
    return complete(c,'Current/deferred tax, uncertainty and ETR workpapers reconciled',dict(jurisdictions=out,total_tax_expense=total_tax,pretax=profit,etr=None if profit==0 else total_tax/profit),entries,
        ['Approved supplemental decision requirements remain model-derived and subject to authority audit',
         'Rates, bases, recoverability, uncertainty, exceptions, allocation and offset rights are evidenced tax-specialist inputs',
         'No tax-law determination, return filing, PillarTwo calculation or universal probability model is performed'])
