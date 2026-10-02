# Phase 3 — four additional core accounting skills

This branch introduces governed contracts and executable bounded workpapers for Revenue Recognition, Financial Instruments/ECL, Provisions & Contingencies and Consolidation. All four remain **REVIEW**. The deterministic workpapers are not equivalent to full production accounting skills.

| Skill | Implemented bounded calculation | Important work still required |
|---|---|---|
| Revenue | SSP allocation, evidenced partial satisfaction, basic revenue/billing bridge and journals | Full five-step contract engine, framework/period branches, variable consideration constraint, modifications, principal/agent, contract-cost and presentation accounting |
| Financial Instruments/ECL | Explicit IFRS 9/ASC 326 route gates, scenario-weighted scalar ECL and allowance journal | Instrument classification/measurement, stage transitions, term structures, CECL methods, collateral, write-offs, disclosure rollforward and UK routes |
| Provisions | Reviewed expected-value/most-likely/ASC 450 input gates, discounted estimate where approved, movement journal | Recognition decision tree, onerous/restructuring/decommissioning/reimbursement, ASC 450 range logic and full disclosures |
| Consolidation | Reviewed perimeter input, aligned trial-balance aggregation, matched intercompany balance elimination | Control/VIE analysis, investment/equity elimination, NCI, FX, unrealized profit, acquisitions/disposals, cash-flow and full statement tie-out |

## Shared safeguards

Framework/period/entity gates; no invented input facts; approved canonical claim retrieval with evidence tiers preserved; Decimal arithmetic; balanced journal checks; explicit specialist routing; unit tests. The result envelope is `partial` pending human review and downstream implementation.

## Completion gate

Do not promote any of these four skills to `production` until the outstanding framework-sensitive decision logic, realistic worked cases, numerical and adversarial regression, governed paragraph citations, public-output integration and independent QA have been completed.
