"""Reference public boundary contract; production adapters must call this boundary.

Only curated accounting fields may enter model context or leave the application.
Raw Markdown, claim registers, evidence objects and arbitrary nested data are excluded.
This module is executable contract code, not an existing production application.
"""
import json
import re

PUBLIC_TEXT = ('topic_id', 'guidance', 'framework', 'jurisdiction', 'entity_scope', 'effective_period', 'status', 'confidence')
PUBLIC_LISTS = ('limitations', 'uncertainties', 'open_items', 'controls', 'reporting', 'required_approvals')
ROUTES = ('answer_context', 'answer', 'retrieval_snippet', 'citation', 'tool_output', 'user_log', 'export')
INTERNAL_TOKEN = re.compile(
    r'(?im)\b(?:exec|version|period|case|dependency|ic-side|ic-relationship|fingerprint):(?=\S)|\b(?:node_id|case_id|period_id|result_version|dependency_id|receipt_internals|source_fingerprint|reviewer_signoff|evidence_tier|routing_metadata|semantic_metadata)\b|\bSource\s*:|\b(?:SOURCE_VERIFIED|MODEL_DERIVED_AUDIT_REQUIRED|'
    r'ChatGPT\s+training\s+data|\b[0-9a-f]{64}\b|\b(?:case_fingerprint|source_hash|claim_register|reviewer_identity)\b|'
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
    for key, allowed in {
        'accounting_determination': ('SUPPORTED', 'UNRESOLVED', 'UNSUPPORTED'),
        'evidence_sufficiency': ('SUFFICIENT', 'INSUFFICIENT'),
        'review_provenance': ('SYSTEM_PREPARED', 'FORMALLY_REVIEWED'),
    }.items():
        if key in record:
            if record[key] not in allowed: raise ValueError('Invalid accounting provenance status')
            result[key] = record[key]
    if 'source_provenance' in record:
        if record['source_provenance'] != 'USER_PROVIDED_SOURCES': raise ValueError('Invalid source provenance')
        result['source_provenance'] = record['source_provenance']
    if 'validation_requirements' in record:
        needs = record['validation_requirements']
        if not isinstance(needs, list): raise ValueError('Requirements must be an array')
        result['validation_requirements'] = []
        for item in needs:
            fields = ('identifier', 'field_path', 'explanation', 'category')
            if not isinstance(item, dict) or set(item) != set(fields): raise ValueError('Invalid requirement')
            result['validation_requirements'].append({key: _text(item[key]) for key in fields})
    if 'anomaly_report' in record:
        result['anomaly_report'] = curate_anomalies(record['anomaly_report'])
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
    if 'calculations' in record:
        if not isinstance(record['calculations'], list): raise ValueError('Calculation array required')
        result['calculations'] = []
        for row in record['calculations']:
            if not isinstance(row, dict): raise ValueError('Calculation object required')
            result['calculations'].append({key: _text(row[key]) for key in ('label', 'amount') if key in row})
    if 'journals' in record:
        if not isinstance(record['journals'], list): raise ValueError('Journal array required')
        result['journals'] = []
        for entry in record['journals']:
            if not isinstance(entry, dict) or not isinstance(entry.get('lines'), list): raise ValueError('Journal lines required')
            lines = []
            for line in entry['lines']:
                if not isinstance(line, dict): raise ValueError('Journal line required')
                lines.append({key: _text(line[key]) for key in ('side', 'account', 'amount') if key in line})
            result['journals'].append({'lines': lines})
    return result

def curate_anomalies(report):
    if report == {}: return {}
    if not isinstance(report, dict): raise ValueError('Invalid anomaly report')
    output = {key: _text(report[key]) for key in ('profile', 'population_status', 'completeness')}
    if output['profile'] != 'presumed_user_provided': raise ValueError('Invalid anomaly profile')
    output['excluded_rows'] = [_text(x) for x in report['excluded_rows']]
    output['limitations'] = [_text(x) for x in report['limitations']]
    output['findings'] = []
    for finding in report['findings']:
        if not isinstance(finding, dict) or finding.get('severity') not in ('PASS','WARNING','BLOCKED','NOT_PERFORMED'): raise ValueError('Invalid finding')
        if type(finding.get('blocks_calculation')) is not bool: raise ValueError('Invalid blocking flag')
        row = {key: _text(finding[key]) for key in ('check_id','severity','source_reference','explanation','resolution')}
        if not isinstance(finding['row_references'],list): raise ValueError('Invalid row references')
        row['row_references'] = [_text(x) for x in finding['row_references']]
        row['blocks_calculation'] = finding['blocks_calculation']
        for key in ('observed','expected','field_path'):
            if key in finding: row[key] = _text(finding[key])
        output['findings'].append(row)
    return output


def serialize_public(record, *, route):
    return json.dumps(public_record(record, route=route), ensure_ascii=False)
