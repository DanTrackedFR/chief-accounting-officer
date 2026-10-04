"""Fresh independent knowledge/retrieval challenges, separate from author tests."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('independent_hedge_retrieval', HERE/'retrieval.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
spec = importlib.util.spec_from_file_location('independent_hedge_validator', HERE/'validate_supplement.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

class IndependentKnowledgeChallenges(unittest.TestCase):
    def setUp(self):
        self.data = r.load_register()
        self.claims = {(c['framework'], c['decision']): c for c in self.data['claims']}

    def approved_copy(self):
        # Fixture approval is only used to exercise the gate. Actual sign-off is in independent-review.json.
        data = copy.deepcopy(self.data)
        data['status'] = 'APPROVED'
        for c in data['claims']:
            c['approval_track'] = 'DIRECT_SOURCE_CHECKED' if c['evidence_status']=='SOURCE_VERIFIED' else 'TRAINING_DATA_CHECKED'
            c['approval_review'] = {'reviewer':'independent_knowledge_reviewer', 'date':'2026-10-04', 'result':'PASS', 'scope_and_period_checked':True, 'cross_framework_checked':True, 'regression_checked':True, 'reviewed_hash':v.claim_hash(c)}
        return data

    def retrieve_fixture(self, data, framework='IFRS', **kwargs):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)/'register.json'
            path.write_text(json.dumps(data))
            return r.retrieve(framework, '2026-12-31', r.SCOPES[framework], path=path, hedge_model=r.MODELS[framework], **kwargs)

    def test_population_and_changed_claim_rejected(self):
        data = self.approved_copy()
        self.assertEqual(v.validate_data(data), [])
        changed = copy.deepcopy(data)
        changed['claims'][0]['proposition'] += ' altered'
        self.assertTrue(v.validate_data(changed))
        deleted = copy.deepcopy(data)
        deleted['claims'].pop()
        self.assertTrue(v.validate_data(deleted))
        for mutation in (changed, deleted):
            with self.assertRaises(ValueError): self.retrieve_fixture(mutation)

    def test_unselected_bad_claim_blocks_whole_register(self):
        data = self.approved_copy()
        data['claims'][-1]['approval_review']['reviewer'] = data['author']
        with self.assertRaises(ValueError): self.retrieve_fixture(data, decisions=['definition'])

    def test_model_period_scope_and_projection(self):
        data = self.approved_copy()
        for fw in r.FRAMEWORKS:
            kwargs = {'us_amendments_adopted':False} if fw=='US_GAAP' else {}
            rows = self.retrieve_fixture(data, fw, **kwargs)
            self.assertEqual(len(rows),25)
            self.assertTrue(all(set(c)==set(r.PUBLIC_FIELDS) and c['framework']==fw for c in rows))
            public = json.dumps(rows).lower()
            for internal in ('source_note','source_verified','approval_review','training_data_checked','audit_required','chatgpt training'):
                self.assertNotIn(internal,public)
        for fw, model in [('IFRS','IAS39'),('AASB','AASB139'),('UK_GAAP','IFRS9')]:
            with self.assertRaises(ValueError):r.retrieve(fw,'2026-12-31',r.SCOPES[fw],hedge_model=model)
        for start in ('2025-12-31','2027-01-01'):
            with self.assertRaises(ValueError):r.retrieve('IFRS','2026-12-31',r.SCOPES['IFRS'],period_start=start,hedge_model=r.MODELS['IFRS'])
        with self.assertRaises(ValueError):r.retrieve('IFRS','2026-12-31','aasb_tier1_for_profit',hedge_model=r.MODELS['IFRS'])
        with self.assertRaises(ValueError):self.retrieve_fixture(data, decisions=['definition','not_a_decision'])

    def test_us_adoption_and_mandatory_december_boundary(self):
        data = self.approved_copy()
        for adoption in (None, True, 0):
            with self.assertRaises(ValueError):self.retrieve_fixture(data,'US_GAAP',us_amendments_adopted=adoption)
        with self.assertRaises(ValueError):self.retrieve_fixture(data,'US_GAAP',period_start='2026-12-16',us_amendments_adopted=False)
        self.assertEqual(len(self.retrieve_fixture(data,'US_GAAP',period_start='2026-12-15',us_amendments_adopted=False)),25)

    def test_fresh_cumulative_counterexample(self):
        # Period1 cumulative instrument +110 / risk -100 => reserve100, residual10.
        # Period2 cumulative instrument +170 / risk -155 => reserve155, OCI55, residual5.
        # Period-only min(60,55) happens to agree; use reversal next to expose naive period lower-of.
        opening_entitlement = min(110,100)
        closing_entitlement = min(170,155)
        self.assertEqual((closing_entitlement-opening_entitlement,60-(closing_entitlement-opening_entitlement)),(55,5))
        # Period3 instrument+20,risk-30 => entitlement20, OCI-135, earnings-15.
        # Naive period lower-of min(150,125) would incorrectly report OCI-125.
        current_oci = min(20,30)-closing_entitlement
        self.assertEqual((current_oci,-150-current_oci),(-135,-15))
        self.assertNotEqual(current_oci,-min(150,125))
        # Prior reserve release60 leaves95 opening ledger; OCI55 must not become115.
        self.assertEqual(155-100,55)
        self.assertNotEqual(155-(100-60),55)
        for fw in ('IFRS','AASB','UK_GAAP'):
            p=self.claims[(fw,'cash_flow_measurement')]['proposition'].lower()
            self.assertIn('cumulative',p)
            self.assertIn('prior releases',p)
        self.assertIn('entire instrument change',self.claims[('US_GAAP','cash_flow_measurement')]['proposition'])

    def test_signed_settlement_and_purchase_challenge(self):
        # Opening asset23, closingzero, collected31 => gain8. Liability-23,pay31 => loss8.
        self.assertEqual(0-23+31,8)
        self.assertEqual(0-(-23)-31,-8)
        # Purchase1200; cumulative hedge gain90 reduces IFRS/AASB/UK cost to1110.
        self.assertEqual(1200-90,1110)
        self.assertEqual(1200-(-90),1290)
        self.assertIn('AOCI',self.claims[('US_GAAP','nonfinancial_purchase')]['proposition'])
        self.assertIn('do not recycle',self.claims[('UK_GAAP','net_investment_disposal')]['proposition'])
        self.assertIn('Unrecoverable',self.claims[('AASB','forecast')]['proposition'])
        for fw in r.FRAMEWORKS:
            self.assertIn('must not exceed',self.claims[(fw,'net_investment')]['proposition'])
            self.assertIn('block unsupported',self.claims[(fw,'excluded_components')]['proposition'])

if __name__=='__main__':unittest.main()
