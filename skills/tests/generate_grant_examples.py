"""Reproduce new synthetic grant accounting examples; never rewrite historical owners."""
import argparse
import hashlib
import json
from pathlib import Path
from grant_cases import case,ready,capture
from production import assess_case,to_public,serializable

ROOT=Path(__file__).resolve().parents[2]

def examples():
    values={}
    for fw,route in [('IFRS','income'),('IFRS','asset'),('IFRS','deduction'),('AASB','income'),('UK_GAAP','performance'),('UK_GAAP','income'),('US_GAAP','income'),('US_GAAP','cost_accumulation'),('IFRS','advance'),('IFRS','past'),('IFRS','repayment'),('IFRS','nonmonetary')]:values[fw.lower()+'-'+route]=(ready(fw,route),'complete')
    changes={
      'conditional-missing-compliance':lambda c:c['grants'][0]['conditions'][0].pop('compliance_memo'),
      'procurement':lambda c:c['grants'][0].update(substance='procurement'),
      'income-tax-assistance':lambda c:c['grants'][0].update(substance='income_tax'),
      'loan-forgiveness-boundary':lambda c:c['grants'][0].update(substance='loan'),
      'missing-eligible-costs':lambda c:c['grants'][0].pop('eligible_costs'),
      'wrong-framework':lambda c:c['grants'][0].update(source_framework='US_GAAP'),
      'duplicate-owner':lambda c:c['journal_ownership'][0].update(accounting_owner='revenue-recognition'),
      'entity-mismatch':lambda c:c['grants'][0].update(source_entity='Another entity'),
      'period-mismatch':lambda c:c['grants'][0].update(source_period=['2025-01-01','2025-12-31']),
      'currency-mismatch':lambda c:c['grants'][0].update(currency='USD')}
    for name,change in changes.items():
        c=case();change(c);capture(c);values[name]=(ready(c=c),'blocked')
    c=case('US_GAAP','nonmonetary');c['grants'][0]['presentation']='cost_accumulation';c['accounting_policy']['presentation_by_class']['asset']='cost_accumulation';capture(c);values['us-nonmonetary-cost-accumulation']=(ready(c=c),'blocked')
    c=case();c['grants'][0]['payments']=[];c['grants'][0]['payment_inventory']=[];c['grants'][0]['expected']['closing_receivable']='100';c['grants'][0]['disclosure']['closing_receivable']='100'
    for r in c['gl']:
        if r['id']=='Grant receivable':r.update(closing='100',statement='100')
        if r['id']=='Grant cash':r.update(closing='0',statement='0')
    capture(c);values['evidenced-unpaid-entitlement']=(ready(c=c),'complete')
    c=case('US_GAAP');c.pop('us_adoption');values['us-nonadopter']=(ready(c=c),'blocked')
    c=case('IFRS','nonmonetary');c['grants'][0].pop('valuation');capture(c);values['missing-valuation']=(ready(c=c),'blocked')
    c=case();c['period_start']='2025-01-01';c['applicability_review']['effective_period'][0]='2025-01-01';values['unsupported-period']=(ready(c=c),'blocked')
    c=ready();c.pop('reviewer_signoff');values['uncertified']=(c,'partial')
    return values


def generate(output):
    output.mkdir(parents=True,exist_ok=True);manifest={};statuses={}
    def write(name,value):
        raw=(json.dumps(value,sort_keys=True,indent=2,default=serializable)+'\n').encode();(output/name).write_bytes(raw);manifest[name]=hashlib.sha256(raw).hexdigest()
    for name,(c,expected) in examples().items():
        r=assess_case('government-grants',c)
        if r['status']!=expected:raise AssertionError((name,r['status'],r['conclusion']))
        if expected!='complete' and r['journal_entry_implications']:raise AssertionError('Uncertified journals')
        statuses[name]=expected
        for kind,value in [('case',c),('result',r),('public',to_public(r)),('schedule',r['calculations']),('journals',r['journal_entry_implications'])]:write(name+'.'+kind+'.json',value)
    write('source-evidence-manifest.json',dict(scope='Synthetic independently reviewed 2026 source agreements and owner cost records; no human authentication or ERP posting',statuses=statuses,files=manifest.copy()))
    (output/'SHA256SUMS.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    return dict(files=len(manifest)+1,cases=len(statuses),statuses=statuses)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'skills/government-grants/examples/production');args=parser.parse_args();print(json.dumps(generate(args.output),sort_keys=True))
