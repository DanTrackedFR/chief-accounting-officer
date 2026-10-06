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
    from orchestration.runtime import CAO
    ledger=CAO().selective_reexecute(f['case'],plan)
    context,events=journal_inputs(f);selected,allocation=e.current_journals(context,events)
    result.update({'reexecution-ledger.json':ledger,'result-versions-final.json':e.versions.record(),'supersession-ledger.json':dict(sorted(e.versions.supersession.items())),'receipt-ledger-final-current.json':[e.receipt(key) for key in sorted(e.edges)],'journal-event-ledger-final.json':dict(events=events,allocation=allocation,selected=selected),'case-registry-final.json':e.cases.record(),'case-statuses-final.json':[dict(case=c.id,status=c.status,outcome=c.outcome) for c in e.cases.cases.values()],'period-reopening-history.json':e.periods.record(),'group-before-after.json':dict(before=original['GROUP'].payload(),after=e.versions.current(n['GROUP'].id).payload()),'analytics-before-after.json':dict(before=original['ANALYTICS'].payload(),after=e.versions.current(n['ANALYTICS'].id).payload()),'public-answer.json':public(f)})
    def lineage(label,version):
        return dict(label=label,source_fingerprint=version.source_fingerprint,result_version=version.version_id,scope_id=version.scope_id,period_id=version.period_id,case_id=version.case_id,dependencies=[dict(dependency=edge,version=bound,currentness=e.versions.state(bound)) for edge,bound in version.dependency_bindings],currentness=e.versions.state(version.version_id))
    result['executable-lineage.json']=[lineage('US source to original revenue',original['US-SEP']),lineage('Original US revenue to original reporting',original['US-REPORT']),lineage('Corrected source to corrected US revenue',e.versions.current(n['US-SEP'].id)),lineage('Corrected US closing to October opening',e.versions.current(n['US-OPEN'].id)),lineage('Current US opening to Group observation',e.versions.current(n['GROUP'].id)),lineage('Current Group observation to analytics',e.versions.current(n['ANALYTICS'].id)),lineage('UK source remains current through US rework',e.versions.current(n['UK-SEP'].id))]
    assert original['UK-SEP']==e.versions.current(n['UK-SEP'].id)
    assert len(selected)==len(result['journal-event-ledger-initial.json']['selected'])
    # Separate restatement and SUBGROUP proofs use the same ordinary API and
    # registry substrate. They do not alter the central four-consumer chain.
    from orchestration.tests.stage2_fixtures import restatement,subgroup
    from orchestration.tests.temporal_intake_fixtures import fixture,OBJECTIVE
    from orchestration.intake import Intake,FixturePlanner
    comparative=initial(build());ce=comparative['coordinator']
    prior=copy.deepcopy(ce.versions.record());comparative_plan,comparative_ledger=restatement(comparative)
    result['comparative-restatement-lineage.json']=dict(original_versions=prior,final_versions=ce.versions.record(),history=ce.versions.history,plan=comparative_plan,reexecution=comparative_ledger,current_receipts=[ce.receipt(k) for k in sorted(ce.edges) if ce.edges[k].dependency_type=='COMPARATIVE'])
    sg=subgroup();se=sg['coordinator'];sg_initial=copy.deepcopy(se.cases.record());sg_plan=correction(sg);sg_ledger=CAO().selective_reexecute(sg['case'],sg_plan)
    result['subgroup-governance.json']=dict(initial_cases=sg_initial,final_cases=se.cases.record(),dependencies=[asdict(x) for x in se.edges.values()],rework=sg_plan,reexecution=sg_ledger,current_receipts=[se.receipt(k) for k in sorted(se.edges) if 'SUBGROUP-US' in (se.edges[k].producer_scope,se.edges[k].consumer_scope)])
    raw,proposal,scope,pack=fixture();engine=Intake(FixturePlanner(proposal));prepared=engine.execute(engine.prepare(OBJECTIVE,raw,[],scope),pack)
    assert prepared.case.outcome=='complete'
    result['period-qualified-intake.json']=dict(facts=prepared.candidates,owner_inputs=prepared.owner_inputs,lineage=prepared.lineage,reviewed_packs=prepared.case.reviewed_input_packs,versions=prepared.case.governance.versions.record(),public=CAO().public(prepared.case))
    attacks=[]
    key=next(k for k,edge in e.edges.items() if edge.consumer_node==n['US-REPORT'].id)
    valid=e.receipt(key)
    for field,value in [('producer_scope','ENTITY-UK'),('consumer_scope','ENTITY-UK'),('producer_period',n['US-OCT'].period_id),('consumer_period',n['US-OCT'].period_id),('producer_framework','IFRS'),('consumer_framework','IFRS'),('value_currency','EUR'),('currentness','STALE'),('metric_path',['case_fingerprint']),('result_version',original['US-SEP'].version_id)]:
        bad=copy.deepcopy(valid);bad[field]=value
        try:e.validate_receipt(bad,valid['consumer_node'])
        except ValueError:attacks.append(dict(attack=field,result='REJECTED'))
        else:raise AssertionError('Adversarial receipt accepted: '+field)
    result['adversarial-results.json']=attacks
    result['architecture-reconstruction-witness.json']=dict(runtime='CAO.run -> existing Graph/CaseRegistry/PeriodRegistry/VersionedExecution -> production owners or bounded observations -> CAO.public/public_record',correction='CAO.correct -> deterministic dependency invalidation -> CAO.selective_reexecute -> current delivery',central_affected=plan['execution_order'],unaffected=plan['unaffected'],authority='Existing production accounting owners only',persistence=False,authenticated_governance=False,stage3_started=False,stage4_started=False)
    result['stage3-handoff-witness.json']=dict(path='orchestration/MULTI-ENTITY-STAGE2-TO-STAGE3-HANDOFF.md',provided_contracts=['Scope/Period-qualified Cases','exact immutable result versions','typed dependency receipts','opening/comparative/restatement history','selective rework','structural SUBGROUP'],deferred=['generalized intercompany networks','framework conversion','currency translation chains','durable persistence','authenticated approvals'])
    return result


def main():
    TARGET.mkdir(exist_ok=True)
    for name,value in artifacts().items():(TARGET/name).write_text(json.dumps(value,sort_keys=True,indent=2,default=str)+'\n')

if __name__=='__main__':main()
