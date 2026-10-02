"""Fail-closed retrieval of approved lease knowledge from the repository tree."""
import json
from pathlib import Path

TOPICS={
 "TOPIC-04-007":"TOPIC-04-007-lease-identification-classification",
 "TOPIC-04-008":"TOPIC-04-008-lease-initial-subsequent-measurement",
 "TOPIC-04-009":"TOPIC-04-009-lease-discount-rate-modification-remeasurement",
 "TOPIC-04-010":"TOPIC-04-010-leases",
 "TOPIC-04-011":"TOPIC-04-011-sale-leaseback"}

def repo_root():
    return Path(__file__).resolve().parents[2]

def retrieve_claims(topic_ids, framework):
    root=repo_root(); out=[]
    for topic_id in topic_ids:
        if topic_id not in TOPICS: raise ValueError("Unregistered topic "+topic_id)
        p=root/"knowledge"/"topics"/TOPICS[topic_id]/"standards-claims.json"
        data=json.loads(p.read_text())
        for claim in data.get("claims",[]):
            if claim.get("framework")==framework and claim.get("approval_review",{}).get("result")=="PASS":
                out.append({"topic_id":topic_id,"claim_id":claim["claim_id"],"proposition":claim["proposition"],
                            "paragraph_references":claim.get("paragraph_references",[]),
                            "effective_period":claim.get("effective_period"),"limitations":claim.get("limitations",[])})
    if not out: raise ValueError("No approved claims retrieved for framework "+framework)
    return out
