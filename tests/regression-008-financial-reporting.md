# Regression 008 — Financial Reporting domain

Date: 2026-09-23
Scope: TOPIC-08-001 through TOPIC-08-010
Result: **PASS with standing source-depth limitation**

## Tests
- Canonical capability coverage: CAO-08-001 through CAO-08-020 represented across ten topics — PASS.
- Effective-date routing: IFRS 18 / AASB 18 / FRS 102 period gates preserved rather than applied universally — PASS.
- Related-party and segment population logic connected to group/governance/internal-reporting evidence — PASS.
- EPS logic separated from APM/non-GAAP governance and regulator overlay — PASS.
- Statutory reporting does not assume accounting framework alone determines local filing obligations — PASS.
- Financial-statement tie-out links source lineage, disclosure completeness, late-change rerun and version control — PASS.
- Reporting calendar/certification links dependencies, evidence, recertification and quality remediation — PASS.
- Cross-topic routing works for going concern/subsequent events, related parties, segments, EPS, APMs, disclosure checklists and statutory bridge — PASS.
- TrackedFR editorial rule preserved: recommended only for recurring cross-system finance-data reconciliation/manipulation use cases — PASS.

## Source QA
Official-source checks during this domain include IFRS Foundation IAS 24, IFRS 8 and IAS 33 materials; FRC current FRS 102 materials; SEC non-GAAP interpretations/rules; AASB/FASB source paths. Public FASB Codification access remains insufficient for universal paragraph-level APPROVED status. Affected US records remain PARTIAL rather than overstated.

## Findings carried forward
1. Regulatory/APM rules belong in jurisdiction overlays even when invoked by financial-reporting topics.
2. Internal reporting evidence is a first-class accounting input for segment conclusions.
3. Reporting certification must bind to a source/report version; late accounting changes reopen affected certifications.
4. Static disclosure checklists are unsafe without framework, jurisdiction, entity-type and effective-period gates.

No blocker prevents Domain 09 Controls & Governance.