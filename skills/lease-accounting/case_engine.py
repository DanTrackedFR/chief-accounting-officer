"""Executable lessee lease vertical slice. Accounting policy is gated by approved repository knowledge."""
from decimal import Decimal
from lease_math import d, money, initial_measurement, liability_schedule

SUPPORTED = {"IFRS", "AASB", "US_GAAP", "UK_GAAP"}

class CaseError(ValueError): pass

def _need(case, names):
    missing=[n for n in names if case.get(n) in (None,"",[])]
    if missing: raise CaseError("Missing required facts: "+", ".join(missing))

def validate_case(case):
    _need(case, ["case_id","framework","period_start","entity","jurisdiction","commencement_date",
                 "contract_contains_lease","payments","periodic_rate","lease_periods"])
    if case["framework"] not in SUPPORTED: raise CaseError("Unsupported framework")
    if case["contract_contains_lease"] is not True:
        raise CaseError("This measurement slice requires an approved conclusion that the contract contains a lease")
    if case.get("role","lessee") != "lessee": raise CaseError("Lessor accounting is outside this skill")
    if case.get("sale_and_leaseback"): raise CaseError("Route sale-and-leaseback to TOPIC-04-011 specialist workflow")
    if case["framework"]=="UK_GAAP" and str(case["period_start"]) < "2026-01-01" and not case.get("early_adopted_revised_section20"):
        raise CaseError("Pre-2026 UK GAAP requires the legacy Section 20 route")
    if case["framework"]=="AASB":
        _need(case,["entity_type","reporting_tier"])
    if case["framework"]=="US_GAAP":
        _need(case,["classification"])
        if case["classification"] not in ("finance","operating"): raise CaseError("US GAAP classification must be finance or operating")
    if len(case["payments"]) != int(case["lease_periods"]):
        raise CaseError("Fixed-payment vertical slice requires one end-period payment per lease period")
    return case

def _citations(framework):
    # Only pinpoint references established in governed lease knowledge are emitted.
    if framework=="IFRS":
        return [
          {"title":"IFRS 16 Leases","locator":"IFRS 16.9 and B9–B31"},
          {"title":"IFRS 16 Leases","locator":"IFRS 16.22–28"},
          {"title":"IFRS 16 Leases","locator":"IFRS 16.29–46"},
          {"title":"IFRS 16 Leases","locator":"IFRS 16.47–60"}]
    if framework=="UK_GAAP":
        return [
          {"title":"FRS 102 Section 20 Leases","locator":"FRS 102 20.47, 20.51–20.54"},
          {"title":"FRS 102 Section 20 Leases","locator":"FRS 102 20.56–20.75"},
          {"title":"FRS 102 Section 20 Leases","locator":"FRS 102 20.76–20.85"}]
    # Current governed records do not establish exact pinpoints for these routes.
    return [{"title":"ASC 842 Leases","locator":"Topic 842 — pinpoint paragraph verification required"}] if framework=="US_GAAP" else [
      {"title":"AASB 16 Leases","locator":"AASB 16 — pinpoint paragraph verification required"}]

def run_case(case):
    validate_case(case)
    payments=[money(x) for x in case["payments"]]
    unpaid=[(i+1,p) for i,p in enumerate(payments)]
    initial=initial_measurement(unpaid,case["periodic_rate"],
        prepayments=case.get("prepayments","0"),direct_costs=case.get("direct_costs","0"),
        incentives=case.get("incentives","0"),restoration=case.get("restoration","0"))
    liability=liability_schedule(initial["lease_liability"],payments,case["periodic_rate"],
                                 final_rounding_tolerance=case.get("rounding_tolerance","0.10"))
    periods=int(case["lease_periods"]); rou0=initial["rou_asset"]
    framework=case["framework"]; classification=case.get("classification")
    if framework=="US_GAAP" and classification=="operating":
        if any(d(case.get(k,"0")) != 0 for k in ("prepayments","direct_costs","incentives","restoration")):
            raise CaseError("ASC 842 operating slice with ROU adjustments requires expanded cost mechanics")
        total=sum(payments,Decimal("0")); lease_cost=money(total/periods)
        rou=[]; opening=rou0
        for row in liability:
            reduction=money(lease_cost-row["interest"]); closing=money(opening-reduction)
            rou.append({"period":row["period"],"opening":opening,"lease_cost":lease_cost,
                        "liability_interest":row["interest"],"rou_reduction":reduction,"closing":closing})
            opening=closing
    else:
        depreciation=money(rou0/periods); rou=[]; opening=rou0
        for i in range(1,periods+1):
            dep=opening if i==periods else depreciation; closing=money(opening-dep)
            rou.append({"period":i,"opening":opening,"depreciation":dep,"closing":closing}); opening=closing
    journals=_journals(framework,classification,initial,liability,rou)
    limitations=[]
    if framework in ("US_GAAP","AASB"):
        limitations.append("The governed knowledge does not yet establish a confirmed pinpoint paragraph for this route; do not present the locator as paragraph-verified.")
    return {"skill_id":"SKILL-LEASE-001","status":"complete","case_id":case["case_id"],
      "framework":framework,"jurisdiction":case["jurisdiction"],"entity":case["entity"],
      "period_start":case["period_start"],"method":"fixed end-period lessee lease vertical slice",
      "initial_measurement":initial,"liability_schedule":liability,"rou_schedule":rou,
      "journal_entries":journals,"citations":_citations(framework),"limitations":limitations,
      "judgments":["Lease identification, term, payment population and discount rate are supplied approved case facts; this calculator does not infer them."],
      "controls":["Tie contract payments to schedule.","Tie liability and ROU closing balances to GL.","Reviewer approves term, rate, classification/elections and citations."],
      "disclosures":["Route schedule totals and judgments to the applicable lease disclosure checklist."],
      "open_items":[]}

def _journals(framework,classification,initial,liability,rou):
    entries=[{"when":"commencement","lines":[["Dr","ROU asset",initial["rou_asset"]],["Cr","lease liability",initial["lease_liability"]]]}]
    adjustment=money(initial["rou_asset"]-initial["lease_liability"])
    if adjustment:
        entries[0]["note"]="ROU/liability difference represents supplied prepayment/direct-cost/incentive/restoration bridge; post the underlying cash/provision accounts from the approved workpaper."
    for l,r in zip(liability,rou):
        if framework=="US_GAAP" and classification=="operating":
            entries.append({"when":f"period {l['period']}","lines":[["Dr","lease expense",r["lease_cost"]],["Cr","lease liability (interest accretion)",l["interest"]],["Cr","ROU asset",r["rou_reduction"]],["Dr","lease liability",l["payment"]],["Cr","cash",l["payment"]]]})
        else:
            entries.append({"when":f"period {l['period']}","lines":[["Dr","interest expense",l["interest"]],["Cr","lease liability",l["interest"]],["Dr","lease liability",l["payment"]],["Cr","cash",l["payment"]],["Dr","ROU depreciation/amortization",r["depreciation"]],["Cr","ROU asset",r["depreciation"]]]})
    return entries
