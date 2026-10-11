"""Durable investigation metadata in the existing native Case checkpoint.

No approval, accounting calculation method or second Case lifecycle. Numeric
movement observations explain evidence requests; native owners decide economics.
"""
import copy
from dataclasses import fields
from decimal import Decimal
from local_cao.context import identity
from orchestration.runtime import CAO
from orchestration.runtime_governance import attach
from orchestration.intake.sources import fingerprint,canonical,RawSource
from orchestration.planning import FACT_ADAPTERS
from orchestration.intake import Intake,FixturePlanner,StructuredProposal,ReviewedInputPack,Binding,PopulationBinding,DocumentBinding,TextAssertion
from interfaces.public_output import public_record
from .context import resolve
from .documents import ingest
from .model import Boundary,validate

OPS={'investigate','document','continue_investigation','investigation','correct_investigation','rework_investigation'}
REVENUE_FIELDS={'performance_obligations':'Identify distinct promised goods/services and any combined obligation.',
    'transaction_price':'Confirm fixed price and variable, refund or termination terms.',
    'satisfaction':'Provide delivery/acceptance dates and evidence of satisfaction for this period.'}


def safe(text):
    public_record({'guidance':text},route='tool_output');return text


def request(state,key,needed,why,source_fields=(),role=None):
    owner=FACT_ADAPTERS[state['family']][0]
    r=dict(id='request-'+fingerprint([state['case_id'],key]),key=key,needed=safe(needed),why=safe(why),
        owner=owner,scope_id=state['snapshot']['scope']['entity'],
        period=[state['snapshot']['scope']['period_start'],state['snapshot']['scope']['reporting_period']],
        source_status='missing_or_unqualified',blocking=True,source_fields=list(source_fields),role=role,status='OPEN')
    prior=next((x for x in state['requests'] if x['id']==r['id']),None)
    if prior is None:state['requests'].append(r)
    else:prior['status']='OPEN'


def active_documents(state):
    return [d for d in state['documents'] if d['id']+':'+d['version'] not in {x.get('supersedes') for x in state['documents']}]


def money(v):
    if type(v) not in (str,int,float) or len(str(v))>80:raise ValueError('Explicit decimal amount')
    n=Decimal(str(v))
    if not n.is_finite():raise ValueError('Nonfinite amount')
    return n


def movement(state, docs):
    roles={}
    for d in docs:
        if d['role'] in roles:raise ValueError('Ambiguous reconciliation role; explicitly supersede old version')
        roles[d['role']]=d
    for role in ('reconciliation_current','reconciliation_comparative','movements'):
        if role not in roles:
            request(state,role,'Supply '+role.replace('_',' ')+' with complete populations and record identities.',
                'Compare current and previous balances and trace movements to transactions.',role=role)
    if not all(r in roles for r in ('reconciliation_current','reconciliation_comparative','movements')):return
    def rows(role,columns):
        d=roles[role]
        if d['warnings'] or len(d['tables'])!=1:raise ValueError('Population completeness or table ambiguity unresolved')
        r=d['tables'][0]['rows']
        if not r or any(not columns<=set(x) for x in r) or len({x['record_id'] for x in r})!=len(r):raise ValueError('Movement schema/population')
        if any(not isinstance(x['record_id'],str) or not x['record_id'] for x in r):raise ValueError('Record identities')
        if 'control_total' not in d['metadata']:raise ValueError('Independent control total missing')
        if sum(money(x['closing']) for x in r)!=money(d['metadata']['control_total']):raise ValueError('Control total mismatch')
        return r
    try:
        current=rows('reconciliation_current',{'record_id','closing'})
        prior=rows('reconciliation_comparative',{'record_id','closing'})
        movements=rows('movements',{'record_id','opening','additions','consumption','closing','invoice_ref'})
        c={x['record_id']:money(x['closing']) for x in current};p={x['record_id']:money(x['closing']) for x in prior}
        m={x['record_id']:x for x in movements}
        if set(c)!=set(m) or set(p)-set(c):raise ValueError('Incomplete comparative/current movements')
        threshold=state['snapshot']['values'].get('investigation_threshold')
        if threshold is None or threshold=='UNKNOWN':
            request(state,'threshold','Confirm an investigation threshold and its currency.','Unknown threshold cannot silently become zero.');return
        threshold=money(threshold);analysis=[]
        for key,row in m.items():
            opening=money(row['opening']);add=money(row['additions']);use=money(row['consumption']);closing=money(row['closing'])
            if opening!=p.get(key,Decimal(0)) or closing!=c[key]:raise ValueError('Comparative/reconciliation contradiction')
            residual=closing-opening-add+use;increase=closing-opening
            analysis.append(dict(record_id=key,increase=str(increase),residual=str(residual),invoice_ref=row['invoice_ref'],
                source_ref=roles['movements']['id']+':'+roles['movements']['version']))
            if residual or abs(increase)>threshold:
                ref=row['invoice_ref']
                if not isinstance(ref,str) or not ref.strip():raise ValueError('Anomalous transaction missing supporting reference')
                request(state,'support-'+fingerprint([key,ref]),'Provide invoice/agreement '+ref+' supporting movement '+key+'.',
                    'Observed increase '+str(increase)+'; reconciliation residual '+str(residual)+'. Confirm service dates and allocation.',role='invoice')
        state['calculations']=[dict(kind='OBSERVATION_ONLY',current_total=str(sum(c.values())),prior_total=str(sum(p.values())),
            increase=str(sum(c.values())-sum(p.values())),transactions=analysis)]
    except (ValueError,ArithmeticError):
        request(state,'population_conflict','Resolve incomplete populations, control totals or contradictory movement/reconciliation amounts.',
            'Arithmetic cannot support an accounting conclusion until the exact populations reconcile.')
        state['conflicts'].append('reconciliation_population')


