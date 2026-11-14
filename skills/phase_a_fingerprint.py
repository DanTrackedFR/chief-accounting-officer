"""Bounded post-merge additive public bridge; historical receipts remain immutable.

Legacy bytes normalize only after exact live-byte, witness and helper checks.
Profile1.2 always binds the corrected implementation, not the historical receipt.
"""
import hashlib
from source_fingerprint import bind_source_mode, HistoricalView

BASE_PRODUCTION = '1283de1ef0a03808095284d734f574462567d624ffcf6aba7023a0e99ee6e16f'
BASE_PUBLIC = '5b3757864ed981be6cbd7f231ec159fb2215f86b82b6b656b4f6955560fbf1fe'
CURRENT_PUBLIC = '735edcaee74f060a5826ae14070b0db5d11b80272dbf8d0954346a757aca4876'
OLD = "    from source_fingerprint import bind_source_mode\n    implementation = bind_source_mode(case, ROOT, PACKAGES, files, implementation, '7011aa04c86f51184354a05e97ab3fceee9036c6a2649761f66135f7ed04ddd2')"
NEW = "    from phase_a_fingerprint import bind_phase_a\n    implementation = bind_phase_a(case, ROOT, PACKAGES, files, implementation, '__PHASE_A_PIN__')"
SOURCE_PIN = '7011aa04c86f51184354a05e97ab3fceee9036c6a2649761f66135f7ed04ddd2'


def bind_phase_a(case,root,packages,files,implementation,pinned):
    if case.get('source_assurance') is not None:
        output=bind_source_mode(case,root,packages,files,implementation,SOURCE_PIN)
        for name in ('skills/phase_a_fingerprint.py','interfaces/source-case.schema.json'):
            output[name]=hashlib.sha256((root/name).read_bytes()).hexdigest()
        return output
    try:
        if hashlib.sha256((root/'skills/phase_a_fingerprint.py').read_bytes()).hexdigest()!=pinned:return implementation
        replacements={}
        for name,expected in (('skills/production.py',BASE_PRODUCTION),('interfaces/public_output.py',BASE_PUBLIC)):
            baseline=(root/'skills/phase-a-compatibility'/('accepted-main-'+name.split('/')[-1]+'.txt')).read_bytes()
            if hashlib.sha256(baseline).hexdigest()!=expected:return implementation
            actual=(root/name).read_bytes()
            if implementation.get(name)!=hashlib.sha256(actual).hexdigest():return implementation
            if name=='skills/production.py':
                text=baseline.decode()
                if text.count(OLD)!=1 or actual!=text.replace(OLD,NEW.replace('__PHASE_A_PIN__',pinned),1).encode():return implementation
            elif hashlib.sha256(actual).hexdigest()!=CURRENT_PUBLIC:return implementation
            replacements[name]=baseline
        output=dict(implementation)
        for name,value in replacements.items():output[name]=hashlib.sha256(value).hexdigest()
        return bind_source_mode(case,HistoricalView(root,root,replacements),packages,files,output,SOURCE_PIN)
    except (OSError,ValueError,UnicodeDecodeError,KeyError):return implementation
