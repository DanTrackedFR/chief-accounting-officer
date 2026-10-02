# Independent QA: six operational accounting skills

Independent reviewer: delegated QA agent, 2026-10-02. Read-only accounting implementation review; this report is the only file authored by this reviewer. Review anchor remote commit: `9d1cc006786efa2d85f3e713bd06b5ae90fa7eab`; final frozen working snapshot local HEAD: `d0c8e1b33887db2f3d924de61e89a8636ee40fb0`; exact reviewed bytes are identified below because the working tree may contain later changes.

## Supported-scope gate: PASS

All six packages pass within their explicitly governed ordinary routes, conditional on retaining the reviewed controls and specialist boundaries. This is not an autonomous standards interpretation, authenticated human approval, ERP posting authorization, full company implementation or direct-source assurance opinion. No package or canonical source rating was promoted by this reviewer.

| Package | Independently reviewed supported route | Gate |
|---|---|---|
| month-end-close | Dependency/calendar actual completion, approved posted journal lineage, incremental accrual, lock/reopen controls | PASS |
| balance-sheet-reconciliations | Complete classified BS inventory, independent source rollforward, gross timing exposure, all-account correction offsets | PASS |
| accounts-receivable | Unpaid invoice rights, ordinary credits, dated receipts, opening deposits, funded applications/refunds, ageing and collection ownership | PASS |
| accounts-payable | Ordinary matched invoices, supported unbilled receipts, prior-accrual clearing, segregated confirmed payments | PASS |
| fixed-assets | Cost-model ordinary tangible PPE, excluded costs, commissioning/CIP, straight-line/UOP, prospective estimates, ordinary disposals | PASS |
| intercompany-accounting | Reciprocal monetary balances, separate opening local books, reviewed recharges, deterministic cent allocation, settlement/FX bridges | PASS |

## Verification evidence

Current complete skills suite: **151 test methods PASS**, including **28 operational methods** and four-framework normal/adverse/public routes. Separate lease suite: **17 PASS**. Repository suite: **53 PASS**. Claims and approvals validators both returned zero errors; claim validator also zero warnings. These are execution results, not counts of accounting scenarios or authenticated reviewer approvals.

Independent probes beyond aggregate fixture arithmetic included a four-recipient two-cent recharge (0.01/0.01/0/0, no negative plug), residual450,000 versus carrying420,000 (zero depreciation), fully settled appreciated currency book bridges, future-funded refund rejection and legitimate opening-deposit-funded refund acceptance. Case fixtures are synthetic. Public adapter routes were exercised; raw evidence, reviewer metadata, document hashes and original source notes do not become public workpapers.

## Counterexamples found and resolved

- Post-period approval was initially conflated with reporting cutoff. Separate execution date now permits normal later preparation; actual posting and calendar task completion remain independently bounded.
- Duplicate destination posting and completed/locked-close chronology were initially unchecked. Source/destination uniqueness, approved working calendar, actual task dates and lock-after-task/posting gates now reject inconsistent records.
- Reduced BS inventory and cross-account corrections could omit offset effects. Full classified TB inventory and aggregate all-account deltas now prevent the A+10/B-10 journal from leaving B falsely reconciled.
- IC pre-FX books could disagree with journals; recharge could lack source allocation. Separate evidenced opening books, recharge/settlement bridge and source allocation requirements resolve this.
- Shares0.498+0.498 were rounded to1.00; a last-recipient rounding plug could turn negative. Exact Decimal weight conservation and largest-remainder whole-cent allocation resolve both.
- UOP revision could ignore100 actual units by accepting0 before/after. Before+after units now reconcile to the complete period output. Legitimate residual above carrying gives zero charge; pre-readiness ordinary PPE disposal blocks.
- AR credit January1 against a December31 invoice certified before a right existed. Invoice/opening/credit/cash chronology now blocks this. Newly added deposits initially allowed January1 refund80 funded by December31 residual80 with opening0; every dated customer liability prefix now rejects it. An opening80 deposit legitimately funds that refund.
- Boolean identity/evidence placeholders, unvalidated AP bank memo and payment roles were rejected through typed nonblank identity/evidence controls.
- UK fixture selection initially applied FRS101/105 propositions to FRS102. Selection now preserves the actual FRS102 applicability gate and full reviewed knowledge population.

