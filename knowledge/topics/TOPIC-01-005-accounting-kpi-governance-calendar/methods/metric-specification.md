# KPI, service level and governance calendar — metric specification

Knowledge type: PRINCIPLES / PRACTICE. Capabilities: CAO-01-011, CAO-01-012. Extends existing README and completion note; prepared 2026-09-27.

## Metric contract

Every reported metric requires: business question, numerator, denominator, source population, exclusions, entity/period and timezone, refresh date, formula/query version, owner, target basis, alert threshold and required action. Review raw exceptions and risk before aggregating. Retain snapshots; a dashboard recalculated after late posting must not silently rewrite the original close claim.

| Metric | Exact illustrative formula | Interpretation and safeguard |
|---|---|---|
| On-time reconciliation | approved by deadline / due population | Separate material high-risk accounts; report unresolved items and aged reconciling items. |
| First-time-right journal | submitted journals approved without correction / submitted journals | Distinguish mechanical rejection from substantive accounting error. |
| Late adjustment | count and absolute value of entries after close lock | Show materiality, root cause and affected financial-statement line. |
| Evidence quality | sampled workpapers passing defined completeness criteria / sampled workpapers | Preserve selection method; do not extrapolate a tiny sample without qualification. |
| Exception resolution | items closed with evidenced accounting disposition within SLA / items due | Ticket closure is not the same as posted and reconciled resolution. |

Example: 170 of 200 reconciliations meet the deadline, so on-time is 85%. If 10 of the 30 late accounts are material cash and revenue balances, the CAO reports both the 85% rate and a high-risk exception, not a single green status. If later 25 are approved, the historical on-time metric remains 85%; a separate eventual-completion metric changes. Set targets from observed baseline and risk appetite, not a universal industry threshold.

## Decision calendar and control

Weekly operations review addresses queue aging, close dependencies, staffing and system incidents. Monthly controller forum certifies material balances, late entries, open errors and KPI exceptions with accountable decisions. Quarterly CAO governance revisits risk assessment, policy, capacity, service provider performance and automation. Annual planning aligns jurisdictional reporting, audit and budget milestones. Each forum has inputs due, decision authority, quorum/substitutes, minutes, due-date owner and escalation. Log postponed decisions; a calendar invitation alone is not governance evidence.

**Negative scenario:** a day-5 close KPI is green but 12 post-lock journals totaling 310,000 arose after day 5. The paired late-adjustment measure fails and triggers materiality and root-cause evaluation. Do not recast the dashboard as successful merely because the lock timestamp met target.

## Source and dependency

These are internal operating metrics, not four-framework recognition rules. Underlying accounting conclusions route to the relevant technical topic and entity period. For US issuers, [SEC Release 33-8810](https://www.sec.gov/rule-release/33-8810) supports a risk-based management ICFR context, not a mandatory KPI list (checked 2026-09-27). Dependencies: TOPIC-02-010 sign-off, TOPIC-09-001 risk assessment, TOPIC-11-008 reporting data and TOPIC-12-009 SLAs. Audit evidence must reproduce the metric from retained extracts and definitions.
