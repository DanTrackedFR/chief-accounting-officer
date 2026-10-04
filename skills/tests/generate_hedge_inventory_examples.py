"""Governed synthetic downstream handoff examples, without copying owner journals."""
import copy
import json
from pathlib import Path
from test_hedge_inventory_integration import inventory_handoff_case
from inventory_cases import ready
from production import assess_case,to_public,serializable

def artifacts():
    output={}
    for fw in ('IFRS','AASB','UK_GAAP'):
        c=ready(c=inventory_handoff_case(fw));complete=assess_case('inventory-cost',c)
        if complete['status']!='complete':raise ValueError(complete['conclusion'])
        unsigned=copy.deepcopy(c);unsigned.pop('reviewer_signoff')
        bad=copy.deepcopy(unsigned);bad['imports'][0]['result']['calculations']['basis_adjustments'][0]['amount']='-91'
        partial=assess_case('inventory-cost',unsigned);blocked=assess_case('inventory-cost',bad)
        if partial['status']!='partial' or blocked['status']!='blocked':raise ValueError('Handoff certification or mutation gate failed')
        stem=Path('skills/inventory-cost/examples')/(fw+'-hedge-basis')
        for suffix,obj in {'.case.json':unsigned,'.complete.public.json':to_public(complete),'.partial.public.json':to_public(partial),'.blocked.case.json':bad,'.blocked.public.json':to_public(blocked)}.items():output[str(stem)+suffix]=obj
    return output

def generate():
    for p,o in artifacts().items():Path(p).write_text(json.dumps(o,default=serializable,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':generate()
