# Automated and management-review control — evidence chain

Extends substantive README. Capabilities CAO-09-007–009. PRINCIPLES/PRACTICE; 2026-09-27.

Automated match control: document PO/receipt/invoice matching rule, permitted tolerance, source fields, configuration version/effective date, change approvals, privileged users, rejected population and monitoring. Compare every source invoice to matched, held and rejected destinations; a control that silently drops records fails completeness. Management review control: define prepared expectation, materiality/precision, report filters, reconciliation to GL, anomaly follow-up, resolution and reviewer competence. A signed dashboard screenshot without report reliability, thresholds and challenged explanations is not enough.

Worked run: 1,000 invoices totaling 500,000 enter match; 950 totaling 470,000 pass, 40 totaling 25,000 are held, ten totaling 5,000 reject. The population reconciles in count and amount, but all 50 exceptions require owner/status and impact on AP cutoff; approved exceptions cannot be hidden by a successful 950. A change from 1% to 8% tolerance requires approved design assessment and versioned before/after tests. If the revised rule incorrectly accepts a 7% quantity overbill, expected outcome is rejection of change or compensating detection.

Evidence packet: approved config and change log, population extract, run ID, counts/amounts by entity, exception queue, reviewer expectation and follow-up, final GL bridge. Source boundaries: [SEC 33-8810](https://www.sec.gov/rule-release/33-8810) and [AS 2201](https://pcaobus.org/oversight/standards/auditing-standards/details/AS2201) checked 2026-09-27 for US context, not universal framework rules. Dependencies 09-002, 11-003/006, 12-001. Result PASS for explicit matched/held/rejected arithmetic and fail-stop design.

**Negative test:** system marks 950 matches as success but omits the ten rejected invoices from its exported control population. Expected FAIL until source-to-accepted/held/rejected count and amount agree.
