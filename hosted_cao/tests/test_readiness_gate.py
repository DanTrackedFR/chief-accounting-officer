"""Independent executable adversarial tests of exact-head CI readiness reuse."""
import io
import json
import os
from pathlib import Path
import tempfile
import textwrap
import unittest
from unittest.mock import patch

WORKFLOW=Path(__file__).resolve().parents[2]/'.github/workflows/cao-orchestration.yml'
SCRIPT=textwrap.dedent(WORKFLOW.read_text().split("python - <<'PYCODE'\n",1)[1].split('          PYCODE',1)[0])
NAMES={'Orchestration authored and independent QA','Hosted service authored and independent QA','Local execution authored and independent QA','Existing skills and lease vertical slice','Repository public-output and canonical tests','Supplemental knowledge and independent knowledge QA','Canonical authority invariants and whitespace','Build 3 intelligence and deterministic integrated proof'}
SHA='a'*40

class IndependentReadinessGateQA(unittest.TestCase):
    def execute(self,runs=None,jobs=None,action='ready_for_review',failure=False):
        self.urls=[]
        current={'id':1,'workflow_id':99,'head_sha':SHA}
        prior={'id':2,'workflow_id':99,'head_sha':SHA,'status':'completed','conclusion':'success'}
        runs=[prior] if runs is None else runs
        jobs=[{'steps':[{'name':name,'conclusion':'success'} for name in NAMES]}] if jobs is None else jobs
        def urlopen(request,timeout):
            self.urls.append(request.full_url)
            if failure:raise OSError('API unavailable')
            if request.full_url.endswith('/actions/runs/1'):value=current
            elif '/actions/runs?' in request.full_url:value={'workflow_runs':runs}
            elif request.full_url.endswith('/jobs'):value={'jobs':jobs}
            else:raise AssertionError(request.full_url)
            return io.BytesIO(json.dumps(value).encode())
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/'out'
            env={'GITHUB_REPOSITORY':'DanTrackedFR/chief-accounting-officer','GITHUB_RUN_ID':'1','HEAD_SHA':SHA,'EVENT_ACTION':action,'GH_TOKEN':'synthetic-only','GITHUB_OUTPUT':str(output)}
            with patch.dict(os.environ,env),patch('urllib.request.urlopen',urlopen),patch('sys.stdout',io.StringIO()):exec(SCRIPT,{})
            return output.read_text().strip()
    def test_full_prior_exact_head_can_reuse(self):self.assertEqual(self.execute(),'cached=true')
    def test_nonreadiness_never_reuses_even_success(self):
        for action in ('synchronize','opened','', 'reopened'):
            self.assertEqual(self.execute(action=action),'cached=false');self.assertEqual(self.urls,[])
    def test_api_error_fails_closed(self):self.assertEqual(self.execute(failure=True),'cached=false')
    def test_other_sha_or_workflow_or_current_id_never_reuses(self):
        base={'id':2,'workflow_id':99,'head_sha':SHA,'status':'completed','conclusion':'success'}
        for field,value in [('head_sha','b'*40),('workflow_id',100),('id',1)]:self.assertEqual(self.execute(runs=[{**base,field:value}]),'cached=false')
    def test_failed_or_unfinished_prior_never_reuses(self):
        base={'id':2,'workflow_id':99,'head_sha':SHA,'status':'completed','conclusion':'success'}
        for field,value in [('status','in_progress'),('conclusion','failure'),('conclusion','cancelled')]:self.assertEqual(self.execute(runs=[{**base,field:value}]),'cached=false')
    def test_each_missing_failed_skipped_step_requires_full_run(self):
        for omitted in NAMES:
            for conclusion in (None,'skipped','failure','cancelled'):
                steps=[{'name':name,'conclusion':'success' if name!=omitted else conclusion} for name in NAMES]
                self.assertEqual(self.execute(jobs=[{'steps':steps}]),'cached=false')
    def test_cached_readiness_with_all_steps_skipped_cannot_chain_reuse(self):
        jobs=[{'steps':[{'name':name,'conclusion':'skipped'} for name in NAMES]}]
        self.assertEqual(self.execute(jobs=jobs),'cached=false')
    def test_empty_malformed_proof_fails_closed(self):
        self.assertEqual(self.execute(runs=[]),'cached=false')
        self.assertEqual(self.execute(jobs=[]),'cached=false')
        self.assertEqual(self.execute(jobs=[{'steps':[{'name':'arbitrary','conclusion':'success'}]}]),'cached=false')

if __name__=='__main__':unittest.main()
