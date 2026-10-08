# Stage 3 independent adversarial QA

Status: ACTIVE; release gate not passed.

Independent reviewer: separate agent context, read-only production review. Production remediation is performed by the implementation agent. Initial review exercised actual native `Intake.ap_control` execution, immutable SQLite Case checkpoint, candidate capture, transition, consumption and ledger restoration. No mocked refusal boundary was used.

Original inspected `memory.py` SHA256: `679432f237560eea2cd2ab24a2f98b59b497b798e6665c3dcb79f03da7e8a779`. Original code and failure log preserved in reviewer scratch `qa-stage3-original`.

## Finding register

| ID | Severity | Boundary and reproducer | Generic remediation | Permanent regression | Independent rerun | Disposition |
|---|---|---|---|---|---|---|
| IQA01 | High | Unknown memory version in coherently hashed USE event survives `audit`; original test failed because no IntegrityError was raised. | Validate USE version against exact retained historical record version and native consuming checkpoint. | `test_unknown_historical_consumption_version_rejected` | PASS in 4-test rerun; original FAIL retained | Remediated |
| IQA02 | High | DOCUMENTED record accepts itself as SUPERSEDED successor; original test failed because no IntegrityError was raised. | Reject self/cyclic lineage and validate reciprocal successor relationship and immutable history. | `test_supersession_cannot_use_self_as_successor` | PASS in 4-test rerun; original FAIL retained | Remediated |
| IQA03 | High | Read-only code review: documentary approval is substring membership, so negative/quoted wording can satisfy `APPROVED subject attribute value`. | Require explicit exact structured governance assertion with semantic polarity and exact bound source evidence. | Pending native reproducer | Pending | Open |
| IQA04 | High | Read-only code review: any existing current result may be declared supporting result; producer Case/Scope and candidate source lineage are not checked. | Bind all supporting results to exact source/evidence/candidate applicability; refuse unrelated lineage. | Pending native reproducer | Pending | Open |
| IQA05 | Capability review | Exact-Scope foundation has no declared broad-policy entity coverage. Group membership alone must not invent policy applicability. | Document bounded exact-Scope refusal; any future inheritance requires explicit legitimate coverage. | No invalid authority demonstrated | Reviewed | Limitation, not substantive defect |

Initial executable run: 4 distinct tests, 2 PASS, 2 FAIL. Original failures remain recorded above; do not replace them with later passing results. Full acceptance proof, concurrency, migration and final exact-tree review remain outstanding.

| IQA06 | High | Unknown consuming root Case/Case accepted in coherently hashed USE event; actual native test originally FAIL. | Validate consuming checkpoint namespace/revision/hash and Case membership. | `test_unknown_consuming_case_in_history_rejected` | Pending | Open |
| IQA07 | High | Candidate accepts `decision.status=approved` with no governance; Decision Register projects approved state. Actual native test originally FAIL. | Govern Decision Register authority independently; proposals cannot grant decision approval. | `test_candidate_cannot_assert_approved_decision_without_governance` | Pending | Open |

Expanded run: 17 independent distinct tests PASS before IQA06/IQA07 additions. Total now 19 distinct tests; latest two added findings remain open. This is not final release acceptance.
