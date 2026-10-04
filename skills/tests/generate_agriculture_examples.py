"""Reproduce Agriculture worked examples using the normal governed public runtime."""
import copy,json
from pathlib import Path
from agriculture_cases import case,ready,PACKAGE,sources,disclosure_support,content
from production import assess_case,to_public,serializable

def artifacts():
    output={}
    routes=[(fw,kind,case(fw,kind)) for fw in ('IFRS','UK_GAAP','AASB','US_GAAP') for kind in (('livestock','crop') if fw!='US_GAAP' else ('livestock',))]
    from test_independent_agriculture import birth_case,death_case,negative_gain_case,specimen
    routes += [(fw,'birth',birth_case(fw)) for fw in ('IFRS','UK_GAAP','AASB')]
    routes += [('IFRS','death',death_case()),('IFRS','loss',negative_gain_case())]
    for fw,kind,category in [('IFRS','bearer-animal','bearer_livestock'),('UK_GAAP','bearer-plant','bearer_plant'),('IFRS','growing-produce','growing_produce')]:
        c=specimen(fw);c['assets'][0]['category']=category;c['accounting_policy']['class_models'][category]='fair_value_less_costs_to_sell'
        content(c,'live-class')['category']=category;content(c,'live-closing')['category']=category
        routes.append((fw,kind,sources(disclosure_support(c))))
    for fw,kind,source in routes:
            c=ready(c=source,release=True);r=assess_case(PACKAGE,c)
            if fw!='US_GAAP' and r['status']!='complete':raise ValueError(r['conclusion'])
            if fw=='US_GAAP' and r['status']!='blocked':raise ValueError('US route silently completed')
            unsigned=copy.deepcopy(c);unsigned.pop('reviewer_signoff')
            partial=assess_case(PACKAGE,unsigned)
            bad=copy.deepcopy(unsigned);bad['classification']['post_harvest_accounting']=True
            blocked=assess_case(PACKAGE,bad)
            root=Path('skills')/PACKAGE/'examples'
            stem=fw+'-'+kind
            outputs={'.case.json':unsigned,'.'+r['status']+'.public.json':to_public(r)}
            if fw!='US_GAAP':outputs.update({'.partial.public.json':to_public(partial),'.blocked.case.json':bad,'.blocked.public.json':to_public(blocked)})
            for suffix,obj in outputs.items():output[str(root/(stem+suffix))]=obj
    return output

def generate():
    for path,obj in artifacts().items():
        target=Path(path);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(obj,indent=2,default=serializable)+'\n')
    # Changes to shared execution bytes stale previous synthetic certifications.
    # Regenerate through their existing generator, never amend real approvals.
    from generate_final_batch_examples import generate as prior
    prior()

if __name__=='__main__':generate()