def examine(state, boundary, supplied=None):
    state['calculations']=[];state['conflicts']=list(state['snapshot']['conflicts'])
    claims={}
    for inference in state['inferences']:
        for c in inference['output']['claims']:
            claims.setdefault(c['key'],set()).add(canonical(c['value']))
    state['conflicts'].extend('inferred-'+k for k,v in claims.items() if len(v)>1)
    for r in state['requests']:r['status']='HISTORICAL'
    docs=active_documents(state)
    for role in {d['role'] for d in docs}:
        if sum(d['role']==role for d in docs)>1:
            state['conflicts'].append('ambiguous-'+role)
    # Any unresolved context conflict blocks accounting, preserving both versions.
    for conflict in state['conflicts']:
        request(state,'context-'+conflict,'Resolve context alternatives for '+conflict+'.','Conflicting scoped context cannot authorize accounting.')
    if state['family']=='customer_contract':
        if not any(d['role']=='contract' for d in docs):
            request(state,'contract','Provide the signed customer contract including schedules and amendments.','Identify promises, pricing, enforceability and recognition terms.',role='contract')
        else:
            for key,why in REVENUE_FIELDS.items():
                request(state,key,why,'Contract observations require explicit accounting qualification for '+key+'.',role='delivery' if key=='satisfaction' else 'contract')
    elif state['family']=='reconciliation':movement(state,docs)
    else:
        owner,keys=FACT_ADAPTERS[state['family']]
        request(state,'owner_evidence','Supply the '+owner+' reviewed input contract: '+', '.join(keys)+'.','Native owner requires source-qualified workpapers.')
    fields={k:v for d in docs for k,v in d['extraction']['fields'].items()}
    inference=validate(supplied,fields) if supplied is not None else boundary.infer(state['objective'],state['snapshot'],docs)
    if inference:
        if inference['family']!=state['family']:raise ValueError('Objective owner changed during continuation')
        # Semantic claims remain inferred, even with genuine source pointers.
        state['inferences'].append(dict(input_hash=fingerprint([state['objective'],state['snapshot']['snapshot_id'],[d['extraction_sha256'] for d in docs]]),output=inference,authority='INFERRED'))
        # Contradictory model interpretations do not establish contradictory source truth,
        # but block reliance until qualified by a reviewer.
        for c in inference['claims']:
            alternatives=[x for i in state['inferences'][:-1] for x in i['output']['claims'] if x['key']==c['key'] and canonical(x['value'])!=canonical(c['value'])]
            if alternatives:state['conflicts'].append('inferred-'+c['key'])
        for q in inference['questions']:request(state,'model-'+q['key'],q['needed'],q['why'],q['source_fields'])
    request(state,'qualification','Provide an independently reviewed native intake pack binding this exact document population and accounting facts.',
        'Extracted text, movement observations and model claims are not reviewed accounting evidence.')
    state['conflicts']=sorted(set(state['conflicts']))


def pack_from_record(raw):
    allowed={f.name for f in fields(ReviewedInputPack)}
    if not isinstance(raw,dict) or set(raw)-allowed:raise ValueError('Native reviewed pack schema')
    r=copy.deepcopy(raw)
    native_scope=r.get('request',{}).get('scope',{})
    if native_scope.get('period_registry'):
        from orchestration.periods import PeriodRegistry
        native_scope['period_registry']=PeriodRegistry.from_record(native_scope['period_registry']).record()
    for key,cls in [('bindings',Binding),('populations',PopulationBinding),('documents',DocumentBinding),('text_assertions',TextAssertion)]:
        r[key]=[cls(**dict(v,path=tuple(v['path']))) for v in r.get(key,[])]
    r['scoped_packs']=[pack_from_record(x) for x in r.get('scoped_packs',[])]
    return ReviewedInputPack(**r)


