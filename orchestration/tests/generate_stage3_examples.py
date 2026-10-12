"""Deterministic bounded Stage 3 evidence from actual ordinary CAO execution."""
import copy
import json
from dataclasses import asdict
from pathlib import Path
from orchestration.tests.stage3_fixtures import *

TARGET=Path(__file__).resolve().parents[1]/'examples/intercompany-framework-currency'


def artifacts():
    f=ordinary_initial();e=f['session'];n=f['nodes'];b=f['basis']
    initial_versions={label:e.versions.current(node.id) for label,node in n.items()}
    context,events,dispositions=journal_inputs(f);selected,allocation=b.current_journals(context,events,dispositions)
    initial_transforms=transformation_receipts(f)
    result={
        'scope-registry.json':e.cases.scopes.record(),
        'period-registry.json':e.periods.record(),
        'cases-initial.json':e.cases.record(),
        'business-network-initial.json':network(f).record(),
        'matching-results-initial.json':[initial_versions['match-'+r].payload()['matching'] for r in sorted(f['source_specs'])],
        'execution-dag.json':dict(nodes=e.graph.record(),dependencies=[dict(asdict(edge),dependency_id=k) for k,edge in sorted(e.edges.items())]),
        'result-versions-initial.json':e.versions.record(),
        'exact-version-receipts-initial.json':[e.receipt(k) for k in sorted(e.edges)],
        'cross-layer-receipts-initial.json':[asdict(b.receipt(k)) for k in sorted(b.contracts)],
        'transformation-receipts-initial.json':initial_transforms,
        'unsupported-framework-conversion.json':b.unsupported_conversion(initial_versions['clean-ENTITY-US'].version_id,'IFRS','unsupported-general-conversion'),
        'posting-ledger-initial.json':dict(events=events,translation_evidence=dispositions,allocation=allocation,selected=selected),
        'public-answer-initial.json':CAO().public(f['case']),
    }
    plan=CAO().correct(f['case'],n['clean-ENTITY-US'].id,legal_source(f,'clean','ENTITY-US',True),'Qualified transaction closing-rate correction')
    result['selective-rework-plan.json']=copy.deepcopy(plan)
    result['stale-versions.json']=[dict(node=k,version=e.versions.current(k,allow_stale=True).version_id,state=e.versions.state(e.versions.current(k,allow_stale=True).version_id)) for k in plan['execution_order']]
    result['unaffected-versions.json']=[dict(node=k,version=e.versions.current(k).version_id) for k in plan['unaffected']]
    reviewed=reviewed_rework_sources(f,plan)
    result['reviewed-rework-packs.json']=copy.deepcopy(reviewed)
    result['reexecution-ledger.json']=CAO().selective_reexecute(f['case'],plan,reviewed)
    context,events,dispositions=journal_inputs(f);selected,allocation=b.current_journals(context,events,dispositions)
    result.update({
        'business-network-final.json':network(f).record(),
        'matching-results-final.json':[e.versions.current(n['match-'+r].id).payload()['matching'] for r in sorted(f['source_specs'])],
        'result-versions-final.json':e.versions.record(),
        'exact-version-receipts-final.json':[e.receipt(k) for k in sorted(e.edges)],
        'cross-layer-receipts-final.json':[asdict(b.receipt(k)) for k in sorted(b.contracts)],
        'transformation-receipts-final.json':transformation_receipts(f),
        'supersession-history.json':dict(versions=e.versions.supersession,history=e.versions.history),
        'posting-ledger-final.json':dict(events=events,translation_evidence=dispositions,allocation=allocation,selected=selected),
        'cases-final.json':e.cases.record(),
        'public-answer-final.json':CAO().public(f['case']),
        'group-before-after.json':dict(before=initial_versions['elimination'].payload()['calculations'],after=e.versions.current(n['elimination'].id).payload()['calculations']),
        'native-owner-results-final.json':{label:e.versions.current(node.id).payload() for label,node in n.items() if not node.selected_skill.startswith('orchestration-')},
        'authority-boundary.json':dict(runtime='Ordinary CAO.run/correct/selective_reexecute with existing Graph/VersionedExecution',
            supported_conversion='Native IFRS ordinary reciprocal-balance reassessment after native US-GAAP EUR translation; explicit zero adjustment',
            unsupported_conversion='General GAAP conversion fails closed',
            legal_posts='Native US IC FX adjustment only; original legal balances are separate carried book evidence',
            group_posts='Native Consolidation reciprocal and investment/equity elimination only',
            translation='Native FX implication already embedded in qualified Group TB; witnessed evidence only',
            residual='Mismatched principal remains unresolved; overall Case partial',
            persistence=False,authenticated_approvals=False,stage4_started=False),
    })
    for relationship in ('timing','fx','mismatch'):
        for label in ('match-'+relationship,relationship+'-'+f['source_specs'][relationship]['a'],relationship+'-'+f['source_specs'][relationship]['b']):
            assert initial_versions[label]==e.versions.current(n[label].id)
    for key in b.contracts:b.validate(b.receipt(key),e.edges[key].consumer_node)
    for record in result['transformation-receipts-final.json']:b.validate_transformation(record)
    return result


def main():
    TARGET.mkdir(exist_ok=True)
    for name,value in artifacts().items():(TARGET/name).write_text(json.dumps(value,sort_keys=True,indent=2,default=str)+'\n')

if __name__=='__main__':main()
