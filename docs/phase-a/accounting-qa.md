# Phase A independent accounting QA

Reviewer: independent accounting QA agent (`accounting_qa`), separate from implementation.
Tested production SHA: `fa1734070c0781d5e4b44f18bb97381c6204e582`.
Date: 2026-11-07. Scope: corrected Phase A machinery calculations, policies,
comparisons, public assumptions/journals and representative hosted durability.

**Conclusion: PASS for the bounded Phase A accounting implementation and focused
integration QA described below. This is not full release acceptance or original-upload
TrackedFR integration acceptance.** No unresolved accounting defect was found in the
reviewed corrected paths. No production edits were made by this reviewer.

## Execution evidence

Command from repository root:

```sh
PYTHONPATH=skills:. python -m unittest skills.tests.test_phase_a_independent_accounting -v
```

Result: **16 tests, PASS**, 2.519 seconds. Full output:
`docs/phase-a/accounting-qa-final.log`.
Permanent reviewer-authored tests: `skills/tests/test_phase_a_independent_accounting.py`.
Numerical expectations were independently authored before implementation in
`accounting-qa-plan.md`; they do not call the production charge helpers to calculate expected
figures. The tests call production helpers only as the system under test.

Two representative tests execute an actual authenticated localhost HTTP server using
`/v1/operations`, `/v1/jobs`, persisted native Case workpapers, result reopening and job
retry/service reopening. Existing test harness code supplies transport/configuration only;
the numerical assets and adverse mutations are independently authored. No live customer
service or original customer register was available to this reviewer.

## Independent calculations and actual results

Common asset: opening gross 79,200; opening accumulated 18,000; residual 3,600;
remaining depreciable basis 57,600; remaining life 24 months (=2 years).

| Independent scenario | Expected | Actual |
|---|---:|---:|
| May monthly charge | 57,600/24 = 2,400.00 | 2,400.00 |
| May actual-day charge and no-election compatibility | 28,800 ×31/365 = 2,446.03 | 2,446.03 |
| February 2026 actual-day charge | 28,800 ×28/365 = 2,209.32 | 2,209.32 |
| February monthly charge | 2,400.00 | 2,400.00 |
| Leap February arithmetic, monthly | 2,400.00 | 2,400.00 |
| Leap February arithmetic, actual-day | 28,800 ×29/366 = 2,281.97 | 2,281.97 |
| May 11–31 reporting stub, explicit actual-days-in-month | 2,400 ×21/31 = 1,625.81 | 1,625.81 |
| Mid-month addition, cost 57,600, available May 11 | 1,625.81; closing NBV 55,974.19 | Same |
| Credit disposal May 19, consideration 62,000 | Depreciation 1,470.97; gain 2,270.97 | Same; disposal receivable, no cash entry |
| Basis 45,360; 12/24/36/60 months | Monthly 3,780/1,890/1,260/756 | Same; equivalent years and both consistent fields agree |
| Basis 128.55, life 0.5 month, residual 100 | Cap charge 128.55; closing NBV 100 | Same |
| Residual above carrying amount | Zero charge with warning | Same; no nonzero journal |
| Closing NBV supplied 318,800 vs calculated 58,800 | +260,000 variance, unchanged charge/journal | Same |
| May then June: opening accumulated advances to20,400; life23months | June2,400; combined4,800; JuneNBV56,400 | Same |

Leap-year arithmetic is unit-tested without broadening hosted source scope: a 2028 Case
remains rejected/unresolved under the existing 2026 boundary.

## Accounting and integrated challenges

- Positive years-only, months-only and consistent both-fields inputs agree for 12, 24,
  36 and 60 months under both conventions; inconsistent fields withhold journals.
- Zero, negative, null and nonnumeric life produce specific field diagnostics. Mixed Cases
  retain only the valid asset's 2,400 charge and proposal. Fully depreciated zero-life
  assets are unresolved with no invented disposal; they may remain in use.
- Partial-month stubs/additions with no explicit treatment withhold dependent journals;
  `actual_days_in_month` supports the independent amounts above.
- Confirmed applicable company monthly policy is applied and provenance identifies a
  client-asserted confirmed company policy. Conflicting current elections and expired
  policy applicability block journal calculation.
