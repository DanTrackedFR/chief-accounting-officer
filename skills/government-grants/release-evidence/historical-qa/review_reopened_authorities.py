"""Prove omitted digest summaries using complete native source archives."""
import base64,gzip,hashlib,importlib.util,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT))
from orchestration.persistence.codec import loads,dumps,decode
from orchestration.tests.generate_persistence_stage2_examples import project
spec=importlib.util.spec_from_file_location('transition',ROOT/'recovery/borrowing-costs-pr42/check_identity_transition.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def lossless(path, legacy_escaped_json=False):
 value=json.loads(path.read_text());wire=gzip.decompress(base64.b64decode(value['payload']));assert hashlib.sha256(wire).hexdigest()==value['sha256'];return decode(json.loads(wire)) if legacy_escaped_json else loads(wire.decode())
old=lossless(HERE/'stage2-pr42-rework-full.json',legacy_escaped_json=True)['checkpoint'];new=lossless(HERE/'stage2-reconstructed-native.json')['checkpoint']
expected=m.expand(json.loads((HERE/'orchestration-fresh/durable-rework-recovery/closed-reopened-period.json').read_text()))['rework']['checkpoint']['retained_evidence']
assert project(new)['retained_evidence']==expected,'Reconstructed authority digests differ from actual eleven-process SQLite capture'
t=m.Transition();prior=json.loads((HERE/'orchestration-migration.json').read_text())['identity_map'];t.forward.update(prior);t.reverse.update({b:a for a,b in prior.items()})
a=m.expand(json.loads(dumps(old)));b=m.expand(json.loads(dumps(new)))
for phase in ('versions','bundles'):t.phase=phase;t.seed(a,b,'native-reopened-checkpoint')
# The restored reconstruction has different SQLite operation revisions. Validate
# complete evidence archives; their source/pack digests match actual capture above.
t.compare(a['session']['evidence_bundles'],b['session']['evidence_bundles'],'native-reopened-checkpoint/session/evidence_bundles')
report=dict(source_archive=json.loads((ROOT/'recovery/borrowing-costs-pr42/stage2-archive-parts.json').read_text())['stage2-current-full'],status='PASS' if not t.errors else 'FAIL',archive_count=len(a['session']['evidence_bundles']),reconstructed_matches_real_sqlite_capture=True,old_full_sha256=hashlib.sha256((HERE/'stage2-pr42-rework-full.json').read_bytes()).hexdigest(),new_full_sha256=hashlib.sha256((HERE/'stage2-reconstructed-native.json').read_bytes()).hexdigest(),identity_map=t.forward,errors=t.errors)
(HERE/'stage2-full-authority-review.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='identity_map'})[:4000])
if t.errors:raise SystemExit(1)
