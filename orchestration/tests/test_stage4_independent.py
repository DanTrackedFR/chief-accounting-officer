"""Independent intermediate QA. Failures retain unremediated contract findings."""
import copy
import unittest
from dataclasses import replace

from orchestration.runtime import CAO
from orchestration.tests import stage4_fixtures as fixture
from orchestration.tests.stage3_fixtures import sides
from additional_cases import certify
from interfaces.public_output import public_record, ROUTES
from orchestration.governed_plan import observation
from orchestration.stage3 import validate_group_loan_population


def bounded_attack_control(f):
    """Isolated legacy bounded chain for attacks, never full-close acceptance.

    The only change is removal of the opt-in completeness declaration in this
    test-local control. The real flagship is independently required to fail
    safely below, and its final positive coverage assertions remain unsatisfied.
    """
    plan = fixture.correct(f)
    preview = copy.deepcopy(f)
    sources = {}
    for key in plan['execution_order']:
        node = preview['session'].graph.nodes[key]
        source = fixture.source(preview, node.logical_id)
        if node.logical_id == 'elimination':
            source.pop('group_population_coverage')
            source = certify('consolidation', source)
        preview['session'].execute(key, observation, source, 'Dependency rework: ' + plan['new_version'])
        sources[key] = source
    CAO().selective_reexecute(f['case'], plan, sources)
    return f


