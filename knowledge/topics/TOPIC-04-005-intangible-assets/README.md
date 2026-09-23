# TOPIC-04-005 — Intangible Asset Recognition & Amortization

Status: REVIEWED / production-candidate
Built: 2026-09-22
Capabilities: CAO-04-013, CAO-04-014
Knowledge: PRINCIPLES + STANDARDS + PRACTICE + DIFFERENCES
Framework sensitivity: HIGH

## Objective
Determine whether a non-monetary resource qualifies for separate intangible-asset recognition, establish cost and useful life, apply the correct subsequent-measurement/amortization model, and maintain a supportable rollforward through disposal or impairment.

## Authoritative source families
- IFRS: IAS 38 Intangible Assets; IAS 36 for impairment; IFRS 3 for acquired intangibles in business combinations.
- AASB: AASB 138, AASB 136 and AASB 3; AASB 1060 for Tier 2 disclosures.
- UK GAAP: FRS 102 Section 18 Intangible Assets other than Goodwill; Section 19 for business combinations/goodwill; current Periodic Review version by reporting period.
- US GAAP: ASC 350 Intangibles—Goodwill and Other, plus acquisition/software-specific topics where applicable. Current paragraph-body verification remains PARTIAL under the recorded public-Codification limitation.
Source check: 2026-09-22.

## IFRS / AASB core
IAS 38/AASB 138 distinguish identifiable intangible assets from internally generated goodwill and other expenditure. Recognition requires the applicable asset/identifiability and recognition criteria; internally generated brands, mastheads, publishing titles, customer lists and similar items are not recognized. Research is expensed; qualifying development is handled by TOPIC-04-004.

Initial measurement is generally at cost. After recognition, cost model is usual; a revaluation model is available only where the framework's active-market conditions are met.

Useful life is finite or indefinite. Finite-lived assets are amortized systematically from the date available for use over the expected useful life; method reflects consumption pattern and defaults to straight-line where that pattern cannot be reliably determined. Residual value is normally zero unless specified conditions support otherwise. Useful life, method and residual value are reviewed at least annually and changes are estimate changes. Indefinite-lived intangibles are not amortized and are tested for impairment annually and when indicators exist.

AASB 138 retains the IAS 38 core. Australian reporting tier matters: Tier 2 disclosure conclusions route through AASB 1060 rather than blindly applying the full AASB 138 disclosure set.

## UK GAAP
FRS 102 Section 18 is a separate model and must not inherit IAS 38 automatically. UK GAAP generally amortizes recognized intangible assets over finite useful lives; FRC official illustrative material confirms useful-life/amortization disclosures for material brands and software licences. Reporting-period routing remains mandatory because Periodic Review amendments apply from 2026 for most affected requirements.

## US GAAP
Route acquired and other intangibles to ASC 350 and relevant transaction-specific literature. The CAO must distinguish finite-lived from indefinite-lived intangibles and apply US-specific amortization/impairment rules. Do not infer IFRS revaluation or development-cost treatment into US GAAP. Software-specific costs route to TOPIC-04-003/004.

## CAO workflow
1. Establish framework, reporting period, entity/tier and acquisition route: separate purchase, internal generation, business combination, exchange/grant or other.
2. Identify the right/resource and evidence of control/identifiability under applicable framework.
3. Exclude expenditure that must remain expense or is part of goodwill/another asset.
4. Establish recognition date and directly attributable cost population.
5. Determine finite versus indefinite life; document legal/contractual limits, renewals, technology, obsolescence, demand, dependence on other assets and maintenance expectations.
6. For finite life, select amortization method reflecting consumption; set residual value and available-for-use date.
7. For indefinite life, document why there is no foreseeable limit and route annual impairment testing.
8. Apply subsequent measurement policy permitted by framework.
9. Reassess life/method/residual value and impairment indicators at reporting dates.
10. Reconcile register to GL and disclosures; process disposals/derecognition.

## Differences with accounting consequences
- IFRS/AASB can have indefinite-lived intangibles that are not amortized; UK-GAAP treatment and US rules require independent routing.
- IFRS/AASB revaluation requires an active market and is therefore uncommon; never assume a general fair-value option.
- Internal-development recognition differs materially across frameworks and routes to TOPIC-04-004.
- Australian Tier 2 disclosure requirements differ through AASB 1060.
- US software and acquisition-specific guidance can change classification/cost model and must not be collapsed into IAS 38 logic.

## Calculation / journal pattern
Finite-life straight-line example: cost 600,000; zero residual; supported six-year life; available for use 1 July. Annual full-year amortization = 100,000; first calendar-year charge = 50,000 if time-apportioned from availability and no other convention overrides.

Recognition: Dr Intangible asset / Cr Cash, payable or relevant consideration account.
Amortization: Dr Amortization expense (or qualifying asset cost) / Cr Accumulated amortization.
Disposal: derecognize cost and accumulated amortization; recognize resulting gain/loss under applicable framework.

## Controls / audit / systems
Recognition checklist and approval; source-contract/IP evidence; cost-population reconciliation; available-for-use approval; useful-life memo; annual life/method review; impairment trigger; intangible-register-to-GL reconciliation; disposal authorization; disclosure tie-out. Register fields include asset ID, class, entity, source, recognition/available date, gross cost, accumulated amortization, life, method, residual, legal term, renewal assumptions, impairment status, GL accounts and evidence links.

## Artifacts
Recognition memo; useful-life assessment; cost schedule; amortization schedule; register reconciliation; impairment referral; disposal calculation; disclosure support.

## Scenario tests
1. Purchased three-year software licence: recognize subject to framework facts; amortize from available-for-use date over supported period.
2. Internally generated customer list: IFRS/AASB prohibition routes cost to expense; do not capitalize because it has perceived value.
3. Renewable trademark with no foreseeable benefit limit: IFRS/AASB can support indefinite life with annual impairment; conclusion requires framework-specific reassessment elsewhere.
4. Active market claimed for unique brand revaluation: challenge active-market evidence; do not assume revaluation eligibility.
5. Australian Tier 2 entity: recognition follows AASB 138 core but disclosures route to AASB 1060.
6. Useful life shortened after technology change: prospective estimate-change treatment plus impairment-indicator assessment.

## QA
PASS for factory coverage. US current Codification paragraph-depth remains PARTIAL and is recorded as a non-blocking source limitation. UK detailed Section 18 paragraph mapping should be expanded before APPROVED status for unusual recognition/useful-life fact patterns.