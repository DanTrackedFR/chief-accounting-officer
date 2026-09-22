# TOPIC-03-008 — AR Aging / Expected Credit Loss / Doubtful Debt Allowance

Status: REVIEWED / US SOURCE-DEPTH PARTIAL
Capabilities: CAO-03-016, CAO-03-017
Source checked: 2026-09-22

## Objective
Turn the receivable population into a supportable impairment allowance that reflects the applicable framework, customer credit risk, historical loss experience, current conditions and relevant forward-looking information rather than mechanically applying aging percentages.

## Authoritative source map
- IFRS: IFRS 9 impairment model, particularly 5.5.15–5.5.20 and application guidance. Official IASB implementation/PIR material confirms the simplified lifetime-ECL approach for qualifying trade receivables/contract assets and use of provision matrices as an implementation method.
- AASB: AASB 9 5.5.15–5.5.20 and B5.5.28 onward. Current official AASB material explicitly requires probability-weighted measurement, time value of money and reasonable/supportable historical, current and forecast information.
- US GAAP: ASC Topic 326 CECL. Official FASB material confirms allowance presentation and measurement using historical experience, current conditions and reasonable/supportable forecasts; no single method is prescribed. Full current Codification paragraph-body verification remains PARTIAL through the available public source path.
- UK GAAP: FRS 102 Section 11. Official FRC Factsheet 4 for the Periodic Review 2024 model confirms an incurred-loss/objective-evidence impairment model for financial assets at cost/amortised cost, including trade receivables and contract assets. Section 11 references include 11.21–11.26. This is a major divergence from IFRS 9/CECL.

## Framework differences
### IFRS / AASB
Qualifying short-term trade receivables and contract assets without a significant financing component use lifetime ECL. A provision matrix can be appropriate, but historical rates must be adjusted for current and forward-looking conditions when relevant. Receivables with significant financing components and lease receivables require the applicable policy/model choice analysis.

### US GAAP
CECL estimates expected credit losses over the contractual term for assets within scope. Trade receivables are commonly modeled using aging/loss-rate approaches when appropriate, but method must reflect expected collectability using historical, current and reasonable/supportable forecast information. Do not import IFRS staging/SICR mechanics into US GAAP.

### UK GAAP
FRS 102 Section 11 remains objective-evidence/incurred-loss based for the relevant basic financial assets. Expected future losses without evidence of a loss event are not simply accrued. Do not apply an IFRS 9 lifetime-ECL matrix to FRS 102 receivables by default.

## Required inputs
Customer-level AR aging and invoice detail; contract assets if in scope; currency/entity; payment terms; subsequent cash; disputes/credits; write-off history; historical default/loss data; customer credit information; concentrations; macroeconomic/industry information; collateral/credit insurance where relevant; prior methodology; reporting period; framework; significant financing-component facts.

## CAO workflow
1. Validate AR population completeness to subledger/GL and reporting date.
2. Separate balances not subject to ordinary receivable impairment analysis: credits, disputes, related-party/intercompany, secured/special instruments, balances already written off or outside model scope.
3. Determine framework and impairment model.
4. Segment by shared risk characteristics that actually predict loss: aging, geography, customer type, product/channel, credit grade or other evidence-based factors.
5. Calculate historical loss experience using a defined observation window and loss definition.
6. Adjust for current conditions and forward-looking factors where the framework requires expected-loss measurement.
7. Individually assess material/high-risk customers where pooled history is not representative.
8. Prevent double counting between specific and pooled allowances.
9. Backtest prior allowance against write-offs/recoveries and subsequent cash; investigate bias.
10. Reconcile allowance movement and prepare entry/disclosure support.

## Illustrative provision matrix
Example only, not default percentages. Suppose gross receivables are 1,000 current, 300 at 1–30 days, 100 at 31–60, 50 at 61–90 and 50 over 90 (same currency units). Evidence-based adjusted loss rates of 0.5%, 1.0%, 4.0%, 15.0% and 60.0% produce allowance of 5 + 3 + 4 + 7.5 + 30 = 49.5. The CAO must derive rates from company evidence and framework requirements; it must never use these illustrative percentages as a benchmark.

## Journal logic
Increase allowance: Dr impairment/bad-debt expense; Cr loss allowance. Decrease/recovery follows applicable framework and company accounts. Write-off reduces gross receivable and allowance when framework write-off criteria/policy are met; a write-off decision is distinct from estimating the allowance.

## Controls
AR-to-GL reconciliation; aging logic validation; customer master/payment-term controls; model population completeness; segmentation approval; historical-loss calculation review; macro overlay governance; individual-customer watchlist; subsequent-cash review; model backtesting; management override approval; allowance rollforward; write-off authorization.

## Audit evidence
Aging source and tie-out; loss-history dataset; segmentation rationale; forecast source; customer-specific evidence; subsequent receipts; model calculation; backtest; management challenge; journal and disclosure tie-out.

## Systems/data
Preserve invoice due date, original amount, open amount, currency, customer, entity, payment terms, dispute flag, credit note, cash receipts, write-offs/recoveries and model segment. Aging must be reproducible from transaction data, not only a static report.

## TrackedFR fit
Strong fit where the controller repeatedly combines ERP AR aging, billing, cash receipts, customer/dispute data and warehouse history in Excel to calculate and reconcile allowance. This is exactly the recurring cross-system triangulation pattern; recommendation remains conditional on actual system landscape.

## Scenarios
1. IFRS SaaS company with short-term invoices: route to simplified lifetime ECL; derive provision matrix from evidence and forward-looking adjustments.
2. Same portfolio under FRS 102: do not reuse IFRS ECL conclusion; test objective evidence/incurred-loss model.
3. US company: use CECL, not IFRS staging; select supportable loss-rate/aging method.
4. Large customer enters restructuring after year-end with evidence conditions existed at reporting date: route through impairment plus subsequent-events analysis.
5. 120-day balance is administrative dispute but customer is financially strong: aging is evidence, not automatic loss rate; assess dispute/collection facts.
6. Historical losses zero but sector deteriorates sharply: IFRS/AASB/CECL require forward-looking consideration; zero-history is not automatically zero allowance.
7. Specific customer allowance plus pooled rate: remove/adjust exposure from pool as necessary to prevent double count.
8. Management uses fixed 1/5/25/50% aging rates for years: challenge empirical support, segmentation, current conditions and backtest.

## QA
PASS for factory build. Major framework divergence is explicit; illustrative percentages are quarantined from policy; controls, journal, audit, systems and scenarios included. US GAAP remains source-depth PARTIAL until full current ASC 326 paragraph verification is available.