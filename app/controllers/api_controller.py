from typing import Any

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    AIProposal,
    AIRequest,
    ApplicationIn,
    AuditIn,
    CitizenMessageIn,
    FairnessResult,
    PseudonymizedApplication,
    RiskRequest,
    RiskResult,
    ReviewDecisionIn,
    ValidationResult,
)
from app.services.ai_service import AIService
from app.services.audit_service import AuditService
from app.services.fairness_service import FairnessService
from app.services.message_service import MessageService
from app.services.policy_service import PolicyService
from app.services.privacy_service import PrivacyService
from app.services.processing_service import InvalidApplicationError, ProcessingService
from app.services.risk_service import RiskService
from app.services.review_service import ReviewService
from app.services.validation_service import ValidationService


router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/validate", response_model=ValidationResult)
def validate_endpoint(application: ApplicationIn) -> ValidationResult:
    return ValidationService.validate(application)


@router.post("/pseudonymize", response_model=PseudonymizedApplication)
def pseudonymize_endpoint(application: ApplicationIn) -> PseudonymizedApplication:
    validation = ValidationService.validate(application)
    if not validation.valid:
        raise HTTPException(status_code=422, detail=validation.errors)
    return PrivacyService.minimize(application)


@router.get("/policy/{provision}")
def policy_endpoint(provision: str) -> dict[str, Any]:
    policy = PolicyService.get(provision)
    if policy is None:
        raise HTTPException(status_code=404, detail="Onbekende voorziening")
    return policy


@router.post("/ai/propose", response_model=AIProposal)
def ai_endpoint(request: AIRequest) -> AIProposal:
    return AIService.propose(request.application, request.policy)


@router.post("/fairness/check", response_model=FairnessResult)
def fairness_endpoint(proposal: AIProposal) -> FairnessResult:
    return FairnessService.check(proposal)


@router.post("/risk", response_model=RiskResult)
def risk_endpoint(request: RiskRequest) -> RiskResult:
    return RiskService.calculate(request.application, request.fairness)


@router.post("/audit")
def audit_endpoint(audit: AuditIn) -> dict[str, Any]:
    return AuditService.create(audit)


@router.get("/audit")
def list_audit() -> list[dict[str, Any]]:
    return AuditService.list_recent()


@router.get("/reviews")
def list_reviews() -> list[dict[str, Any]]:
    return ReviewService.list_cases()


@router.post("/reviews/{audit_id}/decision")
def save_review_decision(audit_id: str, request: ReviewDecisionIn) -> dict[str, Any]:
    result = ReviewService.decide(audit_id, request)
    if result is None:
        raise HTTPException(status_code=404, detail="Reviewzaak niet gevonden")
    return result


@router.post("/citizen-message")
def citizen_message(request: CitizenMessageIn) -> dict[str, str]:
    return {"message": MessageService.create(request)}


@router.post("/process")
def process(application: ApplicationIn) -> dict[str, Any]:
    try:
        return ProcessingService.process(application)
    except InvalidApplicationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors) from exc
