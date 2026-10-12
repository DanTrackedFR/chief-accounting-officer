"""Reproduce the unmodified native temporal refusal; never supply accounting."""
import hashlib
import json
from dataclasses import asdict
from pathlib import Path
from decimal import Decimal
from orchestration.tests import stage4_closing_population as whole
from orchestration.runtime import CAO

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / 'orchestration/examples/multi-entity-multi-period-temporal'
CONTRACTS = (
    'skills/financial-statements/methods.md', 'skills/financial-statements/workflow.py',
    'skills/accounting-changes/methods.md', 'skills/accounting-changes/workflow.py',
    'skills/equity-capital/methods.md', 'skills/cash-flow-reporting/methods.md',
    'skills/accounting-policy-memo-governance/methods.md',
    'orchestration/periods.py', 'orchestration/versions.py',
    'orchestration/temporal_inputs.py', 'orchestration/STAGE2-INTEGRATION-HANDOFF.md',
)


def artifacts():
    f, record = whole.run()
    e = f['session']; n = f['nodes']['reporting']
    source = whole.source(f, 'reporting')
    refusal = record['closing_rework']['native_refusal']
    if refusal['status'] != 'blocked' or 'Restated comparative equity differs from opening current equity' not in refusal['conclusion']:
        raise ValueError('Actual native temporal refusal must reproduce')
    if f['case'].outcome != 'partial' or f['case'].status == 'CLOSED':
        raise ValueError('Unsupported temporal evidence cannot earn closure')
    current = e.versions.current(f['nodes']['elimination'].id)
    comparative_equity = -sum(Decimal(x['balance']) for x in source['comparative_tb'] if x['category'] == 'equity')
    comparative_cash = sum(Decimal(x['balance']) for x in source['comparative_tb'] if x['cash_account'])
    opening_equity = sum(Decimal(x['opening']) + Decimal(x['retrospective_adjustments']) for x in source['equity_bridge'])
    opening_cash = Decimal(source['cash_flow']['opening'])
    producers = [dict(logical_id=e.graph.nodes[x.producer_node].logical_id, contract=asdict(x))
                 for x in e.edges.values() if x.consumer_node == n.id]
    return {
        'temporal-evidence-audit.json': dict(
            outcome='D', evidence_type='Inspection of retained synthetic source evidence; no new reviewed accounting evidence supplied',
            contract_hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in CONTRACTS},
            reporting_identity=dict(node=n.id,case=n.case_id,scope=n.scope_id,period=e.periods.get(n.period_id).record(),framework=n.framework,currency=n.presentation_currency),
            retained_comparative=dict(metadata=source['comparative'],tb=source['comparative_tb'],equity=str(comparative_equity),cash=str(comparative_cash),qualified_group_result_version=None),
            reviewed_current_opening=dict(parent_ledger=f['reviewed_parent_opening_ledger'],equity=str(opening_equity),cash=str(opening_cash),equity_bridge=source['equity_bridge'],cash_flow=source['cash_flow'],independently_qualified_opening_group_result_version=None),
            difference=dict(equity_opening_minus_comparative=str(opening_equity-comparative_equity),cash_opening_minus_comparative=str(opening_cash-comparative_cash),unit='EUR million'),
            incoming_reporting_dependencies=sorted(producers,key=lambda x:x['contract']['producer_node']),
            period_registry=e.periods.record(),
            native_refusal=refusal,current_group_result=asdict(current),
            preserved_original_versions={k:asdict(v) for k,v in record['before'].items()},
            current_version_states={k:dict(version=e.versions.current(v.id,allow_stale=True).version_id,state=e.versions.state(e.versions.current(v.id,allow_stale=True).version_id)) for k,v in sorted(f['nodes'].items())},
            existing_correction_rework=record['closing_correction'],
            new_temporal_result_versions=[],new_temporal_supersessions=[],new_temporal_invalidations=[],
            restatement='NOT ESTABLISHED; neither required nor ruled out by supplied history',
            bridge='NONE EVIDENCED',
            temporal_release_gaps=['TQA01: current reporting binds no separately governed Group comparative/opening result; recertified numeric substitutions are not a legitimate temporal chain'],
            temporal_positive_acceptance=False,
            missing_evidence=[
                'Complete reviewed Group comparative TB and original issued source/version at 2025-10-31',
                'Complete reviewed latest prior Group closing TB at 2026-09-30 and exact governed Period/calendar/Case/Scope/framework/currency',
                'Separately reviewed Group opening TB at 2026-10-01 with equity components and cash-account definitions/bank/GL history',
                'Intervening 2025 comparative to 2026 opening equity and cash movements, exact supported owner results/journals and source provenance',
                'If an error/policy transition is established: authorization/information chronology, original and corrected period inventories, balanced adjustments, materiality and Tax/EPS/underlying-owner handoffs',
                'Qualified native temporal result versions and explicit reporting-consumption mappings; equal values or observation-only loan30 are insufficient',
            ],
            case=dict(status=f['case'].status,outcome=f['case'].outcome),public_answer=CAO().public(f['case']),
            stage4='INCOMPLETE',ready_for_review=False,final_release_validation=False,
        )
    }


def main():
    generated=artifacts(); TARGET.mkdir(parents=True,exist_ok=True)
    for name,value in generated.items():
        (TARGET/name).write_text(json.dumps(value,sort_keys=True,indent=2,default=str)+'\n')


if __name__ == '__main__':main()
