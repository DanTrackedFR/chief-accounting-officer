# Phase 2D Regression Review 001 — Close and GL Family

Date: 2026-09-22
Scope: TOPIC-02-001 through TOPIC-02-010 plus Phase 2C lease architecture.

## Result
The Close and General Ledger family is materially populated at REVIEWED level across all ten mapped top-level topics. Operational topics correctly emphasize principles, practice, controls, evidence and systems rather than manufacturing four-framework content. Standards-sensitive issues route to applicable literature.

## Architecture findings

### 1. Lease topic-ID mismatch — HIGH PRIORITY
The Phase 2B topic universe maps lease capabilities across TOPIC-04-007 through TOPIC-04-011. The Phase 2C vertical slice was stored mainly under a folder named TOPIC-04-010-leases and described that folder as covering CAO-04-017 through CAO-04-024. That folder therefore spans capabilities assigned by the canonical universe to TOPIC-04-007, 04-008, 04-009 and 04-010.

Action: preserve the substantive lease work, but normalize it into the canonical topic IDs before relying on automated completion counts. Do not count the single Phase 2C folder as four separately completed topics until remapping is done.

### 2. Duplicate TOPIC-02-001 folders — CLEANUP REQUIRED
Repository inspection shows multiple TOPIC-02-001 close folders created during build retries. The canonical substantive build should be selected and duplicate folders removed or superseded so machine counts are not inflated.

### 3. Effective-date routing is first-class
IFRS 18 becomes effective for annual periods beginning on/after 1 January 2027 and moves some general preparation concepts from IAS 1 into IAS 8. Current 2026 knowledge must not prematurely route those requirements to the post-2027 location. FRS 102 Periodic Review 2024 similarly reinforces mandatory reporting-period routing.

### 4. Completion status vocabulary
REVIEWED means the topic has substantive CAO knowledge and has passed internal build QA. APPROVED should remain reserved for deeper independent technical review where standards conclusions are material. Operational topics can be REVIEWED without unnecessary paragraph-level standards mapping.

## Family QA
- Coverage: 10/10 Close & GL topics materially populated.
- Orchestration: PASS.
- Controls/evidence integration: PASS.
- Systems/data integration: PASS.
- TrackedFR editorial discipline: PASS.
- Framework overreach: PASS — no forced four-framework analysis on low-sensitivity topics.
- Repository hygiene: PARTIAL due duplicate close folder and lease-ID mismatch.

## Scaling decision
Continue to the next build family. Hygiene issues are recorded and should be fixed without blocking substantive topic progression.