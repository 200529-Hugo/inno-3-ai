import hashlib
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sqlalchemy import JSON, DateTime, Float, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./wmo_audit.db")
PSEUDONYM_SALT = os.getenv("PSEUDONYM_SALT", "hackathon-demo-salt-change-me")
engine = create_engine(DATABASE_URL, future=True)


class Base(DeclarativeBase):
    pass


class AuditRecord(Base):
    __tablename__ = "audit_records"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    citizen_token: Mapped[str] = mapped_column(String, index=True)
    risk: Mapped[str] = mapped_column(String)
    risk_score: Mapped[float] = mapped_column(Float)
    flags: Mapped[dict] = mapped_column(JSON)
    proposal: Mapped[str] = mapped_column(String)
    rationale: Mapped[str] = mapped_column(String)
    route: Mapped[str] = mapped_column(String)


Base.metadata.create_all(engine)
app = FastAPI(title="WMO AI Preparation Service", version="1.0.0")
STATIC_DIR = Path(__file__).parent / "static"

FORBIDDEN_TERMS = [
    "religie", "geloof", "moslim", "christen", "joods", "ras", "huidskleur",
    "nationaliteit", "nederlander", "marokkaan", "turk", "geslacht", "man", "vrouw",
    "seksuele geaardheid", "homoseksueel", "transgender"
]

POLICIES = {
    "huishoudelijke_hulp": {
        "rule": "Ondersteuning kan worden voorbereid wanneer beperkingen de zelfredzaamheid in het huishouden aantoonbaar belemmeren.",
        "required_evidence": ["beperking", "ondersteuningsbehoefte"]
    },
    "rolstoel": {
        "rule": "Een rolstoelvoorziening kan worden voorbereid wanneer langdurige mobiliteitsbeperkingen zelfstandig verplaatsen wezenlijk beperken.",
        "required_evidence": ["mobiliteitsbeperking", "duur"]
    },
    "woningaanpassing": {
        "rule": "Een woningaanpassing kan worden voorbereid wanneer de huidige woning door beperkingen niet veilig of passend bruikbaar is.",
        "required_evidence": ["belemmering woning", "veiligheid of toegankelijkheid"]
    }
}


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


def token_for(citizen_id: str) -> str:
    digest = hashlib.sha256(f"{PSEUDONYM_SALT}:{citizen_id}".encode()).hexdigest()[:12]
    return f"CIT-{digest}"


def validate_application(a: ApplicationIn) -> ValidationResult:
    errors: List[str] = []
    if not a.aiConsent:
        errors.append("AI-toestemming ontbreekt: aiConsent moet true zijn voor AI-ondersteunde voorbereiding.")
    if any(x in a.problemDescription.lower() for x in ["bsn", "burgerservicenummer"]):
        errors.append("Beschrijving lijkt een BSN te bevatten; verwijder persoonsgegevens uit vrije tekst.")
    return ValidationResult(valid=not errors, errors=errors)


def redact_personal_data(text: str, a: ApplicationIn) -> str:
    """Remove structured and commonly formatted PII before the AI boundary."""
    redacted = text
    structured_values = [a.citizenId, a.name, a.address, a.birthDate]
    for value in structured_values:
        if value:
            redacted = re.sub(re.escape(value), "[PERSOONSGEGEVEN VERWIJDERD]", redacted, flags=re.IGNORECASE)

    pii_patterns = [
        r"\b[1-9][0-9]{8}\b",  # BSN-like number (demo heuristic)
        r"\b[1-9][0-9]{3}\s?[A-Z]{2}\b",  # Dutch postcode
        r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b",  # email address
        r"(?<!\d)(?:\+31|0)[1-9](?:[\s-]?\d){8}(?!\d)",  # Dutch phone number
        r"\b\d{4}-\d{2}-\d{2}\b",  # ISO date, including birth dates
    ]
    for pattern in pii_patterns:
        redacted = re.sub(pattern, "[PERSOONSGEGEVEN VERWIJDERD]", redacted, flags=re.IGNORECASE)
    return redacted


def minimize(a: ApplicationIn) -> PseudonymizedApplication:
    return PseudonymizedApplication(
        citizenToken=token_for(a.citizenId),
        ageGroup=a.ageGroup,
        requestedProvision=a.requestedProvision,
        problemDescription=redact_personal_data(a.problemDescription, a),
        severity=a.severity,
        multipleProblems=a.multipleProblems,
        injectForbiddenTermForTest=a.injectForbiddenTermForTest,
    )


def ai_stub(a: PseudonymizedApplication, policy: Dict[str, Any]) -> AIProposal:
    proposal = f"Voorstel: bereid ondersteuning voor de voorziening '{a.requestedProvision}' voor en laat de formele beslissing door een bevoegde medewerker nemen."
    rationale = f"Onderbouwing: leeftijdsgroep {a.ageGroup}; ernst {a.severity}; aanvraag past bij beleidsregel: {policy['rule']}"
    if a.injectForbiddenTermForTest:
        rationale += f" Betrokkene is {a.injectForbiddenTermForTest}."
    return AIProposal(proposal=proposal, rationale=rationale)


