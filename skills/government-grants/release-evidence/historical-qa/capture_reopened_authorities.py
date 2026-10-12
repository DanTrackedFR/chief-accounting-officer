"""Native resumed checkpoint restoration; capture later full sealed authorities."""
import base64,gzip,hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT))
from orchestration.persistence import SQLiteStore
from orchestration.persistence.state import restore
from orchestration.persistence.codec import loads
source=json.loads((HERE/'orchestration-fresh/durable-rework-recovery/full-native-checkpoints.json').read_text())['resumed']
wire=gzip.decompress(base64.b64decode(source['payload']));assert hashlib.sha256(wire).hexdigest()==source['sha256'];doc=loads(wire.decode())
DEST=HERE/'stage2-reopened-full';DEST.mkdir(exist_ok=True);database=DEST/'replay.db'
if database.exists():raise RuntimeError('Preserve previous recovery database; choose fresh destination')
case=restore(doc,doc['company_id'],doc['root_case'])
with SQLiteStore(database) as store:store.save(case,doc['company_id'],doc['company_context'],0)
for phase in ('selection','periods','correction','rework'):
 r=subprocess.run([sys.executable,'-m','orchestration.tests.generate_persistence_stage2_examples',str(database),phase],capture_output=True,text=True)
 (DEST/(phase+'.exit')).write_text(str(r.returncode)+'\n');(DEST/(phase+'.stderr')).write_text(r.stderr)
 if r.returncode:raise RuntimeError(phase+': '+r.stderr)
 wire=r.stdout.strip().encode();compressed=bytearray(gzip.compress(wire,mtime=0));compressed[9]=255
 payload=dict(encoding='gzip-base64 canonical audit JSON',sha256=hashlib.sha256(wire).hexdigest(),payload=base64.b64encode(compressed).decode())
 (DEST/(phase+'.json')).write_text(json.dumps(payload,sort_keys=True)+'\n');print(phase,'captured full authority',flush=True)
