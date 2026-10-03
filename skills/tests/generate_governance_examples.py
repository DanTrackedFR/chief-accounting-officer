"""Regenerate explicitly synthetic governance artifacts through normal runtime."""
import copy,json
from pathlib import Path
from governance_cases import *
from production import assess_case,to_public,serializable

def artifacts(pkg,fw):
    c=ready(pkg,fw);result=assess_case(pkg,c)
    if result['status']!='complete':raise ValueError(result['conclusion'])
    unsigned=copy.deepcopy(c);unsigned.pop('reviewer_signoff');partial=assess_case(pkg,unsigned)
    if partial['status']!='partial':raise ValueError(partial['conclusion'])
    bad=copy.deepcopy(unsigned);bad['requested_action']='certify_compliance';blocked=assess_case(pkg,bad)
    if blocked['status']!='blocked':raise ValueError('Forbidden action accepted')
    stem=f'skills/{pkg}/examples/{fw}'
    return {stem+'.case.json':unsigned,stem+'.complete.public.json':to_public(result),stem+'.partial.public.json':to_public(partial),stem+'.blocked.case.json':bad,stem+'.blocked.public.json':to_public(blocked)}

def generate():
    for pkg in BATCH:
        for fw in FRAMEWORKS:
            for path,value in artifacts(pkg,fw).items():
                p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,default=serializable,indent=2)+'\n')
    # Existing global implementation fingerprint covers the new packages/helper.
    # Preserve prior accounting; regenerate only embedded synthetic certificates.
    from generate_presentation_examples import artifacts as prior
    for fw in FRAMEWORKS:
        for path,value in prior('subsequent-events',fw,'adjusting').items():Path(path).write_text(json.dumps(value,default=serializable,indent=2)+'\n')
if __name__=='__main__':generate()
