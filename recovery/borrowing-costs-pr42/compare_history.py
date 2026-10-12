"""Capture fresh proof separately; compare without rewriting historical authority."""
import base64,gzip,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from orchestration.persistence.codec import loads

def expanded(value):
    if isinstance(value,dict):
        if value.get('encoding')=='gzip-base64 canonical audit JSON':
            wire=gzip.decompress(base64.b64decode(value['payload']))
            assert hashlib.sha256(wire).hexdigest()==value['sha256']
            return expanded(loads(wire.decode()))
        return {k:expanded(v) for k,v in value.items()}
    if isinstance(value,list):return [expanded(v) for v in value]
    return value

def differences(a,b,path='',out=None):
    if out is None:out=[]
    if type(a)!=type(b):out.append(dict(path=path,old=a,new=b));return out
    if isinstance(a,dict):
        for k in sorted(set(a)|set(b)):
            if k not in a or k not in b:out.append(dict(path=path+'/'+k,old=a.get(k),new=b.get(k)))
            else:differences(a[k],b[k],path+'/'+k,out)
    elif isinstance(a,list):
        if len(a)!=len(b):out.append(dict(path=path+'/length',old=len(a),new=len(b)))
        for i,(x,y) in enumerate(zip(a,b)):differences(x,y,path+'/'+str(i),out)
    elif a!=b:out.append(dict(path=path,old=a,new=b))
    return out

if __name__=='__main__':
    stage=sys.argv[1]
    if stage=='2':from orchestration.tests.generate_persistence_stage2_examples import artifacts,TARGET
    else:from orchestration.tests.generate_persistence_stage4_examples import artifacts,TARGET
    dest=Path(__file__).parent/('stage'+stage+'-fresh');dest.mkdir(exist_ok=True)
    values=artifacts();summary={}
    for name,value in values.items():
        (dest/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
        old=json.loads((TARGET/name).read_text());delta=differences(expanded(old),expanded(value))
        (dest/(name+'.differences.json')).write_text(json.dumps(delta,indent=2,sort_keys=True)+'\n')
        summary[name]=len(delta)
    (dest/'comparison-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary)
