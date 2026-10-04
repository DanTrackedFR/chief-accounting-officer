# Independent implementation QA — Inventory & Cost Accounting

Reviewer: independent-inventory-implementation-reviewer. Date: 2026-10-04. Separate from knowledge author, knowledge reviewer and implementation author.

**Frozen implementation candidate disposition: PASS.** All 12 substantive implementation findings are remediated and independently rerun. This disposition supersedes every preparatory/interim result. No unresolved substantive defect in the declared supported ordinary commercial 2026 scope. Review candidate metadata is 0.1.0/review; production metadata, complete repository regression and exact-head CI remain separate integration gates. Metadata/fingerprint changes require fresh certification and independent rerun.

## Executed evidence

- 86 independent test methods PASS (`PYTHONPATH=skills:skills/tests:. python -m unittest skills/tests/test_independent_inventory_cost.py -q`,15.024s). Numerous methods contain separate framework, numerical and adversarial subcases; 86 is the executable method count, not an inflated case count.
- 59 generated supported scenarios independently re-performed: 59 COMPLETE + 59 PARTIAL + 59 BLOCKED = 177 executions. All 177 exact curated public JSON goldens matched, zero issues. The 8 legacy generic example artifacts were regenerated to the current runtime rather than retaining obsolete missing-knowledge claims. Normal authoring emits 295 supported artifacts plus 8 historical artifacts = 303 files.
- Actual upstream cases were recertified and re-executed read-only at reviewed runtime bytes before their numeric assertions entered Inventory; no invented package-result scalar was accepted. Synthetic test approvals do not authenticate a real person or authorize ERP posting.
- All seven public routes tested; no source-note, approval metadata, reviewer or fingerprint leakage. Meaningful valid manufacturing cases COMPLETE with independently recomputed numbers; blocking all inputs does not pass.

## Independent requirement matrix

| Area | Valid difficult cases and independent recomputation | Adversarial cases |
|---|---|---|
| BOM, routing, order | Actual usage different from standard; controlled net issue/return; approved substitution; nonzero scrap/rework; batch/job/order; supplied homogeneous WIP equivalents | Duplicated component alias; unsupported substitution; output exceeds available material without yield evidence; duplicate issue/completion; wrong period; omitted scrap/yield; duplicated rework; unsupported routing hours |
| RM/WIP/FG | Independently recomputed class monetary and quantity bridges; partially completed production; multiple lots/locations; elimination of internal transfers | Unexplained closing difference; negative stock; WIP/FG conversion twice; transfer duplicated across locations; incomplete location population; shared WIP used by different orders |
| Labour | Current actual Payroll numerical result bound to consumed source; manufacturing mapping and hours | Duplicate payroll amount; nonfactory labour; unsupported hours; wrong entity/period; stale owner result; arbitrary owner assertion path |
| Overhead | Fixed/variable pools; low-capacity actual absorption; above-normal production cost ceiling; standard under-/over-recovery; nonzero normal difference disposition | Incomplete/duplicated pool; nonmanufacturing expense; invented driver/capacity; idle loss capitalization; overallocated fixed cost; unsupported variable basis; wrong denominator; variance hidden in stock |
| Standards and variance | Independent material price/usage, labour rate/efficiency, variable spending/efficiency, fixed spending/volume computations; traced normal versus abnormal dispositions | Stale quantities/rates; material divergence unreviewed; unsupported revaluation; variance netting; duplicated PPV; reversed usage sign; unexplained yield; mixed labour variance; mislabeled/double-accounted overhead; cost-source mismatch |
| Ownership/cutoff | Owned goods in transit/third-party custody; customer/vendor-held facts; actual receipt/ship/production economic dates | Consigned/third-party stock wrongly included; owned custody omitted; invoice substituted for economic date; future receipt/completion; shipped stock retained |
| Cost formula | Multi-layer FIFO; moving weighted average; specific segregated item | LIFO outside US; ungoverned US LIFO/retail specialist route; switched group policy; specific ID on interchangeable stock; duplicate layer identities |
| Measurement | Fresh explicit completion/selling estimates; reviewed obsolete/expired stock; IFRS-family reversal ceiling; ordinary US no reversal | Stale prices; omitted costs; improper grouping; reserve sign; US/IFRS contamination; duplicated write-down; arbitrary reserve; invented/stale forecast; expiry/discontinuation hidden |
| Owners | Actual Agriculture harvest, Fixed Assets depreciation, Payroll labour, AP costs and FX results consumed once with numeric binding | Stale/duplicate/wrong dimensions; biology remeasurement/duplicate harvest gain; owner recalculation or liability repost; ignored consumed assertion; inappropriate owner fields |
| Reporting | Inventory→GL→statement; relief→COGS; all proposed journals independently balanced; framework disclosure population | Ledger/statement/COGS mismatch; journal imbalance; incomplete disclosure population; duplicated count/cutoff records |
| Governance/privacy | Current knowledge/implementation/release signatures; explicit PARTIAL without reviewer certification; seven public routes | Stale knowledge/implementation/certification; fabricated approvals; source-note leak; malformed quantity/currency; mixed money without qualified conversion; unknown/population omitted fields |

