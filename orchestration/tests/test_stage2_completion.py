import copy
import unittest
from dataclasses import asdict,replace
from orchestration.runtime import CAO
from orchestration.planning import Issue,DeterministicPlanner
from orchestration.registry import Registry
from orchestration.intake import Intake,FixturePlanner
from orchestration.tests.temporal_intake_fixtures import fixture,OBJECTIVE
from orchestration.tests.stage2_fixtures import build,initial,correction,public

class TemporalIntake(unittest.TestCase):
    def test_issue_round_trip_retains_period(self):
        row=Issue('i','customer_contract','revenue-recognition','qualified',scope_id='US',period_id='SEP')
        self.assertEqual(Issue(**asdict(row)).period_id,'SEP')
    def test_repeated_scope_period_reviewed_packs(self):
        sources,proposal,scope,pack=fixture();engine=Intake(FixturePlanner(proposal));prepared=engine.prepare(OBJECTIVE,sources,[],scope)
        self.assertTrue(prepared.validation['accepted'],prepared.validation)
        result=engine.execute(prepared,pack);self.assertEqual(result.case.outcome,'complete',result.case.open_questions)
        self.assertEqual(len(result.case.graph.nodes),2)
        self.assertEqual(len(result.case.conclusions[0]['calculations']),2)
    def test_material_period_omission_questions(self):
        sources,proposal,scope,pack=fixture();proposal.issues[0].value.pop('period_id')
        result=Intake(FixturePlanner(proposal)).prepare(OBJECTIVE,sources,[],scope)
        self.assertFalse(result.validation['accepted']);self.assertEqual(result.questions[0]['attribute'],'period_candidate')
    def test_same_dates_wrong_calendar_rejected(self):
        sources,proposal,scope,pack=fixture();proposal.facts[0].dimensions['calendar_id']='CALENDAR'
        self.assertFalse(Intake(FixturePlanner(proposal)).prepare(OBJECTIVE,sources,[],scope).validation['accepted'])
    def test_september_source_cannot_certify_october(self):
        sources,proposal,scope,pack=fixture();sources[1]=replace(sources[1],metadata=sources[0].metadata)
        self.assertFalse(Intake(FixturePlanner(proposal)).prepare(OBJECTIVE,sources,[],scope).validation['accepted'])
    def test_pack_period_substitution(self):
        sources,proposal,scope,pack=fixture();engine=Intake(FixturePlanner(proposal));prepared=engine.prepare(OBJECTIVE,sources,[],scope)
        pack.scoped_packs[1].period_id=pack.scoped_packs[0].period_id
        with self.assertRaises(ValueError):engine.execute(prepared,pack)
    def test_binding_period_substitution(self):
        sources,proposal,scope,pack=fixture();engine=Intake(FixturePlanner(proposal));prepared=engine.prepare(OBJECTIVE,sources,[],scope)
        pack.bindings[1]=replace(pack.bindings[1],period_id=pack.bindings[0].period_id)
        with self.assertRaises(ValueError):engine.execute(prepared,pack)
    def test_owner_scope_alias_ambiguous(self):
        from orchestration.execution import OwnerInputs
        sources,proposal,scope,pack=fixture();inputs=OwnerInputs(scope)
        for source in pack.request['facts']['customer_contract']:inputs.add('revenue-recognition',source)
        with self.assertRaises(ValueError):inputs.key('revenue-recognition','ENTITY-US')
    def test_ordinary_repeated_temporal_execution(self):
        sources,proposal,scope,pack=fixture();case=CAO().run(pack.request)
        self.assertEqual(case.outcome,'complete',case.open_questions);self.assertEqual(len(case.graph.nodes),2)

class OrdinaryCorrection(unittest.TestCase):
    def test_ordinary_selective_api(self):
        f=initial(build());plan=correction(f)
        self.assertEqual(public(f)['status'],'partial');self.assertNotIn('800',str(public(f)))
        ledger=CAO().selective_reexecute(f['case'],plan)
        self.assertEqual(len(ledger),4);self.assertEqual(public(f)['status'],'complete');self.assertEqual(public(f)['calculations'][0]['amount'],'900.00')
        self.assertTrue(all(n['status']=='complete' for n in f['case'].workplan_nodes))
    def test_exact_node_required(self):
        f=initial(build())
        with self.assertRaises(ValueError):CAO().correct(f['case'],'revenue-recognition',{},'reviewed')
    def test_native_closed_correction_blocked(self):
        f=initial(build());node=f['nodes']['US-SEP'];e=f['coordinator'];old=e.versions.current(node.id);e.periods.close(node.period_id)
        with self.assertRaises(ValueError):CAO().correct(f['case'],node.id,f['sources'][node.id],'forbidden')
        self.assertEqual(e.versions.current(node.id),old)
