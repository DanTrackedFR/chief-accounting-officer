"""Structured, deterministic source checks. No reviewer or certification authority."""
from collections import Counter
from datetime import date, datetime
from decimal import Decimal
import re
from core_accounting import ReviewRequired, required, dec, cash

PROFILE = 'presumed_user_provided'
CHECKS = ('unique_identifiers', 'duplicate_invoices', 'arithmetic', 'control_totals',
          'gl_reconciliation', 'dates', 'cutoff', 'pre_readiness_disposal', 'signs_units',
          'currency', 'essential_inputs', 'roll_forward', 'depreciation_comparison',
          'qualified_outliers', 'impairment', 'leases', 'readiness', 'classification',
          'assumptions', 'movements', 'recognition', 'supplier_reconciliation')
STATES = ('PASS', 'WARNING', 'BLOCKED', 'NOT_PERFORMED')


def text(value, label):
    if not isinstance(value, str) or not value.strip(): raise ReviewRequired(label + ' must be nonblank text')
    return value


def attestation(value):
    if not isinstance(value, dict): raise ReviewRequired('Case-level source attestation required')
    required(value, 'authenticated_user_reference', 'timestamp', 'statement_version', 'represents_company_records')
    for k in ('authenticated_user_reference', 'timestamp', 'statement_version'): text(value[k], k)
    try:
        d = datetime.fromisoformat(value['timestamp'].replace('Z', '+00:00'))
        if d.tzinfo is None: raise ValueError()
    except ValueError: raise ReviewRequired('Source attestation requires timezone-qualified ISO timestamp') from None
    if value['represents_company_records'] is not True: raise ReviewRequired('Explicit company-record source assertion required')
    # Authenticated-user reference is asserted by the client. Service auth does
    # not turn it into authenticated independent reviewer identity.
    return dict(value)


def source(value):
    if not isinstance(value, dict): raise ReviewRequired('Versioned source reference required')
    for k in ('id', 'version', 'hash'): text(value.get(k), 'Source ' + k)
    if not re.fullmatch('[0-9a-f]{64}', value['hash']): raise ReviewRequired('Source hash must be SHA-256 hex')
    return dict(value)


def iso(value):
    try: return date.fromisoformat(value)
    except (TypeError, ValueError): raise ReviewRequired('Use ISO dates') from None


def number(value, *, positive=False):
    n = dec(value)
    if n < 0 or (positive and n == 0): raise ReviewRequired('Amount, units or life has an invalid sign')
    return n


def normalized(value): return ' '.join(text(value, 'Reference').casefold().split())


