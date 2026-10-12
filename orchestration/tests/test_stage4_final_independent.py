"""Fresh final architecture acceptance; no production or fixture ownership."""
import copy
import unittest
from collections import Counter
from dataclasses import replace
from decimal import Decimal
from orchestration.tests import stage4_temporal_fixtures as t, stage4_closing_population as whole
from orchestration.tests import stage4_fixtures as prior
from orchestration.runtime import CAO
from orchestration.reporting_temporal import validate_reporting_temporal
from interfaces.public_output import ROUTES, public_record


class FinalIndependentArchitecture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.blocked=t.intake_initial()
        cls.accepted,cls.record=t.finish(copy.deepcopy(cls.blocked))

    def setUp(self):
        self.f=copy.deepcopy(self.accepted);self.e=self.f['session'];self.n=self.f['nodes']

    def test_natural_intake_and_ordinary_closure(self):
        self.assertTrue(self.f['intake'].validation['accepted'])
        self.assertGreater(len(self.f['raw_sources']),20)
        self.assertEqual((self.f['case'].outcome,self.f['case'].status),('complete','CLOSED'))
        self.assertTrue(self.f['case'].observer_ran)
        self.assertFalse(self.f['case'].open_questions)

    def test_original_material_conflicts_remain_historical(self):
        b=self.blocked;e=b['session']
        self.assertEqual(b['case'].outcome,'partial');self.assertNotEqual(b['case'].status,'CLOSED')
        self.assertEqual(CAO().public(b['case'])['status'],'partial')
        for label in ('elimination','reporting','analytics','group'):
            self.assertEqual(e.versions.current(b['nodes'][label].id).payload()['status'],'blocked')
        for old in self.record['before'].values():self.assertEqual(self.e.versions.versions[old.version_id],old)

    def test_scope_framework_currency_and_repeated_owner_identity(self):
        self.assertEqual({(n.scope_id,n.framework,n.functional_currency or n.presentation_currency) for n in self.n.values()}, {('ENTITY-NL','IFRS','EUR'),('ENTITY-US','US_GAAP','USD'),('ENTITY-UK','UK_GAAP','GBP'),('GROUP-EUR','IFRS','EUR')})
        counts=Counter(n.selected_skill for n in self.n.values())
        self.assertGreater(counts['intercompany-accounting'],8)
        self.assertGreater(counts['financial-statements'],3)
        self.assertEqual(len({n.id for n in self.n.values()}),len(self.n))
        self.e.graph.validate()

    def test_every_current_receipt_exactly_bound(self):
        for key,edge in self.e.edges.items():
            r=self.e.receipt(key);self.e.validate_receipt(r,edge.consumer_node)
            self.assertEqual(dict(self.e.versions.current(edge.consumer_node).dependency_bindings)[key],r['result_version'])
            self.assertEqual(r['result_version'],self.e.versions.current(edge.producer_node).version_id)

    def test_all_receipt_dimensions_refuse_substitution(self):
        for key,edge in self.e.edges.items():
            r=self.e.receipt(key)
            for field in ('producer_scope','consumer_scope','producer_period','consumer_period','result_version','producer_framework','consumer_framework','value_currency','producer_node','consumer_node'):
                with self.subTest(edge=key,field=field),self.assertRaises(ValueError):
                    self.e.validate_receipt(dict(r,**{field:'independent-substitution'}),edge.consumer_node)

    def test_eight_lineages_have_sealed_sources_and_current_edges(self):
        paths=t.lineages(self.f,self.record);self.assertEqual(len(paths),8)
        for p in paths:
            self.assertEqual(p['status'],'ACCEPTED');self.assertTrue(p['source_snapshot'])
            self.assertTrue(p['receipts'])
            for r in p['receipts']:self.e.validate_receipt(r,r['consumer_node'])
        self.assertIn('analytics',paths[-1]['nodes']);self.assertIn('group',paths[-1]['nodes'])

    def test_full_legal_population_and_four_reciprocal_relations(self):
        source=self.e.sources[self.n['elimination'].id]
        self.assertEqual(len(source['group_population_coverage']['required_legal_result_versions']),8)
        self.assertEqual({x['transaction_id'] for x in source['intercompany']},{'clean','mismatch','timing','fx'})
        self.assertEqual({x['id'] for x in source['entities']},{'ENTITY-NL','ENTITY-US','ENTITY-UK'})
        self.assertEqual(len(self.e.versions.current(self.n['elimination'].id).payload()['journal_entry_implications']),6)

    def test_native_cash_profit_and_separate_temporal_stocks(self):
        c=self.e.versions.current(self.n['reporting'].id).payload()['calculations']
        self.assertEqual((c['current']['profit'],c['current']['cash'],c['current']['closing_equity']),('3.00','490.00','490.00'))
        self.assertEqual((c['opening']['cash'],c['opening']['closing_equity']),('490.00','487.00'))
        self.assertEqual((c['comparative']['cash'],c['comparative']['closing_equity']),('489.00','489.00'))
        self.assertEqual(Decimal(c['cash_flow']['financing']),0)
        source=self.e.sources[self.n['reporting'].id]
        for row in source['equity_bridge']:
            self.assertEqual(Decimal(row['retrospective_adjustments']),0)
            self.assertEqual(Decimal(row['owner_transactions']),0)

    def test_three_distinct_native_temporal_versions(self):
        labels=('adjacent-closing','current-opening','reporting')
        self.assertEqual(len({self.e.versions.current(self.n[l].id).version_id for l in labels}),3)
        opening=self.e.periods.get(self.n['current-opening'].period_id)
        self.assertEqual((opening.period_type,opening.start,opening.end),('OPENING','2026-10-01','2026-10-01'))
        self.assertEqual(self.e.periods.get(self.n['adjacent-closing'].period_id).end,'2026-09-30')

    def test_reporting_rejects_equal_value_tb_relabel(self):
        n=self.n['reporting'];source=copy.deepcopy(self.e.sources[n.id]);source['opening_tb'][0]['id']='fabricated-cash'
        with self.assertRaises(ValueError):validate_reporting_temporal(self.e,n,source,[self.e.receipt(k) for k,v in self.e.edges.items() if v.consumer_node==n.id])

    def test_reporting_rejects_dropped_temporal_declarations(self):
        n=self.n['reporting'];source=copy.deepcopy(self.e.sources[n.id]);source.pop('temporal_reporting')
        with self.assertRaises(ValueError):validate_reporting_temporal(self.e,n,source,[self.e.receipt(k) for k,v in self.e.edges.items() if v.consumer_node==n.id])

    def test_current_native_fx_remeasurement_preserves_original16_history(self):
        old=self.record['before']['fx-ENTITY-UK'].payload()['calculations']['pairs'][0]
        current=self.e.versions.current(self.n['fx-ENTITY-UK'].id).payload()['calculations']['pairs'][0]
        self.assertEqual(Decimal(old['a_functional']),16)
        self.assertEqual((Decimal(current['a_functional']),Decimal(current['a_fx_gain'])),(18,2))
        p=self.e.versions.current(self.n['fx-reassessment'].id).payload()
        self.assertEqual((Decimal(p['calculations']['pairs'][0]['a_functional']),Decimal(p['calculations']['pairs'][0]['b_functional'])),(18,18))
        self.assertEqual(p['journal_entry_implications'],[])
        for label in ('whole-translation-ENTITY-US','whole-translation-ENTITY-UK'):
            self.assertEqual(self.e.versions.current(self.n[label].id).payload()['journal_entry_implications'],[])

    def test_mutable_payloads_and_rehearsal_sources_do_not_alias_versions(self):
        n=self.n['reporting'];v=self.e.versions.current(n.id);original=v.payload()
        exposed=v.payload();exposed['calculations']['current']['cash']='999'
        self.assertEqual(v.payload(),original)
        source=copy.deepcopy(self.e.sources[n.id]);source['current_tb'][0]['balance']='999'
        self.assertNotEqual(source,self.e.sources[n.id])
        self.assertEqual(v.payload(),original)

    def test_full_native_exact_once_allocation(self):
        result=whole.exact_once(self.f)
        self.assertNotIn('release_selection',result)
        self.assertEqual(len(result['native_journal_inventory']),8)
        self.assertEqual(len(result['allocation']),8)
        self.assertEqual(Counter(r['posting_scope'] for r in result['allocation']),{'ENTITY-NL':1,'ENTITY-UK':1,'GROUP-EUR':6})

    def test_analytics_dependency_is_part_of_group_version(self):
        key=self.f['edges'][('analytics','group')]
        self.assertEqual(dict(self.e.versions.current(self.n['group'].id).dependency_bindings)[key],self.e.versions.current(self.n['analytics'].id).version_id)
        public=CAO().public(self.f['case'])
        self.assertIn('intervening movements not inferred',str(public))
        self.assertNotIn('financing cash receipt',str(public).lower())

    def test_public_routes_privacy_and_current_result_selection(self):
        for route in ROUTES:
            public=CAO().public(self.f['case'],route)
            self.assertEqual(public['status'],'complete');self.assertEqual(len(public['calculations']),4)
            for token in ('version:','dependency:','case:','exec:','period:','source_fingerprint','reviewer_signoff','qualified_input_snapshot'):
                self.assertNotIn(token,str(public))

    def test_contaminated_public_text_fails_closed(self):
        for route in ROUTES:
            for token in ('version:secret','dependency:secret','result_version','reviewer_signoff','case_id'):
                with self.subTest(route=route,token=token),self.assertRaises(ValueError):public_record({'guidance':token},route=route)

    def test_equal_value_prior_revision_has_exact_selective_rework(self):
        node=self.n['adjacent-closing'];before={k:self.e.versions.current(k) for k in self.e.graph.nodes}
        p=CAO().correct(self.f['case'],node.id,prior.qualified_replacement(self.f,node.id,t.stock_source(self.f,'adjacent-closing')),'Independent reviewed equal-value prior revision')
        self.assertEqual({self.e.graph.nodes[k].logical_id for k in p['execution_order']},{'current-opening','reporting','analytics','group'})
        self.assertEqual(self.f['case'].status,'IN_PROGRESS')
        for k in p['unaffected']:self.assertEqual(self.e.versions.current(k),before[k])
        CAO().selective_reexecute(self.f['case'],p,t.reviewed_rework(self.f,p))
        self.assertEqual(self.f['case'].status,'CLOSED')
        self.assertEqual(self.e.versions.state(before[node.id].version_id),'SUPERSEDED')

    def test_stale_prior_prevents_exact_once_release(self):
        v=self.e.versions.current(self.n['adjacent-closing'].id);self.e.versions.states[v.version_id]='STALE'
        self.assertEqual(whole.exact_once(self.f)['release_selection'],'REFUSED')

    def temporal_attack(self, attack):
        for kind,label,field in [('OPENING','current-opening','opening_tb'),('COMPARATIVE','prior-year-comparative','comparative_tb')]:
            with self.subTest(role=kind):
                f=copy.deepcopy(self.accepted);e=f['session'];n=f['nodes']['reporting'];source=copy.deepcopy(e.sources[n.id])
                receipts=[e.receipt(k) for k,v in e.edges.items() if v.consumer_node==n.id]
                key=f['edges'][(label,'reporting')];r=next(x for x in receipts if x['dependency_id']==key)
                attack(f,e,n,source,receipts,r,kind,label,field,key)
                with self.assertRaises(ValueError):validate_reporting_temporal(e,n,source,receipts)

    def test_both_temporal_roles_missing_receipt(self):
        self.temporal_attack(lambda f,e,n,s,rs,r,*args:rs.remove(r))

    def test_both_temporal_roles_missing_declaration(self):
        self.temporal_attack(lambda f,e,n,s,rs,r,kind,*args:s['temporal_reporting'].pop(kind))

    def test_both_temporal_roles_wrong_scope(self):
        self.temporal_attack(lambda f,e,n,s,rs,r,*args:r.update(producer_scope='ENTITY-US'))

    def test_both_temporal_roles_wrong_period(self):
        self.temporal_attack(lambda f,e,n,s,rs,r,*args:r.update(producer_period=n.period_id))

    def test_both_temporal_roles_wrong_calendar(self):
        def attack(f,e,n,s,rs,r,kind,label,field,key):
            p=r['producer_period'];e.periods.periods[p]=replace(e.periods.get(p),calendar_id='US-FISCAL')
        self.temporal_attack(attack)

    def test_both_temporal_roles_stale(self):
        self.temporal_attack(lambda f,e,n,s,rs,r,*args:e.versions.states.update({r['result_version']:'STALE'}))

    def test_both_temporal_roles_superseded_equal_value(self):
        def attack(f,e,n,s,rs,r,kind,label,field,key):
            from orchestration.governed_plan import observation
            e.execute(f['nodes'][label].id,observation,t.stock_source(f,label),'Independent equal-value temporal revision')
        self.temporal_attack(attack)

    def test_both_temporal_roles_wrong_version(self):
        self.temporal_attack(lambda f,e,n,s,rs,r,*args:r.update(result_version=e.versions.current(f['nodes']['elimination'].id).version_id))

    def test_both_temporal_roles_equal_value_wrong_population(self):
        self.temporal_attack(lambda f,e,n,s,rs,r,kind,label,field,key:s[field][0].update(source_version='unqualified-equal-value-history'))

    def test_both_temporal_roles_substitution(self):
        self.temporal_attack(lambda f,e,n,s,rs,r,kind,*args:s['temporal_reporting'].update({kind:s['temporal_reporting']['COMPARATIVE' if kind=='OPENING' else 'OPENING']}))

    def test_closed_period_replacement_requires_reopening(self):
        n=self.n['adjacent-closing'];self.e.periods.close(n.period_id)
        with self.assertRaises(ValueError):CAO().correct(self.f['case'],n.id,prior.qualified_replacement(self.f,n.id,t.stock_source(self.f,'adjacent-closing')),'Independent closed-period attack')

if __name__=='__main__':unittest.main()
