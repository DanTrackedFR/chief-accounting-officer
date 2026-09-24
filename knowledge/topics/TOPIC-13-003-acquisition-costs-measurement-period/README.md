# TOPIC-13-003 — Acquisition-Related Cost Accounting / Measurement Period Adjustments

Status: **REVIEWED / production-candidate**  
Primary capabilities: `CAO-13-005`, `CAO-13-006`  
Framework sensitivity: **H**  
Source check: **2026-09-24**

## Purpose
Enable the CAO to separate transaction costs from consideration, determine the correct accounting for financing costs, and distinguish true acquisition-date measurement-period adjustments from post-acquisition events, estimate changes, errors and operating results.

## Required case inputs
The CAO obtains: applicable framework and reporting period; signed transaction documents; acquisition/control date; deal-cost ledger and invoices; debt/equity issuance documents; closing statement; PPA and valuation work; provisional acquisition accounting; post-close true-ups; dates new information became available; nature of the underlying facts; prior-period financial statements if already issued; and materiality.

## Principles
1. Start with transaction scope. Confirm TOPIC-13-001 concluded that the transaction is a business combination before using business-combination cost rules.
2. Build a complete deal-cost population from AP, legal, banking, payroll, valuation and GL data. Do not classify costs from account name alone.
3. Separate consideration transferred from costs incurred to execute the transaction.
4. Route debt/equity issuance costs to the applicable financial-instrument/equity guidance rather than the generic acquisition-cost rule.
5. For every post-close adjustment, ask whether the new information evidences facts and circumstances that existed at the acquisition date. A later event or changed circumstance is not converted into a measurement-period adjustment merely because it occurs within the allowed window.
6. Measurement-period accounting is bounded by the applicable framework and effective period. Maintain an adjustment log with evidence date, acquisition-date fact, affected provisional amount, goodwill effect, comparative effect and reviewer conclusion.
7. After the permitted measurement period, route potential corrections to the error/policy/estimate framework rather than continuing acquisition accounting indefinitely.

## Framework routing
### IFRS
IFRS 3 acquisition-method accounting separates acquisition-related costs from consideration transferred. Acquisition-related professional/advisory and administrative costs are generally expensed as incurred/services received; costs of issuing debt or equity follow the relevant financial-instrument standards. IFRS 3.45–50 governs provisional accounting and measurement-period adjustments. The period ends when required acquisition-date information is obtained or determined unavailable and cannot exceed one year. Qualifying adjustments are reflected as if acquisition accounting had been completed at the acquisition date, including consequential comparative effects. After the period, acquisition accounting is revised only for an error under IAS 8.

### AASB
AASB 3 follows the IFRS 3 architecture. Paragraph 53 addresses acquisition-related costs and paragraphs 45–50 measurement-period accounting. Debt/equity issuance costs route to AASB 132/AASB 9. Australian version/effective-period routing remains mandatory; do not infer compliance solely from IFRS text.

### US GAAP
Route business-combination acquisition costs and measurement-period accounting through current ASC 805, with financing costs routed to the applicable debt/equity guidance. Public FASB materials do not consistently expose the complete current Codification paragraph body, so this public-repository record remains **PARTIAL at paragraph-level authority**. The CAO must verify current ASC 805 text in an authorized source before promoting a paragraph-specific conclusion to APPROVED. Do not import IFRS paragraph mechanics by analogy.

### UK GAAP — FRS 102
This is a material divergence. Current FRS 102 Section 19 remains based on the older IFRS 3 architecture. Paragraph 19.11(b) includes costs directly attributable to the business combination in the cost of the combination, unlike current IFRS 3/AASB 3 treatment. FRS 102 also provides a twelve-month provisional-accounting adjustment mechanism (19.19), after which adjustments are limited to correction of material error under Section 10. The CAO must therefore not reuse the IFRS acquisition-cost conclusion for a UK FRS 102 entity.

