# TrackedFR Phase A integration contract

This is an additive post-merge Profile1.2 correction. Implementation QA is separate from release acceptance and from TrackedFR's original-upload integration acceptance. Profile1.2 remains opt-in (`prepared_unreviewed` + `presumed_user_provided`, both trusted host flags true). Formal/Profile1.1 source assurance, accounting scope, authority and identity remain unchanged.

## Case scope and transport

`entity`, `jurisdiction`, `framework`, `period_start`, `reporting_period`, and `functional_currency` are required nonblank strings and must exactly match the selected durable Case. Country/currency codes and ISO dates must be valid. Framework is IFRS/private US_GAAP/UK_GAAP FRS102/AASB within the existing2026 for-profit boundary; keep applicable edition/tier selectors. `case_id`, `entity_type`, `assumptions`, `source`, and `source_attestation` remain required by the source schema. A source `case_id` is the upstream source binding, distinct from the durable Case reference returned by `start`.

Submit through authenticated `POST /v1/operations`, operation `submit`, with `evidence.facts.machinery` (or `supplier_cost`). Invalid source scope returns HTTP422 `identity_conflict`, aggregates every independent scope defect and safely evaluable row prerequisites, and does not stage evidence. Existing durable Case can reopen, but invalid submissions have no accounting result or proposal. Correct and resubmit before execution; do not change immutable evidence after valid submission.

```json
{"ok":false,"error":{"code":"identity_conflict","message":"Company, entity, period or existing submission identity differs; select the original workspace.","requirements":[{"identifier":"scope.entity.missing","field_path":"evidence.facts.machinery.entity","explanation":"Supply entity matching the selected Case scope (missing).","category":"missing_fact"},{"identifier":"scope.functional_currency.blank","field_path":"evidence.facts.machinery.functional_currency","explanation":"Supply functional currency matching the selected Case scope (blank).","category":"missing_fact"}]}}
```

Malformed HTTP/envelope shape retains HTTP400 `invalid_request` (or other existing transport errors). A valid staged source may execute with HTTP202 and operational job `SUCCEEDED` while accounting is `UNRESOLVED`; inspect governed results, not job success alone. Valid identity with insufficient accounting evidence returns result `validation_requirements`; invalid rows are isolated. Direct engine qualification also produces scope requirements. Requirements always contain `identifier`, `field_path`, `explanation`, `category`; source row paths are1-based (`assets[1].remaining_life_months`). No invalid identity is promoted into supported accounting.

## Useful life and depreciation policy

`remaining_life` ALWAYS means remaining YEARS. `remaining_life_months` means remaining MONTHS. Decimal strings or integers are accepted; binary floats/booleans/non-finite values are rejected. Supply positive life as of the reporting-period start, or availability for a current-period addition. With both fields, exact years×12 must equal months; neither is silently selected on conflict. Row-specific life fields as a group override class life defaults, preventing accidental mixing. `remaining_life_unit`, if supplied, must be `years`; to supply months use the dedicated field. Missing/null/nonnumeric/negative/exhausted/conflicting/unit errors identify the exact field and aggregate with other evaluable defects.

Zero life means the stated useful life has elapsed: assess the remaining depreciable balance or life estimate. An asset fully depreciated but still in use is not automatically disposed of; a zero-life row remains unresolved and creates no depreciation/journal. No historical Case or proposal is rewritten.

```json
{"policy_elections":{"depreciation_convention":"monthly","partial_month_treatment":"actual_days_in_month"},"assets":[{"id":"FA-1","class":"machinery","opening_cost":"24000","opening_accumulated":"6000","remaining_life_months":"24","residual":"0","method":"straight_line","scope":"ordinary_ppe","ready_date":"2025-01-01","expected_depreciation":"750","supplied_net_book_value":"17250","supplied_accumulated_depreciation":"6750","comparison_balance_basis":"closing"}]}
```

The fragment above assumes the selected company/Case period is1–31 May2026 and required source metadata is supplied separately. Result:750.00 depreciation,6,750.00 closing accumulated depreciation,17,250.00 NBV.

Monthly depreciation is recommended for businesses calculating depreciation as part of a monthly close. It provides consistent full-month charges and commonly aligns with fixed-asset registers. Choose actual days if your documented accounting policy uses calendar-day proration. This is operational guidance, not an IFRS/US GAAP/FRS102/AASB mandate.

