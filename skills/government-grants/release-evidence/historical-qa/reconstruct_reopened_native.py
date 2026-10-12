"""Independent original native calls reconstruct source authorities, no store repair."""
import base64,gzip,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT))
from orchestration.persistence.state import restore,snapshot
from orchestration.persistence.codec import loads,dumps
from orchestration.persistence.recovery import validate_intent,execute_native
from orchestration.tests.persistence_stage2_fixtures import attach,correction_intent,journal_intent,reopening,rework_intent
source=json.loads((HERE/'orchestration-fresh/durable-rework-recovery/full-native-checkpoints.json').read_text())['resumed'];wire=gzip.decompress(base64.b64decode(source['payload']));assert hashlib.sha256(wire).hexdigest()==source['sha256'];doc=loads(wire.decode());case=restore(doc,doc['company_id'],doc['root_case'])
def run(intent):
 validate_intent(case,intent);return execute_native(case,intent)
run(journal_intent(case));period=attach(case)['nodes']['adjacent-closing'].period_id
run(dict(kind='CLOSE_PERIOD',period_id=period))
# Preserve the worker's real closed-period refusal and retained review preview.
try:
 refused=correction_intent(case)
 validate_intent(case,refused)
except ValueError:pass
else:raise AssertionError('Closed-period correction was not refused')
run(reopening(case,period));plan=run(correction_intent(case));run(rework_intent(case,plan))
checkpoint=snapshot(case,doc['company_id'],doc['company_context']);wire=dumps(dict(checkpoint=checkpoint)).encode();packed=bytearray(gzip.compress(wire,mtime=0));packed[9]=255
out=dict(encoding='gzip-base64 canonical audit JSON',sha256=hashlib.sha256(wire).hexdigest(),payload=base64.b64encode(packed).decode())
(HERE/'stage2-reconstructed-native.json').write_text(json.dumps(out,sort_keys=True)+'\n');print('Native reopened source authorities captured',len(checkpoint['session']['evidence_bundles']),flush=True)
