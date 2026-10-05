"""Independent adversarial acceptance tests derived from live owner contracts."""
import copy
from dataclasses import replace
from decimal import Decimal
import json
import importlib.util
import unittest
from orchestration.tests.saas_fixtures import flagship, sources, proposal, reviewed_pack, SCOPE
from orchestration.intake import Intake, FixturePlanner
from orchestration.runtime import CAO, Case, Graph, Node
from orchestration.registry import production, ROOT
from orchestration.planning import FACT_ADAPTERS
from additional_cases import certify

class IndependentSaaSAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine, cls.prepared, cls.pack = flagship()
        cls.result = cls.engine.execute(copy.deepcopy(cls.prepared), copy.deepcopy(cls.pack))
    def owner(self, package):
        family = next(f for f,(p,_) in FACT_ADAPTERS.items() if p==package)
        return copy.deepcopy(self.pack.request['facts'][family])
    def reject_owner(self, package, change):
        native=self.owner(package);change(native)
        try: result=production.assess_case(package,certify(package,native))
        except (ValueError,KeyError):return
        self.assertNotEqual(result.get('status'),'complete',str(result.get('conclusion')))
    def test_material_source_conflict_never_clean(self):
        self.assertEqual(self.result.case.outcome,'partial')
        self.assertTrue(self.result.conflicts)
        self.assertNotEqual(self.result.case.status,'CLOSED')
    def test_revenue_billing_cash_and_liability_are_distinct(self):
        n={r['selected_skill']:r for r in self.result.case.workplan_nodes}
        rev=n['revenue-recognition']['result']['calculations'];ar=n['accounts-receivable']['result']['calculations']
        self.assertEqual(str(rev['period_revenue']),'500.00');self.assertEqual(str(ar['billed']),'800')
        self.assertEqual(str(ar['bank_receipts']),'250');self.assertEqual(str(ar['unapplied_liability']),'50')
        self.assertEqual(str(rev['contract_bridge']['closing']),'-1300.00')
    def test_duplicate_receipt_bank_id(self):
        def change(c):
            duplicate=copy.deepcopy(c['receipts'][0]);duplicate['id']='second-receipt';c['receipts'].append(duplicate)
        self.reject_owner('accounts-receivable',change)
    def test_unapplied_cash_cannot_be_ignored(self):
        self.reject_owner('accounts-receivable',lambda c:c.update(gl_unapplied='0'))
    def test_foreign_currency_cannot_be_relabelled(self):
        self.reject_owner('accounts-receivable',lambda c:c['invoices'][1].update(currency='USD'))
    def test_foreign_amount_changed(self):
        self.reject_owner('accounts-receivable',lambda c:c['invoices'][1].update(foreign_amount='101'))
    def test_wrong_fx_item_or_duplicate_position(self):
        for key,value in [('fx_item','missing'),('fx_import','missing')]:
            with self.subTest(key=key):self.reject_owner('accounts-receivable',lambda c:c['invoices'][1].update({key:value}))
    def test_stale_fx_owner_result(self):
        self.reject_owner('accounts-receivable',lambda c:c['imports'][0]['result']['calculations'].update(monetary_fx_profit='99'))
    def test_ar_customer_total_mismatch(self):
        self.reject_owner('accounts-receivable',lambda c:c['closing_customers'][0].update(balance='1399'))
    def test_wrong_framework_credit_method(self):
        self.reject_owner('financial-instruments-ecl',lambda c:c['instrument'].update(impairment_model='CECL'))
    def reject_credit_review(self, change):
        e=self.owner('financial-instruments-ecl');change(e);e=certify('financial-instruments-ecl',e)
        a=self.owner('accounts-receivable');inputs={'accounts-receivable':a,'financial-instruments-ecl':e};g=Graph()
        for pkg,c in inputs.items():
            n=Node(pkg,'review',pkg,'actual exposure',c['entity'],c['framework'],[c['period_start'],c['reporting_period']]);n.status='complete';n.result=production.assess_case(pkg,c);g.add(n)
        case=Case('independent-credit','Review credit',periods=['2026-12-01','2026-12-31'])
        CAO()._challenge(case,g,inputs,{}, {})
        self.assertEqual(g.nodes['financial-instruments-ecl'].status,'blocked')
    def test_stale_loss_rate_table_is_rejected(self):
        # This requalification retains all rate/exposure facts; only date metadata
        # changes. It isolates rate freshness rather than fingerprint rejection.
        self.reject_credit_review(lambda c:c['credit']['loss_rate_review'].update(as_of='2020-12-31',effective_from='2020-01-01',reviewed_on='2020-12-31'))
    def test_malformed_loss_rate_dates_are_rejected(self):
        for key,value in [('effective_from','0000-not-a-date'),('reviewed_on','2026-12-99')]:
            with self.subTest(key=key):self.reject_credit_review(lambda c:c['credit']['loss_rate_review'].update({key:value}))
    def test_unreviewed_loss_rate_table_is_rejected(self):
        self.reject_credit_review(lambda c:c['credit'].pop('loss_rate_review'))
    def test_journal_ownership_mutation_stales_review(self):
        request=copy.deepcopy(self.pack.request);request['journal_ownership'][0]['evidence']='changed after exact review'
        c=CAO().run(request)
        self.assertNotEqual(c.outcome,'complete')
        self.assertTrue(any('journal' in str(n['open_items']).lower() for n in c.workplan_nodes))
    def test_journal_atoms_cannot_be_omitted_doubled_or_forged(self):
        native=[]
        for n in self.result.case.workplan_nodes:
            if n['status']=='complete':native.append(dict(owner=n['selected_skill'],case_fingerprint=n['result']['case_fingerprint'],journals=n['result'].get('journal_entry_implications',[])))
        mapping=self.pack.request['journal_account_mapping'];original=self.pack.request['journal_ownership']
        for mutation in ('omit','duplicate','amount','wrong_witness'):
            events=copy.deepcopy(original)
            if mutation=='omit':events.pop()
            elif mutation=='duplicate':events.append(copy.deepcopy(events[0]))
            elif mutation=='amount':events[3]['primary'][0]['amount']='201'
            else:events[1]['witnesses']=[[dict(owner='revenue-recognition',index=0)]]
            with self.subTest(mutation=mutation),self.assertRaises(ValueError):CAO._qualified_journals(native,mapping,events)
    def test_wrong_entity_period_currency_rejected(self):
        for key,value in [('entity','Other'),('reporting_period','2026-11-30'),('functional_currency','EUR')]:
            request=copy.deepcopy(self.pack.request);request['facts']['receivable_population'][key]=value
            with self.subTest(key=key):self.assertNotEqual(CAO().run(request).outcome,'complete')
    def test_source_binding_changes_rejected(self):
        pack=copy.deepcopy(self.pack);pack.request['facts']['customer_contract']['balance_bridge']['billings']='500'
        with self.assertRaisesRegex(ValueError,'differs from prepared source|requires qualified owner result'):self.engine.execute(copy.deepcopy(self.prepared),pack)
    def test_reopened_and_late_journal_remain_visible(self):
        kinds={r['kind'] for r in self.result.case.close_observations}
        self.assertTrue({'late_posting','reopened_period'}<=kinds)
        late=next(r for r in self.result.case.close_observations if r['kind']=='late_posting')
        self.assertNotEqual(late['effective_date'],late['approval_date'])
    def test_incomplete_close_task_rejected(self):
        self.reject_owner('month-end-close',lambda c:c['tasks'][0].update(complete=False))
    def test_public_privacy_retains_limitations(self):
        public=CAO().public(self.result.case);serialized=json.dumps(public,default=str)
        for forbidden in ('case_fingerprint','payload_fingerprint','Synthetic independent journal integration reviewer','SKILL-','fx-owner'):
            with self.subTest(forbidden=forbidden):self.assertNotIn(forbidden,serialized)
        self.assertTrue(public['open_items']);self.assertTrue(public['limitations'])
    def test_irrelevant_owners_excluded(self):
        invoked=set(self.result.case.skills_invoked)
        self.assertFalse(invoked & {'inventory-cost','agriculture-biological-assets','insurance-contracts-accounting','derivatives-hedge-accounting','business-combinations','consolidation','government-grants','borrowing-costs','investment-property'})
    def test_narrow_revenue_does_not_expand_close(self):
        raw=sources();objective='How much revenue did we recognise from this reviewed contract schedule?'
        e=Intake(FixturePlanner(proposal(raw,objective,'revenue-recognition')));p=e.prepare(objective,raw,[],SCOPE)
        result=e.execute(p,reviewed_pack(p,objective,'revenue-recognition'))
        self.assertEqual(result.case.skills_invoked,['revenue-recognition'])

    def balance_diagnostic(self, change=lambda c:None):
        c=self.owner('management-accounting-analytics');change(c)
        spec=importlib.util.spec_from_file_location('independent_balance',ROOT/'skills/management-accounting-analytics/diagnostics.py')
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        return m.assess_balances(c,{d['id']:d for d in c['documents']})
    def balance_source(self,c):
        return next(d['content'] for d in c['documents'] if d['id']=='balance-source')
    def test_dso_definition_cannot_change(self):
        with self.assertRaises(ValueError):self.balance_diagnostic(lambda c:self.balance_source(c)['dso'].update(denominator='revenue'))
    def test_budget_not_prior_actual(self):
        with self.assertRaises(ValueError):self.balance_diagnostic(lambda c:self.balance_source(c).update(prior_kind='budget'))
    def test_contract_liability_cannot_be_ar_metric(self):
        with self.assertRaises(ValueError):self.balance_diagnostic(lambda c:self.balance_source(c)['refs']['gross_ar'].update(owner_import='revenue-recognition',result_path=['contract_bridge','closing'],amount='-1300'))
    def test_fx_cannot_be_revenue_metric(self):
        with self.assertRaises(ValueError):self.balance_diagnostic(lambda c:self.balance_source(c)['refs']['revenue'].update(owner_import='foreign-currency',result_path=['monetary_fx_profit'],amount='10'))
    def test_bridge_residuals_and_hypothesis(self):
        diagnostic=self.balance_diagnostic()
        self.assertTrue(all(str(b['residual']) in ('0','0.00') for b in diagnostic['bridges'].values()))
        self.assertEqual(diagnostic['management_hypothesis']['disposition'],'REJECTED')
        self.assertFalse(diagnostic['management_hypothesis']['accounting_authority'])
        self.assertEqual(diagnostic['dso']['current_days'],31);self.assertEqual(diagnostic['dso']['prior_days'],30)
        self.assertEqual(diagnostic['dso']['current_denominator'],'800')
    def test_fs_stale_owner_result_invalidates(self):
        request=copy.deepcopy(self.pack.request)
        request['facts']['currency_exposure']['items'][0]['closing_rate']='1.21'
        c=CAO().run(request)
        self.assertNotEqual(c.outcome,'complete')
        self.assertFalse(any(n['selected_skill']=='financial-statements' and n['status']=='complete' for n in c.workplan_nodes))
    def test_ecl_exposure_bucket_reclassification_without_ar_evidence(self):
        def change(c):
            c['credit']['scenarios'][0]['terms'][0]['bucket']='31_60'
            c['credit']['loss_rate_review']['rows']=copy.deepcopy(c['credit']['scenarios'][0]['terms'])
        self.reject_credit_review(change)
    def test_executable_source_lineage_three_quantitative_owners(self):
        owners={r['owner'] for r in self.result.lineage}
        self.assertTrue({'revenue-recognition','accounts-receivable','financial-instruments-ecl'}<=owners)
        for r in self.result.lineage:self.assertTrue(r['extracted_fields']);self.assertTrue(r['source_lineage'])
        self.assertTrue(any(r['producer']=='accounts-receivable' and r['consumer']=='financial-statements' for r in self.result.case.handoff_ledger))
    def test_material_unresolved_reconciliation_not_clean(self):
        public=CAO().public(self.result.case)
        self.assertIn('partial',public['status'].lower())
        self.assertTrue(any('conflict' in str(x).lower() or 'reconciliation' in str(x).lower() for x in public['open_items']))

    def test_changed_original_due_date_cannot_reuse_hardcoded_owner(self):
        raw=sources()
        raw=[replace(r,payload=r.payload.replace('2026-11-01','2026-12-30')) if r.id=='billing' else r for r in raw]
        e=Intake(FixturePlanner(proposal(raw)));p=e.prepare(self.pack.request['objective'],raw,[],SCOPE)
        try:
            pack=reviewed_pack(p);result=e.execute(p,pack)
        except ValueError:return
        n=next(n for n in result.case.workplan_nodes if n['selected_skill']=='accounts-receivable')
        # Source now places domestic opening debt in 1_30, not 31_60. Qualified
        # source input must change or remain explicitly unresolved, never reuse.
        self.assertFalse(n['status']=='complete' and Decimal(str(n['result']['calculations']['ageing']['31_60']))==Decimal('720'))
    def test_narrow_ar_and_ecl_required_dependencies_only(self):
        for owner,objective,expected in [
            ('accounts-receivable','What is our closing AR balance?',{'accounts-receivable','foreign-currency'}),
            ('financial-instruments-ecl','Review the allowance on this AR ageing.',{'financial-instruments-ecl','accounts-receivable','foreign-currency'})]:
            with self.subTest(owner=owner):
                raw=sources();e=Intake(FixturePlanner(proposal(raw,objective,owner)));p=e.prepare(objective,raw,[],SCOPE)
                result=e.execute(p,reviewed_pack(p,objective,owner))
                self.assertEqual(set(result.case.skills_invoked),expected)
                self.assertEqual(result.case.outcome,'complete')
    def test_source_invoice_population_duplicate_and_omission(self):
        for mutation in ('extra','duplicate','owner_omission'):
            with self.subTest(mutation=mutation):
                raw=sources()
                if mutation in ('extra','duplicate'):
                    extra='extra,Alpha,10,2026-12-01,2027-01-01,USD,10,false\n' if mutation=='extra' else 'current,Alpha,800,2026-12-01,2027-01-01,USD,800,false\n'
                    raw=[replace(r,payload=r.payload+extra) if r.id=='billing' else r for r in raw]
                e=Intake(FixturePlanner(proposal(raw)));p=e.prepare(self.pack.request['objective'],raw,[],SCOPE);pack=reviewed_pack(p)
                if mutation=='owner_omission':pack.request['facts']['receivable_population']['invoices'].pop()
                with self.assertRaisesRegex(ValueError,'population differ'):e.execute(p,pack)
    def test_source_duplicate_bank_population(self):
        raw=[replace(r,payload=r.payload+'BANK-DEC,Alpha,250,200,50,5250\n') if r.id=='receipts' else r for r in sources()]
        e=Intake(FixturePlanner(proposal(raw)));p=e.prepare(self.pack.request['objective'],raw,[],SCOPE)
        with self.assertRaisesRegex(ValueError,'population differ'):e.execute(p,reviewed_pack(p))
    def test_source_output_measure_economics_are_coherent(self):
        contract=next(r.payload for r in sources() if r.id=='contract')
        self.assertIn('1500 delivered units / 12000 contracted units = 0.125',contract)
        self.assertIn('October delivered 600, November 400 and December 500 units',contract)
        rev=self.owner('revenue-recognition')
        self.assertEqual(Decimal(rev['price_components']['fixed'])*Decimal(rev['obligations'][0]['progress'])-Decimal(rev['balance_bridge']['opening_revenue']),Decimal('500'))
    def test_owner_result_billing_cash_confusion_rejected(self):
        for amount in ('800','250'):
            raw=[replace(r,payload=r.payload.replace(',500,1300',','+amount+',1300')) if r.id=='revenue' else r for r in sources()]
            e=Intake(FixturePlanner(proposal(raw)));p=e.prepare(self.pack.request['objective'],raw,[],SCOPE)
            with self.subTest(amount=amount),self.assertRaisesRegex(ValueError,'differs from prepared source'):e.execute(p,reviewed_pack(p))
    def test_owner_result_binding_wrong_path_rejected(self):
        pack=copy.deepcopy(self.pack)
        pack.bindings=[replace(b,path=('transaction_price',)) if b.kind=='owner_result' else b for b in pack.bindings]
        with self.assertRaises(ValueError):self.engine.execute(copy.deepcopy(self.prepared),pack)
    def test_owner_result_binding_cannot_use_prior_actual(self):
        pack=copy.deepcopy(self.pack)
        pack.bindings=[replace(b,kind='owner_result',path=('period_revenue',)) if b.fact_id=='prior-revenue' else b for b in pack.bindings]
        with self.assertRaisesRegex(ValueError,'Nonactual source'):self.engine.execute(copy.deepcopy(self.prepared),pack)
    def test_owner_result_binding_stale_qualification_rejected(self):
        pack=copy.deepcopy(self.pack);pack.request['facts']['customer_contract']['obligations'][0]['progress']='0.15'
        with self.assertRaises(ValueError):self.engine.execute(copy.deepcopy(self.prepared),pack)
    def test_owner_result_billing_metric_cannot_masquerade_as_revenue(self):
        raw=[replace(r,payload=r.payload.replace(',500,1300',',800,1300')) if r.id=='revenue' else r for r in sources()]
        e=Intake(FixturePlanner(proposal(raw)));p=e.prepare(self.pack.request['objective'],raw,[],SCOPE);pack=reviewed_pack(p)
        pack.bindings=[replace(b,path=('contract_bridge','billings')) if b.fact_id=='rev-period-result' else b for b in pack.bindings]
        with self.assertRaises(ValueError):e.execute(p,pack)
