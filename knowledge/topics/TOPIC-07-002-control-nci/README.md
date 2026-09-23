# TOPIC-07-002 — Control Assessment / Non-Controlling Interest Accounting

Status: **REVIEWED / production-candidate**
Primary capabilities: CAO-07-003, CAO-07-004
Sensitivity: H
Source check: 2026-09-23

## Objective
Enable the CAO to resolve difficult control conclusions and account for, present, reconcile and document non-controlling interests (NCI) after consolidation scope has been established.

## Required inputs
Framework, reporting period and jurisdiction; legal/entity structure; ownership and voting rights; governing agreements; relevant-activity and decision-right evidence; substantive/protective rights; potential voting rights; principal-agent arrangements; acquisition-date ownership and NCI measurement records; subsequent ownership changes; subsidiary equity and comprehensive-income rollforwards; distributions; acquisition/disposal dates; prior control papers.

## Principles
Control is an accounting conclusion, not an ownership-percentage formula. The analysis identifies the investee's relevant activities, who has current substantive rights to direct them, exposure/rights to returns, and—under IFRS/AASB—the linkage between power and returns. Changes in facts, rights or governance trigger reassessment.

NCI is the equity in a consolidated subsidiary not attributable directly or indirectly to the parent. The NCI rollforward must reconcile opening NCI to closing NCI through acquisition/disposal effects, attributed profit/loss and OCI, distributions, ownership transactions and other applicable movements.

## CAO decision logic
1. Resolve framework, period, reporting entity and whether TOPIC-07-001 has established the candidate subsidiary population.
2. Identify purpose/design, relevant activities and how decisions about those activities are made.
3. Inventory voting, contractual, appointment/removal, potential voting and other rights; distinguish substantive from protective rights.
4. Assess de-facto control, principal-agent/delegated decision making and structured/VIE considerations under the applicable framework. Do not import IFRS conclusions into ASC 810.
5. Document the control conclusion, contrary evidence, judgment and reassessment triggers. Date the conclusion.
6. For each consolidated subsidiary, establish parent and NCI interests, including indirect interests and changes during the period.
7. Resolve acquisition-date NCI measurement under the applicable business-combination framework; do not assume a single framework-wide measurement convention.
8. Attribute post-acquisition profit/loss and OCI between parent and NCI under the applicable framework, including cases where NCI becomes a deficit balance if required.
9. Treat ownership changes that retain control under the applicable equity-transaction model; separately route any loss of control to TOPIC-07-009.
10. Reconcile NCI by subsidiary and in aggregate to consolidation journals, equity, statement presentation and disclosures.
11. Produce the control paper, NCI rollforward, ownership-change paper/JEs, disclosure support and durable memory candidates.

## Framework routing
### IFRS
IFRS 10 is the primary consolidation/control authority. Control requires power over the investee, exposure or rights to variable returns, and ability to use power to affect returns. Protective rights alone do not confer power; principal-agent analysis is required where decision-making is delegated. IFRS 10 requires NCI within equity separately from owners of the parent and treats ownership changes that do not cause loss of control as equity transactions. IFRS 3 governs acquisition-date NCI measurement. Current 2026 IFRIC work on single-investor funds is monitored as interpretive pipeline and must not be treated as a new requirement before finalization.

### AASB
AASB 10 carries the IFRS-aligned control and NCI architecture, but the CAO must use the operative Australian compilation. Current AASB 10 paragraphs 22–23 require NCI within equity separately and ownership changes without loss of control to be equity transactions. AASB 3 governs acquisition-date NCI measurement. Australian entity/reporting overlays must be checked independently.

### UK GAAP
FRS 102 Section 9 plus applicable company law governs consolidated financial statements. The current 2024-edition text requires NCI in net assets within equity separately, separate disclosure/attribution of NCI profit or loss, and attribution of total comprehensive income even if NCI becomes a deficit. Changes in controlling interests that do not cause loss of control are equity transactions under paragraph 9.20A. The FRC notes that Section 9's control model retains architecture based on IFRS requirements predating IFRS 10, so an IFRS 10 control conclusion must not simply be copied into UK GAAP.

### US GAAP
ASC 810 governs consolidation and NCI, with model routing including voting-interest and VIE considerations as applicable. NCI is reported within consolidated equity separately from parent equity; changes in ownership while control is retained are generally equity transactions, while loss of control triggers deconsolidation. Current complete Codification paragraph bodies are not consistently available through the public source path, so paragraph-level authority remains **PARTIAL** pending an authorized current Codification check.

## Key differences and traps
- IFRS/AASB single control architecture is not interchangeable with ASC 810 model routing.
- UK FRS 102 control requirements are not simply IFRS 10 transplanted; apply Section 9 and statutory requirements.
- Acquisition-date NCI measurement can differ by framework and transaction; resolve it from the business-combination topic rather than back-solving from the consolidation rollforward.
- NCI percentage and economic allocation may require analysis of different classes/rights; do not blindly multiply consolidated net assets by a headline ownership percentage.
- Retaining control versus losing control is a hard accounting boundary: ownership-change accounting must stop and reroute when control is lost.

