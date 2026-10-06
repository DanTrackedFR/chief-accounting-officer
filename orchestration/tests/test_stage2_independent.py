"""Independent Stage 2 attacks derived from live governance boundaries."""
import copy
import unittest
from dataclasses import replace
from orchestration.tests.stage2_fixtures import build, initial, correction, public
from orchestration.periods import Period, PeriodRelationship, EffectiveInterval
from orchestration.cases import case_identity
from orchestration.runtime import Case

class IndependentStage2(unittest.TestCase):
    def setUp(self):
        self.f=initial(build()); self.e=self.f['coordinator'];self.n=self.f['nodes'];self.p=self.f['periods']

    def test_scope_calendar_case_substitution_rejected(self):
        period=self.p['CALENDAR-SEP'];objective='Wrong-calendar investigation'
        case=Case(case_identity('ENTITY-US',period.period_id,objective,'new'),objective)
        with self.assertRaises(ValueError):
            self.e.cases.register(case,'ENTITY-US',period.period_id,'new',provenance=('review',))

    def test_required_blocked_node_with_current_version_blocks_parent(self):
        self.n['US-OPEN'].status='blocked'
        self.e.cases.refresh(self.e.graph,self.e.versions,self.e.edges)
        self.assertNotEqual(self.e.cases.get(self.n['GROUP'].case_id).outcome,'complete')

    def test_bound_result_must_belong_to_declared_producer(self):
        node=self.n['US-REPORT'];edge=next(e for e in self.e.edges.values() if e.consumer_node==node.id)
        uk=self.e.versions.current(self.n['UK-SEP'].id)
        with self.assertRaises(ValueError):
            self.e.versions.publish(node,node.result,{'reviewed':'source'},[(edge.id,uk.version_id)],'Wrong producer attack')

    def test_reopened_period_can_close_preserving_identity(self):
        n=self.n['US-SEP'];self.e.periods.close(n.period_id)
        self.e.periods.reopen(n.period_id,'Correction',{'status':'APPROVED','evidence':['review'],'convention':'SYNTHETIC_GOVERNED'},[n.case_id],[n.id])
        self.e.periods.close(n.period_id)
        self.assertEqual(self.e.periods.status[n.period_id],'CLOSED')
        self.assertEqual(len(self.e.periods.reopenings),1)

    def test_bounded_executor_wrong_scope_source_rejected(self):
        n=self.n['UK-CONTROL'];source=copy.deepcopy(self.f['sources'][n.id]);source['scope_id']='ENTITY-US'
        with self.assertRaises(ValueError):self.e.execute(n.id,self.f['executors'][n.id],source,'Wrong Scope source')

    def test_bounded_executor_wrong_period_source_rejected(self):
        n=self.n['UK-CONTROL'];source=copy.deepcopy(self.f['sources'][n.id]);source['period_id']=self.p['CALENDAR-OCT'].period_id
        with self.assertRaises(ValueError):self.e.execute(n.id,self.f['executors'][n.id],source,'Wrong Period source')

    def test_effective_interval_wrong_scope_calendar_rejected(self):
        partial=Period.create('US-FISCAL','2026-10-15','2026-10-31',2027,'04-INCLUSION','PARTIAL_INCLUDED_PERIOD',provenance=('review',))
        self.e.periods.periods[partial.period_id]=partial
        interval=EffectiveInterval('ENTITY-NL','business-combinations',self.p['US-FISCAL-OCT'].period_id,partial.period_id,'ACQUISITION','2026-10-15',('review',))
        with self.assertRaises(ValueError):interval.validate(self.e.periods,self.e.cases.scopes)

    def test_same_amount_superseded_receipt_rejected(self):
        n=self.n['US-SEP'];edge=next(e.id for e in self.e.edges.values() if e.producer_node==n.id);r=self.e.receipt(edge)
        self.e.execute(n.id,self.f['executors'][n.id],self.f['sources'][n.id],'Same-value new review')
        with self.assertRaises(ValueError):self.e.validate_receipt(r,self.n['US-REPORT'].id)

    def test_stale_closed_case_enters_rework_with_history(self):
        group=self.e.cases.get(self.n['GROUP'].case_id);self.assertEqual(group.status,'CLOSED')
        correction(self.f)
        self.assertEqual(group.status,'IN_PROGRESS');self.assertTrue(group.governance_history);self.assertTrue(group.rework_state)

    def test_reopening_nothing_else_stales(self):
        before=copy.deepcopy(self.e.versions.states);n=self.n['US-SEP'];self.e.periods.close(n.period_id)
        self.e.periods.reopen(n.period_id,'review',{'status':'APPROVED','evidence':['review'],'convention':'SYNTHETIC_GOVERNED'},[n.case_id],[n.id])
        self.assertEqual(before,self.e.versions.states)

    def test_transitive_rework_topological_and_uk_identity_unchanged(self):
        uk=self.e.versions.current(self.n['UK-SEP'].id);plan=correction(self.f)
        order=plan['execution_order'];self.assertEqual(order,[self.n[k].id for k in ('US-REPORT','US-OPEN','GROUP','ANALYTICS')])
        self.e.reexecute(plan,self.f['executors'],self.f['sources'])
        self.assertEqual(uk,self.e.versions.current(uk.node_id));self.assertEqual(public(self.f)['calculations'][0]['amount'],'900.00')

    def test_dependency_cycle_rollback(self):
        edge=next(e for e in self.e.edges.values() if e.producer_node==self.n['GROUP'].id)
        backwards=replace(edge,producer_node=edge.consumer_node,consumer_node=edge.producer_node,producer_case=edge.consumer_case,consumer_case=edge.producer_case,producer_scope=edge.consumer_scope,consumer_scope=edge.producer_scope,producer_period=edge.consumer_period,consumer_period=edge.producer_period)
        before=copy.deepcopy(self.n['GROUP'].dependencies)
        with self.assertRaises(ValueError):self.e.add_dependency(backwards)
        self.assertEqual(before,self.n['GROUP'].dependencies)

    def test_wrong_opening_scope_rejected(self):
        edge=next(e for e in self.e.edges.values() if e.dependency_type=='OPENING')
        with self.assertRaises(ValueError):replace(edge,producer_scope='ENTITY-UK').validate(self.e.graph,self.e.cases,self.e.periods)

    def test_partial_disposal_date_mismatch_rejected(self):
        with self.assertRaises(ValueError):replace(self.f['interval'],effective_event='DISPOSAL').validate(self.e.periods,self.e.cases.scopes)

    def test_period_id_provenance_independent_dates_calendar_sensitive(self):
        a=self.p['CALENDAR-SEP'];b=Period.create(a.calendar_id,a.start,a.end,a.fiscal_year,a.fiscal_period,provenance=('new-review',))
        self.assertEqual(a.period_id,b.period_id);self.assertNotEqual(a.period_id,self.p['US-FISCAL-SEP'].period_id)

    def test_history_payload_defensive_copy(self):
        v=self.e.versions.current(self.n['US-SEP'].id);payload=v.payload();payload['calculations']['period_revenue']='999'
        self.assertEqual(v.payload()['calculations']['period_revenue'],'800.00')

    def journal_inputs(self):
        context=dict(entity='GROUP-EUR',framework='IFRS',jurisdiction='NL',currency='EUR',period_start='2026-10-01',reporting_period='2026-10-31',scopes=self.e.cases.scopes.record(),period_registry=self.e.periods.record())
        events=[]
        for label in ('US-SEP','UK-SEP','US-OCT'):
            n=self.n[label];v=self.e.versions.current(n.id)
            for i,j in enumerate(v.payload()['journal_entry_implications']):
                events.append(dict(economic_id=label+'-event-'+str(i),posting_scope=n.scope_id,period=n.period,currency=n.functional_currency,period_id=n.period_id,result_version=v.version_id,primary=[dict(owner=n.id,index=i)],witnesses=[],evidence='reviewed source event'))
        return context,events

    def test_current_journals_complete_population(self):
        context,events=self.journal_inputs();selected,ledger=self.e.current_journals(context,events)
        self.assertEqual(len(selected),18);self.assertEqual(len(ledger),18)

    def test_superseded_journal_event_rejected(self):
        context,events=self.journal_inputs();plan=correction(self.f);self.e.reexecute(plan,self.f['executors'],self.f['sources'])
        with self.assertRaises(ValueError):self.e.current_journals(context,events)

    def test_current_journal_relabel_period_rejected(self):
        context,events=self.journal_inputs();events[0]['period_id']=self.p['US-FISCAL-OCT'].period_id
        with self.assertRaises(ValueError):self.e.current_journals(context,events)

    def test_duplicate_journal_alias_rejected(self):
        context,events=self.journal_inputs();duplicate=copy.deepcopy(events[0]);duplicate['economic_id']='alias';events.append(duplicate)
        with self.assertRaises(ValueError):self.e.current_journals(context,events)

    def test_new_journals_once_history_not_extra_postings(self):
        correction(self.f);self.e.reexecute(self.e.rework_history[-1],self.f['executors'],self.f['sources']);context,events=self.journal_inputs()
        selected,ledger=self.e.current_journals(context,events);self.assertEqual(len(selected),18)
        self.assertEqual(next(j for j in selected if j['owner']==self.n['US-SEP'].id)['lines'][0]['amount'],'900.00')

    def test_public_serialization_omits_internal_dependency_version(self):
        import json
        correction(self.f);self.e.reexecute(self.e.rework_history[-1],self.f['executors'],self.f['sources']);value=json.dumps(public(self.f))
        for key in ('version:', 'dependency:', 'case:', 'fingerprint', 'reviewer', 'SUPERSEDED', 'STALE'):self.assertNotIn(key,value)

    def test_graph_build_determinism(self):
        other=initial(build())['coordinator'];self.assertEqual(self.e.versions.record(),other.versions.record());self.assertEqual(sorted(self.e.edges),sorted(other.edges))

    def test_case_objective_identity_is_distinct(self):
        n=self.n['US-SEP'];self.assertNotEqual(case_identity(n.scope_id,n.period_id,'Other objective','controlled-close'),n.case_id)

    def test_case_scope_substitution_identity_rejected(self):
        c=self.e.cases.get(self.n['US-SEP'].case_id)
        with self.assertRaises(ValueError):self.e.cases.register(Case(c.id,c.objective),'ENTITY-UK',c.period_id,c.cycle,provenance=('review',))

    def test_case_period_substitution_identity_rejected(self):
        c=self.e.cases.get(self.n['US-SEP'].case_id)
        with self.assertRaises(ValueError):self.e.cases.register(Case(c.id,c.objective),c.scope_id,self.p['US-FISCAL-OCT'].period_id,c.cycle,provenance=('review',))

    def test_undeclared_child_consumption_rejected(self):
        edge=next(e for e in self.e.edges.values() if e.consumer_node==self.n['GROUP'].id)
        with self.assertRaises(ValueError):replace(edge,consumption='SAME_CASE').validate(self.e.graph,self.e.cases,self.e.periods)

    def test_wrong_parent_consumption_rejected(self):
        edge=next(e for e in self.e.edges.values() if e.consumer_node==self.n['GROUP'].id)
        self.e.cases.get(edge.producer_case).parent_case_id=self.n['UK-SEP'].case_id
        with self.assertRaises(ValueError):edge.validate(self.e.graph,self.e.cases,self.e.periods)

    def test_comparative_future_source_rejected(self):
        with self.assertRaises(ValueError):self.e.periods.add_relationship(PeriodRelationship(self.p['CALENDAR-OCT'].period_id,self.p['CALENDAR-SEP'].period_id,'COMPARATIVE',('review',)))

    def test_included_period_outside_source_rejected(self):
        with self.assertRaises(ValueError):replace(self.f['interval'],source_period=self.p['CALENDAR-SEP'].period_id).validate(self.e.periods,self.e.cases.scopes)

    def test_new_dependency_cannot_leave_already_current_consumer_unbound(self):
        edge=next(e for e in self.e.edges.values() if e.consumer_node==self.n['ANALYTICS'].id)
        uk=self.n['UK-SEP'];consumer=self.n['UK-CONTROL']
        new=replace(edge,producer_node=uk.id,consumer_node=consumer.id,producer_case=uk.case_id,consumer_case=consumer.case_id,producer_scope=uk.scope_id,consumer_scope=consumer.scope_id,producer_period=uk.period_id,consumer_period=consumer.period_id,metric_path=('calculations','period_revenue'))
        try:self.e.add_dependency(new)
        except ValueError:return
        current=self.e.versions.current(consumer.id,allow_stale=True)
        self.assertNotEqual(self.e.versions.state(current.version_id),'CURRENT')

    def test_required_binding_cannot_be_omitted_on_publish(self):
        n=self.n['US-REPORT']
        with self.assertRaises(ValueError):self.e.versions.publish(n,n.result,{'reviewed':'source'},[],'Omit required dependency attack')

    def test_period_relationship_cycle_rejected(self):
        a=self.p['CALENDAR-SEP'].period_id;b=self.p['CALENDAR-OCT'].period_id
        self.e.periods.add_relationship(PeriodRelationship(a,b,'CURRENT',('review',)))
        with self.assertRaises(ValueError):self.e.periods.add_relationship(PeriodRelationship(b,a,'CURRENT',('review',)))

    def test_equal_amount_stale_group_receipt_rejected(self):
        edge=next(e.id for e in self.e.edges.values() if e.consumer_node==self.n['GROUP'].id);receipt=self.e.receipt(edge)
        self.e.execute(self.n['US-SEP'].id,self.f['executors'][self.n['US-SEP'].id],self.f['sources'][self.n['US-SEP'].id],'Same amount reviewed new source')
        with self.assertRaises(ValueError):self.e.validate_receipt(receipt,self.n['GROUP'].id)

    def test_wrong_period_receipt_equal_amount_rejected(self):
        edge=next(e.id for e in self.e.edges.values() if e.consumer_node==self.n['US-REPORT'].id);receipt=self.e.receipt(edge)
        receipt['producer_period']=self.p['US-FISCAL-OCT'].period_id
        with self.assertRaises(ValueError):self.e.validate_receipt(receipt,self.n['US-REPORT'].id)

    def test_supersession_lineage_cannot_skip_predecessor(self):
        old=self.e.versions.current(self.n['UK-SEP'].id);correction(self.f);new=self.e.versions.current(self.n['US-SEP'].id)
        with self.assertRaises(ValueError):self.e.invalidate(old.version_id,new.version_id)

    def test_rework_plan_unrelated_append_rejected(self):
        plan=copy.deepcopy(correction(self.f));plan['execution_order'].append(self.n['UK-CONTROL'].id)
        with self.assertRaises(ValueError):self.e.reexecute(plan,self.f['executors'],self.f['sources'])

    def test_rework_plan_reverse_order_rejected(self):
        plan=copy.deepcopy(correction(self.f));plan['execution_order'].reverse()
        with self.assertRaises(ValueError):self.e.reexecute(plan,self.f['executors'],self.f['sources'])

    def test_closed_period_ordinary_execution_rejected(self):
        n=self.n['US-SEP'];self.e.periods.close(n.period_id);old=self.e.versions.current(n.id)
        with self.assertRaises(ValueError):self.e.execute(n.id,self.f['executors'][n.id],self.f['sources'][n.id],'ordinary rewrite')
        self.assertEqual(old,self.e.versions.current(n.id))

    def test_reopening_creates_no_accounting_reversal(self):
        n=self.n['US-SEP'];old=self.e.versions.current(n.id).payload()['journal_entry_implications'];self.e.periods.close(n.period_id)
        self.e.periods.reopen(n.period_id,'review',{'status':'APPROVED','evidence':['review'],'convention':'SYNTHETIC_GOVERNED'},[n.case_id],[n.id])
        self.assertEqual(old,self.e.versions.current(n.id).payload()['journal_entry_implications'])

    def test_repeated_production_owner_scope_and_period_independence(self):
        nodes=[self.n[k] for k in ('US-SEP','US-OCT','UK-SEP')]
        versions=[self.e.versions.current(n.id) for n in nodes]
        self.assertEqual(len({n.id for n in nodes}),3);self.assertEqual(len({v.version_id for v in versions}),3)
        self.assertEqual(len({v.exact_case_fingerprint for v in versions}),3)
        oct_before=versions[1];plan=correction(self.f)
        self.assertIn(nodes[1].id,plan['unaffected']);self.assertEqual(oct_before,self.e.versions.current(nodes[1].id))

if __name__=='__main__':unittest.main()



