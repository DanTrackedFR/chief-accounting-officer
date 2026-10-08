"""Retain sealed intake and supplied reviews as evidence, never new approvals."""
import copy
import json
from dataclasses import asdict
from orchestration.intake.sources import RawSource, Inventory, canonical
from orchestration.intake.preparation import Intake
from orchestration.runtime import digest
from orchestration.versions import fingerprint
from .codec import IntegrityError

SEALED = ('inventory', 'validation', 'proposal', 'candidates', 'transformations', 'conflicts', 'questions', 'owner_inputs', 'memory_candidates')


def retain(session, prepared, pack):
    """Called only after native intake qualification; copies its existing seal."""
    prepared._inventory.verify()
    if prepared._seal != Intake._seal(prepared): raise IntegrityError('Changed intake seal')
    # Raw JSON member order participates in native extraction field identity.
    # Keep its original wire order in a string; never regenerate field identities.
    raws = [json.dumps(asdict(raw), ensure_ascii=False, separators=(',', ':'), allow_nan=False)
            for raw in prepared._inventory.raw.values()]
    bundle = dict(raw_sources=raws, fields={k: copy.deepcopy(getattr(prepared, k)) for k in SEALED},
                  proposal=prepared._proposal.record(), context=copy.deepcopy(prepared._current),
                  seal=prepared._seal, pack=asdict(pack), lineage=copy.deepcopy(prepared.lineage))
    bundle_id = digest(bundle)
    if not hasattr(session, 'evidence_bundles'): session.evidence_bundles = {}
    session.evidence_bundles[bundle_id] = bundle
    root_id = pack.request.get('governed_plan', {}).get('root_case')
    if root_id is None and prepared.case is not None: root_id = prepared.case.id
    if root_id is None: raise IntegrityError('Qualified archive requires its exact root Case')
    root = session.cases.get(root_id)
    if not hasattr(root, '_source_qualification_refs'): root._source_qualification_refs = []
    if bundle_id not in root._source_qualification_refs: root._source_qualification_refs.append(bundle_id)
    return bundle_id


