"""Independent final release attacks, written without implementation changes."""
import copy
import unittest
from dataclasses import replace

from orchestration.intake import Intake, FixturePlanner, DocumentBinding
from orchestration.tests.temporal_intake_fixtures import fixture, OBJECTIVE
from orchestration.tests.stage2_fixtures import build, initial, correction, restatement, subgroup
from orchestration.runtime import CAO
from cases import finalize
from orchestration.tests.intake_fixtures import cl
from orchestration.versions import Dependency
from orchestration.scopes import ScopeRegistry
from orchestration.periods import Period, PeriodRegistry


class ReleaseTemporalEvidenceAudit(unittest.TestCase):
    def document_case(self, source_index=0, calendar=None):
        sources, proposal, scope, pack = fixture()
        engine = Intake(FixturePlanner(proposal))
        prepared = engine.prepare(OBJECTIVE, sources, [], scope)
        self.assertTrue(prepared.validation['accepted'], prepared.validation)
        source = prepared._inventory.extractions[sources[source_index].id].source
        native = pack.request['facts']['customer_contract'][0]
        native['reviewed_temporal_document'] = dict(
            fingerprint=source['fingerprint'], metadata=source['metadata'])
        native = finalize('revenue-recognition', native)
        pack.request['facts']['customer_contract'][0] = native
        pack.scoped_packs[0].request['facts']['customer_contract'] = copy.deepcopy(native)
        binding = DocumentBinding(sources[source_index].id, 'revenue-recognition',
            ('reviewed_temporal_document',), native['scope_id'], native['period_id'],
            calendar or pack.scoped_packs[0].calendar_id)
        pack.documents = [binding]
        pack.scoped_packs[0].documents = [binding]
        return engine, prepared, pack

    def test_same_period_document_control_executes(self):
        engine, prepared, pack = self.document_case()
        self.assertEqual(engine.execute(prepared, pack).case.outcome, 'complete')

    def test_october_document_cannot_certify_september(self):
        engine, prepared, pack = self.document_case(source_index=1)
        with self.assertRaises(ValueError):
            engine.execute(prepared, pack)

    def test_document_binding_calendar_cannot_substitute(self):
        engine, prepared, pack = self.document_case(calendar='CALENDAR')
        with self.assertRaises(ValueError):
            engine.execute(prepared, pack)

    def test_same_scope_confirmation_questions_keep_both_periods(self):
        sources, proposal, scope, pack = fixture()
        for fact in proposal.facts:
            fact.confirmation_required = True
        prepared = Intake(FixturePlanner(proposal)).prepare(OBJECTIVE, sources, [], scope)
        self.assertTrue(prepared.validation['accepted'], prepared.validation)
        questions = [q for q in prepared.questions if q['attribute'] == 'recognised_revenue'
                     and q['kind'] == 'confirmation']
        self.assertEqual(len(questions), 2, 'Material questions from different Periods collapsed')
        self.assertEqual({q.get('period_id') for q in questions},
                         {f.dimensions['period_id'] for f in proposal.facts})

    def test_september_established_fact_does_not_answer_october_missing_fact(self):
        sources, proposal, scope, pack = fixture()
        october = proposal.facts[1].dimensions['period_id']
        proposal.facts[1].confirmation_required = True
        proposal.issues[1].value['required_fields'] = []
        proposal.missing_facts.append(cl(dict(attribute='recognised_revenue',
            owner='revenue-recognition', kind='blocking', scope_id='ENTITY-US', period_id=october)))
        prepared = Intake(FixturePlanner(proposal)).prepare(OBJECTIVE, sources, [], scope)
        self.assertTrue(prepared.validation['accepted'], prepared.validation)
        self.assertTrue(any(q['kind'] == 'blocking' and q['attribute'] == 'recognised_revenue'
                            and q.get('period_id') == october for q in prepared.questions))

    def test_ordinary_native_manifest_cannot_substitute_period_identity(self):
        sources, proposal, scope, pack = fixture()
        rows = pack.request['facts']['customer_contract']
        rows[1]['qualified_scope_sources'][0]['metadata']['period_id'] = rows[0]['period_id']
        rows[1] = finalize('revenue-recognition', rows[1])
        case = CAO().run(pack.request)
        self.assertNotEqual(case.outcome, 'complete')
        october = rows[1]['period_id']
        self.assertFalse(any(n['status'] == 'complete' and n['period_id'] == october
                             for n in case.workplan_nodes))

    def test_native_correction_cannot_bypass_manifest_period_qualification(self):
        f = initial(build())
        node = f['nodes']['US-SEP']
        _, _, _, pack = fixture()
        source = copy.deepcopy(f['sources'][node.id])
        source['qualified_scope_sources'] = copy.deepcopy(
            pack.request['facts']['customer_contract'][1]['qualified_scope_sources'])
        source = finalize(node.selected_skill, source)
        original = f['coordinator'].versions.current(node.id)
        with self.assertRaises(ValueError):
            CAO().correct(f['case'], node.id, source, 'Wrong-period source correction')
        self.assertEqual(f['coordinator'].versions.current(node.id), original)

    def test_ordinary_later_period_cannot_use_expired_scope(self):
        sources, proposal, scope, pack = fixture()
        for row in scope['scopes']:
            if row['scope_id'] == 'ENTITY-US':
                row['effective_to'] = '2026-09-30'
        pack.request['scope'] = scope
        case = CAO().run(pack.request)
        self.assertNotEqual(case.outcome, 'complete')
        self.assertFalse(any(n['status'] == 'complete' and n['period'][0] == '2026-10-01'
                             for n in case.workplan_nodes))

    def test_governed_plan_cannot_execute_inactive_scope(self):
        f = build()
        registry = f['coordinator'].cases.scopes
        rows = registry.record()
        for row in rows:
            if row['scope_id'] == 'ENTITY-US':
                row['status'] = 'INACTIVE'
        f['coordinator'].cases.scopes = ScopeRegistry(rows)
        with self.assertRaises((ValueError, AssertionError)):
            initial(f)


