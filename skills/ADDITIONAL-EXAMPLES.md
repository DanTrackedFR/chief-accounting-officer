# Additional accounting workflow examples

Each supported package has four synthetic reviewed input templates and public exports under `examples/`: IFRS, US_GAAP, UK_GAAP and AASB. These are illustrative entities, judgments and amounts, never real company facts or authenticated approvals. The expected exports deliberately say **partial** because no independent case approval is fabricated.

Run `python skills/run_skill.py PACKAGE skills/PACKAGE/examples/FRAMEWORK.case.json --route export`. Read the package's methods and current canonical documents before using an input template. The saved knowledge-review population/hash record is a synthetic example of the required record, not evidence that a real company review occurred. Production use needs company source facts, applicable claim selection and an actual independent reviewer signoff bound to `case_fingerprint`.

The end-to-end test fixture independently regenerates clearly labeled synthetic certification records, tests complete envelopes and checks all seven public routes. Saved-example tests execute the CLI against all twenty input/export pairs. The tax package has no fake numerical example: it returns a blocked handoff until approved tax knowledge exists.

Worked numerical and adverse examples are also documented in each methods.md, including acquisition NCI/cost alternatives, impairment floors/reversal ceilings, carried CTA, three-year equity/cash award schedules and IFRS18/MPM subtotals.
