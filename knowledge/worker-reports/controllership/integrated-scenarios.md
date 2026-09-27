# Controllership cross-topic execution review

Worker desk-check, 2026-09-27. Illustrative facts, not a live ERP test or conclusion about an actual company. These exercise handoffs across owned domains and point to the technical accounting domain where recognition or measurement requires it.

## I-01 — Uninvoiced service and P2P cut-off

**Facts.** An approved annual service contract is for 120,000 paid in advance on 1 July, covering twelve equal months to 30 June. At 31 December, the AP tool shows the invoice and payment; the ERP GL shows 120,000 in prepaid expense and no monthly amortization. The AP tool also contains a separate December 24,000 service receipt not yet invoiced; no GL entry exists. Entity and currency agree; taxes excluded for illustration.

**Expected route.** TOPIC-12-001 verifies receipt/service dates and AP-to-GL completeness. TOPIC-11-003 compares source count/amount, accepted/rejected records and GL postings using run IDs and retained extract filters. TOPIC-02-007 tests the service-period calculation: six of twelve months × 10,000 = 60,000 consumed at 31 December, leaving 60,000 prepaid; assess the separate 24,000 receipt under the relevant expense/liability guidance before posting an accrual. TOPIC-02-002 requires journal support and independent approval. TOPIC-02-004 reconciles prepaid and accrued liability rollforwards to TB. TOPIC-09-003 and 09-005 specify the data population, thresholds, reviewer action and retained evidence; TOPIC-10-002 provides a source-indexed support paper if selected by the auditor.

**Illustrative entries if the service is recognized evenly under the applicable policy and the December receipt establishes an obligation:** debit service expense 60,000 / credit prepaid 60,000; debit December expense 24,000 / credit accrued liability 24,000. The 24,000 conclusion remains conditional on evidence and the governing technical topic; do not assume invoice absence means no liability. Expected balances: prepaid 60,000, accrued liability 24,000. A variance of 24,000 between the receipt population and GL before adjustment is an exception, not a permissible reconciliation plug.

**Failure injection and decision.** If a duplicate retry posts the accrual twice, destination IDs and idempotency key must identify two 24,000 entries; reverse only the duplicate through controlled journal approval. If source receipt date is unknown, stop the cutoff conclusion and obtain support. A reconciled AP invoice count by itself cannot prove the unbilled receipt population is complete.

**Result.** PASS for cross-topic route, arithmetic and fail-stop logic. Evidence to retain: executed contract, invoice/payment IDs, receipt record, period extract/query version, journal IDs, prepaid schedule, AP/source-to-GL bridge, review timestamp and open exception log.

## I-02 — Billing feed and reporting-layer disagreement

**Facts.** The billing system has 1,000 December invoice records totaling 500,000. Interface log shows 995 accepted records totaling 496,000 and five rejected records totaling 4,000. The ERP revenue-related journal batch totals 496,000; reporting dashboard shows 504,000 because eight 1,000 test invoices were included in a warehouse mapping. These totals do not resolve revenue recognition by themselves.

**Expected route.** TOPIC-11-003 and 11-010 reconcile source → accepted/rejected → ERP with stable IDs; 11-008 traces warehouse/reporting mapping and excludes test data under approved release control. TOPIC-12-002 reconciles billing and GL while separating invoicing/cash from recognized revenue. TOPIC-02-001 places the reject resolution on the close critical path; 02-008 requires a quantified flux bridge rather than a “timing” explanation. TOPIC-09-006 challenges report IPE completeness/accuracy, and 09-007 assesses whether repeated reject/mapping failures constitute a control deficiency. TOPIC-10-001 retains the source extracts and bridge for audit. Revenue timing/amount and any GL entries route to Domain 03 technical revenue topics, using executed contracts and performance evidence.

**Arithmetic bridge.** 500,000 source = 496,000 accepted + 4,000 rejected. Dashboard 504,000 = 496,000 ERP batch + 8,000 test records. An 8,000 dashboard difference and a separate 4,000 reject population need different owners and fixes. Neither is a general-ledger plug.

