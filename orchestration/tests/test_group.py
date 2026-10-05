"""Authored end-to-end Group Accounting acceptance and specialist boundaries."""
import copy,json,os,subprocess,sys,unittest
from pathlib import Path
from decimal import Decimal
from orchestration.tests.group_fixtures import *
from orchestration.tests.generate_group_examples import artifacts
from orchestration.runtime import CAO
from orchestration.result_bindings import validate_receipts
from orchestration.period_selection import validate_activity

class GroupAuthored(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.primary=run(False);cls.clean=run(True);cls.owners=owner_cases()
        cls.results={n['selected_skill']:n['result'] for n in cls.clean.case.workplan_nodes if n['status']=='complete'}
    def test_primary_conflict_is_material_partial(self):
        self.assertEqual((self.primary.case.outcome,self.primary.case.status),('partial','DOCUMENTED'))
        self.assertEqual(len(self.primary.conflicts),1);self.assertIn('105 versus 100',json.dumps(CAO().public(self.primary.case)))
    def test_clean_control_complete_closed(self):self.assertEqual((self.clean.case.outcome,self.clean.case.status),('complete','CLOSED'))
    def test_raw_company_sources_not_owner_payloads(self):
        self.assertTrue(all(s.format in ('csv','markdown') for s in group_sources()))
        self.assertNotIn('SKILL-',OBJECTIVE);self.assertGreater(len(self.clean.lineage),45)
    def test_modes_are_semantic_not_keywords(self):self.assertEqual(self.clean.case.work_modes['primary'],'CLOSE_REVIEW')
    def test_nine_production_owners_qualified(self):
        expected={'income-taxes','business-combinations','foreign-currency','intercompany-accounting','asset-impairment','consolidation','financial-statements','management-accounting-analytics','disclosure-management'}
        self.assertEqual(set(self.clean.case.skills_invoked),expected)
        self.assertTrue(all(n['status']=='complete' for n in self.clean.case.workplan_nodes))
    def test_genuine_control_not_ownership_percentage(self):
        c=copy.deepcopy(self.owners['consolidation']);c['entities'][1]['control']['substantive_power']=False
        with self.assertRaises((ValueError,AssertionError)):completed('consolidation',certify('consolidation',c))
    def test_native_acquisition_goodwill_and_full_nci(self):
        c=self.results['business-combinations']['calculations'];self.assertEqual(c['initial_goodwill'],Decimal(225));self.assertEqual(c['nci'],Decimal(200));self.assertEqual(c['net_assets'],Decimal(775))
    def test_tax_fv_to_goodwill_exact_once(self):
        tax=self.results['income-taxes']['calculations']['jurisdictions'][0]['dtl'];bc=self.results['business-combinations']['calculations']
        self.assertEqual(tax,25);self.assertEqual(bc['liabilities'],225);self.assertEqual(bc['initial_goodwill'],800+200-(1000-200-tax))
    def test_pre_post_and_full_year_population(self):
        s=self.owners['foreign-currency'];validate_activity(s)
        self.assertEqual(sum(Decimal(r['revenue'])-Decimal(r['expense']) for r in s['activity_selection']['records']),250)
        self.assertEqual(s['translation']['profit'],'100')
    def test_only_post_profit_in_group(self):self.assertEqual(self.results['foreign-currency']['calculations']['translation']['profit_translated'],85)
    def test_full_year_inclusion_rejected(self):
        s=copy.deepcopy(self.owners['foreign-currency']);s['activity_selection']['included_ids']=['pre','post']
        with self.assertRaises(ValueError):validate_activity(s)
    def test_foreign_goodwill_not_fixed_parent_currency(self):
        self.assertEqual(self.results['foreign-currency']['calculations']['translation']['translated_tb']['goodwill'],180)
        self.assertNotEqual(Decimal(225)*Decimal('.9'),180)
    def test_cta_attribution(self):
        f=self.results['foreign-currency']['calculations']['translation'];self.assertEqual((f['cta_movement'],f['owners_movement'],f['nci_movement']),(-105,-84,-21))
    def test_nci_rollforward(self):
        n=self.results['consolidation']['calculations']['nci'][0];self.assertEqual(180+n['profit']+n['oci'],n['closing']);self.assertEqual(n['closing'],176)
    def test_cons_does_not_recreate_ppa_or_fx(self):
        c=self.owners['consolidation'];self.assertEqual(c['investments'][0]['goodwill'],'0');self.assertEqual(c['investments'][0]['fair_value_adjustments'],{});self.assertTrue(all(e['translation'] is None for e in c['entities']))
    def test_impairment_is_supported_nil_not_invented(self):
        c=self.results['asset-impairment']['calculations'];self.assertEqual((c['carrying'],c['recoverable'],c['loss'],c['headroom']),(880,900,0,20))
    def test_cons_and_statements_semantic_population(self):
        a=self.results['consolidation']['calculations']['consolidated_balances'];b=self.results['financial-statements']['calculations']['current'];self.assertEqual(a,b['lines']);self.assertEqual((b['profit'],b['oci'],b['closing_equity']),(285,-105,2360))
    def test_only_group_adjustments_are_posting_population(self):
        ledger=self.clean.case.journal_ownership_ledger;self.assertTrue(any(not r['posting'] for r in ledger));self.assertTrue(all(r['level']=='group' and r['target_entity']==GROUP for r in ledger))
        self.assertTrue(all(j['owner']=='consolidation' for j in self.clean.case.conclusions[0]['journals']))
    def test_intercompany_source_owner_not_elimination_owner(self):self.assertEqual(self.results['intercompany-accounting']['journal_entry_implications'],[])
    def test_hypothesis_rejected_by_post_acquisition_evidence(self):self.assertEqual(self.clean.case.diagnostics[0]['hypotheses'][0]['disposition'],'REJECTED')
    def test_analytics_escalates_to_accounting(self):self.assertTrue(any(q['status']=='OWNER_RECHECK_SUPPORTED' for q in self.clean.case.accounting_questions))
    def test_public_is_one_cao_answer(self):
        answer=CAO().public(self.clean.case);self.assertIn('Consolidated profit is 285',answer['guidance']);self.assertIn('NCI 176',answer['guidance']);self.assertIn('pre-acquisition',answer['guidance']);self.assertNotIn('SKILL-',json.dumps(answer))
    def test_memory_candidates_never_promoted(self):self.assertTrue(all(m['status']=='PROPOSED' for m in self.clean.case.memory_candidates))
    def test_no_residual_backlog_or_unrelated_owners(self):
        self.assertFalse({'government-grants','borrowing-costs','investment-property','revenue-recognition','debt-financing','employee-benefits-payroll'}&set(self.clean.case.skills_invoked))
    def test_narrow_four_owner_controls(self):
        for owner,objective in [('business-combinations','Review the acquisition accounting for this purchase.'),('intercompany-accounting',"Why do these intercompany balances disagree?"),('foreign-currency','Review foreign subsidiary translation.'),('asset-impairment','Review goodwill impairment.')]:
            with self.subTest(owner=owner):
                r=narrow(owner,objective);self.assertEqual(r.case.skills_invoked,[owner]);self.assertEqual(r.case.outcome,'complete')
    def test_artifacts_match_current_generator(self):
        for name,value in artifacts().items():self.assertEqual(json.loads((Path(__file__).resolve().parents[1]/'examples/group-accounting'/name).read_text()),json.loads(json.dumps(value,default=str)))
    def test_five_executable_material_lineages(self):self.assertEqual(len(artifacts()['end-to-end-lineage.json']),5)
    def test_bridges_no_unexplained_plug(self):
        out=artifacts()
        for name in ('acquisition-bridge.json','nci-bridge.json','cta-bridge.json','goodwill-bridge.json','group-tax-bridge.json','consolidated-equity-bridge.json','group-profit-bridge.json','consolidation-bridge.json'):
            with self.subTest(name=name):self.assertEqual(Decimal(out[name]['residual']),0)
    def test_changed_parent_analytics_source_cannot_override_standalone_result(self):
        from dataclasses import replace
        sources=[replace(s,payload=s.payload.replace('285,200,85','285,300,85')) if s.id=='analytics-source' else s for s in group_sources(True)]
        engine=Intake(FixturePlanner(group_proposal(sources)));prepared=engine.prepare(OBJECTIVE,sources,[],SCOPE)
        result=engine.execute(prepared,group_review_pack(prepared));self.assertNotEqual(result.case.outcome,'complete')
    def test_recoverable_source_cannot_override_actual_valuation_calculation(self):
        from dataclasses import replace
        sources=[replace(s,payload=s.payload.replace('900,180,700','700,180,700')) if s.id=='valuation' else s for s in group_sources(True)]
        engine=Intake(FixturePlanner(group_proposal(sources)));prepared=engine.prepare(OBJECTIVE,sources,[],SCOPE)
        with self.assertRaises(ValueError):engine.execute(prepared,group_review_pack(prepared))
    def test_account_alias_cannot_hide_duplicate_group_event(self):
        from orchestration.runtime import CAO
        native=[dict(owner='consolidation',journals=self.results['consolidation']['journal_entry_implications'])]
        events=[dict(economic_id='event-'+str(i),primary=[dict(owner='consolidation',index=i)],witnesses=[],evidence='Independent source identity') for i,_ in enumerate(native[0]['journals'])]
        duplicate=copy.deepcopy(events[0]);duplicate['economic_id']='different-label';events.append(duplicate)
        with self.assertRaises(ValueError):CAO._qualified_journals(native,{'noncontrolling interest':'NCI alias'},events)
    def test_seed_independent_artifacts(self):
        script='from orchestration.tests.generate_group_examples import artifacts; from orchestration.runtime import digest; print(digest(artifacts()))'
        outputs=[subprocess.check_output([sys.executable,'-c',script],env=dict(os.environ,PYTHONHASHSEED=s),text=True) for s in ('1','271')]
        self.assertEqual(outputs[0],outputs[1])

if __name__=='__main__':unittest.main()
