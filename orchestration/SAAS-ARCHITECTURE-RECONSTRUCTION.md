# SaaS / month-end close: live architecture reconstruction

Baseline main: `2700b3dd7c8cb43c21ff874ef44bd0832e73b351`.
This is an architecture checkpoint, **not a completed flagship or integration candidate**.
No roadmap completion or production promotion is claimed.

## Inspected live architecture

Read architecture/build-roadmap.md, system-overview.md, cao-agent.md,
orchestration.md, case-management.md, company-accounting-memory.md,
context-and-promotion.md; root AGENTS.md; interfaces README, diagnostic contract,
public-output implementation and semantic schema; orchestration planning, intent,
registry, runtime; intake sources, semantic validation and preparation; both
DIAGNOSTIC-INTEGRATION-HANDOFF.md and INTAKE-INTEGRATION-HANDOFF.md; existing
manufacturing, monthly diagnostic and intake source/review scaffolds and generated
examples; all nine assigned owner contracts/methods; production.py, relevant native
workflows, authored/independent tests and all three GitHub workflows.

The live registry has 47 production metadata packages. The assigned nine owners
are available through production.assess_case. Revenue, AR, ECL, FX, Reconciliations,
Close, Financial Statements and Disclosure remain 1.0.0; Analytics is 1.1.0.
Government Grants, Borrowing Costs and Investment Property remain review /
NONPRODUCTION; metadata availability and executable registration are separate.

The executable path is RawSource -> Inventory extraction -> StructuredProposal
-> ProposalValidator -> candidates/conflicts/questions -> ReviewedInputPack with
exact source bindings -> GovernedPlanner -> existing CAO graph -> assess_case ->
challenge/synthesis -> public_record. No source/model assertion approves a native
workpaper. Existing fixture reviewers certify controlled test cases separately.

Native accounting inputs and owner results are fingerprinted against actual
knowledge and implementation. Native imports are reexecuted and exact-compared.
GovernedPlanner imports may add dependencies, never erase them. Runtime preserves
one entity/framework/jurisdiction/current period/functional currency per Case.
Comparative analytic sources are not multi-period owner execution. Context Observer
returns proposed memory candidates; persistence/authenticated approvals/UI are out
of scope. Public output is curated independently of internal Case evidence.

## Integration deficiencies to resolve before flagship execution

1. **AR and ECL semantic adapters are absent.** FACT_ADAPTERS has no AR or ECL
   family, and ProposalValidator rejects an issue whose family/owner is not in
   that table. Production metadata alone therefore does not make these owners
   selectable through intake. Add generic receivable and credit-exposure families,
   with actual governed native populations, rather than a SaaS objective dispatcher.
2. **AR cannot reconcile a period-end foreign monetary receivable.** Its native
   contract requires each invoice/receipt currency equal functional_currency and
   its closing equation is opening + billings - credits - applied cash/deposits.
   There is no reviewed FX movement input. Converting opening/current rows to
   closing-rate amounts would corrupt invoice rights, original due dates and
   movement attribution; omitting the foreign customer would make the scoped
   ageing incomplete. A supported extension must consume actual FX-owner amounts
   by invoice and preserve original foreign/book values and dates. It must not
   calculate rates inside AR or accept an unqualified generic adjustment.
3. **The integrated journal gate duplicates shared economics.** Revenue emits
   recognition, billings and collections; AR emits billings and collections;
   ECL emits its gross additions/receipts as well as allowance changes; FX emits
   settlement and remeasurement. Runtime._journal_mapping sums every completed
   owner journal. It has no reviewed economic-entry disposition linking an
   evidence-only duplicate to the actual posting owner. Owner-result imports'
   evidence_only modes do not govern graph-level journal assembly. Mapping labels
   cannot remove duplicated cash/AR postings. Neither deleting native journals
   nor bypassing the combined GL gate is acceptable. A generic reviewed,
   exact-payload journal ownership/disposition contract is a prerequisite.
4. **SaaS reporting metric handoffs are absent.** _handoff's allowlist includes
   Revenue's period revenue but not AR closing/ageing, ECL allowance or FX monetary
   movements/contract balances. Required reporting bridges infer only inventory
   and revenue links. A supplied FS case can otherwise be complete without
   executable alignment to those selected owners. Add supported semantic metrics
   and required owner/report/reconciliation edges; do not rely on equal totals.
5. **Close/reconciliation exception execution is deliberately fail-closed.**
   Native routes require resolved exception/complete populations for usable clean
   workpapers. An unresolved source conflict must keep the overall Case partial
   or blocked; downstream FS/Disclosure must not consume failed results. Bounded
   analytical evidence can remain usable without claiming clean close approval.
6. **Analytics scope is bounded.** 1.1.0 has a single optional diagnostic bridge
   and on-time-reconciliation KPI. DSO and a set of AR/deferred/ECL/FX bridges are
   not existing native methods. Reusing signed source/owner flux needs no version
   bump; adding executable collection/DSO methods or materially expanded multi-
   bridge contracts does. No fixture helper may become an accounting engine.

These are actual live-contract limitations, not missing accounting source access
or an approval requirement. No skill gates have been relaxed. Reproducers and a
separate review distinguish baseline capability from the requested future
flagship. A completed candidate needs implementation, specialist/independent QA,
regenerated fingerprint-sensitive artifacts, complete regression and exact-head
CI; this checkpoint must remain Draft.

## Preserved scope

No modifications to Government Grants PR #27 or any residual accounting package.
No Treasury/Financing or Group Accounting flagship, multi-entity execution,
persistence, deployed API or UI. Canonical and supplemental knowledge, roadmap,
production contracts and runtime bytes remain unchanged at this checkpoint.