**Failure injection and decision.** If an interface retry reintroduces the five rejects, validate unique IDs and prior acceptance before resubmission; compare totals after reprocessing. If the warehouse test flag is absent, stop external reporting output until lineage and population are proven. Do not book 4,000 revenue merely to match the billing system.

**Result.** PASS for arithmetic, lineage, exception ownership and technical-accounting boundary. Evidence: December source/accepted/rejected lists, job log, GL batch, report SQL/mapping version, reconciliation with unique IDs, disposition of rejects and review approval.

## I-03 — ERP migration, controls and audit opening balances

**Facts.** A legacy AR subledger contains 500,000, but its GL is 480,000. Twenty disputed invoices totaling 20,000 were never posted. Target migration imports 500,000 of open items; a proposed 20,000 suspense credit would make the target TB balance. Separate collections notes assert the invoices were cancelled, but no approved credit notes exist.

**Expected route.** TOPIC-11-005 freezes both original populations and builds an item-level crosswalk. TOPIC-11-002 validates entity/book and customer IDs. TOPIC-12-002/003 establish invoice, dispute, cash and credit states. TOPIC-02-004/005 refuse a clean AR reconciliation without the 20,000 disposition; TOPIC-09-006 validates migration and reporting IPE, TOPIC-10-001/002 retain original-to-target evidence for the auditor. TOPIC-02-009 tests whether any error affects an issued prior period; Domain 03 decides the receivable/revenue and credit-loss treatment. A target equality achieved by suspense is not evidence.

**Arithmetic.** Legacy subledger 500,000 − GL 480,000 = 20,000 gross unreconciled. If evidence eventually supports valid 20,000 credits, the subledger can reduce to 480,000 through approved customer credits and the target reconciles; if invoices are valid, a supported GL adjustment may be appropriate instead. The alternative cannot be selected merely to make totals match. A current-year correction and prior-period restatement have different consequences and need chronology.

**Failure injection.** Migration team posts a 20,000 suspense credit with no invoice IDs and deletes the legacy snapshot. Expected **FAIL**: rollback/hold cutover, preserve snapshots and investigate item-level status. **Result:** PASS for escalation and conditional arithmetic, not a definitive receivable conclusion. Evidence includes item IDs, disputed terms, original issued statements, credit approvals, migration mapping, comparison and sign-off.

## I-04 — Lease modification and intercompany service flow

**Facts.** A subsidiary's lease schedule shows opening liability 200,000, interest 10,000 and payments 40,000, before a 1 October floor-area amendment. The processor increases the liability to 190,000, but has no signed amendment or technical memo. Separately, subsidiary A records an intercompany receivable 100,000; B records payable 95,000. A reporting consolidation draft eliminates 100,000 from both sides.

**Expected route.** The unmodified liability rollforward is 200,000 + 10,000 − 40,000 = 170,000. The extra 20,000 to 190,000 is an unresolved remeasurement, not a balancing plug. TOPIC-12-004/11-003 retain contract population and schedule-to-GL lineage; TOPIC-04-010/011 technical lease topics decide modification date, scope and measurement by actual framework/period before operational posting. TOPIC-02-002 approves any resulting journal; TOPIC-09-003 tests automation input/change controls; TOPIC-10-003 prepares judgment evidence. For intercompany, TOPIC-12-004 preserves both source balances and assigns the 5,000 mismatch before TOPIC-07 elimination conclusions. TOPIC-09-005 and TOPIC-11-008 block an unsupported reporting tie-out.

**Failure injection.** Automated consolidation eliminates 100,000 against a 95,000 liability and books 5,000 to a generic FX account. Expected **FAIL** until counterparty, currency, transaction dates and nature support a specific resolution. **Result:** PASS for two independent fail-stops, arithmetic and cross-worker handoff; no lease or FX accounting conclusion is asserted without technical sources. Evidence: contracts/amendments, source schedules/GL, counterparty confirmations, exception IDs, approvals and reporting bridge.
