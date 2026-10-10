# Build 1 independent adversarial acceptance

A separately delegated reviewer authored `local_cao/tests/test_independent_qa.py`
without implementing the facade or accounting owners. This is independent review,
not a second authored test pass. Review inspected the native persistence and memory
contracts, intake qualification tests, adapter/context/CLI code, Claude instructions,
local guide, execution contract and TrackedFR finance-context requirements.

## Executed acceptance

`python -m unittest local_cao.tests.test_independent_qa -q` passed **24 distinct
independent tests** (exit 0). The test population includes two owner scenarios,
multiple separate-process CLI resumes, and three target-substitution attacks.
Counting subtests or routes again would inflate the distinct test count.

| Concern | Independent evidence |
|---|---|
| Actual native execution | Fixed-assets and accounts-payable complete through facade; stored Case invokes exact owner; output equals native CAO.public |
| Durable recovery | Fresh CLI processes restore answer/export/tool_output; revision remains 1; five persisted operations cannot call CAO.run |
| Missing evidence | Revenue/prepayments return questions, no calculations or journals; empty execute can later accept evidence using same Case identity |
| Reviewed qualification | Missing reviewer signoff and altered reviewed source cannot complete |
| Context authority | APPROVED Markdown and injected instructions never enter native memory ledger or output |
| Company identity | Other company cannot resume known Case; changed context cannot rebind immutable workspace marker |
| Retry economics | Lost submission acknowledgment after committed execution returns safe acknowledgment without owner execution or revision change |
| Public safety | Exact native public parity, fixed error text hides confidential exceptions, no arbitrary public route |
| Paths and private files | Absolute/traversal evidence and symlink workspace/database rejected; new state files have mode 0600 |
| Malformed wire | Unknown operation/authority fields, duplicate JSON keys, nonfinite JSON and non-object requests reject without traceback |
| Historical input | Changed objective cannot overwrite original request bytes |
| Currentness | Native in-memory stale result version maps to STALE; this mapping test does not claim a new persisted selective-rework demonstration |
| Availability | Registry metadata/executor parity is discovered dynamically; unavailable pending specialists cannot complete |
| Objective coverage | Unrelated reviewed AP evidence and empty declared revenue target cannot manufacture completed revenue Case |

## Findings and resolutions

1. **Evidence-free execute froze a blocked Case.** Initial execution saved an empty
   blocked checkpoint; submit then refused all evidence. Implementation now leaves
   unexecuted previews unstored. Independent regression proves execute→submit→execute
   preserves Case identity and produces the legitimate supported result.
2. **Submission retry after execution rejected an identical acknowledged input.**
   Identical evidence now returns the original staging acknowledgment; different
   evidence remains immutable. Independent regression proves no additional native
   owner execution and no extra revision.
3. **Declared accounting objective could complete using unrelated economics.** A
   declared revenue family accepted only an AP workpaper and reported complete.
   Initial key-presence repair was independently bypassed using `[]`, a scope-only
   object, and an empty obligations population. Repair requires a declared fact
   family, meaningful required populations, and actual completed native target-owner
   work before complete delivery. Permanent independent regressions cover both the
   original substitution and all three reproduced bypasses.

No significant reproduced defect remains unresolved in this reviewed bounded
facade. This statement is limited to executed tests and inspected code, not a
claim about arbitrary accounting prose or privileged malicious filesystem writers.

## Scope and owner validation

Actual Claude Code was unavailable: independent tests exercised the exact
stdin/stdout CLI in fresh processes. The documented live Claude prompts still
require owner validation. Model-generated accounting reasoning is explicitly
separate from an executed native result; no live general-purpose model planner
or PDF/XLSX/DOCX extraction is supplied.

Clients must declare a supported native fact family and supply controlled reviewed
workpapers. Natural-language objective semantics are not independently inferred by
this facade. Markdown validates execution dimensions and duplicate keys; unrelated
narrative remains inert asserted context, so semantic contradictions in narrative
are not automatically resolved.

The facade exposes initial execution and current native checkpoint reopening. It
has no sealed native CORRECT/REWORK or memory-promotion operation. Partially
executed checkpoints cannot accept replacement evidence through this facade.
The local guide states that limit and preserves the original Case/history; later
extensions must compose existing qualified native persistence operations. This is
an accurately bounded Build 1 subset, not the full future investigation loop.

Registered source links are inert metadata. TrackedFR requirements distinguish
verified infrastructure and native contracts from proposed fields; they explicitly
require later source-level schema inspection. Preferences/onboarding never replace
approved native positions, and cross-system synchronization claims no distributed
atomicity. No hosted adapter or SaaS authorization is claimed.

The default private workspace and company-context files are ignored. Custom
workspace locations must be ignored explicitly before use, as documented. Host
permissions remain responsible for existing directories, backups and local agents
that already have repository read access.

Full repository and exact-head GitHub checks belong to the integration release
record. The reviewer does not claim those gates from this targeted independent run.