def prepared_intake(state,evidence,scope):
    if not isinstance(evidence,dict) or set(evidence)-{'proposal','pack','sources'} or not {'proposal','pack'}<=set(evidence):raise ValueError('Source-qualified intake required')
    raws=[RawSource(**d['raw_source']) for d in active_documents(state)]
    # Supporting reviewed input snapshots are inert native source envelopes.
    for r in evidence.get('sources',[]):
        raw=RawSource(**r)
        if raw.id in {x.id for x in raws}:raise ValueError('Source substitution')
        raws.append(raw)
    proposal=StructuredProposal.from_record(evidence['proposal'])
    import json
    scope=json.loads(canonical(scope))
    engine=Intake(FixturePlanner(proposal));prepared=engine.prepare(state['objective'],raws,state['snapshot']['governed_records'],scope)
    if not prepared.validation.get('accepted'):raise ValueError('Invalid native intake')
    pack=pack_from_record(evidence['pack'])
    # Every ingested document must be explicitly bound by the supplied native pack;
    # arbitrary unrelated workpapers cannot stand in for the investigated contract.
    bindings=[b.source_id for b in pack.documents+pack.populations+pack.text_assertions]
    bindings.extend(ref['source_id'] for row in prepared.candidates for ref in row['lineage'])
    if not {d['raw_source']['id'] for d in active_documents(state)}<=set(bindings):raise ValueError('Investigation document population unbound')
    return engine,prepared,pack



def replacement_source(engine,prepared,pack,case,key):
    if 'governed_plan' in pack.request:
        from orchestration.intake.governed import qualify_replacement
        return qualify_replacement(engine,prepared,pack,case,key)
    # Ordinary legacy owner packs use the same native Intake validation, plus a
    # complete source snapshot. No certificate or reviewer identity is generated.
    from orchestration.execution import populations
    from orchestration.persistence.evidence import retain
    rows=list(populations(pack.request.get('facts',{})))
    if len(rows)!=1 or key not in case.graph.nodes:raise ValueError('Exact single replacement owner')
    family,source=rows[0];node=case.graph.nodes[key]
    if FACT_ADAPTERS[family][0]!=node.selected_skill or source.get('period_id')!=node.period_id or source.get('scope_id',source.get('entity'))!=node.scope_id:raise ValueError('Replacement dimensions/owner')
    if pack.request.get('case_id')!=case.cycle:raise ValueError('Replacement Case identity')
    snapshot=source.get('qualified_input_snapshot')
    if not isinstance(snapshot,dict) or set(snapshot)!={'source_id','fingerprint'}:raise ValueError('Complete reviewed source snapshot required')
    raw=prepared._inventory.raw.get(snapshot['source_id'])
    stripped={k:v for k,v in source.items() if k not in ('reviewer_signoff','source_population','qualified_scope_sources','qualified_input_snapshot')}
    if raw is None or raw.format!='json' or raw.payload!=[dict(record_id=key,reviewed_input=canonical(stripped))] or prepared._inventory.extractions[raw.id].source['fingerprint']!=snapshot['fingerprint']:raise ValueError('Replacement complete snapshot differs')
    manifest=source.get('qualified_scope_sources',[])
    if len(manifest)!=len(source.get('source_population',[])) or {x['source_id'] for x in manifest}!=set(source.get('source_population',[])) or snapshot['source_id'] not in source.get('source_population',[]):raise ValueError('Replacement full source population')
    for row in manifest:
        ex=prepared._inventory.extractions.get(row['source_id'])
        if ex is None or row!=dict(source_id=ex.source['id'],fingerprint=ex.source['fingerprint'],metadata=ex.source['metadata']):raise ValueError('Replacement source manifest differs')
    incoming=[case.governance.receipt(k) for k,e in sorted(case.governance.edges.items()) if e.consumer_node==key]
    if incoming and source.get('versioned_dependency_receipts')!=incoming:raise ValueError('Replacement stale dependency receipts')
    for r in incoming:case.governance.validate_receipt(r,key)
    qualified=engine.execute(prepared,pack).case
    if qualified is None or qualified.id!=case.id or qualified.outcome!='complete':raise ValueError('Replacement native qualification failed')
    retain(case.governance,prepared,pack)
    return copy.deepcopy(source)



