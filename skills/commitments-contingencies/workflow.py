from reporting_accounting import *

def assess(c,claims):
    common(c,'register','disclosure','gl_recognized','handoffs','contract_inventory')
    register=rows(c['register']);inventory(c,'contract_inventory',register);specialist(c,'legal','Legal contingencies');specialist(c,'provisions','Provisions & Contingencies');specialist(c,'instruments','Financial Instruments')
    disclosure=rows(c['disclosure']);dmap={d['id']:d for d in disclosure}
    if set(dmap)!={r['id'] for r in register}:raise ReviewRequired('Complete commitment-to-disclosure disposition population required')
    entries=[];recognized=ZERO;exposure=ZERO;work=[];journalids=set();expected_accounts={};account_signs={}
    for r in register:
        reviewed(r,c,'contract_evidence','completeness_memo','legal_probability_memo','recognition_memo','measurement_memo');required(r,'kind','opening_commitment','new_commitment','fulfilled','cancelled','fx_commitment','closing_commitment','opening_recognized','charge','unwind','settled','fx_recognized','closing_recognized','gl_closing','route','disclose','source_journals','measurement_handoff','law_probability_supported')
        if r['kind'] not in ['purchase','capital','guarantee','letter_of_credit','litigation','claim','loss_contingency','gain_contingency']:raise ReviewRequired('Commitment contract type unsupported')
        if not flag(r,'law_probability_supported'):raise ReviewRequired('Probability/rights assessment requires qualified legal evidence')
        opening=nonnegative(r['opening_commitment']);add=nonnegative(r['new_commitment']);fulfilled=nonnegative(r['fulfilled']);cancel=nonnegative(r['cancelled']);fx=dec(r['fx_commitment']);close=opening+add-fulfilled-cancel+fx
        if close<0:raise ReviewRequired('Commitment fulfilment/cancellation exceeds contract population')
        agree(r['closing_commitment'],close,'Contract commitment rollforward');exposure+=close
        op=nonnegative(r['opening_recognized']);charge=dec(r['charge']);unwind=nonnegative(r['unwind']);paid=nonnegative(r['settled']);fxr=dec(r['fx_recognized']);rec=op+charge+unwind-paid+fxr
        if rec<0:raise ReviewRequired('Recognized obligation rollforward negative')
        agree(r['closing_recognized'],rec,'Recognition rollforward');agree(r['gl_closing'],rec,'Recognized GL')
        route=r['route']
        allowed={'purchase':['ordinary_commitment','disclosure_only','provision'],'capital':['ordinary_commitment','disclosure_only','provision'],'guarantee':['financial_guarantee','disclosure_only'],'letter_of_credit':['financial_guarantee','disclosure_only'],'litigation':['provision','disclosure_only'],'claim':['provision','disclosure_only'],'loss_contingency':['provision','disclosure_only'],'gain_contingency':['gain_unrecognized','realized_gain']}
        if route not in allowed[r['kind']]:raise ReviewRequired('Contract kind/recognition route mismatch')
        required(r,'recognized_account')
        if rec or op or r['source_journals']:
            account=r['recognized_account'];sign=route!='realized_gain'
            if account=='not_applicable' or account in account_signs and account_signs[account]!=sign:raise ReviewRequired('Recognized account/classification mapping unresolved')
            expected_accounts[account]=expected_accounts.get(account,ZERO)+rec-op;account_signs[account]=sign
        if route not in ['disclosure_only','ordinary_commitment','provision','financial_guarantee','gain_unrecognized','realized_gain']:raise ReviewRequired('Recognition versus disclosure route unresolved')
        if route in ['disclosure_only','ordinary_commitment','gain_unrecognized'] and (op or charge or unwind or paid or fxr or rec):raise ReviewRequired('Disclosure-only exposure cannot enter recognized liabilities/assets')
        if r['kind'] in ['guarantee','letter_of_credit']:
            if route not in ['financial_guarantee','disclosure_only']:raise ReviewRequired('Guarantee requires contract-specific instrument/insurance/obligation classification')
            specialist(c,r['measurement_handoff'],'Guarantee accounting and valuation',rec)
        if route in ['provision','realized_gain']:specialist(c,r['measurement_handoff'],'Provisions & Contingencies',rec)
        js=rows(r['source_journals']);combined=[]
        for j in js:
            reviewed(j,c,'source_case_id');required(j,'lines','account')
            if j['account']!=r['recognized_account']:raise ReviewRequired('Specialist journal recognized account conflicts with register')
            if j['id'] in journalids:raise ReviewRequired('Duplicate specialist journal imported')
            journalids.add(j['id']);balance(j['lines']);entries.append(j['lines']);combined.extend(j['lines'])
        if rec!=op and not js:raise ReviewRequired('Recognition change requires supported specialist source entries')
        if js:
            accounts={j['account'] for j in js}
            if len(accounts)!=1:raise ReviewRequired('Separate recognized liability/asset account bridge required')
            sign=route!='realized_gain';agree(line_delta(combined,next(iter(accounts)),credit=sign),rec-op,'Specialist source journals to recognized movement')
        d=dmap[r['id']];reviewed(d,c,'requirements_memo','exclusion_memo');required(d,'included','amount','recognized_amount')
        include=flag(d,'included')
        if include!=flag(r,'disclose'):raise ReviewRequired('Disclosure disposition differs from reviewed legal/accounting route')
        agree(d['amount'],close if include else 0,'Disclosed contractual exposure');agree(d['recognized_amount'],rec,'Note recognized balance');recognized+=rec
        work.append({'id':r['id'],'kind':r['kind'],'route':route,'contractual_exposure':close,'recognized':rec,'disclosed':include})
    for account,n in expected_accounts.items():agree(line_delta([l for j in entries for l in j],account,credit=account_signs[account]),n,'All imported journals recognized-account bridge')
    agree(c['gl_recognized'],recognized,'Register recognized total GL');population(c,register,[nonnegative(r['opening_commitment'])+nonnegative(r['new_commitment']) for r in register])
    return finish('Complete contracts/claims and distinct recognized/disclosed amounts reconcile.',{'register':work,'maximum_contractual_exposure':exposure,'recognized_balances':recognized},entries,
      ['Maximum guarantee/contract exposure is not its recognized carrying value.','Legal probability and guarantee/contingency measurement must come from resolved specialist evidence; no independent guarantee valuation engine exists here.'],
      ['Nature/terms, maturity/maximum exposure, recognized provisions, uncertainties/reimbursements, guarantee/security, gain contingencies and framework-specific exemptions.'])
