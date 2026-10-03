"""Governed execution boundary shared by the four accounting workflows.

Case conclusions are reviewed accounting inputs, never inferred company facts.
Evidence stays internal; only curated outputs cross the application boundary.
"""
import hashlib
import importlib.util
import json
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path
from core_accounting import ReviewRequired, approved_claims, balance, context, dec, required
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from interfaces.public_output import public_record

PACKAGES = {
    'earnings-per-share': ('SKILL-EPS-001',['TOPIC-08-007']),
    'segment-reporting': ('SKILL-SEG-001',['TOPIC-08-006']),
    'subsequent-events': ('SKILL-EVENT-001',['TOPIC-08-005']),
    'government-grants': ('SKILL-GRANT-001',[]),
    'borrowing-costs': ('SKILL-BORROW-001',['TOPIC-04-003']),
    'cash-flow-reporting': ('SKILL-CASH-001',['TOPIC-08-002','TOPIC-06-001','TOPIC-06-002']),
    'equity-capital': ('SKILL-EQUITY-001',['TOPIC-08-003','TOPIC-13-006']),
    'accounting-changes': ('SKILL-CHANGE-001',['TOPIC-02-009','TOPIC-15-001','TOPIC-15-003','TOPIC-15-006']),
    'going-concern': ('SKILL-GC-001',['TOPIC-08-005','TOPIC-06-006']),
    'commitments-contingencies': ('SKILL-COMMIT-001',['TOPIC-05-003','TOPIC-13-008','TOPIC-06-007']),
    'related-parties': ('SKILL-RP-001',['TOPIC-08-006','TOPIC-13-008']),
    'month-end-close': ('SKILL-CLOSE-001', ['TOPIC-02-001','TOPIC-02-002','TOPIC-02-003','TOPIC-02-006','TOPIC-02-007','TOPIC-02-008','TOPIC-02-010','TOPIC-12-006']),
    'balance-sheet-reconciliations': ('SKILL-REC-001', ['TOPIC-02-004','TOPIC-02-005','TOPIC-02-008']),
    'accounts-receivable': ('SKILL-AR-001', ['TOPIC-03-007','TOPIC-03-009','TOPIC-03-010','TOPIC-03-011','TOPIC-12-002']),
    'accounts-payable': ('SKILL-AP-001', ['TOPIC-05-001','TOPIC-05-002','TOPIC-02-007','TOPIC-12-001']),
    'fixed-assets': ('SKILL-FA-001', ['TOPIC-04-001','TOPIC-04-002','TOPIC-04-003','TOPIC-12-004']),
    'intercompany-accounting': ('SKILL-IC-001', ['TOPIC-07-003','TOPIC-12-004']),
    'revenue-recognition': ('SKILL-REV-001', ['TOPIC-03-001','TOPIC-03-002','TOPIC-03-003','TOPIC-03-004','TOPIC-03-005','TOPIC-03-006','TOPIC-03-012']),
    'financial-instruments-ecl': ('SKILL-ECL-001', ['TOPIC-06-007','TOPIC-06-008','TOPIC-06-009','TOPIC-06-010','TOPIC-03-008','TOPIC-03-009']),
    'provisions-contingencies': ('SKILL-PROV-001', ['TOPIC-05-003','TOPIC-05-004','TOPIC-13-005','TOPIC-15-004']),
    'consolidation': ('SKILL-CONS-001', ['TOPIC-07-%03d'%i for i in range(1,10)]+['TOPIC-13-001']),
    'business-combinations': ('SKILL-BC-001', ['TOPIC-13-001','TOPIC-13-002','TOPIC-13-003']),
    'asset-impairment': ('SKILL-IMP-001', ['TOPIC-04-006']),
    'income-taxes': ('SKILL-TAX-001', ['SUPPLEMENTAL_TAX']),
    'inventory-cost': ('SKILL-INV-001', []),
    'employee-benefits-payroll': ('SKILL-BEN-001', ['TOPIC-05-005','TOPIC-05-006','TOPIC-05-009','TOPIC-05-010']),
    'debt-financing': ('SKILL-DEBT-001', ['TOPIC-06-005','TOPIC-06-006','TOPIC-06-007','TOPIC-13-006']),
    'intangible-assets': ('SKILL-INT-001', ['TOPIC-04-003','TOPIC-04-004','TOPIC-04-005']),
    'fair-value-measurement': ('SKILL-FV-001', ['TOPIC-06-008']),
    'foreign-currency': ('SKILL-FX-001', ['TOPIC-06-002','TOPIC-06-003','TOPIC-06-004','TOPIC-07-006']),
    'share-based-compensation': ('SKILL-SBC-001', ['TOPIC-05-007','TOPIC-05-008']),
    'financial-statements': ('SKILL-FS-001', ['TOPIC-08-%03d'%i for i in range(1,10)]),
}

