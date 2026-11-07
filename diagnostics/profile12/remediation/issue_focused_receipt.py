"""Execute 19 real HTTP regressions and seal a NEW bounded QA receipt, never acceptance.

Run in a committed disposable candidate checkout. The full release runner is not used.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(ROOT/'skills/presumed-sources')]
from build4.run_release import source_hashes, input_hashes
from receipt_integrity import seal_inventory, require, digest


def issue(name):
    require(name.replace('-', '').isalnum(), 'Invalid focused attempt name')
    out = ROOT/'diagnostics/profile12/remediation'/name
    require(not out.exists(), 'Preserve prior focused attempt')
    out.mkdir()
    sources, inputs = source_hashes(), input_hashes()
    for filename, value in [('start-source-hashes.json', sources), ('start-input-hashes.json', inputs)]:
        (out/filename).write_text(json.dumps(value, sort_keys=True, indent=2)+'\n')
    attempt = 'focused-governance-' + name
    temporary = ROOT/'build4/release'/attempt
    require(not temporary.exists(), 'Preserve existing runner attempt')
    command = [sys.executable, 'skills/presumed-sources/suite_runner.py', 'suite', 'diagnostics/profile12', 'regressions.py', '0']
    # The genuine bounded suite runner records actual distinct method IDs.
    with tempfile.TemporaryDirectory() as traces, (out/'suite-0.log').open('w') as log:
        process = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                 env={**os.environ, 'CAO_BUILD4_ATTEMPT': attempt, 'CAO_DIAGNOSTIC_OUT': traces})
    shutil.move(str(temporary/'suite-0.json'), out/'suite-0.json')
    temporary.rmdir()
    row = json.loads((out/'suite-0.json').read_bytes()); row['exit_code'] = process.returncode
    unchanged = sources == source_hashes() and inputs == input_hashes()
    complete = unchanged and row['passed'] and row['tests'] == 19 and process.returncode == 0 and not any(row[k] for k in ('errors','failures','skipped'))
    manifest = dict(scope='focused-governance-qa-v1', source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                    complete=complete, source_unchanged=unchanged, executed_distinct_tests=row['tests'], suite_results=[row],
                    logs=[dict(command=command, path=str((out/'suite-0.log').relative_to(ROOT)), sha256=digest(out/'suite-0.log'), exit_code=process.returncode)],
                    tested_python_sha256=sources, tested_execution_inputs_sha256=inputs)
    (out/'release-regression.json').write_text(json.dumps(manifest, sort_keys=True, indent=2)+'\n')
    require(complete, 'Focused regressions failed; retained actual evidence')
    (out/'outer.log').write_text(json.dumps(dict(scope=manifest['scope'], tests=row['tests'], complete=complete))+'\n')
    (out/'receipt-review.md').write_text('# Focused execution integrity check\n\n'
        'Automated check of 19 actual hosted diagnostic methods, zero errors/failures/skips, '
        'and unchanged before/after source maps. This is NOT independent accounting QA or release acceptance.\n')
    # Bind the original adversarial sidecar population as historical bytes, not as
    # a claim that its 3,844 tests ran on this source. Historical receipt is untouched.
    historical = json.loads((ROOT/'build4/release/presumed-sources-accepted-release.json').read_bytes())
    old_directory = (ROOT/historical['manifest']).parent
    extra = [str(p.relative_to(ROOT)) for p in old_directory.rglob('*') if p.is_file()]
    extra += ['skills/presumed-sources/release/full-regression-presumed-sources-attempt-ci-41779799873-1.log',
              'skills/presumed-sources/release/workflow-migration/receipt-review.md']
    inventory = out.parent/(name+'-inventory.json')
    pointer = seal_inventory(ROOT, out/'release-regression.json', str((out/'outer.log').relative_to(ROOT)),
                             str((out/'receipt-review.md').relative_to(ROOT)), inventory, manifest['scope'], extra)
    pointer_path = out.parent/(name+'-pointer.json')
    require(not pointer_path.exists(), 'Preserve previous pointer')
    pointer_path.write_text(json.dumps(pointer, sort_keys=True, indent=2)+'\n')
    print(str(pointer_path.relative_to(ROOT)))


if __name__ == '__main__':
    issue(sys.argv[1])
