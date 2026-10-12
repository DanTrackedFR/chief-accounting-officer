"""Synthetic reviewed sources for actual production execution; identities are assertions only."""
from decimal import Decimal
from copy import deepcopy
from datetime import date,timedelta
from cases import base,finalize
from operational_cases import approved
from reporting_cases import pol

EDITIONS={'IFRS':'IAS23_2026','AASB':'AASB123_MAR2020','US_GAAP':'ASC835_20_2026','UK_GAAP':'FRS102_SEP2024_2026'}

def case(fw='IFRS',method='mixed'):
    c=base('borrowing-costs',fw);c.update(package='borrowing-costs',functional_currency='EUR',execution_date='2027-02-01',imports=[])
    c['applicability_review']['standard_versions']=[EDITIONS[fw]]
    c['accounting_policy']=pol(c,'policy',borrowing_costs='capitalize',expenditure_basis='carrying_cost' if fw=='UK_GAAP' else 'actual_cash',consistency_memo='Same capitalization policy for entire tangible construction class',interest_basis_memo='Executed actual/actual simple interest contracts; no issue fees')
    c['accounting_policy']['effective_standard']=EDITIONS[fw]
    c['controls']=dict(source_version='v1',as_of=c['reporting_period'],population_count=1,population_amount='200000',owner='synthetic construction owner',reviewer='synthetic complete population reviewer',complete=True,policy_version='v1',cutoff_memo='Bank payment and progress populations independently complete')
    c['disclosure_review']=approved('disclosure',checklist_version='v1',period_entity_memo='Framework selected policy, capitalized amount, capitalization rate and significant project judgments',complete=True)
    p=approved('plant',source_entity=c['entity'],source_framework=fw,source_period=[c['period_start'],c['reporting_period']],asset_type='tangible_construction',purpose='own_use',qualifying_asset=True,substantial_period=True,abandoned=False,shared_components=False,authorized_date='2025-12-01',activity_start='2026-01-01',ready_date=None,opening_expenditure='100000',opening_capitalized='0',actual_net_expenditure='100000',closing_expenditure='200000',asset_opening='100000',asset_closing='0',expected_capitalized='0',authorization_memo='Board-authorized separately identified plant',qualifying_asset_memo='Construction requires substantial time; asset not ready at purchase',readiness_memo='Not ready by annual cutoff',progress_memo='Certified ongoing active physical construction',expenditure_memo='Actual paid invoice distinct from budget')
    p['expenditures']=[approved('invoice',economic_id='invoice-001',date='2026-07-01',cash_date='2026-07-01',amount='100000',basis='cash_paid',project_id='plant',currency='EUR',payment_memo='Bank payment and capital invoice matched')];p['expenditure_inventory']=['invoice']
    p['timeline']=[approved('active',start='2026-01-01',end='2026-12-31',state='active',extended=False,necessary_delay=False,substantial_technical_activity=True,activity_memo='Physical development continuous',suspension_memo='No suspension')];p['timeline_inventory']=['active']
    c['projects']=[p];c['source_inventory']=['plant'];c['borrowings']=[]
    for role,principal,rate in ([('specific','50000','.06'),('general','500000','.08')] if method=='mixed' else [('specific','250000','.06')] if method=='specific' else [('general','500000','.08')]):
        interest=str(Decimal(principal)*Decimal(rate))
        b=approved(role,economic_id=role+'-loan',lender='Synthetic lender '+role,currency='EUR',source_entity=c['entity'],source_framework=fw,source_period=[c['period_start'],c['reporting_period']],role=role,project_id='plant' if role=='specific' else None,complex_features=False,tax_exempt=False,fees='0',fx_adjustment='0',opening_principal=principal,closing_principal=principal,events=[],event_inventory=[],contract_memo='Executed fixed plain domestic loan',yield_memo='Coupon equals eligible effective interest; no fees',population_memo='All legal loans independently searched',cashflow_memo='Accrual and lender cash-flow events reconciled',interest_source_total=interest,cashflow_interest_total=interest)
        b['segments']=[approved('annual',start='2026-01-01',end='2026-12-31',annual_rate=rate,effective_annual_rate=rate,day_basis='actual_actual',investment_income='0',actual_interest=interest,rate_memo='Executed annual simple actual/actual rate')];b['segment_inventory']=['annual'];c['borrowings'].append(b)
    c['borrowing_inventory']=[b['id'] for b in c['borrowings']]
    remeasure(c);capture_sources(c);return c

