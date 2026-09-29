"""Phase 2D Specialist nine-topic structural and numerical challenge.

Run from the repository root: python knowledge/worker-reports/specialist/nine-topic-regression.py
This checks identifiers, evidence ringfencing and worked arithmetic; it does not
turn lower-tier standards evidence into authoritative verification.
"""
import json
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCHEMA = json.loads((ROOT / "knowledge/standards-evidence/claim.schema.json").read_text())
ITEM = SCHEMA["properties"]["claims"]["items"]
TOPICS = {
    "04-001": "ppe-recognition-capitalization",
    "04-002": "depreciation-disposals",
    "04-003": "cip-fa-reconciliation-capitalized-software",
    "04-004": "rd-software-cloud",
    "04-005": "intangible-assets",
    "04-006": "impairment-goodwill",
    "04-011": "sale-leaseback",
    "15-002": "policy-inventory-estimate-methodology",
    "16-006": "entity-regulatory-capital-interface",
}
STATUS = {"SOURCE_VERIFIED", "PRIMARY_CORROBORATED", "SECONDARY_CORROBORATED",
          "MODEL_DERIVED_AUDIT_REQUIRED", "CONFLICTED", "NOT_RESEARCHED"}
FRAMEWORK = {"IFRS", "US_GAAP", "UK_GAAP", "AASB", "SEC", "REGULATORY", "OTHER"}

all_ids = set()
for tid, suffix in TOPICS.items():
    topic = f"TOPIC-{tid}"
    folder = ROOT / "knowledge/topics" / f"{topic}-{suffix}"
    method = (folder / "phase-2d-method.md").read_text()
    register = json.loads((folder / "standards-claims.json").read_text())
    assert register["topic_id"] == topic
    ids = set()
    for claim in register["claims"]:
        cid = claim["claim_id"]
        assert cid.startswith(topic + "-") and cid not in all_ids and cid not in ids
        assert claim["framework"] in FRAMEWORK and claim["evidence_status"] in STATUS
        assert set(ITEM["required"]).issubset(claim) and set(claim).issubset(ITEM["properties"])
        assert claim["proposition"] and claim["sources"]
        assert isinstance(claim["audit_required"], bool)
        assert cid.removeprefix("TOPIC-") in method, cid
        assert claim["reference_confidence"] != "VERIFIED" or claim["evidence_status"] == "SOURCE_VERIFIED"
        if claim["evidence_status"] != "SOURCE_VERIFIED":
            assert claim["audit_required"]
        for source in claim["sources"]:
            assert source["title"] and source["source_kind"]
            assert set(SCHEMA["properties"]["claims"]["items"]["properties"]["sources"]["items"]["required"]).issubset(source)
            if source["source_kind"] == "MODEL_KNOWLEDGE":
                assert not source["inspected"]
        ids.add(cid)
    all_ids.update(ids)
    assert len(ids) >= 4 and any(word in method for word in ("Boundary", "Adverse", "Fail"))
    print(f"{topic}: {len(ids)} distinct annotated claims; method present")

# Reperform numeric scenarios and counterfactual outcomes, not merely file presence.
assert D(500000) + D(20000) + D(30000) == D(550000)
assert (D(600000) - D(60000)) / D(6) == D(90000)
opening_y3 = D(600000) - D(2) * D(90000)
year3 = (opening_y3 - D(60000)) / D(7)
assert (D(400000) - (opening_y3 - year3)).quantize(D(".01")) == D("31428.57")
assert D(200000) + D(120000) + D(80000) - D(300000) == D(100000)
assert D(100000) + D(250000) + D(50000) + D(100000) == D(500000)
assert D(600000) / D(6) * D(6) / D(12) == D(50000)
assert max(D("10.8"), D("11.0")) == D("11.0")
assert D("12.0") - D("11.0") == D("1.0")
assert D("12.0") > D("11.5") and D("12.0") - D("10.8") == D("1.2")
assert D("12.0") < D("12.1")  # US held-and-used recoverability countercase
assert D(1000000) - D(600000) == D(400000)
assert D(400000) * D(".6") == D(240000)
p = D(400000) / (D(1) / D("1.05") + D(1) / D("1.05") ** 2)
closing1 = D(400000) * D("1.05") - p
closing2 = closing1 * D("1.05") - p
assert abs(closing2) < D(".001") and p.quantize(D(".01")) == D("215121.95")
assert (D(4000000) * D(".01") + D(1000000) * D(".05") +
        D(500000) * D(".20") + D(25000)) == D(215000)
assert D(215000) - D(170000) == D(45000)
assert D(16000000) / D(160000000) == D(".10")
assert D(160000000) * D(".11") - D(16000000) == D(1600000)
assert D(30000000) / D(32000000) == D(".9375")
assert max(D(125000), D(180000)) - (D(210000) - D(40000)) == D(10000)
print("PASS: nine claim registers, references, arithmetic and adverse thresholds")
