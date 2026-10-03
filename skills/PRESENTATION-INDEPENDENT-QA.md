# Independent QA — EPS, segments, subsequent events, grants and borrowing costs

## Verdict and review anchor

**Supported-scope PASS:** Earnings per Share, Segment Reporting and Subsequent Events, subject to the explicit bounded expert-method contracts below. **NONPRODUCTION / blocked:** Government Grants and Borrowing Costs, due to actual material approved-knowledge gaps. No unresolved production-blocking finding was observed within the three declared executable scopes after remediation. This does not approve all possible transactions, autonomous standard interpretation or specialist calculations outside those scopes.

Reviewed on 2026-10-03 in branch `phase-3/eps-segments-events-grants-borrowing-costs`, based on current commit `17432530ff62bd0e31948d31e7c33c8bfe15b495`. The batch baseline is main `7bb6733`; current working-tree bytes are identified individually below rather than represented as a different already-committed remote tree. The three candidate contracts remain review0.9.0 at this substantive gate. Version/status promotion must be independently verified with regenerated current examples/fingerprints before final production release. Independent QA edited only this report; it did not promote contracts, edit implementation or change knowledge/source ratings.

## Actual approved knowledge and scope

The audit read current AGENTS.md, architecture/skill-specification.md, manifest, capability matrix, immutable batch map, approved claims and actual substantive topic methods. TOPIC-08-007 maps EPS/APM to CAO-08-013/014 (8 claims); TOPIC-08-006 maps related parties/segments to CAO-08-011/012 (8 claims); TOPIC-08-005 maps going concern/events to CAO-08-009/010 (9 claims). All three are actually APPROVED in the manifest and have individual approval records; stale historical PARTIAL headings do not supersede those records. EPS and segment claims remain model-derived/audit-required. Subsequent Events includes the existing SOURCE_VERIFIED IFRS IAS10 claim, without claiming that this reviewer performed a new direct source audit. No ratings or exact references were promoted.

Government Grants has no substantive approved IAS20/AASB120/grant recognition/measurement topic or claims. Borrowing Costs has incidental approved PPE/CIP references to IAS23/AASB123/ASC835-20, but lacks the substantive specific/general borrowing method, commencement/suspension/cessation, investment-income, weighted-expenditure/rate/cap and UK policy model required for an autonomous capitalization engine. Its TOPIC-04-003 six claims are routing evidence, not a production capitalization method. The immutable map therefore preserves31 mapped claims (25 across the three reporting topics plus6 incidental CIP claims),157 canonical topics and347 capability mappings. Both proposed packages reject all four frameworks, even supplied arbitrary specialist approvals and certificates, and produce no journals.

The explicitly reserved workstreams were not researched, resumed, implemented or edited by this QA. No last-batch conclusion was reused as a substitute for this review.

## Independent findings and remediation

Initial authored tests passed while independent counterexamples still certified incorrect outcomes. Those tests were not accepted as the production gate. The following cases were independently challenged and sent to the implementation owner before remediation:

| Finding / counterexample | Remediation and verified outcome |
|---|---|
| July1 splitfactor2 combined with unchanged100-share post-split interval and ordinary zero-change bridge yielded149.589 weighted shares / basic0.668498 instead of200 /0.5 | Every in-period split/bonus must be consumed by the exact legal boundary/kind and issued/treasury factor. Missing/wrong movement blocks; first-day actions need a separate opening adapter. |
| Completed original provision45/revised55 accepted original statement liability0/revised10 | Bounded litigation adapter binds full original45/revised55 liability stocks to the original/revised statement, not just a balanced delta. Other stock owners/multiple aggregated provisions remain unsupported adapters. |
| Imported actual Financial Statements profit200 coexisted with EPS sourceprofit120 and basic1 rather than ordinary180/basic1.8 | Approved typed full-period statement lines bind numerator components to GL, and supplied actual completed FS profit binds numerically. Contradiction blocks. |
| Imported actual FS revenue400/assets500/liabilities200 coexisted with segment consolidated1000/1600/600 | Segment consolidated definitions reconcile through approved numeric bridges to typed actual statement/GL lines and actual completed FS import. Contradiction blocks. |
| Required segments A/B were publicly labelled requiredFalse despite quantitative thresholds | Output distinguishes qualitative flag and computed combined required flag. Independent complete fixture now shows both requiredTrue. |
| Mixed-profit/loss aggregated group could net the reportability denominator (A100/B−90, C8/D−8 gives group basis18 instead of unnetted operating amounts) | Mixed-sign aggregation fails closed to a qualified denominator adapter. Supported same-sign aggregation does not silently extend to this case. |
| Geographic noncurrent assets9999 certified while actual total assets1600 | Included geographic asset population binds to its typed statement/GL metric and cannot exceed actual total assets. Impossible subset blocks. |
| Litigation45→55 disclosed zero effect by selecting unchanged cash as measured account | Adapter controls primary provision account and derives positive liability change10 from owner calculations; estimated adjusting disclosure must agree to10. Other exposure bases require a separate adapter. Zero-offset bypass blocks. |
| Comparative diluted denominator50 accepted below basic100, publishing dilutedEPS2 versus basic1 | Both original/restated diluted denominators must be at least basic denominators in the declared single-class scope. Failure uses ReviewRequired and returns blocked, rather than escaping the execution boundary. |
| Comparative source lacked entity/framework/prior-span binding | Prior start/end must form a valid preceding span and source identity/framework/span must match exactly. Current restatement method remains independently qualified; incompatible prior source blocks. |

The final probes repeated impossible comparative denominators, geographic overstatement, primary-zero-effect bypass, required flags and metadata privacy across all four frameworks. Additional independent positive sequencing used an option20shares/+0, convertible10/+6 and antidilutive10/+20: accepted denominator130 and numerator106, EPS106/130, with the last instrument excluded. Valid provision45→55 produced effect10 and the correct owned liability bridge across all four frameworks.

## Bounded executable contracts

**EPS:** whole issued/treasury share populations, contiguous actual-day weighted intervals, independently evidenced legal movements, split/bonus retrospective weighting, attributable total/continuing/discontinued numerator-to-statement bridges and complete potential-instrument inventory. Instrument-specific weighted shares, after-tax/timing/numerator adjustments are qualified inputs, not an autonomous option/convertible/contingency valuation engine. Sequencing uses continuing-operations control and no cent-rounding; continuing loss excludes dilution, with the same accepted instruments applied to total/discontinued measures. Comparative original basic/diluted inputs are qualified, dimension-bound and retrospectively restated, not reconstructed from absent prior contracts. Rights, multiple/two-class/participating securities, negative incremental numerators, first-day capital actions and additional/IFRS18 per-share measures need separate methods. UK scope must be evidenced specified IAS33 or a reviewed voluntary route, not a universal exemption or obligation. EPS itself creates no journal.

**Segments:** actual CODM/discrete-information/business population, exact-once groups, qualified economics/aggregation and framework-period reportability parameters. Thresholds and asset-test applicability are independently qualified operative inputs, not invented universal elections. Mixed-sign aggregation is explicitly outside the executed denominator method. Numerical/qualitative required segments, external coverage, all-other population, corporate/intersegment and profit-definition bridges reconcile to actual full-period statement/GL sources. Entity-wide geography/products/customers cover external revenue; geographic included noncurrent assets reconcile and major-customer flags require attribution evidence. Scope/adoption, US significant expense/annual-interim/single-segment checklist, comparison changes and disclosure judgments remain qualified reviewer responsibilities. UK does not acquire a universal IFRS8 obligation. This is disclosure governance, not transaction recognition; no journal is posted.

**Subsequent Events:** complete independent board/legal/treasury/commercial/tax/asset/post-close/forecast searches through the actual qualified authorization/issuance window, feed union-to-event inventory, event/discovery/reporting-condition chronology and separate basis/materiality review. The bounded US public/nonpublic cutoff model is explicitly differentiated; special issuance patterns and post-issuance discovery need separate legal/filing methods. Nonadjusting events produce zero year-end measurement movement and material disclosure requires nature and effect or inability-to-estimate evidence. Adjusting integration supports exactly one fresh complete original/revised litigation provision case, unchanged movements/reimbursements, no reimbursement stock, original/revised owned liability and every balanced statement offset. Other adjusting owners, multiple provision aggregates and alternate disclosure-effect bases need their own stock adapters; a completed external result alone cannot authorize them. Going-concern developments require a matched completed assessment; inappropriate basis fails closed. Owner journals are not reposted.

