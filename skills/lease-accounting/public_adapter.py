"""Curate a skill result through the repository public-output boundary."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from interfaces.public_output import public_record

def to_public_answer(result):
    guidance=(f"Lease case {result['case_id']}: initial lease liability "
              f"{result['initial_measurement']['lease_liability']} and initial ROU asset "
              f"{result['initial_measurement']['rou_asset']}. See the reviewed schedule and journals for subsequent accounting.")
    record={"topic_id":"TOPIC-04-010","guidance":guidance,"framework":result["framework"],
      "jurisdiction":result["jurisdiction"],"entity_scope":result["entity"],
      "effective_period":str(result["period_start"]),"limitations":result["limitations"],
      "uncertainties":result["open_items"],"citations":result["citations"]}
    return public_record(record,route="answer")