def validate(bundle_id, bundle, session=None):
    if set(bundle) != {'raw_sources', 'fields', 'proposal', 'context', 'seal', 'pack', 'lineage'} or digest(bundle) != bundle_id:
        raise IntegrityError('Evidence bundle identity differs')
    if set(bundle['fields']) != set(SEALED): raise IntegrityError('Incomplete sealed intake')
    fields = bundle['fields']
    if fields['validation'].get('accepted') is not True: raise IntegrityError('Unreviewed intake cannot qualify')
    if digest(dict(fields=fields, proposal=bundle['proposal'], context=bundle['context'])) != bundle['seal']:
        raise IntegrityError('Source qualification seal differs')
    inventory = Inventory([RawSource(**json.loads(raw)) for raw in bundle['raw_sources']])
    if canonical(inventory.normalized()) != canonical(fields['inventory']): raise IntegrityError('Source payload/extraction mismatch')
    pack = bundle['pack']
    from orchestration.intake.preparation import ReviewedInputPack
    if set(pack) != set(ReviewedInputPack.__dataclass_fields__): raise IntegrityError('Unknown ReviewedInputPack schema')
    request = pack['request']
    if 'governed_plan' not in request:
        return validate_legacy(pack, fields, inventory, session)
    plan = request['governed_plan']
    nodes = {n['id']: n for n in plan['nodes']}
    if len(nodes) != len(plan['nodes']) or set(nodes) != set(plan['sources']): raise IntegrityError('Incomplete reviewed node population')
    seen = set()
    candidates = {r['id']: r for r in fields['candidates']}
    bound = set()
    for child in pack['scoped_packs']:
        if set(child) != set(ReviewedInputPack.__dataclass_fields__) or child['scoped_packs']: raise IntegrityError('Wrong input pack')
        key = child['request'].get('node_id')
        if key not in nodes or key in seen: raise IntegrityError('Wrong reviewed node identity')
        n = nodes[key]; source = plan['sources'][key]
        if canonical(child['request']) != canonical(dict(objective=request['objective'], node_id=key, source=source)):
            raise IntegrityError('Owner input pack substituted')
        period = next(p for p in plan['periods']['periods'] if p['period_id'] == n['period_id'])
        if (child['scope_id'], child['period_id'], child['calendar_id'], child['relationship_id']) != (n['scope_id'], n['period_id'], period['calendar_id'], None):
            raise IntegrityError('Reviewed pack dimensions differ')
        for b in child['bindings']:
            fact = candidates.get(b['fact_id'])
            if fact is None or b['fact_id'] in bound or fact['promotion'] != 'established' or b['owner'] != n['selected_skill'] or fact['candidate_owner'] != b['owner']:
                raise IntegrityError('Wrong/unreviewed owner binding')
            if (b['scope_id'], b['period_id'], b['calendar_id'], b['kind'], b['relationship_id']) != (n['scope_id'], n['period_id'], period['calendar_id'], 'current', None):
                raise IntegrityError('Wrong reviewed binding dimensions')
            from orchestration.runtime import at
            from orchestration.intake.semantic import transform
            if canonical(at(source, b['path'])) != canonical(transform(fact['claim']['value'], fact['transformation'])):
                raise IntegrityError('Changed owner financial binding')
            bound.add(b['fact_id'])
        if source.get('qualified_input_snapshot'):
            manifest = source['qualified_input_snapshot']
            raw = inventory.raw.get(manifest['source_id'])
            snapshot = {k: v for k, v in source.items() if k not in ('reviewer_signoff', 'source_population', 'qualified_scope_sources', 'qualified_input_snapshot')}
            expected = dict(record_id=n['logical_id'], reviewed_input=json.dumps(snapshot, sort_keys=True, separators=(',', ':')))
            if raw is None or raw.payload != [expected] or inventory.extractions[raw.id].source['fingerprint'] != manifest['fingerprint']:
                raise IntegrityError('Missing/changed source snapshot')
            declared = source.get('source_population', [])
            if len(set(declared)) != len(declared) or set(declared) != {r['source_id'] for r in source.get('qualified_scope_sources', [])} or raw.id not in declared:
                raise IntegrityError('Source population shortened')
            for row in source['qualified_scope_sources']:
                actual = inventory.extractions.get(row['source_id'])
                if actual is None or canonical(row) != canonical(dict(source_id=actual.source['id'], fingerprint=actual.source['fingerprint'], metadata=actual.source['metadata'])):
                    raise IntegrityError('Missing source evidence')
        seen.add(key)
    if seen != set(nodes) or bound != {k for k, r in candidates.items() if r['promotion'] == 'established' and r['candidate_owner']}:
        raise IntegrityError('Source/owner population omitted')
    return {fingerprint(source): source for source in plan['sources'].values()}


