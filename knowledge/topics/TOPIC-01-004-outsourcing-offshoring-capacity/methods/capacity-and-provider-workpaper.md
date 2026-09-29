# Outsourcing, offshoring and capacity — CAO workpaper

Knowledge type: PRINCIPLES / PRACTICE. Capabilities: CAO-01-009, CAO-01-010. Extends existing README and Phase 2D completion note; prepared 2026-09-27.

## Decision sequence

1. Inventory activities and retain/eliminate/automate/centralize/outsource alternatives. Separate transaction handling from recognition and significant estimate decisions.
2. Observe volume, handling time, exception incidence, review time and peak cycles. Build a monthly and close-week capacity curve by skill, entity and timezone. Include audit, leave, training, supervision, system incidents and transition double-running.
3. Assess provider feasibility: data residency, local language and legal entity requirements, control segregation, access to source evidence, audit cooperation, service continuity, subcontractors and exit. Obtain specialist advice for local legal requirements; do not present a generic model as compliant everywhere.
4. Document the retained organization's accountability: policy, material judgments, period-end completeness, certification, audit responses and provider oversight. Define provider's preparation, escalation, control and evidence obligations in a RACI.
5. Pilot one complete source-to-GL flow and one exception/incident. Reconcile populations, test fallback, revoke legacy access and approve transfer only when acceptance conditions pass.

## Capacity calculation and sensitivity

Illustrative monthly AP workload: 4,000 invoices × 6 minutes = 400 processing hours. If 10% require a further 12 minutes, add 80 hours. Add 50 hours of independent review and 40 hours of close peaks: 570 hours before leave and outage reserve. At 130 productive hours per person, that is 4.38 full-time equivalents, which rounds **up** to five people for staffed coverage before further resilience assessment. A provider quote of 500 hours leaves a 70-hour gap; do not pretend future automation has already supplied it. Sensitize volume +25% and exception rate from 10% to 15%, with observed rather than arbitrary minutes. Count retained oversight separately so sourcing does not double-count savings.

## Provider specification and evidence

Contracted output must identify incoming population, accepted/rejected counts and amounts, transaction IDs, processing and posting dates, entity/currency, approvals, errors, corrections and source files. Specify cutoff by timezone, quality measures, incident classification, business-continuity test, change notification, record-retention and audit-access terms. Retained reviewer samples high-risk or unusual entries and reconciles the complete provider output to the GL/subledger; sampling alone does not establish population completeness. Version the provider configuration and exit/migration mapping.

**Adversarial test:** provider marks 4,000 invoices completed but only 3,980 appear in ERP. Status **BLOCKED** until the 20 are traced to rejection, timing or error with individually assigned disposition. An aggregate amount that happens to match after netting credits does not pass. Review segregation, contract-period cutoff and aged exception queue before certification.

## Authority and dependencies

This is CAO practice. Framework requirements flow from the transaction's accounting topic; outsourcing does not change the applicable standard or responsibility for financial statements. For a US issuer, [SEC Release 33-8810](https://www.sec.gov/rule-release/33-8810) informs management's risk-based ICFR evaluation, and [PCAOB AS 2201](https://pcaobus.org/oversight/standards/auditing-standards/details/AS2201) may affect auditor work; neither mandates this staffing formula. Sources checked 2026-09-27. Local law, service-organization reports and contract rights remain case-specific. Handoffs: TOPIC-01-003, TOPIC-09-004, TOPIC-10-001, TOPIC-11-006, TOPIC-12-009.
