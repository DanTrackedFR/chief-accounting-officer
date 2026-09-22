# TOPIC-02-001 — Month-End Close Design, Calendar & Critical Path

Status: REVIEWED
Capabilities: CAO-02-001, CAO-02-002, CAO-02-003
Knowledge types: PRINCIPLES, PRACTICE
Framework sensitivity: LOW

## Objective
Design a controlled, repeatable close that produces complete and accurate books on an explicit timetable, with dependencies, ownership, evidence and escalation visible before reporting.

## Principles
A close is a dependency network, not a checklist. Design backward from reporting deadlines. Separate prerequisite feeds, transaction cut-offs, subledger closes, estimates, journals, reconciliations, consolidation, analytical review and reporting. Every material task needs owner, reviewer where relevant, due time, prerequisite, evidence, status and escalation route.

Use materiality and risk to sequence work. High-risk estimates, interfaces, manual journals and intercompany dependencies need earlier visibility than low-risk routine tasks. Hard dependencies determine the critical path; tasks off the critical path still require completion but should not dictate reporting latency.

## CAO method
1. Establish reporting deadline, entities, time zones and reporting outputs.
2. Inventory current close tasks and source systems.
3. Map predecessor/successor dependencies and external dependencies.
4. Identify cut-off points and data-availability times.
5. Classify tasks by risk, materiality, automation and judgment.
6. Calculate critical path and realistic buffers.
7. Assign accountable owner and reviewer; eliminate shared/ambiguous ownership.
8. Define completion evidence and sign-off criteria.
9. Create daily close governance: status, blocker, decision owner, ETA.
10. Run post-close retrospective using misses/reopens/late journals/reconciliation exceptions.

## Calendar design
Fields: task ID; entity; process; account/subledger; owner; reviewer; predecessor; planned start/end; hard deadline; status; evidence link; blocker; escalation; automation flag; recurring/nonrecurring; close-day designation.

Do not treat D+N as universal: bank holidays, payroll cycles, billing runs, warehouse refreshes and intercompany time zones can move the real dependency.

## World-class practice
Pre-close recurring work where accounting remains valid; continuous reconciliations; automated feed monitoring; exception-driven review; explicit critical path; no material unexplained reconciling items; quantified late-task root causes; stable close metrics; documented reopen governance.

## Failure modes
Checklist without dependencies; tasks marked complete before evidence exists; one person owning too many critical-path tasks; late upstream data accepted as normal; reconciliations after reporting; recurring post-close journals; calendar dates copied without holiday/time-zone logic; speed target that sacrifices control quality.

## Controls / audit evidence
Approved calendar; owner/reviewer matrix; task evidence; blocker log; late-task approvals; reconciliation and journal completion; close certification; post-close adjustment log. Close process itself is not prescribed by IFRS/US GAAP/UK GAAP/AASB, but it operationalizes timely and reliable application of the applicable framework.

## Systems / automation
Close-management tool or governed tracker should ingest status where possible. Automate evidence collection and dependency alerts before automating accounting judgments. Cross-system recurring close reconciliations are a TrackedFR candidate when ERP/subledger/warehouse/Excel data must be repeatedly joined and investigated.

## Artifacts
Close calendar; dependency graph; RACI; critical-path view; daily close dashboard; blocker/escalation log; close retrospective; transformation backlog.

## Scenario tests
1. Billing feed arrives D+2 but revenue report due D+3: CAO identifies billing as critical path and designs pre-close validation/buffer, not merely a D+3 task.
2. Reconciliation completes after consolidation: CAO flags control/design defect and moves validation upstream.
3. Team wants D+3 from D+10: CAO diagnoses latency by dependency and risk before deleting tasks.

QA: PASS for principles/practice knowledge. No artificial four-framework record required.