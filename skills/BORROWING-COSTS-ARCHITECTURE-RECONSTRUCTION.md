# Borrowing Costs #35 — architecture reconstruction

Starting live main: `ea19ee62c938dba06f3faf758a75e17a7da27e15`, verified by live fetch on 2026-10-09.
Branch: `phase-3/borrowing-costs-accounting`. No active Borrowing Costs PR was found; historical branch `phase-3/eps-segments-events-grants-borrowing-costs` is not restarted. Open Government Grants PR27 is protected.

## Existing authority and gap

`SKILL-BORROW-001` version0.1.0 is review/NONPRODUCTION across all frameworks. `production.execute` explicitly refuses the package, and its workflow raises ReviewRequired. TOPIC-04-003 is approved CIP/fixed-asset/software routing authority; it does not prescribe a substantive interest-capitalization method. Its canonical claims and mappings remain unchanged. Debt Financing owns underlying debt accounting; Fixed Assets, Intangibles and Inventory own underlying asset recognition and subsequent measurement.

The extension uses separately governed `SUPPLEMENTAL_BORROWING_COSTS`, not a158th topic. Framework-specific claims, source inspection status, operative-period/entity qualification, independent review and deterministic retrieval precede promotion. A model-reviewed claim retains its audit-required source assurance.

## Runtime integration

The existing `production.assess_case`/`execute` boundary performs context, applicable knowledge/document reviews, balanced journal validation and exact independent certification. Missing substantive facts return blocked; absent/stale certification returns partial with no released journals. The existing public adapter allowlists seven output routes. These boundaries remain authoritative.

The bounded specialist will allocate independently evidenced actual financing costs between qualifying capitalized additions and expense, without recreating debt or asset owners. Its journal is an allocation from already-recognized finance expense into CIP, not a second debt accrual. Actual asset/project, borrowing, expenditure, activity chronology, policy and source/GL populations are required. Single-currency ordinary construction scope is distinguished from advanced FX, grants, investment property, specialized software/inventory and other unsupported cases.

IFRS/AASB specific/general methods, US avoidable-interest methods and UK FRS102 policy choices require separate qualification and reasoning. No production claim is established merely because the arithmetic balances.

## Release and concurrent work

Canonical baseline157 approved topics/347 primary mappings and existing supplemental packages are protected. No Government Grants or Investment Property implementation is authorized. Current Actions need new branch/path coverage for Borrowing Costs and its supplemental validators. Full regression includes skills, leases, public/canonical tests, supplements and orchestration/durable Stages1–4. Historical2,995 tests are not a new result. Promotion and roadmap changes await substantive independent acceptance and exact-head release checks.
