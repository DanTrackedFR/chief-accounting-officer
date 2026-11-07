# GitHub verification recovery boundary

Read-only workflow review against frozen source `126c2f85ea37dc216bb8a732ed4394e4bfbc7e17`. No workflow, source, protection rule or trigger was changed. No workflow was dispatched during this review.

## Safe explicit reviewed reuse

In GitHub Actions, choose **CAO presumed user-provided source assurance** (`cao-presumed-sources.yml`), then **Run workflow**. Select branch `feature/presumed-user-sources`. Set the input exactly:

```
acceptance_pointer: build4/release/presumed-sources-accepted-42297337399-1-v2.json
```

Verify the branch still points to the final published acceptance-evidence commit before dispatch. Record resulting run ID, attempt and actual head SHA. The expected execution result is `ACCEPTANCE_REUSED` with `release_accepted: true`, followed by successful workflow completion. Inspect actual resulting execution evidence; dispatch alone is not success.

**Do not leave the input blank:** blank input invokes a new complete regression. Do not rerun the old fresh-regression run to achieve acceptance.

## Other repository workflows

These are workflow definitions, not a verified list of branch-protection-required status checks. Live protected branch/ruleset requirements have not been established by this local review and must be checked independently before claiming readiness.

| Workflow | Dispatch support | Behavior and limitation |
| --- | --- | --- |
| `cao-build4.yml` | Yes, no inputs | Runs bounded Build 4 tests/proofs and actual current-release verifier. It does not invoke the complete release regression runner. |
| `cao-intelligence.yml` | Yes, no inputs | Runs intelligence suite and proofs; no complete release runner. |
| `cao-service.yml` | Yes, no inputs | Runs hosted service suite and proofs; no complete release runner. |
| `cao-prepared-execution.yml` | Yes, no inputs | Runs prepared accounting and HTTP QA/proofs; no complete release runner. |
| `phase3-skills.yml` | Yes, no inputs | Runs broad skill, lease, supplemental knowledge and repository regression. This is not an evidence-reuse path; do not represent it as a receipt-only check. |
| `cao-orchestration.yml` | Yes, no inputs | Manual dispatch runs the broad accounting regression across orchestration, skills, knowledge, repository, hosted/local service, intelligence and Build 4. **Do not dispatch under the no-full-regression instruction.** |
| `standards-evidence.yml` | No | Has push and PR triggers only. No existing manual-dispatch path is available. |

The orchestration workflow's prior-run reuse branch is limited to a `ready_for_review` event and requires a successful same-workflow run at the exact current head containing all nine named successful gate steps. A regression at the frozen source SHA does not satisfy that exact-head condition after an evidence-only commit. On uncertainty, the workflow falls back to full execution.

All eight workflows have PR event triggers including `ready_for_review`. Marking Ready is therefore not an appropriate shortcut for obtaining missing checks: the assignment requires checks before Ready, and the Profile 1.2 PR-triggered path has no dispatch input and selects fresh regression. A `[skip ci]` evidence commit avoids automatic push/PR execution but does not itself provide successful check evidence.

## Remaining acceptance boundary

Owner dispatch of explicit Profile 1.2 reuse is a concrete next action. Bounded individual workflows can be manually dispatched at the final feature head if required by the live acceptance policy. This review does not recommend broad orchestration/Phase 3 reruns as a workaround.

If orchestration and/or standards status checks are required at the new exact head, the existing workflow definitions do not provide a verified receipt-only manual route for satisfying them. That is an additional CI recovery limitation, separate from unavailable agent dispatch authentication. Resolve the actual required-check set and obtain a separately authorized bounded solution if needed; do not silently waive a mandatory check, change infrastructure, substitute an older head, or rerun the full accounting regression.

Engine release acceptance remains BLOCKED until actual reviewed reuse, applicable exact-head checks, mergeability and readiness requirements are satisfied. Original TrackedFR upload retesting remains separately pending.
