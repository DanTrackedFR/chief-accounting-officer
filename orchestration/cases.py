"""Independent governed work containers composed with the existing runtime Case."""
from dataclasses import asdict
from .periods import identity

TYPES={'LEGAL_ENTITY':'ENTITY_CASE','SUBGROUP':'SUBGROUP_CASE','GROUP':'GROUP_CASE'}


def case_identity(scope_id,period_id,objective,cycle):
    if any(not isinstance(v,str) or not v.strip() for v in (scope_id,period_id,objective,cycle)): raise ValueError('Explicit Case objective/cycle/dimensions required')
    return identity('case',[scope_id,period_id,objective,cycle])


class CaseRegistry:
    def __init__(self,scopes,periods): self.scopes=scopes;self.periods=periods;self.cases={}

    def register(self,case,scope_id,period_id,cycle,parent_id=None,provenance=()):
        scope=self.scopes.get(scope_id); period=self.periods.get(period_id)
        if scope.reporting_calendar and scope.reporting_calendar!=period.calendar_id:raise ValueError('Wrong Case fiscal calendar')
        expected=case_identity(scope_id,period_id,case.objective,cycle)
        if case.id!=expected or case.id in self.cases or not provenance: raise ValueError('Duplicate/substituted/unqualified Case identity')
        if parent_id is not None:
            parent=self.get(parent_id)
            if parent.case_type=='ENTITY_CASE' or scope.scope_type=='GROUP': raise ValueError('Illegal Case parent type')
        case.scope_id=scope_id;case.period_id=period_id;case.case_type=TYPES[scope.scope_type];case.cycle=cycle
        case.parent_case_id=parent_id;case.provenance=list(provenance)
        self.cases[case.id]=case
        if parent_id is not None: self.get(parent_id).child_case_ids.append(case.id)
        return case

    def get(self,key):
        if key not in self.cases: raise ValueError('Unknown governed Case')
        return self.cases[key]

    def bind_node(self,case_id,node):
        case=self.get(case_id)
        if (node.scope_id,node.period_id,node.case_id)!=(case.scope_id,case.period_id,case.id): raise ValueError('Case node Scope/Period contamination')
        if node.id not in case.node_refs:case.node_refs.append(node.id)

    def qualify_consumption(self,edge,producer,consumer):
        source=self.get(producer.case_id);target=self.get(consumer.case_id)
        if edge.producer_case!=source.id or edge.consumer_case!=target.id: raise ValueError('Wrong Case dependency')
        if source.id!=target.id and edge.consumption not in ('DECLARED_CHILD','EXPLICIT_CROSS_CASE'): raise ValueError('Undeclared child result')
        if edge.consumption=='DECLARED_CHILD' and source.parent_case_id!=target.id: raise ValueError('Wrong parent Case')
        # Neither organizational parentage nor Case parentage supplies an edge.
        return True

    def refresh(self,graph,versions,edges):
        for case in self.cases.values():
            required=[graph.nodes[k] for k in case.node_refs if graph.nodes[k].required or graph.nodes[k].material is not False]
            unresolved=[]
            for node in required:
                if node.status=='not_applicable':continue
                current=versions.current(node.id,allow_stale=True)
                if node.status!='complete' or current is None or versions.state(current.version_id)!='CURRENT':unresolved.append(node.id)
                if current is not None and current.payload().get('unresolved_dependencies'):unresolved.append(node.id)
                for edge in edges.values():
                    if edge.consumer_node==node.id and edge.required:
                        producer=versions.current(edge.producer_node,allow_stale=True)
                        if producer is None or versions.state(producer.version_id)!='CURRENT' or graph.nodes[edge.producer_node].status!='complete':unresolved.append(edge.producer_node)
            outcome='partial' if unresolved else 'complete' if required else 'blocked'
            if outcome!=case.outcome:
                case.governance_history.append(dict(previous_status=case.status,previous_outcome=case.outcome,result_versions=list(case.result_version_refs),reason='Required dependency currentness changed'))
                case.outcome=outcome
                if unresolved and case.status in ('CLOSED','DOCUMENTED','CONCLUDED'):
                    case.status='IN_PROGRESS';case.transitions.append('REWORK');case.rework_state=dict(required_nodes=sorted(set(unresolved)))
            case.result_version_refs=[v.version_id for n in case.node_refs if (v:=versions.current(n,allow_stale=True)) is not None]
            case.workplan_nodes=[asdict(graph.nodes[k]) for k in sorted(case.node_refs)]

    def record(self):return [asdict(self.cases[k]) for k in sorted(self.cases)]
