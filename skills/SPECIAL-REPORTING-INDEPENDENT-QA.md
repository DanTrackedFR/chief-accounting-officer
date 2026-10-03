# Independent QA — fixed Phase 3 skills 36, 37, 40, 41 and 42

## Verdict and reviewed scope

**Supported-scope PASS after remediation:** #36 Assets Held for Sale & Discontinued Operations, #40 Hyperinflation Accounting, #41 Non-GAAP / Alternative Performance Measures, #42 SEC / Public Company Reporting & Filing Accounting. **#37 Investment Property: NONPRODUCTION / fail-closed across all four frameworks.** No unresolved production-blocking finding remains within the four explicitly bounded executable contracts. This is not approval of complete accounting engines implied by the skill titles.

A separate reviewer context inspected approved canonical knowledge before implementation, executed independent counterexamples, reported substantive defects to the implementation owner, and independently reran the corrected cases. The reviewer authored only this report and independent regression tests; it did not remediate implementation, alter canonical knowledge, promote packages or certify missing authority away. Review date: 2026-10-03. Baseline main: `c813f16fb6abcaf9a2169e1d9be0f34f5a8d0b22`; branch: `phase-3/disposals-property-hyperinflation-apm-sec`. Working-tree bytes are anchored below. Final metadata promotion, examples, complete regression and exact-head CI remain separate integration gates, to be recorded in the batch completion artifact.

## Governed knowledge sufficiency

#36 uses actual TOPIC-13-004 IFRS/AASB classification and discontinued-presentation knowledge: dated classification prerequisites, premeasurement sequencing, independent component qualification, source profit partition, comparable presentation and component cash flows. It produces no held-for-sale measurement, impairment allocation/reversal, disposal gain, OCI recycling or new journals. US/UK detailed routes remain blocked. Legal/book perimeter populations include assets and liabilities; classification does not authorize an unsupported measurement engine. Optional completed impairment imports require a date-matched supported closing-stock adapter; incompatible Fixed Assets/Business Combinations/Consolidation stock imports block.

#37's actual TOPIC-04-001 knowledge only distinguishes investment property as a boundary leaving ordinary PPE. Whole-repository knowledge search found no substantive standalone IAS40/property definition, mixed-use classification, cost/fair-value model, transfers or framework-difference engine. All recognition/measurement routes reject even arbitrary resolved approvals; no calculations or journals are created. No supplemental namespace or new topic was created.

#40 uses TOPIC-13-011's actual economic-assessment and isolated index workpaper, including relevant sibling documents. Monetary/report-date current measurements remain unindexed; dated historical nonmonetary, equity and income/expense amounts use the same approved general-index series/revision. The isolated schedule explicitly is not complete IAS29 statements, net monetary result, tax, comparative statements, translation, consolidation or journals. Actual period-specific economic evidence and qualified review are mandatory; no index or country status is invented. US/UK detailed mechanics and all owner imports without a full hyperinflation adapter block. Existing Foreign Currency/Consolidation boundaries remain intact.

#41 uses the APM portion of shared TOPIC-08-007 without editing EPS. It binds source-backed expense adjustments to actual same-period statement/journal account populations, compares dictionaries/recurrence across periods, reconciles totals and separately reviews tax/NCI, prominence and actual jurisdictional rules. SEC, EU, UK and Australian methods are distinct actual-case qualified application evidence, not interchangeable embedded rulebooks. IFRS18/AASB18 MPM effective scope is separate. It invents no adjustment, underlying GAAP amount or regulatory clearance.

#42 uses TOPIC-16-001–005 for US registrant accounting-control support. Actual domestic/FPI and annual/interim form facts, case/period-specific current-rule evidence, supplied verified calendar, complete source-to-filing population, source-derived XBRL temporal semantics, scale/sign/unit/context checks, issue/query controls and late-change reruns are mandatory. It does not independently determine securities law, submit EDGAR, certify compliance or officer assertions, give an audit opinion or assert regulator-valid XBRL. TOPIC-16-006/007 industry/prudential methods were inspected and excluded as outside this contract.

