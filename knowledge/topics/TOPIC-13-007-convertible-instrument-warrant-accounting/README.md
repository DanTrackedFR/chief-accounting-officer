# TOPIC-13-007 — Convertible Instrument Accounting / Warrant Accounting

Status: **REVIEWED / production-candidate**
Primary capabilities: CAO-13-013, CAO-13-014
Sensitivity: H
Source check: 2026-09-24

## Purpose
Enable the CAO to classify, initially measure, subsequently account for and document convertible debt, convertible preferred instruments, warrants and similar own-equity-linked instruments without relying on legal labels.

## Required intake
Executed instrument and side letters; issuer/entity; framework/period; functional currency; issue/settlement dates; principal/proceeds; coupon/maturity; conversion ratio or formula; exercise price and currency; reset/anti-dilution/down-round terms; cash-settlement alternatives; holder/issuer settlement choices; redemption/put/call terms; contingent conversion/exercise terms; number/class of underlying shares; transaction costs; fair values/valuation models; modifications; cap table; approvals and settlement evidence.

## Principles
1. Classification precedes measurement. Identify contractual obligations and every settlement path before calculating components.
2. Analyze from the issuer perspective and distinguish liability, equity, compound instrument and derivative components under the applicable framework.
3. Own-share settlement is not automatically equity. Variable cash, variable share counts, foreign-currency exercise prices, net settlement and contingent features can change classification.
4. Separate freestanding instruments from embedded features using framework-specific rules; do not transplant IAS 32 into US GAAP.
5. Preserve initial classification and reassess/reclassify only when the applicable literature requires or permits it.
6. Modifications, induced conversions, repurchases and exercises are separate accounting events and require chronology.
7. Reconcile legal proceeds and cap-table changes to the accounting allocation and GL.

## IFRS
IAS 32 classifies instruments based on contractual substance and whether the issuer has an obligation to deliver cash/another financial asset. For own-equity derivatives, equity classification generally requires exchange of a fixed amount of cash or another financial asset for a fixed number of the issuer's own equity instruments, subject to specific exceptions. A non-derivative convertible instrument containing both a liability and equity component is separated by the issuer: measure the liability component first at the fair value of comparable debt without the equity conversion feature, then assign the residual to equity. IFRS 9 governs financial-liability/derivative measurement after classification; IFRS 7 governs disclosures.

A warrant that fails equity classification is accounted for as a financial liability/derivative under the applicable measurement guidance. IFRIC's 2021 agenda decision notes IAS 32 has no general reclassification requirement merely because a warrant's exercise price later becomes fixed when contractual terms themselves have not changed. Treat current FICE standard-setting separately from current effective IAS 32.

## AASB
Apply current AASB 132 independently. Current paragraphs 28–32 require issuer separation of a qualifying compound non-derivative instrument; the liability component is measured first and the residual is equity. AASB 132's own-equity derivative definition and fixed-for-fixed architecture align with IAS 32's core model. Apply current AASB 9 for liability/derivative measurement and confirm the Australian compilation/effective period.

## UK GAAP / FRS 102
Current FRS 102 Section 22 requires convertible debt or similar compound instruments containing liability and equity components to allocate proceeds between them: determine the fair value of a similar liability without the conversion/equity feature first, allocate the residual to equity, and allocate transaction costs between components on relative fair values. The initial allocation is not subsequently revised. Apply the current reporting-period version, including the Periodic Review 2024 effective gate for periods beginning on/after 1 January 2026. Warrant and complex-feature conclusions require current Section 11/12/22 routing; do not assume IAS 32 detail applies automatically.

## US GAAP
Apply current Codification independently across debt, convertible instruments, derivatives/hedging and equity topics as applicable. US GAAP classification, embedded-feature separation and own-equity scope/exceptions can differ materially from IAS 32. Public FASB material does not expose every current Codification paragraph body needed for APPROVED paragraph-level mapping, so US case conclusions remain source-depth PARTIAL until checked against a licensed/current Codification source. Never infer US classification from IFRS fixed-for-fixed analysis.

## Framework differences
- IFRS/AASB compound-instrument separation is not a proxy for the US convertible model.
- Own-equity/warrant classification tests and exceptions differ materially across frameworks.
- UK FRS 102 has its own Section 22 compound-instrument model and reporting-period gate.
- Reclassification, modifications, induced conversion, transaction-cost allocation and fair-value remeasurement require framework-specific routing.
- Current standard-setting projects are PIPELINE until effective.

