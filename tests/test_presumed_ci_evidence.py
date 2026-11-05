"""Run the two CI evidence writers repeatedly against a small synthetic repository."""
import hashlib
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

            for runner in ('intelligence/tests/run_release.py', 'build4/run_release.py',
                           'skills/presumed-sources/run_release.py',
                           'skills/presumed-sources/execute_release.py',
                           'skills/presumed-sources/verify_release.py',
                           'skills/presumed-sources/receipt_integrity.py'):
                write(runner, (ROOT / runner).read_bytes())
            # The genuine runner checks access to historical commits. Borrow the
            # existing read-only object database, keeping all output in the fixture.
            subprocess.run(['git', 'init', '-q'], cwd=root, check=True)
            objects = subprocess.check_output(
                ['git', 'rev-parse', '--path-format=absolute', '--git-path', 'objects'],
                cwd=ROOT, text=True).strip()
            env = {**os.environ, 'GIT_ALTERNATE_OBJECT_DIRECTORIES': objects,
                   'PYTHONPATH': str(root), 'PATH': str(Path(sys.executable).parent) + os.pathsep + os.environ['PATH']}
            suites = ['orchestration/tests', 'knowledge/borrowing-costs', 'hosted_cao/tests',
                      'intelligence/tests', 'build4/tests', 'knowledge/government-grants',
                      'knowledge/investment-property']
            for suite in suites:
                write(f'{suite}/test_canary.py', b'import unittest\nclass Canary(unittest.TestCase):\n'
                      b'    def test_canary(self):\n        self.assertTrue(True)\n')
            for name in ('borrowing-costs', 'government-grants', 'investment-property'):
                write(f'knowledge/{name}/validate_supplement.py', b'print("synthetic validator")\n')
            write('local_cao/release/release-regression.json', json.dumps({
                'suite_results': [{'suite': suites[0], 'pattern': 'test_*.py'}], 'validators': []
            }).encode())

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
                self.assertEqual(json.loads(receipt.read_bytes())['executed_distinct_tests'], len(suites))
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
