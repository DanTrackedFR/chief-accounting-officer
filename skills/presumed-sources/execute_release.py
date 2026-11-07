"""Execute a new regression, or explicitly verify/reuse acceptance. Never issue it."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from receipt_integrity import require

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from build4.verify_release import verify


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reuse', help='Explicit version-2 acceptance pointer; invalid evidence aborts')
    args = parser.parse_args()
    attempt = os.environ.get('CAO_SOURCES_ATTEMPT', '')
    require(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]*', attempt) is not None,
            'Set a new unique CAO_SOURCES_ATTEMPT')
    out = ROOT / 'build4/release' / attempt
    log = ROOT / 'skills/presumed-sources/release' / ('full-regression-' + attempt + '.log')
    require(out.resolve() == out and log.resolve() == log, 'Output path redirected')
    require(not out.exists() and not log.exists(), 'Preserve prior attempt; choose a new CAO_SOURCES_ATTEMPT')
    if args.reuse is not None:
        # No existence-only, source-hash-only, or historical-version fallback.
        result = verify(args.reuse)
        out.mkdir()
        status = dict(status='ACCEPTANCE_REUSED', acceptance_pointer=args.reuse,
                      verification=result, release_accepted=True)
    else:
        # Exclusive open prevents shell redirection from truncating old evidence.
        with log.open('x') as stream:
            code = subprocess.run([sys.executable, str(ROOT/'skills/presumed-sources/run_release.py')],
                                  cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT).returncode
        if code:
            raise SystemExit(code)
        status = dict(status='REGRESSION_COMPLETE_ACCEPTANCE_PENDING', release_accepted=False,
                      manifest=str((out/'release-regression.json').relative_to(ROOT)))
    with (out/'execution.json').open('x') as stream:
        stream.write(json.dumps(status, sort_keys=True, indent=2) + '\n')
    print(json.dumps(status, sort_keys=True))


if __name__ == '__main__':
    main()
