"""Explicit nonproduction accounting-knowledge boundary."""
from core_accounting import ReviewRequired

def assess(case,claims):
    raise ReviewRequired('NONPRODUCTION: no substantive approved grant recognition/measurement knowledge exists.')
