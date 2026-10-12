"""Execute existing generators into an additive review namespace only."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
# Original generator scripts are untouched. Their destination and comparison
# baseline are redirected locally; no historical target is rewritten.
kind=sys.argv[1]
if kind=='specialist':
 p=ROOT/'recovery/borrowing-costs-pr42/capture_specialist_history.py';s=p.read_text().replace('ROOT=Path(__file__).resolve().parents[2]',f'ROOT=Path({str(ROOT)!r})').replace("dest=Path(__file__).parent/'specialist-fresh'",f'dest=Path({str(HERE / "specialist-fresh")!r})').replace('old=json.loads((ROOT/name).read_text())','old=json.loads(reference_path(ROOT/name).read_text())').replace('from production import serializable','from production import serializable\nfrom orchestration.history_references import prior_reference_path as reference_path')
 exec(compile(s,str(p),'exec'))
elif kind=='orchestration':
 p=ROOT/'recovery/borrowing-costs-pr42/capture_orchestration_history.py';s=p.read_text().replace('ROOT=Path(__file__).resolve().parents[2]',f'ROOT=Path({str(ROOT)!r})').replace("OUT=Path(__file__).parent/'orchestration-fresh'",f'OUT=Path({str(HERE / "orchestration-fresh")!r})');sys.argv=sys.argv[1:];exec(compile(s,str(p),'exec'))
elif kind in ('durable2','durable4'):
 sys.path.insert(0,str(ROOT));import importlib
 m=importlib.import_module('orchestration.tests.generate_persistence_stage'+kind[-1]+'_examples');dest=HERE/'orchestration-fresh'/m.TARGET.name;dest.mkdir(parents=True,exist_ok=True)
 for name,value in m.artifacts().items():(dest/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
 print(kind,'PASS')
else:raise SystemExit('Supported: specialist, orchestration, durable2, durable4')
