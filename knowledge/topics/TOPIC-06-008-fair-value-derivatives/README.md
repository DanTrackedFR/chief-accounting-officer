# TOPIC-06-008 — Fair Value Measurement / Derivative Accounting

Status: **REVIEWED / production-candidate**
Primary capabilities: `CAO-06-016`, `CAO-06-017`
Sensitivity: **H**

## CAO objective
Take a valuation or contract population from facts to a defensible accounting conclusion: determine whether fair value is required/permitted, identify the unit of account and measurement date, select market-participant assumptions and valuation technique, classify inputs, identify derivatives and scope exceptions, determine measurement/P&L-OCI routing, prepare entries and disclosures, and leave reviewable evidence.

## Required inputs
Framework and reporting period; entity/reporting tier; instrument/asset/liability and executed contracts; purpose and contractual cash flows; market/observable data; valuation models and third-party reports; counterparty/own-credit data where relevant; elections and existing policies; derivative inventory; collateral/netting arrangements; prior-period hierarchy and valuation conclusions.

## PRINCIPLES
1. Fair value is a market-based exit-price measurement at the measurement date, not management's entity-specific value.
2. The standard that requires or permits fair value determines the unit of account; the fair-value standard supplies the measurement framework.
3. Use the principal market, or in its absence the most advantageous market, accessible to the entity; transaction costs are not part of fair value, while transport costs can be relevant when location is an asset characteristic.
4. Maximise relevant observable inputs and minimise unobservable inputs. Technique choice follows facts and available data; market, income and cost approaches are methods, not a hierarchy of preferred answers.
5. Hierarchy classification follows the lowest-level input significant to the entire measurement: Level 1 unadjusted quoted price for an identical item in an active market; Level 2 other observable inputs; Level 3 significant unobservable inputs.
6. A model output is not self-validating. Governance must establish source data, assumptions, calibration, independent review, change control and period-end back-testing where useful.
7. Derivative accounting begins with contract identification and scope. Do not assume that every variable-price contract is a derivative or that every derivative is eligible for hedge accounting.
8. A derivative normally requires an underlying, notional/payment provision, little or no initial net investment relative to similar exposure, and net settlement characteristics under the applicable framework; scope exceptions and embedded features must be assessed under that framework.
9. Unless a qualifying hedge-accounting relationship or another specific model changes presentation, derivatives are generally remeasured at fair value with changes routed through earnings/profit or loss.
10. Hedge accounting is deliberately separated into TOPIC-06-009. This topic determines derivative recognition/measurement and hands qualifying designations to that topic.

## STANDARDS routing
### IFRS
- IFRS 13 defines fair value and provides the measurement/disclosure framework when another IFRS requires or permits fair value. Core architecture: objective/scope 1–8; measurement 9–90; valuation techniques 61–66; inputs 67–71; hierarchy 72–90; disclosures 91 onward.
- IFRS 9 governs financial-instrument and derivative recognition/measurement and embedded-derivative routing. IFRS 7 supplies financial-instrument disclosures.
- Do not apply IFRS 13 as though it creates a new recognition basis; first identify the standard requiring/permitting fair value.
- IFRS 13 itself identifies scope/disclosure exceptions, including share-based payment and lease transactions and certain measurements that resemble but are not fair value.

### AASB
- AASB 13 is IFRS 13-aligned for the core fair-value framework. Current AASB material defines fair value as an orderly market-participant exit price and requires relevant observable inputs to be maximised.
- AASB 9 governs financial instruments/derivatives; AASB 7 disclosures; AASB 132 presentation. Resolve Australian reporting tier and effective-period compilation before final disclosure output.

### US GAAP
- ASC 820 is the fair-value measurement framework; ASC 815 governs derivatives and hedging, with instrument-specific Topics also relevant.
- Preserve US-specific derivative scope exceptions and embedded-derivative rules; do not import IFRS 9 bifurcation conclusions.
- **Effective-date gate:** ASU 2025-07 refined Topic 815 derivative scope and also clarified share-based noncash consideration from customers. Resolve entity type and adoption date before applying it.
- FASB issued proposed Topic 815 targeted hedge improvements in June 2026. They are **not current GAAP** unless and until finalized/effective.
- Public FASB sources do not expose every current Codification paragraph body. US paragraph-level status remains `PARTIAL` unless directly verified from authoritative Codification access.

### UK GAAP
- Use the reporting-period gate. FRS 102 Periodic Review 2024 has principal effective date 1 January 2026.
- For 2026+ periods, Section 2A contains the fair-value measurement model; Sections 11/12 govern financial instruments and other financial-instrument issues. Section 12 includes revised hedge accounting based on IFRS 9 concepts.
- FRS 102 contains recognition-and-measurement policy options in the financial-instrument sections. Establish the entity's elected basis before concluding.
- Do not assume the IFRS 13 three-level disclosure package applies to every FRS 102 entity; current FRC material notes specific hierarchy requirements for certain specialised entities and transaction-specific disclosures elsewhere.

## Framework differences that matter
| Issue | IFRS / AASB | US GAAP | UK GAAP FRS 102 |
|---|---|---|---|
| Fair-value framework | IFRS 13 / AASB 13 | ASC 820 | Section 2A for current 2026+ model |
| Derivative model | IFRS 9 / AASB 9 | ASC 815 | Sections 11/12 or permitted elected basis |
| Embedded features | IFRS 9 host-dependent model | ASC 815 instrument-specific bifurcation | Depends on FRS 102 election and Sections 11/12 |
| Hierarchy/disclosure | Three-level hierarchy | Three-level hierarchy | Do not mechanically import full IFRS hierarchy disclosure to all entities |
| Current change gate | normal effective-date checks | ASU 2025-07 adoption; 2026 hedge proposal not current GAAP | Periodic Review 2024 principally effective 1 Jan 2026 |

