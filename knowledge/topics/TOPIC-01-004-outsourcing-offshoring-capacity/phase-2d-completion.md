# TOPIC-01-004 — Phase 2D operational completion

This supplements the existing README without replacing its decision model. Canonical mapping: see `knowledge/capability-topic-matrix.csv`. Status proposed for independent QA: **PARTIAL pending source and scenario review**. Prepared 2026-09-27.

## PRINCIPLES and PRACTICE: operating decision

Separate invoice capture, coding, approval, exception and accrual ownership. Model base hours = volume × observed handling minutes / 60, then add review, exceptions, peak-load and absence capacity. Do not treat theoretical automation savings as available capacity before acceptance testing.

Use an accountable CAO owner, a named process operator and an independent reviewer. Record scope by legal entity and period. Retain the baseline and version of any process design. Make a change only after assessing the effect on accounting conclusions, controls, local obligations, capacity and audit evidence.

## Workpaper and control contract

| Workpaper field | Requirement / acceptance |
|---|---|
| Scope and baseline | Entity, period, source systems, transaction volume, material accounts and the observed failure or delay. |
| Decision | Alternatives, expected quality/capacity benefit, residual risk, accountable owner and approval date. |
| Source-to-output proof | Reconcile source population and exceptions to approved ledger/reporting outputs; preserve IDs, filters, cutoff and run version. |
| Control | Preparer/reviewer distinction, acceptance criteria, evidence at execution, exception owner and escalation deadline. |
| Monitoring | Pair productivity with late adjustments, aging, reopened work and control/audit findings; compare to baseline. |

## Executed scenario — Outsourcing and capacity

**Input:** A provider offers to process 4,000 monthly invoices at lower cost while the retained entity team has one controller and a three-day close.

**Expected CAO route:** Separate invoice capture, coding, approval, exception and accrual ownership. Model base hours = volume × observed handling minutes / 60, then add review, exceptions, peak-load and absence capacity. Do not treat theoretical automation savings as available capacity before acceptance testing.

**Check:** At 4,000 invoices × 6 minutes = 400 processing hours; add 10% exceptions × 12 minutes = 80 hours and 50 review hours: 530 hours before absence/peak buffer. A 500-hour contracted capacity is insufficient; either change scope or add capacity. Treat numbers as illustrative, not a staffing benchmark.

**Result:** PASS for decision routing against the documented input. This is a worked logic check, not evidence of production operation or independent source review.

## Authority and framework boundary

This is principally CAO practice, not a stand-alone IFRS/ASC/FRS/AASB recognition rule. Resolve the underlying accounting item in its technical topic and jurisdiction/period before any posting or external assertion. General control and assurance references are context, not an automatic obligation for all entities. Source checks: SEC management ICFR guidance (2007; [official page](https://www.sec.gov/files/info/smallbus/404guide/intro.shtml)) where US issuer status applies; PCAOB [AS 1105](https://pcaobus.org/oversight/standards/auditing-standards/details/AS1105) for PCAOB audit evidence context. Neither substitutes for applicable accounting standards. Exact local public-company requirements, filing deadlines and paragraph-level citations remain case-specific and require verification.

## Dependencies

Domain 02 close/GL; Domain 09 risk and controls; Domain 10 audit evidence; Domain 11 systems/lineage; Domain 12 operations. Escalate accounting policy and reporting claims to Domains 14–16 as appropriate.

## Capacity and provider acceptance gate

Build capacity by activity and weekly demand curve, not by a single headcount ratio. For each activity store volume, observed handling minutes, exception rate, review minutes, peak factor, policy/technical support hours and resilience cover. Calculate monthly available hours from contracted time less leave, training, governance and control work. Compare at month-end and quarter/year-end separately; record scenario assumptions and confidence intervals. An outsourcing proposal needs a transition double-run budget because the retained team must review the provider while still operating the old process.

The service contract specifies the processing boundary, permitted data, local time zone/cutoff, throughput and accounting-quality SLAs, escalation times for close-critical failures, evidence export, audit access, access removal, incident notification, subcontractor approval and exit assistance. Test one invoice from request to GL and one exception from detection to resolution before migration. Management retains policy, period-end estimation, material judgment, statutory reporting, provider oversight and final sign-off. If local law or privacy constraints alter the model, resolve them through the jurisdiction overlay.

**Control failure probe:** provider posts 250 invoices but returns only 240 IDs. Reconcile source, accepted, rejected and posted counts/amounts, quarantine the unresolved ten and escalate before sign-off. A provider completion certificate cannot replace that bridge.
