"""Profile 1.2 source qualification inside the existing governed production runtime.

No source-review objects are generated. Existing approved methods and exact
framework/period qualification are reused; structured observations are facts,
not certification. Native accounting remains partial and journals are proposals.
"""
import copy
import json
import re
from collections import Counter
from decimal import Decimal
from fractions import Fraction
from calendar import isleap, monthrange
from datetime import date, timedelta
from core_accounting import ReviewRequired, required, cash, journal, balance
from source_screening import PROFILE, Screening, attestation, iso, number, normalized, text, identifier, disposal_input
from prepared_execution import MODE, qualify, reject_records

ZERO = Decimal(0)


def issue(identifier, path, explanation, category='missing_fact'):
    return dict(identifier=identifier, field_path=path, explanation=explanation, category=category)


SCOPE_FIELDS = ('entity', 'jurisdiction', 'framework', 'period_start', 'reporting_period', 'functional_currency')


def scope_requirements(case, expected=None, prefix=''):
    """Shared Profile 1.2 scope checks, including immutable adapter identity."""
    needs=[]
    for key in SCOPE_FIELDS:
        value=case.get(key)
        reason=('missing' if key not in case else 'null' if value is None else
                'invalid_type' if not isinstance(value,str) else 'blank' if not value.strip() else None)
        if reason is None and key in ('period_start','reporting_period'):
            try:iso(value)
            except ReviewRequired:reason='invalid_date'
        if reason is None and key=='framework' and value not in ('IFRS','US_GAAP','UK_GAAP','AASB'):reason='unsupported'
        if reason is None and key=='functional_currency' and (not re.fullmatch('[A-Z]{3}',value) or value=='XXX'):reason='unsupported'
        if reason is None and expected is not None and value!=expected[key]:reason='identity_conflict'
        if reason:
            needs.append(issue('scope.'+key+'.'+reason,prefix+key,
                'Supply '+key.replace('_',' ')+' matching the selected Case scope ('+reason.replace('_',' ')+').',
                'missing_fact' if reason in ('missing','null','blank') else 'invalid_fact'))
    return needs


def independent_row_requirements(case, prefix=''):
    """Only prerequisites independent of invalid scope; no accounting conclusions."""
    needs=[]
    for table,fields in (('assets',('opening_cost','opening_accumulated','ready_date')),):
        for i,row in enumerate(case.get(table,[]) if isinstance(case.get(table,[]),list) else []):
            if not isinstance(row,dict):continue
            for field in fields:
                if row.get(field) in (None,''):
                    path=prefix+table+'['+str(i+1)+'].'+field
                    needs.append(issue('row.'+table+'.'+str(i+1)+'.'+field,path,'Supply '+field.replace('_',' ')+'.'))
    return needs


def requirements(package, case):
    """Only enumerate prerequisites evaluable at this stage; never guess consequences."""
    found = scope_requirements(case)
    populations=('assets','costs','cip','invoices','accruals','payments','supplier_balances')
    if sum(len(case[k]) for k in populations if isinstance(case.get(k),list))>200:
        found.append(issue('bounds.population','source','This profile supports at most 200 supplied rows per Case; partition the population and reconcile the partitions.','invalid_fact'))
    try: identifier(case.get('case_id'), 'Source Case identifier')
    except ReviewRequired:
        found.append(issue('invalid.case_id', 'case_id', 'Supply a nonblank source Case identifier of at most 256 characters.', 'invalid_fact'))
    fields = ['case_id', 'framework', 'jurisdiction', 'entity', 'entity_type', 'period_start',
              'reporting_period', 'functional_currency', 'assumptions', 'source', 'source_attestation']
    if case.get('framework') == 'UK_GAAP': fields += ['uk_standard', 'uk_standard_edition']
    if case.get('framework') == 'AASB': fields += ['aasb_compilation', 'reporting_tier']
    if case.get('framework') == 'US_GAAP': fields += ['us_entity_type']
    for key in fields:
        if key not in SCOPE_FIELDS and case.get(key) in (None, ''): found.append(issue('missing.'+key, key, 'Supply '+key.replace('_',' ')+'.'))
    for key, children in [('source', ('id','version','hash')),
                          ('source_attestation', ('authenticated_user_reference','timestamp','statement_version','represents_company_records'))]:
        if isinstance(case.get(key),dict):
            for child in children:
                if case[key].get(child) in (None, ''):
                    found.append(issue('missing.'+key+'.'+child, key+'.'+child, 'Supply '+child.replace('_',' ')+'.'))
    if 'framework' in case and case['framework'] not in ('IFRS','US_GAAP','UK_GAAP','AASB'):
        found.append(issue('scope.framework','framework','Unsupported accounting framework.','unsupported_scope'))
    if case.get('functional_currency') is not None and (not isinstance(case['functional_currency'],str) or not re.fullmatch('[A-Z]{3}',case['functional_currency']) or case['functional_currency']=='XXX'):
        found.append(issue('scope.functional_currency','functional_currency','Supply a supported functional-currency code.','unsupported_scope'))
    if 'entity_type' in case and case['entity_type']!='for_profit':
        found.append(issue('scope.entity_type','entity_type','This profile requires an ordinary commercial for-profit entity.','unsupported_scope'))
    for field in ('period_start','reporting_period'):
        if case.get(field) not in (None,''):
            try:
                d=iso(case[field])
                if d.year!=2026:found.append(issue('scope.'+field,field,'This profile supports reporting periods wholly within 2026.','unsupported_scope'))
            except ReviewRequired:found.append(issue('invalid.'+field,field,'Supply a valid ISO reporting date.','invalid_fact'))
    if not isinstance(case.get('assumptions',[]),list) or any(not isinstance(v,str) for v in case.get('assumptions',[])):
        found.append(issue('invalid.assumptions','assumptions','Assumptions must be an array.','invalid_fact'))
    for key in ('source','source_attestation'):
        value=case.get(key)
        if value is not None and not isinstance(value,dict):
            found.append(issue('invalid.'+key,key,'Supply an object for '+key.replace('_',' ')+'.','invalid_fact'))
    src=case.get('source')
    if isinstance(src,dict):
        for key in ('id','version','hash'):
            if src.get(key) not in (None,'') and (not isinstance(src[key],str) or not src[key].strip()):
                found.append(issue('invalid.source.'+key,'source.'+key,'Supply nonblank source '+key+'.','invalid_fact'))
        if isinstance(src.get('hash'),str) and src['hash'] and not re.fullmatch('[0-9a-f]{64}',src['hash']):
            found.append(issue('invalid.source.hash','source.hash','Supply a SHA-256 source hash.','invalid_fact'))
    attest=case.get('source_attestation')
    if isinstance(attest,dict):
        for key in ('authenticated_user_reference','statement_version'):
            if attest.get(key) not in (None,'') and (not isinstance(attest[key],str) or not attest[key].strip()):
                found.append(issue('invalid.attestation.'+key,'source_attestation.'+key,'Supply a nonblank client assertion field.','invalid_fact'))
        if 'represents_company_records' in attest and attest['represents_company_records'] is not True:
            found.append(issue('invalid.attestation.assertion','source_attestation.represents_company_records','Explicit company-record assertion must be true.','invalid_fact'))
        if attest.get('timestamp') not in (None,''):
            from datetime import datetime
            try:
                timestamp=datetime.fromisoformat(attest['timestamp'].replace('Z','+00:00'))
                if timestamp.tzinfo is None:raise ValueError()
            except (ValueError,TypeError,AttributeError):
                found.append(issue('invalid.attestation.timestamp','source_attestation.timestamp','Supply a timezone-qualified ISO attestation timestamp.','invalid_fact'))
    fw=case.get('framework')
    for condition,field,explanation in (
        (fw=='US_GAAP' and case.get('us_entity_type') not in (None,'','private_company'),'us_entity_type','Only ordinary private-company US GAAP is supported.'),
        (fw=='UK_GAAP' and case.get('uk_standard') not in (None,'','FRS_102'),'uk_standard','FRS 102 is required.'),
        (fw=='UK_GAAP' and case.get('uk_standard_edition') not in (None,'','2026'),'uk_standard_edition','FRS 102 2026 applicability is required.'),
        (fw=='AASB' and 'reporting_tier' in case and (type(case['reporting_tier']) is not int or case['reporting_tier'] not in (1,2)),'reporting_tier','AASB integer reporting Tier 1 or 2 is required.'),
        (fw=='AASB' and case.get('aasb_compilation') not in (None,'','2026'),'aasb_compilation','AASB 2026 applicability is required.'),
        (case.get('regulatory_overlays') not in (None,[]),'regulatory_overlays','Regulatory overlays require separate applicability assessment.'),
        (case.get('package',package)!=package,'package','Selected source package must match the accounting owner.')):
        if condition:found.append(issue('scope.'+field,field,explanation,'unsupported_scope'))
    if case.get('source_assurance') != PROFILE:
        found.append(issue('scope.source_assurance','source_assurance','Explicit source-assurance profile required.','unsupported_scope'))
    if case.get('review_mode') != MODE:
        found.append(issue('scope.review_mode','review_mode','Profile 1.2 requires prepared-unreviewed execution.','unsupported_scope'))
    if package=='fixed-assets':
        _,policy_needs=depreciation_policy(case)
        found.extend(policy_needs)
    elif case.get('policy_elections',{}) != {}:
        found.append(issue('scope.policy_elections','policy_elections','Supplied elections require a separately supported method.','unsupported_scope'))
    if package not in ('fixed-assets','accounts-payable'):
        found.append(issue('scope.package','package','This source profile is unavailable for the selected package.','unsupported_scope'))
    return found


