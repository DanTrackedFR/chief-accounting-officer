"""Explicit manufacturing contradiction cases using refreshed synthetic review only."""
import copy,unittest
from orchestration import CAO
from orchestration.tests.fixtures import manufacturing
from inventory_cases import sources,ready as inventory_ready
from additional_cases import certify

class ManufacturingContradictions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.request=manufacturing()
    def result(self,mutator,refresh=False):
        r=copy.deepcopy(self.request);mutator(r)
        if refresh:r['facts']['inventory']=inventory_ready(c=sources(r['facts']['inventory']))
        c=CAO().run(r)
        self.assertNotEqual('complete',c.outcome);self.assertNotEqual('CLOSED',c.status)
        return c
    def test_payroll_import_differs(self):self.result(lambda r:r['facts']['inventory']['costs'][0].update(amount='10799'))
    def test_duplicate_ap_cost_direct_inventory(self):
        def mutate(r):
            x=copy.deepcopy(r['facts']['inventory']['costs'][1]);x.update(id='duplicate-ap',owner_import=None);r['facts']['inventory']['costs'].append(x)
        self.result(mutate,True)
    def test_depreciation_wrong_period(self):self.result(lambda r:r['facts']['machinery'].update(reporting_period='2025-12-31'))
    def test_inventory_gl_disagrees(self):
        c=self.result(lambda r:r['challenge_assertions'][0].update(evidence_value='45725'))
        self.assertIn('INVENTORY_GL',str(c.challenge_results));self.assertTrue(c.graph.nodes['inventory-cost'].invalidated_results)
    def test_revenue_quantity_exceeds_inventory_relief(self):
        def mutate(r):
            c=r['facts']['customer_contract'];c['delivered_quantity']='21';r['facts']['customer_contract']=certify('revenue-recognition',c)
        c=self.result(mutate);self.assertIn('SALES_RELIEF',str(c.challenge_results))
    def test_fx_conversion_disagrees(self):self.result(lambda r:r['handoffs'][3].update(amount='111'))
    def test_manufacturing_system_quantity_disagrees(self):self.result(lambda r:r['challenge_assertions'][1].update(evidence_value='61'))
    def test_duplicated_production_order(self):
        def mutate(r):
            x=copy.deepcopy(r['facts']['inventory']['orders'][0]);x['id']='alias-order';r['facts']['inventory']['orders'].append(x)
        self.result(mutate,True)
    def test_stale_owner_full_result(self):self.result(lambda r:r['facts']['inventory']['imports'][0]['result'].update(conclusion='altered'))
    def test_same_source_under_new_handoff_alias(self):
        def mutate(r):
            x=copy.deepcopy(r['handoffs'][0]);x['economic_id']='new-id-same-source';r['handoffs'].append(x)
        self.result(mutate)
    def test_rework_retains_prior_case(self):
        request=copy.deepcopy(self.request);request['challenge_assertions'][0]['evidence_value']='1';cao=CAO();old=cao.run(request)
        new=copy.deepcopy(self.request);new['case_id']='synthetic-factory-reworked';revised=cao.rework(old,new)
        self.assertEqual('partial',old.outcome);self.assertEqual('complete',revised.outcome);self.assertIn(old.id,revised.supersedes)

if __name__=='__main__':unittest.main()
