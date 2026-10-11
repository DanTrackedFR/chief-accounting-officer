# CAO MVP Build 3 — independent adversarial QA

Status: COMPONENT AND INTEGRATION QA PASS; final release/proof review pending.

Separate reviewer inspected Build 1/2A handoffs, local adapter, context resolver, document adapters, inference boundary, investigation loop, private durable Case metadata, native correction/recovery and HTTP jobs. Reviewer authored `intelligence/tests/test_independent_qa.py` without production implementation ownership. Synthetic reviewed packs are explicitly test-only and come from authored fixtures; independent tests mutate/substitute them adversarially. Production does not import test certification helpers.

## Independently reproduced findings

| ID | Defect | Permanent executable regression | Resolution |
| --- | --- | --- | --- |
| B3-IQA-01 | Two active contradictory contracts had no disambiguation conflict | `test_ambiguous_contracts_block_and_request_resolution` | Explicit active-contract ambiguity blocks; rerun PASS |
| B3-IQA-02 | Model contradiction disappeared on continuation without inference | `test_model_conflict_persists_without_new_inference` | Historical inferred conflict remains; rerun PASS |
| B3-IQA-03 | Malformed XLSX parser exception escaped safe API envelope | `test_malformed_xlsx_returns_safe_envelope` | Parser failure safely blocked; rerun PASS |
| B3-IQA-04 | Malformed PDF parser exception escaped safe API envelope | `test_malformed_pdf_returns_safe_envelope` | Parser failure safely blocked; rerun PASS |
| B3-IQA-05 | Model provider could mutate frozen scope/context through aliased objects | `test_model_provider_cannot_mutate_bound_snapshot` | Provider receives isolated copies; rerun PASS |
| B3-IQA-06 | Caller metadata mutation changed extracted document lineage after hashing | `test_document_mutable_input_cannot_change_lineage` | Metadata isolated; rerun PASS |
| B3-IQA-07 | Governed Period registry tuple/list wire mismatch blocked native revenue and hosted jobs | Native revenue and HTTP integration tests | Canonical wire scope preserves exact native qualification; rerun PASS |

Zero unresolved substantive findings in the reviewed paths. This does not substitute for complete repository regression or exact-head Actions.

## Actual independent rerun

Command: `python -m unittest intelligence.tests.test_independent_qa -q`.

39 distinct independently authored tests; exit 0; all PASS; elapsed 46.466 seconds. Reruns are not added to this count.

Coverage includes untrusted APPROVED context, other-entity exclusion, conflicting currencies, effective dates, wrong-company/currency source rejection, CSV population completeness, duplicate headers, formula refusal, hidden row retention, forged XLSX dimensions, scanned/active PDF refusal, inert prompt injection, fabricated inference references, retry bounds, missing evidence refusal, request deduplication, immutable event retry, frozen Case snapshots after onboarding edits, cross-company isolation, document supersession identity, native source bindings, altered contract amounts, altered reviewer-certified economics and wrong Case packs.

## Actual accounting and investigation results

Unfamiliar prepayments: opening 200, additions 4500, consumption 400, closing 4300. Native investigation observation reports increase 4100, residual 0, and identifies supporting invoice ORION-573 from the movement row. Missing completeness returns no calculation and a population conflict. These are observational investigation calculations, not certified accounting economics.

Unfamiliar DOCX customer contract and separately reviewed native intake invoke the real Revenue Recognition owner. Actual revenue is EUR11,494.38. Changing extracted contract price to EUR90,000 while reviewed facts retain EUR17,350 rejects. Omitting document bindings, changing certified economics and substituting Case identity also reject. Restore/execute retries with native CAO execution forced to fail retain exact public result and revision, proving retries do not run economics again.

A real local HTTP server accepts the same native execution through durable jobs, refuses direct synchronous execute, returns exact local public-result parity, preserves checkpoint on a new-key retry and rejects another-company job access.

## Correction and recovery

Qualified contract successor v2 changes fixed price to EUR18,000. Upload immediately returns STALE and refuses ordinary execute. Native CORRECT and REWORK refresh governed synthesis. Original ResultVersion fields remain byte-equivalent except legitimate state/superseded_by transitions; both document versions remain; one rework plan is retained. Retrying the immutable correction preserves checkpoint and journals.

Deterministic fault injection interrupts immediately after native prepare and immediately after native recovery commit. A fresh ExecutionInterface restores the same Case and finishes correction/rework. Both variants retain exactly two operations (one correction, one rework), one rework plan, and a complete governed result. These are deterministic exception-at-commit-boundary tests; final proof should separately describe any real-process kill tests rather than conflating them.

## Remaining release review

Review final synthetic proof under both hash seeds, exact source hashes, full repository regression evidence, validators and final remote Actions before declaring release acceptance. No live-model evaluation has been verified by this reviewer. DOCX body-only extraction warning and PDF reading-order uncertainty must remain visible. Specialist PRs and historical artifacts were not modified by this reviewer. No commit, push or merge performed.

## Release review continuation

B3-IQA-08 OPEN: context item explicitly marked `source_state=unknown` with a non-null investigation threshold was applied as asserted context, potentially suppressing anomaly requests. Independent regression `test_unknown_context_value_cannot_be_applied` fails before remediation. Unknown qualification must remain unresolved; caller-supplied placeholder values do not resolve it. Parser warnings visible in preview regression passes. Independent suite now contains 41 distinct tests; final rerun pending.

Reviewer inspected deterministic proof and bounded release runner. Proof retains original document bytes/hashes, both context/evidence versions, native version immutable-field hashes, fresh-process continuation, actual native revenue/correction, unfamiliar prepayment movement/request, entity isolation and policy conflict. No live model is claimed. Readiness gate explicitly requires the Build 3 intelligence/proof step; a legacy green run lacking that step cannot satisfy it.
