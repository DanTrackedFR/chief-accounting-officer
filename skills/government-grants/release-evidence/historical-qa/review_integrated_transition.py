"""Independent strict expanded integrated proof identity transition."""
import hashlib,importlib.util,json,sys
from pathlib import Path
HERE=Path(__file__).parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location('old_transition',ROOT/'recovery/borrowing-costs-pr42/check_identity_transition.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
oldmanifest=json.loads((ROOT/'recovery/borrowing-costs-pr42/main-proof-migration.json').read_text());t=m.Transition();pairs=[]
modules={'build4/release/integrated-proof.json':'build4.prove_integrated','build4/release/memory-proof.json':'build4.prove_memory','intelligence/release/integrated-proof.json':'intelligence.tests.prove_integrated','hosted_cao/release/http-proof.json':'hosted_cao.tests.prove_http','local_cao/examples/cli-proof.json':'local_cao.tests.prove_cli'}
for name,mod in modules.items():
 prior=ROOT/oldmanifest['files'][name]['current_path'];fresh=HERE/'integration-fresh'/(mod+'.json');pairs.append((name,prior,fresh,m.expand(json.loads(prior.read_text())),m.expand(json.loads(fresh.read_text()))))
# This proof presents SQL version rows ordered by opaque version_id. Bind by
# independently unique lifecycle state, never by array index or hash masking.
for name,prior,fresh,a,b in pairs:
 if name.startswith('intelligence/'):
  for proof in (a,b):
   rows=proof['revenue']['final_versions']
   assert len(rows)==2 and {r['state'] for r in rows}=={'CURRENT','SUPERSEDED'}
   current=next(r for r in rows if r['state']=='CURRENT')
   old=next(r for r in rows if r['state']=='SUPERSEDED')
   assert current['superseded_by'] is None and old['superseded_by']==current['version_id']
   proof['revenue']['final_versions']=sorted(rows,key=lambda r:r['state'])
for phase in ('versions','bundles'):
 t.phase=phase
 for name,prior,fresh,a,b in pairs:t.seed(a,b,name)
for name,prior,fresh,a,b in pairs:t.compare(a,b,name)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files={name:dict(original_sha256=h(ROOT/name),previous_path=str(prior.relative_to(ROOT)),previous_sha256=h(prior),current_path=str(fresh.relative_to(ROOT)),current_sha256=h(fresh)) for name,prior,fresh,a,b in pairs if a!=b}
report=dict(status='PASS' if not t.errors else 'FAIL',compared_files=len(pairs),files=files,identity_map=t.forward,changed_identity_leaves=t.changed,errors=t.errors,passed=not t.errors)
(HERE/'main-proof-migration.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps(dict(compared=len(pairs),migrated=len(files),identity_pairs=len(t.forward),errors=len(t.errors),first_errors=t.errors[:4])))
if t.errors:raise SystemExit(1)
