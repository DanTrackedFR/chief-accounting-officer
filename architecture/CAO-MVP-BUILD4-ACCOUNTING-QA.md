# Build 4 independent accounting QA

The delegated accounting reviewer authored independent expectations and adversarial
challenges, reviewed the integration author's proofs and did not modify production
accounting code. All **13 independently authored accounting tests passed** in 44.827
seconds after remediation. Run `python -m unittest build4.tests.test_accounting_qa -v`.
The final strengthened memory assertions also passed in a targeted 7.548-second rerun.
Logs: `build4/release/accounting-qa-final-memory-rerun.log` and
`build4/release/accounting-memory-final-rerun.log`.

## Reviewed outcomes

Tests use production `ExecutionInterface.call`, real document intake, native accounting
owners and SQLiteStore. Stored immutable results are inspected, never injected.

| Challenge | Independently verified result |
|---|---|
| Unfamiliar Peregrine three-obligation contract | EUR 24,750 allocated 14,850 / 7,425 / 2,475 on SSP 18,000:9,000:3,000; pending calibration recognizes zero; total revenue 17,325 |
| Full billing and journal economics | Receivable 24,750, contract liability 7,425; each journal balances; exact execution retry preserves economics and revision |
| Integrated Boreal correction | Revenue 31,920 → 34,200 from price 42,000 → 45,000 with unchanged satisfaction; delta 2,280; original immutable version retained and superseded; precisely two native operations |
| Qualification challenges | Document approval assertions, unreliable progress, unreviewed fact mutation, wrong framework, wrong period and wrong canonical claim population cannot qualify complete accounting |
| Incomplete specialists | Government Grants, Borrowing Costs and Investment Property remain legitimately blocked without fabricated calculations |
| Prepayment investigation | Increase 11,550, movement residual −500 and source-discovered invoice PGR-98641; bundled invoice without allocation remains blocked |
| Group/entity boundary | Legal-entity document substitution into Group Case is rejected; framework/entity receipts remain qualified |
| Governed memory and source correction | Exact approved historical context reused; native revenue 17,325; one USE; source supersession blocks resume/execute/result, preserves owner versions and returns STALE |
| CONFIRMED memory | CONTEXT_ONLY, unauthenticated and insufficient to provide accounting facts |

Expected amounts were independently calculated using Decimal arithmetic, with exact
allocation, recognition, liability and journal assertions. The reviewer's correction
test executes the author's fresh-process CLI proof and challenges its outputs rather
than accepting the author's assertions.

## Finding and remediation

**AQ-MEM-01 resolved.** After supporting memory evidence was superseded, delivery
blocked correctly but reported `currentness=CURRENT`. The generic preview now reports
STALE for qualified accounting with refused memory dependencies. The permanent test
verifies blocked delivery, no public accounting calculations, exact historical result
preservation and no duplicate USE. Native CLOSED/workplan metadata remains truthful
historical state; a public limitation explains that current delivery needs requalified
context. No alternate lifecycle or unauthorized reopening was introduced.

The original reproduction is preserved in
`build4/release/accounting-memory-currentness-failure.log`. Early seed attempts during
active changes are preserved under `preliminary-accounting-seeds-*`. Initial fixture
errors are distinct from production findings: certification repaired altered canonical
claims, unsupported operations legitimately returned transport success with blocked
accounting, and an annual context fixture lacked a completed AP result for correction.
Final tests respectively preserve altered claims, assert accounting state, and select
the actual December source with a current AP result. No failed attempt is concealed.

## Source-backed policy extension

The reviewer separately inspected `policy_case`, `install_policy`,
`AccountingPolicyMemory` and `prove_memory.policy_proof`. Policy candidates originate
in retained JSON source fields through native Intake. Each policy retains a completed
native AP supporting receipt, exact applicability and explicitly synthetic governance.
Native `resolve_conflict` atomically supersedes the original position and preserves
history. Historical policies guide context; they do not replace Revenue Recognition.

The author's extension test passed independently in 10.011 seconds. A separate
instrumented reviewer rerun verified revenue 17,350 × (55% + 45% × 25%) = 11,494.38,
equal contract asset, zero liability and balanced journals. Both policy records had
one native AP supporting version; states were SUPERSEDED/APPROVED, both
`authenticated=false`, with two exact context USE receipts. The old executed consumer
became STALE/blocked; a new consumer reused the successor. This author-owned test is
not counted again among the 13 reviewer-authored tests.