def resolved_row(case, row, screening, ref):
    result = copy.deepcopy(row)
    cls = row.get('class')
    assumptions = case.get('class_assumptions', {})
    if not isinstance(assumptions, dict): raise ReviewRequired('Class assumptions must be an object')
    policy = assumptions.get(cls, {}) if cls is not None else {}
    if policy:
        required(policy,'framework','entity','effective_from','effective_to','policy_version')
        text(policy['policy_version'],'Policy version')
        if (policy['framework'] != case['framework'] or policy['entity'] != case['entity'] or
            not iso(policy['effective_from']) <= iso(case['period_start']) <= iso(case['reporting_period']) <= iso(policy['effective_to'])):
            raise ReviewRequired('Class assumption applicability unresolved')
        for key in ('remaining_life','remaining_life_months','remaining_life_unit','residual','method','scope','capitalization_threshold','account','recognition_basis'):
            if key in ('remaining_life','remaining_life_months','remaining_life_unit') and any(k in row for k in ('remaining_life','remaining_life_months')):continue
            if key in policy and key not in result: result[key] = policy[key]
        screening.add('assumptions','PASS',[ref],'Applicable company class assumptions applied; row-specific inputs take precedence.')
    return result


def missing_row(screening, row, keys, ref):
    missing = [k for k in keys if row.get(k) in (None,'')]
    for key in missing:
        screening.add('essential_inputs','BLOCKED',[ref], 'Supply '+key.replace('_',' ')+'.',
                      blocks=True, resolution='Supply the required field '+key+'.')
        screening.findings[-1]['field_path'] = ref.replace(':','[')+'].'+key
    return bool(missing)


def specialist(screening,row,ref,package):
    indicators = ('impairment_indicator','lease_like','held_for_sale','sale_leaseback','replacement_component') if package=='fixed-assets' else ('supplier_financing','related_party','disputed_obligation')
    blocked = False
    description = str(row.get('description','')).casefold()
    textual = {'lease_like': ('leased','lease','rental'), 'impairment_indicator': ('damaged','obsolete','impair','idle'),
               'held_for_sale': ('held for sale',), 'sale_leaseback': ('leaseback',), 'supplier_financing': ('reverse factoring','supplier finance'),
               'disputed_obligation': ('disputed','dispute','disputes','disputing')}
    for key in indicators:
        if key in row and type(row[key]) is not bool: raise ReviewRequired('Specialist indicator must be an explicit boolean')
        indicator_text=description
        if key=='disputed_obligation':
            indicator_text=re.sub(r'\b(?:not|never)\s+(?:currently\s+)?(?:disputed|disputing|dispute|disputes)\b|\bno\s+(?:outstanding\s+)?disputes?\b|\bundisputed\b','',description)
        present = row.get(key) is True or any(re.search(r'\b'+re.escape(token)+r'\b',indicator_text) for token in textual.get(key,()))
        check = 'leases' if key in ('lease_like','sale_leaseback') else 'impairment' if key=='impairment_indicator' else 'classification'
        screening.add(check,'BLOCKED' if present else 'PASS',[ref],
                      'Supplied facts indicate a specialist accounting route: '+key.replace('_',' ')+'.' if present else
                      'No '+key.replace('_',' ')+' indicator detected in the supplied structured facts.',
                      blocks=present,resolution='Supply sufficient specialist-route evidence; this profile cannot infer its conclusion.' if present else '')
        if present:screening.findings[-1]['field_path']=ref.replace(':','[')+'].'+key
        blocked |= present
    return blocked


