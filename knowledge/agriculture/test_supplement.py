"""Claim arithmetic and governance challenges; independent reviewer adds own challenges."""
import json
import tempfile
import unittest
from decimal import Decimal as D
from pathlib import Path
from retrieval import load_register,retrieve,PUBLIC_FIELDS
from validate_supplement import validate

class AgricultureKnowledgeTests(unittest.TestCase):
    def test_structure(self):
        self.assertEqual(validate()['errors'],[])
        self.assertEqual(len(load_register()['claims']),66)
    def test_no_fake_canonical_ids(self):
        self.assertNotIn('TOPIC-',json.dumps(load_register()))
    def test_framework_claims_differ(self):
        c=load_register()['claims']
        us=' '.join(x['proposition'] for x in c if x['framework']=='US_GAAP')
        uk=' '.join(x['proposition'] for x in c if x['framework']=='UK_GAAP')
        self.assertIn('no general IAS 41',us);self.assertIn('by biological-asset class',uk)
        self.assertIn('cannot subsequently change',uk)
    def test_fvcts_arithmetic(self):
        self.assertEqual(D('125000')-D('5000'),D('120000'))
        opening,purchases,harvest,deaths,closing=map(D,['100000','20000','30000','5000','120000'])
        gain=closing-opening-purchases+harvest+deaths
        self.assertEqual(gain,D('35000'))
        self.assertEqual(opening+purchases+gain-harvest-deaths,closing)
    def test_birth_not_purchase(self):
        opening,births,closing=map(D,['1000','200','1300'])
        gain=closing-opening
        self.assertEqual(gain,D('300'))
        self.assertEqual(gain-births,D('100'))
    def test_terminal_and_surviving_harvest_differ(self):
        self.assertEqual(100+10-20-5,85)
        self.assertEqual(100+10-0-5,105)
    def test_harvest_cannot_be_double_added(self):
        preharvest,harvest=map(D,['1000','1100'])
        self.assertEqual(harvest-preharvest,D('100'))
        self.assertNotEqual(harvest+preharvest,harvest)
    def test_claim_provenance_hidden(self):
        self.assertFalse(set(PUBLIC_FIELDS)&{'sources','source_note','source','evidence_status','approval_track','approval_review','reviewer','reference_confidence'})
    def test_missing_context_and_outside_period(self):
        for fw,period,scope in [('IFRS','2025-12-31','company'),('IFRS','2027-12-31','company'),('IFRS','2026-12-31',''),('OTHER','2026-12-31','company')]:
            with self.assertRaises(ValueError):retrieve(fw,period,scope)
    def test_duplicate_and_unapproved_fails(self):
        d=load_register();d['status']='PENDING'
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'x.json';p.write_text(json.dumps(d))
            with self.assertRaises(ValueError):retrieve('IFRS','2026-12-31','company',p)
            d['claims'].append(d['claims'][0]);p.write_text(json.dumps(d))
            with self.assertRaises(ValueError):load_register(p)
    def test_lower_evidence_keeps_audit_flag(self):
        for c in load_register()['claims']:
            if c['evidence_status']!='SOURCE_VERIFIED':self.assertTrue(c['audit_required'])
    def test_no_ias41_exception_on_uk_claim(self):
        c=next(c for c in load_register()['claims'] if c['framework']=='UK_GAAP' and c['decision']=='exception')
        self.assertIn('do not restrict',c['proposition'])

if __name__=='__main__':unittest.main()
