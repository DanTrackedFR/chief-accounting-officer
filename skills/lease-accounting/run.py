"""Run a lease case JSON and emit an internal result or curated public answer."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from case_engine import run_case
from public_adapter import to_public_answer

def encode(obj):
    if hasattr(obj,"as_tuple"): return str(obj)
    raise TypeError(type(obj).__name__)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("case_json"); p.add_argument("--public",action="store_true")
    args=p.parse_args()
    case=json.loads(Path(args.case_json).read_text())
    result=run_case(case)
    if args.public: result=to_public_answer(result)
    print(json.dumps(result,indent=2,default=encode))

if __name__=="__main__": main()