class ReleaseVersionAudit(unittest.TestCase):
    def test_low_level_native_rework_cannot_republish_old_ordinary_synthesis(self):
        _, _, _, pack = fixture()
        case = CAO().run(pack.request)
        self.assertEqual(case.outcome, 'complete')
        self.assertIn('800.00', str(CAO().public(case)))
        session = case.governance
        node = next(n for n in case.graph.nodes.values() if n.period[0] == '2026-09-01')
        source = copy.deepcopy(session.sources[node.id])
        source['obligations'][1]['progress'] = '0.75'
        source = finalize(node.selected_skill, source)
        session.execute(node.id, CAO().execute_versioned_owner, source,
                        'Low-level native correction independent audit')
        plan = session.rework_history[-1]
        session.reexecute(plan, {}, {})
        self.assertTrue(all(session.versions.state(key) == 'CURRENT'
                            for key in session.versions.active.values()))
        public = CAO().public(case)
        self.assertNotIn('800.00', str(public))
        self.assertEqual(public['status'], 'partial')

    def native_dependency_case(self):
        f = build()
        session = f['coordinator']
        producer = f['nodes']['US-SEP']
        consumer = f['nodes']['US-OCT']
        edge = Dependency(producer.id, consumer.id, producer.case_id, consumer.case_id,
            producer.scope_id, consumer.scope_id, producer.period_id, consumer.period_id,
            'OPENING', 'EXPLICIT_CROSS_CASE', ('calculations', 'period_revenue'),
            ('independently reviewed native temporal dependency',))
        session.add_dependency(edge)
        version = session.execute(producer.id, f['executors'][producer.id],
            f['sources'][producer.id], 'Native upstream independent audit')
        source = copy.deepcopy(f['sources'][consumer.id])
        source['imports'] = [dict(package=producer.selected_skill,
            case=f['sources'][producer.id], result=version.payload())]
        source['versioned_dependency_receipts'] = [session.receipt(edge.id)]
        return f, session, consumer, source

    def test_native_temporal_consumer_requires_current_reviewed_receipts(self):
        f, session, node, source = self.native_dependency_case()
        omitted = copy.deepcopy(source)
        omitted.pop('versioned_dependency_receipts')
        omitted = finalize(node.selected_skill, omitted)
        with self.assertRaises(ValueError):
            session.execute(node.id, f['executors'][node.id], omitted, 'Missing reviewed receipts')
        source = finalize(node.selected_skill, source)
        version = session.execute(node.id, f['executors'][node.id], source, 'Reviewed exact receipt control')
        self.assertEqual(version.payload()['status'], 'complete')

    def test_native_import_cannot_substitute_equal_metric_with_wrong_result_fingerprint(self):
        f, session, node, source = self.native_dependency_case()
        source['imports'][0]['result']['case_fingerprint'] = 'other-native-input-certification'
        source = finalize(node.selected_skill, source)
        with self.assertRaises(ValueError):
            session.execute(node.id, f['executors'][node.id], source, 'Imported envelope attack')

    def test_second_correction_before_rework_retains_all_pending_consumers(self):
        f = initial(build())
        first = correction(f)
        session = f['coordinator']
        node = f['nodes']['US-SEP']
        second = CAO().correct(f['case'], node.id, copy.deepcopy(f['sources'][node.id]),
                               'Second review before pending rework')
        self.assertEqual(second['execution_order'], first['execution_order'])
        self.assertEqual(set(second['affected_cases']), set(first['affected_cases']))
        with self.assertRaises(ValueError):
            CAO().selective_reexecute(f['case'], first)
        ledger = CAO().selective_reexecute(f['case'], second)
        self.assertEqual(len(ledger), 4)
        self.assertEqual(CAO().public(f['case'])['status'], 'complete')
        self.assertTrue(all(session.versions.state(key) == 'CURRENT'
                            for key in session.versions.active.values()))

    def test_equal_value_replacement_rejects_old_receipt(self):
        f = initial(build())
        session = f['coordinator']
        producer = f['nodes']['UK-SEP']
        edge = next(e for e in session.edges.values() if e.producer_node == producer.id)
        receipt = session.receipt(edge.id)
        old = session.versions.current(producer.id)
        plan = CAO().correct(f['case'], producer.id, copy.deepcopy(f['sources'][producer.id]),
                             'Independent equal-value reviewed replacement')
        self.assertEqual(session.versions.current(producer.id).payload(), old.payload())
        self.assertEqual(session.versions.state(old.version_id), 'SUPERSEDED')
        self.assertEqual(plan['execution_order'], [edge.consumer_node])
        with self.assertRaises(ValueError):
            session.validate_receipt(receipt, edge.consumer_node)

    def test_closed_downstream_blocks_selective_reexecution(self):
        f = initial(build())
        plan = correction(f)
        session = f['coordinator']
        opening = f['nodes']['US-OPEN']
        session.periods.close(opening.period_id)
        with self.assertRaises(ValueError):
            CAO().selective_reexecute(f['case'], plan)
        self.assertNotEqual(CAO().public(f['case'])['status'], 'complete')
        old = session.versions.current(opening.id, allow_stale=True)
        self.assertEqual(session.versions.state(old.version_id), 'STALE')

    def test_restatement_preserves_original_and_rejects_original_comparative_receipt(self):
        f = initial(build())
        session = f['coordinator']
        node = f['nodes']['UK-COMPARATIVE']
        edge = next(e for e in session.edges.values() if e.consumer_node == node.id)
        old_receipt = session.receipt(edge.id)
        original_prior = session.versions.current(edge.producer_node)
        original_comparative = session.versions.current(node.id)
        old_payload = original_comparative.payload()
        restatement(f)
        current = session.versions.current(node.id)
        self.assertEqual(current.predecessor, original_comparative.version_id)
        self.assertEqual(original_comparative.payload(), old_payload)
        self.assertEqual(original_prior.payload()['calculations']['period_revenue'], '800.00')
        self.assertEqual(current.payload()['observed_amount'], '900.00')
        self.assertTrue(current.payload()['restated'])
        self.assertFalse(current.payload()['accounting_authority'])
        with self.assertRaises(ValueError):
            session.validate_receipt(old_receipt, node.id)
        session.validate_receipt(session.receipt(edge.id), node.id)

    def test_subgroup_stales_and_retains_unaffected_entity_versions(self):
        f = subgroup()
        session = f['coordinator']
        node = f['nodes']['SUBGROUP']
        case = session.cases.get(node.case_id)
        original = session.versions.current(node.id)
        uk = session.versions.current(f['nodes']['UK-SEP'].id)
        edge = next(e for e in session.edges.values() if e.producer_node == node.id)
        old_receipt = session.receipt(edge.id)
        plan = correction(f)
        self.assertEqual(case.case_type, 'SUBGROUP_CASE')
        self.assertEqual(case.outcome, 'partial')
        self.assertEqual(session.versions.state(original.version_id), 'STALE')
        with self.assertRaises(ValueError):
            session.validate_receipt(old_receipt, edge.consumer_node)
        CAO().selective_reexecute(f['case'], plan)
        self.assertEqual(case.outcome, 'complete')
        self.assertEqual(session.versions.current(uk.node_id), uk)
        result = session.versions.current(node.id).payload()
        self.assertFalse(result['accounting_authority'])
        self.assertFalse(result.get('journal_entry_implications'))
        self.assertEqual(result['currency'], 'USD')

    def test_ordinary_correction_refresh_does_not_deliver_previous_amount(self):
        f = initial(build())
        plan = correction(f)
        delivered = CAO().public(f['case'])
        self.assertNotEqual(delivered['status'], 'complete')
        self.assertNotIn('800.00', str(delivered))
        CAO().selective_reexecute(f['case'], plan)
        delivered = CAO().public(f['case'])
        self.assertEqual(delivered['status'], 'complete')
        self.assertEqual(delivered['calculations'][0]['amount'], '900.00')
        for internal in ('version:', 'dependency:', 'fingerprint', 'SYNTHETIC_GOVERNED'):
            self.assertNotIn(internal, str(delivered))

    def test_reopened_authorization_cannot_expand_to_other_node(self):
        f = initial(build())
        session = f['coordinator']
        producer = f['nodes']['US-SEP']
        other = f['nodes']['US-REPORT']
        session.periods.close(producer.period_id)
        session.periods.reopen(producer.period_id, 'Limited correction',
            dict(status='APPROVED', evidence=['reviewed'], convention='SYNTHETIC_GOVERNED'),
            [producer.case_id], [producer.id])
        original = session.versions.current(other.id)
        with self.assertRaises(ValueError):
            CAO().correct(f['case'], other.id, f['sources'][other.id], 'Unauthorized work')
        self.assertEqual(session.versions.current(other.id), original)


