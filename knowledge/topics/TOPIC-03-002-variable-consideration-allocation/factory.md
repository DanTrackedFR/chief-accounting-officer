# TOPIC-03-002 — Variable Consideration / Transaction Price Allocation

Status: REVIEWED
Capabilities: CAO-03-004, CAO-03-005
Sensitivity: MEDIUM/HIGH
Source checked: 2026-09-22

## Sources
IFRS 15; ASC 606; revised FRS 102 Section 23 for periods beginning on/after 1 Jan 2026; AASB 15. Primary official source families; REFERENCE_ONLY where licensing requires. This record builds on TOPIC-03-001.

## Variable consideration
Identify every term making consideration uncertain: discounts, rebates, refunds, credits, concessions, incentives, performance bonuses, penalties, returns, service-level credits, usage/volume tiers and similar items. Also assess whether facts/customary practice create variability not obvious from headline price.

Estimate using the framework-appropriate expected-value or most-likely-amount method according to which better predicts consideration. Apply the constraint before including variable amounts so recognized revenue is appropriately protected against significant future reversal under the applicable framework. Reassess estimates each reporting date using current facts.

Do not mechanically equate 'uncertain invoice' with variable consideration. Distinguish price uncertainty from collectibility/credit risk, contract modification and consideration payable to a customer.

## Allocation
Allocate transaction price to performance obligations using relative standalone selling prices (SSP), subject to specific guidance for discounts and variable consideration that relates entirely to one or more, but not all, performance obligations.

### SSP hierarchy
Observable standalone sale price is strongest evidence. If not observable, estimate using a method maximizing observable inputs: adjusted market assessment, expected cost plus margin, or residual approach only where applicable conditions are satisfied. Establish governance for ranges, segmentation, geography, customer class, product maturity and refresh frequency.

Do not use list price automatically as SSP. Do not allocate based on cost merely because it is convenient.

## Framework differences routing
IFRS 15 and ASC 606 share the core model but wording/application differences and subsequent amendments must be checked for material cases. Revised FRS 102 is proportionately aligned, not presumed identical; reporting period is mandatory. AASB for-profit Tier 1 generally follows IFRS 15, while NFP/tier overlays remain separate.

## CAO workflow
1. Start from approved performance obligations and contract transaction-price population.
2. Catalogue variable terms and source data.
3. Select estimation method and document why it predicts the amount.
4. Evaluate constraint evidence and reversal risk factors.
5. Determine total constrained transaction price.
6. Establish SSP evidence for every performance obligation.
7. Test discount/variable-allocation exceptions before relative allocation.
8. Allocate and reconcile allocated total to transaction price.
9. Establish reassessment cadence and change triggers.
10. Pass allocated amounts to recognition-timing engine.

## Calculation pattern
Relative allocation = transaction price × PO SSP / total SSP, unless specific discount/variable allocation guidance changes the result.

Example mechanics only: constrained transaction price 120; SSPs A=100, B=50 → ordinary relative allocation A=80, B=40. Production answer must first test whether discount or variable consideration is specifically attributable.

## Controls
Approved variable-consideration inventory; source completeness; estimate model review; retrospective accuracy analysis; SSP governance/versioning; observable-sale population controls; allocation recalculation; contract amendment trigger; review of manual overrides.

## Data
contract_id, variable_term_id, type, estimate_method, scenarios/probabilities where relevant, constrained_amount, evidence_date, SSP_version, PO_id, observed/estimated flag, SSP_method, allocation_exception, allocated_amount, reviewer.

## Artifacts
Variable-consideration paper; rebate/returns model; constraint assessment; SSP study; allocation workbook; quarterly reassessment evidence; override log.

## Scenarios
1. Sales bonus with binary outcome: assess most-likely vs expected value and constraint rather than always probability-weighting.
2. Portfolio of many similar returns: expected-value approach may better predict outcome; reconcile historical return data.
3. Deep bundle discount: test whether discount belongs entirely to specified obligations before relative allocation.
4. Highly variable licence SSP: residual method is not a convenience shortcut; verify eligibility.
5. Mid-contract estimate change: update transaction price/allocation and route resulting revenue effect under applicable guidance.

## QA
PASS: variable consideration, constraint, SSP and allocation logic are executable and linked to controls/data. Recognition timing remains in TOPIC-03-003.