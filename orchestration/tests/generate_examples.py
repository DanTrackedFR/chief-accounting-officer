"""Regenerate reproducible governed workpapers, no real-case certification."""
import copy,json
from pathlib import Path
from orchestration import CAO
from orchestration.tests.fixtures import manufacturing
ROOT=Path(__file__).resolve().parents[2]

def internal_record(case):
    record=case.record()
    # Source documents/claim registers remain in their governed owner locations.
    # This export is a reference workpaper; the in-memory full record is unchanged.
    record['evidence_refs']=[{k:r[k] for k in ('topic_id','claim_id') if k in r} for r in record['evidence_refs']]
    for node in record['workplan_nodes']:
        node['evidence']=[{k:r[k] for k in ('topic_id','claim_id') if k in r} for r in node['evidence']]
        for result in [node['result']]+node.get('invalidated_results',[]):
            if not result:continue
            for key in ('facts_used','reviewed_claims','knowledge_documents','evidence'):result.pop(key,None)
    return record

def artifacts():
    cao=CAO();request=manufacturing();case=cao.run(request)
    if case.outcome!='complete':raise AssertionError(case.open_questions)
    out={'manufacturing.case.internal.json':internal_record(case),'manufacturing.public.json':cao.public(case),
        'manufacturing.graph.json':[{k:v for k,v in n.items() if k not in ('result','evidence','invalidated_results')} for n in case.workplan_nodes],
        'manufacturing.handoffs.json':case.handoff_ledger,'manufacturing.journals.json':case.conclusions[0]['journals'],
        'manufacturing.challenge.json':case.challenge_results,'manufacturing.memory-candidates.json':case.memory_candidates,
        'manufacturing.execution-ledger.json':case.execution_ledger,'manufacturing.issue-register.json':case.accounting_issues,
        'manufacturing.reconciliation-summary.json':case.conclusions[0]['calculations']}
    partial=copy.deepcopy(request);partial['facts']['grant']=dict(agreement={'amount':'50000','source':'Synthetic government subsidy agreement'},material=True)
    c=cao.run(partial);out['manufacturing.partial.public.json']=cao.public(c);out['manufacturing.partial.graph.json']=[{k:v for k,v in n.items() if k not in ('result','evidence','invalidated_results')} for n in c.workplan_nodes]
    contradiction=copy.deepcopy(request);contradiction['challenge_assertions'][0]['evidence_value']='45725'
    c=cao.run(contradiction);out['manufacturing.contradiction.public.json']=cao.public(c);out['manufacturing.contradiction.challenge.json']=c.challenge_results
    simple=copy.deepcopy(request);simple['objective']='What is our closing AP balance from this reconciled AP workpaper?';simple['handoffs']=[];simple['challenge_assertions']=[]
    c=cao.run(simple);out['simple-ap.public.json']=cao.public(c)
    return out

def main():
    target=ROOT/'orchestration/examples'
    for name,value in artifacts().items():(target/name).write_text(json.dumps(value,indent=2,sort_keys=True,default=str)+'\n')
if __name__=='__main__':main()
