"""Exact additive compatibility witness; no historical recertification.

Normalize only the enumerated opt-in dispatch and enum allowlist additions.
Any other common-byte change, helper change or witness change invalidates seals.
Prepared Cases always bind current bytes plus the new bounded implementation.
"""
import hashlib
from implementation_scope import owners
CHANGES = [('def execute(package, case):', "def execute(package, case, *, allow_prepared_unreviewed=False):\n    mode = case.get('review_mode', 'formal') if isinstance(case, dict) else 'formal'\n    if mode == 'prepared_unreviewed':\n        if allow_prepared_unreviewed is not True: raise ReviewRequired('System preparation is disabled by host configuration')\n        from prepared_execution import execute as prepare\n        return prepare(package, case)\n    if mode != 'formal': raise ReviewRequired('Unknown accounting review mode')\n    if isinstance(case, dict) and any(tag in json.dumps(case, default=str) for tag in ('SYSTEM_DERIVED_NOT_A_REVIEWER', 'SYSTEM_DERIVED', 'SYSTEM_PREPARED')):\n        raise ReviewRequired('System provenance cannot satisfy formal reviewer requirements')"), ("    payload={'case':", "    from prepared_fingerprint import bind_additive_mode\n    implementation = bind_additive_mode(case, ROOT, PACKAGES, files, implementation, '__HELPER_HASH__')\n    payload={'case':"), ("def to_public(result, route='answer'):\n", "def to_public(result, route='answer'):\n    if result.get('review_mode') == 'prepared_unreviewed':\n        from prepared_execution import to_public as prepared_public\n        return prepared_public(result, route)\n"), ('def assess_case(package,case):', 'def assess_case(package,case, *, allow_prepared_unreviewed=False):'), ('    try:return execute(package,case)', '    try:return execute(package,case,allow_prepared_unreviewed=allow_prepared_unreviewed)'), ("        return {'skill_id':PACKAGES[package][0],'status':'blocked','conclusion':'Accounting case cannot be completed: '+reason,", "        blocked = {'skill_id':PACKAGES[package][0],'status':'blocked','conclusion':'Accounting case cannot be completed: '+reason,"), ("; rerun case with new fingerprint'}}\n", "; rerun case with new fingerprint'}}\n\n        if case.get('review_mode') == 'prepared_unreviewed':\n            blocked.update(review_mode='prepared_unreviewed', accounting_determination='UNRESOLVED',\n                evidence_sufficiency='INSUFFICIENT', review_provenance='SYSTEM_PREPARED')\n        return blocked\n")]
PUBLIC_CHANGE = ('    # Citation fields are curated independently; never pass a claim/source object.', "    for key, allowed in {\n        'accounting_determination': ('SUPPORTED', 'UNRESOLVED', 'UNSUPPORTED'),\n        'evidence_sufficiency': ('SUFFICIENT', 'INSUFFICIENT'),\n        'review_provenance': ('SYSTEM_PREPARED', 'FORMALLY_REVIEWED'),\n    }.items():\n        if key in record:\n            if record[key] not in allowed: raise ValueError('Invalid accounting provenance status')\n            result[key] = record[key]\n    # Citation fields are curated independently; never pass a claim/source object.")
BASE_SHA = '719c6b533d2e81a216ca158a9fa3bb880c2f72fe77ad38ee682f244a390fa50c'
PUBLIC_SHA = '240aead226b7913712c13dc2af8b0f22dc8d5a6c17e8f7fb26f5f343539ad35b'


def expected_prepared_dispatch(baseline, pinned):
    expected = baseline
    for old, new in CHANGES:
        if expected.count(old) != 1: raise ValueError('Ambiguous additive transformation')
        expected = expected.replace(old, new.replace('__HELPER_HASH__', pinned), 1)
    return expected


def bind_additive_mode(case, root, packages, files, implementation, pinned):
    output = dict(implementation)
    prepared = case.get('review_mode') == 'prepared_unreviewed'
    extra = [root/'skills/prepared_execution.py', root/'skills/prepared_fingerprint.py']
    if prepared:
        for path in extra: output[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
        from production import canonical_knowledge, PACKAGES
        import json
        # Both authorized package populations are fixed and privately bound;
        # this avoids guessing an absent legacy owner from workpaper amounts.
        for package in ('fixed-assets', 'accounts-payable'):
            claims, documents = canonical_knowledge(PACKAGES[package][1], case.get('framework'), package=package)
            output['prepared-canonical-' + package] = hashlib.sha256(json.dumps([claims, documents], sort_keys=True).encode()).hexdigest()
        return output
    try:
        helper = root/'skills/prepared_fingerprint.py'
        if hashlib.sha256(helper.read_bytes()).hexdigest() != pinned: return output
        witness = root/'skills/prepared-accounting/release/main-fbf8-production.py.txt'
        baseline_bytes = witness.read_bytes()
        if hashlib.sha256(baseline_bytes).hexdigest() != BASE_SHA: return output
        baseline = baseline_bytes.decode('utf-8')
        actual = (root/'skills/production.py').read_bytes()
        if actual != expected_prepared_dispatch(baseline, pinned).encode('utf-8'): return output
        if output.get('skills/production.py') != hashlib.sha256(actual).hexdigest(): return output
        public = root/'skills/prepared-accounting/release/main-fbf8-public-output.py.txt'
        public_bytes = public.read_bytes()
        if hashlib.sha256(public_bytes).hexdigest() != PUBLIC_SHA: return output
        public_text = public_bytes.decode('utf-8')
        old, new = PUBLIC_CHANGE
        actual_public = (root/'interfaces/public_output.py').read_bytes()
        if public_text.count(old) != 1 or actual_public != public_text.replace(old, new, 1).encode('utf-8'): return output
        if output.get('interfaces/public_output.py') != hashlib.sha256(actual_public).hexdigest(): return output
        output['skills/production.py'] = BASE_SHA
        output['interfaces/public_output.py'] = PUBLIC_SHA
        # Reproduce the already approved Investment Property bridge against the
        # exact original dispatcher; it deliberately fails on changed bytes.
        from investment_fingerprint import BASELINE_SHA, expected_dispatch
        bridge = root/'skills/investment_fingerprint.py'
        old_witness = root/'skills/investment-property/fingerprint-baseline/main-e753-production.py.txt'
        bridge_hash = hashlib.sha256(bridge.read_bytes()).hexdigest()
        if bridge_hash != 'a32b9ef41680e8d649d7b3770d0db02ae400613d4337e8e266c29f123e5e8c1b': return implementation
        if hashlib.sha256(old_witness.read_bytes()).hexdigest() != BASELINE_SHA or expected_dispatch(old_witness.read_bytes().decode('utf-8'), bridge_hash) != baseline: return implementation
        if 'investment-property' not in owners(case, packages):
            output['skills/production.py'] = BASELINE_SHA
        else:
            additions = [bridge, old_witness, root/'skills/investment_knowledge.py'] + list((root/'knowledge/investment-property').glob('*.py'))
            for path in additions: output[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    except (OSError, ValueError, UnicodeDecodeError): return implementation
    return output
