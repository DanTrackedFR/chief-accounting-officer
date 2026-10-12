"""Provenance comparison with globally bijective, structure-bound hash mapping.

Version pairs are anchored to stable native node identity and predecessor depth.
A receipt cannot substitute a different producer version under hash masking.
"""
import base64,gzip,json,re,sys
from pathlib import Path
HEX=re.compile('[0-9a-f]{64}')
class Transition:
 def __init__(self):self.forward={};self.reverse={};self.errors=[];self.changed=0;self.stable=set();self.phase="versions"
 def bind(self,a,b,path):
  if a==b:return
  if self.forward.get(a,b)!=b or self.reverse.get(b,a)!=a:self.errors.append({'path':path,'reason':'nonbijective provenance identity','old':a,'new':b});return
  self.forward[a]=b;self.reverse[b]=a
 def version_table(self,value):
  rows=list(value.values()) if isinstance(value,dict) else value
  return isinstance(rows,list) and bool(rows) and all(isinstance(r,dict) and {'node_id','version_id','predecessor'}<=set(r) for r in rows)
 def seed_versions(self,a,b,path):
  def index(table):
   if isinstance(table,list):table={row['version_id']:row for row in table}
   def depth(v,seen=()):
    if v in seen:raise ValueError('historical predecessor cycle')
    p=table[v].get('predecessor');return 0 if p is None else 1+depth(p,seen+(v,))
   out={}
   for key,row in table.items():
    signature=(row['node_id'],depth(key))
    if signature in out:raise ValueError('Ambiguous native node version depth')
    out[signature]=row
   return out
  old,new=index(a),index(b)
  if set(old)!=set(new):self.errors.append({'path':path,'reason':'native node/version sequence changed'})
  for key in set(old)&set(new):
   for field in ('version_id','result_id','source_fingerprint','exact_case_fingerprint','result_fingerprint'):
    x,y=old[key].get(field),new[key].get(field)
    if isinstance(x,str) and isinstance(y,str):self.strings(x,y,path+'/'+str(key)+'/'+field)
 def seed(self,a,b,path=''):
  if isinstance(a,dict) and isinstance(b,dict):
   if self.version_table([a]) and self.version_table([b]) and a['node_id']==b['node_id']:
    for field in ('version_id','result_id','source_fingerprint','exact_case_fingerprint','result_fingerprint'):
     if isinstance(a.get(field),str) and isinstance(b.get(field),str):self.strings(a[field],b[field],path+'/'+field)
   if 'versions' in a and 'versions' in b and self.version_table(a['versions']) and self.version_table(b['versions']):self.seed_versions(a['versions'],b['versions'],path+'/versions')
   if self.phase=='bundles' and 'evidence_bundles' in a and 'evidence_bundles' in b:
    def signature(value,key=''):
     if isinstance(value,dict):return {HEX.sub('<identity>',k):signature(v,k) for k,v in value.items()}
     if isinstance(value,list):
      result=[signature(v,key) for v in value]
      return sorted(result,key=lambda x:json.dumps(x,sort_keys=True)) if key in ('result_versions','required_legal_result_versions','superseded_excluded','journal_versions_preserved','conflicts','bundle_ids') or self.version_table(value) else result
     if isinstance(value,str):return HEX.sub('<identity>',value)
     return value
    table={}
    for key,value in b['evidence_bundles'].items():table.setdefault(json.dumps(signature(value),sort_keys=True),[]).append(key)
    for key,value in a['evidence_bundles'].items():
     candidates=table.get(json.dumps(signature(value),sort_keys=True),[])
     if len(candidates)==1:self.strings(key,candidates[0],path+'/evidence_bundles/key')
   for key in set(a)&set(b):self.seed(a[key],b[key],path+'/'+key)
  elif isinstance(a,list) and isinstance(b,list):
   if self.version_table(a) and self.version_table(b):
    self.seed_versions(a,b,path)
    a=sorted(a,key=lambda x:HEX.sub(lambda m:self.forward.get(m[0],m[0]),x['version_id']));b=sorted(b,key=lambda x:x['version_id'])
   for i,(x,y) in enumerate(zip(a,b)):self.seed(x,y,path+'/'+str(i))
 def strings(self,a,b,path):
  if a!=b and (a.isdecimal() or b.isdecimal()):
   self.errors.append({'path':path,'reason':'numeric accounting or source bytes changed','old':a,'new':b});return
  aa,bb=HEX.findall(a),HEX.findall(b)
  if HEX.sub('<identity>',a)!=HEX.sub('<identity>',b) or len(aa)!=len(bb):self.errors.append({'path':path,'reason':'nonidentity bytes changed','old':a,'new':b});return
  for x,y in zip(aa,bb):self.bind(x,y,path)
  if a!=b:self.changed+=1
 def compare(self,a,b,path=''):
  if type(a)!=type(b):self.errors.append({'path':path,'reason':'type changed'});return
  if isinstance(a,dict):
   mapped={HEX.sub(lambda m:self.forward.get(m[0],m[0]),k):k for k in a}
   missing=set(mapped)-set(b);added=set(b)-set(mapped)
   # Learn new opaque key transitions only when the nonhash role is unique.
   for key in list(missing):
    candidates=[x for x in added if HEX.sub('<identity>',key)==HEX.sub('<identity>',x)]
    if len(candidates)==1:
     target=candidates[0];self.strings(mapped[key],target,path+'/key');mapped[target]=mapped.pop(key);missing.remove(key);added.remove(target)
   if missing or added:self.errors.append({'path':path,'reason':'unmatched authority keys','old_keys':sorted(missing),'new_keys':sorted(added)})
   for key in set(mapped)&set(b):self.compare(a[mapped[key]],b[key],path+'/'+key)
  elif isinstance(a,list):
   if self.version_table(a) and self.version_table(b):
    a=sorted(a,key=lambda x:HEX.sub(lambda m:self.forward.get(m[0],m[0]),x['version_id']));b=sorted(b,key=lambda x:x['version_id'])
   if path.split('/')[-1] in ('result_versions','required_legal_result_versions','superseded_excluded','journal_versions_preserved','conflicts','bundle_ids') and all(isinstance(x,str) for x in a+b):
    a=sorted(a,key=lambda x:HEX.sub(lambda m:self.forward.get(m[0],m[0]),x));b=sorted(b)
   if len(a)!=len(b):self.errors.append({'path':path,'reason':'population length changed','old':len(a),'new':len(b)})
   for i,(x,y) in enumerate(zip(a,b)):self.compare(x,y,path+'/'+str(i))
  elif isinstance(a,str):self.strings(a,b,path)
  elif a!=b:self.errors.append({'path':path,'reason':'nonidentity scalar changed','old':a,'new':b})

