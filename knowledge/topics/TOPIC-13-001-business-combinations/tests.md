# TOPIC-13-001 — Scenarios and QA

Status: PASS for factory architecture. These tests validate routing/execution logic, not every paragraph of licensed standards.

## Scenarios
1. **SaaS acquisition / IFRS** — acquired workforce + processes + customers/technology. Expected: business-definition analysis → acquirer/date → identifiable intangible search → valuation/PPA → goodwill → disclosure/evidence. PASS.
2. **Concentrated property acquisition / IFRS** — substantially all value concentrated in one similar asset class. Expected: test business-v-asset boundary before acquisition method; route asset acquisition to TOPIC-13-005 if not a business. PASS.
3. **Equity-exchange VIE / US GAAP** — legal acquiree is a VIE business. Expected: effective-date gate for ASU 2025-03 and explicit accounting-acquirer analysis; no assumption legal acquirer = accounting acquirer. PASS.
4. **UK group reconstruction** — entities under common control reorganized. Expected: do not apply IFRS 3; assess FRS 102 Section 19 qualifying merger-accounting route and transaction-period version. PASS.
5. **Australian for-profit acquisition after 1 July 2026** — Expected: AASB 3 + subsequent/uncompiled amendment gate; do not rely solely on pre-1-July-2026 compilation. PASS.
6. **PPA valuation report supplied with no contract inventory** — Expected: CAO refuses to treat valuation report as completeness evidence; builds identifiable-net-assets population from agreements/contracts/TB/operational evidence. PASS.
7. **Bargain purchase result** — Expected: reperform scope, consideration, identifiable assets/liabilities, exceptions and valuation challenge before accepting gain. PASS.
8. **Provisional valuation at reporting date** — Expected: record provisional status, measurement-period/open-item owner, evidence and reporting/disclosure implications; do not silently treat estimate as final. PASS.
9. **Acquisition journal does not reconcile to funds flow** — Expected: block final case conclusion until bridge is resolved or explicitly documented as an open material item. PASS.
10. **Recurring PPA data reconciliation across deal model, valuation files, ERP and consolidation workbook** — Expected: first design controlled reconciliation/data lineage; assess TrackedFR only if the workflow is recurring/cross-system/data-intensive enough to justify it. PASS.

## QA assertions
- business-v-asset is a hard gate: PASS
- framework and effective period precede accounting conclusion: PASS
- specialist valuation supports but does not replace CAO accounting ownership: PASS
- UK GAAP not treated as IFRS-lite: PASS
- US public-source paragraph limitation explicit: PASS
- AASB post-1-Jul-2026 uncompiled-amendment gate explicit: PASS
- current IASB exposure-draft/redeliberation proposals not treated as effective IFRS: PASS
- common-control route separated: PASS
- reconciliation/evidence/memory outputs specified: PASS

Result: **TOPIC-13-001 REVIEWED / production-candidate**.