# Independent diagnostic analytics QA

Reviewer is a separate context explicitly delegated for the user's genuinely independent QA requirement. The reviewer inspected the current live architecture and production Analytics contract before candidate implementation, does not implement diagnostic methods/runtime, and owns only this report and independent executable tests.

## Independently derived adversarial matrix

| Area | Attacks and required invariants |
|---|---|
| Bridge integrity | Wrong signed driver, missing driver, dropped residual, forged explained percentage, denominator mismatch; preserve exact starting + signed contributions + visible residual = ending. Reconciliation alone must not assert cause. |
| Attribution | Duplicate economic ID and aliases of identical owner/metric/period/entity source; FX nested in material price and separately attributed; rate/overhead, capacity/variance, write-down/one-off overlap; distinct valid source fractions must remain possible where governed. |
| Comparators | Budget/forecast stale snapshot, wrong version/entity/currency/period, post-period standard, missing comparator population, actual/comparator swapped; no comparator becomes accounting truth. |
| Causation/hypotheses | Association, temporal coincidence and management explanation cannot become established causes; missing evidence cannot support a hypothesis; rejected/unresolved dispositions remain visible publicly. |
| Accounting authority | Diagnostic capitalization, journal, accounting decision, unsupported owner selection, unverifiable result, missing owner execution and omitted question; governed production owner must execute/rechallenge or remain open. |
| Operating vs accounting | Unusual journal alone is not error; operating deterioration alone is not incorrect accounting; one-off amount cannot imply recurring annualised cause. |
| Missing data | Missing quantity/comparator/product segment cannot fabricate volume/variance/full explanation; malformed known family cannot silently disappear. |
| Materiality | No invented thresholds, numeric bool masquerading as materiality, material residual cannot close cleanly, evidenced immaterial residual does not block unrelated owners. |
| Public privacy | Owner routing IDs, reviewer identities, hashes and source notes remain internal across all public routes; limits and hypothesis uncertainty are preserved. |
| Intent | Similar facts with diagnostic/accounting/close/documentation/process objectives select correct work modes; bounded balances do not select broad graph; semantic planner proposal remains subject to runtime governance. |
| Generality | Reusable bridge with a nonmanufacturing expense fixture; no factory-objective dispatch or hardcoded analytical conclusion. |

## Architecture observations before implementation

Existing Analytics 1.0.0 is narrow and expressly excludes budget/forecast; comparator consumption needs an explicit contract/method change without FP&A generation. Existing runtime native owners, exact fingerprint review, combined reporting/journal challenge and public-output allowlist must remain intact. Earlier integration QA demonstrated omission and arbitrary economic-ID relabel bypasses; these are independently targeted again in diagnostic inputs. Analytical identity must bind actual source semantics, not rely solely on caller-chosen economics labels.

Candidate testing and disposition pending implementation/API handoff.

## Candidate review and substantive findings

Independent tests execute `production.assess_case` with actual completed native owners and independently frozen fixture data; adversarial mutations are separately recertified by synthetic fixture controls. This attacks semantics beyond a stale hash gate. No method/runtime or accounting-owner implementation is mocked.

| ID | Finding / reproduction | Remediation / regression |
|---|---|---|
| DIQA-01 | Initial candidate exact-once ledger used only arbitrary frozen economic-component labels. A duplicate owner metric could be relabelled under another economic ID. | Author added semantic owner-metric identity and current/baseline component ties before first executable review. `test_owner_metric_alias_double_count_is_rejected` verifies relabel attack rejected. |
| DIQA-02 | Initial hypothesis class came exclusively from hypothesis assertion; a management explanation could be labelled direct operational evidence. | Author now checks actual source evidence classifications. `test_management_evidence_cannot_be_promoted_by_hypothesis_label` and `test_association_never_supports_operational_cause` verify unresolved/rejected outcome. |
| DIQA-03 | Partition ties checked signs against each other but not actual signed presentation components, allowing reversed capacity/cost contribution under high materiality. | Author bound group/tie signs to current signed owner components and explicitly validates GP owner/sign population. `test_reversed_cost_sign_cannot_be_excused_by_materiality` and `test_owner_component_relabel_cannot_change_margin_basis` pass. |
| DIQA-04 | Requiring every baseline/current component to sum exactly to metric forced zero residual. Independently supplied baseline 15001 versus identified components 15000 was blocked before preserving its valid -1 residual, despite materiality1000. | Author retains frozen baseline and actual owner current integrity while allowing unexplained baseline or omitted owner partition differences to remain explicit residuals. `test_explicit_material_and_immaterial_residual` passes complete with -1 immaterial residual and becomes partial below supplied threshold. Unknown materiality preserves open issue. |
| DIQA-05 | Runtime accepted diagnostics only from COMPLETE Analytics and cleared any PARTIAL diagnostic record. Material residual cases lost valid explanation precisely when needed. | Author preserves native partial diagnostic bridge, caveats and blocked accounting follow-up; challenged invalid analysis still clears. `test_material_residual_keeps_valid_bridge_and_limits_publicly` passes across every public route. |
| DIQA-06 | Comparator ISO timestamps were compared as strings. Impossible `approved_on=2026-00-00` and `frozen_on=2026-11-99` both yielded COMPLETE native output. | Pending author date parsing. Two independently authored malformed-date regressions currently fail. |

