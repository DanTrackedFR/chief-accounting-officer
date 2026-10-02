"""Fail-closed supplemental income-tax claim retrieval; never changes canonical topic IDs."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FRAMEWORKS = {"IFRS", "US_GAAP", "UK_GAAP", "AASB"}
PUBLIC_FIELDS = ("claim_id", "framework", "proposition", "paragraph_references",
                 "effective_period", "entity_scope", "limitations")

def load_register(path=None):
    data = json.loads(Path(path or HERE / "standards-claims.json").read_text())
    if data.get("namespace") != "SUPPLEMENTAL_TAX":
        raise ValueError("Unrecognized supplemental tax namespace")
    claims = data.get("claims", [])
    ids = [c.get("claim_id") for c in claims]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate supplemental tax claim")
    return data

def retrieve(framework, period, entity_scope, path=None):
    if framework not in FRAMEWORKS or not period or not entity_scope:
        raise ValueError("Framework, period and entity scope required")
    data = load_register(path)
    if data.get("status") != "APPROVED":
        raise ValueError("Supplemental tax knowledge is not approved")
    eligible = []
    for c in data["claims"]:
        if c["framework"] != framework:
            continue
        a = c.get("approval_review") or {}
        if (c.get("approval_track") not in ("TRAINING_DATA_CHECKED", "DIRECT_SOURCE_CHECKED")
            or a.get("result") != "PASS" or not all(a.get(k) is True for k in
            ("scope_and_period_checked", "cross_framework_checked", "regression_checked"))):
            raise ValueError("Incomplete tax claim approval: " + c["claim_id"])
        if c.get("audit_required") and c.get("evidence_status") == "SOURCE_VERIFIED":
            raise ValueError("Inconsistent claim assurance")
        eligible.append({k: c[k] for k in PUBLIC_FIELDS if k in c})
    if not eligible:
        raise ValueError("No approved applicable tax claims")
    return eligible
