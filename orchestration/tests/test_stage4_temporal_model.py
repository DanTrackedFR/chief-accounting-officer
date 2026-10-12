import copy
import unittest
from orchestration.tests import stage4_temporal_fixtures as temporal, stage4_closing_population as whole
from orchestration.runtime import CAO


class TemporalIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.f,cls.record=temporal.run()

    def test_native_reporting_and_case_close(self):
        self.assertEqual((self.f['case'].outcome,self.f['case'].status),('complete','CLOSED'))
        self.assertEqual(self.f['case'].open_questions,[])

    def test_distinct_opening_and_comparative_stocks(self):
        f=self.f;e=f['session'];p=e.versions.current(f['nodes']['reporting'].id).payload()['calculations']
        self.assertEqual((p['opening']['closing_equity'],p['opening']['cash']),('487.00','490.00'))
        self.assertEqual((p['comparative']['closing_equity'],p['comparative']['cash']),('489.00','489.00'))

    def test_current_accounting_preserved(self):
        p=self.f['session'].versions.current(self.f['nodes']['reporting'].id).payload()['calculations']['current']
        self.assertEqual((p['profit'],p['closing_equity'],p['cash']),('3.00','490.00','490.00'))

    def test_public_answer_uses_current_reporting_only(self):
        p=CAO().public(self.f['case'])
        self.assertEqual(p['status'],'complete');self.assertEqual(len(p['calculations']),4)
        self.assertNotIn('not yet supportable',p['guidance'])

    def test_no_intervening_financing_event_asserted(self):
        p=CAO().public(self.f['case'])
        self.assertFalse(any('financing cash receipt' in x.lower() for x in p['reporting']))
        self.assertTrue(any('intervening movements not inferred' in x for x in p['reporting']))

    def test_original_versions_are_immutable(self):
        e=self.f['session']
        for v in self.record['before'].values():self.assertEqual(e.versions.versions[v.version_id],v)

    def test_temporal_versions_do_not_refresh_for_current_fx_correction(self):
        for label in ('current-opening','prior-year-comparative'):
            old=self.record['before'][label]
            self.assertEqual(self.f['session'].versions.current(old.node_id),old)

    def test_temporal_receipts_are_exact(self):
        f=self.f;e=f['session'];v=e.versions.current(f['nodes']['reporting'].id)
        for label in ('current-opening','prior-year-comparative'):
            key=f['edges'][(label,'reporting')];r=e.receipt(key);e.validate_receipt(r,v.node_id)
            self.assertEqual(dict(v.dependency_bindings)[key],r['result_version'])

    def test_adjacent_dates_and_calendar(self):
        e=self.f['session'];key=self.f['edges'][('adjacent-closing','current-opening')];edge=e.edges[key]
        self.assertEqual((e.periods.get(edge.producer_period).end,e.periods.get(edge.consumer_period).start),('2026-09-30','2026-10-01'))
        self.assertEqual(e.periods.get(edge.producer_period).calendar_id,e.periods.get(edge.consumer_period).calendar_id)

    def test_exact_once_full_release(self):
        result=whole.exact_once(self.f)
        self.assertNotIn('release_selection',result);self.assertEqual(len(result['native_journal_inventory']),8)
        self.assertEqual(len(result['allocation']),8)

    def test_equal_value_temporal_revision_invalidates_only_consumers(self):
        f=copy.deepcopy(self.f);e=f['session'];n=f['nodes']['adjacent-closing']
        from orchestration.tests import stage4_fixtures as s4
        p=CAO().correct(f['case'],n.id,s4.qualified_replacement(f,n.id,temporal.stock_source(f,'adjacent-closing')),'Separate reviewed equal-value source revision')
        self.assertEqual(set(p['direct']),{f['nodes']['current-opening'].id})
        self.assertEqual(set(p['execution_order']),{f['nodes'][x].id for x in ('current-opening','reporting','analytics','group')})
        for key in p['unaffected']:self.assertEqual(e.versions.state(e.versions.current(key).version_id),'CURRENT')
        CAO().selective_reexecute(f['case'],p,temporal.reviewed_rework(f,p));self.assertEqual(f['case'].status,'CLOSED')
