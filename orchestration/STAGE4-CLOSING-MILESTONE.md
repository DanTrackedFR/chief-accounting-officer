# Closing-date accounting milestone — current Group accounting proved; Stage 4 incomplete

Starting live PR #37 head: `99d15a5c711cd7bd3e0f0f7099ad0f002a856901`.
Existing branch `orchestration/multi-entity-multi-period-flagship`; existing PR remains draft/open/unmerged. Obtain ending immutable head from live GitHub. All original fixtures, 40 checkpoint artifacts and QA history are preserved.

## Supported correction and actual native answer

The pre-implementation contract inspection is `STAGE4-CLOSING-CONTRACT.md`.
Fresh synthetic separately reviewed treasury sheet `TREASURY-CLOSE-2026-10-31-03`
records GBP/USD 0.90, EUR/USD 0.90 and EUR/GBP 1.00 on 31 October.
The original UK 0.80 quote is separately identified as the obsolete September
quote in the export; its original source and native results remain immutable.
USD20 principal, legal book GBP16, UK receivable/US payable, agreement, economic
identity, Case, Scope, Period, framework and currencies remain exact.
The independent UK closing GL18 and opening operation ledger cash100/loan16/
capital116 are supplied evidence, not orchestration targets. A fresh sealed
replacement inventory contains the native workpaper and exact source Fact binding.

Unchanged native Intercompany computes GBP18 closing and GBP2 FX gain, with one
UK-owned Dr receivable / Cr FX journal. Native Foreign Currency consumes the
exact carrying and profit versions; presentation is EUR18/profit2, CTA0, with
no duplicated legal journal. The US side remains USD20/EUR18. Separately reviewed
reporting-basis books18/18 and closing USD/EUR quotes0.90/0.90 go through the
existing ordinary-loan reassessment: commercial principal remains USD20, both
native reporting carrying amounts are EUR18, and no second FX journal is emitted.
Four exact transformation receipts revalidate. Original residual EUR-2 million;
current residual EUR0.00. There is no asymmetric residual elimination or plug.

An independent local-only quote0.85 plus supplied GL17 produces native17/gain1
and translation17. It cannot qualify as a coherent full Group feed against the
retained quotes. This proves the owner does not target18. No residual-dependent
rate algorithm exists.

## Version, dependency and current population proof

Original UK legal version:
`version:c98a94e6c56889dbf946b1cc7366d775a8a144be521b02349a895ee94f7b7fe8`.
Whole-operation control replacement:
`version:5083f67c9bde9d956424b81a052d3f348083d4da868f5b78699132c6ad64c3a3`.
Original is SUPERSEDED, replacement CURRENT; the original object is unchanged.
The preserved earlier opening-correction control is not replaced or rewritten.

Actual edges derive nine affected consumers, in deterministic order:
UK bounded FX translation → UK complete-operation translation → current FX match
→ retained FX-difference refresh → FX reassessment → Group elimination → reporting
→ analytics → Group observation. Twenty-three unrelated nodes retain their exact
versions at closing correction; the earlier separate NL correction has its own
retained six-consumer lineage. No affected list is hardcoded into invalidation.

Two new complete-operation translation nodes contain all current legal positions:
US clean/FX; UK mismatch/timing/FX. Each signed carrying and native profit row binds
an exact current legal version. The reviewed opening operations are US cash100,
loan100, payable20, capital180; UK cash100, mismatch loan10, timing payable30,
FX loan16, capital96. The parent separately reviewed ledger is cash300,
investments258, clean payable90, mismatch payable11, timing receivable30,
capital487. The parent current correction income binds native b_fx_loss through
an actual dependency; it is not an unbound P&L assertion.

Whole operations alone feed Group TBs. Bounded transaction translations only
qualify individual carrying receipts. The smallest generic Stage3 extension
allows a qualified translated payable plus an exact directly EUR-qualified
receivable; existing role/sign/currentness checks remain mandatory. Independent
positive and missing-side/currency attacks prove the symmetric route.

The unchanged ALL_CURRENT_LOAN_SIDES guard independently sees eight October legal
sides and four exact current bilateral matches. Native Consolidation actually
executes four reciprocal and two investment/equity eliminations. Every current
loan and investment account eliminates to zero. Group cash490, opening equity487,
profit3 (NL correction1 plus UK monetary FX2), OCI0, closing equity490. All
corrections are noncash; reviewed complete-operation cash remains490, with no
inherited unsupported financing receipt. Current native Group version:
`version:bbdb8aad60b02982c20df96037992b1d5bd4822ea1312f186687751b117a575d`.

