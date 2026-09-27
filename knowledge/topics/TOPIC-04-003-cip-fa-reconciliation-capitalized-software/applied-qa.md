# TOPIC-04-003 — CIP and fixed-asset bridge test

This adds numeric reperformance to the existing knowledge pack; software recognition remains primarily in 04-004. Capabilities CAO-04-007–009. Authoritative routes: [IAS 16](https://www.ifrs.org/issued-standards/list-of-standards/ias-16-property-plant-and-equipment/), [IAS 38](https://www.ifrs.org/issued-standards/list-of-standards/ias-38-intangible-assets/), [AASB standards](https://standards.aasb.gov.au/) 116/138, [FRC FRS 102](https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/uk-accounting-standards/frs-102/) Sections 17/18 and [FASB ASC](https://asc.fasb.org/) 360/350-40. Verify period-specific editions and the US ASU 2025-06 adoption gate in 04-004; public access does not confirm every current US paragraph.

## Dual rollforward workpaper

Project P has opening CIP 200,000, supported qualifying vendor invoices 120,000, eligible project payroll 80,000 and an accepted in-service portion of 300,000. Closing CIP = 200,000 + 120,000 + 80,000 − 300,000 = 100,000. Journal: Dr CIP 200,000 / Cr AP/payroll 200,000 for current-period costs; Dr PPE 300,000 / Cr CIP 300,000 upon readiness. No depreciation on the remaining 100,000 while it cannot yet operate; the 300,000 asset depreciates from its actual available date. Payroll allocation needs employee, activity, time, rate and approval, not simply a percentage of budget.

Separately reconcile the FA subledger to GL by entity and asset class: gross cost opening + additions + CIP transfers − disposals ± FX/reclassifications = closing gross cost; accumulated depreciation opening + charge − depreciation removed on disposal ± other supported movements = closing accumulated depreciation. Do not let a net-book-value match conceal offsetting errors in gross cost and accumulated depreciation. Link each CIP transfer to one or more asset IDs and retain a one-to-many allocation schedule. Outstanding 100,000 has project-owner confirmation, expected ready date and impairment/abandonment assessment.

## Exceptions exercised

- ERP code is supplier-hosted with no customer-controlled software: route the spend to 04-004's cloud service/prepayment decision rather than forcing the 200,000 through PPE.
- Project commissioned mid-month but ERP record still says CIP: correct the transfer and test depreciation cut-off; a delayed administrative closure is not a deferral election.
- Aged inactive project: obtain continued-viability evidence and refer to 04-006; do not roll forward capitalization indefinitely.
- Subledger and GL totals agree while class totals differ: fail reconciliation, trace asset mapping and post supported corrections. The closing 100,000 project balance is not evidence that all original costs qualified.

Reviewer signs project cost population, exclusions, commissioning record, asset-ID bridge, class-level GL reconciliation and note tie-out. Arithmetic passes; unresolved documentation or unexplained class difference fails acceptance.
