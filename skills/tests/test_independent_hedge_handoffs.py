"""Independent cross-owner original-source and balanced-plug counterexamples."""
import copy
import importlib.util
import unittest
from pathlib import Path
from decimal import Decimal
from core_accounting import ReviewRequired
from cases import ecl
from additional_cases import certify
from hedge_cases import sources,workflow
from test_independent_derivatives_hedge import independent
from production import execute


def fi_host():
    f=ecl();f['case_id']='Independent controlled financial asset host';f['instrument']['id']='actual-host';f=certify('financial-instruments-ecl',f);r=execute('financial-instruments-ecl',f)
    c=independent();c['contracts'][0].update(embedded_feature=True,financial_asset_host=True,separation_required=False,host_id='actual-host',host_item_id=f['case_id'],host_owner='FI-host-link',host_carrying='980')
    c['valuations']=[];c['gl']=[];c['imports']=[dict(id='FI-host',package='financial-instruments-ecl',case=f,result=r)];c['owner_links']=[dict(id='FI-host-link',owner_import='FI-host',result_path=['gross_carrying_amount'],amount='980')]
    return sources(c)

class IndependentHedgeHandoffs(unittest.TestCase):
    def test_matching_current_financial_asset_host_retains_owner_ecl(self):
        c=fi_host();before=copy.deepcopy(c['imports'][0]['result']);r=workflow().assess(c,[])
        self.assertEqual(r['calculations']['derivatives'][0]['route'],'financial_asset_whole_instrument_owner');self.assertEqual(c['imports'][0]['result'],before)
        self.assertEqual(before['calculations']['allowance'],Decimal('62.5'))
        self.assertFalse(r['journal_entry_implications'])
    def test_same_amount_wrong_host_original_case_identity(self):
        c=fi_host();c['contracts'][0]['host_item_id']='Unrelated same amount investment'
        with self.assertRaises(ReviewRequired):workflow().assess(sources(c),[])
    def test_financial_host_wrong_measurement_metric(self):
        c=fi_host();c['owner_links'][0].update(result_path=['allowance'],amount='62.5');c['contracts'][0]['host_carrying']='62.5'
        with self.assertRaises(ReviewRequired):workflow().assess(sources(c),[])

    def test_same_case_wrong_original_instrument_id(self):
        c=fi_host();c['contracts'][0]['host_id']='unrelated-actual-host'
        with self.assertRaises(ReviewRequired):workflow().assess(sources(c),[])
    def report_fixture(self):
        from test_hedge_reporting_integration import actual_hedge,reporting_handoff
        return [actual_hedge()], reporting_handoff([actual_hedge()])
    def certified_report(self,c):
        from reporting_cases import certified
        c=certified('financial-statements',c['framework'],case=c);r=execute('financial-statements',c);self.assertEqual(r['status'],'complete',r['conclusion']);return c,r
    def validator(self,imports,c,r,mapping=None):
        from test_hedge_reporting_integration import validate_handoff
        return validate_handoff(imports,c,r,mapping)
    def test_independent_current_reporting_owner_complete_source_mapping(self):
        from test_hedge_reporting_integration import reporting_handoff
        from hedge_cases import ready,PACKAGE
        imports=[dict(id='independent-source',case=ready(independent(route='cash_flow')))]
        imports[0]['result']=execute(PACKAGE,imports[0]['case']);c=reporting_handoff(imports);c,r=self.certified_report(c)
        receipt=self.validator(imports,c,r);self.assertEqual(receipt['source_ties'][0]['derivative_closing'],Decimal('173'));self.assertEqual(receipt['source_ties'][0]['oci'],Decimal('155.7'))
    def test_balanced_original_reporting_plug_rejected_by_production_handoff(self):
        imports,c=self.report_fixture()
        for row in c['current_tb']:
            if row['id']=='hedge-derivative-forward1':row['balance']='101'
            if row['id']=='hedge-oci-relationship1':row['balance']='-91'
        next(e for e in c['equity_bridge'] if e['id']=='hedge-equity-relationship1').update(oci='91',closing='101')
        for note in c['notes']:
            if note['id']=='hedge-assets-note':note['amount']='601'
            if note['id']=='hedge-oci-note':note['amount']='91'
        c,r=self.certified_report(c)
        with self.assertRaises(ReviewRequired):self.validator(imports,c,r)
    def test_current_reporting_wrong_entity_and_currency(self):
        for field,value in [('entity','Other legal entity'),('currency','USD')]:
            imports,c=self.report_fixture();c[field]=value;c,r=self.certified_report(c)
            with self.subTest(field=field),self.assertRaises(ReviewRequired):self.validator(imports,c,r)
    def test_duplicate_economic_source_and_aliased_target_mapping(self):
        from test_hedge_reporting_integration import validate_handoff
        imports,c=self.report_fixture();c,r=self.certified_report(c)
        duplicate=copy.deepcopy(imports[0]);duplicate['id']='alias-owner'
        with self.assertRaises(ReviewRequired):self.validator(imports+[duplicate],c,r)
        mapping=[dict(id='m1',source_import_id=imports[0]['id'],instrument_id='forward1',relationship_id='relationship1',derivative_tb_id='hedge-derivative-forward1',pnl_tb_id='hedge-pnl-forward1',oci_tb_id='hedge-oci-relationship1',equity_component_id='hedge-equity-relationship1')]
        mapping[0]['pnl_tb_id']=mapping[0]['oci_tb_id']
        with self.assertRaises(ReviewRequired):self.validator(imports,c,r,mapping)
    def test_source_gain_sign_reversal_with_fresh_native_reporting(self):
        imports,c=self.report_fixture();asset=next(r for r in c['current_tb'] if r['id']=='hedge-derivative-forward1');asset.update(balance='-100',category='liability')
        # Change hedge equity contribution by -200 and provide corresponding source P&L; native reporting remains balanced.
        next(r for r in c['current_tb'] if r['id']=='hedge-pnl-forward1').update(balance='190',category='expense')
        next(e for e in c['equity_bridge'] if e['id']=='hedge-equity-relationship1').update(profit='-190',closing='-100')
        c['cash_flow']['start_amount']='10';next(a for a in c['cash_flow']['adjustments'] if a['id']=='hedge-noncash-pnl')['amount']='190'
        c['notes']=[n for n in c['notes'] if not n['id'].startswith('hedge-')]
        c,r=self.certified_report(c)
        with self.assertRaises(ReviewRequired):self.validator(imports,c,r)

    def test_identifiable_unmapped_duplicate_source_posting(self):
        imports,c=self.report_fixture();source=imports[0]['result']['case_fingerprint']
        c['current_tb'].append(dict(id='extra-same-source-asset',balance='1',category='asset',line='Extra derivative duplicate alias',source_version=source,classification_memo='Same known source identifies duplicate derivative economics',cash_account=False))
        c['current_tb'].append(dict(id='extra-same-source-oci',balance='-1',category='oci',line='Extra OCI duplicate alias',source_version=source,classification_memo='Same known source duplicated in distinct line',cash_account=False))
        c['equity_bridge'][0].update(oci='1',closing='301')
        c['notes']=[n for n in c['notes'] if not n['id'].startswith('hedge-')]
        c,r=self.certified_report(c)
        with self.assertRaises(ReviewRequired):self.validator(imports,c,r)

if __name__=='__main__':unittest.main()
