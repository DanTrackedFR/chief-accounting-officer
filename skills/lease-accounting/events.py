"""Lease event router. Implements only event mechanics supported by the vertical slice."""
from lease_math import money, present_value

class EventReviewRequired(ValueError): pass

def assess_modification(event):
    required=("adds_right_of_use","consideration_commensurate","scope_decrease","remaining_payments","revised_periodic_rate")
    missing=[x for x in required if x not in event]
    if missing: raise EventReviewRequired("Missing modification facts: "+", ".join(missing))
    if event["adds_right_of_use"] and event["consideration_commensurate"]:
        return {"treatment":"separate_lease","calculation":None,
                "review":"Create a new lease schedule; retain the existing lease unchanged subject to framework-specific review."}
    if event["scope_decrease"]:
        raise EventReviewRequired("Scope-decrease/partial-termination accounting requires framework-specific carrying-amount and gain/loss inputs; route to TOPIC-04-009.")
    payments=event["remaining_payments"]
    if not payments: raise EventReviewRequired("Remaining payment population required")
    remeasured=present_value([(i+1,money(x)) for i,x in enumerate(payments)],event["revised_periodic_rate"])
    return {"treatment":"remeasure_existing_lease","remeasured_liability":remeasured,
            "review":"Adjust the ROU asset/liability only after confirming the event-specific framework rule and discount-rate treatment in TOPIC-04-009."}

def reassessment(event):
    kind=event.get("kind")
    if kind not in ("term_or_option","index_or_rate","in_substance_fixed"):
        raise EventReviewRequired("Unregistered reassessment type")
    if not event.get("remaining_payments"):
        raise EventReviewRequired("Revised remaining payments required")
    if event.get("periodic_rate") in (None,""):
        raise EventReviewRequired("Supported periodic rate required; whether it is revised or unchanged is a framework decision")
    amount=present_value([(i+1,money(x)) for i,x in enumerate(event["remaining_payments"])],event["periodic_rate"])
    return {"treatment":"remeasure_existing_lease","event_type":kind,"remeasured_liability":amount,
            "review":"Rate selection must be evidenced under the applicable framework/event rule before posting."}
