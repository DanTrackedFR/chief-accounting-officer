"""Explicit nonproduction accounting-knowledge boundary."""
from core_accounting import ReviewRequired

def assess(case,claims):
    raise ReviewRequired('NONPRODUCTION: incidental CIP/interest routing is not a substantive capitalization method.')