## Exact remaining evidence requirement — honest stop

Native Financial Statements refuses:
`Restated comparative equity differs from opening current equity`.
The inherited supplied comparative cash489/equity489 is inconsistent with the
complete current population's reviewed opening equity487 and cash490. Its
comparative/opening history has not been independently reconstructed. We do not
rewrite that source, insert a net liability3, infer a restatement method, or
fabricate a comparative issued statement merely to close the current Case.

Required evidence is a separately reviewed complete comparative/opening Group TB,
legal carrying/receipt lineage, net-assets/equity and cash history, including any
legitimately supported comparative adjustments and their production-owner
semantics. The production reporting contract requires those bridges to agree;
this milestone supplies no authority to reinterpret the old comparative.
Supported closing correction therefore resolves the current FX residual and
current native Group accounting, but does NOT earn end-to-end IQA03 acceptance.

The refusal is independently executed through the ordinary native owner and
CAO selective reexecution. Reporting/analytics/Group observation stay STALE;
public answer remains partial without Group totals. No blocked accounting version
or Case status was fabricated. The aggregate Case stays IN_PROGRESS/partial,
never COMPLETE/CLOSED. Global current-journal release selection also refuses stale
downstream currentness. Eight distinct current native journal implications
(6 Group, 1 NL, 1 UK) and excluded superseded versions are inventoried, but a full
released exact-once ledger is explicitly NOT claimed.

## Independent QA, permanent attacks and validation

Separate reviewer report: `STAGE4-CLOSING-INDEPENDENT-QA.md`.
CLQA01 reproduced ignored altered reviewed presentation quote1.20 while actual
translation still used1.00. Generic supplied quote-sheet validation now rejects
nonfinite/nonpositive, internally inconsistent, or changed retained presentation
quotes before correction qualification. No rate is inferred. Permanent regression
and independent reruns pass. Unresolved substantive findings within the reviewed
closing/current-population implementation:0. IQA03 final acceptance stays OPEN.
The parent profit binding was a proactive review risk correction, not falsely
counted as an independently reproduced finding.

- 277 distinct focused orchestration methods PASS in one combined command.
- 15 selected native FX/Intercompany/Consolidation/journal methods plus 3 public
  privacy methods PASS: 295 distinct focused passing methods total.
- New 15 authored plus 32 independent closing/current-population methods PASS;
  independent 32 also PASS under hash seeds19 and941. Reruns are not new methods.
- Original full Stage4 positive acceptance remains48 executed methods with
  2 FAIL/8 ERROR. Assertions are unchanged, not skipped or expected-failed.
- Both canonical approval and standards claim validators PASS with zero errors:
  157 approved topics,347 capabilities,1598 claims. No knowledge promotion.
- Governed generators produce44 deterministic milestone artifacts under19/941:
  all original40 unchanged, plus4 new closing/current-population/refusal/attack
  files. No JSON manually patched. See generation verification in publication.
- git diff --check PASS. No full repository release, eight final accepted lineages,
  final temporal acceptance or exact-head green readiness claim.

## Durable continuation boundaries

Source/fixture/test/artifact paths:
`tests/stage4_closing_fixtures.py`, `tests/stage4_closing_population.py`,
`tests/test_stage4_closing.py`, `tests/test_stage4_closing_independent.py`,
`tests/generate_stage4_closing_examples.py`,
`examples/multi-entity-multi-period-closing/` (all under orchestration).

Original conflict, opening correction, all previous QA and source populations
remain historical. Current Group completeness guards stay active; omission,
shortened perimeter, missing transformation/match/dependency, stale/superseded,
wrong dimensions and exact native-profit attacks remain permanent. Native
accounting owner workflows and protected knowledge are unchanged.

Stage4 and the roadmap remain INCOMPLETE. Final source-intake population,
comparative/opening/temporal integration, Group release exact-once, eight accepted
lineages, final independent QA, prior flagship migrations, full regression,
handoffs, immutable exact-head CI and readiness remain required. No persistence,
authenticated governance, general accounting converter, new branch/PR or merge.
