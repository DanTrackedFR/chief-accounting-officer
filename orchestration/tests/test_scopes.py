"""Stage 1 authored permanent dimensional and contamination regressions."""
import copy,json,unittest
from dataclasses import replace
from orchestration.scopes import Scope,ScopeRegistry,execution_scopes,execution_identity
from orchestration.runtime import CAO,digest
from orchestration.planning import Graph,Node
from orchestration.scoped_journals import qualify_journal,allocate_scoped
from orchestration.scoped_receipts import validate_scoped_receipt
from orchestration.tests.scope_fixtures import *

class Scopes(unittest.TestCase):
    def test_arbitrary_seven_scopes_independently_addressable(self):
        rows=ROWS+[
            Scope('SUBGROUP-APAC','SUBGROUP','APAC',parent_scope_id='GROUP-EUR',framework='IFRS',jurisdiction='AU',presentation_currency='AUD',provenance=('review',)),
            Scope('ENTITY-AU','LEGAL_ENTITY','Australia','AU-001','SUBGROUP-APAC','AU','AASB','AUD',provenance=('review',)),
            Scope('ENTITY-NZ','LEGAL_ENTITY','NZ','NZ-001','SUBGROUP-APAC','NZ','IFRS','NZD',provenance=('review',))]
        r=ScopeRegistry(rows);self.assertEqual(len(r.record()),7)
        for s in rows:self.assertEqual(r.get(s.scope_id),s)
    def test_duplicate_id(self):
        with self.assertRaises(ValueError):ScopeRegistry(ROWS+[ROWS[0]])
    def test_missing_parent(self):
        with self.assertRaises(ValueError):ScopeRegistry([replace(ROWS[1],parent_scope_id='unknown')])
    def test_self_parent(self):
        with self.assertRaises(ValueError):ScopeRegistry([replace(ROWS[0],parent_scope_id='GROUP-EUR')])
    def test_cycle(self):
        with self.assertRaises(ValueError):ScopeRegistry([Scope('A','SUBGROUP','A',parent_scope_id='B',provenance=('p',)),Scope('B','SUBGROUP','B',parent_scope_id='A',provenance=('p',))])
    def test_illegal_legal_parent(self):
        with self.assertRaises(ValueError):ScopeRegistry(ROWS+[Scope('child','LEGAL_ENTITY','child','child','ENTITY-US',provenance=('p',))])
    def test_illegal_group_child(self):
        with self.assertRaises(ValueError):ScopeRegistry(ROWS+[Scope('child','GROUP','child',parent_scope_id='GROUP-EUR',provenance=('p',))])
    def test_silent_type_conversion(self):
        with self.assertRaises(ValueError):ScopeRegistry([replace(ROWS[1],scope_type='GROUP',parent_scope_id=None)])
    def test_missing_material_dimensions_not_invented(self):
        ctx=copy.deepcopy(SCOPE);ctx['scopes'][1]['functional_currency']=None
        with self.assertRaises(ValueError):execution_scopes(ctx)
    def test_scope_display_name_identity_stable(self):
        a=execution_scopes(SCOPE);ctx=copy.deepcopy(SCOPE);ctx['scopes'][1]['display_name']='Renamed legal business'
        self.assertEqual(execution_identity('revenue-recognition',a['ENTITY-NL']),execution_identity('revenue-recognition',execution_scopes(ctx)['ENTITY-NL']))
    def test_hierarchy_reorder(self):
        self.assertEqual(ScopeRegistry(ROWS).record(),ScopeRegistry(list(reversed(ROWS))).record())
    def test_unrelated_scope_insertion(self):
        ctx=copy.deepcopy(SCOPE);ctx['scopes'].append(Scope('UNRELATED','LEGAL_ENTITY','Other','X',jurisdiction='NL',framework='IFRS',functional_currency='EUR',provenance=('p',)).record())
        self.assertEqual(execution_identity('revenue-recognition',execution_scopes(SCOPE)['ENTITY-US']),execution_identity('revenue-recognition',execution_scopes(ctx)['ENTITY-US']))
    def test_hierarchy_not_dependency(self):
        r=run();nodes=[n for n in r.case.graph.nodes.values() if n.selected_skill=='revenue-recognition']
        self.assertTrue(all(not n.dependencies for n in nodes));self.assertEqual(len(nodes),3)
    def test_metadata_isolation(self):
        s=execution_scopes(SCOPE)
        self.assertEqual([(s[k]['framework'],s[k]['currency'],s[k]['jurisdiction']) for k in ['GROUP-EUR','ENTITY-NL','ENTITY-US','ENTITY-UK']],[('IFRS','EUR','NL'),('IFRS','EUR','NL'),('US_GAAP','USD','US'),('UK_GAAP','GBP','UK')])
        self.assertIsNone(s['GROUP-EUR']['functional_currency']);self.assertIsNone(s['ENTITY-US']['presentation_currency'])

