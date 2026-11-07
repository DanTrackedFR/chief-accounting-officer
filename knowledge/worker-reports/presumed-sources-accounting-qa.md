# Profile 1.2 — independent accounting QA

Reviewer: independent accounting QA agent. Scope: ordinary machinery cost-model
depreciation/disposal and ordinary supplier-cost AP, under the existing governed
2026 framework qualification. No production file was edited by this reviewer.
Tests were independently authored from source facts rather than copied from the
implementation author's fixtures. This is accounting-method QA, not independent
certification of customer records or a new direct-source standards audit.

## Accounting basis and boundaries

The approved canonical applied examples for TOPIC-04-001/002/003 and
TOPIC-05-001 were read together with the existing production workflows, Profile
1.1 contract and Build 2B handoff. No canonical claim, approval, evidence status,
effective-period qualifier or historical numerical artifact was changed.
IAS 16/AASB 116 and the applicable UK/US cost-model routes support the bounded
machinery calculations; ordinary AP remains a control/recognition method, not an
assertion that one provision standard governs every supplier liability.

Independent numerical anchors are:

- Machinery: (600,000 cost − 180,000 accumulated − 60,000 residual) / 4 remaining
  years = 90,000 full-year charge; closing carrying amount = 330,000.
- Ordinary year-end sale: 400,000 proceeds − 330,000 carrying = 70,000 gain;
  gross cost and accumulated depreciation clear separately.
- Production units: (600,000 − 180,000 − 60,000) × 250 / 1,000 = 90,000,
  without requiring an unused year-life input.
- Supplier invoice: 12 units × 10 = 120; absent opening and payments are unknown,
  not zero, so no closing AP is invented.
- Unbilled service: 12 × 800 = 9,600 closing obligation. A known 9,000 opening
  accrual supports a 600 adjustment; absent opening supports the closing amount
  but does not support a numerical adjusting journal.

## Findings reproduced and remediated

1. Current-period invoice expense could be calculated with goods/services receipt
   date missing or preceding the reporting period. Receipt dates are now required
   for those recognition bases; unsupported cutoff/opening routes remain unresolved.
2. Accrual rows did not receive the specialist screening applied to invoices.
   Supplier-financing and other specialist indicators now prevent affected accruals.
3. Residual exceeding carrying amount incorrectly blocked an otherwise supported
   zero-depreciation determination. The bounded charge now remains zero with a
   specific residual warning; no alternative company estimate is substituted.
4. Units-of-production demanded unused remaining year-life evidence. Inputs are
   now method-specific.
5. Supplied opening accrual balances were ignored, producing a duplicate full
   liability proposal. Explicit opening supports the delta; missing opening omits
   the adjustment while retaining supported closing-obligation calculation.
6. An explicit finance-lease description could silently pass ordinary PPE screening.
   Recognizable supplied textual indicators now route the affected row for evidence.
7. Invalid comparison-only GL or control totals discarded supported individual-row
   calculations. Those comparisons now restrict population reconciliation and
   preserve safe row arithmetic.
8. The later ordinary-capital-cost enhancement exposed three further candidate
   issues: cost-row specialist facts were not propagated to the destination;
   unsupported destination scope retained a PPE acquisition proposal; and a
   capitalization threshold was applied to individual invoice lines instead of
   the supported asset unit of account. Executable reproductions are retained in
   `cost-challenge.log`. Specialist facts now apply to source cost and qualified
   target; unsupported destinations cannot receive PPE acquisition proposals;
   threshold assessment uses the supported asset cost unit, not invoice-line
   splitting. All three remediations passed the 47-test rerun retained in
   `cost-remediation.log`.
9. A fully expensed new low-cost unit with zero opening balances still demanded
   unused useful-life input and remained unresolved. The supported expense route
   now produces zero PPE/depreciation without that artificial requirement.
   Nonzero historical carrying balances below a threshold remain unresolved.
   The initial failure is preserved in `threshold-expense-challenge.log`.
