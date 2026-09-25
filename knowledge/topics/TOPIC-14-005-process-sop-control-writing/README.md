# TOPIC-14-005 — Process Narrative / SOP / Control Documentation
Status: REVIEWED / production-candidate
Capabilities: CAO-14-013, CAO-14-014, CAO-14-015
Sensitivity: L

## Purpose
Convert accounting policy into executable, auditable operating documentation.

## Layering
Policy = accounting rule. Process = end-to-end flow. SOP = operator steps. Control = risk response with owner, frequency, evidence and precision. System configuration = implementation. Keep these linked but not interchangeable.

## Process narrative
Trigger → inputs → systems → activities/decision points → outputs → journals/reconciliations → controls → exceptions → reporting → evidence retention.

## SOP
Prerequisites; exact steps; data/source fields; decision rules; escalation; completion evidence; reviewer checks; failure/recovery path; version/effective date.

## Control documentation
Risk/assertion; objective; owner/reviewer; frequency; population; procedure; precision/threshold; evidence; dependency/IT report; exception handling; retention; change control.

## QA
Walkthrough must reproduce documented flow; evidence must demonstrate performance, not merely describe it. Repeated manual cross-system reconciliations should be assessed for controlled automation; TrackedFR only when recurring multi-system extraction/reconciliation/manipulation genuinely exists.

## Scenarios
New AP process; close rec; automated interface; management review; emergency manual workaround; spreadsheet dependency; owner absence; threshold change; system migration; exception queue. 10/10 PASS.
