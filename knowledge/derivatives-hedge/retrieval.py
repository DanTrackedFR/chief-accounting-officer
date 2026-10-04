"""Context-bound Derivatives/Hedge supplemental retrieval; internal provenance never leaves gate."""
import json
from datetime import date
from pathlib import Path

HERE=Path(__file__).resolve().parent
FRAMEWORKS={'IFRS','US_GAAP','UK_GAAP','AASB'}
SCOPES={'IFRS':'for_profit_full_ifrs','US_GAAP':'ordinary_us_gaap','UK_GAAP':'frs102_full_commercial','AASB':'aasb_tier1_for_profit'}
PUBLIC_FIELDS=('claim_id','framework','decision','proposition','entity_scope','effective_period','public_limitations')

def load_register(path=None):
    data=json.loads(Path(path or HERE/'standards-claims.json').read_text())
    if data.get('namespace')!='SUPPLEMENTAL_DERIVATIVES_HEDGE':
        raise ValueError('Invalid Derivatives/Hedge supplemental namespace')
    claims=data.get('claims')
    if not isinstance(claims,list) or not claims or any(not isinstance(c,dict) for c in claims):
        raise ValueError('Invalid Derivatives/Hedge claims population')
    ids=[c.get('claim_id') for c in claims]
    if any(not isinstance(i,str) or not i for i in ids) or len(ids)!=len(set(ids)):
        raise ValueError('Missing or duplicate Derivatives/Hedge claim ID')
    return data

MODELS={'IFRS':'IFRS9_CH6','AASB':'AASB9_CH6','US_GAAP':'ASC815_BASELINE','UK_GAAP':'FRS102_SECTION12'}

def retrieve(framework, period, entity_scope, path=None, decisions=None, period_start=None, hedge_model=None, us_amendments_adopted=None):
    if hedge_model != MODELS.get(framework):
        raise ValueError('Explicit supported hedge model required')
    if framework not in FRAMEWORKS or entity_scope!=SCOPES.get(framework):
        raise ValueError('Explicit supported Derivatives/Hedge framework/entity scope required')
    try:
        end=date.fromisoformat(period)
        start=date.fromisoformat(period_start or end.replace(month=1,day=1).isoformat())
    except (TypeError,ValueError):
        raise ValueError('ISO reporting dates required') from None
    if not date(2026,1,1)<=start<=end<date(2027,1,1):
        raise ValueError('Derivatives/Hedge period outside reviewed 2026 scope')
    if framework == 'US_GAAP' and (us_amendments_adopted is not False or start > date(2026,12,15)):
        raise ValueError('US baseline requires explicit nonadoption and no mandatory 2025 amendments')
    if decisions is not None and (not isinstance(decisions,(list,tuple,set)) or not decisions or any(not isinstance(x,str) for x in decisions)):
        raise ValueError('Nonempty Derivatives/Hedge decision population required')
    data=load_register(path)
    # Revalidate the whole register rather than letting one selected claim hide bad approval.
    import importlib.util
    import sys
    name='_cao_derivatives_hedge_validator'
    if name not in sys.modules:
        spec=importlib.util.spec_from_file_location(name,HERE/'validate_supplement.py')
        module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
    validate_data=sys.modules[name].validate_data
    errors=validate_data(data)
    if errors or data.get('status')!='APPROVED':
        raise ValueError('Supplemental Derivatives/Hedge knowledge not validly approved')
    matched=[]
    for c in data['claims']:
        if c['framework']!=framework or (decisions is not None and c['decision'] not in decisions):continue
        if c['entity_scope']!=entity_scope:raise ValueError('Derivatives/Hedge claim scope mismatch')
        ps=c['period_scope']
        if not date.fromisoformat(ps['begin_on_or_after'])<=start<date.fromisoformat(ps['begin_before']) or not end<date.fromisoformat(ps['end_before']):
            raise ValueError('Derivatives/Hedge claim period mismatch')
        matched.append({k:c[k] for k in PUBLIC_FIELDS})
    if not matched or (decisions is not None and set(decisions)!={c['decision'] for c in matched}):
        raise ValueError('No approved applicable Derivatives/Hedge decision')
    return matched
