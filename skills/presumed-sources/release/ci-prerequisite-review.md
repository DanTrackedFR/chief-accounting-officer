# CI prerequisite correction

The new source-assurance job verifies the complete release receipt by discovering
all seventeen suites. Its initial bootstrap omitted the existing document-test
parser dependencies. Actual initial CI job125443435338 installed openpyxl,
python-docx, pypdf and reportlab; these are not preinstalled on the selected runner.

The corrected workflow installs the unchanged intelligence/requirements.txt plus
reportlab after Python setup and before QA/discovery. Independent engineering
review approved the exact two-file workflow/completion-report patch and found no
other prerequisite gap. No accounting runtime or test-method code changed.

Attempt002 completed3825 distinct tests,17 suites and10 validators with unchanged
source. It remains preserved evidence for that source tree. Attempt003 executes
the exact CI-corrected tree in an isolated detached checkout, at reduced process
priority; the active attempt002 source was not modified or interrupted. Only
attempt003 may be selected as final acceptance. Original probe files remain the
TrackedFR team's separate acceptance; representative engine fixtures are synthetic.
