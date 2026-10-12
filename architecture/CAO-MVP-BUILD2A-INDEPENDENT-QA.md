# Build 2A independent adversarial QA

A separately delegated reviewer who did not implement the service authored
hosted_cao/tests/test_independent_qa.py. Twelve distinct independent tests pass;
reviewer reruns under PYTHONHASHSEED19 and941 pass (12 tests each, counted once).
Reviewer reported zero unresolved substantive findings in the inspected boundary.

Finding: a finished non-durable BLOCKED execution initially omitted its accounting
outcome from job polling. Repair retains only the exact curated operational preview
when there is no native checkpoint; durable outcomes always load the native latest
checkpoint. Independent test reproduces original defect and passes after repair.
Recommendation: serialize checkpoint polling with same-company API calls to avoid
transient native lock errors. Generic company lock now includes job result reads;
reviewer inspected the repair. No accounting engine or historical artifact changed.

Executed independent coverage: both real native fixed-assets/AP exact public parity;
lost-acknowledgment recovery preserving revision1 without owner reexecution; blocked
outcome versus service success; credential/company isolation; concurrent same-key
acceptance/fingerprint conflict; concurrent native execution no duplicate checkpoint;
staged traversal/symlink/malformed JSON/regular-file boundaries; changed accepted
evidence fails closed; real durable stale checkpoint stays stale and cannot complete;
fixed errors/log confidentiality; second worker host-lock refusal.

Authored tests additionally cover version/readiness, size/depth/wire validation,
fresh service restoration, queued crash state, unrelated company job access and
unsupported methods. Fresh-process proof runs actual service startup/HTTP execution,
hard process restart and same-job retry with two native synthetic owners. Tests do
not invent real authenticated accounting approvals. Host-controlled disk/credential
configuration and proxy/TLS are deployment trust assumptions, not adversarial host
security. Full repository/exact-head CI results belong to completion/release evidence.

Latest independent36-test targeted rerun passes (20.928s). Reviewer independently
reproduced fresh HTTP proofs under seeds19/941: SHA256
`d34769d24cea1dd384ccda256e4010e87656263e903552ee0537f9d947f77d45`.
Actual crash-before/after-native-commit and PARTIAL outcome tests inspected.
Roadmap is append-only; existing authorized witness tool changed only its
documentation hash, with all other1100 protected entries unchanged.

Independent readiness review: reviewer-owned test_readiness_gate.py adds8 distinct
executable tests of the exact workflow script. Wrong SHA/workflow/current run,
failed or unfinished runs, every missing/failed/skipped/cancelled required step,
API failures, absent proof and cached-readiness chaining all fail closed. Only a
full successful same-workflow exact-head run permits reuse on ready_for_review;
other events always execute full regression. Eight tests PASS; zero substantive
findings. Combined reviewer-owned population20, combined new population44.
