# Inventory & Cost Accounting integration handoff

Skill #24 upgrades the existing SKILL-INV-001 package to 1.0.0/production. Branch: `phase-3/inventory-cost-accounting`. Single PR: https://github.com/DanTrackedFR/chief-accounting-officer/pull/24. No merge is authorized. The final exact head and GitHub Actions run are recorded in the PR because embedding the commit's own SHA in a committed file would be circular.

Live-main reconstruction began at Agriculture merge `20a538f5670123e2e3c01b5bf4cf045bb2eb09bc`; main was rechecked before release. The missing historical goods/WIP/finished-goods Inventory topic was confirmed. Accounting Policy Inventory supplies no goods-inventory authority. The owner-authorized supplemental namespace resolves the existing package's knowledge blocker without changing canonical topics or creating a competing package.

## Supplemental knowledge and evidence

`knowledge/inventory-cost/`, identifier `SUPPLEMENTAL_INVENTORY_COST`, contains 228 independently approved atomic claims. Approval is separate from direct-source verification.

| Framework | Claims | Source verified | Primary corroborated | Model derived / audit required | Direct-source approvals | Training-data approvals |
|---|---:|---:|---:|---:|---:|---:|
| IFRS | 57 | 0 | 5 | 52 | 0 | 57 |
| US GAAP | 57 | 0 | 1 | 56 | 0 | 57 |
| UK GAAP | 57 | 9 | 0 | 48 | 9 | 48 |
| AASB | 57 | 9 | 0 | 48 | 9 | 48 |
| Total | 228 | 18 | 6 | 204 | 18 | 210 |

Individual source provenance, locators where actually inspected, confidence, audit flags, approval tracks, effective periods, entity restrictions and limitations remain in the register. Official authoritative verification was attempted first. Full inaccessible operative IFRS/ASC guidance was not upgraded to SOURCE_VERIFIED. The independent reviewer challenged every claim, recorded each disposition and bound approved content with hashes. A dedicated validator checks namespace, unique IDs, frameworks, sources, evidence/approval fields, periods, limitations, independent review and retrieval privacy. No canonical Inventory mappings were invented.

Supported reporting scope is ordinary commercial annual periods beginning and ending in 2026: full IFRS, ordinary US GAAP, full FRS 102 commercial and AASB Tier 1 for-profit, with current independently supported applicability. Alternative tiers, early adoption and other periods fail closed.

## Supported manufacturing and inventory accounting

| Capability | Delivered behavior |
|---|---|
| BOM/routing | Controlled versions, expected quantities, actual issues, original-layer returns, supported substitutions, routing hours and production identities; no invented standards or inputs |
| RM/WIP/FG | Monetary class bridges, original item quantity/UOM, supplied homogeneous WIP equivalents, completion quantities and FG unit cost; source population, completion and relief exactly once |
| Cost collection | Actual job, batch, production-order and homogeneous process costing with qualified material, direct labour, variable and fixed manufacturing overhead |
| Overhead recovery | Actual reviewed drivers and normal capacity; low-output unallocated fixed expense and high-output allocation ceiling; signed standard under-/over-recovery with explicit cause and disposition |
| Standard/actual | Current supplied standards and approximation review; standard basis, gross variance journals and normal actual-cost adjustments separated from idle/abnormal expense |
| Variances | Material price/usage, labour rate/efficiency, variable spending/efficiency and fixed spending/volume; actual company individual or grouped reporting; separate controlled resale purchase-standard PPV |
| Losses | Actual normal scrap/rework evidence and abnormal material expense; yield evidence must explain production quantities |
| Purchased cost/formula | Controlled landed-cost components, FIFO, moving weighted average, noninterchangeable specific identification and bounded US unit LIFO/LCM |
| Measurement | Current ageing, expiry and supplied demand evidence; framework-specific lower-cost tests; linked FG recovery for RM; write-downs and permitted capped reversals, with US reversals rejected |
| Controllership/reporting | Ownership, transit and third-party custody, counts/shortages, cutoff, balanced proposed journals, relief/COGS, subledger→GL→statements and framework-specific disclosure data |