def totals(screening, rows, amounts, calculated):
    controls = screening.case.get('control_totals',{})
    if not isinstance(controls,dict): raise ReviewRequired('Control totals must be an object')
    if 'record_count' in controls:
        if type(controls['record_count']) is not int or controls['record_count'] < 0:screening.add('control_totals','WARNING',explanation='Supplied record count is invalid; completeness agreement is unestablished.',population=True,resolution='Supply a nonnegative integer control count.')
        else:screening.compare('control_totals',controls['record_count'],len(rows),label='Supplied record count')
    if 'amount' in controls:
        if amounts is None:
            screening.add('control_totals','NOT_PERFORMED', explanation='Full supplied amount cannot be calculated because some amounts are invalid.',population=True)
        else:
            try:screening.compare('control_totals',controls['amount'],sum(amounts,ZERO),label='Supplied source monetary total')
            except (ReviewRequired,TypeError,ArithmeticError):screening.add('control_totals','WARNING',explanation='Supplied control amount is invalid; population agreement is unestablished.',population=True,resolution='Supply a valid control amount.')
    def compare(check,supplied,calculated,label):
        try:screening.compare(check,supplied,calculated,label=label)
        except (ReviewRequired,TypeError,ArithmeticError):screening.add(check,'WARNING',explanation='Supplied comparison value is invalid; population agreement is unestablished.',population=True,resolution='Supply a valid control or GL amount.')
    for key, value in screening.case.get('gl',{}).items():
        key = {'cost':'closing_cost','accumulated':'closing_accumulated','cip':'closing_cip'}.get(key,key)
        if key in calculated:
            if screening.blocked:
                screening.add('gl_reconciliation','NOT_PERFORMED',explanation='Excluded rows prevent a complete-population GL comparison.',population=True)
            else: compare('gl_reconciliation',value,calculated[key],'Supplied GL '+key.replace('_',' '))
        else:screening.add('gl_reconciliation','NOT_PERFORMED',explanation='Supplied GL dimension has no supported population calculation in this Case.',population=True)
    return dict(record_count=len(rows), monetary_total=None if amounts is None else cash(sum(amounts,ZERO)))


def depreciation_policy(case):
    """Source assertions are policies only when explicitly confirmed and applicable.

    Memory remains context-only; it must be confirmed into asset_policy before use.
    Never choose one side of a confirmed-policy conflict.
    """
    needs=[]
    elections=case.get('policy_elections',{})
    allowed={'depreciation_convention':('monthly','actual_days'),
             'partial_month_treatment':('actual_days_in_month',)}
    def validate(values,path):
        if not isinstance(values,dict):
            needs.append(issue('policy.'+path,path,'Supply a structured depreciation policy election.','invalid_fact'));return {}
        out={}
        for key,value in values.items():
            if key not in allowed or value not in allowed[key]:
                needs.append(issue('policy.'+path+'.'+key,path+'.'+key,'Unsupported policy election; use monthly or actual_days and explicit actual_days_in_month for partial monthly periods.','unsupported_scope'))
            else:out[key]=value
        if 'partial_month_treatment' in out and out.get('depreciation_convention')!='monthly':
            needs.append(issue('policy.partial_basis',path+'.partial_month_treatment','Partial-month treatment requires the monthly convention.','invalid_fact'))
        return out
    selected=validate(elections,'policy_elections')
    provenance='case_election' if selected else 'engine_default_unconfirmed'
    policy=case.get('asset_policy',{})
    if not isinstance(policy,dict):
        needs.append(issue('policy.asset_policy','asset_policy','Supply a policy object.','invalid_fact'));policy={}
    governed={k:policy[k] for k in allowed if k in policy}
    if governed:
        validated=validate(governed,'asset_policy')
        valid=True
        for key in ('confirmation','entity','framework','effective_from','effective_to','policy_version'):
            if not isinstance(policy.get(key),str) or not policy[key].strip():
                needs.append(issue('policy.asset_policy.'+key,'asset_policy.'+key,'Supply explicitly confirmed, entity/framework/period-qualified company policy.'));valid=False
        if valid:
            try:
                valid=(policy['confirmation']=='confirmed' and policy['entity']==case.get('entity') and
                       policy['framework']==case.get('framework') and
                       iso(policy['effective_from'])<=iso(case['period_start'])<=iso(case['reporting_period'])<=iso(policy['effective_to']))
            except (ReviewRequired,KeyError):valid=False
            if not valid:needs.append(issue('policy.applicability','asset_policy','Confirmed company policy is unconfirmed or outside the Case entity/framework/effective window.','invalid_fact'))
        if valid:
            for key,value in selected.items():
                if key not in validated or validated[key]!=value:
                    needs.append(issue('policy.conflict.'+key,'policy_elections.'+key,'Case election conflicts with confirmed company policy; resolve through an explicit governed policy change.','invalid_fact'))
            selected=validated;provenance='confirmed_company_policy_client_asserted'
    return dict(convention=selected.get('depreciation_convention','actual_days'),
                partial_month_treatment=selected.get('partial_month_treatment'),provenance=provenance),needs


def monthly_charge(start,end,basis,months,partial):
    if end<start:return ZERO
    fraction=Fraction(0);d=start
    while d<=end:
        days=monthrange(d.year,d.month)[1];last=min(end,date(d.year,d.month,days))
        if d.day==1 and last.day==days:fraction+=1
        elif partial=='actual_days_in_month':fraction+=Fraction((last-d).days+1,days)
        else:raise ReviewRequired('Monthly partial-period treatment unresolved; explicitly elect actual_days_in_month for reporting stubs, mid-month availability or disposal.')
        d=last+timedelta(days=1)
    value=min(Fraction(basis),Fraction(basis)/Fraction(months)*fraction)
    return cash(Decimal(value.numerator)/Decimal(value.denominator))


def remaining_months(row, screening, ref):
    """Validate both life fields before using either; exact decimal years × 12."""
    keys=('remaining_life','remaining_life_months')
    supplied=[key for key in keys if key in row]
    values={}
    def fail(key, message):
        screening.add('signs_units','BLOCKED',[ref],message,blocks=True,
            resolution='Confirm remaining useful life: remaining_life is years; remaining_life_months is months.')
        screening.findings[-1]['field_path']=ref.replace(':','[')+'].'+key
    if 'remaining_life_unit' in row and row['remaining_life_unit']!='years':
        fail('remaining_life_unit','Invalid remaining-life units; remaining_life represents years. Use remaining_life_months for months.')
    if not supplied:fail('remaining_life','Missing remaining useful life; supply years or remaining_life_months.')
    for key in supplied:
        value=row[key]
        if value is None:
            fail(key,'Null remaining useful life; supply a numeric life in the named field units.');continue
        try:
            from core_accounting import dec
            n=dec(value)
        except ReviewRequired:
            fail(key,'Nonnumeric remaining useful life; supply a finite decimal in '+('years.' if key=='remaining_life' else 'months.'));continue
        if n<ZERO:fail(key,'Negative remaining useful life; supplied life data is inconsistent.');continue
        if n==ZERO:
            fail(key,'Useful life exhausted: the stated useful life has elapsed. Assess the remaining depreciable balance or useful-life estimate; an asset still in use is not automatically disposed of.');continue
        values[key]=n*12 if key=='remaining_life' else n
    if len(values)==2 and values[keys[0]]!=values[keys[1]]:
        for key in keys:fail(key,'Conflicting remaining-life assumptions: years multiplied by 12 must equal remaining_life_months; neither was selected.')
    return next(iter(values.values()),None)


def actual_charge(start, end, basis, months):
    """Exact rational fraction, rounded once to cents, capped at remaining basis."""
    if end<start:return ZERO
    fraction=Fraction(0);d=start
    while d<=end:
        last=min(end,date(d.year,12,31))
        fraction+=Fraction((last-d).days+1,366 if isleap(d.year) else 365)
        d=last+timedelta(days=1)
    value=min(Fraction(basis),Fraction(basis)*12/Fraction(months)*fraction)
    return cash(Decimal(value.numerator)/Decimal(value.denominator))


