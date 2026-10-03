# Phase 3 batches 43–47 — independent accounting QA

Result: **PASS for the bounded management workpaper routes examined**, after corrective reruns on 2026-10-03. This review is separate from implementation-author tests and is not an IPO, audit, policy-authority, disclosure-compliance or FP&A conclusion.

The independent reviewer first read AGENTS.md, artifact and knowledge architecture, canonical topic documents, claim registers, individual Phase 2E reviews, approval/source-note policies and the existing runtime/reviewer/public boundary. The frozen map was established before implementation at commit `4a72c713a62f6df55ecda90d71facec44273aa91`, from live main `5a011a7b4195307743bddb768a13de638ccb8f7b`. All selected knowledge hashes were independently recalculated and matched the frozen map. All thirteen inspected canonical topics were APPROVED; empty registers remained practice and auditor OTHER claims retained their auditor meaning. Historical document status labels did not override canonical approval or remove source/period limitations. No new standards research or knowledge promotion occurred.

## Supported conclusions

| Batch | Examined executable support | Excluded conclusions |
|---|---|---|
| 43 | Nine unique accounting-function diagnostic areas, evidenced gaps/remediation, owner and dependency tracking | IPO score, arbitrary benchmarks, timing/success, SEC status, filing or legal eligibility |
| 44 | Management request/population/book reconciliation, original auditor-selected samples, query support, retained evidence exceptions | Audit opinion, sufficiency, independence, confirmation control, adjustments or substituted samples |
| 45 | Actual accounting owner memo/policy facts, complete claim trace, current policy version, retained supersession, implementation/exception governance | Autonomous recognition/policy selection, fabricated authority/citations, misclassified estimate/error as policy change |
| 46 | Independently supplied current requirement/topic population, owner applicability, note/statement facts and unchanged issued comparatives | Universal checklist, invented/unowned requirements, substantive comparative changes, filing or compliance certification |
| 47 | Controlled posted accounting sources, management/statutory bridge, prior-calendar flux facts and due/completion KPI | Forecasts/budgets, investment/commercial advice, generic BI, manufactured explanations, unsupported adjustments or GL correction |

## Executed independent challenges and corrections

The initial and fresh challenges were executed against actual production integration and workflow code, with synthetic release/outer approvals refreshed when necessary to isolate semantic failures. Fifteen invalid cases initially reached COMPLETE, and one genuine missing-evidence case was incorrectly blocked. The following corrections were independently rerun successfully:

| Challenge | Initial failure | Corrected behavior |
|---|---|---|
| Duplicate readiness area under a new row ID | Ten rows reported for nine areas | Exactly nine unique areas required |
| Changed tracker owner / contradictory independent PBC amount | Original source facts ignored | Frozen owner and amount reconciled |
| PBC evidence cloned under aliased document IDs | Physical records and gross amounts counted twice | Physical accounting record identity counted once |
| Selected unavailable sample with no support document | Genuine evidence gap blocked before useful workpaper | Original selection retained and workpaper PARTIAL; available support remains strict |
| Memo citations removed | Authority trace lost despite owner evidence | All actual applied owner claims traced exactly once |
| Profit amount relabelled as cash | Equal amounts substituted for semantic linkage | Metric binds actual owner result path |
| KPI completion before accounting cycle / due date after execution | False on-time denominator accepted | Actual event chronology bounded by accounting cycle and execution |
| Disclosure owner replaced by analytics governance output | Governance output treated as substantive accounting authority | Nonaccounting governance owners rejected for substantive accounting assertions |
| Readiness count used as cash bridge adjustment | Nine supported areas manufactured a monetary adjustment | Substantive adjustment owner required |
| Release review carried another entity | Contradictory release scope accepted | Exact source dimensions required |
| EUR document metadata with USD content | Currency contradiction ignored | Document/content/report currency reconciled |
| USD and EUR PBC requests aggregated into one gross total | Unlike currencies added without a unit | Unsupported multiple-currency aggregation rejected |
| Original policy-change flag downgraded in tracker | Accounting Changes owner gate bypassed | Source classification and owner semantics frozen |
| Error-correction owner relabelled as policy change | Package name substituted for actual owner classification | Actual completed policy-change classification required |

Further independent tests challenged equal-total source ID substitution, cancelled/reversed omissions, sample substitution, invented paragraph locators, memo contradictions, overlapping policy history, missing disclosure notes/topics, unsupported N/A, changed issued comparatives, unposted sources, unexplained movements, hidden gross offsets, posting modes and owner entity/framework/jurisdiction mismatches. Valid separately retained future policy versions, reviewed N/A without hidden output, zero movement and zero prior balances passed. Open gaps, unavailable samples, open review notes and material incomplete reconciliations remained PARTIAL. Zero prior balances produced an undefined percentage rather than invented growth.

## Validation and privacy

`python -m unittest discover -s skills/tests -p test_independent_governance.py -q`

Final result: **50 tests passed**, 5.08 seconds after the metadata refinement rerun. The positive test includes all twenty package/framework combinations across IFRS, US GAAP, FRS 102 UK GAAP and AASB. All produce no journals. Each positive output was inspected through all seven registered routes: answer context, answer, retrieval snippet, citation, tool output, user log and export. Approved practice did not create fake claims or citations. Raw reviewer records, owner fingerprints, source hashes and internal provenance were absent, while substantive limitations remained visible. Both named-source and training-data note contamination failed closed.

