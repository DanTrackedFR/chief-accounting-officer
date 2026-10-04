"""Normal generator produces governed complete/partial/blocked synthetic examples."""
import copy,json
from pathlib import Path
from hedge_cases import *
from production import assess_case,to_public,serializable

def artifacts():
    output={};routes=[]
    for fw in ('IFRS','AASB','US_GAAP','UK_GAAP'):
        routes += [(fw,'standalone-forward',case(fw)),(fw,'cashflow-pending',case(fw,'cash_flow')),(fw,'cashflow-cancelled',case(fw,'cash_flow','no_longer_expected')),(fw,'cashflow-acquisition',case(fw,'cash_flow','occurred')),(fw,'fairvalue-commitment',fair_value_case(fw)),(fw,'fairvalue-debt',debt_case(fw,'fair_value')),(fw,'cashflow-variable-debt',debt_case(fw,'cash_flow')),(fw,'net-investment',net_investment_case(fw))]
    for name in ('late-documentation','swap-liability-settlement','discontinue-expected','forecast-sale'):
        for fw in ('IFRS','AASB','US_GAAP','UK_GAAP'):routes.append((fw,name,special_case(name,fw)))
    for name in ('rebalancing','cumulative-reversal'):
        for fw in ('IFRS','AASB'):routes.append((fw,name,special_case(name,fw)))
    for fw,name,c in routes:
        complete=assess_case(PACKAGE,ready(c));
        if complete['status']!='complete':raise ValueError(name+': '+str(complete))
        partial=ready(c);partial.pop('reviewer_signoff');bad=copy.deepcopy(partial);bad['model']='unsupported_proposed_model'
        base=Path('skills')/PACKAGE/'examples'/(fw+'-'+name)
        for suffix,obj in {'.case.json':partial,'.complete.public.json':to_public(complete),'.partial.public.json':to_public(assess_case(PACKAGE,partial)),'.blocked.case.json':bad,'.blocked.public.json':to_public(assess_case(PACKAGE,bad))}.items():output[str(base)+suffix]=obj
    return output

def generate():
    for p,o in artifacts().items():
        path=Path(p);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(o,indent=2,default=serializable)+'\n')
if __name__=='__main__':generate()
