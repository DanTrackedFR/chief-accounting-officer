"""Capture deterministic orchestration examples outside historical target paths."""
import importlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT));OUT=Path(__file__).parent/'orchestration-fresh'
GROUPS={
 'foundation':('generate_examples',''),
 'diagnostics':('generate_diagnostic_examples',''),
 'intake':('generate_intake_examples','intake'),
 'saas':('generate_saas_examples','saas-close'),
 'treasury':('generate_treasury_examples','treasury-financing'),
 'group':('generate_group_examples','group-accounting'),
 'scopes':('generate_scope_examples','scope-repeated-owner'),
 'caseperiod':('generate_stage2_examples','case-period-invalidation'),
 'intercompany':('generate_stage3_examples','intercompany-framework-currency'),
 'multip':('generate_stage4_examples','multi-entity-multi-period'),
 'temporal':('generate_stage4_temporal_examples','multi-entity-multi-period-temporal'),
 'temporalmodel':('generate_stage4_temporal_model_examples','multi-entity-multi-period-temporal-model'),
 'durable':('generate_persistence_examples','durable-case-foundation'),
 'memory':('generate_persistence_stage3_examples','company-accounting-memory')}
for group in sys.argv[1:] or GROUPS:
 module,folder=GROUPS[group];values=importlib.import_module('orchestration.tests.'+module).artifacts();directory=OUT/folder;directory.mkdir(parents=True,exist_ok=True)
 for name,value in values.items():(directory/name).write_text(json.dumps(value,sort_keys=True,indent=2,default=str)+'\n')
 print(group,len(values),flush=True)