Unresolved specialist methods remain explicit fail-closed routes: joint/by/co-products; retail technique; dollar-value LIFO pools/indexes/liquidations; separate yield/mix decomposition; manufacturing acquisition-PPV versus consumption-price attribution; heterogeneous stage-equivalent/opening-WIP methods; standalone zero-output factory costing; class transfers; customer/vendor return recovery-owner adapters; positive count adjustments without acquisition/return basis; future-production raw-material recovery without actual linked FG costing; borrowing-cost capitalization; industry/commodity exceptions; unsupported reporting tiers/periods; forecast creation and autonomous standard setting. Internal location transfers are supported with entity-level elimination. No ERP posting, payroll calculation, biological remeasurement or audit opinion is produced.

## Independent QA and remediation

Knowledge author and reviewer, implementation author and reviewer used separate contexts. Knowledge QA: four substantive findings fixed and independently retested—raw-material framework contamination, public scope restrictions, stale approval content hashes and module-import collisions. See `knowledge/inventory-cost/INDEPENDENT-QA.md` for all 228 claim dispositions.

Implementation QA: 12 substantive findings fixed, made executable regressions and independently rerun. These addressed mixed source/GL currencies, contradictory labour rates, duplicate BOM aliases, repeated underlying payroll economics, abnormal material capitalization, unsupported entity scope, disclosure contradictions, malformed chronology, FIFO return-layer ordering, unsupported requested actions and IFRS raw-material recovery. Valid difficult cases demonstrate COMPLETE rather than indiscriminate blocking. See `INDEPENDENT-QA.md` for exact tests, independent numerical results, requirement matrix and promoted-byte hashes.

## Regression and examples

The final promoted-byte release regression passed this complete gate. Exact-head CI is the last integration gate recorded in the PR.

| Suite | Tests |
|---|---:|
| Shared skills, including 109 authored and 86 independent Inventory tests | 943 |
| Lease | 17 |
| Repository | 53 |
| Supplemental Income Tax | 10 |
| Supplemental Agriculture | 83 |
| Supplemental Inventory knowledge: 24 authored + 238 independent | 262 |
| Total, without double counting | 1,368 |

Dedicated supplemental validators, canonical approvals, standards evidence and `git diff --check` pass. Shared coverage includes source-note/public-output privacy, stale knowledge/implementation/certification, malformed populations and owner-boundary regressions. Normal governed generation emits 59 supported scenarios × five artifacts = 295 artifacts, plus eight regenerated historical malformed artifacts: 303 files. Supported outputs include 59 COMPLETE, 59 PARTIAL and 59 adversarial BLOCKED results. Independent read-only re-performance checks all 177 supported public status/JSON goldens. US recovery is explicitly a no-reversal example, not fake IFRS symmetry.

## Cross-skill results and integration controls

Actual current complete Fixed Assets depreciation, Payroll expense, AP acquisition cost, FX historical inventory cost and Agriculture harvest results are independently re-executed and numerically bound to eligible original Inventory targets once. Wrong dimensions, stale results, inappropriate metric paths and duplicate underlying economics block. Agriculture's actual current-period entry remains upstream: opening inventory 0 + retained harvest 70 − Inventory COGS 14 = closing 56; no repeated harvest entry or gain. Post-harvest accounting stays with Inventory. Revenue/COGS, Statements, Disclosure, Systems/Data and Controls interfaces expose reconciled accounting data and owner boundaries. This work does not implement the future end-to-end orchestrator or claim downstream owner certification.

Prepromotion exact-head Actions passed at `3643c67614f70ac4a4df2ddc441e65f4688f4cd9`, run 37192811811. After promotion, normal regeneration, independent promoted-byte rerun and the full 1,368-test release regression passed. GitHub-side normal regeneration also passed 195 Inventory tests; all reviewed financial data, source hashes, certifications and public JSON matched the local approved candidate. JSON object key ordering alone differed in 118 case files, with no substantive differences. The temporary regeneration workflow was removed before the final release commit. Final exact-head Actions must pass before the PR leaves Draft; its exact head and run link are recorded in the PR. Any later file change requires a new exact-head run.

Projected production count after integration is 45, compared with live main's 44. Canonical invariants remain 157/157 APPROVED topics, 347 mappings and 1,598 claims. Income Tax's 64 and Agriculture's 66 claims are unchanged. Inventory's 228 are reported separately. #29 Derivatives & Hedge Accounting and #39 Insurance remain reserved and untouched. Government Grants, Borrowing Costs and Investment Property remain unchanged NONPRODUCTION packages. No merge or other specialist work was performed.
