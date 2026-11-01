"""Deterministic real-HTTP optional-review proof; synthetic evidence only."""
import json
from pathlib import Path
from hosted_cao.tests.test_prepared_engineering_qa import (
    IndependentPreparedEngineeringQA, COMPANY, MODE,
)
from local_cao.adapter import ExecutionInterface
from orchestration.runtime import CAO
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]


def prove():
    fixture = IndependentPreparedEngineeringQA()
    fixture.setUp()
    rows = []
    try:
        for package, amount in [('fixed-assets', '90000.00'), ('accounts-payable', '9600')]:
            cid, job = fixture.execute(package, 'proof-'+package)
            response = job['accounting']
            api = ExecutionInterface(fixture.workspace, allow_prepared_unreviewed=True)
            with api._store() as store:
                native, revision, _ = store.load(COMPANY, cid)
                owners = [node for node in native.graph.nodes.values()
                          if node.selected_skill == package]
                assert len(owners) == 1
                owner = owners[0]
                result = owner.result
                assert result['status'] == 'partial'
                assert result['review_provenance'] == 'SYSTEM_PREPARED'
                assert result['accounting_determination'] == 'SUPPORTED'
                assert not {'knowledge_review', 'applicability_review', 'reviewer_signoff'} & result['facts_used'].keys()
                assert not {'knowledge_review', 'reviewer_signoff'} & result.keys()
                assert not result['journal_entry_implications']
                assert result['proposed_journal_workpaper']
                assert not native.governance.versions.active
                assert 'SYSTEM_DERIVED_NOT_A_REVIEWER' not in json.dumps(result, default=str)
            restarted = fixture.new_service(True)
            try:
                with patch.object(CAO, 'run', side_effect=AssertionError('Restored accounting must not rerun')):
                    recovered = restarted.job(COMPANY, job['id'])
                    local = api.call(fixture.envelope('resume', case_id=cid))
                assert recovered['accounting']['public_result'] == response['public_result']
                assert local['public_result'] == response['public_result']
                assert amount in json.dumps(response['public_result'])
            finally:
                restarted.close()
            rows.append(dict(package=package, review_mode=MODE,
                http_sequence=['initialize:200', 'start:200', 'submit:200',
                               'POST /v1/jobs:202', 'GET /v1/jobs:200'],
                operational_job_state=job['state'], native_owner_status=result['status'],
                native_case_status=response['lifecycle_state'],
                checkpoint_revision=revision, native_formal_result_versions=0,
                fabricated_execution_review=False, journal_posting_authorized=False,
                restart_without_execution=True, local_hosted_public_parity=True,
                public_result=response['public_result']))
        return dict(proof='Synthetic real HTTP governed accounting execution', packages=rows)
    finally:
        fixture.doCleanups()


if __name__ == '__main__':
    print(json.dumps(prove(), indent=2, sort_keys=True))
