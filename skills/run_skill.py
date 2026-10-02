"""Public CLI adapter: python skills/run_skill.py PACKAGE CASE.json."""
import argparse,json
from production import PACKAGES,assess_case,to_public,serializable

def main():
    p=argparse.ArgumentParser();p.add_argument('skill',choices=PACKAGES);p.add_argument('case');p.add_argument('--route',default='answer')
    args=p.parse_args()
    with open(args.case) as f:case=json.load(f)
    result=assess_case(args.skill,case)
    print(json.dumps(to_public(result,args.route),default=serializable,ensure_ascii=False))
if __name__=='__main__':main()