APPROVED is not SOURCE_VERIFIED. Original evidence_status/reference_confidence/audit_required/approval-track/effective-period limitations remain intact, including training-data-derived open authority audits. Supplied approvals and current-rule-check records are evidence inputs, not authenticated reviewer identities or proof that this software browsed an authoritative rule.

## Exact knowledge mappings

The immutable map includes 9 topics, 19 capabilities and 42 claims; shared-topic capabilities do not broaden executable scope.

| Package | Canonical topic | Capabilities | Exact claim IDs |
|---|---|---|---|
| held-for-sale-discontinued-operations | TOPIC-13-004 | CAO-13-007, CAO-13-008 | `TOPIC-13-004-IFRS-001`, `TOPIC-13-004-US-001`, `TOPIC-13-004-UK-001`, `TOPIC-13-004-AASB-001`, `TOPIC-13-004-IFRS-R001`, `TOPIC-13-004-US_GAAP-R002`, `TOPIC-13-004-UK_GAAP-R003`, `TOPIC-13-004-AASB-R004` |
| investment-property | TOPIC-04-001 | CAO-04-001, CAO-04-002, CAO-04-003 | `TOPIC-04-001-AASB-01`, `TOPIC-04-001-IFRS-01`, `TOPIC-04-001-IFRS-02`, `TOPIC-04-001-IFRS-03`, `TOPIC-04-001-UK-01`, `TOPIC-04-001-US-01`, `TOPIC-04-001-US-02`, `TOPIC-04-001-IFRS-E001` |
| hyperinflation-accounting | TOPIC-13-011 | CAO-13-021 | `TOPIC-13-011-IFRS-001`, `TOPIC-13-011-US-001`, `TOPIC-13-011-UK-001`, `TOPIC-13-011-AASB-001`, `TOPIC-13-011-IFRS-R001`, `TOPIC-13-011-IFRS-R002`, `TOPIC-13-011-US_GAAP-R003`, `TOPIC-13-011-US_GAAP-R004`, `TOPIC-13-011-UK_GAAP-R005`, `TOPIC-13-011-UK_GAAP-R006`, `TOPIC-13-011-AASB-R007`, `TOPIC-13-011-AASB-R008`, `TOPIC-13-011-IFRS-R009` |
| alternative-performance-measures | TOPIC-08-007 | CAO-08-013, CAO-08-014 | `TOPIC-08-007-IFRS-001`, `TOPIC-08-007-US-001`, `TOPIC-08-007-UK-001`, `TOPIC-08-007-AASB-001`, `TOPIC-08-007-IFRS-R001`, `TOPIC-08-007-US_GAAP-R002`, `TOPIC-08-007-UK_GAAP-R003`, `TOPIC-08-007-AASB-R004` |
| sec-filing-accounting | TOPIC-16-001 | CAO-16-001, CAO-16-002, CAO-16-003 | `TOPIC-16-001-OTHER-R001` |
| sec-filing-accounting | TOPIC-16-002 | CAO-16-004, CAO-16-005 | `TOPIC-16-002-OTHER-R001`, `TOPIC-16-002-OTHER-R002` |
| sec-filing-accounting | TOPIC-16-003 | CAO-16-006, CAO-16-007 | `TOPIC-16-003-OTHER-R001` |
| sec-filing-accounting | TOPIC-16-004 | CAO-16-008, CAO-16-009 | `TOPIC-16-004-OTHER-R001` |
| sec-filing-accounting | TOPIC-16-005 | CAO-16-010, CAO-16-011 | No normative claims; approved operational workflow documents only |

## Independent counterexamples and remediation

Every counterexample below initially returned COMPLETE despite its contradictory facts. The independently rerun final cases now reject; they are committed as executable regressions rather than discarded review notes.

