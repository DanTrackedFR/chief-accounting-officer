"""Fail closed until a governed tax knowledge extension has been approved."""
from core_accounting import ReviewRequired

def assess(case,claims):
    raise ReviewRequired('Income taxes has no approved canonical topic or framework claim registers. No tax calculation or conclusion may be certified.')
