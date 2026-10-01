# BPMN en architectuur

## BPMN-logica
Gebruik onderstaande Mermaid als snelle visualisatie of teken hem na in draw.io/BPMN-tool.

```mermaid
flowchart LR
    A([Start: WMO-aanvraag]) --> B[Valideer invoer en AI-toestemming]
    B -->|ongeldig / geen toestemming| C[Retourneer duidelijke fout]
    C --> Z([Einde])
    B -->|geldig| D[Minimaliseer data]
    D --> E[Pseudonimiseer citizenId naar token]
    E --> F[Haal beleidsregel op]
    F --> G[AI-stub genereert voorstel + onderbouwing]
    G --> H[Fairness-check]
    H --> I[Bereken risico]
    I --> J{Hoog risico / ernst hoog / fairness flag?}
    J -->|ja| K[Menselijke beoordelaar]
    J -->|nee| L[Transparant burgerbericht]
    K --> M[Audit-log]
    L --> M
    M --> Z
```

## Architectuur

```mermaid
flowchart TB
    Client[Demo client / curl / Postman] --> N8N[n8n workflow]
    N8N --> API[FastAPI services]
    API --> VAL[Validation + minimisation]
    API --> PSEU[Pseudonymisation]
    API --> POL[Policy mock]
    API --> AI[Deterministic AI stub]
    API --> FAIR[Fairness check]
    API --> RISK[Risk engine]
    API --> DB[(PostgreSQL audit log)]
    RISK -->|safe| MSG[Citizen message]
    RISK -->|risk/flag| HUMAN[Human reviewer route]
```

## Privacygrens
Persoonsgegevens komen de API binnen voor validatie maar worden vóór de AI-stap verwijderd. De AI-stub krijgt alleen token, leeftijdsgroep, voorziening, beschrijving, ernst en beleidscontext. In een echte productieomgeving moet vrije tekst aanvullend door PII-detectie/redactie en moeten toegang, encryptie, bewaartermijnen en logging uitgebreider worden ingericht.