class Screening:
    def __init__(self, case):
        self.case = case
        self.source = source(case.get('source'))
        self.findings = []
        self.executed = set()
        self.blocked = set()
        self.population_restrictions = []

    def add(self, check, state, rows=(), explanation='', *, observed=None, expected=None,
            blocks=False, resolution='', population=False):
        if check not in CHECKS or state not in STATES: raise ValueError('Unknown source check')
        self.executed.add(check)
        rowrefs = list(rows)
        item = dict(check_id=check, severity=state, source_reference=self.source['id'],
                    row_references=rowrefs, explanation=explanation,
                    blocks_calculation=blocks, resolution=resolution)
        if observed is not None: item['observed'] = str(observed)
        if expected is not None: item['expected'] = str(expected)
        self.findings.append(item)
        if blocks: self.blocked.update(rowrefs)
        if population: self.population_restrictions.append(check)

    def rows(self, key, *, required_population=False):
        value = self.case.get(key, [])
        if not isinstance(value, list) or any(not isinstance(r, dict) for r in value):
            raise ReviewRequired('Source rows must be an array of objects: ' + key)
        if required_population and not value: raise ReviewRequired('Nonempty source population required: ' + key)
        ids = []
        for i, row in enumerate(value):
            ref = key + ':' + str(i + 1)
            if not isinstance(row.get('id'), str) or not row['id'].strip():
                self.add('essential_inputs', 'BLOCKED', [ref], 'Missing source row identifier.', blocks=True,
                         resolution='Supply a unique row identifier.')
            else: ids.append(row['id'])
        duplicates = {k for k, n in Counter(ids).items() if n > 1}
        for i, row in enumerate(value):
            if row.get('id') in duplicates:
                self.add('unique_identifiers', 'BLOCKED', [key+':'+str(i+1)], 'Duplicate row identifier.',
                         blocks=True, resolution='Resolve duplicate source identifiers.')
        if not duplicates: self.add('unique_identifiers', 'PASS', explanation='Supplied identifiers checked within '+key+'.')
        # Independent date/currency checks remain evaluable even if another
        # calculation prerequisite is missing. Do not invent dependent checks.
        for i,row in enumerate(value):
            ref=key+':'+str(i+1)
            for field in ('date','ready_date','invoice_date','received_date','payment_date','reversal_date'):
                if field in row:
                    try:iso(row[field])
                    except ReviewRequired:
                        self.add('dates','BLOCKED',[ref],'Invalid supplied date.',blocks=True,resolution='Supply a valid ISO date for '+field+'.')
                        self.findings[-1]['field_path']=key+'['+str(i+1)+'].'+field
            if 'currency' in row or 'entity' in row:self.currency(row,ref)
            quantity=row.get('quantity',row.get('units'))
            if quantity is not None and 'unit_price' in row and 'amount' in row:
                try:self.compare('arithmetic',row['amount'],number(quantity)*number(row['unit_price']),[ref],label='Quantity times unit price',blocks=True)
                except ReviewRequired:self.add('signs_units','BLOCKED',[ref],'Invalid quantity, unit price or amount.',blocks=True,resolution='Supply consistent numeric inputs and units.')
        return value

    def row(self, key, i, row, fn):
        ref = key + ':' + str(i+1)
        try: return fn(row, ref)
        except (ReviewRequired, KeyError, TypeError, ArithmeticError) as exc:
            # Never copy arbitrary source text/identities into diagnostic prose.
            message = str(exc) if isinstance(exc, ReviewRequired) else 'Missing or malformed essential accounting input'
            check = 'dates' if 'date' in message.lower() else 'signs_units' if 'sign' in message.lower() else 'essential_inputs'
            self.add(check, 'BLOCKED', [ref], message, blocks=True,
                     resolution='Correct the affected input and resubmit a new Case.')
            return None

    def compare(self, check, supplied, calculated, rows=(), *, label, blocks=False):
        try:actual = cash(supplied); expected = cash(calculated)
        except (ReviewRequired,TypeError,ArithmeticError):
            self.add(check,'BLOCKED' if blocks else 'WARNING',rows,'Supplied comparison value is invalid.',
                     blocks=blocks,population=check in ('gl_reconciliation','control_totals','supplier_reconciliation'),
                     resolution='Supply a valid numeric comparison value.')
            return False
        match = actual == expected
        self.add(check, 'PASS' if match else 'BLOCKED' if blocks else 'WARNING', rows,
                 label + (' agrees.' if match else ' differs from calculation.'),
                 observed=actual, expected=expected, blocks=blocks and not match,
                 population=not match and check in ('gl_reconciliation', 'control_totals', 'supplier_reconciliation'),
                 resolution='' if match else 'Explain and resolve the difference; population reconciliation is unestablished.')
        return match

    def currency(self, row, ref):
        currency = row.get('currency', self.case['functional_currency'])
        if currency != self.case['functional_currency']:
            self.add('currency', 'BLOCKED', [ref], 'Source currency differs from functional currency.',
                     blocks=True, resolution='Supply supported functional-currency amounts; this profile performs no FX conversion.')
            return False
        if row.get('entity', self.case['entity']) != self.case['entity']:
            self.add('currency', 'BLOCKED', [ref], 'Source entity differs from Case scope.', blocks=True,
                     resolution='Separate the entity population.')
            return False
        self.add('currency', 'PASS', [ref], 'Currency and entity scope agree.')
        return True

    def norms(self, row, ref, resolved):
        norms = self.case.get('class_norms', {}).get(row.get('class'), {})
        if not norms: return
        required(norms, 'basis', 'version', 'framework', 'effective_from', 'effective_to', 'entity', 'ranges')
        if (norms['entity'] != self.case['entity'] or norms['framework'] != self.case['framework'] or
            not iso(norms['effective_from']) <= iso(self.case['period_start']) <= iso(self.case['reporting_period']) <= iso(norms['effective_to'])):
            raise ReviewRequired('Company/class norm applicability unresolved')
        text(norms['basis'], 'Norm basis'); text(norms['version'], 'Norm version')
        for key, bounds in norms['ranges'].items():
            if key not in resolved: continue
            lo, hi = number(bounds['min']), number(bounds['max'])
            if lo > hi: raise ReviewRequired('Invalid company norm range')
            n = dec(resolved[key]); outside = n < lo or n > hi
            self.add('qualified_outliers', 'WARNING' if outside else 'PASS', [ref],
                     'Value is outside qualified company/class range.' if outside else 'Value is within qualified company/class range.',
                     observed=n, expected=str(lo)+' to '+str(hi),
                     resolution='Investigate the unusual value; no alternative assumption was substituted.' if outside else '')

    def report(self):
        for check in CHECKS:
            if check not in self.executed:
                self.add(check, 'NOT_PERFORMED', explanation='Applicable evidence or qualified comparison basis was not supplied; no pass is inferred.')
        return dict(profile=PROFILE, findings=self.findings,
                    population_status='UNRECONCILED' if self.population_restrictions or self.blocked else 'SUPPLIED_FILE_BOUNDED',
                    completeness='PRESUMED_FROM_SUPPLIED_FILE_NOT_INDEPENDENTLY_VERIFIED',
                    excluded_rows=sorted(self.blocked), limitations=[
                        'Screening covers supplied structured facts; absence of an indicator is not proof the underlying issue cannot exist.',
                        'No independent verification of source completeness or client identity assertion was performed.'])
