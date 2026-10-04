"""Normal governed generator; synthetic certifications represent no real person."""
import copy,json
from pathlib import Path
from insurance_cases import *
from production import assess_case,to_public,serializable

def scenarios():
    out=[]
    for fw in ('IFRS','AASB'):
        out += [(fw,'gmm',case(fw)),(fw,'gmm-future-increase',case(fw,future_change='30')),(fw,'gmm-future-decrease',case(fw,future_change='-20')),(fw,'gmm-onerous',case(fw,onerous=True)),(fw,'paa-acquisition-capitalized',case(fw,'paa')),(fw,'paa-acquisition-expensed',case(fw,'paa',acquisition_expense=True)),(fw,'paa-reinsurance',reinsurance_case(fw))]
    out += [('US_GAAP','short-duration',case('US_GAAP','us')),('US_GAAP','short-duration-deficiency',case('US_GAAP','us',deficiency=True))]
    return out

def artifacts():
    output={}
    for fw,name,c in scenarios():
        cc=ready(c);result=assess_case(PACKAGE,cc)
        if result['status']!='complete':raise ValueError(name+': '+result['conclusion'])
        partial=copy.deepcopy(cc);partial.pop('reviewer_signoff');bad=copy.deepcopy(partial);bad['insurance_model']='proposed_unsupported_model'
        base=Path('skills')/PACKAGE/'examples'/(fw+'-'+name)
        objects={'.case.json':partial,'.complete.public.json':to_public(result),'.partial.public.json':to_public(assess_case(PACKAGE,partial)),'.blocked.case.json':bad,'.blocked.public.json':to_public(assess_case(PACKAGE,bad))}
        for suffix,obj in objects.items():output[str(base)+suffix]=obj
    # UK route is deliberately a distinct failed native policy boundary.
    uk=base_case_uk();r=assess_case(PACKAGE,uk)
    output['skills/'+PACKAGE+'/examples/UK_GAAP-policy-boundary.blocked.case.json']=uk
    output['skills/'+PACKAGE+'/examples/UK_GAAP-policy-boundary.blocked.public.json']=to_public(r)
    return output

def base_case_uk():
    c=case('UK_GAAP','paa');c['insurance_model']='FRS103_POLICY_REVIEW';return ready(c)

def generate():
    for p,o in artifacts().items():
        path=Path(p);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(o,indent=2,default=serializable)+'\n')
if __name__=='__main__':generate()
