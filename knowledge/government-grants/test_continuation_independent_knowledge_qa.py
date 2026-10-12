"""Fresh continuation review: governed retrieval attacks, not implementation certification."""
import copy
import importlib.util
import json
from collections import Counter
from pathlib import Path
import unittest
HERE = Path(__file__).resolve().parent

def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
r = load('continuation_grant_retrieval', 'retrieval.py')
v = load('continuation_grant_validator', 'validate_supplement.py')

class ContinuationIndependentKnowledgeQA(unittest.TestCase):
    def setUp(self):
        self.data = r.load_register()
    def retrieve(self, framework='IFRS', **changes):
        args = dict(period_start='2026-01-01', grant_model=sorted(r.MODELS[framework])[0])
        args.update(changes)
        return r.retrieve(framework, '2026-09-30', r.SCOPES[framework], **args)
    def test_fresh_review_binds_every_preserved_claim(self):
        review = json.loads((HERE / 'continuation-independent-knowledge-review.json').read_text())
        rows = {c['claim_id']: c for c in review['claim_reviews']}
        self.assertEqual(len(rows), 172)
        for claim in self.data['claims']:
            with self.subTest(claim=claim['claim_id']):
                self.assertEqual(rows[claim['claim_id']]['reviewed_hash'], v.claim_hash(claim))
                self.assertEqual(rows[claim['claim_id']]['evidence_status_preserved'], claim['evidence_status'])
    def test_assurance_is_not_bulk_promoted(self):
        self.assertEqual(Counter(c['evidence_status'] for c in self.data['claims']), {'SOURCE_VERIFIED':47, 'PRIMARY_CORROBORATED':29, 'MODEL_DERIVED_AUDIT_REQUIRED':96})
        for c in self.data['claims']:
            if c['evidence_status'] != 'SOURCE_VERIFIED':
                self.assertTrue(c['audit_required'])
    def test_unreviewed_windows_fail_for_all_models(self):
        for fw in ('IFRS','AASB','UK_GAAP'):
            for model in r.MODELS[fw]:
                for start in ('2025-12-31', '2027-01-01', '2026-10-01'):
                    with self.subTest(fw=fw, model=model, start=start), self.assertRaises(ValueError):
                        self.retrieve(fw, grant_model=model, period_start=start)
    def test_model_and_scope_do_not_follow_labels(self):
        for fw in r.FRAMEWORKS:
            with self.subTest(fw=fw), self.assertRaises(ValueError):
                r.retrieve(fw, '2026-09-30', 'nonprofit', period_start='2026-01-01', grant_model=sorted(r.MODELS[fw])[0])
    def test_us_adoption_does_not_follow_receipt(self):
        adoption=dict(standard='ASU2025-10',annual_period_start='2026-01-01',financial_statements_unissued_at_adoption=True,transition_reviewed=True,evidence_id='qa-reviewed-transition',adoption_date='2026-10-01')
        self.assertEqual(len(self.retrieve('US_GAAP',us_adoption=adoption,execution_date='2026-10-12')),45)
        for key,value in [('financial_statements_unissued_at_adoption',False),('transition_reviewed',False),('evidence_id',''),('annual_period_start','2025-01-01'),('adoption_date','2026-10-13')]:
            changed=dict(adoption);changed[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):
                self.retrieve('US_GAAP',us_adoption=changed,execution_date='2026-10-12')
    def test_disclosure_only_nonadopter_cannot_import_ias20(self):
        for model in ('ASC832_DISCLOSURE_ONLY','IAS20_ACCRUAL','ASC958_ANALOGY'):
            with self.subTest(model=model),self.assertRaises(ValueError):
                self.retrieve('US_GAAP',grant_model=model)
    def test_unselected_mutated_claim_still_invalidates_register(self):
        for key,value in [('entity_scope','aasb_tier2'),('effective_period','future'),('proposition','Cash receipt guarantees compliance')]:
            data=copy.deepcopy(self.data)
            claim=next(c for c in data['claims'] if c['framework']=='AASB')
            claim[key]=value
            with self.subTest(key=key): self.assertTrue(v.validate_data(data))
    def test_unknown_decision_cannot_silently_reduce_support(self):
        with self.assertRaises(ValueError): self.retrieve(decisions=['recognition','invented_analogy'])

if __name__ == '__main__': unittest.main()
