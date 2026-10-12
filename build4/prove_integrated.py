"""Deterministic unfamiliar synthetic proof; approvals explicitly test-only.

CLI calls use fresh Python processes and the production local JSON interface.
Native execution/correction use independent synthetic reviewed packs, never
production adapter-created certificates. Output includes retained source bytes.
"""
import base64,copy,hashlib,json,os,subprocess,sys,tempfile
from dataclasses import asdict
from pathlib import Path
from local_cao.adapter import ExecutionInterface
from build4.fixtures import setup,wire,doc,OBJECTIVE,COMPANY,revenue_evidence
from intelligence.context import resolve
from local_cao.context import parse
from build4.fixtures import context
ROOT=Path(__file__).resolve().parents[1]

def native_receipts(case):
 """Read retained native accounting evidence, never synthesize receipts."""
 e=case.governance
 return copy.deepcopy(dict(versions=e.versions.record(),source_snapshots=e.versions.source_snapshots,dependency_receipts=e.receipts,dependencies={k:asdict(v) for k,v in e.edges.items()},rework_history=e.rework_history,active_versions=e.versions.active,version_history=e.versions.history,graph_history=e.graph.history))

def proof():
 with tempfile.TemporaryDirectory() as tmp:
  api=ExecutionInterface(tmp);setup(api)
  def call(op,**kw):
   r=subprocess.run([sys.executable,'-m','local_cao','--workspace',tmp],input=json.dumps(wire(op,**kw)),text=True,capture_output=True,cwd=ROOT,timeout=90)
   try:v=json.loads(r.stdout)
   except Exception:raise AssertionError((r.returncode,r.stdout,r.stderr))
   assert v['ok'],v
   return v
  start=call('investigate',request_id='boreal-build4',objective=OBJECTIVE,interpretation=dict(family='customer_contract',claims=[],questions=[]));cid=start['case_id']
  with api._store() as st:c,_,_=st.load(COMPANY,cid);scope=c._investigation['snapshot']['scope']
  first=doc(scope);observed=call('document',case_id=cid,event_id='contract',document=first)
  with api._store() as st:c,_,_=st.load(COMPANY,cid);ref=next(iter(c._investigation['documents'][0]['extraction']['fields']))
  targeted=call('continue_investigation',case_id=cid,event_id='terms',interpretation=dict(family='customer_contract',claims=[dict(key='price',value='42000',source_fields=[ref],uncertainty='unreviewed')],questions=[dict(key='refund',needed='What warranty remedies and refunds are enforceable under the executed Boreal agreement?',why='The supplied contract does not quantify warranty remedies; variable consideration requires independent review.',source_fields=[ref])]))
  restored=call('resume',case_id=cid);assert targeted['investigation']==restored['investigation']
  original_inputs=revenue_evidence(api,cid)
  call('submit',case_id=cid,evidence=original_inputs);original=call('execute',case_id=cid);assert original['execution_state']=='complete';assert '31920' in json.dumps(original['public_result'])
  interrupted=subprocess.Popen([sys.executable,'-c',"import json,sys;from local_cao.adapter import ExecutionInterface;api=ExecutionInterface(sys.argv[1]);print(json.dumps(api.call(json.loads(sys.argv[2]))),flush=True);sys.stdin.read()",tmp,json.dumps(wire('resume',case_id=cid))],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
  interrupted_receipt=json.loads(interrupted.stdout.readline());assert interrupted_receipt['public_result']==original['public_result']
  interrupted.kill();interrupted.communicate(timeout=20)
  restart=call('resume',case_id=cid);assert restart['public_result']==original['public_result'] and restart['checkpoint_revision']==original['checkpoint_revision']
  repeat=call('execute',case_id=cid);assert repeat['checkpoint_revision']==original['checkpoint_revision']
  with api._store() as st:c,_,_=st.load(COMPANY,cid);node=next(iter(c.graph.nodes));before=copy.deepcopy(c.governance.versions.record());original_native=native_receipts(c)
  second=doc(scope,text='Fixed price EUR 45000. Corrected executed cold-chain agreement.',version='v2',supersedes='boreal-executed-agreement:v1')
  changed=call('document',case_id=cid,event_id='replacement',document=second);assert changed['currentness']=='STALE'
  evidence=revenue_evidence(api,cid,'45000',True)
  correction=call('correct_investigation',case_id=cid,event_id='correction',node_id=node,reason='Corrected signed agreement',evidence=evidence)
  reworked=call('rework_investigation',case_id=cid,event_id='rework',evidence={});assert reworked['execution_state']=='complete';assert '34200' in json.dumps(reworked['public_result'])
  assert call('correct_investigation',case_id=cid,event_id='correction',node_id=node,reason='Corrected signed agreement',evidence=evidence)['checkpoint_revision']==reworked['checkpoint_revision']
  with api._store() as st:c,rev,_=st.load(COMPANY,cid);revenue_state=copy.deepcopy(c._investigation);after=c.governance.versions.record();final_native=native_receipts(c);ops=st.connection.execute('SELECT count(*) FROM operations WHERE company_id=? AND case_id=?',(COMPANY,cid)).fetchone()[0]
  assert ops==2
  (Path(tmp)/'company-context.md').write_text(context().replace('investigation_threshold: UNKNOWN','investigation_threshold: 1500'))
  p=call('investigate',request_id='cold-chain-prepayments-build4',objective='Why did prepaid cold-chain compliance coverage increase materially in 2026?',target_family='reconciliation');pcid=p['case_id']
  data=[('reconciliation_comparative','record_id,closing\ncold-chain-compliance,2400\nlab-accreditation,600\n','3000',True),('reconciliation_current','record_id,closing\ncold-chain-compliance,18300\nlab-accreditation,450\n','18750',False),('movements','record_id,opening,additions,consumption,closing,invoice_ref\ncold-chain-compliance,2400,18000,2000,18300,BC-20481\nlab-accreditation,600,0,150,450,ACC-339\n','18750',False)]
  for i,(role,text,total,prior) in enumerate(data):
   d=doc(scope,text,format='csv',role=role,id=role,row_count=2,complete_population=True,control_total=total)
   if prior:d['metadata']['period']=['2025-01-01','2025-12-31']
   movement=call('document',case_id=pcid,event_id='schedule-'+str(i),document=d)
  assert movement['investigation']['observations'][0]['increase']=='15750';assert movement['investigation']['observations'][0]['transactions'][0]['residual']=='-100';assert 'BC-20481' in json.dumps(movement['investigation']['requests']);assert movement['execution_state']=='blocked'
  invoice=call('document',case_id=pcid,event_id='invoice',document=doc(scope,'Invoice BC-20481 EUR 18000; cold-chain compliance coverage 24 months. Allocation review absent.',format='text',role='invoice',id='BC-20481'))
  assert invoice['execution_state']=='blocked';assert call('resume',case_id=pcid)['investigation']==invoice['investigation']
  denied=api.call(dict(wire('resume',case_id=cid),company_id='other-company'));assert not denied['ok']
  items=[]
  for entity,fw,cur in [('UK-SUB','UK_GAAP','GBP'),('GROUP','IFRS','EUR')]:
   for key,val in [('framework',fw),('jurisdiction','GB'),('functional_currency',cur),('presentation_currency',cur),('calendar_id','FISCAL-UK')]:items.append(dict(id=entity+'-'+key,key=key,value=val,entity_id=entity,effective_from='2026-01-01',effective_to='2026-12-31',source_state='approved',source_ref='asserted-onboarding',source_version='v1',framework=fw))
  items.append(dict(id='ifrs-only-uk-currency',key='functional_currency',value='USD',entity_id='UK-SUB',effective_from='2026-01-01',effective_to='2026-12-31',source_state='approved',source_ref='foreign-framework-onboarding',source_version='v1',framework='IFRS'))
  items.append(dict(id='group-scope',key='scope_type',value='GROUP',entity_id='GROUP',effective_from='2026-01-01',effective_to='2026-12-31',source_state='user_asserted',source_ref='asserted-onboarding',source_version='v1'))
  group=call('investigate',request_id='group-proof',objective='Investigate the group reconciliation',target_family='reconciliation',context=dict(version='v1',company_id=COMPANY,items=items,selection=dict(entity_id='GROUP',period_start='2026-01-01',period_end='2026-12-31')))
  with api._store() as st:
   gc,_,_=st.load(COMPANY,group['case_id']);group_snapshot=copy.deepcopy(gc._investigation['snapshot']);group_case_type=gc.case_type
  assert group_case_type=='GROUP_CASE' and group_snapshot['scope']['scopes'][0]['scope_type']=='GROUP' and group_snapshot['scope']['scopes'][0]['legal_entity_id'] is None
  assert call('resume',case_id=group['case_id'])['investigation']==group['investigation']
  uk=resolve(parse(context()),dict(version='v1',company_id=COMPANY,items=items,selection=dict(entity_id='UK-SUB',period_start='2026-01-01',period_end='2026-12-31')));assert uk['scope']['framework']=='UK_GAAP' and uk['scope']['currency']=='GBP';assert not uk['governed_records'];assert not uk['conflicts'];assert not any(x.get('id')=='ifrs-only-uk-currency' for x in uk['items']);assert any(x.get('id')=='ifrs-only-uk-currency' for x in uk['history'])
  uk_case=call('investigate',request_id='uk-framework-qualified',objective='Review UK laboratory prepayments',target_family='reconciliation',context=dict(version='v1',company_id=COMPANY,items=items,selection=dict(entity_id='UK-SUB',period_start='2026-01-01',period_end='2026-12-31')))
  wrong_dims=copy.deepcopy(items)
  next(x for x in wrong_dims if x['id']=='UK-SUB-calendar_id')['framework']='IFRS'
  invalid_dimensions=api.call(wire('investigate',request_id='uk-wrong-framework-calendar',objective='Review UK laboratory prepayments',target_family='reconciliation',context=dict(version='v1',company_id=COMPANY,items=wrong_dims,selection=dict(entity_id='UK-SUB',period_start='2026-01-01',period_end='2026-12-31'))))
  assert not invalid_dimensions['ok']
  # Same production owner, distinct entity and period identities. Every request
  # crosses the local JSON CLI; the SQLite reads below observe retained receipts.
  repeated=[]
  for entity,fw,cur,start_date,end_date in [('NL-LAB','IFRS','EUR','2026-01-01','2026-12-31'),('US-LAB','US_GAAP','USD','2026-01-01','2026-12-31'),('NL-LAB','IFRS','EUR','2027-01-01','2027-12-31')]:
   dims=[dict(id=entity+'-'+key+'-'+start_date,key=key,value=value,entity_id=entity,effective_from=start_date,effective_to=end_date,source_state='user_asserted',source_ref='company-onboarding',source_version='v1',framework=fw) for key,value in [('framework',fw),('jurisdiction','US' if fw=='US_GAAP' else 'NL'),('functional_currency',cur),('presentation_currency','EUR' if cur=='USD' else cur),('calendar_id',entity+'-CAL')]]
   sr=call('investigate',request_id=entity+'-'+start_date,objective=OBJECTIVE,interpretation=dict(family='customer_contract',claims=[],questions=[]),context=dict(version='v1',company_id=COMPANY,items=dims,selection=dict(entity_id=entity,period_start=start_date,period_end=end_date)))
   rcid=sr['case_id']
   with api._store() as st:sc,_,_=st.load(COMPANY,rcid);rs=sc._investigation['snapshot']['scope']
   source=doc(rs,text='Executed distinct cold-chain arrangement. Fixed price '+cur+' 42000. Equipment accepted; service progress independently measured.',id=entity+'-agreement-'+start_date)
   observed_owner=call('document',case_id=rcid,event_id='signed',document=source)
   reviewed_inputs=revenue_evidence(api,rcid)
   call('submit',case_id=rcid,evidence=reviewed_inputs)
   er=call('execute',case_id=rcid);assert er['execution_state']=='complete',er
   with api._store() as st:
    sc,_,_=st.load(COMPANY,rcid);receipt=dict(case_id=rcid,scope=rs,node_ids=list(sc.graph.nodes),versions=sc.governance.versions.record())
   receipt['native_receipts']=native_receipts(sc);receipt['reviewed_inputs']=reviewed_inputs;receipt['document_envelope']=source;receipt['response']=er;receipt['source_sha256']=hashlib.sha256(base64.b64decode(source['content_base64'])).hexdigest();repeated.append(receipt)
   assert call('resume',case_id=rcid)['public_result']==er['public_result']
  assert len({x['case_id'] for x in repeated})==3
  conflict_items=[dict(id=k,key='policies',value=v,entity_id=scope['entity'],effective_from='2026-01-01',effective_to=None,source_state='approved',source_ref='asserted-policy',source_version='v1') for k,v in [('a','Recognize immediately'),('b','Defer until delivery')]]
  conflict=call('investigate',request_id='conflict-proof',objective='Determine conflicting policy treatment',target_family='customer_contract',context=dict(version='v1',company_id=COMPANY,items=conflict_items));assert conflict['execution_state']=='blocked' and 'policies' in conflict['investigation']['conflicts']
  with api._store() as st:pc,_,_=st.load(COMPANY,pcid);prepay_state=copy.deepcopy(pc._investigation)
  def retained(state):
   out=copy.deepcopy(state)
   out['documents']=[{k:d[k] for k in ('id','version','role','format','metadata','supersedes','original_sha256','original_bytes','extraction_sha256','original_content_base64','warnings','qualification','tables','blocks') if k in d} for d in state['documents']]
   out.pop('native_events',None)
   return out
  def versions(rows):return [dict(version_id=x['version_id'],state=x['state'],superseded_by=x.get('superseded_by'),immutable_sha256=hashlib.sha256(json.dumps({k:v for k,v in x.items() if k not in ('state','superseded_by')},sort_keys=True,separators=(',',':')).encode()).hexdigest()) for x in rows]
  return dict(contract='cao-build4-proof/1',expected_economics=dict(original=dict(price='42000',equipment_ssp='30000',service_ssp='20000',service_progress='0.40',equipment_revenue='25200',service_revenue='6720',total_revenue='31920'),corrected=dict(price='45000',equipment_revenue='27000',service_revenue='7200',total_revenue='34200'),prepayments=dict(opening='3000',closing='18750',increase='15750',unexplained_residual='-100',allocation_qualified=False)),synthetic_review_only=True,live_model_evaluation=False,fresh_process_each_operation=True,interruption=dict(process_killed_after_durable_checkpoint=True,restoration=restart,duplicate_economics=False),revenue=dict(case_id=cid,original_reviewed_inputs=original_inputs,corrected_reviewed_inputs=evidence,original_native_receipts=original_native,final_native_receipts=final_native,rework_boundary='One corrected owner; zero downstream dependents. Separate native recovery regressions prove dependency selective rework.',start=start,observed=observed,targeted=targeted,original=original,changed=changed,corrected=correction,reworked=reworked,checkpoint_revision=rev,native_operations=ops,original_versions=versions(before),final_versions=versions(after),state=retained(revenue_state)),prepayments=dict(case_id=pcid,start=p,movement=movement,invoice=invoice,state=retained(prepay_state),outcome='BLOCKED: no independently reviewed native accounting pack'),multi_entity=uk,qualified_uk_case=uk_case,wrong_framework_dimensions=invalid_dimensions,repeated_entity_period_owners=repeated,multi_entity_group=dict(case_type=group_case_type,snapshot=group_snapshot,response=group),conflict=conflict,isolation=denied)
if __name__=='__main__':print(json.dumps(proof(),sort_keys=True,indent=2))
