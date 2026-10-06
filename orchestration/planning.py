"""Bounded issue interpreter; future semantic planners implement Planner.identify.

These are supported fact adapters, not a second skill taxonomy. Owners and their
status/contracts are always resolved against Registry. Objective words determine
requested scope; supplied economic facts determine applicable issues.
"""
from dataclasses import dataclass, field, asdict
from typing import Protocol
from .intent import interpret

# Fact families map to existing bounded owner contracts. Other families remain
# visible open questions until an adapter is implemented; never guessed routes.
FACT_ADAPTERS = {
    'debt_population': ('debt-financing', ('debt',)),
    'cash_activity': ('cash-flow-reporting', ('transactions', 'cash_accounts')),
    'receivable_population': ('accounts-receivable', ('invoices',)),
    'credit_exposure': ('financial-instruments-ecl', ('instrument',)),
    'inventory': ('inventory-cost', ('items', 'movements')),
    'machinery': ('fixed-assets', ('assets',)),
    'employee_cost': ('employee-benefits-payroll', ('benefits',)),
    'supplier_cost': ('accounts-payable', ('invoices', 'accruals')),
    'currency_exposure': ('foreign-currency', ('items',)),
    'customer_contract': ('revenue-recognition', ('obligations',)),
    'obligation': ('provisions-contingencies', ('obligation',)),
    'grant': ('government-grants', ('agreement',)),
    'qualifying_interest': ('borrowing-costs', ('project',)),
    'rental_investment': ('investment-property', ('property',)),
    'biological_population': ('agriculture-biological-assets', ('assets',)),
    'derivative_contract': ('derivatives-hedge-accounting', ('contracts',)),
    'insurance_contract': ('insurance-contracts-accounting', ('contracts',)),
    'lease_contract': ('lease-accounting', ('contract_facts',)),
    'reconciliation': ('balance-sheet-reconciliations', ('reconciliations',)),
    'close_calendar': ('month-end-close', ('tasks',)),
    'interface': ('accounting-systems-data-integrity', ('interfaces',)),
    'control': ('accounting-controls-icfr', ('control_rows',)),
    'statement': ('financial-statements', ('current_tb',)),
    'disclosure': ('disclosure-management', ('requirements',)),
    'analytics': ('management-accounting-analytics', ('accounts',)),
    'acquisition': ('business-combinations', ('acquisition',)),
    'group_structure': ('consolidation', ('entities',)),
    'intercompany': ('intercompany-accounting', ('pairs',)),
    'foreign_operation': ('foreign-currency', ('translation',)),
    'impairment_valuation': ('asset-impairment', ('unit',)),
    'tax_temporary_difference': ('income-taxes', ('jurisdictions',)),
}

@dataclass
class Issue:
    id: str
    capability: str
    owner: str
    reason: str
    source_inputs: list = field(default_factory=list)
    dependencies: list = field(default_factory=list)
    required: bool = True
    material: object = None
    considerations: list = field(default_factory=list)
    condition: object = None
    scope_id: str | None = None
    period_id: str | None = None


class Planner(Protocol):
    def interpret(self, objective, facts, context, registry): ...
    def identify(self, objective, facts, context, registry) -> list[Issue]: ...