10. Optional stale/incomplete comparison norms wrongly blocked otherwise supported
    row inputs. Unqualified norms now yield NOT_PERFORMED rather than supplying
    a substitute useful life, amount or accounting assumption. Class assumptions
    actually needed for calculation retain their applicability gates.
11. A capitalization threshold supplied once in the destination asset's qualified
    class policy was not inherited by linked costs unless repeated there. The
    supported unique-destination linkage now preserves that policy applicability.
12. Final read-only review identified three evidence/presentation boundaries:
    invoice-only sources cannot establish zero closing accruals; no supported
    asset rows cannot establish zero financial aggregates; and destination
    readiness/entity/currency exceptions cannot leave a supported PPE proposal.
    Public output must show actual row assumptions when those override supplied
    class defaults, together with explicit user assumptions. Permanent tests
    cover these boundaries and their final remediation result is recorded below.

Initial failing executable evidence remains in
`skills/presumed-sources/release/accounting-qa/first-challenge.log` and
`second-challenge.log`. The first log contains two substantive failures plus an
overly specific reviewer assertion about the residual warning's check identifier;
the assertion was corrected to test the material warning content. Logs are
exploratory candidate evidence and are not exact-final-head release receipts.

## Permanent independent challenges

`skills/tests/test_presumed_accounting_qa.py` contains 48 distinct unittest
methods. Subtests/framework repetitions and reruns are not counted as additional
tests. Coverage includes class-policy applicability, source immutability, missing
life, qualified norms without substitution, no-norm NOT_PERFORMED, duplicate asset
and invoice isolation, invalid first-row amounts with later-row survival, readiness
and disposal chronology, routine expense classification, invoice arithmetic,
currency, receipt cutoff, accrual/invoice overlap, supplied supplier differences,
GL/control restrictions, missing opening balances, proposed-journal balance,
host opt-in, recursive review injection, public privacy and provenance.

Earlier targeted result: **36 tests passed, no failures/errors/skips**; full log
is `skills/presumed-sources/release/accounting-qa/current-challenge.log`.
The final combined targeted suite is **48 independent + 8 authored tests**.
The independent reviewer also inspected the author's eight tests rather than
counting them as independently authored. No case, framework subtest or repeated
execution is counted as an additional distinct test.
Earlier cost-release candidate: **48 passed, no failures/errors/skips** using
`PYTHONPATH=skills:skills/tests:. python -m unittest skills.tests.test_presumed_accounting_qa skills.tests.test_presumed_authored -v`.
The complete targeted log is
`skills/presumed-sources/release/accounting-qa/final-targeted.log`.
The final-evidence challenge expanded coverage to 56 methods. Its pre-remediation
log is `final-evidence-challenge.log`; that run retained six failing assertions
across four methods for the final boundaries in finding 12. Candidate approval
then followed the unchanged-suite remediation rerun: **56 tests passed, no
failures/errors/skips**. Complete log:
`skills/presumed-sources/release/accounting-qa/final-evidence-remediation.log`.
All reproduced substantive accounting findings in this review are resolved in
the tested candidate. The suite contains 48 independent methods and eight
implementation-author methods; the six earlier failing assertions included
three destination-scope subtests and are not six additional test methods.
Complete repository regression, deterministic release artifacts, frozen SHA and
exact-head GitHub Actions remain the release owner's responsibility.

## Remaining bounded limitations

Only the two documented packages and existing qualified commercial 2026 framework
routes are covered. No FX conversion, lease/impairment conclusion, unsupported
movement route, generic useful life or company policy is invented. No supplied-file
completeness or authenticated-user assertion becomes independent certification.
GL agreement does not prove absent liabilities or completeness. Supplier aggregate
comparison does not establish supplier-by-supplier reconciliation without the
necessary movement population. Screening is deterministic and bounded by supplied
facts; a passed check is not proof that an undisclosed issue cannot exist.

No actual customer workbook has been independently authenticated or certified by
this QA. Synthetic fixtures are labeled synthetic. Original external workbooks,
if unavailable to the release owner, must not be represented as tested originals.
