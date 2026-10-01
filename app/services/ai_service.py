from typing import Any

from app.models.schemas import AIProposal, PseudonymizedApplication


class AIService:
    @staticmethod
    def propose(application: PseudonymizedApplication, policy: dict[str, Any]) -> AIProposal:
        proposal = (
            f"Voorstel: bereid ondersteuning voor de voorziening '{application.requestedProvision}' voor "
            "en laat de formele beslissing door een bevoegde medewerker nemen."
        )
        rationale = (
            f"Onderbouwing: leeftijdsgroep {application.ageGroup}; ernst {application.severity}; "
            f"aanvraag past bij beleidsregel: {policy['rule']}"
        )
        if application.injectForbiddenTermForTest:
            rationale += f" Betrokkene is {application.injectForbiddenTermForTest}."
        return AIProposal(proposal=proposal, rationale=rationale)
