"""Version/currentness governance attached to the existing execution Graph.

This module schedules no accounting authority. Executors are provided by CAO and
must use its native production boundary, or an explicitly bounded observation.
"""
import copy
from dataclasses import dataclass, asdict
from .periods import identity


def fingerprint(value): return identity('fingerprint',value).split(':',1)[1]


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
    def __init__(self): self.versions={};self.states={};self.active={};self.supersession={};self.history=[]

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
        return self.versions[key]

    def publish(self,node,payload,source,bindings,reason):
        import json
        if not reason or not isinstance(payload,dict) or payload.get('status')!='complete':raise ValueError('Qualified complete result/version reason required')
        old=self.current(node.id,allow_stale=True)
        result_id=identity('result',[node.id,node.case_id,node.scope_id,node.period_id])
        source_hash=fingerprint(source);result_hash=fingerprint(payload)
        exact=payload.get('case_fingerprint')
        if not isinstance(exact,str) or not exact:raise ValueError('Exact-case fingerprint required')
        for edge,version in bindings:self.require_current(version)
        content=[result_id,old.version_id if old else None,exact,source_hash,result_hash,sorted(bindings),reason]
        key=identity('version',content)
        if key in self.versions:raise ValueError('Version overwrite')
        version=ResultVersion(result_id,key,node.id,node.case_id,node.scope_id,node.period_id,exact,source_hash,result_hash,old.version_id if old else None,reason,tuple(sorted(bindings)),json.dumps(payload,sort_keys=True,default=str,separators=(',',':')))
        self.versions[key]=version;self.states[key]='CURRENT';self.active[node.id]=key
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
        self.graph=graph;self.cases=cases;self.periods=periods;self.edges={};self.versions=VersionRegistry();self.receipts=[];self.rework_history=[]

    def add_dependency(self,edge):
        edge.validate(self.graph,self.cases,self.periods)
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
        if version is None or self.graph.nodes[edge.producer_node].status!='complete':raise ValueError('Required producer blocked/absent')
        from .runtime import at
        payload=version.payload(); value=at(payload,edge.metric_path)
        return dict(dependency_id=edge.id,result_version=version.version_id,producer_node=edge.producer_node,consumer_node=edge.consumer_node,producer_scope=edge.producer_scope,consumer_scope=edge.consumer_scope,producer_period=edge.producer_period,consumer_period=edge.consumer_period,currentness='CURRENT',result_fingerprint=version.result_fingerprint,value=copy.deepcopy(value))

    def validate_receipt(self,receipt,consumer_node):
        if not isinstance(receipt,dict) or receipt.get('dependency_id') not in self.edges:raise ValueError('Undeclared dependency receipt')
        edge=self.edges[receipt['dependency_id']]
        if edge.consumer_node!=consumer_node or receipt!=self.receipt(edge.id):raise ValueError('Wrong Scope/Period/version or stale receipt')
        return self.versions.require_current(receipt['result_version'])

    def execute(self,node_id,executor,source,reason):
        node=self.graph.nodes[node_id]
        self.cases.bind_node(node.case_id,node);self.periods.authorize_execution(node.period_id,node.case_id,node.id)
        receipts=[self.receipt(k) for k,e in sorted(self.edges.items()) if e.consumer_node==node.id]
        declared={self.edges[r['dependency_id']].producer_node for r in receipts}
        if set(node.dependencies)!=declared:raise ValueError('Workplan has unqualified dependencies')
        for receipt in receipts:self.validate_receipt(receipt,node.id)
        previous=self.versions.current(node.id,allow_stale=True)
        result=executor(node,copy.deepcopy(source),copy.deepcopy(receipts))
        version=self.versions.publish(node,result,source,[(r['dependency_id'],r['result_version']) for r in receipts],reason)
        node.result=version.payload();node.status='complete';node.iterations+=1;node.execution_receipt=dict(result_version=version.version_id,period_id=node.period_id,case_id=node.case_id,currentness='CURRENT')
        self.receipts.extend(copy.deepcopy(receipts))
        if previous:self.invalidate(previous.version_id,version.version_id)
        self.cases.refresh(self.graph,self.versions,self.edges)
        return version

    def invalidate(self,old_version,new_version):
        old=self.versions.versions[old_version];new=self.versions.require_current(new_version)
        if new.predecessor!=old_version or new.node_id!=old.node_id:raise ValueError('Broken supersession lineage')
        direct=[];affected=set();causes=[];queue=[old_version]
        while queue:
            upstream=queue.pop(0)
            for node_id in sorted(self.versions.active):
                current=self.versions.current(node_id,allow_stale=True)
                if current is None or node_id in affected:continue
                matches=[edge for edge,bound in current.dependency_bindings if bound==upstream]
                if not matches:continue
                if upstream==old_version:direct.append(node_id)
                affected.add(node_id);queue.append(current.version_id)
                for edge in matches:
                    self.versions.mark_stale(current.version_id,edge,upstream);causes.append(dict(node=node_id,dependency=edge,upstream_version=upstream))
                node=self.graph.nodes[node_id];node.rework_triggered=True;node.challenge_triggered=True;node.status='stale'
                node.execution_receipt['currentness']='STALE'
                self.cases.get(node.case_id).challenge_results.append(dict(kind='dependency-rework',causes=[c for c in causes if c['node']==node_id]))
                self.graph.history.append(dict(node=node_id,event='version-invalidation',upstream=upstream,dependencies=matches))
        order=self.topological(affected)
        plan=dict(changed_upstream=old.node_id,old_version=old_version,new_version=new_version,direct=sorted(direct),transitive=sorted(affected-set(direct)),unaffected=sorted(set(self.graph.nodes)-affected-{old.node_id}),execution_order=order,affected_cases=sorted({self.graph.nodes[n].case_id for n in affected}),affected_periods=sorted({self.graph.nodes[n].period_id for n in affected}),causes=causes)
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
        return ledger

    def current_payloads(self):
        return {n:self.versions.current(n).payload() for n in sorted(self.versions.active)}
