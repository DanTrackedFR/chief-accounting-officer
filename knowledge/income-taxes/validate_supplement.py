#!/usr/bin/env python3
"""Supplemental namespace gate; intentionally separate from 157-topic validators."""
import json
import sys
from pathlib import Path
from retrieval import load_register, FRAMEWORKS

def validate(path=None):
    d = load_register(path)
    errors = []
    claims = d["claims"]
    for fw in FRAMEWORKS:
        if not any(c["framework"] == fw for c in claims):
            errors.append("Missing framework " + fw)
    for c in claims:
        cid = c["claim_id"]
        if c["framework"] not in FRAMEWORKS or not cid.startswith("TAX-" + c["framework"] + "-"):
            errors.append(cid + ": invalid framework/ID")
        if not c.get("proposition") or len(c["proposition"]) < 30:
            errors.append(cid + ": missing proposition")
        if c.get("evidence_status") == "SOURCE_VERIFIED":
            if not any(s.get("inspected") and s.get("source_kind") == "CURRENT_STANDARD"
                       and s.get("locator") for s in c.get("sources", [])):
                errors.append(cid + ": unsupported direct-source rating")
        if c.get("approval_track") == "PENDING" and c.get("approval_review") is not None:
            errors.append(cid + ": inconsistent pending review")
        if d["status"] == "APPROVED" and ((c.get("approval_review") or {}).get("result") != "PASS"
                                        or c.get("approval_track") == "PENDING"):
            errors.append(cid + ": missing independent approval")
    return {"claims":len(claims),"frameworks":sorted(FRAMEWORKS),
            "status":d["status"],"errors":errors}

if __name__ == "__main__":
    result = validate()
    print(json.dumps(result, indent=2))
    sys.exit(bool(result["errors"]))
