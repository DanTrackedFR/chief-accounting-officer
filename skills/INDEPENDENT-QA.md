# Independent QA — four Phase 3 accounting skills

Review date: 2026-10-02. Reviewer: independent QA integration agent, separate from the implementing agent. This reviewer did not edit substantive implementation. Review scope: `AGENTS.md`, `architecture/skill-specification.md`, the approved canonical knowledge and claim registers, four skill contracts and methods, `REVIEWER-CONTROLS.md`, shared execution/public boundaries, workflows, fixtures and tests.

## Gate decision

**PASS for production use of the explicitly supported governed workflows and their specialist-routing boundary.** Final local integration checks and metadata/report alignment passed independent review. Synchronization and green CI for the exact final commit remain the integration controller's gate. This is not approval for arbitrary transactions or autonomous accounting conclusions. The initial bounded engines did not meet this gate; the revised reviewed-case workflows do.

The latest independently executed command was:

```sh
python -m unittest discover -s cao/skills/tests
```

Result: **66 tests passed**. Earlier checkpoints passed 50, 59 and 61 tests. The final suite adds canonical prospective modification, integrated catch-up, matched intercompany, unrealized inventory profit and wholly owned foreign-operation translation cases. Framework-by-skill end-to-end cases cover all 16 combinations of IFRS, US GAAP, FRS 102 and AASB with separately reviewed routes. This reviewer also ran direct counterexample scripts during development, beyond reading the tests.

This reviewer also independently executed the full local integration checks: **17 lease tests passed; 53 other repository tests passed; both standards validators exited successfully with zero errors; `git diff --check` passed**. Approval validation reports 157 approved canonical topics, 347 capabilities and 1,598 claims. Claim validation reports 157 registers and 38 retained historical/noncanonical topic directories without separate registers; approval validation confirms the 157 canonical registers. The final commit/CI/integration gate remains the controller's responsibility.

## Reproduced findings and remediation

Counterexamples below identify behavior found during revision, not behavior asserted to remain in the final implementation. Unless stated otherwise, examples used the synthetic fixtures in `skills/tests/cases.py`, updated reviewer certification through `finalize`, then executed the governed entrypoint.

| Finding and reproducible counterexample | Remediation independently inspected or tested |
|---|---|
| Initial engines accepted `claims=[]`; provisions pointed to equity-note and going-concern topics. | Governed execution retrieves approved canonical claims; provisions uses TOPIC-05-003/004 with the relevant restructuring/judgment dependencies. Legacy engines are internal arithmetic prototypes. |
| Empty `exceptions`, `specialist_items`, contract-cost or intercompany arrays blocked otherwise valid cases; ASC 450 `best_estimate=None` could not reach the minimum-of-range route. | Presence validation allows meaningful empty collections; ASC 450 explicitly distinguishes missing best-estimate decision from an evidenced null decision. |
| Provision outcomes `(amount100, probability-1)` and `(amount200, probability2)` produced 300. | All probability inputs are validated within [0,1], and supported distributions reconcile to one. |
| Cumulative revenue80 with prior recognition30 produced a journal80; opening provision50, settlements20 and closing45 produced reversal5. | Revenue separates cumulative from current period; provision bridge produces current estimate expense15, with settlement separately posted. |
| Revenue price0.02 with four equal SSPs allocated 0.01,0.01,0.01,-0.01. | Deterministic largest-remainder cent allocation reconciles without a negative residual. |
| Variable consideration execution mutated the case by inserting `estimate_result`, invalidating certification. | Calculation no longer mutates the case; case immutability regression passes. |
| Legacy UK unreliable service recovery multiplied a fraction by price rather than using recoverable costs. | Absolute recoverable-cost revenue is used; legacy component consideration and model/election are explicitly resolved. |
| US amortized-cost debt with `impairment_model='none'` certified a zero allowance/reversal. IFRS lease receivable `measurement='ANY'` certified an unknown category. | Invalid kind/category/model combinations are rejected; liability and equity schedules have separate supported measurement routes. |
| Asset-style interest journals were applied to debt liabilities; zero discount factors eliminated expected losses. | Liability EIR debits finance cost and credits liability. Credit discount factors must be positive; unsupported signed-yield mechanics route to specialists. |
| AFS cost100, FV80 and credit loss10 posted allowance10 plus OCI valuation adjustment20, leaving asset70. | Noncredit adjustment10 plus allowance10 leaves carrying value80; regression passes. |
| Prior FV adjustment-20 and current required-10 reposted the closing adjustment instead of reversing10. | Opening valuation adjustment is required; only its period movement is journaled. |
| Decommissioning liability decrease5 credited restoration asset5 without knowing whether any asset remained. | Cost-model carrying floor and remaining life are required; carrying3 produces asset reduction3 and gain2; exhausted/revaluation routes are separately handled. |
| Consolidation accepted nonexistent intercompany entities, duplicate schedules and unsupported investment balances; NCI closing22 did not reconcile to group NCI20. | Entity/account source populations, parent investment tie, duplicate checks and separate NCI attribution reconcile the consolidated balances. |
| String `parent='false'` bypassed control; wholly owned NCI retained an unexplained opening20. | Exactly one evidenced boolean parent is required; wholly owned nonzero NCI is rejected absent a supported resolved route. |
| FX/other bridge amounts lacked corresponding journals; later zero-movement inputs could append journals altering the declared closing balance. | Event journals are balanced and their account deltas must match the bridge whenever journals exist, including zero declared movements. FVOCI allowance uses its OCI account in the FX tie. |
| Stable claim IDs could retain old certification after claim content changed; code changes were not fingerprinted. | Claim-register bytes and implementation bytes participate in the reviewed knowledge/case certification chain. |
| Missing promise IDs and malformed nested inputs escaped the CAO boundary as exceptions rather than results. | `assess_case` returns a structured blocked envelope and specialist handoff for supported packages; CLI uses this adapter. Unknown packages are explicitly rejected. |
| No usable public workpaper/export boundary existed for these workflows. | Public CLI and seven registered routes use the existing allowlist; generated calculations, journals, review state and disclosure requirements are curated, while raw claim/reviewer metadata remain internal. |

