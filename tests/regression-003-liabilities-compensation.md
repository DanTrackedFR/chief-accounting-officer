# Regression 003 — Liabilities / Compensation Batch

Date: 2026-09-23
Scope: TOPIC-05-001 through TOPIC-05-006 plus dependencies into revenue, assets and close.

## Results
PASS — accounting boundaries remain coherent.

1. AP/payroll process knowledge does not override recognition/measurement standards.
2. Ordinary accruals are distinguished from IAS 37/AASB 137/FRS 102 Section 21 provisions and US loss contingencies.
3. Onerous-contract analysis explicitly blocks false IFRS-to-US equivalence.
4. Payroll-to-GL remains accounting scope, not payroll operations.
5. Employee-benefit classification routes share-based awards away from IAS 19/Section 28 and into dedicated SBC topics.
6. Sales commissions route simultaneously to compensation obligation and, where applicable, revenue contract-cost capitalization without double counting.
7. Australian entity/tier/version overlays and UK 2026 effective-period routing remain first-class context.
8. Public FASB source-depth limitation remains visible; no unsupported Codification paragraph bodies are promoted to APPROVED.

## Reusable primitives confirmed
Obligation/past-event test; population completeness; classification; estimate methodology; service-period attribution; capitalization boundary; rollforward; subledger/source-to-GL reconciliation; disclosure; evidence; specialist interface; exception governance.

## Architecture action
Future top-level denominator topics that combine unrelated capabilities may use explicit subcase boundaries inside one topic factory. Do not merge their accounting logic merely because Phase 2B grouped them under one stable topic ID.

## Repository hygiene
Duplicate retry folders in earlier close topics remain a normalization task. They do not change the canonical denominator or progress ledger.