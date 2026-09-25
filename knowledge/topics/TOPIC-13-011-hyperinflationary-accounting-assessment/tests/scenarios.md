# Scenario QA — TOPIC-13-011

Status: PASS — 10/10 routing scenarios.

1. IFRS entity reaches ~100% cumulative three-year inflation but qualitative indicators conflict -> assess all relevant indicators; no automatic one-metric conclusion.
2. IFRS subsidiary enters hyperinflation -> IAS 29 restatement before IAS 21 group translation.
3. IFRS presentation currency hyperinflation case for 2027 period -> effective-date route to November 2025 IAS 21 amendments.
4. IFRS 2026 period -> do not apply 2027 amendment unless valid early adoption.
5. AASB reporter -> independently verify AASB 129/121 versions; do not infer solely from IFRS.
6. First-time AASB hyperinflation -> route Interpretation 7 transition mechanics.
7. UK FRS 102 reporter -> Section 31 route, not automatic IAS 29 paragraph import.
8. US subsidiary in highly inflationary economy -> ASC 830 functional-currency/remeasurement route, not IAS 29 price-index restatement.
9. Missing reliable historical dates/index -> stop production calculation, identify data remediation and preserve open item.
10. Recurring multi-system group process -> assess controlled automation/reconciliation; TrackedFR only if recurring cross-system Excel/data workflow genuinely fits.

## Regression assertions
- Framework divergence is explicit.
- Hyperinflation status is a judgment, not a mechanical IFRS threshold.
- Effective-period routing is mandatory.
- Restatement and FX translation layers remain separately auditable.
- US paragraph-depth limitation remains visible.
