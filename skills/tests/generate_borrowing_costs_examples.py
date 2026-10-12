#!/usr/bin/env python3
"""Generate deterministic reviewed accounting examples from the production boundary."""
import argparse
import hashlib
import json
from pathlib import Path
from copy import deepcopy
from borrowing_costs_cases import case,ready,remeasure,capture_sources
from operational_cases import approved
from production import assess_case,to_public,serializable

ROOT=Path(__file__).resolve().parents[2]

def generate(output):
    output.mkdir(parents=True,exist_ok=True)
    cases={}
    for fw,method in [('IFRS','specific'),('AASB','general'),('US_GAAP','specific'),('UK_GAAP','general')]:
        c=case(fw,method)
        if fw=='IFRS':c['borrowings'][0]['segments'][0]['investment_income']='1000'
        if fw=='AASB':
            p=c['projects'][0];p['expenditures'][0]['amount']='180000'
            b=c['borrowings'][0];b['opening_principal']='650000';b['segments'][0]['annual_rate']=b['segments'][0]['effective_annual_rate']='.075'
        if fw=='US_GAAP':c['projects'][0]['expenditures'][0]['amount']='125000'
        if fw=='UK_GAAP':c['projects'][0]['opening_capitalized']='5000'
        remeasure(c);capture_sources(c);cases[fw.lower()+'-'+method]=c
    cases['ifrs-mixed']=case()
    suspended=case();p=suspended['projects'][0];p['timeline'][0].update(state='suspended',extended=True,substantial_technical_activity=False);remeasure(suspended);capture_sources(suspended);cases['suspended']=suspended
    completed=case();p=completed['projects'][0];p['ready_date']='2026-07-01';p['timeline'][0]['end']='2026-06-30';t=deepcopy(p['timeline'][0]);t.update(id='ready',start='2026-07-01',end='2026-12-31',state='complete');p['timeline'].append(t);p['timeline_inventory'].append('ready');remeasure(completed);capture_sources(completed);cases['completed']=completed
    before=case();p=before['projects'][0];p['activity_start']='2026-07-01';p['timeline'][0]['end']='2026-06-30';p['timeline'][0]['state']='pre';t=deepcopy(p['timeline'][0]);t.update(id='construction',start='2026-07-01',end='2026-12-31',state='active');p['timeline'].append(t);p['timeline_inventory'].append('construction');remeasure(before);capture_sources(before);cases['before-commencement']=before
    timed=case(method='general');b=timed['borrowings'][0];b['events']=[approved('draw',date='2026-04-01',kind='draw',amount='100000'),approved('repay',date='2026-10-01',kind='repayment',amount='50000')];b['event_inventory']=['draw','repay'];s=b['segments'][0];s['end']='2026-06-30';t=deepcopy(s);t.update(id='reset',start='2026-07-01',end='2026-12-31',annual_rate='.09',effective_annual_rate='.09');b['segments'].append(t);b['segment_inventory'].append('reset');remeasure(timed);capture_sources(timed);cases['dated-financing']=timed
    negative=case();negative['projects'][0]['shared_components']=True;capture_sources(negative);cases['unsupported-shared-components']=negative
    manifest={}
    def write(name,value):
        raw=(json.dumps(value,sort_keys=True,indent=2,default=serializable)+'\n').encode();(output/name).write_bytes(raw);manifest[name]=hashlib.sha256(raw).hexdigest()
    for name,c in cases.items():
        c=ready(c=c);r=assess_case('borrowing-costs',c)
        expected='blocked' if name=='unsupported-shared-components' else 'complete'
        if r['status']!=expected:raise RuntimeError(name+': '+r['conclusion'])
        write(name+'.case.json',c);write(name+'.result.json',r);write(name+'.public.json',to_public(r))
        if r['status']=='complete':
            write(name+'.schedule.json',r['calculations'])
            write(name+'.journals.json',r['journal_entry_implications'])
    partial=ready();partial.pop('reviewer_signoff');r=assess_case('borrowing-costs',partial)
    if r['status']!='partial' or r['journal_entry_implications']:raise RuntimeError('Uncertified journals released')
    write('uncertified.case.json',partial);write('uncertified.result.json',r);write('uncertified.public.json',to_public(r))
    write('source-evidence-manifest.json',dict(namespace='SUPPLEMENTAL_BORROWING_COSTS',example_scope='Synthetic 2026 tangible construction, reviewed original evidence and separate framework calculations',files=manifest.copy(),method_cases=list(cases)))
    (output/'SHA256SUMS.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
    return manifest

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'skills/borrowing-costs/examples/production');args=parser.parse_args();manifest=generate(args.output);print(json.dumps({'files':len(manifest)+1,'status':'PASS'},sort_keys=True))
