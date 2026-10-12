# Independent SaaS architecture diagnostics

Baseline inspected: main `2700b3dd7c8cb43c21ff874ef44bd0832e73b351`.
This is an independent architecture diagnostic, not acceptance of a completed
SaaS flagship. Five executable diagnostics reproduce existing boundaries:

```
python -m unittest orchestration.tests.test_saas_architecture_independent -v
```

## Findings derived from implementation

1. **AR foreign-currency population is outside the current owner contract.**
   `skills/accounts-receivable/workflow.py` rejects every invoice and receipt
   whose currency differs from functional currency. Its bridge is exactly
   opening + billed - credits - applied cash/deposits. There is no reviewed FX
   movement input. Adding an `fx_movement` key does not change the bridge. A
   remeasured closing GL fails reconciliation. The foreign invoice and GL
   movement tests reproduce both facts. This cannot be solved by changing the
   currency label on original evidence. A qualified functional-currency adapter
   must preserve original foreign amounts/rates and ownership, or the existing
   AR production contract needs a precisely reviewed extension.

2. **Revenue and AR overlap in invoice/receipt journal implications.**
   Both production workflows emit invoice recognition and receipts. Revenue
   also determines period revenue and contract-net balance; AR determines
   invoice/customer/receipt completeness and ageing. `CAO._journal_mapping`
   adds every completed owner's native journals. An account mapping changes
   account names but cannot designate one owner's journal as corroborating
   evidence for another owner's same economic event. The two-owner same-event
   reproducer ties a real 100 invoice to a 100 GL movement; additive mapping
   produces 200 and correctly rejects it. This is a runtime integration gap,
   not evidence that execution is impossible. A supported remedy would be a
   separately reviewed exact-payload economic-event ownership allocation,
   retaining all native implications while posting/counting each event once.
   Setting Revenue billings/receipts to zero without preserving its true
   contract bridge would be an invalid workaround.

3. **AR and ECL lack semantic fact adapters.**
   Baseline `FACT_ADAPTERS` has customer_contract, currency_exposure,
   reconciliation, close_calendar, statement, disclosure and analytics, but no
   family owned by AR or ECL. Intake validation imports this table. A general
   fact-family/owner-preparation extension is appropriate; this is not a
   fundamental blocker and does not require a parallel engine.

4. **Handoff and synthesis contracts are currently manufacturing-focused.**
   `_handoff` allows factory labour/depreciation/supplier, historical purchase,
   inventory, COGS and revenue. It has no AR, allowance, contract asset,
   contract liability, or monetary-FX reporting semantic. `_synthesis` exposes
   revenue, inventory/COGS and AP metrics. General reviewed bindings and
   explicit semantic sign/classification are needed for SaaS lineage.

5. **Analytics is a bounded account-balance comparison.**
   Its reviewed comparison basis is prior-year calendar balances. SaaS monthly
   cash/AR/deferred bridges and DSO require either clearly governed generic
   diagnostic artifacts outside accounting authority or a properly versioned
   existing Analytics contract expansion. A fixture alone cannot claim that
   current Analytics calculates those methods.

## Required acceptance attacks after remediation

Derived from the boundaries above: reject a mislabeled foreign invoice; a
remeasured AR amount lacking FX owner linkage; duplicate billing/receipt
journals disguised by different account names; omission of native owner
implications from review; changed downstream TB after exact review; a contract
asset folded into billed AR; different contracts netted in contract liability;
FX allocated to revenue growth without revenue-owner support; AR ageing due
dates changed to collection promises; stale or unsupported ECL rates; an open
reconciliation treated as completed by a close checklist; owner input/result
fingerprint changes after downstream qualification; monthly DSO silently
changing denominators or day conventions; an accounting correction described
as commercial growth; and a narrow AR/revenue inquiry acquiring the full close.

Existing gates must remain intact. These five tests intentionally assert
baseline deficiencies and are labelled diagnostic; green means reproduction,
not remediation or flagship completion. Replace them with positive regression
coverage when their specific boundaries are extended, retaining the adversarial
counterexamples. No production package, evidence gate or owner approval was
changed in this independent work.

## Final integration status

The historical gap assertions above have been replaced by current positive
semantic-family coverage and retained fail-closed boundary regressions. The final
independent acceptance review reconstructed and attacked the implementation:
46 distinct methods passed after four documented findings were remediated and
independently rerun. See `SAAS-ACCEPTANCE-INDEPENDENT-QA.md`.
