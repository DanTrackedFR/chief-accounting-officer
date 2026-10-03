"""Emit labelled synthetic artifacts to stdout; caller saves through apply_patch."""
import json,sys,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from presentation_cases import *
from production import assess_case,to_public,serializable

def artifacts(pkg,fw,variant='ordinary'):
    if pkg in BLOCKED:
        c=case(pkg,fw);return {f'skills/{pkg}/examples/{fw}.case.json':c,f'skills/{pkg}/examples/{fw}.blocked.public.json':to_public(assess_case(pkg,c))}
    c=ready(pkg,fw,adjusting(fw) if variant=='adjusting' else None);r=assess_case(pkg,c)
    if r['status']!='complete':raise ValueError(r['conclusion'])
    unsigned=copy.deepcopy(c);unsigned.pop('reviewer_signoff');partial=assess_case(pkg,unsigned)
    if partial['status']!='partial':raise ValueError(partial['conclusion'])
    stem=f'skills/{pkg}/examples/{fw}'+('.adjusting' if variant=='adjusting' else '')
    return {stem+'.case.json':unsigned,stem+'.complete.public.json':to_public(r),stem+'.partial.public.json':to_public(partial)}

if __name__=='__main__':print(json.dumps({p:json.dumps(v,default=serializable,indent=2)+'\n' for p,v in artifacts(*sys.argv[1:]).items()}))
