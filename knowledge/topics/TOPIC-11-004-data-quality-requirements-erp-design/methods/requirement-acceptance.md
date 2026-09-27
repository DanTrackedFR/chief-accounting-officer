# Data quality and ERP requirements — acceptance specification

Extends substantive README. Capabilities CAO-11-010–012. PRINCIPLES/PRACTICE; 2026-09-27.

Convert “accurate accruals” to testable requirements: complete source receipt/service population by entity and date; mandatory contract/rate/currency fields; approved account/entity mapping; cutoff rule; calculated amount and rounding; duplicate rejection; exception queue; qualified approval; reversal/settlement link; report/evidence and rollback. Define data owner, freshness, null/invalid limits, lineage and controls. Each requirement maps to policy/risk, field/config, test case and user acceptance evidence; a green configuration screen without accounting output is not acceptance.

Worked test: 100 receipts × 100 each = 10,000 expected uninvoiced receipts. ERP recognizes 98 / 9,800; two missing ID records total 200. Complete source-to-GL reconciliation fails despite 98% accuracy. Negative variant: valid 10,000 aggregate is posted entirely to wrong entity; dimension-level acceptance fails. Investigate whether missing field, cutoff, interface reject or rule defect, then retest from original source. Preserve requirement version, test dataset, expected result independent of build, actual logs and approval. Underlying expense/asset classification still follows the relevant framework topic.