Controls and Systems/Data interaction must expose substantive inventory inputs and outputs while preserving those owners. Statements/Disclosure/Revenue remain owner boundaries, not Inventory authorization to recalculate or certify those domains. Unsupported complex joint/by-product, retail, dollar-value LIFO, heterogeneous equivalent-unit process, specialist industry, alternative tier and borrowing-cost routes must be explicit fail-closed limitations, not fabricated symmetry.

## Findings, remediation and independent disposition

| Finding | Demonstrated defect | Executable regression / PASS remediation |
|---|---|---|
| IQA-01 | USD case accepted EUR manufacturing cost row | `test_source_wrong_currency_or_dimensions`; explicit currency gate now blocks |
| IQA-02 | Labour cost tracker accepted contradictory original source rate | `test_wrong_labour_source_hours_and_rate`; source hours/rate now bind exactly |
| IQA-03 | BOM component aliases silently overwritten by dict | `test_duplicate_bom_component_under_alias`; economic component uniqueness enforced |
| IQA-04 | Inventory GL in EUR accepted with USD quantities/costs | `test_nonfinite_cost_and_mixed_gl_currency`; source/currency control applies to GL |
| IQA-05 | Same actual Payroll source reused via changed case ID and recertification; mathematically reconciled duplicate labour capitalized | `test_same_actual_payroll_source_under_distinct_case_alias`; underlying owner-source digest ignores narrative/certification aliases |
| IQA-06 | Explicit abnormal material loss ignored and capitalized | `test_abnormal_material_loss_cannot_remain_in_inventory` and valid `test_valid_normal_scrap_source_and_abnormal_material_expense`; abnormal loss reduces eligible WIP and is expensed |
| IQA-07 | Unsupported accounting/entity namespace accepted despite approved knowledge scope | `test_framework_entity_namespace_source_restriction`; scope equals governed framework-specific namespace |
| IQA-08 | Disclosure formula/classes/carrying unsupported strings passed mirrored-source test | `test_disclosure_carrying_classes_formula_contradictions`; typed requirements reconcile current policy, classes, amounts, losses and estimates |
| IQA-09 | Boolean movement sequence accepted as integer | `test_opening_layers_duplicate_alias_and_wrong_chronology`; typed chronology gate excludes bool |
| IQA-10 | Old FIFO issue return appended behind newer purchase, blocking correct subsequent relief | `test_iqa10_return_restores_original_fifo_position` and `test_valid_multilayer_issue_returns_exact_original_cost`; controlled original-layer identity restores exact cost/position |
| IQA-11 | Unsupported requested action returned COMPLETE despite contradictory scope | `test_unowned_external_action_not_complete_accounting`; supported accounting/workpaper whitelist excludes ERP posting, audit opinion, forecasts and autonomous standard setting |
| IQA-12 | IFRS raw-material price decline generated write-down despite recoverable finished goods | `test_iqa12_raw_material_decline_not_write_down_when_fg_recoverable`; typed current actual FG context binds component, unit cost and net sale evidence; eight valid framework/context cases plus contradictory/stale/source/method tests PASS |

Additional reviewer challenges independently passed: owner metric restrictions, full current item ageing/expiry/demand assessment, unique valuation population, prior write-down/original-cost binding, framework-specific disclosures, real opening and retained upstream GL movements, component/group standard-reporting architecture with nonnetted favorable/adverse exposures, PPV attribution boundary, mixed-layer original returns, quantity/equivalent-unit labels, unit costs and class bridges.

## Independently computed production evidence

- Scaled actual RM/WIP/FG: RM 548; WIP 274; FG 822; inventory 1,644; COGS 274. Material 822, labour 274, variable OH 137, fixed pool 274, fixed absorption 137 and idle expense 137.
- Standards: separate material price 82.2, labour rate 27.4, variable spending 13.7, fixed volume 137; an additional case proves labour efficiency 24.66 distinct from rate 27.4, and variable efficiency 24.66. A usage case independently proves material usage 123.3 and actual material 822.
- Signed standard over-recovery −137 does not create inventory profit; actual eligible inventory remains 1,644. Above-normal actual production recovers only the real fixed pool, yielding inventory 1,753.6 and zero idle loss.
- FIFO old-layer return chronology: opening 100 units at10; issue70; new10 units at20; return10 original cheap units; subsequent40 units must cost 400. Independent closing RM200/WIP280/FG840, inventory1,320, COGS280.
- Mixed-layer issue: explicit return of original cheap10 units costs100, inventory1,660; expensive10 costs200, inventory1,680. Neither an unsupported blended cost nor a guessed layer is accepted.
- Ordinary write-down: inventory246.6 and charge95.9. IFRS/UK/AASB supported recovery is68.5 within original cost; US retains zero reversal. US simple latest-layer LIFO/LCM independently yields205.5; complex LIFO pooling remains excluded.

## Real owner consumption and downstream interface validation