Independent stale-input tests covered source bytes/hash/snapshot, release payload, case approval, knowledge-review manifest, frozen actual knowledge bytes, implementation bytes and imported accounting owner output. Byte mutations were simulated with read mocks; canonical and implementation files were not edited. Stale implementation may yield PARTIAL for a direct workpaper or BLOCKED when an imported owner can no longer certify; neither reaches COMPLETE.

## Evidence and limitations

The test approvals are explicitly synthetic and are not authenticated human signoffs. Runtime controls validate supplied current review records, populations and bytes. They cannot independently establish source authenticity, external requirement completeness, legal facts, technical judgment quality or the competence of a person named in an approval. Those remain actual-case review responsibilities. APPROVED knowledge does not mean every operative authority was directly inspected; paragraph/effective-period limitations stay intact. This PASS is for the narrow supported workflows above, not the broader titles or unsupported entities, tiers, industries, methods and accounting assertions.

Only the independent test file and this QA report were authored by this reviewer. No implementation, canonical knowledge, blocked package, reserved item or artifact work was modified, and no commits were created. The parent integration reviewer remains responsible for full existing-production regression, candidate CI, final diff inspection and promotion.

## Metadata refinement review

After integration refined the five SKILL.md descriptions, triggers and related domains, the independent reviewer reread all five complete skill definitions and reran all fifty independent tests. The descriptions and triggers now identify accounting-function readiness tracking, management PBC/sample evidence, completed-owner policy/memo governance, qualified disclosure populations/tie-outs and reconciled controllership bridges/flux/KPIs. Related domains reflect actual approved-topic inputs and specialist handoffs. The bounded contracts remain explicit; no runtime scope or accounting authority was expanded. All five remain version 0.9.0, status review, pending candidate CI and promotion. Report anchors below were refreshed to the actual metadata-reviewed working-tree bytes.

## Reviewed working-tree hash anchors

These anchors identify bytes independently examined at this QA checkpoint. Later edits require rerunning the relevant controls and refreshing the review; this report does not certify future bytes.

| File | SHA-256 |
|---|---|
| `skills/ipo-accounting-readiness/workflow.py` | `7d0dcfde67a98d72ebd2e4a3dedaaab743851c282ec096be0f2c797a362fc481` |
| `skills/ipo-accounting-readiness/methods.md` | `e4a57ea57494a0576c0fb2c974d5ea497be2237dbe310aa1320c2dd930429269` |
| `skills/ipo-accounting-readiness/SKILL.md` | `923a5ab24e6f8d9c964fa6faefe18f6ee897eb887960e0a246d3eca410b659db` |
| `skills/audit-support-pbc/workflow.py` | `3f31e43036cbfe60ad11995bfe8e8e85f63f6c58a655ae2d102d1ffdf771f27d` |
| `skills/audit-support-pbc/methods.md` | `3d8c5cb305541b91fea372ac0e40270de7ec169831ff5951e9f31db49ecdc930` |
| `skills/audit-support-pbc/SKILL.md` | `af3d98a7bf8385c19b577c0119d3ae21d902c418d21b92a6ae5bbc605d131588` |
| `skills/accounting-policy-memo-governance/workflow.py` | `8788b3db21bdc242cd23873414ee8cf1befa7ef5ab98ce4ef2ffcf0537de985c` |
| `skills/accounting-policy-memo-governance/methods.md` | `7ab601016fb0837379dc45348c197c16dba75d241fe35199cfb691af248e72cd` |
| `skills/accounting-policy-memo-governance/SKILL.md` | `721243ad6c6554f9ce85eed48cd27a16c9c59c00874fb8ea3655c992fc009a5e` |
| `skills/disclosure-management/workflow.py` | `29feb6794f26db509e9915d118f327e339fe03469c2721ecb7edbcf8d8d6d16b` |
| `skills/disclosure-management/methods.md` | `dfbef400cc19d29613ccc3801482c2652701ed4ccb58336b3e3a66ee75793e41` |
| `skills/disclosure-management/SKILL.md` | `6f70e92788faa147d263461a93d9de54ba9421066d1fcf6c56beb5d35ff9fd81` |
| `skills/management-accounting-analytics/workflow.py` | `01c2f5d727c9fa6fb59f9951516c2f54de9f8a60a1bd04c229bd4dced994f27a` |
| `skills/management-accounting-analytics/methods.md` | `9b5f89d11707d41b31b00aa432389b20be9b5471e55a8f27d212e1a53be10f7d` |
| `skills/management-accounting-analytics/SKILL.md` | `b7d814dcd540ec3ab64e00aa9ae917722e820407002ebf29b3804278e3c8b561` |
| `skills/GOVERNANCE-KNOWLEDGE-MAP.json` | `2f3412690a71751f95074fdd7b6bd1f513747222dfbd3f3b6c3a4140f42eef10` |
| `skills/governance_accounting.py` | `397af36669c5dbdcaa7d52db7b1db4e35db3882d2b8f71dad8cdfac70a521029` |
| `skills/production.py` | `2815c507e13cb6e92fccb45a531ca3b72e3b982b493b7e2e6d388e7d0323c5e4` |
| `skills/REVIEWER-CONTROLS.md` | `fd4175811374d12396f577f6243d2272b5a4ff7562a659954b1b86a2732f6e13` |
| `interfaces/public_output.py` | `5df913e00294199abd7583324c0a077f7fcbf720c6cbd6c63a0c5d4e58f58357` |
| `skills/tests/governance_cases.py` | `31ac4e2c12179d2ecf1a54a0f30180f5ab53ffd893ad6e6c11b2dabee7ad901f` |
| `skills/tests/test_independent_governance.py` | `643176eec9697fb28fdc3ebe431b700959d96de4a10e75fdccd06af0cb3bcde6` |
