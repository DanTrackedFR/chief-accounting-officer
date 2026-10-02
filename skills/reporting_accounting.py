"""Guarded reporting methods; no implied legal, forecast or valuation facts."""
from calendar import monthrange
from operations_accounting import *

def anniversary(d):
    return d.replace(year=d.year+1,day=min(d.day,monthrange(d.year+1,d.month)[1]))

def line_delta(lines,account,credit=True):
    return sum((dec(l['amount'])*(1 if (l['side']=='Cr')==credit else -1) for l in lines if l['account']==account),ZERO)

def reviewed(r,c,*keys):
    approval(r,c);texts(r,*keys)

def disclosure_review(c):
    required(c,'disclosure_review');d=c['disclosure_review'];reviewed(d,c,'checklist_version','period_entity_memo')
    if not flag(d,'complete'):raise ReviewRequired('Disclosure completeness review unresolved')

def common(c,*keys):
    proof(c,*keys);disclosure_review(c)

def specialist(c,key,target,amount=None):
    h=handoff(c,key,target)
    if amount is not None:
        required(h,'amount');agree(h['amount'],amount,'Specialist measured amount')
    return h

def policy(c,p):
    reviewed(p,c,'method_memo','effective_standard','entity_scope')
    if p['entity_scope']!=c['entity_type']:raise ReviewRequired('Policy entity scope mismatch')
    if p.get('framework')!=c['framework'] or p.get('effective_period')!=[c['period_start'],c['reporting_period']]:raise ReviewRequired('Accounting method does not cover actual framework/period')
