"""Independent correction path challenges; no positive Group closure claimed."""
import copy
import unittest
from decimal import Decimal
from dataclasses import replace
from orchestration.tests import stage4_correction_fixtures as fixture, stage4_fixtures as s4
from orchestration.runtime import CAO
from orchestration.stage3 import validate_native_bindings, validate_group_loan_population
from additional_cases import certify

class IndependentCorrection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.control,cls.result=fixture.run()
    def setUp(self):self.f=copy.deepcopy(self.control);self.r=copy.deepcopy(self.result);self.e=self.f['session'];self.n=self.f['nodes']
    def test_original_and_current_accounting_preserved(self):
        old=self.r['before']['fx-ENTITY-UK'];new=self.e.versions.current(self.n['fx-ENTITY-UK'].id)
        self.assertNotEqual(old.version_id,new.version_id)
        self.assertEqual(self.e.versions.state(old.version_id),'SUPERSEDED')
        self.assertEqual(self.e.versions.state(new.version_id),'CURRENT')
        self.assertEqual(old.payload()['calculations']['pairs'][0]['a_fx_gain'],'0.00')
        self.assertEqual(new.payload()['calculations']['pairs'][0]['a_fx_gain'],'1.00')
    def test_principal_rates_currencies_unchanged(self):
        c=self.e.sources[self.n['fx-ENTITY-UK'].id];old=self.r['before']['fx-ENTITY-UK'].payload()
        self.assertEqual(Decimal(c['pairs'][0]['rate_a']),Decimal('.8'))
        self.assertEqual(c['pairs'][0]['opening_a'],'20')
        self.assertEqual(c['pairs'][0]['currency'],'USD')
        self.assertEqual(old['calculations']['pairs'][0]['a_functional'],'16.00')
        self.assertEqual(self.e.versions.current(self.n['fx-ENTITY-UK'].id).payload()['calculations']['pairs'][0]['a_functional'],'16.00')
    def test_exact_once_native_journal_translation_no_duplicate(self):
        p=self.e.versions.current(self.n['fx-ENTITY-UK'].id).payload()
        self.assertEqual(p['calculations']['journal_entities'],['ENTITY-UK'])
        self.assertEqual(len(p['journal_entry_implications']),1)
        t=self.e.versions.current(self.n['fx-translation-ENTITY-UK'].id).payload()
        self.assertEqual(t['journal_entry_implications'],[])
        self.assertEqual(t['calculations']['translation']['profit_translated'],'1.00')
        self.assertEqual(t['calculations']['translation']['closing_cta'],'0.00')
    def test_residual_not_suppressed_by_principal_match(self):
        p=self.e.versions.current(self.n['fx-reassessment'].id).payload()['calculations']['pairs'][0]
        self.assertEqual(Decimal(p['a_functional'])-Decimal(p['b_functional']),Decimal('-2'))
        self.assertEqual(self.r['residual']['disposition'],'UNRESOLVED')
        self.assertNotIn(self.f['case'].status,('COMPLETE','CLOSED'))
        self.assertEqual(self.e.versions.current(self.n['elimination'].id).payload()['status'],'blocked')
    def test_unrelated_current_versions_unchanged(self):
        unaffected=set(self.r['plan']['unaffected'])
        for label,old in self.r['before'].items():
            if old.node_id in unaffected:
                self.assertEqual(self.e.versions.current(old.node_id).version_id,old.version_id)
                self.assertEqual(self.e.versions.state(old.version_id),'CURRENT')
    def test_translation_wrong_lineage_rejected(self):
        key=self.n['fx-translation-ENTITY-UK'].id;c=fixture.translation_source(self.f,'ENTITY-UK')
        c['versioned_dependency_receipts'][0]['result_version']=self.r['before']['fx-ENTITY-UK'].version_id
        with self.assertRaises(ValueError):
            self.e.execute(key,lambda _:None,c,'Wrong superseded lineage attack')
    def test_translation_owner_amount_substitution_rejected(self):
        c=fixture.translation_source(self.f,'ENTITY-UK');c['translation']['tb'][1]['balance']='18'
        with self.assertRaises(ValueError):validate_native_bindings(self.e,self.n['fx-translation-ENTITY-UK'],c,c['versioned_dependency_receipts'])
    def test_population_cannot_erase_corrected_legal_result(self):
        c=dict(entities=[],group_population_coverage=dict(mode='ALL_CURRENT_LOAN_SIDES',required_legal_result_versions=[]))
        with self.assertRaises(ValueError):validate_group_loan_population(self.e,self.n['elimination'],c,[])
    def test_reassessment_counterparty_translation_omission_rejected(self):
        c=fixture.reassessment_source(self.f)
        c['versioned_dependency_receipts']=[r for r in c['versioned_dependency_receipts'] if r['producer_scope']!='ENTITY-US']
        with self.assertRaises(ValueError):validate_native_bindings(self.e,self.n['fx-reassessment'],c,c['versioned_dependency_receipts'])
    def test_separate_reviewed_native_variation_drives_translation_profit(self):
        # CQA01 reproduction: legitimate alternate evidence changes gain, not closing.
        f=fixture.initial();key=f['nodes']['fx-ENTITY-UK'].id;c=fixture.reviewed_correction(f)
        c['pairs'][0].update(opening_book_a='14',book_a='14')
        c['correction_evidence']['reviewed_opening_book']='14'
        c['correction_evidence']['opening_operation'].update(receivable='14',capital='114')
        c=certify('intercompany-accounting',c)
        CAO().correct(f['case'],key,s4.qualified_replacement(f,key,c),'Independent alternate reviewed ledger')
        native=f['session'].versions.current(key).payload()['calculations']['pairs'][0]
        self.assertEqual(native['a_fx_gain'],'2.00');self.assertEqual(native['a_functional'],'16.00')
        translated=fixture.translation_source(f,'ENTITY-UK')['translation']
        self.assertEqual(Decimal(translated['profit']),Decimal(native['a_fx_gain']))
        self.assertEqual(Decimal(translated['opening_net_assets']),Decimal('114'))
    def test_contradictory_reviewed_operation_ledger_rejected(self):
        c=self.e.sources[self.n['fx-ENTITY-UK'].id]
        c['correction_evidence']['opening_operation']['receivable']='14'
        with self.assertRaisesRegex(ValueError,'ledger'):fixture.translation_source(self.f,'ENTITY-UK')
    def test_contradictory_reviewed_opening_summary_rejected(self):
        c=self.e.sources[self.n['fx-ENTITY-UK'].id]
        c['correction_evidence']['reviewed_opening_book']='14'
        with self.assertRaisesRegex(ValueError,'Correction evidence'):fixture.translation_source(self.f,'ENTITY-UK')
    def test_omitted_native_fx_profit_mapping_rejected(self):
        c=fixture.translation_source(self.f,'ENTITY-UK')
        c['stage3_input_bindings']=[b for b in c['stage3_input_bindings'] if b['target_path']!=['translation','tb',3,'balance']]
        with self.assertRaises(ValueError):validate_native_bindings(self.e,self.n['fx-translation-ENTITY-UK'],c,c['versioned_dependency_receipts'])
    def test_equal_value_wrong_lineage_profit_receipt_rejected(self):
        c=fixture.translation_source(self.f,'ENTITY-UK')
        r=next(r for r in c['versioned_dependency_receipts'] if r['metric_path'][-1]=='a_fx_gain')
        r['result_version']=self.e.versions.current(self.n['fx-ENTITY-US'].id).version_id
        with self.assertRaises(ValueError):
            self.e.execute(self.n['fx-translation-ENTITY-UK'].id,lambda _:None,c,'Forged equal-value profit lineage')
    def test_altered_native_profit_tb_balance_rejected(self):
        c=fixture.translation_source(self.f,'ENTITY-UK');c['translation']['tb'][3]['balance']='0'
        with self.assertRaises(ValueError):validate_native_bindings(self.e,self.n['fx-translation-ENTITY-UK'],c,c['versioned_dependency_receipts'])