def flag(obj, key):
    required(obj, key)
    if type(obj[key]) is not bool:
        raise ReviewRequired(key+' must be an evidenced boolean')
    return obj[key]

def nonnegative(value):
    n = dec(value)
    if n < 0: raise ReviewRequired('Negative amount is not valid for this input')
    return n

def fraction(value):
    n = dec(value)
    if not 0 <= n <= 1: raise ReviewRequired('Fraction outside [0,1]')
    return n

def dates(case):
    required(case, 'period_start','reporting_period','entity_type','policy_elections','evidence','judgment_memo','assumptions')
    try:
        start=date.fromisoformat(case['period_start']); end=date.fromisoformat(case['reporting_period'])
    except (ValueError,TypeError) as exc: raise ReviewRequired('Use ISO reporting dates') from exc
    if start>end: raise ReviewRequired('Period start exceeds reporting date')
    if not isinstance(case['assumptions'],list) or not isinstance(case['policy_elections'],dict):
        raise ReviewRequired('Assumptions array and policy election object required')
    if case['framework']=='UK_GAAP' and case['uk_standard']!='FRS_102':
        raise ReviewRequired('FRS 101/105 require separate framework workflow')
    if case['framework']=='AASB':
        if case['reporting_tier'] not in (1,2): raise ReviewRequired('Resolve Australian reporting tier')
        if case['entity_type']!='for_profit':
            raise ReviewRequired('Australian NFP/public-sector overlay requires specialist scope assessment')
    required(case,'applicability_review')
    review=case['applicability_review']
    required(review,'reviewer','standard_versions','effective_period','entity_scope','exceptions')
    if review['effective_period'] != [case['period_start'],case['reporting_period']]:
        raise ReviewRequired('Applicability review does not cover this period')
    if review['entity_scope'] != case['entity_type']: raise ReviewRequired('Applicability review scope mismatch')
    if not isinstance(review['exceptions'],list): raise ReviewRequired('Applicability exceptions must be an array')
    return start

