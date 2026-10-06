"""Authored integrated lifecycle acceptance; release/independent QA separate."""
import copy
import unittest
from dataclasses import replace
from orchestration.tests.stage4_fixtures import initial,correct,rework
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
        self.assertEqual(len(ledger),6)
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
        for key in p['unaffected']:self.assertEqual(before[key],(self.e.versions.current(key),self.e.graph.nodes[key].iterations))
    def test_owner_group_result_replayed_not_hardcoded(self):
        p=correct(self.f);rework(self.f,p);v=self.e.versions.current(self.n['reporting'].id)
        self.assertEqual(v.payload()['calculations']['current']['closing_equity'],'490.00')
        self.assertEqual(v.payload()['calculations']['current']['profit'],'1.00')
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
