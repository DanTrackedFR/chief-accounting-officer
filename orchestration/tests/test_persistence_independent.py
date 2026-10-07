"""Independent reconstruction/negative QA of the native governed checkpoint."""
import copy
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from orchestration.tests import stage2_fixtures as native
from orchestration.runtime import CAO
from orchestration.persistence import SQLiteStore, snapshot, restore, IntegrityError, RevisionConflict
from orchestration.persistence.codec import dumps, loads

COMPANY = 'company:independent-persistence-review'
CONTEXT = [dict(id='context:independent-profile', attribute='reporting_currency', value='EUR',
                status='DOCUMENTED', scope=dict(entities=['GROUP-EUR']), effective_from='2026-01-01',
                provenance=['synthetic independent test'])]


def governed(partial=True):
    f = native.initial(native.build())
    f['coordinator'].context['company_id'] = COMPANY
    f['coordinator'].context['company_context'] = copy.deepcopy(CONTEXT)
    if partial:
        native.correction(f)
    return f['case']


class IndependentGovernance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = governed()
        cls.doc = snapshot(cls.original, COMPANY, CONTEXT)
        cls.closed = snapshot(governed(False), COMPANY, CONTEXT)

    def reject(self, doc):
        with self.assertRaises(IntegrityError):
            restore(doc, COMPANY, doc['root_case'])

    def test_restoration_never_executes_accounting_or_closes_case(self):
        with patch.object(CAO, 'execute_versioned_owner', side_effect=AssertionError('accounting rerun')), \
             patch.object(CAO, 'run', side_effect=AssertionError('Case rerun')):
            a = restore(copy.deepcopy(self.doc), COMPANY, self.doc['root_case'])
            b = restore(copy.deepcopy(self.doc), COMPANY, self.doc['root_case'])
        self.assertIsNot(a.governance, b.governance)
        self.assertEqual(dumps(snapshot(a, COMPANY, CONTEXT)), dumps(self.doc))
        self.assertEqual(dumps(snapshot(b, COMPANY, CONTEXT)), dumps(self.doc))
        self.assertEqual((a.status, a.outcome), ('IN_PROGRESS', 'partial'))

    def test_case_type_substitution_is_rejected_not_normalized(self):
        d = copy.deepcopy(self.closed)
        next(c for c in d['cases'] if c['id'] == d['root_case'])['case_type'] = 'ENTITY_CASE'
        self.reject(d)

    def test_context_population_cannot_diverge_from_runtime_context(self):
        d = copy.deepcopy(self.doc)
        d['company_context'] = []
        self.reject(d)

    def test_context_company_identity_cannot_diverge(self):
        d = copy.deepcopy(self.doc)
        d['session']['context']['company_id'] = 'company:other'
        self.reject(d)

    def test_missing_historical_typed_receipt_is_rejected(self):
        d = copy.deepcopy(self.doc)
        self.assertTrue(d['receipts'])
        d['receipts'].pop()
        self.reject(d)

    def test_duplicate_historical_typed_receipt_is_rejected(self):
        d = copy.deepcopy(self.doc)
        d['receipts'].append(copy.deepcopy(d['receipts'][0]))
        self.reject(d)

    def test_all_historical_receipts_stay_disqualified(self):
        e = restore(copy.deepcopy(self.doc), COMPANY, self.doc['root_case']).governance
        historical = [r for r in e.receipts if e.versions.states[r['result_version']] != 'CURRENT']
        self.assertTrue(historical)
        for receipt in historical:
            with self.subTest(version=receipt['result_version']):
                with self.assertRaises(ValueError):
                    e.validate_receipt(receipt, receipt['consumer_node'])

    def test_private_checkpoint_not_public_output(self):
        c = restore(copy.deepcopy(self.closed), COMPANY, self.closed['root_case'])
        from interfaces.public_output import ROUTES
        for route in ROUTES:
            answer = dumps(CAO().public(c, route))
            for secret in ('result_version', 'dependency_id', 'source_fingerprint', 'governance_history', 'reviewer_signoff'):
                self.assertNotIn(secret, answer)

    def test_rework_history_missing_upstream_version_is_rejected(self):
        d = copy.deepcopy(self.doc)
        d['rework_history'][0]['causes'][0]['upstream_version'] = 'version:absent'
        self.reject(d)

    def test_graph_invalidation_history_missing_node_is_rejected(self):
        d = copy.deepcopy(self.doc)
        d['graph_history'][0]['node'] = 'exec:absent'
        self.reject(d)

    def test_legacy_stale_execution_label_remains_inert(self):
        d = copy.deepcopy(self.doc)
        node = next(n for n in d['nodes'] if n['id'] in d['active'] and d['states'][d['active'][n['id']]] == 'STALE')
        node['execution_receipt']['currentness'] = 'CURRENT'
        c = restore(d, COMPANY, d['root_case'])
        v = c.governance.versions.active[node['id']]
        self.assertEqual(c.governance.versions.states[v], 'STALE')
        with self.assertRaises(ValueError): c.governance.versions.require_current(v)
        self.assertEqual((c.status, c.outcome), ('IN_PROGRESS', 'partial'))

    def test_complete_node_requires_payload(self):
        d = copy.deepcopy(self.closed)
        next(n for n in d['nodes'] if n['status'] == 'complete')['result'] = None
        self.reject(d)

    def test_legacy_native_manufacturing_exact_roundtrip(self):
        from orchestration.tests.fixtures import manufacturing
        original = CAO().run(manufacturing())
        company = 'company:independent-legacy-manufacturing'
        d = snapshot(original, company, [])
        self.assertTrue(any('period_id' not in source for source in d['source_snapshots'].values()))
        with patch.object(CAO, 'execute_versioned_owner', side_effect=AssertionError('accounting rerun')):
            c = restore(d, company, original.id)
        self.assertEqual(dumps(snapshot(c, company, [])), dumps(d))
        self.assertEqual(CAO().public(c), CAO().public(original))

    def test_legacy_intake_missing_archive_rejected(self):
        from orchestration.tests.intake_fixtures import ap_control
        _, intake = ap_control()
        company = 'company:independent-legacy-intake'
        d = snapshot(intake.case, company, [])
        self.assertTrue(d['session']['evidence_bundles'])
        d['session']['evidence_bundles'] = {}
        with self.assertRaises(IntegrityError): restore(d, company, intake.case.id)

    def test_public_calculation_provenance_population_is_checked(self):
        from orchestration.tests.fixtures import manufacturing
        original = CAO().run(manufacturing())
        d = snapshot(original, COMPANY, [])
        order = d['case_private'][d['root_case']]['_public_calculation_order']
        self.assertTrue(order and order[0])
        order[0].pop()
        self.reject(d)

    def test_currentness_cannot_be_rewritten_even_for_equal_payload(self):
        d = copy.deepcopy(self.doc)
        historical = next(k for k, v in d['states'].items() if v == 'SUPERSEDED')
        d['states'][historical] = 'CURRENT'
        self.reject(d)

    def test_temporal_type_relabel_without_exact_identity_fails(self):
        d = copy.deepcopy(self.doc)
        edge = next(v for v in d['dependencies'].values() if v['dependency_type'] == 'OPENING')
        edge['dependency_type'] = 'COMPARATIVE'
        self.reject(d)

    def test_same_display_names_do_not_merge_entities(self):
        d = copy.deepcopy(self.doc)
        before = {s['scope_id'] for s in d['scopes']}
        for scope in d['scopes']:
            scope['display_name'] = 'Identical name'
        c = restore(d, COMPANY, d['root_case'])
        self.assertEqual({s['scope_id'] for s in c.governance.cases.scopes.record()}, before)

    def test_historical_source_payload_is_separate_from_latest_source(self):
        d = copy.deepcopy(self.doc)
        old = next(k for k, state in d['states'].items() if state == 'SUPERSEDED')
        source = d['source_snapshots'][old]
        self.assertNotEqual(source, d['session']['sources'][d['versions'][old]['node_id']])
        source['evidence'] = ['tampered historical payload']
        self.reject(d)

    def test_false_closed_case_missing_observer_is_rejected(self):
        d = copy.deepcopy(self.closed)
        next(c for c in d['cases'] if c['id'] == d['root_case'])['observer_ran'] = False
        self.reject(d)

    def test_case_history_cannot_skip_challenge(self):
        d = copy.deepcopy(self.closed)
        next(c for c in d['cases'] if c['id'] == d['root_case'])['transitions'].remove('CHALLENGE')
        self.reject(d)


