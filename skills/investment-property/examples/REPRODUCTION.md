# Reproduce new Investment Property examples

From repository root:

```
PYTHONHASHSEED=19 python skills/tests/generate_investment_property_examples.py --verify
PYTHONHASHSEED=941 python skills/tests/generate_investment_property_examples.py --verify
python skills/run_skill.py investment-property skills/investment-property/examples/production/IFRS-fair_value-hold.case.json
```

Each scenario contains an ordinary runtime Case, internal result, curated public
output, calculation schedule and proposed journals. source-evidence-manifest.json
binds exact file and original-source capture hashes, supported status and expected
calculations. All records/values/approvals are explicitly synthetic. Amounts and
balanced journals are independently challenged; this generator is an author tool,
not independent certification. `--verify` is read-only and reproduces exact bytes.
Generation touches only new IP production examples; original0.1.0 and all historical
CAO artifacts are preserved. Incomplete certification emits no released journals.
