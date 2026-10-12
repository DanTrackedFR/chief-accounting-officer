"""Bind opaque retained evidence to replayed complete historical authorities."""
import json
import gzip
import io
import hashlib
from pathlib import Path
from check_identity_transition import Transition,expand,HEX
HERE=Path(__file__).parent;ROOT=HERE.parents[1];pairs=[]
import tarfile

def archive(name):
 record=json.loads((HERE/'stage2-archive-parts.json').read_text())[name]
 chunks=[]
 for part in record['parts']:
  data=(ROOT/part['path']).read_bytes();assert hashlib.sha256(data).hexdigest()==part['sha256'];chunks.append(data)
 data=b''.join(chunks);assert hashlib.sha256(data).hexdigest()==record['archive_sha256']
 with tarfile.open(fileobj=io.BytesIO(data),mode='r:xz') as source:
  return {member.name:json.loads(source.extractfile(member).read()) for member in source.getmembers() if member.isfile()}
old=archive('stage2-baseline-full');new=archive('stage2-current-full')
for name,value in old.items():
 if name=='baseline-reproduction.json' or name not in new:continue
 pairs.append((name,expand(value),expand(new[name])))
for p in (HERE/'stage2-fresh').glob('*.json'):
 if p.name.endswith('.differences.json') or p.name in ('comparison-summary.json','identity-transition-review.json'):continue
 pairs.append(('published/'+p.name,expand(json.loads((ROOT/'orchestration/examples/durable-rework-recovery'/p.name).read_text())),expand(json.loads(p.read_text()))))
t=Transition();t.stable=set(HEX.findall(json.dumps([a for _,a,_ in pairs]))) & set(HEX.findall(json.dumps([b for _,_,b in pairs])))
for name,a,b in pairs:t.seed(a,b,name)
t.phase='bundles'
for name,a,b in pairs:t.seed(a,b,name)
for name,a,b in pairs:t.compare(a,b,name)
reproduction=old['baseline-reproduction.json'];result=dict(status='PASS' if not t.errors and all(reproduction.values()) else 'UNRESOLVED',complete_worker_archives=len([n for n,_,_ in pairs if n.endswith('.json') and n.startswith(('baseline-','correction-','resume-','selection-','periods-','rework-','reclose-','repeat-'))]),compared_records=len(pairs),historical_baseline_reproduction=reproduction,identity_map=t.forward,errors=t.errors);(HERE/'stage2-full-provenance-review.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='identity_map'})[:15000])