## Required production boundaries

Supplied company recognition, legal rights, completeness assertions, valuation, local calendars, rates and approvals require substantive independent review. Fingerprints bind recorded approval to exact inputs, code and canonical knowledge; they do not authenticate people or verify external facts. Ordinary AR credits are against outstanding unpaid rights. Credits of paid invoices requiring customer-credit/refund reclassification remain a technical specialist extension; chronological deposit funds cannot be replaced by later receipts. One-to-many journal lineage, unsupported currencies, write-offs, statutory releases, supplier finance, taxes, provisions, complex assets and transaction overlays require documented specialist routes.

Revaluation, held-for-sale, ROU, software, borrowing/restoration costs and sale-and-leaseback are outside the ordinary PPE method. Group elimination/unrealized profits are owned by Consolidation; functional/translation/net-investment complexity by Foreign Currency; arm's-length/tax/legal pricing by an external Transfer Pricing specialist. A resolved flag alone cannot substitute for the reviewed memo. Supplied downstream results must be complete and dimensionally matched.

Framework applicability must resolve actual IFRS/ASC versions, US entity scope, FRS102 edition/adoption/elections and AASB compilation/tier/for-profit scope. Unsupported FRS101/105 and NFP/public overlays fail closed. Operational documents with empty registers remain approved practice; IFRS18-only and auditor-only claims are not generalized company authority. Canonical knowledge/source confidence and the future direct-source assurance queue are unchanged; the separately blocked income-tax package is not made production by this review.

Later method or implementation changes invalidate this exact-byte review and require reassessment. Final metadata promotion to version1.0.0/production and required execution date were reviewed. The added receipt-before-later-credit guard is a conservative explicit specialist boundary, and does not broaden the unpaid-credit method. All24 archived synthetic case/public pairs contain no reviewer_signoff; the public CLI export test executes24 subprocess cases and matches their saved outputs. Their unsigned results remain partial, rather than manufacturing real approval. These final changes preserve the substantive supported-scope PASS.

## Exact reviewed SHA-256 manifest

