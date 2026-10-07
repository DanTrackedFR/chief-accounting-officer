"""Authored governed correction milestone: honest Outcome B, never closure."""
import copy
import unittest
from decimal import Decimal
from orchestration.tests import stage4_correction_fixtures as fixture, stage4_fixtures as s4
from orchestration.runtime import CAO
from orchestration.governed_plan import observation
from orchestration.stage3 import validate_native_bindings


class CorrectionPath(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.control,cls.record=fixture.run()
    def setUp(self):self.f=copy.deepcopy(self.control);self.r=copy.deepcopy(self.record);self.e=self.f['session'];self.n=self.f['nodes']
    def test_native_owner_remeasures_evidenced_opening_without_target_rate(self):
        source=self.e.sources[self.n['fx-ENTITY-UK'].id];old=self.r['before']['fx-ENTITY-UK'].payload()['facts_used'];p=source['pairs'][0]
        self.assertEqual((p['opening_book_a'],p['book_a']),('15','15'))
        for k in ('rate_a','rate_b','gl_a','gl_b','confirmed_a','confirmed_b','currency','entity_a','entity_b','transaction_id'):
            self.assertEqual(p[k],old['pairs'][0][k])
        result=self.e.versions.current(self.n['fx-ENTITY-UK'].id).payload()
        self.assertEqual(result['calculations']['pairs'][0]['a_functional'],'16.00')
        self.assertEqual(result['calculations']['pairs'][0]['a_fx_gain'],'1.00')
        self.assertEqual(result['calculations']['journal_entities'],['ENTITY-UK'])
    def test_fresh_sealed_evidence_preserves_dimensional_and_economic_identity(self):
        row=self.f['replacement_intakes'][0];pack=row['reviewed_pack'];source=self.e.sources[row['node']]
        self.assertEqual(pack.scoped_packs[0].request['source'],source)
        self.assertEqual(source['intercompany_transactions'],self.r['before']['fx-ENTITY-UK'].payload()['facts_used']['intercompany_transactions'])
        self.assertTrue(source['correction_evidence']['reviewed'])
        self.assertEqual(source['correction_evidence']['source_id'],'UK-IC-OPEN-02')
        self.assertTrue(source['qualified_input_snapshot']['source_id'].startswith('replacement-snapshot-'))
    def test_old_result_is_immutable_superseded_new_is_current(self):
        old=self.r['before']['fx-ENTITY-UK'];new=self.e.versions.current(self.n['fx-ENTITY-UK'].id)
        self.assertEqual(self.e.versions.state(old.version_id),'SUPERSEDED');self.assertEqual(new.predecessor,old.version_id)
        self.assertEqual(self.e.versions.versions[old.version_id],old)
        self.assertEqual(self.e.versions.state(new.version_id),'CURRENT')
    def test_actual_downstream_consumers_stale_and_unrelated_current(self):
        plan=self.r['plan'];affected=set(plan['execution_order'])
        for label,v in self.r['before'].items():
            if self.n[label].id in affected:self.assertEqual(self.r['stale'][label]['state'],'STALE')
            elif label!='fx-ENTITY-UK':
                self.assertEqual(self.e.versions.current(self.n[label].id).version_id,v.version_id)
                self.assertEqual(self.e.versions.state(v.version_id),'CURRENT')
        self.assertIn(self.n['elimination'].id,affected);self.assertNotIn(self.n['fx-translation-ENTITY-US'].id,affected)
        self.assertEqual(plan['execution_order'],self.e.topological(affected))
    def test_current_match_uses_both_exact_legal_versions_preserves_history(self):
        match=self.e.versions.current(self.n['match-fx-current'].id).payload()['matching']
        self.assertEqual(match['classification'],'MATCHED');self.assertEqual(match['transaction_residual'],'0')
        self.assertEqual(set(match['result_versions']),{self.e.versions.current(self.n[x].id).version_id for x in ('fx-ENTITY-UK','fx-ENTITY-US')})
        self.assertEqual(self.r['before']['match-fx'].payload()['matching']['classification'],'FX_DIFFERENCE')
        self.assertEqual(self.e.versions.versions[self.r['before']['match-fx'].version_id].payload(),self.r['before']['match-fx'].payload())
    def test_translation_and_reassessment_retains_two_eur_residual(self):
        t=self.e.versions.current(self.n['fx-translation-ENTITY-UK'].id).payload()['calculations']['translation']
        self.assertEqual(t['profit_translated'],'1.00');self.assertEqual(t['cta_movement'],'0.00')
        self.assertEqual(t['translated_tb']['ic loan'],'16.00')
        self.assertEqual(self.r['residual']['signed_receivable_minus_payable'],'-2.00')
        self.assertTrue(self.r['residual']['material']);self.assertEqual(self.r['residual']['disposition'],'UNRESOLVED')
        self.assertEqual(self.e.versions.current(self.n['fx-reassessment'].id).payload()['journal_entry_implications'],[])
    def test_group_dependency_qualified_but_accounting_reporting_refresh_blocked(self):
        receipt=self.r['qualified_group_dependency'];self.f['basis'].validate(receipt,self.n['elimination'].id)
        self.assertEqual(receipt.value,'16.00')
        for label in ('elimination','reporting','analytics','group'):
            v=self.e.versions.current(self.n[label].id);self.assertEqual(v.payload()['status'],'blocked')
            self.assertEqual(v.payload()['journal_entry_implications'],[])
            self.assertNotEqual(v.version_id,self.r['before'][label].version_id)
        self.assertEqual(self.f['case'].outcome,'partial');self.assertNotEqual(self.f['case'].status,'CLOSED')
        with self.assertRaises(ValueError):self.f['case'].transition('CLOSED')
    def test_current_journals_have_native_fx_once_without_old_or_group_duplicates(self):
        v=self.e.versions.current(self.n['fx-ENTITY-UK'].id)
        event=dict(economic_id='fx-opening-correction',posting_scope=v.scope_id,period_id=v.period_id,period=self.n['fx-ENTITY-UK'].period,currency='GBP',result_version=v.version_id,primary=[dict(owner=v.node_id,index=0)],witnesses=[],evidence='Reviewed native current UK monetary journal')
        context=dict(entity='GROUP-EUR',framework='IFRS',jurisdiction='NL',currency='EUR',period_start='2026-10-01',reporting_period='2026-10-31',scopes=self.e.cases.scopes.record(),period_registry=self.e.periods.record())
        selected,allocation=self.e.current_journals(context,[event])
        self.assertEqual(len(selected),1)
        self.assertEqual(allocation[0]['result_version'],v.version_id)
        self.assertEqual(selected[0]['lines'],[{'side':'Dr','account':'intercompany receivable','amount':'1.00'},{'side':'Cr','account':'FX gain or loss','amount':'1.00'}])
        self.assertNotEqual(allocation[0]['result_version'],self.r['before']['fx-ENTITY-UK'].version_id)
        event['result_version']=self.r['before']['fx-ENTITY-UK'].version_id
        with self.assertRaises(ValueError):self.e.current_journals(context,[event])
    def test_public_refresh_partial_no_accounting_totals_or_private_evidence(self):
        public=CAO().public(self.f['case']);self.assertEqual(public['status'],'partial');self.assertFalse(public.get('calculations'))
        self.assertNotIn('UK-IC-OPEN-02',str(public));self.assertNotIn('reviewer',str(public).lower())
    def test_wrong_lineage_equal_value_reassessment_rejects(self):
        n=self.n['fx-reassessment'];c=copy.deepcopy(self.e.sources[n.id]);c['stage3_input_bindings'][0]['dependency_id']=self.f['edges'][('translation','conversion')]
        with self.assertRaises(ValueError):validate_native_bindings(self.e,n,c,s4.s3.receipts(self.f,n.id))
    def test_superseded_equal_value_receipt_rejects(self):
        c=copy.deepcopy(self.e.sources[self.n['fx-reassessment'].id]);row=next(r for r in c['versioned_dependency_receipts'] if r['producer_scope']=='ENTITY-UK')
        old=self.r['before'][self.e.graph.nodes[row['producer_node']].logical_id]
        row['result_version']=old.version_id
        with self.assertRaises(ValueError):self.e.validate_receipt(row,self.n['fx-reassessment'].id)
    def test_complete_population_guard_remains_active_after_other_conflict_corrected(self):
        plan=s4.correct(self.f)
        refused=False
        for key in plan['execution_order']:
            label=self.e.graph.nodes[key].logical_id
            try:self.e.execute(key,observation,s4.qualified_replacement(self.f,key,fixture.source(self.f,label)),'Dependency rework: '+plan['new_version'])
            except ValueError as error:
                self.assertIn('Full Group accounting omits or duplicates',str(error));refused=True;break
        self.assertTrue(refused);self.assertNotEqual(self.f['case'].status,'CLOSED')
        self.assertEqual(self.e.versions.current(self.n['fx-reassessment'].id).payload()['calculations']['pairs'][0]['b_functional'],'18.00')

    def test_full_current_roster_cannot_omit_corrected_or_counterparty_version(self):
        from orchestration.stage3 import current_legal_loan_versions,validate_group_loan_population
        node=self.n['elimination'];perimeter={'ENTITY-NL','ENTITY-UK','ENTITY-US'}
        roster=current_legal_loan_versions(self.e,node,perimeter)
        receipts=[dict(metric_path=['matching','classification'],result_version=self.e.versions.current(self.n[label].id).version_id) for label in ('match-clean','match-mismatch','match-timing-current','match-fx-current')]
        source=dict(entities=[dict(id=k) for k in sorted(perimeter)],group_population_coverage=dict(mode='ALL_CURRENT_LOAN_SIDES',required_legal_result_versions=roster))
        validate_group_loan_population(self.e,node,source,receipts)  # Coverage only, no accounting acceptance.
        for label in ('fx-ENTITY-UK','fx-ENTITY-US'):
            attack=copy.deepcopy(source);attack['group_population_coverage']['required_legal_result_versions'].remove(self.e.versions.current(self.n[label].id).version_id)
            with self.subTest(omitted=label),self.assertRaises(ValueError):validate_group_loan_population(self.e,node,attack,receipts)
    def test_current_transformation_omission_rejected_at_group_reassessment(self):
        c=fixture.reassessment_source(self.f)
        for scope in ('ENTITY-UK','ENTITY-US'):
            attack=copy.deepcopy(c);attack['versioned_dependency_receipts']=[r for r in attack['versioned_dependency_receipts'] if r['producer_scope']!=scope]
            with self.subTest(omitted=scope),self.assertRaises(ValueError):validate_native_bindings(self.e,self.n['fx-reassessment'],attack,attack['versioned_dependency_receipts'])
    def test_group_dependency_omission_in_sealed_replacement_rejected(self):
        from orchestration.intake.governed import qualify_replacement
        key=self.n['elimination'].id
        correction=s4.correct(self.f)
        for node_id in correction['execution_order']:
            if node_id==key:break
            label=self.e.graph.nodes[node_id].logical_id
            self.e.execute(node_id,observation,s4.qualified_replacement(self.f,node_id,fixture.source(self.f,label)),'Dependency rework: '+correction['new_version'])
        engine,prepared,pack,raw=s4.replacement_intake(self.f,key,fixture.source(self.f,'elimination'))
        plan=pack.request['governed_plan'];plan['dependencies']=[edge for edge in plan['dependencies'] if edge['producer_node']!=self.n['fx-reassessment'].id]
        with self.assertRaises(ValueError):qualify_replacement(engine,prepared,pack,self.f['case'],key)
    def test_wrong_dimensions_cannot_substitute_equal_value_receipt(self):
        n=self.n['fx-reassessment'];c=fixture.reassessment_source(self.f)
        row=next(r for r in c['versioned_dependency_receipts'] if r['producer_scope']=='ENTITY-UK')
        for field,value in [('producer_scope','ENTITY-NL'),('producer_period',self.f['periods']['CALENDAR-SEP'].period_id),('value_currency','GBP'),('producer_framework','IFRS')]:
            attack=copy.deepcopy(row);attack[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.e.validate_receipt(attack,n.id)
    def test_stale_and_superseded_equal_value_sources_cannot_refresh_group(self):
        receipt=fixture.reassessment_source(self.f)['versioned_dependency_receipts']
        for row in receipt:
            old=self.r['before'][self.e.graph.nodes[row['producer_node']].logical_id]
            if self.e.versions.state(old.version_id)=='SUPERSEDED':
                attack=copy.deepcopy(row);attack['result_version']=old.version_id
                with self.assertRaises(ValueError):self.e.validate_receipt(attack,self.n['fx-reassessment'].id)
        original=self.n['fx-ENTITY-US'];source=copy.deepcopy(self.e.sources[original.id]);source['fresh_equal_value_review']='Second independent unchanged legal evidence'
        from additional_cases import certify
        CAO().correct(self.f['case'],original.id,s4.qualified_replacement(self.f,original.id,certify('intercompany-accounting',source)),'Equal-value reviewed replacement')
        with self.assertRaises(ValueError):self.f['basis'].validate(self.r['qualified_group_dependency'],self.n['elimination'].id)


if __name__=='__main__':unittest.main()
