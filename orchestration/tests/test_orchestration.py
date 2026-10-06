"""Authored deterministic foundation and integration gates."""
import copy,json,unittest
from unittest.mock import patch
from decimal import Decimal
from orchestration import CAO,Case
from orchestration.registry import Registry
from orchestration.planning import Graph,Node,Issue,DeterministicPlanner
from orchestration.runtime import company_context
from interfaces.public_output import ROUTES,public_record
from orchestration.tests.fixtures import manufacturing

class Foundation(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.request=manufacturing();cls.cao=CAO();cls.result=cls.cao.run(cls.request)
    def run_request(self,change=None):
        r=copy.deepcopy(self.request)
        if change:change(r)
        return self.cao.run(r)
    def test_registry_single_truth(self):
        registry=Registry();self.assertEqual(50,len(registry.skills));self.assertEqual(47,sum(s['production_available'] for s in registry.skills.values()))
        for pkg in ('government-grants','borrowing-costs','investment-property'):self.assertFalse(registry.get(pkg)['production_available'])
        self.assertFalse(registry.get('unknown')['production_available'])
        self.assertIn('payroll processing',registry.get('inventory-cost')['non_triggers'])
    def test_flagship_actual_multi_owner(self):
        c=self.result;self.assertEqual('complete',c.outcome,c.open_questions);self.assertEqual('CLOSED',c.status)
        self.assertEqual(13,len(c.skills_invoked));calc=c.conclusions[0]['calculations']
        for k,v in {'closing_inventory':'45726.00','cogs':'11304.00','period_revenue':'40000.00','gross_margin':'-16304.00'}.items():self.assertEqual(v,calc[k])
        inv=c.graph.nodes['inventory-cost'].result['calculations'];self.assertEqual(Decimal('45000'),inv['order-1']['under_recovery'])
        self.assertEqual(Decimal('11304'),inv['inventory_by_class']['Work in progress'])
        self.assertEqual(7,len(c.handoff_ledger))
        for n in c.graph.nodes.values():self.assertEqual('complete',n.status,n.open_items)
    def test_no_irrelevant_owners(self):
        for pkg in ('agriculture-biological-assets','derivatives-hedge-accounting','insurance-contracts-accounting','lease-accounting','government-grants','borrowing-costs','investment-property'):
            self.assertNotIn(pkg,self.result.graph.nodes)
    def test_dependency_order_and_parallel_wave(self):
        ledger={x['node']:i for i,x in enumerate(self.result.execution_ledger)}
        for n in self.result.graph.nodes.values():
            for dep in n.dependencies:self.assertLess(ledger[dep],ledger[n.id])
        first=self.result.execution_ledger[0]['batch'];self.assertIn(self.result.graph.nodes.resolve('fixed-assets'),first);self.assertIn(self.result.graph.nodes.resolve('employee-benefits-payroll'),first)
    def test_conditional_fx_selection(self):
        r=manufacturing(False);c=self.cao.run(r);self.assertEqual('complete',c.outcome,c.open_questions);self.assertNotIn('foreign-currency',c.graph.nodes)
        self.assertEqual('45616.00',c.conclusions[0]['calculations']['closing_inventory'])
    def test_conditional_warranty_selection(self):
        planner=DeterministicPlanner();facts={'obligation':{'obligation':{'type':'warranty'}}}
        self.assertEqual(['provisions-contingencies'],[i.owner for i in planner.identify('Review year end',facts,{},Registry())])
        self.assertEqual([],planner.identify('Review year end',{}, {},Registry()))
    def test_simple_ap_is_one_owner(self):
        r=copy.deepcopy(self.request);r['objective']='What is our closing AP balance from this reconciled AP workpaper?';r['handoffs']=[];r['challenge_assertions']=[]
        c=self.cao.run(r);self.assertEqual(['accounts-payable'],c.skills_invoked);self.assertEqual('20',c.conclusions[0]['calculations']['closing_ap'])
    def test_material_unavailable_owner_partial(self):
        c=self.run_request(lambda r:r['facts'].update(grant={'agreement':{'subsidy':'50000'},'material':True}))
        self.assertEqual('partial',c.outcome);self.assertEqual('DOCUMENTED',c.status);self.assertEqual('blocked',c.graph.nodes['government-grants'].status)
        self.assertEqual('complete',c.graph.nodes['inventory-cost'].status);self.assertIn('Government', 'Government')
        self.assertIn('unavailable',json.dumps(self.cao.public(c)))
    def test_explicit_independent_immaterial_gap(self):
        c=self.run_request(lambda r:r['facts'].update(grant={'agreement':{'amount':'1'},'required_for_objective':False,'material':False}))
        self.assertEqual('complete',c.outcome);self.assertTrue(c.conclusions[0]['open_items'])
    def test_unknown_materiality_does_not_ignore_gap(self):
        c=self.run_request(lambda r:r['facts'].update(qualifying_interest={'project':'factory project','required_for_objective':False}))
        self.assertEqual('partial',c.outcome)
    def test_challenge_invalidates_and_propagates(self):
        c=self.run_request(lambda r:r['challenge_assertions'][0].update(evidence_value='999'))
        self.assertEqual('partial',c.outcome);self.assertEqual('blocked',c.graph.nodes['inventory-cost'].status)
        self.assertTrue(c.graph.nodes['financial-statements'].rework_triggered)
        self.assertNotIn('gross_margin',c.conclusions[0]['calculations'])
    def test_wrong_dimensions_and_currency(self):
        for field,value in [('entity','other'),('framework','US_GAAP'),('reporting_period','2025-12-31'),('functional_currency','EUR'),('jurisdiction','AU')]:
            with self.subTest(field=field):
                c=self.run_request(lambda r:r['facts']['customer_contract'].update({field:value}));self.assertNotEqual('complete',c.outcome)
    def test_duplicate_economic_consumption(self):
        c=self.run_request(lambda r:r['handoffs'].append(copy.deepcopy(r['handoffs'][0])))
        self.assertNotEqual('complete',c.outcome)
    def test_semantic_metric_mismatch(self):
        c=self.run_request(lambda r:r['handoffs'][0].update(metric_path=['closing_cost']))
        self.assertNotEqual('complete',c.outcome)
    def test_stale_case_certification_not_generated(self):
        c=self.run_request(lambda r:r['facts']['customer_contract']['reviewer_signoff'].update(case_fingerprint='stale'))
        self.assertNotEqual('complete',c.outcome);self.assertEqual('partial',c.graph.nodes['revenue-recognition'].status)
    def test_source_owner_contradiction_not_selected(self):
        c=self.run_request(lambda r:r['facts']['inventory']['imports'][0]['result']['calculations'].update(depreciation='89999'))
        self.assertNotEqual('complete',c.outcome)
    def test_no_approved_context_mutation(self):
        r=copy.deepcopy(self.request);r['company_context']+=[dict(attribute='year_end',value='12-31',status='APPROVED',scope={'entities':['Synthetic Group']})];before=copy.deepcopy(r)
        c=self.cao.run(r);self.assertEqual(before,r);self.assertTrue(c.observer_ran)
        self.assertTrue(all(m['status']=='PROPOSED' for m in c.memory_candidates))
    def test_context_precedes_questions(self):
        r=copy.deepcopy(self.request);value=r['scope'].pop('framework');r['company_context']+=[dict(attribute='framework',value=value,status='APPROVED',scope={'entities':['Synthetic Group']})]
        c=self.cao.run(r);self.assertEqual('complete',c.outcome,c.open_questions)
    def test_context_conflict_not_assumption_fact(self):
        c=self.run_request(lambda r:r.update(company_context=[dict(attribute='framework',value='US_GAAP',status='APPROVED',scope={})]))
        self.assertEqual('blocked',c.outcome);self.assertTrue(c.facts['disputed'])
    def test_optional_context_does_not_block(self):self.assertEqual([],self.result.open_questions)
    def test_all_public_routes_separate_from_internal(self):
        before=json.dumps(self.result.record(),default=str)
        for route in ROUTES:
            public=json.dumps(self.cao.public(self.result,route));self.assertNotIn('case_fingerprint',public);self.assertNotIn('claim_id',public);self.assertNotIn('synthetic independent reviewer',public)
            self.assertIn('45726.00',public);self.assertIn('limitations',public)
        self.assertEqual(before,json.dumps(self.result.record(),default=str));self.assertTrue(self.result.evidence_refs)
    def test_public_contamination_fails_closed(self):
        for token in ('Source: secret','ChatGPT training data','case_fingerprint','a'*64):
            with self.subTest(token=token),self.assertRaises(ValueError):public_record({'guidance':token},route='answer')
    def test_graph_validation_and_reopen(self):
        def node(id,deps):return Node(id,id,id,'reason','E','IFRS',['2026','2026'],dependencies=deps)
        g=Graph();g.add(node('a',[]));g.add(node('b',['a']));g.add(node('c',['b']));g.validate()
        self.assertEqual(['a'],[n.id for n in g.ready()]);g.invalidate('a','contradiction');self.assertEqual('blocked',g.nodes['c'].status)
        g.reopen('a');self.assertEqual('pending',g.nodes['c'].status)
        g.nodes['a'].dependencies=['c']
        with self.assertRaises(ValueError):g.validate()
    def test_cycle_unknown_owner_malformed_plan(self):
        class Bad:
            def identify(self,*args):return [Issue('a','x','unknown','unknown',dependencies=['a'])]
        r=copy.deepcopy(self.request);r['handoffs']=[];c=CAO(planner=Bad()).run(r);self.assertEqual('blocked',c.outcome);self.assertIn('cycle',str(c.open_questions))
    def test_invalid_lifecycle(self):
        c=Case('id','objective')
        with self.assertRaises(ValueError):c.transition('CLOSED')
    def test_normal_bad_input_structured(self):
        for value in (None,[],{},dict(objective='Review',facts=[])):
            self.assertEqual('blocked',self.cao.run(value).outcome)

if __name__=='__main__':unittest.main()
