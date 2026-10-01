import os


PSEUDONYM_SALT = os.getenv("PSEUDONYM_SALT", "hackathon-demo-salt-change-me")

FORBIDDEN_TERMS = [
    "religie", "geloof", "moslim", "christen", "joods", "ras", "huidskleur",
    "nationaliteit", "nederlander", "marokkaan", "turk", "geslacht", "man", "vrouw",
    "seksuele geaardheid", "homoseksueel", "transgender",
]

POLICIES = {
    "huishoudelijke_hulp": {
        "rule": "Ondersteuning kan worden voorbereid wanneer beperkingen de zelfredzaamheid in het huishouden aantoonbaar belemmeren.",
        "required_evidence": ["beperking", "ondersteuningsbehoefte"],
    },
    "rolstoel": {
        "rule": "Een rolstoelvoorziening kan worden voorbereid wanneer langdurige mobiliteitsbeperkingen zelfstandig verplaatsen wezenlijk beperken.",
        "required_evidence": ["mobiliteitsbeperking", "duur"],
    },
    "woningaanpassing": {
        "rule": "Een woningaanpassing kan worden voorbereid wanneer de huidige woning door beperkingen niet veilig of passend bruikbaar is.",
        "required_evidence": ["belemmering woning", "veiligheid of toegankelijkheid"],
    },
}
