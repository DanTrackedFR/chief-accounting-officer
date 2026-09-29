# TOPIC-01-007 — Phase 2D operational completion

This supplements the existing README without replacing its decision model. Canonical mapping: see `knowledge/capability-topic-matrix.csv`. Status proposed for independent QA: **PARTIAL pending source and scenario review**. Prepared 2026-09-27.

## PRINCIPLES and PRACTICE: operating decision

Classify use by consequence; require grounded inputs, data permissions, validation against the ledger and independent accounting approval. Keep read-only analysis separate from journal posting. Maintain model/prompt/version logs, evaluation cases, access review, incident and rollback procedures.

Use an accountable CAO owner, a named process operator and an independent reviewer. Record scope by legal entity and period. Retain the baseline and version of any process design. Make a change only after assessing the effect on accounting conclusions, controls, local obligations, capacity and audit evidence.

## Workpaper and control contract

| Workpaper field | Requirement / acceptance |
|---|---|
| Scope and baseline | Entity, period, source systems, transaction volume, material accounts and the observed failure or delay. |
| Decision | Alternatives, expected quality/capacity benefit, residual risk, accountable owner and approval date. |
| Source-to-output proof | Reconcile source population and exceptions to approved ledger/reporting outputs; preserve IDs, filters, cutoff and run version. |
| Control | Preparer/reviewer distinction, acceptance criteria, evidence at execution, exception owner and escalation deadline. |
| Monitoring | Pair productivity with late adjustments, aging, reopened work and control/audit findings; compare to baseline. |

## Executed scenario — AI governance and growth readiness

**Input:** A finance copilot suggests releasing an old accrual based on a terse chat summary and offers to post it.

**Expected CAO route:** Classify use by consequence; require grounded inputs, data permissions, validation against the ledger and independent accounting approval. Keep read-only analysis separate from journal posting. Maintain model/prompt/version logs, evaluation cases, access review, incident and rollback procedures.

**Check:** The accrual release is blocked pending support for settlement or extinguishment, period attribution and reviewer sign-off. A confident natural-language answer is not evidence.

**Result:** PASS for decision routing against the documented input. This is a worked logic check, not evidence of production operation or independent source review.

## Authority and framework boundary

This is principally CAO practice, not a stand-alone IFRS/ASC/FRS/AASB recognition rule. Resolve the underlying accounting item in its technical topic and jurisdiction/period before any posting or external assertion. NIST [AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework) is voluntary guidance for governing AI risk; general control and assurance references are context, not an automatic obligation for all entities. Source checks: SEC management ICFR guidance (2007; [official page](https://www.sec.gov/files/info/smallbus/404guide/intro.shtml)) where US issuer status applies; PCAOB [AS 1105](https://pcaobus.org/oversight/standards/auditing-standards/details/AS1105) for PCAOB audit evidence context. Neither substitutes for applicable accounting standards. Exact local public-company requirements, filing deadlines and paragraph-level citations remain case-specific and require verification.

## Dependencies

Domain 02 close/GL; Domain 09 risk and controls; Domain 10 audit evidence; Domain 11 systems/lineage; Domain 12 operations. Escalate accounting policy and reporting claims to Domains 14–16 as appropriate.

## AI use register and decision rights

For each proposed model use store purpose, owner, affected accounts/decisions, data classification, provider and data retention terms, permitted prompts/actions, retrieval sources, model and prompt versions, validation set, human reviewer, incident path and retirement criteria. Risk-tier read-only drafting, classification/reconciliation suggestions and posting authority separately. An AI response should identify source record IDs and show unresolved contradictions. If evidence cannot be traced or reproduced, route to a human workpaper before ledger action.

Test adversarial inputs: a forged instruction inside an invoice, stale policy retrieval, duplicate transaction, conflicting currencies, period cutoff, missing entity, fabricated citation and attempts to reveal restricted customer data. Evaluation should measure false approvals as well as overall accuracy; a high overall accuracy score can conceal rare but material errors. Changes to model, prompt, source connector or retrieval index require regression, sampled expert review and rollback. Monitor drift and incident trends. NIST AI RMF provides voluntary risk management structure; it is not an accounting standard or statutory approval.

**Control failure probe:** an invoice includes a note telling the model to bypass review. Treat invoice text as untrusted source data and reject the instruction; retain the attempted prompt injection in the incident/evaluation log.
