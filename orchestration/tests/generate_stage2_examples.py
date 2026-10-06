"""Reproduce bounded Stage 2 evidence from executable governance, never patches."""
import copy
import json
from dataclasses import asdict
from pathlib import Path
from orchestration.tests.stage2_fixtures import build,initial,correction,public

TARGET=Path(__file__).resolve().parents[1]/'examples/case-period-invalidation'


def journal_inputs(f):
    e=f['coordinator'];context=dict(entity='GROUP-EUR',framework='IFRS',jurisdiction='NL',currency='EUR',period_start='2026-10-01',reporting_period='2026-10-31',scopes=e.cases.scopes.record(),period_registry=e.periods.record())
    events=[]
    for node_id in sorted(e.versions.active):
        version=e.versions.current(node_id);node=e.graph.nodes[node_id]
        for index,journal in enumerate(version.payload().get('journal_entry_implications',[])):
            events.append(dict(economic_id='reviewed-contract-event-'+str(index),posting_scope=node.scope_id,period=node.period,currency=node.functional_currency or node.presentation_currency,period_id=node.period_id,result_version=version.version_id,primary=[dict(owner=node.id,index=index)],witnesses=[],evidence='Synthetic independently reviewed native contract journal event'))
    return context,events


def artifacts():
    f=initial(build());e=f['coordinator'];n=f['nodes']
    original={label:e.versions.current(node.id) for label,node in n.items()}
    context,events=journal_inputs(f);selected,allocation=e.current_journals(context,events)
    result={
        'case-registry-initial.json':copy.deepcopy(e.cases.record()),
        'case-hierarchy.json':[dict(case_id=c.id,parent=c.parent_case_id,children=c.child_case_ids,scope_id=c.scope_id,period_id=c.period_id) for c in e.cases.cases.values()],
        'period-registry.json':e.periods.record(),
        'period-relationships.json':e.periods.record()['relationships'],
        'fiscal-calendars.json':e.periods.record()['calendars'],
        'effective-intervals.json':[asdict(f['interval'])],
        'execution-nodes-initial.json':copy.deepcopy(e.graph.record()),
        'dependency-graph.json':[dict(asdict(edge),id=key) for key,edge in sorted(e.edges.items())],
        'cross-entity-dependencies.json':[dict(asdict(edge),id=key) for key,edge in sorted(e.edges.items()) if edge.producer_scope!=edge.consumer_scope],
        'cross-period-dependencies.json':[dict(asdict(edge),id=key) for key,edge in sorted(e.edges.items()) if edge.producer_period!=edge.consumer_period],
        'result-versions-initial.json':e.versions.record(),
        'receipt-ledger-initial.json':copy.deepcopy(e.receipts),
        'journal-event-ledger-initial.json':dict(events=events,allocation=allocation,selected=selected),
        'case-statuses-initial.json':[dict(case=c.id,status=c.status,outcome=c.outcome) for c in e.cases.cases.values()],
    }
    plan=correction(f)
    result.update({'upstream-correction.json':dict(old_version=original['US-SEP'].version_id,new_version=e.versions.current(n['US-SEP'].id).version_id,source=f['sources'][n['US-SEP'].id]),'invalidation.json':copy.deepcopy(plan),'stale-node-ledger.json':[dict(node=node,version=e.versions.current(node,allow_stale=True).version_id,state='STALE') for node in plan['execution_order']],'unaffected-node-ledger.json':[dict(node=node,version=e.versions.current(node).version_id,state='CURRENT') for node in plan['unaffected']],'selective-rework-plan.json':copy.deepcopy(plan)})
    ledger=e.reexecute(plan,f['executors'],f['sources'])
    context,events=journal_inputs(f);selected,allocation=e.current_journals(context,events)
    result.update({'reexecution-ledger.json':ledger,'result-versions-final.json':e.versions.record(),'supersession-ledger.json':dict(sorted(e.versions.supersession.items())),'receipt-ledger-final-current.json':[e.receipt(key) for key in sorted(e.edges)],'journal-event-ledger-final.json':dict(events=events,allocation=allocation,selected=selected),'case-registry-final.json':e.cases.record(),'case-statuses-final.json':[dict(case=c.id,status=c.status,outcome=c.outcome) for c in e.cases.cases.values()],'period-reopening-history.json':e.periods.record(),'group-before-after.json':dict(before=original['GROUP'].payload(),after=e.versions.current(n['GROUP'].id).payload()),'analytics-before-after.json':dict(before=original['ANALYTICS'].payload(),after=e.versions.current(n['ANALYTICS'].id).payload()),'public-answer.json':public(f)})
    def lineage(label,version):
        return dict(label=label,source_fingerprint=version.source_fingerprint,result_version=version.version_id,scope_id=version.scope_id,period_id=version.period_id,case_id=version.case_id,dependencies=[dict(dependency=edge,version=bound,currentness=e.versions.state(bound)) for edge,bound in version.dependency_bindings],currentness=e.versions.state(version.version_id))
    result['executable-lineage.json']=[lineage('US source to original revenue',original['US-SEP']),lineage('Original US revenue to original reporting',original['US-REPORT']),lineage('Corrected source to corrected US revenue',e.versions.current(n['US-SEP'].id)),lineage('Corrected US closing to October opening',e.versions.current(n['US-OPEN'].id)),lineage('Current US opening to Group observation',e.versions.current(n['GROUP'].id)),lineage('Current Group observation to analytics',e.versions.current(n['ANALYTICS'].id)),lineage('UK source remains current through US rework',e.versions.current(n['UK-SEP'].id))]
    assert original['UK-SEP']==e.versions.current(n['UK-SEP'].id)
    assert len(selected)==len(result['journal-event-ledger-initial.json']['selected'])
    return result


def main():
    TARGET.mkdir(exist_ok=True)
    for name,value in artifacts().items():(TARGET/name).write_text(json.dumps(value,sort_keys=True,indent=2,default=str)+'\n')

if __name__=='__main__':main()
