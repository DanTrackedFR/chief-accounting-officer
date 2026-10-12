"""Version/currentness governance attached to the existing execution Graph.

This module schedules no accounting authority. Executors are provided by CAO and
must use its native production boundary, or an explicitly bounded observation.
"""
import copy
from dataclasses import dataclass, asdict
from .periods import identity


def fingerprint(value): return identity('fingerprint',value).split(':',1)[1]


def blocked_payload(node, source, bindings, blockers):
    """A dependency-governance record, never an accounting result or journal."""
    return dict(status='blocked', case_fingerprint=fingerprint([source, sorted(bindings), sorted(blockers)]),
        unresolved_dependencies=sorted(blockers), accounting_authority=False,
        journal_entry_implications=[], framework=node.framework,
        currency=node.functional_currency or node.presentation_currency,
        limitations=['Required material accounting dependencies remain unresolved.'])


def unresolved_bindings(graph, versions, edges, node_id, bindings):
    """Only actual required/material dependency contracts propagate conflicts."""
    return [key for key, version in bindings
        if (edges[key].required or edges[key].material is not False)
        and (graph.nodes[versions.versions[version].node_id].status != 'complete'
             or versions.versions[version].payload().get('unresolved_dependencies'))]



@dataclass(frozen=True)
class Dependency:
    producer_node: str
    consumer_node: str
    producer_case: str
    consumer_case: str
    producer_scope: str
    consumer_scope: str
    producer_period: str
    consumer_period: str
    dependency_type: str
    consumption: str
    metric_path: tuple
    evidence: tuple
    required: bool = True
    material: bool | None = None
    alignment_evidence: tuple = ()

    @property
    def id(self):
        return identity('dependency',{k:v for k,v in asdict(self).items() if k not in ('evidence','alignment_evidence')})

    def validate(self,graph,cases,periods):
        if type(self.required)!=bool or (self.material is not None and type(self.material)!=bool) or not self.evidence: raise ValueError('Governed dependency/materiality required')
        producer=graph.nodes[self.producer_node]; consumer=graph.nodes[self.consumer_node]
        if producer.id!=self.producer_node or consumer.id!=self.consumer_node or producer.id==consumer.id: raise ValueError('Exact distinct dependency nodes required')
        if (producer.case_id,producer.scope_id,producer.period_id)!=(self.producer_case,self.producer_scope,self.producer_period) or (consumer.case_id,consumer.scope_id,consumer.period_id)!=(self.consumer_case,self.consumer_scope,self.consumer_period): raise ValueError('Dependency dimensional substitution')
        a=periods.get(self.producer_period);b=periods.get(self.consumer_period)
        if self.dependency_type=='CURRENT':
            if a.period_id!=b.period_id: raise ValueError('Wrong current Period')
        elif self.dependency_type in ('OPENING','PRIOR','COMPARATIVE','PARTIAL_INCLUDED_PERIOD'):
            periods.require_relationship(a.period_id,b.period_id,self.dependency_type)
            if self.dependency_type=='OPENING' and producer.scope_id!=consumer.scope_id: raise ValueError('Opening source Scope differs')
        elif self.dependency_type=='QUALIFIED_ALIGNMENT':
            if not self.alignment_evidence: raise ValueError('Qualified calendar alignment required')
        else: raise ValueError('Unsupported temporal dependency')
        cases.qualify_consumption(self,producer,consumer)
        return self


@dataclass(frozen=True)
class ResultVersion:
    result_id: str
    version_id: str
    node_id: str
    case_id: str
    scope_id: str
    period_id: str
    exact_case_fingerprint: str
    source_fingerprint: str
    result_fingerprint: str
    predecessor: str | None
    reason: str
    dependency_bindings: tuple
    payload_json: str

    def payload(self):
        import json
        return json.loads(self.payload_json)


