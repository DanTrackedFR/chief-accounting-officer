# Stage 3 independent QA

Reviewer: independent delegated QA worker, 6 October 2026. The reviewer authored only `orchestration/tests/test_stage3_independent.py` and this report, did not implement remediation, and has not committed; the final scoped review acceptance below follows remediation and rerun.

Basis: AGENTS.md, live Stage 3 architecture reconstruction, Stage 2 handoff and user requirements. Native certified fixture inputs are baseline data; adversarial mutations and rejection expectations were independently authored from the accounting and lineage boundaries. No claim of independent accounting-standard certification is made.

## Initial run

Command: `PYTHONPATH=skills/tests:. python -m unittest orchestration.tests.test_stage3_independent -v`.

Initial core independent run: 10 tests, 4 passed, 6 failed. Two additional lifecycle/cycle checks passed; a further translation economic-identity attack failed (13 total tests). Failures are release findings, not expected-failure decorators.

| Finding | Executable reproduction | Required behavior |
| --- | --- | --- |
| IC-QA-01 | Remove the NL legal-side binding from elimination while retaining conversion mapping and all declared receipts | Reject omitted material legal-side input |
| IC-QA-02 | Redirect translation binding to equal-valued `shadow_value` metadata instead of actual native TB row | Reject annotation masquerading as native consumption |
| IC-QA-03 | Redirect zero-adjustment conversion binding to equal-valued `shadow_value` metadata | Require actual qualified carrying-value input even at zero adjustment |
| IC-QA-04 | Swap US/NL entity IDs while keeping the translated population unchanged | Bind translated population to producer legal Scope |
| IC-QA-05 | Declare `litigation_provision` semantics on a legal intercompany-loan metric with the correct economic ID | Reject unsupported semantic relabelling |
| IC-QA-06 | Re-certify and execute a genuine current native IC source whose metadata row says principal 900000 while native pair principal remains 90; qualify corresponding TransactionSide | Native transaction population must substantiate metadata economic identity and amount |

The initial passing checks verify baseline native bindings, rejected free economic identity after a concurrent author fix, rejected source-row economic substitution, and rejection of clean cross-period matching despite arbitrary alignment evidence.

An additional IC-QA-07 attack supplies `fabricated-event` to `ReportingBasis.translation` despite both source/target economic IDs and native operation being `clean`; it is accepted. Translation transformation records must bind their actual economic identity.

All seven findings were sent promptly to the implementation author. IC-QA-06 uses actual execution/publication and native re-certification; it does not modify the stored version registry.

## Expanded review and reruns

First remediation rerun: all 13 tests passed, independently executed by this reviewer. Further attacks identified IC-QA-08: a natively certified corrected Group source could replace translator CTA 16.36 with 20 while adding an equity offset -3.64, preserving translated TB and native reconciliation. The author added exact CTA dependencies and population checks. Independent rerun of 19 tests then passed, including native shadow disposition rejection, exact-once gross alias rejection, omitted/duplicate translation disposition rejection, and public internal-metadata exclusion.

IC-QA-09: an FX translated EUR balance could be declared LEGAL_ENTITY / USD because legal Scope membership bypassed translation currency qualification. Semantic-to-layer checks remedied it; the reviewer reran and its rejection passes.

IC-QA-10: change conversion native entity_a US to UK while retaining clean transaction IDs, receipts and amounts. Native certification, execution and zero-adjustment transformation qualification all accept; conversion must retain actual bilateral legal Scopes.

IC-QA-11: change conversion native gl_b 90 to 180 and rate_b 1 to 2. Native certification and execution accept and the transformation records adjustment zero despite qualified NL carrying value being 90. Both carrying-value populations need exact qualification.

Pre-final independent run: 22 distinct tests; 20 passed, IC-QA-10 and IC-QA-11 failed. The author then added exact MATCHED role/Scope/principal verification and an exact-version payable carrying-value dependency; receipt reconstruction reruns those guards. Final independent rerun on 6 October 2026: **22 distinct tests passed, 0 failed, 0 errors**, in 8.278 seconds. IC-QA-10 and IC-QA-11 now reject independently. All findings were sent promptly to the author. Reviewer did not edit implementation or fixture files.

## Final change review and fresh rerun

The reviewer inspected `node_record` and its Graph/CaseRegistry serialization callers: only absent (`None`) economic identity is omitted, while actual transaction identity remains serialized. The reviewer also inspected the new monetary-FX rejection before embedded translation journal suppression.

Two independent permanent tests were added: exact legacy serialization field preservation and a genuine certified/executed native FX monetary case whose translation-only disposition must reject. The latter republishes all downstream native owners and supplies current result versions, ensuring rejection is specifically the monetary-FX guard rather than stale receipts.

Fresh final command: `PYTHONPATH=skills/tests:. python -m unittest orchestration.tests.test_stage3_independent -v`. **24 distinct tests passed, 0 failures, 0 errors**, in 7.662 seconds on 6 October 2026. The final two implementation changes introduce no open demonstrated finding in the reviewed scope.

## Acceptance status

The independently reviewed Stage 3 contract scope is accepted after remediation and independent rerun: **zero open demonstrated findings** across IC-QA-01 through IC-QA-11. This is acceptance of the bounded orchestration contract scope and the adversarial suite, not a claim of new accounting authority, authenticated approval, general framework conversion, or Stage 4 completion. Full regression, deterministic artifact generation and migration release gates remain the parent owner's separate responsibility. Subsequent material implementation changes require a rerun.
