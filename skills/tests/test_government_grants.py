"""Authored production boundary and reproducible arithmetic tests."""
import copy
import hashlib
import json
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch
from grant_cases import case,ready,capture
from production import ROOT, assess_case, to_public, case_fingerprint
from core_accounting import balance

class GrantsTests(unittest.TestCase):
    def assess(self,c):return assess_case('government-grants',ready(c=c))
    def blocked(self,c):
        r=self.assess(c);self.assertEqual('blocked',r['status'],r);self.assertEqual([],r['journal_entry_implications']);return r
    def test_framework_income_matching(self):
        for fw in ('IFRS','AASB','UK_GAAP','US_GAAP'):
            with self.subTest(fw=fw):
                r=self.assess(case(fw));self.assertEqual('complete',r['status'],r);self.assertEqual(Decimal('40'),r['calculations']['grants'][0]['current_income'])
                for e in r['journal_entry_implications']:balance(e)
    def test_asset_deferral(self):
        for fw in ('IFRS','AASB','UK_GAAP','US_GAAP'):
            r=self.assess(case(fw,'asset'));self.assertEqual('complete',r['status'],r);self.assertEqual(Decimal('90'),r['calculations']['grants'][0]['closing_deferred'])
    def test_asset_deduction(self):
        r=self.assess(case('IFRS','deduction'));self.assertEqual('complete',r['status']);self.assertEqual(Decimal('100'),r['calculations']['grants'][0]['basis_adjustment']);self.assertEqual(Decimal(0),r['calculations']['grants'][0]['current_income'])
    def test_uk_performance(self):
        r=self.assess(case('UK_GAAP','performance'));self.assertEqual('complete',r['status']);self.assertEqual(Decimal('100'),r['calculations']['grants'][0]['current_income'])
    def test_nonmonetary(self):
        r=self.assess(case('IFRS','nonmonetary'));self.assertEqual('complete',r['status'],r);self.assertNotIn('Grant cash',{l['account'] for e in r['journal_entry_implications'] for l in e})
    def test_advance(self):
        r=self.assess(case('IFRS','advance'));self.assertEqual('complete',r['status']);self.assertEqual(Decimal('100'),r['calculations']['grants'][0]['closing_advance']);self.assertEqual(Decimal(0),r['calculations']['grants'][0]['current_income'])
    def test_past_costs(self):
        r=self.assess(case('IFRS','past'));self.assertEqual('complete',r['status']);self.assertEqual(Decimal('100'),r['calculations']['grants'][0]['current_income'])
    def test_repayment(self):
        for fw in ('IFRS','AASB','UK_GAAP','US_GAAP'):
            r=self.assess(case(fw,'repayment'));self.assertEqual('complete',r['status'],r);self.assertEqual(Decimal('40'),r['calculations']['grants'][0]['repayment_expense'])
    def test_missing_compliance(self):
        c=case();del c['grants'][0]['conditions'][0]['compliance_memo'];capture(c);self.blocked(c)
    def test_cash_is_not_assurance(self):
        c=case();c['grants'][0]['recognition_review']['compliance_supported']=False;capture(c);self.blocked(c)
    def test_uk_unmet_performance(self):
        c=case('UK_GAAP','performance');c['grants'][0]['conditions'][0]['met']=False;capture(c);self.blocked(c)
    def test_us_nonadopter(self):
        c=case('US_GAAP');del c['us_adoption'];self.blocked(c)
    def test_us_cost_accumulation(self):
        r=self.assess(case('US_GAAP','cost_accumulation'));self.assertEqual('complete',r['status']);self.assertEqual(Decimal('100'),r['calculations']['grants'][0]['basis_adjustment'])
    def test_boundary_owners(self):
        for route in ('procurement','shareholder','income_tax','loan','agriculture_fvlcts','assistance'):
            c=case();c['grants'][0]['substance']=route;capture(c);self.blocked(c)
    def test_missing_costs(self):
        c=case();del c['grants'][0]['eligible_costs'];capture(c);self.blocked(c)
    def test_missing_valuation(self):
        c=case('IFRS','nonmonetary');del c['grants'][0]['valuation'];capture(c);self.blocked(c)
    def test_currency_entity_period(self):
        for key,value in [('currency','USD'),('source_entity','Other'),('source_period',['2025-01-01','2025-12-31']),('source_framework','US_GAAP')]:
            c=case();c['grants'][0][key]=value;capture(c);self.blocked(c)
    def test_wrong_period(self):
        c=case();c['period_start']='2025-01-01';c['applicability_review']['effective_period'][0]=c['period_start'];self.blocked(c)
    def test_duplicate_journal_owner(self):
        c=case();c['journal_ownership'][0]['accounting_owner']='revenue-recognition';capture(c);self.blocked(c)
    def test_duplicate_payment(self):
        c=case();p=copy.deepcopy(c['grants'][0]['payments'][0]);p['id']='second';c['grants'][0]['payments'].append(p);c['grants'][0]['payment_inventory'].append('second');capture(c);self.blocked(c)
    def test_stale_source(self):
        c=case();c['grants'][0]['agreement_amount']='101';self.blocked(c)
    def test_gl_mismatch(self):
        c=case();c['gl'][0]['closing']='1';capture(c);self.blocked(c)
    def test_uk_netting(self):
        c=case('UK_GAAP','deduction');self.blocked(c)
    def test_aasb_tier2(self):
        c=case('AASB');c['reporting_tier']=2;self.blocked(c)
    def test_unreviewed_has_no_executable_journals(self):
        c=ready();c.pop('reviewer_signoff');r=assess_case('government-grants',c);self.assertEqual('partial',r['status']);self.assertFalse(r['journal_entry_implications'])
    def test_stale_certificate(self):
        c=ready();c['assumptions'].append('changed');r=assess_case('government-grants',c);self.assertEqual('partial',r['status']);self.assertFalse(r['journal_entry_implications'])
    def test_other_owner_fingerprint_isolation(self):
        c=ready();original=Path.read_bytes
        def altered(p):return original(p)+b'\nchanged' if p==ROOT/'skills/borrowing-costs/workflow.py' else original(p)
        with patch.object(Path,'read_bytes',altered):self.assertEqual(c['reviewer_signoff']['case_fingerprint'],case_fingerprint(c))
    def test_grant_helper_invalidation(self):
        c=ready();original=Path.read_bytes
        def altered(p):return original(p)+b'\nchanged' if p==ROOT/'skills/grant_knowledge.py' else original(p)
        with patch.object(Path,'read_bytes',altered):self.assertNotEqual(c['reviewer_signoff']['case_fingerprint'],case_fingerprint(c))
    def test_all_public_routes(self):
        from interfaces.public_output import ROUTES
        r=self.assess(case())
        for route in ROUTES:
            public=json.dumps(to_public(r,route=route),default=str);self.assertNotIn('synthetic grant census reviewer',public);self.assertNotIn('case_fingerprint',public);self.assertNotIn('MODEL_DERIVED',public)
    def test_preserved_claim_bytes(self):
        preserved=json.loads((ROOT/'skills/government-grants/release-evidence/preserved-knowledge.json').read_text())
        for p,h in preserved.items():self.assertEqual(h,hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),p)

    def test_duplicate_agreement_alias(self):
        c=case();g=copy.deepcopy(c['grants'][0]);g['id']='award-alias';g['economic_id']='alias-economic';c['grants'].append(g);c['source_inventory'].append(g['id']);c['controls'].update(population_count=2,population_amount='200')
        o=copy.deepcopy(c['journal_ownership'][0]);o['id']='ownership-alias';o['economic_id']=g['economic_id'];c['journal_ownership'].append(o);c['ownership_inventory'].append(o['id']);capture(c);self.blocked(c)

    def test_new_grant_examples_exact_reproduction(self):
        import tempfile
        from generate_grant_examples import generate
        saved=json.loads((ROOT/'skills/government-grants/examples/production/SHA256SUMS.json').read_text())
        with tempfile.TemporaryDirectory() as d:
            output=Path(d);generate(output)
            self.assertEqual(saved,json.loads((output/'SHA256SUMS.json').read_text()))
            for name,h in saved.items():
                self.assertEqual(h,hashlib.sha256((ROOT/'skills/government-grants/examples/production'/name).read_bytes()).hexdigest())
                self.assertEqual((ROOT/'skills/government-grants/examples/production'/name).read_bytes(),(output/name).read_bytes())

    def test_due_failed_condition_contradicts_assurance(self):
        c=case();c['grants'][0]['conditions'][0].update(due_date='2026-11-30',met=False);capture(c);self.blocked(c)

    def test_stale_condition_cutoff(self):
        c=case();c['grants'][0]['conditions'][0]['as_of']='2027-01-31';capture(c);self.blocked(c)

    def test_us_recognition_before_incurred_cost(self):
        c=case('US_GAAP');c['grants'][0]['eligible_costs'][0]['incurred_date']='2026-11-01';capture(c);self.blocked(c)

    def test_missing_owner_asset_life(self):
        c=case('IFRS','asset');del c['grants'][0]['asset']['useful_life_years'];capture(c);self.blocked(c)

    def test_asset_unavailable_at_cutoff(self):
        c=case('IFRS','asset');c['grants'][0]['asset']['available_for_use_date']='2027-01-01';capture(c);self.blocked(c)

    def test_future_release_requires_owner_expense_basis(self):
        c=case();c['grants'][0]['release_schedule'][0]['expense_basis']='1';capture(c);self.blocked(c)

    def test_existing_posted_component_is_not_reposted(self):
        c=case();c['journal_ownership'][0]['already_posted']=True;capture(c);self.blocked(c)

    def test_grant_pnl_parallel_shift(self):
        c=case();r=next(r for r in c['gl'] if r['id']=='Grant income');r.update(opening='-40',closing='-80',statement='-80');capture(c);self.blocked(c)
