"""Run the two CI evidence writers repeatedly against a small synthetic repository."""
import hashlib
import importlib.util
import shutil
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / '.github/workflows'


def workflow_command(workflow, step):
    body = workflow.split(f'      - name: {step}\n', 1)[1].split('      - name:', 1)[0]
    command = body.split('        run: ', 1)[1]
    return textwrap.dedent(command[2:]) if command.startswith('|\n') else command.strip()


class IndependentCIEvidenceIsolationQA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('ci_synthetic_contract',
            ROOT/'tests/fixtures/phase_a_v1/runner.py')
        fixture = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fixture)
        cls.contract = fixture.IndependentRunnerContract
        cls.contract.setUpClass()
        cls.addClassCleanup(cls.contract.doClassCleanups)

    def test_retry_and_separate_run_preserve_original_and_prior_attempt_bytes(self):
        orchestration = (WORKFLOWS / 'cao-orchestration.yml').read_text()
        source = (WORKFLOWS / 'cao-presumed-sources.yml').read_text()
        shard_command = workflow_command(orchestration, 'Orchestration authored and independent QA')
        release_command = workflow_command(source, 'Execute new regression or explicitly verify accepted evidence')
        attempt_template = re.search(r'^ +CAO_SOURCES_ATTEMPT: (.+)$', source, re.M).group(1)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)

            def write(name, data):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
                return path

            shutil.copytree(self.contract.base, root, dirs_exist_ok=True)
            env = dict(self.contract.env, PYTHONPATH=str(root),
                       PATH=str(Path(sys.executable).parent)+os.pathsep+os.environ['PATH'])
            self.assertEqual((root/'intelligence/tests/run_release.py').read_bytes(),
                             (ROOT/'intelligence/tests/run_release.py').read_bytes())
            self.assertFalse(list(root.rglob('*.pyc')))

            protected = {}
            for historical in ('intelligence/release/ci-orchestration-module-0.log',
                               'intelligence/release/suite-ci-orchestration-module-0.json',
                               'intelligence/release/suite-ci-orchestration.json',
                               'skills/presumed-sources/release/full-regression-attempt-ci.log',
                               'build4/release/presumed-sources-attempt-ci/release-regression.json'):
                protected[write(historical, b'untouched canary\x00\r\n')] = b'untouched canary\x00\r\n'

            pointer = write('build4/release/presumed-sources-accepted-release.json',
                            (ROOT/'build4/release/presumed-sources-accepted-release.json').read_bytes())
            protected[pointer] = pointer.read_bytes()
            subprocess.run(['git','add','.'],cwd=root,env=env,check=True)
            subprocess.run(['git','-c','user.name=Synthetic QA','-c','user.email=synthetic@example.invalid','commit','-qm','CI isolation fixture'],cwd=root,env=env,check=True)
            env['GITHUB_EVENT_NAME'] = 'workflow_dispatch'
            env['CAO_ACCEPTANCE_POINTER'] = ''
            for run_id, retry in [('123', '1'), ('123', '2'), ('124', '1')]:
                attempt = attempt_template.replace('${{ github.run_id }}', run_id).replace(
                    '${{ github.run_attempt }}', retry)
                env.update(GITHUB_RUN_ID=run_id, GITHUB_RUN_ATTEMPT=retry, CAO_SOURCES_ATTEMPT=attempt)
                for command in (shard_command, release_command):
                    process = subprocess.run(['bash', '-e', '-c', command], cwd=root, env=env,
                                             capture_output=True, text=True, timeout=60)
                    for artifact, original in protected.items():
                        self.assertEqual(artifact.read_bytes(), original, str(artifact))
                    self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
                record = json.loads((root/'build4/release'/attempt/'execution.json').read_bytes())
                self.assertFalse(record['release_accepted'])
                self.assertEqual(record['status'], 'REGRESSION_COMPLETE_ACCEPTANCE_PENDING')
                receipt = root / record['manifest']
                self.assertEqual(receipt.parent.name, attempt)
                self.assertEqual(json.loads(receipt.read_bytes())['executed_distinct_tests'], 136)
                shard = root / f'intelligence/release/suite-ci-orchestration-{run_id}-{retry}.json'
                shard_record = json.loads(shard.read_bytes())['module_results'][0]
                self.assertEqual(shard_record['tests'], 1)
                self.assertEqual(hashlib.sha256((root / shard_record['log']).read_bytes()).hexdigest(),
                                 shard_record['log_sha256'])
                outer_log = root / f'skills/presumed-sources/release/full-regression-{attempt}.log'
                self.assertTrue(json.loads(outer_log.read_text().splitlines()[-1])['complete'])
                for folder in ('build4/release', 'intelligence/release', 'skills/presumed-sources/release'):
                    for artifact in (root / folder).rglob('*'):
                        if artifact.is_file() and artifact != pointer:
                            protected[artifact] = artifact.read_bytes()
                # Repeating an identical run/attempt must fail without truncating any output.
                retry = subprocess.run(['bash', '-e', '-c', release_command], cwd=root, env=env,
                                       capture_output=True, text=True, timeout=60)
                self.assertNotEqual(retry.returncode, 0)
                for artifact, original in protected.items():
                    self.assertEqual(artifact.read_bytes(), original, str(artifact))

    def test_event_routing_with_executed_synthetic_receipt(self):
        source = (WORKFLOWS / 'cao-presumed-sources.yml').read_text()
        command = workflow_command(source, 'Execute new regression or explicitly verify accepted evidence')
        helper = self.contract()
        helper.setUp()
        self.addCleanup(helper.tearDown)
        root = helper.root
        pointer = 'build4/release/qa-pointer-v2.json'
        receipt = root / pointer
        shutil.copyfile(root / 'build4/release/qa-pointer.json', receipt)
        checksum = hashlib.sha256(receipt.read_bytes()).hexdigest()
        attempt_number = 0

        def route(expected_error=None, event='pull_request', action='ready_for_review',
                  manual='', selected=pointer, digest=checksum, optimize='0'):
            nonlocal attempt_number
            attempt_number += 1
            attempt = f'qa-routing-{attempt_number}'
            env = dict(self.contract.env, GITHUB_EVENT_NAME=event, CAO_PR_ACTION=action,
                       CAO_ACCEPTANCE_POINTER=manual, CAO_PR_POINTER=selected,
                       CAO_PR_POINTER_SHA256=digest, CAO_SOURCES_ATTEMPT=attempt,
                       PYTHONOPTIMIZE=optimize, PYTHONPATH=str(root),
                       PATH=str(Path(sys.executable).parent)+os.pathsep+os.environ['PATH'])
            result = subprocess.run(['bash', '-e', '-o', 'pipefail', '-c', command],
                                    cwd=root, env=env, capture_output=True, text=True, timeout=60)
            out = root / 'build4/release' / attempt
            # The runner exclusively creates this log before launching even one suite.
            self.assertFalse((root / 'skills/presumed-sources/release' /
                              f'full-regression-{attempt}.log').exists())
            if expected_error:
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn(expected_error, result.stderr + result.stdout)
                self.assertFalse(out.exists())
            else:
                self.assertEqual(result.returncode, 0, result.stderr)
                status = json.loads((out / 'execution.json').read_bytes())
                self.assertEqual(status['status'], 'ACCEPTANCE_REUSED')
                self.assertIs(status['release_accepted'], True)
                self.assertEqual(status['verification']['distinct_tests'], 136)

        route(event='workflow_dispatch', manual=pointer)
        route('Missing or redirected evidence', event='workflow_dispatch', manual='absent')
        for action in ('ready_for_review', 'synchronize', 'opened', 'reopened'):
            with self.subTest(action=action):
                route(action=action)
                route('are required', action=action, selected='', manual=pointer)
        route('Unsupported release event', event='push')
        route('Unsupported PR action', action='edited')
        route('No such file', selected='build4/release/missing-v2.json')
        route('are required', digest='')
        route('are required', selected='../outside-v2.json')
        route('FAILED', digest='0' * 64)
        for optimize in ('1', '2'):
            route('Optimized Python is not supported', optimize=optimize)

        original = receipt.read_bytes()
        receipt.write_bytes(original + b' ')
        route('FAILED')
        historical = json.loads(original)
        historical['schema_version'] = 1
        receipt.write_text(json.dumps(historical))
        route('version 2 evidence inventory', digest=hashlib.sha256(receipt.read_bytes()).hexdigest())
        receipt.write_bytes(original)

        canary = root / 'tests/test_canary.py'
        original_canary = canary.read_bytes()
        canary.write_bytes(original_canary + b'\n')
        route('Python changed')
        canary.write_bytes(original_canary)
        workflow = root / '.github/workflows/cao-presumed-sources.yml'
        workflow.parent.mkdir(parents=True, exist_ok=True)
        previous_workflow = workflow.read_bytes() if workflow.exists() else None
        workflow.write_text(source)
        route('execution inputs changed')
        if previous_workflow is None:
            workflow.unlink()
        else:
            workflow.write_bytes(previous_workflow)
        manifest = root / json.loads(original)['manifest']
        manifest.write_bytes(manifest.read_bytes() + b' ')
        route('manifest hash differs')
