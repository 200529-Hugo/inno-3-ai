# WMO AI Hackathon Prototype

Dit project demonstreert privacy-by-design, fairness, human-in-the-loop, transparantie en auditbaarheid voor de voorbereiding van synthetische WMO-aanvragen.

## Belangrijk
Gebruik uitsluitend synthetische testdata. Dit is een onderwijsprototype, geen productie- of juridisch beslissysteem.

## Architectuur
- n8n: workflow-entry en validatieroutering
- FastAPI: validatie, pseudonimisering, policy mock, AI-stub, fairness, risico, burgerbericht en audit API
- PostgreSQL: audit-log
- Docker Compose: reproduceerbare installatie

## Starten
Vereist: Docker Desktop / Docker Engine met Compose.

```bash
docker compose up --build
```

Open daarna:
- API Swagger: http://localhost:8000/docs
- n8n: http://localhost:5678

Bij eerste n8n-start maak je lokaal een eigenaar-account aan. Importeer `n8n/wmo-workflow.json` en activeer de workflow.

## Snelle API-demo zonder n8n

```bash
curl -X POST http://localhost:8000/process \
  -H 'Content-Type: application/json' \
  --data-binary @examples/testcase1-low-risk.json
```

Herhaal met testcase 2, 3 en 4.

Audit bekijken:

```bash
curl http://localhost:8000/audit
```

## n8n-demo
Na import/activatie is de webhook in een standaard lokale installatie bedoeld als:

`POST http://localhost:5678/webhook/wmo-application`

Voorbeeld:

```bash
curl -X POST http://localhost:5678/webhook/wmo-application \
  -H 'Content-Type: application/json' \
  --data-binary @examples/testcase1-low-risk.json
```

Als n8n na import een andere test-/production webhook-URL toont, gebruik de URL die in de Webhook-node staat. Exporteer na jullie eigen import en eventuele wijzigingen de workflow opnieuw; dat is het sterkste bewijs dat jullie daadwerkelijke workflow werkt.

## Vier verplichte testcases
1. `testcase1-low-risk.json` → `automatic_message`.
2. `testcase2-high-risk.json` → `human_review`.
3. `testcase3-fairness.json` → fairness false + forbiddenTerms + `human_review`.
4. `testcase4-no-consent.json` → duidelijke validatiefout (422 via `/process`, valid=false via `/validate`).

## Geautomatiseerde tests
Lokaal buiten Docker kan dit met Python 3.12:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
pytest -q
```

## Privacybewijs voor demo
De inkomende testcase bevat bewust synthetische velden `name`, `address`, `birthDate` en `citizenId`, zodat je kunt aantonen dat deze niet terugkomen in `minimizedApplication` en niet aan de AI-functie worden doorgegeven. `citizenId` wordt een eenrichtings-token via SHA-256 + salt. Voor productie is een professioneel secrets/key-management- en pseudonimisatieontwerp nodig.

## Fairnessbewijs
De stub kan alleen voor testcase 3 expres een verboden term injecteren via `injectForbiddenTermForTest`. De fairness-check detecteert beschermde/verboden termen en forceert menselijke review. Dit is bewust een eenvoudige demonstratie; fairness vereist in werkelijkheid bredere tests op bias, context en uitkomsten.

## Mens-in-de-loop
`severity=hoog`, `multipleProblems=true`, fairness failure of een hoge risicoscore leidt naar `human_review`. De AI doet alleen voorbereiding; een bevoegde medewerker neemt de formele beslissing.

## Bestandsstructuur
- `app/main.py` — backend
- `n8n/wmo-workflow.json` — importeerbare workflow
- `examples/` — vier demo-inputs
- `tests/` — vier geautomatiseerde tests
- `docs/` — Scrum, Double Diamond, Prompt Charter, feedback, presentatie en planning
- `evidence/` — zet hier jullie echte foto's/screenshots in

## Wat nog door het team moet worden gedaan
Zie `docs/09-deliverable-checklist.md`. Met name echte gebruikerstests, foto's, feedback van een andere groep, eigen n8n-export na import, presentatie-oefening en Canvas-upload kunnen niet vooraf gegenereerd worden.
