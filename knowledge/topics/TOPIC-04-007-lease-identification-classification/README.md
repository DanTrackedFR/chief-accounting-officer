# TOPIC-04-007 — Lease Identification / Lease Classification

Capabilities: CAO-04-017, CAO-04-018
Status: REVIEWED

## Decision logic
Establish framework, entity type and reporting period. Identify a specified asset and test whether supplier substitution is substantive. Determine whether the customer obtains substantially all economic benefits and directs how and for what purpose the asset is used. Establish enforceable period and commencement. Apply exemptions only after identification. Classify only where the framework requires it.

## Frameworks
- IFRS 16: identification under IFRS 16.9 and B9–B31; short-term/low-value exemptions 5–8. Ordinary lessee recognition does not depend on finance/operating classification.
- ASC 842: control-based identified-PP&E model. Lessees retain finance/operating classification using ownership transfer, reasonably-certain purchase option, major-part, PV/fair-value and specialized-nature criteria.
- FRS 102: revised Section 20 applies for periods beginning on/after 1 January 2026 unless early adopted. It uses identified-asset/control concepts and removes the old lessee split for most leases. Pre-2026 cases require the legacy route.
- AASB 16: for-profit core closely follows IFRS 16, but entity type, reporting tier and Australian overlays require independent checking.

## Evidence and controls
Retain contract/amendments, asset specification, substitution clauses and economics, decision rights, economic-benefit analysis, framework/period, commencement, exemptions/elections and classification memo where applicable. Contract intake must gate schedule creation on approved identification. Reconcile approved leases to recurring AP/procurement/legal contract populations.

## Scenario QA
Dedicated server with no substantive substitution and customer decision rights → lease candidate PASS. Supplier can economically substitute fungible asset throughout use → challenge identified asset PASS. ASC 842 equipment lease → identify then classify PASS. IFRS equivalent → no artificial lessee classification PASS. UK Dec-2025 period → legacy gate PASS. UK Jan-2026 period → revised Section 20 PASS.

## Provenance
Derived from the reviewed Phase 2C lease vertical slice in TOPIC-04-010-leases, whose framework records were checked 2026-09-22. Rights status REFERENCE_ONLY; no standard text reproduced. Public FASB paragraph-body access remains a source-depth limitation.
