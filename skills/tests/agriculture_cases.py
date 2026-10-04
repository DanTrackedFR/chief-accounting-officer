"""Synthetic source evidence and test approvals, never real authenticated records."""
import copy
from decimal import Decimal
from governance_cases import case as previous_case, row, document, source_index
from production import canonical_knowledge,case_fingerprint,PACKAGES
from governance_accounting import digest
PACKAGE='agriculture-biological-assets'

def content(c,id):return next(d['content'] for d in c['documents'] if d['id']==id)

def value(c,id,asset,qty,date,gross,costs='0'):
    v=dict(qualified_valuer='Synthetic independent qualified valuer',qualification_memo='Synthetic competence assessed',independence_memo='Synthetic objectivity review',report_version='synthetic-v1',market_evidence='Synthetic current actual market report',selling_costs_memo='Incremental disposal costs excluding tax and finance',measurement_basis='fair_value_less_costs_to_sell',entity=c['entity'],framework=c['framework'],asset_id=asset['id'],category=asset['category'],currency=c['currency'],measurement_date=date,signed_on=c['execution_date'],control_supported=True,reliable_measurement=True,current_market_evidence=True,quantity=qty,fair_value=gross,costs_to_sell=costs,net_value=str(Decimal(gross)-Decimal(costs)))
    v.update(finance_or_income_tax_included=False,transport_deducted_again=False,other_uncertain_costs=False,
        quantity_unit=asset['quantity_unit'],
        cost_components=[dict(id='selling-commission',kind='commission',amount=costs,incremental_disposal=True,evidence_memo='Synthetic independently qualified actual commission')] if Decimal(costs) else [])
    document(c,id,v)

def disclosure_support(c):
    """Synthetic fixture source preparation from known controlled ledger facts."""
    dis=c['disclosures'];by={g['id']:g for g in c['gl']}
    opening=sum(Decimal(a['opening_value']) for a in c['assets'])
    closing=sum(Decimal(a['amount']) for a in c['assets'])
    purchases=sum(Decimal(a['purchase_cost']) for a in c['assets'])
    gain=Decimal(dis['pnl_measurement_gain']);harvest=Decimal(dis['harvest_entry'])
    mortality=Decimal(by.get('Agriculture mortality loss',{}).get('closing','0'))-Decimal(by.get('Agriculture mortality loss',{}).get('opening','0'))
    q=lambda rows:sum((Decimal(r['quantity']) for r in rows),Decimal(0))
    values=dict(classes=sorted({a['category'] for a in c['assets']}),policies=c['accounting_policy']['agriculture_model'],gain_loss=str(gain),
        rollforward={k:str(v) for k,v in dict(opening=opening,purchases=purchases,measurement_gain=gain,harvest_entry=harvest,mortality_loss=mortality,closing=closing).items()},
        quantities={k:str(v) for k,v in dict(opening=q(c['opening_population']),purchases=q([a for a in c['assets'] if a['state']=='purchase']),births=q([a for a in c['assets'] if a['state']=='birth']),harvest=q([a for a in c['movements'] if a['kind']=='harvest']),deaths=q([a for a in c['movements'] if a['kind']=='death']),closing=q(c['closing_population'])).items()},harvest=str(harvest))
    terminal={m['asset_id']:m for m in c['movements']};used=[]
    for a in c['assets']:
        if a['state']!='opening':used.append(a['initial_value_doc'])
        if a['id'] not in terminal:used.append(a['closing_value_doc'])
        elif terminal[a['id']]['kind']=='harvest':
            used.append(terminal[a['id']]['valuation_doc'])
            used.append(content(c,terminal[a['id']]['harvest_doc'])['produce_valuation_doc'])
    values['valuation']=sorted(used)
    for r in dis['requirements']:
        id=r['id']+'-support';r['support_doc']=id
        payload=dict(requirement_id=r['id'],entity=c['entity'],framework=c['framework'],checked_on=c['execution_date'],support_memo='Synthetic actual qualified '+r['id']+' source',value=values.get(r['id'],'Synthetic documented actual facts reviewed'))
        if any(d['id']==id for d in c['documents']):next(d for d in c['documents'] if d['id']==id)['content']=payload
        else:document(c,id,payload)
    content(c,dis['requirements_doc'])[:]=copy.deepcopy(dis['requirements'])
    return c

