"""Dependency-free validation of the exact JSON Schema subset used in claim.schema.json.

Fail on unknown validation keywords so a schema extension cannot silently weaken checks.
"""
import re

ANNOTATIONS = {'$schema', 'title', 'description', '$comment', 'default'}
SUPPORTED = {'type', 'required', 'properties', 'additionalProperties', 'items', 'enum', 'pattern', 'minLength'}

def validate(value, schema, path='$'):
    errors = []
    unknown = set(schema) - ANNOTATIONS - SUPPORTED
    if unknown:
        return [f'{path}: unsupported schema keywords {sorted(unknown)}']
    predicates = {'object': lambda v: isinstance(v, dict),
                  'array': lambda v: isinstance(v, list),
                  'string': lambda v: isinstance(v, str),
                  'boolean': lambda v: isinstance(v, bool),
                  'null': lambda v: v is None}
    types = schema.get('type')
    if types:
        types = types if isinstance(types, list) else [types]
        if any(t not in predicates for t in types):
            return [f'{path}: unsupported schema type']
        if not any(predicates[t](value) for t in types):
            return [f'{path}: expected type {types}']
    if 'enum' in schema and value not in schema['enum']:
        errors.append(f'{path}: value outside enum')
    if isinstance(value, str):
        if 'pattern' in schema and not re.search(schema['pattern'], value):
            errors.append(f'{path}: pattern mismatch')
        if len(value) < schema.get('minLength', 0):
            errors.append(f'{path}: string too short')
    if isinstance(value, dict):
        for key in schema.get('required', []):
            if key not in value: errors.append(f'{path}: missing {key}')
        properties = schema.get('properties', {})
        for key, item in value.items():
            if key in properties: errors += validate(item, properties[key], f'{path}.{key}')
            elif schema.get('additionalProperties') is False:
                errors.append(f'{path}: unexpected property {key}')
    if isinstance(value, list) and 'items' in schema:
        for i, item in enumerate(value):
            errors += validate(item, schema['items'], f'{path}[{i}]')
    return errors
