# Live architecture reconstruction — Semantic Planner + Document/Data Intake

Baseline: live main `fe057c5752f2b6e5913fa56ecfadbe7fa40afe8e`, verified by fresh
GitHub clone on 2026-10-05. Repository metadata confirms main and push permission.
Read system-overview, cao-agent, orchestration, case-management, onboarding,
company-accounting-memory, context-and-promotion, artifact-architecture,
skill-specification and build-roadmap; memory structural schemas; interfaces
public-output/diagnostic contracts and privacy tests; orchestration planning,
intent, registry, runtime, both integration handoffs and fixtures; production
execution/fingerprints and all three CI workflows. No prior branch is a baseline.

The existing Planner interprets Intent and identifies Issue records. Registry
reads SKILL.md and actual production package metadata. CAO validates dimensions,
constructs Graph, executes production.assess_case, checks actual native imports,
exact-once economics, reporting/journal handoffs and challenge, then curates one
conclusion through public_record. These contracts remain authoritative.

Company Context is an immutable temporal record view, with CONFIRMED, DOCUMENTED
and APPROVED facts; proposals cannot overwrite that view. Context Observer returns
memory candidates. Persistence/authenticated approvals are future work. The public
boundary permits seven routes; internal evidence is retained separately.

47 packages are production. Government Grants, Borrowing Costs and Investment
Property remain unavailable. PR27 is outside scope. No accounting package or
canonical/supplemental knowledge changes are needed for intake.

The repository has no pyproject, requirements or setup configuration. CI installs
Python3.12 only. Although scratch has openpyxl, relying on that undeclared runtime
would break reproducible CI. This workstream uses standard-library JSON, csv,
datetime, decimal and hashlib; workbook/document envelopes accept externally
extracted data. Native XLSX/PDF/DOCX/OCR are explicitly unsupported.

Extension: SemanticPlanner.propose(RequestContext) -> StructuredProposal ->
ProposalValidator -> Intake candidate resolution -> ReviewedInputPack exact source
binding -> GovernedPlanner implementing existing Planner -> existing CAO.
No second orchestrator or production certification path is introduced. Model
output is an untrusted proposition, not authority. Native reviewed input packs
are supplied separately by the application/reviewer; they are never inferred
from approvals mentioned inside uploaded material.

The bounded foundation can prepare raw-ish sources without requiring internal
schemas from the user. Executable work still requires independently reviewed
owner contracts; unsatisfied contract fields remain material open work. Test-only
review scaffolds reuse governed fixture certification conventions, never runtime
approval fabrication. More automatic source-to-owner workpaper construction,
LLM inference, persistence, authentication and UI are outside this release.
