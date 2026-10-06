"""Authored Stage 3 acceptance and permanent adversarial controls."""
import copy
import unittest
from dataclasses import replace, asdict
from orchestration.tests.stage3_fixtures import *
from orchestration.intercompany_network import RESIDUALS


class Stage3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base=ordinary_initial()
    def setUp(self):
        self.f=copy.deepcopy(self.base);self.e=self.f['session'];self.n=self.f['nodes']
    def test_business_triangle_and_acyclic_execution(self):
        net=network(self.f);edges=set(net.relationships())
        self.assertTrue(net.has_business_cycle())
        self.assertTrue({('ENTITY-US','ENTITY-NL'),('ENTITY-NL','ENTITY-UK'),('ENTITY-UK','ENTITY-US')}<=edges)
        self.e.graph.validate()
        self.assertEqual(len(self.e.topological(self.e.graph.nodes)),17)
    def test_all_residual_categories_registered(self):
        self.assertEqual(len(RESIDUALS),7)
    def test_four_relationships_and_both_legal_sides(self):
        net=network(self.f)
        self.assertEqual(len(net.sides),8);self.assertEqual(len(net.decisions),4)
        self.assertEqual({d.classification for d in net.decisions.values()},{'MATCHED','TIMING_DIFFERENCE','FX_DIFFERENCE','UNRESOLVED_MISMATCH'})
    def test_cross_period_preserved(self):
        ss=sides(self.f,'timing');self.assertNotEqual(ss[0].period_id,ss[1].period_id)
        self.assertEqual(ss[0].counterparty_period,ss[1].period_id)
    def test_multi_currency_amounts_preserved(self):
        ss=sides(self.f,'clean');self.assertEqual([s.functional_currency for s in ss],['USD','EUR'])
        self.assertEqual([s.functional_amount for s in ss],['100.00','90.00'])
        self.assertEqual([s.transaction_amount for s in ss],['90','90'])
    def test_unresolved_relationship_blocks_clean_case_closure(self):
        self.assertEqual(self.f['case'].outcome,'partial');self.assertNotEqual(self.f['case'].status,'CLOSED')
    def test_counterparty_fail_closed(self):
        for value in ('unknown','GROUP-EUR','ENTITY-US'):
            with self.subTest(value=value),self.assertRaises(ValueError):
                replace(sides(self.f,'clean')[0],counterparty_scope=value).validate(self.e)
    def test_subgroup_counterparty_rejected(self):
        from orchestration.scopes import Scope
        self.e.cases.scopes=ScopeRegistry(self.e.cases.scopes.record()+[Scope('SUB','SUBGROUP','Subgroup',framework='IFRS',jurisdiction='NL',presentation_currency='EUR',provenance=EVIDENCE).record()])
        with self.assertRaises(ValueError):replace(sides(self.f,'clean')[0],counterparty_scope='SUB').validate(self.e)
    def test_transaction_ids_not_amount_based(self):
        side=sides(self.f,'clean')[0]
        self.assertNotEqual(side.side_id,replace(side,economic_id='another-transaction').side_id)
        self.assertEqual(side.side_id,replace(side,functional_amount='999').side_id)
    def test_account_and_display_aliases_do_not_change_identity(self):
        side=sides(self.f,'clean')[0];before=side.side_id
        self.e.cases.scopes=ScopeRegistry([replace(self.e.cases.scopes.get(r['scope_id']),display_name='New label') for r in self.e.cases.scopes.record()])
        self.assertEqual(before,side.validate(self.e).side_id)
    def test_source_row_and_native_metric_substitution(self):
        for field,value in [('source_fingerprint','bad'),('functional_amount','101.00'),('transaction_amount','91'),('economic_id','alias'),('book_entry_id','alias')]:
            with self.subTest(field=field),self.assertRaises(ValueError):replace(sides(self.f,'clean')[0],**{field:value}).validate(self.e)
    def test_alias_cannot_reuse_legal_book_event(self):
        net=IntercompanyNetwork(self.e,'STAGE3-NETWORK');side=sides(self.f,'clean')[0];net.register(side)
        with self.assertRaises(ValueError):net.register(side)
    def test_wrong_version_dimensions(self):
        a,b=sides(self.f,'clean')
        with self.assertRaises(ValueError):replace(a,result_version=b.result_version).validate(self.e)
    def test_residual_cannot_be_forced_matched(self):
        source=match_source(self.f,'mismatch');d=MatchingDecision(**source['decision'])
        with self.assertRaises(ValueError):replace(d,classification='MATCHED').validate(sides(self.f,'mismatch'))
    def test_decision_requires_exact_current_versions(self):
        source=match_source(self.f,'clean');d=MatchingDecision(**source['decision'])
        with self.assertRaises(ValueError):replace(d,result_versions=('vfake',)).validate(sides(self.f,'clean'))
    def test_business_edges_do_not_create_dependencies(self):
        before={n.id:tuple(n.dependencies) for n in self.n.values()};network(self.f)
        self.assertEqual(before,{n.id:tuple(n.dependencies) for n in self.n.values()})
    def test_dependency_cycle_rejected(self):
        with self.assertRaises(ValueError):add_edge(self.f,'group','clean-ENTITY-US',('observed_results',))
    def test_translation_owner_receipt_and_rate_lineage(self):
        b=self.f['basis'];u=self.e.versions.current(self.n['clean-ENTITY-US'].id);t=self.e.versions.current(self.n['translation'].id)
        r=b.translation(u.version_id,t.version_id,'clean',('calculations','pairs',0,'a_functional'),('translation','tb',1,'balance'),('calculations','translation','translated_tb','ic loan'),EVIDENCE)
        self.assertEqual(r['value'],'90.00');self.assertEqual(r['target_currency'],'EUR');self.assertTrue(r['rate_source']);b.validate_transformation(r)
    def test_framework_qualified_native_reassessment(self):
        b=self.f['basis'];t=self.e.versions.current(self.n['translation'].id);c=self.e.versions.current(self.n['conversion'].id)
        r=b.intercompany_conversion(t.version_id,c.version_id,'clean',('calculations','translation','translated_tb','ic loan'),EVIDENCE)
        self.assertEqual((r['source_framework'],r['target_framework']),('US_GAAP','IFRS'));self.assertEqual(r['adjustment'],'0');b.validate_transformation(r)
    def test_unsupported_conversion_stays_unresolved(self):
        u=self.e.versions.current(self.n['clean-ENTITY-US'].id)
        result=self.f['basis'].unsupported_conversion(u.version_id,'IFRS','arbitrary')
        self.assertEqual(result['status'],'unresolved');self.assertIsNone(result['owner'])
    def test_native_source_mapping_omission_rejected(self):
        source=downstream_source(self.f,'translation');source.pop('stage3_input_bindings');source=certify('foreign-currency',source)
        with self.assertRaises(ValueError):execute(self.f,'translation',source)
    def test_native_translation_input_substitution_rejected(self):
        source=downstream_source(self.f,'translation');source['translation']['tb'][1]['balance']='101';source=certify('foreign-currency',source)
        with self.assertRaises(ValueError):execute(self.f,'translation',source)
    def test_fs_cannot_substitute_balanced_unqualified_tb(self):
        source=downstream_source(self.f,'reporting');source['current_tb'][0]['balance']='0';source=certify('financial-statements',source)
        with self.assertRaises(ValueError):execute(self.f,'reporting',source)
    def test_correction_selectively_stales_six_consumers(self):
        before={label:self.e.versions.current(n.id) for label,n in self.n.items()};p=correct(self.f)
        self.assertEqual([self.e.graph.nodes[k].logical_id for k in p['execution_order']],['match-clean','translation','conversion','elimination','reporting','group'])
        self.assertEqual(self.e.versions.state(before['clean-ENTITY-US'].version_id),'SUPERSEDED')
        for label in ('match-timing','match-fx','match-mismatch','fx-ENTITY-US','mismatch-ENTITY-UK'):
            self.assertEqual(before[label],self.e.versions.current(self.n[label].id))
    def test_selective_reexecute_updates_group_owner_result(self):
        p=correct(self.f);ledger=rework(self.f,p);self.assertEqual(len(ledger),6)
        equity=self.e.versions.current(self.n['elimination'].id).payload()['calculations']['equity']
        self.assertEqual((equity['closing'],equity['profit'],equity['oci']),('381.82','8.18','-16.36'))
    def test_old_receipts_rejected_after_correction(self):
        key=self.f['edges'][('clean-ENTITY-US','translation')];r=self.e.receipt(key);correct(self.f)
        with self.assertRaises(ValueError):self.e.validate_receipt(r,self.n['translation'].id)
    def test_unnecessary_selective_reexecution_rejected(self):
        p=correct(self.f);p['execution_order'].append(self.n['match-fx'].id)
        with self.assertRaises(ValueError):self.e.reexecute(p,{}, {})
    def test_wrong_order_rejected(self):
        p=correct(self.f);p['execution_order'].reverse()
        with self.assertRaises(ValueError):self.e.reexecute(p,{}, {})
    def test_prior_conversion_receipt_cannot_survive_rework(self):
        b=self.f['basis'];t=self.e.versions.current(self.n['translation'].id);c=self.e.versions.current(self.n['conversion'].id)
        r=b.intercompany_conversion(t.version_id,c.version_id,'clean',('calculations','translation','translated_tb','ic loan'),EVIDENCE);rework(self.f,correct(self.f))
        with self.assertRaises(ValueError):b.validate_transformation(r)
    def test_transaction_identity_composes_without_changing_legacy(self):
        context=dict(scope_id='ENTITY-US',scope_type='LEGAL_ENTITY',framework='US_GAAP',jurisdiction='US',functional_currency='USD',presentation_currency=None,period_start='2026-10-01',reporting_period='2026-10-31')
        legacy=execution_identity('intercompany-accounting',context)
        self.assertEqual(legacy,execution_identity('intercompany-accounting',dict(context,economic_id=None)))
        self.assertNotEqual(legacy,execution_identity('intercompany-accounting',dict(context,economic_id='a')))
        self.assertNotEqual(execution_identity('intercompany-accounting',dict(context,economic_id='a')),execution_identity('intercompany-accounting',dict(context,economic_id='b')))
    def test_public_result_preserves_residual_and_qualified_group_values(self):
        result=CAO().public(self.f['case']);self.assertEqual(result['status'],'partial');self.assertTrue(result['open_items'])
        text=str(result)
        for value in ('synthetic independent','reviewer_signoff','source_fingerprint','source_population','version:'):
            self.assertNotIn(value,text)
    def test_public_delivery_blocked_during_rework(self):
        CAO().correct(self.f['case'],self.n['clean-ENTITY-US'].id,legal_source(self.f,'clean','ENTITY-US',True),'Reviewed correction')
        result=CAO().public(self.f['case']);self.assertEqual(result['status'],'partial');self.assertNotIn('381.82',str(result))

    def test_cross_layer_receipts_reject_field_substitution(self):
        b=self.f['basis'];key=self.f['edges'][('conversion','elimination')];r=b.receipt(key)
        for field,value in [('producer_layer','LEGAL_ENTITY'),('framework','US_GAAP'),('currency','USD'),('economic_id','other'),('producer_period','wrong'),('consumer_scope','ENTITY-NL'),('currentness','STALE')]:
            with self.subTest(field=field),self.assertRaises(ValueError):b.validate(replace(r,**{field:value}),r.consumer_node)
    def test_cross_layer_raw_local_basis_cannot_feed_group(self):
        b=ReportingBasis(self.e);key=self.f['edges'][('clean-ENTITY-NL','elimination')]
        self.e.versions.active.pop(self.n['elimination'].id)
        with self.assertRaises(ValueError):b.declare(key,producer_layer='LEGAL_ENTITY',consumer_layer='GROUP_ELIMINATION',framework='US_GAAP',currency='USD',semantic_metric='ordinary_reciprocal_balance',economic_id='clean',required_framework='IFRS',required_currency='EUR',evidence=EVIDENCE)
    def test_translation_receipt_carries_presentation_currency(self):
        r=self.e.receipt(self.f['edges'][('translation','conversion')])
        self.assertEqual(r['value_currency'],'EUR');self.assertEqual(r['producer_framework'],'US_GAAP')
    def test_native_conversion_needs_actual_counterparty_receipt(self):
        source=downstream_source(self.f,'conversion');source['stage3_input_bindings']=source['stage3_input_bindings'][:1]
        with self.assertRaises(ValueError):execute(self.f,'conversion',certify('intercompany-accounting',source))
    def test_current_posting_layers_are_distinct(self):
        rework(self.f,correct(self.f));ctx,events,d=journal_inputs(self.f)
        selected,ledger=self.f['basis'].current_journals(ctx,events,d)
        self.assertEqual(len(selected),3)
        self.assertEqual(sum(event['posting_scope']=='ENTITY-US' for event in ledger),1)
        self.assertEqual(sum(event['posting_scope']=='GROUP-EUR' for event in ledger),2)
        self.assertEqual(len({event['allocated_identity'] for event in ledger}),3)
    def test_old_and_replacement_elimination_cannot_both_post(self):
        ctx,events,d=journal_inputs(self.f);old=copy.deepcopy(events);rework(self.f,correct(self.f));ctx,current,d=journal_inputs(self.f)
        with self.assertRaises(ValueError):self.f['basis'].current_journals(ctx,current+old,d)
    def test_translation_never_posts_to_legal_books(self):
        rework(self.f,correct(self.f));ctx,events,d=journal_inputs(self.f)
        with self.assertRaises(ValueError):self.e.current_journals(ctx,events)
        with self.assertRaises(ValueError):self.f['basis'].current_journals(ctx,events,[])
    def test_duplicate_posting_alias_cannot_evade_allocator(self):
        ctx,events,d=journal_inputs(self.f);alias=copy.deepcopy(events[0]);alias['economic_id']='new-label'
        with self.assertRaises(ValueError):self.f['basis'].current_journals(ctx,events+[alias],d)
    def test_superseded_legal_side_is_not_current(self):
        old=sides(self.f,'clean')[0];correct(self.f)
        with self.assertRaises(ValueError):old.validate(self.e)
    def test_missing_counterparty_remains_residual(self):
        ss=sides(self.f,'clean');net=IntercompanyNetwork(self.e,'STAGE3-NETWORK');net.register(ss[0])
        decision=MatchingDecision(ss[0].relationship_id,(ss[0].side_id,),'MISSING_COUNTERPARTY',EVIDENCE,(ss[0].result_version,),'reviewer','Missing current reciprocal source')
        result=net.match(decision);self.assertEqual(result['classification'],'MISSING_COUNTERPARTY');self.assertIsNone(result['correction'])
    def test_unresolved_numeric_difference_is_visible_not_forced(self):
        value=self.e.versions.current(self.n['match-mismatch'].id).payload()['matching']
        self.assertEqual(value['transaction_residual'],'-1');self.assertEqual(value['transaction_residual_currency'],'EUR');self.assertIsNone(value['correction'])

if __name__=='__main__':unittest.main()
