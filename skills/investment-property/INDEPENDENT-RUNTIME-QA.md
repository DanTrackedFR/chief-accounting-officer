# Independent Investment Property actual-code adversarial QA

Reviewer: separate AI agent `/root/implementation_qa_final`, not the substantive
workflow author; no authenticated human sign-off or authoritative-source audit
is asserted. All documentary sources, names and approvals in the tests are
explicitly synthetic. The earlier reviewer's historical fingerprint preparation
is retained separately and is not represented as this runtime review.

## Executed scope and evidence

Command, repository root:

```sh
PYTHONPATH=skills:skills/tests:. python -m unittest skills.tests.test_independent_investment_property_runtime skills.tests.test_independent_investment_property_integration -v
```

2026-10-12 independent initial combined rerun: **33 test methods PASS; exit 0; 19.494 seconds**.
After the substantive author's class-rollforward correction, **35 test methods
PASS; exit 0; 15.849 seconds**, including independent equations across 27 supported
framework/model/event combinations and all 210 manifest file hashes/42 sources.
The permanent artifact test was then strengthened further to re-execute every
saved Case and compare its exact result; this final strengthened test and
deterministic `--verify` remain **PENDING regeneration of new IP examples and
independent final rerun**. The first read-only `--verify` returned exit 1 because
new IP implementation/document bytes changed the certification fingerprints;
inspection found only `reviewer_signoff` changed in the first saved initial Case.
This is not recorded as PASS and no historical artifact regeneration is authorized.
Final immutable evidence must be stored separately outside the skill fingerprint
population, under `build4/release/ip-independent-final/`, after this report freezes.
Subtests additionally cover framework/model variants and malformed records.
Tests execute ordinary `production.assess_case("investment-property", case)`;
no substantive method is mocked, copied, replaced or implemented by this reviewer.
Fixture certification is synthetic reviewer input, not an engine-generated
approval. The test arithmetic expectations are independently written literals,
not production output or a generated artifact oracle.

Reviewed working-tree baseline HEAD: `387099829d7035f55b8838799e11e722399d167e`.
This is a local independently tested working tree, not a claim of final-head CI.
Reviewed implementation/fixture/test bytes:

| File | SHA-256 |
| --- | --- |
| `skills/investment-property/workflow.py` | `8f1de85ada862ae1eddc6b15d7f8724ead9f36fe1df35a6d84681241f0dde758` |
| `skills/tests/investment_property_cases.py` | `855e9b7ddc325c682a05505b422b83f85b584fb9f56e51f4958519a96366d292` |
| `skills/tests/test_independent_investment_property_runtime.py` | `3bde489679a45b29fbd475df5bebd1e6fcfca26e3881617dcdc13066d7659852` |
| `skills/tests/test_independent_investment_property_integration.py` | `fc7152ef82d7405fe5f7b80e0f810d236416a9574c751e0ad259abd8a9c54be5` |

Hashes bind the final frozen test and corrected workflow sources; the final
strengthened artifact rerun is pending as stated above. Any material implementation change
requires independent rerun. The primary agent owns full regression and exact-head
GitHub Actions evidence and must update the final release ledger accordingly.

## Accounting calculations independently challenged

- Initial cash acquisition: purchase price 590,000 + direct conveyancing 10,000 =
  asset and cash credit 600,000; IFRS, AASB and ordinary US cost routes.
- Annual cost route: gross 600,000 minus nondepreciable land 100,000, divided by
  25 years = depreciation 20,000; closing 580,000. Fixed Assets/Impairment effects
  are evidence only, with no duplicate journal by Investment Property.
- Fair-value holding: 650,000 - opening 600,000 = P&L gain 50,000; IFRS, AASB,
  FRS 102 supported routes. Negative/cent variant: 525,123.45 - 600,000 =
  loss 74,876.55 with reversed debit/credit sides.
- Disposal: 700,000 - selling costs 10,000 = cash 690,000. Fair-value carrying
  650,000 gives gain 40,000; cost carrying 580,000 gives gain 110,000. A separate
  fair-value disposal loss example produces cash 400,000, carrying 650,000,
  disposal loss 250,000, retaining only one preceding fair-value gain 50,000.
- Cost transfer in preserves 600,000; cost transfer out 580,000; fair-value
  transfer out 650,000. All output journals are independently debit/credit summed.

## Failure controls challenged

