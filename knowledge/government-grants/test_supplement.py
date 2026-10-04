"""Authored Government Grants claim governance tests; independent semantic QA is separate."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent

def module(name):
    s=importlib.util.spec_from_file_location('grant_authored_'+name,HERE/(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
v=module('validate_supplement');r=module('retrieval')

class GrantSupplementTests(unittest.TestCase):
    def setUp(self):self.d=r.load_register()
    def test_current_population_structure(self):self.assertEqual(v.validate_data(self.d),[]);self.assertEqual(len(self.d['claims']),172)
    def test_framework_counts(self):self.assertEqual({f:sum(c['framework']==f for c in self.d['claims']) for f in r.FRAMEWORKS},{'IFRS':47,'AASB':48,'UK_GAAP':32,'US_GAAP':45})
    def test_author_has_no_approval(self):
        if self.d['status']=='REVIEWED':self.assertTrue(all(c['approval_track']=='PENDING' and c['approval_review'] is None for c in self.d['claims']))
        else:self.assertTrue(all(c['approval_review']['reviewer']!=self.d['author'] for c in self.d['claims']))
    def test_all_expected_decisions_exact(self):
        for fw,expected in v.EXPECTED_DECISIONS.items():self.assertEqual(set(expected),{c['decision'] for c in self.d['claims'] if c['framework']==fw})
    def test_us_asu_not_live_asc_verified(self):self.assertTrue(all(c['evidence_status']=='PRIMARY_CORROBORATED' and c['audit_required'] for c in self.d['claims'] if c['framework']=='US_GAAP' and c['claim_kind']=='NORMATIVE'))
    def test_ifrs_no_invented_locator(self):self.assertTrue(all(not s['locator'] for c in self.d['claims'] if c['framework']=='IFRS' for s in c['sources']))
    def test_hash_binds_material_content(self):
        c=self.d['claims'][0];x=copy.deepcopy(c);x['proposition']+=' changed';self.assertNotEqual(v.claim_hash(c),v.claim_hash(x));x=copy.deepcopy(c);x['approval_track']='PENDING';self.assertEqual(v.claim_hash(c),v.claim_hash(x))
    def test_mutated_metadata_rejected(self):
        mutations=[('namespace','FAKE'),('status','production')]
        for k,val in mutations:
            d=copy.deepcopy(self.d);d[k]=val;self.assertTrue(v.validate_data(d))
    def test_claim_structure_mutations(self):
        for k,val in [('framework','OTHER'),('entity_scope','nfp'),('evidence_status','VERIFIED'),('reference_confidence','maybe'),('audit_required',None),('tests',[]),('limitations',[]),('period_scope',{}),('effective_period','all years'),('proposition','')]:
            with self.subTest(k=k):
                d=copy.deepcopy(self.d);d['claims'][0][k]=val;self.assertTrue(v.validate_data(d))
    def test_duplicate_identity_rejected(self):d=copy.deepcopy(self.d);d['claims'][1]['claim_id']=d['claims'][0]['claim_id'];self.assertTrue(v.validate_data(d))
    def test_canonical_masquerade_rejected(self):
        d=copy.deepcopy(self.d);d['claims'][0]['topic_id']='TOPIC-99-999';self.assertTrue(v.validate_data(d))
    def test_asu_source_inflation_rejected(self):
        d=copy.deepcopy(self.d);c=next(c for c in d['claims'] if c['framework']=='US_GAAP' and c['claim_kind']=='NORMATIVE');c.update(evidence_status='SOURCE_VERIFIED',audit_required=False,reference_confidence='VERIFIED');self.assertTrue(v.validate_data(d))
    def test_source_structure_mutations(self):
        for key,value in [('url','file:///fake'),('locator',True),('access_date','tomorrow'),('inspected','yes')]:
            d=copy.deepcopy(self.d);c=next(c for c in d['claims'] if c['framework']=='AASB' and c['claim_kind']=='NORMATIVE');c['sources'][0][key]=value;self.assertTrue(v.validate_data(d))
    def test_public_injection_rejected(self):
        for label in ['Source: FASB','Source: ChatGPT training data','MODEL_DERIVED_AUDIT_REQUIRED','PRIMARY_CORROBORATED','DIRECT_SOURCE_CHECKED','source_note']:
            d=copy.deepcopy(self.d);d['claims'][0]['public_limitations'].append(label);self.assertTrue(v.validate_data(d))
    def test_retrieval_scope_and_model_reject(self):
        for fw,scope,model in [('IFRS','nfp','IAS20_ACCRUAL'),('UK_GAAP',r.SCOPES['UK_GAAP'],'IAS20_ACCRUAL'),('AASB',r.SCOPES['AASB'],'IAS20_ACCRUAL'),('US_GAAP',r.SCOPES['US_GAAP'],'ASC832_ASU2025_10_ADOPTED')]:
            with self.assertRaises(ValueError):r.retrieve(fw,'2026-12-31',scope,period_start='2026-01-01',grant_model=model)
    def test_retrieval_bad_periods(self):
        for start,end in [('2025-01-01','2026-01-01'),('2026-01-01','2027-01-01'),('2026-09-01','2026-01-01'),(None,'2026-12-31')]:
            with self.assertRaises(ValueError):r.retrieve('IFRS',end,r.SCOPES['IFRS'],period_start=start,grant_model='IAS20_ACCRUAL')
    def test_pending_never_retrieved(self):
        if self.d['status']=='REVIEWED':
            with self.assertRaises(ValueError):r.retrieve('IFRS','2026-12-31',r.SCOPES['IFRS'],period_start='2026-01-01',grant_model='IAS20_ACCRUAL')
    def test_approved_public_allowlist(self):
        if self.d['status']=='APPROVED':
            cs=r.retrieve('IFRS','2026-12-31',r.SCOPES['IFRS'],period_start='2026-01-01',grant_model='IAS20_ACCRUAL');self.assertTrue(cs);self.assertTrue(all(set(c)==set(r.PUBLIC_FIELDS) for c in cs));self.assertNotIn('source_note',json.dumps(cs))
    def test_us_postperiod_adoption_before_issuance(self):
        if self.d['status']=='APPROVED':
            adoption={'standard':'ASU2025-10','annual_period_start':'2026-01-01','financial_statements_unissued_at_adoption':True,'transition_reviewed':True,'evidence_id':'ADOPTION-QUALIFIED','adoption_date':'2026-08-01'}
            cs=r.retrieve('US_GAAP','2026-06-30',r.SCOPES['US_GAAP'],period_start='2026-01-01',grant_model='ASC832_ASU2025_10_ADOPTED',us_adoption=adoption,execution_date='2026-10-04');self.assertEqual(len(cs),45)
            for execution in [None,'2026-05-01','2026-07-01']:
                with self.assertRaises(ValueError):r.retrieve('US_GAAP','2026-06-30',r.SCOPES['US_GAAP'],period_start='2026-01-01',grant_model='ASC832_ASU2025_10_ADOPTED',us_adoption=adoption,execution_date=execution)
            adoption['adoption_date']='2027-01-01'
            with self.assertRaises(ValueError):r.retrieve('US_GAAP','2026-06-30',r.SCOPES['US_GAAP'],period_start='2026-01-01',grant_model='ASC832_ASU2025_10_ADOPTED',us_adoption=adoption,execution_date='2026-10-04')
    def test_malformed_register_safe(self):
        for d in [None,{},[],{'namespace':'SUPPLEMENTAL_GOVERNMENT_GRANTS','claims':[None]}]:self.assertTrue(v.validate_data(d))

if __name__=='__main__':unittest.main()
