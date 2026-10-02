import importlib.util,sys,unittest
from pathlib import Path
SKILLS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SKILLS))
from core_accounting import ReviewRequired,approved_claims,balance
def load(name):
 p=SKILLS/name/"engine.py"; spec=importlib.util.spec_from_file_location(name.replace("-","_")+"_engine",p)
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
rev=load("revenue-recognition");ecl=load("financial-instruments-ecl")
prov=load("provisions-contingencies");cons=load("consolidation")
def base():
 return {"case_id":"synthetic","framework":"IFRS","reporting_period":"2026-12-31","entity":"Example Ltd","jurisdiction":"NL"}
class FourSkillTests(unittest.TestCase):
 def test_revenue_allocation(self):
  self.assertEqual([x["allocation"] for x in rev.allocate("100",[{"id":"A","ssp":"60"},{"id":"B","ssp":"40"}])],[60,40])
 def test_revenue_run(self):
  c=base();c.update(contract_gate_approved=True,transaction_price="100",recognition_period="2026",obligations=[
   {"id":"A","ssp":"60","satisfaction_fraction":"1","satisfaction_evidence":"signed delivery"},
   {"id":"B","ssp":"40","satisfaction_fraction":"0.5","satisfaction_evidence":"certified progress"}])
  r=rev.run(c,[]);self.assertEqual(r["calculations"]["recognized"],80)
  for j in r["journal_entry_implications"]:self.assertTrue(balance(j))
 def test_revenue_unresolved_blocks(self):
  c=base();c.update(contract_gate_approved=True,transaction_price="100",recognition_period="2026",obligations=[],variable_consideration_unresolved=True)
  with self.assertRaises(ReviewRequired):rev.run(c,[])
 def test_ecl_weighted_and_reversal(self):
  c=base();c.update(model="IFRS_9_SIMPLIFIED_LIFETIME",instrument_scope_approved=True,exposure="1000",
   existing_allowance="100",scenarios=[{"weight":"0.75","pd":"0.10","lgd":"0.50","discount_factor":"1"},
   {"weight":"0.25","pd":"0.20","lgd":"0.50","discount_factor":"1"}])
  r=ecl.run(c,[]);self.assertEqual(r["calculations"]["expected_credit_loss"],62.5)
  self.assertEqual(r["calculations"]["allowance_movement"],-37.5)
 def test_ecl_us_staging_rejected(self):
  c=base();c.update(framework="US_GAAP",us_entity_type="public",model="IFRS_9_STAGE_1_12M",instrument_scope_approved=True,
   exposure="100",existing_allowance="0",scenarios=[{"weight":"1","pd":"0.1","lgd":"1","discount_factor":"1"}])
  with self.assertRaises(ReviewRequired):ecl.run(c,[])
 def test_provision_expected_value(self):
  c=base();c.update(present_obligation=True,past_event=True,recognition_approved=True,measurement_basis="EXPECTED_VALUE",
   existing_provision="0",outcomes=[{"amount":"100","probability":"0.6"},{"amount":"200","probability":"0.4"}])
  r=prov.run(c,[]);self.assertEqual(r["calculations"]["provision"],140)
 def test_provision_us_discount_gate(self):
  c=base();c.update(framework="US_GAAP",us_entity_type="public",present_obligation=True,past_event=True,
   recognition_approved=True,measurement_basis="ASC_450_APPROVED",asc_450_range_memo="reviewed",
   existing_provision="0",outcomes=[{"amount":"100"}],discount_factor="0.9")
  with self.assertRaises(ReviewRequired):prov.run(c,[])
 def test_consolidation_matched_elimination(self):
  c=base();c.update(control_assessment_approved=True,aligned_policies=True,aligned_reporting_dates=True,
   entities=[{"id":"P","in_scope":True,"balances":{"intercompany receivable":"100","cash":"200"}},
             {"id":"S","in_scope":True,"balances":{"intercompany payable":"-100","cash":"50"}}],
   intercompany_pairs=[{"receivable_entity":"P","payable_entity":"S","receivable_account":"intercompany receivable",
                       "payable_account":"intercompany payable","amount":"100","matched":True}])
  r=cons.run(c,[]);self.assertEqual(r["calculations"]["consolidated_balances"]["cash"],250)
  self.assertEqual(r["calculations"]["consolidated_balances"]["intercompany receivable"],0)
 def test_consolidation_unmatched_blocks(self):
  c=base();c.update(control_assessment_approved=True,aligned_policies=True,aligned_reporting_dates=True,
   entities=[],intercompany_pairs=[{"receivable_entity":"P","payable_entity":"S","receivable_account":"AR",
                                     "payable_account":"AP","amount":"100","matched":False}])
  with self.assertRaises(ReviewRequired):cons.run(c,[])
 def test_canonical_approved_retrieval(self):
  claims=approved_claims(["TOPIC-03-001"],"IFRS")
  self.assertTrue(claims);self.assertTrue(all(x["evidence_status"] for x in claims))
if __name__=="__main__":unittest.main()
