"""Insurance accounting of qualified measurements; never actuarial projection."""
from core_accounting import ReviewRequired,required,dec,cash,journal,balance
from datetime import date
from decimal import Decimal
import hashlib,json,re
ZERO=Decimal(0)
PACKAGE='insurance-contracts-accounting'

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),default=str).encode()).hexdigest()
def check(ok,msg):
    if not ok:raise ReviewRequired(msg)
def iso(v):
    try:return date.fromisoformat(v)
    except (ValueError,TypeError):raise ReviewRequired('Actual ISO date required')
def exact(a,b,label):check(cash(a)==cash(b),label+' does not reconcile')
def scalar(a,b,label):check(abs(dec(a)-dec(b))<=Decimal('0.000000000000000001'),label+' does not reconcile at required precision')
def text(r,*keys):
    for k in keys:check(isinstance(r.get(k),str) and bool(r[k].strip()),'Actual '+k+' required')
def flag(r,k):check(type(r.get(k)) is bool,'Actual boolean '+k+' required');return r[k]
def nonneg(v):n=dec(v);check(n>=0,'Negative source amount unsupported');return n
def rows(rs,label,empty=True):
    check(isinstance(rs,list),label+' requires list')
    check(empty or bool(rs),'Actual '+label+' required')
    check(all(isinstance(r,dict) and isinstance(r.get('id'),str) and re.fullmatch(r'[A-Za-z0-9 _./:-]+',r['id']) for r in rs),'Invalid '+label+' identity')
    check(len({r['id'] for r in rs})==len(rs),'Duplicate '+label+' ID')
    return rs

def source(r,docs):
    text(r,'document_id');check(r['document_id'] in docs,'Missing actual source document')
    check(docs[r['document_id']]['content']=={k:v for k,v in r.items() if k!='document_id'},'Source record changed after qualification')

def entry(account,amount,counter):
    a=cash(amount);return journal(('Dr' if a>=0 else 'Cr',account,abs(a)),('Cr' if a>=0 else 'Dr',counter,abs(a)))