class ReleaseJournalAudit(unittest.TestCase):
    def journal_case(self):
        # Import only the established fixture helper; assertions below are new.
        from orchestration.tests.test_stage2_independent import IndependentStage2
        audit = IndependentStage2()
        audit.setUp()
        context, events = audit.journal_inputs()
        return audit, context, events

    def test_valid_prior_period_journals_use_actual_scope_effective_interval(self):
        from orchestration.scoped_journals import allocate_scoped
        audit, context, events = self.journal_case()
        for row in context['scopes']:
            if row['scope_id'] == 'ENTITY-US':
                row['effective_to'] = '2026-09-30'
        node = audit.n['US-SEP']
        version = audit.e.versions.current(node.id)
        native = [dict(owner=node.selected_skill, node=node.id, source_scope=node.scope_id,
            posting_scope=node.scope_id, accounting_layer=node.scope_type,
            currency=node.functional_currency, period=node.period, period_id=node.period_id,
            result_version=version.version_id, journals=version.payload()['journal_entry_implications'])]
        exact_events = [event for event in events if event['result_version'] == version.version_id]
        selected, ledger = allocate_scoped(native, context, exact_events)
        self.assertEqual(len(selected), 6)
        self.assertEqual(len(ledger), 6)

    def test_economic_alias_cannot_count_same_gross_line_twice(self):
        audit, context, events = self.journal_case()
        alias = copy.deepcopy(events[0])
        alias['economic_id'] = 'independent-new-label-same-line'
        with self.assertRaises(ValueError):
            audit.e.current_journals(context, events + [alias])

    def test_replacement_version_cannot_be_assigned_to_another_owner_event(self):
        audit, context, events = self.journal_case()
        uk = audit.e.versions.current(audit.n['UK-SEP'].id)
        events[0]['result_version'] = uk.version_id
        with self.assertRaises(ValueError):
            audit.e.current_journals(context, events)

    def test_current_journals_after_restated_prior_exclude_original_economics(self):
        audit, context, events = self.journal_case()
        original = audit.e.versions.current(audit.n['UK-SEP'].id)
        restatement(audit.f)
        with self.assertRaises(ValueError):
            audit.e.current_journals(context, events)
        context, events = audit.journal_inputs()
        selected, ledger = audit.e.current_journals(context, events)
        uk = [j for j in selected if j['owner'] == original.node_id]
        self.assertEqual(len(selected), 18)
        self.assertEqual(len(ledger), 18)
        self.assertEqual(uk[0]['lines'][0]['amount'], '900.00')
        self.assertEqual(original.payload()['journal_entry_implications'][0][0]['amount'], '800.00')