def load_workflow(package):
    spec=importlib.util.spec_from_file_location(package.replace('-','_')+'_workflow',ROOT/'skills'/package/'workflow.py')
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def canonical_knowledge(topic_ids, framework):
    if topic_ids == ['SUPPLEMENTAL_TAX']:
        spec=importlib.util.spec_from_file_location('supplemental_tax_retrieval',ROOT/'knowledge/income-taxes/retrieval.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        try:
            eligible={c['claim_id'] for c in module.retrieve(framework,'actual period requires case review','for_profit')}
            register=module.load_register()
        except ValueError as exc:raise ReviewRequired(str(exc)) from exc
        claims=[dict(topic_id='SUPPLEMENTAL_TAX',claim_id=c['claim_id'],proposition=c['proposition'],
            references=c.get('paragraph_references',[]),reference_confidence=c['reference_confidence'],
            evidence_status=c['evidence_status'],audit_required=c['audit_required'],limitations=c['limitations'],
            effective_period=c['effective_period'],entity_scope=c['entity_scope']) for c in register['claims'] if c['claim_id'] in eligible]
        docs=[{'topic_id':'SUPPLEMENTAL_TAX','path':str(p.relative_to(ROOT)),
            'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((ROOT/'knowledge/income-taxes').glob('*')) if p.is_file()]
        return claims,docs
    # Explicitly approved operational tie-out topic has no normative claims.
    # Retrieve its documents, but never manufacture accounting authority.
    operational={'TOPIC-02-001','TOPIC-02-002','TOPIC-02-003','TOPIC-02-004','TOPIC-02-005','TOPIC-02-010','TOPIC-03-011','TOPIC-08-009'}
    claims=approved_claims([t for t in topic_ids if t not in operational],framework)
    if 'TOPIC-02-009' in topic_ids and framework=='US_GAAP':
        claims+=approved_claims(['TOPIC-02-009'],'SEC')
    # Operational documents are not universal normative authority. IFRS18 and
    # auditor-only OTHER claims remain in the reviewed documents, not applied
    # company recognition citations merely because this is a close workflow.
    manifest=json.loads((ROOT/'knowledge/phase-2d-topic-manifest.json').read_text())['topics']
    documents=[]
    for tid in topic_ids:
        t=next(x for x in manifest if x['topic_id']==tid)
        if t['status']!='APPROVED':raise ReviewRequired('Canonical topic not approved: '+tid)
        # Canonical methods added during remediation may not occur in the old artifact list.
        claim_path=next(ROOT/p for p in t['artifact_paths'] if p.endswith('/standards-claims.json'))
        paths=set(claim_path.parent.glob('*.md'))
        # New reporting packages read full method trees without changing
        # archived knowledge manifests of existing production packages.
        if list(topic_ids) in [PACKAGES[p][1] for p in ('cash-flow-reporting','equity-capital','accounting-changes','going-concern','commitments-contingencies','related-parties')]:
            paths.update(claim_path.parent.rglob('*.md'))
        if tid in operational or tid.startswith('TOPIC-12-'):
            paths.update(claim_path.parent.rglob('*.md'))
        paths.add(claim_path)
        paths.update(ROOT/p for p in t['artifact_paths'] if p.endswith('.md'))
        for p in sorted(paths):
            documents.append({'topic_id':tid,'path':str(p.relative_to(ROOT)), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    return claims,documents

def execute(package, case):
    if package not in PACKAGES: raise ReviewRequired('Unknown accounting skill')
    if package=='government-grants':raise ReviewRequired('No approved substantive government-grant recognition or measurement knowledge; governed knowledge extension required')
    if package=='borrowing-costs':raise ReviewRequired('Approved CIP routing does not provide a substantive borrowing-cost capitalization method; governed knowledge extension required')
    if package == 'inventory-cost':
        raise ReviewRequired('No approved substantive inventory recognition, costing or subsequent-measurement knowledge; inventory accounting specialist and governed knowledge extension required')
    if not isinstance(case,dict):raise ReviewRequired('Accounting case must be an object')
    try:context(case); dates(case)
    except (KeyError,TypeError,AttributeError) as exc:raise ReviewRequired('Missing or malformed case context: '+str(exc)) from exc
    claims,knowledge=canonical_knowledge(PACKAGES[package][1],case['framework'])
    required(case,'knowledge_review')
    reviewed=case['knowledge_review']
    required(reviewed,'reviewer','claim_ids','documents')
    if set(reviewed['claim_ids']) != {c['claim_id'] for c in claims}:
        raise ReviewRequired('Knowledge review must cover current applicable claim population')
    if reviewed['documents'] != knowledge:
        raise ReviewRequired('Canonical knowledge changed or has not been reviewed')
    try:result=load_workflow(package).assess(case,claims)
    except (KeyError,TypeError,AttributeError) as exc:raise ReviewRequired('Missing or malformed accounting workflow input: '+str(exc)) from exc
    for entry in result.get('journal_entry_implications',[]): balance(entry)
    required(reviewed,'applied_claim_ids','selection_memo','public_caveats')
    used=set(reviewed['applied_claim_ids'])
    if not used or not used<={c['claim_id'] for c in claims}:raise ReviewRequired('Applied claims must be a nonempty subset of reviewed approved claims')
    selected=[c for c in claims if c['claim_id'] in used]
    if package=='accounting-changes' and any('-SEC-' in c['claim_id'] for c in selected) and not case.get('sec',{}).get('registrant'):
        raise ReviewRequired('SEC claims require actual registrant applicability')
    if case['framework']=='UK_GAAP' and any('FRS105' in c['proposition'].replace(' ','') or 'FRS101' in c['proposition'].replace(' ','') for c in selected):raise ReviewRequired('FRS102 case cannot cite FRS101/105-specific propositions as applicable authority')
    if not isinstance(reviewed['public_caveats'],list) or not reviewed['public_caveats']:raise ReviewRequired('Curated accounting/period/authority caveats required')
    result.setdefault('uncertainties',[]).extend(reviewed['public_caveats'])
    result.update(skill_id=PACKAGES[package][0],framework=case['framework'],jurisdiction=case['jurisdiction'],
        entities=[case['entity']],periods=[case['period_start'],case['reporting_period']],
        facts_used={k:v for k,v in case.items() if k not in ('assumptions','knowledge_review','reviewer_signoff')},
        assumptions=case['assumptions'], evidence=selected,reviewed_claims=claims,knowledge_documents=knowledge,
        recommendation_class='REQUIRED',confidence='medium',memory_candidates=[],related_artifacts=[],
        controls_impacted=['Source population to GL tie-out','Independent route, estimate and journal review','Versioned accounting policy and disclosure review'],
        reporting_impacted=['Framework-specific statement presentation and comparative-period consistency'],
        systems_impacted=['Retain case ID, source IDs, policy version, rule route and journal lineage'],
        documentation_required=['Accounting judgment memo','Input evidence','Calculation and reconciliation','Disclosure tie-out','Reviewer certification'],
        audit_evidence_required=['Contract/legal/source evidence','Assumptions and alternatives','Calculation reperformance','Approval record'])
    fingerprint=case_fingerprint(case)
    result['case_fingerprint']=fingerprint
    signoff=case.get('reviewer_signoff',{})
    valid=(signoff.get('case_fingerprint')==fingerprint and bool(signoff.get('reviewer')) and
           signoff.get('reviewer')!=case.get('preparer') and signoff.get('approved') is True)
    result['status']='complete' if valid and not result.get('open_items') else 'partial'
    if not valid: result.setdefault('open_items',[]).append('Independent reviewer must approve this exact case fingerprint before use')
    try:to_public(result)
    except ValueError as exc:raise ReviewRequired('Public output could not be safely curated; reviewer must resolve accounting caveats or account labels') from exc
    return result

def case_fingerprint(case):
    files=[ROOT/'skills/core_accounting.py',ROOT/'skills/production.py',ROOT/'interfaces/public_output.py']
    files += list((ROOT/'skills').glob('*/workflow.py'))+list((ROOT/'skills').glob('*/engine.py'))
    files += list((ROOT/'skills').glob('*/SKILL.md'))+list((ROOT/'skills').glob('*/methods.md'))
    files += [ROOT/'skills/REVIEWER-CONTROLS.md',ROOT/'skills/run_skill.py',ROOT/'skills/advanced_accounting.py',ROOT/'skills/operations_accounting.py']
    files += [ROOT/'skills/reporting_accounting.py',ROOT/'skills/financing_accounting.py']
    files += [ROOT/'skills/presentation_accounting.py']
    implementation={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
    payload={'case':{k:v for k,v in case.items() if k!='reviewer_signoff'},'implementation':implementation}
    return hashlib.sha256(json.dumps(payload,sort_keys=True,default=str).encode()).hexdigest()

def to_public(result, route='answer'):
    standard_titles={
      'SKILL-REV-001':{'IFRS':'IFRS 15','US_GAAP':'ASC 606','UK_GAAP':'FRS 102 Section 23','AASB':'AASB 15'},
      'SKILL-ECL-001':{'IFRS':'IFRS 9 / IFRS 7','US_GAAP':'ASC 326 and instrument-specific measurement guidance','UK_GAAP':'FRS 102 Sections 11/12 and elected measurement model','AASB':'AASB 9 / AASB 7'},
      'SKILL-PROV-001':{'IFRS':'IAS 37','US_GAAP':'ASC 450 and applicable event-specific guidance','UK_GAAP':'FRS 102 Section 21','AASB':'AASB 137'},
      'SKILL-CONS-001':{'IFRS':'IFRS 10','US_GAAP':'ASC 810','UK_GAAP':'FRS 102 Section 9','AASB':'AASB 10'}}
    title=standard_titles.get(result['skill_id'],{}).get(result['framework'],'Framework unresolved')
    additional={'SKILL-BC-001':['IFRS 3','ASC 805','FRS 102 Section 19','AASB 3'],
      'SKILL-EPS-001':['IAS 33','ASC 260','Applicable FRS 102 Section 1 / separately scoped IAS 33','AASB 133'],
      'SKILL-SEG-001':['IFRS 8','ASC 280','Applicable UK segment reporting scope','AASB 8'],
      'SKILL-EVENT-001':['IAS 10','ASC 855','FRS 102 Section 32','AASB 110'],
      'SKILL-CASH-001':['IAS 7 / applicable IFRS 18 amendments','ASC 230','FRS 102 Section 7','AASB 107 / applicable AASB 18 amendments'],
      'SKILL-EQUITY-001':['IAS 32 / applicable equity presentation','ASC 505 / applicable equity presentation','FRS 102 Sections 6 / 22','AASB 132 / applicable equity presentation'],
      'SKILL-CHANGE-001':['IAS 8','ASC 250','FRS 102 Section 10','AASB 108'],
      'SKILL-GC-001':['Applicable IAS 1 / IAS 8 / IAS 10','ASC 205-40 / ASC 855','FRS 102 Sections 3 / 32','Applicable AASB 101 / AASB 108 / AASB 110'],
      'SKILL-COMMIT-001':['IAS 37 / contract-specific guidance','ASC 450 / contract-specific guidance','FRS 102 Section 21 / contract-specific guidance','AASB 137 / contract-specific guidance'],
      'SKILL-RP-001':['IAS 24','ASC 850','FRS 102 Section 33','AASB 124'],
      'SKILL-CLOSE-001':['Applicable recognition guidance / IAS 8','Applicable recognition guidance / ASC 250','Applicable FRS 102 / Section 10','Applicable AASB / AASB 108'],
      'SKILL-REC-001':['IAS 8','ASC 250','FRS 102 Section 10','AASB 108'],
      'SKILL-AR-001':['IFRS 15 / IFRS 9','ASC 606 / ASC 326','FRS 102 Sections 11 / 23','AASB 15 / AASB 9'],
      'SKILL-AP-001':['Applicable expense and liability guidance','Applicable expense and liability guidance','Applicable FRS 102 expense and liability guidance','Applicable AASB expense and liability guidance'],
      'SKILL-FA-001':['IAS 16','ASC 360 / ASC 250','FRS 102 Section 17','AASB 116'],
      'SKILL-IC-001':['IAS 21 / IFRS 10','ASC 830 / ASC 810','FRS 102 Sections 9 / 30','AASB 121 / AASB 10'],
      'SKILL-IMP-001':['IAS 36','ASC 350 / ASC 360','FRS 102 Sections 19 / 27','AASB 136'],
      'SKILL-TAX-001':['IAS 12','ASC 740','FRS 102 Section 29','AASB 112'],
      'SKILL-BEN-001':['IAS 19','Applicable ASC 710 / 712 / 715 / 420','FRS 102 Section 28','AASB 119'],
      'SKILL-DEBT-001':['IFRS 9 / IAS 32','Applicable ASC 470 / interest guidance','FRS 102 Sections 11 / 12','AASB 9 / AASB 132'],
      'SKILL-INT-001':['IAS 38','Applicable ASC 350 / 730 / 985','FRS 102 Section 18','AASB 138'],
      'SKILL-FV-001':['IFRS 13','ASC 820','Applicable FRS 102 fair-value guidance','AASB 13'],
      'SKILL-FX-001':['IAS 21','ASC 830','FRS 102 Section 30','AASB 121'],
      'SKILL-SBC-001':['IFRS 2','ASC 718','FRS 102 Section 26','AASB 2'],
      'SKILL-FS-001':['IAS 1 / IFRS 18 / IAS 7','Applicable ASC presentation / ASC 230','FRS 102 Sections 3–8','AASB 101 / AASB 18 / AASB 107']}
    if result['skill_id'] in additional and result['framework'] in ('IFRS','US_GAAP','UK_GAAP','AASB'):
        title=additional[result['skill_id']][('IFRS','US_GAAP','UK_GAAP','AASB').index(result['framework'])]
    citations=[{'title':title}] if result['evidence'] else []
    for claim in result['evidence']:
        claim_title='SEC issuer materiality and filing guidance' if '-SEC-' in claim['claim_id'] else title
        for ref in claim.get('references',[]):
            if isinstance(ref,str):
                confirmed=claim.get('reference_confidence')=='VERIFIED'
                locator=ref if confirmed else 'Unverified paragraph reference: '+ref
                citations.append({'title':claim_title,'locator':locator})
    # Never copy internal evidence limitations or arbitrary case text to public output.
    guidance=result['conclusion']+'\nReview status: '+result['status']+'\nCalculations: '+json.dumps(result['calculations'],default=serializable,sort_keys=True)+'\nJournals: '+json.dumps(result['journal_entry_implications'],default=serializable)+'\nDisclosure review: '+'; '.join(result['disclosures_impacted'])
    if result.get('specialist_routing'):
        route_info=result['specialist_routing']
        guidance+='\nSpecialist handoff: '+route_info['target']+'; required evidence: '+route_info['required_evidence']+'; '+route_info['completion_gate']
    public_topic=result['evidence'][0]['topic_id'] if result['evidence'] else result['specialist_routing']['topic_id']
    rec={'topic_id':public_topic,'guidance':guidance,
         'framework':result['framework'],'jurisdiction':result['jurisdiction'],
         'entity_scope':result['entities'][0],'effective_period':' to '.join(result['periods']),
         'limitations':result.get('uncertainties',[]),'uncertainties':result.get('open_items',[]),'citations':citations}
    return public_record(rec,route=route)

def serializable(obj):
    if isinstance(obj,Decimal): return str(obj)
    raise TypeError(type(obj).__name__)


def assess_case(package,case):
    """CAO-facing result adapter; unresolved cases return a structured handoff."""
    if package not in PACKAGES:raise ReviewRequired('Unknown accounting skill')
    if not isinstance(case,dict):case={}
    try:return execute(package,case)
    except (ReviewRequired,KeyError,TypeError,AttributeError,ArithmeticError) as exc:
        reason=str(exc)
        routes={
          'earnings-per-share':('TOPIC-08-007','EPS, equity, award, tax and instrument specialists','Legal share rights, complete dated shares/instruments, attributable earnings and qualified instrument methods'),
          'segment-reporting':('TOPIC-08-006','Segment accounting, management and financial reporting specialists','Actual CODM packs, components, aggregation/reportability judgments and reconciled entity-wide disclosures'),
          'subsequent-events':('TOPIC-08-005','Subsequent events, underlying accounting, legal and filing specialists','Authorized window, independent feed/event population, period-end conditions and completed underlying recognition'),
          'government-grants':('unmapped','Grant accounting and standards governance owner','Approved substantive framework-specific grant knowledge and actual agreements/compliance evidence'),
          'borrowing-costs':('TOPIC-04-003','Borrowing-cost accounting and standards governance owner','Substantive approved capitalization method, project and financing facts; CIP pointers are insufficient'),
          'cash-flow-reporting':('TOPIC-08-002','Cash reporting, Financial Statements, FX, Consolidation and Lease specialists','Bank/GL cash definitions, cash source population, indirect/direct bridge, classification and adopted-period memos'),
          'equity-capital':('TOPIC-08-003','Equity, legal capital, SBC and group specialists','Instrument/legal terms, cap table, owner approvals, component and NCI bridges'),
          'accounting-changes':('TOPIC-02-009','Technical accounting, tax/EPS, auditors and SEC securities counsel','Original facts/issued statements, policy/estimate/error analysis, both error measures, comparative bridges and filing evidence'),
          'going-concern':('TOPIC-08-005','Management, treasury, legal and going-concern reviewer','Authorized forecasts, maturities/covenants, feasible documented plans, downside evidence and framework assessment'),
          'commitments-contingencies':('TOPIC-13-008','Provisions, Financial Instruments, guarantee valuation and legal specialists','Complete contracts/claims register, legal probability/recognition analysis, guarantee measurement and disclosure proofs'),
          'related-parties':('TOPIC-08-006','Related-party, legal, Transfer Pricing and Consolidation specialists','Dated relationship declarations, complete source transactions, balances/commitments, terms, exemptions and arm-length support'),
          'month-end-close':('TOPIC-02-001','Close controller and transaction specialist','Frozen task, source, approval and lock histories; cutoff and error assessments'),
          'balance-sheet-reconciliations':('TOPIC-02-004','Account owner and reconciliation reviewer','Complete GL inventory, independent source proofs, item-level exceptions and approved corrections'),
          'accounts-receivable':('TOPIC-03-011','Revenue Recognition, ECL and collections specialists','Contract entitlement, credits, remittances, allowance and collection evidence'),
          'accounts-payable':('TOPIC-05-001','AP, procurement and liability specialist','PO, receipt, invoice, supplier confirmation, accrual and payment evidence'),
          'fixed-assets':('TOPIC-04-001','PPE, Impairment and Lease Accounting specialists','Cost eligibility, commissioning, components, engineering lives, disposal and gross GL proofs'),
          'intercompany-accounting':('TOPIC-07-003','Group accounting, Consolidation, FX and Transfer Pricing specialists','Bilateral contracts, confirmations, rates, recharge agreements and tax review'),
          'revenue-recognition':('TOPIC-03-001','Revenue technical accounting','Executed contracts, amendments, transfer evidence, pricing and policy analysis'),
          'financial-instruments-ecl':('TOPIC-06-007','Financial instruments specialist','Instrument contracts, classification, credit-adjusted measurement and model validation'),
          'provisions-contingencies':('TOPIC-05-003','Provision/legal/valuation specialist','Obligation/counsel evidence, outcome estimates, settlement timing and asset/recovery analysis'),
          'consolidation':('TOPIC-07-009','Group accounting and transaction specialist','Control/legal evidence, certified TBs, PPA, FX, ownership and elimination schedules'),
          'business-combinations':('TOPIC-13-001','Acquisition accounting, legal, tax and valuation specialists','SPA, control date, business definition, PPA, tax and consideration classification'),
          'asset-impairment':('TOPIC-04-006','Impairment and valuation specialist','Unit perimeter, indicators, forecasts, market values, discount inputs and allocation floors'),
          'income-taxes':('SUPPLEMENTAL_TAX','Tax, legal and underlying transaction specialists','Enacted law, tax bases, returns, jurisdictional recoverability, uncertainty, allocation and operative-period memos'),
          'inventory-cost':('unmapped','Inventory specialist and standards governance owner','Approved substantive costing and measurement knowledge; physical quantities, overhead and NRV evidence'),
          'employee-benefits-payroll':('TOPIC-05-005','Employee benefits, HR, employment-law and actuarial specialists','Complete service/entitlement populations, benefit classification and payroll/GL/cash proofs'),
          'debt-financing':('TOPIC-06-005','Debt, legal, instrument and treasury specialists','Executed terms, fee population, approved yields, reporting-date rights and modification conclusions'),
          'intangible-assets':('TOPIC-04-005','Intangible, software, acquisition and impairment specialists','Rights, project gates, cost eligibility, available dates, lives and register/GL bridges'),
          'fair-value-measurement':('TOPIC-06-008','Valuation and underlying accounting specialists','Measurement basis/unit/date, market evidence, significant inputs, reviewed valuations and GL/note proofs'),
          'foreign-currency':('TOPIC-06-003','Foreign currency and group accounting specialist','Functional currency memo, rate feed, transaction population, translated TBs and disposal rights'),
          'share-based-compensation':('TOPIC-05-007','Award accounting, legal and valuation specialist','Grant terms, approved classification, vesting census, valuations and event schedules'),
          'financial-statements':('TOPIC-08-009','Financial reporting and disclosure specialist','Authorized TB, period/entity checklist, comparatives, source-to-line and narrative tie-outs'),
        }
        topic,target,evidence=routes[package]
        return {'skill_id':PACKAGES[package][0],'status':'blocked','conclusion':'Accounting case cannot be completed: '+reason,
          'recommendation_class':'REQUIRED','facts_used':{k:v for k,v in case.items() if k not in ('assumptions','knowledge_review','reviewer_signoff')},
          'assumptions':case.get('assumptions',[]),'framework':case.get('framework','unresolved'),'jurisdiction':case.get('jurisdiction','unresolved'),
          'entities':[case.get('entity','unresolved')],'periods':[case.get('period_start','unresolved'),case.get('reporting_period','unresolved')],
          'method':'Blocked before certification; resolve missing facts/model route or specialist dependency',
          'calculations':{},'evidence':[],'judgments':[],'uncertainties':[reason],'confidence':'low','open_items':[reason],
          'journal_entry_implications':[],'controls_impacted':['No posting or certification until resolved'],
          'reporting_impacted':['Accounting conclusion incomplete'],'disclosures_impacted':['Assess pending matter and uncertainty before reporting'],
          'systems_impacted':['Maintain exception owner and source lineage'],'documentation_required':[evidence],
          'audit_evidence_required':[evidence],'related_artifacts':[],'memory_candidates':[],
          'specialist_routing':{'topic_id':topic,'target':target,'required_evidence':evidence,'completion_gate':'Reviewed framework-specific memo, reconciled schedules/journals and disclosure impacts; rerun case with new fingerprint'}}