def assess(c,claims):
    required(c,'package','execution_date','currency','requested_action','insurance_model','documents','contracts','groups','reports','cash_events','claims','population_review','gl','disclosure_review','statement_review')
    check(c['package']==PACKAGE and c['requested_action']=='accounting_workpaper','Accounting workpaper only; no projection or posting')
    check(c['framework']!='UK_GAAP','UK FRS103 requires actual existing policy/legal scope; generic measurement fail-closed')
    check(c.get('imports',[])==[] and c.get('owner_links',[])==[] and c.get('specialist_items',[])==[],'Unbound accounting-owner imports/features require governed specialist handoff')
    check(set(c['policy_elections'])<={'ifrs18_19_early_adoption','insurance_finance_oci'},'Unsupported unreviewed Insurance policy election')
    check(iso(c['period_start'])>=iso('2026-01-01') and iso(c['reporting_period'])<=iso('2026-12-31'),'Reviewed operative 2026 scope only')
    check(iso(c['execution_date'])>=iso(c['reporting_period']),'Execution predates measurement')
    check(c['entity_type']=='for_profit','Entity overlay unsupported')
    check(isinstance(c['currency'],str) and re.fullmatch('[A-Z]{3}',c['currency']),'Single actual functional currency required')
    fw=c['framework'];check(fw!='UK_GAAP','UK FRS103 requires actual existing policy/legal scope; generic measurement fail-closed')
    if fw=='AASB':
        check(c['reporting_tier']==1,'AASB Tier1 for-profit route only');edition='AASB17_DEC2022_PRE_JULY2026' if iso(c['period_start'])<iso('2026-07-01') else 'AASB17_DEC2022_JULY2026';check(c['aasb_compilation']==edition,'AASB17 exact operative compilation must follow annual period start')
    models={'IFRS':{'IFRS17_GMM','IFRS17_PAA'},'AASB':{'AASB17_GMM','AASB17_PAA'},'US_GAAP':{'ASC944_SHORT_DURATION'}}
    check(c['insurance_model'] in models.get(fw,set()),'Unsupported product/model, VFA, transition or long-duration route')
    from insurance_knowledge import retrieval_module
    module=retrieval_module();module.retrieve(fw,c['reporting_period'],module.SCOPES[fw],period_start=c['period_start'],insurance_model=c['insurance_model'])
    check(flag(c['policy_elections'],'ifrs18_19_early_adoption') is False,'Unsupported early adopted presentation overlay')
    check(c['policy_elections'].get('insurance_finance_oci',False) is False,'Unsupported OCI disaggregation election')
    check(set(c['knowledge_review']['applied_claim_ids'])=={x['claim_id'] for x in claims},'Insurance decision population including excluded boundaries must be reviewed/applied')
    docs={}
    for d in rows(c['documents'],'source documents',False):
        text(d,'reviewer','source_system','version');check(d['reviewer']!=c['preparer'],'Independent source qualification required')
        check(all(d.get(k)==c[k] for k in ('entity','framework','currency')) and d['as_of']==c['reporting_period'],'Source context/date differs')
        check(d['content_hash']==digest(d['content']),'Source bytes changed');docs[d['id']]=d
    contracts=rows(c['contracts'],'contracts',False);groups=rows(c['groups'],'groups',False);reports=rows(c['reports'],'actuarial reports',False)
    events=rows(c['cash_events'],'cash events');claims_pop=rows(c['claims'],'claims')
    pr=c['population_review'];source(pr,docs);text(pr,'reviewer','source_system','completeness_memo');check(pr['reviewer']!=c['preparer'] and flag(pr,'complete'),'Independent complete population review required')
    for key,rs in [('contracts',contracts),('groups',groups),('reports',reports),('cash_events',events),('claims',claims_pop)]:
        check(pr[key+'_ids']==[r['id'] for r in rs],'Complete '+key+' source population differs')
    economic=set()
    for r in contracts+events+claims_pop:
        source(r,docs);text(r,'economic_id');kind='contract' if r in contracts else 'event' if r in events else 'claim';key=(kind,r['economic_id'])
        check(key not in economic,'Duplicate economic '+kind+' alias');economic.add(key)
    bypolicy={p['id']:p for p in contracts};bygroup={g['id']:g for g in groups};byreport={r['group_id']:r for r in reports}
    check(len(byreport)==len(reports) and set(byreport)==set(bygroup),'One qualified report per actual group required')
    group_economics=[g.get('economic_id') for g in groups];check(all(isinstance(x,str) and bool(x) for x in group_economics) and len(set(group_economics))==len(group_economics),'Duplicate group economic identity')
    seen=set();issued_ids=set();held_ids=set()
    for p in contracts:
        text(p,'terms_memo','risk_scenario_memo','boundary_memo','portfolio','product','profitability','recognition_date','coverage_start','coverage_end','issue_date','premium_due_date')
        for k in ('uncertain_event','adverse_effect','nonfinancial_risk','significant_insurance_risk','scope_assessed','financial_guarantee','seller_warranty','fixed_fee_service','separated_component','investment_component','participating','modification','acquired','transition'):
            flag(p,k)
        check(p['uncertain_event'] and p['adverse_effect'] and p['nonfinancial_risk'] and p['significant_insurance_risk'],'Actual significant insurance risk required; investment/service contract belongs to other owner')
        check(p['scope_assessed'] and not any(p[k] for k in ('financial_guarantee','seller_warranty','fixed_fee_service','separated_component','investment_component','participating','modification','acquired','transition')),'Scope exception/component/advanced contract requires separate governed owner')
        check(nonneg(p['insured_event_benefit'])>nonneg(p['no_event_benefit']) and flag(p,'commercial_substance'),'Present-value significant additional benefits require reviewed commercial risk scenarios')
        check(p['perspective'] in {'issued','reinsurance_held'},'Ordinary policyholder accounting unsupported')
        check(iso(p['issue_date'])<=iso(p['recognition_date'])<=iso(c['reporting_period']),'Actual issue/recognition chronology')
        check(iso(p['coverage_start'])<=iso(p['coverage_end']),'Invalid coverage period')
        check(iso(p['premium_due_date'])>=iso(p['issue_date']),'Invalid premium due date')
        check(p['currency']==c['currency'],'FX group requires completed Foreign Currency owner; current single currency only')
        if p['perspective']=='issued':
            if fw=='US_GAAP':
                check(p['recognition_date']==p['coverage_start']==p['premium_due_date'],'US bounded fully paid inception protection begins at premium due date');issued_ids.add(p['id']);continue
            expected=min(iso(p['coverage_start']),iso(p['premium_due_date']),iso(p['onerous_date']) if p['profitability']=='onerous' else iso('9999-12-31'))
            check(iso(p['recognition_date'])==expected,'Issued recognition must use earliest actual coverage/due/onerous trigger');issued_ids.add(p['id'])
        else:held_ids.add(p['id'])
    entries=[];results=[];stocks={};used_events=set();used_claims=set();losses=ZERO
    def emit(a,n,b):
        j=entry(a,n,b)
        if j:entries.append(j)
    for g in groups:
        source(g,docs);gid=g['id'];text(g,'portfolio','grouping_memo','recognition_date','profitability','model')
        check(isinstance(g['contract_ids'],list) and g['contract_ids'] and len(set(g['contract_ids']))==len(g['contract_ids']),'Group contract population invalid')
        ps=[]
        for pid in g['contract_ids']:
            check(pid in bypolicy and pid not in seen,'Policy missing or allocated twice');check(bypolicy[pid]['group_id']==gid,'Actual policy group differs from membership');seen.add(pid);ps.append(bypolicy[pid])
        held=all(p['perspective']=='reinsurance_held' for p in ps);check(held or all(p['perspective']=='issued' for p in ps),'Held/issued mixed group')
        check(all(p['portfolio']==g['portfolio'] and p['profitability']==g['profitability'] and p['product']==g['product'] for p in ps),'Risk/management/profitability grouping differs')
        check(g['original_contract_ids']==g['contract_ids'] and flag(g,'membership_locked'),'Recognized group reassigned')
        if fw in {'IFRS','AASB'}:
            issues=[iso(p['issue_date']) for p in ps];check(max(issues)<min(issues).replace(year=min(issues).year+1),'Annual cohort exceeds one year')
            check(all(p['cohort']==g['cohort']==str(iso(p['issue_date']).year) for p in ps),'Wrong annual cohort')
        check(g['recognition_date']==min(p['recognition_date'] for p in ps),'Group recognition date differs')
        check(iso(g['recognition_date'])>=iso(c['period_start']),'First-year new groups only; opening contracts need governed extension')
        check(g['model']==c['insurance_model'],'Model differs from explicitly governed case model')
        report=byreport[gid];source(report,docs)
        text(report,'actuary','qualification_memo','objectivity_memo','reviewer','model_version','assumption_version','assumptions_memo','signed_on','measurement_date','discount_source','risk_adjustment_source','coverage_method','change_classification_memo')
        check(report['actuary']!=c['preparer'] and report['reviewer']!=c['preparer'] and report['reviewer']!=report['actuary'],'Qualified independent actuarial review required')
        check(all(report[k]==c[k] for k in ('entity','framework','currency')) and report['model']==g['model'],'Actuarial entity/framework/product model mismatch')
        check(report['product']==g['product'] and report['portfolio']==g['portfolio'],'Actuarial product/portfolio differs')
        check(report['measurement_date']==c['reporting_period'] and iso(c['reporting_period'])<=iso(report['signed_on'])<=iso(c['execution_date']),'Stale actuarial measurement/signoff')
        check(report['assumption_version']==g['assumption_version'] and report['model_version']==g['model_version'],'Assumptions/model changed after report')
        check(report['contract_ids']==g['contract_ids'],'Actuarial contract population incomplete')
        actual_claims=[r for r in claims_pop if r['group_id']==gid];actual_events=[r for r in events if r['group_id']==gid]
        check(report['claim_population_hash']==digest(actual_claims) and report['cash_population_hash']==digest(actual_events),'Actuarial source population totals/bytes differ')
        check(report['contract_population_hash']==digest(ps),'Actuarial policy population differs')
        check(report['initial_date']==g['recognition_date'],'Initial actuarial valuation date differs')
        check(report['change_kind'] in {'none','experience','assumption'} and report['change_service']=='future' and report['change_risk']=='nonfinancial','Error/model/policy/financial changes require separate owner or governed financial split')
        check(report['unsupported_features']==[] and flag(report,'boundary_reviewed'),'Actuarial boundary/unsupported features unresolved')
        if report['change_kind']=='none':exact(report['future_change_locked'],0,'No-change classification contradicts future movement');exact(report['future_change_current'],0,'No-change classification contradicts current valuation')
        if not g['model'].endswith('_GMM'):exact(report['future_change_locked'],0,'GMM future-service movement outside model');exact(report['future_change_current'],0,'GMM future-service movement outside model')
        ev={k:ZERO for k in ('premium','acquisition','claim_payment','recovery')}
        for e in actual_events:
            check(e['kind'] in ev and e['policy_id'] in g['contract_ids'],'Cash event outside actual group')
            check(iso(c['period_start'])<=iso(e['date'])<=iso(c['reporting_period']),'Cash cutoff differs')
            ev[e['kind']]+=nonneg(e['amount']);used_events.add(e['id'])
        incurred=ZERO;paid=ZERO
        for q in actual_claims:
            check(q['policy_id'] in g['contract_ids'],'Claim belongs to wrong policy/group');text(q,'occurrence_date','payment_memo')
            policy=bypolicy[q['policy_id']];check(iso(policy['coverage_start'])<=iso(q['occurrence_date'])<=min(iso(policy['coverage_end']),iso(c['reporting_period'])),'Claim occurrence outside actual coverage/reporting cutoff')
            check(q['valuation_date']==c['reporting_period'],'Claim valuation stale')
            incurred+=nonneg(q['incurred']);paid+=nonneg(q['paid']);used_claims.add(q['id'])
        exact(report['incurred'],incurred,'Qualified incurred claims');exact(report['claim_paid'],paid,'Actual claim payments');exact(ev['recovery' if held else 'claim_payment'],paid,'Claims cash source')
        for k in ('opening_lrc','opening_lic','opening_csm','opening_ra','opening_loss'):exact(report[k],0,'First-year '+k)
        n=lambda k:nonneg(report[k]);v=lambda k:dec(report[k])
        premium=ev['premium'];exact(premium,n('expected_premiums'),'Complete within-boundary premium population');exact(n('incurred_pv')+n('incurred_ra'),incurred,'Qualified incurred PV and risk-adjustment split');
        if fw=='US_GAAP':exact(n('incurred_ra'),0,'US claims cannot contain IFRS risk adjustment')
        acq=ev['acquisition'];revenue=ZERO;csm=ZERO;ra=ZERO;loss=ZERO;finance=ZERO;expense=ZERO
        csm0=loss0=interest=change=release=ra0=ra_release=alloc=amort=writeoff=dac=ZERO;expense_election=False
        lrc_account=('Reinsurance remaining coverage ' if held else 'Insurance remaining coverage ')+gid
        lic_account=('Reinsurance incurred recovery ' if held else 'Insurance incurred claims ')+gid
        revenue_account=('Reinsurance service expense ' if held else 'Insurance service revenue ')+gid
        expense_account=('Reinsurance service recovery ' if held else 'Insurance service expense ')+gid
        finance_account=('Reinsurance finance ' if held else 'Insurance finance ')+gid
        if held:
            check(fw in {'IFRS','AASB'} and g['model'].endswith('_PAA'),'Only IFRS/AASB prospective PAA reinsurance held supported')
            check(all(p['reinsurance_kind']=='proportionate' and p['counterparty'] and p['underlying_policy_ids'] for p in ps),'Prospective proportionate treaty/counterparty required')
            for p in ps:
                underlying=p['underlying_policy_ids'];check(len(set(underlying))==len(underlying) and set(underlying)<=issued_ids,'Reinsurance underlying policy mismatch')
                check(all(bypolicy[i]['profitability']!='onerous' for i in underlying),'Underlying onerous reinsurance loss-recovery timing needs governed extension')
                rec=max(iso(p['coverage_start']),min(iso(bypolicy[i]['recognition_date']) for i in underlying))
                check(report['counterparty']==p['counterparty'],'Reinsurance counterparty differs from qualified report')
                ratio=dec(p['recovery_fraction']);check(0<ratio<=1,'Actual treaty recovery percentage required')
                recovery_keys=[(q['policy_id'],q.get('underlying_claim_id')) for q in actual_claims];check(len(set(recovery_keys))==len(recovery_keys),'Underlying recovery duplicated within treaty')
                for q in actual_claims:
                    uq=next((z for z in claims_pop if z['id']==q.get('underlying_claim_id')),None);check(uq is not None and uq['policy_id'] in underlying,'Recovery lacks actual covered underlying claim')
                    exact(q['incurred'],dec(uq['incurred'])*ratio,'Qualified covered proportional incurred recovery');exact(q['paid'],dec(uq['paid'])*ratio,'Actual covered proportional recovery cash')
                check(iso(p['recognition_date'])==rec,'Proportionate reinsurance recognition differs from direct date')
            check(n('loss_recovery')==0,'Reinsurance loss-recovery/retroactive/gain routes require extension')
            exact(acq,0,'Reinsurance acquisition commission unsupported');exact(ev['claim_payment'],0,'Held claim payments cannot be gross direct claims')
            check(isinstance(report.get('underlying_group_ids'),list) and all(i in byreport for i in report['underlying_group_ids']),'Missing actual underlying reinsurance group')
            check(flag(report,'nonperformance_reviewed') and report['underlying_report_ids']==[byreport[bygroup_id]['id'] for bygroup_id in report['underlying_group_ids']],'Qualified reinsurer default/underlying actuarial links required')
            check(set(report['underlying_group_ids'])=={bypolicy[i]['group_id'] for p in ps for i in p['underlying_policy_ids']},'Underlying actuarial group differs')
        else:exact(ev['recovery'],0,'Gross issued recoveries belong to reinsurance owner')
        if g['model'].endswith('_GMM'):
            check(not held and acq==0,'GMM acquisition assets/reinsurance require governed extension')
            check(all(e['date']==g['recognition_date'] for e in actual_events if e['kind']=='premium'),'GMM bounded premiums received at initial recognition only')
            exact(premium,n('expected_premiums'),'Complete inception premiums');out=n('initial_outflows');ra0=n('initial_ra');initial=out+ra0-premium;csm0=max(-initial,ZERO);loss0=max(initial,ZERO)
            exact(report['initial_fcf'],initial,'Initial fulfilment cash flows');exact(report['initial_csm'],csm0,'Initial CSM cannot be plug');exact(report['initial_loss'],loss0,'Initial onerous loss')
            check((loss0>0)==(g['profitability']=='onerous'),'Onerous classification contradicts qualified inception measurement')
            rate=v('locked_rate');check(0<=rate<=1,'Qualified locked rate outside range');fraction=v('interest_fraction');check(0<=fraction<=1,'Interest accrual period invalid')
            check(report['interest_day_basis']=='actual365_simple','Unsupported qualified CSM interest accrual method')
            days=(iso(c['reporting_period'])-iso(g['recognition_date'])).days+1;scalar(fraction,Decimal(days)/Decimal(365),'Actual dated CSM accrual fraction')
            interest=cash(csm0*rate*fraction);exact(report['csm_interest'],interest,'Locked-rate CSM interest')
            change=v('future_change_locked');exact(change,v('future_change_current'),'Current/locked split differs; complex rate change requires governed finance extension');check(flag(report,'discount_curve_unchanged'),'Different current/locked curves unsupported')
            available=csm0+interest-change;check(available>=0 and (loss0==0 or change==0),'CSM-exhaustion or loss reversal needs specialist extension')
            units=n('current_units');remaining=n('remaining_units');check(units+remaining>0,'Actual governed coverage units required')
            if all(iso(p['coverage_end'])<=iso(c['reporting_period']) for p in ps):exact(remaining,0,'Expired GMM coverage cannot retain future units')
            release=cash(available*units/(units+remaining));csm=available-release;exact(report['csm_release'],release,'Coverage-unit CSM release');exact(report['closing_csm'],csm,'CSM rollforward')
            service=n('expected_service');ra_release=n('ra_release');ra=ra0-ra_release;check(ra>=0,'RA release exceeds qualified RA');exact(report['closing_ra'],ra,'RA rollforward');fcf_fin=v('fcf_finance');finance=fcf_fin+interest
            pv=out-service+change+fcf_fin;check(pv>=0,'Remaining qualified PV cannot be negative in bounded issued route');exact(report['closing_pv'],pv,'FCF PV rollforward')
            alloc=n('loss_allocation');check(alloc<=loss0 and (loss0>0 or alloc==0),'Invalid loss-component allocation');text(report,'loss_allocation_method');loss=loss0-alloc
            check(alloc<=service+ra_release,'Loss allocation exceeds supported service movement');revenue=service+ra_release+release-alloc
            lrc=pv+ra+csm;exact(report['closing_loss'],loss,'Loss-component bridge');check(loss<=lrc,'Loss component exceeds total remaining coverage')
            if remaining==0:exact(loss,0,'Expired group loss component must exhaust');exact(lrc,0,'Expired GMM remaining coverage')
            emit('Cash',premium,lrc_account);emit(expense_account,loss0,lrc_account);emit(finance_account,finance,lrc_account);emit(lrc_account,revenue,'Insurance service revenue '+gid);emit(lrc_account,alloc,expense_account);expense+=loss0-alloc
        elif g['model'].endswith('_PAA'):
            check(g['profitability'] in {'no_significant_possibility','remaining','onerous','net_cost'},'Actual profitability group required')
            durations=[(iso(p['coverage_end'])-iso(p['coverage_start'])).days+1 for p in ps]
            one_year=all(iso(p['coverage_end'])<iso(p['coverage_start']).replace(year=iso(p['coverage_start']).year+1) for p in ps)
            check(one_year or (flag(report,'paa_material_equivalence') and not flag(report,'paa_significant_variability')),'PAA eligibility not established at inception')
            check(flag(report,'paa_inception_reviewed'),'PAA inception eligibility review missing')
            check(flag(report,'premium_financing_exemption') and n('max_service_to_due_days')<=365,'PAA premium financing requires independently governed adjustment')
            due_days=max(max(abs((iso(p['coverage_start'])-iso(p['premium_due_date'])).days),abs((iso(p['coverage_end'])-iso(p['premium_due_date'])).days)) for p in ps);exact(report['max_service_to_due_days'],due_days,'Actual service-to-premium due horizon');check(due_days<=365,'Actual service/premium financing exceeds one year')
            check(flag(report,'claim_discount_exemption') and n('max_claim_to_payment_days')<=365,'LIC discounting outside one-year exemption requires governed extension')
            settlement_days=[]
            for q in actual_claims:
                text(q,'expected_settlement_date');check(iso(q['expected_settlement_date'])>=iso(q['occurrence_date']),'Claim settlement predates incurrence');days=(iso(q['expected_settlement_date'])-iso(q['occurrence_date'])).days;check(iso(q['expected_settlement_date'])<=iso(q['occurrence_date']).replace(year=iso(q['occurrence_date']).year+1),'Actual claim expected settlement exceeds one year');settlement_days.append(days)
            exact(report['max_claim_to_payment_days'],max(settlement_days,default=0),'Actual expected claim settlement horizon')
            check(report['revenue_pattern'] in {'time','risk'} and flag(report,'pattern_reviewed'),'Actual expected premium/risk release pattern required')
            fraction=v('service_fraction');check(0<=fraction<=1,'Service allocation outside [0,1]')
            if report['revenue_pattern']=='time':
                patterns=[]
                for p in ps:
                    elapsed=max(0,(min(iso(c['reporting_period']),iso(p['coverage_end']))-iso(p['coverage_start'])).days+1);total=(iso(p['coverage_end'])-iso(p['coverage_start'])).days+1;patterns.append(Decimal(elapsed)/Decimal(total))
                check(all(x==patterns[0] for x in patterns),'Mixed coverage time patterns need actual weighted allocation');scalar(fraction,patterns[0],'Actual elapsed-time premium allocation')
            else:check(flag(report,'significant_risk_pattern'),'Risk-pattern departure not established');scalar(fraction,v('risk_release_fraction'),'Qualified risk-based service release')
            if all(iso(p['coverage_end'])<=iso(c['reporting_period']) for p in ps):exact(fraction,1,'Expired PAA coverage service release')
            revenue=cash(n('expected_premiums')*fraction);exact(report['service_release'],revenue,'Expected-premium service pattern')
            check(revenue<=premium,'Unreceived boundary premiums require receivable/current-boundary extension')
            amort=n('acquisition_amortization');expense_election=flag(report,'acquisition_expense_election')
            check(flag(report,'acquisition_attributable'),'Only actual attributable insurance acquisition cash flows enter insurance cost population')
            if expense_election:check(one_year and amort==0,'PAA acquisition expense election/amortization invalid')
            else:check(amort<=acq and flag(report,'acquisition_attributable'),'Only directly attributable acquisition cash flows capitalizable')
            loss=n('paa_loss');check(flag(report,'onerous_assessed'),'PAA onerous assessment omitted');base=premium-(0 if expense_election else acq)+amort-revenue;expected_loss=max(n('remaining_fcf')-base,ZERO) if flag(report,'onerous_indicator') else ZERO;exact(loss,expected_loss,'PAA qualified onerous excess');check(not held or loss==0,'Reinsurance held cannot apply issued onerous floor')
            lrc=base+loss;check(lrc>=0,'Net asset PAA remaining coverage outside bounded route');expense+= (acq if expense_election else amort)+loss
            if held:
                emit(lrc_account,premium,'Cash');emit(revenue_account,revenue,lrc_account)
            else:
                emit('Cash',premium,lrc_account);emit(expense_account if expense_election else lrc_account,acq,'Cash');emit(expense_account,amort,lrc_account);emit(lrc_account,revenue,'Insurance service revenue '+gid);emit(expense_account,loss,lrc_account)
        else:
            check(not held and all(p['us_contract_type']=='short_duration' for p in ps),'US short-duration issued contracts only; LDTI/MRB/reinsurance unsupported')
            check(flag(report,'us_insurance_entity') and flag(report,'us_contract_scope_reviewed'),'Actual ASC944 insurance-entity and contract scope required')
            check(all(e['date']==g['recognition_date'] for e in actual_events if e['kind']=='premium'),'US bounded inception premium population only')
            check(g['profitability']=='us_aggregation' and report['us_aggregation_basis']==g['aggregation_basis'],'Native US premium-deficiency aggregation required')
            for k in ('initial_ra','closing_ra','initial_csm','closing_csm','csm_release','csm_interest','loss_recovery'):exact(report[k],0,'IFRS RA/CSM prohibited in US route')
            check(report['revenue_pattern']=='protection' and flag(report,'pattern_reviewed'),'US actual protection premium earning required')
            fraction=v('service_fraction');check(0<=fraction<=1,'US earned-premium fraction invalid');scalar(fraction,v('protection_release_fraction'),'Actual qualified US protection earning')
            if all(iso(p['coverage_end'])<=iso(c['reporting_period']) for p in ps):exact(fraction,1,'Expired US coverage fully earned')
            revenue=cash(n('expected_premiums')*fraction);check(revenue<=premium,'US unreceived premium accounting requires extension');exact(report['service_release'],revenue,'US earned premium')
            amort=n('acquisition_amortization');check(flag(report,'successful_acquisition') and flag(report,'acquisition_attributable') and amort<=acq,'US successful acquisition DAC qualification required')
            exact(amort,cash(acq*fraction),'US DAC native premium/protection amortization');dac=acq-amort;base=premium-revenue;check(flag(report,'onerous_assessed'),'US premium deficiency test omitted')
            check(report['investment_income_policy']=='exclude' and n('investment_income')==0,'US investment-income deficiency policy outside bounded scope')
            deficiency=max(n('remaining_claims')+n('maintenance_cost')+dac-base,ZERO);writeoff=min(dac,deficiency);loss=deficiency-writeoff;dac-=writeoff;lrc=base+loss
            exact(report['dac_writeoff'],writeoff,'US DAC deficiency ordering');exact(report['closing_dac'],dac,'US DAC bridge');exact(report['deficiency_liability'],loss,'US deficiency liability');expense=amort+deficiency
            emit('Cash',premium,lrc_account);emit('US DAC '+gid,acq,'Cash');emit(expense_account,amort+writeoff,'US DAC '+gid);emit(lrc_account,revenue,'Insurance service revenue '+gid);emit(expense_account,loss,lrc_account);stocks['US DAC '+gid]=(ZERO,dac)
        estimate=v('past_service_change');lic_fin=v('lic_finance');lic=incurred+estimate+lic_fin-paid;check(lic>=0,'Qualified incurred claim/recovery balance negative')
        exact(report['closing_lic'],lic,'Incurred-claims rollforward');exact(report['closing_lrc'],lrc,'Remaining-coverage rollforward')
        if fw=='US_GAAP':check(lic_fin==0 and flag(report,'claims_undiscounted'),'US bounded undiscounted claims route only')
        if held:
            emit(lic_account,incurred+estimate,expense_account);emit(lic_account,lic_fin,finance_account);emit('Cash',paid,lic_account);stocks[lrc_account]=(ZERO,lrc);stocks[lic_account]=(ZERO,lic)
        else:
            emit(expense_account,incurred+estimate,lic_account);emit(finance_account,lic_fin,lic_account);emit(lic_account,paid,'Cash');stocks[lrc_account]=(ZERO,-lrc);stocks[lic_account]=(ZERO,-lic)
        finance+=lic_fin;expense+=incurred+estimate
        csm_bridge=dict(opening=ZERO,new_business=csm0,interest=interest,future_service_change=-change,service_release=-release,closing=csm)
        ra_bridge=dict(opening=ZERO,new_business=ra0,service_release=-ra_release,closing=ra)
        loss_bridge=dict(opening=ZERO,new_business=loss0 if g['model'].endswith('_GMM') else loss,service_allocation=-alloc,closing=loss)
        lic_bridge=dict(opening=ZERO,incurred_pv=n('incurred_pv'),incurred_ra=n('incurred_ra'),past_service_change=estimate,finance=lic_fin,claim_payments=-paid,closing=lic)
        if g['model'].endswith('_GMM'):lrc_bridge=dict(opening=ZERO,premiums=premium,new_business_loss=loss0,finance=finance-lic_fin,service_release=-revenue,loss_allocation=-alloc,closing=lrc)
        elif g['model'].endswith('_PAA'):lrc_bridge=dict(opening=ZERO,premiums=premium,acquisition_payment=ZERO if held or expense_election else -acq,acquisition_amortization=ZERO if held else amort,service_release=-revenue,onerous_loss=loss,closing=lrc)
        else:lrc_bridge=dict(opening=ZERO,premiums=premium,earned_premiums=-revenue,deficiency_liability=loss,closing=lrc)
        bridges=dict(remaining_coverage=lrc_bridge,incurred_claims=lic_bridge,csm=csm_bridge,risk_adjustment=ra_bridge,loss_component=loss_bridge)
        if fw=='US_GAAP':
            bridges.pop('csm');bridges.pop('risk_adjustment');bridges.pop('loss_component');bridges['premium_deficiency']=dict(opening=ZERO,new_deficiency=loss,closing=loss)
            bridges['dac']=dict(opening=ZERO,successful_acquisition=acq,amortization=-amort,deficiency_writeoff=-writeoff,closing=dac)
        for name,bridge in bridges.items():exact(sum((value for key,value in bridge.items() if key!='closing'),ZERO),bridge['closing'],name+' named rollforward')
        results.append(dict(rollforwards=bridges,id=gid,economic_id=g['economic_id'],perspective='reinsurance_held' if held else 'issued',portfolio=g['portfolio'],model=g['model'],premium=premium,acquisition=acq,revenue=revenue,service_expense=expense,finance=finance,remaining_coverage=lrc,incurred_claims=lic,csm=csm,risk_adjustment=ra,loss_component=loss,report_id=report['id'],contract_ids=g['contract_ids']))
        if fw=='US_GAAP':
            for key in ('csm','risk_adjustment','loss_component'):results[-1].pop(key)
            results[-1]['premium_deficiency_liability']=loss
    check(seen==set(bypolicy),'Missing policy from complete group population');check(used_events=={r['id'] for r in events} and used_claims=={r['id'] for r in claims_pop},'Unused claims/cash population')
    delta={}
    for j in entries:
        balance(j)
        for l in j:delta[l['account']]=delta.get(l['account'],ZERO)+dec(l['amount'])*(1 if l['side']=='Dr' else -1)
    gl=rows(c['gl'],'GL',False);bygl={r['id']:r for r in gl};check(set(delta)==set(bygl),'Complete GL account population differs from journals')
    for a,r in bygl.items():
        source(r,docs);exact(r['opening'],0,'First-year GL opening');exact(r['closing'],delta[a],'Journal-to-GL '+a);exact(r['statement'],r['closing'],'Statement '+a)
    for a,(opening,closing) in stocks.items():check(a in bygl or closing==0,'Contract stock missing from GL');exact(bygl[a]['closing'] if a in bygl else 0,closing,'Contract schedule/GL '+a)
    sr=c['statement_review'];source(sr,docs);check(sr['gl_hash']==digest(gl) and flag(sr,'gross_presentation') and sr['group_ids']==[g['id'] for g in groups],'Insurance statements must retain exact gross population')
    dr=c['disclosure_review'];source(dr,docs);text(dr,'reviewer','framework_checklist','methods_inputs_memo','risk_memo');check(dr['reviewer']!=c['preparer'] and flag(dr,'complete'),'Qualified insurance disclosure review required')
    check(dr['framework']==fw and dr['group_ids']==[g['id'] for g in groups] and dr['report_ids']==[r['id'] for r in reports],'Disclosure population incomplete')
    required_requirements={'amounts','rollforwards','judgments','insurance_risk','financial_risk'}
    check(set(dr['requirement_ids'])==required_requirements,'Actual framework-specific disclosure requirements incomplete')
    support=[]
    for r in gl:
        a=r['id'];category='asset' if a=='Cash' or a.startswith(('US DAC','Reinsurance remaining','Reinsurance incurred')) else 'liability' if a.startswith(('Insurance remaining','Insurance incurred')) else 'revenue' if a.startswith(('Insurance service revenue','Reinsurance service recovery')) else 'expense'
        gid=next((g['id'] for g in groups if a.endswith(' '+g['id'])),None)
        support.append(dict(id=a,group_id=gid,economic_id=bygroup[gid]['economic_id'] if gid else 'insurance_cash',currency=c['currency'],account=a,category=category,signed_balance=dec(r['closing'])))
    exact(sum((dec(r['closing']) for r in gl),ZERO),0,'Insurance source TB')
    return dict(conclusion='Qualified insurance accounting schedules and gross reporting support reconciled',method='Framework-specific first-year insurance accounting of reviewed actuarial inputs',calculations=dict(groups=results,gl_movements=delta,statement_support=support,disclosure_support=dict(requirements=sorted(required_requirements),group_ids=[g['id'] for g in groups],policy_ids=[p['id'] for p in contracts],claim_ids=[q['id'] for q in claims_pop],actuarial_report_ids=[r['id'] for r in reports],amounts=results,amounts_by_group={r['id']:r for r in results}),actuarial_boundary=dict(status='qualified_inputs_consumed',valuation_date=c['reporting_period'],model_versions=[r['model_version'] for r in reports],assumption_registers=[r['assumption_version'] for r in reports])),journal_entry_implications=entries,judgments=['Contract terms, significant insurance risk, aggregation, eligibility and actuarial assumptions are independently reviewed source conclusions'],uncertainties=['First-year single-currency issued GMM/PAA and native US short-duration routes only; advanced models and specialist owner accounting require separate governed methods.'],open_items=[],disclosures_impacted=['Insurance amounts and rollforwards','Qualified methods, assumptions and insurance/financial risk','Issued and held populations remain separate; Disclosure Management owns final requirements'])