class ReleasePeriodAliasAudit(unittest.TestCase):
    def test_fiscal_label_alias_cannot_create_second_actual_period(self):
        f = build()
        registry = f['coordinator'].periods
        period = f['periods']['US-FISCAL-SEP']
        alias = Period.create(period.calendar_id, period.start, period.end,
            period.fiscal_year, 'INDEPENDENT-LABEL-ALIAS', period.period_type,
            period.as_of, ('independently reviewed alias',))
        self.assertNotEqual(alias.period_id, period.period_id)
        with self.assertRaises(ValueError):
            PeriodRegistry(registry.calendars.values(), [period, alias])

    def test_as_of_alias_cannot_create_second_actual_period(self):
        f = build()
        registry = f['coordinator'].periods
        period = f['periods']['US-FISCAL-SEP']
        alias = Period.create(period.calendar_id, period.start, period.end,
            period.fiscal_year, period.fiscal_period, period.period_type,
            '2026-10-01', ('independently reviewed alias',))
        self.assertNotEqual(alias.period_id, period.period_id)
        with self.assertRaises(ValueError):
            PeriodRegistry(registry.calendars.values(), [period, alias])

    def test_cross_calendar_and_distinct_temporal_types_remain_independent(self):
        f = build()
        registry = f['coordinator'].periods
        us = f['periods']['US-FISCAL-SEP']
        calendar = f['periods']['CALENDAR-SEP']
        partial = Period.create(us.calendar_id, us.start, us.end, us.fiscal_year,
            'QUALIFIED-PARTIAL', 'PARTIAL_INCLUDED_PERIOD', us.as_of, ('reviewed inclusion',))
        result = PeriodRegistry(registry.calendars.values(), [us, calendar, partial])
        self.assertEqual(len(result.periods), 3)
        report = Period.create(us.calendar_id, us.end, us.end, us.fiscal_year,
            'AS-OF-REPORT', provenance=('reviewed report',))
        opening = Period.create(us.calendar_id, us.end, us.end, us.fiscal_year,
            'AS-OF-OPENING', 'OPENING', provenance=('reviewed opening',))
        result = PeriodRegistry(registry.calendars.values(), [report, opening])
        self.assertEqual(len(result.periods), 2)

    def test_ordinary_label_alias_cannot_duplicate_native_execution(self):
        _, _, scope, pack = fixture()
        native = pack.request['facts']['customer_contract'][0]
        record = scope['period_registry']
        period = next(row for row in record['periods'] if row['period_id'] == native['period_id'])
        alias = Period.create(period['calendar_id'], period['start'], period['end'],
            period['fiscal_year'], 'NATIVE-EXECUTION-ALIAS', period['period_type'],
            period['as_of'], ('reviewed alias attack',))
        record['periods'].append(dict(alias.record(), status='OPEN'))
        clone = copy.deepcopy(native)
        clone['period_id'] = alias.period_id
        clone['qualified_scope_sources'][0]['metadata']['period_id'] = alias.period_id
        clone = finalize('revenue-recognition', clone)
        pack.request['facts']['customer_contract'] = [native, clone]
        case = CAO().run(pack.request)
        self.assertNotEqual(case.outcome, 'complete')
        self.assertFalse(any(node['status'] == 'complete' for node in case.workplan_nodes))


if __name__ == '__main__':
    unittest.main()
