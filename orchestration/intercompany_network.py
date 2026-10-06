"""Governed relationship graph; never an execution engine or accounting owner.

Explicit commercial IDs identify transactions. Every side retains its own legal
book/result version. Only Stage 2 Dependency objects establish execution edges.
"""
import copy
from dataclasses import dataclass, asdict
from decimal import Decimal, InvalidOperation
from .periods import identity
from .versions import fingerprint

RESIDUALS = frozenset({'MATCHED', 'TIMING_DIFFERENCE', 'FX_DIFFERENCE',
    'CLASSIFICATION_DIFFERENCE', 'MISSING_COUNTERPARTY',
    'MISSING_SOURCE_EVIDENCE', 'UNRESOLVED_MISMATCH'})


def amount(value):
    if not isinstance(value, str):
        raise ValueError('Exact decimal string required')
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError('Invalid amount') from exc
    if not result.is_finite() or result < 0:
        raise ValueError('Finite nonnegative amount required')
    return result


@dataclass(frozen=True)
class TransactionSide:
    network_id: str
    agreement_id: str
    economic_id: str
    book_entry_id: str
    scope_id: str
    counterparty_scope: str
    case_id: str
    period_id: str
    owner_node: str
    result_version: str
    metric_path: tuple
    transaction_class: str
    role: str
    functional_currency: str
    functional_amount: str
    transaction_currency: str
    transaction_amount: str
    source_id: str
    source_path: tuple
    source_fingerprint: str
    evidence: tuple
    counterparty_case: str | None = None
    counterparty_period: str | None = None

    @property
    def relationship_id(self):
        return identity('ic-relationship', [self.network_id, self.agreement_id,
            self.economic_id, sorted([self.scope_id, self.counterparty_scope])])

    @property
    def side_id(self):
        return identity('ic-side', [self.relationship_id, self.scope_id, self.book_entry_id])

    def validate(self, session):
        from .runtime import at
        for key in ('network_id', 'agreement_id', 'economic_id', 'book_entry_id',
                    'scope_id', 'counterparty_scope', 'source_id', 'transaction_class'):
            if not isinstance(getattr(self, key), str) or not getattr(self, key).strip():
                raise ValueError('Explicit commercial/book/source identity required')
        scopes = session.cases.scopes
        origin = scopes.get(self.scope_id)
        counterparty = scopes.get(self.counterparty_scope)
        if origin.scope_type != 'LEGAL_ENTITY' or counterparty.scope_type != 'LEGAL_ENTITY':
            raise ValueError('Both counterparties must be governed legal entities')
        if self.scope_id == self.counterparty_scope:
            raise ValueError('Self-counterparty has no supported native contract')
        if not self.evidence or not self.metric_path or not self.source_path:
            raise ValueError('Exact result/source evidence required')
        if self.role not in ('receivable', 'payable', 'income', 'expense'):
            raise ValueError('Explicit supported legal-side role required')
        version = session.versions.require_current(self.result_version)
        node = session.graph.nodes[self.owner_node]
        if (version.node_id, version.case_id, version.scope_id, version.period_id) != (
                self.owner_node, self.case_id, self.scope_id, self.period_id):
            raise ValueError('Legal side result dimensional substitution')
        if node.status != 'complete' or node.scope_type != 'LEGAL_ENTITY':
            raise ValueError('Current legal producing node required')
        if self.functional_currency != origin.functional_currency:
            raise ValueError('Functional currency differs from governed Scope')
        for cur in (self.functional_currency, self.transaction_currency):
            if not isinstance(cur, str) or len(cur) != 3 or not cur.isupper():
                raise ValueError('Explicit currency identity required')
        if amount(str(at(version.payload(), self.metric_path))) != amount(self.functional_amount):
            raise ValueError('Legal amount must equal exact owner result metric')
        amount(self.transaction_amount)
        source = session.sources[self.owner_node]
        if fingerprint(source) != version.source_fingerprint:
            raise ValueError('Source no longer belongs to exact result version')
        actual = at(source, self.source_path)
        expected = dict(source_id=self.source_id, economic_id=self.economic_id,
            book_entry_id=self.book_entry_id, agreement_id=self.agreement_id,
            network_id=self.network_id, scope_id=self.scope_id,
            counterparty_scope=self.counterparty_scope, period_id=self.period_id,
            transaction_class=self.transaction_class, role=self.role,
            functional_currency=self.functional_currency,
            functional_amount=self.functional_amount, transaction_currency=self.transaction_currency,
            transaction_amount=self.transaction_amount)
        if actual != expected or fingerprint(actual) != self.source_fingerprint:
            raise ValueError('Source row/economic identity differs from reviewed native input')
        if node.selected_skill != 'intercompany-accounting' or len(self.metric_path)!=4 or tuple(self.metric_path[:2])!=('calculations','pairs') or self.metric_path[3] not in ('a_functional','b_functional'):
            raise ValueError('Unsupported transaction-owner semantic mapping; dependency unresolved')
        index=self.metric_path[2]
        if type(index) is not int:
            raise ValueError('Exact native transaction row required')
        pair=source['pairs'][index];calculation=version.payload()['calculations']['pairs'][index]
        native_side='a' if self.metric_path[3]=='a_functional' else 'b'
        other='b' if native_side=='a' else 'a'
        if (pair['entity_'+native_side],pair['entity_'+other],pair['currency'],pair['transaction_id'],pair['id'])!=(self.scope_id,self.counterparty_scope,self.transaction_currency,self.economic_id,calculation['pair']):
            raise ValueError('Native legal transaction/counterparty identity differs')
        if self.role!=('receivable' if native_side=='a' else 'payable') or self.transaction_class!='loan':
            raise ValueError('Unsupported native IC side/classification')
        if amount(str(calculation['foreign_principal']))!=amount(self.transaction_amount):
            raise ValueError('Transaction principal metadata differs from native owner result')
        if (self.counterparty_case is None) != (self.counterparty_period is None):
            raise ValueError('Counterparty Case and Period must be supplied together')
        if self.counterparty_case is not None:
            c = session.cases.get(self.counterparty_case)
            if (c.scope_id, c.period_id) != (self.counterparty_scope, self.counterparty_period):
                raise ValueError('Counterparty Case/Period substitution')
        return self


