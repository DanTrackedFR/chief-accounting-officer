# Independent Insurance knowledge QA

Reviewer: insurance_independent_knowledge_reviewer; author: insurance_knowledge_author. Review date: 4 October 2026. These are separate agent contexts. The reviewer did not write the author's propositions or approve their own substantive changes. Implementation QA must use a third independent context.

All 168 material propositions were individually challenged. `independent-review.json` records a decision-specific counterexample and exact reviewed content hash for every claim. Framework counts are IFRS 65, AASB 65, US GAAP 24 and UK GAAP 14. The supported execution boundary is coherent IFRS/AASB current nonparticipating GMM/PAA, separately eligible PAA held and ordinary US short-duration; UK generic measurement remains blocked pending actual existing policy/legal basis. Normative knowledge of a specialist boundary is not certification of its calculation route.

The reviewer independently inspected the official IFRS Foundation overview, both AASB 17 compilations applicable during 2026, the FRC September 2024 FRS 103 operative PDF, and FASB ASUs 2018-12 and 2020-11. Official ASUs are not the operative Codification and the IFRS overview is not complete provision verification. Evidence remains conservative: nine individually source-verified claims (four AASB, five UK), and 159 independently training-data checked claims with open authoritative audits. No operative assurance was inferred from another framework or from publication headlines.

## Findings, author remediation and independent retest

| ID | Defect challenged | Author remediation | Independent retest |
| --- | --- | --- | --- |
| KQ1 | AASB direct claims covered all 2026 but recorded only the July compilation URL | Added actually inspected pre-July source and exact operative start windows | Both URLs/windows and June/July retrieval boundaries checked; altered/missing windows rejected |
| KQ2 | UK edition timing could imply the entire standard began in 2026 | Distinguished 2015 base, 2026 periodic changes and specified 2024 transition | Native UK period assertions checked |
| KQ3 | UK deficiency prose could deduct DAC from the deficiency again | Explicit liabilities less DAC/intangibles comparison | Liability150, DAC30, intangible10, cash flows130 gives deficiency20 |
| KQ4 | PAA bridge did not express acquisition amortisation sign | Added amortisation and deducted cash cost separately | Premium100, cost12, amortisation3, revenue25 produces LRC66; wrong double deduction produces60 |
| KQ5 | Distinct investment component could route insurance-scope DPF to instruments | Retained DPF scope exception and blocked unsupported execution | DPF exception and nondistinct revenue exclusion checked |
| KQ6 | Fixed-fee election referred to unspecified criteria | Named all three conditions and irrevocable contract choice | Cash compensation, individual pricing and cost uncertainty challenged separately |
| KQ7 | Financial guarantee election omitted historical prerequisites | Prior explicit insurance assertion and use of insurance accounting required | Ordinary guarantee cannot elect based only on significant-risk label |
| KQ8 | Reinsurance grouping lacked explicit three adapted buckets | Net gain, no significant possibility and remaining groups/cohorts named | Reinsurance buckets and issued/held separation checked |
| KQ9 | Malformed AASB operative window string raised uncontrolled AttributeError | Validator type-checks source window object | Reviewer mutation test rerun after author fix |

Independent numerical checks additionally cover locked-rate CSM interest, current/remaining coverage-unit release, US deficiency allocation first through DAC, separate gross/held populations, and reviewed reserve/cash differences. Classification challenges address insignificant risk, product labels, warranties, fixed-fee services, financial guarantees and investment components. Population challenges address group locking/cohorts and unique economic identities. Governance mutations cover all 168 modified propositions, missing/duplicate claims, unrelated invalid claims, author self approval, fake source locators, evidence inflation, unsupported period/entity/model, proposed/early presentation adoption and public source-note leakage.

Run `python knowledge/insurance-contracts/test_independent_claim_qa.py`, authored `test_supplement.py` and the dedicated validator. Public privacy verification is limited to the governed retrieval contract; no live application renderer is certified by this knowledge review.
