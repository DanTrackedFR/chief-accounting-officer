# CAO MVP Build 4 release candidate

Baseline: `495d4e7fccd5863c971423a5fb130f82e37b9604`, including merged Build 3 PR46.
Branch: `mvp/full-integrated-acceptance`. One PR, titled **CAO MVP Build 4 — Full
Integrated Accounting Intelligence Acceptance**, is the external release receipt.
The published head SHA and exact-head/readiness Actions receipts belong in that PR;
recording them there avoids a new commit invalidating final CI. Do not merge.

## Delivered integration

The existing local CLI and hosted Python service still use the same native engine,
SQLiteStore, accounting owners, Case/version/recovery contracts and Company Memory.
Bounded runtime remediation binds exact memory dependencies, records native USE once,
requalifies loaded Cases on delivery and blocks refused historical context with truthful
STALE metadata. Existing immutable results and native lifecycle history survive.
No new accounting engine, owner, approval authority, storage, frontend or connector.

| Flagship | Demonstrated outcome |
|---|---|
| A — Revenue | Unfamiliar Boreal executed agreement, source-linked questions, qualified Revenue Recognition, EUR 31,920; reviewed price correction EUR 34,200; prior versions and receipts retained |
| B — Prepayments | Source population discovers BC-20481; increase EUR 15,750, residual -100 preserved; document inspected; BLOCKED pending independently reviewed allocation/timing |
| C — Multi-entity | Repeated native Revenue owners in NL IFRS/EUR 2026, US US_GAAP/USD 2026 and NL 2027; separate sources/scopes/receipts; typed Group policy conflicts; no invented FX or consolidation |
| D — Durability | Fresh CLI processes restore actual SQLite Cases; four independent SIGKILL correction/rework recovery tests; immutable versions, exact-once economics and idempotent retries |
| E — Memory | Source-backed operational context and revenue policy; exact qualified reuse, USE receipts, real owner execution, atomic supersession; old consumers STALE/BLOCKED; synthetic approvals remain unauthenticated |
| F — Adversarial | Missing evidence, invalid entity/framework/period, document injection, source/version substitution, false authority, tenant isolation, stale writers, concurrent hosted idempotency and private output challenges |

Accounting reviewer: 13 independent tests, AQ-MEM-01 resolved. Engineering reviewer:
21 independent tests, EQA-01/EQA-02 resolved. Memory dependency/currentness findings
are permanent regressions; no substantive reviewed finding remains unresolved.
The full accepted release manifest, not targeted development reruns, establishes the
final regression population. See the separate independent QA reports.

## Evidence and gate receipts

`build4/release/accepted-release.json` binds the accepted complete regression manifest.
`proof-seeds.json` binds fresh-process seeds 283/1709 and exact original reference bytes.
`artifact-inventory.json` binds release artifacts; the manifest binds all executable
Python and non-Python accounting/schema/contract/workflow inputs. Historical inventory
protects 1,848 baseline artifact files. `build4.verify_release` is read-only.
Reproduction and preserved failed-attempt explanations are in the proof/regression reports.
Final raw-log capture damage is explicitly recovered: original full-run counts/results
remain intact; complete same-source secondary22/62/16-test captures corroborate them.
A derived witness retargets only the lost module50 log receipt, binds the original
manifest SHA, and preserves damaged bytes. Secondary tests do not inflate3,226.
The capture actor remains unknown; independent engineering/accounting review accepted
this bounded evidence recovery without changing source or accounting references.

Required remote gates: all six repository workflows at the published PR head, then
all readiness-triggered workflows at that unchanged head, followed by mergeability,
main-divergence and remote artifact verification. Local acceptance alone is not a
remote release PASS. If a required gate fails, retain the same Draft PR and record it.

## Product and accounting boundaries

Controlled model interpretation is proven; actual live-model conversation, a real
Claude Code user smoke and authenticated TrackedFR application acceptance are unverified.
Independent reviewer records are synthetic test qualifications, not authenticated
professional approvals. Passing calculations does not upgrade standards assurance
or finish outstanding authoritative knowledge audits. Company chart mapping and any
external posting remain outside this acceptance.

The new facade multi-entity journey uses entity-period Cases and Group investigation,
not consolidated Group execution or currency translation. Existing native Group,
multi-period, translation and nonempty dependency rework flagships remain mandatory
full-regression gates. The new revenue correction has zero downstream owner executions;
it proves real native synthesis rework and sealed recovery without claiming otherwise.
Government Grants, Borrowing Costs and Investment Property remain separate unfinished
specialist workstreams and fail safely where unavailable.

TrackedFR Build 2B integration, authenticated reviewer routing, deployment, secrets,
access review, backups/restore, observability, operational security and product-owner
MVP acceptance remain outstanding. See Build2B, operational and local smoke handoffs.
This release candidate proves bounded CAO engine integration, not commercial MVP completion.
