# Independent knowledge QA — Investment Property

Reviewer: distinct AI agent `/root/knowledge_qa`, identity `investment_property_independent_knowledge_ai`; no human certification. Date2026-10-12.

Reviewed all96 substantive/governance claims against framework, period, supported entity scope, cross-framework exclusions, journal mathematics and disclosure distinctions. Individual claim hash dispositions and accounting challenges are recorded in `independent-review.json`. All claims retain MODEL_DERIVED_AUDIT_REQUIRED and open direct-source audit; APPROVED represents independent accuracy review, not universal authoritative text verification. Actual primary-source retrieval and inaccessible authority are recorded in `independent-source-challenge.md`.

Four findings were resolved by the implementation author and independently rerun: incorrect UK change-use paragraph, incorrect UK deemed-cost paragraph, unsupported import of IFRS insignificant-use exception into UK mixed-use route, and lineage claim-kind metadata incompatible with the validator. The last finding originally caused three approval/retrieval test failures; those failures are preserved in this explanation and are not represented as passed original runs.

Final command `python -m unittest discover -s knowledge/investment-property -p test_independent_claim_qa.py -v`:12 tests PASS, exit0. Command `python knowledge/investment-property/validate_supplement.py`:96 claims,24 per framework,APPROVED,no errors,exit0. Tests cover corrected UK distinctions, US appraisal/recognition boundary, independently recomputed transfer and disposal amounts, exact claim hashes, mutations, forged assurance/self-approval, unsupported entities/periods/early adoption and retrieval privacy.

Frozen reviewed register SHA256: `36973a0bb639cd88905a15b8f169e79869f1a491ce3ccb8621817bfaff2f25bb`.

Disposition: PASS within the expressly bounded2026 methods. Into-FV owner-use transfers remain runtime unsupported because PPE revaluation belongs to the existing owner. Unsupported construction, ROU, specialized industry/entity measurement, other editions and simplified-disclosure overlays remain excluded. This knowledge pass does not substitute for separate implementation QA, repository regression, deterministic-example verification or exact-final-head CI.
