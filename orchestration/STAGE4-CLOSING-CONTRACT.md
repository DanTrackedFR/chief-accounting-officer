# Reviewed closing-date accounting contract — inspected before implementation

Starting live PR #37 head: `99d15a5c711cd7bd3e0f0f7099ad0f002a856901`.
This is controlled synthetic evidence, not a real treasury feed or authenticated review.

The unchanged production `skills/intercompany-accounting/workflow.py` requires
opening_a/b, separately evidenced opening_book_a/b, book_a/b reconciled to
settlement/recharge, closing rate_a/b, rate_evidence, confirmed_a/b and gl_a/b.
It calculates remaining foreign principal times the supplied closing functional
quote, agrees the independently supplied closing GL, and produces the difference
from pre-remeasurement books as entity-owned FX journals. Changing only opening
books cannot change closing carrying. No orchestration target amount is valid.

`skills/foreign-currency/workflow.py` supports monetary transaction items with
foreign_amount, initial/opening/closing rates, dated settlements and monetary
classification. In this graph Intercompany already owns legal remeasurement;
Foreign Currency therefore uses items=[] and the separately reviewed balanced
operation TB. Exact legal carrying and native FX profit dependencies bind signed
rows. The translation contract separately supports closing presentation quote,
historical equity, profit quote and independently reconciled net-assets/CTA.
It must not duplicate the legal remeasurement journal.

`orchestration/stage3.py` ORDINARY_IC_REASSESSMENT preserves the original USD
commercial principal and exact current translated legal side/metric/sign. The
reviewed reporting-basis pre-reassessment books and rates are supplied native
inputs. For a coherent treasury feed, both sides use the same USD-to-EUR quote;
the production owner checks those books against its calculation and emits no
second legal FX journal. This is not generic framework conversion.

`skills/consolidation/methods.md` and workflow/engine require actual reciprocal
source balances and complete entity TBs. They offer no generic asymmetric
ordinary-loan residual plug. Stage2 immutable versions and existing Stage3 exact
receipts remain the only version/invalidation/transformation architecture.

## Controlled new evidence

A separately supplied treasury close sheet dated 2026-10-31 records GBP per USD
0.90, EUR per USD0.90 and EUR per GBP1.00. The original UK0.80 is retained as an
obsolete 2026-09-30 quote used by the original export; original native results
are valid historical executions of that flawed source, not rewritten facts.
An independently supplied UK closing GL is GBP18 against unchanged USD20,
opening GBP16 and cash100/capital116. The native owner must calculate GBP18,
FXgain2; translation must consume that gain exactly once. These expected values
are review assertions, not inputs to orchestration accounting. The original
USD20 payable and reviewed EUR0.90/USD translation remain unchanged.

The same-day quote triangle is a review consistency check, not a rate solver.
A separately reviewed alternate GBP/USD0.85 with its own GL17 must produce
native17/gain1 and retain EUR17/EUR18 residual; it cannot be forced to close.
Neither quote is selected by a residual-dependent algorithm. No methodology,
owner workflow or original conflict source is changed.
