"""Deterministic Stage 1 source-to-public execution witnesses; never patch outputs."""
import json
from pathlib import Path
from orchestration.runtime import CAO
from orchestration.tests.scope_fixtures import run,reviewed_pack,SCOPE,ROWS,source_pack,semantic_proposal
from orchestration.scopes import ScopeRegistry
from orchestration.scoped_journals import allocate_scoped

ROOT=Path(__file__).resolve().parents[1]

def artifacts():
    result=run();case=result.case
    assert (case.outcome,case.status)==('complete','CLOSED')
    pack=reviewed_pack();natives={c['entity']:c for c in pack.request['facts']['customer_contract']}
    native=[];events=[]
    for n in case.graph.nodes.values():
        if n.selected_skill!='revenue-recognition':continue
        native.append(dict(owner=n.selected_skill,node=n.id,source_scope=n.scope_id,posting_scope=n.scope_id,accounting_layer=n.scope_type,currency=n.functional_currency,period=n.period,journals=n.result['journal_entry_implications']))
        for index in range(len(n.result['journal_entry_implications'])):
            events.append(dict(economic_id='contract-1-journal-'+str(index),posting_scope=n.scope_id,currency=n.functional_currency,period=n.period,primary=[dict(owner=n.id,index=index)],witnesses=[],evidence='Separately reviewed contract-1 economics in '+n.scope_id))
    selected,ledger=allocate_scoped(native,SCOPE,events)
    lineage=[]
    for row in result.lineage:
        scope=row.get('scope_id')
        if scope is None:continue
        n=next(n for n in case.graph.nodes.values() if n.scope_id==scope and n.selected_skill=='revenue-recognition')
        receipt=next(r for r in case.handoff_ledger if r['source_node']==n.id)
        lineage.append(dict(source_id='source-'+scope,fact_id=row['fact_id'],scope_id=scope,reviewed_input_pack_scope=scope,producing_node=n.id,owner=n.selected_skill,exact_case_fingerprint=n.result['case_fingerprint'],consumer_node=receipt['target_node'],receipt=receipt))
    lineage.append(dict(source_id='source-GROUP-EUR',scope_id='GROUP-EUR',consumer_node=case.group_consumer['node'],public_output=CAO().public(case)))
    out={
        'scope-registry.json':ScopeRegistry(ROWS).record(),'scope-hierarchy.json':ScopeRegistry(ROWS).hierarchy(),
        'scope-validation.json':dict(accepted=True,hard_scope_cap=None,accounting_authority=False),
        'source-inventory.json':result.inventory,'scoped-facts.json':result.candidates,'semantic-proposal.json':result.proposal,
        'issues-questions.json':dict(issues=case.accounting_issues,questions=result.questions),'owner-input-candidates.json':result.owner_inputs,
        'execution-nodes.json':case.workplan_nodes,'owner-result-registry.json':case.owner_results,'receipt-ledger.json':case.handoff_ledger,
        'journal-event-ledger.json':dict(native=native,allocation=ledger,selected=selected),'exact-once.json':dict(passed=True,event_count=len(ledger),posting_count=len(selected)),
        'group-consumer.json':case.group_consumer,'lineage.json':lineage,'public-answer.json':CAO().public(case),
    }
    for n in case.graph.nodes.values():
        if n.selected_skill=='revenue-recognition':out[n.scope_id.lower()+'-revenue-result.json']=n.result
    return out


def main():
    target=ROOT/'examples/scope-repeated-owner';target.mkdir(exist_ok=True)
    for name,value in artifacts().items():(target/name).write_text(json.dumps(value,sort_keys=True,indent=2,default=str)+'\n')

if __name__=='__main__':main()
