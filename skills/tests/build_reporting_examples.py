"""Regenerate synthetic unsigned cases and both certification-state public snapshots."""
import json
from pathlib import Path
from reporting_cases import PACKAGES,reporting,certified
from production import assess_case,to_public,serializable

def build():
    for package in PACKAGES:
        directory=Path(__file__).resolve().parents[1]/package/'examples';directory.mkdir(exist_ok=True)
        for framework in ['IFRS','US_GAAP','UK_GAAP','AASB']:
            case=certified(package,framework);complete=assess_case(package,case)
            if complete['status']!='complete':raise RuntimeError(complete['conclusion'])
            del case['reviewer_signoff'];partial=assess_case(package,case)
            for suffix,value in [('case',case),('partial.public',to_public(partial)),('complete.public',to_public(complete))]:
                (directory/(framework+'.'+suffix+'.json')).write_text(json.dumps(value,default=serializable,indent=2,ensure_ascii=False)+'\n')

if __name__=='__main__':build()
