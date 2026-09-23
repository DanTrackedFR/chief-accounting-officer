# TOPIC-07-007 — Group Reporting Package Design / Equity Method Accounting

Status: **REVIEWED / production-candidate**  
Capabilities: CAO-07-013, CAO-07-014  
Sensitivity: H

## Purpose
Design a group reporting package that collects everything required for consolidation and apply equity-method accounting to associates/joint ventures without reducing the process to a percentage-of-profit journal.

## Group reporting package
Required sections should be risk-based but normally include: signed TB and mapping; entity certification; intercompany counterparties/balances/transactions; FX/functional currency; debt/covenants; tax-accounting inputs; leases; PPE/intangibles; provisions/contingencies; revenue/receivables/ECL; payroll/benefits/SBC; related parties; subsequent events/going concern; commitments; legal/regulatory matters; acquisition/disposal/ownership changes; cash-flow data; disclosure data; policy deviations; significant estimates/judgments; local audit findings.

Design rules: one definition per field; explicit unit/currency/sign; entity/period/version keys; hard validation; prior-period comparison; preparer/approver; late-change workflow; no free-text where structured data is needed; retain local-to-group reconciliation.

## Equity method — framework routing
**IFRS.** IAS 28 requires associates to be accounted for using the equity method and IFRS 11 routes joint ventures to the equity method, subject to specified exceptions. Significant influence is participation in financial/operating policy decisions without control or joint control; 20% voting power creates a rebuttable presumption under IAS 28. Initial recognition is at cost, followed by the investor's share of post-acquisition results/OCI and other required adjustments. Consider acquisition-date basis differences, upstream/downstream transactions, losses, impairment and changes/loss of significant influence. IFRS 12 disclosures may apply.

The IASB Equity Method project remains **standard-setting in progress** in September 2026. July 2026 decisions are tentative and do not replace current IAS 28. Never implement exposure-draft/redeliberation proposals as current requirements.

**AASB.** Apply current AASB 128/AASB 11/AASB 12, period-gated. AASB 2024-4 deferred the mandatory date of the 2014 sale/contribution amendments to AASB 10/AASB 128 to annual periods beginning on/after 1 January 2028; earlier application is possible. This is an Australian effective-date difference that must not be inferred from IFRS alone.

**UK GAAP.** FRS 102 Section 14 governs associates and Section 15 joint ventures. Under the 2024 edition, parent investors generally apply equity method to associates in consolidated financial statements, with specified portfolio exceptions; reporting-period gate remains essential. Individual/separate-accounting choices differ from IFRS and must be resolved before calculation.

**US GAAP.** Route equity-method conclusions through ASC 323 and consolidation/control through ASC 810. Do not import IFRS's 20% presumption/application mechanics without US-specific verification. Paragraph-level public-source limitation remains PARTIAL.

## CAO workflow
1. Determine whether control, joint control or significant influence exists before selecting equity method.
2. Obtain investment agreement, cap table/voting rights, board rights, ownership history and financial information.
3. Establish acquisition-date cost and basis differences; document goodwill embedded in investment where framework requires.
4. Obtain aligned investee reporting package; adjust material policy/period differences where required.
5. Calculate share of P&L/OCI/other equity movements, dividends and basis-difference amortization.
6. Identify upstream/downstream transactions and unrealized profits; apply framework-specific elimination.
7. Track cumulative losses and obligations; do not mechanically book losses beyond the permitted/required interest.
8. Perform impairment indicators/testing under applicable framework.
9. Reconcile opening investment + contributions/acquisitions + share results/OCI − distributions ± other changes = closing investment.
10. Tie disclosures and promote durable influence/joint-control conclusions and basis schedules to memory.

## Controls
Investee package certification; ownership-rights review; basis-difference register; policy/calendar alignment; equity-method rollforward; transaction/elimination register; impairment trigger; disclosure checklist; reviewer challenge of significant-influence conclusion.

## Scenario tests
- 22% holding but no participation and dominant shareholder: do not auto-conclude associate; rebuttable presumption requires facts. **PASS**.
- 15% holding plus board seat/material participation: assess significant influence rather than rejecting by percentage. **PASS**.
- July 2026 IASB tentative equity-method decision: flag future/pipeline only. **PASS**.
- Australian sale/contribution transaction before 2028: check operative AASB amendments/early adoption rather than copying IFRS status. **PASS**.

## Sources checked 2026-09-23
IFRS Foundation IAS 28, IFRS 11 and July 2026 Equity Method project updates; FRC FRS 102 September 2024 edition; AASB current standards/version pages and AASB 2024-4; FASB official architecture with existing public-text limitation.

## Completion
CAO can design the package, determine equity-method routing, calculate and reconcile the investment, handle transaction/impairment dependencies and prevent proposed guidance being treated as effective. **REVIEWED / production-candidate.**