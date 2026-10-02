"""Operational control assertions; amounts and accounting judgments are inputs."""
from datetime import timedelta
from decimal import Decimal
from core_accounting import ReviewRequired, cash, dec, required, journal, balance
from advanced_accounting import gate, iso, positive, movement, result, ZERO
from production import flag, nonnegative, fraction

def rows(value, allow_empty=True):
    if not isinstance(value,list) or (not value and not allow_empty):
        raise ReviewRequired('Source population must be an array')
    ids=[]
    for r in value:
        if not isinstance(r,dict):raise ReviewRequired('Source row must be an object')
        required(r,'id'); ids.append(r['id'])
        if not isinstance(r['id'],str):raise ReviewRequired('Source identifier must be text')
    if len(set(ids))!=len(ids):raise ReviewRequired('Duplicate source identifier')
    return value

def proof(c,*keys):
    gate(c,'controls',*keys)
    q=c['controls']
    required(q,'source_version','as_of','population_count','population_amount','owner','reviewer','complete','policy_version','cutoff_memo')
    if q['owner']==q['reviewer'] or not flag(q,'complete') or iso(q['as_of'])!=iso(c['reporting_period']):
        raise ReviewRequired('Independent complete period-end population proof required')
    if not isinstance(q['population_count'],int) or isinstance(q['population_count'],bool) or q['population_count']<0:
        raise ReviewRequired('Population count must be a nonnegative integer')
    nonnegative(q['population_amount'])

def population(c,rs,amounts):
    if len(rs)!=c['controls']['population_count'] or cash(sum(amounts,ZERO))!=cash(c['controls']['population_amount']):
        raise ReviewRequired('Independent source count and absolute amount bridge failed')

def approval(r,c):
    required(r,'owner','reviewer','evidence','approved','approval_date','version','approved_version')
    if r['owner']==r['reviewer'] or not flag(r,'approved') or r['version']!=r['approved_version'] or not isinstance(r['evidence'],str) or not r['evidence'].strip():
        raise ReviewRequired('Independent supported current-version approval required')
    if iso(r['approval_date'])>iso(c['reporting_period']):raise ReviewRequired('Approval falls after workpaper cutoff')

def inperiod(c,d):
    d=iso(d)
    if not iso(c['period_start'])<=d<=iso(c['reporting_period']):raise ReviewRequired('Event outside reporting period')
    return d

def agree(actual,expected,label):
    if cash(actual)!=cash(expected):raise ReviewRequired(label+' reconciliation failed')

def handoff(c,key,target):
    required(c,'handoffs'); h=c['handoffs'].get(key,{})
    required(h,'target','entity','framework','reporting_period','evidence','reviewer','resolved','scope_memo')
    if h['target']!=target or h['entity']!=c['entity'] or h['framework']!=c['framework'] or h['reporting_period']!=c['reporting_period'] or not flag(h,'resolved'):
        raise ReviewRequired('Unresolved or mismatched specialist handoff: '+key)
    # This is an external reviewed memo, not a forged downstream certification.
    # If a downstream result is supplied, enforce its actual result dimensions.
    if 'result' in h:
        r=h['result']
        if r.get('status')!='complete' or r.get('framework')!=c['framework'] or c['entity'] not in r.get('entities',[]) or c['reporting_period'] not in r.get('periods',[]):
            raise ReviewRequired('Downstream skill result is incomplete or out of scope')
    return h

def finish(title,calcs,entries,judgments,notes):
    return result(title,'Approved canonical operational method; independently substantiated source-to-journal-to-GL proof',calcs,entries,judgments,notes,
        ['Company recognition, valuation, legal rights and tax conclusions require supplied evidence and independent review. No universal ERP posting authorization is inferred.'])
