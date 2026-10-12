"""Genuine fresh-process local-contract acceptance, synthetic reviewed economics."""
import json
import unittest
from build4.prove_integrated import proof

class IntegratedJourneys(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=proof()
        json.dumps(cls.result,sort_keys=True,allow_nan=False)
    def test_revenue_native_owner_and_new_economics(self):
        r=self.result['revenue']
        self.assertEqual(r['original']['execution_state'],'complete')
        self.assertIn('31920',json.dumps(r['original']['public_result']))
        self.assertEqual(r['original']['workplan'][0]['owner'],'revenue-recognition')
    def test_source_linked_followup_before_qualification(self):
        r=self.result['revenue']
        self.assertEqual(r['observed']['execution_state'],'blocked')
        self.assertIn('remedies',json.dumps(r['targeted']).lower())
        self.assertFalse(r['observed']['investigation']['accounting_qualified'])
    def test_correction_has_revised_economics_and_history(self):
        r=self.result['revenue']
        self.assertEqual(r['changed']['currentness'],'STALE')
        self.assertEqual(r['reworked']['execution_state'],'complete')
        self.assertIn('34200',json.dumps(r['reworked']['public_result']))
        self.assertGreater(len(r['final_versions']),len(r['original_versions']))
        originals={x['version_id']:x['immutable_sha256'] for x in r['original_versions']}
        finals={x['version_id']:x['immutable_sha256'] for x in r['final_versions']}
        for key,value in originals.items():self.assertEqual(finals[key],value)
    def test_exact_once_retries(self):
        self.assertEqual(self.result['revenue']['native_operations'],2)
    def test_prepaid_discovery_from_actual_population(self):
        r=self.result['prepayments']['movement']
        self.assertEqual(r['investigation']['observations'][0]['increase'],'15750')
        self.assertEqual(r['investigation']['observations'][0]['transactions'][0]['residual'],'-100')
        self.assertIn('BC-20481',json.dumps(r['investigation']['requests']))
        self.assertEqual(r['execution_state'],'blocked')
    def test_invoice_observation_cannot_complete_accounting(self):
        self.assertEqual(self.result['prepayments']['invoice']['execution_state'],'blocked')
    def test_process_interruption_restores_exact_checkpoint(self):
        self.assertTrue(self.result['interruption']['process_killed_after_durable_checkpoint'])
        self.assertFalse(self.result['interruption']['duplicate_economics'])
    def test_framework_entity_period_repeated_owner_isolation(self):
        r=self.result['repeated_entity_period_owners']
        self.assertEqual(len({x['case_id'] for x in r}),3)
        self.assertEqual({x['scope']['framework'] for x in r},{'IFRS','US_GAAP'})
        self.assertEqual({x['scope']['period_start'] for x in r},{'2026-01-01','2027-01-01'})
        for x in r:self.assertEqual(x['response']['execution_state'],'complete')
    def test_group_remains_group_and_conflicts_block(self):
        self.assertEqual(self.result['multi_entity_group']['case_type'],'GROUP_CASE')
        self.assertIsNone(self.result['multi_entity_group']['snapshot']['scope']['scopes'][0]['legal_entity_id'])
        self.assertEqual(self.result['conflict']['execution_state'],'blocked')
    def test_build3_wrong_framework_dimensions_regression(self):
        self.assertFalse(self.result['wrong_framework_dimensions']['ok'])
    def test_build3_irrelevant_framework_does_not_conflict(self):
        self.assertEqual(self.result['multi_entity']['scope']['framework'],'UK_GAAP')
        self.assertEqual(self.result['multi_entity']['conflicts'],[])
        self.assertEqual(self.result['qualified_uk_case']['execution_state'],'blocked')
    def test_cross_company_denied(self):
        self.assertFalse(self.result['isolation']['ok'])

if __name__=='__main__':unittest.main()
