# Independent Government Grants knowledge QA

Reviewer: `grant_independent_knowledge_reviewer`, separate from knowledge author and implementation author/reviewer. Review date: 4 October 2026. Atomic claim disposition: APPROVED, 172 individually challenged claims. `independent-review.json` records a decision-specific counterexample and exact content hash for every claim; no author approval or inherited prior-task QA is used.

## Primary inspection and limits

Independently opened the IFRS Foundation IAS20 official summary, current AASB120 operative portal compilation, FRC September2024 redacted standard Section24 and PeriodicReview effective-date/B24.3A material, and FASB ASU2025-10 issued amendment text including scope, recognition, nonmonetary measurement, repayment, disclosure and65-2 adoption/transition. AASB current portal identifies the2021 compilation applicable to2026 before2027. IFRS operative-body access is not represented as direct verification. ASU primary amendments corroborate US accounting but do not become authoritative live ASC assurance. Independent checks preserve future direct-source audit flags for training-derived and US primary-corroborated claims.

Each normative proposition was assessed against its actual framework, entity/period limits and source metadata. Governance atoms were separately challenged for identity, boundaries, current evidence and exact-once accounting. Numeric counterexamples include loan100/liability85/benefit15, income repayment70/deferral30/expense40, partial net-asset repayment10 with two-fifths elapsed/catch-up4, and deferred rollforward100+60−40−20=100. These are independently constructed examples rather than copies of authored outputs.

## Findings and remediation

| Finding | Challenge | Remediation and independent disposition |
|---|---|---|
| KQ-01 | ASU-only US claims labelled SOURCE_VERIFIED contradicted repository evidence ringfence. | All29 US normative claims PRIMARY_CORROBORATED, provisional assurance and open ASC audit. Actual inspected amendment supports named direct-source accuracy track, separately from operative-authority assurance. Retested PASS. |
| KQ-02 | Unqualified useful-life deferred release could impose land depreciation or ignore actual expense proportions. | IFRS/AASB depreciable owner expense pattern clarified; nondepreciable obligations distinguished, AASB17–18 locator added. Retested PASS. |
| KQ-03 | Generic Agriculture exclusion omitted distinction between FVLCTS special route and cost-model ordinary grant route. | Two separate framework atoms added: unconditional receivable versus conditional satisfaction, cost-model ordinary route and Agriculture ownership. Retested PASS. |
| KQ-04 | Direct assurance accepted ASU source kind; truthy malformed source URL/locator/date could masquerade as inspected source. | SOURCE_VERIFIED requires CURRENT_STANDARD; actual HTTPS/string locator and ISO access date bounded by review date. US amendment remains lower evidence. Independent malformed metadata and assurance-inflation tests PASS. |
| KQ-05 | Public projection contamination detector missed training/source/evidence labels embedded in otherwise public text. | Full internal provenance sentinels enforced in public fields; mutated propositions/limitations and actual allowlisted retrieval tested. PASS. |
| KQ-06 | US adoption after reporting period end but before issuance was falsely blocked by date comparison. | Independent June30 period/Aug1 adoption valid-difficult case requires eligible unissued adoption and an explicit preparation date; missing/before-period/before-adoption dates and future/unreviewed adoption fail closed. Independently retested PASS and recorded in ledger. |

## Adversarial coverage

Receipt does not prove compliance; management expectation and programme labels do not prove eligibility. Procurement, ordinary customer arrangements, tax-liability items, shareholder contributions, ordinary debt, employee awards and intangible/service transfers retain their owners. Future-cost grants cannot create past-period income or unsupported US receivables. Asset deduction and deferred income cannot coexist. Nonmonetary value cannot be invented. Forgiveness assurance/probability and below-market benefits differ across frameworks. Repayment uses actual obligation evidence and deferred balances, preserving error/estimate distinctions.

US issued2025 amendment is not proposal, not mandatory2026, and not automatically applied to nonadopters/NFP/employee benefit plans. FRS102 performance/accrual requires actual class election; both require assurance, nominal measurement and deferred asset-basis netting are not UK policies. AASB Tier1 for-profit scope excludes NFP/public-sector/Tier2. Ordinary IAS20/AASB120 does not remeasure Agriculture biological assets. PPE, R&D, inventory, payroll, debt, tax, Revenue, Financial Statements/Disclosure and Controls/Systems boundaries are individually challenged in the claim ledger. Implementation execution is reserved for the separately fresh implementation reviewer.

## Executable evidence

`test_independent_claim_qa.py` contains11 independent test methods. With20 authored knowledge test methods, the supplemental knowledge suite contains31 tests. Tests validate actual approved claims and independent hashes, reject stale/malformed/unselected invalid claims, reject model/entity/period contamination, preserve public privacy, exercise real retrieval and real US adoption evidence, and challenge the distinct substantive routes. Final command: `python -m unittest discover -s knowledge/government-grants -p 'test_*.py'`.

Approval proves independently checked bounded accounting knowledge, not every source directly authoritative, legal compliance, implementation completion or unconditional promotion.