## Calculation / reconciliation model
Maintain by subsidiary:
`Closing NCI = Opening NCI + acquisition/opening adjustments + NCI share of profit or loss + NCI share of OCI - NCI distributions +/- ownership transactions retaining control +/- other supported movements`.

Every movement must map to an underlying ledger/consolidation journal or approved acquisition/ownership-change calculation. For complex capital structures, calculate allocation using the substantive economic rights rather than a simplistic common-share percentage.

## Documentation
Minimum workpapers:
- control assessment with facts, relevant activities, rights, returns/model routing and conclusion;
- control reassessment trigger log;
- acquisition-date NCI basis and cross-reference to business-combination accounting;
- subsidiary-by-subsidiary NCI rollforward;
- ownership-change analysis and journal support;
- NCI presentation/disclosure tie-out.

## Controls and audit evidence
Key controls: quarterly rights/governance-change trigger; legal-entity/control register review; independent review of judgmental control conclusions; ownership master-data approval; NCI rollforward-to-subsidiary-equity reconciliation; consolidation-journal review; retained-control/lost-control gate; disclosure tie-out.

Audit evidence should permit reperformance of the control conclusion and NCI rollforward. Unsupported ownership percentages, stale governance documents and unexplained NCI movements are exceptions, not acceptable evidence.

## Systems and data
Store effective-dated legal ownership separately from accounting control conclusions. Consolidation systems should carry parent/NCI ownership data, acquisition basis, effective dates and journal lineage. Automated NCI allocation is appropriate only after the accounting model and allocation basis are approved; system rules must not infer control solely from ownership percentage.

## TrackedFR applicability
Relevant where recurring NCI/control-close work requires reconciliation of legal-entity/ownership data, subsidiary trial balances, consolidation-system outputs and GL/reporting data in Excel. Not recommended merely to draft a control memo.

## Outputs
- control assessment / reassessment paper
- effective-dated control register update
- NCI rollforward and reconciliation
- ownership-change accounting paper and journal entries
- NCI disclosure support
- exception list and evidence requests
- Company Accounting Memory candidates for durable control conclusions and NCI methodology

## Scenario tests
1. 48% shareholder with dispersed remaining holders and substantive unilateral decision rights: require facts-based framework-specific control analysis; no automatic no-control conclusion. **PASS**.
2. 80% ownership but another party has substantive rights over relevant activities: ownership alone cannot determine control. **PASS**.
3. Fund manager is an agent and one investor holds 99.99%: do not automatically deem the manager's rights delegated to that investor; perform full IFRS 10 analysis. **PASS**.
4. NCI share of losses exceeds opening NCI: route framework rules; IFRS/AASB/FRS 102 can require attribution producing deficit NCI rather than floor at zero. **PASS**.
5. Parent buys another 10% but retains control: route retained-control ownership-change accounting, not acquisition gain/loss. **PASS**.
6. Parent sells interest and loses control: stop TOPIC-07-002 retained-control mechanics and route deconsolidation to TOPIC-07-009. **PASS**.
7. US VIE fact pattern: route ASC 810 model; do not apply IFRS three-element test as substitute. **PASS**.
8. NCI rollforward does not tie subsidiary equity/consolidation journals: block completion and raise reconciliation exception. **PASS**.

## Completion criteria
PASS only when the CAO resolves framework/period; identifies relevant activities and rights/model; documents control and reassessment triggers; establishes NCI basis; calculates/reconciles NCI; distinguishes retained-control from loss-of-control transactions; prepares evidence/JEs/disclosure support; and records uncertainty/source limitations explicitly.

## Authoritative source register
- IFRS Foundation — IFRS 10 Consolidated Financial Statements landing page: https://www.ifrs.org/issued-standards/list-of-standards/ifrs-10-consolidated-financial-statements/
- IFRS Interpretations Committee — June 2026, Control Assessment for a Single-investor Fund (pipeline/agenda activity): https://www.ifrs.org/news-and-events/updates/ifric/2026/ifric-update-june-2026/
- AASB — AASB 10 current compiled standard: https://standards.aasb.gov.au/aasb-10-nov-2024
- FRC — FRS 102 September 2024 edition, Section 9: https://media.frc.org.uk/documents/FRS_102_September_2024_Redacted_edition_UkckFQ0.pdf
- FRC — significant differences, Section 9 note: https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/uk-accounting-standards/uk-accounting-standards-overview/significant-differences-between-frs-102-and-the-ifrs-for-smes-accounting-standard/
- FASB — ASC Topic 810 source/amendment material; public source-depth limitation applies: https://asc.fasb.org/topic&trid=2129176

Public-repo rights posture: citations, paragraph references where verified, and independently authored explanations only. Do not reproduce licensed standards text as a substitute for the authoritative source.