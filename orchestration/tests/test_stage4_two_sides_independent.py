"""Independent bounded two-side attacks; not full flagship acceptance."""
import copy
import unittest
from orchestration.tests.test_stage4_two_translated_sides import control
from orchestration.tests import stage3_fixtures as s3
from orchestration.governed_plan import observation
from orchestration.stage3 import validate_native_bindings
from additional_cases import certify


class IndependentTwoSides(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = control()

    def setUp(self):
        self.f = copy.deepcopy(self.base)
        self.e = self.f['session']
        self.n = self.f['nodes']['fx-reassessment']
        self.c = copy.deepcopy(self.f['reassessment_source'])

    def validate(self):
        validate_native_bindings(self.e, self.n, self.c, self.c['versioned_dependency_receipts'])

    def test_wrong_native_functional_currency_cannot_qualify_us_legal_side(self):
        # Same amounts, rates, Scope, result lineage: only the claimed native
        # operation currency changes. Equal numbers cannot certify USD as GBP.
        n = self.f['nodes']['fx-translation-ENTITY-US']
        source = copy.deepcopy(self.e.sources[n.id])
        source['translation']['functional_currency'] = 'GBP'
        with self.assertRaises(ValueError):
            self.e.execute(n.id, observation, certify('foreign-currency', source), 'Independent wrong functional currency attack')
            self.c['versioned_dependency_receipts'] = s3.receipts(self.f, self.n.id)
            self.e.execute(self.n.id, observation, certify('intercompany-accounting', self.c), 'Independent currency substitution')

    def test_wrong_economic_identity_rejected(self):
        self.c['conversion_economic_id'] = 'clean'
        with self.assertRaises(ValueError): self.validate()

    def test_wrong_transaction_currency_rejected(self):
        self.c['pairs'][0]['currency'] = 'GBP'
        with self.assertRaises(ValueError): self.validate()

    def test_omitted_receivable_mapping_rejected(self):
        self.c['stage3_input_bindings'].pop(0)
        with self.assertRaises(ValueError): self.validate()

    def test_duplicate_payable_target_rejected(self):
        self.c['stage3_input_bindings'].append(copy.deepcopy(self.c['stage3_input_bindings'][1]))
        with self.assertRaises(ValueError): self.validate()

    def test_native_payable_carrying_plug_rejected(self):
        self.c['pairs'][0]['gl_b'] = '16'
        with self.assertRaises(ValueError): self.validate()

    def test_other_economic_transaction_id_rejected(self):
        self.c['pairs'][0]['transaction_id'] = 'clean'
        with self.assertRaises(ValueError): self.validate()

    def test_services_are_not_generic_conversion_rejected(self):
        self.c['pairs'][0]['recharge'] = '1'
        with self.assertRaises(ValueError): self.validate()

    def test_reviewed_source_mutation_invalidates_translation_qualification(self):
        n = self.f['nodes']['fx-translation-ENTITY-US']
        self.e.sources[n.id]['translation']['tb'][1]['category'] = 'asset'
        with self.assertRaises(ValueError): self.validate()

    def test_payable_receipt_metric_substitution_rejected(self):
        target = self.e.execute(self.n.id, observation, self.c, 'Independent bounded control')
        source = self.e.versions.current(self.f['nodes']['fx-translation-ENTITY-US'].id)
        record = self.f['basis'].intercompany_conversion(source.version_id, target.version_id, 'fx', ('calculations','translation','translated_tb','fx payable'), s3.EVIDENCE)
        record['source_metric'][-1] = 'cash'
        with self.assertRaises(ValueError): self.f['basis'].validate_transformation(record)

    def test_clean_bounded_control_preserves_unequal_eur_and_history(self):
        target = self.e.execute(self.n.id, observation, self.c, 'Independent bounded control')
        result = target.payload()
        pair = result['calculations']['pairs'][0]
        self.assertEqual((pair['a_functional'],pair['b_functional']), ('16.00','18.00'))
        self.assertEqual(result['journal_entry_implications'], [])
        self.assertEqual(self.f['historical_fx']['matching']['classification'], 'FX_DIFFERENCE')

    def test_framework_receipt_native_side_substitution_rejected(self):
        target = self.e.execute(self.n.id, observation, self.c, 'Independent bounded control')
        source = self.e.versions.current(self.f['nodes']['fx-translation-ENTITY-US'].id)
        record = self.f['basis'].intercompany_conversion(source.version_id, target.version_id, 'fx', ('calculations','translation','translated_tb','fx payable'), s3.EVIDENCE)
        record['native_side'] = 'gl_a'
        with self.assertRaises(ValueError): self.f['basis'].validate_transformation(record)

    def test_superseded_legal_side_invalidates_translation_and_reassessment(self):
        target = self.e.execute(self.n.id, observation, self.c, 'Independent bounded control')
        source = self.e.versions.current(self.f['nodes']['fx-translation-ENTITY-US'].id)
        record = self.f['basis'].intercompany_conversion(source.version_id, target.version_id, 'fx', ('calculations','translation','translated_tb','fx payable'), s3.EVIDENCE)
        n = self.f['nodes']['fx-ENTITY-US']
        legal = copy.deepcopy(self.e.sources[n.id])
        legal['independent_review_note'] = 'Fresh separately reviewed equal-value source'
        self.e.execute(n.id, observation, certify('intercompany-accounting', legal), 'Independent exact-version replacement')
        with self.assertRaises(ValueError): self.f['basis'].validate_transformation(record)
