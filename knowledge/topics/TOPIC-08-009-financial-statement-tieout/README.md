# TOPIC-08-009 — Financial Statement Tie-Out / Disclosure Controls & Review

Status: REVIEWED / production-candidate
Primary capabilities: CAO-08-017, CAO-08-018
Sensitivity: H

## Principle
A financial-statement tie-out proves lineage from the approved accounting records and governed disclosure sources to every quantitative and material qualitative assertion in the issued report. It is not a last-minute arithmetic check.

## CAO workflow
1. Freeze the reporting version and identify authoritative source TB/consolidation and disclosure datasets.
2. Create statement-to-TB mapping and note-to-statement cross-reference.
3. Tie every primary-statement amount to approved source data; tie note totals/subtotals and rollforwards to statements, subledgers or governed calculations.
4. Reperform internal arithmetic, cross-footing, percentages, per-share amounts, comparative amounts and currency/unit scaling.
5. Test consistency of accounting policies, significant judgments, estimates, commitments, contingencies, related parties, segment information, subsequent events and going concern against the underlying topic workpapers.
6. Search for repeated amounts/narratives across annual report sections and resolve inconsistencies rather than overwriting one copy.
7. Validate current-period framework/effective-date/disclosure checklist and entity/jurisdiction overlay.
8. Log every review note with owner, severity, disposition and evidence; rerun tie-out after late entries or disclosure changes.
9. Lock final signed/authorized version and preserve source lineage.

## Control design
Required attributes: preparer and independent reviewer; source references; version/date; materiality/risk logic; completeness checklist; review-note closure; late-change trigger; final certification. High-risk disclosures receive deeper source-level review even when quantitatively immaterial.

Automated checks can validate arithmetic, repeated values, source mappings and version drift, but do not replace judgment over completeness or wording. For recurring reports fed from ERP/consolidation/disclosure workbooks, cross-system reconciliation automation can be valuable. TrackedFR is relevant only where recurring extraction/reconciliation/manipulation across finance systems and Excel is present.

## Audit evidence
Retain final TB/consolidation version, mapping, disclosure checklist, tie-out workbook/output, source workpapers, review-note log, late-change log, approval and signed/final report hash or version identifier.

## Scenarios
- Late top-side journal after first tie-out -> invalidate affected certifications and rerun mapped statements/notes.
- Note rollforward ties internally but not to balance sheet -> fail; investigate scope/mapping/source-version mismatch.
- Narrative says no covenant breach while debt memo says waiver obtained after period end -> route inconsistency to debt/subsequent-event topics before sign-off.
- Same KPI appears with two definitions in annual report -> fail governance review and route to APM definition owner.

## Framework routing
Tie-out mechanics are framework-independent practice, but the completeness population is framework/jurisdiction/period sensitive. Pull disclosure requirements from the applicable IFRS, US GAAP/SEC, UK GAAP/legal, or AASB/Australian overlay rather than embedding a static checklist here.