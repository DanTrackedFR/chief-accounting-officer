"""Independent adversarial Profile 1.2 QA; synthetic data, never original uploads.

Only context text is reused from existing tests. Source rows, amounts, assertions
and adverse mutations below are independently authored. No reviewer fixture is
created or refreshed for the presumed-source path.
"""
import copy
import hashlib
import http.client
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

from hosted_cao.service import Service, Server, Error
from local_cao.adapter import ExecutionInterface
from local_cao.tests.test_authored import context
from orchestration.runtime import CAO
from orchestration.cases import case_identity
from orchestration.periods import compatibility_period
from local_cao.context import scope, parse

ROOT = Path(__file__).resolve().parents[2]
COMPANY = 'synthetic-demo-001'
MODE = 'prepared_unreviewed'
PROFILE = 'presumed_user_provided'
TOKEN = 'source-assurance-independent-http-' + 'r' * 32
USER = 'private-attesting-user-independent-QA'
SOURCE_HASH = hashlib.sha256(b'independently generated synthetic source').hexdigest()
FAMILY = {'fixed-assets': 'machinery', 'accounts-payable': 'supplier_cost'}


def synthetic_case(package='fixed-assets', count=None):
    """Independently generated scenario, not the customer's original register."""
    case = dict(case_id='synthetic-source-accounting-case', entity='ENTITY-DEMO',
                framework='IFRS', jurisdiction='NL', entity_type='for_profit',
                period_start='2026-01-01', reporting_period='2026-12-31',
                functional_currency='EUR', assumptions=[],
                source=dict(id='synthetic-upload-independent-QA', version='1', hash=SOURCE_HASH),
                source_attestation=dict(authenticated_user_reference=USER,
                    timestamp='2026-11-02T09:00:00+01:00', statement_version='company-records-v1',
                    represents_company_records=True))
    policy = dict(framework='IFRS', entity='ENTITY-DEMO', effective_from='2026-01-01',
                  effective_to='2026-12-31', policy_version='synthetic-policy-v1')
    if package == 'fixed-assets':
        case['class_assumptions'] = {'machinery': dict(policy, remaining_life='10', residual='0',
                                                     method='straight_line', scope='ordinary_ppe')}
        case['assets'] = [dict(id='FA-'+str(i), **{'class': 'machinery'},
                             opening_cost=str(10000+i*1000), opening_accumulated='0', ready_date='2025-01-01')
                          for i in range(1, (count or 27)+1)]
    else:
        case['class_assumptions'] = {'services': dict(policy, account='administrative expense',
                                                     recognition_basis='services_received')}
        case['invoices'] = [dict(id='AP-'+str(i), **{'class': 'services'}, supplier='Supplier '+str(i),
                                invoice_number='INV-'+str(i), amount=str(100+i*10),
                                invoice_date='2026-06-15', received_date='2026-06-14')
                            for i in range(1, (count or 10)+1)]
    return case


def supplied(package='fixed-assets', case=None):
    return {'facts': {FAMILY[package]: synthetic_case(package) if case is None else case}}


