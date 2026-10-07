# Durable Case + Company Accounting Memory handoff

Documentation only. Stage4 does not implement persistence or authenticated
governance. This next workstream starts only after owner integration of Stage4.

Persist the existing governed objects and their exact identities rather than
creating a second accounting authority: Company Context and Scope hierarchy;
Case hierarchy/status/outcome; governed Period/fiscal calendar; execution nodes
and native owner identity; sealed source snapshots and ReviewedInputPacks;
immutable results, supersession and dependency receipts; corrections, invalidation,
selective rework, conflicts, observation and final public-answer provenance.

Opening and comparative relationships must retain different types and exact
producer/consumer Scope, Period, calendar, framework, currency and version.
An October2025 comparative cannot become an October2026 opening by matching value.
Restoration must preserve historical immutable evidence and currentness: stale or
superseded receipts cannot qualify reporting or journal release after reload.

Future acceptance should prove restart roundtrips, deterministic reconstruction,
immutable history, selective dependency rework, closed-period governance, exact-once
journal selection and public/privacy boundaries against the accepted Stage4
flagship and all earlier single-entity/Group controls. Define storage transaction,
concurrency, authorization, recovery and migration contracts before implementation;
none is silently supplied by synthetic reviewer signoffs in the present fixture.

Reuse native production accounting owners, Consolidation and Financial Statements.
Do not invent intervening history, general conversion authority or parallel ledgers.
The Stage4 integration handoff, independent QA, deterministic artifacts and release
manifest are the starting compatibility gates. Roadmap advancement is limited to
this next workstream; implementation remains outside PR37.
