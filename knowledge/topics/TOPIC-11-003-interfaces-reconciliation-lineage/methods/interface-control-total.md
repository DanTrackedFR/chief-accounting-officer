# Interface reconciliation and lineage — control total

Extends substantive README. Capabilities CAO-11-007–009. PRINCIPLES/PRACTICE; 2026-09-27.

At every hop retain source ID/grain, extraction query and timestamp, field/transformation map, run/config version, count, signed and absolute amount, accepted/rejected/deduplicated counts and destination IDs. Compare both directions: source records without destination and destination records without source. Idempotency is tested on retry; a timeout does not prove absence of a posting. If amounts transform by FX/tax/allocation, reconcile with a separately approved formula and rate version.

Example: billing source 1,000 transactions / 500,000. Payload 1,000/500,000; ERP accepts 995/496,000 and rejects 5/4,000; GL posted batch 995/496,000. Initial source-to-GL difference 4,000 is explained **but unresolved**; each rejected ID needs owner and disposition. A rerun cannot post the 995 twice. **Negative test:** reporting layer shows 500,000 after inserting a 4,000 manual row not traceable to source. Expected FAIL; remove unsupported row and resolve rejects through controlled original flow. Audit packet retains full bridge and versions. Underlying revenue policy remains Domain 03.
