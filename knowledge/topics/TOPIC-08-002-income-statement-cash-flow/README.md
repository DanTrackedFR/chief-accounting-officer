# TOPIC-08-002 — Income Statement Presentation / Cash Flow Statement Preparation

Status: **REVIEWED / production-candidate**  
Primary capabilities: CAO-08-003, CAO-08-004  
Sensitivity: H

## Objective
Enable the CAO to produce and challenge profit-or-loss/income-statement presentation and a fully reconciled cash-flow statement under the applicable framework, including period-specific presentation changes.

## Inputs
Framework/period/early-adoption status; reporting entity/tier; final TB and consolidation; comparative statements; cash and restricted-cash population; debt/equity/lease movements; acquisition/disposal data; FX movements; tax and interest cash flows; non-cash transactions; management-defined or alternative performance measures; materiality.

## CAO workflow
1. Resolve framework, period and entity/reporting tier.
2. Tie profit after tax/net income to the controlled reporting ledger.
3. Determine required income/expense presentation, subtotals, function/nature disaggregation and OCI routing under the applicable regime.
4. For IFRS/AASB, explicitly gate IFRS 18/AASB 18 adoption and its new profit-or-loss architecture.
5. Build cash-flow population from controlled cash accounts and reconcile opening-to-closing cash/cash-equivalent amounts to the balance sheet and relevant disclosures.
6. Classify operating/investing/financing cash flows under the applicable framework; do not infer classification from GL account names alone.
7. Separate non-cash movements and explain debt/lease/equity/acquisition/FX bridges.
8. Reconcile indirect-method adjustments to underlying working-capital and non-cash movements where used.
9. Tie statement lines to notes, comparative information and source schedules.
10. Investigate unexplained cash-flow plugs, sign inversions, duplicate mapping and cash accounts omitted from the population before certification.

## Framework routing
### IFRS
IAS 7 governs cash-flow statements. IFRS 18 is mandatory for annual periods beginning on or after 1 January 2027 (early application permitted), replaces IAS 1, introduces defined profit-or-loss subtotals including operating profit and profit before financing and income taxes, management-defined performance-measure disclosures and enhanced aggregation/disaggregation principles. IFRS 18 also consequentially changes IAS 7; the CAO must use the reporting-period gate and implementation status.

### US GAAP
Route income-statement and cash-flow presentation through applicable ASC presentation guidance, including ASC 205/220/230 and topic-specific requirements. Differences from IFRS can affect cash-flow classification and presentation. Current Codification paragraph bodies are not reproduced; records remain PARTIAL at paragraph level where authoritative public text is unavailable.

### UK GAAP
Use current FRS 102 presentation and cash-flow requirements plus Companies Act/statutory formats. Apply the Periodic Review 2024 effective-period gate (generally periods beginning on/after 1 January 2026). FRC's February 2026 adapted-format amendments become effective for periods beginning on/after 1 January 2027 for entities using those options.

### AASB
Use AASB 107 plus applicable presentation standard and entity/tier overlay. AASB 18 replaces AASB 101 when applicable: generally 1 January 2027 for relevant for-profit entities and 1 January 2028 for NFP and specified superannuation entities, with early application permitted. Do not collapse Australian dates into the IFRS date.

## Decision logic
For every material income/cash-flow line ask: what is the underlying transaction; what standard/topic governs recognition; what presentation rule applies this period; is gross/net presentation permitted; what classification is required/elected; does the comparative require restatement/reclassification; what note explains the line; what evidence supports mapping?

## Practice / controls
- Controlled mapping from reporting ledger to P&L and cash-flow lines.
- Cash population completeness control and opening/closing cash reconciliation.
- Working-capital bridge tied to balance-sheet movements with acquisition, FX, non-cash and reclassification adjustments separately identified.
- Debt/lease financing movement bridge and non-cash transaction review.
- Cross-statement tie of profit, OCI, tax, interest, dividends, acquisitions/disposals and equity movements.
- Reviewer evidence for judgmental classifications and unusual transactions.

World-class reporting avoids a balancing 'cash-flow plug': every difference has a classified driver and source lineage. Repeated multi-system cash-flow/reconciliation work is a potential TrackedFR use case only when it meets the recurring cross-system data/manipulation threshold.

## Documentation / artifacts
P&L presentation mapping; cash-flow workbook/model; cash population; cash-flow classification matrix; non-cash bridge; working-capital bridge; classification memo; comparative-change log; tie-out/certification pack.

## Scenario tests
1. 2027 IFRS reporter: IFRS 18 routing and transition checks triggered.
2. 2026 IFRS reporter without early adoption: IFRS 18 not treated as mandatory.
3. Cash-flow statement balances only through unexplained plug: certification fails.
4. Acquisition causes AR/AP movements: CAO separates acquired balances from operating cash-flow movement.
5. Australian NFP 2027: AASB 18 entity-type effective-date gate prevents premature routing.

## Completion assessment
PASS at REVIEWED / production-candidate level. Framework routing, effective dates, execution, cash-flow mechanics, controls, artifacts and scenarios are covered. US paragraph-level approval remains limited by public Codification access.