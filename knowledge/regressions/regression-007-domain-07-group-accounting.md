# Regression 007 — Domain 07 Group Accounting & Consolidation

Date: 2026-09-23  
Scope: TOPIC-07-001 through TOPIC-07-009  
Result: **PASS with continuing source-depth guardrail**

## Cross-topic assertions
- Control/perimeter determination precedes consolidation mechanics: PASS.
- Joint control/significant influence are not inferred from percentage alone: PASS.
- Entity TB → translation/mapping → consolidation adjustments → consolidated TB → financial statements lineage is preserved: PASS.
- Intercompany matching precedes elimination; unresolved differences are not plugged: PASS.
- Functional-currency, transaction remeasurement and foreign-operation translation remain separate concepts: PASS.
- Ownership change route depends on whether control/joint control/significant influence boundary is crossed: PASS.
- Partial disposal without loss of control is distinguished from loss-of-control accounting: PASS.
- Equity method includes basis differences, investee results/OCI, transactions, losses and impairment rather than percentage-of-profit only: PASS.
- Joint-operation versus joint-venture classification under IFRS/AASB is rights/obligations based: PASS.
- Acquisition/disposal topics invoke complex-transaction knowledge rather than duplicating PPA/business-combination rules: PASS.
- Current requirements are separated from IASB Equity Method pipeline decisions and future IAS 21/AASB effective-date changes: PASS.
- AASB is independently period-gated rather than inferred from IFRS: PASS.
- UK FRS 102 reporting-period gate retained: PASS.
- US paragraph-level records do not receive unsupported APPROVED status where current Codification body text is unavailable publicly: PASS.

## Architecture findings
1. **Transformation lineage is a first-class group-accounting requirement.** The CAO must preserve separate source-TB, translation, mapping, elimination/top-side and reporting layers.
2. **Boundary-crossing is reusable decision logic.** Ownership changes should call a common pre/post relationship resolver before calculation.
3. **Effective-date routing remains mandatory.** November 2025 IAS 21 amendments apply from 1 January 2027 unless early applied; AASB 2024-4 defers specified AASB 10/128 amendments to 1 January 2028; IASB Equity Method redeliberations remain non-effective pipeline.
4. **Certification requires coherence, not just a balanced TB.** Opening equity, NCI, CTA, intercompany, acquisition/disposal and FS tie-out bridges are mandatory review objects.

## Source QA
Official sources checked during batch: IFRS Foundation issued-standard/project pages; FRC FRS 102 September 2024/current amendment material; AASB current standards/version pages and AASB 2024-4. Existing FASB public-access limitation continues and is non-blocking at REVIEWED / production-candidate status.

## Blockers
None. US paragraph-level primary-text completeness remains PARTIAL, already recorded globally.

## Outcome
Domain 07 is fully worked through at the canonical top-level topic denominator. Proceed to Domain 08 Financial Reporting, skipping TOPIC-08-005 because it is already worked through.