Across scopes, qualified policy/period/entity methods, source IDs/counts/amounts, current-version evidence and independent approvals, numeric GL/statement bridges, complete disclosure reviews and exact knowledge/implementation/case certification are mandatory. Reviewer assertions are supplied evidence, not authentication. Missing/stale/non-independent certification produces partial; unsupported/malformed routes block without new posting. Public output contains generated controlled amounts/classifications and intentionally reviewed segment labels, not raw source/evidence/reviewer/hash objects. All seven routes were tested. No filing, ERP action, legal cap-table change or external communication is authorized.

## Executed final verification

- **422 shared skill unittest methods PASS**, including **87 targeted presentation methods** and the existing98 financing methods.
- **53 repository**, **17 Lease Accounting**, **10 supplemental tax** tests PASS: **502 total executed unittest methods**. Parameterized framework, privacy and CLI subcases are additional, not falsely counted as separate methods.
- Canonical claim/approval validators: no errors; claim warnings empty.157 APPROVED topics/347 mappings/1598 canonical claims preserved. Supplemental tax validator:64 APPROVED claims/four frameworks/no errors, unchanged source track.
- Independently injected internal reviewer/hash/source metadata stayed private across all seven public routes for all three supported packages/four frameworks. Both blocked proposals stayed blocked despite arbitrary resolved inputs/certificates.
- Current worked-example tests exercise unsigned partial outputs and synthetic completed public CLI paths, including nested current owner result validation. Synthetic approval assertions are never represented as real company review.
- Older financing archives remain unchanged historical examples. Shared implementation fingerprint changes intentionally invalidate their archived nested FV certifications; the regression harness refreshes only clearly synthetic nested owner cases in a temporary file. This does not approve real cases or make stale archived certifications current. Fresh production cases must obtain new independent approval.
- Earlier transient test failures during concurrent fixes/example refresh were not accepted as passes. The final422-method frozen run supersedes them. `git diff --check` passes.

No remaining production-blocking finding was observed within these declared supported scopes. Promotion remains conditional on final metadata/example/hash verification and the owner's exact-head CI/integration gate. The two genuine knowledge-gap proposals remain nonproduction. Any material accounting, source-control or privacy change requires renewed independent review.

## Exact SHA-256 reviewed bytes

The report itself is excluded from its own hash register. These exact bytes, not a blanket future approval, define this gate.

