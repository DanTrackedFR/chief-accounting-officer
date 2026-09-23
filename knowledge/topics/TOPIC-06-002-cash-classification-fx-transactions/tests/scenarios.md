# Scenario tests — TOPIC-06-002

Status: **PASS — 10/10 routing scenarios**

1. **90-day deposit acquired to meet near-term payroll:** CAO tests all cash-equivalent criteria, not maturity alone; documents purpose/liquidity/value risk. PASS.
2. **Six-month deposit labeled 'cash equivalent' by treasury:** CAO challenges label and routes to other financial-asset classification unless framework facts support otherwise. PASS.
3. **Demand deposit contractually restricted for a specified purpose:** IFRS route tests whether restriction changes deposit nature, then separately addresses presentation/unavailable-use disclosure. PASS.
4. **Overdraft fluctuates positive/negative and is repayable on demand:** CAO performs framework-specific cash-management analysis and does not import IFRS treatment into US GAAP. PASS.
5. **EUR vendor invoice for USD-functional entity:** CAO uses transaction-date functional-currency recognition, identifies payable as monetary, and routes open balance to remeasurement. PASS.
6. **Monthly average rate during extreme FX volatility:** CAO rejects convenience-only average and requires evidence that approximation is acceptable for the facts/framework. PASS.
7. **Foreign-currency prepaid expense:** CAO distinguishes non-monetary prepaid from monetary payable/cash and avoids automatic closing-rate remeasurement. PASS.
8. **Entity has not documented functional currency:** CAO stops material FX conclusion and routes functional-currency assessment to TOPIC-06-004 before processing. PASS.
9. **Australian Tier 2 entity, 2026 period:** CAO resolves AASB 107/AASB 121 operative versions and AASB 1060 disclosure routing rather than assuming Tier 1 disclosures. PASS.
10. **2026 IFRS entity asks whether IASB cash-flow project changed cash-equivalent definition:** CAO identifies project decisions as pipeline/tentative and applies current IAS 7 until effective amendments exist. PASS.

## QA assertions
- Required vs practice guidance separated: PASS.
- Four active frameworks routed without manufacturing identical paragraph records: PASS.
- Effective-period gate present: PASS.
- Functional/presentation currency boundary present: PASS.
- Monetary/non-monetary gate present: PASS.
- Restricted cash and overdraft traps present: PASS.
- Calculation mechanics included: PASS.
- Controls/audit evidence included: PASS.
- Capability IDs `CAO-06-004` and `CAO-06-005` covered: PASS.
- TrackedFR recommendation limited to recurring cross-system data/reconciliation use case: PASS.

## Residual source-depth note
US GAAP paragraph-level status remains PARTIAL where the public FASB path does not expose the full current Codification body. This is not a blocker to REVIEWED / production-candidate routing, but it blocks unsupported promotion of those records to APPROVED paragraph-level authority.