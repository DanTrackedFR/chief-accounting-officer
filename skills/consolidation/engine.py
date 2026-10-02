"""Simple full-consolidation aggregation and matched intercompany elimination workpaper."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core_accounting import dec,cash,required,context,ReviewRequired,journal,envelope

TOPICS=["TOPIC-07-001","TOPIC-07-002","TOPIC-07-003","TOPIC-07-004","TOPIC-07-005"]

def run(case,claims):
    context(case);required(case,"control_assessment_approved","entities","intercompany_pairs","aligned_policies","aligned_reporting_dates")
    if case["control_assessment_approved"] is not True: raise ReviewRequired("Consolidation perimeter not approved")
    if case["aligned_policies"] is not True or case["aligned_reporting_dates"] is not True:
        raise ReviewRequired("Harmonize policies/reporting dates before consolidation")
    if case.get("acquisition_or_disposal") or case.get("foreign_currency_unresolved") or case.get("unrealized_profit_unresolved"):
        raise ReviewRequired("Specialist acquisition, FX or unrealized-profit schedule required")
    totals={}
    for entity in case["entities"]:
        required(entity,"id","balances","in_scope")
        if entity["in_scope"] is not True: raise ReviewRequired("Exclude unconsolidated entity or resolve scope")
        for account,amount in entity["balances"].items():
            totals[account]=cash(totals.get(account,dec("0"))+dec(amount))
    entries=[]
    for pair in case["intercompany_pairs"]:
        required(pair,"receivable_entity","payable_entity","receivable_account","payable_account","amount","matched")
        if pair["matched"] is not True: raise ReviewRequired("Unreconciled intercompany balance")
        amount=cash(pair["amount"])
        if amount<0: raise ReviewRequired("Negative elimination requires reviewed direction")
        ra,pa=pair["receivable_account"],pair["payable_account"]
        if totals.get(ra,0)<amount or totals.get(pa,0)>-amount:
            raise ReviewRequired("Elimination exceeds matched receivable/payable balance")
        totals[ra]=cash(totals[ra]-amount);totals[pa]=cash(totals[pa]+amount)
        entries.append(journal(("Dr",pa,amount),("Cr",ra,amount)))
    return envelope("SKILL-CONS-001",case,"Approved full-consolidation perimeter, aligned TB aggregation and matched balance elimination",
      {"consolidated_balances":totals,"elimination_count":len(entries)},entries,
      ["Control, NCI, opening investment/equity elimination and group policy alignment require separate approved schedules"],
      ["This workpaper does not automatically eliminate investment/equity, unrealized profits, transactions, FX or calculate NCI; do not use its balances as completed group financial statements"],claims)
