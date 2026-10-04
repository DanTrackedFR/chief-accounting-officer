# Independent implementation QA — Skill 29

Reviewer context: `implementation_reviewer`; implementation author is a separate agent. No implementation edits performed by reviewer. Synthetic source approvals used by tests do not constitute company approvals.

## Review status

BOUND ACCOUNTING REVIEW PASS, pending final promoted-byte rerun and external release gates. All 38 independent test methods pass; combined authored, independent and Inventory suites:78 methods pass. Governed execution, seven public-output routes, knowledge/implementation/certification freshness and current-owner integrations have been exercised. Production eligibility is recommended only for the explicitly bounded methods, subject to final production-byte fingerprints, full shared regression and exact-head CI; those release gates remain root responsibility.

Fresh positive examples use notional 1,730 and different valuation amounts; include four-framework standalone derivatives and cash-flow hedges, nonfinancial-purchase handoff, cancellation, end-period discontinuation with expected transaction retained, cumulative lower-of reversal across an opening reserve, signed swap liability settlement, fair-value hedge of a firm commitment with independently different hedged-risk change and prospective IFRS rebalancing.

## Recorded findings

| ID | Finding | Remediation / regression |
|---|---|---|
| IQ-29-01 | Initial investment conclusion trusted boolean without comparison evidence. | Author added independently documented comparator and checked numeric conclusion. `test_initial_investment_contradiction` independently passes. |
| IQ-29-02 | Generic exception name/memo could bypass derivative recognition absent framework-specific legal conditions. | Author restricted exception routes and added qualification facts; unsupported own-equity/guarantee routes fail closed. `test_unsupported_exception_does_not_skip_valuation` and framework/rights mutations pass. |
| IQ-29-03 | Late designation documentation blocked whole execution instead of ordinary derivative accounting. | Author added prospective fallback to standalone; `test_late_docs_default_derivative_result` independently passes with ordinary P&L/GL. |
| IQ-29-04 | Current independently measured risk change could contradict its own opening/current cumulative source values. | Author added cumulative risk bridge; `test_hedged_risk_current_vs_cumulative` passes. Fresh cumulative reversal positive verifies actual current OCI is change in cumulative effective reserve. |
| IQ-29-05 | Numeric-only owner binding does not establish actual instrument, debt schedule, FX operation or qualifying net investment. Consolidation currently exposes no dedicated per-operation net-investment metric. | Author added debt indexed-result binding to original debt item/principal/maturity and net-investment per-operation TB/rates/ownership adapter. Independent actual Debt FV/CF and four-framework NI positives pass; identity and excess exposure negatives pass. FX numeric owner linkage separately tracked IQ-29-09. |

| IQ-29-06 | NI disposal boolean released reserve while actual FX/Consolidation source had no disposal. | Author requires actual reviewed full FX-owner disposal. Independent manufactured-disposal negative passes. |
| IQ-29-07 | Comparison initial99 versus comparable100 incorrectly inferred little initial investment and omitted premium recognition. | Author restricts executable monetary derivative route to zero initial investment; independent99/100 regression passes. |
| IQ-29-08 | Unconsumed actual quoted-equity FV result was accepted as a numeric owner import in a standalone forward workpaper. | Author requires every owner assertion used semantically once; independent actual equity FV import regression passes. |
| IQ-29-09 | Unrelated FX receivable AR current closing72 bound a forecast purchase risk because numeric amount matched. | Author binds exact owner transaction ID, original foreign quantity and actual functional currency. Fresh current-owner regression independently passes. |

| IQ-29-10 | A qualified full FX disposal can still contradict the current group owner if Consolidation has no same-operation loss-of-control event. | Author added same-operation/date actual loss-of-control and derecognition-journal requirement; independent actual-full-FX/current-group contradiction blocks. Valid disposal accounting remains dependent on both underlying owners. |

## Scope constraints requiring truthful release reporting

Complex options and excluded components, portfolio/macro techniques, retained IAS39 routes, early US amendments, intragroup exceptional qualification, midperiod independently split accounting and post-discontinuation effective-interest basis amortization currently fail closed. A bounded route should not be described as complete advanced/lifecycle support.

## Execution

`PYTHONPATH=skills:skills/tests:. python -m unittest skills/tests/test_independent_derivatives_hedge.py -q`: 38 independent methods pass after authored remediation. Combined target suites78 methods pass. Independently recomputed all260 generated artifacts byte-for-byte:52 scenario sets, with52 COMPLETE,52 PARTIAL and52 BLOCKED public results;0 mismatches. Numerous independent mutations execute as subtests. Final promoted-byte rerun and anchors remain outstanding.

Actual production owner integration: independently constructed fixed-rate Debt FV and variable-rate Debt CF cases pass original-source ID/principal/maturity/rate-type binding. Four-framework NI cases consume actual current Consolidation and Foreign Currency owner results and pass; operation mismatch, net-investment excess, wrong translation amount and manufactured disposal fail. Actual current Inventory owner consumes -90 signed basis exactly once into160 closing inventory; refreshed-source receipt quantity/adjustment-ID mutations fail. Existing Fair Value owner is quoted equity only: unrelated current result blocked; complex derivative valuation requires independently qualified external evidence. Hedge reporting includes exact signed GL/statement and P&L/reserve bridges, without producing final statements.
