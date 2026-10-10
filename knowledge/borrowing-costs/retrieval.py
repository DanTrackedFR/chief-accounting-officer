"""Approved context-bound Borrowing Costs supplemental retrieval; internal evidence stays internal."""
import json
from datetime import date
from pathlib import Path
import importlib.util
HERE=Path(__file__).resolve().parent
FRAMEWORKS={'IFRS','US_GAAP','UK_GAAP','AASB'}
SCOPES={'IFRS':'for_profit_full_ifrs','US_GAAP':'ordinary_us_gaap','UK_GAAP':'frs102_full_commercial','AASB':'aasb_tier1_for_profit'}
PUBLIC_FIELDS=('claim_id','framework','decision','proposition','entity_scope','effective_period','public_limitations')

def load_register(path=None):
 d=json.loads(Path(path or HERE/'standards-claims.json').read_text())
 if d.get('namespace')!='SUPPLEMENTAL_BORROWING_COSTS':raise ValueError('Invalid Borrowing Costs namespace')
 cs=d.get('claims')
 if not isinstance(cs,list) or not cs or any(not isinstance(c,dict) for c in cs):raise ValueError('Invalid Borrowing Costs population')
 ids=[c.get('claim_id') for c in cs]
 if any(not isinstance(i,str) or not i for i in ids) or len(ids)!=len(set(ids)):raise ValueError('Invalid Borrowing Costs identities')
 return d

def retrieve(framework,period,entity_scope,path=None,decisions=None,period_start=None,early_presentation_adoption=False):
 if framework not in FRAMEWORKS or entity_scope!=SCOPES.get(framework):raise ValueError('Explicit supported Borrowing Costs framework/entity scope required')
 if early_presentation_adoption is not False:raise ValueError('Early presentation/disclosure adoption not reviewed')
 try:
  end=date.fromisoformat(period);start=date.fromisoformat(period_start or end.replace(month=1,day=1).isoformat())
 except (TypeError,ValueError):raise ValueError('ISO reporting dates required') from None
 if not date(2026,1,1)<=start<=end<date(2027,1,1):raise ValueError('Borrowing Costs period outside reviewed 2026 scope')
 if decisions is not None and (not isinstance(decisions,(list,tuple,set)) or not decisions or any(not isinstance(x,str) for x in decisions)):raise ValueError('Nonempty Borrowing Costs decision population required')
 d=load_register(path)
 spec=importlib.util.spec_from_file_location('_borrowing_supplement_validator',HERE/'validate_supplement.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
 if v.validate_data(d) or d.get('status')!='APPROVED':raise ValueError('Borrowing Costs knowledge not validly independently approved')
 matched=[]
 for c in d['claims']:
  if c['framework']!=framework or (decisions is not None and c['decision'] not in decisions):continue
  if c['entity_scope']!=entity_scope:raise ValueError('Borrowing Costs claim scope mismatch')
  ps=c['period_scope']
  if not date.fromisoformat(ps['begin_on_or_after'])<=start<date.fromisoformat(ps['begin_before']) or not end<date.fromisoformat(ps['end_before']):raise ValueError('Borrowing Costs claim period mismatch')
  matched.append({k:c[k] for k in PUBLIC_FIELDS})
 if not matched or (decisions is not None and set(decisions)!={c['decision'] for c in matched}):raise ValueError('No approved applicable Borrowing Costs decision')
 return matched
