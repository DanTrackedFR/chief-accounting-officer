"""Shared guarded arithmetic and approved-topic retrieval for Phase 3 skills."""
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

CENT=Decimal("0.01")
FRAMEWORKS={"IFRS","US_GAAP","UK_GAAP","AASB"}

class ReviewRequired(ValueError): pass

def dec(value):
    if isinstance(value,(float,bool)): raise ReviewRequired("Use decimal strings, not binary floats or booleans")
    try:
        result=Decimal(str(value))
        if not result.is_finite(): raise ReviewRequired("Non-finite decimal input")
        return result
    except Exception as exc: raise ReviewRequired("Invalid decimal input") from exc

def cash(value): return dec(value).quantize(CENT,rounding=ROUND_HALF_UP)

def required(case,*keys):
    missing=[k for k in keys if case.get(k) in (None,"")]
    if missing: raise ReviewRequired("Missing required facts: "+", ".join(missing))

def context(case):
    required(case,"case_id","framework","reporting_period","entity","jurisdiction")
    if case["framework"] not in FRAMEWORKS: raise ReviewRequired("Unsupported framework")
    if case["framework"]=="UK_GAAP": required(case,"uk_standard","uk_standard_edition")
    if case["framework"]=="AASB": required(case,"aasb_compilation","reporting_tier")
    if case["framework"]=="US_GAAP": required(case,"us_entity_type")
    return case

def approved_claims(topic_ids,framework,root=None):
    root=Path(root) if root else Path(__file__).resolve().parents[1]
    manifest=json.loads((root/"knowledge/phase-2d-topic-manifest.json").read_text())
    # Manifest format is validated by the repository's existing approval validator.
    entries=manifest if isinstance(manifest,list) else manifest.get("topics",[])
    output=[]
    for tid in topic_ids:
        match=[x for x in entries if x.get("topic_id")==tid]
        if len(match)!=1 or match[0].get("status")!="APPROVED":
            raise ReviewRequired("Canonical topic not approved: "+tid)
        paths=[root/p for p in match[0].get("artifact_paths",[]) if p.endswith("/standards-claims.json")]
        if len(paths)!=1 or not paths[0].is_file(): raise ReviewRequired("Missing canonical claim path for "+tid)
        claims=json.loads(paths[0].read_text())["claims"]
        accepted=[x for x in claims if x.get("framework")==framework and x.get("approval_review",{}).get("result")=="PASS"]
        if not accepted: raise ReviewRequired("No approved "+framework+" claims for "+tid)
        output.extend({"topic_id":tid,"claim_id":c["claim_id"],"proposition":c["proposition"],
                       "references":c.get("paragraph_references",[]),"reference_confidence":c.get("reference_confidence"),
                       "evidence_status":c.get("evidence_status"),"limitations":c.get("limitations",[]),"effective_period":c.get("effective_period"),
                       "entity_scope":c.get("entity_scope"),"audit_required":c.get("audit_required")}
                      for c in accepted)
    return output

def balance(lines):
    if any(x.get("side") not in ("Dr","Cr") or not x.get("account") or dec(x["amount"])<0 for x in lines):
        raise ReviewRequired("Journal requires valid sides/accounts and nonnegative amounts")
    dr=sum((dec(x["amount"]) for x in lines if x["side"]=="Dr"),Decimal(0))
    cr=sum((dec(x["amount"]) for x in lines if x["side"]=="Cr"),Decimal(0))
    if cash(dr)!=cash(cr): raise ReviewRequired(f"Journal does not balance: {dr} vs {cr}")
    return True

def journal(*rows):
    lines=[{"side":side,"account":account,"amount":cash(amount)} for side,account,amount in rows if cash(amount)!=0]
    balance(lines)
    return lines

def envelope(skill,case,method,calcs,journals,judgments,limitations,claims):
    return {"skill_id":skill,"status":"partial","framework":case["framework"],"jurisdiction":case["jurisdiction"],
            "entities":[case["entity"]],"periods":[case["reporting_period"]],"method":method,
            "calculations":calcs,"journal_entry_implications":journals,"judgments":judgments,
            "uncertainties":limitations,"evidence":claims,"open_items":["Independent accounting review and sign-off required"],
            "confidence":"medium","controls_impacted":["Reconcile source inputs, schedule, journals and ledger"],
            "disclosures_impacted":["Apply the framework-specific disclosure checklist"],
            "audit_evidence_required":["Source facts, policy/elections, assumptions, calculation and reviewer approval"]}