@dataclass(frozen=True)
class MatchingDecision:
    relationship_id: str
    side_ids: tuple
    classification: str
    evidence: tuple
    result_versions: tuple
    reviewer: str
    reason: str
    period_alignment: tuple = ()

    def validate(self, sides):
        if self.classification not in RESIDUALS or not self.evidence or not self.reviewer or not self.reason:
            raise ValueError('Explicit reviewed residual classification required')
        if set(self.side_ids) != {s.side_id for s in sides} or len(self.side_ids) != len(sides):
            raise ValueError('Decision side population differs')
        if tuple(sorted(self.result_versions)) != tuple(sorted(s.result_version for s in sides)):
            raise ValueError('Residual disposition belongs to different result versions')
        if any(s.relationship_id != self.relationship_id for s in sides):
            raise ValueError('Decision relationship differs')
        if len(sides) == 1:
            if self.classification not in ('MISSING_COUNTERPARTY', 'MISSING_SOURCE_EVIDENCE', 'UNRESOLVED_MISMATCH'):
                raise ValueError('Missing bilateral side cannot be matched')
            return
        if len(sides) != 2:
            raise ValueError('Bilateral decision requires exactly two legal sides')
        a, b = sides
        if (a.scope_id, a.counterparty_scope) != (b.counterparty_scope, b.scope_id):
            raise ValueError('Nonreciprocal counterparties')
        if (a.counterparty_case is not None and (a.counterparty_case, a.counterparty_period) != (b.case_id, b.period_id)) or (b.counterparty_case is not None and (b.counterparty_case, b.counterparty_period) != (a.case_id, a.period_id)):
            raise ValueError('Explicit reciprocal Case/Period differs')
        if self.classification == 'MATCHED':
            if {a.role, b.role} not in ({'receivable', 'payable'}, {'income', 'expense'}):
                raise ValueError('Matched sides need reciprocal accounting roles')
            if a.transaction_class != b.transaction_class or a.transaction_currency != b.transaction_currency or amount(a.transaction_amount) != amount(b.transaction_amount):
                raise ValueError('Mismatch cannot be forced to MATCHED')
            if a.period_id != b.period_id and not self.period_alignment:
                raise ValueError('Cross-period match requires explicit timing/alignment disposition')
            if a.functional_currency == b.functional_currency and amount(a.functional_amount) != amount(b.functional_amount):
                raise ValueError('Unexplained functional amount difference')
        # Other classifications are reviewed evidence, never guessed corrections.


