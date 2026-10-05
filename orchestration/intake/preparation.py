"""Candidate resolution and audited owner preparation; never creates certification."""
import copy
from dataclasses import dataclass, field, asdict
from orchestration.runtime import CAO, company_context, at, dimensions, digest, number
from orchestration.intent import Intent
from orchestration.planning import Issue, FACT_ADAPTERS
from .sources import Inventory, fingerprint, canonical
from .semantic import RequestContext, ProposalValidator, transform

# Explicit semantic contracts prevent equal numbers from substituting a different
# accounting concept. Extensions require a governed producer calculation path.
OWNER_RESULT_PATHS = {
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

@dataclass(frozen=True)
class PopulationBinding:
    source_id: str
    source_column: str
    owner: str
    path: tuple
    owner_key: str = 'id'
    table: str = 'table'

@dataclass(frozen=True)
class DocumentBinding:
    """Separately qualified source bytes and extraction dimensions for prose/evidence."""
    source_id: str
    owner: str
    path: tuple

@dataclass
class ReviewedInputPack:
    request: dict
    bindings: list
    populations: list = field(default_factory=list)
    documents: list = field(default_factory=list)

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
                             [v['family']],list(v['dependencies'])))
        by_owner={i.owner:i for i in out}
        for issue in out:
            supplied=facts.get(issue.source_inputs[0],{})
            for imp in supplied.get('imports',[]):
                if imp.get('package') not in by_owner:raise ValueError('Required actual owner dependency absent from semantic issues')
                upstream=by_owner[imp['package']].id
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
                               copy.deepcopy(company_records),self.registry.snapshot())
            proposal=self.planner.propose(req)
            validation=ProposalValidator(self.registry).validate(proposal,inventory,current,objective)
            result.validation=validation.record()
            if not validation.accepted:
                result.questions=[dict(kind='blocking',attribute='proposal',question='Resolve invalid semantic proposal.')];return result
            proposal=validation.proposal;result.proposal=proposal.record()
            fields=inventory.fields()
            for key in sorted(set(ctx_conflicts)):
                result.conflicts.append(dict(attribute=key,kind='context',status='DISPUTED'))
            for f in proposal.facts:
                row=asdict(f);row['promotion']='unresolved'
                refs=[fields[e] for e in f.claim.evidence]
                row['lineage']=copy.deepcopy(refs)
                if f.conflicts:
                    row['promotion']='disputed'
                    result.conflicts.append(dict(id='declared-'+f.id,attribute=f.attribute,fact_ids=[f.id]+f.conflicts,kind='declared',status='DISPUTED'))
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
                        attribute=key[1],kind='source',status='DISPUTED'))
                    for r in rows:r['promotion']='disputed';r['conflicts']=ids
            for attribute,c in proposal.context_candidates.items():
                conflict=attribute in current and current[attribute]!=c.value
                result.memory_candidates.append(dict(attribute=attribute,value=copy.deepcopy(c.value),
                    status='PROPOSED',semantic_status=c.status,source_refs=c.evidence,conflict=conflict))
                if conflict:result.conflicts.append(dict(attribute=attribute,kind='context',status='DISPUTED'))
            candidates={r['id']:r for r in result.candidates}
            for issue in proposal.issues:
                v=issue.value;available=[candidates[id] for id in v['fact_ids']]
                unresolved=[r['id'] for r in available if r['promotion']!='established']
                present={r['attribute'] for r in available if r['promotion']=='established'}
                missing=sorted(set(v['required_fields'])-present)
                result.owner_inputs.append(dict(issue_id=v['id'],target_owner=v['owner'],family=v['family'],
                    available_fact_ids=v['fact_ids'],required_fields=v['required_fields'],missing_fields=missing,
                    unresolved_judgments=unresolved,source_mappings=[dict(fact_id=r['id'],refs=r['claim']['evidence']) for r in available],
                    transformations=[t['id'] for t in result.transformations if t['id'][10:] in v['fact_ids']],
                    status='candidate',review_required=True,
                    owner_contract_inputs=copy.deepcopy(self.registry.get(v['owner']).get('inputs',[])),
                    qualification_required=['native source evidence','knowledge review','applicability review','independent exact-case certification']))
                for key in missing:self._question(result,'blocking',key,v['owner'])
                for id in unresolved:
                    r=candidates[id]
                    # Exact document wording is already answerable from source.
                    # Preserve owner-review candidates without asking the user to
                    # repeat quoted terms or treating them as accounting truth.
                    sourced_wording=(r['claim']['status'] in ('EXTRACTED','OBSERVED') and r['transformation']=='identity' and isinstance(r['claim']['value'],str) and r['claim']['evidence'] and not r['conflicts'])
                    if sourced_wording:continue
                    self._question(result,'blocking' if r['promotion']=='disputed' else 'confirmation',r['attribute'],v['owner'])
            for conflict in result.conflicts:self._question(result,'blocking',conflict['attribute'],'')
            for c in proposal.missing_facts:
                v=c.value;key=v['attribute']
                # Context and actual extracted fields answer questions; a model
                # missing-fact assertion does not override supplied evidence.
                answered=key in current or any(r['attribute']==key and r['promotion']=='established' for r in result.candidates)
                if not answered:self._question(result,v['kind'],key,v['owner'])
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
    def _question(result,kind,attribute,owner):
        # Fixed/validated labels only; no source paragraphs or model rationale.
        question=dict(kind=kind,attribute=attribute,owner=owner,question='Resolve '+attribute.replace('_',' ')+'.')
        if not any(q['attribute']==attribute and q['kind']==kind for q in result.questions):result.questions.append(question)

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
            candidates={r['id']:r for r in prepared.candidates};owners={FACT_ADAPTERS[f][0]:v for f,v in request.get('facts',{}).items() if f in FACT_ADAPTERS}
            for binding in pack.documents:
                if not isinstance(binding,DocumentBinding) or binding.owner not in owners:raise ValueError('Invalid reviewed source document binding')
                source=prepared._inventory.extractions.get(binding.source_id)
                if not source:raise ValueError('Reviewed source document missing')
                expected=at(owners[binding.owner],list(binding.path))
                actual=dict(fingerprint=source.source['fingerprint'],metadata=source.source['metadata'])
                if canonical(expected)!=canonical(actual):raise ValueError('Source document changed after separate accounting qualification')
                prepared.lineage.append(dict(source_document=binding.source_id,owner=binding.owner,owner_input_path=list(binding.path),binding_kind='qualified_document',source_description=source.source['name']))
            for population in pack.populations:
                if not isinstance(population,PopulationBinding) or population.owner not in owners:raise ValueError('Invalid source population binding')
                fields=[value for item in prepared.inventory for value in item['fields'].values() if value['source_id']==population.source_id and value['location'].get('table')==population.table and value['location'].get('column')==population.source_column]
                ids=[value['value'] for value in fields]
                native=at(owners[population.owner],list(population.path))
                if not ids or not isinstance(native,list) or len(set(ids))!=len(ids) or sorted(ids)!=sorted(row[population.owner_key] for row in native):raise ValueError('Source and reviewed owner population differ')
            seen=set();bound=set()
            for binding in pack.bindings:
                if not isinstance(binding,Binding) or binding.fact_id not in candidates or binding.owner not in owners:raise ValueError('Invalid owner binding')
                c=candidates[binding.fact_id]
                if c['promotion']!='established':raise ValueError('Unresolved source cannot become owner input')
                if binding.kind in ('current','owner_result'):
                    if c['dimensions'].get('comparator')!='actual':raise ValueError('Nonactual source cannot become current owner input')
                elif binding.kind=='comparator':
                    native=owners[binding.owner];comp=(native.get('diagnostic') or {}).get('comparator',{})
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
                target=(binding.owner,binding.path)
                if target in seen:raise ValueError('Duplicate owner target')
                seen.add(target);bound.add(binding.fact_id)
                if binding.kind=='owner_result':
                    contract=OWNER_RESULT_PATHS.get((c['family'],c['attribute']))
                    if not contract or contract[0]!=binding.owner or len(contract[1])!=len(binding.path) or any(expected!='*' and expected!=actual for expected,actual in zip(contract[1],binding.path)):raise ValueError('Owner result semantic metric contract mismatch')
                    from orchestration.registry import production
                    result=production.assess_case(binding.owner,owners[binding.owner])
                    if result.get('status')!='complete':raise ValueError('Reviewed result binding requires qualified owner result')
                    value=at(result['calculations'],list(binding.path))
                else:value=at(owners[binding.owner],list(binding.path))
                matches=number(value)==number(c['claim']['value']) if binding.kind=='owner_result' and c['transformation']=='decimal' else canonical(value)==canonical(c['claim']['value'])
                if not matches:raise ValueError('Reviewed owner input differs from prepared source fact')
                prepared.lineage.append(dict(fact_id=c['id'],owner=binding.owner,owner_input_path=list(binding.path),binding_kind=binding.kind,
                    extracted_fields=c['claim']['evidence'],source_lineage=c['lineage']))
            if any(c['promotion']=='established' and c['candidate_owner'] and c['id'] not in bound for c in candidates.values()):raise ValueError('Established owner fact omitted from reviewed mapping')
            selected={i.value['owner'] for i in prepared._proposal.issues}
            if set(owners)-selected:raise ValueError('Reviewed pack includes unselected owners')
            for owner in owners:
                matching=[r for r in prepared.owner_inputs if r['target_owner']==owner]
                if not matching or not any(candidates[id]['promotion']=='established' and id in bound for r in matching for id in r['available_fact_ids']):raise ValueError('Owner has no traceable established input')
                for r in matching:
                    for key in r['required_fields']:
                        if not any(candidates[id]['attribute']==key and id in bound for id in r['available_fact_ids']):raise ValueError('Required prepared input not bound')
        cao=CAO(GovernedPlanner(prepared._proposal,prepared.candidates,prepared.questions),self.registry)
        case=cao.run(request)
        case.requested_output='Governed accounting intake review'
        for row in prepared.candidates:
            public_fact=dict(id=row['id'],attribute=row['attribute'],value=copy.deepcopy(row['claim']['value']),
                             semantic_status=row['claim']['status'],source_refs=row['claim']['evidence'])
            bucket={'established':'established','assumed':'assumed','disputed':'disputed'}.get(row['promotion'])
            if bucket=='assumed':case.facts[bucket].append(dict(attribute=row['attribute'],value='Unconfirmed source assumption'))
            elif bucket:case.facts[bucket].append(public_fact)
        case.memory_candidates.extend(copy.deepcopy(prepared.memory_candidates))
        # Evidence testing is arithmetic over already governed owner results;
        # it cannot generate accounting conclusions, journals or approval events.
        completed={n['selected_skill']:n['result'] for n in case.workplan_nodes if n['status']=='complete' and n['result']}
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
