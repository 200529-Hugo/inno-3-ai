# WMO AI Hackathon-opdracht

## 1. Programma van de dag

| Onderdeel | Duur | Wat |
|---|---:|---|
| Gastcollege | 1 uur | Een externe spreker laat zien wat AI in de praktijk betekent en waarom jij zelf verantwoordelijk bent om de ontwikkelingen te volgen. |
| Hackathon-opdracht | 4 uur | Je team bouwt een werkend prototype (zie hieronder). |
| Presentatie | 20 minuten | Je team presenteert proces en resultaat aan de docenten. |

## 2. Context

Gemeenten krijgen dagelijks aanvragen voor WMO-voorzieningen, zoals huishoudelijke hulp, een rolstoel of een woningaanpassing. Die aanvragen worden nu handmatig verwerkt. Dat kost tijd en er worden fouten gemaakt. De gemeente wil dit versnellen met AI en workflow-automatisering, maar wel ethisch verantwoord en privacyvriendelijk.

Jullie zijn het ontwikkelteam dat hiervoor een prototype bouwt.

## 3. Scrum: Project Goal

**Project Goal:** Aan het einde van de hackathon hebben wij een werkend prototype opgeleverd dat WMO-aanvragen automatisch en transparant voorbereidt met AI, zonder persoonsgegevens aan de AI te geven, en dat complexe of risicovolle aanvragen doorstuurt naar een menselijke beoordelaar. Wij kunnen aantonen dat het gebruikers is voorgelegd en dat de feedback is verwerkt.

Werk als Scrum-team met één sprint van 4 uur. Toon in de presentatie:

- **Sprint Goal:** jullie eigen, concrete doel voor deze sprint, afgeleid van het Project Goal.
- **Product Backlog en Sprint Backlog:** een simpel bord (fysiek of digitaal) met user stories, prioriteit en status.
- **Definition of Done:** minimaal de vier testcases (paragraaf 6.4) werken aantoonbaar.
- **Rollen:** wie is Product Owner en wie is Scrum Master? Deze rollen mogen wisselen.
- **Sprint Review en Retrospective:** kort en in de presentatie verwerkt (wat ging goed, wat doen we de volgende keer anders).

## 4. Proces: Design Thinking (Double Diamond)

Je volgt het Double Diamond-model en toont dat aantoonbaar aan in de presentatie.

Foto’s van post-its, whiteboards of schetsen zijn ruim voldoende. Het gaat erom dat wij de stappen kunnen volgen.

### 4.1 Verplichte feedbackrondes (binnen de 4 uur)

#### A. Feedback op de oplossing van minimaal 2 niet-ICT-studenten

Zoek in het gebouw minimaal 2 HBO-studenten van een andere richting, bijvoorbeeld Journalistiek of Administratie. Laat hen jullie oplossing gebruiken (bijvoorbeeld het burgerbericht of het reviewer-scherm) en vraag expliciet om feedback.

Leg vast:

- een foto van de student terwijl die test (met toestemming);
- het resultaat van de test: wat ging goed, wat was onduidelijk?
- de aanpassing die jullie daarna hebben gedaan.

#### B. Feedback op de presentatie van minimaal 1 andere hackathon-groep

Oefen jullie presentatie voor een andere groep en vraag expliciet om feedback. Geef ook zelf feedback op de presentatie van die groep.

Leg vast:

- wat jullie kregen;
- wat jullie gaven;
- wat jullie hebben aangepast.

Laat de feedback en de verwerking zien in een overzicht van drie kolommen:

| Feedback | Besluit | Aanpassing |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |

## 5. Technologie-eisen

### Verplicht

- **n8n** voor de workflow-orkestratie.
- De workflow lever je in als export (**JSON**) in Canvas (**workflow as code**).

### Vrije keuze

Jullie kiezen en motiveren in de presentatie:

- programmeertaal en framework voor de services, bijvoorbeeld Python met FastAPI, voor AI-analyse, fairness-check en beleid;
- database voor de audit-log, waarbij Postgres een logische keuze is;
- optioneel: een front-end, bijvoorbeeld React, voor een burgerportaal of reviewer-dashboard;
- AI: een echt LLM of een stub (nagebootste AI). Gebruik bij een echt LLM alleen synthetische testdata, nooit echte persoonsgegevens;
- installatie: zorg dat een ander team jullie oplossing kan starten met duidelijke instructies. Docker Compose wordt aanbevolen;
- vibe coding is toegestaan. Je moet dan wel laten zien hoe je AI-assistenten hebt gebruikt (zie paragraaf 6.3).

## 6. Opdracht: wat moet je opleveren?

### 6.1 Functionele eisen: het prototype

Ontwerp en implementeer een end-to-end oplossing die:

