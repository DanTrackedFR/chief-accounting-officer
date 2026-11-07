"""Independent exact legacy refusal compatibility and opt-in diagnostics QA.

No accounting/reference output is regenerated. The historical wrong-framework
response is loaded from the existing hash-checked reference resolver. The small
request fixture reproduces the actual public context route without document or
accounting execution and needs no external parser dependencies.
"""
import copy
import http.client
import json
from pathlib import Path
import tempfile
import threading
import unittest

from hosted_cao.service import Service, Server
from local_cao.adapter import ExecutionInterface
from orchestration.history_references import reference_path

ROOT = Path(__file__).resolve().parents[1]
COMPANY = 'synthetic-demo-001'
MODE = 'prepared_unreviewed'
PROFILE = 'presumed_user_provided'
TOKEN = 'historical-error-independent-QA-' + 'z' * 32
LOCAL_MESSAGE = 'Check contract version, operation and required input fields.'
HTTP_MESSAGE = 'Check the versioned request contract.'


def envelope(operation, **fields):
    return dict(contract_version='1.0', company_id=COMPANY, operation=operation, **fields)


def company_context():
    return (ROOT/'company-context.example.md').read_text().replace('ENTITY-DEMO', 'ASTERION-NL').replace(
        'legal_name: Synthetic Group', 'legal_name: Asterion Cold-chain Group').replace(
        'industry: SaaS', 'industry: Laboratory cold-chain equipment and monitoring').replace(
        'business_description: Synthetic accounting demonstration',
        'business_description: Synthetic manufacturer and monitoring operator serving research laboratories').replace(
        'investigation_threshold: UNKNOWN', 'investigation_threshold: 1500')


def wrong_framework_request():
    items = []
    for entity, framework, currency in [('UK-SUB', 'UK_GAAP', 'GBP'), ('GROUP', 'IFRS', 'EUR')]:
        for key, value in [('framework', framework), ('jurisdiction', 'GB'),
                           ('functional_currency', currency), ('presentation_currency', currency),
                           ('calendar_id', 'FISCAL-UK')]:
            items.append(dict(id=entity+'-'+key, key=key, value=value, entity_id=entity,
                              effective_from='2026-01-01', effective_to='2026-12-31',
                              source_state='approved', source_ref='asserted-onboarding',
                              source_version='v1', framework=framework))
    items.append(dict(id='ifrs-only-uk-currency', key='functional_currency', value='USD', entity_id='UK-SUB',
                      effective_from='2026-01-01', effective_to='2026-12-31', source_state='approved',
                      source_ref='foreign-framework-onboarding', source_version='v1', framework='IFRS'))
    items.append(dict(id='group-scope', key='scope_type', value='GROUP', entity_id='GROUP',
                      effective_from='2026-01-01', effective_to='2026-12-31', source_state='user_asserted',
                      source_ref='asserted-onboarding', source_version='v1'))
    wrong = copy.deepcopy(items)
    next(row for row in wrong if row['id'] == 'UK-SUB-calendar_id')['framework'] = 'IFRS'
    return envelope('investigate', request_id='uk-wrong-framework-calendar', objective='Review UK laboratory prepayments',
                    target_family='reconciliation', context=dict(version='v1', company_id=COMPANY,
                    items=wrong, selection=dict(entity_id='UK-SUB', period_start='2026-01-01', period_end='2026-12-31')))


def frozen_wrong_framework_response():
    return json.loads(reference_path('build4/release/integrated-proof.json').read_bytes())['wrong_framework_dimensions']


def legacy_local_error(operation):
    return dict(contract_version='1.0', operation=operation, ok=False,
                error=dict(code='invalid_request', message=LOCAL_MESSAGE),
                public_result=dict(status='blocked', guidance=LOCAL_MESSAGE))


