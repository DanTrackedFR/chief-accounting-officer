"""One JSON request on stdin; one versioned response on stdout."""
import argparse
import json
import sys
from .adapter import ExecutionInterface, decode, MAX_BYTES, ERRORS
from interfaces.public_output import public_record


def main():
    p = argparse.ArgumentParser(description='Local governed CAO execution contract')
    p.add_argument('--workspace', default='.cao-local')
    args = p.parse_args()
    try:
        text = sys.stdin.read(MAX_BYTES+1)
        if len(text.encode()) > MAX_BYTES: raise ValueError('Request limit')
        result = ExecutionInterface(args.workspace).call(decode(text))
    except (ValueError, TypeError, OSError, RecursionError):
        result = dict(contract_version='1.0', ok=False,
            error=dict(code='invalid_request', message=ERRORS['invalid_request']),
            public_result=public_record(dict(status='blocked', guidance=ERRORS['invalid_request']), route='tool_output'))
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))
    return 0 if result['ok'] else 2


if __name__ == '__main__': sys.exit(main())
