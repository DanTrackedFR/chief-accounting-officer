# Independent Agriculture implementation QA

Reviewer: independent implementation context, separate from knowledge author, independent knowledge approver and implementation author. Date: 2026-10-04. Tests: `skills/tests/test_independent_agriculture.py`.

The reviewer authored fresh accounting source scenarios with 3.7-scaled monetary populations, two-unit cohorts and 83kg synthetic harvest output. Additional cases independently construct births, zero-salvage deaths and negative measurement gains. Synthetic recertification is fixture preparation only, not authentication of real evidence.

## Findings and remediation

| Finding | Fresh reproduction and original result | Required correction | Executable regression |
|---|---|---|---|
| AGR-IQA-01 | Reclassify a purchase as a birth, remove consideration, adjust cash/gain GL and source register. No independent birth event exists; original returned COMPLETE. | Independent dated birth source must bind physical identity, asset, control, event identity and quantity; reject aliases. | `test_iqa01_birth_*`, valid independent birth case |
| AGR-IQA-02 | Valuation explicitly supplies income-tax/financing/already-adjusted-transport selling-cost components. Original ignored components and returned COMPLETE. | Structured eligible incremental disposal components reconcile exactly, with explicit excluded-cost and double-transport checks. | `test_iqa02_*` |
| AGR-IQA-03 | Qualified requirements tracker and matching source have an empty evidence memo with supported=True. Original returned COMPLETE without actual note support. | Each requirement needs substantive evidence and independent dated, entity/framework-specific support. Quantitative disclosures bind to actual bridges and valuation/category populations. | `test_iqa03_*` and current disclosure population tests |
| AGR-IQA-04 | Put a private reviewer identity into quantity_unit or harvest produce_unit. Original COMPLETE serialized that identity through public calculations on every route. | Curated quantity/produce unit enums and controlled currency syntax; no arbitrary unit text in public schedules. | `test_iqa04_*`, all public-route privacy assertions |
| AGR-IQA-05 | Explicit FRS102 2015 / superseded AASB compilation and corresponding standard_versions in a 2026 case. Original returned COMPLETE. | Governed operative edition with independently sourced entity/framework/period review and matching context declarations. | `test_iqa05_*`, source edition contradiction |
| AGR-IQA-06 | UK individual class source explicitly elects cost while global policy says fair value. Original ignored class election and returned COMPLETE. | Bind actual categories to documented class models and source classification policy; reject conflicting class elections. | `test_iqa06_*`, valid UK bearer-plant FV election |

All six findings were remediated by the implementation author and independently rerun. The final independent suite passes **48 tests**, including valid IFRS/AASB/UK routes and fresh adversarial subcases. No unresolved substantive implementation finding remains. Command: `PYTHONPATH=skills:skills/tests python -m unittest skills/tests/test_independent_agriculture.py -q`.

Independent verdict: PASS for the bounded supported accounting contract below. This verdict covers implementation scope, source controls, fresh arithmetic, explicit exclusions, stale certifications and public output; production promotion still requires root integration, reproduced worked examples, full repository regression and exact final-head CI. The verdict does not certify excluded framework/valuation/owner methods or real evidence authentication.

## Bounded accounting contract reviewed

Supported execution is an individually identified, single-currency, controlled-source 2026 Agriculture workpaper for IFRS, AASB Tier1 for-profit and full FRS102 elected FV less costs to sell. Supports opening/purchased/born surviving units, negative and positive P&L remeasurement, whole-unit harvest boundary and zero-salvage mortality; independent physical and monetary populations tie to GL and disclosure support. Classification-only support does not produce recognition journals.

Excluded scope is genuine and tested: postharvest inventory costing/NRV, agricultural grant accounting, US monetary execution, UK cost model, FV reliability exceptions, actual biological valuation models, sales/recoveries, partial harvest, parent yields, land/PPE/intangibles accounting, multicurrency, general financial statements, entity/tier/operative-period overlays and unbound accounting-owner imports. Named owner dependencies block rather than silently substitute another owner's accounting. IFRS/AASB bearer plants route PPE while bearer animals remain Agriculture; UK class policy does not inherit the IFRS plant carve-out.

## Challenge coverage

Fresh tests challenge inventory/PPE/nonagricultural routes, erroneous preharvest inventory routes, harvest aliases/double counting, closing harvested/dead assets, missing source records, quantity and stock-flow/GL disagreement, purchase-as-opening and birth-as-purchase contamination, current valuation and recognition evidence, dates and source identities, unsupported fair values, wrong gain signs and OCI/equity, UK/US/AASB framework differences, class election and edition contradictions, source support omissions, grant/FV/PPE/inventory/FX owner contradictions, mixed currencies and units, stale source bytes, knowledge selection/document hashes, release fingerprint and case/implementation certification, malformed/nonfinite values, and every public allowlist route. Unsupported price/physical decomposition correctly blocks instead of manufacturing a split.
