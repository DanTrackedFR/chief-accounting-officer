"""Current Hedge result consumed by the actual six-statement reporting owner.

The test adapter binds current executable source bytes to statement rows and
separate OCI/P&L/equity bridges. It does not change either owner contract.
"""
import copy
import unittest
from decimal import Decimal
from hedge_cases import case,ready,sources,workflow,PACKAGE
from additional_cases import reporting
from production import execute,assess_case,case_fingerprint
from core_accounting import ReviewRequired,dec
from reporting_cases import certified


def actual_hedge(fw='IFRS'):
    c=ready(case(fw,'cash_flow'));return dict(id='hedge-owner',case=c,result=execute(PACKAGE,c))


def reporting_handoff(imports):
    """Fresh complete source reperformance, economic identity and exact signed rows."""
    if not imports:raise ReviewRequired('Actual Hedge owner required')
    sources=[];seen=set();first=imports[0]['case'];c=reporting(first['framework'])
    profit=Decimal('200');oci=Decimal(0);source_pnl=Decimal(0)
    for imp in imports:
        hc=imp['case'];current=execute(PACKAGE,hc)
        if current['status']!='complete' or workflow().digest(current)!=workflow().digest(imp['result']):
            raise ReviewRequired('Actual current completed Hedge owner bytes required')
        if any(hc[k]!=c[k] for k in ('entity','framework','jurisdiction','period_start','reporting_period')):
            raise ReviewRequired('Reporting owner context differs from Hedge')
        for row in current['calculations']['derivatives']:
            economic=(hc['entity'],hc['reporting_period'],row['id'])
            if economic in seen:raise ReviewRequired('Duplicate derivative economic owner posting')
            seen.add(economic)
            if row['route'] not in {'cash_flow'}:raise ReviewRequired('This independent adapter tests basic continuing CF only')
            closing=dec(row['closing']);pnl=dec(row['ineffectiveness'])
            c['current_tb'].append(dict(id='hedge-derivative-'+row['id'],balance=str(closing),category='asset' if closing>=0 else 'liability',line='Derivative balance '+row['id'],source_version=current['case_fingerprint'],classification_memo='Actual current independently qualified Hedge result',cash_account=False))
            c['current_tb'].append(dict(id='hedge-pnl-'+row['id'],balance=str(-pnl),category='revenue' if pnl>=0 else 'expense',performance_category='financing',line='Derivative ineffectiveness',source_version=current['case_fingerprint'],classification_memo='Hedge owner actual signed earnings effect',cash_account=False))
            profit+=pnl;source_pnl+=pnl
        for reserve in current['calculations']['hedge_reserves']:
            if dec(reserve['opening'])!=0 or dec(reserve['reclassification']) or dec(reserve['basis_adjustment']):
                raise ReviewRequired('Independent integration adapter is continuing first-year reserve only')
            movement=dec(reserve['recognized_oci']);oci+=movement
            c['current_tb'].append(dict(id='hedge-oci-'+reserve['id'],balance=str(-movement),category='oci',line='Cash-flow hedge OCI',source_version=current['case_fingerprint'],classification_memo='Actual owner reserve movement; closing reserve is represented exactly once through OCI',cash_account=False))
        sources.append(dict(case_fingerprint=current['case_fingerprint'],result_hash=workflow().digest(current),original_source_hashes={d['id']:d['content_hash'] for d in hc['documents']}))
    # OCI is unclosed in this TB. Do not also add the closing reserve as equity.
    for imp in imports:
        for reserve in imp['result']['calculations']['hedge_reserves']:
            d=imp['result']['calculations']['derivatives'][0]
            c['equity_bridge'].append(dict(source_case_fingerprint=imp['result']['case_fingerprint'],id='hedge-equity-'+reserve['id'],opening='0',profit=str(d['ineffectiveness']),oci=str(reserve['recognized_oci']),owner_transactions='0',retrospective_adjustments='0',other='0',closing=str(dec(d['ineffectiveness'])+dec(reserve['closing'])),memo='Dedicated source Hedge equity contribution; baseline owner bridge remains separate'))
    c['currency']=first['currency']
    c['cash_flow']['start_amount']=str(profit)
    c['cash_flow']['adjustments'].append(dict(id='hedge-noncash-pnl',amount=str(-source_pnl),source='Current reexecuted Hedge source fingerprints '+','.join(s['case_fingerprint'] for s in sources),noncash_acquisition_fx_excluded=True,memo='Reverse only noncash derivative earnings; no invented cash/OCI adjustment'))
    c['notes'] += [dict(id='hedge-assets-note',target='assets',amount=str(Decimal('500')+sum((dec(i['result']['calculations']['derivatives'][0]['closing']) for i in imports),Decimal(0))),population_evidence=workflow().digest(sources),memo='Actual derivative carrying balances included in asset population'),dict(id='hedge-profit-note',target='profit',amount=str(profit),population_evidence=workflow().digest(sources),memo='Source P&L exact tie'),dict(id='hedge-oci-note',target='oci',amount=str(oci),population_evidence=workflow().digest(sources),memo='Source reserve exact OCI tie')]
    c['hedge_source_receipts']=sources
    return c