- Default actual days is explicitly `engine_default_unconfirmed`, never represented as
  user-confirmed policy. Explicit row residual wins over a conflicting class default;
  after removing the row residual, only the class value actually used is exposed with
  class provenance. Unused class life and private policy identity do not leak.
- Opening comparisons use opening gross/accumulated, closing comparisons use closing
  values, disposed closing balances are zero, and partial comparison evidence does not
  invent missing supplied values. A260,000 mismatch creates no balancing journal.
- An authenticated hosted mixed Case combines monthly depreciation, material balance
  mismatch and a second exhausted-life asset: overall determination stays UNRESOLVED;
  only the valid first row has proposals, applied assumptions or comparisons. Native
  and public journal lines agree exactly and balance. Reopening returns identical outputs.
- Hosted public proposals retain row references and proposals-only qualification.
  `journal_entry_implications` remains empty, so no posting authority is introduced.
- All four supported framework selectors calculate the bounded scenario; an NFP Case
  is withheld. Existing standards/knowledge approval and framework boundaries are not
  independently reapproved by this numerical correction review.

## Findings and dispositions

No corrected-production accounting defect was identified in these scenarios. Two initial
reviewer test failures were fixture/assertion errors, not production defects: a May Case
was first submitted against the annual company context and correctly rejected for identity
conflict; the fixture was corrected to May. A native Decimal amount was initially compared
to a string; the assertion was corrected to Decimal. No production behavior or existing test
was weakened. The initial/final logs preserve the verification history.

## Final historical-workpaper compatibility recheck

Engineering independently identified H01 after the first production freeze: accepted
historical workpapers lack the new `journal_rows` metadata. The final reviewed commits
`da493a66` and `b86e247b` preserve read access and original guidance without guessing row
lineage, mutating historical workpapers or replaying accounting. They omit new structured
proposals on such reads and add `integration.historical_journal_lineage` as a separate
integration migration requirement/limitation. The existing historical accounting
determination is retained; this migration requirement does not falsely recast a prior
accounting conclusion as newly executed or reviewed.

The independent 16-test suite was rerun successfully at the final SHA above. Additionally,
a direct historical-shape public-read probe verified native workpaper and result equality
before/after serialization, original 2,446.03 amount retention, no invented structured
proposals, the explicit migration requirement and absence of new convention lines from
historical guidance. Probe output: `accounting-qa-historical-read.log`. This accounting
probe is a shape/immutability test; engineering owns the stronger actual accepted97d
persisted-store red/green evidence. No new accounting calculation logic was added by H01.

## Final units-of-production disclosure challenge

The final source `fa173407` narrows new convention prose to rows that actually used
an `applied_depreciation_policy`. Independent recheck: all16 accounting tests pass
at this final SHA. A fresh UOP-only scenario uses opening79,200 minus accumulated18,000
minus residual3,600 =57,600 basis,13 period units and160 remaining units: expected and
actual charge4,680.00. Public journal amount agrees; neither a calendar convention nor
years/months life-unit assumption is represented as applied. Adding a separate
straight-line row gives total7,126.03 (=4,680+2,446.03), with the actual-day convention
assumption attached only to the straight-line row. This corrects an explanatory
precision issue without changing amounts. Probe output: `accounting-qa-uop.log`.

## Policy memory qualification limit

Native CompanyMemory remains CONTEXT_ONLY. That is an authority boundary, not a confirmed
accounting-policy registry. A remembered candidate may inform the next request, but the
adapter/user must explicitly confirm it into entity/framework/period-qualified `asset_policy`
before it governs calculations. Automatic authoritative reuse of native memory is not
provided and must not be advertised. A remembered policy must not silently become a
confirmed company policy or a policy change. Within this boundary, the implemented conflict
checks and documented resubmission requirement are a safe bounded policy-precedence
contract. Independent accounting acceptance here does not claim an automatic memory
promotion mechanism exists.

## Remaining acceptance

Original Phase A files, including Pulse Restore, require separately owned TrackedFR adapter
retesting. The original release receipt does not cover this corrected source. Full release
regression/governance acceptance must be separately authorized. No full historical release
regression, merge, deployment or historical evidence rewrite was performed by this reviewer.
