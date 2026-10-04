"""Clearly synthetic native Insurance/Statements/Disclosure handoff fixtures."""
import copy
from decimal import Decimal
from insurance_cases import case,reinsurance_case,ready,PACKAGE
from production import execute,case_fingerprint
from additional_cases import reporting,certify
import governance_cases as governance

def insurance_import(fw='IFRS',reinsurance=False,route='gmm'):
    c=ready(reinsurance_case(fw) if reinsurance else case(fw,route))
    r=execute(PACKAGE,c)
    assert r['status']=='complete',r
    return governance.row(c,'insurance-owner',package=PACKAGE,case=c,result=r,mode='evidence_only')

def reporting_fixture(fw='IFRS',reinsurance=False,route='gmm'):
    imp=insurance_import(fw,reinsurance,route);ic=imp['case'];source=imp['result'];c=reporting(fw)
    c.update(currency=ic['currency'],entity=ic['entity'],jurisdiction=ic['jurisdiction'])
    c['current_tb']=[];mapping=[];profit=Decimal(0);cash=Decimal(0)
    for s in source['calculations']['statement_support']:
        tid='insurance-'+s['id'];bal=Decimal(str(s['signed_balance']))
        c['current_tb'].append(dict(id=tid,balance=str(bal),category=s['category'],line=s['id'],source_version=source['case_fingerprint'],classification_memo='Synthetic independently reviewed Insurance statement mapping',cash_account=s['account']=='Cash',insurance_source_id=s['id'],insurance_economic_id=s['economic_id']))
        mapping.append(dict(id=tid,source_id=s['id'],tb_id=tid))
        if s['category'] in ('revenue','expense'):profit-=bal
        if s['account']=='Cash':cash+=bal
    c['comparative_tb']=[dict(id='cash',balance='0',category='asset',line='cash',source_version='synthetic-issued-prior',classification_memo='Actual first-year zero source',cash_account=True)]
    c['equity_bridge']=[dict(id='insurance-equity',opening='0',profit=str(profit),oci='0',owner_transactions='0',retrospective_adjustments='0',other='0',closing=str(profit),memo='Synthetic Insurance accounting earnings bridge')]
    c['cash_flow'].update(start_subtotal='profit',start_amount=str(profit),adjustments=[dict(id='insurance-operating-bridge',amount=str(cash-profit),source='Actual Insurance journal and stock movements',noncash_acquisition_fx_excluded=True,memo='Synthetic gross insurance service/contract movements')],investing='0',financing='0',fx='0',opening='0',closing=str(cash),balance_sheet_bridge='0',opening_balance_sheet_bridge='0',classifications=[dict(id='insurance-operating-cash',kind='insurance_premiums_claims_acquisition',date=c['reporting_period'],**{'class':'operating'},amount=str(cash),memo='Synthetic independently reviewed Insurance cash population')])
    c['notes']=[dict(id='insurance-cash-note',target='cash',amount=str(cash),population_evidence='Synthetic actual bank and Insurance journal population',memo='Gross cash support')]
    c=certify('financial-statements',c);r=execute('financial-statements',c);assert r['status']=='complete',r
    return imp,dict(id='reporting-owner',package='financial-statements',case=c,result=r),mapping

def disclosure_fixture(fw='IFRS',reinsurance=False,route='gmm'):
    imp=insurance_import(fw,reinsurance,route);source=imp['result'];c=governance.case('disclosure-management',fw)
    c.update(currency=imp['case']['currency'],imports=[imp],documents=[],document_inventory=[],notes=[],note_inventory=[],requirements=[])
    version='qualified-insurance-2026';metrics=('premium','acquisition','revenue','service_expense','finance','remaining_coverage','incurred_claims','csm','risk_adjustment','loss_component','premium_deficiency_liability')
    for gid,g in source['calculations']['disclosure_support']['amounts_by_group'].items():
        fields=[(metric,[metric],g[metric]) for metric in metrics if metric in g]
        fields += [('rollforward-'+name+'-'+key,['rollforwards',name,key],value) for name,bridge in g['rollforwards'].items() for key,value in bridge.items()]
        for label,tail,amount in fields:
            metric=tail[-1];rid=gid+'-'+label;value=str(amount);path=['disclosure_support','amounts_by_group',gid]+tail
            governance.document(c,'applicability-'+rid,dict(requirement_id=rid,applicable=True,current_source_version=version),currency=c['currency'])
            governance.document(c,'prior-'+rid,dict(period=['2025-01-01','2025-12-31'],requirement_key=rid,units=c['currency'],amount='0'),currency=c['currency'])
            governance.document(c,'statement-'+rid,dict(metric=metric,units=c['currency'],amount=value),currency=c['currency'])
            c['requirements'].append(governance.row(c,rid,amount=value,topic_id='SUPPLEMENTAL_INSURANCE_CONTRACTS',requirement_key=rid,requirement_text='Synthetic actual qualified Insurance amount and rollforward requirement',owner_import=imp['id'],applicability_doc='applicability-'+rid,accountable_owner='Synthetic actual disclosure controller',applicability_memo='Actual independently scoped group and effective-period requirement',applicable=True,owner_requirement=source['disclosures_impacted'][0],metric=metric,result_path=path))
            c['notes'].append(governance.row(c,'note-'+rid,requirement_id=rid,note_location='Synthetic insurance note '+gid,cross_reference='Actual Insurance reporting schedule',narrative=source['conclusion'],amount=value,prior_amount='0',issued_prior_doc='prior-'+rid,units=c['currency'],statement_doc='statement-'+rid,unchanged_comparative=True,review_notes_closed=True))
    c['note_inventory']=[n['id'] for n in c['notes']];c['source_inventory']=[r['id'] for r in c['requirements']]
    c['requirement_source']=governance.source_index(c,'insurance-requirement-register',c['requirements'])
    c['requirement_source'].update(requirement_version=version,current_scope_memo='Actual current Insurance entity/framework scope',topic_coverage_memo='Synthetic separately approved Insurance namespace, no canonical mapping',authority_review_memo='Current qualified requirements reviewed independently',checked_on=c['execution_date'],effective_period=[c['period_start'],c['reporting_period']],applicable_topic_inventory=['SUPPLEMENTAL_INSURANCE_CONTRACTS'])
    c['controls'].update(population_count=len(c['requirements']),population_amount=str(sum(abs(Decimal(r['amount'])) for r in c['requirements'])))
    c=governance.ready('disclosure-management',fw,c,release=True);r=execute('disclosure-management',c);assert r['status']=='complete',r
    return imp,dict(id='disclosure-owner',package='disclosure-management',case=c,result=r)
