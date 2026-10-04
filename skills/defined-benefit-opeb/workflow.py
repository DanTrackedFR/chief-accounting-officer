"""Qualified actuarial stock-flow accounting; never an actuarial valuation."""
from final_batch_accounting import *
KEYS=('plans','plan_source','documents','document_inventory','imports','owner_links','owner_link_inventory','gl','gl_inventory','governance_method')
LIMITS=['Qualified actuarial and plan-source accounting workpaper, not an actuarial valuation or opinion.','Only the event-free IFRS deficit pension bridge creates journals. US, FRS 102 and AASB detailed accounting presentation require separately governed methods.','Surplus/asset ceiling, minimum funding, multi-employer, amendments, settlements, curtailments, foreign currency and other-long-term routes are excluded.']
OBL=('opening_obligation','service_cost','interest_cost','benefits_paid','actuarial_loss','closing_obligation')
ASSET=('opening_assets','asset_interest','contributions','benefits_paid','asset_remeasurement_gain','closing_assets')
def assess(c,claims):
    ps,d=start(c,'plans',True);original(c,'plan_source',ps);unique([p['plan_id'] for p in ps],'physical plan')
    if not ps:raise ReviewRequired('Actual plan population required')
    totals=dict(opening_deficit=ZERO,closing_deficit=ZERO,contributions=ZERO,service_cost=ZERO);entries=[];cash_flow=ZERO;expense=ZERO;oci=ZERO
    for p in ps:
        enum(p,'classification',{'defined_benefit_pension','other_postemployment'})
        terms=snapshot(c,d,p['terms_doc'],p['currency']);exact_fields(p,terms,['plan_id','classification','single_employer'],'Plan terms')
        if not flag(p,'single_employer'):raise ReviewRequired('Multi-employer accounting requires separate governed method')
        for k in ('amendment','settlement','curtailment','minimum_funding','asset_ceiling_issue','fx','contributions_already_expensed','assumption_selection_requested'):
            if flag(p,k):raise ReviewRequired('Unsupported specialist plan feature: '+k)
            if terms[k]!=p[k]:raise ReviewRequired('Plan feature omitted from tracker')
        census=snapshot(c,d,p['census_doc'],p['currency']);hr=snapshot(c,d,p['hr_doc'],p['currency'])
        inventory(census,'inventory',rows(census['employees'],False));inventory(hr,'inventory',rows(hr['employees'],False))
        if digest(census)!=digest(hr):raise ReviewRequired('Independent employee/census reconciliation failed')
        report=snapshot(c,d,p['report_doc'],p['currency']);custody=snapshot(c,d,p['assets_doc'],p['currency'])
        texts(report,'actuary','qualifications_memo','objectivity_memo','assumption_review_memo','signed_on','report_id','method','measurement_date')
        if report['measurement_date']!=c['reporting_period'] or not iso(c['reporting_period'])<=iso(report['signed_on'])<=iso(c['execution_date']):raise ReviewRequired('Actuarial report is stale or misdated')
        if report['period']!=[c['period_start'],c['reporting_period']] or report['entity']!=c['entity'] or report['plan_id']!=p['plan_id'] or report['framework']!=c['framework'] or report['currency']!=p['currency']:raise ReviewRequired('Actuarial report scope mismatch')
        if report['method']!={'IFRS':'IAS19_qualified','US_GAAP':'ASC715_qualified','UK_GAAP':'FRS102_28_qualified','AASB':'AASB119_qualified'}[c['framework']]:raise ReviewRequired('Wrong framework actuarial accounting method')
        if not isinstance(report['assumptions'],dict) or not report['assumptions'] or report['census_hash']!=digest(census):raise ReviewRequired('Qualified assumptions/census lineage absent')
        exact_fields(p,report,OBL+ASSET+('classification',),'Qualified actuarial rollforward')
        exact_fields(p,report,('amendment','settlement','curtailment','minimum_funding','asset_ceiling_issue','fx','assumption_selection_requested'),'Qualified report feature scope')
        exact_fields(custody,report,ASSET+('plan_id','currency','measurement_date'),'Custodian plan assets')
        for k in OBL+ASSET: nonnegative(p[k]) if k not in ('actuarial_loss','asset_remeasurement_gain') else dec(p[k])
        exact(p['closing_obligation'],dec(p['opening_obligation'])+dec(p['service_cost'])+dec(p['interest_cost'])-dec(p['benefits_paid'])+dec(p['actuarial_loss']),'Obligation rollforward')
        exact(p['closing_assets'],dec(p['opening_assets'])+dec(p['asset_interest'])+dec(p['contributions'])-dec(p['benefits_paid'])+dec(p['asset_remeasurement_gain']),'Asset rollforward')
        opening=dec(p['opening_obligation'])-dec(p['opening_assets']);closing=dec(p['closing_obligation'])-dec(p['closing_assets'])
        if min(opening,closing)<0:raise ReviewRequired('Surplus/asset-ceiling analysis requires separate method')
        exact(p['amount'],closing,'Plan source funded deficit')
        statement=snapshot(c,d,p['statement_doc'],p['currency']);exact_fields(statement,p,('plan_id','currency'),'Plan statement')
        exact(statement['net_liability'],closing,'Statement funded deficit');exact(statement['gl_net_liability'],closing,'GL funded deficit')
        paid=snapshot(c,d,p['contributions_doc'],p['currency']);exact(paid['contributions'],p['contributions'],'Independent cash contribution');exact_fields(paid,p,('plan_id','currency'),'Contribution source')
        for k,v in [('opening_deficit',opening),('closing_deficit',closing),('contributions',dec(p['contributions'])),('service_cost',dec(p['service_cost']))]:totals[k]+=v
        if c['requested_action']=='accounting':
            if c['framework']!='IFRS' or p['classification']!='defined_benefit_pension':raise ReviewRequired('Detailed US/UK/AASB or OPEB accounting method is not governed by the IFRS illustration')
            if c['period_start'][-5:]!='01-01' or c['reporting_period'][-5:]!='12-31' or c['period_start'][:4]!=c['reporting_period'][:4]:raise ReviewRequired('IFRS bridge is one annual calendar period only')
            rate=dec(report['assumptions']['qualified_opening_discount_rate'])
            exact(p['interest_cost'],dec(p['opening_obligation'])*rate,'Supplied opening obligation interest');exact(p['asset_interest'],dec(p['opening_assets'])*rate,'Supplied opening asset interest')
            e=dec(p['service_cost'])+dec(p['interest_cost'])-dec(p['asset_interest']);o=dec(p['actuarial_loss'])-dec(p['asset_remeasurement_gain']);con=dec(p['contributions'])
            exact(statement['pnl_expense'],e,'IFRS P&L');exact(statement['oci_loss'],o,'IFRS OCI');exact(closing,opening+e+o-con,'Funded status/journal bridge')
            entries += [signed_entry('Pension expense','DB net liability',e),signed_entry('Pension OCI','DB net liability',o),signed_entry('Cash','DB net liability',-con)]
            expense+=e;oci+=o;cash_flow+=con
    unique([p['currency'] for p in ps] if len(ps)==1 else [p['plan_id'] for p in ps],'plan source')
    if len({p['currency'] for p in ps})!=1:raise ReviewRequired('Unlike plan currencies cannot be aggregated')
    if entries:
        stocks(c,{'DB net liability':(-totals['opening_deficit'],-totals['closing_deficit'])})
        by={r['id']:r for r in c['gl']};exact(by['Cash']['closing'],dec(by['Cash']['opening'])-cash_flow,'Cash funding/GL')
        for account,value in (('Pension expense',expense),('Pension OCI',oci)):
            exact(by[account]['opening'],0,'Annual statement account opening');exact(by[account]['closing'],value,'Annual statement account closing')
        totals.update(pnl_expense=expense,oci_loss=oci)
    review_release(c,KEYS)
    return finalize(c,'Qualified defined-benefit/OPEB accounting workpaper; no actuarial valuation',totals,LIMITS,entries=entries)