## Supported scope and explicit boundaries

- Revenue: reviewed customer-contract gate, pricing/constraint inputs, SSP or evidenced specific allocation, point-in-time/over-time and legacy UK routes, supported modifications, cumulative/current-period bridges and contract costs. Legal enforceability, complex licences, mixed contracts, financing valuation and complex events remain independently supported inputs or specialist cases.
- Instruments/ECL: supported asset classification and general/simplified IFRS/AASB, US CECL/AFS and UK incurred-loss/elected-model routes; term/scenario arithmetic, gross/allowance/FV bridges, ordinary liability EIR and eligible equity FV schedules. POCI/PCD, IAS 39, guarantees/commitments, derivatives/hedges, complex own-credit, negative yields and specialized FVOCI/events require the named specialist evidence rather than forced generic calculation.
- Provisions: independently evidenced obligation/probability thresholds, framework-specific range/best-estimate measurement, discount/unwind/settlement and supported event bridges, gross separate recoveries, onerous/restructuring boundaries and cost-model restoration interaction. Gain contingencies use a separate asset route; legal opinions, US exit/ARO exceptions and revaluation mechanics remain specialist dependencies.
- Consolidation: framework-specific reviewed control perimeter, certified aligned TBs, supported translation, investment/equity elimination, source-matched intercompany eliminations, supported profit/tax/event entries, NCI attribution and statement/equity/cash-flow/CTA ties. Acquisition valuation, hyperinflation, equity-method/JV and complex disposal/control exceptions retain explicit specialist handoffs.

Accounting judgments and source evidence are reviewer inputs by design. Memos/booleans do not themselves establish legal rights, control, an independently verified forecast, a human identity or posting permission. Case completion requires the exact independent signoff and resolved workflow gates. Unsupported or unresolved cases return `blocked`; stale or absent approval returns `partial`. No ERP posting is authorized by this QA result.

## Methods, evidence and public-output assessment

The four `methods.md` files align with the implemented supported routes, numerical bridges and specialist boundaries. Representative full claim IDs referenced in the methods were checked against canonical registers and found present. `REVIEWER-CONTROLS.md` correctly separates evidence review, certification, illustrative account mapping and posting controls, and distinguishes CAO-facing `assess_case` from the internal `execute` certification engine. Gain methods explicitly define the input as closing outstanding receivable after receipts, not total award plus already received cash. The four skill contracts are version 1.0.0 with production status for this supported scope; the consolidated handoff report consistently preserves its specialist boundaries and evidence limitations.

The review assessed accounting consistency against the approved repository knowledge. **No direct-source evidence rating was promoted.** APPROVED topic status does not imply SOURCE_VERIFIED authority. Training-data-derived claims retain their evidence status, direct-source audit requirement and provisional pinpoint limitations. This QA is not a new operative-standard paragraph audit or licensing clearance.

Public-output tests and inspected adapters support the repository's contract boundary, not an assertion that an unrelated deployed renderer has been audited. Internal source notes, claim evidence labels, hashes and reviewer records must continue to be excluded. Material accounting uncertainty and reporting-period qualifications must remain visible in ordinary guidance.

No unresolved demonstrated accounting/arithmetic defect remained in the reviewed supported routes after the documented fixes and final 66-test run. New material rules or scope expansion require renewed versioned regression and independent review.