| Election | Exact basis and treatment |
|---|---|
| `monthly` | Remaining depreciable balance ÷ remaining months for a full eligible calendar month. Eligible months summed before one final cent rounding. |
| `monthly` + `actual_days_in_month` | Partial reporting, mid-month availability/disposal: inclusive eligible days ÷ actual days in that month; sum month fractions, then apply charge. |
| `monthly`, partial month without treatment | Affected row unresolved; requirement at `policy_elections.partial_month_treatment`; no assumed full/half-month rule. |
| `actual_days` | Remaining balance×12÷remaining months×inclusive actual-day year fraction. Each calendar year's denominator365/366. |
| No convention election | Preserve established legacy actual-days behavior; disclose `engine_default_unconfirmed` and request policy confirmation. |

Balance means `max(opening_cost + supported additions − opening_accumulated − residual, 0)`, not original cost divided by original lifetime. Charge is capped at remaining depreciable balance; HALF_UP to cents once per asset/reporting period. No broad mismatch tolerance. Compare `expected_depreciation` using the applied convention. With an unconfirmed basis, explain the legacy basis and ask for confirmation; never infer binding policy from an amount. Round each Case period once; cross-period rounding differences of a cent may arise. Roll opening balances and remaining life forward explicitly each new period; do not reuse unchanged starting remaining life indefinitely. Existing units-of-production method remains separate and does not use year/month life or the straight-line convention.

## Policy precedence and memory boundary

1. Explicitly confirmed, applicable company `asset_policy` governs. Convention fields require `confirmation:"confirmed"`, exact `entity`/`framework`, enclosing `effective_from`/`effective_to`, and nonblank `policy_version`. This is a client-confirmed policy assertion, not independent source certification.
2. A valid explicit Case election governs where no confirmed company policy applies. Identical elections are compatible; conflicting election or unqualified supplied company policy blocks instead of overriding it. A change requires explicit governed resolution, not an implicit election.
3. Applicable established company memory remains governed `CONTEXT_ONLY`. It can suggest the policy for confirmation, but is not automatically promoted to calculation authority. Adapters must explicitly confirm and resubmit it as the qualified company policy above. No automatic binding-memory reuse is claimed. Do not conceal known policy conflicts when making that confirmation.
4. Without a new election or applicable confirmed policy, legacy actual days remains the engine basis. An engine default is never presented as confirmed user policy.

`asset_policy` is reusable by explicitly supplying the same applicable policy/version in subsequent Cases. Native company-memory lifecycle/approval authority is unchanged.

## Balance comparisons

Optional asset fields: `supplied_net_book_value`, `supplied_accumulated_depreciation`, and required-when-comparing `comparison_balance_basis:"opening"|"closing"`. Opening is at `period_start` before current movements/charge; closing is at `reporting_period` after charge and disposal. Disposed closing cost/accumulated/NBV are zero; opening comparisons use the original opening balances. Ambiguous dates require correction, not comparison against an assumed date.

`balance_comparisons` records row/asset reference, source path, supplied/calculated values, supplied-minus-calculated variance, balance basis, `MATCH|MISMATCH|INVALID|UNRESOLVED_BASIS` and explanation. If both balances exist, an additional record checks gross cost−supplied accumulated=supplied NBV. Partial comparison evidence never invents the missing supplied amount. Invalid/ambiguous comparison evidence creates an actionable requirement while preserving independently supported calculations. Mismatches produce warnings and do not change cost, depreciation, balances, disposal or journals. No automatic balancing proposal is created.

## Structured public outputs

Machine-readable accounting integrations must consume these arrays, never parse guidance JSON:

```json
{"proposed_journals":[{"journal_reference":"proposal-example","case_reference":"accounting-case-example","row_reference":"assets:1","asset_or_transaction_reference":"FA-1","lines":[{"side":"Dr","account":"depreciation expense","amount":"750.00"},{"side":"Cr","account":"accumulated depreciation","amount":"750.00"}],"currency":"EUR","period_start":"2026-05-01","reporting_period":"2026-05-31","accounting_determination":"SUPPORTED","qualification_status":"PROPOSED","source_reference":"register-v1"}],"applied_assumptions":[{"row_reference":"assets:1","field":"depreciation_convention","value":"monthly","provenance":"case_election"},{"row_reference":"assets:1","field":"remaining_life_months","value":"24","provenance":"explicit_user_input"}]}
```