class IntercompanyNetwork:
    def __init__(self, session, network_id):
        if not isinstance(network_id, str) or not network_id.strip():
            raise ValueError('Explicit network identity required')
        self.session = session
        self.network_id = network_id
        self.sides = {}
        self.decisions = {}
        self.history = []

    def register(self, side):
        side.validate(self.session)
        if side.network_id != self.network_id:
            raise ValueError('Wrong network')
        # An alias in agreement/economic ID cannot reuse an existing book event.
        if any((s.scope_id, s.period_id, s.book_entry_id) == (side.scope_id, side.period_id, side.book_entry_id)
               for s in self.sides.values()):
            raise ValueError('Duplicate legal book event or alias')
        if side.side_id in self.sides:
            raise ValueError('Duplicate legal side')
        self.sides[side.side_id] = side
        return side.side_id

    def match(self, decision):
        if len(set(decision.side_ids)) != len(decision.side_ids):
            raise ValueError('Repeated matching side')
        sides = [self.sides[key].validate(self.session) for key in decision.side_ids]
        decision.validate(sides)
        if decision.classification == 'MATCHED' and len(sides) == 2:
            periods=[self.session.periods.get(s.period_id) for s in sides]
            if (periods[0].start,periods[0].end)!=(periods[1].start,periods[1].end):
                raise ValueError('Different dated Periods require timing disposition')
        if any(key in d.side_ids for key in decision.side_ids for d in self.decisions.values()):
            raise ValueError('Legal side already consumed by a match')
        self.decisions[decision.relationship_id] = decision
        result = self.result(decision.relationship_id)
        self.history.append(copy.deepcopy(result))
        return result

    def result(self, relationship_id):
        decision = self.decisions[relationship_id]
        sides = [self.sides[k].validate(self.session) for k in decision.side_ids]
        decision.validate(sides)
        residual = None
        if len(sides) == 2 and sides[0].functional_currency == sides[1].functional_currency:
            residual = str(amount(sides[0].functional_amount) - amount(sides[1].functional_amount))
        transaction_residual=None
        if len(sides)==2 and sides[0].transaction_currency==sides[1].transaction_currency:
            transaction_residual=str(amount(sides[0].transaction_amount)-amount(sides[1].transaction_amount))
        return dict(transaction_residual=transaction_residual,transaction_residual_currency=sides[0].transaction_currency if transaction_residual is not None else None,relationship_id=relationship_id, network_id=self.network_id,
            classification=decision.classification, sides=[asdict(s) | {'side_id': s.side_id} for s in sides],
            functional_residual=residual, residual_currency=sides[0].functional_currency if residual is not None else None,
            correction=None, accounting_authority=False, evidence=list(decision.evidence),
            result_versions=sorted(decision.result_versions))

    def relationships(self):
        return sorted({(s.scope_id, s.counterparty_scope) for s in self.sides.values()})

    def has_business_cycle(self):
        adjacency = {}
        for a, b in self.relationships():
            adjacency.setdefault(a, set()).add(b)
        def walk(node, path):
            if node in path:
                return True
            return any(walk(child, path | {node}) for child in adjacency.get(node, ()))
        return any(walk(node, set()) for node in adjacency)

    def record(self):
        return dict(network_id=self.network_id, sides=[asdict(self.sides[k]) | {'side_id': k} for k in sorted(self.sides)],
            decisions=[asdict(self.decisions[k]) for k in sorted(self.decisions)],
            business_edges=self.relationships(), business_cycle=self.has_business_cycle(),
            execution_edges_inferred=False)
