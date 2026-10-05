"""Authored Treasury source-to-public acceptance and owner-bound regressions."""
import copy,json,unittest
from decimal import Decimal
from pathlib import Path
from orchestration.tests.treasury_fixtures import *
from orchestration.tests.generate_treasury_examples import artifacts
from orchestration.runtime import CAO
from orchestration.registry import production

class TreasuryAuthored(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.e,cls.p,cls.pack=flagship();cls.result=cls.e.execute(cls.p,cls.pack)
  cls.ce,cls.cp,cls.cpack=flagship(True);cls.clean=cls.ce.execute(cls.cp,cls.cpack)
 def test_primary_material_conflict_stays_documented(self):
  self.assertEqual(self.result.case.outcome,'partial');self.assertEqual(self.result.case.status,'DOCUMENTED');self.assertTrue(self.result.conflicts)
 def test_clean_control_closes(self):self.assertEqual((self.clean.case.outcome,self.clean.case.status),('complete','CLOSED'))
 def test_genuine_intake_has_source_inventory(self):self.assertEqual(len(self.result.inventory),18);self.assertGreater(len(self.result.candidates),60)
 def test_qualified_native_owners(self):self.assertTrue(all(n['status']=='complete' for n in self.clean.case.workplan_nodes))
 def test_expected_modes(self):self.assertEqual(self.clean.case.work_modes['primary'],'RECONCILIATION_INVESTIGATION');self.assertIn('DIAGNOSTIC_ANALYTICS',self.clean.case.work_modes['secondary'])
 def test_exact_once_principal_cash(self):
  js=self.clean.case.conclusions[0]['journals'];cash=sum(Decimal(l['amount'])*(1 if l['side']=='Dr' else -1) for j in js for l in j['lines'] if l['account']=='Cash');self.assertEqual(cash,-280)
 def test_witness_retained(self):self.assertTrue(any(e['witnesses'] for e in self.clean.case.journal_ownership_ledger))
 def test_source_bank_population_is_complete(self):self.assertEqual(len(self.cpack.populations),1);self.assertGreater(len(self.cpack.documents),15)
 def test_fx_is_not_interest(self):
  v=self.clean.case.conclusions[0]['calculations'];self.assertEqual(Decimal(v['debt_effective_interest']),80);self.assertEqual(Decimal(v['monetary_fx_profit']),-80)
 def test_governed_reporting_composition(self):
  v=self.clean.case.conclusions[0]['calculations'];self.assertEqual(Decimal(v['reported_debt']),880);self.assertEqual(Decimal(v['current_debt']),880);self.assertEqual(Decimal(v['noncurrent_debt']),0)
 def test_hedge_oci_is_not_cash(self):
  v=self.clean.case.conclusions[0]['calculations'];self.assertEqual(Decimal(v['hedge_oci']),36);self.assertEqual(Decimal(v['hedge_pnl']),4);self.assertEqual(Decimal(v['cash_financing']),-200)
 def test_hypothesis_rejected_with_evidence(self):self.assertEqual(self.clean.hypothesis_results[0]['disposition'],'REJECTED')
 def test_rate_bridge_residual_explicit(self):
  b=self.clean.case.diagnostics[0]['bridge'];self.assertEqual(Decimal(b['residual']),0);self.assertEqual(Decimal(b['change']),20)
 def test_memory_not_promoted(self):self.assertTrue(all(m['status']=='PROPOSED' for m in self.clean.case.memory_candidates))
 def test_unavailable_borrowing_costs_is_precise_open_owner(self):
  req=copy.deepcopy(self.cpack.request);req['facts']['qualifying_interest']={'project':{'asset':'qualifying construction'}};r=CAO().run(req);self.assertNotEqual(r.outcome,'complete');self.assertTrue(any(n['selected_skill']=='borrowing-costs' and n['status']=='blocked' for n in r.workplan_nodes))
 def test_normal_interest_excludes_borrowing_costs(self):self.assertNotIn('borrowing-costs',self.clean.case.skills_invoked)
 def test_no_irrelevant_financial_asset_or_fv_owner(self):self.assertNotIn('financial-instruments-ecl',self.clean.case.skills_invoked);self.assertNotIn('fair-value-measurement',self.clean.case.skills_invoked)
 def test_missing_debt_reporting_handoff_blocks_fs(self):
  req=copy.deepcopy(self.cpack.request);req['handoffs']=[r for r in req['handoffs'] if r['semantic']!='debt_base'];r=CAO().run(req);self.assertNotEqual(r.outcome,'complete')
 def test_wrong_reporting_semantic_target_rejects(self):
  req=copy.deepcopy(self.cpack.request);next(r for r in req['handoffs'] if r['semantic']=='interest_expense')['target_path']=['owner_support','current_debt'];self.assertNotEqual(CAO().run(req).outcome,'complete')
 def test_noncurrent_fx_cannot_be_guessed(self):
  req=copy.deepcopy(self.cpack.request);b=next(r for r in req['handoffs'] if r['semantic']=='debt_noncurrent');b['components']=[dict(producer='foreign-currency',metric_path=['monetary_fx_profit'],sign=-1)];self.assertNotEqual(CAO().run(req).outcome,'complete')
 def test_source_bytes_and_dimensions_require_review(self):
  req=copy.deepcopy(self.cpack);req.request['facts']['currency_exposure']['source_material']['fx']['metadata']['currency']='USD'
  with self.assertRaises(ValueError):self.ce.execute(copy.deepcopy(self.cp),req)
 def test_result_binding_cannot_use_equal_unrelated_metric(self):
  req=copy.deepcopy(self.cpack);i=next(i for i,b in enumerate(req.bindings) if b.fact_id=='debt-close');req.bindings[i]=Binding('debt-close','debt-financing',('debt',0,'principal'),'owner_result')
  with self.assertRaises(ValueError):self.ce.execute(copy.deepcopy(self.cp),req)
 def test_artifacts_match_saved(self):
  for name,value in artifacts().items():self.assertEqual(json.loads((Path(__file__).resolve().parents[1]/'examples/treasury-financing'/name).read_text()),json.loads(json.dumps(value,default=str)))
 def test_four_executable_lineages(self):self.assertEqual(len(artifacts()['end-to-end-lineage.json']),4)
 def test_all_bridges_no_plugs(self):
  out=artifacts()
  for name in ['debt-bridge.json','cash-bridge.json','financing-cash-bridge.json']:self.assertEqual(Decimal(out[name]['residual']),0)

 def test_narrow_hedge_retains_only_debt_dependency(self):
  e,p,pack=flagship(True,bounded='derivatives-hedge-accounting',objective='Review this cash-flow hedge relationship');r=e.execute(p,pack);self.assertEqual(set(r.case.skills_invoked),{'derivatives-hedge-accounting','debt-financing'})
 def test_narrow_cash_uses_only_debt_currency_and_cash(self):
  e,p,pack=flagship(True,bounded='cash-flow-reporting',objective='Why does financing cash flow differ from debt movement?');r=e.execute(p,pack);self.assertEqual(set(r.case.skills_invoked),{'debt-financing','foreign-currency','cash-flow-reporting'})
 def test_hash_seed_artifacts_are_identical(self):
  import os,subprocess,sys
  script="from orchestration.tests.generate_treasury_examples import artifacts; from orchestration.runtime import digest; print(digest(artifacts()))"
  values=[subprocess.check_output([sys.executable,'-c',script],env=dict(os.environ,PYTHONHASHSEED=seed),text=True) for seed in ('1','271')]
  self.assertEqual(values[0],values[1])
if __name__=='__main__':unittest.main()