def validate_handoff(imports,c,r,mapping=None):
    import importlib.util
    from pathlib import Path
    spec=importlib.util.spec_from_file_location('hedge_current_reporting',Path(__file__).resolve().parents[1]/PACKAGE/'handoffs.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    if mapping is None:
        mapping=[dict(id='source-map-'+i['id'],source_import_id=i['id'],instrument_id='forward1',relationship_id='relationship1',derivative_tb_id='hedge-derivative-forward1',pnl_tb_id='hedge-pnl-forward1',oci_tb_id='hedge-oci-relationship1',equity_component_id='hedge-equity-relationship1') for i in imports]
    return mod.validate_reporting_handoff(imports,dict(case=c,result=r),mapping)

class HedgeReportingIntegration(unittest.TestCase):
    def report(self,c):return assess_case('financial-statements',certified('financial-statements',c['framework'],case=c))
    def test_current_actual_reporting_owner_exact_four_frameworks(self):
        for fw in ('IFRS','AASB','US_GAAP','UK_GAAP'):
            imp=actual_hedge(fw);c=reporting_handoff([imp]);r=self.report(c)
            self.assertEqual(r['status'],'complete',r['conclusion'])
            validated=validate_handoff([imp],c,r);self.assertEqual(validated['status'],'validated')
            source=imp['result']['calculations'];out=r['calculations']['current']
            self.assertEqual(out['lines']['Derivative balance forward1'],source['derivatives'][0]['closing'])
            self.assertEqual(out['profit']-Decimal('200'),source['derivatives'][0]['ineffectiveness'])
            self.assertEqual(out['oci'],source['hedge_reserves'][0]['closing'])
            self.assertEqual(dec(next(e for e in r['calculations']['equity_components'] if e['id'].startswith('hedge-equity-'))['oci']),out['oci'])
            self.assertEqual(out['closing_equity'],Decimal('100')+out['profit']+out['oci'])
            self.assertEqual(r['calculations']['cash_flow']['closing'],Decimal('290'))
    def test_duplicate_source_owner_rejected(self):
        i=actual_hedge()
        with self.assertRaises(ReviewRequired):reporting_handoff([i,copy.deepcopy(i)])
    def test_fabricated_result_rejected(self):
        i=actual_hedge();i['result']['calculations']['derivatives'][0]['closing']='101'
        with self.assertRaises(ReviewRequired):reporting_handoff([i])
    def test_unauthorized_owner_result_cannot_bypass_reexecution(self):
        i=actual_hedge();i['case']['reviewer_signoff']['case_fingerprint']='fabricated'
        with self.assertRaises(ReviewRequired):reporting_handoff([i])
    def test_reporting_oci_mismatch_rejected(self):
        c=reporting_handoff([actual_hedge()]);c['equity_bridge'][0]['oci']='89'
        self.assertEqual(self.report(c)['status'],'blocked')
    def test_reporting_derivative_mismatch_rejected(self):
        c=reporting_handoff([actual_hedge()]);next(r for r in c['current_tb'] if r['id']=='hedge-derivative-forward1')['balance']='99'
        self.assertEqual(self.report(c)['status'],'blocked')
    def test_reporting_pnl_mismatch_rejected(self):
        c=reporting_handoff([actual_hedge()]);c['cash_flow']['start_amount']='209'
        self.assertEqual(self.report(c)['status'],'blocked')
    def test_duplicate_closed_reserve_posting_rejected(self):
        c=reporting_handoff([actual_hedge()]);c['current_tb'].append(dict(id='wrong-second-reserve',balance='-90',category='equity',line='Duplicate hedge reserve',source_version='bad',classification_memo='Wrong double posting of OCI already included',cash_account=False))
        self.assertEqual(self.report(c)['status'],'blocked')
    def test_financial_instruments_host_classification_and_ecl_remain_owner(self):
        from cases import ecl
        fi=ecl('IFRS');before=execute('financial-instruments-ecl',fi);original=workflow().digest(fi)
        c=case();c['contracts'][0].update(embedded_feature=True,financial_asset_host=True,separation_required=False,host_owner='host-link',host_carrying='980',host_item_id=fi['case_id'])
        c['imports']=[dict(id='host1',package='financial-instruments-ecl',case=fi,result=before)]
        c['owner_links']=[dict(id='host-link',owner_import='host1',result_path=['gross_carrying_amount'],amount='980')]
        c['valuations']=[];c['gl']=[];c=sources(c)
        out=execute(PACKAGE,ready(c))
        self.assertEqual(out['status'],'complete')
        self.assertEqual(out['calculations']['derivatives'][0]['route'],'financial_asset_whole_instrument_owner')
        self.assertEqual(out['journal_entry_implications'],[])
        after=execute('financial-instruments-ecl',fi)
        self.assertEqual(workflow().digest(fi),original)
        self.assertEqual(workflow().digest(before),workflow().digest(after))
        self.assertEqual(after['calculations']['allowance'],Decimal('62.50'))
        self.assertEqual(fi['instrument']['measurement'],'amortized_cost')
    def test_financial_instruments_result_cannot_be_rewritten_by_hedge(self):
        from cases import ecl
        fi=ecl('IFRS');result=execute('financial-instruments-ecl',fi);result['calculations']['allowance']='0'
        c=case();c['contracts'][0].update(embedded_feature=True,financial_asset_host=True,separation_required=False,host_owner='host-link',host_carrying='980')
        c['imports']=[dict(id='host1',package='financial-instruments-ecl',case=fi,result=result)]
        c['owner_links']=[dict(id='host-link',owner_import='host1',result_path=['gross_carrying_amount'],amount='980')]
        c['valuations']=[];c['gl']=[]
        with self.assertRaises(ReviewRequired):execute(PACKAGE,ready(sources(c)))
    def test_balanced_fresh_reporting_plug_rejected_by_production_handoff(self):
        i=actual_hedge();c=reporting_handoff([i])
        next(x for x in c['current_tb'] if x['id']=='hedge-derivative-forward1')['balance']='101'
        next(x for x in c['current_tb'] if x['id']=='hedge-oci-relationship1')['balance']='-91'
        component=next(x for x in c['equity_bridge'] if x['id']=='hedge-equity-relationship1');component.update(oci='91',closing='101')
        next(x for x in c['notes'] if x['id']=='hedge-assets-note')['amount']='601'
        next(x for x in c['notes'] if x['id']=='hedge-oci-note')['amount']='91'
        c=certified('financial-statements',c['framework'],case=c);r=execute('financial-statements',c)
        self.assertEqual(r['status'],'complete')
        with self.assertRaises(ReviewRequired):validate_handoff([i],c,r)
    def test_source_mapping_wrong_economic_item_rejected(self):
        i=actual_hedge();c=certified('financial-statements','IFRS',case=reporting_handoff([i]));r=execute('financial-statements',c)
        mapping=[dict(id='wrong-map',source_import_id=i['id'],instrument_id='unrelated-forward',relationship_id='relationship1',derivative_tb_id='hedge-derivative-forward1',pnl_tb_id='hedge-pnl-forward1',oci_tb_id='hedge-oci-relationship1',equity_component_id='hedge-equity-relationship1')]
        with self.assertRaises(ReviewRequired):validate_handoff([i],c,r,mapping)
    def test_duplicate_reporting_mapping_rejected(self):
        i=actual_hedge();c=certified('financial-statements','IFRS',case=reporting_handoff([i]));r=execute('financial-statements',c)
        m=dict(id='one',source_import_id=i['id'],instrument_id='forward1',relationship_id='relationship1',derivative_tb_id='hedge-derivative-forward1',pnl_tb_id='hedge-pnl-forward1',oci_tb_id='hedge-oci-relationship1',equity_component_id='hedge-equity-relationship1');n=copy.deepcopy(m);n['id']='two'
        with self.assertRaises(ReviewRequired):validate_handoff([i],c,r,[m,n])
    def test_reporting_note_tie_rejects_wrong_reserve(self):
        c=reporting_handoff([actual_hedge()]);next(n for n in c['notes'] if n['id']=='hedge-oci-note')['amount']='91'
        self.assertEqual(self.report(c)['status'],'blocked')

if __name__=='__main__':unittest.main()
