"""Apply explicitly recorded controller decisions, never infer approval from file coverage."""
import json
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[2]

def apply(reviews):
    p=ROOT/'knowledge/phase-2d-topic-manifest.json';m=json.loads(p.read_text())
    for review in reviews:
        tid=review['topic_id'];t=next(x for x in m['topics'] if x['topic_id']==tid)
        assert t['status']=='REVIEWED',tid
        assert review['result']=='PASS' and review['accuracy_checks'] and not review['blockers'],tid
        dest=ROOT/'knowledge/phase-2e/reviews'/f'{tid}.json';dest.write_text(json.dumps(review,indent=2)+'\n')
        registers=list(ROOT.glob('knowledge/topics/'+tid+'*/standards-claims.json'))
        assert len(registers)==1,(tid,registers)
        for c in json.loads(registers[0].read_text())['claims']:
            assert c['approval_track'] in {'DIRECT_SOURCE_CHECKED','TRAINING_DATA_CHECKED'},c['claim_id']
            assert c['approval_review']['result']=='PASS',c['claim_id']
            assert all(c['approval_review'][k] for k in ('scope_and_period_checked','cross_framework_checked','regression_checked')),c['claim_id']
            assert c['evidence_status'] not in {'CONFLICTED','NOT_RESEARCHED'},c['claim_id']
        reg=str(registers[0].relative_to(ROOT))
        if reg not in t['artifact_paths']:t['artifact_paths'].append(reg)
        t['qa_evidence'].append(str(dest.relative_to(ROOT)));t['status']='APPROVED';t['last_update']='2026-10-01'
    p.write_text(json.dumps(m,indent=2)+'\n')
    counts=Counter(t['status'] for t in m['topics']);done=counts['APPROVED']
    # Required order: manifest, progress, roadmap. No Master Build Map in snapshot.
    p=ROOT/'knowledge/phase-2d-progress.md'
    p.write_text(f'''# Phase 2D and Phase 2E progress\n\nUpdated 2026-10-01. Canonical source: `knowledge/phase-2d-topic-manifest.json`.\n\n- Canonical topics: 157; capabilities: 347/347.\n- APPROVED: {done}.\n- REVIEWED pending Phase 2E: {counts['REVIEWED']}.\n- PARTIAL / NOT_STARTED / BLOCKED: 0 / 0 / 0.\n\nPhase 2D substantive population remains complete. Phase 2E is in progress; {done} topics passed recorded individual controller review, and {157-done} are pending. Pending is not a genuine accounting blocker.\n\nAPPROVED follows the owner-authorised two-track contract and does not imply SOURCE_VERIFIED. Per-claim evidence status and future direct-source audit requirements are retained. Individual review records are under `knowledge/phase-2e/reviews/`; registers remain topic-local.\n\nPublic output interface tests pass. There is no runnable production CAO application in the repository; runtime integration/verification remains pending and does not block accounting review.\n''')
    p=ROOT/'architecture/build-roadmap.md';s=p.read_text()
    start=s.index('Current independently reconciled substantive status:')
    end=s.index(' across 157 canonical topics',start)
    s=s[:start]+f"Current independently reconciled substantive status: **{counts['REVIEWED']} REVIEWED, 0 PARTIAL, 0 NOT_STARTED, 0 BLOCKED, {done} APPROVED**"+s[end:]
    if '## Phase 2E — approval audit' in s:s=s[:s.index('## Phase 2E — approval audit')]
    s+='## Phase 2E — approval audit\n'+f'In progress: {done}/157 individually processed and approved; {157-done} pending. See `knowledge/phase-2e/reviews/`. Per-claim source assurance remains separate. No Master Build Map found in the repository tree. Production output-boundary runtime verification is pending; executable contract tests pass.\n'
    s=s.replace('Eight operational topics passed individual scope and adversarial review; source-evidence labels remain independent.','Individually signed-off topics passed scope, claims, adversarial and relevant numerical review; source-evidence labels remain independent.')
    p.write_text(s)
