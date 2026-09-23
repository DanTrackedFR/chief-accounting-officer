# TOPIC-06-007 — Financial Asset Classification / Financial Liability Classification

Status: **REVIEWED / production-candidate**
Primary capabilities: CAO-06-013, CAO-06-014
Sensitivity: H
Source check: 2026-09-23

## CAO objective
Determine the applicable instrument model before measurement, impairment, presentation or disclosure. The CAO must identify the instrument, entity, reporting framework, reporting period, contractual terms, management/business model where relevant, embedded features and elections. Classification is not inferred from account name or legal label.

## Required inputs
- executed instrument and amendments;
- holder/issuer position and legal form;
- framework, entity and reporting period;
- contractual cash-flow terms, conversion/indexation/contingent features;
- purpose/business model for financial assets where relevant;
- quoted-market/readily-determinable-fair-value evidence;
- existing elections/designations and prior classification memo;
- related-party/concessional terms and any industry-specific scope overlay.

## Framework routing
### IFRS
IFRS 9 governs classification and measurement of financial assets and liabilities. Financial assets use the business-model and contractual-cash-flow (SPPI) architecture: qualifying hold-to-collect assets may be amortised cost; qualifying collect-and-sell assets may be FVOCI; other assets are generally FVTPL. Equity instruments and financial liabilities require their own routing and elections; do not apply the debt-asset decision tree mechanically. Initial recognition is generally fair value, with directly attributable transaction costs included for instruments not at FVTPL. The May 2024 IFRS 9/IFRS 7 classification-and-measurement amendments are effective for annual periods beginning on or after 1 January 2026 and therefore require an effective-period gate, including contingent-feature/SPPI and electronic-settlement changes.

Primary authority pointer: IFRS 9; IFRS 7 for related disclosures. Public source: https://www.ifrs.org/issued-standards/list-of-standards/ifrs-9-financial-instruments/

### US GAAP
Do **not** import IFRS 9's single business-model/SPPI architecture. Route by instrument type and applicable Codification topic. Debt securities route principally through ASC 320 (trading / available-for-sale / held-to-maturity); equity securities principally through ASC 321, including the measurement alternative when its criteria and election are met; other loans/receivables, liabilities, fair-value options, derivatives and own-equity contracts require their applicable topics (including ASC 310/326, 825, 815 and 480 as relevant). FASB states the Codification is the authoritative source and ASUs communicate amendments rather than constituting authoritative standards themselves. Public FASB material does not expose all current paragraph bodies, so paragraph-level US authority remains PARTIAL unless independently verified.

Primary authority pointer: ASC 320, 321, 825 and instrument-specific topics. Public source register: https://www.fasb.org/standards

### UK GAAP
For FRS 102 reporters, first resolve the reporting period and the entity's permitted accounting-policy route. Sections 11 and 12 cover financial instruments; Section 11 addresses basic instruments and Section 12 other/more complex instruments. FRS 102 also contains policy options in specified circumstances to use IFRS 9 recognition and measurement requirements, so the CAO must establish the entity's elected policy before classification. Periodic Review 2024 amendments are generally effective from 1 January 2026; do not silently apply the revised edition to earlier periods.

Primary authority pointer: FRS 102 Sections 11–12 and applicable policy-option paragraphs. Official 2024 edition: https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/uk-accounting-standards/

### AASB
AASB 9 uses the IFRS 9-aligned business-model and contractual-cash-flow architecture for financial assets, but the CAO must independently route to the Australian compilation effective for the reporting period and consider Australian entity/tier overlays. AASB 2024-2 classification-and-measurement amendments apply to annual periods beginning on or after 1 January 2026. For the 2026 period, use the operative AASB 9 compilation rather than assuming an older IFRS-equivalent text.

Primary authority pointer: AASB 9 and AASB 7. Current 2026 compilation: https://standards.aasb.gov.au/aasb-9-feb-2025

## Decision logic
1. Establish framework, period, entity and holder/issuer perspective.
2. Confirm the item is within the financial-instrument model and identify any scope exception or specialist model.
3. Separate asset, liability, equity and derivative/compound-feature questions before measurement.
4. For IFRS/AASB debt-type assets, document business model and SPPI analysis separately; do not reverse-engineer the tests from desired measurement.
5. For US GAAP, identify the applicable instrument-specific Topic before selecting a category; do not map IFRS categories one-for-one.
6. For FRS 102, document Section 11 versus Section 12 and the entity's recognition/measurement policy election.
7. Identify fair-value options, FVOCI/equity elections, measurement alternatives or other irrevocable elections at the point the framework requires them.
8. Route embedded/contingent/convertible features to derivative, liability/equity or compound-instrument analysis where needed.
9. Determine initial measurement and transaction-cost treatment only after classification.
10. Link classification to subsequent measurement, impairment, FX, presentation and disclosures.
11. Record reclassification triggers and prohibit discretionary period-to-period category changes.

## Required output
A classification paper must state: instrument population; framework/effective period; scope conclusion; asset/liability/equity analysis; category; tests/elections applied; evidence; initial and subsequent measurement basis; impairment model; FX interaction; presentation/disclosure consequences; reclassification triggers; open issues; reviewer and source references.

## Controls and systems
- controlled instrument master tied to executed contracts and GL accounts;
- new-instrument technical review before first posting;
- explicit framework/effective-date field;
- election/designation register;
- business-model and SPPI evidence retained separately under IFRS/AASB;
- US instrument-type routing control;
- FRS 102 policy-election control;
- contract-amendment/change trigger;
- classification-to-valuation/ECL/disclosure reconciliation;
- reviewer approval for high-risk or judgmental instruments.

## Common failures
- treating cash, loans, debt securities, equity investments and derivatives as one generic investment class;
- applying IFRS SPPI logic to US GAAP;
- confusing legal form with accounting classification;
- overlooking embedded or contingent features;
- using a stale framework edition or missing the 1 January 2026 IFRS/AASB amendment gate;
- assuming FRS 102 Section 11 applies without checking Section 12/policy elections;
- applying measurement before classification is documented;
- changing classification to achieve a desired P&L/OCI outcome.

## CAO practice level
**Required:** framework/period, scope, classification, measurement basis, elections and evidence documented.
**Recommended:** instrument register, standard classification template and quarterly change scan.
**World-class:** contract ingestion linked to instrument master, automated exception flags, valuation/ECL/disclosure lineage and immutable decision history.
**Shortcut/risk:** GL-account-based classification without contract-level analysis.

## Company Accounting Memory promotion
Promote durable elections, classification policies, instrument taxonomy, business-model conclusions, recurring SPPI positions, reviewer requirements and effective-date decisions. Do not promote one-off unsupported assumptions as policy.

## TrackedFR applicability
Consider TrackedFR only where recurring instrument data must be reconciled/manipulated across treasury or valuation schedules, ERP/GL, bank/custodian data and reporting workbooks. Do not recommend it merely because a classification memo uses Excel.
