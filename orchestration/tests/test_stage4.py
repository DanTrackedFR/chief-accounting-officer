"""Authored integrated lifecycle acceptance; release/independent QA separate."""
import copy
import unittest
from dataclasses import replace
from orchestration.tests.stage4_fixtures import correct
from orchestration.tests.stage4_temporal_fixtures import initial, intake_initial, finish

def rework(f,plan):
    # Positive acceptance now includes separately reviewed treasury correction;
    # retained incomplete fixtures continue to prove safe population rejection.
    _,record=finish(f,plan);f['accepted_lifecycle']=record;return record['ledger']
from orchestration.tests.stage3_fixtures import sides
from orchestration.runtime import CAO


class Stage4Lifecycle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.base=initial()
    def setUp(self):
        self.f=copy.deepcopy(self.base);self.e=self.f['session'];self.n=self.f['nodes']
    def test_real_material_conflict_remains_partial(self):
        self.assertEqual(self.f['case'].outcome,'partial');self.assertNotEqual(self.f['case'].status,'CLOSED')
        self.assertEqual([s.transaction_amount for s in sides(self.f,'mismatch')],['10','11'])
    def test_actual_group_accounting_reporting_analytics_blocked(self):
        for label in ('uk-conversion','elimination','reporting','group','analytics'):
            v=self.e.versions.current(self.n[label].id)
            self.assertEqual(v.payload()['status'],'blocked');self.assertEqual(v.payload()['journal_entry_implications'],[])
    def test_qualified_correction_reaches_ordinary_closed_case(self):
        p=correct(self.f);ledger=rework(self.f,p)
        self.assertEqual(self.f['case'].outcome,'complete');self.assertEqual(self.f['case'].status,'CLOSED')
        self.assertEqual(len(ledger),9)
        self.assertTrue(self.f['case'].observer_ran);self.assertTrue(self.f['case'].artifacts)
    def test_actual_selective_rework_set(self):
        p=correct(self.f)
        self.assertEqual({self.e.graph.nodes[k].logical_id for k in p['execution_order']},{'match-mismatch','uk-conversion','elimination','reporting','group','analytics'})
        for label in ('translation','conversion','clean-ENTITY-US','match-clean','match-fx','match-timing','nl-opening','nl-comparative'):
            self.assertIn(self.n[label].id,p['unaffected'])
    def test_exact_old_results_preserved_immutably(self):
        v=self.e.versions.current(self.n['mismatch-ENTITY-NL'].id);payload=v.payload();p=correct(self.f);rework(self.f,p)
        self.assertEqual(self.e.versions.versions[v.version_id].payload(),payload)
        self.assertEqual(self.e.versions.state(v.version_id),'SUPERSEDED')
        self.assertEqual(self.e.versions.current(v.node_id).predecessor,v.version_id)
    def test_unrelated_results_are_not_reexecuted(self):
        before={key:(v,self.e.graph.nodes[key].iterations) for key in self.e.graph.nodes if (v:=self.e.versions.current(key)) is not None}
        p=correct(self.f);rework(self.f,p)
        record=self.f['accepted_lifecycle']
        for key in record['closing_correction']['unaffected']:self.assertEqual(record['before_closing'][key],(self.e.versions.current(key),self.e.graph.nodes[key].iterations))
    def test_owner_group_result_replayed_not_hardcoded(self):
        p=correct(self.f);rework(self.f,p);v=self.e.versions.current(self.n['reporting'].id)
        self.assertEqual(v.payload()['calculations']['current']['closing_equity'],'490.00')
        self.assertEqual(v.payload()['calculations']['current']['profit'],'3.00')
        self.assertEqual(v.payload()['calculations']['current']['cash'],'490.00')
    def test_frameworks_currencies_remain_distinct(self):
        values={(n.scope_id,n.framework,n.functional_currency or n.presentation_currency) for n in self.n.values()}
        self.assertEqual(values,{('ENTITY-NL','IFRS','EUR'),('ENTITY-US','US_GAAP','USD'),('ENTITY-UK','UK_GAAP','GBP'),('GROUP-EUR','IFRS','EUR')})
    def test_wrong_scope_period_case_receipt_rejected(self):
        r=self.e.receipt(self.f['edges'][('clean-ENTITY-US','translation')])
        for field in ('producer_scope','consumer_scope','producer_period','consumer_period','result_version','producer_framework','value_currency'):
            with self.subTest(field=field),self.assertRaises(ValueError):self.e.validate_receipt(dict(r,**{field:'wrong'}),r['consumer_node'])
    def test_sibling_case_result_substitution_rejected(self):
        edge=self.e.edges[self.f['edges'][('mismatch-ENTITY-NL','match-mismatch')]]
        with self.assertRaises(ValueError):replace(edge,producer_case=self.n['mismatch-ENTITY-UK'].case_id).validate(self.e.graph,self.e.cases,self.e.periods)
    def test_stale_receipt_cannot_survive_material_correction(self):
        r=self.e.receipt(self.f['edges'][('mismatch-ENTITY-NL','match-mismatch')]);correct(self.f)
        with self.assertRaises(ValueError):self.e.validate_receipt(r,r['consumer_node'])
    def test_wrong_topological_order_cannot_reexecute(self):
        p=correct(self.f);bad=copy.deepcopy(p);bad['execution_order'].reverse()
        with self.assertRaises(ValueError):CAO().selective_reexecute(self.f['case'],bad)
    def test_unrelated_owner_cannot_be_added_to_rework(self):
        p=correct(self.f);bad=copy.deepcopy(p);bad['execution_order'].append(self.n['translation'].id)
        with self.assertRaises(ValueError):CAO().selective_reexecute(self.f['case'],bad)
    def test_native_reviewer_bypass_cannot_correct(self):
        from orchestration.tests.stage4_fixtures import legal_source
        c=legal_source(self.f,'mismatch','ENTITY-NL',True);c['reviewer_signoff']['approved']=False
        with self.assertRaises(ValueError):CAO().correct(self.f['case'],self.n['mismatch-ENTITY-NL'].id,c,'Attack')
    def test_equal_value_wrong_counterparty_rejected(self):
        s=sides(self.f,'mismatch')[0]
        with self.assertRaises(ValueError):replace(s,counterparty_scope='ENTITY-US').validate(self.e)
    def test_network_business_cycle_does_not_add_execution_cycle(self):
        from orchestration.tests.stage3_fixtures import network
        self.assertTrue(network(self.f).has_business_cycle());self.e.graph.validate()
    def test_opening_comparative_exact_prior_result_preserved(self):
        for label,typ in [('nl-opening','OPENING'),('nl-comparative','COMPARATIVE')]:
            n=self.n[label];edge=next(e for e in self.e.edges.values() if e.consumer_node==n.id)
            self.assertEqual(edge.dependency_type,typ);v=self.e.versions.current(n.id)
            self.assertEqual(v.payload()['observed_amount'],'30.00');self.assertTrue(v.dependency_bindings)
    def test_closed_period_correction_requires_reopening(self):
        n=self.n['mismatch-ENTITY-NL'];self.e.periods.close(n.period_id)
        with self.assertRaises(ValueError):correct(self.f)
    def test_historical_blocked_report_is_superseded(self):
        old=self.e.versions.current(self.n['reporting'].id);p=correct(self.f);rework(self.f,p)
        self.assertEqual(self.e.versions.state(old.version_id),'SUPERSEDED')
        self.assertEqual(old.payload()['status'],'blocked')
    def test_corrected_receipts_use_actual_replacement_versions(self):
        p=correct(self.f);rework(self.f,p)
        for key in self.e.edges:
            r=self.e.receipt(key);self.e.validate_receipt(r,r['consumer_node'])
            self.assertEqual(r['result_version'],self.e.versions.current(r['producer_node']).version_id)


