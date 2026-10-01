from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class ApplicationIn(BaseModel):
    citizenId: str = Field(min_length=1)
    name: Optional[str] = None
    address: Optional[str] = None
    birthDate: Optional[str] = None
    ageGroup: Literal["0-17", "18-34", "35-49", "50-64", "65-74", "75+"]
    requestedProvision: Literal["huishoudelijke_hulp", "rolstoel", "woningaanpassing"]
    problemDescription: str = Field(min_length=5)
    severity: Literal["laag", "middel", "hoog"]
    multipleProblems: bool = False
    aiConsent: bool
    injectForbiddenTermForTest: Optional[str] = None


class ValidationResult(BaseModel):
    valid: bool
    errors: List[str] = Field(default_factory=list)


class PseudonymizedApplication(BaseModel):
    citizenToken: str
    ageGroup: str
    requestedProvision: str
    problemDescription: str
    severity: str
    multipleProblems: bool
    injectForbiddenTermForTest: Optional[str] = None


class AIProposal(BaseModel):
    proposal: str
    rationale: str


class FairnessResult(BaseModel):
    passed: bool
    forbiddenTerms: List[str]
    rationalePresent: bool


class RiskResult(BaseModel):
    risk: Literal["laag", "middel", "hoog"]
    riskScore: float
    requiresHuman: bool
    reasons: List[str]


class AuditIn(BaseModel):
    citizenToken: str
    risk: str
    riskScore: float
    flags: Dict[str, Any]
    proposal: str
    rationale: str
    route: str


class AIRequest(BaseModel):
    application: PseudonymizedApplication
    policy: Dict[str, Any]


class RiskRequest(BaseModel):
    application: PseudonymizedApplication
    fairness: FairnessResult


class CitizenMessageIn(BaseModel):
    route: Literal["automatic_message", "human_review"]
    proposal: str


class ReviewDecisionIn(BaseModel):
    decision: Literal["goedgekeurd", "afgewezen", "meer_informatie"]
    notes: str = Field(min_length=3, max_length=2000)
    reviewerName: str = Field(min_length=2, max_length=100)
