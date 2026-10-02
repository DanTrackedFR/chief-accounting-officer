# Foreign currency — economic judgment and two numerical layers

Read TOPIC-06-002/003/004 and TOPIC-07-006 canonical methods and registers. Establish functional currency from price-setting and cost primary indicators, with financing/retention support and alternative conclusions. Currency of incorporation, invoicing, debt or parent's reporting choice is not decisive. Distinguish ledger, functional and presentation currencies.

| Layer | Input/rates | Outcome |
| --- | --- | --- |
| Initial transaction | Foreign amount × transaction-date functional-per-foreign quote | Functional recognition amount |
| Monetary settlement/remeasurement | Settlement-date cash + remaining foreign × closing quote | Transaction gain/loss in P&L |
| Historical nonmonetary | Historical recognition amount retained | No closing-rate retranslation |
| FV nonmonetary | Supported FV × valuation-date rate | Follow underlying reviewed P&L/OCI origin |
| Foreign operation | Functional TB first; assets/liabilities closing, income dated/appropriate average, equity historical | Separately derived OCI/CTA and NCI allocation |

IAS21, ASC830, Section30 and AASB121 are independently selected in knowledge/applicability review. Ordinary non-hyperinflationary exchangeable operations only. If ledger differs from functional, run a full remeasurement method first; do not translate incorrect ledgers. Hyperinflation/high inflation, lack of exchangeability, hedges/net investments and functional-currency change require separate specialist assessment, including 2025 exchangeability and 2027 presentation-currency amendment period scope. IFRS18 FX P&L classification requires the period-specific reporting method.

## Inputs and bridges

Transaction items have unique IDs, initial amounts/dates/rates, evidenced opening books, settlement amounts/dates/rates, closing rates, classification and account. Quote is functional units per foreign unit. The initial opening_route reconciles in-period recognition to the original transaction rate; carried_monetary reconciles prior-period foreign balances to the approved opening closing rate, not the original historical rate. This slice starts with a reviewed transaction recognition/opening balance; it generates settlement and subsequent adjustment journals, not duplicate initial recognition. Monetary balance bridge: closing + settled cash - opening book gives asset gain or liability loss. Historical nonmonetary disposal is not a currency-only settlement.

Translation uses an identified foreign operation, the common reporting presentation currency, a separate presentation-per-functional quote and a balanced functional TB. A/L must use closing rate; profit rate must match supported average approximation. Full local net-asset bridge includes opening, profit, OCI and dated capital flows. Translation movement = translated closing net assets - translated opening - translated profit - translated other OCI - translated flows. Opening CTA + current movement must independently equal the translated historical-equity TB imbalance (the accumulated closing reserve). Allocate current movement to owners/NCI using reviewed rights. Opening CTA is a separately certified group reserve, not inserted into local functional equity. Continuing operations use reporting-date valuation_date; full disposals use disposal-date TB/rate, not a later year-end rate.

Full disposal requires a reviewed qualifying-disposal trigger and owners/NCI cumulative CTA bridge. Owner reserve recycles to disposal result; NCI reserve derecognizes with NCI, not parent P&L. Partial/retained-control disposals and framework exceptions are separately routed.

## Worked examples and review

Foreign receivable100 at1.10, settlement40 at1.15, remaining60 at1.20 => initial110, cash46, closing72, totalFXgain8. Historical asset100 at1.10 remains110, not120. FVnonmonetary150 at valuation-date1.18 =>177, with origin determined by its underlying accounting method.

Foreign operation opening netUSD100 ×0.90=90, profitUSD20 ×0.85=17, closingUSD120 ×0.80=96 => CTA movement -11. With no opening CTA, functional TB cash120/equity-100/profit-20 translates96/-90/-17, agreeing to closing CTA -11; owners80% movement -8.8/NCI -2.2. With opening CTA +10 and historical equity translated at0.80, closing accumulated CTA is -1 (10-11), matching96-80-17; comparing -1 to movement -11 would incorrectly reject valid carried reserves. A dividend10 at0.82 changes the bridge; a CTA plug concealing the missing dividend fails.

Retain functional-currency factor memo, approved quote/rate feed, transaction ledger, settlement bank evidence, net-assets/TB/equity-rate layers, volatility challenge, ownership/disposal evidence and reserve/GL/note tie. No raw internal source notes or reviewer metadata pass through to_public.
