"""Closed, versioned value codec. No pickle, imports or executable stored values."""
import json
import math
from datetime import date, datetime
from decimal import Decimal


class IntegrityError(ValueError):
    """A checkpoint must fail closed, never silently repair governed state."""


def encode(value):
    if value is None or type(value) in (str, bool, int): return value
    if type(value) is float:
        if not math.isfinite(value): raise IntegrityError('Nonfinite checkpoint value')
        return value
    if type(value) is Decimal:
        if not value.is_finite(): raise IntegrityError('Nonfinite checkpoint amount')
        return {'$type': 'decimal', 'value': str(value)}
    if type(value) in (date, datetime): return {'$type': type(value).__name__, 'value': value.isoformat()}
    if type(value) is tuple: return {'$type': 'tuple', 'value': [encode(v) for v in value]}
    if type(value) is list: return [encode(v) for v in value]
    if type(value) is dict:
        if any(type(k) is not str for k in value) or '$type' in value: raise IntegrityError('Invalid/reserved checkpoint key')
        return {k: encode(value[k]) for k in sorted(value)}
    raise IntegrityError('Unsupported checkpoint value type')


def decode(value):
    if isinstance(value, list): return [decode(v) for v in value]
    if isinstance(value, dict):
        if '$type' not in value: return {k: decode(v) for k, v in value.items()}
        if set(value) != {'$type', 'value'}: raise IntegrityError('Unknown codec fields')
        kind, v = value['$type'], value['value']
        if kind == 'tuple' and isinstance(v, list): return tuple(decode(x) for x in v)
        if kind == 'decimal' and isinstance(v, str):
            n = Decimal(v)
            if not n.is_finite() or str(n) != v: raise IntegrityError('Noncanonical decimal')
            return n
        if kind == 'date' and isinstance(v, str):
            n = date.fromisoformat(v)
            if n.isoformat() == v: return n
        if kind == 'datetime' and isinstance(v, str):
            n = datetime.fromisoformat(v)
            if n.isoformat() == v: return n
        raise IntegrityError('Unknown/noncanonical codec type')
    if type(value) not in (str, int, float, bool, type(None)): raise IntegrityError('Unsupported decoded value')
    return value


def dumps(value):
    return json.dumps(encode(value), sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)


def loads(text):
    def pairs(rows):
        out = {}
        for k, v in rows:
            if k in out: raise IntegrityError('Duplicate JSON key')
            out[k] = v
        return out
    try:
        raw = json.loads(text, object_pairs_hook=pairs, parse_constant=lambda _: (_ for _ in ()).throw(IntegrityError('Nonfinite JSON')))
        result = decode(raw)
        if dumps(result) != text: raise IntegrityError('Noncanonical checkpoint encoding')
        return result
    except (TypeError, ValueError, ArithmeticError) as exc:
        raise IntegrityError('Invalid checkpoint encoding') from exc
