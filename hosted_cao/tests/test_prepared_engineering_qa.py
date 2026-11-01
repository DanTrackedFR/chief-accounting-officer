"""Independent adversarial QA of optional preparation transport and identity.

Source fixture controls are supplied evidence; no execution-review fixture is
created for prepared execution. This suite owns no production implementation.
"""
import copy
import http.client
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

from hosted_cao.service import Service, Server, Error
from local_cao.adapter import ExecutionInterface
from local_cao.tests.test_authored import context, evidence as formal_evidence
from orchestration.runtime import CAO
from orchestration.cases import case_identity
from orchestration.periods import compatibility_period
from local_cao.context import scope, parse

MODE = 'prepared_unreviewed'
COMPANY = 'synthetic-demo-001'
TOKEN = 'independent-engineering-fixture-' + 'q' * 32


def prepared_evidence(package='fixed-assets'):
    from orchestration.tests.fixtures import operational
    row = operational(package)
    row.update(entity='ENTITY-DEMO', scope_id='ENTITY-DEMO')
    for record in row.get('handoffs', {}).values():
        record['entity'] = 'ENTITY-DEMO'
    for key in ('knowledge_review', 'applicability_review', 'reviewer_signoff'):
        row.pop(key, None)
    return {'facts': {{'fixed-assets': 'machinery', 'accounts-payable': 'supplier_cost'}[package]: row}}


