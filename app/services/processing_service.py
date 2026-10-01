from typing import Any

from app.models.schemas import ApplicationIn, AuditIn, CitizenMessageIn
from app.services.ai_service import AIService
from app.services.audit_service import AuditService
from app.services.fairness_service import FairnessService
from app.services.message_service import MessageService
from app.services.policy_service import PolicyService
from app.services.privacy_service import PrivacyService
from app.services.risk_service import RiskService
from app.services.validation_service import ValidationService


class InvalidApplicationError(Exception):
    def __init__(self, errors: list[str]):
        super().__init__("; ".join(errors))
        self.errors = errors


class ProcessingService:
    @staticmethod
    def process(application: ApplicationIn) -> dict[str, Any]:
        validation = ValidationService.validate(application)
        if not validation.valid:
            raise InvalidApplicationError(validation.errors)

        minimized = PrivacyService.minimize(application)
        policy = PolicyService.get(minimized.requestedProvision)
        if policy is None:
            raise ValueError("Onbekende voorziening")

        proposal = AIService.propose(minimized, policy)
        fairness = FairnessService.check(proposal)
        risk = RiskService.calculate(minimized, fairness)
        route = "human_review" if risk.requiresHuman else "automatic_message"
        audit = AuditService.create(AuditIn(
            citizenToken=minimized.citizenToken,
            risk=risk.risk,
            riskScore=risk.riskScore,
            flags={
                "fairness": fairness.model_dump(),
                "riskReasons": risk.reasons,
                "application": minimized.model_dump(exclude={"injectForbiddenTermForTest"}),
            },
            proposal=proposal.proposal,
            rationale=proposal.rationale,
            route=route,
        ))
        citizen_message = MessageService.create(CitizenMessageIn(route=route, proposal=proposal.proposal))

        return {
            "validation": validation,
            "minimizedApplication": minimized,
            "policy": policy,
            "proposal": proposal,
            "fairness": fairness,
            "risk": risk,
            "route": route,
            "citizenMessage": citizen_message,
            "audit": audit,
        }
