"""Permanent authored temporal/dependency controls."""
import copy
import unittest
from dataclasses import replace
from orchestration.tests.stage2_fixtures import build,initial,correction,public
from orchestration.periods import Period,PeriodRelationship,EffectiveInterval
from orchestration.cases import case_identity
from orchestration.runtime import Case
from orchestration.scopes import execution_identity

class PeriodControls(unittest.TestCase):
    def setUp(self):self.f=build();self.e=self.f['coordinator'];self.p=self.f['periods']
    def test_deterministic_period_identity(self):
        a=self.p['US-FISCAL-SEP'];self.assertEqual(Period.create(a.calendar_id,a.start,a.end,a.fiscal_year,a.fiscal_period,provenance=('other evidence',)).period_id,a.period_id)
    def test_calendar_identity_distinct(self):self.assertNotEqual(self.p['US-FISCAL-SEP'].period_id,self.p['CALENDAR-SEP'].period_id)
    def test_dates_identity_distinct(self):
        a=self.p['CALENDAR-SEP'];b=Period.create(a.calendar_id,'2026-09-02',a.end,a.fiscal_year,a.fiscal_period,provenance=('p',));self.assertNotEqual(a.period_id,b.period_id)
    def test_end_before_start(self):
        with self.assertRaises(ValueError):Period.create('CALENDAR','2026-10-01','2026-09-30',2026,'SEP',provenance=('p',))
    def test_malformed_date(self):
        with self.assertRaises(ValueError):Period.create('CALENDAR','20260901','2026-09-30',2026,'SEP',provenance=('p',))
    def test_identity_relabel(self):
        with self.assertRaises(ValueError):replace(self.p['CALENDAR-SEP'],calendar_id='US-FISCAL').validate()
    def test_self_relationship(self):
        a=self.p['CALENDAR-SEP'].period_id
        with self.assertRaises(ValueError):self.e.periods.add_relationship(PeriodRelationship(a,a,'CURRENT',('p',)))
    def test_period_cycle(self):
        a=self.p['CALENDAR-SEP'].period_id;b=self.p['CALENDAR-OCT'].period_id
        self.e.periods.add_relationship(PeriodRelationship(a,b,'CURRENT',('p',)))
        with self.assertRaises(ValueError):self.e.periods.add_relationship(PeriodRelationship(b,a,'CURRENT',('p',)))
    def test_wrong_opening_dates(self):
        with self.assertRaises(ValueError):self.e.periods.add_relationship(PeriodRelationship(self.p['CALENDAR-AUG'].period_id,self.p['CALENDAR-OCT'].period_id,'OPENING',('p',)))
    def test_wrong_opening_calendar(self):
        with self.assertRaises(ValueError):self.e.periods.add_relationship(PeriodRelationship(self.p['US-FISCAL-SEP'].period_id,self.p['CALENDAR-OCT'].period_id,'OPENING',('p',)))
    def test_wrong_comparative(self):
        with self.assertRaises(ValueError):self.e.periods.add_relationship(PeriodRelationship(self.p['CALENDAR-OCT'].period_id,self.p['CALENDAR-SEP'].period_id,'COMPARATIVE',('p',)))
    def test_partial_interval_mismatch(self):
        with self.assertRaises(ValueError):replace(self.f['interval'],source_period=self.p['CALENDAR-SEP'].period_id).validate(self.e.periods,self.e.cases.scopes)
    def test_effective_date_mismatch(self):
        with self.assertRaises(ValueError):replace(self.f['interval'],effective_date='2026-10-16').validate(self.e.periods,self.e.cases.scopes)
    def test_effective_scope_unknown(self):
        with self.assertRaises(ValueError):replace(self.f['interval'],scope_id='UNKNOWN').validate(self.e.periods,self.e.cases.scopes)

