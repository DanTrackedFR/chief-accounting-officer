#!/usr/bin/env python3
"""Validate canonical approval evidence separately from underlying source assurance."""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FINDINGS = ("scope_review", "period_and_scope_check", "cross_framework_check",
            "numerical_reperformance", "cross_topic_check")

def validate_topic(topic, register, review):
    errors = []
    def require(condition, message):
        if not condition:
            errors.append(message)
    tid = topic.get("topic_id")
    require(topic.get("status") == "APPROVED", "topic not APPROVED")
    require(register.get("topic_id") == tid == review.get("topic_id"), "topic IDs differ")
    require(review.get("baseline_status") == "REVIEWED", "missing substantive REVIEWED baseline")
    require(review.get("result") == "PASS" and review.get("blockers") == [], "unresolved topic review")
    require(bool(review.get("reviewer")) and bool(DATE.fullmatch(review.get("date", ""))), "missing reviewer/date")
    for field in FINDINGS:
        require(isinstance(review.get(field), str) and bool(review[field].strip()), "missing " + field)
    accuracy = review.get("accuracy_checks", [])
    require(bool(accuracy) and all(x.get("result") == "PASS" and x.get("challenge") for x in accuracy),
            "missing independent accuracy challenge")
    claims = register.get("claims", [])
    if not claims:
        require(review.get("claim_register_disposition") == "NON_NORMATIVE_SCOPE_REVIEW",
                "empty register without documented non-normative scope review")
    else:
        require(review.get("claim_register_disposition") == "MATERIAL_CLAIMS_REGISTERED",
                "incorrect register disposition")
    checks = review.get("claim_checks", [])
    require(len(checks) == len(claims), "claim review coverage mismatch")
    ids = [c.get("claim_id") for c in claims]
    require(len(set(ids)) == len(ids), "duplicate claim ID")
    require(set(ids) == {c.get("claim_id") for c in checks}, "claim checks differ from register")
    for claim in claims:
        cid = claim.get("claim_id", "<missing>")
        def ck(condition, message):
            require(condition, cid + ": " + message)
        check = next((c for c in checks if c.get("claim_id") == cid), {})
        track = claim.get("approval_track")
        ck(track in {"DIRECT_SOURCE_CHECKED", "TRAINING_DATA_CHECKED"}, "invalid track")
        ck(check.get("result") == "PASS" and check.get("approval_track", check.get("track")) == track,
           "claim check failed or track differs")
        ck(bool(check.get("challenge") or check.get("accuracy_check") or check.get("finding_refs")),
           "missing linked individual finding")
        ck(bool(claim.get("reviewer")) and bool(DATE.fullmatch(claim.get("review_date", ""))),
           "missing claim reviewer/date")
        for field in ("effective_period", "entity_scope"):
            ck(isinstance(claim.get(field), str) and bool(claim[field].strip()), "missing " + field)
        approval = claim.get("approval_review", {})
        ck(approval.get("result") == "PASS" and bool(approval.get("reviewer"))
           and bool(DATE.fullmatch(approval.get("date", ""))), "missing approval disposition")
        ck(all(approval.get(f) is True for f in ("scope_and_period_checked", "cross_framework_checked",
                                               "regression_checked")), "incomplete approval checks")
        status = claim.get("evidence_status")
        ck(status not in {"CONFLICTED", "NOT_RESEARCHED"}, "unresolved evidence")
        if track == "DIRECT_SOURCE_CHECKED":
            ck(status == "SOURCE_VERIFIED" and claim.get("reference_confidence") == "VERIFIED",
               "direct-source status not justified")
            sources = [s for s in claim.get("sources", []) if s.get("inspected") is True
                       and s.get("source_kind") in {"CURRENT_STANDARD", "REGULATOR"}]
            ck(any(s.get("url") and s.get("locator") for s in sources), "no inspected operative authority")
            ck(claim.get("source_note") in {"Source: " + s.get("title", "") for s in sources},
               "source note differs from operative source")
        else:
            ck(status != "SOURCE_VERIFIED" and claim.get("audit_required") is True,
               "training-data source assurance overstated")
            ck(claim.get("source_note") == "Source: ChatGPT training data", "missing training-data note")
            ck(bool(claim.get("limitations")), "missing authority limitation")
            ck(any(str(x.get("outcome", "")).startswith("PASS") and x.get("model") and x.get("date")
                   and not x.get("disagreements") for x in claim.get("model_reviews", [])),
               "missing recorded independent training-data disposition")
    return errors

def audit(root=ROOT):
    manifest = json.loads((root / "knowledge/phase-2d-topic-manifest.json").read_text())
    topics = manifest["topics"]
    errors, tracks, statuses = [], Counter(), Counter()
    registers, empty, claim_ids = set(), 0, set()
    if len(topics) != 157 or len({t["topic_id"] for t in topics}) != 157:
        errors.append("canonical population differs from 157 unique topics")
    capabilities = {c for t in topics for c in t["capability_ids"]}
    if len(capabilities) != 347:
        errors.append("canonical capability coverage differs from 347")
    for topic in topics:
        tid = topic["topic_id"]
        paths = [p for p in topic["artifact_paths"] if p.endswith("/standards-claims.json")]
        review_path = "knowledge/phase-2e/reviews/" + tid + ".json"
        if len(paths) != 1 or review_path not in topic.get("qa_evidence", []):
            errors.append(tid + ": missing canonical register or QA evidence"); continue
        registers.add(paths[0])
        try:
            register = json.loads((root / paths[0]).read_text())
            review = json.loads((root / review_path).read_text())
        except (OSError, ValueError) as exc:
            errors.append(tid + ": unreadable evidence: " + str(exc)); continue
        errors.extend(tid + ": " + e for e in validate_topic(topic, register, review))
        empty += not register["claims"]
        for claim in register["claims"]:
            cid = claim["claim_id"]
            if cid in claim_ids:
                errors.append(tid + ": globally duplicate claim " + cid)
            claim_ids.add(cid)
            tracks[claim.get("approval_track")] += 1
            statuses[claim.get("evidence_status")] += 1
    return {"topics": len(topics), "approved": sum(t["status"] == "APPROVED" for t in topics),
            "capabilities": len(capabilities), "canonical_registers": len(registers),
            "empty_registers_scope_reviewed": empty, "claims": len(claim_ids),
            "approval_tracks": dict(tracks), "evidence_statuses": dict(statuses),
            "errors": len(errors), "error_details": errors}

if __name__ == "__main__":
    result = audit()
    print(json.dumps(result, indent=2))
    sys.exit(bool(result["errors"]))
