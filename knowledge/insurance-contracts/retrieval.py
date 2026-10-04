"""Approved context-bound Insurance supplemental retrieval; internal evidence stays internal."""
import json
from datetime import date
from pathlib import Path
import importlib.util
HERE=Path(__file__).resolve().parent
FRAMEWORKS={'IFRS','US_GAAP','UK_GAAP','AASB'}
SCOPES={'IFRS':'for_profit_full_ifrs','US_GAAP':'ordinary_us_gaap','UK_GAAP':'frs102_full_commercial','AASB':'aasb_tier1_for_profit'}
PUBLIC_FIELDS=('claim_id','framework','decision','proposition','entity_scope','effective_period','public_limitations')
MODELS={'IFRS':{'IFRS17_GMM','IFRS17_PAA'},'AASB':{'AASB17_GMM','AASB17_PAA'},'US_GAAP':{'ASC944_SHORT_DURATION'},'UK_GAAP':{'FRS103_POLICY_REVIEW'}}
def load_register(path=None):
 d=json.loads(Path(path or HERE/'standards-claims.json').read_text())
 if d.get('namespace')!='SUPPLEMENTAL_INSURANCE_CONTRACTS':raise ValueError('Invalid Insurance namespace')
 cs=d.get('claims')
 if not isinstance(cs,list) or not cs or any(not isinstance(c,dict) for c in cs):raise ValueError('Invalid Insurance population')
 ids=[c.get('claim_id') for c in cs]
 if any(not isinstance(i,str) or not i for i in ids) or len(ids)!=len(set(ids)):raise ValueError('Invalid Insurance identities')
 return d

def retrieve(framework,period,entity_scope,path=None,decisions=None,period_start=None,insurance_model=None,early_presentation_adoption=False):
 if framework not in FRAMEWORKS or entity_scope!=SCOPES.get(framework):raise ValueError('Explicit supported Insurance framework/entity scope required')
 if insurance_model not in MODELS[framework]:raise ValueError('Explicit supported Insurance model required')
 if early_presentation_adoption is not False:raise ValueError('Early presentation/disclosure adoption not reviewed')
 try:
  end=date.fromisoformat(period);start=date.fromisoformat(period_start or end.replace(month=1,day=1).isoformat())
 except (TypeError,ValueError):raise ValueError('ISO reporting dates required') from None
 if not date(2026,1,1)<=start<=end<date(2027,1,1):raise ValueError('Insurance period outside reviewed 2026 scope')
 if decisions is not None and (not isinstance(decisions,(list,tuple,set)) or not decisions or any(not isinstance(x,str) for x in decisions)):raise ValueError('Nonempty Insurance decision population required')
 d=load_register(path)
 spec=importlib.util.spec_from_file_location('_insurance_supplement_validator',HERE/'validate_supplement.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
 if v.validate_data(d) or d.get('status')!='APPROVED':raise ValueError('Insurance knowledge not validly independently approved')
 matched=[]
 for c in d['claims']:
  if c['framework']!=framework or (decisions is not None and c['decision'] not in decisions):continue
  if c['entity_scope']!=entity_scope:raise ValueError('Insurance claim scope mismatch')
  ps=c['period_scope']
  if not date.fromisoformat(ps['begin_on_or_after'])<=start<date.fromisoformat(ps['begin_before']) or not end<date.fromisoformat(ps['end_before']):raise ValueError('Insurance claim period mismatch')
  matched.append({k:c[k] for k in PUBLIC_FIELDS})
 if not matched or (decisions is not None and set(decisions)!={c['decision'] for c in matched}):raise ValueError('No approved applicable Insurance decision')
 return matched