class Stage4Intake(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from orchestration.tests.stage4_temporal_fixtures import intake_initial
        cls.base=intake_initial()
    def setUp(self):self.f=copy.deepcopy(self.base)
    def test_objective_intake_preserves_controlled_sources_and_work_modes(self):
        self.assertEqual(self.f['case'].outcome,'partial')
        self.assertTrue(self.f['intake'].validation['accepted'])
        self.assertGreater(len(self.f['raw_sources']),20)
        self.assertEqual(self.f['case'].work_modes['primary'],'CLOSE_REVIEW')
        self.assertIn('DIAGNOSTIC_ANALYTICS',self.f['case'].work_modes['secondary'])
    def test_intake_correction_closes_same_governed_graph(self):
        p=correct(self.f);rework(self.f,p)
        self.assertEqual(self.f['case'].status,'CLOSED')
    def attack(self,change):
        engine=self.f['intake_engine'];prepared=self.f['intake'];pack=self.f['reviewed_pack']
        change(pack)
        with self.assertRaises(ValueError):engine.execute(prepared,pack)
    def test_reused_reviewed_pack_rejected(self):
        self.attack(lambda p:p.scoped_packs.append(copy.deepcopy(p.scoped_packs[0])))
    def test_wrong_reviewed_pack_scope_rejected(self):
        self.attack(lambda p:setattr(p.scoped_packs[0],'scope_id','ENTITY-UK'))
    def test_wrong_reviewed_pack_period_rejected(self):
        self.attack(lambda p:setattr(p.scoped_packs[0],'period_id','period:wrong'))
    def test_wrong_fiscal_calendar_rejected(self):
        self.attack(lambda p:setattr(p.scoped_packs[0],'calendar_id','Wrong-calendar'))
    def test_wrong_source_input_selected_rejected(self):
        self.attack(lambda p:p.scoped_packs[0].request.update(source=p.scoped_packs[1].request['source']))
    def test_material_node_omission_rejected(self):
        self.attack(lambda p:p.scoped_packs.pop())
    def test_hidden_native_population_change_rejected(self):
        def change(p):
            child=next(c for c in p.scoped_packs if c.request['source'].get('translation'))
            source=child.request['source'];source['translation']['tb'][0]['balance']='101'
            p.request['governed_plan']['sources'][child.request['node_id']]=copy.deepcopy(source)
        self.attack(change)
    def test_source_manifest_omission_rejected(self):
        def change(p):
            child=next(c for c in p.scoped_packs if c.bindings)
            child.request['source']['qualified_scope_sources']=[]
            p.request['governed_plan']['sources'][child.request['node_id']]=copy.deepcopy(child.request['source'])
        self.attack(change)
    def test_source_economic_identity_reuse_rejected(self):
        def change(p):
            child=next(c for c in p.scoped_packs if c.bindings and 'pairs' in c.request['source'])
            child.request['source']['economic_id']='unrelated'
            p.request['governed_plan']['sources'][child.request['node_id']]=copy.deepcopy(child.request['source'])
        self.attack(change)


class Stage4PublicAndEconomics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from orchestration.tests.stage4_temporal_fixtures import intake_initial
        cls.base=intake_initial();cls.clean=copy.deepcopy(cls.base);cls.plan=correct(cls.clean);rework(cls.clean,cls.plan)
    def test_conflict_answer_cannot_claim_group_report_supported(self):
        p=CAO().public(self.base['case']);self.assertEqual(p['status'],'partial');self.assertNotIn('calculations',p)
        self.assertIn('not yet supportable',p['guidance']);self.assertIn('10 EUR million versus 11 EUR million',str(p))
    def test_clean_answer_has_native_totals_and_analytics_with_units(self):
        p=CAO().public(self.clean['case']);self.assertEqual(p['status'],'complete')
        self.assertIn('490.00',str(p));self.assertIn('EUR millions',str(p));self.assertIn('Observed prior-year cash stock difference',str(p));self.assertNotIn('financing cash receipt',str(p))
    def test_public_routes_preserve_same_private_boundary(self):
        from interfaces.public_output import ROUTES
        for route in ROUTES:
            p=CAO().public(self.clean['case'],route)
            for token in ('version:','dependency:','period:','case:','exec:','synthetic accounting reviewer','reviewer_signoff','source_fingerprint'):
                self.assertNotIn(token,str(p))
    def test_public_text_internals_fail_closed(self):
        from interfaces.public_output import public_record,ROUTES
        tokens=['exec:secret','version:secret','period:secret','case:secret','dependency:secret','node_id','case_id','result_version','reviewer_signoff','evidence_tier','routing_metadata','semantic_metadata']
        for route in ROUTES:
            for token in tokens:
                with self.subTest(route=route,token=token),self.assertRaises(ValueError):public_record(dict(guidance=token),route=route)
    def test_exact_once_current_layers_and_translation_dispositions(self):
        from orchestration.tests.stage4_fixtures import journal_ledger
        j=journal_ledger(self.clean);self.assertEqual(len(j['selected']),8)
        self.assertEqual(sum(r['posting_scope']=='ENTITY-NL' for r in j['allocation']),1)
        self.assertEqual(sum(r['posting_scope']=='GROUP-EUR' for r in j['allocation']),6)
        self.assertEqual(sum(r['posting_scope']=='ENTITY-UK' for r in j['allocation']),1)
        self.assertEqual(len(j['dispositions']),2)
    def test_posting_alias_duplication_rejected(self):
        from orchestration.tests.stage4_fixtures import journal_ledger
        from orchestration.scoped_journals import allocate_scoped
        j=journal_ledger(self.clean);f=copy.deepcopy(self.clean);e=f['session']
        duplicate=copy.deepcopy(j['events'][0]);duplicate['economic_id']='alias'
        # Same current journal cannot appear twice under unrelated event labels.
        events=j['events']+[duplicate]
        context=dict(entity='GROUP-EUR',framework='IFRS',jurisdiction='NL',currency='EUR',period_start='2026-10-01',reporting_period='2026-10-31',scopes=e.cases.scopes.record(),period_registry=e.periods.record())
        with self.assertRaises(ValueError):f['basis'].current_journals(context,events,j['dispositions'])
    def test_qualified_native_transformation_paths(self):
        from orchestration.tests.stage4_fixtures import transforms
        f=copy.deepcopy(self.clean);rs=transforms(f);self.assertEqual(len(rs),4)
        for r in rs:f['basis'].validate_transformation(r)
        self.assertEqual({r['source_framework'] for r in rs if r['kind']=='FRAMEWORK_CONVERSION'},{'US_GAAP','UK_GAAP'})
    def test_current_unsupported_general_conversion_fails_closed(self):
        e=self.clean['session'];v=e.versions.current(self.clean['nodes']['clean-ENTITY-US'].id)
        self.assertEqual(self.clean['basis'].unsupported_conversion(v.version_id,'IFRS','general')['status'],'unresolved')
