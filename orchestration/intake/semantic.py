"""Untrusted semantic proposer contract and deterministic, fail-closed validation.

A model adapter implements propose(RequestContext)->StructuredProposal. No prose
can invoke an owner. Fixtures implement the same interface without network calls.
"""
import copy
import re
from datetime import date
from decimal import Decimal, InvalidOperation
from dataclasses import dataclass, field, asdict
from typing import Protocol
from orchestration.intent import Intent, WorkMode
from orchestration.planning import FACT_ADAPTERS
from .sources import canonical, bounded
from orchestration.scopes import execution_scopes

STATUSES = {'EXTRACTED','OBSERVED','INFERRED','USER_STATED','CONTEXT_DERIVED','CALCULATED','ASSUMED','DISPUTED','UNRESOLVED'}
COMPARATORS = {'actual','prior_actual','budget','forecast','standard','target'}
SOURCE_FAMILIES = {'trial_balance','general_ledger','pnl','balance_sheet','management_accounts','inventory_report','bom_routing','payroll_export','ap_export','ar_aging','bank_statement','fx_report','fixed_asset_register','lease_schedule','debt_schedule','revenue_report','contract','accounting_policy','reconciliation','close_checklist','control_matrix','audit_finding','management_commentary','management_memo','actuarial_report','valuation_report','unknown'}
DIMENSIONS = {'scope_id','entity','period','currency','unit','account_id','item_id','record_id','comparator','jurisdiction','framework','version','amount_currency'}
FRAMEWORKS = {'IFRS','US_GAAP','UK_GAAP','AASB'}
CONTEXT_ATTRIBUTES = {'entity','framework','jurisdiction','currency','year_end','systems','policies','gross_margin_basis','industry'}

@dataclass
class Claim:
    value: object
    status: str
    confidence: float
    rationale: str
    evidence: list = field(default_factory=list)

@dataclass
class FactCandidate:
    id: str
    family: str
    attribute: str
    claim: Claim
    dimensions: dict = field(default_factory=dict)
    candidate_owner: str = ''
    economic_id: str = ''
    extraction_method: str = 'semantic proposal'
    confirmation_required: bool = True
    transformation: str = 'identity'
    conflicts: list = field(default_factory=list)

@dataclass
class StructuredProposal:
    objective: Claim
    requested_output: Claim
    primary_mode: Claim
    secondary_modes: list = field(default_factory=list)
    supporting_modes: list = field(default_factory=list)
    entities: list = field(default_factory=list)
    periods: list = field(default_factory=list)
    frameworks: list = field(default_factory=list)
    jurisdictions: list = field(default_factory=list)
    classifications: dict = field(default_factory=dict)
    column_mappings: list = field(default_factory=list)
    issues: list = field(default_factory=list)
    facts: list = field(default_factory=list)
    assumptions: list = field(default_factory=list)
    disputed_facts: list = field(default_factory=list)
    missing_facts: list = field(default_factory=list)
    hypotheses: list = field(default_factory=list)
    context_candidates: dict = field(default_factory=dict)
    bounded_owner: Claim | None = None
    interpreted_objective: Claim | None = None

    def record(self):return asdict(self)

    @classmethod
    def from_record(cls, record):
        """Strict JSON adapter boundary. Reject unknown fields/approval payloads."""
        from dataclasses import fields
        def exact(value, target):
            if not isinstance(value,dict) or set(value)-{f.name for f in fields(target)}:raise ValueError('Unknown structured proposal field')
            return value
        def claim(value):return Claim(**exact(value,Claim))
        data=copy.deepcopy(exact(record,cls))
        for key in ('objective','requested_output','primary_mode'):
            data[key]=claim(data[key])
        for key in ('secondary_modes','supporting_modes','entities','periods','frameworks','jurisdictions','issues','assumptions','disputed_facts','missing_facts','hypotheses','column_mappings'):
            if key in data:data[key]=[claim(v) for v in data[key]]
        for key in ('classifications','context_candidates'):
            if key in data:data[key]={k:claim(v) for k,v in data[key].items()}
        for key in ('bounded_owner','interpreted_objective'):
            if data.get(key):data[key]=claim(data[key])
        if 'facts' in data:
            facts=[]
            for raw in data['facts']:
                raw=copy.deepcopy(exact(raw,FactCandidate));raw['claim']=claim(raw['claim']);facts.append(FactCandidate(**raw))
            data['facts']=facts
        return cls(**data)

