"""Independent full-population guard attacks; no closure bypass or fixture edits."""
import copy
import unittest

from orchestration.stage3 import validate_group_loan_population
from orchestration.tests import stage4_fixtures as fixture


class IndependentPopulationGuard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.control = fixture.initial()

    def reject_false_perimeter(self, entities):
        f = copy.deepcopy(self.control)
        node = f['nodes']['elimination']
        # Reproduces a reviewed full-close source attempting to redefine the
        # population to no legal economics. Other accounting fields are immaterial
        # to this contract-level regression, which calls the actual runtime guard.
        source = dict(entities=entities, group_population_coverage=dict(
            mode='ALL_CURRENT_LOAN_SIDES', required_legal_result_versions=[]))
        self.assertTrue(any(n.scope_type == 'LEGAL_ENTITY' and n.selected_skill ==
            'intercompany-accounting' for n in f['session'].graph.nodes.values()))
        with self.assertRaises(ValueError):
            validate_group_loan_population(f['session'], node, source, [])

    def test_full_population_cannot_erase_legal_perimeter(self):
        self.reject_false_perimeter([])

    def test_full_population_cannot_substitute_group_for_legal_perimeter(self):
        self.reject_false_perimeter([dict(id='GROUP-EUR', balances={})])

    def test_full_population_cannot_substitute_unknown_scope(self):
        self.reject_false_perimeter([dict(id='UNDECLARED-LEGAL-PERIMETER', balances={})])

    def test_full_population_cannot_omit_one_registered_legal_entity(self):
        f = copy.deepcopy(self.control)
        node = f['nodes']['elimination']
        from orchestration.stage3 import current_legal_loan_versions
        perimeter = {'ENTITY-NL', 'ENTITY-US'}
        source = dict(entities=[dict(id=key) for key in sorted(perimeter)],
            group_population_coverage=dict(mode='ALL_CURRENT_LOAN_SIDES',
                required_legal_result_versions=current_legal_loan_versions(f['session'],node,perimeter)))
        with self.assertRaisesRegex(ValueError, 'perimeter'):
            validate_group_loan_population(f['session'], node, source, [])

    def replacement(self, label='mismatch-ENTITY-NL'):
        f = copy.deepcopy(self.control)
        key = f['nodes'][label].id
        if label == 'mismatch-ENTITY-NL':
            supplied = fixture.legal_source(f, 'mismatch', 'ENTITY-NL', True)
        else:
            supplied = fixture.source(f, label)
        engine, prepared, pack, raw = fixture.replacement_intake(f, key, supplied)
        return f, key, engine, prepared, pack, raw

    def qualify(self, values):
        from orchestration.intake.governed import qualify_replacement
        f, key, engine, prepared, pack, raw = values
        return qualify_replacement(engine, prepared, pack, f['case'], key)

    def test_fresh_replacement_preserves_original_execution(self):
        values = self.replacement()
        f, key, engine, prepared, pack, raw = values
        original = f['session'].versions.current(key)
        qualified = self.qualify(values)
        self.assertEqual(f['session'].versions.current(key).version_id, original.version_id)
        self.assertEqual(qualified['pairs'][0]['gl_b'], '10')
        self.assertTrue(all(r.metadata['provenance'].startswith('Fresh separately reviewed') for r in raw))

    def test_replacement_rejects_unsealed_accounting_mutation(self):
        values = self.replacement()
        pack = values[4]
        source = pack.request['governed_plan']['sources'][values[1]]
        source['pairs'][0]['gl_b'] = '9'
        pack.scoped_packs[0].request['source'] = copy.deepcopy(source)
        with self.assertRaises(ValueError):
            self.qualify(values)

    def test_replacement_rejects_different_retained_case_identity(self):
        values = self.replacement()
        values[4].request['governed_plan']['root_case'] = 'sibling-case'
        with self.assertRaisesRegex(ValueError, 'Case'):
            self.qualify(values)

    def test_replacement_rejects_changed_execution_identity(self):
        values = self.replacement()
        values[4].request['governed_plan']['nodes'][0]['logical_id'] = 'another-execution'
        with self.assertRaises(ValueError):
            self.qualify(values)

    def test_replacement_rejects_omitted_snapshot_manifest(self):
        values = self.replacement()
        pack = values[4]
        source = pack.request['governed_plan']['sources'][values[1]]
        source['source_population'].remove(source['qualified_input_snapshot']['source_id'])
        pack.scoped_packs[0].request['source'] = copy.deepcopy(source)
        with self.assertRaises(ValueError):
            self.qualify(values)

    def test_replacement_rejects_sealed_obsolete_matching_receipt(self):
        f = copy.deepcopy(self.control)
        key = f['nodes']['match-clean'].id
        supplied = fixture.source(f, 'match-clean')
        supplied['versioned_dependency_receipts'][0]['result_version'] = 'obsolete-version'
        engine, prepared, pack, raw = fixture.replacement_intake(f, key, supplied)
        with self.assertRaisesRegex(ValueError, 'obsolete'):
            self.qualify((f, key, engine, prepared, pack, raw))

    def test_replacement_rejects_removed_incoming_dependency(self):
        values = self.replacement('match-clean')
        values[4].request['governed_plan']['dependencies'].pop()
        with self.assertRaisesRegex(ValueError, 'dependency'):
            self.qualify(values)

    def temporal_source(self):
        f = copy.deepcopy(self.control)
        label = 'timing-effective-ENTITY-NL'
        return f, f['nodes'][label].id, fixture.source(f,label)

    def test_effective_interval_is_consumed_by_native_execution(self):
        f, key, source = self.temporal_source()
        version=f['session'].versions.current(key)
        prior=f['session'].versions.current(f['nodes']['timing-ENTITY-NL'].id)
        self.assertEqual(version.payload()['calculations']['pairs'][0]['a_functional'],'30.00')
        self.assertIn(prior.version_id,[v for edge,v in version.dependency_bindings])
        self.assertEqual(source['governed_effective_interval']['included_period'],f['nodes']['timing-effective-ENTITY-NL'].period_id)
        self.assertNotEqual(f['nodes']['timing-current-ENTITY-NL'].period_id, f['nodes']['timing-ENTITY-NL'].period_id)

    def test_effective_interval_wrong_owner_rejects_ordinary_correction(self):
        from additional_cases import certify
        from orchestration.runtime import CAO
        f,key,source=self.temporal_source()
        source['governed_effective_interval']['owner']='foreign-currency'
        source=certify('intercompany-accounting',source)
        with self.assertRaises(ValueError):
            CAO().correct(f['case'],key,source,'Independent wrong owner interval attack')

    def test_effective_interval_wrong_scope_rejects_ordinary_correction(self):
        from additional_cases import certify
        from orchestration.runtime import CAO
        f,key,source=self.temporal_source()
        source['governed_effective_interval']['scope_id']='ENTITY-UK'
        source=certify('intercompany-accounting',source)
        with self.assertRaises(ValueError):
            CAO().correct(f['case'],key,source,'Independent wrong Scope interval attack')

    def test_effective_interval_wrong_included_period_rejects_ordinary_correction(self):
        from additional_cases import certify
        from orchestration.runtime import CAO
        f,key,source=self.temporal_source()
        source['governed_effective_interval']['included_period']=f['periods']['CALENDAR-OCT'].period_id
        source=certify('intercompany-accounting',source)
        with self.assertRaises(ValueError):
            CAO().correct(f['case'],key,source,'Independent wrong Period interval attack')

    def test_prior_loan_correction_invalidates_exact_temporal_consumers(self):
        from orchestration.runtime import CAO
        f=copy.deepcopy(self.control)
        e=f['session'];key=f['nodes']['timing-ENTITY-NL'].id
        source=fixture.legal_source(f,'timing','ENTITY-NL')
        # Equal-value replacement still changes source lineage; prior temporal
        # consumers must refresh actual consumed versions rather than values.
        source['independent_reconfirmation']='Fresh separately reviewed September reconfirmation'
        from additional_cases import certify
        source=certify('intercompany-accounting',source)
        plan=CAO().correct(f['case'],key,source,'Independent prior source correction')
        direct={f['nodes'][label].id for label in ('match-timing','nl-opening','nl-comparative','timing-current-ENTITY-NL','timing-effective-ENTITY-NL')}
        self.assertEqual(set(plan['direct']),direct)
        self.assertEqual(set(plan['transitive']),{f['nodes']['group'].id})
        self.assertEqual(set(plan['unaffected']),set(e.graph.nodes)-direct-{key,f['nodes']['group'].id})
        for label in ('clean-ENTITY-US','fx-ENTITY-UK','mismatch-ENTITY-NL'):
            version=e.versions.current(f['nodes'][label].id)
            self.assertEqual(e.versions.require_current(version.version_id).version_id,version.version_id)
