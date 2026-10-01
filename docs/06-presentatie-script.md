# Presentatiescript — 20 minuten inclusief vragen

## 0:00–2:00 Context, Project Goal, Sprint Goal
Spreker 1:
"Gemeenten verwerken WMO-aanvragen grotendeels handmatig. Ons prototype versnelt de voorbereiding, maar laat AI geen formeel besluit nemen. Ons Project Goal is een transparante, privacyvriendelijke voorbereiding met menselijke escalatie. Ons Sprint Goal was om binnen vier uur een reproduceerbare end-to-end demo te bouwen waarin alle vier verplichte testcases aantoonbaar werken."

Toon: Project Goal, Sprint Goal, Scrum-bord, rollen, DoD.

## 2:00–5:00 Double Diamond
Spreker 2:
Discover: belangrijkste risico's/gebruikersbehoeften.
Define: probleemstatement + succescriteria.
Develop: drie opties; waarom stub + n8n + FastAPI + Postgres.
Deliver: bouwen, testen, feedback verwerken.

Toon eigen foto's/post-its; niet alleen dit document.

## 5:00–15:00 Demo
### Architectuur in 30–45 sec
"n8n ontvangt de aanvraag. De API valideert en pseudonimiseert, haalt statisch beleid op, genereert via de stub een voorstel, controleert fairness en risico, routeert naar automatisch bericht of mens en schrijft auditdata weg."

### Testcase 1 — laag risico
Verwachting vooraf uitspreken: automatisch burgerbericht.
Laat request + output + audit zien.
Wijs op `citizenToken` en afwezigheid van naam/adres/geboortedatum in `minimizedApplication`.

### Testcase 2 — hoog risico
Verwachting: `human_review` vanwege ernst hoog/meervoudige problematiek.

### Testcase 3 — fairness
Verwachting: verboden term wordt geflagd en route wordt `human_review`.
Leg uit: woordenlijst is een prototypecontrole, geen volledige fairnessgarantie.

### Testcase 4 — toestemming ontbreekt
Verwachting: HTTP 422 / duidelijke foutmelding vóór AI-verwerking.

### Prompt Charter onderweg (±45 sec)
Noem: geen besluit, geen PII, policy-grounded, verboden kenmerken niet meewegen, menselijke review bij risico.

## 15:00–17:00 Feedback
Toon echte foto's + drie kolommen feedback → besluit → aanpassing.
Noem ten minste één concrete UX- of tekstwijziging die uit feedback kwam.
Noem feedback van andere groep en wat jullie in de presentatie veranderden.

## 17:00–17:30 Retrospective
Wat ging goed / wat volgende keer anders. Kort en concreet.

## 17:30–20:00 Vragen
Reserveer bewust tijd. Als docenten eerder vragen stellen, bewaak dat testcases 1–4 eerst zichtbaar zijn.

## Noodscenario bij falende live demo
Maak vóór de presentatie screenshots of een schermopname van:
1. testcase 1 output;
2. testcase 2 route human_review;
3. testcase 3 forbiddenTerms;
4. testcase 4 fout;
5. GET /audit;
6. n8n workflow.
