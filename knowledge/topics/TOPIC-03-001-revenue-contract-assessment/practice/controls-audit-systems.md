> Retained-content interpretation: use the canonical `phase-2d-method.md` and its topic-local claim register for the selected framework and reporting period. Earlier PASS/source-verified/source-depth-PARTIAL labels are historical assessments; evidence tier is defined only by the claim register. Source access is not a substantive completion gate.

# Practice — Revenue Contract Assessment

## Controls
Contract-completeness reconciliation between CRM/CPQ, contract repository, billing and ERP; nonstandard-term approval; accounting review trigger for new products/contract templates; side-letter certification; contract-modification trigger; performance-obligation master review; periodic sample of standard contracts; framework/version review.

## Audit evidence
Executed contracts/amendments; legal enforceability support where judgmental; sales/product materials showing promises; pricing/SSP data; collectibility evidence; contract-combination analysis; accounting memo; system population reconciliation; approval trail. [TOPIC-03-001-IFRS-R042] [TOPIC-03-001-US-R042] [TOPIC-03-001-UK-R042] [TOPIC-03-001-AASB-R042] [TOPIC-03-001-IFRS-R002] [TOPIC-03-001-US-R002] [TOPIC-03-001-UK-R002] [TOPIC-03-001-AASB-R002] [TOPIC-03-001-IFRS-R006] [TOPIC-03-001-US-R006] [TOPIC-03-001-UK-R006] [TOPIC-03-001-AASB-R006]

## Systems/data
Canonical contract ID linking CRM, CLM, billing and ERP. Store customer/entity, execution/commencement dates, product/SKU, contract version, modification lineage, payment terms, promise IDs, performance-obligation IDs, accounting review status and evidence links. [TOPIC-03-001-IFRS-R002] [TOPIC-03-001-US-R002] [TOPIC-03-001-UK-R002] [TOPIC-03-001-AASB-R002]

## Common failures
Accounting from invoice rather than contract; missing side letters; assuming all SKUs are separate performance obligations; ignoring implicit promises; treating cash receipt as proof revenue exists; failing to combine linked contracts; applying IFRS/ASC logic to pre-2026 FRS 102; ignoring scope interactions such as leases. [TOPIC-03-001-IFRS-R005] [TOPIC-03-001-US-R005] [TOPIC-03-001-UK-R005] [TOPIC-03-001-AASB-R005] [TOPIC-03-001-IFRS-R006] [TOPIC-03-001-US-R006] [TOPIC-03-001-UK-R006] [TOPIC-03-001-AASB-R006] [TOPIC-03-001-IFRS-R007] [TOPIC-03-001-US-R007] [TOPIC-03-001-UK-R007] [TOPIC-03-001-AASB-R007] [TOPIC-03-001-IFRS-R001] [TOPIC-03-001-US-R001] [TOPIC-03-001-UK-R001] [TOPIC-03-001-AASB-R001] [TOPIC-03-001-UK-R016] [TOPIC-03-001-UK-R017]

## TrackedFR
Strong fit for recurring completeness/reconciliation between CRM/CLM, billing, ERP and warehouse data feeding revenue accounting. Not recommended merely for writing a technical revenue memo.

## Scenario tests — executed
1. SaaS subscription + implementation: PASS — inventory promises; do not assume setup is distinct. [TOPIC-03-001-IFRS-R008] [TOPIC-03-001-US-R008] [TOPIC-03-001-UK-R008] [TOPIC-03-001-AASB-R008]
2. Two contracts negotiated together with cross-dependent pricing: PASS — contract-combination test before allocation. [TOPIC-03-001-IFRS-R042] [TOPIC-03-001-US-R042] [TOPIC-03-001-UK-R042] [TOPIC-03-001-AASB-R042] [TOPIC-03-001-IFRS-R006] [TOPIC-03-001-US-R006] [TOPIC-03-001-UK-R006] [TOPIC-03-001-AASB-R006]
3. Cash deposit where contract criteria not met: PASS — liability/reassessment route, not automatic revenue. [TOPIC-03-001-IFRS-R002] [TOPIC-03-001-US-R002] [TOPIC-03-001-UK-R002] [TOPIC-03-001-AASB-R002] [TOPIC-03-001-IFRS-R005] [TOPIC-03-001-US-R005] [TOPIC-03-001-UK-R005] [TOPIC-03-001-AASB-R005]
4. Warranty + product: PASS — distinguish assurance/service-type warranty and route accordingly. [TOPIC-03-001-IFRS-R010] [TOPIC-03-001-US-R010] [TOPIC-03-001-UK-R010] [TOPIC-03-001-AASB-R010]
5. Stand-ready support with monthly services: PASS — evaluate series/performance-obligation model. [TOPIC-03-001-IFRS-R009] [TOPIC-03-001-US-R009] [TOPIC-03-001-UK-R009] [TOPIC-03-001-AASB-R009]
6. Marketplace contract involving third party: PASS — scope/promises established, then route principal-agent. [TOPIC-03-001-IFRS-R001] [TOPIC-03-001-US-R001] [TOPIC-03-001-UK-R001] [TOPIC-03-001-AASB-R001]
7. UK period beginning Jan 2026: PASS — revised Section 23 five-step model and UK simplifications. [TOPIC-03-001-UK-R017]
8. UK pre-2026 period: PASS — effective-period gate prevents revised Section 23 from being silently applied. [TOPIC-03-001-UK-R016] [TOPIC-03-001-UK-R017]
9. Australian NFP arrangement: PASS — request entity/NFP context before inheriting for-profit IFRS result. [TOPIC-03-001-AASB-R022]
10. US contract with share-based customer consideration: PASS — route current Topic 606 amendment/effective-date analysis rather than stale model. [TOPIC-03-001-US-R015]

Result: 10/10 routing scenarios pass. ASC 606 paragraph-depth remains PARTIAL, recorded rather than fabricated.
