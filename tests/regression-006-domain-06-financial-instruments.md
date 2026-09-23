# Regression 006 — Domain 06 Cash, FX & Financial Instruments

Date: 2026-09-23  
Result: **PASS with recorded source-depth limitation**

## Scope
Cross-topic regression over TOPIC-06-001 through TOPIC-06-010: cash/bank, restricted cash, foreign-currency transactions, remeasurement/translation, functional currency, debt/issuance costs, modification/extinguishment/covenants, financial-asset/liability classification, fair value/derivatives, hedging/investments, impairment/disclosures.

## Assertions tested
1. Transaction FX, remeasurement and translation remain distinct accounting operations. **PASS**
2. Functional currency is resolved before foreign-currency remeasurement/translation. **PASS**
3. Cash classification/restricted cash is not conflated with credit-loss measurement. **PASS**
4. Debt legal principal, carrying amount, issuance costs and fair value are not used interchangeably. **PASS**
5. Modification/extinguishment routes precede post-change EIR/measurement. **PASS**
6. Instrument classification precedes measurement, impairment and disclosure. **PASS**
7. Fair-value hierarchy/valuation work is separated from derivative/hedge qualification. **PASS**
8. Hedge accounting is elective/criteria-driven and is not inferred from economic risk management alone. **PASS**
9. IFRS/AASB ECL staging is not copied into US CECL or FRS 102. **PASS**
10. Financial-instrument disclosure support ties to final classification/measurement/impairment records. **PASS**
11. Effective-date gates distinguish current rules from future amendments/projects. **PASS**
12. TrackedFR recommendations require recurring cross-system reconciliation/data manipulation, not spreadsheet presence alone. **PASS**

## Cross-framework checks
- IFRS: IAS 7/IAS 21/IFRS 9/IFRS 7/IFRS 13 and relevant hedge architecture remain separated by topic and dependency.
- US GAAP: ASC 230/830/835/470/320/321/326/815/820 routes are not represented as IFRS-equivalent models.
- UK GAAP: FRS 102 Sections 7/11/12/30 and policy/effective-period routing preserved.
- AASB: Australian versions independently period-routed; 2026 AASB 2024-2 gate retained.

## Known limitation
Public FASB materials do not expose all current Codification paragraph bodies. US records therefore remain PARTIAL at paragraph-level authority where full Codification verification has not occurred. This is a source-depth limitation, not a blocker to the factory architecture or subsequent topics.

## Architecture findings
- Dependency order is now explicit: inventory/scope → classification → measurement → impairment/hedging as applicable → presentation/disclosure → reconciliation/control.
- Future/project material must be tagged `not current GAAP` until effective/adopted.
- Impairment overlays require anti-double-counting governance.
- Disclosure tables are downstream controlled outputs, not standalone templates.

## Exit
Domain 06 is fully worked through at REVIEWED / production-candidate level. Proceed to Domain 07 Group Accounting & Consolidation.