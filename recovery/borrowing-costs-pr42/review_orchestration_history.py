"""Review captured orchestration authority using native version anchors."""
import json
from pathlib import Path
from check_identity_transition import Transition,expand,HEX
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).parent;dest=HERE/'orchestration-fresh';pairs=[];missing=[]
for p in dest.rglob('*.json'):
 name=p.relative_to(dest);old=ROOT/'orchestration/examples'/name
 if not old.exists():missing.append(str(name));continue
 pairs.append((str(name),expand(json.loads(old.read_text())),expand(json.loads(p.read_text()))))
t=Transition();t.stable=set(HEX.findall(json.dumps([a for _,a,_ in pairs]))) & set(HEX.findall(json.dumps([b for _,_,b in pairs])))
for name,a,b in pairs:
 try:t.seed(a,b,name)
 except (KeyError,AttributeError,TypeError,ValueError) as error:t.errors.append({'path':name,'reason':'native version anchor unavailable','details':str(error)})
t.phase='bundles'
for name,a,b in pairs:t.seed(a,b,name)
for name,a,b in pairs:t.compare(a,b,name)
result=dict(status='PASS' if not t.errors and not missing and pairs else 'UNRESOLVED',compared_files=len(pairs),missing_historical_files=missing,identity_map=t.forward,errors=t.errors,changed_identity_leaves=t.changed);(HERE/'orchestration-identity-review.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='identity_map'})[:10000])
