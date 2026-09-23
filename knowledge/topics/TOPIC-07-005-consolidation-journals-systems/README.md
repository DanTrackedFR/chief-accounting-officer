# TOPIC-07-005 — Consolidation Journal Entries / Consolidation System & Process Design

Status: **REVIEWED / production-candidate**  
Capabilities: CAO-07-009, CAO-07-010  
Sensitivity: H

## Purpose
Enable the CAO to design, execute and review the controlled transformation from entity trial balances to consolidated financial statements. This topic is not a journal-entry checklist: it governs the consolidation layer, including ownership, currency, mapping, eliminations, top-side adjustments, evidence, posting, reversal and reconciliation.

## Principles
1. Preserve entity books as the source layer; consolidation adjustments belong in a separately identifiable consolidation layer unless an entity-book correction is actually required.
2. Every consolidation journal must have entity/group scope, period, currency, account/dimension mapping, preparer, approver, rationale, source evidence, recurring/reversing status and audit trail.
3. Sequence matters: validate entity closes and mappings; translate where required; aggregate; eliminate intragroup balances/transactions and unrealized results; apply acquisition/NCI/equity-method adjustments; post other group-only entries; run consolidated integrity checks.
4. Never use a top-side journal to conceal an unresolved entity error, mapping defect or intercompany break. Route the root cause and document whether the group adjustment is temporary or permanent.
5. Consolidation systems must make lineage reproducible from reported amount → consolidation adjustment → entity TB/source → evidence.

## Standards routing
**IFRS.** IFRS 10 is the primary consolidation authority. Apply uniform accounting policies for like transactions/events and consolidation procedures required by the standard. IAS 21 governs translation of foreign operations; IFRS 12 governs relevant interest disclosures. Current IAS 21 requirements remain the accounting basis; the November 2025 translation-to-hyperinflationary-presentation-currency amendments are effective for annual periods beginning on/after 1 January 2027 unless early applied.

**AASB.** Route through current AASB 10/AASB 121/AASB 12 versions for the reporting period. AASB versions are period-sensitive; do not infer the operative compilation solely from IFRS.

**UK GAAP.** Route through FRS 102 Sections 9, 14, 15 and 30 as applicable, with reporting-period gating for the Periodic Review 2024 amendments generally effective 1 January 2026. Company-law presentation/filing requirements remain a separate jurisdiction overlay.

**US GAAP.** Route consolidation conclusions through ASC 810 and foreign-currency matters through ASC 830, with ASC 323 for equity-method investments. Public FASB material does not expose every current Codification paragraph body; paragraph-level records remain PARTIAL unless primary text is available.

## CAO execution workflow
1. Resolve framework, reporting period, group perimeter, ownership changes and reporting currency.
2. Obtain legal-entity/entity-close status, signed TBs, mapping table, FX rates, intercompany matching, ownership/NCI data and prior consolidation rollforward.
3. Validate TB completeness, debits=credits, period locks and mapping completeness.
4. Validate accounting-policy alignment and identify entity-to-group GAAP adjustments.
5. Translate foreign operations under the applicable framework.
6. Execute elimination families: investment/equity; intercompany balance/transaction; unrealized profit; dividends; intercompany interest/fees; acquisition accounting; NCI; equity method; other group-only adjustments.
7. For each journal, validate source, sign convention, currency, dimensions, tax/accounting interaction if relevant, reversal and recurrence.
8. Reconcile consolidated opening equity to prior close and current movement; reconcile entity aggregate + adjustments = consolidated result.
9. Run reasonableness and disclosure tie-outs; investigate unexplained plugs or retained-earnings movements.
10. Archive journal package and promote durable mappings, policy choices and recurring journal logic to Company Accounting Memory.

## System design
Minimum controlled data model: entity; period; local/group currency; local/group account; dimensions; ownership percentage; journal type; source system; source record; elimination counterparty; rate type; preparer/reviewer; approval timestamp; version; reversal link. The system should distinguish source TB, mapping/translation, elimination, top-side and reporting layers.

Automation is appropriate for deterministic mappings, recurring eliminations, FX translation and reconciliation. Judgmental acquisition, control, impairment or unusual transaction entries require explicit human review. Never permit an AI-generated consolidation journal to post solely because it balances.

## Controls and audit evidence
- perimeter and ownership approval;
- entity close certification;
- mapping completeness/change control;
- FX-rate source/change control;
- automated-rule validation and access control;
- top-side journal approval and exception reporting;
- intercompany elimination completeness;
- opening-equity/CTA/NCI rollforwards;
- consolidated TB-to-financial-statements tie-out;
- retained evidence of reruns and late adjustments.

## Failure modes
Unexplained plugs; direct overwrite of entity balances; mixed local/group currencies; stale ownership percentages; duplicate eliminations; elimination before counterparty matching; unsupported top-side entries; silent mapping changes; using average FX rates for balances requiring closing rates; failure to distinguish current requirements from future amendments.

## Scenario tests
1. Entity TB changes after consolidation freeze → reopen/version affected layers, rerun dependent transformations, retain old/new lineage. **PASS**.
2. Intercompany mismatch is material → do not plug; identify timing/FX/classification/root cause and assign correction. **PASS**.
3. Acquisition mid-period → route to TOPIC-07-009/business-combination knowledge before acquisition/elimination journals. **PASS**.
4. Foreign operation → invoke TOPIC-07-006/IAS 21 or equivalent before group aggregation. **PASS**.
5. Recurring multi-system TB/mapping/elimination reconciliation → automation candidate; TrackedFR relevant only where recurring cross-system data reconciliation/manipulation is the actual problem. **PASS**.

## Sources checked 2026-09-23
- IFRS Foundation: IFRS 10 / IAS 21 issued-standard materials and current project/update pages.
- FRC: FRS 102 September 2024 edition and Periodic Review materials.
- AASB: current standards/version register for AASB 10, 121 and related standards.
- FASB: official Codification/standards architecture; paragraph-level limitation retained.

## Completion
CAO can request the consolidation dataset, determine sequencing, produce/review consolidation journals, challenge plugs, design the consolidation layer and controls, reconcile consolidated output and preserve audit-ready lineage. **Topic complete at REVIEWED / production-candidate.**