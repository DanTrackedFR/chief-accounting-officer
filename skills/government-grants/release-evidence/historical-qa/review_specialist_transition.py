"""Independent strict digest-field transition witness; original history is immutable."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT))
def reference_path(name):
 name=Path(name)
 key=str(name.relative_to(ROOT)) if name.is_absolute() else str(name)
 row=json.loads((Path(__file__).parent/'main-reference-baseline.json').read_text()).get(key)
 target=ROOT/row['current_path'] if row else ROOT/key
 if row:assert hashlib.sha256(target.read_bytes()).hexdigest()==row['current_sha256']
 return target
HERE=Path(__file__).parent
ALLOWED={'case_fingerprint','payload_fingerprint','owner_result_fingerprint','content_hash','body_hash'}
forward={};reverse={};files={};changes=[]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compare(a,b,path):
 if type(a)!=type(b):raise AssertionError(('type',path))
 if isinstance(a,dict):
  if set(a)!=set(b):raise AssertionError(('keys',path))
  for k in a:compare(a[k],b[k],path+'/'+k)
 elif isinstance(a,list):
  if len(a)!=len(b):raise AssertionError(('population',path))
  for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+'/'+str(i))
 elif a!=b:
  if path.split('/')[-1] not in ALLOWED:raise AssertionError(('nonidentity change',path,a,b))
  if not all(isinstance(x,str) and len(x)==64 and set(x)<=set('0123456789abcdef') for x in (a,b)):raise AssertionError(('not digest',path))
  if forward.setdefault(a,b)!=b or reverse.setdefault(b,a)!=a:raise AssertionError(('nonbijective',path))
  changes.append(dict(path=path,old=a,new=b))
summary=json.loads((HERE/'specialist-fresh/comparison-summary.json').read_text())
for name in summary:
 original=ROOT/name;prior=reference_path(name);fresh=HERE/'specialist-fresh'/name
 start=len(changes);compare(json.loads(prior.read_text()),json.loads(fresh.read_text()),name)
 if len(changes)>start:
  files[name]=dict(original_sha256=digest(original),previous_path=str(prior.relative_to(ROOT)),previous_sha256=digest(prior),current_path=str(fresh.relative_to(ROOT)),current_sha256=digest(fresh),differences=changes[start:])
manifest=dict(status='PASS',errors=[],passed=True,review='Independent synthetic reproduction; strict digest-field-only and globally bijective transition; all numeric, journal, source and public payloads equal.',compared_files=len(summary),changed_public_outputs=[],files=files,identity_map=forward)
(HERE/'specialist-migration.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print(json.dumps(dict(compared=len(summary),migrated=len(files),identity_pairs=len(forward),changed_leaves=len(changes),nonidentity_changes=0,public_changes=0)))
