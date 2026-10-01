"""Deterministic fixed-payment lease arithmetic; no accounting policy inference."""
from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")

def d(value):
    if isinstance(value, float):
        raise TypeError("Pass Decimal or string, never binary floats")
    return Decimal(str(value))

def money(value):
    return d(value).quantize(CENT, rounding=ROUND_HALF_UP)

def present_value(payments, periodic_rate):
    """payments: sequence of (integer period index, amount), 0 = commencement."""
    r = d(periodic_rate)
    if r <= -1:
        raise ValueError("Periodic rate must exceed -100%")
    if not payments:
        raise ValueError("Provide at least one payment")
    result = Decimal("0")
    for period, amount in payments:
        if not isinstance(period, int) or period < 0 or d(amount) < 0:
            raise ValueError("Payment period must be nonnegative integer and amount nonnegative")
        result += d(amount) / (Decimal(1) + r) ** period
    return money(result)

def initial_measurement(unpaid_payments, periodic_rate, *, prepayments="0", direct_costs="0", incentives="0", restoration="0"):
    """Unpaid payments must have period >= 1; commencement cash is a prepayment."""
    if any(period < 1 for period, _ in unpaid_payments):
        raise ValueError("Commencement payments belong in prepayments, not liability")
    liability = present_value(unpaid_payments, periodic_rate)
    rou = money(liability + d(prepayments) + d(direct_costs) - d(incentives) + d(restoration))
    if rou < 0:
        raise ValueError("Negative ROU amount requires separate technical review")
    return {"lease_liability": liability, "rou_asset": rou}

def liability_schedule(opening_liability, payments, periodic_rate, *, final_rounding_tolerance="0.02"):
    """End-of-period cash payments; amounts and interest rounded to cents each period."""
    opening = money(opening_liability)
    rate = d(periodic_rate)
    if rate <= -1:
        raise ValueError("Periodic rate must exceed -100%")
    rows = []
    for index, payment in enumerate(payments, 1):
        cash = money(payment)
        if cash < 0:
            raise ValueError("Negative payments need separate treatment")
        interest = money(opening * rate)
        closing = money(opening + interest - cash)
        rows.append({"period": index, "opening": opening, "interest": interest, "payment": cash, "closing": closing})
        opening = closing
    if abs(opening) > d(final_rounding_tolerance):
        raise ValueError(f"Unreconciled closing liability {opening}; check payment population, rate and term")
    return rows

def level_payment(present_value_amount, periodic_rate, periods):
    if not isinstance(periods, int) or periods <= 0:
        raise ValueError("Periods must be positive integer")
    pv, rate = d(present_value_amount), d(periodic_rate)
    if pv < 0 or rate <= -1:
        raise ValueError("Invalid PV or rate")
    if rate == 0:
        return money(pv / periods)
    return money(pv * rate / (Decimal(1) - (Decimal(1) + rate) ** (-periods)))
