# Sources and QA — TOPIC-13-002

Checked: 2026-09-24
Rights posture: REFERENCE_ONLY. No authoritative standard body is republished here.

## Authoritative anchors
- IFRS Foundation — IFRS 3 Business Combinations: acquisition method; consideration transferred; contingent consideration; measurement period; subsequent accounting. Official public issued-standard material used for paragraph anchors 37–40, 45–50 and 54–58.
- IFRS Foundation — current project/update pages: tentative IASB decisions are tracked as pipeline and must not be treated as effective IFRS requirements.
- FASB — ASC Topic 805 / ASU 2015-16, *Business Combinations (Topic 805): Simplifying the Accounting for Measurement-Period Adjustments*. ASU is amendment history, not a substitute for current Codification.
- FRC — current FRS 102 overview/significant-differences material: Section 19 continues to be based on IFRS 3 (2004); current UK GAAP contingent-consideration mechanics must be sourced from the applicable FRS 102 version.
- AASB — AASB 3 official online standard, including consideration transferred (37–40), measurement period (45–50), subsequent accounting (54–58). Effective-period compilation gate retained.

## Framework-difference controls
1. Do not equate FRS 102 Section 19 with current IFRS 3.
2. Do not use an ASU as if it were the complete current ASC 805 text.
3. Do not treat a post-acquisition target achievement as acquisition-date evidence merely because the earn-out existed at closing.
4. Do not route every contingent-consideration change to goodwill.
5. Do not allow the measurement period to become an unrestricted one-year hindsight window.
6. AASB conclusions require Australian version/effective-period confirmation, not IFRS inference alone.

## Executed scenario QA
| Scenario | Expected CAO behavior | Result |
|---|---|---|
| Earn-out based on next-year EBITDA; actual EBITDA exceeds forecast | Separate acquisition-date valuation from later operating performance; apply framework-specific subsequent accounting rather than reflexively adjust goodwill | PASS |
| Valuation report received four months after close using facts demonstrably existing at acquisition date | Assess as potential measurement-period adjustment; document evidence and provisional item affected | PASS |
| New customer contract signed after acquisition date changes forecast | Treat as post-acquisition event, not measurement-period evidence of an acquisition-date fact without contrary evidence | PASS |
| IFRS liability-classified contingent consideration | Initial FV; subsequent framework routing generally FV changes through P&L outside valid measurement-period adjustment | PASS |
| IFRS equity-classified contingent consideration | Do not remeasure after acquisition date; settlement within equity subject to applicable guidance | PASS |
| US GAAP measurement-period adjustment identified in current quarter | Apply current ASC 805 and ASU 2015-16 architecture; do not automatically revise comparative prior-period statements | PASS |
| UK FRS 102 reporter | Route to applicable Section 19; flag material divergence from modern IFRS 3 before calculation | PASS |
| Australian period begins after 1 July 2026 | Require current AASB 3 version/amendment routing rather than relying solely on Dec-2022 compilation | PASS |
| Seller remains employee and earn-out depends on continued employment | Trigger separate-transaction/remuneration analysis before treating amount as purchase consideration | PASS |
| PPA incomplete at first reporting date | Record provisional amounts, open-item register, missing evidence and measurement-period deadline | PASS |

## QA result
**PASS — REVIEWED / production-candidate.**

Residual limitation: complete current US Codification paragraph body was not available through the public authoritative path used in this build. US paragraph-level approval therefore remains PARTIAL; this is not a blocker to the CAO workflow or to continuing Phase 2D.
