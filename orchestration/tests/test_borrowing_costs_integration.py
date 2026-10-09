"""Narrow production owner routing and durable native-result compatibility."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from dataclasses import asdict
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'skills/tests'))
from borrowing_costs_cases import case,ready,capture_sources
from production import assess_case,to_public
from orchestration import CAO,Case
from orchestration.registry import Registry
from orchestration.planning import DeterministicPlanner,Graph,Node
from orchestration.scopes import Scope,ScopeRegistry,execution_identity
from orchestration.periods import FiscalCalendar,Period,PeriodRegistry
from orchestration.cases import CaseRegistry,case_identity
from orchestration.persistence import SQLiteStore,snapshot
from orchestration.persistence.codec import dumps
from interfaces.public_output import ROUTES


def governed():
    c=case();scope_id=c['entity'];calendar=FiscalCalendar('CALENDAR','Calendar year',1,1,('synthetic reviewed calendar',))
    p=Period.create('CALENDAR','2026-01-01','2026-12-31',2026,'ANNUAL',provenance=('synthetic reviewed annual period',))
    scope=Scope(scope_id,'LEGAL_ENTITY',scope_id,legal_entity_id=scope_id,jurisdiction=c['jurisdiction'],framework=c['framework'],functional_currency='EUR',presentation_currency='EUR',reporting_calendar='CALENDAR',provenance=('synthetic reviewed entity',))
    scopes=ScopeRegistry([scope]);periods=PeriodRegistry([calendar],[p]);cases=CaseRegistry(scopes,periods)
    obj='Review borrowing costs for our qualifying plant construction'
    root=cases.register(Case(case_identity(scope_id,p.period_id,obj,'close'),obj),scope_id,p.period_id,'close',provenance=('synthetic reviewed objective',))
    context=dict(scope_id=scope_id,scope_type='LEGAL_ENTITY',framework=c['framework'],jurisdiction=c['jurisdiction'],functional_currency='EUR',presentation_currency='EUR',period_start=p.start,reporting_period=p.end,period_id=p.period_id)
    c.update(scope_id=scope_id,scope_type='LEGAL_ENTITY',period_id=p.period_id,presentation_currency='EUR')
    c=ready(c=c)
    node=Node(execution_identity('borrowing-costs',context),'qualifying_interest','borrowing-costs',obj,scope_id,c['framework'],[p.start,p.end],scope_id=scope_id,scope_type='LEGAL_ENTITY',jurisdiction=c['jurisdiction'],functional_currency='EUR',presentation_currency='EUR',period_id=p.period_id,case_id=root.id,logical_id='borrowing-costs')
    graph=Graph();graph.add(node);cases.bind_node(root.id,node)
    plan=dict(scopes=scopes.record(),periods=periods.record(),cases=[dict(case_id=root.id,objective=obj,scope_id=scope_id,period_id=p.period_id,cycle='close',parent_id=None,provenance=root.provenance)],root_case=root.id,nodes=graph.record(),dependencies=[],sources={node.id:c})
    result=CAO().run(dict(objective=obj,governed_plan=plan));return result,node.id


class BorrowingIntegration(unittest.TestCase):
    def test_registry_identity_and_authority(self):
        r=Registry().get('borrowing-costs');self.assertEqual('SKILL-BORROW-001',r['id']);self.assertTrue(r['production_available']);self.assertEqual(['SUPPLEMENTAL_BORROWING_COSTS'],r['knowledge_topics'])
    def test_semantic_trigger(self):
        items=DeterministicPlanner().identify('Review our construction interest accounting',{'qualifying_interest':{'project':{'id':'plant'}}},{},Registry());self.assertEqual(['borrowing-costs'],[i.owner for i in items])
    def test_ordinary_interest_nontrigger(self):
        items=DeterministicPlanner().identify('Review ordinary debt interest accounting',{'debt_population':{'debt':[{'id':'loan'}]}},{},Registry());self.assertNotIn('borrowing-costs',[i.owner for i in items])
    def test_governed_owner_execution(self):
        c,n=governed();self.assertEqual('complete',c.outcome,c.open_questions);self.assertEqual('complete',c.graph.nodes[n].status);self.assertEqual(['borrowing-costs'],[x.selected_skill for x in c.graph.nodes.values()])
    def test_native_durable_roundtrip(self):
        c,n=governed();self.assertEqual('complete',c.outcome,c.open_questions)
        company='synthetic-borrowing-company';context=[];before=snapshot(c,company,context)
        with tempfile.TemporaryDirectory() as d:
            with SQLiteStore(str(Path(d)/'case.db')) as s:
                self.assertEqual(1,s.save(c,company,context,0));restored,revision,ctx=s.load(company,c.id)
                self.assertEqual(1,revision);self.assertEqual(dumps(before),dumps(snapshot(restored,company,ctx)))
                self.assertEqual(c.graph.nodes[n].result,restored.graph.nodes[n].result)
    def test_public_privacy_all_routes(self):
        c,n=governed();self.assertEqual('complete',c.outcome,c.open_questions)
        for route in ROUTES:
            public=json.dumps(CAO().public(c,route))
            for key in ('original_source_snapshot','reviewer_signoff','knowledge_review','case_fingerprint','source_note','MODEL_DERIVED_AUDIT_REQUIRED'):
                self.assertNotIn(key,public)

if __name__=='__main__':unittest.main()
