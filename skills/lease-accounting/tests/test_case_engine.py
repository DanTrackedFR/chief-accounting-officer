import sys, unittest
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(HERE))
from case_engine import run_case, CaseError
from public_adapter import to_public_answer
from retrieval import retrieve_claims

def base(framework="IFRS"):
 return {"case_id":"L-001","framework":framework,"period_start":"2026-01-01","entity":"Example Co",
 "jurisdiction":"NL","commencement_date":"2026-01-01","contract_contains_lease":True,
 "payments":["100000"]*5,"periodic_rate":"0.05","lease_periods":5}

class CaseEngineTests(unittest.TestCase):
 def test_ifrs_end_to_end(self):
  r=run_case(base()); self.assertEqual(str(r["initial_measurement"]["lease_liability"]),"432947.67")
  self.assertLessEqual(abs(r["liability_schedule"][-1]["closing"]),0.02)
  self.assertLessEqual(abs(r["rou_schedule"][-1]["closing"]),0.02)
  self.assertTrue(any("IFRS 16.22" in c["locator"] for c in r["citations"]))
  public=to_public_answer(r); self.assertNotIn("journal_entries",public); self.assertEqual(public["framework"],"IFRS")
 def test_us_finance(self):
  c=base("US_GAAP"); c["classification"]="finance"; r=run_case(c)
  self.assertIn("pinpoint paragraph",r["limitations"][0])
 def test_us_operating_single_cost(self):
  c=base("US_GAAP"); c["classification"]="operating"; r=run_case(c)
  self.assertEqual(r["rou_schedule"][0]["lease_cost"],100000)
  self.assertEqual(r["rou_schedule"][-1]["closing"],0)
 def test_uk_period_gate(self):
  c=base("UK_GAAP"); c["period_start"]="2025-01-01"
  with self.assertRaises(CaseError): run_case(c)
 def test_aasb_overlay_required(self):
  with self.assertRaises(CaseError): run_case(base("AASB"))
  c=base("AASB"); c.update(entity_type="for-profit",reporting_tier="Tier 1"); self.assertEqual(run_case(c)["status"],"complete")
 def test_sale_leaseback_routes_out(self):
  c=base(); c["sale_and_leaseback"]=True
  with self.assertRaises(CaseError): run_case(c)
 def test_claim_retrieval_is_approved(self):
  claims=retrieve_claims(["TOPIC-04-007","TOPIC-04-009"],"IFRS")
  self.assertTrue(claims); self.assertTrue(any(x["paragraph_references"] for x in claims))
if __name__=="__main__": unittest.main()