class RepeatedOwners(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.proof=run();cls.pack=reviewed_pack()
    def test_proof_complete_without_conversion_total(self):
        c=self.proof.case;self.assertEqual((c.outcome,c.status),('complete','CLOSED'));self.assertIsNone(c.group_consumer['consolidated_total']);self.assertEqual(len(c.group_consumer['limitations']),2)
    def test_package_key_collision_no_overwrite(self):
        n=[n for n in self.proof.case.workplan_nodes if n['selected_skill']=='revenue-recognition'];self.assertEqual(len(n),3)
        for field in ('id','scope_id'):self.assertEqual(len({r[field] for r in n}),3)
        self.assertEqual(len({r['result']['case_fingerprint'] for r in n}),3)
        self.assertEqual(len({digest(r['result']) for r in n}),3)
    def test_independent_packs_and_sources(self):
        natives=self.pack.request['facts']['customer_contract'];self.assertEqual(len({id(c) for c in natives}),3)
        self.assertEqual(len({tuple(c['source_population']) for c in natives}),3)
        self.assertEqual(len({b.scope_id for b in self.pack.bindings}),3)
    def test_node_alias_ambiguity_fail_closed(self):
        with self.assertRaises(ValueError):self.proof.case.graph.nodes['revenue-recognition']
    def test_graph_order_does_not_change_results(self):
        pack=reviewed_pack();pack.request['facts']['customer_contract'].reverse();c=CAO().run(pack.request)
        self.assertEqual(c.outcome,'complete');self.assertEqual(c.group_consumer,self.proof.case.group_consumer)
    def test_source_order_does_not_change_facts(self):
        sources=list(reversed(source_pack()));p=semantic_proposal(sources);e=Intake(FixturePlanner(p));r=e.execute(e.prepare(OBJECTIVE,sources,[],SCOPE),reviewed_pack())
        self.assertEqual(r.case.group_consumer,self.proof.case.group_consumer)
    def _attack_receipt(self,scope,field,value):
        p=reviewed_pack();r=next(r for r in p.request['group_consumer']['receipts'] if r['source_scope']==scope);r[field]=value
        c=CAO().run(p.request);self.assertNotEqual(c.outcome,'complete')
    def test_us_as_uk(self):self._attack_receipt('ENTITY-US','source_scope','ENTITY-UK')
    def test_uk_as_nl(self):self._attack_receipt('ENTITY-UK','source_scope','ENTITY-NL')
    def test_nl_as_us(self):self._attack_receipt('ENTITY-NL','source_scope','ENTITY-US')
    def test_equal_value_wrong_scope_substitution(self):
        p=reviewed_pack();rs=p.request['group_consumer']['receipts'];self.assertEqual(rs[0]['result']['calculations']['period_revenue'],rs[1]['result']['calculations']['period_revenue']);rs[1]['result']=rs[0]['result']
        self.assertNotEqual(CAO().run(p.request).outcome,'complete')
    def test_usd_relabel_eur(self):self._attack_receipt('ENTITY-US','currency','EUR')
    def test_gbp_relabel_eur(self):self._attack_receipt('ENTITY-UK','currency','EUR')
    def test_us_gaap_as_ifrs(self):self._attack_receipt('ENTITY-US','framework','IFRS')
    def test_uk_gaap_as_ifrs(self):self._attack_receipt('ENTITY-UK','framework','IFRS')
    def test_stale_receipt(self):self._attack_receipt('ENTITY-US','currentness','SUPERSEDED')
    def test_us_carries_uk_jurisdiction(self):
        p=reviewed_pack();p.request['facts']['customer_contract'][1]['jurisdiction']='UK';self.assertNotEqual(CAO().run(p.request).outcome,'complete')
    def test_uk_carries_nl_jurisdiction(self):
        p=reviewed_pack();p.request['facts']['customer_contract'][2]['jurisdiction']='NL';self.assertNotEqual(CAO().run(p.request).outcome,'complete')
    def test_group_consumed_as_legal(self):
        p=reviewed_pack();p.request['group_consumer']['scope_id']='ENTITY-US';self.assertNotEqual(CAO().run(p.request).outcome,'complete')
    def test_legal_as_group_without_typed_receipt(self):self._attack_receipt('ENTITY-US','consumption_type','GROUP_ACCOUNTING_RESULT')
    def test_wrong_source_entity(self):
        sources=source_pack();index=next(i for i,s in enumerate(sources) if s.id=='source-ENTITY-US');sources[index]=replace(sources[index],metadata=dict(sources[index].metadata,entity='ENTITY-UK',scope_id='ENTITY-UK'))
        e=Intake(FixturePlanner(semantic_proposal(sources)));r=e.prepare(OBJECTIVE,sources,[],SCOPE);self.assertFalse(r.validation['accepted'])
    def test_ambiguous_scope_never_guessed(self):
        sources=source_pack();p=semantic_proposal(sources);p.facts[1].dimensions.pop('entity');p.facts[1].dimensions.pop('scope_id')
        r=Intake(FixturePlanner(p)).prepare(OBJECTIVE,sources,[],SCOPE);self.assertFalse(r.validation['accepted'])
    def test_semantic_entity_creation_rejected(self):
        sources=source_pack();p=semantic_proposal(sources);p.entities=[cl('NEW-ENTITY',p.facts[0].claim.evidence,'OBSERVED',.99)]
        self.assertFalse(Intake(FixturePlanner(p)).prepare(OBJECTIVE,sources,[],SCOPE).validation['accepted'])
    def test_unknown_scope_candidate_remains_unresolved(self):
        sources=source_pack();p=semantic_proposal(sources);p.entities=[cl('NEW-ENTITY',status='UNRESOLVED',confidence=0)]
        r=Intake(FixturePlanner(p)).prepare(OBJECTIVE,sources,[],SCOPE);self.assertTrue(r.validation['accepted']);self.assertTrue(any(q['attribute']=='scope_candidate' for q in r.questions));self.assertNotIn('NEW-ENTITY',[s['scope_id'] for s in SCOPE['scopes']])
    def test_wrong_scope_reviewed_pack(self):
        sources=source_pack();e=Intake(FixturePlanner(semantic_proposal(sources)));r=e.prepare(OBJECTIVE,sources,[],SCOPE);p=reviewed_pack();p.scope_id='ENTITY-UK'
        with self.assertRaises(ValueError):e.execute(r,p)
    def test_wrong_scope_fact_binding(self):
        sources=source_pack();e=Intake(FixturePlanner(semantic_proposal(sources)));r=e.prepare(OBJECTIVE,sources,[],SCOPE);p=reviewed_pack();p.bindings[1]=replace(p.bindings[1],scope_id='ENTITY-UK')
        with self.assertRaises(ValueError):e.execute(r,p)
    def test_mixed_entity_issue(self):
        sources=source_pack();p=semantic_proposal(sources);p.issues[0].value['fact_ids'].append('fact-ENTITY-US');self.assertFalse(Intake(FixturePlanner(p)).prepare(OBJECTIVE,sources,[],SCOPE).validation['accepted'])
    def test_scope_qualified_questions(self):
        sources=source_pack();p=semantic_proposal(sources);p.issues[1].value['required_fields'].append('functional_currency')
        r=Intake(FixturePlanner(p)).prepare(OBJECTIVE,sources,[],SCOPE);self.assertTrue(any('ENTITY-US' in q['question'] for q in r.questions))
    def test_public_no_fingerprints_or_internal_routing(self):
        value=json.dumps(CAO().public(self.proof.case));self.assertNotIn('exec:',value);self.assertNotIn('case_fingerprint',value);self.assertIn('USD',value);self.assertIn('conversion unresolved',value)
    def test_four_source_to_consumer_lineages(self):
        c=self.proof.case
        for scope in ('ENTITY-NL','ENTITY-US','ENTITY-UK'):
            self.assertTrue(any(r.get('scope_id')==scope and r.get('source_lineage') for r in self.proof.lineage));self.assertTrue(any(r['source_scope']==scope for r in c.handoff_ledger))
        self.assertEqual(c.group_consumer['context_lineage']['source_id'],'source-GROUP-EUR')

class ScopedJournals(unittest.TestCase):
    def native(self,scope='ENTITY-US'):
        s=execution_scopes(SCOPE)[scope]
        return dict(owner='revenue-recognition',node=execution_identity('revenue-recognition',s),source_scope=scope,posting_scope=scope,accounting_layer=s['scope_type'],currency=s['currency'],period=['2026-01-01','2026-12-31'],journals=[[dict(side='Dr',account='Receivable',amount='100'),dict(side='Cr',account='Revenue',amount='100')]])
    def event(self,row):return dict(economic_id='commercial-1',posting_scope=row['posting_scope'],currency=row['currency'],period=row['period'],primary=[dict(owner=row['node'],index=0)],witnesses=[],evidence='Reviewed original transaction')
    def test_group_to_legal_journal(self):
        with self.assertRaises(ValueError):qualify_journal(SCOPE,'GROUP-EUR','ENTITY-US','GROUP')
    def test_legal_to_group_journal(self):
        with self.assertRaises(ValueError):qualify_journal(SCOPE,'ENTITY-US','GROUP-EUR','LEGAL_ENTITY')
    def test_identical_cross_scope_events_not_deduplicated(self):
        rows=[self.native('ENTITY-US'),self.native('ENTITY-UK')];selected,ledger=allocate_scoped(rows,SCOPE,[self.event(r) for r in rows]);self.assertEqual(len(selected),2);self.assertEqual(len({r['allocated_identity'] for r in ledger}),2)
    def test_legal_and_group_same_commercial_relation_distinct(self):
        rows=[self.native('ENTITY-NL'),self.native('ENTITY-US'),self.native('GROUP-EUR')];self.assertEqual(len(allocate_scoped(rows,SCOPE,[self.event(r) for r in rows])[0]),3)
    def _alias(self,field):
        row=self.native();event=self.event(row);other=copy.deepcopy(event);other['economic_id']='renamed-'+field
        with self.assertRaises(ValueError):allocate_scoped([row],SCOPE,[event,other])
    def test_same_scope_account_alias(self):self._alias('account')
    def test_same_scope_event_description(self):self._alias('event')
    def test_same_scope_nature_alias(self):self._alias('nature')
    def test_same_scope_duplicate_identity(self):
        row=self.native();event=self.event(row)
        with self.assertRaises(ValueError):allocate_scoped([row],SCOPE,[event,event])
    def test_posting_scope_poisoned_native(self):
        row=self.native();row['posting_scope']='GROUP-EUR'
        with self.assertRaises(ValueError):allocate_scoped([row],SCOPE,[self.event(row)])

if __name__=='__main__':unittest.main()
