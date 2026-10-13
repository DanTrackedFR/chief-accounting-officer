"""Deterministic successor to the immutable Borrowing Costs history reviewer.

Opaque version inventories are consumers, not identity authorities. Compare
structured producers across every file first, then verify inventory membership
against the resulting bijection. Never infer mappings by zipping inventories.
The original reviewer and all historical accounting artifacts remain unchanged.
"""
import importlib.util
from pathlib import Path

LOCATION = Path(__file__).resolve().parents[1] / "recovery/borrowing-costs-pr42/check_identity_transition.py"
SPEC = importlib.util.spec_from_file_location("_frozen_borrowing_history_review", LOCATION)
ORIGINAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ORIGINAL)
HEX = ORIGINAL.HEX
expand = ORIGINAL.expand
INVENTORIES = frozenset(("result_versions", "required_legal_result_versions",
                        "superseded_excluded", "journal_versions_preserved",
                        "conflicts", "bundle_ids"))


class Transition(ORIGINAL.Transition):
    def __init__(self):
        super().__init__()
        self.pending_inventories = []

    def seed(self, old, current, path=""):
        # Preserve the frozen reviewer's unique-role inference for historical
        # singleton references that have no separate scalar producer. Establish
        # these before any multi-member inventory is checked; never zip an
        # ambiguous population to manufacture identity bindings.
        if (isinstance(old, list) and isinstance(current, list)
                and path.split("/")[-1] in INVENTORIES
                and len(old) == len(current) == 1
                and isinstance(old[0], str) and isinstance(current[0], str)):
            self.strings(old[0], current[0], path + "/unique-role")
        super().seed(old, current, path)

    def compare(self, old, current, path=""):
        if (isinstance(old, list) and isinstance(current, list)
                and path.split("/")[-1] in INVENTORIES
                and all(isinstance(value, str) for value in old + current)):
            self.pending_inventories.append((list(old), list(current), path))
            return
        super().compare(old, current, path)

    def finish(self):
        """Check exact populations without adding any new provenance bindings."""
        for old, current, path in self.pending_inventories:
            normalized = []
            for value in old:
                for identity in HEX.findall(value):
                    if identity not in self.forward and identity not in self.stable:
                        # An identical member needs no migration authorization.
                        if value not in current:
                            self.errors.append({"path": path, "reason": "unanchored inventory identity", "old": identity})
                normalized.append(HEX.sub(lambda match: self.forward.get(match[0], match[0]), value))
            if sorted(normalized) != sorted(current):
                self.errors.append({"path": path, "reason": "inventory members changed",
                                    "old": sorted(normalized), "new": sorted(current)})
        self.pending_inventories.clear()
        return not self.errors
