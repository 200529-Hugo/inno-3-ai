# Eisencontrole — 1 oktober 2026

## Conclusie

De technische prototype-eisen zijn aantoonbaar werkend. Docker Compose start reproduceerbaar, de n8n-export importeert en orkestreert de losse services, de vier verplichte scenario's slagen via de webhook en succesvolle verwerkingen worden in PostgreSQL geaudit.

Het project kan pas als volledig ingeleverd worden beschouwd nadat het team de niet-technische bewijsstukken heeft verzameld en de invulvelden voor rollen, feedback, review en retrospective heeft ingevuld. Die bewijzen mogen niet worden verzonnen.

## Technische eisen

| Eis | Status | Bewijs |
|---|---|---|
| Aanvraag via webhook/API | Gereed | `POST /process` en n8n-webhook `/webhook/wmo-application` |
| Validatie en toestemming | Gereed | `/validate`; testcase 4 geeft HTTP 422 met duidelijke uitleg |
| Dataminimalisatie | Gereed | `minimizedApplication` bevat geen naam, adres, geboortedatum of direct citizenId |
| Pseudonimisering | Gereed | citizenId wordt met salt naar een `CIT-...` token gehasht |
| Geen PII naar AI | Gereed voor prototype | Gestructureerde PII wordt verwijderd; herkenbare PII in vrije tekst wordt geredigeerd; aanvullende productiecontrole blijft nodig |
| Beleidsregels | Gereed | `/policy/{provision}` met drie voorzieningen |
| AI-voorstel + onderbouwing | Gereed | Deterministische stub via `/ai/propose` |
| Fairness-check | Gereed voor prototype | Woordenlijst + controle op onderbouwing; flag forceert menselijke review |
| Mens-in-de-loop | Gereed | Ernst hoog, meervoudige problematiek, hoge score of fairness-fout geeft `human_review` |
| Transparant burgerbericht | Gereed | Bericht benoemt AI-ondersteuning en menselijke eindverantwoordelijkheid |
| Auditdatabase | Gereed | Token, risico, score, flags, voorstel, onderbouwing en route in PostgreSQL |
| n8n workflow as code | Gereed | JSON importeert in n8n 2.41.5 en orkestreert de afzonderlijke stappen |
| Reproduceerbare installatie | Gereed | Healthchecks en vaste n8n-versie in Docker Compose; instructies in README |

## Verificatie-uitkomst

- Docker-services: PostgreSQL healthy, API healthy, n8n healthy.
- Geautomatiseerde suite: 6 tests geslaagd.
- Testcase 1 via API en n8n: HTTP 200, `automatic_message`, fairness geslaagd.
- Testcase 2 via API en n8n: HTTP 200, `human_review`.
- Testcase 3 via API en n8n: HTTP 200, fairness gefaald op `religie`, `human_review`.
- Testcase 4 via API en n8n: HTTP 422, `VALIDATION_FAILED`, duidelijke melding over ontbrekende AI-toestemming.
- Workflow-import: geslaagd in n8n 2.41.5.
- Audit: vereiste velden aanwezig en records door de n8n-workflow opgeslagen.

## Nog door het team te doen

1. Vul Product Owner, Scrum Master en Developers in `docs/01-scrum-plan.md` in.
2. Maak/fotografeer het echte Scrum-bord met prioriteit en eindstatus.
3. Leg Discover, Define en Develop vast met eigen post-its/schetsen; voeg foto's toe aan `evidence/`.
4. Laat minimaal twee niet-ICT-studenten testen, vraag toestemming voor foto's, noteer hun opleiding/richting en verwerk minimaal één concrete verbetering.
5. Oefen met een andere hackathongroep; noteer ontvangen én gegeven feedback en de presentatieaanpassing.
6. Vul de drie-kolommentabel in `docs/05-feedback-template.md` in met echte resultaten.
7. Vul Sprint Review en Retrospective concreet in; vervang alle `[NAAM]`- en voorbeeldvelden.
8. Maak screenshots van vier webhookresultaten, de audit-log en de n8n-workflow als noodscenario voor de demo.
9. Verdeel de spreekrollen, oefen op maximaal 20 minuten en upload alle deliverables naar Canvas.

## Bekende prototypegrenzen

- De AI is bewust een deterministische stub; dit moet in de presentatie als ontwerpkeuze worden gemotiveerd.
- PII-redactie en fairness op basis van patronen/termen zijn demonstratiecontroles, geen productiegarantie.
- Het standaard pseudonimiseringssalt is alleen voor de demo. Gebruik in productie secrets management, sleutelrotatie en toegangsbeheer.
- Er is geen reviewer-dashboard; menselijke review is een aantoonbare route/status. Een frontend is volgens de opdracht optioneel.