def native_event(store,company,case,rev,state,event_id,fp,intent):
    staged=next((x for x in state.setdefault('native_events',[]) if x['id']==event_id),None)
    if staged is None:
        staged=dict(id=event_id,hash=fp,intent=copy.deepcopy(intent));state['native_events'].append(staged)
        rev=store.save(case,company,state['snapshot']['governed_records'],rev)
    elif staged['hash']!=fp:raise ValueError('Immutable native event')
    operations=[]
    for (key,) in store.connection.execute('SELECT operation_id FROM operations WHERE company_id=? AND case_id=?',(company,case.id)):
        record=store.operation(company,case.id,key)
        if canonical(record['intent'])==canonical(staged['intent']):operations.append(key)
    if len(operations)>1:raise ValueError('Ambiguous native operation')
    key=operations[0] if operations else store.prepare(case,company,state['snapshot']['governed_records'],rev,staged['intent'])
    store.recover(company,case.id,key)
    case,rev,_=store.load(company,case.id);state=case._investigation
    state['pending_correction']=staged['intent']['kind']=='CORRECT'
    if staged['intent']['kind']=='REWORK':
        for q in state['requests']:q['status']='QUALIFIED_BY_NATIVE_INTAKE'
    return case,rev,state


def preview(api,case,revision):
    state=case._investigation
    out=api._delivery(case,revision,'tool_output')
    if not state.get('qualified') or state.get('pending_correction'):
        out.update(execution_state='blocked',currentness='STALE' if state.get('pending_correction') else 'NOT_EXECUTED')
        out['public_result']=public_record(dict(status='blocked',guidance='Investigation requires qualified evidence.',
            open_items=[r['needed'] for r in state['requests'] if r['status']=='OPEN']), route='tool_output')
    out['investigation']=dict(context_snapshot_id=state['snapshot']['snapshot_id'],
        requests=copy.deepcopy(state['requests']),documents=[dict(id=d['id'],version=d['version'],role=d['role'],qualification=d['qualification']) for d in state['documents']],
        conflicts=list(state['conflicts']),round=state['round'],accounting_qualified=state.get('qualified',False),pending_correction=state.get('pending_correction',False))
    # Observational calculations remain separate from public accounting calculations.
    out['investigation']['observations']=copy.deepcopy(state['calculations'])
    # Operational opaque references stay outside accounting public_result.
    for calc in state['calculations']:
        for row in calc.get('transactions',[]):
            safe(row['record_id']);safe(row['invoice_ref'])
    return out


