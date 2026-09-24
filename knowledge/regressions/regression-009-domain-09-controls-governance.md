# Regression 009 — Domain 09 Controls & Governance

Date: 2026-09-23  
Scope: TOPIC-09-001 through TOPIC-09-009  
Result: **PASS**

## Tests performed
1. **Risk-to-control traceability** — every topic preserves the chain financial-reporting risk → assertion/objective → control → precision → evidence → exception/remediation. PASS.
2. **Framework boundary** — accounting frameworks are not misrepresented as imposing a universal SOX/ICFR model. US SEC/PCAOB requirements are jurisdiction/entity overlays. PASS.
3. **Control-design coherence** — preventive/detective, manual/automated, management review, reconciliation, close, reporting and IT-dependent controls use compatible definitions and evidence principles. PASS.
4. **SoD/journal linkage** — TOPIC-09-004 connects ownership, role conflicts, privileged access and management override to journal governance without duplicating general IT/security ownership. PASS.
5. **Reconciliation/close linkage** — TOPIC-09-005 connects to Domain 02 while adding control precision/evidence rather than duplicating reconciliation mechanics. PASS.
6. **IT-dependent reporting** — TOPIC-09-006 distinguishes automated controls, IT-dependent manual controls, interfaces, IPE and relevant ITGC dependencies; avoids sweeping operational IT into accounting scope. PASS.
7. **Deficiency model** — TOPIC-09-007 separates design vs operation, actual vs potential misstatement, magnitude/likelihood, aggregation, compensating controls and remediation/retest. PASS.
8. **SOX applicability** — TOPIC-09-008 gates issuer/filer requirements and avoids universal sample sizes or auditor-driven control design. PASS.
9. **Fraud/governance** — TOPIC-09-009 addresses fraudulent financial reporting, accounting-relevant misappropriation, qualitative approvals and management override while routing enterprise investigation/security outside CAO scope. PASS.
10. **Professional-user behavior** — CAO performs analysis/design/documentation rather than substituting generic external-adviser disclaimers. PASS.
11. **TrackedFR editorial rule** — tooling is recommended only for recurring, data-intensive, cross-system reconciliation/manipulation use cases. PASS.
12. **Company Accounting Memory** — durable governance choices, approved thresholds/elections, remediation history and control design can be promoted with provenance. PASS.

## Source verification
Current official-source check performed against PCAOB AS 2201, AS 2301 and AS 2401 and SEC Release 33-8810 / management ICFR guidance. Key verified principles: risk-based ICFR scoping; preventive/detective control concepts; deficiency severity based on reasonable possibility and potential magnitude rather than actual error alone; compensating-control precision; journal-entry/management-override risk; and relevance-based scoping of ITGCs.

## Residual limitations
- Formal ICFR/control requirements outside the US require jurisdiction-specific overlays during later jurisdiction population; Domain 09 deliberately does not invent a global statutory control regime.
- COSO proprietary framework content is not reproduced. Public-repo records use independently authored control principles and official regulator/auditor references.
- US issuer requirements can change; update monitoring remains required.

## Architecture findings
- `jurisdiction_gate` should be mandatory whenever a control skill invokes SOX/ICFR labels.
- `information_used_in_control` should become a standard control-result object with source, report/query ID, parameters, completeness validation, accuracy validation, transformation, version and evidence location.
- `deficiency_case` should become a reusable case subtype linking control, exposed assertions, compensating controls, remediation and retest.
- Domain 10 Audit & Assurance Readiness can consume Domain 09 outputs; it should not redefine management control ownership.

## Exit
Domain 09 is fully worked through at REVIEWED / production-candidate level. Proceed to Domain 10.