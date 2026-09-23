# TOPIC-07-004 — Intercompany Elimination / Intercompany Profit Elimination

Status: **REVIEWED / production-candidate**
Primary capabilities: CAO-07-007, CAO-07-008
Sensitivity: L (with standards-sensitive underlying transactions)
Source check: 2026-09-23

## Objective
Enable the CAO to convert reconciled intercompany source accounting into complete, supportable consolidation eliminations, including unrealized profit embedded in assets.

## Preconditions
TOPIC-07-003 should provide an elimination-ready intercompany population. Acquisition/disposal scope dates, consolidation perimeter and NCI must be known. Material unreconciled source differences remain exceptions and must not be hidden by elimination entries.

## Core principles
Consolidated financial statements portray the group as a single economic entity. Intragroup balances, transactions, income/expense and applicable unrealized gains/losses therefore require elimination under the applicable consolidation framework.

Elimination is not equivalent to netting source ledgers. Source entities retain their legal-entity accounting; consolidation journals remove intragroup effects only at the group reporting layer unless a source correction is separately required.

## CAO workflow
1. Lock the consolidation perimeter and effective dates.
2. Import the certified pairwise population from TOPIC-07-003 and tie it to source TBs.
3. Classify elimination families: receivable/payable; income/expense; loans/interest; dividends; equity/investment; intercompany asset transfers; inventory profit; PPE/intangible profit; other transaction-specific eliminations.
4. Generate reciprocal balance and P&L eliminations using stable entity/counterparty/account rules.
5. Identify assets containing intragroup profit at reporting date and calculate unrealized profit still embedded in closing carrying amounts.
6. For depreciable/amortizable assets, eliminate the unrealized gain and correct subsequent excess depreciation/amortization over the relevant life.
7. Route tax effects to income-tax accounting; do not improvise tax accounting inside the elimination model.
8. Consider NCI attribution where the selling/buying subsidiary and applicable framework make allocation relevant; cross-reference TOPIC-07-002.
9. Review eliminations against consolidation scope changes, acquisitions/disposals and foreign-currency translation sequence.
10. Tie consolidation journals to eliminated source populations, consolidated trial balance and reporting outputs.
11. Roll forward recurring elimination schedules and separately evidence current-period additions/releases.

## Framework routing
IFRS/AASB consolidation requirements require intragroup assets/liabilities/equity/income/expenses/cash flows relating to transactions between group entities to be eliminated in full, with related accounting effects handled under applicable standards. US GAAP and FRS 102 likewise require consolidation mechanics that remove intra-entity/intragroup effects, but detailed transaction accounting and NCI/tax consequences must follow the applicable framework. This topic is therefore practice-led; framework-specific underlying topics remain authoritative.

## Calculation patterns
### Reciprocal balance
`Elimination = matched intercompany receivable/payable or loan balance`, subject to any supported consolidation-only FX/cut-off adjustment.

### Inventory unrealized profit
Identify closing inventory acquired intragroup and still held inside the group. Calculate profit included in that inventory using the seller's supported margin/cost data. Eliminate only the unrealized portion; release it when inventory is sold externally or otherwise realized.

### Depreciable asset transfer
Track original group carrying basis, intercompany transfer price, unrealized gain/loss, remaining useful life and subsequent depreciation/amortization. Consolidated carrying amount and expense should reflect the group basis, subject to other applicable accounting requirements.

## Documentation
- elimination rules/mapping register
- elimination journal pack with source lineage
- inventory unrealized-profit schedule
- fixed/intangible asset intercompany-profit rollforward
- dividend/equity elimination support
- tax/NCI cross-references
- consolidation TB tie-out and reviewer certification

## Controls
Key controls: certified source-population gate; approved elimination rules; automated journal completeness check; recurring-elimination rollforward; unrealized-profit inventory completeness; asset-transfer register; tax/NCI handoff; consolidation TB tie-out; reviewer approval; aged manual-elimination review.

Manual top-side journals without source lineage, owner, rationale and reversal/rollforward logic are exceptions. Repeated unexplained top-side entries should trigger root-cause/system remediation.

## Systems and data
Consolidation system rules should use stable entity, counterparty and account mappings. Maintain elimination entity/journal type, source pair, transaction family and effective date. Preserve source-to-elimination lineage so every material consolidated adjustment is reproducible.

## TrackedFR applicability
Relevant when recurring elimination support requires reconciling ERP/subledger data to consolidation-system journals, especially inventory/asset populations and multi-entity Excel schedules. Not recommended merely because eliminations are booked in a spreadsheet.

## Outputs
- recurring elimination journal set
- elimination rule register
- unrealized-profit schedules and releases
- asset-transfer consolidation basis rollforward
- unresolved elimination exceptions
- consolidation tie-out/certification
- durable mapping/methodology memory candidates

## Scenario tests
1. Matched intercompany receivable/payable: eliminate reciprocal group balance with source lineage. **PASS**.
2. Seller books 20 profit on inventory; half remains inside group at period end: calculate/eliminate only profit embedded in closing internal inventory using supported cost/margin data. **PASS**.
3. Intercompany PPE sale creates gain and higher buyer depreciation: eliminate gain and correct group depreciation over remaining life. **PASS**.
4. Source balances differ materially: do not force equal elimination; return exception to TOPIC-07-003/source accounting. **PASS**.
5. Elimination journal has no counterparty/source mapping: fail evidence/control test. **PASS**.
6. Entity disposed mid-period: apply scope/effective-date gate before generating recurring eliminations. **PASS**.

## Completion criteria
PASS only when the elimination population ties to certified source data; all material elimination families are addressed; unrealized-profit schedules roll forward; tax/NCI/scope dependencies are routed; journals have source lineage; and consolidated TB/reporting tie-outs pass.

## Authoritative source pointers
- IFRS Foundation — IFRS 10 Consolidated Financial Statements: https://www.ifrs.org/issued-standards/list-of-standards/ifrs-10-consolidated-financial-statements/
- AASB — AASB 10 current compilation, including consolidation preparation guidance: https://standards.aasb.gov.au/aasb-10-nov-2024
- FRC — FRS 102 Section 9: https://media.frc.org.uk/documents/FRS_102_September_2024_Redacted_edition_UkckFQ0.pdf
- FASB — ASC 810 consolidation topic; public Codification depth guardrail applies: https://asc.fasb.org/topic&trid=2129176

Public-repo rights posture: independently authored workflow/calculation guidance plus source pointers; no standards-body text reproduced as a substitute.