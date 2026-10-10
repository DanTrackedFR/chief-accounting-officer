"""Approved, period/model-bound Government Grants retrieval with internal metadata excluded."""
import json
from datetime import date
from pathlib import Path
import importlib.util
HERE=Path(__file__).resolve().parent
FRAMEWORKS={'IFRS','US_GAAP','UK_GAAP','AASB'}
SCOPES={'IFRS':'for_profit_full_ifrs','US_GAAP':'us_business_entity_early_adopter','UK_GAAP':'frs102_full_commercial','AASB':'aasb_tier1_for_profit'}
MODELS={'IFRS':{'IAS20_ACCRUAL'},'AASB':{'AASB120_ACCRUAL'},'US_GAAP':{'ASC832_ASU2025_10_ADOPTED'},'UK_GAAP':{'FRS102_ACCRUAL','FRS102_PERFORMANCE'}}
PUBLIC_FIELDS=('claim_id','framework','decision','proposition','entity_scope','effective_period','public_limitations')

def load_register(path=None):
    d=json.loads(Path(path or HERE/'standards-claims.json').read_text())
    if not isinstance(d,dict) or d.get('namespace')!='SUPPLEMENTAL_GOVERNMENT_GRANTS':raise ValueError('Invalid Government Grants namespace')
    cs=d.get('claims')
    if not isinstance(cs,list) or not cs or any(not isinstance(c,dict) for c in cs):raise ValueError('Invalid Government Grants population')
    ids=[c.get('claim_id') for c in cs]
    if any(not isinstance(i,str) or not i for i in ids) or len(ids)!=len(set(ids)):raise ValueError('Invalid Government Grants identities')
    return d

def retrieve(framework,period,entity_scope,path=None,decisions=None,period_start=None,grant_model=None,early_presentation_adoption=False,us_adoption=None,execution_date=None):
    if framework not in FRAMEWORKS or entity_scope!=SCOPES.get(framework):raise ValueError('Explicit supported Government Grants framework/entity scope required')
    if grant_model not in MODELS[framework]:raise ValueError('Explicit supported Government Grants model required')
    if early_presentation_adoption is not False:raise ValueError('Early presentation/disclosure adoption not reviewed')
    try:
        end=date.fromisoformat(period);start=date.fromisoformat(period_start)
    except (TypeError,ValueError):raise ValueError('ISO reporting dates and period start required') from None
    if not date(2026,1,1)<=start<=end<date(2027,1,1):raise ValueError('Government Grants period outside reviewed 2026 scope')
    if framework=='US_GAAP':
        if not isinstance(us_adoption,dict) or us_adoption.get('standard')!='ASU2025-10' or us_adoption.get('annual_period_start')!=start.isoformat() or us_adoption.get('financial_statements_unissued_at_adoption') is not True or us_adoption.get('transition_reviewed') is not True or not us_adoption.get('evidence_id'):raise ValueError('Current US recognition requires evidenced qualified early adoption')
        try:adoption_date=date.fromisoformat(us_adoption.get('adoption_date'))
        except (TypeError,ValueError):raise ValueError('US adoption date required') from None
        try:preparation_date=date.fromisoformat(execution_date)
        except (TypeError,ValueError):raise ValueError('Actual US preparation date required') from None
        if preparation_date<end or adoption_date<date(2025,12,4) or adoption_date>preparation_date:raise ValueError('US adoption date invalid for actual preparation date')
    if decisions is not None and (not isinstance(decisions,(list,tuple,set)) or not decisions or any(not isinstance(x,str) for x in decisions)):raise ValueError('Nonempty Government Grants decision population required')
    d=load_register(path)
    spec=importlib.util.spec_from_file_location('_grant_supplement_validator',HERE/'validate_supplement.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    if v.validate_data(d) or d.get('status')!='APPROVED':raise ValueError('Government Grants knowledge not validly independently approved')
    matched=[]
    for c in d['claims']:
        if c['framework']!=framework or (decisions is not None and c['decision'] not in decisions):continue
        if c['entity_scope']!=entity_scope:raise ValueError('Government Grants claim scope mismatch')
        ps=c['period_scope']
        if not date.fromisoformat(ps['begin_on_or_after'])<=start<date.fromisoformat(ps['begin_before']) or not end<date.fromisoformat(ps['end_before']):raise ValueError('Government Grants claim period mismatch')
        matched.append({k:c[k] for k in PUBLIC_FIELDS})
    if not matched or (decisions is not None and set(decisions)!={c['decision'] for c in matched}):raise ValueError('No approved applicable Government Grants decision')
    return matched
