"""Independent claim governance and fresh accounting counterexamples; reviewer-owned."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
HERE=Path(__file__).resolve().parent

def module(name, filename):
    spec=importlib.util.spec_from_file_location(name,HERE/filename)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
v=module('insurance_independent_validator','validate_supplement.py')
r=module('insurance_independent_retrieval','retrieval.py')

class IndependentInsuranceClaimQA(unittest.TestCase):
    def setUp(self):
        self.data=r.load_register()
        self.cs={(c['framework'],c['decision']):c for c in self.data['claims']}

    def reject(self,data,fw='IFRS',**kw):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'claims.json';path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                r.retrieve(fw,'2026-12-31',r.SCOPES[fw],path=path,insurance_model=sorted(r.MODELS[fw])[0],**kw)

    def test_every_claim_has_independent_specific_challenge(self):
        report=json.loads((HERE/'independent-review.json').read_text())
        ledger={x['claim_id']:x for x in report['claim_reviews']}
        self.assertEqual(len(ledger),168)
        for c in self.data['claims']:
            with self.subTest(claim=c['claim_id']):
                item=ledger[c['claim_id']]
                self.assertEqual(item['reviewed_hash'],v.claim_hash(c))
                self.assertEqual(item['result'],'PASS')
                self.assertGreater(len(item['challenge']),45)
                self.assertNotEqual(c['approval_review']['reviewer'],self.data['author'])
        self.assertEqual(v.validate_data(self.data),[])

    def test_each_changed_claim_invalidates_approval(self):
        for index,c in enumerate(self.data['claims']):
            with self.subTest(claim=c['claim_id']):
                changed=copy.deepcopy(self.data)
                changed['claims'][index]['proposition']+=' Unsupported override.'
                self.assertTrue(v.validate_data(changed))

    def test_missing_duplicate_and_unselected_claim_fail_closed(self):
        for fw in r.FRAMEWORKS:
            d=copy.deepcopy(self.data)
            d['claims'].pop(next(i for i,c in enumerate(d['claims']) if c['framework']==fw))
            self.reject(d,decisions=['definition'])
        d=copy.deepcopy(self.data);d['claims'].append(copy.deepcopy(d['claims'][0]));self.reject(d)
        d=copy.deepcopy(self.data);d['claims'][-1]['approval_review']['reviewer']=d['author']
        self.reject(d,decisions=['definition'])

    def test_all_four_routes_and_privacy(self):
        for fw in r.FRAMEWORKS:
            rows=r.retrieve(fw,'2026-12-31',r.SCOPES[fw],insurance_model=sorted(r.MODELS[fw])[0])
            self.assertEqual(len(rows),{'IFRS':65,'AASB':65,'US_GAAP':24,'UK_GAAP':14}[fw])
            for row in rows:self.assertEqual(set(row),set(r.PUBLIC_FIELDS))
            public=json.dumps(rows).lower()
            for forbidden in ('source_note','source_verified','approval_review','audit_required','chatgpt training','reference_confidence','training_data_checked'):
                self.assertNotIn(forbidden,public)
            self.assertIn('qualified',public)

    def test_period_scope_and_framework_transplant(self):
        for fw in r.FRAMEWORKS:
            for start,end in [('2025-12-31','2026-12-31'),('2026-01-01','2027-01-01'),('2026-12-31','2026-01-01')]:
                with self.assertRaises(ValueError):r.retrieve(fw,end,r.SCOPES[fw],period_start=start,insurance_model=sorted(r.MODELS[fw])[0])
            with self.assertRaises(ValueError):r.retrieve(fw,'2026-12-31','public_sector',insurance_model=sorted(r.MODELS[fw])[0])
            with self.assertRaises(ValueError):r.retrieve(fw,'2026-12-31',r.SCOPES[fw],insurance_model='IFRS17_VFA')
            with self.assertRaises(ValueError):r.retrieve(fw,'2026-12-31',r.SCOPES[fw],insurance_model=sorted(r.MODELS[fw])[0],early_presentation_adoption=True)
        with self.assertRaises(ValueError):r.retrieve('US_GAAP','2026-12-31',r.SCOPES['US_GAAP'],insurance_model='IFRS17_PAA')
        with self.assertRaises(ValueError):r.retrieve('UK_GAAP','2026-12-31',r.SCOPES['UK_GAAP'],insurance_model='IFRS17_GMM')

    def test_evidence_inflation_fabrication_and_canonical_masquerade(self):
        for key,value in [('evidence_status','SOURCE_VERIFIED'),('audit_required',False),('paragraph_references',['IFRS17.999']),('topic_id','TOPIC-17-999')]:
            d=copy.deepcopy(self.data);d['claims'][0][key]=value;self.reject(d)
        d=copy.deepcopy(self.data);d['claims'][0]['sources'][0]['locator']='17.999';self.reject(d)
        d=copy.deepcopy(self.data);d['claims'][0]['public_limitations'].append('Source: ChatGPT training data');self.reject(d)

    def test_aasb_both_compilations_and_entity_boundary(self):
        for c in self.data['claims']:
            if c['framework']=='AASB':
                self.assertEqual(c['entity_scope'],'aasb_tier1_for_profit')
                self.assertIn('exclude public-sector', ' '.join(c['limitations']))
            if c['framework']=='AASB' and c['evidence_status']=='SOURCE_VERIFIED':
                urls={s['url'] for s in c['sources']}
                self.assertIn('https://standards.aasb.gov.au/aasb-17-dec-2022',urls)
                self.assertIn('https://standards.aasb.gov.au/aasb-17-dec-2022-0',urls)
        for start in ('2026-01-01','2026-06-30','2026-07-01'):
            self.assertEqual(len(r.retrieve('AASB','2026-12-31',r.SCOPES['AASB'],period_start=start,insurance_model='AASB17_PAA')),65)

    def test_direct_source_windows_and_notes_rejected(self):
        ix=next(i for i,c in enumerate(self.data['claims']) if c['framework']=='AASB' and c['evidence_status']=='SOURCE_VERIFIED')
        for kind in ('remove_prejuly','wrong_window','source_note','claim_kind'):
            d=copy.deepcopy(self.data)
            if kind=='remove_prejuly':
                d['claims'][ix]['sources']=[s for s in d['claims'][ix]['sources'] if s['url'].endswith('-0')]
            elif kind=='wrong_window':d['claims'][ix]['sources'][0]['operative_period_start']='future2027'
            elif kind=='source_note':d['claims'][ix]['public_limitations'].append('Source: Private actuary')
            else:d['claims'][ix]['claim_kind']='FICTION'
            self.reject(d,'AASB')

    def test_scope_election_and_component_counterexamples(self):
        for fw in ('IFRS','AASB'):
            get=lambda d:self.cs[(fw,d)]['proposition'].lower()
            for term in ('prior explicit','use of insurance','irrevocable','otherwise route'):
                self.assertIn(term,get('financial_guarantee'))
            for term in ('individual customer risk','services rather than cash','service use rather than cost','irrevocable'):
                self.assertIn(term,get('fixed_fee'))
            self.assertIn('discretionary participation',get('investment_component'))
            self.assertIn('excluded',get('investment_component'))
            self.assertIn('significant',get('significant_risk'))
            self.assertIn('financial risk alone',get('significant_risk'))

    def test_group_reinsurance_and_paa_challenges(self):
        for fw in ('IFRS','AASB'):
            get=lambda d:self.cs[(fw,d)]['proposition'].lower()
            self.assertIn('do not subsequently',get('group_lock'))
            self.assertIn('more than one year',get('annual_cohort'))
            for t in ('net-gain-at-inception','no-significant-possibility','remaining','annual cohorts'):
                self.assertIn(t,get('reinsurance_group'))
            for t in ('earlier','onerous','proportionate','underlying'):
                self.assertIn(t,get('reinsurance_recognition'))
            self.assertIn('each contract',get('paa_eligibility'))
            self.assertIn('at inception',get('paa_eligibility'))
            self.assertIn('each service portion',get('paa_financing'))
            self.assertIn('claim incurrence',get('paa_claims'))
            self.assertIn('eligibility does not waive',get('paa_onerous'))
            self.assertIn('do not offset',get('reinsurance_presentation'))

    def test_paa_acquisition_signed_bridge_numeric_regression(self):
        # KQ4: paid cost reduces LRC, amortisation adds it. Deducting both yields wrong60.
        remaining=100-12+3-25
        self.assertEqual(remaining,66)
        self.assertNotEqual(remaining,100-12-3-25)
        for fw in ('IFRS','AASB'):
            p=self.cs[(fw,'paa_remaining')]['proposition'].lower()
            self.assertIn('adds premiums, acquisition amortisation',p)
            self.assertIn('deducts qualifying acquisition cash flows',p)

    def test_csm_locked_interest_and_service_release(self):
        # Future-service unfavorable20 reduces CSM; locked interest3%; units2/(2+4).
        pre_release=120+120*.03-20
        release=pre_release*2/6
        self.assertAlmostEqual(release,34.53333333333333)
        self.assertNotEqual(release,(120+120*.06-20)*2/6)
        self.assertAlmostEqual(pre_release-release,69.06666666666666)
        for fw in ('IFRS','AASB'):
            self.assertIn('initial recognition',self.cs[(fw,'csm_interest')]['proposition'])
            self.assertIn('current plus expected remaining',self.cs[(fw,'coverage_units')]['proposition'])
            self.assertIn('past/current',self.cs[(fw,'future_service')]['proposition'])
            self.assertIn('net outflow',self.cs[(fw,'csm_initial')]['proposition'])

    def test_native_us_and_uk_numeric_deficiency(self):
        # US40 deficiency reduces DAC30, adds10 liability. UK test uses net110 vs130=20.
        us_loss=190+20+30-200
        self.assertEqual((us_loss,min(us_loss,30),max(us_loss-30,0)),(40,30,10))
        self.assertEqual(max(130-(150-30-10),0),20)
        self.assertIn('LESS related DAC',self.cs[('UK_GAAP','adequacy')]['proposition'])
        self.assertIn('without deducting DAC again',self.cs[('UK_GAAP','adequacy')]['proposition'])
        self.assertIn('2015',self.cs[('UK_GAAP','period')]['proposition'])
        self.assertIn('January2024',self.cs[('UK_GAAP','period')]['proposition'])
        self.assertIn('not aligned',self.cs[('UK_GAAP','ifrs_boundary')]['proposition'])
        self.assertIn('existing policy',self.cs[('UK_GAAP','production_boundary')]['proposition'])
        self.assertIn('first through reduction',self.cs[('US_GAAP','deficiency_allocation')]['proposition'])
        self.assertIn('do not govern',self.cs[('US_GAAP','classification')]['proposition'])

    def test_qualified_actuarial_and_owner_boundaries(self):
        for fw in r.FRAMEWORKS:
            self.assertIn('qualified',' '.join(self.cs[(fw,'actuarial_boundary')]['public_limitations']).lower())
            self.assertTrue(self.cs[(fw,'actuarial_boundary')]['audit_required'])
        for fw in ('IFRS','AASB'):
            for t in ('model version','assumption register','valuation date','qualified signoff'):
                self.assertIn(t,self.cs[(fw,'actuarial_boundary')]['proposition'])
            self.assertIn('without ERP posting',self.cs[(fw,'owner_boundaries')]['proposition'])
            self.assertIn('never generates',self.cs[(fw,'actuarial_boundary')]['proposition'])

if __name__=='__main__':unittest.main()
