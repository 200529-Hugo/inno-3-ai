# Scrum-plan — WMO AI Hackathon

## Project Goal
Aan het einde van de hackathon hebben wij een werkend prototype opgeleverd dat WMO-aanvragen automatisch en transparant voorbereidt met AI, zonder persoonsgegevens aan de AI te geven, en dat complexe of risicovolle aanvragen doorstuurt naar een menselijke beoordelaar. Wij kunnen aantonen dat het gebruikers is voorgelegd en dat de feedback is verwerkt.

## Sprint Goal
Binnen één sprint van vier uur leveren we een reproduceerbare end-to-end demo op waarin een WMO-aanvraag via n8n wordt gevalideerd, geminimaliseerd en gepseudonimiseerd, door een AI-stub wordt voorbereid, op fairness en risico wordt gecontroleerd, correct naar automatisch bericht of menselijke review wordt gerouteerd en volledig wordt geaudit; alle vier verplichte testcases zijn aantoonbaar uitvoerbaar.

## Rollen
Vul namen in vóór de start.

- Product Owner: [NAAM]
- Scrum Master: [NAAM]
- Developers: [NAMEN]

De Product Owner bewaakt scope en acceptatiecriteria. De Scrum Master bewaakt tijd, Scrum-bord en blokkades. Developers bouwen/testen/documenteren. Rollen mogen wisselen.

## Product Backlog
| Prioriteit | User story | Acceptatiecriteria |
|---|---|---|
| P0 | Als gemeente wil ik een WMO-aanvraag via API/webhook ontvangen | JSON-aanvraag komt via n8n binnen |
| P0 | Als privacy officer wil ik dat PII nooit naar AI gaat | AI-input bevat geen naam, adres, geboortedatum of citizenId; alleen token/leeftijdsgroep |
| P0 | Als behandelaar wil ik een uitlegbaar voorstel | voorstel + onderbouwing aanwezig |
| P0 | Als gemeente wil ik risicovolle aanvragen handmatig beoordelen | ernst=hoog, meervoudige problematiek of fairness-fout => human_review |
| P0 | Als burger wil ik transparantie over AI | burgerbericht zegt dat AI ondersteunt en mens verantwoordelijk is |
| P0 | Als auditor wil ik beslissingen terugvinden | token, risico, flags, voorstel, rationale en route in database |
| P0 | Als team wil ik de vier verplichte tests demonstreren | alle vier aantoonbaar geslaagd |
| P1 | Als reviewer wil ik auditregels bekijken | GET /audit toont recente regels |
| P1 | Als docent wil ik installatie kunnen reproduceren | docker compose + README |
| P1 | Als docent wil ik procesbewijs zien | Scrum, Double Diamond, feedbackoverzicht, retro |
| P2 | Als reviewer wil ik een visueel dashboard | optioneel, alleen als P0/P1 klaar zijn |

## Sprint Backlog en statusbord
Maak in Trello/Miro/whiteboard drie kolommen: To do / Doing / Done. Start met onderstaande kaarten.

1. Docker Compose starten — P0
2. API health check — P0
3. n8n workflow importeren — P0
4. Testcase 1 uitvoeren — P0
5. Testcase 2 uitvoeren — P0
6. Testcase 3 uitvoeren — P0
7. Testcase 4 uitvoeren — P0
8. Audit-log controleren — P0
9. BPMN + architectuur opnemen — P1
10. Twee niet-ICT gebruikerstests — P0
11. Feedback verwerken — P0
12. Presentatie oefenen met andere groep — P0
13. Slides/screenshots verzamelen — P1
14. Retrospective invullen — P1

## Definition of Done
Een item is Done als:

1. code/configuratie in de projectmap staat;
2. het lokaal reproduceerbaar draait of de reden van een technische blokkade aantoonbaar is;
3. geen echte persoonsgegevens worden gebruikt;
4. relevante foutpaden zijn getest;
5. output begrijpelijk is voor demo/presentatie;
6. de vier verplichte testcases aantoonbaar werken;
7. auditdata voor succesvolle verwerkingen wordt opgeslagen;
8. bewijsmateriaal (screenshot/foto/testresultaat) is vastgelegd.

## Sprint Review
Te tonen: webhook/API-call, privacy-minimalisatie, voorstel, fairness-resultaat, risicoroute, auditrecord en vier testcases. Verzamel docent-/peerreacties als input voor vervolg.

## Retrospective — invulbaar
Wat ging goed: [bijv. strakke scope, deterministische stub, parallel gewerkt].

Wat kon beter: [bijv. eerder integreren, meer tijd voor UX, minder afhankelijkheid van live demo].

Volgende keer: [bijv. CI-test, echte policy-service, reviewer-UI, secrets management, uitgebreidere fairness-evaluatie].
