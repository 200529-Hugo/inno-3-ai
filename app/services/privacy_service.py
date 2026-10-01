import hashlib
import re

from app.config import PSEUDONYM_SALT
from app.models.schemas import ApplicationIn, PseudonymizedApplication


class PrivacyService:
    PII_PATTERNS = [
        r"\b[1-9][0-9]{8}\b",
        r"\b[1-9][0-9]{3}\s?[A-Z]{2}\b",
        r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b",
        r"(?<!\d)(?:\+31|0)[1-9](?:[\s-]?\d){8}(?!\d)",
        r"\b\d{4}-\d{2}-\d{2}\b",
    ]

    @staticmethod
    def token_for(citizen_id: str) -> str:
        digest = hashlib.sha256(f"{PSEUDONYM_SALT}:{citizen_id}".encode()).hexdigest()[:12]
        return f"CIT-{digest}"

    @classmethod
    def redact_personal_data(cls, text: str, application: ApplicationIn) -> str:
        redacted = text
        for value in [application.citizenId, application.name, application.address, application.birthDate]:
            if value:
                redacted = re.sub(
                    re.escape(value),
                    "[PERSOONSGEGEVEN VERWIJDERD]",
                    redacted,
                    flags=re.IGNORECASE,
                )
        for pattern in cls.PII_PATTERNS:
            redacted = re.sub(pattern, "[PERSOONSGEGEVEN VERWIJDERD]", redacted, flags=re.IGNORECASE)
        return redacted

    @classmethod
    def minimize(cls, application: ApplicationIn) -> PseudonymizedApplication:
        return PseudonymizedApplication(
            citizenToken=cls.token_for(application.citizenId),
            ageGroup=application.ageGroup,
            requestedProvision=application.requestedProvision,
            problemDescription=cls.redact_personal_data(application.problemDescription, application),
            severity=application.severity,
            multipleProblems=application.multipleProblems,
            injectForbiddenTermForTest=application.injectForbiddenTermForTest,
        )
