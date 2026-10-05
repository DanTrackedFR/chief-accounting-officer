"""Explicit bounded execution scopes; no arbitrary entity graph or persistence.

One native workpaper per owner remains supported. A reviewed scope table admits
different legal/group contexts without weakening the default dimension gate.
"""
from datetime import date


def execution_scopes(context):
    rows = context.get('execution_scopes')
    default = {k: context[k] for k in ('entity', 'framework', 'jurisdiction', 'period_start', 'reporting_period', 'currency')}
    if rows is None:
        return {context['entity']: default}
    if not isinstance(rows, list) or not 1 <= len(rows) <= 3:
        raise ValueError('Bounded execution requires one to three explicit scopes')
    out = {}
    for row in rows:
        if not isinstance(row, dict) or set(row) != set(default) | {'level'}:
            raise ValueError('Explicit execution scope dimensions required')
        if row['level'] not in ('entity', 'group') or row['entity'] in out:
            raise ValueError('Duplicate or invalid execution scope')
        if row['framework'] != context['framework']:
            raise ValueError('Mixed local/group frameworks remain unsupported')
        if not isinstance(row['currency'], str) or len(row['currency']) != 3 or not row['currency'].isupper():
            raise ValueError('Invalid execution currency')
        start, end = date.fromisoformat(row['period_start']), date.fromisoformat(row['reporting_period'])
        if start > end or start < date.fromisoformat(context['period_start']) or end > date.fromisoformat(context['reporting_period']):
            raise ValueError('Execution period outside bounded Case')
        out[row['entity']] = dict(row)
    if context['entity'] not in out or any(out[context['entity']][k] != v for k, v in default.items()):
        raise ValueError('Case reporting scope absent or contradictory')
    if len(out)>1 and (out[context['entity']]['level']!='group' or any(r['level']!='entity' for e,r in out.items() if e!=context['entity'])):
        raise ValueError('Bounded scopes require one reporting group and separate legal entities')
    return out


def scoped_context(context, source):
    scope = execution_scopes(context).get(source.get('entity'))
    if scope is None:
        raise ValueError('Owner outside explicit execution scopes')
    return dict(context, **scope)