class IndependentPresumedEngineeringQA(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workspace = self.root/'company'; self.workspace.mkdir()
        (self.workspace/'company-context.md').write_text(context())
        self.companies = {COMPANY: self.workspace}
        self.credentials = [dict(caller_id='independent-test-client', token=TOKEN, companies=[COMPANY])]
        self.service = self.new_service()
        self.server = Server(('127.0.0.1', 0), self.service)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()
        self.addCleanup(self.close)
        self.assertTrue(self.call('initialize')[1]['ok'])

    def new_service(self, prepared=True, presumed=True):
        return Service(self.root/'jobs', self.companies, self.credentials,
                       allow_prepared_unreviewed=prepared, allow_presumed_user_sources=presumed)

    def close(self):
        self.server.shutdown(); self.server.server_close(); self.thread.join(); self.service.close()

    def envelope(self, operation, **fields):
        return dict(contract_version='1.0', company_id=COMPANY, operation=operation, **fields)

    def http(self, path, body=None, **headers):
        connection = http.client.HTTPConnection(*self.server.server_address, timeout=60)
        connection.request('GET' if body is None else 'POST', path,
            None if body is None else json.dumps(body),
            {'Authorization': 'Bearer '+TOKEN, 'X-CAO-Company': COMPANY,
             'Content-Type': 'application/json', **headers})
        response = connection.getresponse()
        result = response.status, json.loads(response.read()); connection.close()
        return result

    def call(self, operation, **fields):
        return self.http('/v1/operations', self.envelope(operation, **fields))

    def start(self, package='fixed-assets', rid='presumed', **fields):
        fields.setdefault('review_mode', MODE); fields.setdefault('source_assurance', PROFILE)
        status, result = self.call('start', request_id=rid, objective='Calculate supported accounting',
                                  target_family=FAMILY[package], **fields)
        self.assertEqual(status, 200, result); self.assertTrue(result['ok'], result)
        return result['case_id']

    def stage(self, package='fixed-assets', rid='presumed', case=None):
        cid = self.start(package, rid)
        status, result = self.call('submit', case_id=cid, evidence=supplied(package, case))
        self.assertEqual(status, 200, result); self.assertTrue(result['ok'], result)
        return cid

    def job(self, cid, key='presumed-job', **fields):
        return self.http('/v1/jobs', self.envelope('execute', case_id=cid, **fields),
                         **{'Idempotency-Key': key})

    def complete(self, package='fixed-assets', rid='presumed', case=None):
        cid = self.stage(package, rid, case)
        status, job = self.job(cid, rid)
        self.assertEqual(status, 202, job); self.assertTrue(self.service.run_one())
        status, done = self.http('/v1/jobs/'+job['id'])
        self.assertEqual(status, 200, done); self.assertEqual(done['state'], 'SUCCEEDED', done)
        accounting = done['accounting']; self.assertTrue(accounting['ok'], accounting)
        self.assertTrue(accounting['durable'], accounting)
        self.assertIn(accounting['execution_state'], ('partial', 'blocked'), accounting)
        return cid, done

    def assert_amount(self, public, label, expected):
        from decimal import Decimal
        amounts = {row['label']: Decimal(row['amount']) for row in public['calculations']}
        self.assertEqual(amounts[label], Decimal(expected), public)

    def native(self, cid):
        with ExecutionInterface(self.workspace)._store() as store:
            case, _, _ = store.load(COMPANY, cid)
        results = [n.result for n in case.graph.nodes.values() if n.result and n.result.get('source_assurance') == PROFILE]
        self.assertEqual(len(results), 1)
        return case, results[0]

    def test_real_http_27_machinery_rows_and_10_invoices(self):
        for package, label, expected in [('fixed-assets', 'depreciation', '64800'),
                                          ('accounts-payable', 'invoices', '1550')]:
            with self.subTest(package=package):
                _, job = self.complete(package, package)
                public = job['accounting']['public_result']
                self.assert_amount(public, label, expected)
                self.assertEqual(job['accounting']['execution_state'], 'partial')
                self.assertEqual(public['accounting_determination'], 'SUPPORTED')
                self.assertEqual(public['review_provenance'], 'SYSTEM_PREPARED')
                self.assertEqual(public['source_provenance'], 'USER_PROVIDED_SOURCES')
                self.assertEqual(public['anomaly_report']['population_status'], 'SUPPLIED_FILE_BOUNDED')
                self.assertIn('No policy elections were assumed.', public['guidance'])
                self.assertFalse(public.get('journals'))

    def test_default_off_and_dependent_exact_boolean_switches(self):
        request = self.envelope('start', request_id='off', objective='Calculate supported accounting',
                                target_family='machinery', review_mode=MODE, source_assurance=PROFILE)
        self.assertFalse(ExecutionInterface(self.workspace, allow_prepared_unreviewed=True).call(request)['ok'])
        for value in (1, 0, 'true', None, [], {}):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    ExecutionInterface(self.workspace, allow_prepared_unreviewed=True, allow_presumed_user_sources=value)
                with self.assertRaises(ValueError): self.new_service(True, value)
                with self.assertRaises(ValueError): CAO(allow_prepared_unreviewed=True, allow_presumed_user_sources=value)
        for construct in (lambda: ExecutionInterface(self.workspace, allow_presumed_user_sources=True),
                          lambda: self.new_service(False, True), lambda: CAO(allow_presumed_user_sources=True)):
            with self.assertRaises(ValueError): construct()

    def test_no_implicit_profile_upgrade_from_row(self):
        status, started = self.call('start', request_id='profile11', objective='Calculate supported accounting',
                                    target_family='machinery', review_mode=MODE)
        self.assertEqual(status, 200, started)
        evidence = supplied(); evidence['facts']['machinery']['source_assurance'] = PROFILE
        status, result = self.call('submit', case_id=started['case_id'], evidence=evidence)
        self.assertFalse(result['ok'], result)

    def test_formal_and_profile11_identity_unchanged_and_profile12_disjoint(self):
        for order in ('presumed-first', 'historical-first'):
            rid = order
            config = parse(context()); s = scope(config); p = compatibility_period(s)
            expected = case_identity(s['entity'], p.period_id, 'Calculate supported accounting', rid+'-formal')
            def old():
                _, formal = self.call('start', request_id=rid+'-formal', objective='Calculate supported accounting', target_family='machinery')
                _, previous = self.call('start', request_id=rid+'-old', objective='Calculate supported accounting', target_family='machinery', review_mode=MODE)
                self.assertTrue(formal['ok']); self.assertTrue(previous['ok'])
                self.assertEqual(formal['case_id'], expected)
                previous_cycle = json.dumps([rid+'-old', MODE], sort_keys=True, ensure_ascii=False, separators=(',', ':'))
                self.assertEqual(previous['case_id'], case_identity(s['entity'], p.period_id, 'Calculate supported accounting', previous_cycle))
                return formal['case_id'], previous['case_id']
            if order == 'presumed-first':
                new = self.start(rid=rid); formal, previous = old()
            else:
                formal, previous = old(); new = self.start(rid=rid)
            self.assertEqual(len({new, formal, previous}), 3)

    def test_same_request_id_profile_change_cannot_rebind(self):
        self.start(rid='immutable-profile')
        status, result = self.call('start', request_id='immutable-profile', objective='Calculate supported accounting',
                                  target_family='machinery', review_mode=MODE)
        self.assertFalse(result['ok'], result)

    def test_profile_selection_requires_prepared_mode_and_supported_family(self):
        for mode, family in [('formal', 'machinery'), (MODE, 'customer_contract')]:
            status, result = self.call('start', request_id=family, objective='Calculate supported accounting',
                                      target_family=family, review_mode=mode, source_assurance=PROFILE)
            self.assertFalse(result.get('ok'), (status, result))

    def test_disabled_host_rejects_omitted_assurance_on_existing_case(self):
        cid = self.stage()
        api = ExecutionInterface(self.workspace, allow_prepared_unreviewed=True)
        for op in ('submit', 'status', 'execute', 'result', 'resume'):
            fields = dict(case_id=cid)
            if op == 'submit': fields['evidence'] = supplied()
            self.assertFalse(api.call(self.envelope(op, **fields))['ok'], op)

    def test_wire_and_row_mode_assurance_package_substitution_reject(self):
        cid = self.start()
        for fields in ({'review_mode': 'formal'}, {'source_assurance': 'unqualified'}):
            status, result = self.job(cid, key='swap', **fields)
            self.assertNotEqual(status, 202, result)
        for field, value in [('review_mode', 'formal'), ('source_assurance', 'other'), ('package', 'revenue-recognition')]:
            case = synthetic_case(); case[field] = value
            _, result = self.call('submit', case_id=cid, evidence=supplied(case=case))
            self.assertFalse(result['ok'], field)

    def test_review_injection_rejects_wire_and_staged_json(self):
        for i, field in enumerate(('knowledge_review', 'applicability_review', 'reviewer_signoff')):
            case = synthetic_case(); case['assets'][0][field] = {'reviewer': 'invented reviewer'}
            cid = self.start(rid='review-'+str(i))
            _, direct = self.call('submit', case_id=cid, evidence=supplied(case=case))
            self.assertFalse(direct['ok'])
            folder = self.workspace/'staged'; folder.mkdir(exist_ok=True)
            (folder/'injected.json').write_text(json.dumps(supplied(case=case)))
            _, staged = self.call('submit', case_id=cid, staged_file_id='injected')
            self.assertFalse(staged['ok'])

    def test_extra_owners_imports_and_journal_authority_reject(self):
        cid = self.start()
        values = []
        e = supplied(); e['facts']['customer_contract'] = {'obligations': ['invented']}; values.append(e)
        e = supplied(); e['facts']['machinery']['imports'] = []; values.append(e)
        e = supplied(); e['journal_pack_review'] = {'reviewer': 'invented'}; values.append(e)
        for e in values:
            _, result = self.call('submit', case_id=cid, evidence=e)
            self.assertFalse(result['ok'], result)

    def test_source_case_missing_reports_specific_field(self):
        cid = self.start(); case = synthetic_case(); case.pop('case_id')
        status, result = self.call('submit', case_id=cid, evidence=supplied(case=case))
        self.assertEqual(status, 422, result); self.assertEqual(result['error']['code'], 'invalid_request')
        fields = [r['field_path'] for r in result['error']['requirements']]
        self.assertIn('evidence.facts.machinery.case_id', fields)

    def test_submission_once_and_idempotent_job_retry(self):
        cid = self.stage(); first = self.job(cid)
        self.assertEqual(first[0], 202); self.assertEqual(self.job(cid)[1]['id'], first[1]['id'])
        other = self.stage('accounts-payable', 'other')
        self.assertEqual(self.job(other)[0], 409)
        self.assertTrue(self.service.run_one())
        done = self.http('/v1/jobs/'+first[1]['id'])[1]
        self.assertEqual(done['state'], 'SUCCEEDED')
        with patch.object(CAO, 'run', side_effect=AssertionError('owner replay')):
            again = self.job(cid)
            self.assertEqual(again[1]['accounting'], done['accounting'])

    def test_restart_recovers_both_jobs_without_owner_execution(self):
        jobs = [self.complete(p, p)[1] for p in FAMILY]
        restarted = self.new_service(); self.addCleanup(restarted.close)
        self.server.service = restarted
        with patch.object(CAO, 'run', side_effect=AssertionError('owner replay after restart')):
            for before in jobs:
                after = self.http('/v1/jobs/'+before['id'])[1]
                self.assertEqual(after['accounting']['public_result'], before['accounting']['public_result'])
                api = ExecutionInterface(self.workspace, allow_prepared_unreviewed=True, allow_presumed_user_sources=True)
                local = api.call(self.envelope('resume', case_id=before['case_id']))
                self.assertEqual(local['public_result'], before['accounting']['public_result'])

    def test_accepted_jobs_bind_source_attestation_and_class_assumptions(self):
        mutations = [lambda c: c['source'].update(version='2'),
                     lambda c: c['source_attestation'].update(authenticated_user_reference='replacement-user'),
                     lambda c: c['class_assumptions']['machinery'].update(remaining_life='5')]
        for i, mutate in enumerate(mutations):
            cid = self.stage(rid='mutate-'+str(i)); status, job = self.job(cid, 'mutate-'+str(i))
            self.assertEqual(status, 202)
            api = ExecutionInterface(self.workspace, allow_prepared_unreviewed=True, allow_presumed_user_sources=True)
            _, folder = api._request(cid, api._configuration(COMPANY))
            e = json.loads((folder/'evidence.json').read_text()); mutate(e['facts']['machinery'])
            (folder/'evidence.json').write_text(json.dumps(e))
            with patch.object(CAO, 'run', side_effect=AssertionError('mutated inputs reached owner')):
                self.assertTrue(self.service.run_one())
            done = self.http('/v1/jobs/'+job['id'])[1]
            self.assertEqual(done['state'], 'FAILED')
            self.assertEqual(done['error']['code'], 'conflict')
            self.assertNotIn(USER, json.dumps(done))
            self.assertNotIn(SOURCE_HASH, json.dumps(done))

    def test_accepted_job_binds_immutable_assurance_descriptor(self):
        cid = self.stage(); status, job = self.job(cid); self.assertEqual(status, 202)
        path = self.workspace/'requests/presumed.json'; descriptor = json.loads(path.read_text())
        descriptor.pop('source_assurance'); path.write_text(json.dumps(descriptor))
        self.assertTrue(self.service.run_one())
        self.assertEqual(self.http('/v1/jobs/'+job['id'])[1]['state'], 'FAILED')

    def test_descriptor_assurance_deletion_cannot_bypass_disabled_host_reads(self):
        cid, before = self.complete()
        path = self.workspace/'requests/presumed.json'
        original = json.loads(path.read_text())
        for remove in (('source_assurance',), ('source_assurance', 'review_mode')):
            descriptor = copy.deepcopy(original)
            for field in remove: descriptor.pop(field)
            path.write_text(json.dumps(descriptor))
            for enabled in (False, True):
                api = ExecutionInterface(self.workspace, allow_prepared_unreviewed=True,
                                         allow_presumed_user_sources=enabled)
                with patch.object(CAO, 'run', side_effect=AssertionError('descriptor attack reached owner')):
                    for op in ('status', 'questions', 'result', 'resume', 'execute'):
                        refused = api.call(self.envelope(op, case_id=cid))
                        self.assertFalse(refused['ok'], (remove, enabled, op, refused))
                        self.assertNotIn('USER_PROVIDED_SOURCES', json.dumps(refused))
            path.write_text(json.dumps(original))
        self.assertEqual(self.http('/v1/jobs/'+before['id'])[1]['accounting']['public_result'],
                         before['accounting']['public_result'])

    def test_job_preacceptance_reports_all_missing_envelope_fields(self):
        status, refused = self.http('/v1/jobs', {'contract_version': '1.0', 'operation': 'execute'},
                                    **{'Idempotency-Key': 'missing-bindings'})
        self.assertEqual(status, 400, refused)
        self.assertEqual(refused['error']['code'], 'invalid_request')
        self.assertEqual({x['field_path'] for x in refused['error']['requirements']}, {'company_id', 'case_id'})
        with self.service.db() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM jobs').fetchone()[0], 0)

    def test_missing_staged_source_case_is_specific_preacceptance_error(self):
        cid = self.stage()
        api = ExecutionInterface(self.workspace, allow_prepared_unreviewed=True, allow_presumed_user_sources=True)
        _, folder = api._request(cid, api._configuration(COMPANY))
        staged = json.loads((folder/'evidence.json').read_text())
        staged['facts']['machinery'].pop('case_id')
        (folder/'evidence.json').write_text(json.dumps(staged))
        status, refused = self.job(cid)
        self.assertEqual(status, 400, refused)
        self.assertEqual(refused['error']['code'], 'invalid_request')
        self.assertIn('evidence.facts.machinery.case_id', [x['field_path'] for x in refused['error']['requirements']])
        with self.service.db() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM jobs').fetchone()[0], 0)

    def test_failed_job_safe_error_projection_preserves_requirements(self):
        # Deliberate transport fault injection after acceptance: both raised
        # structured validation and returned local refusal must retain field
        # requirements; an unexpected exception must keep its detail private.
        need = dict(identifier='request.case_id', field_path='case_id',
                    explanation='Supply a nonblank case id.', category='missing_fact')
        for i, behavior in enumerate(('raised-validation', 'returned-validation', 'unexpected-private-error')):
            cid = self.stage(rid='error-projection-'+str(i)); _, accepted = self.job(cid, 'error-'+str(i))
            if behavior == 'raised-validation':
                injection = patch.object(self.service, '_execute_job', side_effect=Error('invalid_request', requirements=[need]))
            elif behavior == 'returned-validation':
                injection = patch.object(self.service, '_execute_job', return_value=dict(ok=False,
                    error=dict(code='invalid_request', message='Check the versioned request contract.', requirements=[need])))
            else:
                injection = patch.object(self.service, '_execute_job', side_effect=RuntimeError('private-job-exception-QA '+USER))
            with injection: self.assertTrue(self.service.run_one())
            status, failed = self.http('/v1/jobs/'+accepted['id'])
            self.assertEqual(status, 200); self.assertEqual(failed['state'], 'FAILED')
            if behavior == 'unexpected-private-error':
                self.assertEqual(failed['error']['code'], 'unavailable')
                self.assertNotIn('private-job-exception-QA', json.dumps(failed))
            else:
                self.assertEqual(failed['error']['code'], 'invalid_request')
                self.assertEqual(failed['error']['requirements'], [need])
            self.assertNotIn(USER, json.dumps(failed))
            restarted = self.new_service(); self.addCleanup(restarted.close)
            self.assertEqual(restarted.job(COMPANY, accepted['id'])['error'], failed['error'])

    def test_unknown_fact_names_do_not_echo_private_provenance_into_errors(self):
        cid = self.start()
        evidence = {'facts': {'Source: ChatGPT training data private-QA-reference':
                             {'source_assurance': PROFILE}}}
        _, refused = self.call('submit', case_id=cid, evidence=evidence)
        self.assertFalse(refused['ok'], refused)
        encoded = json.dumps(refused)
        self.assertNotIn('Source: ChatGPT training data', encoded)
        self.assertNotIn('private-QA-reference', encoded)

    def test_public_routes_exclude_client_identity_hash_and_approval_objects(self):
        case = synthetic_case(); case['assets'][0]['approved_by'] = 'private-source-approver-independent-QA'
        cid, _ = self.complete(case=case)
        api = ExecutionInterface(self.workspace, allow_prepared_unreviewed=True, allow_presumed_user_sources=True)
        for route in ('answer_context', 'answer', 'retrieval_snippet', 'citation', 'tool_output', 'user_log', 'export'):
            result = api.call(self.envelope('resume', case_id=cid, route=route)); self.assertTrue(result['ok'], result)
            public = json.dumps(result['public_result'])
            for value in (USER, SOURCE_HASH, 'private-source-approver-independent-QA', 'source_attestation',
                          'knowledge_population', 'knowledge_documents', 'reviewer_signoff', 'FORMALLY_REVIEWED'):
                self.assertNotIn(value, public)
            self.assert_amount(result['public_result'], 'depreciation', '64800')

    def test_class_assumption_private_evidence_is_never_published(self):
        case = synthetic_case()
        case['class_assumptions']['machinery']['approved_by'] = 'private-class-policy-approver-QA'
        _, job = self.complete(case=case)
        self.assertNotIn('private-class-policy-approver-QA', json.dumps(job['accounting']['public_result']))

    def test_native_records_are_assertions_never_fabricated_reviews(self):
        cid, _ = self.complete(); case, result = self.native(cid)
        for field in ('knowledge_review', 'applicability_review', 'reviewer_signoff'):
            self.assertNotIn(field, result['facts_used'])
        self.assertEqual(result['source_assertion']['origin'], 'CLIENT_ASSERTION_NOT_INDEPENDENT_CERTIFICATION')
        self.assertEqual(result['source_assertion']['attestation']['authenticated_user_reference'], USER)
        self.assertEqual(result['source_lineage']['source']['hash'], SOURCE_HASH)
        self.assertFalse(result['journal_entry_implications']); self.assertTrue(result['proposed_journal_workpaper'])
        self.assertFalse(case.governance.versions.active)

    def test_attestation_invalid_boolean_and_timezone_stay_unresolved(self):
        for i, change in enumerate(({'represents_company_records': 1}, {'represents_company_records': False},
                                    {'timestamp': '2026-11-02T09:00:00'})):
            case = synthetic_case(); case['source_attestation'].update(change)
            _, job = self.complete(rid='attestation-'+str(i), case=case)
            public = job['accounting']['public_result']
            self.assertEqual(public['accounting_determination'], 'UNRESOLVED')
            self.assertFalse(public.get('calculations'))

    def test_plain_ap_does_not_require_po_receipt_matching_inputs(self):
        _, job = self.complete('accounts-payable')
        report = job['accounting']['public_result']['anomaly_report']
        matching = [f for f in report['findings'] if f['check_id'] == 'arithmetic']
        self.assertTrue(any(f['severity'] == 'NOT_PERFORMED' for f in matching))
        self.assertFalse(any(f['severity'] == 'PASS' for f in matching))

    def test_ap_matching_when_supplied_selectively_blocks_error(self):
        case = synthetic_case('accounts-payable'); case['invoices'][0]['po_amount'] = '999'
        _, job = self.complete('accounts-payable', case=case)
        public = job['accounting']['public_result']; self.assert_amount(public, 'invoices', '1440')
        self.assertIn('invoices:1', public['anomaly_report']['excluded_rows'])
        self.assertEqual(public['accounting_determination'], 'UNRESOLVED')

    def test_material_missing_inputs_aggregate_and_preserve_valid_rows(self):
        case = synthetic_case(); case['assets'][0].pop('ready_date'); case['assets'][1].pop('opening_accumulated')
        _, job = self.complete(case=case); public = job['accounting']['public_result']
        self.assert_amount(public, 'depreciation', '62500')
        self.assertEqual(public['accounting_determination'], 'UNRESOLVED')
        self.assertEqual(set(public['anomaly_report']['excluded_rows']), {'assets:1', 'assets:2'})
        self.assertGreaterEqual(len(public['validation_requirements']), 2)

    def test_no_outlier_pass_without_qualified_norm(self):
        _, job = self.complete(); findings = job['accounting']['public_result']['anomaly_report']['findings']
        outliers = [f for f in findings if f['check_id'] == 'qualified_outliers']
        self.assertTrue(outliers); self.assertTrue(all(f['severity'] == 'NOT_PERFORMED' for f in outliers))

    def test_wrong_class_policy_scope_blocks_without_generic_defaults(self):
        for i, change in enumerate(({'framework': 'US_GAAP'}, {'entity': 'OTHER'}, {'effective_to': '2025-12-31'})):
            case = synthetic_case(); case['class_assumptions']['machinery'].update(change)
            _, job = self.complete(rid='policy-'+str(i), case=case)
            public = job['accounting']['public_result']
            self.assertFalse(public.get('calculations'), 'An excluded population cannot establish a zero depreciation total')
            self.assertEqual(len(public['anomaly_report']['excluded_rows']), 27)
            self.assertNotIn('Proposed journal implications:', public['guidance'])
            self.assertEqual(public['accounting_determination'], 'UNRESOLVED')


class IndependentPresumedFingerprintQA(unittest.TestCase):
    def test_profile11_fingerprint_matches_unchanged_main7146_algorithm(self):
        import production
        from implementation_scope import fingerprint_files
        from prepared_fingerprint import bind_additive_mode
        from hosted_cao.tests.test_prepared_engineering_qa import prepared_evidence
        for package in FAMILY:
            case = prepared_evidence(package)['facts'][FAMILY[package]]
            case.update(package=package, review_mode=MODE)
            files = fingerprint_files(case, ROOT, production.PACKAGES)
            implementation = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
            for name, witness in [('skills/production.py', 'main-7146-production.py.txt'),
                                  ('interfaces/public_output.py', 'main-7146-public-output.py.txt')]:
                implementation[name] = hashlib.sha256((ROOT/'skills/presumed-sources/release'/witness).read_bytes()).hexdigest()
            # Existing Profile 1.1 helper, method and canonical populations remain
            # unchanged. The old algorithm binds those bytes and the original
            # shared-boundary hashes, not the new compatibility helper's claims.
            implementation = bind_additive_mode(case, ROOT, production.PACKAGES, files, implementation,
                '1c371d847f0f86eb7eba5bb9a1b92a13250f52db4f9a09dca5f675f5d2ef0977')
            expected = hashlib.sha256(json.dumps({'case': case, 'implementation': implementation},
                                                 sort_keys=True, default=str).encode()).hexdigest()
            self.assertEqual(production.case_fingerprint(case), expected, package)

    def test_new_profile_fingerprint_binds_all_helpers_and_private_source_inputs(self):
        import production
        original_read = Path.read_bytes
        for package in FAMILY:
            case = synthetic_case(package); case.update(package=package, review_mode=MODE, source_assurance=PROFILE)
            baseline = production.case_fingerprint(case)
            for name in ('skills/source_execution.py', 'skills/source_screening.py', 'skills/source_fingerprint.py',
                         'skills/presumed-sources/additive-changes.json', 'interfaces/public_output.py'):
                target = ROOT/name
                def changed(path, *args, **kwargs):
                    value = original_read(path, *args, **kwargs)
                    return value+b'\n# independent source-profile byte mutation\n' if path == target else value
                with self.subTest(package=package, name=name), patch.object(Path, 'read_bytes', changed):
                    self.assertNotEqual(production.case_fingerprint(case), baseline)
            for field in ('source', 'source_attestation', 'class_assumptions'):
                changed_case = copy.deepcopy(case)
                changed_case[field]['independent_mutation'] = 'changed'
                self.assertNotEqual(production.case_fingerprint(changed_case), baseline)

    def test_new_compatibility_witnesses_and_helper_tamper_invalidate_formal_normalization(self):
        import production
        from local_cao.tests.test_authored import evidence
        original_read = Path.read_bytes
        case = evidence('fixed-assets')['facts']['machinery']
        baseline = production.case_fingerprint(case)
        for name in ('skills/source_fingerprint.py', 'skills/presumed-sources/additive-changes.json',
                     'skills/presumed-sources/release/main-7146-production.py.txt',
                     'skills/presumed-sources/release/main-7146-public-output.py.txt'):
            target = ROOT/name
            def changed(path, *args, **kwargs):
                value = original_read(path, *args, **kwargs)
                return value+b'\n# independent witness byte mutation\n' if path == target else value
            with self.subTest(name=name), patch.object(Path, 'read_bytes', changed):
                self.assertNotEqual(production.case_fingerprint(case), baseline)


if __name__ == '__main__':
    unittest.main()