def fixed_assets(case, screening):
    import production
    charge = production.load_workflow('fixed-assets').charge
    assets = screening.rows('assets', required_population=True)
    costs = screening.rows('costs'); cip = screening.rows('cip')
    work=[];costwork=[]; entries=[]; expenses=ZERO; input_amounts=[]
    capital_entries=[]
    selected_policy,_=depreciation_policy(case)
    additions={row.get('id'):ZERO for row in assets if isinstance(row.get('id'),str)}
    expensed_destinations=set()
    def resolve_cost(raw,ref):
        value=copy.deepcopy(raw)
        targets=[a for a in assets if a.get('id')==value.get('destination')] if value.get('destination') is not None else []
        target=resolved_row(case,targets[0],screening,ref) if len(targets)==1 else {}
        if 'class' not in value and 'class' in target:value['class']=target['class']
        value=resolved_row(case,value,screening,ref)
        if 'capitalization_threshold' in target:
            if 'capitalization_threshold' in value and number(value['capitalization_threshold'])!=number(target['capitalization_threshold']):
                raise ReviewRequired('Conflicting capitalization thresholds for one asset unit')
            value.setdefault('capitalization_threshold',target['capitalization_threshold'])
        return value
    def cost_row(raw,ref):
        row=resolve_cost(raw,ref)
        screening.numeric_inputs(row,ref)
        if missing_row(screening,row,('amount','kind','date','offset'),ref):return
        if ref in screening.blocked or not screening.currency(row,ref):return
        if not iso(case['period_start'])<=iso(row['date'])<=iso(case['reporting_period']):raise ReviewRequired('Cost date outside reporting period')
        text(row['offset'],'Offset account')
        if specialist(screening,row,ref,'fixed-assets'):return
        n=number(row['amount'],positive=True)
        excluded=row['kind'] in ('training','general_overhead','abnormal_waste')
        if row['kind'] not in ('purchase','freight','installation','training','general_overhead','abnormal_waste'):raise ReviewRequired('Cost classification is ambiguous or requires a specialist route')
        if 'eligible' in row and type(row['eligible']) is not bool:raise ReviewRequired('Eligibility input must be an explicit boolean')
        below=False
        if 'capitalization_threshold' in row and not excluded and row.get('eligible') is not False:
            if missing_row(screening,row,('destination',),ref):return
            target=[a for a in assets if a.get('id')==row['destination']]
            if len(target)!=1:raise ReviewRequired('Threshold requires one supported asset unit of account')
            qualifying=number(target[0]['opening_cost'])
            for related in costs:
                if related.get('destination')==row['destination'] and related.get('kind') in ('purchase','freight','installation') and related.get('eligible') is not False:
                    qualified=resolve_cost(related,ref)
                    if 'capitalization_threshold' in qualified and number(qualified['capitalization_threshold'])!=number(row['capitalization_threshold']):raise ReviewRequired('Conflicting asset capitalization thresholds')
                    qualifying+=number(related['amount'],positive=True)
            below=qualifying<number(row['capitalization_threshold'])

        if excluded or row.get('eligible') is False or below:
            if missing_row(screening,row,('account',),ref):return
            text(row['account'],'Expense account')
            entries.append(journal(('Dr',row['account'],n),('Cr',row['offset'],n)))
            if row.get('destination') is not None:expensed_destinations.add(row['destination'])
            screening.add('classification','PASS',[ref],
                'Training, general overhead and abnormal waste are expensed under the governed cost method.' if excluded else 'Cost is expensed using the explicit eligibility or applicable company capitalization threshold.')
            return ('expense',n,dict(row_reference=ref,assumption_class=row.get('class'),applied_assumptions={k:row[k] for k in ('capitalization_threshold',) if k in row}))
        if missing_row(screening,row,('destination',),ref):return
        targets=[r for r in assets if r.get('id')==row['destination']]
        if len(targets)!=1:raise ReviewRequired('Cost destination must identify one supplied asset')
        target=resolved_row(case,targets[0],screening,ref)
        target_ref='assets:'+str(assets.index(targets[0])+1)
        if target_ref in screening.blocked:raise ReviewRequired('Linked asset source scope or date is unresolved')
        ready=iso(target.get('ready_date'))
        if ready>iso(case['reporting_period']):raise ReviewRequired('Uncommissioned costs require supported CIP treatment, not a PPE proposal')
        disposal=disposal_input(target)
        if disposal.get('enabled'):
            if disposal.get('ordinary_sale') is not True or iso(disposal.get('date'))<ready:raise ReviewRequired('Destination disposal accounting route or chronology is unresolved')
        if target.get('scope')!='ordinary_ppe' or target.get('asset_type','machinery')!='machinery' or target.get('model','cost')!='cost':raise ReviewRequired('Capital cost destination is outside ordinary machinery cost-method scope')
        if specialist(screening,target,ref,'fixed-assets'):return
        if iso(row['date'])>iso(targets[0].get('ready_date')):raise ReviewRequired('Post-readiness improvement/component cost requires supported specialist route')
        additions[row['destination']]+=n
        entries.append(journal(('Dr','PPE cost',n),('Cr',row['offset'],n)))
        capital_entries.append((ref,target_ref,entries[-1]))
        screening.add('classification','PASS',[ref],'Ordinary purchase, freight or installation cost directly attributable before readiness is capitalized under the governed cost method.')
        return ('capital',n,dict(row_reference=ref,assumption_class=row.get('class'),applied_assumptions={k:row[k] for k in ('capitalization_threshold',) if k in row}))
    for i,row in enumerate(costs):
        value=screening.row('costs',i,row,cost_row)
        if value is not None:
            costwork.append(value[2])
            if value[0]=='expense':expenses+=value[1]
    for i,row in enumerate(cip):
        screening.add('movements','BLOCKED',['cip:'+str(i+1)],'CIP commissioning or transfer requires a supported movement assessment.',blocks=True,resolution='Use the existing governed CIP movement workflow or supply a commissioned machinery register.')
    # Selective blocking respects calculation dependencies: an unresolved cost
    # cannot leave the affected asset's depreciable basis apparently supported.
    for key,rows in [('costs',costs),('cip',cip)]:
        for i,row in enumerate(rows):
            if key+':'+str(i+1) not in screening.blocked:continue
            destination=row.get('destination',row.get('asset_id'))
            for j,asset in enumerate(assets):
                if destination is None or asset.get('id')==destination:
                    screening.add('movements','BLOCKED',['assets:'+str(j+1)],'Unresolved related cost/project movement affects this asset basis.',blocks=True,resolution='Resolve the linked source movement before depreciating this asset.')
    def calculate(raw,ref):
        row_entries=[]
        row=resolved_row(case,raw,screening,ref)
        screening.numeric_inputs(row,ref)
        specialist(screening,row,ref,'fixed-assets')
        needed=('opening_cost','opening_accumulated','residual','ready_date','method','scope')
        # Fully expensed zero-opening destinations have no depreciation basis
        # and do not need an unused remaining-life assumption.
        zero_expensed=False
        try:zero_expensed=row.get('id') in expensed_destinations and number(row.get('opening_cost'))==ZERO and number(row.get('opening_accumulated'))==ZERO and additions.get(row.get('id'),ZERO)==ZERO
        except ReviewRequired:pass
        if not zero_expensed:
            if row.get('method')=='straight_line':life_months=remaining_months(row,screening,ref)
            elif row.get('method')=='units_of_production':needed+=('remaining_units','period_units')
        if missing_row(screening,row,needed,ref):return
        if ref in screening.blocked:return
        if not screening.currency(row,ref):return
        if row['scope']!='ordinary_ppe' or row.get('asset_type','machinery')!='machinery':raise ReviewRequired('Only ordinary machinery cost-method scope is supported')
        if row.get('model','cost')!='cost':raise ReviewRequired('Only the ordinary cost method is supported')
        if row.get('change',{}).get('enabled') or any(row.get(k) not in (None,0,'0') for k in ('additions','transfers','revaluation')):
            raise ReviewRequired('Register movement or estimate change requires separately supported evidence')
        opening_cost=number(row['opening_cost']);acc=number(row['opening_accumulated']);res=number(row['residual'])
        if acc>opening_cost:raise ReviewRequired('Opening accumulated depreciation exceeds opening cost; current movements cannot cure the opening balance')
        cost=opening_cost+additions.get(row['id'],ZERO)
        if acc>cost:raise ReviewRequired('Accumulated depreciation exceeds supported cost')
        if res>cost-acc:screening.add('assumptions','WARNING',[ref],'Supplied residual exceeds current carrying amount; depreciation is zero while this persists.',resolution='Confirm the current residual assumption; no replacement was assumed.')
        ready=iso(row['ready_date']);start=iso(case['period_start']);end=iso(case['reporting_period']);last=end
        disp=disposal_input(row)
        if disp.get('enabled'):
            if missing_row(screening,disp,('date','proceeds','ordinary_sale'),ref):return
            last=iso(disp['date'])
            if last<ready:
                screening.add('pre_readiness_disposal','BLOCKED',[ref],'Disposal precedes availability for use.',blocks=True,resolution='Resolve chronology or use supported uncommissioned-asset route.');return
            if not start<=last<=end:raise ReviewRequired('Disposal date outside reporting period')
            if disp['ordinary_sale'] is not True:raise ReviewRequired('Disposal requires a specialist sale route')
        if ready>end:
            screening.add('readiness','BLOCKED',[ref],'Asset is not available for use at reporting date.',blocks=True,resolution='Supply supported CIP/uncommissioned classification; no depreciation charged.');return
        if cost==ZERO and acc==ZERO and row['id'] in expensed_destinations:
            if 'expected_depreciation' in row:screening.compare('depreciation_comparison',row['expected_depreciation'],ZERO,[ref],label='Supplied depreciation')
            screening.add('classification','PASS',[ref],'All supported costs for this zero-opening asset were expensed; no PPE or depreciation is recognized.')
            return dict(id=row['id'],row_reference=ref,cost=ZERO,depreciation=ZERO,closing_cost=ZERO,
                        closing_accumulated=ZERO,carrying=ZERO,disposal_gain=ZERO,assumption_class=row.get('class'),applied_assumptions={k:row[k] for k in ('capitalization_threshold',) if k in row})
        life=ZERO;units=ZERO
        if row['method']=='units_of_production':
            if missing_row(screening,row,('remaining_units','period_units'),ref):return
            life=number(row['remaining_units'],positive=True);units=number(row['period_units'])
            if units>life:raise ReviewRequired('Production exceeds remaining units')
        elif row['method']=='straight_line':
            life=life_months
        else:raise ReviewRequired('Unsupported depreciation method')
        screening.norms(row,ref,{**row,'amount':cost})
        threshold=row.get('capitalization_threshold')
        if threshold is not None and cost<number(threshold):
            screening.add('classification','BLOCKED',[ref],'Opening asset cost is below the supplied capitalization threshold.',blocks=True,resolution='Resolve opening carrying balance and policy treatment; do not expense a historic carrying amount automatically.');return
        basis=max(cost-acc-res,ZERO)
        if row['method']=='straight_line':
            if selected_policy['convention']=='monthly':
                try:amount=monthly_charge(max(start,ready),last,basis,life,selected_policy['partial_month_treatment'])
                except ReviewRequired as exc:
                    screening.add('assumptions','BLOCKED',[ref],str(exc),blocks=True,resolution='Confirm the partial-month accounting policy.')
                    screening.findings[-1]['field_path']='policy_elections.partial_month_treatment'
                    return
            else:amount=actual_charge(max(start,ready),last,basis,life)
        else:amount=charge(max(start,ready),last,basis,life,row['method'],units)
        if 'expected_depreciation' in row:screening.compare('depreciation_comparison',row['expected_depreciation'],amount,[ref],label='Supplied depreciation')
        closingcost=cost;closingacc=acc+amount;gain=ZERO
        row_entries.append(journal(('Dr','depreciation expense',amount),('Cr','accumulated depreciation',amount)))
        if disp.get('enabled'):
            proceeds=number(disp['proceeds']);gain=cash(proceeds-(cost-closingacc))
            # Receipt is a separate fact from a sale and its consideration.
            description=str(row.get('description','')).casefold()
            credit=disp.get('payment_terms')=='credit' or bool(re.search(r'\b(on credit|no cash received|unpaid|receivable)\b',description))
            if disp.get('cash_received') is True and not credit:
                consideration='cash'
            elif disp.get('cash_received') is False and disp.get('payment_terms')=='credit':
                consideration='disposal receivable'
            elif proceeds==ZERO:
                consideration='disposal consideration'
            else:
                raise ReviewRequired('Disposal settlement unresolved: supply supported cash receipt or unpaid credit consideration evidence')
            row_entries.append(journal(('Dr',consideration,proceeds),('Dr','accumulated depreciation',closingacc),('Dr','disposal loss',max(-gain,ZERO)),('Cr','PPE cost',cost),('Cr','disposal gain',max(gain,ZERO))))
            closingcost=ZERO;closingacc=ZERO
        for k,val in [('gl_cost',closingcost),('gl_accumulated',closingacc)]:
            if k in row:screening.compare('gl_reconciliation',row[k],val,[ref],label='Supplied asset '+k)
        if 'closing_cost' in row:screening.compare('roll_forward',row['closing_cost'],closingcost,[ref],label='Asset cost roll-forward')
        screening.add('dates','PASS',[ref],'Availability and disposal chronology checked.')
        entries.extend(row_entries)
        return dict(id=row['id'],row_reference=ref,cost=cost,depreciation=amount,closing_cost=closingcost,
                    closing_accumulated=closingacc,carrying=closingcost-closingacc,disposal_gain=gain,
                    applied_depreciation_policy=selected_policy if row['method']=='straight_line' else None,
                    assumption_class=row.get('class'),applied_assumptions={k:row[k] for k in (('method','residual','scope','capitalization_threshold','remaining_units','period_units') if row['method']=='units_of_production' else ('method','residual','scope','capitalization_threshold','remaining_life','remaining_life_months')) if k in row})
    for i,row in enumerate(assets):
        value=screening.row('assets',i,row,calculate)
        if value is not None:work.append(value)
        try:
            n=number(row['opening_cost'])
            if input_amounts is not None:input_amounts.append(n)
        except (KeyError,ReviewRequired):input_amounts=None
    for cost_ref,asset_ref,entry in capital_entries:
        if asset_ref in screening.blocked:
            entries.remove(entry)
            costwork[:]=[r for r in costwork if r['row_reference']!=cost_ref]
            screening.add('movements','BLOCKED',[cost_ref],'Linked asset validation failed; capital journal withheld.',blocks=True,resolution='Resolve the asset opening position and movement evidence together.')
    calcs=dict(assets=work,cost_rows=costwork)
    if work:
        calcs.update(depreciation=sum((r['depreciation'] for r in work),ZERO),
                     closing_cost=sum((r['closing_cost'] for r in work),ZERO),
                     closing_accumulated=sum((r['closing_accumulated'] for r in work),ZERO))
    if work or costwork:calcs['excluded_expense']=expenses
    population=totals(screening,assets,input_amounts,calcs)
    return calcs,entries,population


