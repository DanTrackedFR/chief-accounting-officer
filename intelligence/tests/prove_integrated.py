"""Deterministic unfamiliar synthetic proof; approvals explicitly test-only.

CLI calls use fresh Python processes and the production local JSON interface.
Native execution/correction use independent synthetic reviewed packs, never
production adapter-created certificates. Output includes retained source bytes.
"""
import base64,copy,hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
from local_cao.adapter import ExecutionInterface
from intelligence.tests.fixtures import setup,wire,doc,OBJECTIVE,COMPANY,revenue_evidence
from intelligence.context import resolve
from local_cao.context import parse
from local_cao.tests.test_authored import context
ROOT=Path(__file__).resolve().parents[2]

def proof():
 with tempfile.TemporaryDirectory() as tmp:
  api=ExecutionInterface(tmp);setup(api)
  def call(op,**kw):
   r=subprocess.run([sys.executable,'-m','local_cao','--workspace',tmp],input=json.dumps(wire(op,**kw)),text=True,capture_output=True,cwd=ROOT)
   try:v=json.loads(r.stdout)
   except Exception:raise AssertionError((r.returncode,r.stdout,r.stderr))
   assert v['ok'],v
   return v
  start=call('investigate',request_id='halcyon-proof',objective=OBJECTIVE,interpretation=dict(family='customer_contract',claims=[],questions=[]));cid=start['case_id']
  with api._store() as st:c,_,_=st.load(COMPANY,cid);scope=c._investigation['snapshot']['scope']
  first=doc(scope);observed=call('document',case_id=cid,event_id='contract',document=first)
  with api._store() as st:c,_,_=st.load(COMPANY,cid);ref=next(iter(c._investigation['documents'][0]['extraction']['fields']))
  targeted=call('continue_investigation',case_id=cid,event_id='terms',interpretation=dict(family='customer_contract',claims=[dict(key='price',value='17350',source_fields=[ref],uncertainty='unreviewed')],questions=[dict(key='refund',needed='Does the Halcyon agreement permit refunds for service outages?',why='The supplied contract does not quantify outage remedies.',source_fields=[ref])]))
  restored=call('resume',case_id=cid);assert targeted['investigation']==restored['investigation']
  call('submit',case_id=cid,evidence=revenue_evidence(api,cid));original=call('execute',case_id=cid);assert original['execution_state']=='complete';assert '11494.38' in json.dumps(original['public_result'])
  repeat=call('execute',case_id=cid);assert repeat['checkpoint_revision']==original['checkpoint_revision']
  with api._store() as st:c,_,_=st.load(COMPANY,cid);node=next(iter(c.graph.nodes));before=copy.deepcopy(c.governance.versions.record())
  second=doc(scope,text='Fixed price EUR 18000. Corrected telemetry contract.',version='v2',supersedes='halcyon-agreement:v1')
  changed=call('document',case_id=cid,event_id='replacement',document=second);assert changed['currentness']=='STALE'
  evidence=revenue_evidence(api,cid,'18000',True)
  correction=call('correct_investigation',case_id=cid,event_id='correction',node_id=node,reason='Corrected signed agreement',evidence=evidence)
  reworked=call('rework_investigation',case_id=cid,event_id='rework',evidence={});assert reworked['execution_state']=='complete';assert '11925' in json.dumps(reworked['public_result'])
  assert call('correct_investigation',case_id=cid,event_id='correction',node_id=node,reason='Corrected signed agreement',evidence=evidence)['checkpoint_revision']==reworked['checkpoint_revision']
  with api._store() as st:c,rev,_=st.load(COMPANY,cid);revenue_state=copy.deepcopy(c._investigation);after=c.governance.versions.record();ops=st.connection.execute('SELECT count(*) FROM operations WHERE company_id=? AND case_id=?',(COMPANY,cid)).fetchone()[0]
  assert ops==2
  (Path(tmp)/'company-context.md').write_text(context().replace('investigation_threshold: UNKNOWN','investigation_threshold: 700'))
  p=call('investigate',request_id='prepayments-proof',objective='Why did prepaid field monitoring costs increase?',target_family='reconciliation');pcid=p['case_id']
  data=[('reconciliation_comparative','record_id,closing\nfield-network,1200\ntraining,400\n','1600',True),('reconciliation_current','record_id,closing\nfield-network,9350\ntraining,350\n','9700',False),('movements','record_id,opening,additions,consumption,closing,invoice_ref\nfield-network,1200,9200,1050,9350,QX-7826\ntraining,400,0,50,350,TR-611\n','9700',False)]
  for i,(role,text,total,prior) in enumerate(data):
   d=doc(scope,text,format='csv',role=role,id=role,row_count=2,complete_population=True,control_total=total)
   if prior:d['metadata']['period']=['2025-01-01','2025-12-31']
   movement=call('document',case_id=pcid,event_id='schedule-'+str(i),document=d)
  assert movement['investigation']['observations'][0]['increase']=='8100';assert 'QX-7826' in json.dumps(movement['investigation']['requests']);assert movement['execution_state']=='blocked'
  invoice=call('document',case_id=pcid,event_id='invoice',document=doc(scope,'Invoice QX-7826 EUR 9200; monitoring coverage 18 months. Allocation review absent.',format='text',role='invoice',id='QX-7826'))
  assert invoice['execution_state']=='blocked';assert call('resume',case_id=pcid)['investigation']==invoice['investigation']
  denied=api.call(dict(wire('resume',case_id=cid),company_id='other-company'));assert not denied['ok']
  items=[]
  for entity,fw,cur in [('UK-SUB','UK_GAAP','GBP'),('GROUP','IFRS','EUR')]:
   for key,val in [('framework',fw),('jurisdiction','GB'),('functional_currency',cur),('presentation_currency',cur),('calendar_id','FISCAL-UK')]:items.append(dict(id=entity+'-'+key,key=key,value=val,entity_id=entity,effective_from='2026-01-01',effective_to='2026-12-31',source_state='approved',source_ref='asserted-onboarding',source_version='v1'))
  uk=resolve(parse(context()),dict(version='v1',company_id=COMPANY,items=items,selection=dict(entity_id='UK-SUB',period_start='2026-01-01',period_end='2026-12-31')));assert uk['scope']['framework']=='UK_GAAP' and uk['scope']['currency']=='GBP';assert not uk['governed_records']
  conflict_items=[dict(id=k,key='policies',value=v,entity_id=scope['entity'],effective_from='2026-01-01',effective_to=None,source_state='approved',source_ref='asserted-policy',source_version='v1') for k,v in [('a','Recognize immediately'),('b','Defer until delivery')]]
  conflict=call('investigate',request_id='conflict-proof',objective='Determine conflicting policy treatment',target_family='customer_contract',context=dict(version='v1',company_id=COMPANY,items=conflict_items));assert conflict['execution_state']=='blocked' and 'policies' in conflict['investigation']['conflicts']
  with api._store() as st:pc,_,_=st.load(COMPANY,pcid);prepay_state=copy.deepcopy(pc._investigation)
  def retained(state):
   out=copy.deepcopy(state)
   out['documents']=[{k:d[k] for k in ('id','version','role','format','metadata','supersedes','original_sha256','original_bytes','extraction_sha256','original_content_base64','warnings','qualification','tables','blocks') if k in d} for d in state['documents']]
   out.pop('native_events',None)
   return out
  def versions(rows):return [dict(version_id=x['version_id'],state=x['state'],superseded_by=x.get('superseded_by'),immutable_sha256=hashlib.sha256(json.dumps({k:v for k,v in x.items() if k not in ('state','superseded_by')},sort_keys=True,separators=(',',':')).encode()).hexdigest()) for x in rows]
  return dict(contract='cao-build3-proof/1',synthetic_review_only=True,live_model_evaluation=False,fresh_process_each_operation=True,revenue=dict(case_id=cid,start=start,observed=observed,targeted=targeted,original=original,changed=changed,corrected=correction,reworked=reworked,checkpoint_revision=rev,native_operations=ops,original_versions=versions(before),final_versions=versions(after),state=retained(revenue_state)),prepayments=dict(case_id=pcid,start=p,movement=movement,invoice=invoice,state=retained(prepay_state),outcome='BLOCKED: no independently reviewed native accounting pack'),multi_entity=uk,conflict=conflict,isolation=denied)
if __name__=='__main__':print(json.dumps(proof(),sort_keys=True,indent=2))
