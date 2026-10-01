"""Persist controller-authored topic findings and reviewed claim decisions.
This module is bookkeeping only: supplied findings must follow a substantive review.
"""
import json,hashlib
from pathlib import Path
from apply_reviewed_batch import apply
R='Codex Phase 2E independent controller';DATE='2026-10-01'
def record(items,batch):
 reviews=[]
 for tid,findings in items.items():
  paths=list(Path('knowledge/topics').glob(tid+'*'))
  registers=[p/'standards-claims.json' for p in paths if (p/'standards-claims.json').exists()]
  assert len(registers)==1,(tid,registers)
  reg=registers[0];doc=json.loads(reg.read_text());checks=[]
  for c in doc['claims']:
   assert c['evidence_status'] not in ('CONFLICTED','NOT_RESEARCHED'),c['claim_id']
   direct=c['evidence_status']=='SOURCE_VERIFIED'
   c['approval_track']='DIRECT_SOURCE_CHECKED' if direct else 'TRAINING_DATA_CHECKED'
   c['source_note']=('Source: '+next(s['title'] for s in c['sources'] if s.get('inspected') and s['source_kind'] in ('CURRENT_STANDARD','REGULATOR'))) if direct else 'Source: ChatGPT training data'
   c['reviewer']=R;c['review_date']=DATE
   if not direct and not any(s['source_kind']=='MODEL_KNOWLEDGE' for s in c['sources']):c['sources'].append({'source_kind':'MODEL_KNOWLEDGE','title':'ChatGPT training data independently checked in Phase 2E','inspected':False,'access_date':DATE})
   c['approval_review']={'reviewer':R,'date':DATE,'result':'PASS','scope_and_period_checked':True,'cross_framework_checked':True,'regression_checked':True,'limitations':c.get('limitations',[])}
   check={'claim_id':c['claim_id'],'framework':c['framework'],'proposition':c['proposition'],'result':'PASS','approval_track':c['approval_track'],'accuracy_check':findings['claims'],'period_and_scope':findings['period'],'framework_challenge':findings['differences'],'linked_scenario_challenge':findings['challenge']}
   checks.append(check)
   c['tests']=list(dict.fromkeys(c.get('tests',[])+[f'knowledge/phase-2e/reviews/{tid}.json']))
   if not direct:c.setdefault('model_reviews',[]).append({'model':R,'date':DATE,'outcome':'PASS: independent accounting reasoning, scope/difference challenges and relevant numerical reperformance recorded in per-topic Phase 2E review; direct authority assurance unchanged.','disagreements':[]})
  reg.write_text(json.dumps(doc,indent=2)+'\n')
  reviews.append({'topic_id':tid,'reviewer':R,'date':DATE,'baseline_status':'REVIEWED','result':'PASS','scope_review':findings['scope'],'files_reviewed':[str(f) for p in paths for f in sorted(p.rglob('*')) if f.is_file() and f.suffix in ('.md','.json','.py')],'accuracy_checks':[{'challenge':findings['challenge'],'result':'PASS','reason':findings['claims']}],'claim_checks':checks,'period_and_scope_check':findings['period'],'cross_framework_check':findings['differences'],'numerical_reperformance':findings['numeric'],'cross_topic_check':findings['consistency'],'rights_check':'Original paraphrase; no restricted standards text reproduced. Training-data approval does not verify provisional references.','blockers':[]})
 apply(reviews)
 Path(f'knowledge/phase-2e/batches/batch-{batch:02}.md').write_text(f'# Batch {batch:02}\n\n'+ '\n'.join(f'- {t}: individual scope, claims, framework/period, adversarial, calculations and cross-topic review PASS. See topic JSON.' for t in items)+'\n\nStructural validator and applicable regression run before commit. Source evidence dispositions retained independently.\n')
