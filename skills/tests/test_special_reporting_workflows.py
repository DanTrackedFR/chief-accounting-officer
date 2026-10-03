"""Bounded batch safety, archived examples and certification regression."""
import copy,json,unittest
from pathlib import Path
from unittest.mock import patch
from special_reporting_cases import *
from production import assess_case,to_public,case_fingerprint,ROOT
from interfaces.public_output import ROUTES

class SpecialReportingTests(unittest.TestCase):
    def test_framework_routes_and_no_posting(self):
        supported={PACKAGES[0]:{'IFRS','AASB'},PACKAGES[1]:{'IFRS','AASB'},PACKAGES[2]:set(FRAMEWORKS),PACKAGES[3]:{'IFRS','US_GAAP'}}
        for p in PACKAGES+BLOCKED:
            for fw in FRAMEWORKS:
                with self.subTest(package=p,framework=fw):
                    r=assess_case(p,ready(p,fw) if p not in BLOCKED else case(p,fw))
                    self.assertEqual(r['status'],'complete' if fw in supported.get(p,set()) else 'blocked')
                    self.assertEqual(r['journal_entry_implications'],[])
                    if r['status']=='blocked':self.assertEqual(r['calculations'],{})
    def test_certification_is_case_exact(self):
        for p in PACKAGES:
            c=ready(p);c['assumptions'].append('Fresh material assumption')
            self.assertEqual(assess_case(p,c)['status'],'partial')
            c.pop('reviewer_signoff');self.assertEqual(assess_case(p,c)['status'],'partial')
    def test_old_implementation_certificates_rejected(self):
        original=Path.read_bytes
        for p in PACKAGES:
            c=ready(p)
            def changed(path):
                b=original(path)
                return b+b'\n# changed implementation' if path.name=='special_reporting.py' else b
            with patch.object(Path,'read_bytes',changed):
                self.assertEqual(assess_case(p,c)['status'],'partial')
    def test_knowledge_changes_block_all_candidates(self):
        original=Path.read_bytes
        for p in PACKAGES:
            c=ready(p)
            def changed(path):
                b=original(path)
                return b+b'\nchanged knowledge' if 'knowledge/topics/' in str(path) else b
            with patch.object(Path,'read_bytes',changed):self.assertEqual(assess_case(p,c)['status'],'blocked')
    def test_malformed_populations_fail_closed(self):
        keys=dict(zip(PACKAGES,['assets','items','adjustments','filing_lines']))
        for p in PACKAGES:
            for value in [None,{},'not rows',[None],[{}]]:
                c=case(p);c[keys[p]]=value
                with self.subTest(package=p,value=value):self.assertEqual(assess_case(p,ready(p,c=c))['status'],'blocked')
    def test_missing_owner_stale_and_cross_entity_imports(self):
        for p in PACKAGES:
            for imp in [dict(package='financial-statements',case={},result={}),dict(package='investment-property',case={},result={})]:
                c=case(p);c['imports']=[imp]
                self.assertEqual(assess_case(p,ready(p,c=c))['status'],'blocked')
    def test_forbidden_actions(self):
        for p in PACKAGES:
            for action in ['post','file','certify_compliance','full_measurement']:
                c=case(p);c['requested_action']=action
                self.assertEqual(assess_case(p,ready(p,c=c))['status'],'blocked')
    def test_sec_actual_apm_owner_exact_once(self):
        from production import load_workflow
        owner=ready('alternative-performance-measures','US_GAAP');actual=assess_case('alternative-performance-measures',owner)
        c=case('sec-filing-accounting','US_GAAP')
        c['imports']=[approved('apm-owner',package='alternative-performance-measures',case=owner,result=actual,mode='evidence_only')]
        c['filing_review'].update(apm_present=True,apm_amounts={'current':'180','prior':'130'})
        def refreshed(c):
            c['filing_review']['reviewed_release_fingerprint']=load_workflow('sec-filing-accounting').release_fingerprint(c)
            return ready('sec-filing-accounting','US_GAAP',c)
        self.assertEqual(assess_case('sec-filing-accounting',refreshed(c))['status'],'complete')
        for mutation in ['amount','duplicate','owner','journal']:
            d=copy.deepcopy(c)
            if mutation=='amount':d['filing_review']['apm_amounts']['current']='181'
            elif mutation=='duplicate':d['imports'].append(copy.deepcopy(d['imports'][0]));d['imports'][-1]['id']='duplicate'
            elif mutation=='owner':d['imports'][0]['case']['entity']='OTHER'
            else:d['imports'][0]['mode']='post'
            self.assertEqual(assess_case('sec-filing-accounting',refreshed(d))['status'],'blocked')
    def test_sec_fpi_us_gaap_and_interim_forms(self):
        from production import load_workflow
        for fw,issuer,form,kind in [('US_GAAP','fpi','20-F','annual'),('US_GAAP','domestic','10-Q','interim'),('IFRS','fpi','6-K','interim')]:
            c=case('sec-filing-accounting',fw);c['filer'].update(issuer_type=issuer,form=form,filing_kind=kind)
            c['rule'].update(issuer_type=issuer,form=form,filing_kind=kind)
            if kind=='interim':
                c['filer']['quarter']='Q2'
                def shorten(v):
                    if isinstance(v,dict):return {k:shorten(x) for k,x in v.items()}
                    if isinstance(v,list):return [shorten(x) for x in v]
                    return {'2026-12-31':'2026-06-30','2025-12-31':'2025-06-30'}.get(v,v) if isinstance(v,str) else v
                c=shorten(c)
            c['filing_review']['reviewed_release_fingerprint']=load_workflow('sec-filing-accounting').release_fingerprint(c)
            self.assertEqual(assess_case('sec-filing-accounting',ready('sec-filing-accounting',fw,c))['status'],'complete')
    def test_saved_examples_are_current(self):
        for p in PACKAGES+BLOCKED:
            for fw in FRAMEWORKS:
                path=ROOT/'skills'/p/'examples'/f'{fw}.case.json';c=json.loads(path.read_text());r=assess_case(p,c)
                if (path.parent/f'{fw}.blocked.public.json').exists():
                    self.assertEqual(r['status'],'blocked');suffix='blocked'
                else:
                    self.assertEqual(r['status'],'partial');suffix='partial'
                    complete=assess_case(p,ready(p,fw,c));self.assertEqual(complete['status'],'complete')
                    self.assertEqual(to_public(complete),json.loads((path.parent/f'{fw}.complete.public.json').read_text()))
                self.assertEqual(to_public(r),json.loads((path.parent/f'{fw}.{suffix}.public.json').read_text()))
    def test_public_source_provenance_private(self):
        for p in PACKAGES:
            r=assess_case(p,ready(p));r['facts_used']['secret_source_notes']='INTERNAL_SOURCE_CANARY'
            r['reviewer_metadata']={'secret':'INTERNAL_REVIEWER_CANARY'}
            for route in ROUTES:
                rendered=json.dumps(to_public(r,route=route))
                self.assertNotIn('INTERNAL_SOURCE_CANARY',rendered);self.assertNotIn('INTERNAL_REVIEWER_CANARY',rendered)
                self.assertNotIn('case_fingerprint',rendered);self.assertNotIn('document_sha256',rendered)

if __name__=='__main__':unittest.main()