@dataclass(frozen=True)
class RequestContext:
    objective: str
    conversation: tuple
    source_inventory: list
    company_context: list
    registry_metadata: list
    registered_scopes: list = field(default_factory=list)

class SemanticPlanner(Protocol):
    def propose(self, request: RequestContext) -> StructuredProposal: ...

class FixturePlanner:
    """Injected deterministic fixture; never selects owners by objective keywords."""
    def __init__(self, proposal):self.proposal=copy.deepcopy(proposal)
    def propose(self, request):
        if not isinstance(request,RequestContext):raise ValueError('RequestContext required')
        return copy.deepcopy(self.proposal)

@dataclass
class Validation:
    accepted: bool
    errors: list
    proposal: StructuredProposal | None = None
    def record(self):return dict(accepted=self.accepted,errors=self.errors)


def period(value):
    if not isinstance(value,list) or len(value)!=2 or any(not isinstance(x,str) for x in value):raise ValueError('ISO date period pair required')
    start,end=[date.fromisoformat(x) for x in value]
    if start>end or [start.isoformat(),end.isoformat()]!=value:raise ValueError('Invalid period')


def transform(value, method):
    if method=='identity':return copy.deepcopy(value)
    if method=='decimal':
        if type(value) not in (str,int,float) or not re.fullmatch(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)',str(value)):raise ValueError('Malformed amount; explicit decimal required')
        n=Decimal(str(value))
        if not n.is_finite() or len(str(value))>100:raise ValueError('Amount invalid')
        return str(n)
    if method=='boolean':
        if type(value) is bool:return value
        if value not in ('true','false'):raise ValueError('Explicit boolean required')
        return value=='true'
    if method=='percentage':
        return str(Decimal(transform(value,'decimal'))/Decimal(100))
    if method=='calendar_date':
        from datetime import datetime
        if not isinstance(value,str):raise ValueError('Explicit calendar date required')
        return datetime.strptime(value,'%d %B %Y').date().isoformat()
    if method=='iso_date':
        if not isinstance(value,str) or date.fromisoformat(value).isoformat()!=value:raise ValueError('Ambiguous date')
        return value
    raise ValueError('Unsupported transformation')


