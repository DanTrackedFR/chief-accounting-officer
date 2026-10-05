# Independent intake adversarial QA

Reviewer: separate agent/context, no implementation edits. Scope: semantic contract,
source adapters, proposal validation, resolution/promotion, reviewed-owner binding,
public boundary and flagship claims. Reviewed current files directly rather than
relying on implementer summaries. Regressions: `orchestration/tests/test_intake_independent.py`.

## Findings requiring remediation

1. **Framework contradiction accepted (high):** an extracted numeric candidate can
   assert US_GAAP under current IFRS execution context. Known vocabulary validation
   alone does not establish framework provenance or consistency. Reject contradictory
   authoritative dimensions or retain an explicit dispute; never establish silently.
2. **Declared candidate conflicts ignored (high):** a candidate with a nonempty
   `conflicts` list is promoted established. Validate conflict identities and carry
   disputed status/questions, or reject unsupported conflict references.
3. **Economic alias duplication (high):** identical source field can be submitted
   twice under different semantic attribute names. The original identity includes the
   attribute and therefore permits alias duplication. Initial regression failed;
   during review an implementation change made it pass. Independently rerun required.
4. **Contract flagship lacks meaningful term extraction (acceptance blocker):**
   fixture produces a constant generic owner-review sentence for arbitrary contract
   text. It does not propose parties, term, consideration, billing, cancellation or
   services. This does not meet the explicit second flagship. Add source-backed term
   proposals through injected semantic fixtures; keep inference unresolved and route
   judgments to Revenue. A model-free general parser is not required.
5. **Prior comparator disconnected from uploaded source (high):** changing prior
   gross profit CSV from 15000 to 123 leaves diagnostic bridge change -31304. Review
   pack explicitly skips prior-profit binding and supplies the existing comparator
   document. Reject mismatches or bind the actual comparator with preserved status
   and review gates. This is a real end-to-end lineage defect, not a parser limitation.
6. **Management hypothesis never tested (acceptance blocker):** FX commentary is
   merely serialized into proposal. No disposition links it to diagnostic evidence.
   Add explicit deterministic hypothesis evaluation, reject unsupported causation,
   retain actual analytic references and public-safe limitation/disposition.

## Independently checked controls

Private model text in invalid missing attributes does not reach public output.
Mutating a prepared AP candidate while removing its binding is rejected before
execution. Existing immutable raw/extraction comparisons, inert path labels,
production-owner metadata checks and separately reviewed packs are sound bounded
foundations. Native binary PDF/DOCX/XLSX, OCR, persistence, authenticated uploads and
live model inference are explicitly unsupported and are acceptable scope limits.

## Initial execution

First run: six tests, four failures (findings 1–4). Expanded run: eight tests,
five failures (1, 2, 4, 5, 6); economic alias regression passed after concurrently
applied remediation. No protected accounting packages or knowledge were changed.
Final independent rerun pending implementation remediation.

## Remediation verification

All six substantive findings have executable regressions and independently reran
successfully after implementation remediation:

- Framework dimensions now reject disagreement with governed Company Context.
- Supplied unresolved conflict references cannot establish facts.
- Numeric source-field aliases cannot duplicate economic identity.
- Contract control now proposes seven distinct, paragraph-backed terms (parties,
  term, consideration, billing, services, cancellation and variable amounts). The
  reviewer retained live `services` naming; no implementation changes were made
  by this reviewer. Contract accounting and unspecified rights remain unresolved.
- Prior comparator has an explicit comparator binding; changing the source value
  while retaining the reviewed fixture now raises a deterministic mismatch.
- Management FX claim has a structured metric comparison and `REJECTED`
  disposition, source references and result evidence, with accounting authority
  explicitly false. No prose keyword dispatch grants accounting authority.

The expanded independent suite has 17 tests, including nine separate malformed
proposal subcases, and passed. It additionally checks boolean/nested amounts,
malformed dimensions, missing evidence, unknown/NONPRODUCTION owners, forged
approval/assumption, inference promotion, approved-context preservation, known
context question suppression, omitted owner bindings, malformed CSV/binary/nested
cells/document page/metadata, inert formula/path inputs, tampered source-row
lineage and privacy on every public route. A secondary-diagnostic underrouting
attempt is rejected by the source-supported issue coverage check.

No remaining precise architectural blocker was identified in this bounded
foundation. ReviewedInputPack remains separate, externally qualified scaffolding;
intake does not certify entire owner workpapers from documents. Not every owner
field is populated from raw sources, and full arbitrary contract understanding is
not claimed. Those limitations must remain explicit in integration handoff.

## Final lifecycle/dimension refinement review

Independently inspected the final integration delta: `GovernedPlanner` provides
validated material questions to the existing CAO before CHALLENGE, synthesis,
documentation and closure. A conflicting factory Case no longer closes and then
has its history rewritten. The new executable closure regression checks partial
outcome, DOCUMENTED status, presence of the labour conflict, partial synthesis,
CHALLENGE transition and absence of any CLOSED transition. Additional regressions
reject a record identity exceeding the bound and prevent row EUR amounts from
being established using USD source metadata. Final independent command:

`python -m unittest orchestration.tests.test_intake_independent -q`

**20 tests passed in 20.817 seconds.** Earlier 17-test totals above describe the
prior review iteration; this 20-test rerun is the final independent evidence.
No additional findings or implementation changes by the reviewer.

## Additional material-question finding and final remediation

**IQA-7 — Source-answerable document wording caused unnecessary questions.**
The contract control initially asked seven separate confirmations for exact
paragraphs already present in the supplied source: parties, term, consideration,
billing timing, services, cancellation and variable amounts. This was an execution
quality defect against the requested material-question boundary. The independent
regression reproduced it: 21-test run had one failure listing all seven fields.

Remediation suppresses questions for exact sourced EXTRACTED/OBSERVED text with
identity transformation and no conflict. It retains the textual candidates as
unresolved owner-review evidence; it does not promote wording or management
positions to accounting truth. Required refund-rights and performance-obligation
questions remain blocking, unresolved judgments remain in the owner-input pack,
and the contract Case remains blocked. The reviewer independently inspected this
narrow rule and verified the conditions in the regression.

Final independent rerun after remediation:
`python -m unittest orchestration.tests.test_intake_independent -q`

**21 tests passed in 20.979 seconds.** This supersedes earlier iteration totals.
Seven substantive findings are documented, remediated and executable. No remaining
precise blocker was identified within the stated supported foundation scope.

## Additional declaration-resolution finding

**IQA-8 — Dangling semantic assumptions/disputes could be ignored.** Top-level
assumptions and disputed-fact declarations were validated as envelopes but could
remain disconnected from Fact Candidates. Candidate resolution would therefore
not carry their material uncertainty forward. The independent parameterized
regression reproduced both: the initial 22-test execution failed its assumptions
and disputed_facts subcases because both proposals were accepted.

Remediation requires each assumption declaration to match an ASSUMED candidate,
and each dispute declaration to match a DISPUTED or UNRESOLVED candidate. Unbound
declarations fail closed. The reviewer inspected both guards and independently
reran the regression and entire suite.

**Final independent result: 22 tests passed in 21.217 seconds**, using
`python -m unittest orchestration.tests.test_intake_independent -q`.

This supersedes all earlier iteration totals. Eight substantive findings have
been documented, remediated and independently rerun as executable regressions.
No remaining scoped architectural blocker identified; supported limitations above
continue to apply. This reviewer changed only independent tests and this report.
