"""Candidate resolution and audited owner preparation; never creates certification."""
import copy
import re
from dataclasses import dataclass, field, asdict
from orchestration.runtime import CAO, company_context, at, dimensions, digest, number
from orchestration.intent import Intent
from orchestration.planning import Issue, FACT_ADAPTERS
from .sources import Inventory, fingerprint, canonical
from .semantic import RequestContext, ProposalValidator, transform

# Explicit semantic contracts prevent equal numbers from substituting a different
# accounting concept. Extensions require a governed producer calculation path.
OWNER_RESULT_PATHS = {
    ('impairment_valuation','recoverable_value'): ('asset-impairment', ('recoverable',)),
    ('derivative_contract','effective'): ('derivatives-hedge-accounting', ('derivatives','*','effective')),
    ('derivative_contract','ineffective'): ('derivatives-hedge-accounting', ('derivatives','*','ineffectiveness')),
    ('derivative_contract','closing_reserve'): ('derivatives-hedge-accounting', ('hedge_reserves','*','closing')),
    ('debt_population','closing_base'): ('debt-financing', ('debt',0,'closing')),
    ('cash_activity','closing_cash'): ('cash-flow-reporting', ('closing',)),
    ('derivative_contract','derivative_closing'): ('derivatives-hedge-accounting', ('derivatives','*','closing')),
    ('customer_contract', 'recognised_revenue'): ('revenue-recognition', ('period_revenue',)),
    ('receivable_population', 'closing_ar'): ('accounts-receivable', ('closing_ar',)),
    ('credit_exposure', 'closing_allowance'): ('financial-instruments-ecl', ('allowance',)),
    ('currency_exposure', 'monetary_fx_profit'): ('foreign-currency', ('monetary_fx_profit',)),
}

@dataclass
class IntakeResult:
    inventory: list = field(default_factory=list)
    validation: dict = field(default_factory=dict)
    proposal: dict = field(default_factory=dict)
    candidates: list = field(default_factory=list)
    transformations: list = field(default_factory=list)
    conflicts: list = field(default_factory=list)
    questions: list = field(default_factory=list)
    owner_inputs: list = field(default_factory=list)
    memory_candidates: list = field(default_factory=list)
    case: object = None
    lineage: list = field(default_factory=list)
    hypothesis_results: list = field(default_factory=list)

    def artifacts(self):
        out={k:copy.deepcopy(getattr(self,k)) for k in self.__dataclass_fields__ if k!='case'}
        if self.case:out['case']=self.case.record()
        return out

@dataclass(frozen=True)
class Binding:
    """Independently supplied source->reviewed owner input mapping.

    No implicit aggregation/conversion/defaults. The reviewed request is separately
    provided by the application/reviewer, not by the semantic model or raw file.
    """
    fact_id: str
    owner: str
    path: tuple
    kind: str = 'current'
    scope_id: str | None = None
    period_id: str | None = None
    calendar_id: str | None = None
    relationship_id: str | None = None

@dataclass(frozen=True)
class PopulationBinding:
    source_id: str
    source_column: str
    owner: str
    path: tuple
    owner_key: str = 'id'
    table: str = 'table'
    value_column: str = ''
    scope_id: str | None = None
    period_id: str | None = None
    calendar_id: str | None = None
    relationship_id: str | None = None

@dataclass(frozen=True)
class DocumentBinding:
    """Separately qualified source bytes and extraction dimensions for prose/evidence."""
    source_id: str
    owner: str
    path: tuple
    scope_id: str | None = None
    period_id: str | None = None
    calendar_id: str | None = None
    relationship_id: str | None = None

@dataclass(frozen=True)
class TextAssertion:
    """Reviewed single-capture extraction rule, tied to a native semantic input.

    Patterns cannot authorize accounting. Missing/ambiguous passages block; the
    original paragraph, source identity and exact owner target retain lineage.
    """
    source_id: str
    owner: str
    pattern: str
    path: tuple
    transformation: str = 'identity'
    scope_id: str | None = None
    period_id: str | None = None
    calendar_id: str | None = None
    relationship_id: str | None = None

@dataclass
class ReviewedInputPack:
    request: dict
    bindings: list
    populations: list = field(default_factory=list)
    documents: list = field(default_factory=list)
    text_assertions: list = field(default_factory=list)
    scope_id: str | None = None
    period_id: str | None = None
    calendar_id: str | None = None
    relationship_id: str | None = None
    scoped_packs: list = field(default_factory=list)

