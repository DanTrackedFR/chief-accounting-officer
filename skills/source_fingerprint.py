"""Exact additive Profile 1.2 witness; historical artifacts are never reissued.

Only enumerated dispatcher/public-boundary additions normalize. Any changed
accounting byte, captured digest, witness, transformation or helper invalidates
legacy normalization. New source Cases bind real bytes and all new helpers.
"""
import hashlib
import json
from pathlib import Path
from prepared_fingerprint import bind_additive_mode

WITNESSES = {'skills/production.py': '039fa1731344eb053d793f3c384d77c21373952bf6b33647ff75f9a9ce3c9d12',
             'interfaces/public_output.py': '2e09cadd23751b990e9bf7d658b6bd99d58d97b2fa668b680338758ae593f60e'}
TRANSFORM_HASH = '95f66209cc7c29a9346ddb97a2d28eed888ba43b55711443e3ac311919aca1bc'
PREPARED_PIN = '1c371d847f0f86eb7eba5bb9a1b92a13250f52db4f9a09dca5f675f5d2ef0977'


class HistoricalView:
    """Read-only exact-byte view, solely after captured implementation validation."""
    def __init__(self, path, root, replacements):
        self.path = path; self.root = root; self.replacements = replacements
    def __truediv__(self, name): return HistoricalView(self.path/name,self.root,self.replacements)
    def read_bytes(self):
        relative = str(self.path.relative_to(self.root))
        return self.replacements.get(relative,self.path.read_bytes())
    def read_text(self): return self.read_bytes().decode('utf-8')
    def relative_to(self, root): return self.path.relative_to(root.path if isinstance(root,HistoricalView) else root)
    def glob(self, pattern):return [HistoricalView(p,self.root,self.replacements) for p in self.path.glob(pattern)]
    def __str__(self):return str(self.path)


def bind_source_mode(case, root, packages, files, implementation, pinned):
    output = dict(implementation)
    new = case.get('source_assurance') is not None
    extras = ['skills/source_execution.py','skills/source_screening.py','skills/source_fingerprint.py',
              'skills/presumed-sources/additive-changes.json',
              'skills/presumed-sources/release/main-7146-production.py.txt',
              'skills/presumed-sources/release/main-7146-public-output.py.txt']
    if new:
        output = bind_additive_mode(case,root,packages,files,output,PREPARED_PIN)
        for name in extras:output[name] = hashlib.sha256((root/name).read_bytes()).hexdigest()
        return output
    try:
        if hashlib.sha256((root/'skills/source_fingerprint.py').read_bytes()).hexdigest()!=pinned:return implementation
        transforms=(root/'skills/presumed-sources/additive-changes.json').read_bytes()
        if hashlib.sha256(transforms).hexdigest()!=TRANSFORM_HASH:return implementation
        replacements={}
        for name,changes in json.loads(transforms).items():
            witness='skills/presumed-sources/release/main-7146-'+('production.py.txt' if name=='skills/production.py' else 'public-output.py.txt')
            baseline=(root/witness).read_bytes()
            if hashlib.sha256(baseline).hexdigest()!=WITNESSES[name]:return implementation
            expected=baseline.decode('utf-8')
            for old,newtext in changes:
                if expected.count(old)!=1:return implementation
                expected=expected.replace(old,newtext.replace('__SOURCE_PIN__',pinned),1)
            actual=(root/name).read_bytes()
            if expected.encode()!=actual or output.get(name)!=hashlib.sha256(actual).hexdigest():return implementation
            replacements[name]=baseline
            output[name]=WITNESSES[name]
        view=HistoricalView(root,root,replacements)
        return bind_additive_mode(case,view,packages,files,output,PREPARED_PIN)
    except (OSError,ValueError,UnicodeDecodeError,KeyError):return implementation
