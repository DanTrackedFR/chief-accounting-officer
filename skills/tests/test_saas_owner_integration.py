"""Specialist regressions for the precise AR FX integration and Close defect."""
import copy
import unittest
from decimal import Decimal
from orchestration.tests.saas_fixtures import flagship
from orchestration.registry import production
from additional_cases import certify
from operational_cases import approved


class SaaSOwnerIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _, _, cls.pack = flagship()

    def ar(self):
        return copy.deepcopy(self.pack.request['facts']['receivable_population'])

    def settlement(self):
        c = self.ar()
        imported = c['imports'][0]
        fx = imported['case']
        fx['items'][0].update(settled_foreign='50', settlement_date='2026-12-20')
        fx = certify('foreign-currency', fx)
        imported.update(case=fx, result=production.assess_case('foreign-currency', fx))
        c['receipts'].append(approved('foreign-receipt', customer='Beta', amount='60', date='2026-12-20',
            allocations=[dict(id='foreign-allocation', invoice_id='old-foreign', amount='60')],
            bank_id='BANK-FX', bank_confirmed=True, currency='USD'))
        c['closing_customers'][1]['balance'] = '60'
        c.update(bank_total='310', gl_ar='1460')
        return c

    def test_foreign_settlement_and_remaining_remeasurement_reconcile(self):
        r = production.assess_case('accounts-receivable', certify('accounts-receivable', self.settlement()))
        self.assertEqual(r['status'], 'complete', r.get('conclusion'))
        self.assertEqual(r['calculations']['closing_ar'], Decimal('1460'))
        self.assertEqual(r['calculations']['fx_movement'], Decimal('10'))

    def test_unsupported_foreign_credit_fails_closed(self):
        c = self.ar()
        c['credits'] = [approved('foreign-credit', invoice_id='old-foreign', amount='5', date='2026-12-31',
                                  entitlement_supported=True, offset='contract balance', currency='USD')]
        r = production.assess_case('accounts-receivable', certify('accounts-receivable', c))
        self.assertNotEqual(r['status'], 'complete')

    def test_original_fx_invoice_date_must_match_owner_position(self):
        c = self.ar(); c['invoices'][1]['invoice_date'] = '2026-10-16'
        r = production.assess_case('accounts-receivable', certify('accounts-receivable', c))
        self.assertNotEqual(r['status'], 'complete')

    def test_close_reopen_requires_nonblank_authorization(self):
        c = copy.deepcopy(self.pack.request['facts']['close_calendar'])
        c['close']['reopen_authorization'] = ''
        r = production.assess_case('month-end-close', certify('month-end-close', c))
        self.assertNotEqual(r['status'], 'complete')


if __name__ == '__main__':
    unittest.main()