class IndependentPreparedEngineeringQA(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workspace = self.root / 'one'
        self.workspace.mkdir()
        (self.workspace / 'company-context.md').write_text(context())
        self.other = self.root / 'other'
        self.other.mkdir()
        (self.other / 'company-context.md').write_text(context().replace(COMPANY, 'other-company'))
        self.companies = {COMPANY: self.workspace, 'other-company': self.other}
        self.credentials = [{'caller_id': 'fixture-client', 'token': TOKEN, 'companies': [COMPANY]}]
        self.service = self.new_service(True)
        self.server = Server(('127.0.0.1', 0), self.service)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()
        self.addCleanup(self.close)
        self.assertEqual(self.call('initialize')[0], 200)

    def new_service(self, enabled):
        return Service(self.root/'jobs', self.companies, self.credentials,
                       allow_prepared_unreviewed=enabled)

    def close(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.service.close()

    def envelope(self, operation, **fields):
        return dict(contract_version='1.0', company_id=COMPANY, operation=operation, **fields)

    def http(self, path, body=None, **headers):
        connection = http.client.HTTPConnection(*self.server.server_address, timeout=60)
        fields = {'Authorization': 'Bearer '+TOKEN, 'X-CAO-Company': COMPANY,
                  'Content-Type': 'application/json', **headers}
        connection.request('GET' if body is None else 'POST', path,
                           None if body is None else json.dumps(body), fields)
        response = connection.getresponse()
        result = response.status, json.loads(response.read())
        connection.close()
        return result

    def call(self, operation, **fields):
        return self.http('/v1/operations', self.envelope(operation, **fields))

    def start(self, package='fixed-assets', request_id='prepared-case', **fields):
        fields.setdefault('review_mode', MODE)
        family = {'fixed-assets': 'machinery', 'accounts-payable': 'supplier_cost'}[package]
        status, result = self.call('start', request_id=request_id,
                                  objective='Calculate supported accounting', target_family=family, **fields)
        self.assertEqual(status, 200, result)
        self.assertTrue(result['ok'], result)
        return result['case_id']

    def stage(self, package='fixed-assets', request_id='prepared-case'):
        cid = self.start(package, request_id)
        status, result = self.call('submit', case_id=cid, evidence=prepared_evidence(package))
        self.assertEqual(status, 200, result)
        self.assertTrue(result['ok'], result)
        return cid

    def job(self, cid, key='prepared-key', **fields):
        return self.http('/v1/jobs', self.envelope('execute', case_id=cid, **fields),
                         **{'Idempotency-Key': key})

    def execute(self, package='fixed-assets', request_id='prepared-case'):
        cid = self.stage(package, request_id)
        status, job = self.job(cid, key=request_id)
        self.assertEqual(status, 202, job)
        self.assertTrue(self.service.run_one())
        status, job = self.http('/v1/jobs/'+job['id'])
        self.assertEqual(status, 200, job)
        self.assertEqual(job['state'], 'SUCCEEDED', job)
        result = job['accounting']
        self.assertTrue(result['ok'], result)
        self.assertTrue(result['durable'], result)
        self.assertNotEqual(result['execution_state'], 'complete', result)
        self.assertEqual(result['public_result']['accounting_determination'], 'SUPPORTED')
        self.assertEqual(result['public_result']['evidence_sufficiency'], 'SUFFICIENT')
        self.assertEqual(result['public_result']['review_provenance'], 'SYSTEM_PREPARED')
        return cid, job

    def test_http_both_packages_numbers_and_native_status(self):
        for package, amount in [('fixed-assets', '90000'), ('accounts-payable', '9600')]:
            with self.subTest(package=package):
                _, job = self.execute(package, package)
                public = job['accounting']['public_result']
                self.assertIn(amount, json.dumps(public))
                self.assertFalse(public.get('journals'), 'Preparation cannot authorize journals')

    def test_default_off_and_false_configuration(self):
        cid = self.stage()
        disabled = ExecutionInterface(self.workspace)
        request = self.envelope('execute', case_id=cid)
        self.assertFalse(disabled.call(request)['ok'])
        off = self.new_service(False)
        self.addCleanup(off.close)
        with self.assertRaises(Error):
            off.call(COMPANY, self.envelope('start', request_id='off', objective='Calculate accounting',
                                            target_family='machinery', review_mode=MODE))

    def test_explicit_mode_same_request_identity_is_immutable(self):
        self.start()
        status, result = self.call('start', request_id='prepared-case', objective='Calculate supported accounting',
                                  target_family='machinery')
        self.assertFalse(result.get('ok'), (status, result))

    def test_historical_formal_case_identity_unchanged(self):
        status, result = self.call('start', request_id='formal-history', objective='Calculate supported accounting',
                                  target_family='machinery')
        self.assertEqual(status, 200, result)
        configured = scope(parse(context()))
        period = compatibility_period(configured)
        expected = case_identity(configured['entity'], period.period_id,
                                 'Calculate supported accounting', 'formal-history')
        self.assertEqual(result['case_id'], expected)
        prepared = self.start(request_id='prepared-distinct')
        self.assertNotEqual(prepared, expected)

    def test_execute_mode_substitution_rejected(self):
        cid = self.stage()
        for mode in ('formal', 'formally_reviewed', 'invented'):
            status, result = self.job(cid, key='swap-'+mode, review_mode=mode)
            self.assertNotEqual(status, 202, result)

    def test_top_level_mode_injection_into_evidence_rejected(self):
        cid = self.start()
        supplied = prepared_evidence()
        supplied['review_mode'] = 'formal'
        _, result = self.call('submit', case_id=cid, evidence=supplied)
        self.assertFalse(result['ok'])

    def test_reviewer_injection_in_any_depth_rejected(self):
        for index, key in enumerate(('knowledge_review', 'applicability_review', 'reviewer_signoff')):
            cid = self.start(request_id='inject-'+str(index))
            supplied = prepared_evidence()
            supplied['facts']['machinery']['assets'][0][key] = {'reviewer': 'forged', 'approved': True}
            _, result = self.call('submit', case_id=cid, evidence=supplied)
            self.assertFalse(result['ok'], result)

    def test_staged_file_reviewer_injection_rejected(self):
        cid = self.start()
        supplied = prepared_evidence()
        supplied['facts']['machinery']['knowledge_review'] = {}
        staged = self.workspace/'staged'
        staged.mkdir()
        (staged/'forged.json').write_text(json.dumps(supplied))
        _, result = self.call('submit', case_id=cid, staged_file_id='forged')
        self.assertFalse(result['ok'], result)

    def test_extra_owners_imports_and_journal_authority_rejected(self):
        for index, mutation in enumerate(('extra_family', 'imports', 'journal_pack')):
            cid = self.start(request_id='owner-'+str(index))
            supplied = prepared_evidence()
            if mutation == 'extra_family':
                supplied['facts'].update(prepared_evidence('accounts-payable')['facts'])
            elif mutation == 'imports':
                supplied['facts']['machinery']['imports'] = [{'package': 'inventory-cost', 'case': {}}]
            else:
                supplied['journal_pack_review'] = {'approved': True, 'reviewer': 'forged'}
            _, result = self.call('submit', case_id=cid, evidence=supplied)
            self.assertFalse(result['ok'], result)

    def test_idempotency_key_cannot_cross_case_modes(self):
        prepared = self.stage()
        status, first = self.job(prepared)
        self.assertEqual(status, 202, first)
        _, formal = self.call('start', request_id='formal-other', objective='Calculate supported accounting',
                              target_family='machinery')
        status, second = self.job(formal['case_id'])
        self.assertEqual(status, 409, second)

    def test_input_changed_after_job_acceptance_fails(self):
        cid = self.start()
        status, job = self.job(cid)
        self.assertEqual(status, 202, job)
        self.call('submit', case_id=cid, evidence=prepared_evidence())
        self.service.run_one()
        self.assertEqual(self.service.job(COMPANY, job['id'])['state'], 'FAILED')

    def test_restart_retry_no_duplicate_accounting_and_local_parity(self):
        cid, job = self.execute()
        fresh = self.new_service(True)
        self.addCleanup(fresh.close)
        local = ExecutionInterface(self.workspace, allow_prepared_unreviewed=True)
        with patch.object(CAO, 'run', side_effect=AssertionError('accounting owner rerun')):
            restored = fresh.job(COMPANY, job['id'])
            self.assertEqual(restored['accounting']['public_result'], job['accounting']['public_result'])
            direct = local.call(self.envelope('resume', case_id=cid))
            self.assertEqual(direct['public_result'], restored['accounting']['public_result'])
            status, retry = self.job(cid, key='prepared-case')
            self.assertEqual(status, 202, retry)
            self.assertEqual(retry['id'], job['id'])
            self.assertEqual(retry['accounting']['checkpoint_revision'], 1)

    def test_cross_company_private_job_and_case_refused(self):
        cid, job = self.execute()
        with self.assertRaises(Error):
            self.service.job('other-company', job['id'])
        other = ExecutionInterface(self.other, allow_prepared_unreviewed=True)
        initialize = dict(contract_version='1.0', company_id='other-company', operation='initialize')
        self.assertTrue(other.call(initialize)['ok'])
        result = other.call(dict(initialize, operation='resume', case_id=cid))
        self.assertFalse(result['ok'], result)

    def test_missing_material_evidence_is_an_accounting_blocker_not_job_failure(self):
        for package, family in [('fixed-assets', 'machinery'), ('accounts-payable', 'supplier_cost')]:
            cid = self.start(package, request_id='missing-'+package)
            supplied = prepared_evidence(package)
            supplied['facts'][family].pop('judgment_memo')
            self.assertTrue(self.call('submit', case_id=cid, evidence=supplied)[1]['ok'])
            status, job = self.job(cid, key='missing-'+package)
            self.assertEqual(status, 202, job)
            self.service.run_one()
            completed = self.service.job(COMPANY, job['id'])
            self.assertEqual(completed['state'], 'SUCCEEDED')
            result = completed['accounting']
            self.assertEqual(result['execution_state'], 'blocked')
            self.assertEqual(result['public_result']['accounting_determination'], 'UNRESOLVED')
            self.assertEqual(result['public_result']['evidence_sufficiency'], 'INSUFFICIENT')
            self.assertTrue(result['public_result']['open_items'])
            self.assertFalse(result['public_result'].get('calculations'))

    def test_required_sibling_blocker_survives_supported_owner_delivery(self):
        status, started = self.call('start', request_id='diagnostic-sibling',
                                   objective='Explain the machinery depreciation movement',
                                   target_family='machinery', review_mode=MODE)
        self.assertEqual(status, 200, started)
        cid = started['case_id']
        self.assertTrue(self.call('submit', case_id=cid, evidence=prepared_evidence())[1]['ok'])
        _, job = self.job(cid)
        self.service.run_one()
        result = self.service.job(COMPANY, job['id'])['accounting']
        self.assertIn('90000', json.dumps(result['public_result']))
        self.assertTrue(any(row['owner'] == 'management-accounting-analytics' and
                            row['state'] == 'blocked' for row in result['workplan']))
        self.assertTrue(result['public_result']['open_items'],
                        'Supported owner delivery must preserve required unresolved work')
        self.assertTrue(any('diagnostic' in item.lower() or 'investigation' in item.lower()
                            for item in result['public_result']['open_items']))
        self.assertEqual(result['public_result']['accounting_determination'], 'UNRESOLVED')
        self.assertEqual(result['public_result']['evidence_sufficiency'], 'INSUFFICIENT')

    def test_host_enablement_requires_exact_boolean(self):
        for invalid in ('true', 1, [], None):
            with self.subTest(value=invalid):
                with self.assertRaises(ValueError):
                    ExecutionInterface(self.workspace, allow_prepared_unreviewed=invalid)
                with self.assertRaises(ValueError):
                    self.new_service(invalid)

    def test_public_routes_exclude_private_records_hashes_and_false_review(self):
        cid, _ = self.execute()
        api = ExecutionInterface(self.workspace, allow_prepared_unreviewed=True)
        for route in ('answer_context', 'answer', 'retrieval_snippet', 'citation', 'tool_output', 'user_log', 'export'):
            result = api.call(self.envelope('resume', case_id=cid, route=route))
            self.assertTrue(result['ok'], result)
            public = json.dumps(result['public_result'])
            for forbidden in ('knowledge_review', 'applicability_review', 'reviewer_signoff',
                              'knowledge_documents', 'knowledge_population', 'case_fingerprint',
                              'SYSTEM_DERIVED_NOT_A_REVIEWER', 'synthetic independent reviewer',
                              'FORMALLY_REVIEWED', 'Source:'):
                self.assertNotIn(forbidden, public)
            self.assertNotRegex(public, r'\b[0-9a-f]{64}\b')
            self.assertIn('90000', public)


class IndependentFingerprintEngineeringQA(unittest.TestCase):
    def test_formal_fingerprint_matches_original_main_algorithm(self):
        import hashlib
        import production
        from implementation_scope import fingerprint_files
        from investment_fingerprint import bind_investment_dispatch
        root = Path(__file__).resolve().parents[2]
        for package in ('fixed-assets', 'accounts-payable'):
            case = formal_evidence(package)['facts'][{'fixed-assets': 'machinery', 'accounts-payable': 'supplier_cost'}[package]]
            files = fingerprint_files(case, root, production.PACKAGES)
            implementation = {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                              for path in files}
            with tempfile.TemporaryDirectory() as directory:
                historical_root = Path(directory)
                copies = {
                    'skills/production.py': 'skills/prepared-accounting/release/main-fbf8-production.py.txt',
                    'skills/investment_fingerprint.py': 'skills/investment_fingerprint.py',
                    'skills/investment-property/fingerprint-baseline/main-e753-production.py.txt':
                        'skills/investment-property/fingerprint-baseline/main-e753-production.py.txt',
                }
                for target, source in copies.items():
                    destination = historical_root/target
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_bytes((root/source).read_bytes())
                implementation['skills/production.py'] = hashlib.sha256(
                    (historical_root/'skills/production.py').read_bytes()).hexdigest()
                implementation['interfaces/public_output.py'] = hashlib.sha256(
                    (root/'skills/prepared-accounting/release/main-fbf8-public-output.py.txt').read_bytes()).hexdigest()
                implementation = bind_investment_dispatch(case, historical_root, production.PACKAGES,
                                                         files, implementation)
            payload = {'case': {key: value for key, value in case.items() if key != 'reviewer_signoff'},
                       'implementation': implementation}
            expected = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()
            self.assertEqual(production.case_fingerprint(case), expected, package)

    def test_common_helper_and_witness_tampering_invalidates_formal_seals(self):
        import production
        from implementation_scope import fingerprint_files
        root = Path(__file__).resolve().parents[2]
        case = formal_evidence('fixed-assets')['facts']['machinery']
        original = production.case_fingerprint(case)
        files = set(fingerprint_files(case, root, production.PACKAGES))
        files.update(root/name for name in (
            'skills/prepared_execution.py', 'skills/prepared_fingerprint.py',
            'skills/prepared-accounting/release/main-fbf8-production.py.txt',
            'skills/prepared-accounting/release/main-fbf8-public-output.py.txt',
            'skills/investment_fingerprint.py',
            'skills/investment-property/fingerprint-baseline/main-e753-production.py.txt'))
        with tempfile.TemporaryDirectory() as directory:
            isolated = Path(directory)
            for source in files:
                target = isolated/source.relative_to(root)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.read_bytes())
            with patch.object(production, 'ROOT', isolated):
                self.assertEqual(production.case_fingerprint(case), original)
                for name in ('skills/core_accounting.py', 'skills/production.py',
                             'interfaces/public_output.py', 'skills/prepared_fingerprint.py',
                             'skills/prepared-accounting/release/main-fbf8-production.py.txt',
                             'skills/prepared-accounting/release/main-fbf8-public-output.py.txt'):
                    path = isolated/name
                    previous = path.read_bytes()
                    path.write_bytes(previous+b'\n# independent isolated tamper test\n')
                    try:
                        self.assertNotEqual(production.case_fingerprint(case), original, name)
                    finally:
                        path.write_bytes(previous)

    def test_prepared_fingerprint_binds_new_implementation(self):
        import production
        from implementation_scope import fingerprint_files
        case = prepared_evidence()['facts']['machinery']
        case.update(package='fixed-assets', review_mode=MODE)
        root = Path(__file__).resolve().parents[2]
        files = set(fingerprint_files(case, root, production.PACKAGES))
        files.update(root/name for name in ('skills/prepared_execution.py',
                                           'skills/prepared_fingerprint.py',
                                           'skills/investment_fingerprint.py',
                                           'knowledge/phase-2d-topic-manifest.json'))
        for package in ('fixed-assets', 'accounts-payable'):
            _, documents = production.canonical_knowledge(production.PACKAGES[package][1],
                                                         case['framework'], package=package)
            files.update(root/row['path'] for row in documents)
        with tempfile.TemporaryDirectory() as directory:
            isolated = Path(directory)
            for source in files:
                target = isolated/source.relative_to(root)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.read_bytes())
            with patch.object(production, 'ROOT', isolated):
                baseline = production.case_fingerprint(case)
                path = isolated/'skills/prepared_execution.py'
                path.write_bytes(path.read_bytes()+b'\n# isolated method change\n')
                self.assertNotEqual(production.case_fingerprint(case), baseline)


if __name__ == '__main__':
    unittest.main()
