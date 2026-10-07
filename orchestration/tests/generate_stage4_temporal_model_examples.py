"""Generate actual temporal lifecycle; no result or status overrides."""
import json
from dataclasses import asdict
from pathlib import Path
from orchestration.tests import stage4_temporal_fixtures as t, stage4_closing_population as whole
from orchestration.runtime import CAO

TARGET=Path(__file__).resolve().parents[1]/'examples/multi-entity-multi-period-temporal-model'


def artifacts():
    f,r=t.run();e=f['session'];n=f['nodes']
    if (f['case'].status,f['case'].outcome)!=('CLOSED','complete'):raise ValueError('Actual complete temporal lifecycle required')
    source={label:e.sources[n[label].id] for label in ('adjacent-closing','current-opening','prior-year-comparative','reporting','analytics')}
    return {
        'reviewed-temporal-evidence.json':source,
        'temporal-dependencies.json':dict(period_registry=e.periods.record(),dependencies=[dict(asdict(v),id=k) for k,v in sorted(e.edges.items())],receipts=e.receipts),
        'original-conflict-and-corrections.json':dict(original={k:asdict(v) for k,v in r['before'].items()},payable_correction=r['payable_correction'],closing_correction=r['closing_correction'],rework=r['ledger']),
        'current-reporting-and-analytics.json':{label:asdict(e.versions.current(n[label].id)) for label in ('elimination','adjacent-closing','current-opening','prior-year-comparative','reporting','analytics','group')},
        'versions-and-invalidation.json':dict(versions=e.versions.record(),supersession=e.versions.supersession,rework=e.rework_history),
        'exact-once.json':whole.exact_once(f),
        'current-case-and-public-answer.json':dict(status=f['case'].status,outcome=f['case'].outcome,public_answer=CAO().public(f['case']),stage4_release='NOT YET CERTIFIED; final independent QA and release gates remain'),
    }


def main():
    TARGET.mkdir(parents=True,exist_ok=True)
    for name,value in artifacts().items():(TARGET/name).write_text(json.dumps(value,sort_keys=True,indent=2,default=str)+'\n')


if __name__=='__main__':main()