class IndependentHistoricalErrorCompatibilityQA(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name); self.workspace = self.root/'company'; self.workspace.mkdir()
        (self.workspace/'company-context.md').write_text(company_context())
        self.assertTrue(self.api().call(envelope('initialize'))['ok'])
        self.services = []

    def api(self, prepared=False, presumed=False):
        return ExecutionInterface(self.workspace, allow_prepared_unreviewed=prepared,
                                  allow_presumed_user_sources=presumed)

    def service(self, prepared=False, presumed=False):
        value = Service(self.root/('jobs-'+str(len(self.services))), {COMPANY: self.workspace},
                        [dict(caller_id='historical-error-test', token=TOKEN, companies=[COMPANY])],
                        allow_prepared_unreviewed=prepared, allow_presumed_user_sources=presumed)
        self.services.append(value); self.addCleanup(value.close)
        return value

    def http(self, service, path, body):
        server = Server(('127.0.0.1', 0), service)
        worker = threading.Thread(target=server.serve_forever); worker.start()
        try:
            connection = http.client.HTTPConnection(*server.server_address, timeout=30)
            connection.request('POST', path, json.dumps(body),
                {'Authorization': 'Bearer '+TOKEN, 'X-CAO-Company': COMPANY,
                 'Content-Type': 'application/json', 'Idempotency-Key': 'historical-error-test'})
            response = connection.getresponse(); output = response.status, json.loads(response.read())
            connection.close(); return output
        finally:
            server.shutdown(); server.server_close(); worker.join()

    def test_default_formal_wrong_framework_response_is_exact_frozen_record(self):
        self.assertEqual(self.api().call(wrong_framework_request()), frozen_wrong_framework_response())

    def test_profile11_host_wrong_framework_response_is_exact_frozen_record(self):
        self.assertEqual(self.api(prepared=True).call(wrong_framework_request()), frozen_wrong_framework_response())

    def test_default_formal_malformed_local_refusals_keep_original_envelopes(self):
        requests = [envelope('execute'), envelope('start', objective='Calculate accounting', target_family='machinery'),
                    dict(envelope('diagnose'), unexpected='unregistered')]
        for request in requests:
            with self.subTest(operation=request['operation']):
                self.assertEqual(self.api().call(request), legacy_local_error(request['operation']))

    def test_profile11_malformed_local_refusals_keep_original_envelopes(self):
        for operation in ('start', 'execute'):
            request = envelope(operation, review_mode=MODE)
            if operation == 'start': request.update(objective='Calculate accounting', target_family='machinery')
            with self.subTest(operation=operation):
                self.assertEqual(self.api(prepared=True).call(request), legacy_local_error(operation))

    def test_hosted_wrong_framework_error_is_exact_frozen_record_for_legacy_hosts(self):
        for prepared in (False, True):
            with self.subTest(prepared=prepared):
                status, response = self.http(self.service(prepared=prepared), '/v1/operations', wrong_framework_request())
                self.assertEqual(status, 422); self.assertEqual(response, frozen_wrong_framework_response())

    def test_default_formal_hosted_malformed_binding_keeps_original_error(self):
        status, response = self.http(self.service(), '/v1/jobs', envelope('execute'))
        self.assertEqual(status, 400)
        self.assertEqual(response, dict(api_version='1.0', ok=False,
                         error=dict(code='invalid_request', message=HTTP_MESSAGE)))

    def test_profile11_hosted_malformed_binding_keeps_original_error(self):
        status, response = self.http(self.service(prepared=True), '/v1/jobs', envelope('execute', review_mode=MODE))
        self.assertEqual(status, 400)
        self.assertEqual(response, dict(api_version='1.0', ok=False,
                         error=dict(code='invalid_request', message=HTTP_MESSAGE)))

    def test_enabled_source_host_local_missing_bindings_remain_structured(self):
        request = dict(contract_version='1.0', operation='execute', review_mode=MODE, source_assurance=PROFILE)
        response = self.api(prepared=True, presumed=True).call(request)
        self.assertFalse(response['ok']); self.assertEqual(response['error']['code'], 'invalid_request')
        self.assertEqual({row['field_path'] for row in response['error']['requirements']}, {'company_id', 'case_id'})
        self.assertFalse(response.get('durable')); self.assertFalse(response['public_result'].get('calculations'))

    def test_enabled_source_host_http_missing_binding_remains_structured(self):
        service = self.service(prepared=True, presumed=True)
        status, response = self.http(service, '/v1/jobs', envelope('execute', review_mode=MODE, source_assurance=PROFILE))
        self.assertEqual(status, 400); self.assertEqual(response['error']['code'], 'invalid_request')
        self.assertEqual({row['field_path'] for row in response['error']['requirements']}, {'case_id'})
        with service.db() as db:
            self.assertEqual(db.execute('SELECT count(*) FROM jobs').fetchone()[0], 0)

    def test_enabled_source_host_unknown_fields_keep_structured_fallback(self):
        request = envelope('diagnose', unexpected='unregistered')
        local = self.api(prepared=True, presumed=True).call(request)
        self.assertFalse(local['ok'])
        self.assertEqual([row['field_path'] for row in local['error']['requirements']], ['$'])
        status, hosted = self.http(self.service(prepared=True, presumed=True), '/v1/operations', request)
        self.assertEqual(status, 400)
        self.assertEqual([row['field_path'] for row in hosted['error']['requirements']], ['$'])


if __name__ == '__main__':
    unittest.main()