def handle(api,r,company,config):
    from local_cao.adapter import immutable,canonical as wire,Failure
    from orchestration.periods import compatibility_period
    from orchestration.cases import case_identity
    import hashlib
    op=r['operation'];boundary=Boundary(getattr(api,'model_provider',None))
    if op=='investigate':
        objective=r.get('objective');cycle=identity(r.get('request_id'))
        if not isinstance(objective,str) or not objective.strip() or len(objective)>4000:raise ValueError('Objective required')
        safe(objective)
        snapshot=resolve(config,r.get('context'),company=company)
        family=r.get('target_family')
        inference=None
        if family is None:
            inference=validate(r['interpretation']) if 'interpretation' in r else boundary.infer(objective,snapshot,[])
            if inference is None:raise ValueError('Structured interpretation/model provider required')
            family=inference['family']
        if family not in FACT_ADAPTERS:raise ValueError('Unsupported family')
        s=snapshot['scope'];p=compatibility_period(s);cid=case_identity(s['entity'],p.period_id,objective,cycle)
        d=dict(company_id=company,case_id=cid,target_family=family,native_request=dict(case_id=cycle,objective=objective,scope=s,company_context=[],facts={}),context_snapshot=snapshot)
        folder=api._path('requests');folder.mkdir(mode=0o700,exist_ok=True)
        immutable(folder/(cycle+'.json'),d)
        submissions=api._path('submissions/'+hashlib.sha256(cid.encode()).hexdigest());submissions.mkdir(mode=0o700,parents=True,exist_ok=True)
        with api._store() as store:
            if store._head(company,cid):case,rev,_=store.load(company,cid);return preview(api,case,rev)
            native=d['native_request'];case=CAO().run(native)
            if not hasattr(case,'governance'):attach(case,case.graph,s,{},native)
            rev=0
            state=dict(contract='cao-investigation/1',case_id=cid,objective=objective,family=family,
                snapshot=snapshot,documents=[],requests=[],calculations=[],conflicts=[],inferences=[],round=0,events=[],qualified=False,pending_correction=False)
            case._investigation=state;examine(state,boundary,inference or r.get('interpretation'))
            rev=store.save(case,company,[],rev)
            state['snapshot']=resolve(config,r.get('context'),store.memory(),company,case)
            examine(state,boundary,inference or r.get('interpretation'))
            rev=store.save(case,company,[],rev)
            return preview(api,case,rev)
    d,_=api._request(r.get('case_id'),config)
    if 'context_snapshot' not in d:raise ValueError('Not a Build 3 investigation')
    with api._store() as store:
        case,rev,_=store.load(company,d['case_id']);state=case._investigation
        if op in {'investigation','status','questions','resume','result'}:return preview(api,case,rev)
        event_id=identity(r.get('event_id')) if op!='execute' else None
        if event_id:
            prior=next((x for x in state['events'] if x['id']==event_id),None)
            fp=fingerprint(r)
            if prior:
                if prior['hash']!=fp:raise ValueError('Immutable investigation event')
                return preview(api,case,rev)
            if len(state['events'])>=64:raise ValueError('Investigation round limit')
        if op=='document':
            observation=ingest(r['document'],company,state['snapshot']['scope'])
            old=next((x for x in state['documents'] if (x['id'],x['version'])==(observation['id'],observation['version'])),None)
            if old:
                if fingerprint(old)!=fingerprint(observation):raise ValueError('Document version changed')
            else:
                previous=[x for x in active_documents(state) if x['id']==observation['id']]
                if previous and observation.get('supersedes')!=previous[0]['id']+':'+previous[0]['version']:raise ValueError('Explicit reciprocal document successor required')
                if observation.get('supersedes') and not any(x['id']==observation['id'] and x['role']==observation['role'] and x['id']+':'+x['version']==observation['supersedes'] for x in active_documents(state)):raise ValueError('Unknown/mismatched document predecessor')
                state['documents'].append(observation)
                if case.governance.versions.active:state['pending_correction']=True
            examine(state,boundary,r.get('interpretation'))
        elif op=='continue_investigation':
            examine(state,boundary,r.get('interpretation'))
        elif op=='execute':
            if state.get('qualified') and not state.get('pending_correction'):return preview(api,case,rev)
            if case.governance.versions.active:raise ValueError('Native correction/rework required')
            if state['conflicts']:raise ValueError('Resolve investigation conflicts')
            evidence=api.read_json('submissions/'+hashlib.sha256(d['case_id'].encode()).hexdigest()+'/intake.json')
            engine,prepared,pack=prepared_intake(state,evidence,state['snapshot']['scope'])
            if pack.request.get('case_id')!=d['native_request']['case_id']:raise ValueError('Native Case identity binding')
            result=engine.execute(prepared,pack);new=result.case
            if new is None or new.id!=case.id or not hasattr(new,'governance'):raise ValueError('Native investigation execution unavailable')
            if not any(n.selected_skill==FACT_ADAPTERS[state['family']][0] for n in new.graph.nodes.values()):raise ValueError('Target owner not invoked')
            new._investigation=state;case=new
            state['qualified']=True;state['pending_correction']=False
            for q in state['requests']:q['status']='QUALIFIED_BY_NATIVE_INTAKE'
        elif op in {'correct_investigation','rework_investigation'}:
            if not state['qualified'] or state['conflicts']:raise ValueError('Qualified original/consistent replacement required')
            staged=next((x for x in state.get('native_events',[]) if x['id']==event_id),None)
            if staged:
                intent=staged['intent']
            elif op=='rework_investigation' and not case.governance.rework_history[-1]['execution_order']:
                intent=dict(kind='REWORK',plan=case.governance.rework_history[-1],reviewed_sources={})
            else:
                engine,prepared,pack=prepared_intake(state,r['evidence'],case.governance.context)
                if op=='correct_investigation':
                    key=r['node_id'];source=replacement_source(engine,prepared,pack,case,key)
                    intent=dict(kind='CORRECT',node_id=key,source=source,reason=r['reason'])
                else:
                    plan=case.governance.rework_history[-1];sources={}
                    for key in plan['execution_order']:sources[key]=replacement_source(engine,prepared,pack,case,key)
                    intent=dict(kind='REWORK',plan=plan,reviewed_sources=sources)
            case,rev,state=native_event(store,company,case,rev,state,event_id,fp,intent)
        else:raise ValueError('Investigation operation')
        if event_id:
            state['events'].append(dict(id=event_id,hash=fp,operation=op));state['round']+=1
        if len(wire(state).encode())>1_500_000:raise ValueError('Aggregate investigation limit')
        rev=store.save(case,company,state['snapshot']['governed_records'],rev)
        return preview(api,case,rev)
