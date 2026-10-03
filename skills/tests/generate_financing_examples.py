"""Emit clearly synthetic example files for apply_patch; never issue company approval."""
import copy,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from financing_cases import case,ready,FRAMEWORKS,PACKAGES
from production import assess_case,to_public,serializable

def artifacts(package,framework):
    if package=='inventory-cost':
        c=case(package,framework);r=assess_case(package,c)
        return {f'skills/{package}/examples/{framework}.case.json':c,
            f'skills/{package}/examples/{framework}.blocked.public.json':to_public(r)}
    c=ready(package,framework);r=assess_case(package,c)
    if r['status']!='complete':raise ValueError(r['conclusion'])
    unsigned=copy.deepcopy(c);unsigned.pop('reviewer_signoff');partial=assess_case(package,unsigned)
    if partial['status']!='partial':raise ValueError(partial['conclusion'])
    return {f'skills/{package}/examples/{framework}.case.json':unsigned,
        f'skills/{package}/examples/{framework}.partial.public.json':to_public(partial),
        f'skills/{package}/examples/{framework}.complete.public.json':to_public(r)}

if __name__=='__main__':
    print(json.dumps({p:json.dumps(v,default=serializable,indent=2)+'\n' for p,v in artifacts(sys.argv[1],sys.argv[2]).items()}))