class GovernedPlanner:
    """Implements the existing Planner using validated, evidence-backed issues."""
    def __init__(self, proposal, candidates, questions=()):
        self.proposal=copy.deepcopy(proposal);self.candidates=copy.deepcopy(candidates)
        self.questions=copy.deepcopy(list(questions))
    def material_questions(self):return [copy.deepcopy(q) for q in self.questions if q['kind'] in ('blocking','confirmation')]
    def interpret(self,objective,facts,context,registry):
        p=self.proposal
        if objective!=p.objective.value:raise ValueError('Objective changed after validation')
        return Intent(p.primary_mode.value,[c.value for c in p.secondary_modes],
                      [dict(mode=c.value,reason='Validated supporting work mode') for c in p.supporting_modes],
                      p.bounded_owner.value if p.bounded_owner else None,
                      'Validated semantic work proposal').validate()
    def identify(self,objective,facts,context,registry):
        out=[]
        for c in self.proposal.issues:
            v=c.value;meta=registry.get(v['owner'])
            if not meta.get('production_available') or not meta.get('execution_available'):raise ValueError('Owner unavailable after proposal validation')
            out.append(Issue(v['id'],v['family'],v['owner'],'Validated source-supported work issue',
                             [v['family']],list(v['dependencies']),scope_id=v.get('scope_id'),period_id=v.get('period_id')))
        by_owner={(i.owner,i.scope_id):i for i in out}
        for issue in out:
            supplied=facts.get(issue.source_inputs[0],{})
            if isinstance(supplied,list):
                supplied=next((r for r in supplied if r.get('scope_id',r.get('entity'))==issue.scope_id and r.get('period_id')==issue.period_id),{})
            for imp in supplied.get('imports',[]):
                matches=[i for i in out if i.owner==imp.get('package') and (i.scope_id is None or i.scope_id==imp['case'].get('scope_id',imp['case'].get('entity'))) and (i.period_id is None or i.period_id==imp['case'].get('period_id'))]
                if len(matches)!=1:raise ValueError('Required exact owner dependency absent from semantic issues')
                upstream=matches[0].id
                if upstream not in issue.dependencies:issue.dependencies.append(upstream)
        return out


