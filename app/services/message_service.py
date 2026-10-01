from app.models.schemas import CitizenMessageIn


class MessageService:
    @staticmethod
    def create(request: CitizenMessageIn) -> str:
        if request.route == "human_review":
            return (
                "Uw aanvraag is ontvangen. AI is alleen gebruikt om informatie voor te bereiden. "
                "Vanwege de aard of risico-indicatoren wordt uw aanvraag door een medewerker beoordeeld. "
                "Een mens neemt de beslissing."
            )
        return (
            "Uw aanvraag is ontvangen. AI heeft geholpen bij het voorbereiden van een voorstel: "
            f"{request.proposal} Een bevoegde medewerker blijft verantwoordelijk voor de formele beslissing."
        )