| Owner | Actual independently executed assertion | Inventory result |
|---|---|---|
| Fixed Assets | `depreciation`90,000 from real current FA case | Inventory37,534.4 |
| Payroll | `expense`10,800 from real current payroll case | Inventory10,064.8 |
| AP | `invoices`120 from real current AP case | Inventory1,630.4 |
| FX | Historical nonmonetary actual transaction initial basis110 USD, selected by transaction ID | Inventory178.5 |
| Agriculture | Actual `harvest_entry`70; owner journal retained once | Real period opening0 + retained70 − own COGS14 = inventory56; only Inventory sale journal generated |

All owners are re-executed by the existing shared import gate and numeric source paths tie to the consumed source. Stale results, wrong dimensions, duplicate underlying economics, wrong metrics, wrong qualification and amount mismatches block. This specialist review validates exact downstream handoff interfaces to Statements, Revenue/COGS, Disclosure, Systems and Controls; it does not claim full orchestrator execution or control/audit certification. Full source populations and typed inventory disclosure data accompany the exact values. The framework statement bridge and every own journal account reconcile to actual period opening/closing GL and statements. Agriculture retained entries are separately mapped to the actual owner journal instead of being added to period opening or reposted.

## Raw-material framework challenge and supported boundaries

Eight valid raw-context scenarios independently reperform at rescaled amounts. IFRS/AASB recoverable finished goods preserve raw cost and total inventory 1,644; actual nonrecoverable FG evidence with appropriate replacement-cost measurement gives inventory 1,534.4 and charge 109.6. US/UK supplied reviewed formula-specific LCNRV cases give 1,534.4/109.6 and reject an automatic IAS2 recovery exemption. The controlled source states the actual finished-good cost basis and reviewed net sales estimate; missing/currentness/identity/cost/method contradictions block. No selling price or forecast is invented.

Supported manufacture includes actual and standard costs, controlled individual or grouped company variance accounts, net BOM issues/returns with exact original layers, job/batch/order and homogeneous process equivalents, actual normal-capacity fixed and usage-based variable overhead, under-/over-recovery, normal scrap/rework evidence and explicit abnormal material expense, RM/WIP/FG cost and quantity bridges, cost/formula relief, current ownership/count/cutoff, ageing/NRV/measurement/reversal and reconciled own/retained-owner journals. The mandatory challenge families above are exercised by the named methods and subcases; exact source originals are deliberately refreshed only when testing a coherent independently reviewed synthetic population, so semantic challenges cannot pass merely because a stale hash blocks.

Precise exclusions remain: complex joint/by-product/retail methods; dollar-value LIFO pools/indexes/liquidations; mixed manufacturing purchase-PPV versus consumed-material-price attribution without a company-specific method; unsupported separate mix/yield decomposition or standard revaluation; heterogeneous equivalent-unit/opening-WIP methods; unowned borrowing-cost capitalization; industry-specific measurement; alternative reporting tiers/early adoption; autonomous forecasts and MES/ERP operation. Raw-context measurement requires the actual linked FG evidence or fails closed. Downstream Statements/Disclosure/Systems/Controls are interface validations, not a claim to have built or executed the future orchestrator. No audit/control effectiveness opinion or filing/posting action is produced.

## Reviewed byte hashes

These SHA256 values identify the frozen review-candidate bytes. Production metadata changes invalidate its certification fingerprint and require root regeneration/review/CI; this table must be updated by an independently rerun promoted-byte review before final handoff.

| File | SHA256 |
|---|---|
| `skills/inventory-cost/workflow.py` | `c3243578d695f0717ba7c94e74c3f8d6aa84debe04b6f887119741f007d523a5` |
| `skills/inventory-cost/SKILL.md` | `2cfb01639c17990ae88c45e5f40f9dd0cf949baa6d397fb964f77d305c2391a9` |
| `skills/inventory-cost/methods.md` | `5337e0f29eeeab4a01afaa5d28f9e6e069932f7d3e86b6811c269aff8b58ccff` |
| `skills/inventory-cost/INVENTORY-KNOWLEDGE-MAP.json` | `4634732f06874dbae829271db12ef41c4398c241f1da7adfeb9c1fd863c5fdbb` |
| `skills/production.py` | `86bc9eb5de6516cad8b3dbffc7237ff24ce7ecb606a4ce67cbbecc55642eb19e` |
| `skills/REVIEWER-CONTROLS.md` | `df3ce9eb492a861eee17ea88a30afa7b85cf4b1e933655cc6c783dfb6e2b3b22` |
| `interfaces/public_output.py` | `5df913e00294199abd7583324c0a077f7fcbf720c6cbd6c63a0c5d4e58f58357` |
| `knowledge/inventory-cost/standards-claims.json` | `7fd80072d75c276013b2ea8e0074684d1f4ef952006df48528383fdfb1ed9e23` |
| `skills/tests/test_independent_inventory_cost.py` | `515e17306ea00aca6c471fe5129c3448c53289a1a97017a1727b93189d65c90a` |

Canonical/TAX/Agriculture knowledge and #29/#39 are outside reviewer write ownership. Reviewer changed only this report and the independent Inventory test file. No merge performed.
