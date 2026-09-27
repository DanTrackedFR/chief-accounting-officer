# Technical documentation quality and evidence traceability — applied factory

Canonical capability map: CAO-14-020 technical documentation quality review checks logic, arithmetic, effective date and reviewer sign-off; CAO-14-021 accounting citation and evidence traceability binds every material claim to an accessible versioned authority and source record. The ECL trace test below exercises both capabilities.

Retains original README. CAO-14-020/021. Source check 2026-09-27. Proposed REVIEWED candidate for quality method.

## Claim-to-source and amount-to-ledger graphs

Review every material **claim** for exact source, source type/authority, framework, paragraph if verified, applicable version/period, effective/transition condition and fact linkage. Review every material **number** for entity, source export/report parameters, transformation, calculation, ledger statement and disclosure location. A valid URL to a standard is not evidence that a particular paragraph supports the claim; sample the actual content where authorized. [IFRS IAS 8](https://www.ifrs.org/issued-standards/list-of-standards/ias-8-basis-of-preparation-of-financial-statements/), [FASB Codification](https://asc.fasb.org/), [FRC FRS 102](https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/uk-accounting-standards/frs-102/) and [AASB portal](https://standards.aasb.gov.au/) are primary publisher entrypoints, but the review must select exact period/version. Record public FASB paragraph-body limitations as PARTIAL. Do not copy official standards text or imply secondary guidance is binding.

## Review procedure and exception severity

Create a trace matrix with record ID, claim, source ID, paragraph verification status, fact evidence ID, calculation ID, reviewer, exception and final disposition. Test scope/effective date before detailed wording. Reperform one high-risk calculation, then inspect consistency among memo, journal, workpaper, financial statement note, management narrative and system mapping. Check contradictory evidence, alternative, preparer/reviewer segregation and versioning. Severity: blocking (wrong framework/period, missing critical contract, unsupported measurement, unreproducible figure), review-required (plausible but unverified paragraph, incomplete sensitivity), editorial (label or cross-link). A document can be excellent prose yet fail approval on blocking evidence.

## Worked lineage

An ECL paper concludes closing allowance 215k. Source aging has 4m×1% +1m×5% +0.5m×20%=190k; supported forward overlay 25k yields 215k. GL currently contains 170k, so required adjustment 45k. The review verifies 5.5m aged population to AR ledger, each rate's evidence, no duplicate overlay, model formula, approved journal Dr ECL 45k/Cr allowance 45k, note gross 5.5m/net 5.285m, and prior-period comparison. If ledger gross is 5.7m, arithmetic checks alone do not cure 0.2m missing population: block. A generic “IFRS 9” link without relevant scope/method paragraph verification is source review-incomplete, not false authority.

## Executed challenge tests

S1: correct source URL but wrong effective period → FAIL. S2: reputable professional-firm interpretation presented as primary authority → FAIL hierarchy. S3: 190+25=215, 215−170=45 and 5,500−215=5,285 (thousands) → arithmetic PASS conditional on source population. S4: exact ASC paragraph claimed without accessible current body → mark PARTIAL and escalate. S5: old version overwritten rather than superseded → fail audit lineage. Deliverable is a signed review report listing blockers and owner, not merely a blanket PASS. Dependencies 14-001 research, 14-003 memos, 15-002 estimate, 08-009 tie-out and 10-004 audit defense.
