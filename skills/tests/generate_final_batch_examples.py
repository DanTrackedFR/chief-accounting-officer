"""Synthetic approvals only; regenerate with the normal governed runtime."""
import copy,json
from pathlib import Path
from final_batch_cases import ready,BATCH
from production import assess_case,to_public,serializable

def routes():
    return [(BATCH[0],fw,False) for fw in ('IFRS','US_GAAP','UK_GAAP','AASB')]+[(BATCH[0],'IFRS',True)]+[(p,'IFRS',False) for p in BATCH[1:]]

def artifacts(pkg,fw,accounting=False):
    c=ready(pkg,fw,accounting=accounting);r=assess_case(pkg,c)
    if r['status']!='complete':raise ValueError(r['conclusion'])
    unsigned=copy.deepcopy(c);unsigned.pop('reviewer_signoff');partial=assess_case(pkg,unsigned)
    if partial['status']!='partial':raise ValueError(partial['conclusion'])
    bad=copy.deepcopy(unsigned);bad['requested_action']='certify_compliance';blocked=assess_case(pkg,bad)
    if blocked['status']!='blocked':raise ValueError('Forbidden action accepted')
    stem='IFRS-accounting' if accounting else fw if pkg==BATCH[0] else 'practice'
    base=f'skills/{pkg}/examples/{stem}'
    return {base+'.case.json':unsigned,base+'.complete.public.json':to_public(r),base+'.partial.public.json':to_public(partial),base+'.blocked.case.json':bad,base+'.blocked.public.json':to_public(blocked)}

def generate():
    for p,fw,a in routes():
        for path,value in artifacts(p,fw,a).items():
            target=Path(path);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(value,default=serializable,indent=2)+'\n')
    # The shared implementation digest invalidates nested synthetic owner
    # certificates in previous governance and adjusting-event examples.
    # Regenerate with their existing normal generator, never hand-edit hashes.
    from generate_governance_examples import generate as prior
    prior()

if __name__=='__main__':generate()
