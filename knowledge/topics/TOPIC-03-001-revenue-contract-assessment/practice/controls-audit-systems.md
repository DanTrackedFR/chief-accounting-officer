# Practice — Revenue Contract Assessment

## Controls
Contract-completeness reconciliation between CRM/CPQ, contract repository, billing and ERP; nonstandard-term approval; accounting review trigger for new products/contract templates; side-letter certification; contract-modification trigger; performance-obligation master review; periodic sample of standard contracts; framework/version review.

## Audit evidence
Executed contracts/amendments; legal enforceability support where judgmental; sales/product materials showing promises; pricing/SSP data; collectibility evidence; contract-combination analysis; accounting memo; system population reconciliation; approval trail.

## Systems/data
Canonical contract ID linking CRM, CLM, billing and ERP. Store customer/entity, execution/commencement dates, product/SKU, contract version, modification lineage, payment terms, promise IDs, performance-obligation IDs, accounting review status and evidence links.

## Common failures
Accounting from invoice rather than contract; missing side letters; assuming all SKUs are separate performance obligations; ignoring implicit promises; treating cash receipt as proof revenue exists; failing to combine linked contracts; applying IFRS/ASC logic to pre-2026 FRS 102; ignoring scope interactions such as leases.

## TrackedFR
Strong fit for recurring completeness/reconciliation between CRM/CLM, billing, ERP and warehouse data feeding revenue accounting. Not recommended merely for writing a technical revenue memo.

## Scenario tests — executed
1. SaaS subscription + implementation: PASS — inventory promises; do not assume setup is distinct.
2. Two contracts negotiated together with cross-dependent pricing: PASS — contract-combination test before allocation.
3. Cash deposit where contract criteria not met: PASS — liability/reassessment route, not automatic revenue.
4. Warranty + product: PASS — distinguish assurance/service-type warranty and route accordingly.
5. Stand-ready support with monthly services: PASS — evaluate series/performance-obligation model.
6. Marketplace contract involving third party: PASS — scope/promises established, then route principal-agent.
7. UK period beginning Jan 2026: PASS — revised Section 23 five-step model and UK simplifications.
8. UK pre-2026 period: PASS — effective-period gate prevents revised Section 23 from being silently applied.
9. Australian NFP arrangement: PASS — request entity/NFP context before inheriting for-profit IFRS result.
10. US contract with share-based customer consideration: PASS — route current Topic 606 amendment/effective-date analysis rather than stale model.

Result: 10/10 routing scenarios pass. ASC 606 paragraph-depth remains PARTIAL, recorded rather than fabricated.