Initial independent review passed 19 executable tests after DIQA-01–03 author changes. Expanded review after residual remediation passed 22 tests. Later expanded run reproduced DIQA-06 as two failures; repeated inherited test methods have subsequently been removed from the suite to avoid duplicate counts.

## Additional verified controls

Exact gross-profit and percentage-point bridge including separate denominator effect; prior/current owner amount integrity; incorrect comparator entity/currency/period/version/freeze ordering; budget masquerading as actual; independently supplied forecast supported only as comparator; missing quantity/incomplete populations; duplicate economics; Boolean/NaN/Infinity materiality; unsupported capitalization/journal/treatment fields; wrong accounting-owner amount; no-evidence/association hypotheses; requested intent modes and bounded inquiries; real Inventory accounting recheck; seven-route source/reviewer/hash/routing privacy and retained uncertainty. Monthly flagship now has matching December native owners and November comparator rather than a monthly objective over annual owners.

Final independent disposition pending DIQA-06 remediation and independent rerun on final promoted candidate bytes.

DIQA-06 remediation converts malformed diagnostic dates/fields into governed `ReviewRequired` rather than uncaught native exceptions. Independent rerun against production Analytics **1.1.0**: **30 tests PASS**, 21.957 seconds. This includes additional hypothesis dispositions, observation-only anomalies, prohibited FP&A/automatic-correction requests and omitted capacity preserved as explicit −25,000 residual.

## DIQA-07 — native component-lineage omission bypass

Final review inspected newly added actual Inventory subcomponent allocation. Removing `component_allocation` from material and other-cost sources, changing material current price/amount from 10/120 to 20/240, and reducing other-current from 9024 to 8904 leaves total COGS 11304 unchanged. Native source/release/case re-review still produces COMPLETE and now attributes invented material inflation offset by a fabricated overhead partition reduction. The optional field waives the actual native component validation.

Executable reproduction: `test_omitting_allocation_cannot_enable_false_cost_partition` currently FAIL. Multi-group partitions of an owner metric must retain group-level semantic native component lineage or an explicit independently governed source-population mode; omission must not waive required lineage. Direct single-group metrics may bind the existing full owner component tie. Final independent approval remains pending remediation/rerun.

## Final independent remediation review and rerun

DIQA-07 now requires every group in a multi-group owner partition to retain numeric native component allocation or direct current owner references. References enforce native owner identity and original component-metric uniqueness; altered component amounts cannot be concealed by unchanged aggregate COGS. Rate-based rows with supplied current owner references are separately rechecked as actual numeric assertions. The reviewer inspected these controls and reran the independently authored omission attack successfully.

Final command: `python -m unittest orchestration.tests.test_diagnostic_independent -q`.

Result: **31 tests PASS**, 25.259 seconds, against promoted **SKILL-ANALYTICS-001 version 1.1.0 production**. All seven documented findings have executable passing regression. DIQA-01–03 were independently identified before executable candidate testing and author-remediated early; DIQA-04, DIQA-06 and DIQA-07 had independently failing native reproductions, while DIQA-05 was an inspected runtime loss subsequently verified with material-residual public tests.

