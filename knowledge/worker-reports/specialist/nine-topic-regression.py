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
# TOPIC-04-011: independently derive the annuity and compare every published row.
from decimal import ROUND_HALF_UP
q = lambda value: value.quantize(D(".01"), rounding=ROUND_HALF_UP)
rate, term, initial = D(".05"), 5, D(400000)
fixed = initial * rate / (1 - (1 + rate) ** -term)
assert q(fixed) == D("92389.92")
assert abs(sum(fixed / (1 + rate) ** t for t in range(1, term + 1)) - initial) < D(".000001")
# Boundary: the rejected 100k payment cannot support the 400k inception PV.
assert q(sum(D(100000) / (1 + rate) ** t for t in range(1, term + 1))) == D("432947.67")
workpaper = (ROOT / "knowledge/topics/TOPIC-04-011-sale-leaseback/applied-qa.md").read_text()
fixed_text, variable_text = workpaper.split("## Variable-only leaseback:", 1)
rows = [line for line in fixed_text.splitlines() if line.startswith("| Year ")]
assert len(rows) == 5
balance, total_interest, total_cash, total_principal = initial, D(0), D(0), D(0)
for year, line in enumerate(rows, 1):
    interest = q(balance * rate)
    cash = q(fixed) if year < term else balance + interest
    principal = cash - interest
    closing = balance + interest - cash
    depreciation, accumulated = D(48000), D(48000) * year
    rou = D(240000) - accumulated
    expected = [balance, interest, cash, principal, closing, depreciation, accumulated, rou]
    published = [D(cell.strip().replace(",", "")) for cell in line.split("|")[2:-1]]
    assert published == expected, (year, published, expected)
    # Reconcile the journal-driven net liability movement to principal repayment.
    assert balance - closing == principal
    assert closing >= 0 and rou >= 0
    total_interest += interest; total_cash += cash; total_principal += principal
    balance = closing
assert balance == 0 and total_principal == initial
assert total_interest == D("61949.59") and total_cash == D("461949.59")
assert initial + total_interest - total_cash == 0
# Framework-specific initial journals: IFRS/AASB, UK proportionate/deferred, US operating.
for framework, rou, gain, deferred in [
    ("IFRS", D(240000), D(240000), D(0)),
    ("AASB", D(240000), D(240000), D(0)),
    ("UK proportionate", D(240000), D(240000), D(0)),
    ("UK deferred", D(400000), D(0), D(400000)),
    ("US operating", D(400000), D(400000), D(0)),
]:
    assert D(1000000) + rou == D(600000) + initial + gain + deferred, framework
assert D(1000000) == D(600000) + D(400000)  # separate US variable-only sale
# Preserve adverse route text and all six evidence-tier flags; no source promotion.
method = (ROOT / "knowledge/topics/TOPIC-04-011-sale-leaseback/phase-2d-method.md").read_text()
for boundary in ("finance", "repurchase", "off-market", "termination", "transition", "deferred"):
    assert boundary in method.lower()
claims = json.loads((ROOT / "knowledge/topics/TOPIC-04-011-sale-leaseback/standards-claims.json").read_text())["claims"]
assert len(claims) == 6 and all(c["audit_required"] for c in claims)
assert {c["framework"] for c in claims} == {"IFRS", "AASB", "UK_GAAP", "US_GAAP"}
assert sum(c["evidence_status"] == "PRIMARY_CORROBORATED" for c in claims) == 5
assert sum(c["evidence_status"] == "MODEL_DERIVED_AUDIT_REQUIRED" for c in claims) == 1
print("TOPIC-04-011 fixed: PV 400000; payment 92389.92; final 92389.91; interest 61949.59; liability/ROU zero")
assert D(400000) * D(".6") == D(240000)
p = D(400000) / (D(1) / D("1.05") + D(1) / D("1.05") ** 2)
closing1 = D(400000) * D("1.05") - p
closing2 = closing1 * D("1.05") - p
assert abs(closing2) < D(".001") and p.quantize(D(".01")) == D("215121.95")
assert D("240000") - q(p) == D("24878.05")
assert q(p) - D("190000") == D("25121.95")
variable_rows = [line for line in variable_text.splitlines() if line.startswith("| Year ")]
assert len(variable_rows) == 2
vb = initial
for year, line in enumerate(variable_rows, 1):
    vi = q(vb * rate); vp = q(p); vc = vb + vi - vp
    cells = [cell.strip() for cell in line.split("|")[2:-1]]
    assert [D(cell.replace(",", "")) for cell in cells[:5]] == [vb, vi, vp, vc, D(240000 if year == 1 else 190000)]
    assert D(cells[-1].replace(",", "")) == D(240000) - D(120000) * year
    vb = vc
assert vb == 0
assert (D(4000000) * D(".01") + D(1000000) * D(".05") +
        D(500000) * D(".20") + D(25000)) == D(215000)
assert D(215000) - D(170000) == D(45000)
assert D(16000000) / D(160000000) == D(".10")
assert D(160000000) * D(".11") - D(16000000) == D(1600000)
assert D(30000000) / D(32000000) == D(".9375")
assert max(D(125000), D(180000)) - (D(210000) - D(40000)) == D(10000)
print("PASS: nine claim registers, references, arithmetic and adverse thresholds")
