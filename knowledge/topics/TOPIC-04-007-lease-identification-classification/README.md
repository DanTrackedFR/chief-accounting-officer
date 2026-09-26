# TOPIC-04-007 — Lease Identification / Lease Classification
Capabilities: CAO-04-017, CAO-04-018
Status: REVIEWED / production-candidate

## Canonical scope
Determine whether a contract contains a lease and, where the applicable framework requires it, classify the lease. This canonical topic reuses the proven Phase 2C lease vertical slice rather than duplicating standards content.

## Decision path
1. Resolve entity, framework, reporting period and lessee/lessor role.
2. Obtain contract, amendments and side letters.
3. Test scope, specified asset and substantive substitution rights.
4. Test rights to economic benefits and to direct use.
5. Separate lease/non-lease components and document elections.
6. Apply framework-specific classification only after lease identification.
7. Preserve the conclusion, evidence, reviewer and effective-period framework.

## Shared factory artifacts
Authoritative framework records, differences, source/effective-date maps, workflow, controls, examples and QA live in `../TOPIC-04-010-leases/`. The shared workflow steps 1–6 cover identification/components and step 11 covers framework-specific classification. This avoids four inconsistent copies of lease authority.

## QA
PASS — embedded-asset scenario tests specified asset, substitution, economic benefits and decision rights before measurement.
PASS — IFRS-versus-ASC-842 scenario routes classification/model differences correctly.
PASS — UK pre/post-2026 scenarios enforce the effective-period gate.
PASS — Australian NFP scenario applies the Australian overlay rather than blind IFRS inheritance.

See `../TOPIC-04-010-leases/tests/executed-scenarios.md` for executed evidence (S1, S3, S6–S8). Residual paragraph-level source QA limitations remain those recorded in the shared vertical slice; REVIEWED does not mean final APPROVED.
