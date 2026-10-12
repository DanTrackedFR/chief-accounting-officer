"""Independent expanded provenance transition review against main-resolved references."""
import hashlib,importlib.util,json,sys
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT))
def reference_path(name):
 name=Path(name)
 key=str(name.relative_to(ROOT)) if name.is_absolute() else str(name)
 row=json.loads((Path(__file__).parent/'main-reference-baseline.json').read_text()).get(key)
 target=ROOT/row['current_path'] if row else ROOT/key
 if row:assert hashlib.sha256(target.read_bytes()).hexdigest()==row['current_sha256']
 return target
spec=importlib.util.spec_from_file_location('old_transition',ROOT/'recovery/borrowing-costs-pr42/check_identity_transition.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
t=m.Transition();pairs=[]
full_review=HERE/'stage2-full-authority-review.json'
if full_review.exists():
 verified=json.loads(full_review.read_text());assert verified['status']=='PASS' and not verified['errors']
 for filename,key in (('stage2-pr42-rework-full.json','old_full_sha256'),('stage2-reconstructed-native.json','new_full_sha256')):assert hashlib.sha256((HERE/filename).read_bytes()).hexdigest()==verified[key]
 t.forward.update(verified['identity_map']);t.reverse.update({b:a for a,b in verified['identity_map'].items()})
for fresh in sorted((HERE/'orchestration-fresh').rglob('*.json')):
 name='orchestration/examples/'+str(fresh.relative_to(HERE/'orchestration-fresh'));prior=reference_path(name)
 pairs.append((name,prior,fresh,m.expand(json.loads(prior.read_text())),m.expand(json.loads(fresh.read_text()))))
for phase in ('versions','bundles'):
 t.phase=phase
 for name,prior,fresh,a,b in pairs:t.seed(a,b,name)
# Learn remaining structure-bound certificate identities before unordered ID
# sets are checked. A full second validation checks every leaf using one fixed
# bijection; no provenance population or successor edge is discarded.
for name,prior,fresh,a,b in pairs:t.compare(a,b,name)
discovery_errors=list(t.errors);t.errors=[];t.changed=0
for name,prior,fresh,a,b in pairs:t.compare(a,b,name)
expected=[dict(path='orchestration/examples/manufacturing.partial.graph.json/13/open_items/0',reason='nonidentity bytes changed',old='Accounting owner unavailable for production: government-grants',new='Missing reviewed source workpaper for grant'),dict(path='orchestration/examples/manufacturing.partial.public.json/open_items/0',reason='nonidentity bytes changed',old='grant: Accounting owner unavailable for production: government-grants',new='grant: Missing reviewed source workpaper for grant')]
behavior=[error for error in t.errors if error in expected]
assert len(behavior)==2,'Expected explicit Government Grants promotion labels must be independently reproduced'
t.errors=[error for error in t.errors if error not in expected]

def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files={name:dict(original_sha256=h(ROOT/name),previous_path=str(prior.relative_to(ROOT)),previous_sha256=h(prior),current_path=str(fresh.relative_to(ROOT)),current_sha256=h(fresh)) for name,prior,fresh,a,b in pairs if a!=b}
report=dict(status='PASS' if not t.errors else 'FAIL',compared_files=len(pairs),files=files,identity_map=t.forward,changed_identity_leaves=t.changed,approved_behavior_transitions=behavior,discovery_errors=discovery_errors,errors=t.errors,passed=not t.errors)
(HERE/'orchestration-migration.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps(dict(compared=len(pairs),migrated=len(files),identity_pairs=len(t.forward),errors=len(t.errors),first_errors=t.errors[:4])))
if t.errors:raise SystemExit(1)