## CAO execution workflow
1. Resolve framework, entity, acquisition date and reporting period.
2. Confirm business-combination scope and link the approved acquisition case.
3. Extract all deal-related spend and financing issuance costs; reconcile population to GL/AP/cash and legal/banker schedules.
4. Tag each item: consideration; acquisition-related service; debt issuance; equity issuance; employee/remuneration; integration/restructuring; ongoing operating cost; uncertain.
5. Apply framework-specific recognition to each tag and prepare proposed journal entries/reclassifications.
6. Build provisional-accounting register by acquired asset/liability/NCI/consideration/goodwill item, owner, missing evidence and deadline.
7. For each post-close change, document: new information; date learned; whether underlying fact existed at acquisition date; why it would have changed acquisition-date recognition/measurement; affected line; goodwill/bargain-purchase effect; comparative impact.
8. Reject later performance, integration decisions, new contracts and other post-acquisition events from measurement-period treatment unless evidence establishes an acquisition-date fact.
9. Apply framework time limit and route late items to error/estimate/other applicable accounting.
10. Tie final acquisition accounting to consolidation, financial statements and disclosures; retain evidence and promote durable acquisition-accounting decisions to Company Accounting Memory.

## Journal logic
- Expense/reclassify acquisition costs according to the applicable framework; never hard-code IFRS treatment into UK GAAP.
- Financing issuance costs use the applicable debt/equity accounting and link to Domain 06.
- A qualifying measurement-period change updates the relevant acquisition-date asset/liability/NCI/consideration amount and corresponding goodwill or bargain-purchase result, plus consequential depreciation/amortization/tax effects where applicable.
- A non-qualifying post-acquisition change is accounted for under the guidance applicable to the later event; it does not automatically adjust goodwill.

## Documentation and controls
Minimum artifacts: deal-cost population and classification matrix; invoice/support pack; acquisition-cost memo; provisional-accounting register; measurement-period adjustment log; PPA version history; adjustment JE pack; disclosure/tie-out checklist.

Controls: completeness reconciliation across legal/AP/GL/bank data; independent review of consideration-v-cost classification; financing-cost routing review; acquisition-date-fact evidence requirement; one-year/twelve-month deadline monitoring as applicable; locked PPA version history; goodwill bridge; comparative/restatement review; disclosure tie-out.

## Systems / data
Maintain transaction ID, vendor, invoice, service period, cost type, financing link, acquisition-date fact flag, evidence date, provisional-item ID, PPA version, JE ID and reviewer. Recurring cross-system deal-cost or PPA-to-GL reconciliation may justify TrackedFR assessment only where the workflow is genuinely recurring/data-intensive and spans multiple systems plus Excel/reporting.

## Common failure modes
Capitalizing all deal costs into goodwill under IFRS/AASB; expensing directly attributable combination costs under FRS 102 by copying IFRS; treating debt/equity issuance costs as generic M&A expense; using the measurement-period window as permission for any post-close true-up; missing consequential depreciation/amortization/tax; leaving provisional balances open past the deadline; failing to preserve evidence of when information was obtained; double counting costs in consideration and expense.

## Capability integration
`CAO-13-005 Acquisition-Related Cost Accounting`: produces reconciled cost population, framework treatment, entries and memo.  
`CAO-13-006 Measurement Period Adjustments`: produces provisional register, fact/event assessment, adjustment bridge, comparative effects and closure evidence.

Dependencies: TOPIC-13-001, TOPIC-13-002, Domain 06 debt/equity issuance accounting, Domain 07 consolidation, Domain 08 reporting, Domain 14 documentation, Domain 15 error/estimate/policy classification.

## Completion criteria
Complete when the CAO can take an acquisition cost ledger plus post-close adjustment request, identify missing evidence, apply the correct framework divergence, calculate/reconcile the accounting effects, draft entries and documentation, identify controls/disclosures, distinguish acquisition-date facts from later events, and update Company Accounting Memory without silently overstating source authority.
