"""Regenerate synthetic diagnostic artifacts through governed public/native gates."""
import json
from pathlib import Path
from orchestration import CAO
from orchestration.tests.diagnostic_fixtures import diagnostic_manufacturing
from orchestration.tests.generate_examples import internal_record

def artifacts():
    request=diagnostic_manufacturing();cao=CAO();case=cao.run(request)
    if case.outcome!='complete':raise AssertionError((case.open_questions,[(n['id'],n['open_items']) for n in case.workplan_nodes if n['status']!='complete']))
    d=case.diagnostics[0]
    return {'factory-diagnostic.public.json':cao.public(case),'factory-diagnostic.case.internal.json':internal_record(case),
        'factory-diagnostic.bridge.json':d['bridge'],'factory-diagnostic.hypotheses.json':d['hypotheses'],
        'factory-diagnostic.attribution-ledger.json':d['attribution_ledger'],'factory-diagnostic.accounting-questions.json':case.accounting_questions,
        'factory-diagnostic.intent.json':case.work_modes,'factory-diagnostic.graph.json':[{k:v for k,v in n.items() if k not in ('result','invalidated_results','evidence')} for n in case.workplan_nodes],
        'factory-diagnostic.challenge.json':case.challenge_results,'factory-diagnostic.memory-candidates.json':case.memory_candidates}

def main():
    target=Path(__file__).resolve().parents[1]/'examples'
    for name,value in artifacts().items():(target/name).write_text(json.dumps(value,sort_keys=True,indent=2,default=str)+'\n')
if __name__=='__main__':main()
