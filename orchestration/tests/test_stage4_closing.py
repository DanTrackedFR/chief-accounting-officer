"""Closing-date milestone and complete current population, safe historical refusal."""
import copy
import unittest
from decimal import Decimal
from orchestration.tests import stage4_closing_fixtures as closing, stage4_closing_population as full, stage4_fixtures as s4,stage4_correction_fixtures as prior
from orchestration.stage3 import validate_native_bindings,validate_group_loan_population
from orchestration.runtime import CAO
from orchestration.governed_plan import observation


class ClosingPopulation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.control,cls.record=full.run()
    def setUp(self):self.f=copy.deepcopy(self.control);self.r=copy.deepcopy(self.record);self.e=self.f['session'];self.n=self.f['nodes']
    def test_original_conflict_stays_immutable(self):
        old=self.r['before']['fx-ENTITY-UK'];self.assertEqual(self.e.versions.versions[old.version_id],old)
        self.assertEqual(old.payload()['calculations']['pairs'][0]['a_functional'],'16.00')
        self.assertEqual(self.r['before']['match-fx'].payload()['matching']['classification'],'FX_DIFFERENCE')
        self.assertEqual(self.r['before']['fx-reassessment'].payload()['calculations']['pairs'][0]['b_functional'],'18.00')
    def test_current_native_legal_and_translation_economics(self):
        pair=self.e.versions.current(self.n['fx-ENTITY-UK'].id).payload()['calculations']['pairs'][0]
        self.assertEqual((pair['a_functional'],pair['a_fx_gain']),('18.00','2.00'))
        for label,profit in [('fx-translation-ENTITY-UK','2.00'),('whole-translation-ENTITY-UK','2.00')]:
            result=self.e.versions.current(self.n[label].id).payload();self.assertEqual(result['calculations']['translation']['profit_translated'],profit);self.assertEqual(result['journal_entry_implications'],[])
    def test_four_material_current_relationships_enter_group(self):
        source=self.e.sources[self.n['elimination'].id]
        self.assertEqual({p['transaction_id'] for p in source['intercompany']},{'clean','mismatch','timing','fx'})
        validate_native_bindings(self.e,self.n['elimination'],source,s4.s3.receipts(self.f,self.n['elimination'].id))
        self.assertEqual(len(source['group_population_coverage']['required_legal_result_versions']),8)
    def test_group_native_accounting_not_receipt_only(self):
        result=self.e.versions.current(self.n['elimination'].id).payload();self.assertEqual(result['status'],'complete')
        self.assertEqual(len(result['journal_entry_implications']),6)
        balances=result['calculations']['consolidated_balances']
        for account in ('ic payable','uk payable','clean loan','mismatch loan','timing loan','timing payable','fx loan','fx payable','investment'):
            self.assertEqual(Decimal(balances[account]),0)
        self.assertEqual(result['calculations']['equity']['profit'],'3')
        self.assertEqual(result['calculations']['equity']['closing'],'490')
        self.assertEqual(result['calculations']['cash_flow']['financing'],'0')
    def test_group_residual_is_zero_from_native_accounting(self):
        pair=self.e.versions.current(self.n['fx-reassessment'].id).payload()['calculations']['pairs'][0]
        self.assertEqual(Decimal(pair['a_functional'])-Decimal(pair['b_functional']),0)
        self.assertEqual(pair['foreign_principal'],'20');self.assertEqual(self.e.versions.current(self.n['fx-reassessment'].id).payload()['journal_entry_implications'],[])
    def test_exact_once_excludes_old_legal_and_group_versions(self):
        ledger=full.exact_once(self.f);self.assertEqual(len(ledger['native_journal_inventory']),8);self.assertEqual(ledger['release_selection'],'REFUSED')
        self.assertEqual(len({(x['result_version'],tuple((p['owner'],p['index']) for p in x['primary'])) for x in ledger['events']}),8)
        for row in ledger['native_journal_inventory']:self.assertEqual(self.e.versions.state(row['result_version']),'CURRENT')
        for old in ledger['superseded_excluded']:self.assertNotIn(old,{row['result_version'] for row in ledger['native_journal_inventory']})
    def test_selective_closing_rework_derived_and_unrelated_current(self):
        p=self.r['closing_correction'];self.assertEqual(p['execution_order'],self.e.topological(p['execution_order']))
        self.assertIn(self.n['whole-translation-ENTITY-UK'].id,p['execution_order']);self.assertNotIn(self.n['whole-translation-ENTITY-US'].id,p['execution_order'])
        before=self.r['before']['fx-ENTITY-US'];self.assertEqual(self.e.versions.current(before.node_id),before)
        for label in ('timing-ENTITY-NL','timing-current-ENTITY-NL','timing-effective-ENTITY-NL'):
            self.assertEqual(self.e.versions.current(self.n[label].id),self.r['before'][label])
    def test_actual_native_comparative_refusal_keeps_case_partial(self):
        refusal=self.r['closing_rework']['native_refusal'];self.assertEqual(refusal['status'],'blocked')
        self.assertIn('Restated comparative equity differs from opening current equity',refusal['conclusion'])
        self.assertEqual(refusal['calculations'],{});self.assertEqual(refusal['journal_entry_implications'],[])
        self.assertEqual(self.f['case'].outcome,'partial');self.assertNotEqual(self.f['case'].status,'CLOSED')
        for label in ('reporting','analytics','group'):
            self.assertEqual(self.e.versions.state(self.e.versions.current(self.n[label].id,allow_stale=True).version_id),'STALE')
        self.assertEqual(CAO().public(self.f['case'])['status'],'partial');self.assertFalse(CAO().public(self.f['case']).get('calculations'))
    def test_closure_without_genuine_reviewed_comparative_is_rejected(self):
        with self.assertRaises(ValueError):self.f['case'].transition('CLOSED')
    def test_population_cannot_omit_legal_side_or_current_legal_version(self):
        original=self.e.sources[self.n['elimination'].id]
        for version in original['group_population_coverage']['required_legal_result_versions']:
            c=copy.deepcopy(original);c['group_population_coverage']['required_legal_result_versions'].remove(version)
            with self.subTest(version=version),self.assertRaises(ValueError):validate_group_loan_population(self.e,self.n['elimination'],c,c['versioned_dependency_receipts'])
    def test_population_cannot_shorten_legal_perimeter(self):
        for scope in ('ENTITY-NL','ENTITY-US','ENTITY-UK'):
            c=copy.deepcopy(self.e.sources[self.n['elimination'].id]);c['entities']=[x for x in c['entities'] if x['id']!=scope]
            with self.subTest(scope=scope),self.assertRaises(ValueError):validate_group_loan_population(self.e,self.n['elimination'],c,c['versioned_dependency_receipts'])
    def test_each_group_dependency_or_exact_current_receipt_is_required(self):
        source=self.e.sources[self.n['elimination'].id]
        for index,row in enumerate(source['versioned_dependency_receipts']):
            c=copy.deepcopy(source);c['versioned_dependency_receipts'].pop(index)
            with self.subTest(dependency=row['dependency_id']),self.assertRaises(ValueError):validate_native_bindings(self.e,self.n['elimination'],c,s4.s3.receipts(self.f,self.n['elimination'].id))
    def test_whole_operation_signed_row_cannot_change(self):
        for label in ('whole-translation-ENTITY-US','whole-translation-ENTITY-UK'):
            c=copy.deepcopy(self.e.sources[self.n[label].id]);c['translation']['tb'][1]['balance']='18'
            with self.subTest(label=label),self.assertRaises(ValueError):validate_native_bindings(self.e,self.n[label],c,s4.s3.receipts(self.f,self.n[label].id))
    def test_parent_current_native_profit_has_exact_dependency(self):
        c=copy.deepcopy(self.e.sources[self.n['elimination'].id]);c['entities'][0]['balances']['correction income']='-2'
        with self.assertRaises(ValueError):validate_native_bindings(self.e,self.n['elimination'],c,s4.s3.receipts(self.f,self.n['elimination'].id))
    def test_superseded_transformation_and_wrong_dimensions_rejected(self):
        receipts=s4.s3.receipts(self.f,self.n['fx-reassessment'].id)
        row=next(x for x in receipts if x['producer_scope']=='ENTITY-UK')
        for key,value in [('producer_scope','ENTITY-NL'),('producer_period',self.f['periods']['CALENDAR-SEP'].period_id),('value_currency','GBP'),('producer_framework','IFRS'),('result_version',self.r['before']['fx-translation-ENTITY-UK'].version_id)]:
            x=copy.deepcopy(row);x[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):self.e.validate_receipt(x,self.n['fx-reassessment'].id)


if __name__=='__main__':unittest.main()
