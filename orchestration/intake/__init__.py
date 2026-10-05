"""Semantic proposal -> deterministic validation -> candidates -> existing CAO."""
from .sources import RawSource, Inventory
from .semantic import Claim, FactCandidate, StructuredProposal, RequestContext, SemanticPlanner, FixturePlanner, ProposalValidator
from .preparation import Intake, IntakeResult, Binding, ReviewedInputPack, PopulationBinding, DocumentBinding, TextAssertion
