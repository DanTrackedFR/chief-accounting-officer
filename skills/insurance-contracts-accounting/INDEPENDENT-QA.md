# Independent implementation QA — Insurance Accounting #39

Reviewer role: fresh implementation reviewer, distinct from knowledge author, knowledge reviewer and implementation author. This review does not approve actuarial models or accounting knowledge. The reviewer authored `skills/tests/test_independent_insurance_contracts.py` and did not alter the workflow, fixtures or reporting handoffs.

Status: PASS — bounded implementation independently approved at the reviewed byte anchors below. Promotion and exact-head CI remain root integration gates; any subsequent accounting code or source changes require a fresh independent rerun.

## Fresh methodology

Semantic attacks refresh the controlled source snapshots and case certification. A changed byte hash alone therefore cannot conceal the substantive error. Positive cases independently scale money by 1.6 while preserving actual rates and release proportions, combine materially different GMM groups, exercise IFRS/AASB profitable/onerous/future-service and PAA, held reinsurance, and native US DAC/premium-deficiency accounting. Valid examples must reconcile, so a block-all implementation fails review.

## Findings and executable regressions

| ID | Finding | Regression | State |
|---|---|---|---|
| IQA-01 | Expired PAA contracts retained half their revenue/LRC | time_paa_expired_coverage_cannot_retain_half_lrc | Independently retested fixed |
| IQA-02 | Policy group_id could contradict actual group membership | wrong_policy_group_id | Independently retested fixed |
| IQA-03 | Cohort label could differ from actual issue year | wrong_date_bound_cohort | Independently retested fixed |
| IQA-04 | Claims predating coverage could be incurred | claim_occurs_before_coverage | Independently retested fixed |
| IQA-05 | Unknown underlying reinsurance group raised raw lookup exception | reinsurance_wrong_underlying_and_counterparty | Independently retested fixed |
| IQA-06 | Expired GMM contracts retained future coverage units/CSM/LRC | gmm_expired_with_unreleased_service | Independently retested fixed |
| IQA-07 | US route silently ignored IFRS future-service changes | us_unsupported_future_change_not_ignored | Independently retested fixed |
| IQA-08 | A report labeled no change could contain future-service assumption movements | none_change_cannot_contain_assumption_movement | Independently retested fixed |
| IQA-09 | Two groups could share one economic identity | positive_multiple_groups_no_alias | Independently retested fixed |
| IQA-10 | Half-year inception could accrue a full year of CSM interest | gmm_interest_period_bound_to_coverage | Independently retested fixed |
| IQA-11 | PAA undiscounted-claims exemption could contradict actual expected settlement | paa_claim_exemption_bound_to_actual_settlement | Independently retested fixed |
| IQA-12 | Explicit OCI election was silently ignored | report_financial_oci_request_not_ignored | Independently retested fixed |
| IQA-13 | Two-decimal monetary rounding admitted an incorrect service fraction and material revenue | positive_actual_time_paa_and_fraction_precision | Independently retested fixed |
| IQA-14 (root-origin) | Output omitted named auditable movement schedules | independent_named_schedule_identities_and_signs | Independently retested fixed |
| IQA-15 (root-origin, reviewer corroborated) | Native US presentation retained IFRS labels and recognition/qualification boundaries required explicit restriction | native_us_entity_scope_dac_amortization_and_recognition; independent_named_schedule_identities_and_signs | Independently retested fixed |
| IQA-16 (root/author-origin) | Unbound specialist imports and unreviewed elections needed explicit rejection | unbound_specialist_imports_and_elections_fail_closed | Independently retested fixed |
| IQA-17 (author-origin) | AASB compilation and acquisition-expense attribution required exact operative qualification | final_compilation_early_adoption_and_expensed_acquisition_guard | Independently retested fixed |
| IQA-18 (author-origin) | Financing horizon and duplicate underlying recoveries needed additional original-source bindings | actual_financing_horizon_and_duplicate_underlying_recovery | Independently retested fixed |

41 independent test methods passed in 10.8 seconds, including numerous framework and source-dimension subcases. All 13 reviewer-discovered implementation findings were independently rerun after remediation. The additional authored financing-horizon and duplicate-underlying-recovery guards were independently attacked and passed. Native Statements/Disclosure handoffs were independently rerun for IFRS/AASB GMM/PAA, native US and held IFRS/AASB cases. Duplicate mappings, aliases under other source versions/lines, stale results, missing populations and wrong owners fail closed. Training-data and direct-source provenance remain private; shared case, knowledge and implementation staleness are challenged independently.

## Supported scope and limitations under review

The candidate is a first-year 2026, single functional currency, qualified-input accounting engine. It consumes the actuary's reviewed reports, versions, assumptions and populations. It never creates future claims, RA, mortality/lapse, yield curves, catastrophe assumptions or coverage forecasts. IFRS/AASB GMM issued and eligible PAA issued/proportionate held; native US short-duration issued/DAC/deficiency routes are the intended bounded executable routes. UK native insurance measurement, advanced VFA, transition, GMM held/loss recovery, complex modifications/acquisitions, FX and OCI must remain fail-closed. Final approved scope is subject to the final anchors and independent rerun.

## Independent positive calculations and owner boundaries

The reviewer supplied a valid half-year GMM inception using 184/365 of a year: CSM interest 3.02, service release 38.26 and closing CSM 114.76; a consistent actual elapsed-time PAA allocation; two policies within one PAA group; and two separate materially different GMM groups. Each passes. Existing Financial Instruments/ECL, Fair Value, Derivatives/Hedge and FX owners actually reexecuted COMPLETE alongside insurance refusal tests. This proves ownership preservation and bounded refusal, not consumption of their valuation/FX outputs. Insurance revenue stays in Insurance; investment/separation/participating/foreign-currency cases require the specialist owners and remain blocked.

## Final reviewed anchors

The machine-readable `INDEPENDENT-QA-ANCHORS.json` records SHA-256 hashes of the reviewed executable accounting, shared retrieval/privacy, native reporting owner, methods and test files. The report and anchor file omit their own hashes to avoid circular references. Post-promotion independent rerun passed: 41 independent methods plus 9 native integration methods, 50 tests total, in 14.7 seconds. Every previously anchored executable/retrieval/privacy/test file is byte-identical; SKILL.md changes only version 0.9.0→1.0.0 and status review→production. Updated anchors bind those final metadata bytes. Exact-final-head GitHub Actions remains the root integration gate.

The root-origin output completeness gap is also closed: named LRC, LIC, CSM, RA and loss bridges (plus native US DAC) were independently recalculated with positive and negative future-service changes, profitable and onerous groups, issued PAA, both acquisition elections, US deficiency ordering and held IFRS/AASB. Every signed opening-plus-movements bridge equals its closing amount and the closing accounting stock. The final native US output omits CSM/RA/loss-component fields and schedules. It exposes premium_deficiency_liability and the premium_deficiency/DAC bridges. Independent tests rechecked insurance-entity/source-scope restrictions, bounded fully paid coverage inception recognition and protection-pattern DAC amortization; unsupported earlier premium or other populations fail closed.

## Post-promotion verification

The prior review candidate `305704ad60d25e791857b4dee2ca00c7ea18bfd7` passed Actions run `37207876023`. That run is review-candidate evidence; the final promoted head needs its own exact-head CI. The reviewer independently reran 50 tests on promoted 1.0.0/production metadata and confirmed all anchored code remains unchanged. No open implementation findings remain within the bounded supported scope.
