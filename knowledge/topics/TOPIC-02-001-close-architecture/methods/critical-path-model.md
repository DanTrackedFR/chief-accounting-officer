# Month-end close — critical-path model and acceptance

Extends the existing README, factory and alternate/retry packs for TOPIC-02-001; canonical entrypoint proposed here, with other folders preserved. Capabilities CAO-02-001–003. PRINCIPLES/PRACTICE; 2026-09-27.

## Dependency calculation

For each close activity capture predecessor, earliest start, duration, due date, owner/reviewer, evidence and escalation. Illustrative network, in business days from day 0: AP cutoff (2); AP reconciliation (1, after AP cutoff); accrual review (1, after AP reconciliation); billing completeness (3); revenue journal (1, after billing); consolidation (1, after both accrual review and revenue journal); statement tie-out (1, after consolidation). Earliest completion: AP chain 2+1+1=4; revenue chain 3+1=4; consolidation at day 5 and tie-out day 6. Both branches are critical; reducing AP by one day alone does not shorten the day-6 finish. If billing completeness slips to day 4, completion becomes day 7. Record this mathematically, not as a blanket “day-5 close” pledge.

The calendar must specify local timezones and late upstream feeds. Each task's sign-off is conditioned on a complete input population and subsequent transaction capture. A pre-close reconciliation rolls forward activity through period end; it cannot pretend a mid-month snapshot is the final balance. Close lock requires material account certification, journal approvals, identified exceptions and authority to reopen. Material unresolved exceptions receive documented ownership and impact assessment, not a cosmetic green marker.

## CAO artifacts, controls and evidence

Produce a dependency graph, entity calendar, cutoff memo, completeness controls, reconciliation tracker, journal exception register, late-adjustment log and lock certification. Version the source queries and last-successful interface runs. Reviewer confirms the cutoff evidence, not merely the task checkbox. For a change, compare three closes' elapsed path, late entries, aged exceptions and audit findings. An outage invokes a documented manual fallback followed by source-to-GL catch-up reconciliation.

**Executed perturbation:** billing feed arrives one day late. Expected critical path day 7, not day 6. Result PASS; forcing lock on day 6 without a complete revenue population fails and routes to risk-assessed estimate or reopen governance. Technical revenue treatment remains Domain 03. This operational close design does not prescribe recognition under IFRS/US GAAP/UK GAAP/AASB. IFRS 18 presentation transition is a reporting dependency for annual periods beginning on/after 1 January 2027, per the [IFRS overview](https://www.ifrs.org/issued-standards/list-of-standards/ifrs-18-presentation-and-disclosure-in-financial-statements/) checked 2026-09-27.

**Negative test:** manager marks billing completeness complete on day 3 while five rejects remain unassigned. Expected FAIL; preserve reject IDs, period exposure and revised critical path before lock.
