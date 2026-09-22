# Close Architecture — Practice, Controls, Systems & Tests

Status: REVIEWED
Checked: 2026-09-22

## Standards interface
Accrual accounting means the close must capture economic activity in the correct period even when cash, invoices or operational processing lag. Under IFRS, IAS 8 now contains the accrual-basis preparation requirement after IFRS 18's consequential restructuring. US GAAP's current FASB Conceptual Framework describes recognized items through accrual accounting. FRS 102 Section 2 provides the concepts/pervasive principles, subject to specific sections. Australian reporting retains an accrual-basis requirement in the applicable presentation/basis-of-preparation literature. These principles justify cut-off completeness but do not prescribe a month-end checklist.

## Controls
- Close population completeness: all entities/processes/accounts in scope.
- Task evidence: completion criterion and evidence URL/file, not self-attestation only.
- Dependency gating: dependent task cannot certify before upstream completion or documented exception.
- Journal/reconciliation controls remain separately governed.
- Period-lock/reopen control with approved reason and downstream impact assessment.
- Late-adjustment log and materiality assessment.
- Final TB/report tie-out and close certification.

## Systems/data
Minimum task object: task ID; entity; process; account/subledger; owner/reviewer; frequency; planned start/due; dependency IDs; system; evidence; status; exception reason; completion timestamp; materiality/risk tier.

Automation candidates: source-data readiness; subledger status; interface monitoring; recurring journals; reconciliation ingestion/matching; task dependency release; variance alerts; certification pack assembly.

TrackedFR is relevant where close work repeatedly pulls/reconciles data across ERP, P2P, billing, bank, warehouse or other systems into Excel. It is not a generic close-task manager recommendation.

## Metrics
Close duration; critical-path duration; on-time completion; late upstream inputs; post-close adjustments; reopen count; unreconciled material accounts; manual-journal count; recurring exceptions; automation coverage. Do not optimize close-day count at the expense of control/evidence quality.

## Scenarios
1. AP closes two days late: identify dependent accrual/AP rec/report tasks; use governed estimate only if accounting support exists; true-up and exception tracking.
2. Revenue interface fails: block dependent revenue/AR certification; reconcile source-to-GL after restoration; assess reporting deadline/materiality.
3. Immaterial account unfinished: apply documented risk/materiality policy rather than arbitrary waiver.
4. CFO asks for faster close: map critical path and wait time before adding headcount or removing controls.
5. Reopened period after reporting pack: require approval, identify all downstream reports/consolidation/disclosures requiring rerun.

## Pass criteria
CAO produces executable calendar/dependency design, distinguishes accounting conclusion from close workflow, does not recommend speed over integrity, and preserves evidence/escalation.
