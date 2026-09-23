# Regression 005 — FX and debt handoff

Date: 2026-09-23  
Scope: TOPIC-06-001 through TOPIC-06-006, with dependencies into close, compensation, reporting and group accounting.  
Result: **PASS with non-blocking source-depth guardrails**.

## Tests
1. Bank/cash reconciliation remains accounting scope, not treasury cash-management advice — PASS.
2. Foreign-currency transaction accounting, remeasurement and presentation-currency translation remain distinct — PASS.
3. Functional-currency assessment precedes material FX remeasurement/translation conclusions — PASS.
4. IFRS/AASB Lack of Exchangeability effective-date gate (1 Jan 2025) retained — PASS.
5. IFRS/AASB hyperinflationary-presentation-currency amendment is future-effective 1 Jan 2027 and is not applied as current mandatory accounting — PASS.
6. UK FRS 102 2026 effective-period gate retained and IAS 21 requirements are not blindly imported — PASS.
7. Intragroup monetary-balance elimination does not automatically erase transaction FX consequences — PASS.
8. Debt legal principal is kept separate from accounting carrying amount/unamortized issuance costs — PASS.
9. Debt modification analysis preserves original EIR, old/new cash flows and fee classification — PASS.
10. Current IFRS 9 and current ASC 470 remain authoritative despite active IASB/FASB projects — PASS.
11. Covenant assessment is separated from modification math and routes to presentation/going-concern/disclosure topics — PASS.
12. US paragraph-level claims remain PARTIAL where public Codification access is insufficient — PASS.

## Architecture findings
- Effective-date metadata is now critical for FX/financial-instrument records because 2025, 2026 and 2027 amendments overlap.
- Future standard-setting projects require an explicit `not_current_gaap` flag or equivalent in the later machine-readable record layer.
- Functional-currency conclusions should be durable Company Accounting Memory with source date and reassessment trigger.
- Debt modification models need immutable pre-modification snapshots for auditability.

## Non-blocking actions
- Continue to TOPIC-06-007 financial asset/liability classification and measurement.
- Maintain public-source guardrail for ASC paragraph depth.
- Normalize duplicate early topic folders only after active scaling; canonical Phase 2B IDs remain authoritative.
