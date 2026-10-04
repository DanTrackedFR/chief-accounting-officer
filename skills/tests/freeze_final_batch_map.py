"""Freeze actual approved canonical bytes BEFORE implementing batch 30/48/49/50."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE='eb915dea82831d4ff385591ea4c4265633957132'
SELECTION={
 'defined-benefit-opeb':(30,'Defined Benefit & Other Post-Employment Benefits',{'TOPIC-05-005':[10]},'Qualified single-employer DB/OPEB report, census, obligation/assets and funded-status workpaper. IFRS event-free deficit pension accounting bridge only; US/UK/AASB detailed presentation, actuarial valuation, surplus/ceiling, minimum funding, amendments, settlements, curtailments, multi-employer and other-long-term methods fail closed.'),
 'accounting-controls-icfr':(48,'Accounting Controls & SOX / ICFR',{'TOPIC-09-001':[1,2,3],'TOPIC-09-002':[4,5,6],'TOPIC-09-003':[7,8,9],'TOPIC-09-004':[10,11],'TOPIC-09-007':[17,18],'TOPIC-09-008':[19,20],'TOPIC-09-009':[21,22]},'Risk/control design and complete occurrence/evidence readiness, qualified precision, action-level segregation, deficiency and retested remediation workpapers; no legal SOX applicability, testing opinion, effectiveness or management/auditor certification.'),
 'accounting-systems-data-integrity':(49,'Accounting Systems & Data Integrity',{'TOPIC-11-002':[4,5,6],'TOPIC-11-003':[7,8,9],'TOPIC-11-004':[10],'TOPIC-11-005':[13,14],'TOPIC-11-006':[15],'TOPIC-11-007':[17,18],'TOPIC-11-009':[21,22]},'Supplied entity/book/master-data and interface lineage, exact item/signed/gross source-target and migration ties, qualified zero-tolerance data-quality, access/EUC/AI-change evidence requirements; no engineering, writes, migration execution, source invention or reporting analytics engine.'),
 'accounting-operating-model':(50,'Accounting Operating Model & Team Governance',{'TOPIC-01-001':[2,3],'TOPIC-01-002':[4,5,6],'TOPIC-01-003':[8],'TOPIC-01-004':[9,10],'TOPIC-01-005':[11,12],'TOPIC-01-006':[13,14],'TOPIC-01-007':[15,16]},'Supplied accounting service/process and team populations, retained accountable RACI, actual peak-hour capacity, qualified maturity classification, evidenced governance cadence/SLA, dependency/transition/automation/AI readiness; no headcount benchmarks, HR decisions, ROI forecasts, IPO scoring or duplicate accounting analytics.'),
}
def freeze():
 manifest=json.loads((ROOT/'knowledge/phase-2d-topic-manifest.json').read_text())['topics']
 out=dict(schema_version=1,baseline_main=BASE,roadmap_batch=[30,48,49,50],owner_authorization='Skill30 explicitly released from the reserved queue for this batch',invariants=dict(approved_topics=157,capability_mappings=347,canonical_claims=1598,supplemental_tax_claims=64,approved_is_source_verified=False),packages={},untouched_packages=['government-grants','borrowing-costs','investment-property'],reserved_queue=[24,29,38,39],inspected_not_imported=['TOPIC-09-005','TOPIC-09-006','TOPIC-11-001','TOPIC-11-008','TOPIC-11-010','TOPIC-01-008'])
 for pkg,(number,name,selection,boundary) in SELECTION.items():
  info=dict(roadmap_number=number,roadmap_name=name,supported_executable_boundary=boundary,topics=[])
  for tid,ids in selection.items():
   t=next(t for t in manifest if t['topic_id']==tid);assert t['status']=='APPROVED'
   caps=['CAO-'+tid[6:8]+'-'+str(i).zfill(3) for i in ids];assert set(caps)<=set(t['capability_ids'])
   reg=next(ROOT/p for p in t['artifact_paths'] if p.endswith('standards-claims.json'))
   paths=set(reg.parent.rglob('*.md'))|{ROOT/p for p in t['artifact_paths'] if p.endswith('.md')}|{ROOT/'knowledge/phase-2e/reviews'/f'{tid}.json'}
   info['topics'].append(dict(topic_id=tid,topic_status=t['status'],capability_ids=caps,canonical_topic_capability_ids=t['capability_ids'],register=str(reg.relative_to(ROOT)),sha256=hashlib.sha256(reg.read_bytes()).hexdigest(),claims=json.loads(reg.read_text())['claims'],knowledge_documents=[dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(paths)]))
  out['packages'][pkg]=info
 target=ROOT/'skills/FINAL-BATCH-KNOWLEDGE-MAP.json'
 if target.exists():raise RuntimeError('Immutable map already exists; do not overwrite')
 target.write_text(json.dumps(out,indent=2)+'\n')
 print('Frozen',sum(len(p['topics']) for p in out['packages'].values()),'topics;',sum(len(t['claims']) for p in out['packages'].values() for t in p['topics']),'actual claims')
if __name__=='__main__':freeze()