def expand(value):
 if isinstance(value,dict):
  if value.get('encoding') in ('gzip-base64 canonical audit JSON','gzip-base64 canonical checkpoint JSON'):
   import hashlib
   wire=gzip.decompress(base64.b64decode(value['payload']));assert hashlib.sha256(wire).hexdigest()==value['sha256'];return expand(json.loads(wire))
  return {k:expand(v) for k,v in value.items()}
 if isinstance(value,list):return [expand(v) for v in value]
 if isinstance(value,str) and value[:1] in '{[':
  try:
   parsed=json.loads(value)
   if isinstance(parsed,(dict,list)):return expand(parsed)
  except ValueError:pass
 return value
if __name__=='__main__':
 stage=sys.argv[1];folder={'2':'durable-rework-recovery','4':'full-durable-cao-integration'}[stage];base=Path(__file__).resolve().parents[2];fresh=Path(__file__).parent/('stage'+stage+'-fresh');transition=Transition();pairs=[]
 for p in fresh.glob('*.json'):
  if p.name.endswith('.differences.json') or p.name in ('comparison-summary.json','identity-transition-review.json'):continue
  old=expand(json.loads((base/'orchestration/examples'/folder/p.name).read_text()));new=expand(json.loads(p.read_text()));pairs.append((p.name,old,new));
 transition.stable=set(HEX.findall(json.dumps([a for _,a,_ in pairs]))) & set(HEX.findall(json.dumps([b for _,_,b in pairs])))
 for phase in ('versions','bundles'):
  transition.phase=phase
  for name,old,new in pairs:transition.seed(old,new,name)
 for name,old,new in pairs:transition.compare(old,new,name)
 result={'status':'PASS' if not transition.errors and pairs else 'UNRESOLVED','files':len(pairs),'changed_identity_leaves':transition.changed,'identity_map':transition.forward,'errors':transition.errors};(fresh/'identity-transition-review.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='identity_map'})[:18000])