def fairness_check(p: AIProposal) -> FairnessResult:
    text = f"{p.proposal} {p.rationale}".lower()
    found = sorted({term for term in FORBIDDEN_TERMS if re.search(rf"\b{re.escape(term)}\b", text)})
    return FairnessResult(passed=(len(found) == 0 and bool(p.rationale.strip())), forbiddenTerms=found, rationalePresent=bool(p.rationale.strip()))


def calculate_risk(a: PseudonymizedApplication, fair: FairnessResult) -> RiskResult:
    score = 0.15
    reasons = []
    if a.severity == "middel":
        score += 0.25
        reasons.append("ernst is middel")
    if a.severity == "hoog":
        score += 0.60
        reasons.append("ernst is hoog")
    if a.multipleProblems:
        score += 0.25
        reasons.append("meervoudige problematiek")
    if not fair.passed:
        score += 0.50
        reasons.append("fairness-check gefaald")
    score = min(score, 1.0)
    requires_human = a.severity == "hoog" or a.multipleProblems or not fair.passed or score >= 0.60
    risk = "hoog" if score >= 0.60 else "middel" if score >= 0.35 else "laag"
    return RiskResult(risk=risk, riskScore=score, requiresHuman=requires_human, reasons=reasons)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/validate", response_model=ValidationResult)
def validate_endpoint(a: ApplicationIn):
    return validate_application(a)


@app.post("/pseudonymize", response_model=PseudonymizedApplication)
def pseudonymize_endpoint(a: ApplicationIn):
    validation = validate_application(a)
    if not validation.valid:
        raise HTTPException(status_code=422, detail=validation.errors)
    return minimize(a)


@app.get("/policy/{provision}")
def policy_endpoint(provision: str):
    if provision not in POLICIES:
        raise HTTPException(status_code=404, detail="Onbekende voorziening")
    return POLICIES[provision]


class AIRequest(BaseModel):
    application: PseudonymizedApplication
    policy: Dict[str, Any]


@app.post("/ai/propose", response_model=AIProposal)
def ai_endpoint(req: AIRequest):
    return ai_stub(req.application, req.policy)


@app.post("/fairness/check", response_model=FairnessResult)
def fairness_endpoint(p: AIProposal):
    return fairness_check(p)


class RiskRequest(BaseModel):
    application: PseudonymizedApplication
    fairness: FairnessResult


@app.post("/risk", response_model=RiskResult)
def risk_endpoint(req: RiskRequest):
    return calculate_risk(req.application, req.fairness)


@app.post("/audit")
def audit_endpoint(a: AuditIn):
    record_id = str(uuid.uuid4())
    record = AuditRecord(
        id=record_id,
        created_at=datetime.now(timezone.utc),
        citizen_token=a.citizenToken,
        risk=a.risk,
        risk_score=a.riskScore,
        flags=a.flags,
        proposal=a.proposal,
        rationale=a.rationale,
        route=a.route,
    )
    with Session(engine) as session:
        session.add(record)
        session.commit()
    return {"logged": True, "auditId": record_id}


@app.get("/audit")
def list_audit():
    with Session(engine) as session:
        records = session.query(AuditRecord).order_by(AuditRecord.created_at.desc()).limit(100).all()
        return [
            {
                "id": r.id,
                "createdAt": r.created_at,
                "citizenToken": r.citizen_token,
                "risk": r.risk,
                "riskScore": r.risk_score,
                "flags": r.flags,
                "proposal": r.proposal,
                "rationale": r.rationale,
                "route": r.route,
            }
            for r in records
        ]


class CitizenMessageIn(BaseModel):
    route: Literal["automatic_message", "human_review"]
    proposal: str


@app.post("/citizen-message")
def citizen_message(req: CitizenMessageIn):
    if req.route == "human_review":
        return {
            "message": "Uw aanvraag is ontvangen. AI is alleen gebruikt om informatie voor te bereiden. Vanwege de aard of risico-indicatoren wordt uw aanvraag door een medewerker beoordeeld. Een mens neemt de beslissing."
        }
    return {
        "message": f"Uw aanvraag is ontvangen. AI heeft geholpen bij het voorbereiden van een voorstel: {req.proposal} Een bevoegde medewerker blijft verantwoordelijk voor de formele beslissing."
    }


@app.post("/process")
def process(a: ApplicationIn):
    validation = validate_application(a)
    if not validation.valid:
        raise HTTPException(status_code=422, detail=validation.errors)
    minimized = minimize(a)
    policy = POLICIES[minimized.requestedProvision]
    proposal = ai_stub(minimized, policy)
    fair = fairness_check(proposal)
    risk = calculate_risk(minimized, fair)
    route = "human_review" if risk.requiresHuman else "automatic_message"
    audit = audit_endpoint(AuditIn(
        citizenToken=minimized.citizenToken,
        risk=risk.risk,
        riskScore=risk.riskScore,
        flags={"fairness": fair.model_dump(), "riskReasons": risk.reasons},
        proposal=proposal.proposal,
        rationale=proposal.rationale,
        route=route,
    ))
    message = citizen_message(CitizenMessageIn(route=route, proposal=proposal.proposal))
    return {
        "validation": validation,
        "minimizedApplication": minimized,
        "policy": policy,
        "proposal": proposal,
        "fairness": fair,
        "risk": risk,
        "route": route,
        "citizenMessage": message["message"],
        "audit": audit,
    }
