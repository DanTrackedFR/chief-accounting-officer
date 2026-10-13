"""Read-only Git-backed comparison; create a new witness, never repair originals."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[2]
MAIN='e75375b84813b9d584db12aa692b2f4d16baf052'

def prepare():
 listing=subprocess.check_output(['git','ls-tree','-r',MAIN],cwd=ROOT,text=True)
 selected=[]
 for line in listing.splitlines():
  metadata,name=line.split('\t',1)
  if '/examples/' in name or '/release/' in name or name.startswith(('knowledge/','recovery/','skills/borrowing-costs/','skills/government-grants/')):
   selected.append((name,metadata.split()[2]))
 names=[x[0] for x in selected]
 current=subprocess.check_output(['git','hash-object','--stdin-paths'],cwd=ROOT,input='\n'.join(names)+'\n',text=True).splitlines()
 errors=[name for (name,old),new in zip(selected,current) if old!=new]
 if len(current)!=len(selected):errors.append('Git preservation population incomplete')
 assert not errors,('Historical bytes changed',errors)
 files={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names}
 value=dict(status='PASS',baseline_main=MAIN,compared_files=len(files),git_blob_population_sha256=hashlib.sha256(listing.encode()).hexdigest(),errors=[],files=files,historical_artifacts_regenerated=False)
 out=ROOT/'build4/release/investment-property-historical-preservation.json'
 out.write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
 print(json.dumps(dict(status='PASS',files=len(files),baseline_main=MAIN)))

if __name__=='__main__':prepare()
