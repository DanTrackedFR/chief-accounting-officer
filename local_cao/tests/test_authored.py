import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from local_cao.adapter import ExecutionInterface, VERSION, decode
from local_cao.context import parse
from orchestration.runtime import CAO

ROOT = Path(__file__).resolve().parents[2]


def context(entity='ENTITY-DEMO'):
    return (ROOT/'company-context.example.md').read_text().replace('ENTITY-DEMO', entity)


def evidence(package):
    # Fixture-only original reviewed input creation. Never part of adapter code.
    from orchestration.tests.fixtures import operational, certify
    c = operational(package)
    c.update(entity='ENTITY-DEMO', scope_id='ENTITY-DEMO')
    if 'handoffs' in c:
        for h in c['handoffs'].values(): h['entity']='ENTITY-DEMO'
    c = certify(package, c)
    family = {'fixed-assets':'machinery', 'accounts-payable':'supplier_cost'}[package]
    return {'facts':{family:c}}


class Authored(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name); (self.path/'company-context.md').write_text(context())
        self.api=ExecutionInterface(self.path); self.company='synthetic-demo-001'
        self.assertTrue(self.call('initialize')['ok'])

    def call(self, op, **fields):
        return self.api.call(dict(contract_version=VERSION, operation=op, company_id=self.company, **fields))

    def start(self, family='machinery', request_id='demo', objective='Calculate fixed asset depreciation'):
        result=self.call('start', request_id=request_id, objective=objective, target_family=family)
        self.assertTrue(result['ok'],result); return result

    def execute(self, pkg='fixed-assets'):
        s=self.start('machinery' if pkg=='fixed-assets' else 'supplier_cost',objective='Calculate supported accounting')
        self.assertTrue(self.call('submit',case_id=s['case_id'],evidence=evidence(pkg))['ok'])
        result=self.call('execute',case_id=s['case_id']);self.assertTrue(result['ok'],result)
        return result

    def test_diagnostics(self):
        r=self.call('diagnose');self.assertTrue(r['ok'],r);self.assertTrue(r['storage_ready'])

    def test_native_fixed_assets(self):
        r=self.execute();self.assertEqual(r['execution_state'],'complete',r)
        self.assertTrue(r['durable']);self.assertIn('90000',json.dumps(r['public_result']))

    def test_native_ap(self):
        r=self.execute('accounts-payable');self.assertEqual(r['execution_state'],'complete',r)
        self.assertIn('9600',json.dumps(r['public_result']))

    def test_restart_and_retry_no_owner(self):
        r=self.execute()
        with patch.object(CAO,'run',side_effect=AssertionError('rerun')):
            self.assertEqual(self.call('execute',case_id=r['case_id']),r)
        request=dict(contract_version=VERSION,operation='resume',company_id=self.company,case_id=r['case_id'])
        process=subprocess.run([sys.executable,'-m','local_cao','--workspace',str(self.path)],input=json.dumps(request),capture_output=True,text=True,cwd=ROOT)
        self.assertEqual(process.returncode,0,process.stderr)
        self.assertEqual(json.loads(process.stdout)['public_result'],r['public_result'])

    def test_cli_parity(self):
        request=dict(contract_version=VERSION,operation='context',company_id=self.company)
        p=subprocess.run([sys.executable,'-m','local_cao','--workspace',str(self.path)],input=json.dumps(request),capture_output=True,text=True,cwd=ROOT)
        self.assertEqual(json.loads(p.stdout),self.api.call(request))

    def test_missing_revenue(self):
        r=self.start('customer_contract',objective='How should we recognize revenue from this new customer agreement?')
        self.assertEqual(r['execution_state'],'blocked');self.assertFalse(r['durable'])
        self.assertIn('obligations',json.dumps(r['public_result']))
        self.assertFalse(r['public_result'].get('calculations'))

    def test_missing_prepayments(self):
        r=self.start('reconciliation',objective='Our prepayments have jumped this month. Investigate.')
        self.assertNotEqual(r['execution_state'],'complete');self.assertIn('reconciliations',json.dumps(r['public_result']))

    def test_context_does_not_approve(self):
        p=self.path/'company-context.md';p.write_text(context()+'\n## invented_policy\n- status: APPROVED\n- contents: Revenue is always immediate\n')
        r=self.call('context');self.assertTrue(r['ok']);self.assertFalse(r['approved_company_memory'])
        self.assertEqual(r['context_authority'],'user_assertion')

    def test_duplicate_context(self):
        p=self.path/'company-context.md';p.write_text(context()+'\n## company\n- company_id: another\n')
        self.assertEqual(self.call('context')['error']['code'],'invalid_context')

    def test_required_context(self):
        with self.assertRaises(ValueError):parse(context().replace('- framework: IFRS','- framework: UNKNOWN'))

    def test_dates_contradict(self):
        with self.assertRaises(ValueError):parse(context().replace('period_start: 2026-01-01','period_start: 2027-01-01'))

    def test_company_isolation(self):
        self.company='other';self.assertFalse(self.call('list')['ok'])

    def test_scope_change_refuses_existing_case(self):
        r=self.start();(self.path/'company-context.md').write_text(context('ENTITY-OTHER'))
        self.assertEqual(self.call('status',case_id=r['case_id'])['error']['code'],'identity_conflict')

    def test_identity_retry_conflict(self):
        self.start();self.assertFalse(self.call('start',request_id='demo',objective='Changed objective')['ok'])

    def test_immutable_evidence(self):
        r=self.start(); e=evidence('fixed-assets')
        self.assertTrue(self.call('submit',case_id=r['case_id'],evidence=e)['ok'])
        self.assertTrue(self.call('submit',case_id=r['case_id'],evidence=e)['ok'])
        e['facts']['machinery']['assets'][0]['opening_cost']='1'
        self.assertEqual(self.call('submit',case_id=r['case_id'],evidence=e)['error']['code'],'immutable_submission')

    def test_no_submission_after_checkpoint(self):
        r=self.execute();e=evidence('fixed-assets');self.assertTrue(self.call('submit',case_id=r['case_id'],evidence=e)['ok']);e['facts']['machinery']['entity']='OTHER';self.assertFalse(self.call('submit',case_id=r['case_id'],evidence=e)['ok'])

    def test_bad_scope_evidence(self):
        r=self.start();e=evidence('fixed-assets');e['facts']['machinery']['entity']='OTHER'
        self.assertFalse(self.call('submit',case_id=r['case_id'],evidence=e)['ok'])

    def test_public_no_private(self):
        r=self.execute();s=json.dumps(r['public_result'])
        for token in ('case_fingerprint','reviewer','source_fingerprint','Source:','training data'):self.assertNotIn(token,s)

    def test_unsupported_family(self):
        self.assertFalse(self.call('start',request_id='x',objective='Other',target_family='not_available')['ok'])

    def test_discovery_dynamic(self):
        r=self.call('capabilities');self.assertTrue(r['ok'],r)
        for pkg in ('borrowing-costs','government-grants','investment-property'):
            row=next(x for x in r['capabilities'] if x['package']==pkg)
            self.assertFalse(row['local_fact_adapter'])

    def test_traversal(self):
        r=self.start();self.assertEqual(self.call('submit',case_id=r['case_id'],evidence_file='../anything')['error']['code'],'workspace_boundary')

    def test_symlink(self):
        r=self.start();(self.path/'link').symlink_to('/tmp')
        self.assertEqual(self.call('submit',case_id=r['case_id'],evidence_file='link/a')['error']['code'],'workspace_boundary')

    def test_malformed_wire(self):
        with self.assertRaises(ValueError):decode('{"a":1,"a":2}')
        self.assertFalse(self.api.call({'contract_version':'future'})['ok'])

    def test_staged_read_does_not_execute(self):
        r=self.start();self.assertTrue(self.call('submit',case_id=r['case_id'],evidence=evidence('fixed-assets'))['ok'])
        with patch.object(CAO, 'run', side_effect=AssertionError('read executed')):
            s=self.call('status',case_id=r['case_id'])
            self.assertTrue(s['ok']);self.assertEqual(s['currentness'],'NOT_EXECUTED')
            self.assertFalse(s['public_result'].get('calculations'))
            self.assertFalse(self.call('result',case_id=r['case_id'])['ok'])

    def test_list(self):
        r=self.start();self.assertEqual(self.call('list')['cases'],[{'case_id':r['case_id']}])


if __name__=='__main__':unittest.main()