def validate_legacy(pack, fields, inventory, session):
    """Preserve native legacy qualification, never execute owner-result bindings."""
    from orchestration.execution import OwnerInputs, populations
    from orchestration.planning import FACT_ADAPTERS
    from orchestration.intake.preparation import Binding, PopulationBinding, DocumentBinding, TextAssertion
    from orchestration.runtime import at, number
    from orchestration.temporal_inputs import validate_binding, validate_source, validate_pack
    request = pack['request']; context = request['scope']; owners = OwnerInputs(context)
    for family, source in populations(request.get('facts', {})):
        if family in FACT_ADAPTERS: owners.add(FACT_ADAPTERS[family][0], source)
    candidates = {r['id']: r for r in fields['candidates']}; bound = set(); targets = set()
    bindings = [Binding(**b) for b in pack['bindings']]
    # Use native temporal validation for the actual pack and each qualification.
    from orchestration.intake.preparation import ReviewedInputPack
    def native_pack(row):
        values=copy.deepcopy(row)
        for key, cls in [('bindings', Binding), ('populations', PopulationBinding), ('documents', DocumentBinding), ('text_assertions', TextAssertion)]:
            values[key]=[cls(**v) for v in values[key]]
        values['scoped_packs']=[native_pack(v) for v in values['scoped_packs']]
        return ReviewedInputPack(**values)
    restored_pack=native_pack(pack);validate_pack(context, restored_pack, list(owners.values()))
    for binding in bindings:
        key=owners.key(binding.owner,binding.scope_id,binding.period_id);source=owners[key]
        fact=candidates.get(binding.fact_id)
        if fact is None or fact['promotion']!='established' or (fact['candidate_owner'] and fact['candidate_owner']!=binding.owner):
            raise IntegrityError('Unreviewed/wrong-owner legacy binding')
        target=(key,tuple(binding.path))
        if target in targets:raise IntegrityError('Duplicate legacy owner target')
        targets.add(target);bound.add(binding.fact_id)
        validate_binding(context,source,binding,fact['dimensions'])
        for ref in fact['lineage']:
            if ref['source_id'] not in inventory.extractions:raise IntegrityError('Missing legacy source evidence')
            if ref['source_fingerprint']!=inventory.extractions[ref['source_id']].source['fingerprint']:raise IntegrityError('Changed legacy source fingerprint')
        if binding.kind=='owner_result':
            versions=[v for v in session.versions.versions.values() if v.source_fingerprint==fingerprint(source)] if session else []
            if not versions:raise IntegrityError('Legacy owner-result evidence absent')
            values=[at(v.payload()['calculations'],binding.path) for v in versions]
            matches=any(number(value)==number(fact['claim']['value']) if fact['transformation']=='decimal' else canonical(value)==canonical(fact['claim']['value']) for value in values)
        elif binding.kind in ('current','comparator'):
            matches=canonical(at(source,binding.path))==canonical(fact['claim']['value'])
        else:raise IntegrityError('Unknown legacy binding kind')
        if not matches:raise IntegrityError('Changed legacy owner binding')
    if bound!={k for k,r in candidates.items() if r['promotion']=='established' and r['candidate_owner']}:
        # Context facts may also be bound; never drop required owner facts.
        if not {k for k,r in candidates.items() if r['promotion']=='established' and r['candidate_owner']}<=bound:
            raise IntegrityError('Legacy owner fact population omitted')
    for key, source in owners.items():
        manifest=source.get('qualified_scope_sources',[])
        if manifest:
            if len(manifest)!=len(source.get('source_population',[])) or {r['source_id'] for r in manifest}!=set(source['source_population']):
                raise IntegrityError('Legacy source population shortened')
            for row in manifest:
                ex=inventory.extractions.get(row['source_id'])
                if ex is None or canonical(row)!=canonical(dict(source_id=ex.source['id'],fingerprint=ex.source['fingerprint'],metadata=ex.source['metadata'])):
                    raise IntegrityError('Legacy source manifest differs')
        for binding in restored_pack.documents+restored_pack.populations+restored_pack.text_assertions:
            if owners.key(binding.owner,binding.scope_id,binding.period_id)!=key:continue
            ex=inventory.extractions.get(binding.source_id)
            if ex is None:raise IntegrityError('Legacy bound source absent')
            validate_source(context,source,ex.source['metadata'],binding)
    repeated={pkg for pkg in owners.packages.values() if list(owners.packages.values()).count(pkg)>1}
    expected={key for key,pkg in owners.packages.items() if pkg in repeated};seen=set()
    for child in restored_pack.scoped_packs:
        rows=list(populations(child.request.get('facts',{})))
        if len(rows)!=1 or child.scoped_packs:raise IntegrityError('Wrong legacy scoped pack')
        family,source=rows[0];key=owners.key(FACT_ADAPTERS[family][0],child.scope_id,child.period_id)
        if key not in expected or key in seen or fingerprint(source)!=fingerprint(owners[key]):raise IntegrityError('Legacy scoped pack substituted')
        validate_pack(context,child,[source]);seen.add(key)
    if seen!=expected:raise IntegrityError('Missing legacy repeated-owner review pack')
    return {fingerprint(source):source for source in owners.values()}
