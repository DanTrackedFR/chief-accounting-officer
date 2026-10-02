"""Scenario-weighted ECL arithmetic with explicit IFRS 9 / US CECL route gating."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core_accounting import dec,cash,required,context,ReviewRequired,journal,envelope

TOPICS=["TOPIC-06-007","TOPIC-06-010"]

def run(case,claims):
    context(case);required(case,"model","exposure","scenarios","existing_allowance","instrument_scope_approved")
    if case["instrument_scope_approved"] is not True: raise ReviewRequired("Instrument scope/classification not approved")
    model=case["model"]
    if case["framework"] in ("IFRS","AASB") and model not in ("IFRS_9_STAGE_1_12M","IFRS_9_STAGE_2_LIFETIME","IFRS_9_STAGE_3_LIFETIME","IFRS_9_SIMPLIFIED_LIFETIME"):
        raise ReviewRequired("Select applicable IFRS 9 impairment route")
    if case["framework"]=="US_GAAP" and model!="ASC_326_CECL":
        raise ReviewRequired("ASC 326 CECL and IFRS 9 staging are not interchangeable")
    if case["framework"]=="UK_GAAP": raise ReviewRequired("Resolve period-specific UK impairment model in specialist route")
    if model=="IFRS_9_STAGE_1_12M" and case.get("lifetime_pd_used"): raise ReviewRequired("Stage 1 requires 12-month default-event scope")
    exposure=dec(case["exposure"])
    if exposure<0: raise ReviewRequired("Negative exposure")
    scenarios=case["scenarios"]; weights=sum((dec(x["weight"]) for x in scenarios),dec("0"))
    if weights!=1: raise ReviewRequired("Scenario weights must sum to exactly one")
    losses=[]
    for s in scenarios:
        required(s,"weight","pd","lgd","discount_factor")
        w,pd,lgd,df=(dec(s[k]) for k in ("weight","pd","lgd","discount_factor"))
        if not(0<=w<=1 and 0<=pd<=1 and 0<=lgd<=1 and 0<df<=1): raise ReviewRequired("Invalid ECL input")
        losses.append(exposure*w*pd*lgd*df)
    allowance=cash(sum(losses,dec("0")));existing=cash(case["existing_allowance"])
    movement=cash(allowance-existing)
    lines=journal(("Dr","credit loss expense",movement),("Cr","loss allowance",movement)) if movement>=0 else journal(
      ("Dr","loss allowance",-movement),("Cr","credit loss reversal",-movement))
    return envelope("SKILL-ECL-001",case,model,
      {"expected_credit_loss":allowance,"opening_allowance":existing,"allowance_movement":movement},[lines],
      ["Model, stage, exposure, forward-looking scenario weights, PD, LGD and discount factors require documented approval"],
      ["Simplified scalar PD/LGD model: not a substitute for exposure-at-default term structures, cash-shortfall modelling, collateral or stage-transition assessment"],claims)
