"""Evidence-record constructors; never infer source inspection."""
import json
from pathlib import Path
def create(tid,entries,replace=False):
 paths=list(Path('knowledge/topics').glob(tid+'*'));regs=[p/'standards-claims.json' for p in paths if (p/'standards-claims.json').exists()]
 if regs:p=regs[0];d=json.loads(p.read_text())
 else:
  m=json.load(open('knowledge/phase-2d-topic-manifest.json'));t=next(t for t in m['topics'] if t['topic_id']==tid)
  root=next((Path(a).parent for a in t['artifact_paths'] if a.endswith('/README.md')),paths[0]);p=root/'standards-claims.json';d={'topic_id':tid,'claims':[]}
 if replace:d['claims']=[]
 for i,e in enumerate(entries,1):
  framework,prop,*source=e;direct=bool(source)
  c={'claim_id':f'{tid}-{framework}-E{i:03}','framework':framework,'proposition':prop,'paragraph_references':[source[2]] if direct else [],'reference_confidence':'VERIFIED' if direct else 'UNKNOWN','evidence_status':'SOURCE_VERIFIED' if direct else 'MODEL_DERIVED_AUDIT_REQUIRED','sources':[{'source_kind':'REGULATOR' if framework in ('OTHER','SEC','REGULATORY') else 'CURRENT_STANDARD','title':source[0],'url':source[1],'locator':source[2],'access_date':'2026-10-01','inspected':True}] if direct else [{'source_kind':'MODEL_KNOWLEDGE','title':'ChatGPT training data independently checked in Phase 2E','inspected':False,'access_date':'2026-10-01'}],'effective_period':'Select actual framework edition, annual start and adopted amendments as described in topic review.','entity_scope':'Topic-specific scope and tier resolved in linked Phase 2E review.','audit_required':not direct,'limitations':[] if direct else ['Training-data checked; operative authority not claimed inspected; exact paragraph references not asserted.'],'tests':[f'knowledge/phase-2e/reviews/{tid}.json'],'model_reviews':[],'reviewer':None,'review_date':None}
  assert not any(x['claim_id']==c['claim_id'] for x in d['claims']);d['claims'].append(c)
 p.write_text(json.dumps(d,indent=2)+'\n');return p