def accounts_payable(case,screening):
    invoices=screening.rows('invoices');accruals=screening.rows('accruals')
    if not invoices and not accruals:raise ReviewRequired('Nonempty invoice or accrual population required')
    keys=[]
    for row in invoices:
        try:keys.append((normalized(row.get('supplier')),normalized(row.get('invoice_number'))))
        except ReviewRequired:keys.append(None)
    duplicates={k for k,n in Counter(keys).items() if k is not None and n>1}
    for i,key in enumerate(keys):
        if key in duplicates:screening.add('duplicate_invoices','BLOCKED',['invoices:'+str(i+1)],'Duplicate supplier/invoice reference.',blocks=True,resolution='Resolve duplicate liabilities before including these invoices.')
    if not duplicates:screening.add('duplicate_invoices','PASS',explanation='Supplier/invoice references checked for exact normalized duplicates.')
    entries=[];work=[];acs=[]
    def invoice(raw,ref):
        row=resolved_row(case,raw,screening,ref)
        screening.numeric_inputs(row,ref)
        specialist(screening,row,ref,'accounts-payable')
        if missing_row(screening,row,('supplier','invoice_number','amount','invoice_date','account','recognition_basis'),ref):return
        normalized(row['supplier']);normalized(row['invoice_number']);text(row['account'],'Recognition account')
        if re.search(r'\b(refundable|repayable)\b',str(row.get('description','')).casefold()) and re.search(r'\b(deposit|security)\b',str(row.get('description','')).casefold()):
            raise ReviewRequired('Refundable deposit evidence requires supported terms and asset classification; generic expense recognition is unresolved')
        if ref in screening.blocked:return
        if not screening.currency(row,ref):return
        if row.get('accrual_id'):
            raise ReviewRequired('Linked prior-accrual clearing needs the existing governed AP movement workflow')
        if row['recognition_basis'] not in ('goods_received','services_received','supplier_invoice_obligation'):
            raise ReviewRequired('Supplier obligation recognition basis is unsupported or ambiguous')
        d=iso(row['invoice_date']);start=iso(case['period_start']);end=iso(case['reporting_period'])
        if not start<=d<=end:
            screening.add('cutoff','BLOCKED',[ref],'Invoice date falls outside reporting period.',blocks=True,resolution='Supply the correct opening-balance or subsequent-period route.');return
        if row['recognition_basis'] in ('goods_received','services_received') and missing_row(screening,row,('received_date',),ref):return
        if 'received_date' in row and iso(row['received_date'])<start:
            screening.add('cutoff','BLOCKED',[ref],'Receipt precedes reporting period; current expense cannot be inferred.',blocks=True,resolution='Supply supported opening-accrual clearing or error treatment.');return
        if 'received_date' in row and iso(row['received_date'])>end:
            screening.add('cutoff','BLOCKED',[ref],'Receipt follows period end.',blocks=True,resolution='Resolve recognition/cutoff; a future receipt does not support current expense.');return
        if 'payment_date' in row and iso(row['payment_date'])<d:
            screening.add('dates','WARNING',[ref],'Payment precedes invoice date.',resolution='Confirm advance-payment treatment; no cash movement is inferred.')
        n=number(row['amount'],positive=True)
        for label in ('po_amount','received_amount'):
            if label in row:
                if not screening.compare('arithmetic',row[label],n,[ref],label='Supplied '+label,blocks=True):return
            else:screening.add('arithmetic','NOT_PERFORMED',[ref],label.replace('_',' ')+' matching was not performed; no matching evidence supplied.')
        if 'units' in row or 'unit_price' in row:
            if missing_row(screening,row,('units','unit_price'),ref):return
            if not screening.compare('arithmetic',n,number(row['units'])*number(row['unit_price']),[ref],label='Quantity times unit price',blocks=True):return
        screening.norms(row,ref,{**row,'amount':n})
        screening.add('recognition','PASS',[ref],'Supplier obligation calculated using the supplied recognition basis; no PO/receipt match is inferred.')
        entries.append(journal(('Dr',row['account'],n),('Cr','accounts payable',n)))
        return dict(id=row['id'],row_reference=ref,amount=n,assumption_class=row.get('class'),applied_assumptions={'recognition_basis':row['recognition_basis']})
    def accrual(raw,ref):
        row=resolved_row(case,raw,screening,ref)
        screening.numeric_inputs(row,ref)
        specialist(screening,row,ref,'accounts-payable')
        if missing_row(screening,row,('supplier','units','rate','received_date','received_supported','invoiced_received','account','recognition_basis'),ref):return
        if ref in screening.blocked:return
        if not screening.currency(row,ref):return
        text(row['account'],'Accrual account');normalized(row['supplier'])
        if row['received_supported'] is not True:raise ReviewRequired('Receipt evidence required for unbilled-receipt accrual')
        if row['recognition_basis'] not in ('goods_received','services_received'):raise ReviewRequired('Unbilled receipt recognition unresolved')
        if not iso(case['period_start'])<=iso(row['received_date'])<=iso(case['reporting_period']):raise ReviewRequired('Accrual receipt date outside reporting period')
        if 'invoice_overlap_resolved' not in row and any(not isinstance(i.get('supplier'),str) or not i['supplier'].strip() or normalized(i['supplier'])==normalized(row['supplier']) for i in invoices):
            raise ReviewRequired('Potential duplicate invoice/accrual liability; supply an explicit overlap assessment')
        if row.get('invoice_overlap_resolved',True) is not True:raise ReviewRequired('Invoice/accrual overlap unresolved')
        n=cash(number(row['units'])*number(row['rate'])-number(row['invoiced_received']))
        if n<0:raise ReviewRequired('Invoiced receipts exceed supplied service population')
        value=dict(id=row['id'],row_reference=ref,amount=n,assumption_class=row.get('class'),applied_assumptions={'recognition_basis':row['recognition_basis']})
        if 'opening_accrual' in row:
            prior=number(row['opening_accrual']);delta=n-prior
            entries.append(journal(('Dr',row['account'],max(delta,ZERO)),('Dr','accrued expenses',max(-delta,ZERO)),('Cr','accrued expenses',max(delta,ZERO)),('Cr',row['account'],max(-delta,ZERO))))
            value.update(opening_accrual=prior,expense_movement=delta)
        else:
            screening.add('roll_forward','NOT_PERFORMED',[ref],'Opening accrual/postings were not supplied; closing obligation calculated, adjusting journal omitted.',resolution='Supply the existing opening accrual to calculate the net journal movement.')
        if 'gl_closing' in row:screening.compare('gl_reconciliation',row['gl_closing'],n,[ref],label='Supplied accrual closing GL')
        return value
    for key,rows,fn,target in [('invoices',invoices,invoice,work),('accruals',accruals,accrual,acs)]:
        for i,row in enumerate(rows):
            value=screening.row(key,i,row,fn)
            if value is not None:target.append(value)
    calcs=dict(invoice_rows=work,accrual_rows=acs)
    if work or case.get('invoices')==[]:calcs['invoices']=sum((r['amount'] for r in work),ZERO)
    if acs or case.get('accruals')==[]:calcs['closing_accruals']=sum((r['amount'] for r in acs),ZERO)
    payments_supported=True
    if 'payments' in case:
        try:
            payment_rows=screening.rows('payments')
            detail=ZERO
            for payment in payment_rows:
                for field in ('date','payment_date'):
                    if field in payment and not iso(case['period_start'])<=iso(payment[field])<=iso(case['reporting_period']):
                        raise ReviewRequired('Payment date outside the reporting period')
                detail+=number(payment['amount'])
            if 'payments_total' not in case or cash(detail)!=cash(number(case['payments_total'])):
                raise ReviewRequired('Payment detail and aggregate do not reconcile; resolve payment evidence before asserting closing AP')
            if any(ref.startswith('payments:') for ref in screening.blocked):
                raise ReviewRequired('Payment detail contains excluded rows; closing AP is unresolved')
            screening.add('roll_forward','PASS',explanation='Supplied payment detail reconciles to supplied aggregate; no bank confirmation inferred.')
        except (ReviewRequired,KeyError,TypeError,ArithmeticError):
            payments_supported=False
            screening.add('roll_forward','BLOCKED',explanation='Supplied payment detail is invalid or conflicts with the aggregate; invoice recognition is retained but closing AP is unresolved.',population=True,resolution='Reconcile the supplied payment detail and aggregate with supported settlement evidence.')
    # A supplied listing does not establish opening AP, payments or closing AP.
    if 'opening_ap_total' in case and 'payments_total' in case and 'invoices' in calcs and not screening.blocked and payments_supported:
        try:
            opening=number(case['opening_ap_total']);payments=number(case['payments_total']);closing=opening+calcs['invoices']-payments
            if closing<0:raise ReviewRequired('Payments exceed supported AP balances; supply supported advance-payment treatment')
        except (ReviewRequired,TypeError,ArithmeticError):
            screening.add('roll_forward','BLOCKED',explanation='Opening AP or payment aggregate is invalid; supported invoice recognition is retained.',population=True,resolution='Supply valid opening AP and period payment evidence, including advance-payment treatment where relevant.')
        else:calcs.update(opening_ap=opening,payments=payments,closing_ap=closing);screening.add('roll_forward','PASS',explanation='Supplied opening plus invoices less supplied payments calculated; no bank matching inferred.')

    amounts=[]
    try:
        for row in invoices:amounts.append(number(row['amount'],positive=True))
        for row in accruals:amounts.append(cash(number(row['units'])*number(row['rate'])))
    except (KeyError,ReviewRequired):amounts=None
    for key,metric in [('gl_ap','closing_ap'),('gl_accrual','closing_accruals')]:
        if key in case:
            if metric in calcs and not screening.blocked:screening.compare('gl_reconciliation',case[key],calcs[metric],label='Supplied '+key)
            else:screening.add('gl_reconciliation','NOT_PERFORMED',explanation='Supported complete population balance unavailable for supplied GL comparison.',population=True)
    if 'supplier_balances' in case:
        confirmations=screening.rows('supplier_balances')
        try:
            supplied=sum((number(r['balance']) for r in confirmations),ZERO)
            if 'closing_ap' in calcs and not screening.blocked:screening.compare('supplier_reconciliation',supplied,calcs['closing_ap'],label='Supplied supplier balance aggregate')
            else:screening.add('supplier_reconciliation','NOT_PERFORMED',explanation='Supplier movement evidence or supported complete AP balance unavailable; individual supplier reconciliation not established.',population=True)
        except (ReviewRequired,KeyError):screening.add('supplier_reconciliation','WARNING',explanation='Supplied supplier balances contain missing or invalid amounts.',population=True,resolution='Supply valid supplier balances and movement evidence.')
    population=totals(screening,invoices+accruals,amounts,calcs)
    return calcs,entries,population


