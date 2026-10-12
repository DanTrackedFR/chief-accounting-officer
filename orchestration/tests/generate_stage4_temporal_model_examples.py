"""Generate actual temporal lifecycle; no result or status overrides."""
import json
import io
import unittest
from dataclasses import asdict
from pathlib import Path
from orchestration.tests import stage4_temporal_fixtures as t, stage4_closing_population as whole
from orchestration.runtime import CAO

TARGET=Path(__file__).resolve().parents[1]/'examples/multi-entity-multi-period-temporal-model'


def artifacts():
    f,r=t.run();e=f['session'];n=f['nodes']
    if (f['case'].status,f['case'].outcome)!=('CLOSED','complete'):raise ValueError('Actual complete temporal lifecycle required')
    source={label:e.sources[n[label].id] for label in ('adjacent-closing','current-opening','prior-year-comparative','reporting','analytics')}
    suite=unittest.TestLoader().loadTestsFromNames([
        'orchestration.tests.test_stage4_temporal_model_independent',
        'orchestration.tests.test_stage4_final_independent'])
    stream=io.StringIO();adversarial=unittest.TextTestRunner(stream=stream,verbosity=1).run(suite)
    if not adversarial.wasSuccessful():raise ValueError(stream.getvalue())
    return {
        'reviewed-temporal-evidence.json':source,
        'temporal-dependencies.json':dict(period_registry=e.periods.record(),dependencies=[dict(asdict(v),id=k) for k,v in sorted(e.edges.items())],receipts=e.receipts),
        'original-conflict-and-corrections.json':dict(original={k:asdict(v) for k,v in r['before'].items()},payable_correction=r['payable_correction'],closing_correction=r['closing_correction'],rework=r['ledger']),
        'current-reporting-and-analytics.json':{label:asdict(e.versions.current(n[label].id)) for label in ('elimination','adjacent-closing','current-opening','prior-year-comparative','reporting','analytics','group')},
        'versions-and-invalidation.json':dict(versions=e.versions.record(),supersession=e.versions.supersession,rework=e.rework_history),
        'exact-once.json':whole.exact_once(f),
        'eight-accepted-lineages.json':t.lineages(f,r),
        'governed-source-intake.json':dict(raw_sources=[asdict(x) for x in f['raw_sources']],reviewed_pack=asdict(f['reviewed_pack']),validation=f['intake'].validation,lineage=f['intake'].lineage),
        'adversarial-results.json':dict(methods=adversarial.testsRun,failures=len(adversarial.failures),errors=len(adversarial.errors),skipped=len(adversarial.skipped),result='PASS',reruns_not_additional_distinct_tests=True),
        'current-case-and-public-answer.json':dict(status=f['case'].status,outcome=f['case'].outcome,public_answer=CAO().public(f['case'])),
    }


def main():
    TARGET.mkdir(parents=True,exist_ok=True)
    for name,value in artifacts().items():(TARGET/name).write_text(json.dumps(value,sort_keys=True,indent=2,default=str)+'\n')


if __name__=='__main__':main()
