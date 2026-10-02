"""Provision measurement arithmetic, with framework-specific recognition gates."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core_accounting import dec,cash,required,context,ReviewRequired,journal,envelope

TOPICS=["TOPIC-08-003","TOPIC-08-005","TOPIC-15-004"]

def run(case,claims):
    context(case);required(case,"present_obligation","past_event","recognition_approved","measurement_basis","outcomes","existing_provision")
    if not case["present_obligation"] or not case["past_event"]:
        raise ReviewRequired("Provision recognition not established; assess contingent disclosure")
    if case["recognition_approved"] is not True:
        raise ReviewRequired("Framework-specific probability and measurement recognition gate not approved")
    if case["framework"]=="US_GAAP" and case["measurement_basis"]!="ASC_450_APPROVED":
        raise ReviewRequired("US GAAP ASC 450 measurement requires separately approved range/estimate")
    if case["framework"]!="US_GAAP" and case["measurement_basis"] not in ("EXPECTED_VALUE","MOST_LIKELY"):
        raise ReviewRequired("Unsupported measurement basis")
    outcomes=case["outcomes"]
    if not outcomes: raise ReviewRequired("No supported outcome estimates")
    if case["measurement_basis"]=="EXPECTED_VALUE":
        if sum((dec(x["probability"]) for x in outcomes),dec("0"))!=1:
            raise ReviewRequired("Outcome probabilities must sum to one")
        estimate=sum((dec(x["amount"])*dec(x["probability"]) for x in outcomes),dec("0"))
    elif case["measurement_basis"]=="MOST_LIKELY":
        if len(outcomes)!=1: raise ReviewRequired("Provide reviewed single most-likely outcome")
        estimate=dec(outcomes[0]["amount"])
    else:
        if len(outcomes)!=1 or not case.get("asc_450_range_memo"):
            raise ReviewRequired("ASC 450 measurement memo and selected estimate required")
        estimate=dec(outcomes[0]["amount"])
    if estimate<0: raise ReviewRequired("Negative settlement estimate")
    factor=dec(case.get("discount_factor","1"))
    if not 0<factor<=1: raise ReviewRequired("Invalid discount factor")
    if case["framework"]=="US_GAAP" and factor!=1 and not case.get("us_discounting_exception_approved"):
        raise ReviewRequired("Do not discount ASC 450 provisions by default")
    provision=cash(estimate*factor); movement=cash(provision-dec(case["existing_provision"]))
    lines=journal(("Dr","provision expense",movement),("Cr","provision",movement)) if movement>=0 else journal(
      ("Dr","provision",-movement),("Cr","provision reversal",-movement))
    return envelope("SKILL-PROV-001",case,case["measurement_basis"],
      {"undiscounted_estimate":cash(estimate),"provision":provision,"movement":movement},[lines],
      ["Present obligation, probability, reliable estimation, measurement basis, discounting and reimbursement assessed separately"],
      ["Reimbursement, unwinding, restructuring, onerous contracts and contingent disclosures require event-specific review"],claims)
