"""Mechanical claim linkage and executable accounting checks; no status promotion."""
from pathlib import Path
import json, re, math
from decimal import Decimal
def validate_schema(value, schema, path='$'):
 types={'object':dict,'array':list,'string':str,'boolean':bool,'null':type(None)}
 if 'type' in schema:
  allowed=schema['type'] if isinstance(schema['type'],list) else [schema['type']]
  assert any(isinstance(value,types[t]) for t in allowed),(path,'type')
 if 'enum' in schema: assert value in schema['enum'],(path,'enum',value)
 if isinstance(value,str):
  if 'minLength' in schema: assert len(value)>=schema['minLength'],path
  if 'pattern' in schema: assert re.search(schema['pattern'],value),path
 if isinstance(value,dict):
  assert set(schema.get('required',[]))<=set(value),(path,'required')
  props=schema.get('properties',{})
  if schema.get('additionalProperties') is False: assert set(value)<=set(props),(path,'extra')
  for k,v in value.items():
   if k in props: validate_schema(v,props[k],path+'.'+k)
 if isinstance(value,list) and 'items' in schema:
  for i,v in enumerate(value): validate_schema(v,schema['items'],path+'['+str(i)+']')


ROOT = Path(__file__).resolve().parents[3]
TOPICS = ROOT / "knowledge/topics"
SCHEMA = json.loads((ROOT / "knowledge/standards-evidence/claim.schema.json").read_text())
FW = {"IFRS":"IFRS","US":"US_GAAP","UK":"UK_GAAP","AASB":"AASB"}
URLS = {
 "IFRS":"https://www.ifrs.org/issued-standards/list-of-standards/",
 "US":"https://asc.fasb.org/",
 "UK":"https://www.frc.org.uk/library/standards-codes-policy/accounting-and-reporting/uk-accounting-standards/frs-102/",
 "AASB":"https://standards.aasb.gov.au/accounting-standards"}

def render_claims(folder):
 p=TOPICS/folder
 register=json.loads((p/"standards-claims.json").read_text())
 existing={c["claim_id"]:c for c in register["claims"]}
 topic=register["topic_id"]
 marker=re.compile(r"\[\[([A-Z]+:[A-Z][0-9]+(?:;[A-Z]+:[A-Z][0-9]+)*)\]\]")
 method=p/"phase-2d-method.md"
 text=method.read_text()
 # Each tagged segment is independently authored. A segment is a single rule;
 # author, not this helper, selects the applicable frameworks and keys.
 for line in text.splitlines():
  start=0
  for m in marker.finditer(line):
   proposition=line[start:m.start()].strip().lstrip("- ").strip()
   for token in m.group(1).split(";"):
    fw,key=token.split(":");cid=f"{topic}-{fw}-{key}"
    if cid in existing and existing[cid]["proposition"]!=proposition:
     raise ValueError(f"Claim key reused for different text: {cid}")
    existing[cid]={"claim_id":cid,"framework":FW[fw],"proposition":proposition,
      "paragraph_references":[],"reference_confidence":"UNKNOWN",
      "evidence_status":"MODEL_DERIVED_AUDIT_REQUIRED",
      "sources":[{"source_kind":"MODEL_KNOWLEDGE","title":"Independently authored accounting method; primary-source attempt recorded in research log",
       "url":URLS[fw],"locator":None,"version_date":None,"access_date":"2026-09-29","inspected":False}],
      "effective_period":"Reporting period and adoption branch specified in phase-2d-method.md",
      "entity_scope":"Framework/entity applicability branches specified in phase-2d-method.md",
      "audit_required":True,"limitations":["Direct authoritative audit remains open; no exact paragraph asserted from uncertain model knowledge."],
      "tests":["phase-2d-scenarios.json"],"model_reviews":[],
      "reviewer":None,"review_date":None}
   start=m.end()
 rendered=marker.sub(lambda m:" ".join(f"[{topic}-{x.replace(':','-')}]" for x in m.group(1).split(";")),text)
 method.write_text(rendered)
 register["claims"]=list(existing.values())
 validate_schema(register,SCHEMA)
 (p/"standards-claims.json").write_text(json.dumps(register,indent=2)+"\n")