def execute(package, case):
    import production
    reject_records(case)
    pending=requirements(package,case)
    working=copy.deepcopy(case)
    working.setdefault('policy_elections',{})
    if not pending:
        try:
            qualification=copy.deepcopy(working)
            if package=='fixed-assets':qualification['policy_elections']={}  # bounded elections validated above; shared Profile 1.1 stays unchanged
            edition=qualify(package,qualification)
            attestation(case['source_attestation'])
            if not isinstance(case['assumptions'],list):raise ReviewRequired('Assumptions must be an array')
            if case.get('specialist_items'):raise ReviewRequired('Unresolved specialist accounting matters require sufficient evidence')
            if case.get('asset_policy',{}).get('model','cost')!='cost':raise ReviewRequired('Only ordinary cost-method machinery is supported')
        except (ReviewRequired,TypeError,KeyError) as exc:
            pending.append(issue('scope.qualification','scope',str(exc) if isinstance(exc,ReviewRequired) else 'Malformed accounting scope.','unsupported_scope'))
    if pending:return blocked(package,case,pending)
    claims,documents=production.canonical_knowledge(production.PACKAGES[package][1],case['framework'],package=package)
    if not claims or any(c.get('evidence_status') in ('CONFLICTED','NOT_RESEARCHED') for c in claims):
        return blocked(package,case,[issue('scope.knowledge','scope','Governed accounting knowledge assurance unresolved.','unsupported_scope')])
    try:
        screening=Screening(case)
        calcs,entries,population=(fixed_assets if package=='fixed-assets' else accounts_payable)(working,screening)
        report=screening.report()
    except (ReviewRequired,KeyError,TypeError,ArithmeticError) as exc:
        return blocked(package,case,[issue('source.validation','source',str(exc) if isinstance(exc,ReviewRequired) else 'Malformed source input.','invalid_fact')])
    for lines in entries:balance(lines)
    needs=[]
    for i,f in enumerate(report['findings']):
        if f['severity']=='BLOCKED':
            needs.append(issue('screening.'+f['check_id']+'.'+re.sub('[^A-Za-z0-9_.-]','_',f.get('field_path',','.join(f['row_references']) or 'population')),f.get('field_path',','.join(f['row_references']) or 'population'),f['explanation'],'anomaly'))
    unresolved=bool(needs)
    result=dict(skill_id=production.PACKAGES[package][0],framework=case['framework'],jurisdiction=case['jurisdiction'],
        entities=[case['entity']],periods=[case['period_start'],case['reporting_period']],review_mode=MODE,source_assurance=PROFILE,
        status='partial',accounting_determination='UNRESOLVED' if unresolved else 'SUPPORTED',
        evidence_sufficiency='INSUFFICIENT' if unresolved else 'SUFFICIENT',review_provenance='SYSTEM_PREPARED',source_provenance='USER_PROVIDED_SOURCES',
        source_assertion=dict(origin='CLIENT_ASSERTION_NOT_INDEPENDENT_CERTIFICATION',attestation=copy.deepcopy(case['source_attestation'])),
        source_lineage=dict(source=copy.deepcopy(case['source']),case=case['case_id']),case_fingerprint=production.case_fingerprint(case),
        facts_used=copy.deepcopy(case),assumptions=case['assumptions'],applied_class_assumptions=copy.deepcopy(case.get('class_assumptions',{})),
        policy_elections_disclosure='No policy elections were assumed.' if not case.get('policy_elections') else 'Supplied elections applied.',
        knowledge_population=claims,knowledge_documents=documents,evidence=[],calculations=calcs,population=population,anomaly_report=report,
        validation_requirements=needs,open_items=[n['explanation'] for n in needs],uncertainties=report['limitations'],
        conclusion='Nally calculated these results using the information you provided.' if any(isinstance(v,Decimal) for v in calcs.values()) else 'No supported financial amounts could be calculated; resolve the listed requirements.',
        proposed_journal_workpaper=entries,journal_entry_implications=[],confidence='medium',memory_candidates=[],related_artifacts=[])
    production.to_public(result)
    return result


