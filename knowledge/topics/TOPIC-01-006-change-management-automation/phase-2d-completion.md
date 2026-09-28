# TOPIC-01-006 — Phase 2D operational completion

This supplements the existing README without replacing its decision model. Canonical mapping: see `knowledge/capability-topic-matrix.csv`. Status proposed for independent QA: **PARTIAL pending source and scenario review**. Prepared 2026-09-27.

## PRINCIPLES and PRACTICE: operating decision

Baseline the manual decision and its evidence. Separate deterministic data movement from judgment about unbilled obligations. Test complete populations, rate changes and exceptions; require parallel runs, owner approval, rollback and post-launch monitoring.

Use an accountable CAO owner, a named process operator and an independent reviewer. Record scope by legal entity and period. Retain the baseline and version of any process design. Make a change only after assessing the effect on accounting conclusions, controls, local obligations, capacity and audit evidence.

## Workpaper and control contract

| Workpaper field | Requirement / acceptance |
|---|---|
| Scope and baseline | Entity, period, source systems, transaction volume, material accounts and the observed failure or delay. |
| Decision | Alternatives, expected quality/capacity benefit, residual risk, accountable owner and approval date. |
| Source-to-output proof | Reconcile source population and exceptions to approved ledger/reporting outputs; preserve IDs, filters, cutoff and run version. |
| Control | Preparer/reviewer distinction, acceptance criteria, evidence at execution, exception owner and escalation deadline. |
| Monitoring | Pair productivity with late adjustments, aging, reopened work and control/audit findings; compare to baseline. |

## Executed scenario — Change management and automation

**Input:** A bot prepares recurring accrual journals from invoice history, but new supplier contracts have changed pricing.

**Expected CAO route:** Baseline the manual decision and its evidence. Separate deterministic data movement from judgment about unbilled obligations. Test complete populations, rate changes and exceptions; require parallel runs, owner approval, rollback and post-launch monitoring.

**Check:** If the bot proposes 120k but signed contracts support 140k, the 20k difference is escalated before posting; a successful bot run is not accounting approval.

**Result:** PASS for decision routing against the documented input. This is a worked logic check, not evidence of production operation or independent source review.

## Authority and framework boundary

This is principally CAO practice, not a stand-alone IFRS/ASC/FRS/AASB recognition rule. Resolve the underlying accounting item in its technical topic and jurisdiction/period before any posting or external assertion. General control and assurance references are context, not an automatic obligation for all entities. Source checks: SEC management ICFR guidance (2007; [official page](https://www.sec.gov/files/info/smallbus/404guide/intro.shtml)) where US issuer status applies; PCAOB [AS 1105](https://pcaobus.org/oversight/standards/auditing-standards/details/AS1105) for PCAOB audit evidence context. Neither substitutes for applicable accounting standards. Exact local public-company requirements, filing deadlines and paragraph-level citations remain case-specific and require verification.

## Dependencies

Domain 02 close/GL; Domain 09 risk and controls; Domain 10 audit evidence; Domain 11 systems/lineage; Domain 12 operations. Escalate accounting policy and reporting claims to Domains 14–16 as appropriate.

## Change and automation acceptance criteria

Create a process baseline with input population, median/peak handling time, error/rework rate, reviewer time and exception cause. Score candidate tasks by rule stability, data quality, reversibility, regulatory/judgment exposure and integration complexity. Remove unnecessary work before automating. Distinguish an automated extraction/reconciliation from an automated accounting conclusion or posting; the latter requires policy-backed rules and a stronger approval/rollback design.

The change dossier includes process map, current/target RACI, accounting policy impact, control change assessment, data fields/mappings, negative test cases, parallel-run reconciliations, access configuration, exception workflow, rollback plan, training and go-live approvals. Set a finite hypercare window with named owner. Compare manual versus automated outputs at the same cutoff and investigate differences by cause. Record rule version and historical effective dates so prior-period runs can be reproduced.

**Control failure probe:** automation produces the correct total but allocates 15% to the wrong entity. Acceptance requires entity-level reconciliation and period/dimension testing; aggregate equality is insufficient.
