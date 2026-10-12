"""Independent model review: explicit lineage, not numerical equality, qualifies stocks."""
import copy
import unittest
from decimal import Decimal
from orchestration.tests import stage4_temporal_fixtures as t
from orchestration.runtime import production
from orchestration.reporting_temporal import validate_reporting_temporal
from additional_cases import certify


class IndependentTemporalModel(unittest.TestCase):
    def setUp(self):
        self.f = t.build()

    def native(self, label='adjacent-closing', change=None):
        source = t.stock_source(self.f, label)
        if change:
            change(source)
            source = certify('financial-statements', source)
        return production.assess_case('financial-statements', source)

    def test_gross_original_residuals_survive_boundary(self):
        rows = {x['id']: Decimal(x['balance']) for x in t.stock_source(self.f,'adjacent-closing')['current_tb']}
        self.assertEqual(rows, {'cash':Decimal(490),'mismatch receivable':Decimal(10),'mismatch payable':Decimal(-11),'fx receivable':Decimal(16),'fx payable':Decimal(-18),'equity':Decimal(-487)})
        self.assertEqual(sum(rows.values()), 0)

    def test_prior_year_comparative_is_original_distinct_stock(self):
        s = t.stock_source(self.f,'prior-year-comparative')
        self.assertEqual(s['reporting_period'], '2025-10-31')
        self.assertEqual([(r['id'],r['balance']) for r in s['current_tb']], [('cash','489'),('equity','-489')])
        self.assertNotEqual(s['current_tb'], t.stock_source(self.f,'adjacent-closing')['current_tb'])

    def test_native_supplied_stock_acceptance_is_not_a_year_bridge(self):
        for label in ('adjacent-closing','prior-year-comparative'):
            with self.subTest(label=label):
                result = self.native(label)
                self.assertEqual(result['status'], 'complete')
                self.assertEqual(Decimal(result['calculations']['current']['profit']), 0)
        self.assertNotIn('temporal_bridge',t.stock_source(self.f,'adjacent-closing'))

    def test_adjacent_opening_date_is_required(self):
        r = self.native(change=lambda s:s['opening'].update(period_end='2025-10-31'))
        self.assertEqual(r['status'],'blocked')
        self.assertIn('adjacent prior closing',r['conclusion'])

    def test_zero_cash_review_cannot_cover_actual_nonzero_flow(self):
        r = self.native(change=lambda s:s['cash_flow'].update(financing='1'))
        self.assertEqual(r['status'],'blocked')
        self.assertIn('zero actual movements',r['conclusion'])

    def test_zero_cash_review_requires_evidence(self):
        r = self.native(change=lambda s:s['cash_flow']['zero_movement_review'].update(evidence=[]))
        self.assertEqual(r['status'],'blocked')

    def test_required_temporal_edges_require_declarations_even_without_marker(self):
        e=self.f['session'];n=self.f['nodes']['reporting']
        self.assertEqual({x.dependency_type for x in e.edges.values() if x.consumer_node==n.id},{'CURRENT','QUALIFIED_ALIGNMENT','COMPARATIVE'})
        with self.assertRaises(ValueError):
            validate_reporting_temporal(e,n,{},[])

    def qualified_boundary(self):
        from orchestration.governed_plan import observation
        e=self.f['session'];source={'temporal_reporting':{}}
        closing=self.f['nodes']['adjacent-closing']
        e.execute(closing.id,observation,t.stock_source(self.f,'adjacent-closing'),'Independent prior closing')
        receipts=[]
        for label,kind,field in [('current-opening','OPENING','opening_tb'),('prior-year-comparative','COMPARATIVE','comparative_tb')]:
            n=self.f['nodes'][label];native=t.stock_source(self.f,label)
            e.execute(n.id,observation,native,'Independent boundary reproduction')
            key=self.f['edges'][(label,'reporting')]
            source['temporal_reporting'][kind]=key
            source[field]=copy.deepcopy(native['current_tb'])
            source['opening' if kind=='OPENING' else 'comparative']={'period_end':native['opening']['period_end'] if kind=='OPENING' else n.period[1]}
            receipts.append(e.receipt(key))
        return e,self.f['nodes']['reporting'],source,receipts

    def test_exact_native_boundary_versions_qualify(self):
        e,n,s,r=self.qualified_boundary()
        validate_reporting_temporal(e,n,s,r)

    def test_equal_cash_and_equity_do_not_authorize_substituted_population(self):
        e,n,s,r=self.qualified_boundary()
        s['opening_tb'][1]['id']='unrelated receivable'
        with self.assertRaises(ValueError):validate_reporting_temporal(e,n,s,r)

    def test_native_source_mutation_cannot_retain_result_version(self):
        e,n,s,r=self.qualified_boundary()
        e.sources[r[0]['producer_node']]['current_tb'][0]['source_version']='forged-v2'
        with self.assertRaises(ValueError):validate_reporting_temporal(e,n,s,r)

    def test_exact_receipt_currency_cannot_be_relabelled(self):
        e,n,s,r=self.qualified_boundary();r[0]['value_currency']='USD'
        with self.assertRaises(ValueError):validate_reporting_temporal(e,n,s,r)

    def test_opening_receipt_cannot_be_reused_as_comparative(self):
        e,n,s,r=self.qualified_boundary();s['temporal_reporting']['COMPARATIVE']=s['temporal_reporting']['OPENING']
        with self.assertRaises(ValueError):validate_reporting_temporal(e,n,s,r)

    def test_stale_boundary_version_cannot_be_consumed(self):
        e,n,s,r=self.qualified_boundary();e.versions.states[r[0]['result_version']]='STALE'
        with self.assertRaises(ValueError):validate_reporting_temporal(e,n,s,r)

    def test_superseded_equal_value_boundary_receipt_is_rejected(self):
        from orchestration.governed_plan import observation
        e,n,s,r=self.qualified_boundary();producer=self.f['nodes']['current-opening']
        e.execute(producer.id,observation,t.stock_source(self.f,'current-opening'),'Independent equal-value reviewed revision')
        with self.assertRaises(ValueError):validate_reporting_temporal(e,n,s,r)

    def test_wrong_result_version_is_rejected(self):
        e,n,s,r=self.qualified_boundary();r[0]['result_version']=r[1]['result_version']
        with self.assertRaises(ValueError):validate_reporting_temporal(e,n,s,r)

    def test_wrong_scope_receipt_is_rejected(self):
        e,n,s,r=self.qualified_boundary();r[0]['producer_scope']='ENTITY-US'
        with self.assertRaises(ValueError):validate_reporting_temporal(e,n,s,r)

    def test_wrong_period_receipt_is_rejected(self):
        e,n,s,r=self.qualified_boundary();r[0]['producer_period']=n.period_id
        with self.assertRaises(ValueError):validate_reporting_temporal(e,n,s,r)

    def test_calendar_substitution_is_rejected(self):
        from dataclasses import replace
        e,n,s,r=self.qualified_boundary();key=r[1]['producer_period']
        e.periods.periods[key]=replace(e.periods.get(key),calendar_id='US-FISCAL')
        with self.assertRaises(ValueError):validate_reporting_temporal(e,n,s,r)

    def test_wrong_population_date_is_rejected(self):
        e,n,s,r=self.qualified_boundary();s['opening']['period_end']='2025-10-31'
        with self.assertRaises(ValueError):validate_reporting_temporal(e,n,s,r)

    def test_missing_prior_closing_receipt_blocks_opening(self):
        e,n,s,r=self.qualified_boundary();opening=self.f['nodes']['current-opening']
        native=e.sources[opening.id]
        with self.assertRaises(ValueError):validate_reporting_temporal(e,opening,native,[])

    def test_stale_prior_closing_blocks_current_opening_consumption(self):
        e,n,s,r=self.qualified_boundary();closing=self.f['nodes']['adjacent-closing']
        e.versions.states[e.versions.current(closing.id).version_id]='STALE'
        with self.assertRaises(ValueError):validate_reporting_temporal(e,n,s,r)

    def test_superseded_equal_value_prior_closing_blocks_opening_chain(self):
        from orchestration.governed_plan import observation
        e,n,s,r=self.qualified_boundary();closing=self.f['nodes']['adjacent-closing']
        e.execute(closing.id,observation,t.stock_source(self.f,'adjacent-closing'),'Independent equal-value prior closing revision')
        with self.assertRaises(ValueError):validate_reporting_temporal(e,n,s,r)

    def test_opening_is_distinct_current_boundary_version(self):
        e,n,s,r=self.qualified_boundary();closing=self.f['nodes']['adjacent-closing'];opening=self.f['nodes']['current-opening']
        a=e.versions.current(closing.id);b=e.versions.current(opening.id)
        self.assertNotEqual(a.version_id,b.version_id)
        self.assertEqual(e.periods.get(opening.period_id).period_type,'OPENING')
        self.assertEqual(e.periods.get(opening.period_id).start,'2026-10-01')
        self.assertEqual(b.dependency_bindings,((self.f['edges'][('adjacent-closing','current-opening')],a.version_id),))

    def test_explicit_opening_alignment_alone_requires_temporal_declarations(self):
        e=self.f['session'];n=self.f['nodes']['reporting']
        del e.edges[self.f['edges'][('prior-year-comparative','reporting')]]
        with self.assertRaises(ValueError):validate_reporting_temporal(e,n,{},[])

    def test_equal_value_relabel_does_not_supply_missing_receipts(self):
        e=self.f['session'];n=self.f['nodes']['reporting']
        s={'temporal_reporting':{'OPENING':self.f['edges'][('current-opening','reporting')], 'COMPARATIVE':self.f['edges'][('prior-year-comparative','reporting')]},'opening_tb':copy.deepcopy(t.stock_source(self.f,'adjacent-closing')['current_tb'])}
        s['comparative_tb']=copy.deepcopy(s['opening_tb'])
        with self.assertRaises(ValueError):validate_reporting_temporal(e,n,s,[])


if __name__ == '__main__': unittest.main()