class VersionRegistry:
    def __init__(self,graph=None,edges=None):
        self.graph=graph;self.edges=edges;self.versions={};self.states={};self.active={};self.supersession={};self.history=[]
        # Immutable source payloads belong to their exact versions, not the
        # mutable latest-input table. Persistence never reconstructs old evidence.
        self.source_snapshots={}

    def current(self,node_id,allow_stale=False):
        key=self.active.get(node_id)
        if key is None:return None
        version=self.versions[key]
        if not allow_stale and self.states[key]!='CURRENT': raise ValueError('Stale result cannot satisfy current dependency')
        return version

    def state(self,key):
        if key not in self.versions: raise ValueError('Unknown result version')
        return self.states[key]

    def require_current(self,key):
        if self.state(key)!='CURRENT' or self.active[self.versions[key].node_id]!=key: raise ValueError('Stale/superseded result rejected')
        version=self.versions[key]
        for edge,bound in version.dependency_bindings:self.require_current(bound)
        return version

    def publish(self,node,payload,source,bindings,reason):
        import json
        if not reason or not isinstance(payload,dict) or payload.get('status') not in ('complete','blocked'):raise ValueError('Qualified result/version reason required')
        old=self.current(node.id,allow_stale=True)
        result_id=identity('result',[node.id,node.case_id,node.scope_id,node.period_id])
        source_hash=fingerprint(source);result_hash=fingerprint(payload)
        exact=payload.get('case_fingerprint')
        if not isinstance(exact,str) or not exact:raise ValueError('Exact-case fingerprint required')
        for edge,version in bindings:
            producer=self.require_current(version)
            contract=self.edges.get(edge) if self.edges is not None else None
            if contract is None or contract.producer_node!=producer.node_id or contract.consumer_node!=node.id:raise ValueError('Wrong dependency version producer/consumer')
            if (producer.scope_id,producer.period_id,producer.case_id)!=(contract.producer_scope,contract.producer_period,contract.producer_case):raise ValueError('Dependency binding dimensions differ')
        expected={k for k,e in (self.edges or {}).items() if e.consumer_node==node.id}
        if {edge for edge,version in bindings}!=expected or len(bindings)!=len(expected):raise ValueError('Dependency binding omitted/duplicated')
        blockers=unresolved_bindings(self.graph,self,self.edges,node.id,bindings)
        if blockers and payload!=blocked_payload(node,source,bindings,blockers):raise ValueError('Unresolved material dependency cannot support accounting result')
        if not blockers and payload.get('status')=='blocked':raise ValueError('Blocked result requires actual unresolved dependency')
        content=[result_id,old.version_id if old else None,exact,source_hash,result_hash,sorted(bindings),reason]
        key=identity('version',content)
        if key in self.versions:raise ValueError('Version overwrite')
        version=ResultVersion(result_id,key,node.id,node.case_id,node.scope_id,node.period_id,exact,source_hash,result_hash,old.version_id if old else None,reason,tuple(sorted(bindings)),json.dumps(payload,sort_keys=True,default=str,separators=(',',':')))
        self.versions[key]=version;self.states[key]='CURRENT';self.active[node.id]=key
        self.source_snapshots[key]=copy.deepcopy(source)
        if old:
            self.states[old.version_id]='SUPERSEDED';self.supersession[old.version_id]=key
        self.history.append(dict(event='PUBLISH',version=key,predecessor=version.predecessor,reason=reason))
        return version

    def mark_stale(self,key,edge,upstream):
        if self.state(key)=='CURRENT':
            self.states[key]='STALE';self.history.append(dict(event='STALE',version=key,dependency=edge,upstream=upstream))

    def record(self):return [dict(asdict(self.versions[k]),state=self.states[k],superseded_by=self.supersession.get(k)) for k in sorted(self.versions)]


