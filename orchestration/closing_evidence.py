"""Validation of supplied closing quote evidence; no rates or accounting generated."""
from decimal import Decimal


def validate_quote_sheet(sheet, closing_date, retained_presentation_quotes):
    if sheet.get('reviewed') is not True or sheet.get('valuation_date')!=closing_date:
        raise ValueError('Reviewed closing-date quote sheet required')
    quotes={key:Decimal(str(sheet[key])) for key in ('gbp_per_usd','eur_per_usd','eur_per_gbp')}
    if any(not value.is_finite() or value<=0 for value in quotes.values()):
        raise ValueError('Finite positive supplied closing quotes required')
    if quotes['gbp_per_usd']*quotes['eur_per_gbp']!=quotes['eur_per_usd']:
        raise ValueError('Closing quote evidence is internally contradictory; no inferred replacement quote')
    for key,value in retained_presentation_quotes.items():
        if quotes[key]!=Decimal(str(value)):
            raise ValueError('Closing sheet requires separately reviewed replacement of retained presentation quote')
    return quotes
