import re

from app.config import FORBIDDEN_TERMS
from app.models.schemas import AIProposal, FairnessResult


class FairnessService:
    @staticmethod
    def check(proposal: AIProposal) -> FairnessResult:
        text = f"{proposal.proposal} {proposal.rationale}".lower()
        found = sorted({
            term for term in FORBIDDEN_TERMS
            if re.search(rf"\b{re.escape(term)}\b", text)
        })
        rationale_present = bool(proposal.rationale.strip())
        return FairnessResult(
            passed=(not found and rationale_present),
            forbiddenTerms=found,
            rationalePresent=rationale_present,
        )
