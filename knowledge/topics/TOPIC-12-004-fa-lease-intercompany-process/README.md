# TOPIC-12-004 — Fixed Asset / Lease / Intercompany Accounting Processes

Status: REVIEWED / production-candidate
Primary capabilities: CAO-12-010, CAO-12-011, CAO-12-012
Framework sensitivity: H; this process topic consumes conclusions from PPE, lease and group-accounting topics.

## Objective
Translate approved technical accounting into repeatable subledger operations with complete populations, controlled changes and GL reconciliation.

## Fixed assets
Intake approved capital additions with source invoice/project/asset lineage; establish in-service date, class, location/entity, cost components, useful life/residual value and depreciation method from approved policy; control transfers/disposals; reconcile FA register additions/depreciation/disposals/CIP to GL; investigate orphan GL postings and register-only items; perform physical/existence controls appropriate to asset risk.

## Leases
Maintain complete contract population; connect contract/amendment to lease assessment; control commencement, term, payment stream, rate and modification inputs; run schedule; post ROU/liability/expense entries according to framework conclusion; reconcile lease system/schedule to GL and disclosure populations; maintain modification and termination queue. Technical lease conclusions remain in TOPIC-04-010/011 knowledge.

## Intercompany
Require bilateral transaction identifiers, counterparty, entity/currency, nature and settlement status. Reconcile reciprocal balances before consolidation; distinguish timing, FX, classification, missing transaction and true disagreement; assign owner to each difference; eliminate using controlled rules; preserve source balances and elimination lineage. Do not plug differences to force zero.

## Shared controls
Population completeness; approved master data; subledger configuration/versioning; posting-interface totals; period lock; change approval; subledger-to-GL reconciliation; aging of exceptions; reviewer certification; disclosure/reporting tie-out where relevant.

## Systems
Every automated posting must retain run ID, source population, rule/config version, output batch and exception population. Completeness precedes accuracy testing.

## Artifacts
FA rollforward/reconciliation; lease reconciliation and modification log; intercompany matrix and mismatch queue; posting-control totals; process narratives; close evidence.

## Scenarios
Capital project goes live mid-month: route capitalization/in-service judgment to asset topic then update register prospectively as required. Lease amendment changes space: technical modification analysis precedes schedule change. Intercompany receivable has no counterparty payable: trace source transaction and cut-off rather than booking an unsupported elimination.

## Completion criteria
CAO can operationalize authoritative conclusions into controlled recurring subledger processes and reconcile them end-to-end without duplicating technical standards logic.