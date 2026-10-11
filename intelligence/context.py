"""Immutable Case-specific view; CompanyMemory remains the only memory authority."""
import copy
import json
from datetime import date
from decimal import Decimal
from local_cao.context import scope, identity
from orchestration.intake.sources import bounded, fingerprint, canonical

VERSION = 'cao-context/1'
FIELDS = {'framework','jurisdiction','functional_currency','presentation_currency','calendar_id',
          'materiality','investigation_threshold','business_model','revenue_model','policies',
          'historical_positions','responsibilities','locations','fiscal_calendar','period_start','period_end'}


def resolve(config, structured=None, memory=None, company=None, qualification_case=None):
    base = scope(config); company = company or base['company_id']
    if company != base['company_id']: raise ValueError('Context company mismatch')
    entries=[]
    # Markdown values are assertions even when the prose labels them APPROVED.
    for section, fields in config.items():
        for key,value in fields.items():
            entries.append(dict(key=key,value=None if value in ('UNKNOWN','TODO','') else value,
                entity_id=base['entity'],authority='user_asserted',source='markdown:'+section,
                version=fingerprint(config),effective_from=base['period_start'],effective_to=base['reporting_period']))
    if structured is not None:
        bounded(structured)
        if not isinstance(structured,dict) or set(structured)-{'version','company_id','items','selection'} or not {'version','company_id','items'}<=set(structured):
            raise ValueError('Versioned context envelope required')
        identity(structured['version'])
        if structured['company_id']!=company or not isinstance(structured['items'],list): raise ValueError('Context namespace mismatch')
        ids=set()
        for raw in structured['items']:
            required={'id','key','value','entity_id','effective_from','effective_to','source_state','source_ref','source_version'}
            if not isinstance(raw,dict) or set(raw)-required-{'framework','supersedes'} or required-set(raw): raise ValueError('Context item schema')
            r=copy.deepcopy(raw); identity(r['id']);identity(r['entity_id']);identity(r['source_version'])
            if r['id'] in ids or r['key'] not in FIELDS: raise ValueError('Duplicate/unknown context item')
            ids.add(r['id'])
            if r['source_state'] not in {'unknown','inferred','user_asserted','document_backed','proposed','approved','superseded','retracted'}: raise ValueError('Context state')
            if not isinstance(r['source_ref'],str) or not r['source_ref']: raise ValueError('Context source reference')
            for k in ('effective_from','effective_to'):
                if r[k] is not None and (not isinstance(r[k],str) or date.fromisoformat(r[k]).isoformat()!=r[k]): raise ValueError('Context dates')
            if r['effective_from'] and r['effective_to'] and r['effective_from']>r['effective_to']: raise ValueError('Context interval')
            r['authority']='inferred' if r['source_state']=='inferred' else 'user_asserted'
            # A reference alone does not establish document retrieval or qualification.
            if r['source_state']=='document_backed':r['authority']='document_reference_unqualified'
            r['version']=structured['version'];entries.append(r)
        # Arbitrary latest-edit supersession cannot erase conflicting policies.
    values={};conflicts=[];unknown=[];selected=[]
    selected_scope=base['entity']
    if structured and structured.get('selection'):
        selection=structured['selection']
        if not isinstance(selection,dict) or set(selection)!={'entity_id','period_start','period_end'}:raise ValueError('Explicit selection schema')
        identity(selection['entity_id']);selected_scope=selection['entity_id']
        start,end=selection['period_start'],selection['period_end']
        if date.fromisoformat(start)>date.fromisoformat(end):raise ValueError('Selected period')
        if selected_scope!=base['entity']:
            exact={}
            for e in entries:
                if e['entity_id']==selected_scope and e.get('source_state') not in {'inferred','superseded','retracted','unknown'} and e['effective_from'] and e['effective_from']<=start and (not e['effective_to'] or e['effective_to']>=end):
                    if e['key'] in exact and canonical(exact[e['key']])!=canonical(e['value']):raise ValueError('Conflicting execution selection')
                    exact[e['key']]=e['value']
            required={'framework','jurisdiction','functional_currency','presentation_currency','calendar_id'}
            if not required<=set(exact):raise ValueError('Local entity dimensions required; group context is not a fallback')
            from local_cao.context import parse
            text='## company\n- company_id: '+company+'\n- legal_name: selected\n## execution\n- entity_id: '+selected_scope+'\n- period_start: '+start+'\n- period_end: '+end+'\n'+'\n'.join('- '+k+': '+str(exact[k]) for k in required)
            base=scope(parse(text))
        else:
            base['period_start']=start;base['reporting_period']=end
    aliases={'functional_currency':'functional_currency','presentation_currency':'presentation_currency','calendar_id':'reporting_calendar'}
    for e in entries:
        if e['entity_id']!=selected_scope:continue
        if e.get('framework') and e['framework']!=base['framework']:continue
        if e.get('source_state') in {'retracted','superseded'}:continue
        if not e['effective_from'] or e['effective_from']>base['period_start'] or (e['effective_to'] and e['effective_to']<base['reporting_period']):continue
        selected.append(e);key=e['key'];value=e['value']
        if value is None:unknown.append(key);continue
        if e['authority']=='inferred':continue
        if key in values and canonical(values[key])!=canonical(value):conflicts.append(key)
        else:values[key]=copy.deepcopy(value)
    governed=[];memory_refs=[];refusals=[]
    if memory is not None and qualification_case is not None:
        audit=memory.audit(company)
        subjects=sorted({(r['subject'],r['attribute']) for r in audit['company_context']})
        for subject,attribute in subjects:
            result=memory.retrieve(company,qualification_case.id,qualification_case.id,subject,attribute)
            refusals.extend(result['refused'])
            for entry in result['qualified']:
                r=entry['record'];v=r['value'];key=r['attribute']
                if key in values and canonical(values[key])!=canonical(v):conflicts.append(key)
                values[key]=copy.deepcopy(v)
                governed.append(dict(id=r['record_id'],attribute=key,value=copy.deepcopy(v),status=r['status'],
                    scope=dict(entities=[selected_scope],framework=base['framework']),
                    effective_from=r['effective_from']['value'],effective_to=r['effective_to']['value'],provenance=[r['version_id']]))
                memory_refs.append(dict(record_id=r['record_id'],version_id=r['version_id'],attribute=key,source_case=r['source']['case_id'],use='CONTEXT_ONLY'))
            if result['conflicts']:conflicts.append(attribute)
            if any(x['record']['status'] not in {'SUPERSEDED','RETRACTED'} for x in result['refused']):conflicts.append(attribute)
    for key in ('materiality','investigation_threshold'):
        if key in values and values[key] not in (None,'UNKNOWN'):
            if type(values[key]) not in (str,int,float):raise ValueError('Numeric context type')
            n=Decimal(str(values[key]))
            if not n.is_finite() or n<0:raise ValueError('Numeric context value')
    for key in conflicts:values.pop(key,None)
    if 'materiality' in values and values['materiality'] is not None:base['materiality']=str(values['materiality'])
    from orchestration.periods import compatibility_period,PeriodRegistry,FiscalCalendar
    period=compatibility_period(base)
    base['period_registry']=PeriodRegistry([FiscalCalendar(period.calendar_id,'Explicit bounded investigation calendar',None,None,('asserted-context',))],[period]).record()
    base['period_id']=period.period_id
    result=dict(contract=VERSION,company_id=company,scope=base,values=values,items=selected,
        history=entries,unknowns=sorted(set(unknown)-values.keys()),conflicts=sorted(set(conflicts)),
        governed_records=governed,memory_references=memory_refs,
        refused_memory=[dict(record_id=x['record']['record_id'],reasons=x['reasons']) for x in refusals])
    result=json.loads(canonical(result))
    result['snapshot_id']=fingerprint(result)
    return result