- `AGENTS.md`: `c0df142ddf21da3fbe72e6693f2d70cace47374769bc9491dbf1f64f1e6dc8ea`
- `architecture/skill-specification.md`: `da33eff1a7839c9e9740c2e941b377df55505155ed733246a5ca5c51affdbfa7`
- `skills/OPERATIONAL-TOPIC-MAP.md`: `f35355c387696f59f7b4fe7dc59755e74d04bf9cfaec7bc09b052e7a029a4d21`
- `skills/REVIEWER-CONTROLS.md`: `c82e4a84ce6ccbda2a77431bbc404502e15e0809f586959d43c0aebaef4fb54a`
- `skills/production.py`: `b797f261b378dee97ce0eba5a9212cb4725ccb34f0d1d01765563ee596e12f8b`
- `skills/operations_accounting.py`: `61345ea7857e5334dd408fce5e3dc8f028dd2d4ae2f7b5b232523ecc11fd6c6a`
- `skills/core_accounting.py`: `c668a8c5b334c0f8cb98da27e14fe764972c28d7f8b0a875600e1e51fd6589ae`
- `skills/advanced_accounting.py`: `7fa7ed7ad9f267ffb78422e52cabec277b1a0e6ce4e3b599d06af609423157ff`
- `skills/month-end-close/SKILL.md`: `2fc09c5d8cb476b08b102fce0c41497588f8e8527bf0bdb3a73fc4e390783495`
- `skills/month-end-close/methods.md`: `d75c30148461245a3336da37477f394f6922019b6ef330617369b3970dba8f5d`
- `skills/month-end-close/workflow.py`: `61dfa0a02e149b6c245fe4ead8b1e3ec33e2349627ec1e734be4e3ccef29423e`
- `skills/balance-sheet-reconciliations/SKILL.md`: `4f885b78531ef9865db5395bae545b901710175de35061db8abae9b91dae676d`
- `skills/balance-sheet-reconciliations/methods.md`: `68c9d8bd0507f6b62c270337d384240d577a4b072fe5db1460ca78052068a55b`
- `skills/balance-sheet-reconciliations/workflow.py`: `470c40e456dbdb8fd668f58d9f9aab95afd0801e35071eacf93d584e0d9a188c`
- `skills/accounts-receivable/SKILL.md`: `eaa583bea27f790331b1a84f6589aa48f4edb513c6556745a0e1eb1aa8ebc5e6`
- `skills/accounts-receivable/methods.md`: `f7fe12e1195e393377b0525428d528bbddbce9f4b0a4d7eb7ed935df3b11d462`
- `skills/accounts-receivable/workflow.py`: `bd748a661cf70a51f38aaf0e6bf1474b9d9e3cff7a8a0449f70b3ae9179a6261`
- `skills/accounts-payable/SKILL.md`: `8e7f8c7abb78839c380955f509d59b9d2ec92c2dd8a993ca0f8b42ecf47b7e28`
- `skills/accounts-payable/methods.md`: `50d2847d07a25b3b33f396f7af8748c65770192cc3625f2e279c4a6cc669aaf2`
- `skills/accounts-payable/workflow.py`: `20b8c69a2659682e15bd64e684e095c140fe2b0736f7ff0611860f989086eac0`
- `skills/fixed-assets/SKILL.md`: `61f38798e9d259e1d79f876cdba72210de9b8d43076ab3cd8ef43c43cc4d1e83`
- `skills/fixed-assets/methods.md`: `3fa50ddcd76ad97b768cbc99d185bb02c0892bce327cfb2a0fec5b762ebe99dc`
- `skills/fixed-assets/workflow.py`: `29aca5c3df369a3302afc0a692c0ceee976b32c0696902d25d450a4dba8cf286`
- `skills/intercompany-accounting/SKILL.md`: `bc9b7c8e68e9da4bed49ae2f3e7be20fa5cc04ee7eb5b53d924f773ebcd657ab`
- `skills/intercompany-accounting/methods.md`: `ce15d8a2ca2da40a532d87fe5446b7a9cbadf0a1fb4606ac19fa4e53c276b89c`
- `skills/intercompany-accounting/workflow.py`: `62074bddb64a6e9582da85de5e39347472c86008de200fe85b9e5b83c5bdcd82`
- `skills/tests/operational_cases.py`: `bd18ecc024593c34d8bdc22121cf969c62613ca03ac26f49a20d99ff46485d4f`
- `skills/tests/test_operational_workflows.py`: `8dbef9575c0a10d54023d616d00e9900a026440f311de08da5017e26f55f3098`
- `skills/tests/test_operational_routes.py`: `9a124825b410a675f7b3fdf30687bf270f4aa4b9bad318f4068682c8b2483766`
- `skills/run_skill.py`: `38a4aaa89fa160b547e20b69eca7622d2344c025914cb90751fca26032e3d3a9`
- `skills/month-end-close/examples/AASB.case.json`: `b82ad9a18c053221fe1e5ca0ed506f4776e44bbd03dd53be473cf4fe3a987bc1`
- `skills/month-end-close/examples/AASB.public.json`: `1b0a8b122ab0d6c3613f0238e61d4f3916bc51f0131b67e01d4f589523469af4`
- `skills/month-end-close/examples/IFRS.case.json`: `15a25205a3b5f8956a1047d85eb5391e864d806285361d1409ef30613743e2f9`
- `skills/month-end-close/examples/IFRS.public.json`: `9be0fca7b6dbee584aef380ef2c64fd355a3a29bfb2d7b0cdab0f4a4d5605840`
- `skills/month-end-close/examples/UK_GAAP.case.json`: `21ae52cb752862f4ea55f6aa68c65192d8b7c07bcae3aaf8271e1feac98a18c5`
- `skills/month-end-close/examples/UK_GAAP.public.json`: `aafbf771e5295288408d088930df03d16c750030257d15f8dc1250ab807041c1`
- `skills/month-end-close/examples/US_GAAP.case.json`: `46e8f3f973640894382741e2049f4950274af9077ab1ce5b9fb95cf6d6469600`
- `skills/month-end-close/examples/US_GAAP.public.json`: `ac32d00b18407c84f682836f01e2636988b1c310648e6f557d1723ae4c534efe`
- `skills/balance-sheet-reconciliations/examples/AASB.case.json`: `78583df20e83cb87627b3d5679510b0d3f7e9b0d1aefeaf050701a985dbd58bf`
- `skills/balance-sheet-reconciliations/examples/AASB.public.json`: `f2c9860f828d0fc84fe403a57b1e6d7e841d7f01a5ac9063f9b8f1a615db3790`
- `skills/balance-sheet-reconciliations/examples/IFRS.case.json`: `3dbb2315b2db87b55924ab753068639499f5dc3da54c88c85e2bf5a37324c6ac`
- `skills/balance-sheet-reconciliations/examples/IFRS.public.json`: `c4b5d3e2bf516d5b95ee9b1ae4db8618ad601bbd6de0d3ac8b32a5633eb1ac0c`
- `skills/balance-sheet-reconciliations/examples/UK_GAAP.case.json`: `0b88178b7324fb4882379ac9861ae6d27989c3e574fe5a46633be8e66c2e87f2`
- `skills/balance-sheet-reconciliations/examples/UK_GAAP.public.json`: `5fb0308306d4aa0d38dcf050935d06d300160ec1655b6c402b84c80da9bfb386`
- `skills/balance-sheet-reconciliations/examples/US_GAAP.case.json`: `e3fb13a788492c381d639756a051891bc4796c3b564f6b208dd1810b407bcef5`
- `skills/balance-sheet-reconciliations/examples/US_GAAP.public.json`: `800e183bff0ff570278d163b9aebb97825409ca145c84f668e415aba052a040c`
- `skills/accounts-receivable/examples/AASB.case.json`: `70af0aeed66e35b73f1e97cbdfe1905d6867c9f19667dfbc5f1adef5bc9768e0`
- `skills/accounts-receivable/examples/AASB.public.json`: `f2d3c4f7f4a66632470db27beab29c7124cf72614e0cd6d439196bc185c73a5c`
- `skills/accounts-receivable/examples/IFRS.case.json`: `a9dd1c31f194f522ba184a868f4c334a9bf7ffb8eed7386bd8721ee6c267e2b2`
- `skills/accounts-receivable/examples/IFRS.public.json`: `82de56fc96b1ec2e6a952215f804c214badcf500ce2ddda9c4f957d99d0d8e2d`
- `skills/accounts-receivable/examples/UK_GAAP.case.json`: `f6839649b053937766497a1dd793b9b97981a3d1b5c50771386336b0fa9e0a6d`
- `skills/accounts-receivable/examples/UK_GAAP.public.json`: `8dffd331ca9662d4cb88679cca14fce1d98b5063b710612210898cd80bd7adc1`
- `skills/accounts-receivable/examples/US_GAAP.case.json`: `937df672fa2f8315f401ef38091296526a34e4f008b5025c6d725ce61e3fd4dd`
- `skills/accounts-receivable/examples/US_GAAP.public.json`: `824200b7a97637324d2ea5de6110084d215d56906a8ea96a9ce0ad70f88225a1`
- `skills/accounts-payable/examples/AASB.case.json`: `a252f9febd346ae2ab934419fa397cbd3c20a7539c70418395968e665c9ca2c4`
- `skills/accounts-payable/examples/AASB.public.json`: `0c533eb72d67119a04bd23b4c5cf1a334dd61346149489a12e321832d1b4dea8`
- `skills/accounts-payable/examples/IFRS.case.json`: `55442348079ae861f7f8411c3a474b9a5392ad073b7bdc4826571519306ea8c5`
- `skills/accounts-payable/examples/IFRS.public.json`: `42774cf321a632d3e0408c7f3d90b2fc737f80dfdebd3353a260f9e93da8b534`
- `skills/accounts-payable/examples/UK_GAAP.case.json`: `d144cc45cf48d148475c811caf0000a3eb29ede91135b4f9f5386181d1460c98`
- `skills/accounts-payable/examples/UK_GAAP.public.json`: `9ecb19f48b5a6fc039abdec11998f8809bdfddadae4a848017dec190164fb232`
- `skills/accounts-payable/examples/US_GAAP.case.json`: `18160f501eb0524ea4c0ff3f6513285379c16ef3c54d88f0dfd5a57f821ef959`
- `skills/accounts-payable/examples/US_GAAP.public.json`: `d6f847f61c6e6ae1877407356ff4e2f1e702490acf7f6ad44c7afaedd5b59fa5`
- `skills/fixed-assets/examples/AASB.case.json`: `6481c10d426075c0a6632833b7a9151c9f547b2e3f0028a9cbfba269cb4b06c1`
- `skills/fixed-assets/examples/AASB.public.json`: `bcad9de1658ab88c51f2840853f8a662c945802a088e2c4388c158a3485a67fb`
- `skills/fixed-assets/examples/IFRS.case.json`: `f7ee6d4eb98468d476d659a5fff49729e5148b7001f7ef9f89319be0f44a16e8`
- `skills/fixed-assets/examples/IFRS.public.json`: `9d71b74de7fde5268fc9196d4ddb71bf2ac0687be597e41055388030161a86ce`
- `skills/fixed-assets/examples/UK_GAAP.case.json`: `4fac29053d7caa535e1e8591b1ffb3aa44c6c688b174f0111bc4146a3f4287bb`
- `skills/fixed-assets/examples/UK_GAAP.public.json`: `029693207801e319ec0ebef15ebe29dad96de75e88727a37857699dd67c638ca`
- `skills/fixed-assets/examples/US_GAAP.case.json`: `1b4a65fb6bdef125b60c79790d9c1ab30e60c0d28e8b7efa33d6147f82e6b399`
- `skills/fixed-assets/examples/US_GAAP.public.json`: `78a9cfd2de20f47f7d36336c24281eed6dbead664c9bbffd4e01abc7d7cc168b`
- `skills/intercompany-accounting/examples/AASB.case.json`: `1a5bcd060415328f1e6500074e66c93928b8e17df68307eba20f634e422820cf`
- `skills/intercompany-accounting/examples/AASB.public.json`: `660e28518fef3b342eadb204d1bfe0e24e6a8d2f6cec8e6ae9dde598e61b37f7`
- `skills/intercompany-accounting/examples/IFRS.case.json`: `b8631245792dd38601357ec53a16e2ce8bbe235d487b91a9e23fb35cb9b1f952`
- `skills/intercompany-accounting/examples/IFRS.public.json`: `7ceebe29a0cff214a2c5f5c5cbbaa6cc8594089b750f2215b923114dc7e63656`
- `skills/intercompany-accounting/examples/UK_GAAP.case.json`: `aa2e1b53b8ad0d452bf06b0f95d9f41a6651c5b8d5f97649f630bbad3d14c0e0`
- `skills/intercompany-accounting/examples/UK_GAAP.public.json`: `cfbff7238f65555d191ba68cc6b2a3a145327a69256fcdac0eced8d48d8d8263`
- `skills/intercompany-accounting/examples/US_GAAP.case.json`: `52b3d09153e783cebe8c8d7f3dee4553ee19306b9b5c7f2bca2e8118ffeee947`
- `skills/intercompany-accounting/examples/US_GAAP.public.json`: `27f5a910262197b897d053d15a0a357c693b3e4ee721dac3180747aa2e413c1e`
