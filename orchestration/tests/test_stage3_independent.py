"""Independent release attacks: contracts must reject plausible false lineage.

Authored from Stage 3 requirements, separately from the implementation tests.
Fixtures provide native certified baseline data; mutations attack orchestration.
"""
import copy
import unittest
from dataclasses import replace
from orchestration.tests.stage3_fixtures import build, initial, downstream_source, receipts, sides, EVIDENCE
from orchestration.stage3 import validate_native_bindings
from orchestration.cross_layer_receipts import ReportingBasis
from orchestration.intercompany_network import IntercompanyNetwork, MatchingDecision


class IndependentStage3Audit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = initial(build())

    def setUp(self):
        self.f = copy.deepcopy(self.baseline)
        self.e = self.f['session']

    def validate(self, label, source):
        n = self.f['nodes'][label]
        return validate_native_bindings(self.e, n, source, receipts(self.f, n.id))

    def test_baseline_native_population_contracts(self):
        for label in ('translation', 'conversion', 'elimination', 'reporting'):
            self.validate(label, downstream_source(self.f, label))

    def test_omitted_legal_counterparty_binding_rejected(self):
        source = downstream_source(self.f, 'elimination')
        source['stage3_input_bindings'] = source['stage3_input_bindings'][:1]
        with self.assertRaises(ValueError):
            self.validate('elimination', source)

    def test_translation_row_bound_to_real_tb_not_shadow_annotation(self):
        source = downstream_source(self.f, 'translation')
        source['shadow_value'] = source['translation']['tb'][1]['balance']
        source['stage3_input_bindings'][0]['target_path'] = ['shadow_value']
        with self.assertRaises(ValueError):
            self.validate('translation', source)

    def test_conversion_zero_adjustment_cannot_bind_shadow_principal(self):
        source = downstream_source(self.f, 'conversion')
        source['shadow_value'] = source['pairs'][0]['gl_a']
        source['stage3_input_bindings'][0]['target_path'] = ['shadow_value']
        with self.assertRaises(ValueError):
            self.validate('conversion', source)

    def test_consolidation_population_must_belong_to_producer_scope(self):
        source = downstream_source(self.f, 'elimination')
        source['entities'][0]['id'], source['entities'][1]['id'] = source['entities'][1]['id'], source['entities'][0]['id']
        with self.assertRaises(ValueError):
            self.validate('elimination', source)

    def test_receipt_economic_identity_cannot_be_free_annotation(self):
        basis = ReportingBasis(self.e)
        edge = self.f['edges'][('clean-ENTITY-US', 'translation')]
        # Declaration before consumption, retaining a current legal producer.
        consumer = self.f['nodes']['translation'].id
        self.e.versions.active.pop(consumer)
        with self.assertRaises(ValueError):
            basis.declare(edge, producer_layer='LEGAL_ENTITY', consumer_layer='TRANSLATION',
                framework='US_GAAP', currency='USD', semantic_metric='litigation_provision',
                economic_id='fabricated-unrelated-event', required_framework='US_GAAP',
                required_currency='USD', evidence=EVIDENCE)
            basis.receipt(edge)

    def test_receipt_semantic_identity_cannot_be_free_annotation(self):
        basis = ReportingBasis(self.e)
        edge = self.f['edges'][('clean-ENTITY-US', 'translation')]
        self.e.versions.active.pop(self.f['nodes']['translation'].id)
        with self.assertRaises(ValueError):
            basis.declare(edge, producer_layer='LEGAL_ENTITY', consumer_layer='TRANSLATION',
                framework='US_GAAP', currency='USD', semantic_metric='litigation_provision',
                economic_id='clean', required_framework='US_GAAP',
                required_currency='USD', evidence=EVIDENCE)
            basis.receipt(edge)

    def test_translation_transformation_economic_identity_is_bound(self):
        basis = ReportingBasis(self.e)
        source = self.e.versions.current(self.f['nodes']['clean-ENTITY-US'].id)
        target = self.e.versions.current(self.f['nodes']['translation'].id)
        with self.assertRaises(ValueError):
            basis.translation(source.version_id, target.version_id, 'fabricated-event',
                ('calculations', 'pairs', 0, 'a_functional'),
                ('translation', 'tb', 1, 'balance'),
                ('calculations', 'translation', 'translated_tb', 'ic loan'), EVIDENCE)

    def test_group_cannot_replace_owner_cta_with_balanced_offset(self):
        from orchestration.tests.stage3_fixtures import correct, rework, execute
        from additional_cases import certify
        rework(self.f, correct(self.f))
        source = downstream_source(self.f, 'elimination', True)
        # Preserve all translated TB keys, entity identity, exact receipts,
        # clean match, balanced source population and native reconciliation.
        # The translator certified CTA 16.36, not the substituted 20.
        source['entities'][1]['balances']['CTA'] = '20'
        source['entities'][1]['balances']['unqualified offset'] = '-3.64'
        source['statement_mapping']['unqualified offset'] = 'equity'
        source['cta_bridge'].update(translation='20', closing='20')
        source = certify('consolidation', source)
        with self.assertRaises(ValueError):
            execute(self.f, 'elimination', source)

    def test_translation_cannot_hide_as_legal_layer_to_relabel_currency(self):
        basis = ReportingBasis(self.e)
        edge = self.f['edges'][('translation', 'conversion')]
        self.e.versions.active.pop(self.f['nodes']['conversion'].id)
        with self.assertRaises(ValueError):
            basis.declare(edge, producer_layer='LEGAL_ENTITY', consumer_layer='FRAMEWORK_ADJUSTMENT',
                framework='US_GAAP', currency='USD', semantic_metric='translated_intercompany_balance',
                economic_id='clean', required_framework='US_GAAP', required_currency='USD', evidence=EVIDENCE)
            basis.receipt(edge)

    def test_conversion_counterparty_population_must_match_source_legal_scopes(self):
        from orchestration.tests.stage3_fixtures import execute
        from additional_cases import certify
        source = downstream_source(self.f, 'conversion')
        source['pairs'][0]['entity_a'] = 'ENTITY-UK'
        source = certify('intercompany-accounting', source)
        with self.assertRaises(ValueError):
            target = execute(self.f, 'conversion', source)
            translated = self.e.versions.current(self.f['nodes']['translation'].id)
            self.f['basis'].intercompany_conversion(translated.version_id, target.version_id, 'clean',
                ('calculations', 'translation', 'translated_tb', 'ic loan'), EVIDENCE)

    def test_conversion_other_legal_carrying_value_requires_exact_source(self):
        from orchestration.tests.stage3_fixtures import execute
        from additional_cases import certify
        source = downstream_source(self.f, 'conversion')
        source['pairs'][0].update(gl_b='180', rate_b='2')
        source = certify('intercompany-accounting', source)
        with self.assertRaises(ValueError):
            target = execute(self.f, 'conversion', source)
            translated = self.e.versions.current(self.f['nodes']['translation'].id)
            self.f['basis'].intercompany_conversion(translated.version_id, target.version_id, 'clean',
                ('calculations', 'translation', 'translated_tb', 'ic loan'), EVIDENCE)

    def test_exact_source_row_cannot_change_transaction_identity(self):
        side = sides(self.f, 'clean')[0]
        with self.assertRaises(ValueError):
            replace(side, economic_id='another-event').validate(self.e)

    def test_cross_period_cannot_be_clean_match(self):
        ss = sides(self.f, 'timing')
        net = IntercompanyNetwork(self.e, 'STAGE3-NETWORK')
        for side in ss:
            net.register(side)
        decision = MatchingDecision(ss[0].relationship_id, tuple(s.side_id for s in ss),
            'MATCHED', EVIDENCE, tuple(s.result_version for s in ss), 'independent QA',
            'Dates differ; arbitrary evidence cannot align dated periods', EVIDENCE)
        with self.assertRaises(ValueError):
            net.match(decision)

    def test_correction_stales_only_actual_consumers_and_old_receipts_fail(self):
        from orchestration.tests.stage3_fixtures import correct, rework
        before = {label: self.e.versions.current(n.id).version_id for label, n in self.f['nodes'].items()}
        edge = self.f['edges'][('clean-ENTITY-US', 'translation')]
        old_receipt = self.e.receipt(edge)
        plan = correct(self.f)
        affected = {'match-clean', 'translation', 'conversion', 'elimination', 'reporting', 'group'}
        self.assertEqual({self.e.graph.nodes[k].logical_id for k in plan['execution_order']}, affected)
        for label, version in before.items():
            if label not in affected | {'clean-ENTITY-US'}:
                self.assertEqual(self.e.versions.current(self.f['nodes'][label].id).version_id, version)
        with self.assertRaises(ValueError):
            self.e.versions.require_current(old_receipt['result_version'])
        rework(self.f, plan)
        for label in affected:
            version = self.e.versions.current(self.f['nodes'][label].id)
            self.assertNotEqual(version.version_id, before[label])
            self.e.versions.require_current(version.version_id)

    def test_business_cycle_does_not_create_execution_cycle(self):
        from orchestration.tests.stage3_fixtures import network
        net = network(self.f)
        self.assertTrue(net.has_business_cycle())
        self.assertFalse(net.record()['execution_edges_inferred'])
        self.e.graph.validate()
        self.assertEqual(len(self.e.graph.nodes), 17)

    def journal_inputs(self):
        from orchestration.tests.stage3_fixtures import correct, rework
        rework(self.f, correct(self.f))
        events = []
        for n in self.e.graph.nodes.values():
            version = self.e.versions.current(n.id)
            if n.selected_skill == 'foreign-currency':
                continue
            for index, journal in enumerate(version.payload().get('journal_entry_implications', [])):
                events.append(dict(economic_id=n.economic_id + '-' + str(index),
                    posting_scope=n.scope_id, period=n.period, period_id=n.period_id,
                    currency=n.functional_currency or n.presentation_currency,
                    result_version=version.version_id, primary=[dict(owner=n.id, index=index)],
                    witnesses=[], evidence='Independent synthetic gross journal attribution'))
        context = dict(entity='GROUP-EUR', framework='IFRS', jurisdiction='NL', currency='EUR',
            period_start='2026-10-01', reporting_period='2026-10-31',
            scopes=self.e.cases.scopes.record(), period_registry=self.e.periods.record())
        dispositions = [dict(translation_version=self.e.versions.current(self.f['nodes']['translation'].id).version_id,
            group_version=self.e.versions.current(self.f['nodes']['elimination'].id).version_id,
            source_path=['entities', 1, 'balances'], evidence=['Independent embedded translation review'])]
        return context, events, dispositions

    def test_exact_once_legal_and_group_with_embedded_translation(self):
        context, events, dispositions = self.journal_inputs()
        selected, ledger = self.f['basis'].current_journals(context, events, dispositions)
        self.assertEqual(len(selected), 3)
        self.assertEqual(len(ledger), 3)
        owners = {row['owner'] for row in selected}
        self.assertEqual(owners, {self.f['nodes']['clean-ENTITY-US'].id, self.f['nodes']['elimination'].id})
        self.assertNotIn(self.f['nodes']['translation'].id, owners)

    def test_economic_alias_cannot_duplicate_current_gross_journal(self):
        context, events, dispositions = self.journal_inputs()
        alias = copy.deepcopy(events[0])
        alias['economic_id'] = 'new-name-for-same-gross-lines'
        with self.assertRaises(ValueError):
            self.f['basis'].current_journals(context, events + [alias], dispositions)

    def test_embedded_translation_disposition_cannot_be_omitted_or_duplicated(self):
        context, events, dispositions = self.journal_inputs()
        for population in ([], dispositions + dispositions):
            with self.subTest(population=population), self.assertRaises(ValueError):
                self.f['basis'].current_journals(context, events, population)

    def test_translation_disposition_cannot_point_to_shadow_population(self):
        from orchestration.tests.stage3_fixtures import execute
        from additional_cases import certify
        context, events, dispositions = self.journal_inputs()
        group_node = self.f['nodes']['elimination']
        source = copy.deepcopy(self.e.sources[group_node.id])
        source['shadow_population'] = copy.deepcopy(source['entities'][1]['balances'])
        group = execute(self.f, 'elimination', certify('consolidation', source))
        for label in ('reporting', 'group'):
            execute(self.f, label, downstream_source(self.f, label, True))
        for event in events:
            if event['posting_scope'] == 'GROUP-EUR':
                event['result_version'] = group.version_id
        dispositions[0]['group_version'] = group.version_id
        dispositions[0]['source_path'] = ['shadow_population']
        with self.assertRaises(ValueError):
            self.f['basis'].current_journals(context, events, dispositions)

    def test_public_output_does_not_disclose_internal_receipt_annotations(self):
        from orchestration.tests.stage3_fixtures import ordinary_initial
        from orchestration.runtime import CAO
        f = ordinary_initial()
        output = CAO().public(f['case'])
        text = str(output)
        for forbidden in ('source_fingerprint', 'reviewer_signoff', 'stage3_input_bindings',
                          'Independent synthetic source', 'rate_population', 'result_version'):
            self.assertNotIn(forbidden, text)
        self.assertEqual(output['status'], 'partial')
        self.assertTrue(output['open_items'])

    def test_legal_owner_must_qualify_real_transaction_population(self):
        side = sides(self.f, 'clean')[0]
        node = self.f['nodes']['clean-ENTITY-US']
        # Metadata row is not part of the native IC calculation. Alter principal
        # metadata, preserving functional result and exact source-row hash.
        source = self.e.sources[node.id]
        source['intercompany_transactions'][0]['transaction_amount'] = '900000'
        from orchestration.versions import fingerprint
        row = source['intercompany_transactions'][0]
        from orchestration.tests.stage3_fixtures import execute
        from additional_cases import certify
        # Native certification accepts unknown orchestration metadata; a new
        # genuine current version therefore exposes the population disconnect.
        version = execute(self.f, 'clean-ENTITY-US', certify('intercompany-accounting', source))
        forged = replace(side, result_version=version.version_id,
            transaction_amount='900000', source_fingerprint=fingerprint(row))
        with self.assertRaises(ValueError):
            forged.validate(self.e)


if __name__ == '__main__':
    unittest.main()
