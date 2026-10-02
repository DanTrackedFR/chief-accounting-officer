"""Revenue allocation and recognition mechanics; contract judgments remain reviewer inputs."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core_accounting import dec,cash,required,context,ReviewRequired,journal,envelope

TOPICS=["TOPIC-03-001","TOPIC-03-002","TOPIC-03-003","TOPIC-03-004","TOPIC-03-005","TOPIC-03-006","TOPIC-03-012"]

def allocate(price,obligations):
    if not obligations: raise ReviewRequired("No distinct obligations")
    total=sum((dec(x["ssp"]) for x in obligations),dec("0"))
    if total<=0 or any(dec(x["ssp"])<=0 for x in obligations): raise ReviewRequired("Invalid stand-alone selling prices")
    from decimal import ROUND_DOWN
    amount=cash(price)
    if amount<0:raise ReviewRequired("Negative allocation price")
    exact=[amount*dec(x["ssp"])/total for x in obligations]
    shares=[x.quantize(dec("0.01"),rounding=ROUND_DOWN) for x in exact]
    cents=int((amount-sum(shares))/dec("0.01"))
    order=sorted(range(len(shares)),key=lambda i:(-(exact[i]-shares[i]),i))
    for i in order[:cents]:shares[i]+=dec("0.01")
    out=[{"obligation":x["id"],"allocation":v} for x,v in zip(obligations,shares)]
    if sum(x["allocation"] for x in out)!=amount: raise ReviewRequired("Allocation reconciliation failed")
    return out

def run(case,claims):
    context(case)
    required(case,"contract_gate_approved","obligations","transaction_price","recognition_period")
    if case["contract_gate_approved"] is not True: raise ReviewRequired("Contract criteria not established")
    if case.get("variable_consideration_unresolved") or case.get("principal_agent_unresolved") or case.get("modification_unresolved"):
        raise ReviewRequired("Resolve variable consideration, principal/agent or modification before recognition")
    obligations=case["obligations"]
    for x in obligations:
        if not all(k in x for k in ("id","ssp","satisfaction_fraction","satisfaction_evidence")):
            raise ReviewRequired("Each obligation needs SSP, supported satisfaction and evidence")
        if not dec("0")<=dec(x["satisfaction_fraction"])<=dec("1"):
            raise ReviewRequired("Satisfaction fraction outside [0,1]")
        if not x["satisfaction_evidence"]: raise ReviewRequired("Missing satisfaction evidence")
    allocations=allocate(case["transaction_price"],obligations)
    revenue=[{"obligation":x["obligation"],"recognized":cash(x["allocation"]*dec(o["satisfaction_fraction"]))}
             for x,o in zip(allocations,obligations)]
    total=sum((x["recognized"] for x in revenue),dec("0"))
    billing=cash(case.get("billings_to_date","0"))
    if billing<0: raise ReviewRequired("Negative billings require credit/refund workflow")
    net=cash(total-billing)
    entries=[journal(("Dr","contract asset / receivable",total),("Cr","revenue",total))]
    if billing: entries.append(journal(("Dr","receivable",billing),("Cr","contract asset / contract liability",billing)))
    return envelope("SKILL-REV-001",case,"Reviewed five-step revenue model: SSP allocation and evidenced satisfaction",
      {"allocation":allocations,"revenue":revenue,"recognized":total,"billings":billing,
       "net_contract_asset_if_positive_or_liability_if_negative":net},entries,
      ["Contract gate, distinct promises, SSP, transaction price, satisfaction and presentation supplied by reviewer"],
      ["Illustrative journal route requires reconciliation to actual invoice/receivable and contract-balance accounts"],claims)
