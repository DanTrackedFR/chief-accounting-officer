"""Authored quantitative/intent/integration regression; no production mocks."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path
from decimal import Decimal as D
from orchestration import CAO
from orchestration.intent import Intent, interpret
from orchestration.planning import DeterministicPlanner
from orchestration.registry import Registry
from orchestration.tests.diagnostic_fixtures import diagnostic_manufacturing
from governance_cases import ready, refresh_release
from governance_accounting import digest
from production import assess_case, to_public
spec=importlib.util.spec_from_file_location('diagnostic_methods',Path(__file__).resolve().parents[2]/'skills/management-accounting-analytics/diagnostics.py')
methods=importlib.util.module_from_spec(spec);spec.loader.exec_module(methods)

class DiagnosticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.request=diagnostic_manufacturing();cls.c=cls.request['facts']['analytics']
    def changed(self,fn):
        c=copy.deepcopy(self.c);fn(c)
        for d in c['documents']:d['content_hash']=digest(d['content'])
        return ready('management-accounting-analytics',c=refresh_release(c))
    def result(self,c):return assess_case('management-accounting-analytics',c)
    def doc(self,c,id):return next(x['content'] for x in c['documents'] if x['id']==id)
    def test_bridge_and_margin_percentage_denominator(self):
        r=self.result(self.c);self.assertEqual(r['status'],'complete');b=r['calculations']['diagnostic']['bridge']
        self.assertEqual(D(b['starting']),D('15000'));self.assertEqual(D(b['ending']),D('-16304'))
        total=sum((D(x['contribution']) for x in b['drivers']),D(0))
        self.assertEqual(D(b['starting'])+total+D(b['residual']),D(b['ending']))
        self.assertAlmostEqual(D(b['explained_percent']),D(100))
        p=b['margin_points'];self.assertAlmostEqual(D(p['starting'])+sum((D(x['contribution']) for x in p['drivers']),D(0))+D(p['denominator_effect'])+D(p['residual']),D(p['ending']))
        self.assertEqual(D(p['starting']),D(30));self.assertEqual(D(p['ending']),D('-40.76'))
    def test_rate_quantity_interaction_convention(self):
        rows=[dict(q0=10,p0=2,q1=12,p1=3)]
        self.assertEqual(methods.rate_quantity(rows),[('quantity',D(4)),('rate',D(12))])
    def test_mix_population_convention_reconciles(self):
        rows=[dict(q0=10,p0=2,q1=5,p1=3),dict(q0=10,p0=4,q1=20,p1=5)]
        self.assertEqual(sum(v for k,v in methods.price_volume_mix(rows)),D(55))
    def test_period_intents_and_negative_selection(self):
        planner=DeterministicPlanner();reg=Registry();facts=self.request['facts']
        expected=[('Why did gross margin fall?','DIAGNOSTIC_ANALYTICS'),('How should we account for factory under-absorption?','ACCOUNTING_DETERMINATION'),('Review the manufacturing close.','CLOSE_REVIEW'),('Prepare the manufacturing accounting memo.','DOCUMENTATION'),('Our manufacturing close is too manual. Review the process.','PROCESS_CONTROL_REVIEW'),('What is closing inventory?','REPORTING')]
        for obj,mode in expected:
            with self.subTest(mode=mode):self.assertEqual(interpret(obj).primary,mode)
        selected=lambda obj:{i.owner for i in planner.identify(obj,facts,{},reg)}
        self.assertNotIn('management-accounting-analytics',selected(expected[1][0]))
        self.assertNotIn('inventory-cost',selected(expected[4][0]))
        self.assertNotIn('month-end-close',selected(expected[-1][0]))
        self.assertNotIn('management-accounting-analytics',selected(expected[-1][0]))
        self.assertIn('accounting-policy-memo-governance',selected(expected[3][0]))
    def test_governed_intent_rejects_duplicates(self):
        with self.assertRaises(ValueError):Intent('DIAGNOSTIC_ANALYTICS',['DIAGNOSTIC_ANALYTICS']).validate()
    def test_actual_vs_supplied_budget_comparator(self):
        def mutate(c):
            d=c['diagnostic'];s=self.doc(c,'diagnostic-prior');s.update(kind='budget',period=[c['period_start'],c['reporting_period']]);d['comparator'].update(kind='budget',period=s['period'])
            for g in d['groups']:self.doc(c,g['doc'])['baseline_period']=s['period']
        r=self.result(self.changed(mutate));self.assertEqual(r['status'],'complete',r['conclusion']);self.assertEqual(r['calculations']['diagnostic']['bridge']['comparator_kind'],'budget')
    def test_all_supplied_comparator_kinds(self):
        for kind in ('forecast','standard','target','approved_baseline'):
            def mutate(c):
                d=c['diagnostic'];s=self.doc(c,'diagnostic-prior');s.update(kind=kind,period=[c['period_start'],c['reporting_period']]);d['comparator'].update(kind=kind,period=s['period'])
                for g in d['groups']:self.doc(c,g['doc'])['baseline_period']=s['period']
            r=self.result(self.changed(mutate));self.assertEqual(r['status'],'complete',r['conclusion'])
    def test_material_residual_preserves_native_schedule(self):
        def mutate(c):
            s=self.doc(c,'diagnostic-prior');s['amount']='19000';s['records'][0]['amount']='19000'
        r=self.result(self.changed(mutate));self.assertEqual(r['status'],'partial');b=r['calculations']['diagnostic']['bridge'];self.assertEqual(D(b['residual']),D('-4000'));self.assertTrue(r['open_items'])
    def test_immaterial_residual_is_visible(self):
        def mutate(c):
            s=self.doc(c,'diagnostic-prior');s['amount']='15001';s['records'][0]['amount']='15001'
        r=self.result(self.changed(mutate));self.assertEqual(r['status'],'complete');self.assertEqual(D(r['calculations']['diagnostic']['bridge']['residual']),D(-1))
    def test_unknown_materiality_never_waives_residual(self):
        def mutate(c):
            c['diagnostic']['materiality']=None;s=self.doc(c,'diagnostic-prior');s['amount']='15001';s['records'][0]['amount']='15001'
        r=self.result(self.changed(mutate));self.assertEqual(r['status'],'partial')
    def test_omitted_driver_remains_residual(self):
        def mutate(c):
            d=c['diagnostic'];d['groups']=[g for g in d['groups'] if g['id']!='capacity'];d['group_inventory']=[g['id'] for g in d['groups']];d['component_ties']=[t for t in d['component_ties'] if t['groups']!=['capacity']]
        r=self.result(self.changed(mutate));self.assertEqual(r['status'],'partial');self.assertEqual(D(r['calculations']['diagnostic']['bridge']['residual']),D('-25000'))
    def test_hypothesis_supported_rejected_partial_unresolved(self):
        for value,cls,expected in [('20000','bridge_attribution','SUPPORTED'),('50000','bridge_attribution','REJECTED'),('20000','statistical_association','UNRESOLVED')]:
            def mutate(c):h=c['diagnostic']['hypotheses'][0];h['evidence_class']=cls;h['tests'][0]['value']=value
            r=self.result(self.changed(mutate));self.assertEqual(r['calculations']['diagnostic']['hypotheses'][0]['disposition'],expected)
        def mutate(c):h=c['diagnostic']['hypotheses'][0];h['tests'].append(dict(h['tests'][0],value='50000'))
        r=self.result(self.changed(mutate));self.assertEqual(r['calculations']['diagnostic']['hypotheses'][0]['disposition'],'PARTIALLY_SUPPORTED')
    def test_fpna_action_flags_reject(self):
        for flag in ('budgeting','forecasting','commercial_planning','automatic_gl_correction'):
            r=self.result(self.changed(lambda c:c['governance_method'].update({flag:True})));self.assertEqual(r['status'],'blocked')
    def test_mandatory_diagnostic_facts(self):
        request=copy.deepcopy(self.request);request['facts']['analytics']=self.changed(lambda c:c.update(diagnostic=None))
        c=CAO().run(request);self.assertNotEqual(c.outcome,'complete')
    def test_monthly_factory_and_owner_recheck(self):
        c=CAO().run(self.request);self.assertEqual(c.outcome,'complete',c.open_questions);self.assertEqual(c.periods,['2026-12-01','2026-12-31']);self.assertEqual(c.work_modes['primary'],'DIAGNOSTIC_ANALYTICS')
        self.assertEqual(c.accounting_questions[0]['target_owner'],'inventory-cost');self.assertEqual(c.accounting_questions[0]['status'],'OWNER_RECHECK_SUPPORTED')
        self.assertTrue(any(n['issue']=='diagnostic accounting follow-up' for n in c.workplan_nodes))
        self.assertEqual(len(c.conclusions[0]['journals']),len(CAO().run(dict(self.request,objective='Review the manufacturing close.')).conclusions[0]['journals']))
        self.assertTrue(all(m['status'] in ('PROPOSED','OBSERVED') for m in c.memory_candidates))
    def test_reusable_nonmanufacturing_expense_bridge(self):
        from governance_cases import row
        def mutate(c):
            ap=copy.deepcopy(self.request['facts']['supplier_cost'])
            c['imports'].append(row(c,'expense-owner',package='accounts-payable',case=ap,result=assess_case('accounts-payable',ap),mode='evidence_only'))
            ref=dict(owner_import='expense-owner',result_path=['invoices'],amount='120')
            d=c['diagnostic'];d.update(metric='expense',presentation_basis='signed_balance',revenue=None,hypotheses=[],signals=[])
            current=self.doc(c,'diagnostic-current');current.update(metric='expense',presentation_basis='signed_balance',amount='120',records=[dict(id='expense-posted',amount='120')],inventory=['expense-posted'],owner_components=[dict(sign=1,ref=ref)])
            prior=self.doc(c,'diagnostic-prior');prior.update(metric='expense',presentation_basis='signed_balance',amount='100',expense='100',records=[dict(id='expense-prior',amount='100')],inventory=['expense-prior'])
            source=self.doc(c,'other-cost');source.pop('component_allocation');source.update(metric='expense',presentation_basis='signed_balance',source_owner='accounts-payable',source_metric='invoices',method='owner_flux',records=[dict(id='expense-change',baseline_amount='100',current_amount='120',current_owner=ref,economic_components=['expense-source-population'])],inventory=['expense-change'])
            d['groups']=[dict(id='expense',doc='other-cost',method='owner_flux',sign=1,labels={'movement':'Supported expense movement'},accounting_check=None)];d['group_inventory']=['expense'];d['component_ties']=[dict(groups=['expense'],current_owner=ref,baseline_field='expense',sign=1)]
        r=self.result(self.changed(mutate));self.assertEqual(r['status'],'complete',r['conclusion']);b=r['calculations']['diagnostic']['bridge'];self.assertEqual(D(b['change']),D(20));self.assertEqual(D(b['residual']),D(0))

    def test_native_skill_public_does_not_emit_diagnostic_lineage(self):
        r=self.result(self.c)
        for route in ('answer_context','answer','retrieval_snippet','citation','tool_output','user_log','export'):
            public=json.dumps(to_public(r,route));self.assertNotIn('owner_import',public);self.assertNotIn('attribution_ledger',public);self.assertNotIn('source_doc',public)

if __name__=='__main__':unittest.main()
