"""Evidence-dependent methods reuse the established execution/control boundary."""
from reporting_accounting import *
from datetime import date
import json

def same_result(a,b):
    # The existing public/CLI serializer represents Decimal amounts as strings.
    # Canonical JSON comparison preserves exact completed-result bytes/keys and
    # boolean types while permitting their documented JSON round trip.
    return json.dumps(a,sort_keys=True,default=str)==json.dumps(b,sort_keys=True,default=str)

def begin(c,key):
    common(c,key,'accounting_policy','gl','imports')
    texts(c,'preparer','entity','jurisdiction','case_id')
    if iso(c['reporting_period']).year>=9999:raise ReviewRequired('Unsupported date arithmetic range')
    policy(c,c['accounting_policy'])
    if c['entity_type']!='for_profit' or c['applicability_review']['exceptions']:
        raise ReviewRequired('Unresolved entity/period overlay requires specialist method')
    rs=rows(c[key]);inventory(c,'source_inventory',rs)
    for r in rs:
        approval(r,c)
        if r.get('source_entity')!=c['entity'] or r.get('source_framework')!=c['framework'] or r.get('source_period')!=[c['period_start'],c['reporting_period']]:
            raise ReviewRequired('Source entity/framework/period mismatch')
    return rs

def enum(r,key,values):
    required(r,key)
    if not isinstance(r[key],str) or r[key] not in values:raise ReviewRequired('Unsupported controlled accounting route: '+key)
    return r[key]

def signed_entry(account,offset,change,asset=True):
    change=cash(change)
    side='Dr' if (change>=0)==asset else 'Cr'
    return journal((side,account,abs(change)),('Cr' if side=='Dr' else 'Dr',offset,abs(change)))

def imports(c,allowed):
    """Actual completed downstream results, exact-once; never accept a memo as a skill result."""
    from production import execute,case_fingerprint
    output=[];seen=set()
    for r in rows(c['imports']):
        approval(r,c);required(r,'package','case','result')
        if r['package'] not in allowed:raise ReviewRequired('Unsupported imported accounting skill')
        source=r['case'];supplied=r['result']
        if source.get('entity')!=c['entity'] or source.get('framework')!=c['framework'] or source.get('period_start')!=c['period_start'] or source.get('reporting_period')!=c['reporting_period']:
            raise ReviewRequired('Imported entity/framework/period mismatch')
        fresh=execute(r['package'],source)
        if fresh['status']!='complete' or not same_result(supplied,fresh) or supplied.get('case_fingerprint')!=case_fingerprint(source):
            raise ReviewRequired('Imported result must be current, complete and unaltered')
        key=(r['package'],source['case_id'])
        if key in seen:raise ReviewRequired('Duplicate imported accounting conclusion')
        # This is not an aggregation engine. Imported recognition is retained as
        # evidence only; posting it here would double-count the source workflow.
        if r.get('mode')!='evidence_only':raise ReviewRequired('Imported accounting journal ownership must remain with its originating skill')
        seen.add(key)
    return output

def ledger(c,entries):
    """Every journal offset, including P&L, has an independently inventoried GL bridge."""
    accounts=rows(c['gl']);inventory(c,'gl_inventory',accounts)
    delta={}
    for entry in entries:
        balance(entry)
        for l in entry:
            if not isinstance(l['account'],str) or not l['account'].strip():raise ReviewRequired('Journal account must be curated text')
            delta[l['account']]=delta.get(l['account'],ZERO)+dec(l['amount'])*(1 if l['side']=='Dr' else -1)
    if set(delta)-{r['id'] for r in accounts}:raise ReviewRequired('Journal account absent from GL population')
    for r in accounts:
        approval(r,c);agree(r['closing'],dec(r['opening'])+delta.get(r['id'],ZERO),'All-account journal-to-GL')
        agree(r['statement'],r['closing'],'GL-to-financial-statements')

def stocks(c,values):
    by={r['id']:r for r in rows(c['gl'])}
    for account,(opening,closing) in values.items():
        if account not in by:
            if opening or closing:raise ReviewRequired('Opening/closing source stock account omitted')
            continue
        agree(by[account]['opening'],opening,'Source opening stock/GL');agree(by[account]['closing'],closing,'Source closing stock/GL')

def year_fraction(start,end):
    if max(start.year,end.year)>=9999:raise ReviewRequired('Unsupported date arithmetic range')
    value=ZERO
    for year in range(start.year,end.year+1):
        lo=max(start,date(year,1,1));hi=min(end,date(year,12,31))
        if hi>=lo:value+=Decimal((hi-lo).days+1)/Decimal((date(year+1,1,1)-date(year,1,1)).days)
    return value

def complete(c,title,calcs,entries,judgments):
    ledger(c,entries)
    return finish(title,calcs,entries,judgments,
        ['Reviewed operative-framework disclosure checklist; source and GL amounts tie to statement/note population',
         'Policies, movements, significant judgments and unrecognized or specialist-dependent exposures'])
