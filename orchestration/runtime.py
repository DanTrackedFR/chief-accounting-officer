"""Governed Case runtime. Accounting authority stays behind assess_case.

No approval is generated here. Reviewed consumer workpapers must already bind
actual upstream results; execution verifies them against this graph's fresh owner
results. Future input preparation adapters must preserve that review boundary.
"""
import copy
import re
import hashlib
import json
from dataclasses import asdict, dataclass, field
from decimal import Decimal
from datetime import date
from .registry import Registry, production
from .intent import Intent, interpret
from .planning import DeterministicPlanner, Graph, Node, Issue, FACT_ADAPTERS
from interfaces.public_output import public_record
from .scopes import execution_scopes, scoped_context, execution_identity, scope_registry


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str, separators=(',', ':')).encode()).hexdigest()


def currency(c):
    value = c.get('currency', c.get('functional_currency'))
    if isinstance(value, dict): return value.get('functional')
    if value: return value
    value = c.get('governance_method', {}).get('currency')
    return value


def currency_from_node(n):
    return n.functional_currency or n.presentation_currency or ''


def dimensions(c):
    return (c.get('entity'), c.get('framework'), c.get('jurisdiction'), c.get('period_start'),
            c.get('reporting_period'), currency(c))


def at(value, path):
    for k in path:
        if isinstance(value, list):
            if type(k) is int:
                if not 0 <= k < len(value): raise ValueError('Metric index absent')
                value=value[k]; continue
            matches = [r for r in value if isinstance(r, dict) and r.get('id') == k]
            if len(matches) != 1: raise ValueError('Metric row absent or duplicated')
            value = matches[0]
        else: value = value[k]
    return value


def inputs_for_synthesis(result):
    return [v for v in result.get('calculations',{}).values() if isinstance(v,dict) and 'actual_eligible_total' in v]


def number(value):
    if isinstance(value, bool): raise ValueError('Boolean is not an accounting amount')
    n = Decimal(str(value))
    if not n.is_finite(): raise ValueError('Nonfinite accounting amount')
    return n


@dataclass
class Case:
    id: str
    objective: str
    requested_output: str = 'Accounting review workpaper'
    title: str = 'CAO accounting case'
    status: str = 'OPEN'
    opened_at: object = None
    closed_at: object = None
    entities: list = field(default_factory=list)
    periods: list = field(default_factory=list)
    frameworks: list = field(default_factory=list)
    jurisdictions: list = field(default_factory=list)
    industries: list = field(default_factory=list)
    materiality: object = None
    facts: dict = field(default_factory=lambda: dict(established=[], assumed=[], disputed=[]))
    open_questions: list = field(default_factory=list)
    accounting_issues: list = field(default_factory=list)
    workplan_nodes: list = field(default_factory=list)
    skills_invoked: list = field(default_factory=list)
    knowledge_refs: list = field(default_factory=list)
    evidence_refs: list = field(default_factory=list)
    judgments: list = field(default_factory=list)
    alternatives: list = field(default_factory=list)
    conclusions: list = field(default_factory=list)
    challenge_results: list = field(default_factory=list)
    artifacts: list = field(default_factory=list)
    decisions: list = field(default_factory=list)
    memory_candidates: list = field(default_factory=list)
    supersedes: list = field(default_factory=list)
    superseded_by: list = field(default_factory=list)
    transitions: list = field(default_factory=lambda: ['OPEN'])
    outcome: str = 'blocked'
    execution_ledger: list = field(default_factory=list)
    handoff_ledger: list = field(default_factory=list)
    economic_ledger: list = field(default_factory=list)
    observer_ran: bool = False
    journal_mapping_valid: bool = False
    journal_ownership_ledger: list = field(default_factory=list)
    work_modes: dict = field(default_factory=dict)
    diagnostics: list = field(default_factory=list)
    balance_diagnostics: dict = field(default_factory=dict)
    close_observations: list = field(default_factory=list)
    accounting_questions: list = field(default_factory=list)
    scope_registry: list = field(default_factory=list)
    owner_results: list = field(default_factory=list)
    reviewed_input_packs: list = field(default_factory=list)
    group_consumer: dict = field(default_factory=dict)

    scope_id: str = ''
    period_id: str = ''
    case_type: str = ''
    cycle: str = ''
    parent_case_id: str | None = None
    child_case_ids: list = field(default_factory=list)
    node_refs: list = field(default_factory=list)
    result_version_refs: list = field(default_factory=list)
    governance_history: list = field(default_factory=list)
    rework_state: dict = field(default_factory=dict)
    provenance: list = field(default_factory=list)

    def transition(self, target):
        lifecycle = ['OPEN', 'SCOPED', 'IN_PROGRESS', 'CHALLENGE', 'CONCLUDED', 'DOCUMENTED', 'CLOSED']
        if lifecycle.index(target) != lifecycle.index(self.status)+1:
            raise ValueError('Invalid Case transition')
        if target == 'CONCLUDED' and not self.challenge_results:
            raise ValueError('Distinct challenge required')
        if target == 'CLOSED' and (not self.observer_ran or not self.artifacts):
            raise ValueError('Documentation and Context Observer required')
        # A blocked/partial conclusion is a documented unresolved position, never
        # an assertion that material open work is complete.
        if target == 'CLOSED' and self.outcome != 'complete':
            raise ValueError('Unresolved Case remains DOCUMENTED; explicit blocked delivery is separate')
        self.status = target; self.transitions.append(target)
    def record(self):
        value=asdict(self)
        if hasattr(self,'governance'):
            g=self.governance
            value['governance']=dict(periods=g.periods.record(),cases=g.cases.record(),versions=g.versions.record(),dependencies=[dict(asdict(e),id=k) for k,e in sorted(g.edges.items())],receipts=g.receipts,rework=g.rework_history)
        return value


def company_context(records, scope):
    """Temporal nonmutating current view, rejecting conflicting scoped truth."""
    current = {}; conflicts = []
    if not isinstance(records, list): raise ValueError('Company Context must be governed records')
    for r in records:
        if not isinstance(r, dict): raise ValueError('Malformed context record')
        if r.get('status') not in ('CONFIRMED', 'DOCUMENTED', 'APPROVED'): continue
        s = r.get('scope', {})
        if s.get('entities') and scope.get('entity') not in s['entities']: continue
        if s.get('jurisdictions') and scope.get('jurisdiction') not in s['jurisdictions']: continue
        if s.get('periods') and scope.get('reporting_period') not in s['periods']: continue
        when = scope.get('period_start')
        if r.get('effective_from') and (not when or r['effective_from'] > when): continue
        if r.get('effective_to') and (not when or r['effective_to'] < scope.get('reporting_period', when)): continue
        key = r['attribute']
        if key in current and current[key] != r['value']:
            conflicts.append(key)
        else: current[key] = copy.deepcopy(r['value'])
    for key in conflicts: current.pop(key, None)
    return current, sorted(set(conflicts))