## CAO execution workflow
1. Lock issuer, framework, reporting/transaction date, functional currency and materiality.
2. Build a contractual-terms matrix covering every payment, redemption, conversion/exercise and settlement path.
3. Determine whether the instrument is freestanding or part of another financing and identify all components/features.
4. Apply framework-specific liability/equity classification to the host and own-equity-linked feature.
5. Determine whether compound separation, embedded derivative accounting or freestanding derivative accounting applies.
6. Obtain fair values/market yield and valuation inputs where needed; challenge model consistency with contractual terms.
7. Allocate proceeds and transaction costs under the applicable framework.
8. Build subsequent accounting: EIR/accretion, fair-value remeasurement where required, interest, conversion/exercise/expiry and equity rollforward.
9. For modification, repurchase or induced conversion, establish event chronology and route to specific accounting before posting.
10. Prepare entries, disclosures, EPS dependencies, valuation evidence and classification memo.
11. Reconcile cash/proceeds, debt schedule, derivative balance, equity accounts and cap table to GL.
12. Promote durable classification policies/elections to Company Accounting Memory.

## Calculation architecture
For an IFRS/AASB/qualifying FRS 102 compound instrument: gross proceeds → fair value/PV of comparable liability without equity conversion feature → residual equity component → transaction-cost allocation → liability EIR schedule → conversion/redemption/repurchase bridge. For liability-classified warrants: initial fair value → period-end fair value → P&L movement → settlement/expiry. Every valuation input requires source, date, methodology, reviewer and sensitivity where material.

## Documentation, controls and audit
Minimum package: executed instrument; terms matrix; classification decision tree; framework references; valuation/methodology; comparable debt yield support; proceeds/cost allocation; amortization/fair-value schedule; modification/conversion memo; cap-table reconciliation; JEs; disclosure/EPS handoff; evidence index.

Controls: Legal-to-Accounting intake for new/changed instruments; independent contract review; classification approval; valuation model/input review; cap-table-to-GL reconciliation; derivative fair-value close control; modification trigger; disclosure tie-out; access/version control.

## Systems / automation
Maintain stable instrument/component IDs across legal repository, debt register, valuation model, cap-table platform and GL. Automate repeatable schedules and reconciliations only after classification is approved. TrackedFR is relevant where recurring valuation/debt/cap-table/GL data must be reconciled across systems; not merely because a convertible analysis is prepared in Excel.

## Scenario QA
1. Fixed principal convertible into fixed number of issuer ordinary shares under IFRS/AASB with cash coupon: evaluate compound liability/equity split; do not record all proceeds as debt.
2. Conversion into variable number of shares based on principal/value: fixed-for-fixed fails unless a specific exception applies; route to liability/derivative analysis.
3. Warrant exercise price denominated in foreign currency: do not assume equity; assess applicable exceptions and framework.
4. Warrant exercise price becomes fixed later without contractual amendment: under current IFRS architecture do not invent a general reclassification rule.
5. Convertible includes cash-settlement choice: analyze who controls settlement and each contractual path before classification.
6. US convertible with same economics as IFRS example: run independent Codification analysis; do not reuse IFRS component split.
7. UK FRS 102 compound convertible: liability first, residual equity, transaction costs allocated on relative fair values; preserve period gate.
8. Convertible is modified to induce early conversion: invoke modification/induced-conversion requirements; preserve old/new terms and incremental consideration.
9. Liability-classified warrant: recurring fair-value close process, P&L movement, valuation evidence and GL reconciliation required.
10. Instrument converts/exercises: reconcile legal settlement and cap-table issuance to derecognition/reclassification and GL before case closure.

Expected routing: **10/10 PASS**.

## Completion criteria
Complete when the CAO can extract contractual terms, classify each component under the applicable framework, calculate initial/subsequent accounting, handle conversion/exercise/modification, produce entries/disclosures/evidence, reconcile cap-table/debt/valuation data to GL and clearly distinguish current authority from pipeline standard setting.

## Dependencies
TOPIC-06 financial instruments/fair value/debt; TOPIC-08 EPS/reporting; TOPIC-13-006 debt restructuring/equity financing; TOPIC-14 technical memo; TOPIC-15 judgments; valuation/legal/tax inputs where relevant.

## Source register
Primary/current anchors checked 2026-09-24: IFRS Foundation IAS 32 official standard page and IFRIC warrant agenda material; AASB current AASB 132 compilation including paragraphs 28–32 and application guidance; FRC current FRS 102 Section 22/Periodic Review materials; current FASB Codification required for production US paragraph-level conclusions. Repository content is independently authored summary and references only.