def sources(c):
    """Fixture authoring only: build separately labelled controlled source snapshots."""
    c['asset_source']=source_index(c,'original-biological-register',c['assets']);c['asset_source']['source_doc']='register'
    c['movement_source']=source_index(c,'original-terminal-events',c['movements']);c['movement_source']['source_doc']='events'
    for id,rs in [('register',c['assets']),('events',c['movements']),('opening-pop',c['opening_population']),('closing-pop',c['closing_population'])]:
        if any(d['id']==id for d in c['documents']):
            d=next(d for d in c['documents'] if d['id']==id);d['content']=copy.deepcopy(rs)
        else:document(c,id,rs)
    c['source_inventory']=[r['id'] for r in c['assets']]
    for key in ('movements','opening_population','closing_population'):
        c[{'movements':'movement_inventory','opening_population':'opening_inventory','closing_population':'closing_inventory'}[key]]=[r['id'] for r in c[key]]
    c['controls'].update(population_count=len(c['assets']),population_amount=str(sum(Decimal(r['amount']) for r in c['assets'])))
    return c

def refresh(c):
    for d in c['documents']:d['content_hash']=digest(d['content'])
    from production import load_workflow
    c['release_review']=row(c,'release',review_memo='Synthetic independent exact source review',payload_fingerprint=digest({k:c[k] for k in load_workflow(PACKAGE).KEYS}))
    return c

