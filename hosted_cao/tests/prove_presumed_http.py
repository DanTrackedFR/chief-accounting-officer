"""Repeatable actual HTTP numerical proof using explicitly synthetic 27/10 inputs."""
import hashlib
import json
from collections import Counter
from unittest.mock import patch
from hosted_cao.tests.test_presumed_engineering_qa import IndependentPresumedEngineeringQA, PROFILE
from orchestration.runtime import CAO


def proof():
    fixture=IndependentPresumedEngineeringQA('test_real_http_27_machinery_rows_and_10_invoices')
    fixture.setUp()
    try:
        rows=[]
        for package,count in [('fixed-assets',27),('accounts-payable',10)]:
            cid,done=fixture.complete(package,package)
            public=done['accounting']['public_result']
            status,retry=fixture.job(cid,package)
            assert status==202 and retry['id']==done['id']
            fixture.service.close();fixture.service=fixture.new_service();fixture.server.service=fixture.service
            with patch.object(CAO,'run',side_effect=AssertionError('Restart must use persisted result')):
                status,recovered=fixture.http('/v1/jobs/'+done['id'])
            assert status==200 and recovered['accounting']['public_result']==public
            native,result=fixture.native(cid)
            assert result['status']=='partial' and result['source_assurance']==PROFILE
            rows.append(dict(package=package,synthetic_records=count,calculations=public['calculations'],
                checks=dict(sorted(Counter(f['severity'] for f in public['anomaly_report']['findings']).items())),
                population_status=public['anomaly_report']['population_status'],validation_requirements=public['validation_requirements'],
                review_provenance=public['review_provenance'],source_provenance=public['source_provenance'],
                public_sha256=hashlib.sha256(json.dumps(public,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
                restart_equal=True,idempotent_retry_equal=True,native_status=result['status']))
        status,invalid=fixture.http('/v1/jobs',fixture.envelope('execute'),**{'Idempotency-Key':'malformed'})
        assert status==400 and invalid['error']['code']=='invalid_request'
        assert any(x['field_path']=='case_id' for x in invalid['error']['requirements'])
        return dict(profile=PROFILE,input_origin='Representative synthetic fixtures; TrackedFR separately retests original contract-probe files.',
                    executions=rows,malformed_case_binding=invalid['error'])
    finally:fixture.doCleanups()

if __name__=='__main__':print(json.dumps(proof(),sort_keys=True,indent=2))
