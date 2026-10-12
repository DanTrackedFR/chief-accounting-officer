"""Milestone artifacts from the ordinary governed intake/correction lifecycle.

Not a release acceptance record; remaining gates are explicitly labelled.
"""
import copy
import json
from dataclasses import asdict
from pathlib import Path
from orchestration.tests.stage4_fixtures import intake_initial,correct,reviewed_rework,journal_ledger,transforms
from orchestration.tests.stage3_fixtures import network
from orchestration.runtime import CAO

TARGET=Path(__file__).resolve().parents[1]/'examples/multi-entity-multi-period'


def artifacts():
    f=intake_initial();e=f['session'];n=f['nodes'];before={label:e.versions.current(node.id) for label,node in n.items()}
    def record_versions():return e.versions.record()
    def current_results():return {label:e.versions.current(node.id).payload() for label,node in sorted(n.items())}
    def receipts():
        return [e.receipt(key) for key,edge in sorted(e.edges.items()) if e.graph.nodes[edge.producer_node].status=='complete' and not e.versions.current(edge.producer_node).payload().get('unresolved_dependencies')]
    a={
        'source-pack.json':[asdict(r) for r in f['raw_sources']],
        'source-pack-inventory.json':f['intake'].inventory,
        'scope-registry.json':e.cases.scopes.record(),
        'period-registry.json':e.periods.record(),
        'fiscal-calendars.json':[asdict(c) for c in e.periods.calendars.values()],
        'effective-intervals.json':[asdict(f['effective_interval'])],
        'case-hierarchy-initial.json':e.cases.record(),
        'semantic-proposal.json':f['intake'].proposal,
        'material-questions.json':f['intake'].questions,
        'issue-register.json':f['intake'].proposal['issues'],
        'owner-input-candidates.json':f['intake'].owner_inputs,
        'reviewed-input-packs.json':asdict(f['reviewed_pack']),
        'source-fact-lineage.json':f['intake'].lineage,
        'execution-graph-initial.json':e.graph.record(),
        'dependency-graph.json':[dict(asdict(edge),dependency_id=k) for k,edge in sorted(e.edges.items())],
        'owner-results-initial.json':current_results(),
        'result-versions-initial.json':record_versions(),
        'current-receipts-initial.json':receipts(),
        'intercompany-network-initial.json':network(f).record(),
        'current-timing-match.json':before['match-timing-current'].payload(),
        'group-accounting-initial.json':before['elimination'].payload(),
        'group-reporting-initial.json':before['reporting'].payload(),
        'analytics-initial.json':before['analytics'].payload(),
        'conflict-register.json':[before['match-mismatch'].payload()['matching']],
        'case-statuses-initial.json':{c.id:dict(status=c.status,outcome=c.outcome,scope_id=c.scope_id,period_id=c.period_id) for c in e.cases.cases.values()},
        'public-answer-initial.json':CAO().public(f['case']),
    }
    plan=correct(f);a['qualified-correction.json']=copy.deepcopy(e.sources[n['mismatch-ENTITY-NL'].id]);a['invalidation.json']=copy.deepcopy(plan)
    a['stale-node-ledger.json']=[dict(node=k,version=e.versions.current(k,allow_stale=True).version_id,state=e.versions.state(e.versions.current(k,allow_stale=True).version_id)) for k in plan['execution_order']]
    a['unaffected-node-ledger.json']=[dict(node=k,version=e.versions.current(k).version_id,status=e.graph.nodes[k].status) for k in plan['unaffected']]
    a['selective-rework-plan.json']=copy.deepcopy(plan)
    try:
        reviewed=reviewed_rework(f,plan)
    except ValueError as error:
        if 'Full Group accounting omits or duplicates current legal loan economics' not in str(error):raise
        # Capture the real governed refusal. No final accounting result is made.
        a['rework-refusal.json']=dict(error=str(error),required_action='Qualify all current loan populations through native owners before retrying the corrected clean control')
        a['fresh-replacement-intake-checkpoint.json']=[dict(node=row['node'],raw_sources=[asdict(source) for source in row['raw_sources']],inventory=row['prepared'].inventory,validation=row['prepared'].validation,proposal=row['prepared'].proposal,lineage=row['prepared'].lineage,reviewed_pack=asdict(row['reviewed_pack']),accounting_acceptance='NOT_ESTABLISHED_BY_SOURCE_QUALIFICATION') for row in f.get('replacement_intakes',[])]
        a['result-versions-checkpoint.json']=record_versions()
        a['supersession-history.json']=dict(versions=e.versions.supersession,events=e.versions.history)
        a['public-answer-checkpoint.json']=CAO().public(f['case'])
        a['acceptance-state.json']=dict(status='INCOMPLETE',open_findings=['S4-IQA03'],corrected_clean_control_complete=False,independent_final_qa=False,full_release_regression=False,required_adversarial_coverage_complete=False,roadmap_complete=False,ready_for_review=False)
        return a
    a['reviewed-rework-packs.json']=copy.deepcopy(reviewed);a['reexecution-ledger.json']=CAO().selective_reexecute(f['case'],plan,reviewed)
    a.update({
        'result-versions-final.json':record_versions(),
        'current-receipts-final.json':receipts(),
        'owner-results-final.json':current_results(),
        'intercompany-network-final.json':network(f).record(),
        'transformation-receipts-final.json':transforms(f),
        'exact-once-ledger-final.json':journal_ledger(f),
        'group-accounting-final.json':e.versions.current(n['elimination'].id).payload(),
        'group-reporting-final.json':e.versions.current(n['reporting'].id).payload(),
        'analytics-final.json':e.versions.current(n['analytics'].id).payload(),
        'case-hierarchy-final.json':e.cases.record(),
        'case-statuses-final.json':{c.id:dict(status=c.status,outcome=c.outcome,scope_id=c.scope_id,period_id=c.period_id) for c in e.cases.cases.values()},
        'supersession-history.json':dict(versions=e.versions.supersession,events=e.versions.history),
        'public-answer-final.json':CAO().public(f['case']),
        'acceptance-state.json':dict(status='INTERMEDIATE',independent_final_qa=False,full_release_regression=False,required_adversarial_coverage_complete=False,roadmap_complete=False,ready_for_review=False,notes=['Source correction and downstream source inventory completeness still require independent acceptance; do not treat these milestone artifacts as final release.']),
    })
    def chain(labels):
        result=[]
        for label in labels:
            node=n[label];v=e.versions.current(node.id)
            result.append(dict(label=label,node=node.id,scope=v.scope_id,case=v.case_id,period=v.period_id,version=v.version_id,framework=node.framework,currency=node.functional_currency or node.presentation_currency,economic_id=node.economic_id,source_fingerprint=v.source_fingerprint,currentness=e.versions.state(v.version_id),bindings=v.dependency_bindings))
        # Every adjacent step must be an actual execution edge, not equal totals.
        for left,right in zip(result,result[1:]):
            if not any(edge.producer_node==left['node'] and edge.consumer_node==right['node'] for edge in e.edges.values()):raise ValueError('Missing executable lineage edge')
        return result
    a['executable-lineage.json']={
        'nl':chain(['clean-ENTITY-NL','conversion','elimination','reporting']),
        'us':chain(['clean-ENTITY-US','translation','conversion','elimination','reporting']),
        'uk':chain(['mismatch-ENTITY-UK','uk-translation','uk-conversion','elimination','reporting']),
        'legal-side-a':chain(['clean-ENTITY-US','match-clean','elimination','reporting']),
        'legal-side-b':chain(['clean-ENTITY-NL','match-clean','elimination','reporting']),
        'opening':chain(['timing-ENTITY-NL','nl-opening','group']),
        'comparative':chain(['timing-ENTITY-NL','nl-comparative','group']),
        'original-conflict':dict(owner_version=asdict(before['mismatch-ENTITY-NL']),matching_version=asdict(before['match-mismatch']),blocked_group_version=asdict(before['reporting']),public_answer=a['public-answer-initial.json']),
        'corrected':dict(source=a['qualified-correction.json'],new_version=asdict(e.versions.current(n['mismatch-ENTITY-NL'].id)),supersession=a['supersession-history.json'],invalidation=plan,reexecution=a['reexecution-ledger.json'],reporting=asdict(e.versions.current(n['reporting'].id)),analytics=asdict(e.versions.current(n['analytics'].id)),case_status=f['case'].status,public_answer=a['public-answer-final.json']),
    }
    return a


def main():
    TARGET.mkdir(exist_ok=True)
    generated=artifacts()
    for path in TARGET.glob('*.json'):
        if path.name not in generated:path.unlink()
    for name,value in generated.items():(TARGET/name).write_text(json.dumps(value,sort_keys=True,indent=2,default=str)+'\n')

if __name__=='__main__':main()
