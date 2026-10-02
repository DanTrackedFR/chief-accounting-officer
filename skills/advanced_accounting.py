"""Guardrails for additional Phase 3 workflows; no company facts inferred."""
from datetime import date
from decimal import Decimal
from core_accounting import ReviewRequired, cash, dec, required, journal
from production import flag, nonnegative

ZERO=Decimal(0)

def gate(c, *keys):
    required(c,'specialist_items',*keys)
    if not isinstance(c['specialist_items'],list) or c['specialist_items']:
        raise ReviewRequired('Resolve specialist matters before accounting execution')
    if not isinstance(c['evidence'],list) or not c['evidence'] or any(not isinstance(e,str) or not e.strip() for e in c['evidence']) or not isinstance(c['judgment_memo'],str) or not c['judgment_memo'].strip():
        raise ReviewRequired('Evidence population and accounting judgment memo required')
    if c['applicability_review']['exceptions']:
        raise ReviewRequired('Resolve applicability exceptions with specialist')

def iso(value):
    try:return date.fromisoformat(value)
    except (ValueError,TypeError):raise ReviewRequired('Use ISO event dates')

def event_date(c,value):
    d=iso(value)
    if d>iso(c['reporting_period']):raise ReviewRequired('Event follows reporting date')
    return d

def positive(value):
    n=nonnegative(value)
    if not n:raise ReviewRequired('Positive value required')
    return n

def unique(rows,key='id'):
    if not isinstance(rows,list) or not rows:raise ReviewRequired('Nonempty source population required')
    ids=[r.get(key) for r in rows]
    if any(not x for x in ids) or len(ids)!=len(set(ids)):
        raise ReviewRequired('Source IDs must be present and unique')

def movement(account,offset,delta):
    delta=cash(delta)
    return journal(('Dr',account,max(delta,ZERO)),('Cr',offset,max(delta,ZERO)),
                   ('Cr',account,max(-delta,ZERO)),('Dr',offset,max(-delta,ZERO)))

def result(conclusion,method,calcs,entries,judgments,disclosures,uncertainties=None):
    return {'conclusion':conclusion,'method':method,'calculations':calcs,
      'journal_entry_implications':[e for e in entries if e], 'judgments':judgments,
      'disclosures_impacted':disclosures,'uncertainties':uncertainties or [],'open_items':[],
      'controls_impacted':['Freeze source population and effective standards edition','Independent reperformance and adverse-route challenge','Schedule-to-journal-to-GL-to-note reconciliation'],
      'documentation_required':['Source facts, alternative routes, period/entity applicability, valuation/legal/tax memos where relevant'],
      'audit_evidence_required':['Complete versioned source population, approved inputs and independent certification']}
