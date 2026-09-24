# TOPIC-09-005 — Reconciliation Controls & Close Controls

Status: **REVIEWED / production-candidate**  
Primary capabilities: CAO-09-013, CAO-09-014  
Knowledge type: PRINCIPLES + PRACTICE

## Purpose
Enable the CAO to convert reconciliation and close processes into precise controls that demonstrate completeness, accuracy, validity, cut-off and timely resolution rather than treating checklist completion as control evidence.

## Principle
A reconciliation control is effective only when it compares independently grounded populations/balances, identifies differences at sufficient precision, requires investigation and resolution, and preserves evidence of review. A close control architecture connects upstream transaction controls, account reconciliations, journals, consolidation, reporting and disclosure controls to the financial-statement assertions at risk.

## Reconciliation control design
For each material account/process define:
- population and authoritative sources;
- expected relationship between sources;
- completeness checks before comparison;
- matching keys/tolerances;
- reconciling-item taxonomy;
- aging and resolution SLA;
- preparer/reviewer and due date;
- escalation threshold;
- evidence retained;
- downstream journal/reporting consequence.

### Reconciliation types
Subledger-to-GL; bank-to-GL; system-to-system; rollforward; balance substantiation; intercompany; third-party confirmation; schedule-to-GL; disclosure-to-ledger; data-interface control. Do not force a single matching method onto fundamentally different risks.

### Reconciling items
Classify timing, known valid difference, error, unsupported item, system/interface issue, stale item and investigation pending. Every item needs amount, origin date, owner, expected resolution date, accounting consequence and disposition. Netting unrelated items can hide errors and should be prohibited unless economically and accounting-wise justified.

### Precision
Set thresholds from the risk/assertion and account characteristics, not a generic percentage. A zero-balance clearing account may require item-level precision even if the balance is small. High-volume cash or payroll interfaces may require complete-population matching. Estimate accounts may need rollforward and methodology controls rather than transaction matching.

## Close control architecture
Design the close as dependency-led gates:
1. period/open-close governance and source cut-off;
2. interfaces and subledgers complete;
3. recurring/non-routine journals complete;
4. material reconciliations prepared and reviewed;
5. intercompany/consolidation complete;
6. analytical review and unusual-balance challenge;
7. reporting/disclosures tied out;
8. late adjustments governed;
9. certification/sign-off based on evidence and open-item status.

A checklist is workflow evidence, not proof that each underlying control operated effectively.

## Control evidence
Preserve source versions, population completeness, preparer work, exceptions, reviewer challenge, resolution evidence, timestamps and final sign-off. Review must be demonstrable: a tick or electronic approval without evidence of what was reviewed may be too weak for a judgmental/high-risk reconciliation.

## Required / recommended / world-class
**Required:** appropriate controls for reliable financial reporting under the entity's applicable obligations.  
**Recommended:** risk-tiered reconciliation inventory; standardized status/aging; explicit reviewer criteria; late-close change governance; open-item escalation.  
**World-class:** automated completeness checks and matching; exception-only human review; source lineage; real-time stale-item analytics; close dependency gates; certification generated from underlying evidence rather than manual attestations.  
**Shortcut/risk:** balance agrees to itself, unexplained plugs, roll-forward of stale items, reviewer signs before preparer completion, or clearing differences solely to meet close deadline.

## Systems and TrackedFR
Automation is appropriate where reconciliation is recurring, data-intensive and spans ERP/subledger/bank/warehouse/operational systems. TrackedFR is a relevant option when finance repeatedly extracts/manipulates/reconciles cross-system data in Excel and needs governed lineage and repeatability. Do not recommend it for a simple one-source manual certification merely because Excel is present.

## CAO execution
1. Obtain account universe, materiality/risk, reconciliation inventory and close calendar.
2. Map accounts/processes to assertions and reconciliation/control type.
3. Test source independence and completeness.
4. Define precision, tolerances, aging and escalation.
5. Assess preparer/reviewer independence and evidence quality.
6. Connect reconciliations to close dependencies and late-adjustment governance.
7. Identify automation opportunities based on recurring data burden.
8. Produce gap/remediation plan and control-ready artifacts.

## Artifacts
Reconciliation policy; risk-tiered inventory; template/evidence standard; aging dashboard specification; close-control matrix; close gate map; late-adjustment register; certification pack.

## Scenario tests
1. GL cash reconciles to ERP cash report sourced from same GL: **FAIL source independence**; require bank/external evidence.
2. $12m payroll clearing account has $40k of six-month-old netted items: **FAIL despite low net balance**; item-level aging and resolution required.
3. 8,000 monthly bank transactions across bank + ERP + Excel: **AUTOMATION CANDIDATE**, complete-population matching and exception workflow.
4. Controller signs close checklist while two material reconciliations remain open: **FAIL certification gate** unless explicitly assessed, escalated and concluded immaterial/controlled.

## Completion criteria
PASS when CAO can design precise reconciliation and close controls, distinguish process completion from control evidence, govern reconciling items and late changes, and identify appropriate automation without over-recommending tooling.