class ProposalValidator:
    def __init__(self, registry):self.registry=registry

    def validate(self, proposal, inventory, context, objective):
        errors=[]
        def fail(code, location):errors.append(dict(kind='blocking',code=code,location=location))
        try:
            inventory.verify();fields=inventory.fields();registered=execution_scopes(context)
            if not isinstance(proposal,StructuredProposal):raise ValueError('StructuredProposal required')
            bounded(proposal.record())
            # Envelope validation is recursive; every semantic assertion uses Claim.
            def claim(c,loc):
                if not isinstance(c,Claim):raise ValueError('Claim envelope required: '+loc)
                if c.status not in STATUSES:raise ValueError('Invalid semantic status: '+loc)
                if type(c.confidence) not in (int,float) or not 0<=c.confidence<=1:raise ValueError('Invalid confidence: '+loc)
                if not isinstance(c.rationale,str) or not c.rationale.strip():raise ValueError('Rationale required: '+loc)
                if not isinstance(c.evidence,list) or len(set(c.evidence))!=len(c.evidence) or any(e not in fields for e in c.evidence):raise ValueError('Evidence absent/duplicated: '+loc)
                if c.status in {'EXTRACTED','OBSERVED','CALCULATED'} and not c.evidence:raise ValueError('Sourced status needs evidence: '+loc)
                if c.status=='CONTEXT_DERIVED':
                    known=any(c.value==v for v in context.values())
                    if isinstance(c.value,dict) and set(c.value)=={'scope_id','value'} and c.value['scope_id'] in registered:
                        known=any(c.value['value']==v for v in registered[c.value['scope_id']].values())
                    if not known:raise ValueError('Unknown context assertion: '+loc)
                if c.status in {'UNRESOLVED','DISPUTED','ASSUMED'} and c.confidence>0.5:raise ValueError('Impossible confidence/status: '+loc)
                if c.status=='USER_STATED' and c.value!=objective:raise ValueError('User-stated assertion not in request: '+loc)
            for name in ('objective','requested_output','primary_mode'):claim(getattr(proposal,name),name)
            if proposal.objective.value!=objective:raise ValueError('Objective changed')
            for name in ('secondary_modes','supporting_modes','entities','periods','frameworks','jurisdictions','assumptions','disputed_facts','hypotheses'):
                for i,c in enumerate(getattr(proposal,name)):claim(c,name+str(i))
            for name in ('classifications','context_candidates'):
                for key,c in getattr(proposal,name).items():claim(c,name+key)
            if proposal.bounded_owner:claim(proposal.bounded_owner,'bounded_owner')
            if proposal.interpreted_objective:claim(proposal.interpreted_objective,'interpreted_objective')
            modes=[proposal.primary_mode.value]+[c.value for c in proposal.secondary_modes+proposal.supporting_modes]
            if any(m not in {w.value for w in WorkMode} for m in modes) or len(modes)!=len(set(modes)):raise ValueError('Invalid/duplicated work mode')
            if proposal.bounded_owner and (len(modes)!=1 or proposal.primary_mode.value!='REPORTING'):raise ValueError('Bounded owner requires simple reporting')
            registered=execution_scopes(context)
            for c in proposal.entities:
                if c.value not in registered and c.status!='UNRESOLVED':raise ValueError('Unknown entity must remain unresolved Scope Candidate')
            for c in proposal.periods:period(c.value)
            for c in proposal.frameworks:
                if c.value not in FRAMEWORKS or c.status in {'INFERRED','ASSUMED','UNRESOLVED'}:raise ValueError('Unqualified/fabricated framework')
            for key,c in proposal.context_candidates.items():
                if key not in CONTEXT_ATTRIBUTES:raise ValueError('Invalid context candidate')
                if isinstance(c.value,dict):
                    if set(c.value)!={'scope_id','value'} or c.value['scope_id'] not in registered:raise ValueError('Unknown scoped context candidate')
                    value=c.value['value']
                else:value=c.value
                if key=='framework' and value not in FRAMEWORKS:raise ValueError('Fabricated framework')
            def owner(value):
                m=self.registry.get(value)
                if not m.get('production_available') or not m.get('execution_available'):raise ValueError('Unknown/NONPRODUCTION owner')
                for fw in proposal.frameworks:
                    if m.get('applicable_frameworks') and fw.value not in m['applicable_frameworks']:raise ValueError('Unsupported owner framework')
            if proposal.bounded_owner:owner(proposal.bounded_owner.value)
            for id,c in proposal.classifications.items():
                if id not in inventory.extractions or not isinstance(c.value,dict) or set(c.value)!={'family','certainty'}:raise ValueError('Classification invalid')
                if c.value['family'] not in SOURCE_FAMILIES or c.value['certainty'] not in {'classified','probable','ambiguous','unknown'}:raise ValueError('Unknown source family/certainty')
                if c.value['certainty']=='classified' and (c.confidence<0.9 or not c.evidence):raise ValueError('Classification overconfidence')
                if any(fields[e]['source_id']!=id for e in c.evidence):raise ValueError('Classification evidence wrong source')
            for mapping in proposal.column_mappings:
                if not isinstance(mapping,Claim):raise ValueError('Column mapping Claim required')
                claim(mapping,'column_mapping');v=mapping.value
                if not isinstance(v,dict) or set(v)!={'field','original','normalized'} or v['field'] not in fields:raise ValueError('Invalid column mapping')
                if fields[v['field']]['location'].get('column')!=v['original'] or not re.fullmatch('[a-z][a-z0-9_]{0,80}',v['normalized']):raise ValueError('Column mapping loses source')
            issue_ids=set()
            for issue in proposal.issues:
                if not isinstance(issue,Claim):raise ValueError('Issue Claim required')
                claim(issue,'issue');v=issue.value
                if not isinstance(v,dict) or set(v)-{'scope_id'}!={'id','owner','family','fact_ids','dependencies','required_fields'}:raise ValueError('Issue schema invalid')
                if not isinstance(v['id'],str) or not v['id'] or v['id'] in issue_ids:raise ValueError('Duplicate issue identity')
                issue_ids.add(v['id']);owner(v['owner'])
                if v.get('scope_id') and v['scope_id'] not in registered:raise ValueError('Unknown issue Scope Candidate')
                if v['family'] not in FACT_ADAPTERS or FACT_ADAPTERS[v['family']][0]!=v['owner']:raise ValueError('Family/owner mismatch')
                if any(not isinstance(v[k],list) or any(not isinstance(x,str) for x in v[k]) for k in ('fact_ids','dependencies','required_fields')):raise ValueError('Malformed issue lists')
                if len(set(v['fact_ids']))!=len(v['fact_ids']):raise ValueError('Duplicate issue facts')
                if any(not re.fullmatch('[a-z][a-z0-9_]{0,80}',key) for key in v['required_fields']):raise ValueError('Unsafe field label')
            ids=set();economic=set()
            for f in proposal.facts:
                if not isinstance(f,FactCandidate) or not isinstance(f.id,str) or not f.id or f.id in ids:raise ValueError('Duplicate/invalid fact identity')
                ids.add(f.id);claim(f.claim,'fact-'+f.id)
                if f.family not in FACT_ADAPTERS or (f.candidate_owner and FACT_ADAPTERS[f.family][0]!=f.candidate_owner):raise ValueError('Invalid fact owner/family')
                if f.candidate_owner:owner(f.candidate_owner)
                if not isinstance(f.attribute,str) or not re.fullmatch('[a-z][a-z0-9_]{0,80}',f.attribute):raise ValueError('Invalid fact attribute')
                if type(f.confirmation_required) is not bool:raise ValueError('Confirmation flag invalid')
                if not isinstance(f.conflicts,list) or any(not isinstance(x,str) or not x for x in f.conflicts):raise ValueError('Conflict identity invalid')
                if set(f.dimensions)-DIMENSIONS:raise ValueError('Unknown dimension')
                for k,v in f.dimensions.items():
                    if k=='period':period(v)
                    elif not isinstance(v,str) or not v or len(v)>120:raise ValueError('Dimension invalid')
                if 'comparator' in f.dimensions and f.dimensions['comparator'] not in COMPARATORS:raise ValueError('Comparator invalid')
                if len(registered)>1 and not f.dimensions.get('entity') and not f.dimensions.get('scope_id'):raise ValueError('Ambiguous Scope Candidate')
                scope_id=f.dimensions.get('scope_id',f.dimensions.get('entity',context.get('entity')))
                fact_scope=registered.get(scope_id)
                if f.dimensions.get('scope_id') and f.dimensions.get('entity') and f.dimensions['scope_id']!=f.dimensions['entity']:raise ValueError('Fact Scope identity differs')
                if not fact_scope:raise ValueError('Unknown fact execution scope')
                for key in ('entity','currency','jurisdiction'):
                    if key in f.dimensions and fact_scope.get(key) and f.dimensions[key]!=fact_scope[key]:raise ValueError('Execution dimension mismatch')
                if f.dimensions.get('comparator')=='actual' and context.get('period_start') and f.dimensions.get('period')!=[fact_scope['period_start'],fact_scope['reporting_period']]:raise ValueError('Current fact period mismatch')
                if 'framework' in f.dimensions and (f.dimensions['framework'] not in FRAMEWORKS or (fact_scope.get('framework') and f.dimensions['framework']!=fact_scope['framework'])):raise ValueError('Framework invalid or mismatched')
                if 'currency' in f.dimensions and not re.fullmatch('[A-Z]{3}',f.dimensions['currency']):raise ValueError('Currency invalid')
                if 'amount_currency' in f.dimensions:
                    if not re.fullmatch('[A-Z]{3}',f.dimensions['amount_currency']) or any(inventory.extractions[fields[e]['source_id']].source['metadata'].get('amount_currency')!=f.dimensions['amount_currency'] for e in f.claim.evidence):raise ValueError('Foreign amount denomination lacks matching source evidence')
                if len(registered)>1:
                    for evidence in f.claim.evidence:
                        metadata=inventory.extractions[fields[evidence]['source_id']].source['metadata']
                        if metadata.get('scope_id',metadata.get('entity'))!=scope_id:raise ValueError('Fact source Scope differs or ambiguous')
                        for key in ('framework','jurisdiction'):
                            if metadata.get(key) is not None and metadata[key]!=fact_scope[key]:raise ValueError('Fact source metadata contamination')
                if f.transformation not in {'identity','decimal','iso_date','boolean'}:raise ValueError('Unsafe transformation')
                if f.claim.status in {'EXTRACTED','OBSERVED','CALCULATED'}:
                    if len(f.claim.evidence)!=1 or transform(fields[f.claim.evidence[0]]['value'],f.transformation)!=f.claim.value:raise ValueError('Extracted fact differs from source/transformation')
                    if f.claim.status=='CALCULATED' and f.transformation=='identity':raise ValueError('Calculation method absent')
                    if f.transformation=='decimal' and (not f.dimensions.get('unit') or (f.dimensions['unit']=='currency' and not f.dimensions.get('currency'))):raise ValueError('Amount currency/unit required')
                if f.claim.status in {'INFERRED','ASSUMED','DISPUTED','UNRESOLVED'} and not f.confirmation_required:raise ValueError('Hidden assumption/judgment')
                if f.claim.status=='ASSUMED' and not any(c.value==f.claim.value for c in proposal.assumptions):raise ValueError('Undeclared assumption')
                # Alias-proof identity within one semantic metric/record. Different
                # sources of the same metric are conflicts, not silently deduped.
                identity=(tuple(f.claim.evidence),f.attribute,canonical(f.dimensions))
                if f.transformation=='decimal':identity=('numeric-source',tuple(f.claim.evidence))
                if identity in economic or (f.economic_id and ('economic',scope_id,f.economic_id) in economic):raise ValueError('Duplicate economic identity')
                economic.add(identity)
                if f.economic_id:economic.add(('economic',scope_id,f.economic_id))
            for issue in proposal.issues:
                v=issue.value
                if any(id not in ids for id in v['fact_ids']) or any(d not in issue_ids for d in v['dependencies']):raise ValueError('Unknown fact/dependency')
                selected=[f for f in proposal.facts if f.id in v['fact_ids']]
                if not selected or any(f.family!=v['family'] for f in selected):raise ValueError('Issue lacks matching source facts')
                scopes={f.dimensions.get('scope_id',f.dimensions.get('entity',context['entity'])) for f in selected}
                if len(scopes)>1 and not (v.get('scope_id') and registered[v['scope_id']]['scope_type'] in ('GROUP','SUBGROUP')):raise ValueError('Mixed-entity issue source population')
                if v.get('scope_id') and len(scopes)==1 and scopes!={v['scope_id']}:raise ValueError('Issue Scope differs from facts')
            for h in proposal.hypotheses:
                v=h.value
                if not isinstance(v,dict) or set(v)!={'id','description','tests'} or not isinstance(v['description'],str) or not isinstance(v['id'],str) or not isinstance(v['tests'],list) or not v['tests']:raise ValueError('Hypothesis schema invalid')
                for test in v['tests']:
                    if not isinstance(test,dict) or set(test)!={'left_owner','left_path','right_owner','right_path','factor','operator'}:raise ValueError('Hypothesis test schema invalid')
                    for side in ('left','right'):
                        owner(test[side+'_owner'])
                        if not isinstance(test[side+'_path'],list) or not test[side+'_path'] or any(not isinstance(k,str) or len(k)>120 for k in test[side+'_path']):raise ValueError('Hypothesis metric path invalid')
                    if test['operator'] not in {'magnitude_above','magnitude_below','equal'} or type(test['factor']) not in (int,float) or not 0<=test['factor']<=1:raise ValueError('Hypothesis method invalid')
            # Standalone declarations cannot disappear during candidate
            # resolution. Link them to governed fact states or fail closed.
            for declaration in proposal.assumptions:
                if not any(f.claim.status=='ASSUMED' and f.claim.value==declaration.value for f in proposal.facts):raise ValueError('Unbound assumption declaration')
            for declaration in proposal.disputed_facts:
                if not any(f.claim.status in ('DISPUTED','UNRESOLVED') and f.claim.value==declaration.value for f in proposal.facts):raise ValueError('Unbound disputed fact declaration')
            referenced={id for i in proposal.issues for id in i.value['fact_ids']}
            if any(f.candidate_owner and f.id not in referenced for f in proposal.facts):raise ValueError('Owner-supported fact omitted from issue planning')
            # Validate DAG independently of runtime.
            edges={i.value['id']:i.value['dependencies'] for i in proposal.issues};active=set();done=set()
            def walk(id):
                if id in active:raise ValueError('Proposal dependency cycle')
                if id in done:return
                active.add(id)
                for dep in edges[id]:walk(dep)
                active.remove(id);done.add(id)
            for id in edges:walk(id)
            if proposal.bounded_owner:
                roots=[i.value['id'] for i in proposal.issues if i.value['owner']==proposal.bounded_owner.value]
                needed=set()
                def require(id):
                    if id in needed:return
                    needed.add(id)
                    for dep in edges[id]:require(dep)
                for id in roots:require(id)
                if not roots or needed!=set(edges):raise ValueError('Simple inquiry over-routing')
            selected={i.value['owner'] for i in proposal.issues}
            if proposal.primary_mode.value=='DIAGNOSTIC_ANALYTICS' and 'management-accounting-analytics' not in selected:raise ValueError('Diagnostic owner omitted')
            for missing in proposal.missing_facts:
                if not isinstance(missing,Claim):raise ValueError('Missing fact Claim required')
                claim(missing,'missing');v=missing.value
                if not isinstance(v,dict) or set(v)-{'scope_id'}!={'attribute','owner','kind'} or v['kind'] not in {'blocking','confirmation','nonblocking'}:raise ValueError('Missing fact schema invalid')
                if not isinstance(v['attribute'],str) or not re.fullmatch('[a-z][a-z0-9_]{0,80}',v['attribute']):raise ValueError('Unsafe missing field label')
                if v.get('scope_id') and v['scope_id'] not in registered:raise ValueError('Unknown question Scope')
                if v['owner']:owner(v['owner'])
            return Validation(True,[],copy.deepcopy(proposal))
        except (ValueError,TypeError,KeyError,AttributeError,InvalidOperation,OverflowError) as exc:
            # Do not echo model content or source text into questions/errors.
            fail('INVALID_PROPOSAL','validation')
            return Validation(False,errors)
