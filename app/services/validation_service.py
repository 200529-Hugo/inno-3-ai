from app.models.schemas import ApplicationIn, ValidationResult


class ValidationService:
    @staticmethod
    def validate(application: ApplicationIn) -> ValidationResult:
        errors: list[str] = []
        if not application.aiConsent:
            errors.append("AI-toestemming ontbreekt: aiConsent moet true zijn voor AI-ondersteunde voorbereiding.")
        if any(term in application.problemDescription.lower() for term in ["bsn", "burgerservicenummer"]):
            errors.append("Beschrijving lijkt een BSN te bevatten; verwijder persoonsgegevens uit vrije tekst.")
        return ValidationResult(valid=not errors, errors=errors)