class CaseControls(unittest.TestCase):
    def setUp(self):self.f=build();self.e=self.f['coordinator'];self.n=self.f['nodes']
    def test_case_multiple_objectives(self):
        n=self.n['US-SEP'];self.assertNotEqual(case_identity(n.scope_id,n.period_id,'Other investigation','controlled-close'),n.case_id)
    def test_case_multiple_periods(self):self.assertNotEqual(self.n['US-SEP'].case_id,self.n['US-OPEN'].case_id)
    def test_case_duplicate_identity(self):
        c=self.e.cases.get(self.n['US-SEP'].case_id)
        with self.assertRaises(ValueError):self.e.cases.register(Case(c.id,c.objective),c.scope_id,c.period_id,c.cycle,provenance=('p',))
    def test_wrong_case_scope(self):
        with self.assertRaises(ValueError):self.e.cases.bind_node(self.n['US-SEP'].case_id,replace(self.n['US-SEP'],scope_id='ENTITY-UK'))
    def test_wrong_case_period(self):
        with self.assertRaises(ValueError):self.e.cases.bind_node(self.n['US-SEP'].case_id,replace(self.n['US-SEP'],period_id=self.n['US-OPEN'].period_id))
    def test_wrong_parent(self):
        edge=next(e for e in self.e.edges.values() if e.consumer_node==self.n['GROUP'].id)
        source=self.e.cases.get(edge.producer_case);source.parent_case_id=self.n['UK-SEP'].case_id
        with self.assertRaises(ValueError):edge.validate(self.e.graph,self.e.cases,self.e.periods)
    def test_hierarchies_independent(self):
        self.assertTrue(all(self.e.cases.get(n.case_id).parent_case_id==self.n['GROUP'].case_id for n in [self.n['US-SEP'],self.n['UK-SEP']]))
        self.assertEqual(self.n['UK-SEP'].dependencies,[])
    def test_unrelated_child_issue_does_not_block(self):
        initial(self.f);c=self.e.cases.get(self.n['UK-SEP'].case_id);c.open_questions.append(dict(question='Independent process review'));c.outcome='partial';self.e.cases.refresh(self.e.graph,self.e.versions,self.e.edges)
        self.assertEqual(self.e.cases.get(self.n['GROUP'].case_id).outcome,'complete')
    def test_required_blocked_producer_propagates(self):
        initial(self.f);n=self.n['US-OPEN'];self.e.versions.mark_stale(self.e.versions.current(n.id).version_id,'test-required','test-upstream');n.status='blocked';self.e.cases.refresh(self.e.graph,self.e.versions,self.e.edges)
        self.assertNotEqual(self.e.cases.get(self.n['GROUP'].case_id).outcome,'complete')