| Finding | Verified correction |
|---|---|
| APM expense journal outside actual GAAP subtotal | Exact journal/account membership and amount bind to same-period source ledger. |
| APM prior quarter compared with current full year | Same prior-year calendar span required; alternative fiscal/transition bases need a separate method. |
| SEC profit tag and its caller-owned expected kind both set to instant | Source metric controls duration/instant semantics. |
| HFS prior component profit changed 20→99 with unchanged total100 | Actual component source statement and full prior ledger subset bind the split. |
| Hyperinflation monetary cash dated at acquisition rather than reporting date | Monetary/current stocks require reporting-date measurement. |
| SEC prior comparative changed to a 20-year span | Actual comparative source basis must match prior-year calendar span. |
| HFS component cash flows multiplied tenfold | Actual approved bank source ties exactly to displayed cash flows. |
| HFS current component profit changed30→99 while total remained150 | Actual component/continuing statements partition the full-entity source ledger. |
| APM prior adjustment labels changed while definition keys remained identical | Actual label/definition/recurrence dictionary semantics compare across periods. |
| APM prior recurring share-compensation expense described nonrecurring | Cross-period recurrence semantics must match; unsupported changes block. |
| HFS same component source30 counted twice with a new outer ID | Independent source statements and exact ledger IDs partition current profit exactly once. |
| HFS same bank transaction counted twice with a new outer ID | Unique actual bank IDs reconcile exactly once to independent complete bank population. |
| HFS balance-sheet assets source treated as profit | Profit metric and compatible units required for current/component/prior records. |

A read-review also found that the first component-source helper compared component profit30 to imported full-entity Financial Statements profit150. The corrected full-entity adapter separates component scope. An independently constructed completed Financial Statements owner with actual profit200 now supports HFS component30/continuing170; internally reconciled HFS201 contradicting that owner is rejected. Owner journals are not reposted.

## Executed independent verification

- `test_independent_special_reporting.py`: **16 unittest methods PASS**: thirteen original substantive counterexamples; 92 independent scope/privacy/case-certification assertions; eight mocked stale-knowledge/implementation checks; actual completed-owner positive and contradiction checks.
- Separate authored workflow suite inspected and run: **9 unittest methods PASS** at this review snapshot. These authored tests alone were not accepted as independent QA.
- Supported positive workpapers complete; missing own certification becomes partial. Unsupported measurement/model, country-threshold shortcut, invented APM adjustment, recurring-item misdescription, stale rule, false deadline, wrong filer/form, XBRL scale/sign/unit and incomplete disclosure controls reject.
- All four Investment Property framework routes reject despite arbitrary approval claims. Other unsupported US/UK and legal/filing/certification routes reject without new journals.
- Internal provenance/reviewer/hash injection remained private through all seven public routes: answer_context, answer, retrieval_snippet, citation, tool_output, user_log, export.
- Changed knowledge-document bytes reject; changed implementation bytes invalidate the old case certificate. Mocked reads changed no repository knowledge files.
- Manifest independently counted **157 APPROVED topics** and capability CSV **347 mappings**. Canonical knowledge, evidence records and the 64 supplemental-tax claim register have no diff against baseline, preserving the existing **1,598 canonical claims** and actual evidence/audit values.
- Government Grants/Borrowing Costs and reserved #24/#29/#30/#38/#39 artifacts have no changes from this batch. Existing production implementations are unchanged except the necessary shared registration/fingerprint integration; example certificate refreshes are integration work, not changed accounting scope.

No remaining supported-scope production blocker was observed. Promotion and integration require the owner's complete repository/lease/tax/privacy/adversarial regression, regenerated current examples and exact final-head CI. Any anchored implementation change requires reviewer rerun and refreshed anchors.

## Reviewed SHA-256 bytes

