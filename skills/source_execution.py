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
from core_accounting import ReviewRequired, required, cash, journal, balance
from source_screening import PROFILE, Screening, attestation, iso, number, normalized, text
from prepared_execution import MODE, qualify, reject_records

ZERO = Decimal(0)


def issue(identifier, path, explanation, category='missing_fact'):
    return dict(identifier=identifier, field_path=path, explanation=explanation, category=category)


def requirements(package, case):
    """Only enumerate prerequisites evaluable at this stage; never guess consequences."""
    found = []
    fields = ['case_id', 'framework', 'jurisdiction', 'entity', 'entity_type', 'period_start',
              'reporting_period', 'functional_currency', 'assumptions', 'source', 'source_attestation']
    if case.get('framework') == 'UK_GAAP': fields += ['uk_standard', 'uk_standard_edition']
    if case.get('framework') == 'AASB': fields += ['aasb_compilation', 'reporting_tier']
    if case.get('framework') == 'US_GAAP': fields += ['us_entity_type']
    for key in fields:
        if case.get(key) in (None, ''): found.append(issue('missing.'+key, key, 'Supply '+key.replace('_',' ')+'.'))
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
    if case.get('source_assurance') != PROFILE:
        found.append(issue('scope.source_assurance','source_assurance','Explicit source-assurance profile required.','unsupported_scope'))
    if case.get('review_mode') != MODE:
        found.append(issue('scope.review_mode','review_mode','Profile 1.2 requires prepared-unreviewed execution.','unsupported_scope'))
    if case.get('policy_elections') not in (None, {}):
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
        for key in ('remaining_life','residual','method','scope','capitalization_threshold','account','recognition_basis'):
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
               'disputed_obligation': ('disputed','dispute')}
    for key in indicators:
        if key in row and type(row[key]) is not bool: raise ReviewRequired('Specialist indicator must be an explicit boolean')
        present = row.get(key) is True or any(re.search(r'\b'+re.escape(token)+r'\b',description) for token in textual.get(key,()))
        check = 'leases' if key in ('lease_like','sale_leaseback') else 'impairment' if key=='impairment_indicator' else 'classification'
        screening.add(check,'BLOCKED' if present else 'PASS',[ref],
                      'Supplied facts indicate a specialist accounting route: '+key.replace('_',' ')+'.' if present else
                      'No '+key.replace('_',' ')+' indicator detected in the supplied structured facts.',
                      blocks=present,resolution='Supply sufficient specialist-route evidence; this profile cannot infer its conclusion.' if present else '')
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


