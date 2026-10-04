"""Normal governed generator for synthetic Inventory/manufacturing workpapers."""
import copy,json
from pathlib import Path
from inventory_cases import *
from production import assess_case,to_public,serializable

def artifacts():
    output={};routes=[]
    for fw in ('IFRS','US_GAAP','UK_GAAP','AASB'):
        for co in ('actual','standard'):routes.append((fw,'manufacturing-'+co,case(fw,costing=co)))
        for formula in ('FIFO','WEIGHTED_AVERAGE','SPECIFIC_IDENTIFICATION'):routes.append((fw,'resale-'+formula,case(fw,'resale',formula=formula)))
        routes += [(fw,'write-down',valuation_case(fw)),(fw,'recovery-no-reversal' if fw=='US_GAAP' else 'reversal',valuation_case(fw,True)),(fw,'over-recovery',over_recovery_case(fw))]
    routes += [('IFRS','material-return',return_case()),('IFRS','standard-material-return',return_case('standard')),('IFRS','high-output',high_capacity_case()),('US_GAAP','LIFO',case('US_GAAP','resale',formula='LIFO')),('US_GAAP','LCM',valuation_case('US_GAAP',False,'LIFO'))]
    routes += [('IFRS','company-grouped-variances',grouped_standard_case()),('IFRS','purchase-standard-PPV',purchase_standard_case()),('IFRS','count-shortage',count_case()),('IFRS','goods-in-transit',location_case('Goods in transit')),('IFRS','owned-third-party',location_case()),('IFRS','normal-scrap',loss_case())]
    for architecture in ('job','batch','process'):
        c=case();c['orders'][0]['architecture']=architecture;routes.append(('IFRS',architecture,sources(c)))
    from test_independent_inventory_cost import owner_case,agriculture_intake_case
    for pkg in ('fixed-assets','employee-benefits-payroll','accounts-payable','foreign-currency'):
        routes.append(('IFRS','owner-'+pkg,owner_case(pkg)))
    routes.append(('IFRS','agriculture-harvest',agriculture_intake_case()))
    routes += [(fw,'raw-finished-goods-'+('recoverable' if recoverable else 'unrecoverable'),raw_context_case(fw,recoverable)) for fw in ('IFRS','US_GAAP','UK_GAAP','AASB') for recoverable in (True,False)]
    for fw,kind,c in routes:
        c=ready(c=c);r=assess_case(PACKAGE,c)
        if r['status']!='complete':raise ValueError(kind+': '+r['conclusion'])
        unsigned=copy.deepcopy(c);unsigned.pop('reviewer_signoff');partial=assess_case(PACKAGE,unsigned)
        bad=copy.deepcopy(unsigned);bad['scope']['borrowing_capitalization']=True;blocked=assess_case(PACKAGE,bad)
        base=Path('skills')/PACKAGE/'examples'/(fw+'-'+kind)
        for suffix,obj in {'.case.json':unsigned,'.complete.public.json':to_public(r),'.partial.public.json':to_public(partial),'.blocked.case.json':bad,'.blocked.public.json':to_public(blocked)}.items():output[str(base)+suffix]=obj
    from generate_financing_examples import artifacts as historical
    for framework in ('IFRS','US_GAAP','UK_GAAP','AASB'):output.update(historical(PACKAGE,framework))
    return output

def generate():
    for path,obj in artifacts().items():Path(path).write_text(json.dumps(obj,indent=2,default=serializable)+'\n')
    from generate_agriculture_examples import generate as prior
    prior()
if __name__=='__main__':generate()
