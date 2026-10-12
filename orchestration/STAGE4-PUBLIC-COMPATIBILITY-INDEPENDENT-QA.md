# Stage 4 inherited public compatibility independent review

**Intermediate independent checkpoint review, not final Stage 4 QA.** Prior review history is preserved. IQA03 remains OPEN. This review independently reproduced two previously unrecorded release compatibility defects; both remain **OPEN and unremediated** at this checkpoint. Neither was introduced by the bounded two-translated-side extension.

## PCIQA01 — blocked native missing-fact reason cannot reach public output

Reproduction:

```sh
python -m unittest discover -s skills/tests -p test_additional_workflows.py -k test_tax_is_blocked_not_false_production -q
```

One existing test errors. `assess_case('income-taxes', {'framework':'IFRS','reviewer_signoff':{'approved':True}})` legitimately returns blocked, no calculations and no evidence. Its conclusion/open items/uncertainties carry `Missing required facts: case_id, reporting_period, entity, jurisdiction`. `to_public` copies that reason into guidance and caveats; the public boundary correctly rejects the internal `case_id` token. Thus a safe refusal cannot be rendered publicly. This is an adapter curation defect: remediation must translate internal missing-fact field names into useful public-language requirements, preserving blocked status, all substantive caveats, and zero fabricated citations. Do not allow arbitrary internal identifiers through the public boundary.

Permanent lifecycle test: `test_missing_native_identity_is_curated_without_losing_blocked_reason`, four frameworks and seven public routes, with blocked reason/caveat preservation and internal-token rejection requirements.

## PCIQA02 — ordinary dependency caveats falsely match internal provenance

Reproduction:

```sh
python -m unittest discover -s skills/tests -p test_agriculture.py -k test_generated_examples_reproduce -q
```

One existing test errors while producing the legitimate blocked Agriculture example. Setting `classification.post_harvest_accounting=True` returns `Accounting case cannot be completed: Unsupported Agriculture dependency: post_harvest_accounting`. `interfaces/public_output.py` treats every `dependency:` occurrence as internal provenance, including this ordinary accounting caveat. Direct `public_record` also rejects natural-language `Outstanding dependency: obtain separately reviewed harvest-cost evidence.`

Remediation must distinguish concrete internal dependency identifiers from ordinary dependency prose, or curate the prose safely at a generic output boundary. Preserve the unsupported accounting condition, blocked result, harvest-accounting caveat and all material limitations. Do not silently drop caveats or broadly disable provenance screening.

Permanent tests: `test_unsupported_agriculture_dependency_remains_publicly_blocked`, seven routes; `test_natural_dependency_caveat_is_not_an_internal_identifier`, seven routes. A fourth test independently requires actual internal dependency/case/version/fingerprint/signoff tokens to remain rejected.

## Inherited checkpoint verification

Compared raw working-tree bytes against `git show e34121bdb68f23db815a580d666b52bc0ef02c98:<path>`. All four relevant files are byte-identical:

| Path | SHA256 |
| --- | --- |
| `interfaces/public_output.py` | `52349538909d90ac2212c213ecee159adeda1f836acf009b5bb75593cf334004` |
| `skills/production.py` | `4b3f89e1659778812f5b34c05b5124d3d8db37d8c60a3039cd139ae51d8a1ce2` |
| `skills/tests/test_additional_workflows.py` | `22449ad2f4ff4ccd43e236a61dfa69e5cd9e9058373b5b15064d1bdd56b668d9` |
| `skills/tests/generate_agriculture_examples.py` | `02c2788246edc03b126efcaa297c2e511f5d9f509ff9283662a242a132632051` |

These public paths do not call the changed Stage 3 two-side orchestration validators. Both defects are inherited release failures from the supplied checkpoint, rather than regression caused by that extension.

## Permanent executable result and outstanding gate

`python -m unittest discover -s orchestration/tests -p test_stage4_public_compatibility_independent.py -q`: **4 distinct tests executed; FAILED with 42 subtest errors** (28 tax-route/framework errors, seven Agriculture-route errors, seven natural-caveat-route errors). Actual internal-token rejection test passes. Subtests do not increase the distinct test total. No expected-failure marker, guard bypass or production edits were used.

Required next steps: generic remediation, rerun these four tests and both original reproductions independently, regenerate any genuinely changed deterministic outputs through governed generators, then include them in the full release regression. Until those steps pass, **two substantive findings remain unresolved** in this intermediate review. This report cannot support final acceptance, roadmap completion or clean CI claims.

## Subsequent generic remediation and independent rerun

The initial reproduction and failed-suite history above are preserved. Both findings are now **RESOLVED within this intermediate compatibility review**:

- PCIQA01: production output adapter narrowly translates deterministic `Missing required facts:` field names into substantive public-language requirements. It curates guidance and both caveat arrays, preserving every requirement, blocked status and empty citations. Arbitrary contaminated reasons and unmapped provenance still fail closed.
- PCIQA02: internal typed identifier prefix screening requires an immediately following non-whitespace identifier suffix. Actual `dependency:secret` and every supported concrete typed identifier remain rejected; ordinary colon-space dependency prose can render. Other provenance names, source notes and hashes remain rejected even after spaces, tabs or newlines.

The reviewer independently inspected both production changes and extended the permanent suite. **Nine distinct permanent methods PASS**. The two original existing reproductions also independently PASS: tax workflow **one distinct test** and Agriculture generator reproduction **one distinct test**. Repeated reruns do not increase these counts. Added attacks cover all eight concrete identifier prefixes across all seven routes; whitespace before internal field names/hash/source prose; arbitrary contaminated reasons; unmapped missing-fact provenance; and exact preservation of all mapped substantive requirements in guidance and both caveat arrays.

No production edits were made by the independent reviewer. This narrows unresolved findings in this compatibility review to **zero**. It does not resolve IQA03 or constitute final independent Stage 4 QA, full release regression, exact-head CI acceptance or permission to advance the roadmap.