class VersionedExecution:
    def __init__(self,graph,cases,periods):
        from .runtime import CAO
        self.cao=CAO()
        self.graph=graph;self.cases=cases;self.periods=periods;self.edges={};self.versions=VersionRegistry(graph,self.edges);self.receipts=[];self.rework_history=[]

    def add_dependency(self,edge):
        edge.validate(self.graph,self.cases,self.periods)
        if self.versions.current(edge.consumer_node,allow_stale=True) is not None:raise ValueError('Dependency contracts cannot silently change after qualified execution')
        if edge.id in self.edges:raise ValueError('Duplicate dependency')
        target=self.graph.nodes[edge.consumer_node]
        dependencies=list(target.dependencies)
        if edge.producer_node not in target.dependencies:target.dependencies.append(edge.producer_node)
        try:self.graph.validate()
        except Exception:
            target.dependencies=dependencies;self.graph.validate();raise
        self.edges[edge.id]=edge
        return edge.id

    def receipt(self,edge_id):
        edge=self.edges[edge_id];edge.validate(self.graph,self.cases,self.periods)
        version=self.versions.current(edge.producer_node)
        if version is None or self.graph.nodes[edge.producer_node].status!='complete' or version.payload().get('unresolved_dependencies'):raise ValueError('Required producer blocked/absent/unresolved')
        from .runtime import at
        payload=version.payload(); value=at(payload,edge.metric_path)
        producer=self.graph.nodes[edge.producer_node];consumer=self.graph.nodes[edge.consumer_node]
        value_currency=payload.get('currency',producer.functional_currency or producer.presentation_currency)
        if producer.economic_id is not None and producer.selected_skill=='foreign-currency' and tuple(edge.metric_path)[:2]==('calculations','translation'):
            native_source=self.sources[producer.id]
            if fingerprint(native_source)!=version.source_fingerprint:raise ValueError('Translation source version differs')
            value_currency=native_source['translation']['presentation_currency']
        return dict(dependency_id=edge.id,result_version=version.version_id,producer_node=edge.producer_node,consumer_node=edge.consumer_node,producer_scope=edge.producer_scope,consumer_scope=edge.consumer_scope,producer_period=edge.producer_period,consumer_period=edge.consumer_period,producer_framework=payload.get('framework',producer.framework),consumer_framework=consumer.framework,producer_functional_currency=producer.functional_currency,producer_presentation_currency=producer.presentation_currency,consumer_functional_currency=consumer.functional_currency,consumer_presentation_currency=consumer.presentation_currency,value_currency=value_currency,metric_path=list(edge.metric_path),currentness='CURRENT',result_fingerprint=version.result_fingerprint,value=copy.deepcopy(value))

    def validate_receipt(self,receipt,consumer_node):
        if not isinstance(receipt,dict) or receipt.get('dependency_id') not in self.edges:raise ValueError('Undeclared dependency receipt')
        edge=self.edges[receipt['dependency_id']]
        if edge.consumer_node!=consumer_node or receipt!=self.receipt(edge.id):raise ValueError('Wrong Scope/Period/version or stale receipt')
        return self.versions.require_current(receipt['result_version'])

    def execute(self,node_id,executor,source,reason):
        node=self.graph.nodes[node_id]
        if not isinstance(source,dict) or (source.get('scope_id',source.get('entity')),source.get('period_id'))!=(node.scope_id,node.period_id):raise ValueError('Execution source Scope/Period differs')
        from .scopes import authorize_scope
        authorize_scope(self.cases.scopes,node)
        self.cases.bind_node(node.case_id,node);self.periods.authorize_execution(node.period_id,node.case_id,node.id)
        bindings=[]
        for key,edge in sorted(self.edges.items()):
            if edge.consumer_node!=node.id:continue
            producer=self.versions.current(edge.producer_node)
            if producer is None:raise ValueError('Required producer absent')
            self.versions.require_current(producer.version_id)
            bindings.append((key,producer.version_id))
        if set(node.dependencies)!={self.edges[key].producer_node for key,_ in bindings}:raise ValueError('Workplan has unqualified dependencies')
        blockers=unresolved_bindings(self.graph,self.versions,self.edges,node.id,bindings)
        if blockers:
            result=blocked_payload(node,source,bindings,blockers)
            previous=self.versions.current(node.id,allow_stale=True)
            version=self.versions.publish(node,result,source,bindings,reason)
            if hasattr(self,'sources'):self.sources[node.id]=copy.deepcopy(source)
            node.result=version.payload();node.status='blocked';node.iterations+=1
            node.execution_receipt=dict(result_version=version.version_id,period_id=node.period_id,case_id=node.case_id,currentness='CURRENT',status='blocked')
            if previous:self.invalidate(previous.version_id,version.version_id)
            self.cases.refresh(self.graph,self.versions,self.edges)
            return version
        receipts=[self.receipt(k) for k,e in sorted(self.edges.items()) if e.consumer_node==node.id]
        declared={self.edges[r['dependency_id']].producer_node for r in receipts}
        if set(node.dependencies)!=declared:raise ValueError('Workplan has unqualified dependencies')
        for receipt in receipts:self.validate_receipt(receipt,node.id)
        previous=self.versions.current(node.id,allow_stale=True)
        if node.selected_skill.startswith('orchestration-'):
            if source.get('method') in ('STAGE3_MATCH','STAGE3_GROUP_OBSERVATION'):
                from .stage3 import bounded_executor
                result=bounded_executor(self,node,copy.deepcopy(source),copy.deepcopy(receipts))
            else:
                result=executor(node,copy.deepcopy(source),copy.deepcopy(receipts))
            if result.get('accounting_authority') is not False or result.get('journal_entry_implications'):raise ValueError('Bounded consumer cannot create accounting authority or postings')
        else:
            from .temporal_inputs import validate_native_sources
            context=dict(getattr(self,'context',{}),scopes=self.cases.scopes.record(),period_registry=self.periods.record())
            validate_native_sources(context,node,source)
            if receipts and source.get('versioned_dependency_receipts')!=receipts:raise ValueError('Native consumer requires independently reviewed exact version bindings')
            # Imported native results must match the exact registered producing
            # version as well as their independently reviewed native contract.
            for imported in source.get('imports',[]):
                actual=imported.get('case',{})
                matches=[r for r in receipts if self.graph.nodes[r['producer_node']].selected_skill==imported.get('package') and r['producer_scope']==actual.get('scope_id',actual.get('entity')) and r['producer_period']==actual.get('period_id')]
                if len(matches)!=1 or fingerprint(imported.get('result'))!=self.versions.require_current(matches[0]['result_version']).result_fingerprint:raise ValueError('Imported native result lacks exact current producer version')
            from .stage3 import validate_native_bindings
            validate_native_bindings(self,node,source,receipts)
            result=self.cao.execute_versioned_owner(node,copy.deepcopy(source),copy.deepcopy(receipts))
            if node.selected_skill=='intercompany-accounting' and node.scope_type=='GROUP' and source.get('stage3_contract')=='ORDINARY_IC_REASSESSMENT' and (result.get('journal_entry_implications') or result.get('calculations',{}).get('journal_entities')):
                raise ValueError('Zero-adjustment framework reassessment cannot publish legal-book journals')
        version=self.versions.publish(node,result,source,[(r['dependency_id'],r['result_version']) for r in receipts],reason)
        if hasattr(self,'sources'):self.sources[node.id]=copy.deepcopy(source)
        node.result=version.payload();node.status='complete';node.iterations+=1;node.execution_receipt=dict(result_version=version.version_id,period_id=node.period_id,case_id=node.case_id,currentness='CURRENT')
        self.receipts.extend(copy.deepcopy(receipts))
        if previous:self.invalidate(previous.version_id,version.version_id)
        self.cases.refresh(self.graph,self.versions,self.edges)
        return version

    def invalidate(self,old_version,new_version):
        old=self.versions.versions[old_version];new=self.versions.require_current(new_version)
        if new.predecessor!=old_version or new.node_id!=old.node_id:raise ValueError('Broken supersession lineage')
        # A second reviewed correction may arrive before the first rework.
        # Active consumers can still bind an earlier immutable predecessor.
        # Traverse only those actually consumed replaced versions.
        lineage={old_version};previous=old.predecessor
        while previous:
            lineage.add(previous);previous=self.versions.versions[previous].predecessor
        direct=[];affected=set();causes=[];queue=sorted(lineage)
        while queue:
            upstream=queue.pop(0)
            for node_id in sorted(self.versions.active):
                current=self.versions.current(node_id,allow_stale=True)
                if current is None or node_id in affected:continue
                matches=[edge for edge,bound in current.dependency_bindings if bound==upstream]
                if not matches:continue
                if upstream in lineage:direct.append(node_id)
                affected.add(node_id);queue.append(current.version_id)
                for edge in matches:
                    self.versions.mark_stale(current.version_id,edge,upstream);causes.append(dict(node=node_id,dependency=edge,upstream_version=upstream))
                node=self.graph.nodes[node_id];node.rework_triggered=True;node.challenge_triggered=True;node.status='stale'
                node.execution_receipt['currentness']='STALE'
                self.cases.get(node.case_id).challenge_results.append(dict(kind='dependency-rework',causes=[c for c in causes if c['node']==node_id]))
                self.graph.history.append(dict(node=node_id,event='version-invalidation',upstream=upstream,dependencies=matches))
        order=self.topological(affected)
        plan=dict(changed_upstream=old.node_id,old_version=old_version,new_version=new_version,direct=sorted(set(direct)),transitive=sorted(affected-set(direct)),unaffected=sorted(set(self.graph.nodes)-affected-{old.node_id}),execution_order=order,affected_cases=sorted({self.graph.nodes[n].case_id for n in affected}),affected_periods=sorted({self.graph.nodes[n].period_id for n in affected}),causes=causes)
        self.rework_history.append(plan);self.cases.refresh(self.graph,self.versions,self.edges)
        return plan

    def topological(self,selected):
        remaining=set(selected);order=[]
        while remaining:
            ready=sorted(n for n in remaining if not set(self.graph.nodes[n].dependencies)&remaining)
            if not ready:raise ValueError('Dependency cycle')
            order.extend(ready);remaining-=set(ready)
        return order

    def reexecute(self,plan,executors,sources):
        if not self.rework_history or plan!=self.rework_history[-1]:raise ValueError('Current exact rework plan required')
        stale={n for n in self.graph.nodes if (v:=self.versions.current(n,allow_stale=True)) is not None and self.versions.state(v.version_id)=='STALE'}
        if set(plan['execution_order'])!=stale or plan['execution_order']!=self.topological(stale):raise ValueError('Unnecessary rerun or invalid rework order')
        ledger=[]
        for node in plan['execution_order']:
            old=self.versions.current(node,allow_stale=True)
            new=self.execute(node,executors[node],sources[node],'Dependency rework: '+plan['new_version'])
            ledger.append(dict(node=node,old_version=old.version_id,new_version=new.version_id))
        for case_id in plan['affected_cases']:
            case=self.cases.get(case_id)
            if case.outcome!='complete':continue
            for node_id in case.node_refs:
                node=self.graph.nodes[node_id]
                if node.required:self.versions.require_current(self.versions.current(node_id).version_id)
                for receipt in [self.receipt(k) for k,e in self.edges.items() if e.consumer_node==node_id]:self.validate_receipt(receipt,node_id)
            case.challenge_results.append(dict(kind='selective-rework-currentness',status='PASS',upstream=plan['new_version'],reexecuted=[r for r in ledger if self.graph.nodes[r['node']].case_id==case_id]))
            case.rework_state=dict(status='CURRENT',upstream=plan['new_version'])
            if case.status=='IN_PROGRESS':
                for status in ('CHALLENGE','CONCLUDED','DOCUMENTED'):case.transition(status)
                if case.observer_ran and case.artifacts:case.transition('CLOSED')
        return ledger

    def current_payloads(self):
        return {n:self.versions.require_current(self.versions.current(n).version_id).payload() for n in sorted(self.versions.active)}

    def current_journals(self,context,events):
        """Only exact current result versions may contribute posting economics.

        Opening/comparative observations are lineage, not owner postings. Event
        declarations remain reviewed input; supersession creates no reversal.
        """
        from .scoped_journals import allocate_scoped
        native=[]
        for key in sorted(self.versions.active):
            version=self.versions.current(key)
            node=self.graph.nodes[key]; payload=version.payload()
            journals=payload.get('journal_entry_implications',[])
            if not journals:continue
            if node.economic_id is not None and node.selected_skill=='foreign-currency' and self.sources[node.id].get('translation',{}).get('enabled'):
                raise ValueError('Translation implications require explicit reporting-layer disposition, never legal posting')
            if node.selected_skill=='intercompany-accounting' and any(entity!=node.scope_id for entity in payload.get('calculations',{}).get('journal_entities',[])):
                raise ValueError('IC journals belong to distinct legal books; qualified per-book owner required')
            native.append(dict(economic_id=node.economic_id,owner=node.selected_skill,node=node.id,source_scope=node.scope_id,posting_scope=node.scope_id,accounting_layer=node.scope_type,currency=node.functional_currency or node.presentation_currency,period=node.period,period_id=node.period_id,result_version=version.version_id,journals=journals))
        for event in events:
            if event.get('result_version') is None:raise ValueError('Exact current journal result version required')
            version=self.versions.require_current(event['result_version'])
            if (version.scope_id,version.period_id)!=(event.get('posting_scope'),event.get('period_id')):raise ValueError('Journal Scope/Period relabelled')
            refs=event['primary']+[r for witness in event['witnesses'] for r in witness]
            if any(r['owner']!=version.node_id for r in refs):raise ValueError('Journal references wrong version producing node')
        return allocate_scoped(native,context,events)
