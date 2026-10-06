"""Fresh reviewer attacks: coordinated mutations, not single-field smoke tests."""
import copy,json,unittest
from dataclasses import replace
from orchestration.scopes import Scope,ScopeRegistry,execution_scopes,execution_identity
from orchestration.scoped_journals import allocate_scoped
from orchestration.runtime import CAO,digest
from orchestration.intake import Intake,FixturePlanner,PopulationBinding,DocumentBinding,TextAssertion
from orchestration.tests.scope_fixtures import ROWS,SCOPE,OBJECTIVE,source_pack,semantic_proposal,reviewed_pack,completed,run
from cases import finalize

class IndependentScopeQA(unittest.TestCase):
    def execute(self,pack=None,sources=None,proposal=None):
        sources=sources or source_pack();e=Intake(FixturePlanner(proposal or semantic_proposal(sources)))
        prepared=e.prepare(OBJECTIVE,sources,[],SCOPE)
        if not prepared.validation['accepted']:return None
        return e.execute(prepared,pack or reviewed_pack()).case
    def reject(self,p,sources=None):
        try:c=self.execute(p,sources)
        except (ValueError,KeyError,TypeError):return
        self.assertTrue(c is None or c.outcome!='complete')
    def refresh(self,p,index):
        native=finalize('revenue-recognition',p.request['facts']['customer_contract'][index]);p.request['facts']['customer_contract'][index]=native
        p.scoped_packs[index].request['facts']['customer_contract']=copy.deepcopy(native)
        result=completed('revenue-recognition',native);r=p.request['group_consumer']['receipts'][index]
        r.update(result=result,result_fingerprint=digest(result),exact_case_fingerprint=result['case_fingerprint']);r['economic_identity'][-1]=result['case_fingerprint']
    def native(self,scope='ENTITY-US'):
        s=execution_scopes(SCOPE)[scope]
        return dict(owner='revenue-recognition',node=execution_identity('revenue-recognition',s),source_scope=scope,posting_scope=scope,accounting_layer=s['scope_type'],currency=s['currency'],period=['2026-01-01','2026-12-31'],journals=[[dict(side='Dr',account='AR',amount='100'),dict(side='Cr',account='Revenue',amount='100')]])
    def event(self,r):return dict(economic_id='sale-1',posting_scope=r['posting_scope'],currency=r['currency'],period=r['period'],primary=[dict(owner=r['node'],index=0)],witnesses=[],evidence='reviewed transaction')
    def test_coordinated_wrong_source_population(self):
        p=reviewed_pack();p.request['facts']['customer_contract'][1]['source_population']=['source-ENTITY-UK'];self.refresh(p,1)
        self.reject(p)
    def test_coordinated_mixed_source_population(self):
        p=reviewed_pack();p.request['facts']['customer_contract'][1]['source_population'].append('source-ENTITY-NL');self.refresh(p,1)
        self.reject(p)
    def test_journal_currency_agreement_does_not_authorize_relabel(self):
        r=self.native();r['currency']='EUR'
        with self.assertRaises(ValueError):allocate_scoped([r],SCOPE,[self.event(r)])
    def test_journal_node_scope_must_match(self):
        r=self.native();r['node']=execution_identity('revenue-recognition',execution_scopes(SCOPE)['ENTITY-UK'])
        with self.assertRaises(ValueError):allocate_scoped([r],SCOPE,[self.event(r)])
    def test_journal_node_owner_must_match(self):
        r=self.native();r['owner']='asset-impairment'
        with self.assertRaises(ValueError):allocate_scoped([r],SCOPE,[self.event(r)])
    def test_journal_period_must_be_bounded(self):
        r=self.native();r['period']=['2025-01-01','2025-12-31']
        with self.assertRaises(ValueError):allocate_scoped([r],SCOPE,[self.event(r)])
    def test_wrong_scope_qualified_document_matching_payload(self):
        from orchestration.intake.sources import Inventory
        sources=source_pack();inv=Inventory(sources);uk=inv.extractions['source-ENTITY-UK'].source
        p=reviewed_pack();native=p.request['facts']['customer_contract'][1]
        native['qualified_source_documents']={'uk':dict(fingerprint=uk['fingerprint'],metadata=uk['metadata'])}
        native['source_semantic_controls']=dict(text_assertions=[],populations=[])
        binding=DocumentBinding('source-ENTITY-UK','revenue-recognition',('qualified_source_documents','uk'),'ENTITY-US')
        p.documents=[binding];p.scoped_packs[1].documents=[binding];self.refresh(p,1)
        self.reject(p,sources)
    def test_same_scope_document_metadata_contamination(self):
        from orchestration.intake.sources import Inventory
        sources=source_pack();original=next(x for x in sources if x.id=='source-ENTITY-US')
        sources.append(replace(original,id='supplemental-us',payload='policy\nReviewed revenue policy\n',metadata=dict(original.metadata,framework='UK_GAAP',currency='GBP',jurisdiction='UK')))
        supplemental=Inventory(sources).extractions['supplemental-us'].source
        p=reviewed_pack();native=p.request['facts']['customer_contract'][1]
        native['qualified_source_documents']={'policy':dict(fingerprint=supplemental['fingerprint'],metadata=supplemental['metadata'])}
        native['source_semantic_controls']=dict(text_assertions=[],populations=[])
        binding=DocumentBinding('supplemental-us','revenue-recognition',('qualified_source_documents','policy'),'ENTITY-US')
        p.documents=[binding];p.scoped_packs[1].documents=[binding];self.refresh(p,1);self.reject(p,sources)
    def test_inactive_scope_cannot_produce_current_result(self):
        p=reviewed_pack();p.request['scope']['scopes'][2]['status']='INACTIVE'
        try:c=CAO().run(p.request)
        except ValueError:return
        self.assertNotEqual(c.outcome,'complete')
    def test_scope_effective_after_period_cannot_execute_current(self):
        p=reviewed_pack();p.request['scope']['scopes'][2]['effective_from']='2026-07-01'
        try:c=CAO().run(p.request)
        except ValueError:return
        self.assertNotEqual(c.outcome,'complete')
    def test_scope_expired_before_period_end_cannot_execute_current(self):
        p=reviewed_pack();p.request['scope']['scopes'][2]['effective_to']='2026-06-30'
        try:c=CAO().run(p.request)
        except ValueError:return
        self.assertNotEqual(c.outcome,'complete')
    def test_inactive_scope_cannot_receive_current_posting(self):
        ctx=copy.deepcopy(SCOPE);ctx['scopes'][2]['status']='INACTIVE';r=self.native()
        with self.assertRaises(ValueError):allocate_scoped([r],ctx,[self.event(r)])
    def test_source_scope_and_entity_metadata_must_agree(self):
        sources=source_pack();index=next(i for i,x in enumerate(sources) if x.id=='source-ENTITY-NL');sources[index]=replace(sources[index],metadata=dict(sources[index].metadata,entity='ENTITY-UK'))
        self.reject(reviewed_pack(),sources)
    def test_group_context_source_must_exist(self):
        p=reviewed_pack();p.request['group_consumer']['context_source']['source_id']='NONEXISTENT';self.reject(p)
    def test_group_context_source_scope_must_match_inventory(self):
        p=reviewed_pack();p.request['group_consumer']['context_source']['source_id']='source-ENTITY-US';self.reject(p)
    def test_equal_value_whole_receipt_swap(self):
        p=reviewed_pack();p.request['group_consumer']['receipts'][2]=copy.deepcopy(p.request['group_consumer']['receipts'][1]);self.reject(p)
    def test_omitted_expected_producer(self):
        p=reviewed_pack();p.request['group_consumer']['expected_producers'].pop();self.reject(p)
    def test_qualified_pack_missing_binding(self):
        p=reviewed_pack();p.bindings.pop()
        with self.assertRaises(ValueError):self.execute(p)
    def test_qualified_pack_duplicate_fact_binding(self):
        p=reviewed_pack();p.bindings.append(p.bindings[0])
        with self.assertRaises(ValueError):self.execute(p)
    def test_owner_input_package_duplicate_conflict(self):
        p=reviewed_pack();other=copy.deepcopy(p.request['facts']['customer_contract'][0]);other['evidence']=['other'];p.request['facts']['customer_contract'].append(other)
        with self.assertRaises(ValueError):self.execute(p)
    def test_currency_dimension_native_poison(self):
        p=reviewed_pack();p.request['facts']['customer_contract'][1]['functional_currency']='EUR';self.refresh(p,1);self.reject(p)
    def test_receipt_currency_dimension_poison(self):
        p=reviewed_pack();p.request['group_consumer']['receipts'][2]['functional_currency']='EUR';self.reject(p)
    def test_receipt_result_fingerprint_equal_value_not_identity(self):
        p=reviewed_pack();rs=p.request['group_consumer']['receipts'];rs[2]['result_fingerprint']=rs[1]['result_fingerprint'];self.reject(p)
    def test_framework_recertification_does_not_authorize_scope_change(self):
        p=reviewed_pack();p.request['facts']['customer_contract'][1]['framework']='IFRS';self.refresh(p,1);self.reject(p)
    def test_jurisdiction_recertification_does_not_authorize_scope_change(self):
        p=reviewed_pack();p.request['facts']['customer_contract'][2]['jurisdiction']='NL';self.refresh(p,2);self.reject(p)
    def test_source_without_identity_not_filename_inference(self):
        sources=source_pack();sources[1]=replace(sources[1],metadata={k:v for k,v in sources[1].metadata.items() if k not in ('entity','scope_id')});self.reject(reviewed_pack(),sources)
    def test_semantic_unknown_scope_not_registry_write(self):
        sources=source_pack();p=semantic_proposal(sources);p.issues[0].value['scope_id']='NEW';self.assertIsNone(self.execute(sources=sources,proposal=p));self.assertEqual(len(ScopeRegistry(ROWS).record()),4)
    def test_collision_id_despite_distinct_legal_id(self):
        with self.assertRaises(ValueError):ScopeRegistry(ROWS+[replace(ROWS[1],legal_entity_id='other')])
    def test_missing_parent_scope_independent(self):
        with self.assertRaises(ValueError):ScopeRegistry(ROWS+[replace(ROWS[1],scope_id='OTHER',parent_scope_id='ABSENT')])
    def test_self_parent_scope_independent(self):
        with self.assertRaises(ValueError):ScopeRegistry(ROWS+[replace(ROWS[1],scope_id='OTHER',parent_scope_id='OTHER')])
    def test_per_scope_fingerprints_sources_and_nodes_distinct(self):
        c=run().case;nodes=[n for n in c.graph.nodes.values() if n.selected_skill=='revenue-recognition']
        self.assertEqual(len({n.id for n in nodes}),3);self.assertEqual(len({n.result['case_fingerprint'] for n in nodes}),3)
        self.assertEqual(len({tuple(x['source_population']) for x in reviewed_pack().request['facts']['customer_contract']}),3)
    def test_scope_child_pack_reused_as_other_entity(self):
        p=reviewed_pack();p.scoped_packs[1]=copy.deepcopy(p.scoped_packs[2]);self.reject(p)
    def test_hierarchy_subgroup_cycle(self):
        a=Scope('A','SUBGROUP','A',parent_scope_id='B',provenance=('p',));b=replace(a,scope_id='B',parent_scope_id='A')
        with self.assertRaises(ValueError):ScopeRegistry(ROWS+[a,b])
    def test_parent_metadata_does_not_create_dependency(self):
        c=run().case;self.assertTrue(all(not n.dependencies for n in c.graph.nodes.values() if n.scope_type=='LEGAL_ENTITY'))
    def test_independent_identity_serialization_and_reorder(self):
        a=execution_scopes(SCOPE);ctx=json.loads(json.dumps(SCOPE));ctx['scopes'].reverse();b=execution_scopes(ctx)
        self.assertEqual({k:execution_identity('revenue-recognition',v) for k,v in a.items()},{k:execution_identity('revenue-recognition',v) for k,v in b.items()})
    def test_insertion_no_owner_identity_change(self):
        ctx=copy.deepcopy(SCOPE);ctx['scopes'].append(replace(ROWS[1],scope_id='OTHER',legal_entity_id='OTHER').record());a=execution_scopes(SCOPE);b=execution_scopes(ctx)
        self.assertEqual(execution_identity('revenue-recognition',a['ENTITY-US']),execution_identity('revenue-recognition',b['ENTITY-US']))
    def test_group_journal_legal_posting_coordinated_relabel(self):
        r=self.native('GROUP-EUR');r.update(posting_scope='ENTITY-US',accounting_layer='LEGAL_ENTITY',currency='USD')
        with self.assertRaises(ValueError):allocate_scoped([r],SCOPE,[self.event(r)])
    def test_legal_journal_group_posting_coordinated_relabel(self):
        r=self.native();r.update(posting_scope='GROUP-EUR',accounting_layer='GROUP',currency='EUR')
        with self.assertRaises(ValueError):allocate_scoped([r],SCOPE,[self.event(r)])
    def test_alias_duplicate_across_two_native_lines(self):
        r=self.native();r['journals'].append(copy.deepcopy(r['journals'][0]));r['journals'][1][0]['account']='Renamed receivable';e=self.event(r);other=copy.deepcopy(e);other['primary'][0]['index']=1
        with self.assertRaises(ValueError):allocate_scoped([r],SCOPE,[e,other])
    def test_legitimate_cross_scope_nonduplicate(self):
        a=self.native('ENTITY-NL');b=self.native('ENTITY-US');self.assertEqual(len(allocate_scoped([a,b],SCOPE,[self.event(a),self.event(b)])[0]),2)
    def test_public_nested_internal_identifiers_absent(self):
        s=json.dumps(CAO().public(run().case));self.assertFalse(any(x in s for x in ('exec:','payload_fingerprint','case_fingerprint','result_fingerprint','source_population','source-ENTITY')))
    def test_artifact_regeneration_exact(self):
        from orchestration.tests.generate_scope_examples import artifacts
        self.assertEqual(json.dumps(artifacts(),sort_keys=True,default=str),json.dumps(artifacts(),sort_keys=True,default=str))
    def test_group_generic_registry_and_owner_nodes(self):
        from orchestration.tests.group_fixtures import run as group_run
        c=group_run(True).case;self.assertEqual(c.outcome,'complete');self.assertTrue(c.scope_registry);self.assertTrue(all(n.id.startswith('exec:') for n in c.graph.nodes.values()))
    def test_single_entity_automatic_registry(self):
        from orchestration.tests.fixtures import revenue
        native=revenue();native['functional_currency']='EUR';native=finalize('revenue-recognition',native)
        c=CAO().run(dict(case_id='qa-single',objective='Review revenue',scope={k:SCOPE[k] for k in ('framework','jurisdiction','period_start','reporting_period','currency')}|{'entity':native['entity']},facts={'customer_contract':native}))
        self.assertEqual(len(c.scope_registry),1);self.assertEqual(c.outcome,'complete')

if __name__=='__main__':unittest.main()
