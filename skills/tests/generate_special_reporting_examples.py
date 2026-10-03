"""Regenerate synthetic cases and public workpapers through governed runtime."""
import copy,json
from pathlib import Path
from special_reporting_cases import *
from production import assess_case,to_public,serializable

def artifacts(pkg,fw):
    c=ready(pkg,fw) if pkg not in BLOCKED else case(pkg,fw)
    r=assess_case(pkg,c);stem=f'skills/{pkg}/examples/{fw}'
    if r['status']=='blocked':return {stem+'.case.json':c,stem+'.blocked.public.json':to_public(r)}
    if r['status']!='complete':raise ValueError(r['conclusion'])
    unsigned=copy.deepcopy(c);unsigned.pop('reviewer_signoff');partial=assess_case(pkg,unsigned)
    assert partial['status']=='partial'
    return {stem+'.case.json':unsigned,stem+'.complete.public.json':to_public(r),stem+'.partial.public.json':to_public(partial)}

def generate():
    for pkg in PACKAGES+BLOCKED:
        for fw in FRAMEWORKS:
            for p,v in artifacts(pkg,fw).items():
                path=Path(p);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(v,default=serializable,indent=2)+'\n')
    # Shared implementation fingerprint invalidates embedded adjusting-owner proofs.
    from generate_presentation_examples import artifacts as prior_artifacts
    for fw in FRAMEWORKS:
        for p,v in prior_artifacts('subsequent-events',fw,'adjusting').items():
            Path(p).write_text(json.dumps(v,default=serializable,indent=2)+'\n')
if __name__=='__main__':generate()
