# Independent accounting QA — optional review mode

Independent reviewer authored `skills/tests/test_prepared_accounting_qa.py`,
inspected canonical approval/source governance and existing operational owners,
and did not edit accounting implementation. Reviewed baseline:
`fbf8bb9a092955d2cd5fbf728c85e6dc62f4bd1c`; branch:
`feature/prepared-accounting-execution`.

**PASS: 29 independent tests, 7.357 seconds, zero failures or errors.**

Command: `PYTHONPATH=skills:skills/tests:. python -m unittest skills.tests.test_prepared_accounting_qa -v`.
Raw receipt: `skills/prepared-accounting/release/accounting-qa/final.log`, SHA-256
`40dc24cbebca1bf59e94d0311204f2f1325b882a0582a09962af40b7f9909190`.
Test source SHA-256: `75ab11690ba54839af4f997b0cb599a8e69c5109c16e34c5e618a2498a237e31`.
Prepared implementation SHA-256 at this execution:
`19b9c34e59c8fbaab9f079b7db8aadbe01604c948e92985b520410ce1547291d`.
Production dispatcher SHA-256 at this execution:
`039fa1731344eb053d793f3c384d77c21373952bf6b33647ff75f9a9ce3c9d12`.
Release owner must bind these tests to final source and remote gates.

## Independently reperformed economics

| Owner | Independent expectation | Verified result |
|---|---|---|
| Fixed assets / machinery | (600,000 cost − 180,000 opening accumulated depreciation − 60,000 residual) ÷ 4 remaining years | EUR 90,000 depreciation; closing accumulated 270,000; carrying amount 330,000 |
| AP / supplier cost | 12 received units × EUR 800 − zero invoiced receipt | EUR 9,600 accrual; EUR 20 closing AP from 120 invoiced less 100 paid |
| AP subsequent backtest | 10,400 subsequent invoice less 9,600 estimate | EUR 800 variance remains a backtest; supplied January service evidence does not silently increase the December accrual |

Native owners execute, input Cases remain unchanged, and proposed workpaper
journals balance. Native posting implications remain empty; public journal
implications are proposals requiring separate posting authorization.

## Reviewed safeguards

Both packages return SUPPORTED / SUFFICIENT / SYSTEM_PREPARED with truthful native
partial status. Missing material evidence returns blocked accounting, UNRESOLVED /
INSUFFICIENT, a specific public evidence issue and no numerical conclusion.
Supported calculations gain no universal independent-signoff open item. Formal
certified fixtures retain complete status and unchanged economics.

The suite challenges missing facts, incomplete/mismatched source populations,
source self-approval, stale/future source approvals, unresolved/mismatched handoffs,
unsupported asset model/method/scope/readiness, missing receipts, currency/cutoff/
reversal errors and payment segregation. Source-evidence controls remain mandatory
and distinct from execution-review signoff.

Positive economics pass for narrow 2026 for-profit IFRS, US private company,
UK FRS 102 and AASB routes, including AASB Tiers 1 and 2. Negative tests cover
other years, unknown elections, unsupported frameworks, UK FRS 101/105/wrong
edition, Australian invalid/bool tiers and NFP/public sector, regulated/public US
scopes and explicit regulatory overlays. New-mode UK/AASB 2026 selectors are
bounded implementation qualification tokens; this review does not claim that
these tokens independently verify operative standards.

Injected knowledge/applicability/signoff records, including null and empty records,
are rejected. Machine sentinel review cannot certify formal Cases. Other owners
cannot enter the mode; changing mode changes the Case fingerprint. CONFLICTED or
NOT_RESEARCHED canonical assurance blocks execution.

Final safeguard audit added an independent regression for relabelled system records.
For both owners and all three formal review record roles, a non-human worker name
with provenance SYSTEM_DERIVED or origin SYSTEM_PREPARED is rejected explicitly
by the system-provenance gate. The test recomputes signoff fingerprints so stale
signoff cannot mask a bypass. The author's generalized reserved-tag guard passes
all 12 combinations. Earlier 26-test receipt remains preserved as
`skills/prepared-accounting/release/accounting-qa/pre-provenance-extension.log`.

