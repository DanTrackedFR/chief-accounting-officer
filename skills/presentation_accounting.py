"""Bounded presentation controls reuse existing governed accounting execution."""
from financing_accounting import *
from datetime import timedelta

def qualified(c,p,target):
    policy(c,p);texts(p,'scope_memo','boundary_memo')
    if p.get('target')!=target:raise ReviewRequired('Wrong specialist method owner')
    if not flag(p,'resolved'):raise ReviewRequired('Specialist method unresolved')
    return p

def source(c,r):
    approval(r,c)
    if r.get('source_entity')!=c['entity'] or r.get('source_framework')!=c['framework'] or r.get('source_period')!=[c['period_start'],c['reporting_period']]:raise ReviewRequired('Source dimensions mismatch')

def ratio(n,d):
    d=nonnegative(d)
    if d==0:raise ReviewRequired('EPS denominator must be positive')
    return dec(n)/d

def completed(c,r,allowed):
    from production import execute
    approval(r,c)
    if r.get('package') not in allowed:raise ReviewRequired('Unsupported accounting owner')
    s=r['case']
    if any(s.get(k)!=c.get(k) for k in ('entity','framework','period_start','reporting_period')):raise ReviewRequired('Accounting owner dimensions mismatch')
    fresh=execute(r['package'],s)
    if fresh['status']!='complete' or not same_result(fresh,r['result']):raise ReviewRequired('Accounting owner must be completed, current and unaltered')
    return fresh

def public_label(r):
    texts(r,'label')
    # Generated workpapers never serialize raw records or specialist metadata.
    return r['label']

def statement_source(c,metrics):
    """Independent period statement line population binds disclosed totals to GL."""
    p=c['financial_statement_source'];policy(c,p);reviewed(p,c,'mapping_memo','full_period_memo')
    lines=rows(p['lines']);inventory(p,'line_inventory',lines);by={r['id']:r for r in rows(c['gl'])};totals={k:ZERO for k in metrics};seen=set()
    for r in lines:
        source(c,r);metric=enum(r,'metric',set(metrics));account=r['account']
        if account not in by or (metric,account) in seen:raise ReviewRequired('Missing or duplicated statement-source GL account')
        seen.add((metric,account));sign=-1 if flag(r,'credit_nature') else 1
        value=dec(by[account]['closing'])*sign;agree(r['amount'],value,'Statement line/GL');totals[metric]+=value
    if {r['metric'] for r in lines}!=set(metrics):raise ReviewRequired('Required period statement metric absent')
    for r in c['imports']:
        if r['package']=='financial-statements':
            current=r['result']['calculations']['current']
            for metric in set(metrics)&{'profit','revenue','assets','liabilities'}:agree(totals[metric],current[metric],'Actual completed Financial Statements import')
    return totals
