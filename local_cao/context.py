"""Bounded Markdown configuration; never accounting-policy approval."""
import re
from datetime import date
from decimal import Decimal

ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.:-]{0,119}')
REQUIRED = {'company': ('company_id', 'legal_name'), 'execution':
    ('entity_id', 'framework', 'jurisdiction', 'period_start', 'period_end',
     'functional_currency', 'presentation_currency', 'calendar_id')}


def identity(value):
    if not isinstance(value, str) or not ID.fullmatch(value):
        raise ValueError('Invalid stable identity')
    return value


def parse(text):
    if not isinstance(text, str) or len(text.encode()) > 100_000:
        raise ValueError('Context size limit')
    sections = {}; section = None
    for line in text.splitlines():
        if line.startswith('## '):
            section = line[3:].strip().lower()
            if section in sections: raise ValueError('Duplicate context section')
            sections[section] = {}
        elif line.startswith('- '):
            key, sep, value = line[2:].partition(':')
            key = key.strip(); value = value.strip()
            if section is None or not sep or not re.fullmatch(r'[a-z][a-z0-9_]*', key):
                raise ValueError('Use section headings and key: value bullets')
            if key in sections[section]: raise ValueError('Conflicting or duplicate context field')
            sections[section][key] = value
    for section, fields in REQUIRED.items():
        for key in fields:
            if not sections.get(section, {}).get(key) or sections[section][key] in ('UNKNOWN', 'TODO'):
                raise ValueError('Required context field missing: '+section+'.'+key)
    c = sections['company']; e = sections['execution']
    for key in ('company_id',): identity(c[key])
    for key in ('entity_id', 'calendar_id'): identity(e[key])
    if e['framework'] not in ('IFRS', 'US_GAAP', 'UK_GAAP', 'AASB'):
        raise ValueError('Unsupported reporting framework')
    if not re.fullmatch(r'[A-Z]{2}', e['jurisdiction']): raise ValueError('Use jurisdiction country code')
    for key in ('functional_currency', 'presentation_currency'):
        if not re.fullmatch(r'[A-Z]{3}', e[key]): raise ValueError('Use currency code')
    if date.fromisoformat(e['period_start']) > date.fromisoformat(e['period_end']):
        raise ValueError('Reporting dates conflict')
    if e.get('materiality') not in (None, '', 'UNKNOWN'):
        n = Decimal(e['materiality'])
        if not n.is_finite() or n < 0: raise ValueError('Invalid materiality')
    return sections


def scope(context):
    e = context['execution']
    result = dict(company_id=context['company']['company_id'], entity=e['entity_id'],
        scope_id=e['entity_id'], framework=e['framework'], jurisdiction=e['jurisdiction'],
        period_start=e['period_start'], reporting_period=e['period_end'],
        currency=e['functional_currency'], functional_currency=e['functional_currency'],
        presentation_currency=e['presentation_currency'], reporting_calendar=e['calendar_id'])
    if e.get('materiality') not in (None, '', 'UNKNOWN'): result['materiality'] = e['materiality']
    from orchestration.scopes import Scope
    row = Scope(e['entity_id'], 'LEGAL_ENTITY', e['entity_id'], e['entity_id'],
        jurisdiction=e['jurisdiction'], framework=e['framework'],
        functional_currency=e['functional_currency'], presentation_currency=e['presentation_currency'],
        reporting_calendar=e['calendar_id'], provenance=('user-asserted-execution-dimensions',)).record()
    row['provenance'] = list(row['provenance'])
    result['scopes'] = [row]
    return result
