"""Deterministic controlled SaaS source-to-public-result reference artifacts."""
import copy
import json
from dataclasses import asdict
from decimal import Decimal
from pathlib import Path
from orchestration.tests.saas_fixtures import flagship, sources
from orchestration.tests.generate_examples import internal_record

ROOT = Path(__file__).resolve().parents[2]


def artifacts():
    engine, prepared, pack = flagship()
    result = engine.execute(prepared, pack)
    case = result.case
    assert case.outcome == 'partial' and case.journal_mapping_valid
    owners = {n['selected_skill']: n for n in case.workplan_nodes if n['status'] == 'complete'}
    balances = case.balance_diagnostics
    lineage = []
    for fact, package, path, downstream, metric, amount in [
        ('rev-progress', 'revenue-recognition', ['period_revenue'], 'financial-statements', 'revenue', '500'),
        ('ar-applied', 'accounts-receivable', ['closing_ar'], 'financial-statements', 'ar_balance', '1520'),
        ('rev-billings', 'revenue-recognition', ['contract_bridge', 'closing'], 'balance-sheet-reconciliations', 'contract_balance', '-1300'),
    ]:
        source = next(r for r in result.lineage if r['fact_id'] == fact)
        value = owners[package]['result']['calculations']
        for key in path:
            value = value[key]
        assert Decimal(value) == Decimal(amount)
        handoff = next(r for r in case.handoff_ledger if r['producer'] == package and r['consumer'] == downstream and r['semantic'] == metric)
        lineage.append(dict(source_fact=source, accounting_owner=package, owner_result_path=path,
                            owner_result_amount=str(value), downstream_handoff=handoff,
                            analytical_result=copy.deepcopy(balances), final_public_amount=str(value)))
    rec = owners['balance-sheet-reconciliations']['result']['calculations']
    out = {
        'raw-source-pack.json': [asdict(s) for s in sources()],
        'source-inventory.json': [{k: v for k, v in r.items() if k != 'fields'} for r in result.inventory],
        'extraction-ledger.json': [v for r in result.inventory for v in r['fields'].values()],
        'transformation-ledger.json': result.transformations,
        'semantic-proposal.json': result.proposal,
        'work-modes.json': case.work_modes,
        'fact-candidates.json': result.candidates,
        'conflict-register.json': result.conflicts,
        'material-questions.json': result.questions,
        'owner-input-candidates.json': result.owner_inputs,
        'source-owner-bindings.json': [asdict(b) for b in pack.bindings],
        'source-population-bindings.json': [asdict(b) for b in pack.populations],
        'issue-register.json': case.accounting_issues,
        'workplan-graph.json': [{k: v for k, v in n.items() if k not in ('result', 'evidence', 'invalidated_results')} for n in case.workplan_nodes],
        'execution-ledger.json': case.execution_ledger,
        'owner-handoff-ledger.json': case.handoff_ledger,
        'journal-ownership-ledger.json': case.journal_ownership_ledger,
        'ar-bridge.json': balances['bridges']['ar'],
        'deferred-revenue-bridge.json': dict(opening='1000',billings='800',recognised='500',closing='1300',residual='0',formula='opening contract liability + contract billings - recognised revenue = closing contract liability',governed_signed_contract_net=balances['bridges']['contract_net']),
        'revenue-movement.json': balances['revenue'],
        'billings.json': balances['billings'],
        'cash-collections.json': balances['cash_collections'],
        'ageing-movement.json': balances['ageing'],
        'collection-dso-analysis.json': {k: balances[k] for k in ('collection_ratio', 'dso', 'management_hypothesis')},
        'ecl-movement.json': balances['bridges']['allowance'],
        'fx-bridge.json': owners['foreign-currency']['result']['calculations'],
        'close-exception-register.json': case.close_observations,
        'reconciliation-summary.json': dict(owner_results=rec, source_conflicts=result.conflicts,
                                            status='qualified workpapers reconcile; supplied summary contradictions remain open'),
        'reporting-disclosure.json': {p: owners[p]['result']['calculations'] for p in ('financial-statements', 'disclosure-management')},
        'analytics-result.json': balances,
        'accounting-escalation.json': case.accounting_questions,
        'challenge-result.json': case.challenge_results,
        'close-cleanliness.json': [dict(area='Governed recognition, receivable, allowance, FX and statement workpapers',classification='clean'),dict(area='Late manual accrual and authorized reclose',classification='explained exception'),dict(area='Allowance deterioration',classification='accounting effect',status='governed ECL determination complete'),dict(area='Ageing total and reconciliation/checklist contradiction',classification='data/control issue',status='open; obtain complete export and disposition'),dict(area='Lower absolute cash collection and older unpaid invoices',classification='economic deterioration',status='customer payment reasons unresolved')],
        'final-case.internal.json': internal_record(case),
        'final-public-answer.json': engine.public(result),
        'memory-candidates.json': result.memory_candidates + case.memory_candidates,
        'end-to-end-lineage.json': lineage,
        'management-hypothesis.json': result.hypothesis_results,
    }
    return out


def main():
    target = ROOT / 'orchestration/examples/saas-close'
    target.mkdir(exist_ok=True)
    for name, value in artifacts().items():
        (target / name).write_text(json.dumps(value, indent=2, sort_keys=True, default=str) + '\n')


if __name__ == '__main__':
    main()
