# TOPIC-02-009 — Prior-Period Errors & Opening-Balance / Roll-Forward Integrity

Manifest status: PARTIAL (QA owns promotion). Worker proposal: substantively REVIEWED-ready, with isolated ASC authority audit.
Capabilities: CAO-02-019, CAO-02-020
Knowledge: PRINCIPLES + STANDARDS + PRACTICE
Framework sensitivity: MEDIUM
Source/evidence check: 2026-09-29; see `standards-claims.json`.

## Phase 2D completion entrypoint

Read `methods/phase-2d-error-correction.md` for the full four-framework recognition, presentation, disclosure, materiality, interim, SEC registrant, opening-balance, controls and systems method. Read `tests/phase-2d-worked-error-cases.md` for five recalculated and adverse cases. `standards-claims.json` identifies each normative assertion's source, evidence tier, effective period and audit queue. The earlier README/factory, restatement bridge and alternate same-ID paper are preserved as supporting material. Claim-level ASC authority remains provisional without current Basic View inspection; this does not prevent substantive independent QA.

## Objective
Distinguish errors from estimate changes and policy changes, correct material errors under the applicable framework, and prove opening balances and rollforwards preserve accounting continuity.

## IFRS / AASB
IAS 8 and AASB 108 define prior-period errors around failure to use or misuse reliable information that was available, or reasonably obtainable, when prior financial statements were authorized. Material prior-period errors are corrected retrospectively by restating comparative amounts unless impracticable. Estimate changes arise from new information/developments and are recognized prospectively. Accounting-policy changes are generally retrospective unless specific transition or impracticability applies. [IFRS-01, IFRS-02, AU-01, AU-02]

AASB 108 inspected compilation applies for periods beginning on/after 1 January 2023; check later amendments and Tier 2 disclosure scope. [AU-02, AU-03]

## UK GAAP
Use FRS 102 Section 10 Accounting Policies, Estimates and Errors for classification and correction, with period/version routing. Do not infer UK treatment solely from IAS 8. [UK-01, UK-02, UK-03]

## US GAAP
Use the authoritative FASB Codification, particularly the accounting-changes/error-corrections literature applicable to the entity and SEC overlay where relevant. FASB Concepts Statements are not authoritative GAAP.

For the error-specific ASC paragraph inspection list and direct-access limitation, see `canonical-sources.md`. For the completed SEC registrant materiality, Big R/little r/out-of-period and Item 4.02 decision route, see `practice/us-issuer-overlay.md`. The issuer route does not certify current ASC paragraph applicability.

## CAO decision tree
1. Establish what was known/available at original authorization date.
2. Identify whether current information is genuinely new or reveals misuse/omission of prior available information.
3. Classify: error, estimate change, policy change, or fact-pattern change.
4. Assess quantitative and qualitative materiality individually and collectively.
5. Determine required correction method and comparative/opening-equity effects under framework.
6. Quantify tax, EPS, covenant, compensation, regulatory and disclosure effects where applicable.
7. Reconcile corrected closing balances to next-period opening balances.
8. Document cause, control deficiency, remediation and disclosure.

## Opening-balance integrity
For every material balance: prior closing audited/reported amount + approved restatement/reclassifications + FX/consolidation/perimeter changes = current opening amount. Migration openings additionally trace source-to-target account mapping, entity/dimension mapping and conversion rules. Differences require explicit disposition; never force-balance with undocumented plugs.

## Controls
Opening-balance tie-out; rollforward continuity; restatement ledger; mapping approval; error log; materiality review; disclosure tie-out; migration control totals; no direct opening-balance postings without approval/evidence.

## Artifacts
Error-v-estimate memo; materiality assessment; correction JE/restatement schedule; opening-balance bridge; rollforward; disclosure support; remediation plan.

## Tests
New customer default caused by post-year-end event may update an estimate rather than prove error; spreadsheet formula omitted known invoices is an error. Migration difference cannot be cleared to suspense without root-cause evidence. Material prior-period error cannot be hidden in current-period expense.