## CAO execution workflow
1. Lock framework, reporting period, entity type/tier and policy elections.
2. Establish the accounting unit and why fair value is required/permitted.
3. Establish measurement date, principal market and market participants.
4. Obtain independent market data and model/source lineage.
5. Select valuation technique and document why it fits the instrument and available data.
6. Identify significant inputs; determine observable/unobservable status and hierarchy level.
7. Reconcile opening-to-closing fair values and independently challenge significant changes.
8. For contracts, run derivative definition and scope-exception assessment before measurement.
9. Assess embedded features under the applicable framework and host classification.
10. Measure recognised derivative at fair value and determine default P&L/earnings routing.
11. If management has designated a hedge, hand off to TOPIC-06-009 before concluding OCI/basis-adjustment treatment.
12. Prepare entries, disclosures and fair-value hierarchy/rollforward support as applicable.
13. Reconcile valuation population to treasury/legal records, subledger and GL.
14. Produce conclusion memo, valuation evidence pack and open-item log; promote durable elections/methodologies to Company Accounting Memory.

## Calculations and examples
### Simple forward mark-to-market control
For a receive-foreign-currency forward, a control valuation can be expressed as the present value of the difference between contracted and current forward economics for the remaining term. Production valuation must reflect contract convention, currency pair, settlement mechanics, curves, credit/non-performance effects where applicable and the framework's unit of account.

### Hierarchy example
An exchange-traded share measured using an unadjusted quoted price for the identical share in an active market is normally Level 1. A vanilla interest-rate swap valued from observable yield curves is commonly Level 2. A private-company instrument with a material unobservable revenue multiple or probability-weighted scenario input can be Level 3. Classification follows the significant inputs actually used, not the label of the instrument.

## Documentation
Minimum pack: scope/measurement-basis memo; instrument/contract inventory; valuation methodology; market-data evidence; model/version evidence; input hierarchy assessment; independent price verification/model validation evidence; derivative and embedded-feature assessment; accounting entries; disclosure support; reconciliation to GL; reviewer sign-off; effective-date/election record.

## Controls / audit / systems
- Completeness control over derivative and fair-value populations using treasury, legal, procurement, investment and GL sources.
- Approved valuation-source hierarchy and stale-price/escalation rules.
- Independent price verification for material externally priced positions.
- Model inventory, validation, access/change control and version retention.
- Level 3 assumption approval, sensitivity/reasonableness review and rollforward control.
- Contract-change trigger for derivative/embedded-feature reassessment.
- GL-to-valuation and disclosure tie-outs with reconciling-item ownership.
- Effective-date control for accounting-standard changes.
- TrackedFR is relevant only where recurring cross-system valuation/contract/GL data must be reconciled or manipulated; it is not recommended merely because a valuation workbook exists.

## Scenario tests
1. Active-market listed security → quoted identical active-market price → Level 1.
2. OTC vanilla swap using observable curves → derivative recognised; likely Level 2; hedge status separately assessed.
3. Private investment using significant unobservable forecast/multiple → Level 3 with assumption governance.
4. Commodity purchase contract with variable price → do not label derivative until scope/net-settlement/normal-use or applicable exception analysis is complete.
5. Convertible/structured host → embedded-feature analysis routed by framework; no cross-framework shortcut.
6. US contract potentially affected by ASU 2025-07 → adoption/effective-date gate required.
7. UK period beginning 1 Jan 2026 → current FRS 102 Section 2A/Sections 11–12 routing.
8. UK pre-2026 period → prior-version routing; do not retroactively apply 2026 architecture.
9. Management calls a valuation Level 2 but material unobservable input drives value → Level 3 challenge.
10. Designated hedge → TOPIC-06-009 required before OCI/basis accounting conclusion.

## QA result
**PASS — REVIEWED / production-candidate.** All primary capabilities covered; all four active frameworks routed; current-change gates identified; fair-value and derivative logic separated from hedge accounting; calculations/practice/controls/audit/systems and 10 scenarios included. Residual US Codification paragraph-depth limitation is explicitly retained rather than inferred.

## Authoritative source register — checked 2026-09-23
- IFRS Foundation — IFRS 13 Fair Value Measurement overview and supporting material: https://www.ifrs.org/issued-standards/list-of-standards/ifrs-13-fair-value-measurement/
- FASB — ASU 2025-07, Derivatives and Hedging (Topic 815) and Revenue (Topic 606): https://www.fasb.org/Page/Document?pdf=ASU+2025-07.pdf
- FASB — proposed Topic 815 targeted improvements, June 2026 (pipeline only): https://www.fasb.org/Page/Document?pdf=Proposed+ASU+Derivatives+and+Hedging+%28Topic+815%29.pdf
- FRC — FRS 102 current edition / Periodic Review status: https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/uk-accounting-standards/frs-102/
- FRC — current FRS 102 differences page (updated February 2026): https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/uk-accounting-standards/uk-accounting-standards-overview/significant-differences-between-frs-102-and-the-ifrs-for-smes-accounting-standard/
- AASB — AASB 13 current compilation: https://standards.aasb.gov.au/aasb-13-dec-2022
- AASB — AASB 9 current compilation navigator: https://standards.aasb.gov.au/aasb-9-sep-2020

Public-repository rights posture: authoritative sources are referenced, not reproduced. Explanations above are independently authored.