class DeterministicPlanner:
    """Evidence-led bounded interpretation, no external LLM/network dependency."""
    def interpret(self, objective, facts, context, registry):
        return interpret(objective).validate()

    def identify(self, objective, facts, context, registry):
        intent = self.interpret(objective, facts, context, registry)
        objective = objective.lower()
        # Bounded balance inquiry scales to one owner. No broad task default for
        # unsupported prose: the runtime exposes the missing decomposition.
        simple_ap = 'ap' in objective.split() and 'balance' in objective and not any(
            word in objective for word in ('review', 'year-end', 'margin', 'close'))
        simple_ap = bool(intent.bounded_owner)
        families = [k for k,v in FACT_ADAPTERS.items() if v[0] == intent.bounded_owner] if simple_ap else list(facts)
        if not intent.bounded_owner:
            if intent.primary=='ACCOUNTING_DETERMINATION' and 'how' in objective:
                families=[k for k in families if k not in {'analytics','statement','disclosure','close_calendar','reconciliation','interface','control','task_attributes'}]
            elif intent.primary=='PROCESS_CONTROL_REVIEW':
                families=[k for k in families if k in {'close_calendar','interface','control','task_attributes'}]
            elif intent.primary=='DOCUMENTATION':
                families=[k for k in families if k not in {'analytics','statement','disclosure','close_calendar','reconciliation','interface','control','task_attributes'}]
        issues = []
        for family in families:
            if family not in FACT_ADAPTERS: continue
            owner, populations = FACT_ADAPTERS[family]
            values=facts.get(family)
            for supplied in values if isinstance(values,list) else [values]:
                if not isinstance(supplied,dict): continue
                if not any(supplied.get(k) for k in populations): continue
                scope_id=supplied.get('scope_id',supplied.get('entity'))
                period_id=supplied.get('period_id')
                suffix=':'+str(scope_id)+((':'+str(period_id)) if period_id is not None else '')
                issue=Issue(owner+suffix if isinstance(values,list) else owner, family, owner,
                    'Supplied '+family.replace('_',' ')+' population affects requested accounting work',
                    [family], required=supplied.get('required_for_objective',True),
                    material=supplied.get('material'), scope_id=scope_id)
                issue.period_id=period_id
                issues.append(issue)
        # Cross-cutting architecture rules produce actual graph nodes when the
        # task attributes call for them, even if their workpapers are missing.
        rules = {
            'significant_judgment': [('accounting-policy-memo-governance','technical documentation'),
                ('accounting-controls-icfr','controls'), ('audit-support-pbc','audit evidence')],
            'recurring_process': [('month-end-close','accounting operations'),
                ('accounting-controls-icfr','controls'), ('accounting-systems-data-integrity','systems and automation')],
            'material_balance': [('balance-sheet-reconciliations','reconciliation'),
                ('financial-statements','financial reporting'), ('disclosure-management','disclosure')],
            'new_process': [('accounting-policy-memo-governance','policy'),
                ('accounting-operating-model','process owner reviewer'),
                ('accounting-systems-data-integrity','system'), ('accounting-controls-icfr','control evidence')],
            'recurring_manual_cross_system_reconciliation': [('accounting-systems-data-integrity','automation and data workflow')],
        }
        if not simple_ap:
            for attribute, owners in rules.items():
                if intent.primary in ('PROCESS_CONTROL_REVIEW','DOCUMENTATION') and attribute=='material_balance':continue
                if intent.primary=='ACCOUNTING_DETERMINATION' and 'how' in objective and attribute!='significant_judgment':continue
                if facts.get('task_attributes', {}).get(attribute) is True:
                    for owner, capability in owners:
                        found = next((i for i in issues if i.owner == owner), None)
                        if found: found.considerations.append(capability)
                        else: issues.append(Issue(owner, capability, owner, attribute+' requires '+capability))
        if not intent.bounded_owner:
            required_modes = {'DIAGNOSTIC_ANALYTICS': [('management-accounting-analytics','requested diagnostic investigation')], 'DOCUMENTATION': [('accounting-policy-memo-governance','requested accounting memo')],
                'PROCESS_CONTROL_REVIEW': [('accounting-systems-data-integrity','requested process/data review'), ('accounting-controls-icfr','requested control review')]}
            for owner, reason in required_modes.get(intent.primary, []):
                if not any(i.owner==owner for i in issues):issues.append(Issue(owner, reason, owner, reason))
        # Imports are addressed by exact owner + Scope + governed Period. A
        # package alias is retained only for a unique legacy execution.
        def source_for(issue):
            rows=[v for k in issue.source_inputs for v in (facts[k] if isinstance(facts[k],list) else [facts[k]])
                  if v.get('scope_id',v.get('entity'))==issue.scope_id and v.get('period_id')==issue.period_id]
            if len(rows)>1:raise ValueError('Ambiguous exact issue source')
            return rows[0] if rows else {}
        queue=[(i,source_for(i)) for i in issues];inspected=set()
        for issue,supplied in queue:
            identity=(issue.owner,issue.scope_id,issue.period_id)
            if identity in inspected:continue
            inspected.add(identity)
            for imp in supplied.get('imports',[]):
                upstream=imp.get('package');actual=imp.get('case')
                if not isinstance(upstream,str) or not upstream or not isinstance(actual,dict):raise ValueError('Actual imported owner case required')
                scope=actual.get('scope_id',actual.get('entity'));period=actual.get('period_id')
                matches=[i for i in issues if (i.owner,i.scope_id,i.period_id)==(upstream,scope,period)]
                if len(matches)>1:raise ValueError('Ambiguous imported execution')
                if matches:dep=matches[0]
                else:
                    repeated=any(i.owner==upstream for i in issues)
                    key=upstream+':'+str(scope)+':'+str(period) if repeated or period else upstream
                    dep=Issue(key,'owner dependency',upstream,'Actual supplied accounting workpaper requires this owner result',scope_id=scope,period_id=period)
                    issues.append(dep)
                if dep.id not in issue.dependencies:issue.dependencies.append(dep.id)
                queue.append((dep,actual))
        return issues