class CAO:
    def __init__(self, planner=None, registry=None):
        self.planner = planner or DeterministicPlanner(); self.registry = registry or Registry()

    def run(self, request):
        """Accept objective and supplied source workpapers/context; return internal Case.

        Normal governed errors become visible blocked nodes/open items. This is
        not a general prose-to-source-document extraction service.
        """
        if not isinstance(request, dict): request = {}
        objective = request.get('objective')
        c = Case(str(request.get('case_id', 'case')), objective if isinstance(objective, str) else '')
        graph = Graph(); c.graph = graph
        try: self._run(c, graph, copy.deepcopy(request))
        except (ValueError, KeyError, TypeError, AttributeError, ArithmeticError) as exc:
            c.open_questions.append(dict(kind='blocking', question=str(exc)))
            c.outcome = 'blocked'
            # Preserve completed work/evidence on malformed planning/inputs.
            c.workplan_nodes = c.graph.record()
        return c

    def _run(self, c, graph, request):
        if not c.objective.strip(): raise ValueError('User objective required')
        if 'governed_plan' in request:
            from .governed_plan import run
            return run(c,request)
        scope = request.get('scope', {})
        context, conflicts = company_context(request.get('company_context', []), scope)
        for k, v in scope.items():
            if k in context and context[k] != v: conflicts.append(k)
            else: context[k] = v
        for k in set(conflicts):
            context.pop(k, None)
            c.facts['disputed'].append(dict(attribute=k, reason='Supplied facts conflict with governed Company Context'))
        for k in ('entity', 'framework', 'jurisdiction', 'period_start', 'reporting_period', 'currency'):
            if not context.get(k): c.open_questions.append(dict(kind='blocking', question='Resolve '+k))
        if c.open_questions: raise ValueError('Resolve missing or disputed execution dimensions')
        scopes=execution_scopes(context)
        c.entities=[context['entity']]+sorted(e for e in scopes if e!=context['entity']); c.periods=[context['period_start'],context['reporting_period']]
        c.reviewed_input_packs=copy.deepcopy(request.get('reviewed_scope_packs',[]))
        c.scope_registry=scope_registry(context).record()
        c.frameworks=sorted({s['framework'] for s in scopes.values()}); c.jurisdictions=sorted({s['jurisdiction'] for s in scopes.values()})
        c.industries = [context['industry']] if context.get('industry') else []
        c.materiality = context.get('materiality')
        c.facts['established'] = [dict(attribute=k,value=v) for k,v in context.items()]
        c.facts['assumed'] = copy.deepcopy(request.get('assumptions', []))
        facts = request.get('facts', {})
        if not isinstance(facts, dict): raise ValueError('Source facts must be an object')
        proposal=self.planner.interpret(c.objective,facts,context,self.registry) if hasattr(self.planner,'interpret') else interpret(c.objective)
        if not isinstance(proposal,Intent):raise ValueError('Planner intent must be governed structured Intent')
        c.work_modes=proposal.record()
        issues = self.planner.identify(c.objective, facts, context, self.registry)
        if not isinstance(issues, list) or any(not isinstance(i, Issue) for i in issues):
            raise ValueError('Planner must return bounded structured issues')
        if not issues: raise ValueError('No supported issue decomposition; supply accounting facts or a scoped planner')
        for family in set(facts)&set(FACT_ADAPTERS):
            if not isinstance(facts[family], (dict,list)):
                c.open_questions.append(dict(kind='blocking', question='Malformed supplied fact family: '+family))
        unknown = set(facts)-set(FACT_ADAPTERS)-{'task_attributes'}
        for family in sorted(unknown): c.open_questions.append(dict(kind='blocking', question='Unsupported fact family: '+family))
        from .execution import OwnerInputs, populations
        inputs=OwnerInputs(context)
        for family,source in populations(facts):
            if family in FACT_ADAPTERS and self.registry.get(FACT_ADAPTERS[family][0]).get('production_available'): inputs.add(FACT_ADAPTERS[family][0],copy.deepcopy(source))
        queue=list(inputs.values())
        inspected=set()
        for source in queue:
            for imp in source.get('imports',[]):
                key=inputs.add(imp['package'],copy.deepcopy(imp['case']))
                if key not in inspected: inspected.add(key);queue.append(inputs[key])
        for i in issues:
            if not isinstance(i.id, str) or not i.id or not isinstance(i.owner, str): raise ValueError('Malformed issue identity')
            if type(i.required) is not bool or (i.material is not None and type(i.material) is not bool): raise ValueError('Invalid dependency materiality')
            candidates=[key for key in inputs if inputs.packages[key]==i.owner and (i.scope_id is None or inputs[key].get('scope_id',inputs[key].get('entity'))==i.scope_id) and (getattr(i,'period_id',None) is None or inputs[key].get('period_id')==getattr(i,'period_id',None))]
            if len(candidates)>1:raise ValueError('Issue must identify exact Scope/Period for repeated owner')
            node_context=scoped_context(context,inputs[candidates[0]]) if candidates else scoped_context(context,context)
            key=execution_identity(i.owner,node_context)
            graph.add(Node(key,i.capability,i.owner,i.reason,node_context['entity'],node_context['framework'],[node_context['period_start'],node_context['reporting_period']],
                logical_id=i.id,scope_id=node_context['scope_id'],scope_type=node_context['scope_type'],jurisdiction=node_context['jurisdiction'],period_id=node_context.get('period_id',''),
                functional_currency=node_context['functional_currency'],presentation_currency=node_context['presentation_currency'],
                prerequisites=self.registry.get(i.owner).get('context_requirements',{}).get('required',[]),
                dependencies=list(i.dependencies),source_inputs=i.source_inputs,
                owner_result_dependencies=list(i.dependencies),required=i.required,material=i.material,condition=i.condition))
        for n in graph.nodes.values():
            n.dependencies=[graph.nodes.resolve(d) for d in n.dependencies]
        # Integrator bindings infer reporting/other dependencies as actual edges.
        bindings = request.get('handoffs', [])
        if proposal.bounded_owner:
            bindings=[b for b in bindings if b.get('producer') in graph.nodes and b.get('consumer') in graph.nodes]
            request['challenge_assertions']=[a for a in request.get('challenge_assertions',[]) if a.get('node') in graph.nodes]
            request.pop('journal_account_mapping',None)
        if not isinstance(bindings, list): raise ValueError('Handoffs must be a list')
        bindings=[b for b in bindings if b.get('consumer') in graph.nodes]
        request['challenge_assertions']=[a for a in request.get('challenge_assertions',[]) if a.get('node') in graph.nodes]
        for b in bindings:
            b['consumer']=graph.nodes.resolve(b['consumer']);b['producer']=graph.nodes.resolve(b['producer'])
            if b['consumer'] not in graph.nodes or b['producer'] not in graph.nodes: raise ValueError('Handoff owner node absent')
            n=graph.nodes[b['consumer']]
            if b['producer'] not in n.dependencies: n.dependencies.append(b['producer'])
        for n in graph.nodes.values():
            for receipt in inputs.get(n.id,{}).get('qualified_owner_results',[]):
                upstream=graph.nodes.resolve(receipt.get('producer'))
                if upstream not in graph.nodes:raise ValueError('Unknown specialist receipt producer')
                if upstream not in n.dependencies:n.dependencies.append(upstream)
        by_owner={owner:[n for n in graph.nodes.values() if n.selected_skill==owner] for owner in {n.selected_skill for n in graph.nodes.values()}}
        # Required combined-conclusion bridges are inferred, never made optional
        # by omission of caller-supplied handoffs. Native owner imports already
        # govern the actual upstream cost links inside Inventory/Analytics/etc.
        required_bridges=[('inventory-cost','financial-statements','cogs'),
            ('inventory-cost','balance-sheet-reconciliations','inventory_balance'),
            ('revenue-recognition','financial-statements','revenue'),
            ('accounts-receivable','financial-statements','ar_balance'),
            ('financial-instruments-ecl','financial-statements','allowance'),
            ('revenue-recognition','financial-statements','contract_balance'),
            ('foreign-currency','financial-statements','monetary_fx'),
            ('accounts-receivable','balance-sheet-reconciliations','ar_balance'),
            ('financial-instruments-ecl','balance-sheet-reconciliations','allowance'),
            ('revenue-recognition','balance-sheet-reconciliations','contract_balance')]
        for upstream,semantics in [('debt-financing',['debt_base','debt_current','debt_noncurrent','interest_expense']),('derivatives-hedge-accounting',['derivative_balance','hedge_reserve','hedge_pnl','hedge_oci']),('cash-flow-reporting',['cash_balance','financing_cash','operating_cash'])]:
            for semantic in semantics:required_bridges.append((upstream,'financial-statements',semantic))
        if 'debt-financing' in by_owner and 'foreign-currency' in by_owner:required_bridges.append(('foreign-currency','financial-statements','monetary_fx'))
        for upstream,downstream,semantic in required_bridges:
            if upstream not in by_owner or downstream not in by_owner:continue
            if semantic=='contract_balance' and 'accounts-receivable' not in by_owner:continue
            if semantic=='monetary_fx' and not {'accounts-receivable','debt-financing'} & set(by_owner):continue
            producers=by_owner[upstream];consumers=by_owner[downstream]
            if len(producers)!=1 or len(consumers)!=1:raise ValueError('Repeated-owner reporting requires explicit scoped consumer contracts')
            producer=producers[0];consumer=consumers[0]
            if producer.id not in consumer.dependencies:consumer.dependencies.append(producer.id)
            matched=[b for b in bindings if b.get('producer')==producer.id and b.get('consumer')==consumer.id and b.get('semantic')==semantic]
            if len(matched)!=1:
                consumer.status='blocked';consumer.open_items.append('Missing or duplicated qualified '+semantic+' owner bridge')
        for b in bindings:
            for component in b.get('components',[]):
                dependency=graph.nodes.resolve(component.get('producer'));component['producer']=dependency
                if dependency not in graph.nodes:raise ValueError('Unknown composed owner dependency')
                if dependency not in graph.nodes[b['consumer']].dependencies:graph.nodes[b['consumer']].dependencies.append(dependency)
        graph.validate(); c.accounting_issues=[asdict(i) for i in issues]
        from .runtime_governance import attach,publish,finish
        session=attach(c,graph,context,inputs,request)
        c.transition('SCOPED'); c.transition('IN_PROGRESS')
        consumed=set(); owned={}; entries=set()
        while any(n.status == 'pending' for n in graph.nodes.values()):
            ready = graph.ready()
            if not ready:
                for n in graph.nodes.values():
                    if n.status=='pending': n.status='blocked'; n.open_items.append('Required owner dependency unresolved')
                break
            batch=[n.id for n in ready]
            for n in ready:
                n.iterations += 1
                if n.condition is not None:
                    if not isinstance(n.condition, dict) or set(n.condition) != {'fact','equals'}: raise ValueError('Malformed conditional node')
                    if facts.get(n.condition['fact']) != n.condition['equals']:
                        n.status='not_applicable'; continue
                meta=self.registry.get(n.selected_skill)
                if not meta['production_available'] or not meta['execution_available']:
                    n.status='blocked'; n.open_items.append('Accounting owner unavailable for production: '+n.selected_skill); continue
                source=inputs.get(n.id)
                if not isinstance(source, dict):
                    n.status='blocked'; n.open_items.append('Missing reviewed source workpaper for '+n.issue); continue
                session.periods.authorize_execution(n.period_id,n.case_id,n.id)
                node_context=scoped_context(context,source)
                expected=(n.entity,n.framework,node_context['jurisdiction'],*n.period,node_context['currency'])
                if dimensions(source) != expected:
                    n.status='blocked'; n.open_items.append('Owner entity/framework/jurisdiction/period/currency mismatch'); continue
                if meta['applicable_frameworks'] and n.framework not in meta['applicable_frameworks']:
                    n.status='blocked'; n.open_items.append('Framework outside owner contract'); continue
                try:
                    from .temporal_inputs import validate_native_sources
                    validate_native_sources(context,n,source)
                    repeated=sum(x.selected_skill==n.selected_skill for x in graph.nodes.values())>1
                    if repeated:
                        population=source.get('source_population');manifest=source.get('qualified_scope_sources')
                        if not isinstance(population,list) or not population or not isinstance(manifest,list) or not manifest:raise ValueError('Repeated owner requires exact scoped source qualification')
                        if len(set(population))!=len(population) or {r['source_id'] for r in manifest}!=set(population) or len(manifest)!=len(population):raise ValueError('Scoped owner source population differs')
                        for row in manifest:
                            source_meta=row['metadata']
                            if source_meta.get('scope_id',source_meta.get('entity'))!=n.scope_id or source_meta.get('entity')!=n.scope_id:raise ValueError('Repeated owner source Scope contamination')
                            if (source_meta.get('currency'),source_meta.get('framework'),source_meta.get('jurisdiction'),source_meta.get('period'))!=(node_context['currency'],n.framework,n.jurisdiction,n.period) or not row.get('fingerprint'):raise ValueError('Repeated owner source dimensional contamination')
                    if context.get('period_registry') and n.dependencies:
                        exact_receipts=[session.receipt(k) for k,e in sorted(session.edges.items()) if e.consumer_node==n.id]
                        if source.get('versioned_dependency_receipts')!=exact_receipts:raise ValueError('Explicit temporal native consumer requires separately reviewed exact-version receipts')
                    from .period_selection import validate_activity
                    validate_activity(source)
                    from .result_bindings import validate_receipts
                    validate_receipts(n,graph,inputs,c)
                    for imp in source.get('imports', []):
                        matches=[node for node in graph.nodes.values() if node.selected_skill == imp['package'] and node.scope_id==imp['case'].get('scope_id',imp['case'].get('entity')) and (not imp['case'].get('period_id') or node.period_id==imp['case']['period_id'])]
                        producer=matches[0] if len(matches)==1 else None
                        if not producer or producer.status!='complete' or digest(imp['result'])!=digest(producer.result):
                            raise ValueError('Imported owner result stale, incomplete or contradictory')
                    for b in [b for b in bindings if b['consumer']==n.id]:
                        self._handoff(c, graph, inputs, b, consumed)
                    r=production.assess_case(n.selected_skill,source)
                    if not isinstance(r,dict) or r.get('skill_id')!=meta['id'] or r.get('status') not in ('complete','partial','blocked','not_applicable'):
                        raise ValueError('Malformed owner result envelope')
                    # Public curation is mandatory even before internal synthesis.
                    production.to_public(r, 'answer_context')
                    if r.get('status')=='complete' and r.get('case_fingerprint')!=production.case_fingerprint(source):
                        raise ValueError('Stale exact-case certification')
                    if r.get('status')=='complete' and (r.get('entities')!=[n.entity] or r.get('framework')!=n.framework or r.get('jurisdiction')!=node_context['jurisdiction'] or r.get('periods')!=n.period):
                        raise ValueError('Owner result envelope dimensions differ')
                    n.result=r; n.status=r['status']; n.open_items=list(r.get('open_items',[])); n.evidence=copy.deepcopy(r.get('evidence',[]))
                    n.execution_receipt=self._result_receipt(n,source)
                    if n.status=='complete':publish(session,n,source)
                    matches=[p for p in c.reviewed_input_packs if p['node']==n.id]
                    if matches:n.execution_receipt['reviewed_input_pack_fingerprint']=matches[0]['pack_fingerprint']
                    c.skills_invoked.append(n.selected_skill)
                    c.execution_ledger.append(dict(node=n.id,batch=batch,status=n.status,case_fingerprint=r.get('case_fingerprint')))
                    if n.status == 'complete':
                        from .scoped_journals import qualify_journal
                        posting=source.get('posting_scope_id',n.scope_id)
                        layer=source.get('journal_layer',n.scope_type)
                        qualify_journal(node_context,n.scope_id,posting,layer)
                        self._economics(c,n,source,owned,entries)
                    c.evidence_refs.extend(n.evidence); c.judgments.extend(r.get('judgments',[]))
                    c.knowledge_refs.extend(copy.deepcopy(r.get('knowledge_documents',[])))
                    c.facts['assumed'].extend(r.get('assumptions',[]))
                except (ValueError,KeyError,TypeError,AttributeError,ArithmeticError) as exc:
                    n.status='blocked'; n.result=None; n.open_items.append(str(exc))
        self._diagnostic_followups(c,graph,inputs,context)
        # Optional intake extension returns validated material questions before
        # challenge/synthesis/closure. Accounting work may proceed independently;
        # unresolved intake evidence prevents a clean Case close.
        if hasattr(self.planner, 'material_questions'):
            questions=self.planner.material_questions()
            if not isinstance(questions,list) or any(not isinstance(q,dict) or q.get('kind') not in ('blocking','confirmation') or not isinstance(q.get('question'),str) for q in questions):
                raise ValueError('Invalid material intake questions')
            public_record(dict(open_items=[q['question'] for q in questions]),route='answer_context')
            c.open_questions.extend(copy.deepcopy(questions))
        c.transition('CHALLENGE')
        self._challenge(c,graph,inputs,request,context)
        analytics=next((n for n in graph.nodes.values() if n.selected_skill=='management-accounting-analytics'),None)
        if analytics and analytics.status not in ('complete','partial'):
            c.diagnostics=[];c.balance_diagnostics={}
        c.owner_results=[n.execution_receipt for n in graph.nodes.values() if n.status=='complete']
        if request.get('group_consumer') is not None:
            from .scoped_receipts import consume_group
            c.group_consumer=consume_group(request['group_consumer'],graph,inputs,context,c)
            from .runtime_governance import adopt
            target=graph.nodes[c.group_consumer['node']]
            target.result.update(status='complete',case_fingerprint=digest(request['group_consumer']))
            adopt(session,target,request['group_consumer']);publish(session,target,request['group_consumer'])
        from .runtime_governance import reconcile
        reconcile(session)
        c.workplan_nodes=graph.record()
        unresolved=[n for n in graph.nodes.values() if n.status in ('blocked','partial')]
        critical=[n for n in unresolved if n.required or n.material is not False]
        if c.open_questions: critical += [None]
        complete=any(n.status=='complete' for n in graph.nodes.values())
        c.outcome='partial' if critical and complete else 'blocked' if critical else 'complete'
        c.conclusions=[self._synthesis(c,graph,context)]
        mapping=request.get('journal_account_mapping',{}) if c.journal_mapping_valid else {}
        for entry in c.conclusions[0]['journals']:
            for line in entry['lines']:line['account']=mapping.get(line['account'],line['account'])
        c.transition('CONCLUDED')
        self._observe(c,context,request)
        c.artifacts=[dict(id=c.id+'-'+kind,type=kind,status='DRAFT',version=1,source_case=c.id,
            entities=c.entities,periods=c.periods,frameworks=c.frameworks) for kind in (
            'case-record','workplan-graph','issue-register','skill-execution-ledger','handoff-ledger',
            'reconciliation-summary','journal-pack','challenge-report','cao-conclusion','public-answer','memory-candidates')]
        c.transition('DOCUMENTED')
        # Verify the actual public adapter before allowing a clean close.
        self.public(c)
        if c.outcome == 'complete': c.transition('CLOSED')
        finish(c)

    def _diagnostic_followups(self,c,g,inputs,context):
        analytics=next((n for n in g.nodes.values() if n.selected_skill=='management-accounting-analytics' and n.status in ('complete','partial')),None)
        if not analytics:return
        diagnostic=analytics.result['calculations'].get('diagnostic')
        balances=analytics.result['calculations'].get('balance_diagnostics')
        if not diagnostic and not balances:
            if c.work_modes.get('primary')=='DIAGNOSTIC_ANALYTICS' or 'DIAGNOSTIC_ANALYTICS' in c.work_modes.get('secondary',[]):c.open_questions.append(dict(kind='blocking',question='Supply reviewed diagnostic periods, comparators and driver evidence to explain the movement'))
            return
        approval=inputs[analytics.id].get('reviewer_signoff',{})
        if approval.get('approved') is not True or approval.get('case_fingerprint')!=production.case_fingerprint(inputs[analytics.id]):return
        if diagnostic and diagnostic['bridge']['metric']=='gross_profit' and diagnostic['bridge']['presentation_basis']!=context.get('gross_margin_basis'):
            g.invalidate(analytics.id,'Diagnostic margin basis differs from approved company presentation policy');return
        if diagnostic:c.diagnostics=[copy.deepcopy(diagnostic)]
        if balances:c.balance_diagnostics=copy.deepcopy(balances)
        questions=list(diagnostic['accounting_questions']) if diagnostic else []
        for i,q in enumerate(balances.get('accounting_questions',[]) if balances else []):
            questions.append(dict(q,id='balance-'+str(i),reason='Material receivable ageing requires governed accounting review'))
        for question in questions:
            q=copy.deepcopy(question);owner=q['target_owner'];meta=self.registry.get(owner)
            existing=[n for n in g.nodes.values() if n.selected_skill==owner and n.issue!='diagnostic accounting follow-up']
            ctx=scoped_context(context,inputs[existing[0].id]) if len(existing)==1 else scoped_context(context,context)
            key=execution_identity(owner,ctx)+':recheck:'+digest(q['id'])
            node=Node(key,'diagnostic accounting follow-up',owner,q['reason'],ctx['entity'],ctx['framework'],c.periods,
                logical_id='diagnostic-'+q['id'],scope_id=ctx['scope_id'],scope_type=ctx['scope_type'],jurisdiction=ctx['jurisdiction'],functional_currency=ctx['functional_currency'],presentation_currency=ctx['presentation_currency'],
                dependencies=[analytics.id]+[n.id for n in existing],source_inputs=q['source_evidence'])
            g.add(node);g.validate();node.iterations=1
            source=inputs.get(existing[0].id) if len(existing)==1 else None
            inputs[node.id]=source
            try:
                if analytics.status!='complete':raise ValueError('Material diagnostic evidence unresolved before accounting follow-up')
                if not meta['production_available'] or not meta['execution_available']:raise ValueError('Accounting owner unavailable for diagnostic determination')
                if not existing or existing[0].status!='complete':raise ValueError('Accounting question requires current completed owner work')
                result=production.assess_case(owner,source);production.to_public(result,'answer_context')
                if result['status']!='complete' or digest(result)!=digest(existing[0].result):raise ValueError('Accounting owner recheck unresolved or changed; rework required')
                if number(at(result['calculations'],q['result_path']))!=number(q['amount']):raise ValueError('Analytical finding differs from accounting owner')
                from .runtime_governance import adopt,publish
                adopt(c.governance,node,source)
                node.status='complete';node.result=result;node.execution_receipt=self._result_receipt(node,source);publish(c.governance,node,source);q['status']='OWNER_RECHECK_SUPPORTED'
                q['accounting_conclusion']=result['conclusion']
                if owner=='inventory-cost' and q['result_path']==['manufacturing_expense']:
                    expense=sum((number(line['amount']) for journal in result.get('journal_entry_implications',[]) for line in journal if line['side']=='Dr' and line['account']=='Unallocated overhead expense'),Decimal(0))
                    if expense==number(q['amount']):q['accounting_disposition']='unallocated manufacturing expense'
            except (ValueError,KeyError,TypeError,ArithmeticError) as exc:
                node.status='blocked';node.open_items=[str(exc)];q['status']='UNRESOLVED'
            c.accounting_questions.append(q)
            c.execution_ledger.append(dict(node=node.id,batch=[node.id],status=node.status,action='diagnostic owner recheck',reuses=[n.id for n in existing]))

    def execute_versioned_owner(self, node, source, receipts):
        """Existing native production boundary for temporal/versioned execution.

        Accounting consumer imports remain separately reviewed native contracts;
        an orchestration receipt cannot manufacture a native accounting approval.
        """
        meta=self.registry.get(node.selected_skill)
        if not meta.get('production_available') or not meta.get('execution_available'):
            raise ValueError('Unavailable accounting owner')
        if dimensions(source)!=(node.scope_id,node.framework,node.jurisdiction,*node.period,currency_from_node(node)):
            raise ValueError('Versioned owner Scope/Period dimensions differ')
        if source.get('period_id')!=node.period_id:raise ValueError('Versioned owner governed Period differs')
        result=production.assess_case(node.selected_skill,source)
        production.to_public(result,'answer_context')
        if result.get('status')!='complete' or result.get('case_fingerprint')!=production.case_fingerprint(source):
            raise ValueError('Versioned native accounting result not qualified')
        if result.get('entities')!=[node.scope_id] or result.get('framework')!=node.framework or result.get('periods')!=node.period:
            raise ValueError('Versioned native result dimensions differ')
        return result

    def correct(self, case, node_id, reviewed_source, reason):
        """Publish a qualified correction on the retained ordinary Case graph.

        Period reopening is separately governed. The caller supplies an already
        reviewed native input, never an inferred replacement certification.
        """
        from .governed_plan import observation
        session=case.governance
        if node_id not in dict(session.graph.nodes):raise ValueError('Correction requires exact execution node')
        if session.versions.current(node_id) is None:raise ValueError('Correction requires current original result')
        session.cao=self
        session.execute(node_id,observation,copy.deepcopy(reviewed_source),reason)
        session.sources[node_id]=copy.deepcopy(reviewed_source)
        plan=session.rework_history[-1]
        self._refresh_versioned(case,final=False)
        return copy.deepcopy(plan)

    def restate(self, case, node_id, reviewed_source, reason, approval):
        """Governed history classification, without accounting restatement authority."""
        if not isinstance(approval,dict) or set(approval)!={'status','evidence','convention'} or approval['status']!='APPROVED' or approval['convention']!='SYNTHETIC_GOVERNED' or not approval['evidence']:
            raise ValueError('Governed restatement lineage approval required')
        session=case.governance
        original=session.versions.current(node_id)
        plan=self.correct(case,node_id,reviewed_source,reason)
        session.versions.history.append(dict(event='RESTATEMENT_LINEAGE',original_version=original.version_id,restated_version=plan['new_version'],approval=copy.deepcopy(approval),accounting_authority=False))
        return plan

    def selective_reexecute(self, case, plan, reviewed_sources=None):
        """Rerun only the current exact dependency plan, then refresh delivery."""
        from .governed_plan import observation
        session=case.governance;session.cao=self
        sources=copy.deepcopy(dict(session.sources))
        for key,value in (reviewed_sources or {}).items():
            if key not in plan['execution_order']:raise ValueError('Unrelated reviewed rework input')
            sources[key]=copy.deepcopy(value)
        # Clear delivery before execution so a failed native recertification can
        # never leave the previous public conclusion current.
        self._refresh_versioned(case,final=False)
        try:
            ledger=session.reexecute(plan,{key:observation for key in plan['execution_order']},sources)
            for key in plan['execution_order']:session.sources[key]=sources[key]
            self._refresh_versioned(case,final=True)
            return ledger
        except (ValueError,KeyError,TypeError,AttributeError,ArithmeticError):
            self._refresh_versioned(case,final=False)
            raise

    def _refresh_versioned(self,case,final):
        session=case.governance
        case.conclusions=[];case.diagnostics=[];case.balance_diagnostics={}
        case.journal_mapping_valid=False;case.journal_ownership_ledger=[]
        if hasattr(case,'_scoped_postings'):del case._scoped_postings
        case.group_consumer={}
        session.cases.refresh(session.graph,session.versions,session.edges)
        case.workplan_nodes=session.graph.record()
        case.owner_results=[dict(n.execution_receipt) for n in session.graph.nodes.values() if n.status=='complete']
        if final and hasattr(session,'request'):
            # Revalidate existing native challenge contracts against the new
            # independently supplied source/result population. No approvals are
            # manufactured by the correction API.
            self._challenge(case,session.graph,session.sources,session.request,session.context)
            from .runtime_governance import reconcile
            reconcile(session)
            if case.outcome=='complete':case.conclusions=[self._synthesis(case,session.graph,session.context)]
            case.workplan_nodes=session.graph.record()
        case.execution_ledger.append(dict(action='selective-currentness-refresh',status=case.outcome))

    def rework(self, previous, revised_request):
        if revised_request.get('case_id') == previous.id:
            raise ValueError('Rework requires a new versioned Case identity')
        revised=self.run(revised_request)
        revised.supersedes.append(previous.id)
        previous.superseded_by.append(revised.id)
        return revised

    def _handoff(self,c,graph,inputs,b,consumed):
        producer=graph.nodes[b['producer']]; consumer=graph.nodes[b['consumer']]
        if producer.status!='complete': raise ValueError('Incomplete owner handoff')
        if dimensions(inputs[producer.id]) != dimensions(inputs[consumer.id]): raise ValueError('Handoff dimensions differ')
        path=b['metric_path']; purpose=b['purpose']; semantic=b['semantic']
        if producer.selected_skill=='derivatives-hedge-accounting' and consumer.selected_skill=='financial-statements':
            calc=producer.result['calculations']; relationships=inputs[producer.id]['relationships']
            if any(d['route']!='cash_flow' or number(d['opening']) or number(d['settlement']) for d in calc['derivatives']) or any(number(r[k]) for r in calc['hedge_reserves'] for k in ('opening','reclassification','basis_adjustment')) or any(r['status'] not in ('active','rebalanced') for r in relationships):
                raise ValueError('Hedge reporting handoff supports first-year continuing cash-flow hedges only; prior movements require separate governed mapping')
        allowed={
            'debt_base':('debt-financing',None,'report'),
            'debt_current':('debt-financing',None,'report'),
            'debt_noncurrent':('debt-financing',None,'report'),
            'interest_expense':('debt-financing',None,'report'),
            'derivative_balance':('derivatives-hedge-accounting',None,'report'),
            'hedge_reserve':('derivatives-hedge-accounting',None,'report'),
            'hedge_pnl':('derivatives-hedge-accounting',None,'report'),
            'hedge_oci':('derivatives-hedge-accounting',None,'report'),
            'cash_balance':('cash-flow-reporting',['closing'],'report'),
            'financing_cash':('cash-flow-reporting',['financing'],'report'),
            'operating_cash':('cash-flow-reporting',['direct_operating'],'report'),
            'factory_labour':('employee-benefits-payroll',['expense'],'absorb'),
            'factory_depreciation':('fixed-assets',['depreciation'],'absorb'),
            'factory_supplier':('accounts-payable',['invoices'],'absorb'),
            'historical_purchase':('foreign-currency',None,'absorb'),
            'inventory_balance':('inventory-cost',['closing_inventory'],'report'),
            'cogs':('inventory-cost',['cogs'],'report'),
            'revenue':('revenue-recognition',['period_revenue'],'report'),
            'ar_balance':('accounts-receivable',['closing_ar'],'report'),
            'allowance':('financial-instruments-ecl',['allowance'],'report'),
            'credit_exposure':('accounts-receivable',['closing_ar'],'review'),
            'contract_balance':('revenue-recognition',['contract_bridge','closing'],'report'),
            'monetary_fx':('foreign-currency',['monetary_fx_profit'],'report'),
        }
        if semantic.startswith('ar_ageing_') and semantic[10:] in ('current','1_30','31_60','61_90','over90'):
            allowed[semantic]=('accounts-receivable',['ageing',semantic[10:]],'review')
        spec=allowed.get(semantic)
        if not spec or producer.selected_skill!=spec[0] or purpose!=spec[2] or (spec[1] is not None and path!=spec[1]):
            raise ValueError('Semantic owner metric mismatch')
        if semantic=='historical_purchase' and (len(path)!=3 or path[0]!='transactions' or path[2]!='initial'):
            raise ValueError('FX historical metric mismatch')
        tails={'debt_base':('debt','closing'),'debt_current':('debt','current'),'debt_noncurrent':('debt','noncurrent'),'interest_expense':('debt','effective_interest'),'derivative_balance':('derivatives','closing'),'hedge_reserve':('hedge_reserves','closing'),'hedge_pnl':('derivatives','ineffectiveness'),'hedge_oci':('hedge_reserves','recognized_oci')}
        if semantic in tails and (len(path)!=3 or (path[0],path[2])!=tails[semantic]):raise ValueError('Owner metric path contradicts semantic')
        value=number(at(producer.result['calculations'],path))
        components=b.get('components',[])
        if components:
            if semantic not in ('debt_base','debt_current','debt_noncurrent') or len(components)!=1:raise ValueError('Unsupported composed monetary balance')
            component=components[0]
            fxnode=graph.nodes.get(component.get('producer'))
            if not fxnode or fxnode.selected_skill!='foreign-currency' or fxnode.status!='complete' or component.get('metric_path')!=['monetary_fx_profit'] or component.get('sign')!=-1:raise ValueError('Qualified monetary owner component required')
            dc=inputs[producer.id];fc=inputs[fxnode.id]
            if dimensions(dc)!=dimensions(fc) or len(dc['debt'])!=1 or len(fc['items'])!=1:raise ValueError('Monetary source population/dimensions differ')
            debt=dc['debt'][0];item=fc['items'][0];base=producer.result['calculations']['debt'][0]
            tx=fxnode.result['calculations']['transactions'][0]
            if item['id']!=debt['id'] or item['side']!='liability' or item['type']!='monetary':raise ValueError('Wrong monetary debt source')
            if number(debt['opening_carrying'])!=number(item['opening_book']) or number(base['repayments'])!=number(tx['settlement']) or number(base['effective_interest'])!=number(base['cash_interest']) or number(base['draws']) or number(base['eligible_cost']):raise ValueError('Monetary bridge outside qualified plain settled-interest liability scope')
            if number(base['closing'])!=number(item['foreign_amount']-Decimal(0) if isinstance(item['foreign_amount'],Decimal) else item['foreign_amount'])*number(item['opening_rate'])-number(tx['settlement']):raise ValueError('Original currency base and principal differ')
            if semantic!='debt_base' and number(value)!=number(base['closing']):raise ValueError('FX maturity allocation requires complete evidenced principal class')
            value-=number(at(fxnode.result['calculations'],component['metric_path']))
            if value!=number(tx['closing']):raise ValueError('Monetary closing liability bridge differs')
        sign=number(b.get('sign',1))
        if semantic in ('ar_balance','credit_exposure') or semantic.startswith('ar_ageing_'):
            if sign!=1:raise ValueError('Receivable exposure sign cannot invert')
        if semantic in ('contract_balance','allowance') and consumer.selected_skill=='financial-statements':
            row=at(inputs[consumer.id],b['target_path'][:-1])
            category='asset' if semantic=='allowance' or value>=0 else 'liability'
            if row.get('category')!=category:raise ValueError('Owner balance statement classification differs')
        if consumer.selected_skill=='financial-statements':
            targets={'debt_base':('liability',-1),'interest_expense':('expense',1),'derivative_balance':('asset' if value>=0 else 'liability',1),'hedge_pnl':('revenue' if value>=0 else 'expense',-1),'hedge_oci':('oci',-1),'cash_balance':('asset',1)}
            if semantic in targets:
                expected_category,expected_sign=targets[semantic]
                if len(b['target_path'])!=3 or b['target_path'][0]!='current_tb' or b['target_path'][2]!='balance' or sign!=expected_sign or at(inputs[consumer.id],b['target_path'][:-1]).get('category')!=expected_category:raise ValueError('Owner reporting semantic target/classification differs')
            if semantic=='financing_cash' and b['target_path']!=['cash_flow','financing']:raise ValueError('Financing cash must bind actual statement cash flow')
        actual=number(at(inputs[consumer.id],b['target_path']))*sign
        if actual!=value or number(b['amount'])!=value: raise ValueError('Owner and consumer amount contradiction')
        if not isinstance(b.get('economic_id'),str) or not b['economic_id'] or not b.get('qualification_evidence'):
            raise ValueError('Economic identity and eligible-cost evidence required')
        identity=(b['economic_id'],purpose if purpose=='absorb' else (purpose,consumer.id))
        metric_identity=('metric',producer.id,tuple(path),purpose if purpose=='absorb' else (purpose,consumer.id))
        target_identity=('target',consumer.id,tuple(b['target_path']),purpose)
        if identity in consumed or metric_identity in consumed or target_identity in consumed: raise ValueError('Economic source consumed twice')
        consumed.update((identity,metric_identity,target_identity))
        c.handoff_ledger.append(dict(producer=producer.id,consumer=consumer.id,semantic=semantic,
            metric_path=path,economic_id=b['economic_id'],amount=str(value),purpose=purpose,
            fingerprint=producer.result['case_fingerprint'],components=copy.deepcopy(components),qualification_evidence=b['qualification_evidence']))

    @staticmethod
    def _result_receipt(n, source):
        return dict(producing_node=n.id,owner=n.selected_skill,scope_id=n.scope_id,scope_type=n.scope_type,
            framework=n.framework,jurisdiction=n.jurisdiction,functional_currency=n.functional_currency,
            presentation_currency=n.presentation_currency,period=n.period,
            exact_case_fingerprint=n.result.get('case_fingerprint'),result_fingerprint=digest(n.result),currentness='CURRENT')

    def _economics(self,c,n,source,owned,entries):
        # Owner economic source identities are carried explicitly by source rows;
        # consumers may reference them via actual imports, never own them again.
        refs={r.get('economic_id') for r in source.get('owner_links',[])}
        for population in ('movements','costs','benefits','invoices','assets','items','obligations'):
            rows=source.get(population,[])
            if not isinstance(rows,list): continue
            for row in rows:
                id=row.get('economic_id')
                if not id or id in refs: continue
                key=(n.scope_id,tuple(n.period),id)
                if key in owned: raise ValueError('Duplicate economics within posting Scope: '+id)
                owned[key]=n.id
                c.economic_ledger.append(dict(economic_id=id,owner=n.id,population=population,source_scope=n.scope_id,posting_scope=n.scope_id,currency=currency(source),period=n.period))
        for index,j in enumerate(n.result.get('journal_entry_implications',[])):
            c.journal_ownership_ledger.append(dict(source_scope=n.scope_id,posting_scope=n.scope_id,accounting_layer=n.scope_type,owner=n.selected_skill,node=n.id,currency=currency(source),period=n.period,economic_identity=[n.scope_id,n.id,n.result['case_fingerprint'],index],posting=True))
            signature=(n.id,digest(j))
            if signature in entries: raise ValueError('Duplicate owner journal')
            entries.add(signature)

    def _challenge(self,c,g,inputs,request,context):
        findings=[]
        def flag(nodes,code,message):
            findings.append(dict(code=code,nodes=nodes,finding=message))
            for id in nodes:
                if id in g.nodes: g.invalidate(id,message)
        for n in list(g.nodes.values()):
            if n.status=='complete':
                fresh=production.assess_case(n.selected_skill,inputs[n.id])
                if digest(fresh)!=digest(n.result): flag([n.id],'STALE_OWNER','Owner result changed during challenge')
        ar=next((n for n in g.nodes.values() if n.selected_skill=='accounts-receivable' and n.status=='complete'),None)
        ecl=next((n for n in g.nodes.values() if n.selected_skill=='financial-instruments-ecl' and n.status=='complete'),None)
        if ar and ecl:
            ec=inputs[ecl.id];ac=ar.result['calculations'];gross=ecl.result['calculations']['gross_carrying_amount']
            valid=number(gross)==number(ac['closing_ar'])
            if ec['credit']['method']=='loss_rate':
                valid=valid and all(sum((number(t['exposure']) for t in scenario['terms']),Decimal(0))==number(gross) for scenario in ec['credit']['scenarios'])
                review=ec['credit'].get('loss_rate_review',{})
                try:
                    dates={key:date.fromisoformat(review[key]) for key in ('as_of','effective_from','reviewed_on')}
                    valid=valid and all(dates[key].isoformat()==review[key] for key in dates) and dates['as_of']==date.fromisoformat(c.periods[1]) and dates['effective_from']<=date.fromisoformat(c.periods[0])<=dates['reviewed_on']<=date.fromisoformat(ec['execution_date']) and bool(review['source_version'].strip())
                    rows=review['rows']
                    valid=valid and all(scenario['terms']==rows for scenario in ec['credit']['scenarios'])
                    valid=valid and all(number(t['exposure'])==number(ac['ageing'][t['bucket']]) for t in rows)
                    valid=valid and {t['bucket'] for t in rows}=={bucket for bucket,amount in ac['ageing'].items() if number(amount)!=0}
                except (KeyError,TypeError,ValueError):valid=False
            if not valid:flag([ecl.id],'AR_ECL_EXPOSURE','Reviewed credit exposure does not reconcile to current governed receivables')
        close_owner=next((n for n in g.nodes.values() if n.selected_skill=='month-end-close' and n.status=='complete'),None)
        if close_owner:
            source=inputs['month-end-close']
            c.close_observations=[dict(kind='late_posting',effective_date=j['posting_date'],posted_at=j['posted_at'],approval_date=j['approval_date'],amount=str(sum((number(l['amount']) for l in j['lines'] if l['side']=='Dr'),Decimal(0))),status='supported_cutoff_and_approval') for j in source['journals'] if j['posted_at']>c.periods[1]]
            if source['close']['reopened']:c.close_observations.append(dict(kind='reopened_period',status='authorized_and_reclosed'))
        # Cross-owner delivered quantity is not established by a revenue amount.
        # Require a reconciliation if an actual contract source supplies units.
        inventory=next((n for n in g.nodes.values() if n.selected_skill=='inventory-cost' and n.status=='complete'),None)
        revenue=next((n for n in g.nodes.values() if n.selected_skill=='revenue-recognition' and n.status=='complete'),None)
        if inventory and revenue:
            sales=inputs[revenue.id].get('delivered_quantity')
            if sales is not None:
                relieved=sum((number(m['quantity']) for m in inputs[inventory.id].get('movements',[]) if m.get('kind')=='sale'),Decimal(0))
                if number(sales)!=relieved:
                    flag([revenue.id,inventory.id],'SALES_RELIEF','Revenue delivered units differ from inventory sale relief; reconcile source populations')
        if inventory and revenue and context.get('gross_margin_basis') not in ('inventory_relief_only','inventory_relief_and_manufacturing_expense'):
            c.open_questions.append(dict(kind='blocking',question='Confirm gross-margin policy: does cost of sales include unallocated manufacturing expense?'))
        # Structured independent assertions compare actual owner metrics with
        # separately supplied GL/system/quantity/policy evidence. No prose wins.
        assertions=request.get('challenge_assertions',[])
        if not isinstance(assertions,list): raise ValueError('Challenge assertions must be a list')
        for a in assertions:
            id=g.nodes.resolve(a['node']); n=g.nodes.get(id)
            if n is None: raise ValueError('Unknown challenged owner')
            if n.status!='complete': continue
            actual=at(n.result['calculations'],a['metric_path'])
            if a.get('operator','equal')=='equal': valid=number(actual)==number(a['evidence_value'])
            elif a['operator']=='at_least': valid=number(actual)>=number(a['evidence_value'])
            else: raise ValueError('Unknown challenge operator')
            if not a.get('evidence_ref'): raise ValueError('Independent challenge evidence required')
            if not valid: flag([id],a['code'],'Contradictory '+a['code']+' evidence requires rework')
        # Preserve policy/prior-case conflict and alternative treatment as actual
        # unresolved review nodes. A caller cannot mark a conflict resolved by prose.
        for conflict in request.get('policy_conflicts',[]):
            flag(conflict['nodes'],'POLICY_CONFLICT',conflict['finding'])
            c.alternatives.extend(conflict.get('alternatives',[]))
        reporting=next((n for n in g.nodes.values() if n.selected_skill=='financial-statements' and n.status=='complete'),None)
        journal_owners=[n for n in g.nodes.values() if n.issue!='diagnostic accounting follow-up' and n.status=='complete' and n.result.get('journal_entry_implications')]
        if reporting and (len(journal_owners)>1 or 'journal_account_mapping' in request):
            try:
                self._journal_mapping(c,g,inputs,request,reporting)
                c.journal_mapping_valid=True
            except (ValueError,KeyError,TypeError,ArithmeticError) as exc:
                flag([reporting.id],'JOURNAL_MAPPING',str(exc))
        for n in g.nodes.values():
            if n.status in ('blocked','partial'):
                findings.append(dict(code='OPEN_OWNER',nodes=[n.id],finding='; '.join(n.open_items)))
        c.challenge_results=[dict(phase='CHALLENGE',checks=['facts','framework/jurisdiction','evidence conflicts',
            'alternatives and estimates','policy/prior decisions','duplicate economics','current owner results',
            'journals/reconciliations','controls','disclosures','systems','audit documentation'],
            findings=findings,passed=not findings)]

    def _journal_mapping(self,c,g,inputs,request,reporting):
        if 'source_assembly_journals' in request:
            from .journal_scopes import validate_assembly
            native=[dict(owner=n.selected_skill,case_fingerprint=n.result['case_fingerprint'],journals=n.result.get('journal_entry_implications',[]))
                for n in g.nodes.values() if n.issue!='diagnostic accounting follow-up' and n.status=='complete']
            validate_assembly(c,g,inputs,request,native)
            return
        mapping=request.get('journal_account_mapping');review=request.get('journal_pack_review',{})
        if not isinstance(mapping,dict) or any(not isinstance(k,str) or not isinstance(v,str) for k,v in mapping.items()):
            raise ValueError('Malformed journal mapping')
        native=[dict(owner=n.selected_skill,case_fingerprint=n.result['case_fingerprint'],journals=n.result.get('journal_entry_implications',[]))
            for n in g.nodes.values() if n.issue!='diagnostic accounting follow-up' and n.status=='complete']
        payload=dict(mapping=mapping,native_owner_journals=native)
        if 'journal_ownership' in request:payload['journal_ownership']=request['journal_ownership']
        if 'journal_event_sources' in request:payload['journal_event_sources']=request['journal_event_sources']
        if request.get('journal_event_sources') is not None:
            sources=request['journal_event_sources'];seen=set()
            if not isinstance(sources,list) or len(sources)!=len(request.get('journal_ownership',[])):raise ValueError('Complete event source population required')
            for event,source in zip(request['journal_ownership'],sources):
                if set(source)!={'economic_id','entity','period','currency','origin','record','nature'} or source['economic_id']!=event['economic_id']:raise ValueError('Event source binding differs')
                if (source['entity'],source['period'],source['currency'])!=(c.entities[0],c.periods,currency(inputs[reporting.id])):raise ValueError('Event source dimensions differ')
                key=(source['origin'],source['record']) if source['origin']=='bank' else tuple(source[k] for k in ('origin','record','nature'))
                if any(not isinstance(v,str) or not v.strip() for v in key) or key in seen:raise ValueError('Economic source counted twice under event aliases')
                seen.add(key)
        if review.get('payload_fingerprint')!=digest(payload) or review.get('approved') is not True or not review.get('reviewer') or review.get('reviewer')==review.get('preparer'):
            raise ValueError('Mapped journal pack requires independent exact-payload review')
        delta={}
        selected,ledger=self._qualified_journals(native,mapping,request.get('journal_ownership'))
        if c is not None:c.journal_ownership_ledger=ledger;c._journal_mapping=copy.deepcopy(mapping)
        for entry in selected:
            for line in entry['lines']:
                account=mapping.get(line['account'],line['account'])
                delta[account]=delta.get(account,Decimal(0))+number(line['amount'])*(1 if line['side']=='Dr' else -1)
        if request.get('journal_event_sources') is not None and 'cash-flow-reporting' in inputs:
            cash_accounts={row['id'] for row in inputs[reporting.id]['current_tb'] if row.get('cash_account') is True}
            bank={row['bank_id']:row for row in inputs['cash-flow-reporting']['transactions']}
            consumed_bank=set()
            for source,event in zip(request['journal_event_sources'],selected):
                cash_amount=sum((number(line['amount'])*(1 if line['side']=='Dr' else -1) for line in event['lines'] if mapping.get(line['account'],line['account']) in cash_accounts),Decimal(0))
                if cash_amount:
                    if source['origin']!='bank' or source['record'] not in bank or source['record'] in consumed_bank:raise ValueError('Cash event needs unique original bank record')
                    row=bank[source['record']]
                    if number(row['amount'])!=cash_amount:raise ValueError('Posting cash amount differs from original bank event')
                    consumed_bank.add(source['record'])
                elif source['origin']=='bank':raise ValueError('Noncash event cannot claim bank cash ownership')
            if consumed_bank!=set(bank):raise ValueError('Native bank cash population omitted from exact-once postings')
        source=inputs[reporting.id]
        current={row['id']:number(row['balance']) for row in source['current_tb']}
        opening={row['id']:number(row['balance']) for row in source['comparative_tb']}
        for account in set(delta)|set(current)|set(opening):
            if delta.get(account,Decimal(0))!=current.get(account,Decimal(0))-opening.get(account,Decimal(0)):
                raise ValueError('Mapped owner journals disagree with reviewed statement GL movement: '+account)

    @staticmethod
    def _qualified_journals(native,mapping,ownership=None):
        """Retain all implications; count independently qualified economic events once.

        Witness sets must match the entire mapped debit/credit population (gross,
        not just net balance). Every native journal appears exactly once. Runtime
        creates neither source-event identity nor reviewer authorization.
        """
        journals={(r['owner'],i):j for r in native for i,j in enumerate(r['journals'])}
        if ownership is None:
            return [dict(owner=owner,index=i,lines=copy.deepcopy(j)) for (owner,i),j in journals.items()],[]
        if not isinstance(ownership,list) or not ownership:raise ValueError('Reviewed journal economic-event population required')
        used={};events=set();selected=[];ledger=[]
        atoms={(owner,i,line):number(v['amount']) for (owner,i),j in journals.items() for line,v in enumerate(j)}
        def resolve(refs):
            if not isinstance(refs,list) or not refs:raise ValueError('Journal reference population required')
            out=[];total={}
            for ref in refs:
                if not isinstance(ref,dict) or set(ref) not in ({'owner','index'},{'owner','index','line','amount'}) or type(ref['index']) is not int:raise ValueError('Invalid journal reference')
                key=(ref['owner'],ref['index'])
                if key not in journals:raise ValueError('Native journal absent')
                if 'line' in ref:
                    if type(ref['line']) is not int or not 0<=ref['line']<len(journals[key]):raise ValueError('Native journal line absent')
                    indexes=[ref['line']]
                else:indexes=list(range(len(journals[key])))
                lines=[]
                for i in indexes:
                    line=copy.deepcopy(journals[key][i]);token=key+(i,)
                    amount=number(ref['amount']) if 'line' in ref else number(line['amount'])
                    if line['side'] not in ('Dr','Cr') or amount<0 or amount>atoms[token]:raise ValueError('Invalid journal line allocation')
                    if atoms[token]==0 and token in used:raise ValueError('Zero journal implication consumed twice')
                    used[token]=used.get(token,Decimal(0))+amount
                    if used[token]>atoms[token]:raise ValueError('Journal implications consumed twice')
                    line['amount']=str(amount);lines.append(line)
                    account=(mapping.get(line['account'],line['account']),line['side'])
                    total[account]=total.get(account,Decimal(0))+amount
                out.append(dict(owner=key[0],index=key[1],lines=lines))
            if sum((v for (account,side),v in total.items() if side=='Dr'),Decimal(0))!=sum((v for (account,side),v in total.items() if side=='Cr'),Decimal(0)):raise ValueError('Economic journal allocation is not balanced')
            return out,{k:v for k,v in total.items() if v}
        for event in ownership:
            if not isinstance(event,dict) or set(event)!={'economic_id','primary','witnesses','evidence'} or not isinstance(event['economic_id'],str) or not event['economic_id'] or not isinstance(event['evidence'],str) or not event['evidence']:raise ValueError('Qualified journal event identity/evidence required')
            if event['economic_id'] in events:raise ValueError('Duplicate journal economic identity')
            events.add(event['economic_id']);actual,totals=resolve(event['primary']);selected.append(dict(owner=actual[0]['owner'],lines=[line for part in actual for line in part['lines']]))
            if not isinstance(event['witnesses'],list):raise ValueError('Invalid journal witnesses')
            for witness in event['witnesses']:
                _,other=resolve(witness)
                if other!=totals:raise ValueError('Corroborating journal economics differ from posting owner')
            ledger.append(copy.deepcopy(event))
        if used!=atoms:raise ValueError('Native journal implication population omitted or partially allocated')
        return selected,ledger

    def _synthesis(self,c,g,context):
        if hasattr(c,'governance'):
            c._synthesis_currentness=sorted((node,key,c.governance.versions.state(key)) for node,key in c.governance.versions.active.items())
        values={}; journals=[]; controls=[]; reporting=[]; limits=[]; approvals=[]
        for n in g.nodes.values():
            if n.issue=='diagnostic accounting follow-up' or n.status!='complete' or not n.result: continue
            r=n.result
            # Numeric accounting authority is extracted by owner semantic, not
            # added indiscriminately across results.
            metrics={'inventory-cost':('closing_inventory','cogs'),'revenue-recognition':('period_revenue',),'accounts-payable':('closing_ap',),'accounts-receivable':('closing_ar','billed','credits','applied_cash_and_deposits','unapplied_liability','fx_movement','bank_receipts'),'financial-instruments-ecl':('allowance','expense'),'foreign-currency':('monetary_fx_profit',)}
            for metric in metrics.get(n.selected_skill,()):
                if metric in r.get('calculations',{}): values[(n.scope_id+' '+n.framework+' '+currency_from_node(n)+(' '+n.period[0]+' to '+n.period[1] if sum(x.selected_skill==n.selected_skill and x.scope_id==n.scope_id for x in g.nodes.values())>1 else '')+' '+metric) if sum(x.selected_skill==n.selected_skill for x in g.nodes.values())>1 else metric]=str(number(r['calculations'][metric]))
            for j in r.get('journal_entry_implications',[]): journals.append(dict(owner=n.id,lines=copy.deepcopy(j)))
            controls.extend(r.get('controls_impacted',[])); reporting.extend(r.get('reporting_impacted',[])+r.get('disclosures_impacted',[]))
            limits.extend(r.get('uncertainties',[])); approvals.extend(r.get('documentation_required',[]))
        if c.journal_mapping_valid and hasattr(c,'_scoped_postings'):
            journals=[dict(owner=r['owner'],lines=r['lines']) for r in c._scoped_postings]
        elif c.journal_mapping_valid and c.journal_ownership_ledger:
            native=[dict(owner=n.selected_skill,journals=n.result.get('journal_entry_implications',[])) for n in g.nodes.values() if n.issue!='diagnostic accounting follow-up' and n.status=='complete']
            # Verified at challenge against the approved mapping. Line-grain
            # allocations retain bank receipt residuals without duplicate cash.
            selected,_=self._qualified_journals(native,c._journal_mapping,c.journal_ownership_ledger)
            journals=[dict(owner=r['owner'],lines=r['lines']) for r in selected]
        revenue_owner=next((n for n in g.nodes.values() if n.selected_skill=='revenue-recognition' and n.status=='complete'),None)
        if revenue_owner and sum(n.selected_skill=='revenue-recognition' for n in g.nodes.values())==1:
            contract=number(revenue_owner.result['calculations']['contract_bridge']['closing'])
            values.update(contract_asset=str(max(contract,0)),contract_liability=str(max(-contract,0)))
        inventory=next((n for n in g.nodes.values() if n.selected_skill=='inventory-cost' and n.status=='complete'),None)
        if inventory:
            calc=inventory.result['calculations']
            for label,amount in sorted(calc.get('inventory_by_class',{}).items()): values[label]=str(number(amount))
            for label in ('write_down','reversal','manufacturing_expense'):
                if label in calc:values[label]=str(number(calc[label]))
            for order in inputs_for_synthesis(inventory.result):
                for label in ('material','direct_labour','variable_overhead','fixed_overhead','absorbed_fixed','under_recovery','actual_eligible_total','completed_cost','closing_wip','finished_unit_cost'):
                    if label in order:values[label]=str(number(order[label]))
        if 'period_revenue' in values and 'cogs' in values:
            revenue=number(values['period_revenue']); relief_margin=revenue-number(values['cogs'])
            values['revenue_less_inventory_relief']=str(relief_margin)
            overhead=number(values.get('manufacturing_expense','0'))
            basis=context.get('gross_margin_basis')
            if basis in ('inventory_relief_only','inventory_relief_and_manufacturing_expense'):
                cost_of_sales=number(values['cogs'])+(overhead if basis=='inventory_relief_and_manufacturing_expense' else Decimal(0))
                margin=revenue-cost_of_sales
                values['cost_of_sales']=str(cost_of_sales)
                values['gross_margin']=str(margin);values['gross_margin_percent']=str(margin/revenue*100) if revenue else None
        open_items=[dict(node=n.id,issue=n.issue,reason='; '.join(n.open_items),required=n.required,material=n.material)
            for n in g.nodes.values() if n.status in ('blocked','partial')]
        text='The supplied accounting workpapers support the requested conclusion within the reviewed scope.' if c.outcome=='complete' else 'The accounting review is unresolved in the areas listed below; completed workpapers are retained.'
        if c.diagnostics:
            d=c.diagnostics[0];b=d['bridge']
            text='The '+b['metric'].replace('_',' ')+' moved from '+format(number(b['starting']),',.2f')+' to '+format(number(b['ending']),',.2f')+'. Explained signed movement is '+format(number(b['explained_amount']),',.2f')+'; explicit unexplained residual is '+format(number(b['residual']),',.2f')+'.'
            if c.outcome!='complete':text+=' The review remains unresolved in the listed areas.'
            for driver in b['drivers']:
                text+=' '+driver['label']+': '+format(number(driver['contribution']),',.2f')+' ('+driver['category'].replace('_',' ')+', '+driver['confidence']+' confidence; bridge contribution).'
            text+=' Accounting treatment remains with the reviewed accounting owner; diagnostic attribution does not authorize an adjustment.'
            for q in c.accounting_questions:
                text+=' Accounting check '+q['issue']+': '+('supported by the completed accounting workpaper' if q['status']=='OWNER_RECHECK_SUPPORTED' else 'unresolved')+'.'
                if q.get('accounting_disposition')=='unallocated manufacturing expense':text+=' The accounting owner records '+q['amount']+' as unallocated manufacturing expense; the analytical bridge itself does not authorize capitalization.'
            values.update(diagnostic_change=b['change'],diagnostic_explained=b['explained_amount'],diagnostic_residual=b['residual'])
            if b['explained_percent'] is not None:values['diagnostic_explained_percent']=b['explained_percent']
            for h in d['hypotheses']:limits.append('Hypothesis: '+h['hypothesis']+'; '+h['disposition']+' ('+h['evidence_class'].replace('_',' ')+').')
            for observation in d['observations']:limits.append(observation['observation']+'; observation only. '+observation['question'])
            if b['comparator_kind']!='actual':limits.append('Supplied '+b['comparator_kind']+' is an analytical comparator, not accounting actual or a new forecast.')
        if c.balance_diagnostics:
            d=c.balance_diagnostics
            reporting=['Revenue, billed receivables, allowance and contract balances tie to reviewed statements.','Receivable FX is presented separately from revenue.']
            if any(n.selected_skill=='disclosure-management' and n.status=='complete' for n in g.nodes.values()):reporting.append('The scoped monthly credit-loss note consumes reviewed allowance and statement results; external filing compliance is outside this review.')
            status='The reviewed close balances reconcile' if c.outcome=='complete' else 'The close is partial: material source or close evidence remains unresolved'
            text=status+'. Revenue changed from '+d['revenue']['prior']+' to '+d['revenue']['current']+', while bank collections changed from '+d['cash_collections']['prior']+' to '+d['cash_collections']['current']+'. Billings were '+d['billings']['current']+'; they are distinct from revenue and cash receipts. Gross billed receivables closed at '+d['bridges']['ar']['closing']+'. Contract liability closed at '+d['contract_liability']+'; it is not a receivable. The reviewed credit allowance closed at '+d['bridges']['allowance']['closing']+'. Receivable FX contributed '+d['fx_effect']+' to the AR movement, separately from billings and collections; it does not explain revenue growth. Unapplied cash of '+d['unapplied_cash']+' remains a customer liability.'
            if c.close_observations:text+=' The period was reopened and reclosed under reviewed authorization; a late-posted journal has supported economic cutoff and approval and is not automatically an accounting error.'
            text+=' Older unpaid invoices require collection follow-up; the supplied evidence does not establish why each customer paid late. The claim that collections only look worse because revenue grew is '+d['management_hypothesis']['disposition'].lower()+'. The accounting owners support the recognition, credit allowance and FX amounts; these are accounting effects, not evidence of a commercial accounting error.'
            if c.outcome!='complete':text+=' Resolve the listed source/reconciliation contradictions before declaring the close clean. Preserve the original due dates and obtain the complete ageing export and reconciliation disposition.'
            for q in c.accounting_questions:text+=' The allowance accounting check is '+('supported by the reviewed workpaper' if q['status']=='OWNER_RECHECK_SUPPORTED' else 'unresolved')+'.'
            for name,b in d['bridges'].items():
                values[name+'_residual']=b['residual']
                if number(b['residual']):limits.append('Explicit '+name.replace('_',' ')+' bridge residual '+b['residual']+'.')
            if d['dso']['current'] is not None:values['snapshot_collection_days']=d['dso']['current'];values['prior_snapshot_collection_days']=d['dso']['prior']
            limits.append(d['dso']['formula']+'. '+d['dso']['limitation'])
        debt=next((n for n in g.nodes.values() if n.selected_skill=='debt-financing' and n.status=='complete'),None)
        cash_owner=next((n for n in g.nodes.values() if n.selected_skill=='cash-flow-reporting' and n.status=='complete'),None)
        hedge=next((n for n in g.nodes.values() if n.selected_skill=='derivatives-hedge-accounting' and n.status=='complete'),None)
        if debt:
            balances=debt.result['calculations']['debt']
            for label in ('opening','draws','eligible_cost','effective_interest','cash_interest','repayments','closing','current','noncurrent'):
                values['debt_'+label]=str(sum((number(row[label]) for row in balances),Decimal(0)))
            for handoff in c.handoff_ledger:
                if g.nodes.get(handoff['consumer']) is not None and g.nodes[handoff['consumer']].selected_skill=='financial-statements' and handoff['semantic'] in ('debt_base','debt_current','debt_noncurrent'):
                    values[{'debt_base':'reported_debt','debt_current':'current_debt','debt_noncurrent':'noncurrent_debt'}[handoff['semantic']]]=handoff['amount']
            text+=' The governed liability schedule closes at '+values['debt_closing']+' before the separately governed currency movement.'
            if 'reported_debt' in values:text+=' Reported debt is '+values['reported_debt']+', with current '+values.get('current_debt','unresolved')+' and noncurrent '+values.get('noncurrent_debt','unresolved')+'.'
            text+=' Accounting interest is '+values['debt_effective_interest']+'; cash interest is '+values['debt_cash_interest']+' and principal repaid is '+values['debt_repayments']+'. These are distinct from noncash currency and valuation effects. Classification relies on the supplied reporting-date rights and covenant evidence; no waiver or refinancing right is inferred.'
        if cash_owner:
            calc=cash_owner.result['calculations']
            for metric in ('opening','closing','direct_operating','investing','financing','fx'):values['cash_'+metric]=str(number(calc[metric]))
            text+=' Cash reconciles from '+values['cash_opening']+' to '+values['cash_closing']+': operating '+values['cash_direct_operating']+', investing '+values['cash_investing']+', financing '+values['cash_financing']+' and cash FX '+values['cash_fx']+'. Noncash debt remeasurement and derivative fair-value movements are excluded from bank flows; the supplied interest classification policy governs cash presentation.'
        if hedge:
            calc=hedge.result['calculations'];values['derivative_balance']=str(sum((number(row['closing']) for row in calc['derivatives']),Decimal(0)));values['hedge_pnl']=str(sum((number(row.get('ineffectiveness',0))+number(row.get('earnings_release',0)) for row in calc['derivatives']),Decimal(0)));values['hedge_reserve']=str(sum((number(row['closing']) for row in calc['hedge_reserves']),Decimal(0)));values['hedge_oci']=str(sum((number(row['recognized_oci']) for row in calc['hedge_reserves']),Decimal(0)))
            text+=' The externally valued derivative closes at '+values['derivative_balance']+'. The governed hedge result allocates '+values['hedge_pnl']+' to earnings and '+values['hedge_oci']+' to OCI; the closing reserve is '+values['hedge_reserve']+'. Accounting effectiveness is based on the actual designated risk evidence and does not establish an offset of unrelated currency exposures. Valuation models and market inputs are supplied by the qualified valuation source.'
        if debt or cash_owner:
            text+=(' The reviewed accounting and cash reconciliations complete within scope.' if c.outcome=='complete' else ' The review remains partial: resolve the listed cash-flow/source or accounting exceptions before declaring the close clean.')
        assembly=next((n for n in g.nodes.values() if n.selected_skill=='consolidation' and n.status=='complete'),None)
        statements=next((n for n in g.nodes.values() if n.selected_skill=='financial-statements' and n.status=='complete'),None)
        if assembly and statements and any(r['consumer']==statements.id and r['semantic']=='consolidated_population' for r in c.handoff_ledger):
            owners={n.selected_skill:n.result['calculations'] for n in g.nodes.values() if n.status=='complete'}
            current=statements.result['calculations']['current'];con=assembly.result['calculations']
            for label in ('assets','liabilities','closing_equity','revenue','expenses','profit','oci'):
                values['consolidated_'+label]=str(number(current[label]))
            values['closing_nci']=str(number(con['nci'][0]['closing']))
            text=('The reviewed group accounts reconcile within the supplied scope. ' if c.outcome=='complete' else 'The group review is partial; material source evidence remains unresolved. ')
            text+='Consolidated profit is '+values['consolidated_profit']+' and OCI is '+values['consolidated_oci']+' in the group presentation currency. Closing equity is '+values['consolidated_closing_equity']+', including NCI '+values['closing_nci']+'. '
            if 'business-combinations' in owners:
                acq=owners['business-combinations']
                for label in ('consideration','net_assets','nci','initial_goodwill'):values['acquisition_'+label]=str(number(acq[label]))
                text+='Acquisition-date amounts in the subsidiary functional currency are: consideration '+values['acquisition_consideration']+', identifiable net assets '+values['acquisition_net_assets']+', initial NCI '+values['acquisition_nci']+' and goodwill '+values['acquisition_initial_goodwill']+'. '
            if 'foreign-currency' in owners:
                fx=owners['foreign-currency']['translation'];values['post_acquisition_profit']=str(number(fx['profit_translated']));values['translation_oci']=str(number(fx['cta_movement']))
                text+='Only the supported post-acquisition contribution of '+values['post_acquisition_profit']+' enters group profit. Translation contributes '+values['translation_oci']+' to OCI; it is separate from operating performance. '
            if 'intercompany-accounting' in owners:
                values['qualified_intercompany_elimination']=str(number(owners['intercompany-accounting']['pairs'][0]['a_functional']))
            values['group_goodwill']=str(number(con['consolidated_balances'].get('goodwill',0)))
            text+='Closing goodwill is '+values['group_goodwill']+'. '
            if 'asset-impairment' in owners:
                imp=owners['asset-impairment'];values['goodwill_test_loss']=str(number(imp['loss']));values['goodwill_test_headroom']=str(number(imp['headroom']))
                text+='The supplied independent unit valuation supports impairment '+values['goodwill_test_loss']+' with headroom '+values['goodwill_test_headroom']+'. '
            values['group_deferred_tax_liability']=str(-number(con['consolidated_balances'].get('Deferred tax liability',0)))
            text+='The acquisition tax determination is included once in identifiable net assets and goodwill; the translated closing deferred-tax liability is '+values['group_deferred_tax_liability']+'. Bilateral intercompany balances are reconciled before consolidation-only elimination; unresolved source differences are never plugged. '
            if c.diagnostics:
                rejected=any(h['id']=='full-year-contribution' and h['disposition']=='REJECTED' for h in c.diagnostics[0]['hypotheses'])
                if rejected:text+='Management’s full-year acquisition contribution claim is rejected: pre-acquisition results do not belong in group profit. '
            if c.outcome!='complete':text+='Resolve the listed intercompany/source contradiction before declaring the accounts clean. '
            reporting=['Qualified consolidated statements preserve goodwill, NCI and translation OCI.','Scoped acquisition, group performance and impairment evidence supports the reviewed disclosures; this is not filing certification.']
        if 'closing_inventory' in values: text+=' Supported closing inventory is '+values['closing_inventory']+'.'
        if 'gross_margin' in values: text+=' Gross margin under the supplied presentation policy is '+values['gross_margin']+'.'
        if c.group_consumer:
            text=c.group_consumer['summary']; limits.extend(c.group_consumer['limitations'])
            journals=[]
        return dict(conclusion=text,status=c.outcome,calculations=values,journals=journals,open_items=open_items,
            controls=sorted(set(controls)),reporting=sorted(set(reporting)),limitations=sorted(set(limits)),
            required_approvals=sorted(set(approvals)),confidence='medium' if c.outcome=='complete' else 'low')

    def _observe(self,c,context,request):
        for k in ('framework','jurisdiction','currency','year_end','industry','gross_margin_basis','policies','systems','known_processes'):
            if k in context:
                c.memory_candidates.append(dict(id=c.id+'-'+k,attribute=k,value=copy.deepcopy(context[k]),
                    status='PROPOSED',scope_id=context['entity'],source_case=c.id,source_refs=['supplied-governed-context'],
                    effective_from=context.get('period_start'),effective_to=None,learned_at=None,
                    related_cases=[c.id],supersedes=[],conflict=False))
        for observation in request.get('observations',[]):
            candidate=copy.deepcopy(observation); candidate.update(status='OBSERVED',source_case=c.id)
            c.memory_candidates.append(candidate)
        c.observer_ran=True

    def public(self,c,route='answer'):
        """Separate curated representation; internal evidence is never mutated."""
        if hasattr(c,'governance'):
            stale=any(c.governance.versions.state(key)!='CURRENT' for key in c.governance.versions.active.values())
            view=sorted((node,key,c.governance.versions.state(key)) for node,key in c.governance.versions.active.items())
            changed_synthesis=bool(c.conclusions) and getattr(c,'_synthesis_currentness',None)!=view
            if changed_synthesis or (stale and not c.conclusions):return public_record(dict(guidance='Accounting work requires selective rework before current delivery.',status='partial',open_items=['Resolve stale dependent results.']),route=route)
        if hasattr(c,'governance') and not c.conclusions:
            observations=[]
            for node_id in sorted(c.governance.versions.active):
                node=c.graph.nodes[node_id]
                version=c.governance.versions.current(node_id,allow_stale=True)
                if node.case_id!=c.id or c.governance.versions.state(version.version_id)!='CURRENT':continue
                payload=version.payload()
                if 'observed_amount' in payload:observations.append(dict(label='Qualified local observation ('+payload['currency']+')',amount=payload['observed_amount']))
            return public_record(dict(guidance='Qualified entity results and downstream reporting observations were refreshed; unrelated work did not require rerun.' if c.governance.rework_history else 'Qualified entity results and reporting observations are current.',status=c.outcome,calculations=observations,limitations=['Local observations retain their original framework and currency; no consolidated converted total is established.']),route=route)
        s=c.conclusions[0] if c.conclusions else dict(conclusion='Accounting work is blocked.',status=c.outcome,
            calculations={},journals=[],open_items=[],controls=[],reporting=[],limitations=[],required_approvals=[])
        # Owners' curated public boundary was executed already. Only accounting
        # amounts, consequences, caveats and open work are emitted here.
        record=dict(guidance=s['conclusion'],status=c.outcome,framework=c.frameworks[0] if c.frameworks else '',
            jurisdiction=c.jurisdictions[0] if c.jurisdictions else '',entity_scope=', '.join(c.entities),
            effective_period=' to '.join(c.periods),
            calculations=[dict(label=k.replace('_',' '),amount=v) for k,v in s['calculations'].items() if v is not None],
            journals=[dict(lines=[dict(side=l['side'],account=l['account'],amount=str(l['amount'])) for l in j['lines']]) for j in s['journals']],
            open_items=[o['issue']+': '+o['reason'] for o in s['open_items']]+[q['question'] for q in c.open_questions],
            controls=s['controls'],reporting=s['reporting'],required_approvals=s['required_approvals'],
            limitations=s['limitations'],uncertainties=[str(a) for a in c.facts['assumed']],
            confidence=s.get('confidence','low'))
        discrepancies={}
        for fact in c.facts.get('disputed',[]):
            label=fact.get('attribute','')
            if not re.fullmatch(r'[a-z][a-z0-9_]{0,80}',label):continue
            try:value=str(number(fact['value']))
            except (ValueError,KeyError,ArithmeticError):continue
            discrepancies.setdefault(label,[]).append(value)
        for label,amounts in discrepancies.items():
            if len(set(amounts))>1:record['open_items'].append('Source conflict for '+label.replace('_',' ')+': '+' versus '.join(dict.fromkeys(amounts))+'. Obtain a reviewed reconciliation; no balancing plug is accepted.')
        # Deny known reviewer identifiers even if inserted inside otherwise
        # allowlisted text. Do not mutate the internal approval evidence.
        private=[]
        def visit(o):
            if isinstance(o,dict):
                for key,value in o.items():
                    if key in ('reviewer','approved_by','reviewer_identity') and isinstance(value,str) and value:private.append(value)
                    else:visit(value)
            elif isinstance(o,list):
                for value in o:visit(value)
        visit(c.workplan_nodes)
        curated=public_record(record,route=route)
        encoded=json.dumps(curated,ensure_ascii=False)
        if any(value in encoded for value in private):raise ValueError('Private reviewer identity in public content')
        return curated
