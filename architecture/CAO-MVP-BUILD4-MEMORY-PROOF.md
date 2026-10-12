# Build 4 Company Accounting Memory integrated acceptance

The Orion journey creates a sealed supplier-cost Case with the real Accounts Payable owner, observes a finance-system control from retained evidence, captures it with the native `SQLiteStore.memory()` API, and explicitly records synthetic governance with `authenticated=false`. This setup is distinct from the client interface: no client promotion operation exists and no human authentication is claimed. Subsequent customer-contract Cases use actual `ExecutionInterface.call` investigation/document/submit/execute operations; Revenue Recognition requires its own reviewed source pack and executes independently of context memory.

The permanent tests cover qualified cross-Case reuse, exact version references, wrong entity and framework exclusion, expired effective dates, contradictory current positions, rejected synthetic authentication, user assertions without memory authority, supporting-result supersession, immutable historical snapshots, restart, idempotent consumption, interrupted USE publication recovery, and native Revenue Recognition execution after context reuse.

## Substantive finding and remediation

The original production investigation boundary copied qualified memory references into its snapshot but did not bind native `memory_context_dependencies` or publish a native USE receipt. It also returned the stored snapshot on continuation without requalifying the supporting result's currentness. Original observation is retained in `build4/release/memory-original-observation.json`; the failed assertion is retained in `memory-finding-before.log`.

The bounded integration repair binds qualified exact references before checkpointing, uses the existing native `consume_context` API before delivery, and requalifies each immutable version on every investigation continuation or delivery. Existing native USE events are reused across retries. A crash after checkpoint publication but before USE publication is repaired before delivery. Superseded or changed positions produce blocked requests; original snapshots and accounting results remain retained. Stale policy context cannot enter controlled inference or owner execution. No additional database, authority, owner, or accounting method was introduced.

For reviewed owner execution, caller scope is checked against the original investigation scope before native qualified context is added. Native `prepared._current` supplies the governed context and exact memory dependencies; caller facts and independent owner qualification remain mandatory. No-memory requests retain their existing source and artifact fingerprints.

Native memory retrieval excludes wrong-entity/framework/effective-period records before its refused population. Accordingly, these unrelated historical positions do not generate global context conflicts. Applicable contradictory positions remain retained and block qualification.

## Deterministic reproduction

Run from the repository root:

```sh
PYTHONHASHSEED=731 python -m build4.prove_memory --output /tmp/orion-memory-731.json
PYTHONHASHSEED=1907 python -m build4.prove_memory --output /tmp/orion-memory-1907.json
cmp /tmp/orion-memory-731.json /tmp/orion-memory-1907.json
python -m unittest build4.tests.test_memory_journey -v
```

The generator refuses to overwrite an existing output. The fresh-process proof uses new temporary SQLite files, original source identities, real native source result versions, context/result payloads, exact memory version and USE receipts, and cross-entity exclusion. Both retained final seed outputs are byte-identical, SHA-256 `c193ea991ffbd32fbedc5a087c791013743762a6e3e5b848cd9d0261774bf760`.

This is deterministic native and controlled qualification acceptance. It does not establish authenticated policy approvals, live-model conversation, Claude Code user smoke testing, TrackedFR authentication, or commercial operational acceptance. All synthetic reviewers and approvals remain explicitly synthetic.

Initial authored runs incorrectly expected out-of-scope records to appear as refusals and had an adapted fixture with mismatched specialist handoff/source period. Those attempts are retained as `memory-fixture-initial.log` and `memory-fixture-second.log`. They were fixture/assertion defects, not accepted production defects. Native exclusion remains the intended behavior. The 21 original intelligence authored tests passed after remediation without modifying their expectations.

The enhanced CLI proof also resumes the consumer in genuinely separate `python -m local_cao` processes before and after native source correction. The original result version and supersession history remain retained; the later CLI delivery blocks the stale position while retaining its original snapshot identity. Run `python -m build4.prove_memory` for stdout JSON; `--output` remains available for safe new-file creation. The earlier proof seed files remain preserved, and the enhanced CLI proof is retained separately as `memory-cli-proof-seed731.json` / `memory-cli-proof-seed1907.json`.

## Historical accounting-policy decision extension

The ERP decision above is operational context. A separate Orion revenue-policy journey now proves historical accounting-policy reuse: a native Intake observes the exact `policies` field in a retained company accounting memorandum and executes its supporting Accounts Payable owner. The original candidate is captured as `policies_positions` with exact applicability/effective dates and explicit synthetic governance. It requires independently reviewed standalone selling prices and satisfaction evidence for distinct equipment and monitoring promises.

A subsequent Case reuses this historical position as context and executes the real Revenue Recognition owner against its own signed document and independently reviewed native source pack. The memory position supplies no price, allocation, recognition amount, or reviewer authentication. A more explicit acceptance/service-date policy succeeds it through native atomic `resolve_conflict`; both records and version histories remain retained. The original consumer becomes blocked, while a new consumer reuses only the qualified successor. No candidate or approval was retrofitted into an existing sealed Case.

`AccountingPolicyMemory.test_historical_revenue_policy_reuse_and_atomic_supersession` retains this executable coverage. Enhanced deterministic outputs include the complete accounting-policy source and successor records, scoped immutable snapshots, ledger history and USE receipts. Fresh seeds 731 and 1907 reproduce byte-identically: SHA-256 `29aeb47a9cbac75a6918b629b990af11c3c2d5f24132e257038e24c8ccd111a6`. They are retained as `memory-policy-proof-seed731.json` and `memory-policy-proof-seed1907.json`; earlier proofs remain unchanged.