def case(fw='IFRS',kind='livestock'):
    c=previous_case('ipo-accounting-readiness',fw)
    for k in ('readiness','readiness_source','dependencies','dependency_inventory','governance_method'):c.pop(k,None)
    c.update(package=PACKAGE,case_id='Synthetic Agriculture '+fw+' '+kind,requested_action='accounting',currency='USD',documents=[],document_inventory=[],imports=[],assets=[],movements=[],opening_population=[],closing_population=[])
    # Optional framework context is retained explicitly in fingerprint-sensitive payloads.
    c.setdefault('uk_standard_edition','not_applicable');c.setdefault('aasb_compilation','not_applicable')
    edition={'IFRS':'IAS41_2026_no_IFRS18','AASB':'AASB141_compilation2022_2026','UK_GAAP':'FRS102_September2024_2026','US_GAAP':'ASC905_2026'}[fw]
    c['applicability_review']['standard_versions']=[edition]
    if fw=='AASB':c['aasb_compilation']=edition
    c['classification']=row(c,'scope',checked_on=c['execution_date'],scope_memo='Actual synthetic agricultural transformation scope',legal_control_memo='Actual synthetic rights reviewed',biological_transformation_memo='Growth/harvest activity supported',source_system='Synthetic farm register',subledger='Synthetic biological subledger',entity=c['entity'],framework=fw,jurisdiction=c['jurisdiction'],effective_period=[c['period_start'],c['reporting_period']],reporting_basis={'IFRS':'full_IFRS','UK_GAAP':'full_FRS102','AASB':'Tier1_for_profit','US_GAAP':'ASC905_producer'}[fw],early_presentation_adoption=False,opening_population_doc='opening-pop',closing_population_doc='closing-pop',**{k:False for k in ('government_assistance','fx','valuation_requested','post_harvest_accounting','external_posting','unsupported_contract_rights')})
    c['accounting_policy']['agriculture_model']='fair_value_less_costs_to_sell'
    c['classification'].update(operative_edition=edition,edition_doc='edition-source')
    document(c,'edition-source',{k:c['classification'][k] for k in ('operative_edition','entity','framework','effective_period','checked_on','reporting_basis','early_presentation_adoption')}|dict(edition_memo='Synthetic independent operative edition and actual-case applicability review'))
    category='consumable_livestock' if kind=='livestock' else 'consumable_crop'
    c['accounting_policy']['class_models']={category:'fair_value_less_costs_to_sell'}
    # Three source units: surviving opening, terminal opening harvest, purchased survivor.
    for id,state,op,cl,qty in [('live','opening','100','130','1'),('harvest','opening','50','0','1'),('purchase','purchase','0','80','1')]:
        a=row(c,id,physical_id='physical-'+id,category=category,state=state,amount=cl,quantity=qty,quantity_unit='biological_units',currency='USD',opening_value=op,purchase_cost='60' if state=='purchase' else '0',control_doc=id+'-control',classification_doc=id+'-class',opening_valuation_memo='Prior controlled biological GL/source carrying value',recognition_date='2026-06-01',initial_value_doc=id+'-initial',closing_value_doc=id+'-closing',purchase_doc=id+'-purchase')
        c['assets'].append(a)
        document(c,a['control_doc'],dict(asset_id=id,physical_id=a['physical_id'],control_supported=True,probable_benefits=True,rights_memo='Actual synthetic control from documented past transaction',entity=c['entity'],framework=fw,jurisdiction=c['jurisdiction'],checked_on=c['execution_date']))
        document(c,a['classification_doc'],dict(asset_id=id,category=category,framework=fw,scope_memo='Qualified synthetic agricultural activity/living classification',route='agriculture',living=True,agricultural_activity=True,agriculture_model='fair_value_less_costs_to_sell'))
        if state=='opening':c['opening_population'].append(row(c,id,quantity=qty,physical_id=a['physical_id'],carrying_value=op))
        if cl!='0':
            c['closing_population'].append(row(c,id,quantity=qty,physical_id=a['physical_id'],carrying_value=cl));value(c,a['closing_value_doc'],a,qty,c['reporting_period'],str(Decimal(cl)+Decimal(5)),'5')
        if state=='purchase':
            value(c,a['initial_value_doc'],a,qty,a['recognition_date'],'75','5')
            document(c,a['purchase_doc'],dict(asset_id=id,date=a['recognition_date'],quantity=qty,cost='60'))
    a=c['assets'][1];h=row(c,'harvest-event',asset_id=a['id'],event_source_id='original-harvest-event-1',kind='harvest',date='2026-09-30',currency='USD',quantity='1',harvest_quantity='100',valuation_doc='harvest-value',harvest_doc='harvest-record')
    c['movements']=[h];value(c,'harvest-value',a,'1',h['date'],'75','5')
    document(c,'harvest-record',dict(asset_id=a['id'],date=h['date'],harvest_quantity='100',produce_unit='kg',produce_id='harvested-produce-1',produce_category='meat' if kind=='livestock' else 'grain',produce_valuation_doc='produce-value',qualified_produce_fvcts='70',entire_asset_harvested=True,boundary_only=True,inventory_entry_value='70'))
    value(c,'produce-value',dict(id='harvested-produce-1',category='meat' if kind=='livestock' else 'grain',quantity_unit='kg'),'100',h['date'],'75','5')
    content(c,'produce-value').update(point_at_harvest=True,origin_asset_id=a['id'])
    c['gl']=[row(c,'Biological assets',currency='USD',opening='150',closing='210',statement='210'),row(c,'Cash',currency='USD',opening='1000',closing='940',statement='940'),row(c,'Agriculture measurement gain',currency='USD',opening='0',closing='-70',statement='-70'),row(c,'Harvest inventory entry',currency='USD',opening='0',closing='70',statement='70')];c['gl_inventory']=[g['id'] for g in c['gl']]
    keys={'classes','policies','gain_loss','quantities','rollforward','harvest','valuation','restrictions','commitments','risk'} if fw in {'IFRS','AASB'} else {'classes','policies','gain_loss','valuation','rollforward'}
    requirements=[dict(id=k,supported=True,evidence_memo='Synthetic actual current '+k+' disclosure proof') for k in sorted(keys)]
    document(c,'requirements',requirements)
    c['disclosures']=row(c,'agriculture-disclosures',requirements_memo='Independently qualified actual framework requirements',checked_on=c['execution_date'],scope_memo='2026 bounded case, no universal checklist',requirements_doc='requirements',requirements=requirements,requirement_inventory=[r['id'] for r in requirements],closing_carrying_value='210',pnl_measurement_gain='70',harvest_entry='70',presentation='asset_and_profit_or_loss')
    return refresh(sources(disclosure_support(c)))

def ready(fw='IFRS',c=None,release=False):
    c=copy.deepcopy(c if c is not None else case(fw))
    if release:refresh(c)
    claims,docs=canonical_knowledge(PACKAGES[PACKAGE][1],c['framework'],package=PACKAGE)
    c['knowledge_review']=dict(reviewer='Synthetic independent Agriculture knowledge reviewer',claim_ids=[x['claim_id'] for x in claims],documents=docs,applied_claim_ids=[x['claim_id'] for x in claims],selection_memo='Synthetic current bounded framework agricultural decisions with excluded exception/dependency awareness',public_caveats=['Qualified current Agriculture valuation and operative-period evidence required. Post-harvest inventory and grants require separate owners.'])
    c['reviewer_signoff']=dict(reviewer='Synthetic independent exact Agriculture case reviewer',approved=True,case_fingerprint=case_fingerprint(c))
    return c
