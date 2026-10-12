"""Strict byte-audited additive dispatch bridge; never refresh existing certification.

Only the enumerated Investment Property dispatcher additions are neutral for other
owners. Any common-byte change, witness tamper or helper tamper fails normalization.
"""
import hashlib
from pathlib import Path
from implementation_scope import owners
BASELINE_SHA = '10a34f9fcbe28bb291373fe9c640470ee8bd1202b46590ec66a2a2105d28dfb4'
CHANGES = [("'investment-property': ('SKILL-IP-001',['TOPIC-04-001']),", "'investment-property': ('SKILL-IP-001',['SUPPLEMENTAL_INVESTMENT_PROPERTY']),"), ('def canonical_knowledge(topic_ids, framework, package=None):\n', "def canonical_knowledge(topic_ids, framework, package=None):\n    if topic_ids == ['SUPPLEMENTAL_INVESTMENT_PROPERTY']:\n        from investment_knowledge import mapped_knowledge\n        return mapped_knowledge(framework)\n"), ("    if package=='investment-property':raise ReviewRequired('NONPRODUCTION: approved PPE knowledge supplies a classification boundary only; investment-property definition, model, transfer and framework-specific recognition/measurement methods are absent')\n", "    if package=='investment-property' and (not isinstance(case,dict) or case.get('skill_version')!='1.0.0'):\n        raise ReviewRequired('NONPRODUCTION: approved PPE knowledge supplies a classification boundary only; investment-property definition, model, transfer and framework-specific recognition/measurement methods are absent')\n"), ("if package in ('borrowing-costs','government-grants') and result['status']!='complete':", "if package in ('borrowing-costs','government-grants','investment-property') and result['status']!='complete':"), ('    implementation={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}\n', "    implementation={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}\n    # Exact reviewed additive dispatch bridge; common accounting edits still invalidate.\n    bridge_path = ROOT/'skills/investment_fingerprint.py'\n    if hashlib.sha256(bridge_path.read_bytes()).hexdigest() == '__HELPER_HASH__':\n        from investment_fingerprint import bind_investment_dispatch\n        implementation = bind_investment_dispatch(case, ROOT, PACKAGES, files, implementation)\n"), ("    if result['skill_id']=='SKILL-BORROW-001':title=", "    if result['skill_id']=='SKILL-IP-001':title={'IFRS':'IAS 40 owned property','AASB':'AASB 140 Tier 1 owned property','UK_GAAP':'FRS 102 Section 16 owned property','US_GAAP':'Ordinary US historical-cost real estate'}.get(result['framework'],'Property framework unresolved')\n    if result['skill_id']=='SKILL-BORROW-001':title=")]

def expected_dispatch(baseline, helper_hash):
    out=baseline
    for old,new in CHANGES:
        if out.count(old)!=1:raise ValueError('Ambiguous baseline transformation')
        out=out.replace(old,new.replace('__HELPER_HASH__',helper_hash),1)
    return out

def bind_investment_dispatch(case, root, packages, files, implementation):
    selected=owners(case,packages)
    output=dict(implementation)
    helper=root/'skills/investment_fingerprint.py'
    witness=root/'skills/investment-property/fingerprint-baseline/main-e753-production.py.txt'
    try:
        baseline_bytes=witness.read_bytes()
        baseline=baseline_bytes.decode('utf-8')
        helper_hash=hashlib.sha256(helper.read_bytes()).hexdigest()
        if hashlib.sha256(baseline_bytes).hexdigest()!=BASELINE_SHA:return output
        dispatcher_bytes=(root/'skills/production.py').read_bytes()
        if dispatcher_bytes!=expected_dispatch(baseline,helper_hash).encode('utf-8'):return output
        if output.get('skills/production.py')!=hashlib.sha256(dispatcher_bytes).hexdigest():return output
    except (OSError,ValueError,UnicodeDecodeError):return output
    if 'investment-property' not in selected:
        output['skills/production.py']=BASELINE_SHA
    else:
        additions=[helper,witness,root/'skills/investment_knowledge.py']
        additions+=list((root/'knowledge/investment-property').glob('*.py'))
        for path in additions:output[str(path.relative_to(root))]=hashlib.sha256(path.read_bytes()).hexdigest()
    return output
