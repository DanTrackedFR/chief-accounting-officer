"""Reference public boundary contract; production adapters must call this boundary.

Only curated accounting fields may enter model context or leave the application.
Raw Markdown, claim registers, evidence objects and arbitrary nested data are excluded.
This module is executable contract code, not an existing production application.
"""
import json
import re

PUBLIC_TEXT = ('topic_id', 'guidance', 'framework', 'jurisdiction', 'entity_scope', 'effective_period')
PUBLIC_LISTS = ('limitations', 'uncertainties')
ROUTES = ('answer_context', 'answer', 'retrieval_snippet', 'citation', 'tool_output', 'user_log', 'export')
INTERNAL_TOKEN = re.compile(
    r'(?im)\bSource\s*:|\b(?:SOURCE_VERIFIED|MODEL_DERIVED_AUDIT_REQUIRED|'
    r'PRIMARY_CORROBORATED|SECONDARY_CORROBORATED|DIRECT_SOURCE_CHECKED|TRAINING_DATA_CHECKED)\b|'
    r'\b(?:source_note|approval_track|evidence_status|audit_required|approval_review)\b'
)

def _text(value):
    if not isinstance(value, str):
        raise ValueError('Public text must be a string')
    if INTERNAL_TOKEN.search(value):
        raise ValueError('Internal provenance in public content; curate before publishing')
    return value

def public_record(record, *, route):
    """Fail closed on contaminated content; never drop substantive caveats silently."""
    if route not in ROUTES:
        raise ValueError('Unregistered public route')
    if not isinstance(record, dict):
        raise ValueError('Public record must be an object')
    result = {key: _text(record[key]) for key in PUBLIC_TEXT if key in record}
    for key in PUBLIC_LISTS:
        if key in record:
            if not isinstance(record[key], list):
                raise ValueError('Public caveats must be an array')
            result[key] = [_text(item) for item in record[key]]
    # Citation fields are curated independently; never pass a claim/source object.
    if 'citations' in record:
        if not isinstance(record['citations'], list):
            raise ValueError('Public citations must be an array')
        result['citations'] = []
        for citation in record['citations']:
            if not isinstance(citation, dict):
                raise ValueError('Public citation must be an object')
            result['citations'].append({key: _text(citation[key]) for key in
                                      ('title', 'url', 'locator') if key in citation})
    return result

def serialize_public(record, *, route):
    return json.dumps(public_record(record, route=route), ensure_ascii=False)