class IndependentSQLite(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.root = governed()

    def test_database_trigger_abort_rolls_back_real_partial_insert(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'case.db'
            with SQLiteStore(path) as store:
                store.save(self.root, COMPANY, CONTEXT, 0)
                store.connection.execute("CREATE TRIGGER reject_second BEFORE INSERT ON objects WHEN NEW.revision=2 AND NEW.kind='version' BEGIN SELECT RAISE(ABORT,'injected failure'); END")
                with self.assertRaises(ValueError):
                    store.save(self.root, COMPANY, CONTEXT, 1)
                self.assertEqual(store.connection.execute('SELECT count(*) FROM checkpoints').fetchone()[0], 1)
                self.assertEqual(store.connection.execute('SELECT count(*) FROM objects WHERE revision=2').fetchone()[0], 0)
                self.assertEqual(store.load(COMPANY, self.root.id)[1], 1)

    def test_interleaved_independent_connections_reject_obsolete_writer(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'case.db'
            with SQLiteStore(path) as a, SQLiteStore(path) as b:
                a.save(self.root, COMPANY, CONTEXT, 0)
                original = b.load(COMPANY, self.root.id)
                a.save(self.root, COMPANY, CONTEXT, 1)
                with self.assertRaises(RevisionConflict):
                    b.save(original[0], COMPANY, original[2], original[1])
                self.assertEqual(b.load(COMPANY, self.root.id)[1], 2)

    def test_noncanonical_and_unknown_value_types_fail_closed(self):
        for payload in ('{"x":1,"x":1}', '{"x":NaN}', '{"x":{"$type":"execute","value":"anything"}}'):
            with self.subTest(payload=payload), self.assertRaises(IntegrityError): loads(payload)

    def test_malformed_schema_does_not_initialize_over_existing_data(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'case.db'
            db = sqlite3.connect(path)
            db.execute('CREATE TABLE existing(value TEXT)')
            db.execute("INSERT INTO existing VALUES('keep')")
            db.commit(); db.close()
            with self.assertRaises(IntegrityError): SQLiteStore(path)
            db = sqlite3.connect(path)
            self.assertEqual(db.execute('SELECT value FROM existing').fetchone()[0], 'keep')
            self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0], 0)
            db.close()

if __name__ == '__main__': unittest.main()
