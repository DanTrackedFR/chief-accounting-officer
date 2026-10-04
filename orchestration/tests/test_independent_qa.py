"""Independent adversarial regressions, authored from architecture and public API."""
import copy
import json
import unittest
from orchestration.runtime import CAO, Case, company_context
from orchestration.planning import Issue, Node, Graph, DeterministicPlanner
from orchestration.registry import production
from orchestration.tests.fixtures import manufacturing
from operational_cases import operational
from additional_cases import certify

class FixedPlanner:
    def __init__(self, issues): self.issues=issues
    def identify(self, *args): return copy.deepcopy(self.issues)

class IndependentQA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ap=operational('accounts-payable');ap['functional_currency']='EUR'
        cls.ap=certify('accounts-payable',ap)
        cls.scope=dict(entity=ap['entity'],framework=ap['framework'],jurisdiction=ap['jurisdiction'],period_start=ap['period_start'],reporting_period=ap['reporting_period'],currency='EUR')
    def request(self):
        return dict(objective='What is our closing AP balance from this reconciled AP workpaper?',scope=copy.deepcopy(self.scope),facts={'supplier_cost':copy.deepcopy(self.ap)})
    def test_simple_ap_one_owner(self):
        c=CAO().run(self.request())
        self.assertEqual(c.outcome,'complete');self.assertEqual(c.skills_invoked,['accounts-payable'])
        self.assertEqual(c.status,'CLOSED');self.assertTrue(c.observer_ran)
    def test_wrong_each_execution_dimension(self):
        for key in ('entity','framework','jurisdiction','period_start','reporting_period','functional_currency'):
            with self.subTest(key=key):
                r=self.request();r['facts']['supplier_cost'][key]='wrong'
                c=CAO().run(r);self.assertEqual(c.outcome,'blocked');self.assertFalse(c.skills_invoked)
    def test_native_reviewer_gate_remains(self):
        r=self.request();r['facts']['supplier_cost'].pop('reviewer_signoff')
        c=CAO().run(r);self.assertNotEqual(c.outcome,'complete');self.assertNotEqual(c.status,'CLOSED')
        self.assertTrue(any('review' in str(n['open_items']).lower() for n in c.workplan_nodes))
    def test_nonproduction_material_grant_retains_ap(self):
        r=self.request();r['objective']='Review our supplier and grant accounting'
        r['facts']['grant']={'agreement':'actual subsidy','material':True}
        c=CAO().run(r);self.assertEqual(c.outcome,'partial')
        self.assertIn('accounts-payable',c.skills_invoked);self.assertNotIn('government-grants',c.skills_invoked)
        self.assertEqual(c.status,'DOCUMENTED')
    def test_nonproduction_immaterial_independent_grant(self):
        r=self.request();r['objective']='Review our supplier and grant accounting'
        r['facts']['grant']={'agreement':'actual subsidy','material':False,'required_for_objective':False}
        c=CAO().run(r);self.assertEqual(c.outcome,'complete')
        self.assertTrue(CAO().public(c)['open_items'])
    def test_custom_node_identity_not_skill_identity(self):
        p=FixedPlanner([Issue('ap-issue-1','liability','accounts-payable','actual supplier population',['supplier_cost'])])
        c=CAO(planner=p).run(self.request())
        self.assertEqual(c.outcome,'complete');self.assertEqual(c.status,'CLOSED')
    def test_malformed_supplied_known_family_is_visible(self):
        r=self.request();r['objective']='Review accounting completeness';r['facts']['inventory']=['material unsupported inventory data']
        c=CAO().run(r);self.assertNotEqual(c.outcome,'complete')
        self.assertIn('inventory',str(CAO().public(c)).lower())
    def test_materiality_flag_rejects_integer(self):
        r=self.request();p=FixedPlanner([Issue('accounts-payable','liability','accounts-payable','supplier',['supplier_cost'],material=1)])
        c=CAO(planner=p).run(r);self.assertEqual(c.outcome,'blocked')
    def test_unknown_owner_blocks_without_execution(self):
        p=FixedPlanner([Issue('unknown','unknown','unregistered-accounting-owner','supplied novel issue')])
        c=CAO(planner=p).run(self.request());self.assertEqual(c.outcome,'blocked');self.assertFalse(c.skills_invoked)
        self.assertIn('unavailable',str(CAO().public(c)))
    def test_false_condition_is_not_applicable(self):
        p=FixedPlanner([Issue('accounts-payable','liability','accounts-payable','conditional evidence',['supplier_cost'],condition={'fact':'active','equals':True})])
        c=CAO(planner=p).run(self.request());self.assertEqual(c.workplan_nodes[0]['status'],'not_applicable');self.assertFalse(c.skills_invoked)
    def test_simple_keyword_does_not_force_inventory(self):
        r=self.request();r['objective']='What is the closing AP balance for our manufacturing subsidiary?'
        c=CAO().run(r);self.assertEqual(c.skills_invoked,['accounts-payable']);self.assertEqual(c.outcome,'complete')
    def test_all_public_routes_retain_caveats_and_hide_private(self):
        from interfaces.public_output import ROUTES
        c=CAO().run(self.request());c.conclusions[0]['limitations'].append('Current evidence excludes a disputed supplier claim.')
        for route in ROUTES:
            p=CAO().public(c,route);self.assertIn('Current evidence excludes a disputed supplier claim.',p['limitations'])
            self.assertNotIn('reviewer_signoff',json.dumps(p));self.assertNotIn('case_fingerprint',json.dumps(p))
    def test_material_unresolved_case_cannot_close(self):
        c=Case('qa','review');c.status='DOCUMENTED';c.outcome='partial';c.observer_ran=True;c.artifacts=[{'id':'a'}]
        with self.assertRaises(ValueError):c.transition('CLOSED')
    def test_graph_cycle_unknown_and_duplicate(self):
        for deps in (['b'],['a'],['a','a']):
            g=Graph();g.add(Node('a','x','accounts-payable','r','E','IFRS',[],dependencies=deps))
            with self.assertRaises(ValueError):g.validate()
    def test_independent_ready_nodes_and_transitive_invalidation(self):
        g=Graph()
        for id,deps in [('a',[]),('b',[]),('c',['a']),('d',['c'])]:g.add(Node(id,'x','accounts-payable','r','E','IFRS',[],dependencies=deps))
        g.validate();self.assertEqual({n.id for n in g.ready()},{'a','b'})
        for n in g.nodes.values():n.status='complete';n.result={'retained':'prior evidence'}
        g.invalidate('a','wrong entity');self.assertEqual(g.nodes['b'].status,'complete')
        self.assertEqual([g.nodes[x].status for x in ('a','c','d')],['blocked']*3)
    def test_context_proposal_expiry_scope_and_conflict(self):
        records=[dict(attribute='currency',value='USD',status='APPROVED',scope={'entities':[self.scope['entity']]},effective_from='2020-01-01'),dict(attribute='currency',value='EUR',status='PROPOSED',scope={}),dict(attribute='currency',value='GBP',status='APPROVED',scope={'entities':['other']}),dict(attribute='currency',value='JPY',status='CONFIRMED',scope={},effective_to='2025-12-31')]
        before=copy.deepcopy(records);view,conflicts=company_context(records,self.scope)
        self.assertEqual(view['currency'],'USD');self.assertFalse(conflicts);self.assertEqual(records,before)
        records.append(dict(attribute='currency',value='EUR',status='CONFIRMED',scope={}))
        view,conflicts=company_context(records,self.scope);self.assertNotIn('currency',view);self.assertEqual(conflicts,['currency'])
    def test_context_answers_dimensions_and_no_mutation(self):
        r=self.request();r['company_context']=[dict(attribute=k,value=v,status='APPROVED',scope={}) for k,v in r.pop('scope').items()]
        before=copy.deepcopy(r);c=CAO().run(r);self.assertEqual(c.outcome,'complete');self.assertEqual(r,before)
        self.assertTrue(all(m['status'] in ('PROPOSED','OBSERVED') for m in c.memory_candidates))
    def test_public_retains_internal_and_rejects_training_attribution(self):
        c=CAO().run(self.request());before=copy.deepcopy(c.record());public=CAO().public(c)
        self.assertEqual(c.record(),before);self.assertNotIn('case_fingerprint',json.dumps(public));self.assertNotIn('evidence_status',json.dumps(public))
        c.conclusions[0]['limitations'].append('ChatGPT training data')
        with self.assertRaises(ValueError):CAO().public(c)
    def test_distinct_challenge_changes_material_result(self):
        r=self.request();r['challenge_assertions']=[dict(node='accounts-payable',metric_path=['closing_ap'],evidence_value='999999',operator='equal',evidence_ref='independent supplier confirmation',code='SUPPLIER_CONFIRMATION')]
        c=CAO().run(r);self.assertEqual(c.outcome,'blocked');self.assertEqual(c.status,'DOCUMENTED')
        self.assertTrue(c.workplan_nodes[0]['rework_triggered']);self.assertFalse(c.challenge_results[0]['passed'])
    def test_nested_owner_imports_are_planned_transitively(self):
        facts={'supplier_cost':{'invoices':[{'id':'invoice'}],'imports':[{'package':'employee-benefits-payroll','case':{'benefits':[{'id':'benefit'}],'imports':[{'package':'foreign-currency','case':{'items':[{'id':'fx'}]},'result':{}}]},'result':{}}]}}
        issues=DeterministicPlanner().identify('Review supplier liabilities',facts,self.scope,CAO().registry)
        by={i.owner:i for i in issues}
        self.assertIn('foreign-currency',by)
        self.assertIn('foreign-currency',by['employee-benefits-payroll'].dependencies)
    def test_duplicate_handoff_economic_alias_is_rejected(self):
        r=manufacturing();duplicate=copy.deepcopy(r['handoffs'][0]);duplicate['economic_id']='different-spelling-same-owner-metric';r['handoffs'].append(duplicate)
        c=CAO().run(r);self.assertNotEqual(c.outcome,'complete')
        self.assertNotEqual(c.status,'CLOSED')
    def test_reporting_owner_handoffs_cannot_be_omitted(self):
        r=manufacturing();r['handoffs']=[]
        c=CAO().run(r);self.assertNotEqual(c.outcome,'complete')
        self.assertNotEqual(c.status,'CLOSED')
        self.assertTrue(any(word in str(CAO().public(c)).lower() for word in ('handoff','mapping','lineage','bridge','owner')))
    def test_journal_account_remapping_cannot_change_accounting(self):
        r=manufacturing();r['journal_account_mapping']['accounts payable']='Revenue'
        c=CAO().run(r);self.assertNotEqual(c.outcome,'complete');self.assertNotEqual(c.status,'CLOSED')
    def test_fresh_pack_review_does_not_authorize_wrong_gl_mapping(self):
        from orchestration.runtime import digest
        r=manufacturing();clean=CAO().run(r)
        self.assertEqual(clean.outcome,'complete')
        native=[dict(owner=n.selected_skill,case_fingerprint=n.result['case_fingerprint'],journals=n.result.get('journal_entry_implications',[])) for n in clean.graph.nodes.values() if n.status=='complete']
        r['journal_account_mapping']['accounts payable']='Revenue'
        r['journal_pack_review']['payload_fingerprint']=digest(dict(mapping=r['journal_account_mapping'],native_owner_journals=native))
        c=CAO().run(r);self.assertNotEqual(c.outcome,'complete')
        findings=c.challenge_results[0]['findings']
        self.assertTrue(any('GL movement' in f['finding'] for f in findings),str(findings))
    def test_combined_journal_validation_cannot_be_omitted(self):
        r=manufacturing();r.pop('journal_account_mapping');r.pop('journal_pack_review')
        c=CAO().run(r);self.assertNotEqual(c.outcome,'complete')
    def test_missing_margin_basis_asks_material_question(self):
        r=manufacturing();r['company_context']=[]
        c=CAO().run(r);self.assertEqual(c.outcome,'partial');self.assertEqual(c.status,'DOCUMENTED')
        values=c.conclusions[0]['calculations'];self.assertNotIn('gross_margin',values)
        self.assertIn('revenue_less_inventory_relief',values)
        self.assertTrue(any('gross margin' in q['question'].lower().replace('_',' ').replace('-',' ') for q in c.open_questions))
    def test_alternate_approved_margin_basis_preserves_factory_expense(self):
        r=manufacturing();r['company_context'][0]['value']='inventory_relief_only'
        c=CAO().run(r);self.assertEqual(c.outcome,'complete')
        values=c.conclusions[0]['calculations'];D=__import__('decimal').Decimal
        self.assertEqual(D(values['gross_margin']),D('28696'))
        self.assertEqual(D(values['cost_of_sales']),D(values['cogs']))
        self.assertEqual(D(values['manufacturing_expense']),D('45000'))
    def test_proposed_margin_policy_cannot_be_established(self):
        r=manufacturing();r['company_context'][0]['status']='PROPOSED'
        c=CAO().run(r);self.assertEqual(c.outcome,'partial');self.assertNotIn('gross_margin',c.conclusions[0]['calculations'])
        self.assertFalse(any(f['attribute']=='gross_margin_basis' for f in c.facts['established']))
    def test_actual_owner_full_result_stale_import_rejected(self):
        r=manufacturing();r['facts']['inventory']['imports'][0]['result']['conclusion']='altered owner accounting conclusion'
        c=CAO().run(r);self.assertNotEqual(c.outcome,'complete');self.assertNotEqual(c.status,'CLOSED')
    def test_flagship_quantities_synthesis_and_negative_routes(self):
        r=manufacturing();c=CAO().run(r);self.assertEqual(c.outcome,'complete',str(c.open_questions)+str(c.conclusions))
        selected=set(c.skills_invoked)
        self.assertTrue({'inventory-cost','fixed-assets','employee-benefits-payroll','accounts-payable','foreign-currency','revenue-recognition','financial-statements'}<=selected)
        self.assertFalse({'agriculture-biological-assets','derivatives-hedge-accounting','insurance-contracts-accounting','lease-accounting','government-grants','borrowing-costs'}&selected)
        values=c.conclusions[0]['calculations'];D=__import__('decimal').Decimal
        self.assertEqual(D(values['period_revenue'])-D(values['cost_of_sales']),D(values['gross_margin']))
        self.assertEqual(D(values['period_revenue'])-D(values['cogs']),D(values['revenue_less_inventory_relief']))
        self.assertEqual(D(values['cost_of_sales']),D(values['cogs'])+D(values['manufacturing_expense']))
        self.assertEqual(D(values['manufacturing_expense']),D('45000'))
        self.assertEqual(D(values['gross_margin']),D('-16304'))
        self.assertTrue(c.handoff_ledger)

if __name__=='__main__':unittest.main()