- aanvragen ontvangt via een webhook of API;
- de aanvraag valideert en data minimaliseert (geen PII naar de AI);
- persoonsgegevens pseudonimiseert (`citizenId → token`);
- beleidsregels ophaalt (mock-API of statische data is voldoende);
- een AI-service aanroept (LLM of stub) om een voorstel te genereren;
- een fairness-check uitvoert (detecteer verboden termen en controleer de onderbouwing);
- complexe of risicovolle aanvragen naar een menselijke beoordelaar stuurt;
- de burger een transparant bericht geeft (AI ondersteunt, mens beslist);
- beslissingen logt in een audit-database (token, risico, flags, voorstel en onderbouwing).

### 6.2 Ethiek en privacy: harde eisen

- **Privacy-by-design:** naam, adres en geboortedatum gaan nooit in een AI-prompt. Gebruik een leeftijdsgroep in plaats van een exacte geboortedatum.
- **Fairness:** detecteer verboden kenmerken (religie, ras, nationaliteit, geslacht, enzovoort) in AI-output.
- **Mens-in-de-loop:** bij hoog risico of ernst = hoog beslist altijd een mens.
- **Transparantie:** de burger weet dat AI heeft meegewerkt en dat een mens beslist.
- **Audit:** alle beslissingen, flags en risicoscores worden bewaard.

### 6.3 Deliverables

De onderstaande onderdelen laat je zien in de presentatie en upload je naar Canvas:

| # | Deliverable |
|---:|---|
| 1 | BPMN-diagram van het proces |
| 2 | Architectuurdiagram |
| 3 | Werkende n8n-workflow (JSON-export) |
| 4 | Endpoints met de benodigde functies (bijvoorbeeld validatie, pseudonimisering, beleid, AI, fairness) |
| 5 | Audit-database met vastgelegde beslissingen |
| 6 | Prompt Charter (zie hieronder) |
| 7 | Installatie-instructies in een README |
| 8 | Bewijs Double Diamond (foto’s, post-its, schetsen) |
| 9 | Bewijs feedback (paragraaf 4.1) |
| 10 | AI-gebruikslog: een korte verantwoording van welke AI-assistenten jullie gebruikten, waarvoor en wat je zelf hebt gecontroleerd of aangepast |

#### Wat is een Prompt Charter?

Een kort document met de regels voor jullie AI:

- wat de AI wel en niet mag doen, bijvoorbeeld geen discriminerende content;
- toon en stijl: vriendelijk, duidelijk, professioneel;
- veiligheidsrichtlijnen, bijvoorbeeld geen medische of financiële adviezen zonder disclaimer;
- hoe de AI omgaat met gevoelige informatie: privacy en vertrouwelijkheid;
- hoe tools worden gebruikt.

### 6.4 Testcases voor de demo

| # | Testcase | Verwacht resultaat |
|---:|---|---|
| 1 | Laag risico: neutrale aanvraag | Automatisch burgerbericht |
| 2 | Hoog risico: meervoudige problematiek en ernst = hoog | Doorsturen naar menselijke beoordelaar |
| 3 | Fairness-flag: AI-output bevat een verboden term | Flag en review door een mens |
| 4 | Validatie faalt: toestemming AI = false | Duidelijke foutmelding |

## 7. Eisen aan de presentatie (20 minuten, inclusief vragen)

| Onderdeel | Tijd | Inhoud |
|---|---:|---|
| Context en Project Goal | 2 min | Wat is het probleem? Wat is jullie Project Goal en Sprint Goal? |
| Double Diamond | 3 min | Toon de vier fasen met bewijs (foto’s van post-its, persona’s, keuzes). |
| Demo | 10 min | Laat de 4 testcases live zien. Leg onderweg kort de BPMN, architectuur en het Prompt Charter uit. |
| Feedback | 2 min | Laat zien: feedback van de niet-ICT-studenten (foto, resultaat, aanpassing) en van de andere groep. |
| Vragen | 3 min | Vragen van de docenten. |

Verder verwachten we:

- alle teamleden zijn aanwezig en dragen bij aan de presentatie;
- een korte terugblik (Retrospective): wat ging goed en wat doen jullie een volgende keer anders?
- werkt de live demo niet? Laat dan een opname of screenshots zien en leg uit waarom het niet werkt.

## 8. Beoordeling (docenten)

| Criterium | Weging | Wat kijken we naar? |
|---|---:|---|
| Proces (Double Diamond en Scrum) | 20% | Zijn alle fasen aantoonbaar? Zijn Project Goal, Sprint Goal, backlog en Definition of Done zichtbaar? |
| Technische implementatie | 30% | Werkt het systeem end-to-end? Zijn alle 4 testcases aangetoond? Zijn de deliverables compleet? |
| Ethiek, privacy en fairness | 20% | Privacy-by-design, fairness-check, mens-in-de-loop, transparantie en audit. |
| Feedback | 15% | Is er feedback gehaald bij 2 niet-ICT-studenten en 1 andere groep? Is de verwerking aantoonbaar? |
| Presentatie en demo | 15% | Duidelijk, binnen de tijd en onderbouwd. Is het AI-gebruik verantwoord? |

Per criterium beoordelen we op: **onvoldoende**, **voldoende** of **goed**.