class Intake:
    def __init__(self, planner, registry=None):
        from orchestration.registry import Registry
        self.planner=planner;self.registry=registry or Registry()

    def prepare(self, objective, sources, company_records, scope, conversation=()):
        result=IntakeResult()
        try:
            inventory=Inventory(sources);result.inventory=inventory.normalized()
            current,ctx_conflicts=company_context(copy.deepcopy(company_records),scope)
            for k,v in scope.items():
                if k in current and current[k]!=v:ctx_conflicts.append(k)
                else:current[k]=copy.deepcopy(v)
            for k in set(ctx_conflicts):current.pop(k,None)
            req=RequestContext(objective,tuple(conversation),copy.deepcopy(result.inventory),
                               copy.deepcopy(company_records),self.registry.snapshot(),__import__('orchestration.scopes',fromlist=['scope_registry']).scope_registry(current).record())
            proposal=self.planner.propose(req)
            validation=ProposalValidator(self.registry).validate(proposal,inventory,current,objective)
            result.validation=validation.record()
            if not validation.accepted:
                result.questions=[dict(kind='blocking',attribute='period_candidate',question='Resolve exact material Period and calendar before qualifying accounting work.')] if any(e.get('code')=='UNRESOLVED_PERIOD' for e in validation.errors) else [dict(kind='blocking',attribute='scope_candidate',question='Resolve ambiguous or unregistered Scope Candidate before qualifying accounting work.')] if any(e.get('code')=='UNRESOLVED_SCOPE' for e in validation.errors) else [dict(kind='blocking',attribute='proposal',question='Resolve invalid semantic proposal.')];return result
            proposal=validation.proposal;result.proposal=proposal.record();result._current=current
            fields=inventory.fields()
            for key in sorted(set(ctx_conflicts)):
                result.conflicts.append(dict(attribute=key,kind='context',status='DISPUTED'))
            for f in proposal.facts:
                row=asdict(f);row['promotion']='unresolved'
                refs=[fields[e] for e in f.claim.evidence]
                row['lineage']=copy.deepcopy(refs)
                if f.conflicts:
                    row['promotion']='disputed'
                    result.conflicts.append(dict(id='declared-'+f.id,attribute=f.attribute,scope_id=f.dimensions.get('scope_id',f.dimensions.get('entity',current['entity'])),fact_ids=[f.id]+f.conflicts,kind='declared',status='DISPUTED'))
                elif f.claim.status=='ASSUMED':row['promotion']='assumed'
                elif f.claim.status=='DISPUTED':row['promotion']='disputed'
                elif f.claim.status in {'EXTRACTED','OBSERVED','CALCULATED'} and f.claim.confidence>=.95 and not f.confirmation_required:
                    # Source numeric rows establish source facts only. They never
                    # certify accounting reliability, classification or causation.
                    dimensions_ok=all(f.dimensions.get(k) for k in ('entity','period','comparator'))
                    for ref in refs:
                        meta=inventory.extractions[ref['source_id']].source['metadata']
                        for key in ('entity','period','currency','comparator'):
                            if key in f.dimensions and meta.get(key)!=f.dimensions[key]:dimensions_ok=False
                        if meta.get('controlled_export') is not True:dimensions_ok=False
                        loc=ref['location']
                        for table in inventory.extractions[ref['source_id']].tables:
                            if table['name']!=loc.get('table'):continue
                            for source_row in table['rows']:
                                if source_row['source_row']!=loc.get('row'):continue
                                for key in ('currency','entity','comparator','unit'):
                                    original=source_row['original']
                                    if original.get(key) and original[key]!=f.dimensions.get(key):dimensions_ok=False
                    if dimensions_ok and (f.transformation in {'decimal','iso_date','boolean'} or (f.claim.status=='EXTRACTED' and f.transformation=='identity' and len(refs)==1 and refs[0]['location'].get('table'))):row['promotion']='established'
                if f.transformation!='identity' and refs:
                    value=transform(refs[0]['value'],f.transformation)
                    result.transformations.append(dict(id='transform-'+f.id,source_fields=list(f.claim.evidence),
                        method=f.transformation,output=value,reason='Explicit validated field normalization',
                        input_fingerprints=[ref['extracted_fingerprint'] for ref in refs]))
                result.candidates.append(row)
            # Compare one semantic metric at matching scope, preserving every source.
            groups={}
            for row in result.candidates:
                key=(row['family'],row['attribute'],canonical(row['dimensions']))
                groups.setdefault(key,[]).append(row)
            for key,rows in groups.items():
                if len({canonical(r['claim']['value']) for r in rows})>1:
                    ids=[r['id'] for r in rows]
                    result.conflicts.append(dict(id='conflict-'+str(len(result.conflicts)+1),fact_ids=ids,
                        attribute=key[1],scope_id=rows[0]['dimensions'].get('scope_id',rows[0]['dimensions'].get('entity',current['entity'])),kind='source',status='DISPUTED'))
                    for r in rows:r['promotion']='disputed';r['conflicts']=ids
            for attribute,c in proposal.context_candidates.items():
                candidate_scope=c.value['scope_id'] if isinstance(c.value,dict) else current['entity']
                value=c.value['value'] if isinstance(c.value,dict) else c.value
                from orchestration.scopes import execution_scopes
                scoped_current=execution_scopes(current)[candidate_scope]
                conflict=attribute in scoped_current and scoped_current[attribute]!=value
                result.memory_candidates.append(dict(attribute=attribute,value=copy.deepcopy(value),scope_id=candidate_scope,
                    status='PROPOSED',semantic_status=c.status,source_refs=c.evidence,conflict=conflict))
                if conflict:result.conflicts.append(dict(attribute=attribute,scope_id=candidate_scope,kind='context',status='DISPUTED'))
            for candidate in proposal.entities:
                if candidate.status=='UNRESOLVED':
                    result.questions.append(dict(kind='blocking',attribute='scope_candidate',scope_id=None,question='Resolve unregistered Scope Candidate before adding it to governed company context.'))
            candidates={r['id']:r for r in result.candidates}
            for issue in proposal.issues:
                v=issue.value;available=[candidates[id] for id in v['fact_ids']]
                unresolved=[r['id'] for r in available if r['promotion']!='established']
                present={r['attribute'] for r in available if r['promotion']=='established'}
                missing=sorted(set(v['required_fields'])-present)
                issue_scope=v.get('scope_id') or next(iter({r['dimensions'].get('scope_id',r['dimensions'].get('entity',current['entity'])) for r in available}))
                result.owner_inputs.append(dict(issue_id=v['id'],target_owner=v['owner'],scope_id=issue_scope,period_id=v.get('period_id'),family=v['family'],
                    available_fact_ids=v['fact_ids'],required_fields=v['required_fields'],missing_fields=missing,
                    unresolved_judgments=unresolved,source_mappings=[dict(fact_id=r['id'],refs=r['claim']['evidence']) for r in available],
                    transformations=[t['id'] for t in result.transformations if t['id'][10:] in v['fact_ids']],
                    status='candidate',review_required=True,
                    owner_contract_inputs=copy.deepcopy(self.registry.get(v['owner']).get('inputs',[])),
                    qualification_required=['native source evidence','knowledge review','applicability review','independent exact-case certification']))
                for key in missing:self._question(result,'blocking',key,v['owner'],issue_scope,v.get('period_id'))
                for id in unresolved:
                    r=candidates[id]
                    # Exact document wording is already answerable from source.
                    # Preserve owner-review candidates without asking the user to
                    # repeat quoted terms or treating them as accounting truth.
                    sourced_wording=(r['claim']['status'] in ('EXTRACTED','OBSERVED') and r['transformation']=='identity' and isinstance(r['claim']['value'],str) and r['claim']['evidence'] and not r['conflicts'])
                    if sourced_wording:continue
                    self._question(result,'blocking' if r['promotion']=='disputed' else 'confirmation',r['attribute'],v['owner'],issue_scope,v.get('period_id'))
            for conflict in result.conflicts:self._question(result,'blocking',conflict['attribute'],'',conflict.get('scope_id'))
            for c in proposal.missing_facts:
                v=c.value;key=v['attribute']
                # Context and actual extracted fields answer questions; a model
                # missing-fact assertion does not override supplied evidence.
                question_scope=v.get('scope_id',current['entity'])
                from orchestration.scopes import execution_scopes
                scoped_current=execution_scopes(current)[question_scope]
                answered=key in scoped_current or (question_scope==current['entity'] and key in current) or any(r['attribute']==key and r['promotion']=='established' and r['dimensions'].get('scope_id',r['dimensions'].get('entity'))==question_scope and (v.get('period_id') is None or r['dimensions'].get('period_id')==v['period_id']) for r in result.candidates)
                if not answered:self._question(result,v['kind'],key,v['owner'],question_scope,v.get('period_id'))
            for key in ('entity','framework','jurisdiction','period_start','reporting_period','currency'):
                if not current.get(key):self._question(result,'blocking',key,'')
            result._inventory=inventory;result._proposal=proposal;result._current=current
            result._seal=self._seal(result)
            return result
        except (ValueError,TypeError,KeyError,AttributeError,ArithmeticError):
            result.validation=dict(accepted=False,errors=[dict(kind='blocking',code='INVALID_INTAKE',location='source/request')])
            result.questions=[dict(kind='blocking',attribute='input',question='Supply valid supported source extraction and execution dimensions.')]
            return result

    @staticmethod
    def _seal(result):
        keys=('inventory','validation','proposal','candidates','transformations','conflicts','questions','owner_inputs','memory_candidates')
        return digest(dict(fields={k:getattr(result,k) for k in keys},proposal=result._proposal.record(),context=result._current))

    @staticmethod
    def _question(result,kind,attribute,owner,scope_id=None,period_id=None):
        # Fixed/validated labels only; no source paragraphs or model rationale.
        multiple=hasattr(result,'_current') and len(result._current.get('scopes',result._current.get('execution_scopes',[])))>1
        multiple=multiple or any(r.get('dimensions',{}).get('entity')!=scope_id for r in result.candidates if r.get('dimensions',{}).get('entity'))
        question=dict(kind=kind,attribute=attribute,owner=owner,scope_id=scope_id,period_id=period_id,question=('Resolve '+scope_id+'’s ' if scope_id and multiple else 'Resolve ')+attribute.replace('_',' ')+'.')
        if not any(q['attribute']==attribute and q['kind']==kind and q.get('scope_id')==scope_id and q.get('period_id')==period_id for q in result.questions):result.questions.append(question)

    def execute(self, prepared, pack=None):
        """Run existing CAO against separately reviewed and exactly mapped inputs.

        Disputes keep the final Case partial even when independent qualified work
        can run. Disputed/inferred fields cannot be bound into owner source facts.
        """
        if not prepared.validation.get('accepted'):return prepared
        prepared._inventory.verify()
        if prepared._seal!=self._seal(prepared):raise ValueError('Prepared proposal/candidates changed after validation')
        request=dict(case_id='intake-case',objective=prepared._proposal.objective.value,
                     requested_output='Governed accounting intake review',scope=copy.deepcopy(prepared._current),facts={})
        if pack is not None:
            if not isinstance(pack,ReviewedInputPack):raise ValueError('Separate ReviewedInputPack required')
            request=copy.deepcopy(pack.request)
            if request.get('objective')!=prepared._proposal.objective.value:raise ValueError('Reviewed objective mismatch')
            for k,v in prepared._current.items():
                if request.get('scope',{}).get(k)!=v:raise ValueError('Reviewed scope mismatch')
            candidates={r['id']:r for r in prepared.candidates}
            from orchestration.execution import OwnerInputs,populations
            owners=OwnerInputs(request['scope'])
            for family,native in populations(request.get('facts',{})):
                if family in FACT_ADAPTERS:owners.add(FACT_ADAPTERS[family][0],native)
            def binding_key(binding):return owners.key(binding.owner,binding.scope_id,binding.period_id)
            from orchestration.scopes import scope_registry
            registered=scope_registry(request['scope'])
            def qualify_source(source_id,key,binding):
                extraction=prepared._inventory.extractions.get(source_id)
                if extraction is None:raise ValueError('Source inventory identity absent')
                meta=extraction.source['metadata'];native=owners[key];target=registered.get(native['entity'])
                source_scope=meta.get('scope_id',meta.get('entity'))
                if meta.get('scope_id') and meta.get('entity') and meta['scope_id']!=meta['entity']:raise ValueError('Source Scope/entity metadata conflict')
                origin=registered.get(source_scope)
                from orchestration.scopes import execution_scopes
                origin_context=execution_scopes(request['scope'])[source_scope]
                for dimension in ('currency','framework','jurisdiction'):
                    if dimension in meta and meta[dimension]!=origin_context[dimension]:raise ValueError('Qualified source metadata differs from governed origin Scope')
                if source_scope!=target.scope_id:
                    if target.scope_type=='LEGAL_ENTITY':
                        if origin.scope_type not in ('GROUP','SUBGROUP') or target.scope_id not in meta.get('applies_to_scope_ids',[]):raise ValueError('Legal owner source population crosses Scope')
                    elif target.scope_type not in ('GROUP','SUBGROUP'):raise ValueError('Source Scope mismatch')
                from orchestration.temporal_inputs import validate_source
                validate_source(request['scope'],native,meta,binding)
                return extraction
            group_contract=request.get('group_consumer')
            if group_contract is not None:
                group_source=group_contract.get('context_source',{})
                extraction=prepared._inventory.extractions.get(group_source.get('source_id'))
                if extraction is None:raise ValueError('Group context source missing from inventory')
                meta=extraction.source['metadata']
                if (meta.get('scope_id',meta.get('entity')),meta.get('framework'),meta.get('currency'))!=(group_source.get('scope_id'),group_source.get('framework'),group_source.get('currency')):raise ValueError('Group context source differs from actual scoped inventory')
                if group_contract.get('qualified_context_fingerprint')!=extraction.source['fingerprint']:raise ValueError('Group context source fingerprint differs')

            repeated={pkg for pkg in owners.packages.values() if list(owners.packages.values()).count(pkg)>1}
            if repeated:
                expected={key for key,pkg in owners.packages.items() if pkg in repeated};seen_packs=set();pack_records=[]
                for child in pack.scoped_packs:
                    if not isinstance(child,ReviewedInputPack) or not child.scope_id or child.scoped_packs:raise ValueError('Independent scoped ReviewedInputPack required')
                    rows=list(populations(child.request.get('facts',{})))
                    if len(rows)!=1 or rows[0][0] not in FACT_ADAPTERS:raise ValueError('Scoped pack must certify one exact execution')
                    family,native=rows[0];key=owners.key(FACT_ADAPTERS[family][0],child.scope_id,child.period_id)
                    if key not in expected or key in seen_packs or native.get('scope_id',native['entity'])!=child.scope_id or digest(native)!=digest(owners[key]):raise ValueError('Scoped pack reused across executions')
                    if child.request.get('objective')!=request['objective']:raise ValueError('Scoped pack objective differs')
                    if any(binding_key(x)!=key for x in child.bindings):raise ValueError('Scoped pack source population mixed')
                    wanted=[asdict(x) for x in pack.bindings if binding_key(x)==key]
                    if canonical([asdict(x) for x in child.bindings])!=canonical(wanted):raise ValueError('Scoped pack bindings differ from exact execution')
                    for field in ('populations','documents','text_assertions'):
                        wanted=[asdict(x) for x in getattr(pack,field) if binding_key(x)==key]
                        if canonical([asdict(x) for x in getattr(child,field)])!=canonical(wanted):raise ValueError('Scoped pack source evidence differs')
                    from orchestration.temporal_inputs import validate_pack
                    validate_pack(request['scope'],child,[native])
                    seen_packs.add(key);pack_records.append(dict(node=key,scope_id=child.scope_id,pack_fingerprint=digest(dict(request=child.request,bindings=[asdict(x) for x in child.bindings]))))
                if seen_packs!=expected:raise ValueError('Repeated owners require separate ReviewedInputPacks')
                request['reviewed_scope_packs']=pack_records

            from orchestration.temporal_inputs import validate_pack
            validate_pack(request['scope'],pack,list(owners.values()))
            if pack.scope_id is not None and any(native.get('scope_id',native['entity'])!=pack.scope_id for native in owners.values()):raise ValueError('ReviewedInputPack certifies another Scope')
            for owner,native in owners.items():
                if owners.packages[owner] in repeated:
                    actual_sources={ref['source_id'] for binding in pack.bindings if binding_key(binding)==owner for ref in candidates[binding.fact_id]['lineage']}
                    declared=native.get('source_population')
                    if not isinstance(declared,list) or not declared or len(set(declared))!=len(declared) or set(declared)!=actual_sources:raise ValueError('Repeated owner source population differs from exact scoped fact lineage')
                    qualified=native.get('qualified_scope_sources')
                    if not isinstance(qualified,list) or len(qualified)!=len(declared) or {r['source_id'] for r in qualified}!=set(declared):raise ValueError('Qualified scoped source manifest required')
                    for row in qualified:
                        actual=prepared._inventory.extractions[row['source_id']].source
                        if canonical(row)!=canonical(dict(source_id=actual['id'],fingerprint=actual['fingerprint'],metadata=actual['metadata'])):raise ValueError('Scoped native source qualification differs from actual inventory')
                    for source_id in declared:
                        meta=prepared._inventory.extractions[source_id].source['metadata']
                        if meta.get('scope_id',meta.get('entity'))!=native['entity']:raise ValueError('Owner source population crosses Scope')
                manifest=native.get('source_semantic_controls')
                if native.get('qualified_source_documents') and manifest is None:raise ValueError('Qualified source documents require reviewed semantic controls')
                if manifest is not None:
                    actual=dict(text_assertions=[asdict(x) for x in pack.text_assertions if binding_key(x)==owner],
                        populations=[asdict(x) for x in pack.populations if binding_key(x)==owner])
                    if canonical(manifest)!=canonical(actual):raise ValueError('Required reviewed source semantic-control population omitted or changed')
            for binding in pack.documents:
                if not isinstance(binding,DocumentBinding) or binding_key(binding) not in owners:raise ValueError('Invalid reviewed source document binding')
                source=qualify_source(binding.source_id,binding_key(binding),binding)
                expected=at(owners[binding_key(binding)],list(binding.path))
                actual=dict(fingerprint=source.source['fingerprint'],metadata=source.source['metadata'])
                if canonical(expected)!=canonical(actual):raise ValueError('Source document changed after separate accounting qualification')
                prepared.lineage.append(dict(source_document=binding.source_id,owner=binding.owner,owner_input_path=list(binding.path),binding_kind='qualified_document',source_description=source.source['name']))
            for assertion in pack.text_assertions:
                if not isinstance(assertion,TextAssertion) or binding_key(assertion) not in owners or len(assertion.pattern)>300:
                    raise ValueError('Invalid reviewed text assertion')
                extraction=qualify_source(assertion.source_id,binding_key(assertion),assertion)
                if not extraction or not extraction.blocks:raise ValueError('Text assertion source absent')
                if assertion.transformation in ('decimal','calendar_date') and extraction.source['metadata'].get('entity')!=owners[binding_key(assertion)]['entity']:raise ValueError('Text amount/date crosses source legal entity')
                if assertion.transformation=='decimal' and extraction.source['metadata'].get('currency')!=dimensions(owners[binding_key(assertion)])[-1]:raise ValueError('Text amount crosses source currency')
                pattern=re.compile(assertion.pattern)
                if pattern.groups!=1:raise ValueError('Single explicit text capture required')
                matches=[(field,match.group(1)) for field in extraction.fields.values() for match in pattern.finditer(str(field['value']))]
                if len(matches)!=1:raise ValueError('Missing or ambiguous source text assertion')
                field,value=matches[0]
                value=transform(value,assertion.transformation)
                expected=at(owners[binding_key(assertion)],list(assertion.path))
                if canonical(value)!=canonical(expected):raise ValueError('Source text contradicts reviewed accounting input')
                prepared.lineage.append(dict(source_document=assertion.source_id,extracted_fields=[field['id']],owner=assertion.owner,
                    owner_input_path=list(assertion.path),binding_kind='reviewed_text_assertion',transformation=assertion.transformation))
            for population in pack.populations:
                if not isinstance(population,PopulationBinding) or binding_key(population) not in owners:raise ValueError('Invalid source population binding')
                qualify_source(population.source_id,binding_key(population),population)
                fields=[value for item in prepared.inventory for value in item['fields'].values() if value['source_id']==population.source_id and value['location'].get('table')==population.table and value['location'].get('column')==population.source_column]
                ids=[value['value'] for value in fields]
                native=at(owners[binding_key(population)],list(population.path))
                expected_ids=list(native) if isinstance(native,dict) else [row[population.owner_key] for row in native] if isinstance(native,list) else []
                if not ids or len(set(ids))!=len(ids) or sorted(ids)!=sorted(expected_ids):raise ValueError('Source and reviewed owner population differ')
                if population.value_column:
                    if not isinstance(native,dict):raise ValueError('Key/value population requires a native mapping')
                    all_fields=prepared._inventory.fields()
                    for keyfield in fields:
                        related=[f for f in all_fields.values() if f['source_id']==population.source_id and f['location'].get('table')==population.table and f['location'].get('row')==keyfield['location'].get('row') and f['location'].get('column')==population.value_column]
                        if len(related)!=1 or number(related[0]['value'])!=number(native[keyfield['value']]):raise ValueError('Keyed source population value differs')
                    prepared.lineage.append(dict(source_document=population.source_id,owner=population.owner,owner_input_path=list(population.path),binding_kind='complete_keyed_population'))
            seen=set();bound=set()
            for binding in pack.bindings:
                if not isinstance(binding,Binding) or binding.fact_id not in candidates or binding_key(binding) not in owners:raise ValueError('Invalid owner binding')
                c=candidates[binding.fact_id]
                if c['promotion']!='established':raise ValueError('Unresolved source cannot become owner input')
                if binding.kind in ('current','owner_result'):
                    if c['dimensions'].get('comparator')!='actual':raise ValueError('Nonactual source cannot become current owner input')
                elif binding.kind=='comparator':
                    native=owners[binding_key(binding)];comp=(native.get('diagnostic') or {}).get('comparator',{})
                    kind=c['dimensions'].get('comparator');expected_kind='actual' if kind=='prior_actual' else kind
                    valid=comp.get('kind')==expected_kind and comp.get('period')==c['dimensions'].get('period') and binding.path==('documents',comp.get('doc'),'content','amount')
                    balance=native.get('balance_diagnostics')
                    if balance and isinstance(balance,dict) and set(balance)=={'doc'}:
                        try:
                            source=at(native,['documents',balance['doc'],'content'])
                            valid=valid or (kind=='prior_actual' and source['prior_kind']=='actual' and source['prior_period']==c['dimensions'].get('period') and binding.path[:4]==('documents',balance['doc'],'content','prior') and len(binding.path) in (5,6))
                        except (ValueError,KeyError,TypeError):pass
                    if binding.owner!='management-accounting-analytics' or not valid:raise ValueError('Comparator binding contract mismatch')
                else:raise ValueError('Unknown binding kind')
                if c['candidate_owner'] and binding.owner!=c['candidate_owner']:raise ValueError('Owner binding crosses boundary')
                native=owners[binding_key(binding)]
                from orchestration.temporal_inputs import validate_binding
                validate_binding(request['scope'],native,binding,c['dimensions'])
                if c['dimensions'].get('amount_currency'):
                    if binding.owner!='intercompany-accounting' or binding.path[:1]!=('pairs',) or binding.path[-1] not in ('confirmed_a','confirmed_b') or at(native,list(binding.path[:-1])+['currency'])!=c['dimensions']['amount_currency']:raise ValueError('Nominal amount denomination differs from native owner contract')
                if c['dimensions'].get('scope_id',c['dimensions'].get('entity'))!=native['entity']:
                    if len(binding.path)<4 or binding.path[:2]!=('entities',c['dimensions'].get('entity')) or binding.path[2]!='balances' or c['dimensions'].get('currency')!=dimensions(native)[-1]:
                        raise ValueError('Numeric source entity/currency differs from semantic assembly target')
                target=(binding_key(binding),binding.path)
                if target in seen:raise ValueError('Duplicate owner target')
                seen.add(target);bound.add(binding.fact_id)
                if binding.kind=='owner_result':
                    contract=OWNER_RESULT_PATHS.get((c['family'],c['attribute']))
                    if not contract or contract[0]!=binding.owner or len(contract[1])!=len(binding.path) or any(expected!='*' and expected!=actual for expected,actual in zip(contract[1],binding.path)):raise ValueError('Owner result semantic metric contract mismatch')
                    from orchestration.registry import production
                    result=production.assess_case(binding.owner,owners[binding_key(binding)])
                    if result.get('status')!='complete':raise ValueError('Reviewed result binding requires qualified owner result')
                    value=at(result['calculations'],list(binding.path))
                else:value=at(owners[binding_key(binding)],list(binding.path))
                matches=number(value)==number(c['claim']['value']) if binding.kind=='owner_result' and c['transformation']=='decimal' else canonical(value)==canonical(c['claim']['value'])
                if not matches:raise ValueError('Reviewed owner input differs from prepared source fact')
                prepared.lineage.append(dict(fact_id=c['id'],owner=binding.owner,scope_id=native['entity'],producing_node=binding_key(binding),owner_input_path=list(binding.path),binding_kind=binding.kind,
                    extracted_fields=c['claim']['evidence'],source_lineage=c['lineage']))
            if any(c['promotion']=='established' and c['candidate_owner'] and c['id'] not in bound for c in candidates.values()):raise ValueError('Established owner fact omitted from reviewed mapping')
            selected={i.value['owner'] for i in prepared._proposal.issues}
            if set(owners.packages.values())-selected:raise ValueError('Reviewed pack includes unselected owners')
            for owner in owners:
                matching=[r for r in prepared.owner_inputs if r['target_owner']==owners.packages[owner] and r['scope_id']==owners[owner]['entity'] and (r.get('period_id') is None or r['period_id']==owners[owner].get('period_id'))]
                if not matching or not any(candidates[id]['promotion']=='established' and id in bound for r in matching for id in r['available_fact_ids']):raise ValueError('Owner has no traceable established input')
                for r in matching:
                    for key in r['required_fields']:
                        if not any(candidates[id]['attribute']==key and id in bound for id in r['available_fact_ids']):raise ValueError('Required prepared input not bound')
        cao=CAO(GovernedPlanner(prepared._proposal,prepared.candidates,prepared.questions),self.registry)
        case=cao.run(request)
        case.requested_output='Governed accounting intake review'
        for row in prepared.candidates:
            public_fact=dict(id=row['id'],attribute=row['attribute'],value=copy.deepcopy(row['claim']['value']),
                             semantic_status=row['claim']['status'],scope_id=row['dimensions'].get('scope_id',row['dimensions'].get('entity')),source_refs=row['claim']['evidence'])
            bucket={'established':'established','assumed':'assumed','disputed':'disputed'}.get(row['promotion'])
            if bucket=='assumed':case.facts[bucket].append(dict(attribute=row['attribute'],value='Unconfirmed source assumption'))
            elif bucket:case.facts[bucket].append(public_fact)
        case.memory_candidates.extend(copy.deepcopy(prepared.memory_candidates))
        # Evidence testing is arithmetic over already governed owner results;
        # it cannot generate accounting conclusions, journals or approval events.
        completed={n['selected_skill']:n['result'] for n in case.workplan_nodes if n['status']=='complete' and n['result'] and sum(x['selected_skill']==n['selected_skill'] for x in case.workplan_nodes)==1}
        for h in prepared._proposal.hypotheses:
            v=h.value;checks=[];refs=[]
            for test in v['tests']:
                try:
                    left=number(at(completed[test['left_owner']]['calculations'],test['left_path']))
                    right=number(at(completed[test['right_owner']]['calculations'],test['right_path']))*number(test['factor'])
                    op=test['operator']
                    checks.append(abs(left)>abs(right) if op=='magnitude_above' else abs(left)<abs(right) if op=='magnitude_below' else left==right)
                    refs.append(dict(test=copy.deepcopy(test),left=str(left),right=str(right)))
                except (ValueError,TypeError,KeyError,ArithmeticError):checks.append(None)
            disposition='UNRESOLVED' if None in checks else 'SUPPORTED' if all(checks) else 'REJECTED' if not any(checks) else 'PARTIALLY_SUPPORTED'
            prepared.hypothesis_results.append(dict(id=v['id'],description=v['description'],disposition=disposition,
                evidence=refs,source_refs=h.evidence,semantic_status=h.status,accounting_authority=False))
            for conclusion in case.conclusions:
                conclusion['limitations'].append('Management explanation '+disposition.lower().replace('_',' ')+' by the supplied accounting and diagnostic evidence; attribution remains scoped to that evidence.')
        prepared.case=case;return prepared

    def public(self, prepared, route='answer'):
        from interfaces.public_output import public_record
        if prepared.case:return CAO().public(prepared.case,route)
        return public_record(dict(guidance='Accounting intake requires further evidence.',status='blocked',
            open_items=[q['question'] for q in prepared.questions]),route=route)