References above are illustrative; actual generated references are stable, not client-selected. Hosted `case_reference` is a curated hash of durable Case identity and distinguishes different Cases sharing an upstream source identifier. Direct engine-only results use a curated source-Case reference. `journal_reference` is stable for Case+row+native workpaper index across reads/retries; it is not a posting key or authority. Each nonempty proposal serializes exact native `proposed_journal_workpaper` lines; parallel native row lineage identifies its source row. No presentation-layer journal calculation exists. Empty/invalid/excluded rows cannot leak lines. Per-proposal determination is bounded supported-row qualification; the overall Case may still be unresolved for another row or scope.

Amounts and comparison values are exact numeric DECIMAL STRINGS, consistent with existing calculations; parse with a decimal library. They are not prose and should not be converted through binary floating point. Numeric-string JSON schema patterns and balanced-line public checks enforce the contract. `null` comparison amounts/variance mean not calculated, not zero.

`applied_assumptions` is an allowlisted array of actual used values and row/Case context. Provenance: `explicit_user_input`, `client_asserted_class_assumption`, `case_election`, `confirmed_company_policy_client_asserted`, `engine_default_unconfirmed`, `explicit_field_semantics`, or `governed_method`. Includes convention, remaining-life fields/units/basis, residual, scope/classification, availability, supported thresholds/recognition and framework/period/currency where used. Invalid/excluded row assumptions are not claimed as applied. No default is labeled a confirmed policy. Unresolved assumptions remain requirements rather than falsely applied assumptions.

Public lineage exposes curated source ID and row references. Native private source hash, attestation/identity and review metadata remain private. All seven existing public routes use the same allowlist. Guidance remains available for humans. Native `journal_entry_implications` stays empty under this source profile; it is neither repurposed nor a posting authorization. `proposed_journals` is the authoritative structured proposal contract. There is no automatic posting.

## Migration and TrackedFR retesting

Update the adapter to validate scope before submitting, aggregate and display requirements, pass remaining months through `remaining_life_months`, confirm the actual company convention and explicit partial treatment, identify comparison dates, and consume the three structured arrays. Existing year-based callers require no life conversion. Never convert all historical numeric values indiscriminately.

Inventory previously persisted Cases/proposals where an upstream month column was mapped to `remaining_life`. Compare against original register metadata and independently assess potentially material errors (illustrative12× understatement). Job success does not establish correct units. Preserve original Cases/results; use a separately identified correction Case and governed review of any external posting impact. Do not silently rewrite stored results or assume proposals were posted.

TrackedFR: retest the original Phase A files, including Pulse Restore. The original bundle/register were unavailable here, so synthetic acceptance does not substitute for original-upload acceptance. Repeat all six scope variants and aggregation; zero/negative/missing/null/nonnumeric life; 12/24/36/60 month equivalence; May/February and explicit partial policy; opening/closing supplied NBV/accumulated balance checks including the original~260,000 error; native/public proposal agreement; actual assumption provenance; invalid-row isolation; persisted reopen and idempotent retries. Verify the adapter obtains every accounting amount from structured fields without guidance parsing. Keep original-upload integration acceptance separately owned.

Operational limitations and follow-up issues are in operational-readiness.md. Full source-bound accounting release regression, new receipt, independent artifact/historical/governance verification, exact-head GitHub checks and owner merge/deployment decisions remain separately authorized release work. The historical Profile1.2 receipt does not cover this corrected implementation.

### Reading pre-correction persisted Cases

Historical native workpapers do not contain the new parallel row-lineage metadata.
They remain readable and unchanged; no accounting is rerun during reads. If a
historical workpaper lacks that metadata, `proposed_journals` is empty and
`integration.historical_journal_lineage` explicitly requests a separately
identified correction Case for structured proposals. Existing human guidance
retains the original proposed workpaper information. Do not treat the empty new
array as evidence that the historical workpaper contained no proposal, and do
not infer row references by parsing its prose. Historical conclusions/amounts
remain historical results, not new unit/policy acceptance.