## Determinism and release status

Reviewer-selected seeds 283/1709 initially reproduced an **interim** integrated proof
of 1,145,128 bytes with hash
`4ef1b7c807c582740c8cd96e75731c66623ed86e2390ea94c707646c4a284357`.
The `accounting-seed-*-receipt.json` files describe that interim proof only.

The final proof inventory is `build4/release/proof-seeds.json`. Its final integrated
hash is `6eff2736b4b2a50b3e7eda09c782d58b95f80d460cd24048b7d2fb2605dc8e0b`;
final memory hash is
`865ed018134987c83a05150f7a40b22d167f782f62e6446be5a1e9c2be336300`.
The final release source/artifact inventory and exact-head CI receipts must bind these
proofs to the frozen source. This accounting report does not claim that the ongoing
full repository regression or GitHub release gates have completed.

## Acceptance and limits

**Independent accounting review passes; zero substantive accounting findings remain
open in the reviewed scope.** Qualifications are explicitly synthetic engineering
acceptance, not authenticated professional approval or direct standards-text audit.
The governed standards register retains model-derived evidence and open authoritative
audits. Document extraction alone does not establish enforceability, SSP or satisfaction.
Contract-clearing journals require company account mapping and do not authorize posting.

The correction proves a price amendment with unchanged recognition judgments. Process
interruption in the integrated proof occurs after commit; it alone does not prove
mid-transaction crash atomicity. Group context is retained without claiming consolidation
or USD→EUR conversion. The −500 prepayment residual remains visible despite prioritization
materiality, and missing allocation legitimately keeps accounting blocked.
Live inference, authenticated reviewer identity, actual Claude Code user smoke testing,
TrackedFR application acceptance and external posting are unverified here.

## Final local acceptance receipt

The reviewer independently inspected `attempt-003/release-regression.json`: all 14 suite records passed with zero errors/failures, and deduplicating their recorded test identities gives exactly 3,226 distinct tests. All seven validator receipts and the whitespace gate report exit zero. Rehashing every recorded execution input confirmed the current 351 Python files and 1,820 execution-input files match the tested inventory. The manifest records complete=true and historical_artifacts_regenerated=false.

Both final proof files were independently byte-counted and SHA-256 checked against `proof-seeds.json`, matching the final hashes above. The reviewer reperformed final revenue 31,920→34,200 and balanced-journal assertions, checked prepayment increase 15,750 with legitimately blocked unqualified allocation, and inspected native memory-policy revenue 11,494.38 with STALE superseded consumer. Local accounting acceptance remains PASS with no unresolved substantive reviewed finding. This receipt makes no remote exact-head CI, readiness or mergeability claim.

## Raw-log evidence recovery caveat

Subsequent engineering review identified incomplete raw logs for modules 9/20 and a
module-50 raw-log hash mismatch despite unchanged source and passing recorded test
populations. The original full manifest and available raw bytes must remain preserved;
this report's earlier manifest inspection does not certify those defective raw logs.

Accounting concurs with the bounded recovery approach: complete secondary executions
of the same frozen source, explicit parent-manifest hash and provenance caveat, and a
derived witness replacing only the defective module-50 log receipt. Secondary runs
must not add to the 3,226 distinct full-run count. No accounting input, expected result,
reference artifact, production method or result history may change under this recovery.
No economics migration or new accounting conclusion is justified or required.

The reviewer independently read all three completed secondary receipts: 22, 62 and
16 tests passed with complete raw logs, unchanged source/execution inputs and verified
log hashes. The recovered manifest retains exactly 3,226 tests, unchanged test results,
tested inventories and all 22 gate receipts. Only module-50 log path/hash fields change,
with explicit original-log and recovery provenance added. Its parent manifest SHA-256
`b7d9d9e45d571c1dd8db671a61dd860b32e96a558cec2aca910a33162be530d1` independently
matches preserved bytes. Original expected hash 87fd… and damaged preserved hash 8adb…
remain explicit; the actor is unknown.

With engineering concurrence, recovered local accounting acceptance is verified PASS.
No economics migration occurred or is required. Damaged original logs remain caveated;
secondary tests are not counted again. This receipt makes no remote CI claim.