class IndependentStage4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.initial = fixture.intake_initial()
        cls.bounded = bounded_attack_control(copy.deepcopy(cls.initial))

    def setUp(self):
        self.f = copy.deepcopy(self.bounded)
        self.e = self.f['session']

    def test_iqa01_complete_snapshot_is_in_declared_source_population(self):
        """A retained snapshot pointer cannot substitute a complete manifest."""
        f = copy.deepcopy(self.initial)
        pack = f['reviewed_pack']
        child = next(c for c in pack.scoped_packs if c.bindings)
        source = child.request['source']
        snapshot = source['qualified_input_snapshot']['source_id']
        source['source_population'].remove(snapshot)
        source['qualified_scope_sources'] = [r for r in source['qualified_scope_sources'] if r['source_id'] != snapshot]
        pack.request['governed_plan']['sources'][child.request['node_id']] = copy.deepcopy(source)
        with self.assertRaises(ValueError):
            f['intake_engine'].execute(f['intake'], pack)

    def test_iqa02_recharge_cannot_enter_ordinary_framework_conversion(self):
        """Keep closing principal equal while substituting service economics."""
        source = fixture.uk_conversion(self.f)
        pair = source['pairs'][0]
        for key in ('opening_a', 'opening_b', 'opening_book_a', 'opening_book_b'):
            pair[key] = '9'
        pair['recharge'] = '1'
        source['recharges'] = [dict(id='independent-service', owner='synthetic owner',
            reviewer='synthetic reviewer', evidence='Supplied service recharge', approved=True,
            approval_date='2026-10-31', version='v1', approved_version='v1', cost_pool='1',
            allocations=[dict(id='allocation', entity='ENTITY-NL', pair_id=pair['id'], share='1')],
            markup='0', agreement='Services agreement', tax_review='Reviewed', date='2026-10-31',
            provider='ENTITY-UK', currency='EUR', source_complete=True)]
        source = certify('intercompany-accounting', source)
        with self.assertRaises(ValueError):
            CAO().correct(self.f['case'], self.f['nodes']['uk-conversion'].id, source,
                          'Independent unsupported service conversion attack')

    def test_iqa03_current_relationships_have_group_population_dispositions(self):
        """Whole-close completeness needs inclusion or explicit reviewed exclusion."""
        eliminated = {p['transaction_id'] for p in self.e.sources[self.f['nodes']['elimination'].id]['intercompany']}
        # September evidence is not assumed to be a current closing balance;
        # the actual October UK timing side and both FX sides are current.
        required = {n.economic_id for n in self.f['nodes'].values()
                    if n.scope_type == 'LEGAL_ENTITY' and n.selected_skill == 'intercompany-accounting'
                    and n.period == ['2026-10-01', '2026-10-31']}
        dispositions = self.e.sources[self.f['nodes']['elimination'].id].get('relationship_dispositions', [])
        excluded = {r['economic_id'] for r in dispositions
                    if r.get('status') == 'REVIEWED_EXCLUSION' and r.get('evidence')}
        self.assertEqual(required - eliminated - excluded, set())

    def test_iqa03_uncovered_current_relationships_cannot_close_full_group_objective(self):
        f = copy.deepcopy(self.initial)
        # Final positive acceptance stays a hard requirement. Today this raises
        # on missing populations; safe rejection is necessary but not acceptance.
        try:
            fixture.rework(f, fixture.correct(f))
        except ValueError as exc:
            self.fail('Positive full-Group accounting integration remains incomplete: ' + str(exc))
        self.assertEqual(f['case'].outcome, 'complete')
        self.assertEqual(f['case'].status, 'CLOSED')

    def test_iqa03_real_flagship_missing_population_fails_safely(self):
        f = copy.deepcopy(self.initial)
        plan = fixture.correct(f)
        with self.assertRaisesRegex(ValueError, 'Full Group accounting omits or duplicates'):
            fixture.rework(f, plan)
        self.assertEqual(f['case'].outcome, 'partial')
        self.assertNotEqual(f['case'].status, 'CLOSED')
        answer = CAO().public(f['case'])
        self.assertEqual(answer['status'], 'partial')
        self.assertNotIn('calculations', answer)

    def test_iqa03_generic_gate_rejects_omitted_and_forged_roster(self):
        node = self.f['nodes']['elimination']
        source = fixture.group_source(self.f)
        receipts = source['versioned_dependency_receipts']
        with self.assertRaisesRegex(ValueError, 'Full Group accounting omits or duplicates'):
            validate_group_loan_population(self.e, node, source, receipts)
        source['group_population_coverage']['required_legal_result_versions'].pop()
        with self.assertRaisesRegex(ValueError, 'actual current legal results'):
            validate_group_loan_population(self.e, node, source, receipts)

    def test_initial_blocked_results_are_not_accounting_authority(self):
        e = self.initial['session']
        for label in ('uk-conversion', 'elimination', 'reporting', 'analytics'):
            v = e.versions.current(self.initial['nodes'][label].id)
            self.assertFalse(v.payload()['accounting_authority'])
            self.assertEqual(v.payload()['journal_entry_implications'], [])
            self.assertTrue(v.dependency_bindings)

    def test_stale_group_answer_cannot_publish_previous_totals(self):
        fixture.correct(self.f)
        answer = CAO().public(self.f['case'])
        self.assertEqual(answer['status'], 'partial')
        self.assertNotIn('calculations', answer)
        self.assertTrue(answer['open_items'])

    def test_invalidated_population_follows_consumed_versions(self):
        before = {k: self.e.versions.current(k).version_id for k in self.e.graph.nodes}
        plan = fixture.correct(self.f)
        affected = set(plan['execution_order'])
        self.assertEqual({self.e.graph.nodes[k].logical_id for k in affected},
                         {'match-mismatch', 'uk-conversion', 'elimination', 'reporting', 'group', 'analytics'})
        for key in plan['unaffected']:
            self.assertEqual(self.e.versions.current(key).version_id, before[key])

    def test_translation_disposition_cannot_point_to_equal_wrong_entity(self):
        ledger = fixture.journal_ledger(self.f)
        bad = copy.deepcopy(ledger['dispositions'])
        bad[0]['source_path'] = ['entities', 2, 'balances']
        with self.assertRaises(ValueError):
            self.f['basis'].current_journals(self.context(), ledger['events'], bad)

    def context(self):
        return dict(entity='GROUP-EUR', framework='IFRS', jurisdiction='NL', currency='EUR',
                    period_start='2026-10-01', reporting_period='2026-10-31',
                    scopes=self.e.cases.scopes.record(), period_registry=self.e.periods.record())

    def test_zero_implication_translation_needs_no_posting_disposition(self):
        ledger = fixture.journal_ledger(self.f)
        for label in ('translation', 'uk-translation'):
            self.assertEqual(self.e.versions.current(self.f['nodes'][label].id).payload()['journal_entry_implications'], [])
        selected, _ = self.f['basis'].current_journals(self.context(), ledger['events'], [])
        self.assertEqual(selected, ledger['selected'])

    def test_journal_event_cannot_relabel_current_version_as_other_book(self):
        ledger = fixture.journal_ledger(self.f)
        bad = copy.deepcopy(ledger['events'])
        bad[0]['posting_scope'] = 'ENTITY-UK'
        with self.assertRaises(ValueError):
            self.f['basis'].current_journals(self.context(), bad, ledger['dispositions'])

    def test_duplicate_translation_disposition_rejected(self):
        ledger = fixture.journal_ledger(self.f)
        with self.assertRaises(ValueError):
            self.f['basis'].current_journals(self.context(), ledger['events'], ledger['dispositions'] * 2)

    def test_framework_receipt_cannot_change_supported_zero_adjustment(self):
        receipts = fixture.transforms(self.f)
        receipt = next(r for r in receipts if r['kind'] == 'FRAMEWORK_CONVERSION')
        receipt['adjustment'] = '1'
        with self.assertRaises(ValueError):
            self.f['basis'].validate_transformation(receipt)

    def test_matching_original_source_fingerprint_cannot_be_relabelled(self):
        side = sides(self.f, 'clean')[0]
        with self.assertRaises(ValueError):
            replace(side, source_id='invented-original-source').validate(self.e)

    def test_raw_provenance_objects_do_not_cross_public_routes(self):
        for route in ROUTES:
            value = public_record(dict(guidance='Reviewed conclusion',
                source_manifest={'reviewer': 'PRIVATE'}, claim_register=['PRIVATE']), route=route)
            self.assertEqual(value, {'guidance': 'Reviewed conclusion'})

    def test_public_dynamic_reviewer_identity_fails_closed(self):
        source = self.e.sources[self.f['nodes']['analytics'].id]
        source['reviewer_identity'] = 'Reviewed financing cash receipt'
        with self.assertRaises(ValueError):
            CAO().public(self.f['case'])


if __name__ == '__main__':
    unittest.main()