def blocked(package,case,needs):
    import production
    return dict(skill_id=production.PACKAGES.get(package,('UNSUPPORTED',))[0],framework=case.get('framework',''),jurisdiction=case.get('jurisdiction',''),
        entities=[case.get('entity','')],periods=[case.get('period_start',''),case.get('reporting_period','')],review_mode=MODE,source_assurance=PROFILE,
        status='blocked',accounting_determination='UNRESOLVED',evidence_sufficiency='INSUFFICIENT',review_provenance='SYSTEM_PREPARED',source_provenance='USER_PROVIDED_SOURCES',
        conclusion='Supply the listed information to execute the affected accounting calculations.',validation_requirements=needs,
        open_items=[n['explanation'] for n in needs],calculations={},journal_entry_implications=[],proposed_journal_workpaper=[],
        facts_used=copy.deepcopy(case),assumptions=case.get('assumptions',[]),evidence=[],uncertainties=[])


def to_public(result,route):
    from interfaces.public_output import public_record
    from production import serializable
    fa=result['skill_id']=='SKILL-FA-001'
    guidance=result['conclusion']
    if any(isinstance(v,Decimal) for v in result['calculations'].values()):
        guidance+='\n'+('Ordinary machinery uses the governed cost method; depreciation starts when available for use (IAS 16, ASC 360, FRS 102 Section 17 or AASB 116, as applicable).' if fa else 'Recognize supplied ordinary supplier obligations under the applicable governed recognition method; unbilled accruals require supported goods or services receipt.')
        guidance+='\nCalculated valid rows are bounded by the supplied file; excluded rows are not included in a complete population total.'
        guidance+='\n'+result['policy_elections_disclosure']
        if fa:
            policy,_=depreciation_policy(result['facts_used'])
            guidance+='\nApplied depreciation convention: '+policy['convention']+' ('+policy['provenance']+').'
            guidance+='\nMonthly depreciation is recommended for businesses calculating depreciation as part of a monthly close. It provides consistent full-month charges and commonly aligns with fixed-asset registers. Choose actual days if your documented accounting policy uses calendar-day proration.'
            if policy['provenance']=='engine_default_unconfirmed':guidance+=' Confirm the company convention; the backward-compatible actual-day basis was used, not inferred from supplied depreciation.'
        applied=[];used_classes=set()
        for table in ('assets','cost_rows','invoice_rows','accrual_rows'):
            for row in result['calculations'].get(table,[]):
                if row.get('assumption_class') is not None:used_classes.add(row['assumption_class'])
                values=row.get('applied_assumptions',{})
                if values:applied.append(dict(row_reference=row['row_reference'],assumptions=values))
        defaults={name:{k:v for k,v in policy.items() if k in ('remaining_life','residual','method','scope','capitalization_threshold','account','recognition_basis') and isinstance(v,(str,int,Decimal))} for name,policy in result.get('applied_class_assumptions',{}).items() if name in used_classes}
        guidance+='\nSupplied class defaults: '+json.dumps(defaults,sort_keys=True,default=serializable)
        guidance+='\nApplied row assumptions: '+json.dumps(applied,sort_keys=True,default=serializable)
        guidance+='\nExplicit user assumptions: '+json.dumps(result.get('assumptions',[]),default=serializable)
        guidance+='\nProposed journal implications: '+json.dumps(result['proposed_journal_workpaper'],default=serializable)
    public=dict(guidance=guidance,status=result['status'],accounting_determination=result['accounting_determination'],
        evidence_sufficiency=result['evidence_sufficiency'],review_provenance='SYSTEM_PREPARED',source_provenance='USER_PROVIDED_SOURCES',
        framework=result['framework'],jurisdiction=result['jurisdiction'],entity_scope=result['entities'][0],effective_period=' to '.join(result['periods']),
        limitations=result.get('uncertainties',[])+['Prepared without independent review. Journal workpapers are proposals; no posting is authorized.'],
        open_items=result.get('open_items',[]),validation_requirements=result.get('validation_requirements',[]),
        calculations=[dict(label=k.replace('_',' '),amount=str(v)) for k,v in result['calculations'].items() if isinstance(v,Decimal)],
        anomaly_report=result.get('anomaly_report',{}))
    rendered=public_record(public,route=route)
    private=[]
    def collect(value):
        if isinstance(value,dict):
            for key,item in value.items():
                if key in ('authenticated_user_reference','reviewer','approved_by','reviewer_identity','preparer','owner','hash','evidence'):
                    if isinstance(item,str) and len(item)>=4:private.append(item)
                else:collect(item)
        elif isinstance(value,list):
            for item in value:collect(item)
    collect(result.get('facts_used',{}))
    encoded=json.dumps(rendered,ensure_ascii=False)
    if any(value in encoded for value in private):raise ReviewRequired('Private source identity or evidence cannot be published')
    return rendered