class VersionControls(unittest.TestCase):
    def setUp(self):self.f=initial(build());self.e=self.f['coordinator'];self.n=self.f['nodes']
    def test_central_selective_chain(self):
        old=self.e.versions.current(self.n['US-SEP'].id);uk=self.e.versions.current(self.n['UK-SEP'].id);plan=correction(self.f)
        self.assertEqual(set(plan['execution_order']),{self.n[k].id for k in ['US-REPORT','US-OPEN','GROUP','ANALYTICS']});self.assertEqual(self.e.versions.state(old.version_id),'SUPERSEDED')
        self.assertEqual(self.e.versions.current(self.n['US-SEP'].id).payload()['calculations']['period_revenue'],'900.00')
        ledger=self.e.reexecute(plan,self.f['executors'],self.f['sources']);self.assertEqual(len(ledger),4);self.assertEqual(self.e.versions.current(uk.node_id),uk)
        self.assertEqual(public(self.f)['calculations'][0]['amount'],'900.00')
    def test_global_invalidation_rejected(self):
        p=correction(self.f)
        for k in ['UK-SEP','UK-CONTROL','NL-CONTROL']:
            self.assertIn(self.n[k].id,p['unaffected']);self.assertEqual(self.e.versions.state(self.e.versions.current(self.n[k].id).version_id),'CURRENT')
    def test_direct_invalidation(self):self.assertEqual(correction(self.f)['direct'],[self.n['US-REPORT'].id])
    def test_transitive_invalidation(self):self.assertEqual(len(correction(self.f)['transitive']),3)
    def test_scope_parent_not_invalidation(self):self.assertNotIn(self.n['UK-CONTROL'].id,correction(self.f)['execution_order'])
    def test_closed_history_preserved(self):
        old=self.e.versions.current(self.n['US-SEP'].id);payload=old.payload();correction(self.f);self.assertEqual(self.e.versions.versions[old.version_id].payload(),payload)
    def test_closed_change_fails(self):
        n=self.n['US-SEP'];self.e.periods.close(n.period_id)
        with self.assertRaises(ValueError):self.e.execute(n.id,self.f['executors'][n.id],self.f['sources'][n.id],'Unauthorized update')
    def test_reopening_alone_no_invalidation(self):
        n=self.n['US-SEP'];before=copy.deepcopy(self.e.versions.states);self.e.periods.close(n.period_id);self.e.periods.reopen(n.period_id,'r',dict(status='APPROVED',evidence=['p'],convention='SYNTHETIC_GOVERNED'),[n.case_id],[n.id]);self.assertEqual(before,self.e.versions.states)
    def test_stale_receipt_fails(self):
        edge=next(k for k,e in self.e.edges.items() if e.consumer_node==self.n['GROUP'].id);receipt=self.e.receipt(edge);correction(self.f)
        with self.assertRaises(ValueError):self.e.validate_receipt(receipt,self.n['GROUP'].id)
    def test_superseded_receipt_fails(self):
        edge=next(k for k,e in self.e.edges.items() if e.consumer_node==self.n['US-REPORT'].id);receipt=self.e.receipt(edge);correction(self.f)
        with self.assertRaises(ValueError):self.e.validate_receipt(receipt,self.n['US-REPORT'].id)
    def test_wrong_period_receipt_fails(self):
        edge=next(iter(self.e.edges));r=self.e.receipt(edge);r['producer_period']=self.n['GROUP'].period_id
        with self.assertRaises(ValueError):self.e.validate_receipt(r,r['consumer_node'])
    def test_wrong_scope_receipt_fails(self):
        edge=next(iter(self.e.edges));r=self.e.receipt(edge);r['producer_scope']='ENTITY-UK'
        with self.assertRaises(ValueError):self.e.validate_receipt(r,r['consumer_node'])
    def test_order_fail_closed(self):
        plan=correction(self.f);plan=copy.deepcopy(plan);plan['execution_order'].reverse()
        with self.assertRaises(ValueError):self.e.reexecute(plan,self.f['executors'],self.f['sources'])
    def test_unrelated_rerun_fail_closed(self):
        plan=copy.deepcopy(correction(self.f));plan['execution_order'].append(self.n['UK-SEP'].id)
        with self.assertRaises(ValueError):self.e.reexecute(plan,self.f['executors'],self.f['sources'])
    def test_old_versions_not_current_economics(self):
        correction(self.f);self.e.reexecute(self.e.rework_history[-1],self.f['executors'],self.f['sources']);self.assertEqual(len(self.e.current_payloads()),9);self.assertEqual(len(self.e.versions.versions),14)
    def test_current_dependency_wrong_calendar(self):
        edge=next(e for e in self.e.edges.values() if e.consumer_node==self.n['GROUP'].id)
        with self.assertRaises(ValueError):replace(edge,dependency_type='CURRENT').validate(self.e.graph,self.e.cases,self.e.periods)
    def test_dependency_id_stable(self):
        edge=next(iter(self.e.edges.values()));self.assertEqual(edge.id,replace(edge,evidence=('different reviewed evidence',)).id)
    def test_public_no_internal_lineage(self):
        import json
        correction(self.f);self.e.reexecute(self.e.rework_history[-1],self.f['executors'],self.f['sources']);answer=json.dumps(public(self.f))
        for token in ['version:','exec:','dependency:','fingerprint','reviewer','SUPERSEDED','STALE']:self.assertNotIn(token,answer)

if __name__=='__main__':unittest.main()