@dataclass
class Node:
    id: str
    issue: str
    selected_skill: str
    reason_selected: str
    entity: str
    framework: str
    period: list
    prerequisites: list = field(default_factory=list)
    dependencies: list = field(default_factory=list)
    source_inputs: list = field(default_factory=list)
    owner_result_dependencies: list = field(default_factory=list)
    status: str = 'pending'
    result: object = None
    open_items: list = field(default_factory=list)
    evidence: list = field(default_factory=list)
    downstream_consumers: list = field(default_factory=list)
    rework_triggered: bool = False
    challenge_triggered: bool = False
    iterations: int = 0
    invalidated_results: list = field(default_factory=list)
    period_id: str = ''
    case_id: str = ''
    logical_id: str = ''
    economic_id: str | None = None
    scope_id: str = ''
    scope_type: str = ''
    jurisdiction: str = ''
    functional_currency: str | None = None
    presentation_currency: str | None = None
    execution_receipt: dict = field(default_factory=dict)
    required: bool = True
    material: object = None
    condition: object = None


def node_record(node):
    row=asdict(node)
    if row.get('economic_id') is None:row.pop('economic_id',None)
    return row


class Graph:
    def __init__(self):
        from .execution import NodeTable
        self.nodes = NodeTable(); self.history = []
    def add(self, node):
        if node.id in self.nodes: raise ValueError('Duplicate workplan node')
        self.nodes[node.id] = node
    def validate(self):
        for n in self.nodes.values():
            n.dependencies=[self.nodes.resolve(d) for d in n.dependencies]
            if len(set(n.dependencies)) != len(n.dependencies): raise ValueError('Duplicate dependency')
            if any(d not in self.nodes for d in n.dependencies): raise ValueError('Unknown dependency')
        active = set(); visited = set()
        def walk(id):
            if id in active: raise ValueError('Dependency cycle')
            if id in visited: return
            active.add(id)
            for dep in self.nodes[id].dependencies: walk(dep)
            active.remove(id); visited.add(id)
        for id in self.nodes: walk(id)
        for n in self.nodes.values():
            n.downstream_consumers = [x.id for x in self.nodes.values() if n.id in x.dependencies]
    def ready(self):
        return [n for n in self.nodes.values() if n.status == 'pending' and all(
            self.nodes[d].status in ('complete', 'not_applicable') for d in n.dependencies)]
    def invalidate(self, id, reason):
        n = self.nodes[id]
        if n.result is not None: n.invalidated_results.append(n.result)
        n.status = 'blocked'; n.result = None
        n.rework_triggered = n.challenge_triggered = True
        if reason not in n.open_items: n.open_items.append(reason)
        self.history.append(dict(node=id, event='invalidate', reason=reason))
        for child in n.downstream_consumers:
            if self.nodes[child].status != 'blocked': self.invalidate(child, 'Upstream challenged: '+n.selected_skill+' ('+n.scope_id+')')
    def reopen(self, id):
        n = self.nodes[id]; n.status='pending'; n.result=None; n.open_items=[]; n.rework_triggered=True
        self.history.append(dict(node=id, event='reopen'))
        for child in n.downstream_consumers: self.reopen(child)
    def record(self): return [node_record(n) for n in self.nodes.values()]