This report excludes itself from its own anchor. The immutable knowledge map separately enumerates every consumed canonical document hash; its anchored bytes bind that register.

| File | SHA-256 |
|---|---|
| `interfaces/public_output.py` | `5df913e00294199abd7583324c0a077f7fcbf720c6cbd6c63a0c5d4e58f58357` |
| `skills/SPECIAL-REPORTING-KNOWLEDGE-MAP.json` | `3a78c5f2438550955db358f07dd27b06920970f7df6ae1961d36ed4c9600b089` |
| `skills/alternative-performance-measures/SKILL.md` | `466a6a3f2fbaeb7097e0c92ea534b2ccbdff68c969c2e086e028b29df5a551f9` |
| `skills/alternative-performance-measures/methods.md` | `588ae0a2cde5a53544c78225c95a1483e1f3533b7b724993143312c342c2a2f6` |
| `skills/alternative-performance-measures/workflow.py` | `661fcea41e7620d6868bb32fccf52dbe7acf205c9fdb292fce1bc21eb95c00b9` |
| `skills/held-for-sale-discontinued-operations/SKILL.md` | `103b807fdb7c0f840fbffe5be6dedb54dbd77b4c2c9cce3f355ff499aa3f53e5` |
| `skills/held-for-sale-discontinued-operations/methods.md` | `d35b24da3b19598d06414b51631433ec0dafd34e023beeeec52f89323da525a7` |
| `skills/held-for-sale-discontinued-operations/workflow.py` | `066bdf6952ca1232e182fbdf8d76d568ba898093164041667cfd75df3db90864` |
| `skills/hyperinflation-accounting/SKILL.md` | `d7bd6d311c90adccf75d161291b795e14cd4b1f92991f941e4b1ea25a45970ba` |
| `skills/hyperinflation-accounting/methods.md` | `cdcb684f5f4eb22b59da4330173029583ac06c5ad21fe2dd00335187d3bb7087` |
| `skills/hyperinflation-accounting/workflow.py` | `c6e2af0514a9d5f01808c6be9388cfa68918cbcbec820b1f79715c680461791e` |
| `skills/investment-property/SKILL.md` | `248435f35e1dcddba45160a9e927ce498153b9ceb91a060f9e83be0a8d12180a` |
| `skills/investment-property/methods.md` | `d0b4ec4b2e239ca62ca9dd8ef950062ee4a1f8a0ee3f756bcde7e0628d5e8643` |
| `skills/investment-property/workflow.py` | `2349c570bac544756ef5b90d9dafc07efb41ccecfe2871ea90d25b641b602f2a` |
| `skills/production.py` | `ddc974097dc67eb5d5b9985bca9aa4b26727c89e707a147644182c438b449940` |
| `skills/sec-filing-accounting/SKILL.md` | `4be0e42e8b721e759b9fe34368dbc8f3c51f436ba15fffa1f986ba3132cb52d3` |
| `skills/sec-filing-accounting/methods.md` | `bcbfa3f8b33a8fc778c06efe61837c1e304b1faef9feeb6f9495bd30a89a0be8` |
| `skills/sec-filing-accounting/workflow.py` | `2b677ab734d74811cbf9d6f58a0c82e6092b55e37025375f9143774de703bfb7` |
| `skills/special_reporting.py` | `0fc6e1c1512c86f26ee057f5426486df94889ab9f93c4d6d98984727c3e7a8af` |
| `skills/tests/special_reporting_cases.py` | `735ed4ca4b4e40211e2cde3a2e0b4518afea67bf1d42b8354ebfa7c854b1713e` |
| `skills/tests/test_independent_special_reporting.py` | `90b0b7ca858d399257409daa0075851efd3420099dd9f7e4d13654f0ed4747f1` |
| `skills/tests/test_special_reporting_workflows.py` | `0ae61dac4fa54d575f614174cd0344e53029048c7eaf8bc995176964a6bd5f6a` |
