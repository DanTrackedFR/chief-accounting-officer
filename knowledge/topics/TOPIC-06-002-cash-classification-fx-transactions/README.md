# TOPIC-06-002 — Cash Classification & Presentation / Foreign Currency Transaction Accounting

Status: **REVIEWED / production-candidate**  
Primary capabilities: `CAO-06-004`, `CAO-06-005`  
Sensitivity: **H**  
Last source check: **2026-09-23**

## Objective
Enable the CAO to determine what belongs in cash and cash equivalents, resolve restricted/overdraft/presentation questions, and account for transactions denominated in a currency other than the entity's functional currency from initial recognition through settlement or period-end remeasurement.

This topic inherits bank-reconciliation and restricted-cash mechanics from TOPIC-06-001 and hands period-end remeasurement/translation to TOPIC-06-003 and functional-currency judgments to TOPIC-06-004.

## Required inputs
1. Reporting framework, entity, reporting period and reporting tier/entity type where relevant.
2. Functional currency and presentation currency.
3. Bank/investment instrument terms, maturity from acquisition, withdrawal restrictions and overdraft terms.
4. Foreign-currency transaction date, denomination, amount, settlement terms and related asset/liability classification.
5. Spot-rate source and policy for practical average rates, where used.
6. Reporting-date and settlement-date rates where the monetary item remains open or settles.
7. Existing accounting policy/elections and materiality.

## Core accounting model
### Cash classification
- Start with the framework definition of cash and cash equivalents; do not classify an instrument from its account label.
- Assess demand availability, purpose, liquidity, convertibility to a known amount, value risk and maturity from acquisition.
- Restrictions do not automatically remove a demand deposit from cash. Assess whether the restriction changes the nature of the deposit and separately assess balance-sheet classification and disclosure.
- Overdraft inclusion is framework-specific and fact-sensitive; document repayability on demand and whether it is integral to cash management before net presentation or cash-equivalent treatment.
- Reconcile the financial-statement cash population to bank/subledger/GL populations and explain exclusions.

### Foreign-currency transactions
- Determine functional currency before processing foreign-currency accounting. If unresolved or challenged, route to TOPIC-06-004.
- Identify whether the transaction is denominated or requires settlement in a currency other than functional currency.
- Translate initial recognition using the applicable transaction-date rate under the governing framework; a practical average rate is acceptable only when it reasonably approximates actual rates under the applicable guidance and policy.
- Determine whether the resulting asset/liability is monetary or non-monetary. This distinction drives subsequent FX accounting.
- Open monetary items normally require reporting-date remeasurement under the applicable framework. Non-monetary items follow the measurement basis of the underlying asset/liability and the framework's FX rules.
- Separate transaction FX from foreign-operation translation. Translation belongs in TOPIC-06-003.
- On settlement, calculate the difference between the carrying amount translated/remeasured previously and the functional-currency settlement amount, then route the exchange difference to the appropriate income/OCI treatment under the applicable framework.

## CAO decision sequence
1. Lock framework, period, functional currency and presentation currency.
2. For cash questions, obtain instrument/legal terms and determine cash, cash equivalent, other financial asset, restricted presentation, or borrowing/overdraft classification.
3. For FX transactions, identify denomination, transaction date and monetary/non-monetary nature.
4. Validate rate source and date; challenge stale/manual/unapproved rates.
5. Book initial recognition.
6. If open at reporting date, determine whether remeasurement is required and hand detailed period-end mechanics to TOPIC-06-003.
7. If settled, calculate realized FX and reconcile settlement to bank/AP/AR/treasury-accounting records.
8. Evaluate presentation/disclosure and cash-flow consequences.
9. Produce journal support, calculation, reconciliation and policy/judgment memo for material or unusual conclusions.
10. Promote durable functional-currency conclusions, rate-source policy, cash-equivalent policy and overdraft treatment to Company Accounting Memory.

## Documentation standard
A material case should retain instrument/contract terms, functional-currency conclusion or reference, transaction population, rate evidence, monetary/non-monetary classification, calculation, journal entry, reviewer evidence, financial-statement presentation/disclosure conclusion and unresolved exceptions.

## Controls and systems
Minimum controls include approved FX-rate source and interface; rate-date validation; completeness of foreign-currency open items; automated remeasurement configuration review; cash-account master-data governance; cash-equivalent eligibility review; restricted-account flagging; overdraft presentation review; bank/subledger/GL reconciliation; and disclosure tie-out.

Recurring cross-system cash/FX reconciliations involving bank data, ERP subledgers, GL, rate tables and Excel are valid candidates for TrackedFR assessment. A one-off technical classification memo is not.

## Completion criteria
The CAO can classify cash/cash-equivalent populations, identify when restrictions/overdrafts require additional analysis, record a foreign-currency transaction using the correct currency/rate logic, distinguish monetary from non-monetary follow-on accounting, route remeasurement/translation correctly, propose entries, identify controls/disclosures, and retain auditable evidence.