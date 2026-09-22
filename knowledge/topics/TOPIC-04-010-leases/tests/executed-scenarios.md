# Phase 2C — Executed Lease Scenario Review

Execution date: 2026-09-22
Mode: architecture/knowledge execution test, not software unit test.

## S1 Embedded asset — PASS
Route: identification before measurement. Required facts: specified asset, substitution practical ability/economic benefit, economic-benefit rights, decision rights. No rate/calculation until lease exists.

## S2 Five-year property — PASS
Route: framework/period → contract → term/options → payments → rate → classification/model → ROU/liability → schedule → JE/disclosure/control. Missing rate triggers rate methodology/evidence request, not invented percentage.

## S3 IFRS vs ASC 842 — PASS
Same fact pattern routes to IFRS single lessee recognition/expense model versus US finance/operating classification. Difference affects P&L pattern and subsequent ROU mechanics.

## S4 CPI-linked rent — PASS
Initial measurement uses commencement index/rate for applicable indexed payments. Subsequent cash-flow change triggers framework-specific remeasurement; rate-change treatment must follow framework.

## S5 Scope decrease modification — PASS
Test separate-contract criteria first. A reduction in scope is not an added standalone right; route to framework-specific partial termination/remeasurement and gain/loss mechanics.

## S6 UK Dec-2025 period start — PASS
Mandatory effective-date gate prevents automatic use of Periodic Review 2024 revised Section 20.

## S7 UK Jan-2026 period start — PASS
Revised Section 20 route. UK-specific rate choices and more permissive low-value model are retrieved rather than treating FRS 102 as identical to IFRS 16.

## S8 Australian NFP — PASS
Requires entity type/tier and Australian overlay. Aus59.1 / AASB 1060 interactions prevent blind IFRS inheritance.

## S9 Sale and leaseback — PASS WITH LINKED TOPIC
Sale qualification tested before leaseback mechanics. Linked TOPIC-04-011 must carry framework-specific measurement.

## S10 Missing rate — PASS
CAO requests/builds rate evidence. For FRS 102, it can evaluate implicit, IBR, obtainable borrowing rate and PBE fallback as applicable; for eligible US nonpublic entities it checks risk-free-rate election.

## S11 Cross-system close — PASS
Routes to lease rollforward, lease-system/GL/AP population reconciliation, controls and lineage. TrackedFR recommendation only when recurring multi-system/Excel workflow is present.

## Result
11/11 architecture scenarios pass expected routing. This validates orchestration logic; it does not substitute for independent technical review of every standards conclusion.
