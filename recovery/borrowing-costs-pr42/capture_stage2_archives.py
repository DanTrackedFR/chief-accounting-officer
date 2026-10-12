"""Retain complete worker authorities before the generator emits slim proofs."""
import base64,gzip,hashlib,json,subprocess,sys
from pathlib import Path
checkout=Path(sys.argv[1]).resolve();destination=Path(sys.argv[2]).resolve();destination.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(checkout))
import os
os.chdir(checkout)
from orchestration.tests import generate_persistence_stage2_examples as generator
original=subprocess.run
counts={}
def capture(*args,**kwargs):
 r=original(*args,**kwargs)
 command=args[0] if args else kwargs['args']
 if isinstance(command,list) and 'orchestration.tests.generate_persistence_stage2_examples' in command:
  phase=command[-1];counts[phase]=counts.get(phase,0)+1
  if r.returncode==0:
   document=json.loads(r.stdout);wire=json.dumps(document,sort_keys=True,separators=(',',':')).encode();packed=bytearray(gzip.compress(wire,mtime=0));packed[9]=255
   envelope=dict(encoding='gzip-base64 canonical audit JSON',sha256=hashlib.sha256(wire).hexdigest(),payload=base64.b64encode(packed).decode());(destination/(phase+'-'+str(counts[phase])+'.json')).write_text(json.dumps(envelope,sort_keys=True)+'\n')
  (destination/(phase+'-'+str(counts[phase])+'.exit')).write_text(str(r.returncode)+'\n')
 return r
subprocess.run=capture
values=generator.artifacts()
for name,value in values.items():(destination/name).write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
(difference:=destination/'baseline-reproduction.json').write_text(json.dumps({name:value==json.loads((generator.TARGET/name).read_text()) for name,value in values.items()},indent=2)+'\n')
print(difference.read_text())
