"""Source-population inclusion windows, bounded to a single reporting Case.

No prorating, comparative execution, disposal accounting or inferred dates.
Amounts are selected from disjoint, complete supplied dated activity windows.
"""
from datetime import date
from decimal import Decimal
from .runtime import number


def validate_activity(source):
    selection=source.get('activity_selection')
    acquisition=any(r.get('semantic')=='acquisition_goodwill' for r in source.get('qualified_owner_results',[]))
    if selection is None:
        if acquisition:raise ValueError('Acquisition source requires a supported activity-selection population')
        return
    if set(selection)!={'source_start','source_end','effective_date','records','inventory','included_ids','included_profit','revenue_account','expense_account','evidence','full_year_balances','equity_account'} or not selection['evidence']:
        raise ValueError('Complete sourced activity-selection contract required')
    start,end,effective=[date.fromisoformat(selection[k]) for k in ('source_start','source_end','effective_date')]
    if start>=end or not start<=effective<=end or selection['source_end']!=source['reporting_period']:
        raise ValueError('Invalid source or effective-date population')
    governed_activity_interval(source)
    records=selection['records'];ids=[r['id'] for r in records]
    if len(ids)!=len(set(ids)) or sorted(ids)!=sorted(selection['inventory']):raise ValueError('Dated activity population incomplete')
    if source['translation']['operation_id']!=source['entity']:raise ValueError('Foreign operation entity differs from activity source')
    included=[];profit=Decimal(0);revenue=Decimal(0);expense=Decimal(0);intervals=[]
    for row in records:
        if set(row)!={'id','entity','currency','start','end','revenue','expense'}:raise ValueError('Activity record dimensions required')
        if row['entity']!=source['entity'] or row['currency']!=source['currency']['functional']:
            raise ValueError('Activity entity/currency contamination')
        rs,re=date.fromisoformat(row['start']),date.fromisoformat(row['end'])
        if not start<=rs<=re<=end or rs<effective<=re:raise ValueError('Unsupported activity split across effective date')
        intervals.append((rs,re))
        if rs>=effective:
            included.append(row['id']);revenue+=number(row['revenue']);expense+=number(row['expense']);profit+=number(row['revenue'])-number(row['expense'])
    intervals.sort()
    if not intervals or intervals[0][0]!=start or intervals[-1][1]!=end or any((b[0]-a[1]).days!=1 for a,b in zip(intervals,intervals[1:])):
        raise ValueError('Activity source periods have a gap or overlap')
    if sorted(included)!=sorted(selection['included_ids']) or number(selection['included_profit'])!=profit:
        raise ValueError('Pre-effective activity included or unsupported post-effective result')
    if number(source['translation']['profit'])!=profit:raise ValueError('Translation uses incorrect included-period profit')
    balances={r['id']:number(r['balance']) for r in source['translation']['tb']}
    if balances.get(selection['revenue_account'])!=-revenue or balances.get(selection['expense_account'])!=expense:
        raise ValueError('Included revenue/expense source population differs from translation')

    full={k:number(v) for k,v in selection['full_year_balances'].items()}
    total_revenue=sum((number(r['revenue']) for r in records),Decimal(0))
    total_expense=sum((number(r['expense']) for r in records),Decimal(0))
    if sum(full.values(),Decimal(0))!=0 or full.get(selection['revenue_account'])!=-total_revenue or full.get(selection['expense_account'])!=total_expense:
        raise ValueError('Full-year legal-entity TB differs from complete activity population')
    for account,value in full.items():
        if account in (selection['revenue_account'],selection['expense_account'],selection['equity_account']):continue
        if balances.get(account)!=value:raise ValueError('Legal-entity closing balance differs from foreign-operation source')
    pre_profit=total_revenue-total_expense-profit
    if balances.get(selection['equity_account'])!=full.get(selection['equity_account'],Decimal(0))-pre_profit:
        raise ValueError('Acquisition equity does not preserve pre-acquisition retained profit')


def governed_activity_interval(source):
    """Normalize the existing qualified cutoff through generic Period dimensions.

    Native specialist acquisition-date receipts and full population checks still
    establish the cutoff's authority. No date inference or amount proration.
    """
    from .periods import FiscalCalendar,Period,PeriodRegistry,PeriodRelationship,EffectiveInterval
    from .scopes import Scope,ScopeRegistry
    selection=source['activity_selection']
    calendar=source.get('reporting_calendar') or 'UNSPECIFIED:'+source['entity']
    provenance=tuple(selection['evidence']) if isinstance(selection['evidence'],list) else (selection['evidence'],)
    whole=Period.create(calendar,selection['source_start'],selection['source_end'],date.fromisoformat(selection['source_end']).year,'BOUNDED-SOURCE',provenance=provenance)
    included=Period.create(calendar,selection['effective_date'],selection['source_end'],whole.fiscal_year,'BOUNDED-INCLUDED','PARTIAL_INCLUDED_PERIOD',provenance=provenance)
    periods=PeriodRegistry([FiscalCalendar(calendar,'Supplied bounded source calendar',1,1,provenance)],[whole,included],[PeriodRelationship(whole.period_id,included.period_id,'PARTIAL_INCLUDED_PERIOD',provenance)])
    scopes=ScopeRegistry([Scope(source['entity'],'LEGAL_ENTITY',source['entity'],source['entity'],provenance=provenance)])
    interval=EffectiveInterval(source['entity'],'business-combinations',whole.period_id,included.period_id,'ACQUISITION',selection['effective_date'],provenance).validate(periods,scopes)
    from dataclasses import asdict
    return dict(period_registry=periods.record(),effective_interval=asdict(interval))