| File | SHA-256 |
|---|---|
| `interfaces/public_output.py` | `5df913e00294199abd7583324c0a077f7fcbf720c6cbd6c63a0c5d4e58f58357` |
| `knowledge/topics/TOPIC-04-003-cip-fa-reconciliation-capitalized-software/README.md` | `19eb722e26babf27f098eee41a155ece289a34ee21ec5d336d732a33610d3709` |
| `knowledge/topics/TOPIC-04-003-cip-fa-reconciliation-capitalized-software/applied-qa.md` | `6406d2391d1f73682b809cd2885afcb47bd37bf7f8fd2363195f46da631d41a6` |
| `knowledge/topics/TOPIC-04-003-cip-fa-reconciliation-capitalized-software/knowledge-pack.md` | `99fbeeb4e8f43db98b9678aadf22f15b63abee45fc9735087828a533259a0ad4` |
| `knowledge/topics/TOPIC-04-003-cip-fa-reconciliation-capitalized-software/phase-2d-method.md` | `6f682fed66d8822e18b007bdc5781a42ecaa5a11ec36d32faf2d4058f5215161` |
| `knowledge/topics/TOPIC-04-003-cip-fa-reconciliation-capitalized-software/standards-claims.json` | `378b24254f5d3fe03ae08aa288320966f5264eea5ffaa8774db99024bab4c129` |
| `knowledge/topics/TOPIC-08-005-going-concern-subsequent-events/README.md` | `d9919c05f4645b0f51a0b6baea02aa87ffa59c48bd62836dc009e83753ebfe9b` |
| `knowledge/topics/TOPIC-08-005-going-concern-subsequent-events/differences/framework-differences.md` | `0b63afcc1495f90ba63c178dab4ac8189afbecf2b66328354e3bb61db7915703` |
| `knowledge/topics/TOPIC-08-005-going-concern-subsequent-events/evidence-and-regression.md` | `67fa84640454433e1c3a5ece58146a66d10cb45bb1125d1703328740817f59bf` |
| `knowledge/topics/TOPIC-08-005-going-concern-subsequent-events/financing-event-case.md` | `16b01d17d2847fa371936dfa4f6562f424a5d06909daa2b7e672ad9a390f04a5` |
| `knowledge/topics/TOPIC-08-005-going-concern-subsequent-events/methods/cao-workflow.md` | `fb62a7db2996715ff7375a8d87a52348bb02d0c1ab8bd431a9ce2e85e812e276` |
| `knowledge/topics/TOPIC-08-005-going-concern-subsequent-events/methods/subsequent-event-log.md` | `dff3099a70561f0923a21dd943d09c78edbcba932cc7546d0a3e6d30806599da` |
| `knowledge/topics/TOPIC-08-005-going-concern-subsequent-events/practice/controls-audit-systems.md` | `574431925d75942f78031bb80da899a0a5b61ebc5d17180b70b8a5979e6d64ae` |
| `knowledge/topics/TOPIC-08-005-going-concern-subsequent-events/sources.md` | `2e65bffd7b910878965672f4ecf4cfddd45d9abfc4c45776b1ee2ca0f4bb3f90` |
| `knowledge/topics/TOPIC-08-005-going-concern-subsequent-events/standards/authoritative-subsequent-events-map.md` | `2ffdf64b88dc7665decdfd5595158222caf5e5ce5ab92b455c58731b2a4e67c9` |
| `knowledge/topics/TOPIC-08-005-going-concern-subsequent-events/standards/frameworks.md` | `b98cafd52eb734c98b3b923dd51e1e4e5f5cde75c3feeaa11b9637b103bddc43` |
| `knowledge/topics/TOPIC-08-005-going-concern-subsequent-events/standards-claims.json` | `868384df64644709bc7c523ed070f525f0f4dc202d9ba23e3b82d75068bc295c` |
| `knowledge/topics/TOPIC-08-005-going-concern-subsequent-events/tests/qa.md` | `bcbe758781b5ee5ad98239bd65d7e34013269ae9fd99a333282c305b039c1d62` |
| `knowledge/topics/TOPIC-08-005-going-concern-subsequent-events/tests/scenarios.md` | `75202c817af6d62368c4bd84f6ba4b324ec70734ffcef55876e4dbc3820bdc72` |
| `knowledge/topics/TOPIC-08-006-related-parties-segments/README.md` | `ee962fdc16a4d5a70d2df9c525bfc32a2fb496955faa0c552894d22ba612db8e` |
| `knowledge/topics/TOPIC-08-006-related-parties-segments/evidence-and-regression.md` | `afcaedcc27c27f6a183c468581f6499a55831c6e730fb70404acff6172f9746e` |
| `knowledge/topics/TOPIC-08-006-related-parties-segments/practice-and-tests.md` | `b08fcd622e21a4eda8d33f6f4eed32f00f6f89a2b138a7f4c1266b4d9267bb17` |
| `knowledge/topics/TOPIC-08-006-related-parties-segments/segment-and-relationship-reconciliation.md` | `19775935afb5a8ad7b2ffdfab52131e3d55878f6e1a6d67f252b4f86a4682edb` |
| `knowledge/topics/TOPIC-08-006-related-parties-segments/standards-claims.json` | `c5f7fc359f9e173b556e2bc0c76902347fb091dfb9df74540d96d861d00a71c2` |
| `knowledge/topics/TOPIC-08-007-eps-apm-governance/README.md` | `ab929837a542494379c9ca72db05b05c29cd1d6afaaa35e9c24ae535dd6cfe89` |
| `knowledge/topics/TOPIC-08-007-eps-apm-governance/eps-apm-case.md` | `ff5c46c64f3ea6b7821d8dca7e8da293150bfdae2b521e43c1cf35c9e21a53c0` |
| `knowledge/topics/TOPIC-08-007-eps-apm-governance/evidence-and-regression.md` | `dca4f4526878d5d9e7fd633e7cca89ca49ec0e8fd4d995cf24d2d346f002e4e8` |
| `knowledge/topics/TOPIC-08-007-eps-apm-governance/standards-claims.json` | `978bbe5c35950fd194a0e7cd75d4c70c11667d26c7f683f9625207a9bdecfe92` |
| `knowledge/topics/TOPIC-08-007-eps-apm-governance/weighted-shares-and-publication-gate.md` | `64a455df51511eac1457ceef7b765befb07a664c0cc07c93796808d69cd18384` |
| `skills/PRESENTATION-KNOWLEDGE-MAP.json` | `0a17d2975e47b7429231b88ddd0e48f97b84d635640e94387c675155ddd2a376` |
| `skills/REVIEWER-CONTROLS.md` | `fd4175811374d12396f577f6243d2272b5a4ff7562a659954b1b86a2732f6e13` |
| `skills/borrowing-costs/SKILL.md` | `5bb44e8adb0bd1c69e2aa72ce18818b572d2c531af1945ba72c16c6f66452ecd` |
| `skills/borrowing-costs/examples/AASB.blocked.public.json` | `d12e49451149f579bcee61343769ced9570311ec82a61a350a52cbf757f81c80` |
| `skills/borrowing-costs/examples/AASB.case.json` | `89960f4ee6370e207829509228e48cd64ffe9d93e440414d23e1d46bb86f20e3` |
| `skills/borrowing-costs/examples/IFRS.blocked.public.json` | `9ba42d35eb6f234579caaa6bce4d0996051e62102c4d1ab498791e3e3a0fc845` |
| `skills/borrowing-costs/examples/IFRS.case.json` | `f54db20f0480cc317cacef043cc3b8c6b2c5b877d69cabdf98cdfc7a1885a2f9` |
| `skills/borrowing-costs/examples/UK_GAAP.blocked.public.json` | `409d386ce97cc8cc306731e2053905d8e7cc8faf2ea68328df807112a6e6af84` |
| `skills/borrowing-costs/examples/UK_GAAP.case.json` | `89da24833c5c108470f02e0f1b01894159fc472599a1074a1bcb4110bae7af3b` |
| `skills/borrowing-costs/examples/US_GAAP.blocked.public.json` | `76781824400d56c620397e93ff7a1fd530b5f3266920418214c5b5beee4b7566` |
| `skills/borrowing-costs/examples/US_GAAP.case.json` | `426b8029d8eee8d65c1750c56390892e1373e06ddd3daf5cc3185244d68bb4a8` |
| `skills/borrowing-costs/methods.md` | `ad437298eb98112772c9bb8090dcb4cbe6d01393cbaff3efb865060de0ba96cf` |
| `skills/borrowing-costs/workflow.py` | `a8b2d853eeb0792b1a9c49ecb0f6b74137d119c8f9be23e0406fe7c7dac2ac33` |
| `skills/core_accounting.py` | `c668a8c5b334c0f8cb98da27e14fe764972c28d7f8b0a875600e1e51fd6589ae` |
| `skills/earnings-per-share/SKILL.md` | `37ccbbe0c85e18b1d2c67c7336c68f18e7fc470afc3fca00ee93718af93fef6d` |
| `skills/earnings-per-share/examples/AASB.case.json` | `d8ed508edbfded009f1e3b66e15d1c0a932a8393c4b9b1cdf07009e4cac04203` |
| `skills/earnings-per-share/examples/AASB.complete.public.json` | `ff4a44ea010e63289c9d3eeefaf72671e5c33fac281547270e8f6bf7dc289991` |
| `skills/earnings-per-share/examples/AASB.partial.public.json` | `a280975cfe2e476ad0c8cc5d7eb25d833a264065909ceee23522535bab96b08a` |
| `skills/earnings-per-share/examples/IFRS.case.json` | `3ff8a406b568f8132cf879936a6023cb51761b814238480a259cb72ed5023697` |
| `skills/earnings-per-share/examples/IFRS.complete.public.json` | `25582ae2080b287dab0550ff3aafc592f3e4d3e19725f550f4623fcf7c91645e` |
| `skills/earnings-per-share/examples/IFRS.partial.public.json` | `5e042986dc0468896a2c26c843b8ee751e03e48f015c51b61279305b88c6f062` |
| `skills/earnings-per-share/examples/UK_GAAP.case.json` | `b6ac4d068891a94974e26a42fe9a3415d08e552411f47676ad50a70073bab4d6` |
| `skills/earnings-per-share/examples/UK_GAAP.complete.public.json` | `9266b8f123106032abbedca4e63269af1934f3630ad77c7571009892162180fe` |
| `skills/earnings-per-share/examples/UK_GAAP.partial.public.json` | `4e1b5849a959c208bfb6f4fa429eda4a8529fb8789fff678d0dc90bca7d62ae4` |
| `skills/earnings-per-share/examples/US_GAAP.case.json` | `0935f7944e62af94266c9a4ed4dc9c7b6e28b7bcc5c3ddf83bd66e9a85d4c397` |
| `skills/earnings-per-share/examples/US_GAAP.complete.public.json` | `d4028f0d044453355f3bdf55dd09c848d60ba5ed47b68e1288847746bc03b73b` |
| `skills/earnings-per-share/examples/US_GAAP.partial.public.json` | `95ac03b5a9d24caa0abd14a85eb332727b4c200698c7c4d8b321b75e9f2305bf` |
| `skills/earnings-per-share/methods.md` | `14870104f39184d9726515bb58b5cd68d8403f4f8ac5c2627f1ee466c208be0c` |
| `skills/earnings-per-share/workflow.py` | `aee14736309b00d6891e764993e473bdd9857d17b0b98d49bba2a987fbd621b4` |
| `skills/financing_accounting.py` | `72717ca1da5c60e9b8cf23a522e64cfee81819006e3c616155b56a4abca3979b` |
| `skills/government-grants/SKILL.md` | `8aa8c8ec7b96b26f73ed5ad708fb99526bb966497d48f7d46c632c07d72402f3` |
| `skills/government-grants/examples/AASB.blocked.public.json` | `cae6d116c6fc741701d99ff0406a32d547a41680b234f8ba3ce183c0f35fabcb` |
| `skills/government-grants/examples/AASB.case.json` | `3d8a607f05b7932bd226f874eaaa911bee9d91858db632a3ae7b72c1201bedf0` |
| `skills/government-grants/examples/IFRS.blocked.public.json` | `055491f558980d6f30e74d4d8c2215d278bb9c1472f632f0f4d78c56bf45ba01` |
| `skills/government-grants/examples/IFRS.case.json` | `e29b86a7a36733f9ec63ca2412e478f7302360b0f9c08f9f46990faaa8afbc02` |
| `skills/government-grants/examples/UK_GAAP.blocked.public.json` | `4285b4b58b4a0d970d7ae3ffc60863d17720c997f716fe106a1dd2f167cd02f2` |
| `skills/government-grants/examples/UK_GAAP.case.json` | `0c3ea66aac80e527f1380e71a67ae1c4048c31b213540f20c7005621f954a58c` |
| `skills/government-grants/examples/US_GAAP.blocked.public.json` | `dc76bbc26c28b4bbbea0158c06c6902656821077c37522e72365da3a761de43b` |
| `skills/government-grants/examples/US_GAAP.case.json` | `5345cbd61f89a5118b6da50061ab28eb1556a9d04c64d1577b97abf00d3eaf94` |
| `skills/government-grants/methods.md` | `4a172b5403325576649f4bacb74749d00ff6978ff567d324445052ed11a3d66f` |
| `skills/government-grants/workflow.py` | `7975338f21cc629a432ddca4a7a27afa745109cb818d95c539199c8d2a7e1ebe` |
| `skills/operations_accounting.py` | `61345ea7857e5334dd408fce5e3dc8f028dd2d4ae2f7b5b232523ecc11fd6c6a` |
| `skills/presentation_accounting.py` | `508baacac35660865cac4b34c4c74c39f8545c083236ad3fc1c09983535dd5cb` |
| `skills/production.py` | `d3686447e35978ae3ddb4e1ac1da7b3851ad3755113490b254f69a5abbd963e1` |
| `skills/reporting_accounting.py` | `c5032cc7d09508acf04ea3614b589440f61fffe6a99aad111ce775f40f4559d0` |
| `skills/run_skill.py` | `38a4aaa89fa160b547e20b69eca7622d2344c025914cb90751fca26032e3d3a9` |
| `skills/segment-reporting/SKILL.md` | `0658ae279c3ec441f78938e6c216077923a20818d9d472dbd7ca0e0276b69e95` |
| `skills/segment-reporting/examples/AASB.case.json` | `8fe852cca01e3ce2d6de686617672ab53fecf21c93393c4d93d9205a7f0c2838` |
| `skills/segment-reporting/examples/AASB.complete.public.json` | `29c06a6d9a4b969460ede9f53085349be5858c346c667a7ab687759a7f191d86` |
| `skills/segment-reporting/examples/AASB.partial.public.json` | `251571a855339822e292231237c57e992eee67af790e496eaf3a40af6c1b6aad` |
| `skills/segment-reporting/examples/IFRS.case.json` | `5d2493f4f40ab5ee6feac73d8e741764bbc0c1b0c1e21d7e157bc8e0d9581a2c` |
| `skills/segment-reporting/examples/IFRS.complete.public.json` | `ce7c7c0d385c911b597e70f3b4918047b963b9f5b1b5864b7e212fce761cef3f` |
| `skills/segment-reporting/examples/IFRS.partial.public.json` | `b6e4c595d3a44454d3c373b1477dda3dec15b27bc016dffea5a4c9ea87ca8263` |
| `skills/segment-reporting/examples/UK_GAAP.case.json` | `4ac31675382d589f2a7f0d0f10b1c2c070455e7442bc084db7ae03e8f90567ea` |
| `skills/segment-reporting/examples/UK_GAAP.complete.public.json` | `51e00f6fadbf976d30f8762813384ddcd1430af80d2db72db49996a489571185` |
| `skills/segment-reporting/examples/UK_GAAP.partial.public.json` | `af8739ba2c1b7e40765971b9d467c3170395ad339089c62ec56c3fa8b14c22cb` |
| `skills/segment-reporting/examples/US_GAAP.case.json` | `12bc1d1fd5c9dc86cc4d07d1846587fb0c65a2257e75f26d20a777752f768815` |
| `skills/segment-reporting/examples/US_GAAP.complete.public.json` | `684415971e2b4dcb714b41f1f5541806d37bebb095cad7606923d5339d34f680` |
| `skills/segment-reporting/examples/US_GAAP.partial.public.json` | `fb74d75034fa65ed3ea7cf166f73a27438dd6d44fcdf8e00bd968c5412e18601` |
| `skills/segment-reporting/methods.md` | `77f51bb91a7d6b9633e16b07ce075cee08d27cf7afbeb99fe97ab520dbb6310f` |
| `skills/segment-reporting/workflow.py` | `ef15725e96ad10f8b32d4a8e589d8aa6683b8a996d3b427d7af20b71782bf2fe` |
| `skills/subsequent-events/SKILL.md` | `19bcbb4f0a64d3a75df776eef610cbdb7c2015c1be64aeacca15ed52bf6050d4` |
| `skills/subsequent-events/examples/AASB.adjusting.case.json` | `c9ed5430a23d2c668c1473953a2e8e708d3b47cdef49059ca8a312e975d3e46c` |
| `skills/subsequent-events/examples/AASB.adjusting.complete.public.json` | `80e7137a1c1d929beaa0ec1ac9585626603ac73227c685f85345442105d9d650` |
| `skills/subsequent-events/examples/AASB.adjusting.partial.public.json` | `81e3ecf67d44a0fc0790067a67cd62faa6467cc94d46ad1f64ac3dca2b3ec95d` |
| `skills/subsequent-events/examples/AASB.case.json` | `61995a406bb1095bc8a856c03e2ff18b925ee1dc9a21c8014c679e702fbf01e6` |
| `skills/subsequent-events/examples/AASB.complete.public.json` | `6ac37ff072b64e5bb5fe7e3c3b420056909841ee3a609e17a82e5f3107e0ed7b` |
| `skills/subsequent-events/examples/AASB.partial.public.json` | `0b49cc45af1fadaa7450c085b4fa12f4eb7c503cedb18395a0f3d9eac2574024` |
| `skills/subsequent-events/examples/IFRS.adjusting.case.json` | `2832bc5dc31c6719926eb1c995255cd0402e85d5ea19df694c8cc89d63e281cc` |
| `skills/subsequent-events/examples/IFRS.adjusting.complete.public.json` | `7464eac0650a0600a7bca394d22044d0719ab7ca73fa47d238497228653928e4` |
| `skills/subsequent-events/examples/IFRS.adjusting.partial.public.json` | `385ad629d94e833b129cd3c05089d0237bef658df83967a816c0d9fecfd9bd38` |
| `skills/subsequent-events/examples/IFRS.case.json` | `95c4abee615cdde07a2537bae43f28235fc27c395d0edabc64978a037ea1b9b6` |
| `skills/subsequent-events/examples/IFRS.complete.public.json` | `89e1d327ba17b2dc93ec50bedab3c4a5f02054c27feecd6f2f0159ac6d8c3a02` |
| `skills/subsequent-events/examples/IFRS.partial.public.json` | `5ce6e4310e91e648b81cd7640da6d11af538e79bd5759601ef1895af2b70be66` |
| `skills/subsequent-events/examples/UK_GAAP.adjusting.case.json` | `d885fe3172bd30abf5b3326b861c36bfe3dbd050e012720456aa23cde73b41a9` |
| `skills/subsequent-events/examples/UK_GAAP.adjusting.complete.public.json` | `24b5909134e0cd851fd5537988f9b91f900a4dfff0f3900d20338733737121ff` |
| `skills/subsequent-events/examples/UK_GAAP.adjusting.partial.public.json` | `f794fd375ba91f4283685ad875b771fdf5f9cbe21bd58b50f3b4938bc911ef0d` |
| `skills/subsequent-events/examples/UK_GAAP.case.json` | `dec12af8eb36c0cdb96116b0c91db6d41d20e7c02546fa87ca7f7212286c8f60` |
| `skills/subsequent-events/examples/UK_GAAP.complete.public.json` | `9cc349e1da017b6ceea09d9896f481b267fbe2b3665f9f1fb764567c1e5fd948` |
| `skills/subsequent-events/examples/UK_GAAP.partial.public.json` | `047008c4babdf7e9ffa028fdf7b17cae5735ebe4f7ae1e8cfe9e209fe1f03357` |
| `skills/subsequent-events/examples/US_GAAP.adjusting.case.json` | `4e673b7983b67d49ce59eb01419ade38f927cf82d565f7db49c48c7464237dbe` |
| `skills/subsequent-events/examples/US_GAAP.adjusting.complete.public.json` | `0a5b3e4163ee812d43d99fe53410bc36b2c6030f172242904d95d7289799f09f` |
| `skills/subsequent-events/examples/US_GAAP.adjusting.partial.public.json` | `71f0ec4d80fe10faccc3b586a8a08e4f105a48c5cce81174b6e4b953e865ecd7` |
| `skills/subsequent-events/examples/US_GAAP.case.json` | `7cc375eb88e9bda125ce734a2b0535c0a988e689e37f3b3caed60e08777ad677` |
| `skills/subsequent-events/examples/US_GAAP.complete.public.json` | `219b03db43acb817e8a8c4480abf793560f3fb717f48225be99869f1ae79f7cb` |
| `skills/subsequent-events/examples/US_GAAP.partial.public.json` | `c30c253eed6ea0355cd54f41248c2cc35d049736c11cd398b70139dbbdd209f6` |
| `skills/subsequent-events/methods.md` | `bfa234e56f2ddfc95877e5dcd8bb61ce9de130da2bebe0f9120a665156174da1` |
| `skills/subsequent-events/workflow.py` | `e467a831dc94d0b5b491e7e9f5a0a00341cae0bcc4763a02fc6a5fba5efe25e0` |
| `skills/tests/generate_presentation_examples.py` | `831162f2af5922c1b9ea79edf93df9876229bd36f4b1d0d7591ad5c238f70375` |
| `skills/tests/presentation_cases.py` | `e04a1fee7fa1659a9dca137f2aeaf1c8d8a5e746978613bcb3afafa52fe31510` |
| `skills/tests/test_financing_workflows.py` | `11e9e375bd489e4606ed66a24b2567c64b34e5ae0c2849a830474ab587da3099` |
| `skills/tests/test_presentation_workflows.py` | `efea3e84c82c39f156854bb6d1af2fdf258a62d1e060379372ec04faadcc9864` |
