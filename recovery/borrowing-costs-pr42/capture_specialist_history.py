"""Fresh synthetic artifacts captured separately; no historical target writes."""
import json,sys,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path[:0]=[str(ROOT/'skills'),str(ROOT/'skills/tests')]
from production import serializable
from generate_governance_examples import artifacts as governance
from governance_cases import BATCH,FRAMEWORKS
from generate_inventory_examples import artifacts as inventory
from generate_hedge_inventory_examples import artifacts as hedge
from generate_insurance_examples import artifacts as insurance
from generate_presentation_examples import artifacts as presentation
from presentation_cases import PACKAGES,BLOCKED
out={}
for pkg in BATCH:
 for fw in FRAMEWORKS:out.update(governance(pkg,fw))
for generator in (inventory,hedge,insurance):out.update(generator())
for pkg in PACKAGES:
 for fw in FRAMEWORKS:
  out.update(presentation(pkg,fw))
  if pkg=='subsequent-events':out.update(presentation(pkg,fw,'adjusting'))
dest=Path(__file__).parent/'specialist-fresh';summary={};hashes=re.compile(r'[0-9a-f]{64}')
def shape(v):
 if isinstance(v,dict):return {hashes.sub('<identity>',k):shape(x) for k,x in v.items()}
 if isinstance(v,list):return [shape(x) for x in v]
 if isinstance(v,str):return hashes.sub('<identity>',v)
 return v
for name,value in out.items():
 v=json.loads(json.dumps(value,default=serializable));p=dest/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n')
 old=json.loads((ROOT/name).read_text());summary[name]=dict(exact=old==v,hash_normalized_match=shape(old)==shape(v),public=name.endswith('public.json'))
(dest/'comparison-summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print(json.dumps({'files':len(summary),'nonidentity_differences':[k for k,v in summary.items() if not v['hash_normalized_match']],'changed_public':[k for k,v in summary.items() if v['public'] and not v['exact']]}))
