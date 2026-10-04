"""Actual current Hedge result consumed by the Inventory owner exactly once."""
import copy
import unittest
from decimal import Decimal
from hedge_cases import case as hedge_case,ready as hedge_ready,sources as hedge_sources
from inventory_cases import case,ready,sources,content,replace_doc,row,document,disclosure_support
from production import execute,assess_case

def inventory_handoff_case(fw='IFRS'):
    h=hedge_case(fw,'cash_flow','occurred')
    h['currency']='USD'
    h['contracts'][0]['notional']='10'
    h['valuations'][0].update(notional='10',currency='USD')
    h['population_review']['notional_total']='10'
    r=h['relationships'][0]
    r.update(actual_instrument_quantity='10',actual_item_quantity='10',forecast_quantity='10',acquired_quantity='10',sku='goods',acquisition_id='economic-receipt')
    r['risk_measurement'].update(quantity='10',currency='USD')
    h=hedge_ready(hedge_sources(h));result=execute('derivatives-hedge-accounting',h)
    adjustment=result['calculations']['basis_adjustments'][0]
    c=case(fw,'resale');m=c['movements'][0]
    m.update(owner_kind='hedge_basis',owner_import='hedge-owner',hedge_basis_adjustment_id=adjustment['id'],amount='110',date=r['transaction_date'])
    # Receipt must precede the sale in the actual supplied chronology.
    c['movements'][1]['date']='2026-12-31';c['movements'][1]['sequence']=2
    src=content(c,m['source_doc']);src.update(date=m['date'],hedge_basis_adjustment_id=adjustment['id'],hedge_already_in_components=False)
    content(c,c['movements'][1]['source_doc'])['date']='2026-12-31'
    c['items'][0]['closing_cost']='160';c['gl'][0]['closing']=c['gl'][0]['statement']='160'
    c['disclosures']['closing_inventory']='160'
    c['imports']=[row(c,'hedge-owner',package='derivatives-hedge-accounting',case=h,result=result,mode='evidence_only')]
    payload=dict(economic_id=m['economic_id'],adjustment='-90',currency='USD',production_mapping_memo='Exact identified purchased SKU and receipt',cost_qualification_memo='Framework nonfinancial basis handoff independently reviewed',eligible_manufacturing=True)
    document(c,'hedge-binding-source',payload)
    c['owner_links']=[row(c,'hedge-basis-link',owner_import='hedge-owner',result_path=['basis_adjustments',adjustment['id'],'amount'],economic_id=m['economic_id'],target_id=m['id'],source_doc='hedge-binding-source',source_field='adjustment',amount='-90')]
    c['owner_links_inventory']=['hedge-basis-link']
    effect=dict(movement_id=m['id'],owner_import='hedge-owner',owner_account='Nonfinancial asset basis adjustment',account='Merchandise',amount='-90',hedge_basis_adjustment_id=adjustment['id'])
    document(c,'hedge-retained-source',effect)
    c['owner_gl_effects']=[row(c,'hedge-retained',source_doc='hedge-retained-source',**effect)];c['owner_gl_effects_inventory']=['hedge-retained']
    cutoff=[dict(id=m['id'],economic_id=m['economic_id'],ownership_supported=True,date_reviewed=True) for m in c['movements']]
    c['cutoff']['records']=cutoff;replace_doc(c,'cutoff-source',cutoff)
    disclosure_support(c)
    return sources(c)

class HedgeInventoryIntegration(unittest.TestCase):
    def result(self,c):return assess_case('inventory-cost',ready(c=c))
    def blocked(self,c):self.assertEqual('blocked',self.result(c)['status'])
    def test_current_completed_handoff_three_frameworks(self):
        for fw in ('IFRS','AASB','UK_GAAP'):
            with self.subTest(framework=fw):
                c=inventory_handoff_case(fw);r=self.result(c);self.assertEqual('complete',r['status'],r['conclusion'])
                self.assertEqual(Decimal('160'),r['calculations']['closing_inventory'])
                self.assertEqual(Decimal('-90'),r['calculations']['retained_owner_intake'])
                self.assertEqual(Decimal('150'),r['calculations']['inventory_own_movement'])
                self.assertFalse(any(l['account'].startswith('Hedge reserve') for j in r['journal_entry_implications'] for l in j))
    def test_adjustment_not_repeated_in_purchase_components(self):
        c=inventory_handoff_case();content(c,'receipt-source')['hedge_already_in_components']=True;self.blocked(sources(c))
    def test_duplicate_handoff(self):
        c=inventory_handoff_case();r=copy.deepcopy(c['owner_links'][0]);r['id']='alias';c['owner_links'].append(r);c['owner_links_inventory'].append('alias');self.blocked(sources(c))
    def test_wrong_sku_receipt_and_period(self):
        for key,value in [('item','other'),('economic_id','other-receipt'),('date','2026-12-30')]:
            c=inventory_handoff_case();c['movements'][0][key]=value;self.blocked(sources(c))
    def test_wrong_owner_entity_currency_and_stale_result(self):
        for key,value in [('entity','Other entity'),('currency','EUR'),('reporting_period','2025-12-31')]:
            c=inventory_handoff_case();c['imports'][0]['case'][key]=value;self.blocked(sources(c))
        c=inventory_handoff_case();c['imports'][0]['result']['calculations']['basis_adjustments'][0]['amount']='-91';self.blocked(sources(c))
    def test_missing_retained_effect(self):
        c=inventory_handoff_case();c['owner_gl_effects']=[];c['owner_gl_effects_inventory']=[];self.blocked(sources(c))
    def test_wrong_gross_receipt_cost(self):
        c=inventory_handoff_case();c['movements'][0]['amount']='200';self.blocked(sources(c))
    def test_repeated_retained_journal(self):
        c=inventory_handoff_case();c['owner_gl_effects'].append(copy.deepcopy(c['owner_gl_effects'][0]));c['owner_gl_effects'][-1]['id']='alias';c['owner_gl_effects_inventory'].append('alias');self.blocked(sources(c))
    def test_generated_handoffs_reproduce(self):
        import json
        from pathlib import Path
        from production import serializable
        from generate_hedge_inventory_examples import artifacts
        root=Path(__file__).resolve().parents[2]
        for p,o in artifacts().items():self.assertEqual(json.loads((root/p).read_text()),json.loads(json.dumps(o,default=serializable)),p)

if __name__=='__main__':unittest.main()
