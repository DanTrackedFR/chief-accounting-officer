"""python -m orchestration.run_case request.json; public output only."""
import argparse,json
from .runtime import CAO

def main():
    p=argparse.ArgumentParser();p.add_argument('request');p.add_argument('--route',default='answer')
    args=p.parse_args()
    try:
        with open(args.request) as f: request=json.load(f)
        cao=CAO();case=cao.run(request);record=cao.public(case,args.route)
    except (ValueError,TypeError,OSError):
        # Never render an opaque exception, internal bytes or contaminated text.
        from interfaces.public_output import public_record
        record=public_record(dict(guidance='Accounting work is blocked pending safe input and output review.',
            status='blocked',open_items=['Resolve invalid input or contaminated accounting output.']),route='answer')
    print(json.dumps(record,ensure_ascii=False))
if __name__=='__main__':main()
