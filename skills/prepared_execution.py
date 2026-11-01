"""Bounded system preparation, never a reviewer or posting authority.

Canonical populations are background knowledge, not an invented applied-claim
selection. Existing owners retain every source, policy and reconciliation gate.
"""
import copy
from datetime import date
from core_accounting import ReviewRequired, context, required, balance

MODE = 'prepared_unreviewed'
SYSTEM = 'SYSTEM_DERIVED_NOT_A_REVIEWER'
PACKAGES = {'fixed-assets': 'machinery', 'accounts-payable': 'supplier_cost'}
RECORDS = {'knowledge_review', 'applicability_review', 'reviewer_signoff'}


def reject_records(value):
    if isinstance(value, dict):
        if RECORDS & value.keys():
            raise ReviewRequired('System preparation rejects supplied accounting review records')
        for item in value.values(): reject_records(item)
    elif isinstance(value, list):
        for item in value: reject_records(item)


def qualify(package, case):
    if package not in PACKAGES:
        raise ReviewRequired('System preparation is unavailable for this accounting package')
    if not isinstance(case, dict): raise ReviewRequired('Accounting case must be an object')
    if case.get('package', package) != package: raise ReviewRequired('Case implementation owner differs from selected accounting skill')
    reject_records(case)
    context(case)
    required(case, 'period_start', 'entity_type', 'policy_elections')
    start = date.fromisoformat(case['period_start']); end = date.fromisoformat(case['reporting_period'])
    if not date(2026, 1, 1) <= start <= end <= date(2026, 12, 31):
        raise ReviewRequired('System preparation supports reporting periods wholly within 2026 only')
    if case['entity_type'] != 'for_profit':
        raise ReviewRequired('System preparation requires for-profit commercial entity scope')
    if case['policy_elections'] != {}:
        raise ReviewRequired('Policy election requires separate supported-method assessment')
    if case.get('regulatory_overlays') not in (None, []):
        raise ReviewRequired('Regulatory overlay requires separate applicability assessment')
    fw = case['framework']
    if fw == 'UK_GAAP' and (case.get('uk_standard') != 'FRS_102' or case.get('uk_standard_edition') != '2026'):
        raise ReviewRequired('System preparation requires FRS 102 2026 edition')
    if fw == 'AASB' and (type(case.get('reporting_tier')) is not int or case['reporting_tier'] not in (1, 2) or case.get('aasb_compilation') != '2026'):
        raise ReviewRequired('System preparation requires qualified AASB 2026 compilation and Tier 1 or 2')
    if fw == 'US_GAAP' and case.get('us_entity_type') != 'private_company':
        raise ReviewRequired('System preparation excludes regulated or public US entities')
    if package == 'accounts-payable': return 'Governed ordinary supplier-cost reconciliation profile, 2026'
    return {'IFRS': 'IAS 16 / IAS 8 ordinary cost method, 2026',
            'US_GAAP': 'ASC 360 ordinary historical cost, 2026',
            'UK_GAAP': 'FRS 102 Section 17, 2026',
            'AASB': 'AASB 116 / AASB 108 ordinary cost method, 2026'}[fw]