All seven public routes retain numbers while excluding reviewer names, raw knowledge
documents/claims/hashes and private source metadata. Material assumptions, treatment
requirements and proposed journal account implications remain visible. Provenance
injected through assumptions fails closed. Package citations are background guidance
with no manufactured claim-level locators. Canonical source assurance is not promoted;
this is not an operative source-text audit.

## Findings and resolution

**AQ-PREP-01 — public explanation incomplete: resolved.** Initial renderer emitted
only reconciliation conclusion/numbers, omitting requirements, material assumptions
and journals. Author added deterministic treatment explanations, assumptions and
proposed journal implications. Permanent independent public-output test passes.
One interim wording assertion was corrected to recognize equivalent “ready for use”
and “available for use”; that was test vocabulary, not a production defect.

**AQ-PREP-02 — owner mismatch accepted: resolved.** Independently reproduced
`execute('fixed-assets', case_with_package_accounts_payable, allow_prepared_unreviewed=True)`
returning supported EUR 90,000. Early opt-in dispatch bypassed formal owner
consistency. Author added the equivalent prepared qualification guard. Permanent
regression rejects both mismatch directions. Failing 23-test run preserved in
`skills/prepared-accounting/release/accounting-qa/owner-mismatch-reproduction.log`.

**AQ-PREP-03 — supplier profile implied blanket provisions applicability: resolved.**
Final accounting audit challenged internal AP selectors naming IAS 37/AASB 137
as if those standards governed every ordinary supplier obligation. Ordinary trade
payables and many contractual accruals are financial liabilities; provisions are a
distinct scope. Mandatory recognition handoffs mitigated calculation risk but did
not justify misleading applicability provenance. Author replaced all AP selectors
with the neutral “Governed ordinary supplier-cost reconciliation profile, 2026”.
No numerical result, canonical claim metadata or source-assurance status changed.
Permanent independent regression checks all four supported frameworks, exact neutral
system-derived profile, separately retained framework, unchanged canonical knowledge
population/documents and absence of invented applied claim IDs/evidence. A Git diff
against baseline confirmed no canonical topic standards-claims, manifest or
standards-evidence changes. Previous 27-test receipt is preserved in
`skills/prepared-accounting/release/accounting-qa/pre-supplier-profile-correction.log`.

**AQ-PREP-04 — blocked rendering implied unsupported accounting scope: resolved.**
Release author's final refusal audit found the common prepared renderer defaulted
non-FA blocked owners to AP treatment and background guidance. Although it emitted
no supported number, it could imply that supplier accounting applied to an
unsupported package or unqualified period. Author added a separate early refusal
renderer within the existing public boundary. It returns only the precise issue,
open items, qualified dimensions and UNRESOLVED / INSUFFICIENT / SYSTEM_PREPARED;
there are no treatment assertions, calculations, proposed journals or citations.
Permanent independent regression checks two unsupported owners, missing evidence
in both allowed owners, and future periods in both allowed owners across all
seven public routes (42 refusal combinations). All retain specific refusal reasons
and omit invented AP/FA treatment, background claims and supported numbers. Earlier
28-test receipt is preserved in
`skills/prepared-accounting/release/accounting-qa/pre-refusal-renderer-correction.log`.

A preliminary run before implementation API wiring produced signature TypeErrors;
it is not counted as substantive implementation testing.

## Limits and acceptance

No substantive accounting finding remains open in this native scope. Fixture source
approvals are synthetic, not authenticated professional sign-offs. Source-row,
completeness and specialist-handoff evidence remain required; the enhancement removes
mandatory named execution review, not evidence sufficiency. Reviewer did not rewrite
canonical knowledge, historical accounting references or production calculations.

This receipt covers native accounting QA. Full repository regression, HTTP,
restart, idempotency, isolation, remote exact-head Actions, mergeability and final
freeze require separate engineering/release receipts. No completion claim for
those gates is made here.

