# Public accounting output boundary

No runnable CAO application, retrieval service or production renderer is present in this repository at the Phase 2E audit snapshot. `public_output.py` is an executable interface contract for future adapters. Its contract tests are runnable; production integration and runtime verification remain pending.

Every future route must call `public_record` before model context, retrieval, answers, citations, tool responses, user-visible logs or exports. Use curated guidance, public accounting caveats and period/scope fields. Never hand raw topic files, claim registers or provenance to a model that writes user answers. Unknown fields are excluded recursively; contaminated allowlisted text fails closed and must be curated without deleting accounting uncertainty.

This control governs application output. Internal evidence remains reviewable in the repository and is not confidential from repository readers. Extend the registered route list and tests before adding an output adapter.

Run `python -m unittest discover -s tests -p 'test_*.py'` from the repository root.
