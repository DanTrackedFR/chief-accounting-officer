"""Source-qualified bridge from validated intake into ordinary governed plans.

ReviewedInputPacks are supplied separately. No model/source can approve a plan,
certify accounting, fabricate a blocked dependency or select arbitrary owners.
"""
import copy
import json
from dataclasses import asdict
from .preparation import ReviewedInputPack
from .sources import canonical
from .semantic import transform
from orchestration.runtime import CAO, at, digest
from orchestration.planning import FACT_ADAPTERS
from orchestration.periods import PeriodRegistry
from orchestration.scopes import ScopeRegistry


def execute(engine, prepared, pack):
    if not prepared.validation.get('accepted'):return prepared
    if not isinstance(pack,ReviewedInputPack) or not pack.scoped_packs:
        raise ValueError('Independently reviewed node input packs required')
    prepared._inventory.verify()
    if prepared._seal!=engine._seal(prepared):raise ValueError('Prepared intake changed after qualification')
    request=copy.deepcopy(pack.request)
    if request.get('objective')!=prepared._proposal.objective.value or request.get('scope')!=prepared._current:
        raise ValueError('Reviewed objective/context differs from intake')
    plan=request['governed_plan'];nodes={row['id']:row for row in plan['nodes']}
    if len(nodes)!=len(plan['nodes']) or set(plan['sources'])!=set(nodes):raise ValueError('Complete exact node source population required')
    if canonical(plan['scopes'])!=canonical(request['scope']['scopes']) or canonical(plan['periods'])!=canonical(request['scope']['period_registry']):
        raise ValueError('Governed Scope/Period registry differs from sealed source context')
    scopes=ScopeRegistry(plan['scopes']);periods=PeriodRegistry.from_record(plan['periods'])
    candidates={row['id']:row for row in prepared.candidates}
    selected={(issue.value['owner'],issue.value['scope_id'],issue.value['period_id']) for issue in prepared._proposal.issues}
    natives={key for key,n in nodes.items() if not n['selected_skill'].startswith('orchestration-')}
    if {(nodes[key]['selected_skill'],nodes[key]['scope_id'],nodes[key]['period_id']) for key in natives}!=selected:
        raise ValueError('Native work differs from validated semantic selection')
    seen=set();bound=set();lineage=[]
    for child in pack.scoped_packs:
        if not isinstance(child,ReviewedInputPack) or child.scoped_packs or set(child.request)!={'objective','node_id','source'}:
            raise ValueError('Exact independently supplied node review required')
        key=child.request['node_id']
        if key not in nodes or key in seen or child.request['objective']!=request['objective']:
            raise ValueError('Node input pack collision/substitution')
        n=nodes[key];p=periods.get(n['period_id'])
        if (child.scope_id,child.period_id,child.calendar_id)!=(n['scope_id'],n['period_id'],p.calendar_id) or child.relationship_id is not None:
            raise ValueError('Reviewed node Scope/Period/calendar differs')
        source=plan['sources'][key]
        if canonical(child.request['source'])!=canonical(source):raise ValueError('Reviewed native input differs from execution source')
        seen.add(key)
        for binding in child.bindings:
            if binding.fact_id not in candidates or binding.fact_id in bound or binding.kind!='current':raise ValueError('Exact unique source binding required')
            fact=candidates[binding.fact_id];dims=fact['dimensions']
            if fact['promotion']!='established' or binding.owner!=n['selected_skill'] or fact['candidate_owner']!=n['selected_skill']:
                raise ValueError('Unresolved/wrong-owner source cannot qualify native input')
            if (binding.scope_id,binding.period_id,binding.calendar_id)!=(n['scope_id'],n['period_id'],p.calendar_id) or binding.relationship_id is not None:
                raise ValueError('Binding dimensions differ from exact ReviewedInputPack')
            if (dims['scope_id'],dims['period_id'],dims['calendar_id'])!=(n['scope_id'],n['period_id'],p.calendar_id) or dims['period_role']!='CURRENT':raise ValueError('Source population crosses Scope/Period')
            if fact['economic_id'] and fact['economic_id']!=n.get('economic_id'):raise ValueError('Source economic identity differs from native node')
            if canonical(at(source,binding.path))!=canonical(transform(fact['claim']['value'],fact['transformation'])):
                raise ValueError('Source differs from reviewed native financial input')
            for ref in fact['lineage']:
                original=prepared._inventory.extractions[ref['source_id']].source
                manifests=source.get('qualified_scope_sources',[])
                expected=dict(source_id=original['id'],fingerprint=original['fingerprint'],metadata=original['metadata'])
                if expected not in manifests:raise ValueError('Native source manifest differs from sealed inventory')
                if original['metadata'].get('scope_id')!=n['scope_id'] or original['metadata'].get('period_id')!=n['period_id']:
                    raise ValueError('Source lineage crosses Scope/Period')
            bound.add(binding.fact_id);lineage.append(dict(fact_id=binding.fact_id,node=key,scope_id=n['scope_id'],period_id=p.period_id,owner_input_path=list(binding.path),source_lineage=fact['lineage']))
        if key in natives and not source.get('pending_dependency_evidence'):
            manifest=source.get('qualified_input_snapshot')
            if not isinstance(manifest,dict) or set(manifest)!={'source_id','fingerprint'}:raise ValueError('Complete independent native source snapshot required')
            original=prepared._inventory.raw.get(manifest['source_id'])
            if original is None or original.format!='json' or len(original.payload)!=1:raise ValueError('Native input source snapshot absent/ambiguous')
            meta=original.metadata
            if (meta.get('scope_id'),meta.get('period_id'),meta.get('calendar_id'),meta.get('framework'),meta.get('currency'))!=(n['scope_id'],p.period_id,p.calendar_id,n['framework'],n['functional_currency'] or n['presentation_currency']):raise ValueError('Native input snapshot crosses governed dimensions')
            snapshot={k:copy.deepcopy(v) for k,v in source.items() if k not in ('reviewer_signoff','source_population','qualified_scope_sources','qualified_input_snapshot')}
            expected=dict(record_id=n['logical_id'],reviewed_input=json.dumps(snapshot,sort_keys=True,separators=(',',':')))
            actual=prepared._inventory.extractions[original.id].source
            if original.payload[0]!=expected or actual['fingerprint']!=manifest['fingerprint']:raise ValueError('Complete reviewed native source population differs')
            declared=source.get('source_population',[])
            if manifest['source_id'] not in declared:raise ValueError('Complete input snapshot omitted from source population')
            if len(set(declared))!=len(declared) or set(declared)!={row['source_id'] for row in source.get('qualified_scope_sources',[])}:raise ValueError('Native source population incomplete/duplicated')
            for row in source['qualified_scope_sources']:
                extraction=prepared._inventory.extractions.get(row['source_id'])
                if extraction is None or row!=dict(source_id=extraction.source['id'],fingerprint=extraction.source['fingerprint'],metadata=extraction.source['metadata']):raise ValueError('Native source manifest differs from inventory')
        if key in natives and not source.get('pending_dependency_evidence') and not child.bindings:
            raise ValueError('Native execution requires source-qualified financial input')
        if source.get('pending_dependency_evidence') and child.bindings:raise ValueError('Pending evidence cannot certify accounting')
    if seen!=set(nodes) or bound!={key for key,row in candidates.items() if row['promotion']=='established' and row['candidate_owner']}:
        raise ValueError('Reviewed node/source population omitted')
    # Runtime rejects fabricated pending nodes: blocked publication is derived
    # solely from actual unresolved required producer versions.
    case=CAO().run(request)
    case.work_modes=dict(primary=prepared._proposal.primary_mode.value,secondary=[c.value for c in prepared._proposal.secondary_modes])
    prepared.lineage.extend(lineage);prepared.case=case
    return prepared
