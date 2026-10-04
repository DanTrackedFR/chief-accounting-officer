"""Native cross-owner ties and balanced reporting counterexamples."""
import copy
import importlib.util
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core_accounting import ReviewRequired
from production import execute
from additional_cases import certify
import governance_cases
from insurance_integration_cases import reporting_fixture,disclosure_fixture

def handoffs():
    spec=importlib.util.spec_from_file_location('_insurance_handoffs_tests',Path(__file__).resolve().parents[1]/'insurance-contracts-accounting/handoffs.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

class InsuranceIntegrationTests(unittest.TestCase):
    def test_native_statements_supported_routes(self):
        for fw,route,held in [('IFRS','gmm',False),('AASB','gmm',False),('IFRS','paa',False),('AASB','paa',True),('US_GAAP','paa',False)]:
            with self.subTest(framework=fw,route=route,held=held):
                imp,r,m=reporting_fixture(fw,held,route)
                self.assertEqual('validated',handoffs().validate_reporting_handoff(imp,r,m)['status'])

    def test_native_disclosures_supported_routes(self):
        for fw,held,route in [('IFRS',False,'gmm'),('AASB',False,'gmm'),('IFRS',True,'paa'),('AASB',True,'paa'),('US_GAAP',False,'paa')]:
            with self.subTest(framework=fw,held=held):
                imp,d=disclosure_fixture(fw,held,route)
                receipt=handoffs().validate_disclosure_handoff(imp,d)
                self.assertEqual('validated',receipt['status']);self.assertFalse(receipt['compliance_certified'])

    def test_same_amount_wrong_source_identity_blocks(self):
        imp,r,m=reporting_fixture();c=r['case'];c['current_tb'][0]['insurance_economic_id']='another-contract-same-amount'
        c=certify('financial-statements',c);r['case']=c;r['result']=execute('financial-statements',c)
        self.assertEqual('complete',r['result']['status'])
        with self.assertRaises(ReviewRequired):handoffs().validate_reporting_handoff(imp,r,m)

    def test_balanced_plug_on_insurance_statement_line_blocks(self):
        imp,r,m=reporting_fixture();c=r['case'];liability=next(x for x in c['current_tb'] if x['category']=='liability')
        extra=copy.deepcopy(liability);extra.update(id='balanced-extra-liability',balance='-17',source_version='other-owner');extra.pop('insurance_source_id');extra.pop('insurance_economic_id')
        asset=copy.deepcopy(extra);asset.update(id='balanced-extra-asset',balance='17',category='asset',line='other asset line')
        c['current_tb'] += [extra,asset];c=certify('financial-statements',c);r.update(case=c,result=execute('financial-statements',c))
        self.assertEqual('complete',r['result']['status'])
        with self.assertRaises(ReviewRequired):handoffs().validate_reporting_handoff(imp,r,m)

    def test_duplicate_economic_posting_under_other_owner_blocks(self):
        imp,r,m=reporting_fixture();c=r['case'];original=c['current_tb'][0]
        extra=copy.deepcopy(original);extra.update(id='cash-alias',source_version='ordinary-revenue-owner',line='another cash line',cash_account=False)
        opposite=dict(id='alias-offset',balance=str(-__import__('decimal').Decimal(extra['balance'])),category='liability',source_version='other-owner',line='alias offset',classification_memo='Synthetic balanced plug',cash_account=False)
        c['current_tb'] += [extra,opposite];c=certify('financial-statements',c);r.update(case=c,result=execute('financial-statements',c))
        self.assertEqual('complete',r['result']['status'])
        with self.assertRaises(ReviewRequired):handoffs().validate_reporting_handoff(imp,r,m)

    def test_duplicate_target_and_missing_mapping_block(self):
        imp,r,m=reporting_fixture()
        for bad in [m[:-1],m+[dict(m[0],id='duplicate-source')], [dict(x,tb_id=m[0]['tb_id']) for x in m]]:
            with self.assertRaises(ReviewRequired):handoffs().validate_reporting_handoff(imp,r,bad)

    def test_stale_source_certification_blocks(self):
        imp,r,m=reporting_fixture();imp['case']['reviewer_signoff']['case_fingerprint']='stale'
        with self.assertRaises(ReviewRequired):handoffs().validate_reporting_handoff(imp,r,m)

    def test_disclosure_incomplete_amount_population_blocks_receipt(self):
        imp,d=disclosure_fixture();c=d['case'];rid=c['requirements'][-1]['id']
        c['requirements']=[r for r in c['requirements'] if r['id']!=rid]
        c['notes']=[n for n in c['notes'] if n['requirement_id']!=rid]
        c['note_inventory']=[n['id'] for n in c['notes']];c['source_inventory']=[r['id'] for r in c['requirements']]
        c['requirement_source']['records']=copy.deepcopy(c['requirements']);c['requirement_source']['inventory']=c['source_inventory'][:]
        c['controls'].update(population_count=len(c['requirements']),population_amount=str(sum(abs(__import__('decimal').Decimal(r['amount'])) for r in c['requirements'])))
        c=governance_cases.ready('disclosure-management',c=c,release=True);d.update(case=c,result=execute('disclosure-management',c))
        self.assertEqual('complete',d['result']['status'])
        with self.assertRaises(ReviewRequired):handoffs().validate_disclosure_handoff(imp,d)

    def test_disclosure_namespace_cannot_be_invented(self):
        imp,d=disclosure_fixture();c=d['case']
        for r in c['requirements']:r['topic_id']='SUPPLEMENTAL_FAKE_INSURANCE'
        c['requirement_source']['records']=copy.deepcopy(c['requirements']);c['requirement_source']['applicable_topic_inventory']=['SUPPLEMENTAL_FAKE_INSURANCE']
        c=governance_cases.ready('disclosure-management',c=c,release=True)
        with self.assertRaises(ReviewRequired):execute('disclosure-management',c)

if __name__=='__main__':unittest.main()
