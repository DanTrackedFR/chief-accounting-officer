# Write-offs, recovery and cash application — completion method

Capabilities are preserved from the canonical README and the useful bad-debt retry folder; one topic is counted. Credit loss, commercial concession, legal debt release and a bank remittance match are different decisions. [TOPIC-03-009-IFRS-R001] [TOPIC-03-009-US-R001] [TOPIC-03-009-UK-R001] [TOPIC-03-009-AASB-R001]

## Recognition and measurement

IFRS/AASB writes off all or part of a financial asset when no reasonable expectation of recovery remains. [TOPIC-03-009-IFRS-R002] [TOPIC-03-009-AASB-R002]
US charges the uncollectible balance against the allowance when deemed uncollectible under the applicable loss policy. [TOPIC-03-009-US-R003]
UK Sections11/12 or FRS105 applies the valid receivable's impairment/derecognition method; an IFRS9 policy election instead uses its no-reasonable-recovery write-off route. [TOPIC-03-009-UK-R004]
Estimate the required allowance before charging a write-off; insufficient existing allowance does not justify hiding the excess in revenue. [TOPIC-03-009-IFRS-R005] [TOPIC-03-009-US-R005] [TOPIC-03-009-UK-R005] [TOPIC-03-009-AASB-R005]
Accounting write-off and cessation of legal enforcement are not necessarily the same event. [TOPIC-03-009-IFRS-R006] [TOPIC-03-009-US-R006] [TOPIC-03-009-UK-R006] [TOPIC-03-009-AASB-R006]
IFRS/AASB actual recoveries of written-off amounts are recognized through the credit-loss/recovery result, not new customer revenue. [TOPIC-03-009-IFRS-R007] [TOPIC-03-009-AASB-R007]
US recovery credits the allowance, followed by an independent reassessment of required closing losses; this must not leave an unsupported allowance. [TOPIC-03-009-US-R008]
UK recovery follows the selected loss model and reporting presentation; it is not revenue from selling the goods again. [TOPIC-03-009-UK-R009]
Apply customer cash to supported invoice rights and identify discounts, concessions, fees, FX and true residual debt separately; unexplained residuals do not automatically become write-offs. [TOPIC-03-009-IFRS-R010] [TOPIC-03-009-US-R010] [TOPIC-03-009-UK-R010] [TOPIC-03-009-AASB-R010]
Netting unrelated receivables/payables requires the framework's valid offsetting conditions; matching software alone cannot establish a legal right. [TOPIC-03-009-IFRS-R011] [TOPIC-03-009-US-R011] [TOPIC-03-009-UK-R011] [TOPIC-03-009-AASB-R011]
Material prior-period billing errors follow the error model rather than being disguised as current credit losses. [TOPIC-03-009-IFRS-R012] [TOPIC-03-009-US-R012] [TOPIC-03-009-UK-R012] [TOPIC-03-009-AASB-R012]

## Period, regime, presentation and disclosure

Select historical versus adopted IFRS9/AASB9 or CECL periods before deciding loss measurement; write-off against a properly measured allowance remains distinct from initial adoption equity adjustments. [TOPIC-03-009-IFRS-R013] [TOPIC-03-009-US-R013] [TOPIC-03-009-AASB-R013]
UK current FRS102 Sections11/12/eligible IAS39/IFRS9 choices, FRS101 adopted IFRS and FRS105 Section9 are separate routes; revised revenue adoption does not itself switch the receivable-loss model. [TOPIC-03-009-UK-R014]
Disclose material allowance write-offs/recoveries and the loss policy under the applicable instrument-note regime; IFRS/AASB Tier1, US public/nonpublic, UK regime and Australian Tier2 relief are independently assessed. [TOPIC-03-009-IFRS-R015] [TOPIC-03-009-US-R015] [TOPIC-03-009-UK-R015] [TOPIC-03-009-AASB-R015]
Accounting write-off does not by itself prove a deductible tax bad debt or remove applicable VAT/GST correction obligations. [TOPIC-03-009-IFRS-R016] [TOPIC-03-009-US-R016] [TOPIC-03-009-UK-R016] [TOPIC-03-009-AASB-R016]

## Workpaper WO-009 and opposite outcomes

Gross receivables280 comprise insolvent invoice80 plus remaining portfolio200; opening allowance70. With invoice80 now uncollectible, Dr loss10/Cr allowance10; Dr allowance80/Cr AR80. Gross remaining200, allowance0, loss10. Later recovery15: IFRS/AASB Dr cash15/Cr loss recovery15; US Dr cash15/Cr allowance15. An independently required closing portfolio allowance25 produces IFRS/AASB Dr loss25/Cr allowance25 and US Dr loss10/Cr allowance10. Both end at cash15+grossAR200−allowance25=190, versus opening net210: net loss20. The different recovery mechanics reconcile to the same economics without duplicating income. [TOPIC-03-009-IFRS-R005] [TOPIC-03-009-AASB-R005] [TOPIC-03-009-US-R005] [TOPIC-03-009-UK-R005] [TOPIC-03-009-IFRS-R007] [TOPIC-03-009-AASB-R007] [TOPIC-03-009-US-R008] [TOPIC-03-009-UK-R009]

A separate remittance50 against invoice60 leaves valid AR10: Dr cash50/Cr AR50. If correspondence proves an agreed price concession10, Dr revenue10/Cr AR10; if there is only payment delay, retain AR10 and assess losses. A bank fee2 deducted by the bank from a60 gross customer settlement instead yields Dr cash58/Dr bank-fee expense2/Cr AR60; do not reduce revenue2 or retain fictitious customer debt2. [TOPIC-03-009-IFRS-R010] [TOPIC-03-009-US-R010] [TOPIC-03-009-UK-R010] [TOPIC-03-009-AASB-R010]

WO-009 retains insolvency/legal collection evidence, partial-versus-full rationale, loss-model bridge, authorization, recovery remittance, tax/VAT separate assessment and invoice allocation. Controls reconcile allowance opening+charge−write-off+recoveries/remeasurement=closing, ensure recovery15 appears once, and require distinct write-off and cash-application approvals. Data keeps invoice/exposure_id after accounting write-off, writeoff_id, amount/date, legal-enforcement status, recovery_id, bank transaction, allocation_id and residual reason. Retry folder assertions link to the same canonical register; neither folder is silently discarded.
