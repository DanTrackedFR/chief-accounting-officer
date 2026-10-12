"""Authored end-to-end and accounting-boundary regressions for controlled SaaS close."""
import copy
import json
import unittest
from decimal import Decimal
from dataclasses import replace
from orchestration.tests.saas_fixtures import flagship, narrow, sources, proposal, reviewed_pack, SCOPE, OBJECTIVE
from orchestration.intake import Intake, FixturePlanner
from orchestration.planning import FACT_ADAPTERS
from orchestration.registry import production
from additional_cases import certify


class SaaSFlagship(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine, cls.prepared, cls.pack = flagship()
        cls.result = cls.engine.execute(copy.deepcopy(cls.prepared), copy.deepcopy(cls.pack))

    def source_attack(self, source, before, after):
        raw = sources()
        item = next(s for s in raw if s.id == source)
        raw[raw.index(item)] = replace(item, payload=item.payload.replace(before, after))
        engine = Intake(FixturePlanner(proposal(raw)))
        prepared = engine.prepare(OBJECTIVE, raw, [], SCOPE)
        with self.assertRaises(ValueError):
            engine.execute(prepared, reviewed_pack(prepared))

    def owner_attack(self, package, mutation):
        family = next(f for f, (owner, _) in FACT_ADAPTERS.items() if owner == package)
        case = copy.deepcopy(self.pack.request['facts'][family])
        mutation(case)
        try:
            result = production.assess_case(package, certify(package, case))
        except (ValueError, KeyError):
            return
        self.assertNotEqual(result.get('status'), 'complete')

    def test_material_close_conflicts_are_partial(self):
        self.assertEqual(self.result.case.outcome, 'partial')
        self.assertEqual(len(self.result.questions), 2)
        self.assertEqual(len(self.result.conflicts), 2)

    def test_clean_control_completes(self):
        engine, prepared, pack = flagship(clean=True)
        result = engine.execute(prepared, pack)
        self.assertEqual(result.case.outcome, 'complete')
        self.assertFalse(result.questions)

    def test_owner_results_complete_without_certifying_sources(self):
        self.assertTrue(all(n['status'] == 'complete' for n in self.result.case.workplan_nodes))
        self.assertEqual(self.result.case.status, 'DOCUMENTED')

    def test_modes_are_scoped_to_close_investigation(self):
        modes = self.result.case.work_modes
        self.assertEqual(modes['primary'], 'CLOSE_REVIEW')
        self.assertEqual(set(modes['secondary']), {'DIAGNOSTIC_ANALYTICS', 'RECONCILIATION_INVESTIGATION'})

    def test_irrelevant_production_and_unavailable_owners_excluded(self):
        owners = set(self.result.case.skills_invoked)
        self.assertEqual(len(owners), 9)
        self.assertFalse(owners & {'inventory-cost', 'agriculture-biological-assets', 'insurance-contracts-accounting', 'derivatives-hedge-accounting', 'business-combinations', 'consolidation', 'government-grants', 'borrowing-costs', 'investment-property'})

    def test_revenue_only_stays_bounded(self):
        engine, prepared, pack = narrow('revenue-recognition', 'How much revenue did we recognise from this reviewed contract schedule?')
        result = engine.execute(prepared, pack)
        self.assertEqual(result.case.skills_invoked, ['revenue-recognition'])

    def test_ar_only_requires_its_actual_fx_exposure(self):
        engine, prepared, pack = narrow('accounts-receivable', 'What is our closing AR balance?')
        result = engine.execute(prepared, pack)
        self.assertEqual(set(result.case.skills_invoked), {'accounts-receivable', 'foreign-currency'})

    def test_ecl_only_requires_actual_exposure_not_entire_close(self):
        engine, prepared, pack = narrow('financial-instruments-ecl', 'Review the allowance on this AR ageing.')
        result = engine.execute(prepared, pack)
        self.assertEqual(set(result.case.skills_invoked), {'financial-instruments-ecl', 'accounts-receivable', 'foreign-currency'})

    def test_invoice_cannot_replace_revenue(self):
        self.source_attack('revenue', ',500,1300', ',800,1300')

    def test_receipt_cannot_replace_revenue(self):
        self.source_attack('revenue', ',500,1300', ',250,1300')

    def test_contract_liability_cannot_replace_ar(self):
        self.source_attack('ar_summary', '1520,1520', '1300,1520')

    def test_contract_asset_cannot_be_billed_receivable(self):
        self.owner_attack('accounts-receivable', lambda c: c['invoices'][2].update(entitlement_supported=False))

    def test_unqualified_rate_change_is_source_mismatch(self):
        self.source_attack('loss_rates', ',0.10,', ',0.20,')

    def test_receipt_duplicate_rejected(self):
        def duplicate(c):
            row = copy.deepcopy(c['receipts'][0]); row['id'] = 'duplicate'; c['receipts'].append(row)
        self.owner_attack('accounts-receivable', duplicate)

    def test_wrong_due_date_source_rejected(self):
        self.source_attack('billing', '2026-11-01', '2026-12-30')

    def test_wrong_invoice_date_source_rejected(self):
        self.source_attack('billing', '2026-10-15', '2026-12-15')

    def test_foreign_original_amount_source_rejected(self):
        self.source_attack('billing', 'EUR,100,true', 'EUR,110,true')

    def test_fx_remeasurement_cannot_be_missing(self):
        self.owner_attack('accounts-receivable', lambda c: c.pop('imports'))

    def test_customer_to_gl_disagreement_rejected(self):
        self.owner_attack('accounts-receivable', lambda c: c['closing_customers'][1].update(balance='110'))

    def test_reopened_period_needs_evidence(self):
        self.owner_attack('month-end-close', lambda c: c['close'].update(reopen_authorization=''))

    def test_unapproved_journal_cannot_complete(self):
        self.owner_attack('month-end-close', lambda c: c['journals'][0].update(approved=False))

    def test_unresolved_close_task_cannot_complete(self):
        self.owner_attack('month-end-close', lambda c: c['tasks'][0].update(complete=False))

    def test_wrong_source_journal_approval_date_rejected(self):
        self.source_attack('journals', '2027-01-02,2027-01-02', '2026-12-31,2027-01-02')

    def test_reconciliation_difference_not_plugged(self):
        self.owner_attack('balance-sheet-reconciliations', lambda c: c['reconciliations'][0].update(source_closing='5245'))

    def test_material_unexplained_reconciliation_not_complete(self):
        self.owner_attack('balance-sheet-reconciliations', lambda c: c['reconciliations'][0].update(gl_closing='5245'))

    def test_effective_date_is_not_approval_date(self):
        observation = self.result.case.close_observations[0]
        self.assertEqual(observation['effective_date'], '2026-12-31')
        self.assertEqual(observation['approval_date'], '2027-01-02')

    def test_late_journal_and_authorized_reopen_exposed(self):
        self.assertEqual({r['kind'] for r in self.result.case.close_observations}, {'late_posting', 'reopened_period'})

    def test_all_bridges_have_zero_explicit_residual(self):
        bridges = self.result.case.balance_diagnostics['bridges']
        self.assertEqual(set(bridges), {'ar', 'contract_net', 'allowance'})
        for bridge in bridges.values():
            self.assertEqual(Decimal(bridge['residual']), 0)
            self.assertEqual(Decimal(bridge['opening']) + sum((Decimal(d['amount']) for d in bridge['drivers']), Decimal(0)), Decimal(bridge['closing']))

    def test_fx_not_revenue_growth(self):
        balances = self.result.case.balance_diagnostics
        self.assertEqual(Decimal(balances['revenue']['change']), 100)
        self.assertEqual(Decimal(balances['fx_effect']), 10)
        self.assertEqual(sum(Decimal(d['amount']) for d in balances['bridges']['ar']['drivers'] if d['label'] == 'Receivable FX'), 10)

    def test_dso_formula_is_snapshot_billings_and_calendar_days(self):
        dso = self.result.case.balance_diagnostics['dso']
        self.assertEqual(dso['formula'], 'ending gross billed AR / period net billings * actual calendar days')
        self.assertEqual((dso['current_days'], dso['prior_days']), (31, 30))
        self.assertEqual(Decimal(dso['current']), Decimal('58.90'))
        self.assertEqual(Decimal(dso['prior']), Decimal('54.60'))

    def test_growth_only_collection_explanation_rejected(self):
        self.assertEqual(self.result.hypothesis_results[0]['disposition'], 'REJECTED')

    def test_accounting_escalation_uses_ecl_owner(self):
        question = self.result.case.accounting_questions[0]
        self.assertEqual(question['target_owner'], 'financial-instruments-ecl')
        self.assertEqual(question['status'], 'OWNER_RECHECK_SUPPORTED')

    def test_three_material_lineages_reach_source_rows(self):
        for fact, source in [('rev-progress', 'revenue'), ('ar-applied', 'receipts'), ('rev-billings', 'revenue')]:
            link = next(r for r in self.result.lineage if r['fact_id'] == fact)
            self.assertEqual(link['source_lineage'][0]['source_id'], source)
            self.assertTrue(link['source_lineage'][0]['location']['row'])

    def test_public_journals_count_postings_once_and_balance(self):
        answer = self.engine.public(self.result)
        self.assertEqual(len(answer['journals']), 7)
        for journal in answer['journals']:
            self.assertEqual(sum(Decimal(l['amount']) * (1 if l['side'] == 'Dr' else -1) for l in journal['lines']), 0)

    def test_public_answer_no_internal_provenance(self):
        text = json.dumps(self.engine.public(self.result))
        for forbidden in ['fingerprint', 'Synthetic independent', 'SKILL-', 'source_notes', 'owner_import']:
            self.assertNotIn(forbidden, text)

    def test_memory_candidates_not_promoted(self):
        self.assertTrue(self.result.memory_candidates)
        self.assertFalse(any(r.get('promoted') is True for r in self.result.memory_candidates))


if __name__ == '__main__':
    unittest.main()
