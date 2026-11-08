"""Include independent bounded runner governance QA in permanent discovery."""
import importlib.util
from pathlib import Path

_path = Path(__file__).resolve().parents[1] / 'tests/fixtures/phase_a_v1/runner.py'
_spec = importlib.util.spec_from_file_location('independent_runner_recovery_qa', _path)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
IndependentRunnerContract = _module.IndependentRunnerContract