def execute(package, case):
    import production
    edition = qualify(package, case)
    working = copy.deepcopy(case)
    # Compatibility input for existing date and operational proof gates. It is
    # explicitly machine-derived and never copied to a formal review record.
    working['applicability_review'] = dict(reviewer=SYSTEM, standard_versions=[edition],
        effective_period=[case['period_start'], case['reporting_period']],
        entity_scope=case['entity_type'], exceptions=[], provenance='SYSTEM_DERIVED')
    production.dates(working)
    claims, documents = production.canonical_knowledge(production.PACKAGES[package][1], case['framework'], package=package)
    if not claims or any(c.get('evidence_status') in ('CONFLICTED', 'NOT_RESEARCHED') for c in claims):
        raise ReviewRequired('Canonical accounting knowledge assurance unresolved')
    result = production.load_workflow(package).assess(working, claims)
    for entry in result.get('journal_entry_implications', []): balance(entry)
    # This exact owner-level generic sentence confounds review with evidence.
    generic = 'Company recognition, valuation, legal rights and tax conclusions require supplied evidence and independent review. No universal ERP posting authorization is inferred.'
    result['uncertainties'] = [x for x in result.get('uncertainties', []) if x != generic]
    supported = not result.get('open_items')
    result.update(skill_id=production.PACKAGES[package][0], framework=case['framework'], jurisdiction=case['jurisdiction'],
        entities=[case['entity']], periods=[case['period_start'], case['reporting_period']],
        case_fingerprint=production.case_fingerprint(case), review_mode=MODE,
        status='partial', accounting_determination='SUPPORTED' if supported else 'UNRESOLVED',
        evidence_sufficiency='SUFFICIENT' if supported else 'INSUFFICIENT', review_provenance='SYSTEM_PREPARED',
        evidence=[], knowledge_population=claims, knowledge_documents=documents,
        applicability_provenance=dict(origin='SYSTEM_DERIVED', standard_versions=[edition],
            framework=case['framework'], period=[case['period_start'], case['reporting_period']], entity_scope=case['entity_type']),
        facts_used=copy.deepcopy(case), assumptions=case['assumptions'], confidence='medium',
        recommendation_class='REQUIRED', memory_candidates=[], related_artifacts=[],
        controls_impacted=['Source population and schedule reconcile to ledger', 'Proposed journals require separate posting authorization'],
        reporting_impacted=['Framework-specific presentation and disclosure requirements'],
        systems_impacted=['Retain versioned evidence and calculation lineage'],
        documentation_required=['Source evidence, material assumptions and accounting calculation'],
        audit_evidence_required=['Complete source population and calculation reperformance'])
    result['proposed_journal_workpaper'] = result.pop('journal_entry_implications', [])
    result['journal_entry_implications'] = []
    production.to_public(result)
    return result


def to_public(result, route):
    from interfaces.public_output import public_record
    from production import serializable
    import json
    if result['status'] == 'blocked':
        from production import _public_requirement_text
        return public_record(dict(guidance=_public_requirement_text(result['conclusion']), status='blocked',
            accounting_determination='UNRESOLVED', evidence_sufficiency='INSUFFICIENT',
            review_provenance='SYSTEM_PREPARED', framework=result['framework'], jurisdiction=result['jurisdiction'],
            entity_scope=result['entities'][0], effective_period=' to '.join(result['periods']),
            open_items=[_public_requirement_text(item) for item in result.get('open_items', [])], citations=[]), route=route)
    fa = result['skill_id'] == 'SKILL-FA-001'
    keys = ('depreciation', 'closing_cost', 'closing_accumulated', 'closing_cip', 'excluded_expense') if fa else ('opening_ap', 'invoices', 'payments', 'closing_ap', 'closing_accruals')
    calculations = {k: result['calculations'][k] for k in keys if k in result['calculations']}
    treatment = ('Qualifying ordinary machinery costs are capitalized under the cost model. Depreciation starts when ready for use; the depreciable carrying amount excludes residual value and is allocated over the supported remaining life or production units.' if fa else 'Recognize supplier obligations for goods or services received by period end. Measure supported unbilled receipts using evidenced quantities and rates, avoid duplicate invoice accruals, and reconcile payments and supplier balances to the ledger.')
    guidance = result['conclusion'] + '\n' + treatment + '\nCalculations: ' + json.dumps(calculations, default=serializable, sort_keys=True)
    if result.get('assumptions'): guidance += '\nMaterial assumptions: ' + '; '.join(result['assumptions'])
    guidance += '\nProposed journal implications: ' + json.dumps(result.get('proposed_journal_workpaper', []), default=serializable)
    private = []
    def visit(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key in ('reviewer', 'approved_by', 'reviewer_identity') and isinstance(item, str) and item: private.append(item)
                else: visit(item)
        elif isinstance(value, list):
            for item in value: visit(item)
    visit(result.get('facts_used', {}))
    if any(identity in guidance for identity in private): raise ReviewRequired('Private review identity cannot be published')
    public = public_record(dict(guidance=guidance, status=result['status'],
        accounting_determination=result['accounting_determination'], evidence_sufficiency=result['evidence_sufficiency'],
        review_provenance='SYSTEM_PREPARED', framework=result['framework'], jurisdiction=result['jurisdiction'],
        entity_scope=result['entities'][0], effective_period=' to '.join(result['periods']),
        limitations=result.get('uncertainties', []) + ['Journal workpapers are proposals; posting requires separate authorization.'],
        open_items=result.get('open_items', []),
        citations=[{'title': ('Fixed assets' if result['skill_id']=='SKILL-FA-001' else 'Accounts payable') + ' governed knowledge package — background guidance'}]), route=route)

    if any(identity in json.dumps(public, ensure_ascii=False) for identity in private):
        raise ReviewRequired('Private review identity cannot be published')
    return public