def remeasure(c):
    """Fixture oracle performs independent daily arithmetic, no production assess call."""
    p=c['projects'][0];opening=Decimal(p['opening_expenditure']);expenditure=opening;capital=Decimal(0);actual=Decimal(0)
    start=date.fromisoformat(c['period_start']);end=date.fromisoformat(c['reporting_period']);balances={b['id']:Decimal(b['opening_principal']) for b in c['borrowings']}
    loan_totals={b['id']:Decimal(0) for b in c['borrowings']};seg_totals={}
    general_interest=Decimal(0);general_weight=Decimal(0)
    for b in c['borrowings']:
        if b['role']!='general':continue
        balance=Decimal(b['opening_principal'])
        for offset in range((end-start).days+1):
            d=start+timedelta(days=offset)
            balance+=sum((Decimal(e['amount'])*(1 if e['kind']=='draw' else -1) for e in b['events'] if e['date']==d.isoformat()),Decimal(0))
            s=next(s for s in b['segments'] if s['start']<=d.isoformat()<=s['end'])
            basis=Decimal(360 if s['day_basis']=='actual_360' else 365)
            general_interest+=balance*Decimal(s['annual_rate'])/basis;general_weight+=balance/Decimal(365)
    general_rate=general_interest/general_weight if general_weight else Decimal(0)
    for offset in range((end-start).days+1):
        d=start+timedelta(days=offset)
        expenditure+=sum((Decimal(x['amount']) for x in p['expenditures'] if x['date']==d.isoformat()),Decimal(0))
        active=next(t['state'] for t in p['timeline'] if t['start']<=d.isoformat()<=t['end']) in {'active','temporary'}
        specific=[];general=[];incurred=Decimal(0)
        for b in c['borrowings']:
            for e in b['events']:
                if e['date']==d.isoformat():balances[b['id']]+=Decimal(e['amount'])*(1 if e['kind']=='draw' else -1)
            s=next(s for s in b['segments'] if s['start']<=d.isoformat()<=s['end'])
            divisor=Decimal(365 if s['day_basis'] in {'actual_actual','actual_365'} else 360)
            cost=balances[b['id']]*Decimal(s['annual_rate'])/divisor
            income=Decimal(s['investment_income'])/Decimal((date.fromisoformat(s['end'])-date.fromisoformat(s['start'])).days+1)
            loan_totals[b['id']]+=cost;seg_totals[(b['id'],s['id'])]=seg_totals.get((b['id'],s['id']),Decimal(0))+cost
            incurred+=cost;(specific if b['role']=='specific' else general).append((balances[b['id']],cost,income))
        actual+=incurred
        if active and expenditure>0 and c['accounting_policy']['borrowing_costs']=='capitalize':
            base=expenditure+(Decimal(p['opening_capitalized'])+capital if c['framework']=='UK_GAAP' else 0)
            specific_principal=sum((r[0] for r in specific),Decimal(0))
            residual=max(Decimal(0),base-specific_principal)
            general_principal=sum((r[0] for r in general),Decimal(0))
            general_cost=residual*general_rate/Decimal(365) if general_principal else Decimal(0)
            if c['framework']=='US_GAAP':
                specific_cost=sum((min(base,r[0])*r[1]/r[0] if r[0] else Decimal(0) for r in specific),Decimal(0))
            else:specific_cost=sum((r[1]-r[2] for r in specific),Decimal(0))
            capital+=specific_cost+general_cost
    rounding=lambda n:n.quantize(Decimal('.01'))
    for b in c['borrowings']:
        for s in b['segments']:s['actual_interest']=str(rounding(seg_totals[(b['id'],s['id'])]))
        b['closing_principal']=str(balances[b['id']]);b['interest_source_total']=b['cashflow_interest_total']=str(rounding(loan_totals[b['id']]))
    actual=rounding(actual);capital=min(actual,rounding(capital));net=sum((Decimal(x['amount']) for x in p['expenditures']),Decimal(0));prior=Decimal(p['opening_capitalized'])
    p.update(actual_net_expenditure=str(net),closing_expenditure=str(opening+net),asset_opening=str(opening+prior),asset_closing=str(opening+prior+net+capital),expected_capitalized=str(capital))
    c['financing_gl_interest']=str(actual);c['expected_expense']=str(actual-capital)
    c['controls']['population_amount']=str(opening+net)
    # Snapshot after source owners recognize original debt expense and paid asset cost.
    c['gl']=[approved('Construction asset',opening=str(opening+prior+net),closing=str(opening+prior+net+capital),statement=str(opening+prior+net+capital)),approved('Interest expense',opening=str(actual),closing=str(actual-capital),statement=str(actual-capital))];c['gl_inventory']=['Construction asset','Interest expense']
    return c

def ready(fw='IFRS',method='mixed',c=None):
    c=deepcopy(c) if c is not None else case(fw,method)
    c=finalize('borrowing-costs',c)
    from production import canonical_knowledge,PACKAGES
    claims,_=canonical_knowledge(PACKAGES['borrowing-costs'][1],c['framework'])
    c['knowledge_review']['applied_claim_ids']=[r['claim_id'] for r in claims]
    from production import case_fingerprint
    c['reviewer_signoff']['case_fingerprint']=case_fingerprint(c)
    return c


def capture_sources(c):
    c['original_source_snapshot']=approved('original-source-capture',capture_memo='Independently frozen original source records before calculation or reviewer certification',records=deepcopy({key:c[key] for key in ('projects','borrowings','gl','financing_gl_interest','functional_currency')}))
    return c