Independent tests cover missing original sources, acquisition cost economics,
duplicate economic ownership, duplicate property identities, legal title/owner,
entity/framework/currency/period identities, policy/edition/adoption leakage,
ordinary US fair-value refusal, FRS 102 forbidden ordinary cost election,
Australian Tier 2 refusal, unsupported property/lease/construction features,
mixed-use segregation and insignificance, wrong valuation basis/date, unreliable
or uncertain valuation, duplicate external recognition, missing GL offsets,
statement mismatch, exact source snapshot contradictions, missing numeric
disclosure sources, transfer direction and continuing-involvement disposal.

A coherent but wrong depreciation source, carrying values, GL and disclosure
re-certification is independently rejected by mathematical reperformance.
Replacing a current sign-off with stale or self-approved certification cannot
release journals; stale knowledge documents block. Repeated assessment leaves
the input case unchanged, and source mutation changes its case fingerprint.
All **seven actual registered public routes** are executed without skips; raw
source objects, reviewer names, valuation report hashes and internal source notes
are absent. Supplemental public topic identity is intentionally allowed by the
public contract and is not incorrectly treated as provenance leakage.

## Finding and independent final disposition

**R1 — missing post-acquisition annual measurement (material; fixed).**

Reproduction: `test_non_cutoff_initial_recognition_requires_subsequent_owner_accounting`.
Set initial cost acquisition/event/cash and cost-document dates to 30 June 2026,
keep the annual 31 December reporting period and 600,000 closing carrying amount,
recapture the altered documentary population and obtain a new synthetic case
certification. Original code returned COMPLETE without post-acquisition
depreciation/impairment owner accounting. This was not merely stale certification.

The substantive author bounded event routes to reporting cutoff, tied initial
legal acquisition date to event date, and added independently reviewed prior
asset identity/model/carrying history. The reviewer independently reran R1 and
expanded denials to non-cutoff cost/FV initial, transfer and disposal routes,
wrong prior asset model/carrying/date/currency, in-period acquisition presented
as opening ownership, and unsupported prior impairment basis. All pass.

Disposition: **RESOLVED within the explicitly cutoff-only first release**.
Midyear acquisition/transfers are unsupported, not silently declared correct.

Initial test development had two non-findings: expecting PARTIAL rather than
BLOCKED when source memo mutation contradicted the original snapshot, and
incorrectly denying the contract-approved supplemental public topic identifier.
Those assertions were corrected; no production change was requested for them.

**Author-discovered class rollforward defect — independently rechecked.**
The author corrected transfer-in class opening from PPE source carrying 600,000
to Investment Property class opening zero. The former numbers doubled the
movement in the disclosure rollforward even though individual journals balanced.
The permanent independent test recomputes opening + additions - depreciation -
impairment + fair-value movement + transfers - disposal carrying = closing for
27 supported framework/model/event routes. Transfer-in explicitly requires
0 + 600,000 transfer = 600,000 closing. This review preserves discovery attribution
and does not imply the independent reviewer originally found the author's defect.

The example generation script was inspected: `--verify` compares population and
bytes read-only; generation is restricted to the new IP `examples/production`
namespace. At this review checkpoint `git diff --name-only` over historical
skill examples and orchestration evidence was empty. The separate existing
`build4/verify_release.py` verifier is modified by integration work; that is code,
not a rewritten historical example or result. This
is not a substitute for the primary agent's full historical integrity proof.

## Explicit review limitations

The independent integration suite additionally executes the native CAO owner,
closes the Investment Property Case, verifies the 50,000 gain, and proves no
unrelated owners execute. An incomplete material property source leaves a
separate Accounts Payable owner complete and Investment Property blocked.
SQLite save/repeated restores preserve byte-exact canonical Case snapshots,
including native history and result versions; restore is performed while
`CAO.run` is mocked to forbid accounting replay. Local adapter execution/restart,
resume and execute retries preserve accounting results; an altered independently
recaptured/re-certified source cannot replace a committed immutable submission
or its historical result. A real HTTP queued job executes the native owner and
its public result equals the local resumed result exactly.

This suite does **not**, by itself, prove selective rework, Company Memory,
all historical artifact reproduction, full repository regression or exact-head
Actions. Those separate release gates must remain explicit in the primary
agent's release evidence. Synthetic external-owner and valuation evidence is not authentication
or an external valuation engine; no ERP posting is performed or authorized.
Framework knowledge/source assurance is independently reviewed by the separate
knowledge reviewer, not certified by this implementation test report.

Runtime review disposition: **PASS for corrected bounded accounting and existing
33 runtime/integration tests; final strengthened 35-method artifact reproduction
gate PENDING**. The external final evidence directory will record its actual
independent completion without modifying this fingerprint-bound report.