The suite independently verifies governed intent primary/secondary/supporting selection, bounded simple balances, complete native GP and percentage-point bridges, alias/duplicate economics, incorrect signs/metric population, current/baseline integrity, actual-versus-comparator isolation, supplied forecast consumption, wrong entity/currency/period/version/freeze, malformed dates, incomplete quantities/populations, controlled thresholds, explicit immaterial/material/unknown residuals and omitted partition, supported/partially supported/rejected/unresolved hypotheses, evidence-class relabel protection, association/observation limits, prohibited journals/capitalization/FP&A, native component omission bypass, actual Inventory recheck and all seven public routes with retained uncertainty.

Independent disposition: **PASS for the bounded intent/diagnostic foundation and matching-period manufacturing scenario**, subject to the integration author's complete repository regression, regenerated artifact verification and immutable exact-head CI. This is not approval of arbitrary semantic natural-language planning, arbitrary ingestion, every owner combination, authenticated real-world source approvals, statistical causation, future FP&A capabilities, persistence or a complete product interface. Current operational decomposition relies on independently reviewed supplied source conventions and owner-bound native cost components; source certification remains supplied case evidence.

Reviewed implementation hashes (internal reproducibility record):

| File | SHA-256 |
|---|---|
| skills/management-accounting-analytics/diagnostics.py | b50823f09533d995943cfaf2db42979eae753ff362d6061b51238ba33ac64507 |
| skills/management-accounting-analytics/SKILL.md | eac726f1e7e50b4b126793ab8a5d521a4416d94c7395a0093a1d21c277ef3daf |
| skills/management-accounting-analytics/methods.md | 9b31cfbaf93552f74058c11654ba123ef2427b087b81b3efbcc3e40393a8b0f1 |
| orchestration/runtime.py | 48f1df3b0bba08edddb9867831ec548bcfe847450ab977ec5bdf15efa21eeb23 |
| orchestration/intent.py | 641aae9e02dad1ef5269a7b48e1a0e73127e80cfcefcac1381430fdc507365e9 |
| orchestration/tests/diagnostic_fixtures.py | 0030f57a0720f14d12abb9c8bcb87b02ea98aecfbd89b0c3ea9e06bb912ec16d |

## Protected-roadmap manifest maintenance review

The full shared-suite run identified a pre-existing stale protected roadmap hash in the Insurance release manifest. The independent reviewer retrieved the original manifest and roadmap from live-main commit `186b302877c1c63e4e5c224d846aefb032a378cf` through local git objects. Live-main/current roadmap SHA-256 was `282ad11dfb1dfd2e2db7b28c5313221fd4bcb4c8902d68b9786a533de7d6e092`; original Insurance manifest instead recorded `d117f21585afb255a3ad2db3cf3528541a6798fa389e900178c28f5c47997927`. The current diagnostic branch had not changed that roadmap at the time of diagnosis. This mismatch predated this workstream.

The owner explicitly requests a narrow roadmap completion edit after final gates. Updating only that roadmap entry to the exact authorized roadmap bytes retains the existing protection rather than removing a check. Independent comparison verified all other manifest contents unchanged, including 1,100 other protected path/hash entries, baseline metadata, canonical counts and supplemental counts. The original Insurance release test remains unchanged and still asserts every protected file's exact current hash.

Added `test_only_authorized_roadmap_protection_label_may_change`: it requires precisely one protected roadmap entry, verifies its hash matches actual roadmap bytes, and verifies a frozen semantic digest of the ENTIRE original manifest with only that single hash replaced by a placeholder. It is CI-portable and does not depend on historical git objects. This prevents unrelated protected hashes or manifest metadata from being silently updated as part of this maintenance.

Independent maintenance rerun: `python -m unittest orchestration.tests.test_diagnostic_independent.IndependentProtectedRoadmapMaintenanceQA skills.tests.test_insurance_release -q` — **5 tests PASS**, 0.056 seconds. No diagnostic implementation or normative knowledge was changed in this maintenance. The independent diagnostic suite now contains 32 tests; its 31 diagnostic tests previously passed against the unchanged reviewed implementation, and this additional manifest-preservation test passes separately. The final authorized roadmap completion edit must update the same single protection entry and pass the unchanged Insurance release and new independent maintenance test, then fresh exact-head CI.
