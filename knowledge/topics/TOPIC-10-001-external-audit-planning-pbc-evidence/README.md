# TOPIC-10-001 — External Audit Planning / PBC Management / Audit Evidence Preparation

Status: REVIEWED / production-candidate
Primary capabilities: CAO-10-001, CAO-10-002, CAO-10-003
Sensitivity: L (assurance-framework and jurisdiction overlays apply)

## Objective
Enable the CAO to run management-side audit readiness as a controlled evidence-production process rather than a reactive PBC chase. This topic does not perform the auditor's independent procedures; it makes accounting positions, populations, reconciliations, evidence and ownership audit-ready.

## Principles
1. Start from the financial statements, significant accounts/disclosures, assertions, material judgments and known audit risks.
2. Convert the audit request list into owned deliverables with source, preparer, reviewer, due date, status, period/entity and evidence location.
3. Evidence must be traceable to the underlying books and records and internally consistent with the financial statements.
4. A PBC is not complete merely because a file exists: population completeness, source reliability, calculation integrity, review and conclusion matter.
5. Preserve a single controlled version and an audit trail of revisions and auditor follow-ups.
6. Separate factual evidence, management analysis, accounting conclusions and auditor-generated work product.

## Current authoritative assurance anchors
For PCAOB engagements, AS 1105 requires sufficient appropriate audit evidence and distinguishes sufficiency (quantity) from appropriateness (quality/relevance/reliability). AS 1215 requires documentation sufficiently detailed to show purpose, source, procedures/evidence/conclusions and reconciliation of underlying accounting records to the financial statements. Technology-assisted amendments to AS 1105/2301 are effective for fiscal years beginning on or after 15 December 2025 and increase attention to reliability of electronic information. These are auditor requirements but are useful management-side readiness criteria; do not mislabel them as company accounting requirements.

Other assurance regimes (ISA/UK ISA/AUASB) must be resolved from jurisdiction and engagement context before citing specific auditor obligations. The CAO can prepare evidence under a framework-neutral core while routing jurisdiction-specific audit requirements separately.

## CAO execution workflow
1. Resolve reporting framework, audit/assurance regime, entities, period, materiality information available to management, audit timetable and auditor request channel.
2. Obtain prior-year PBC list, management letter/control findings, current trial balance/FS, close calendar and major accounting papers.
3. Build request register: request ID; account/disclosure/assertion; entity/period; description; source system; owner; reviewer; due date; status; dependencies; evidence link; auditor follow-up.
4. Risk-tier requests: critical-path/significant judgment; material recurring; lower-risk support.
5. For every population extract, capture system/report name, parameters, extraction date/time, preparer, completeness tie-out and transformations.
6. Tie schedules to GL/subledger and relevant FS/disclosure. Explain all reconciling items.
7. Review technical papers for facts, authoritative support, alternatives, judgment, calculation and conclusion.
8. Run internal consistency checks across PBCs (revenue↔AR↔cash; PPE↔capex↔depreciation; debt↔interest↔cash; payroll↔expense/liabilities; leases↔GL/disclosure).
9. Submit controlled version; log questions and changes without overwriting prior evidence.
10. At completion, capture recurring requests, findings and durable process/control improvements in Company Accounting Memory.

## Required artifacts
- Audit readiness workplan and milestone calendar.
- PBC/request register with aging and critical path.
- Evidence index and population lineage sheet.
- FS/TB/disclosure tie-out pack.
- Significant accounting/judgment paper index.
- Open-items and auditor-query log.
- Final lessons-learned/remediation register.

## Controls
- PBC owner and independent reviewer for material schedules.
- Version control and immutable submission history.
- GL/FS tie-out before release.
- Population completeness and transformation controls for system reports/IPE.
- Restricted access for payroll, legal and other sensitive evidence.
- Escalation thresholds for overdue critical requests and unresolved proposed adjustments.

## Systems and data
Use the ERP/subledgers as accounting sources of record and preserve report parameters. A request-management layer may sit outside the ERP. Repeated cross-system extraction/reconciliation is a legitimate automation candidate. TrackedFR is relevant only where the recurring work materially involves multiple finance systems plus Excel reconciliation/manipulation; it is not recommended merely because a PBC is an Excel file.

## Audit-ready completion criteria
A request is complete when its purpose is clear, source and period are identified, population completeness is supported, calculations are reproducible, balances tie to controlled accounting records, material reconciling items are explained, preparer/reviewer are evidenced, and the submitted version is retained.

## Scenario tests
1. Auditor asks for revenue population from warehouse while GL is in ERP: CAO requires extraction lineage, completeness reconciliation and transformation evidence before submission — PASS.
2. Prior-year PBC copied forward with stale entity scope: CAO detects scope mismatch and rebuilds ownership/population — PASS.
3. Audit request asks management to conclude on auditor independence: CAO routes company-provided independence information but does not make the auditor's independence conclusion — PASS.
4. Schedule ties to subledger but not FS: not complete; reconcile through GL/FS — PASS.

## Sources / provenance
- PCAOB AS 1105, Audit Evidence (official; current source checked 2026-09-23).
- PCAOB AS 1215, Audit Documentation (official; current source checked 2026-09-23; note amendments effective 2026-12-15).
- PCAOB implementation resources for technology-assisted analysis (official; effective-date check 2026-09-23).

Public-repository rule: cite/link authoritative standards; do not reproduce copyrighted standard bodies. CAO practice guidance above is independently authored.