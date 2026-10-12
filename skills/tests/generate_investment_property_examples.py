"""Generate only new synthetic IP artifacts; never rewrite historical CAO examples."""
import hashlib
import json
from pathlib import Path
import sys
from investment_property_cases import case,ready,capture
from production import assess_case,to_public

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'skills/investment-property/examples/production'

def encoding(obj):return json.dumps(obj,sort_keys=True,indent=2,default=str)+'\n'
def digest(text):return hashlib.sha256(text.encode()).hexdigest()

def cases():
 for fw in ['IFRS','AASB','UK_GAAP','US_GAAP']:
  models=['cost','fair_value'] if fw in ['IFRS','AASB'] else ['fair_value','group_cost'] if fw=='UK_GAAP' else ['cost']
  for model in models:
   for route in ['initial','hold','disposal']:
    yield fw+'-'+model+'-'+route,ready(fw,model,route),'complete'
  model='cost' if fw=='US_GAAP' else 'fair_value'
  yield fw+'-mixed-separable',ready(fw,model,mixed='separable'),'complete'
 for fw in ['IFRS','AASB']:
  for route,model in [('transfer_in_cost','cost'),('transfer_out_cost','cost'),('transfer_out_fv','fair_value')]:
   yield fw+'-'+route,ready(fw,model,route),'complete'
 yield 'unsupported-us-fair-value',ready('US_GAAP','fair_value'),'blocked'
 yield 'unsupported-uk-cost-election',ready('UK_GAAP','cost'),'blocked'
 mutations={
  'missing-material-evidence':lambda c:c['valuation'].update(evidence=''),
  'unsupported-valuation':lambda c:c['valuation'].update(basis='asking_price'),
  'cross-framework-leakage':lambda c:c['valuation'].update(framework='US_GAAP'),
  'entity-mismatch':lambda c:c['valuation'].update(legal_entity='Another entity'),
  'currency-mismatch':lambda c:c['valuation'].update(currency='USD'),
  'period-mismatch':lambda c:c['valuation'].update(period=['2025-01-01','2025-12-31']),
  'duplicate-journal-owner':lambda c:c['ownership_register'][0].update(accounting_owner='Fair Value'),
  'wrong-prior-model':lambda c:c['properties'][0]['opening_history'].update(measurement_model='cost'),
 }
 for name,mutate in mutations.items():
  c=case();mutate(c);capture(c);yield name,ready(c=c),'blocked'
 c=ready();del c['reviewer_signoff'];yield 'incomplete-certification',c,'partial'

def artifacts():
 files={};scenarios=[]
 for name,c,expected in cases():
  r=assess_case('investment-property',c)
  assert r['status']==expected,(name,r['status'],r.get('open_items'))
  items={'case':c,'result':r,'public':to_public(r),'schedule':r['calculations'],'journals':r['journal_entry_implications']}
  for suffix,obj in items.items():files[name+'.'+suffix+'.json']=encoding(obj)
  source=encoding(c['original_source_snapshot'])
  scenarios.append(dict(name=name,expected_status=expected,source_sha256=digest(source),case_sha256=digest(files[name+'.case.json']),expected_calculations=r['calculations'],journal_count=len(r['journal_entry_implications']),synthetic=True))
 files['source-evidence-manifest.json']=encoding(dict(namespace='new-investment-property-synthetic-examples-only',historical_files_rewritten=False,scenarios=scenarios,files={name:digest(text) for name,text in sorted(files.items())}))
 return files

def main():
 files=artifacts()
 if '--verify' in sys.argv:
  assert OUT.exists(),'Examples absent'
  assert {p.name for p in OUT.iterdir() if p.is_file()}==set(files),'Example population differs'
  for name,text in files.items():assert (OUT/name).read_text()==text,('Reproduction differs',name)
 else:
  OUT.mkdir(parents=True,exist_ok=True)
  for name,text in files.items():(OUT/name).write_text(text)
 print(encoding(dict(status='PASS',files=len(files),scenarios=sum(name.endswith('.case.json') for name in files),mode='verify' if '--verify' in sys.argv else 'generate')))

if __name__=='__main__':main()