def check_scenarios(folder, supplied_cases=None):
 p=TOPICS/folder
 cases=json.loads((p/"phase-2d-scenarios.json").read_text())
 register=json.loads((p/"standards-claims.json").read_text())
 ids={c["claim_id"] for c in register["claims"]}
 results=[]
 for case in (supplied_cases if supplied_cases is not None else cases["cases"]):
  assert case["claim_ids"] and set(case["claim_ids"])<=ids,case["id"]
  assert case["frameworks"],case["id"]
  env=dict(case.get("facts",{}))
  for name,expr in case.get("calculations",{}).items():
   env[name]=eval(expr,{"__builtins__":{},"sum":sum,"min":min,"max":max,"round":round,"abs":abs,"pow":pow},env)
  for name,expected in case.get("expected_calculations",{}).items():
   assert abs(env[name]-expected)<=case.get("tolerance",0.011),(case["id"],name,env[name],expected)
  if "route" in case:
   got=bool(eval(case["route"],{"__builtins__":{}},env))
   assert got==case["expected_route"],(case["id"],"route",got)
  framework_results={}
  for framework, decision in case.get('framework_routes',{}).items():
   actual=eval(decision['expression'],{'__builtins__':{}},env)
   assert actual==decision['expected'],(case['id'],framework,'framework route',actual)
   framework_results[framework]=actual
  control_results={}
  for name, decision in case.get('control_checks',{}).items():
   actual=eval(decision['expression'],{'__builtins__':{}},env)
   assert actual==decision['expected'],(case['id'],name,'control',actual)
   control_results[name]=actual
  ledger=dict(case.get("opening_balances",{}))
  for entry in case.get("journals",[]):
   amounts=[eval(str(x["amount"]),{"__builtins__":{}},env) for x in entry["lines"]]
   assert abs(sum(a if x["side"]=="Dr" else -a for a,x in zip(amounts,entry["lines"])))<=0.011,(case["id"],entry["event"],"unbalanced")
   for x,a in zip(entry["lines"],amounts):
    ledger[x["account"]]=ledger.get(x["account"],0)+(a if x["side"]=="Dr" else -a)
  for account,expected in case.get("expected_balances",{}).items():
   assert abs(ledger.get(account,0)-expected)<=0.011,(case["id"],account,ledger.get(account,0),expected)
  for field in ["workpaper_outcome","control_outcome","data_outcome","presentation_disclosure_outcome"]:
   assert len(case[field])>20,(case["id"],field)
  results.append({"case_id":case["id"],"result":"PASS","frameworks":case["frameworks"],"calculations":env,"ledger":ledger,"framework_routes":framework_results,"control_checks":control_results})
 return results

def check_topic(folder):
 p=TOPICS/folder
 register=json.loads((p/"standards-claims.json").read_text())
 validate_schema(register,SCHEMA)
 ids={c["claim_id"] for c in register["claims"]}
 assert len(ids)==len(register["claims"])
 missing=[]
 for f in p.rglob("*.md"):
  for cid in re.findall(r"\[(TOPIC-\d\d-\d\d\d-(?:IFRS|US|UK|AASB)-[A-Z0-9]+)\]",f.read_text()):
   if cid not in ids:missing.append((str(f),cid))
 assert not missing,missing
 assert all(c["audit_required"] or c["evidence_status"]=="SOURCE_VERIFIED" for c in register["claims"])
 return check_scenarios(folder)

if __name__=="__main__":
 import sys
 for folder in sys.argv[1:]:
  result=check_topic(folder)
  print(folder,len(result),"executed cases PASS")
