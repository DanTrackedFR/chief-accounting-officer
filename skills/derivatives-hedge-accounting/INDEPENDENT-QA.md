# Independent implementation QA — Skill 29

Reviewer context: `implementation_reviewer`; implementation author is a separate agent. No implementation edits performed by reviewer. Synthetic source approvals used by tests do not constitute company approvals.

## Review status

BOUND ACCOUNTING REVIEW PASS, pending final promoted-byte rerun and external release gates. All 48 independent test methods pass (38 accounting +10 cross-owner handoffs); authored plus independent suites:93 methods pass before final Inventory artifact regeneration. Including nine Inventory methods, the targeted set is102 methods. Governed execution, seven public-output routes, knowledge/implementation/certification freshness and current-owner integrations have been exercised. Production eligibility is recommended only for the explicitly bounded methods, subject to final production-byte fingerprints, full shared regression and exact-head CI; those release gates remain root responsibility.

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

| IQ-29-11 | Reporting input could contain balanced derivative/OCI/P&L plugs after source construction while the original Hedge receipt was unchanged. | Author added production `handoffs.py` validator which reexecutes both native owners and binds unique explicit derivative/P&L/OCI/dedicated-equity mappings. Fresh balanced plug, sign reversal, wrong entity/currency, duplicate economics, target aliases and identifiable extra unmapped source-posting regressions pass. Both engines remain unchanged. |
| IQ-29-12 | Whole financial-asset host routing accepted unrelated same-amount FI case or allowance substituted for gross carrying amount. | Author binds current single-instrument FI case identity, actual financial-asset kind, gross-carrying metric, and original instrument identity if present. Independent matching host preserves current ECL62.5 unchanged; wrong case/original ID/metric regressions pass. |

## Scope constraints requiring truthful release reporting

Complex options and excluded components, portfolio/macro techniques, retained IAS39 routes, early US amendments, intragroup exceptional qualification, midperiod independently split accounting and post-discontinuation effective-interest basis amortization currently fail closed. A bounded route should not be described as complete advanced/lifecycle support.

## Execution

`PYTHONPATH=skills:skills/tests:. python -m unittest skills/tests/test_independent_derivatives_hedge.py skills/tests/test_independent_hedge_handoffs.py -q`: 48 independent methods pass after authored remediation. Authored plus independent suites93 methods pass; final targeted total including Inventory is102 methods. Independently recomputed all260 generated artifacts byte-for-byte:52 scenario sets, with52 COMPLETE,52 PARTIAL and52 BLOCKED public results;0 mismatches. Numerous independent mutations execute as subtests. Final promoted-byte rerun and anchors remain outstanding.

Actual production owner integration: independently constructed fixed-rate Debt FV and variable-rate Debt CF cases pass original-source ID/principal/maturity/rate-type binding. Four-framework NI cases consume actual current Consolidation and Foreign Currency owner results and pass; operation mismatch, net-investment excess, wrong translation amount and manufactured disposal fail. Actual current Inventory owner consumes -90 signed basis exactly once into160 closing inventory; refreshed-source receipt quantity/adjustment-ID mutations fail. Existing Fair Value owner is quoted equity only: unrelated current result blocked; complex derivative valuation requires independently qualified external evidence. Hedge reporting includes exact signed GL/statement and P&L/reserve bridges, without producing final statements.

Reporting source validator is deliberately bounded to first-year continuing/rebalanced cash-flow hedges with zero opening balances, settlement, reclassification and basis adjustment. It validates actual completed Hedge and native Financial Statements outputs with exact unique semantic mapping and source population. It does not generate company baseline balances or replace statement-owner accounting. Other reporting routes require their explicit governed adapters.

## Final promoted-byte independent verification

Independent implementation reviewer returned a read-only PASS on 2026-10-04:102 targeted methods, including48 independent methods; all275 artifacts reproduced byte-for-byte; all12 recorded findings resolved;0 open material findings. No files were edited during verification. Final exact-head CI remains the external release gate recorded in PR25.

| Anchor | SHA256 |
|---|---|
| Production SKILL metadata | e51cdf6ef5b6d616dbd1f31c5cf1e4dc2d4a919f45b1435aff9416d02cffa36d |
| Hedge workflow | 99d1e761cddc1f1e9745ca8010cb0b089361beb4b5c19ae6074c1acc54c5d7d8 |
| Native reporting handoff | d4ca94d74b10712c9ea945ed2d6bb071e7c935c169153fed8f3a806e663d323e |
| Inventory workflow | 693b8f44000f83743e4004a45596e4e20818e97fbe7216ee41cf82dfcf28cc5e |
| Shared production boundary | cdbf8a51a5b7e9290c7e1fe5c3c183ba0a028b6537ddd86d35f54d89c70c3de1 |
| Independent accounting tests | 8dd9bbcb1dd29381d7268582baf35a37a12429ba0c3d2edb22878016a1eb0ce5 |
| Independent handoff tests | 2269076f50c9ca7a048603959b7301026bdde50f42f399252ba1b60a1d272487 |
| Canonical map | bc1927bccd8ddc2204731d4406a91e1e3852fab9fabde1ad956739b557b9c6b8 |
| Supplemental map | d142cac62270a8d81eb2649d7b90a0c688ec819bbfdf043514e9087ea19990bf |