def fixed_assets(case, screening):
    import production
    charge = production.load_workflow('fixed-assets').charge
    assets = screening.rows('assets', required_population=True)
    costs = screening.rows('costs'); cip = screening.rows('cip')
    work=[]; entries=[]; expenses=ZERO; input_amounts=[]
    additions={row.get('id'):ZERO for row in assets}
    def cost_row(raw,ref):
        row=resolved_row(case,raw,screening,ref)
        if missing_row(screening,row,('amount','kind','date','offset'),ref):return
        if ref in screening.blocked or not screening.currency(row,ref):return
        if not iso(case['period_start'])<=iso(row['date'])<=iso(case['reporting_period']):raise ReviewRequired('Cost date outside reporting period')
        text(row['offset'],'Offset account')
        n=number(row['amount'],positive=True)
        excluded=row['kind'] in ('training','general_overhead','abnormal_waste')
        if row['kind'] not in ('purchase','freight','installation','training','general_overhead','abnormal_waste'):raise ReviewRequired('Cost classification is ambiguous or requires a specialist route')
        if 'eligible' in row and type(row['eligible']) is not bool:raise ReviewRequired('Eligibility input must be an explicit boolean')
        below='capitalization_threshold' in row and n<number(row['capitalization_threshold'])
        if excluded or row.get('eligible') is False or below:
            if missing_row(screening,row,('account',),ref):return
            text(row['account'],'Expense account')
            entries.append(journal(('Dr',row['account'],n),('Cr',row['offset'],n)))
            screening.add('classification','PASS',[ref],
                'Training, general overhead and abnormal waste are expensed under the governed cost method.' if excluded else 'Cost is expensed using the explicit eligibility or applicable company capitalization threshold.')
            return ('expense',n)
        if missing_row(screening,row,('destination',),ref):return
        targets=[r for r in assets if r.get('id')==row['destination']]
        if len(targets)!=1:raise ReviewRequired('Cost destination must identify one supplied asset')
        if iso(row['date'])>iso(targets[0].get('ready_date')):raise ReviewRequired('Post-readiness improvement/component cost requires supported specialist route')
        additions[row['destination']]+=n
        entries.append(journal(('Dr','PPE cost',n),('Cr',row['offset'],n)))
        screening.add('classification','PASS',[ref],'Ordinary purchase, freight or installation cost directly attributable before readiness is capitalized under the governed cost method.')
        return ('capital',n)
    for i,row in enumerate(costs):
        value=screening.row('costs',i,row,cost_row)
        if value is not None and value[0]=='expense':expenses+=value[1]
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
        row=resolved_row(case,raw,screening,ref)
        if missing_row(screening,row,('opening_cost','opening_accumulated','residual','ready_date','method','scope'),ref):return
        if ref in screening.blocked:return
        if not screening.currency(row,ref):return
        if row['scope']!='ordinary_ppe' or row.get('asset_type','machinery')!='machinery':raise ReviewRequired('Only ordinary machinery cost-method scope is supported')
        if row.get('model','cost')!='cost':raise ReviewRequired('Only the ordinary cost method is supported')
        if specialist(screening,row,ref,'fixed-assets'):return
        if row.get('change',{}).get('enabled') or any(row.get(k) not in (None,0,'0') for k in ('additions','transfers','revaluation')):
            raise ReviewRequired('Register movement or estimate change requires separately supported evidence')
        cost=number(row['opening_cost'])+additions.get(row['id'],ZERO);acc=number(row['opening_accumulated']);res=number(row['residual'])
        if acc>cost:raise ReviewRequired('Accumulated depreciation exceeds supported cost')
        if res>cost-acc:screening.add('assumptions','WARNING',[ref],'Supplied residual exceeds current carrying amount; depreciation is zero while this persists.',resolution='Confirm the current residual assumption; no replacement was assumed.')
        ready=iso(row['ready_date']);start=iso(case['period_start']);end=iso(case['reporting_period']);last=end
        disp=row.get('disposal',{})
        if disp.get('enabled'):
            if missing_row(screening,disp,('date','proceeds','ordinary_sale'),ref):return
            last=iso(disp['date'])
            if last<ready:
                screening.add('pre_readiness_disposal','BLOCKED',[ref],'Disposal precedes availability for use.',blocks=True,resolution='Resolve chronology or use supported uncommissioned-asset route.');return
            if not start<=last<=end:raise ReviewRequired('Disposal date outside reporting period')
            if disp['ordinary_sale'] is not True:raise ReviewRequired('Disposal requires a specialist sale route')
        if ready>end:
            screening.add('readiness','BLOCKED',[ref],'Asset is not available for use at reporting date.',blocks=True,resolution='Supply supported CIP/uncommissioned classification; no depreciation charged.');return
        life=ZERO;units=ZERO
        if row['method']=='units_of_production':
            if missing_row(screening,row,('remaining_units','period_units'),ref):return
            life=number(row['remaining_units'],positive=True);units=number(row['period_units'])
            if units>life:raise ReviewRequired('Production exceeds remaining units')
        elif row['method']=='straight_line':
            if missing_row(screening,row,('remaining_life',),ref):return
            life=number(row['remaining_life'],positive=True)
        else:raise ReviewRequired('Unsupported depreciation method')
        screening.norms(row,ref,{**row,'amount':cost})
        threshold=row.get('capitalization_threshold')
        if threshold is not None and cost<number(threshold):
            screening.add('classification','BLOCKED',[ref],'Opening asset cost is below the supplied capitalization threshold.',blocks=True,resolution='Resolve opening carrying balance and policy treatment; do not expense a historic carrying amount automatically.');return
        amount=charge(max(start,ready),last,max(cost-acc-res,ZERO),life,row['method'],units)
        if 'expected_depreciation' in row:screening.compare('depreciation_comparison',row['expected_depreciation'],amount,[ref],label='Supplied depreciation')
        closingcost=cost;closingacc=acc+amount;gain=ZERO
        entries.append(journal(('Dr','depreciation expense',amount),('Cr','accumulated depreciation',amount)))
        if disp.get('enabled'):
            proceeds=number(disp['proceeds']);gain=cash(proceeds-(cost-closingacc))
            entries.append(journal(('Dr','cash',proceeds),('Dr','accumulated depreciation',closingacc),('Dr','disposal loss',max(-gain,ZERO)),('Cr','PPE cost',cost),('Cr','disposal gain',max(gain,ZERO))))
            closingcost=ZERO;closingacc=ZERO
        for k,val in [('gl_cost',closingcost),('gl_accumulated',closingacc)]:
            if k in row:screening.compare('gl_reconciliation',row[k],val,[ref],label='Supplied asset '+k)
        if 'closing_cost' in row:screening.compare('roll_forward',row['closing_cost'],closingcost,[ref],label='Asset cost roll-forward')
        screening.add('dates','PASS',[ref],'Availability and disposal chronology checked.')
        return dict(id=row['id'],row_reference=ref,cost=cost,depreciation=amount,closing_cost=closingcost,
                    closing_accumulated=closingacc,carrying=closingcost-closingacc,disposal_gain=gain,
                    applied_assumptions={k:row[k] for k in ('method','remaining_life','residual','scope','remaining_units','period_units') if k in row})
    for i,row in enumerate(assets):
        value=screening.row('assets',i,row,calculate)
        if value is not None:work.append(value)
        try:
            n=number(row['opening_cost'])
            if input_amounts is not None:input_amounts.append(n)
        except (KeyError,ReviewRequired):input_amounts=None
    calcs=dict(assets=work,depreciation=sum((r['depreciation'] for r in work),ZERO),
               closing_cost=sum((r['closing_cost'] for r in work),ZERO),closing_accumulated=sum((r['closing_accumulated'] for r in work),ZERO),excluded_expense=expenses)
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
        if missing_row(screening,row,('supplier','invoice_number','amount','invoice_date','account','recognition_basis'),ref):return
        normalized(row['supplier']);normalized(row['invoice_number']);text(row['account'],'Recognition account')
        if ref in screening.blocked:return
        if not screening.currency(row,ref):return
        if specialist(screening,row,ref,'accounts-payable'):return
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
        return dict(id=row['id'],row_reference=ref,amount=n)
    def accrual(raw,ref):
        row=resolved_row(case,raw,screening,ref)
        if missing_row(screening,row,('supplier','units','rate','received_date','received_supported','invoiced_received','account','recognition_basis'),ref):return
        if ref in screening.blocked:return
        if not screening.currency(row,ref):return
        if specialist(screening,row,ref,'accounts-payable'):return
        text(row['account'],'Accrual account')
        if row['received_supported'] is not True:raise ReviewRequired('Receipt evidence required for unbilled-receipt accrual')
        if row['recognition_basis'] not in ('goods_received','services_received'):raise ReviewRequired('Unbilled receipt recognition unresolved')
        if not iso(case['period_start'])<=iso(row['received_date'])<=iso(case['reporting_period']):raise ReviewRequired('Accrual receipt date outside reporting period')
        if any(normalized(i.get('supplier',''))==normalized(row['supplier']) for i in invoices) and 'invoice_overlap_resolved' not in row:
            raise ReviewRequired('Potential duplicate invoice/accrual liability; supply an explicit overlap assessment')
        if row.get('invoice_overlap_resolved',True) is not True:raise ReviewRequired('Invoice/accrual overlap unresolved')
        n=cash(number(row['units'])*number(row['rate'])-number(row['invoiced_received']))
        if n<0:raise ReviewRequired('Invoiced receipts exceed supplied service population')
        value=dict(id=row['id'],row_reference=ref,amount=n)
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
    calcs=dict(invoice_rows=work,accrual_rows=acs,invoices=sum((r['amount'] for r in work),ZERO),closing_accruals=sum((r['amount'] for r in acs),ZERO))
    # A supplied listing does not establish opening AP, payments or closing AP.
    if 'opening_ap_total' in case and 'payments_total' in case and not screening.blocked:
        opening=number(case['opening_ap_total']);payments=number(case['payments_total']);closing=opening+calcs['invoices']-payments
        if closing<0:screening.add('roll_forward','BLOCKED',explanation='Payments exceed supported AP balances.',population=True,resolution='Supply supported advance-payment treatment.')
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
            edition=qualify(package,working)
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
        conclusion='Nally calculated these results using the information you provided.',
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
    if result['calculations']:
        guidance+='\n'+('Ordinary machinery uses the governed cost method; depreciation starts when available for use (IAS 16, ASC 360, FRS 102 Section 17 or AASB 116, as applicable).' if fa else 'Recognize supplied ordinary supplier obligations under the applicable governed recognition method; unbilled accruals require supported goods or services receipt.')
        guidance+='\nCalculated valid rows are bounded by the supplied file; excluded rows are not included in a complete population total.'
        guidance+='\n'+result['policy_elections_disclosure']
        guidance+='\nApplied assumptions: '+json.dumps({name:{k:v for k,v in policy.items() if k in ('remaining_life','residual','method','scope','capitalization_threshold','account','recognition_basis')} for name,policy in result.get('applied_class_assumptions',{}).items()},sort_keys=True,default=serializable)
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
