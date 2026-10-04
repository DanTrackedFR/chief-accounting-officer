"""Read governed metadata, never mirror the 50-skill roadmap."""
import csv
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills'))
import production


def metadata(path):
    """Parse the repository's deliberately bounded frontmatter without dependencies.

    Reject unsupported YAML constructs rather than interpreting guessed metadata.
    """
    text = path.read_text()
    if not text.startswith('---\n'):
        raise ValueError('Skill frontmatter missing')
    block = text.split('---', 2)[1]
    out = {}; parent = None
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith('#'): continue
        key, sep, raw = line.strip().partition(':')
        if not sep: raise ValueError('Unsupported metadata line')
        raw = raw.strip()
        if raw.startswith('[') and raw.endswith(']'):
            value = next(csv.reader([raw[1:-1]], skipinitialspace=True)) if raw != '[]' else []
            value = [s.strip().strip('"\'') for s in value]
        elif raw in ('true', 'false'): value = raw == 'true'
        elif not raw: value = {}
        else: value = raw.strip('"\'')
        if line.startswith(' '):
            if parent is None or not isinstance(out[parent], dict): raise ValueError('Unsupported nested metadata')
            out[parent][key] = value
        else:
            out[key] = value; parent = key
    return out


class Registry:
    def __init__(self, root=ROOT):
        self.skills = {}
        for path in sorted((root / 'skills').glob('*/SKILL.md')):
            m = metadata(path); package = path.parent.name
            m['id'] = m.get('id', m.get('skill_id'))
            if not m['id']: raise ValueError('Missing governed skill identity')
            for field in ('triggers','non_triggers','related_domains','dependencies','related_skills','inputs','outputs','applicable_frameworks'):
                m.setdefault(field, [])
            m.setdefault('context_requirements', {})
            identity = production.PACKAGES.get(package, (m['id'], []))[0]
            if m['id'] != identity: raise ValueError('Registry identity differs from metadata')
            if any(s['id'] == identity for s in self.skills.values()): raise ValueError('Duplicate skill identity')
            # A metadata production flag is necessary, never sufficient: actual
            # execution still checks knowledge, stale implementation and review.
            self.skills[package] = dict(m, package=package,
                production_available=m['status'] == 'production',
                execution_available=package in production.PACKAGES,
                knowledge_topics=production.PACKAGES.get(package, (identity, []))[1],
                contract_path=str(path.relative_to(root)),
                limitations=text_boundary(path.read_text()))
    def get(self, package):
        if package in self.skills: return self.skills[package]
        return dict(package=package, id=None, status='unknown', production_available=False,
                    execution_available=False, applicable_frameworks=[], context_requirements={})
    def snapshot(self): return list(self.skills.values())


def text_boundary(text):
    # Preserve actual source contract; do not invent uniform framework promises.
    return text.split('---', 2)[-1].strip()
