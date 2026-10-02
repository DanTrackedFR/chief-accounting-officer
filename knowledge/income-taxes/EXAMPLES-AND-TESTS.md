# Synthetic examples and independent-reperformance test specification

All amounts illustrative currency units, not company facts or assumed statutory tax rates. Each numerical case assumes an independently supported 25% rate **solely for arithmetic**. Recognition and legal-tax conclusions remain framework-specific.

## A. Tax bases and temporary differences
Equipment carrying amount 1,000; tax base 700; taxable temporary difference 300; illustrative DTL 75. Separately, accrued expense carrying liability 200, tax base zero, deductible temporary difference 200; illustrative gross DTA 50 **only if** applicable recognition/recovery tests pass. Net 25 only if framework and legal offset criteria independently pass. Example origination journals: Dr deferred tax expense 75 / Cr DTL 75; Dr DTA 50 / Cr deferred tax benefit 50. Combined net expense 25; debits and credits each 125 across the two journals. Under FRS 102, independently establish that the differences meet Section 29's timing-difference-plus method; do not import the IFRS conclusion automatically.

## B. Recoverability / valuation allowance
Gross deductible difference 400 -> gross potential DTA 100. Supported recoverable portion 240 -> 60. IFRS/AASB: recognize only supported DTA 60, with 40 unrecognized and tracked; US: gross DTA 100 and valuation allowance 40, net 60, subject to ASC 740-specific assessment. This is an accounting presentation contrast, not a substitute for framework recognition analysis. UK: independently apply the operative Section 29 recovery test.

## C. Rate change
Existing taxable difference 300: opening DTL at 25% = 75. If a legally qualifying new 30% rate applies to reversal, revised DTL = 90; movement 15. Journal Dr deferred tax expense 15 / Cr DTL 15 **if** original item arose in profit/loss; otherwise trace to the relevant OCI/equity/acquisition allocation. IFRS/AASB substantive-enactment assessment and US enactment requirement are separate gates.

## D. Current tax and ETR
Illustrative pretax profit 1,000, taxable-profit reconciliation: +100 permanent nondeductible expense, -200 deductible temporary reversal, +50 current taxable timing adjustment = 950 taxable profit. At supported example rate 25%, current tax 237.50. The statutory-rate benchmark is 250; permanent-item impact +25; net temporary current-tax effect -37.50. Reconcile current and deferred components and other items before stating a total ETR; **current tax divided by accounting profit is not the ETR**. Journal Dr current tax expense 237.50 / Cr current tax payable 237.50, before credits, installments and prior-year true-ups.

## E. Outside-basis / combination / uncertainty adversarial cases
An investment carrying amount exceeding tax base does not automatically create a recognized DTL: test control over reversal and foreseeable reversal under IAS 12/AASB 112 and separately apply ASC 740/FRS 102. Acquisition-date fair-value uplift of 200 with zero incremental tax base -> illustrative DTL 50, normally reflected in acquisition accounting rather than an ordinary operating-tax journal; determine goodwill and relevant exceptions with acquisition specialist. An uncertain tax position with a 60% estimated acceptance probability does **not** establish an identical liability under IFRIC 23 and ASC 740: independently apply each framework's decision and measurement route.

## Regression acceptance matrix
- Four frameworks × current/deferred/uncertainty/combination/share-based/outside-basis/OCI = 28 independently assessed route families.
- Arithmetic: positive/negative differences, zero tax base, losses, recoverability, rate changes, rounding, opening-to-closing rollforward and balanced journals.
- Adversarial: wrong effective period, unsupported rate, wrong UK edition, IFRS vs US uncertain-position interchange, US substantive-enactment misuse, absent forecast, expired losses, unsupported offset, duplicated tax effects on acquisition, OCI misallocation, false SEC/Australian tier, missing reviewer and source-note leakage.
- End-to-end: source-population tie-out -> framework judgment -> current/deferred calculation -> ledger journal -> statements -> ETR -> disclosures -> reviewer signoff -> privacy allowlist. QA owner must implement and execute executable tests against approved knowledge and the eventual skill integration; this file does **not** assert those tests passed.
