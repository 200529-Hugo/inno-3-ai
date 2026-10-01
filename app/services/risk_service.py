from app.models.schemas import FairnessResult, PseudonymizedApplication, RiskResult


class RiskService:
    @staticmethod
    def calculate(application: PseudonymizedApplication, fairness: FairnessResult) -> RiskResult:
        score = 0.15
        reasons: list[str] = []
        if application.severity == "middel":
            score += 0.25
            reasons.append("ernst is middel")
        if application.severity == "hoog":
            score += 0.60
            reasons.append("ernst is hoog")
        if application.multipleProblems:
            score += 0.25
            reasons.append("meervoudige problematiek")
        if not fairness.passed:
            score += 0.50
            reasons.append("fairness-check gefaald")

        score = min(score, 1.0)
        requires_human = (
            application.severity == "hoog"
            or application.multipleProblems
            or not fairness.passed
            or score >= 0.60
        )
        risk = "hoog" if score >= 0.60 else "middel" if score >= 0.35 else "laag"
        return RiskResult(risk=risk, riskScore=score, requiresHuman=requires_human, reasons=reasons)
