# Double Diamond-bewijs

## 1. Discover — probleem begrijpen (±20 min)
Doelgroep: burger die WMO aanvraagt, WMO-consulent/reviewer, privacy officer/auditor.

Vragen:
- Waar gaat nu tijd verloren?
- Welke informatie is echt nodig voor voorbereiding?
- Welke informatie mag nooit naar AI?
- Wanneer is menselijke beoordeling verplicht?
- Wat moet een burger begrijpen over AI-gebruik?

Te maken bewijs: foto van post-its met minimaal 8 observaties/vragen.

Voorbeeldinzichten:
- snelheid is minder belangrijk dan uitlegbaarheid bij risicovolle aanvragen;
- vrije tekst kan onbedoeld persoonsgegevens bevatten;
- deterministische demo is nuttiger dan een onvoorspelbaar LLM;
- burgerbericht moet verschil tussen 'voorstel' en 'besluit' helder maken.

## 2. Define — probleem scherpstellen (±15 min)
Probleemdefinitie:
"Hoe kunnen we een WMO-aanvraag sneller voorbereiden zonder persoonsgegevens aan AI te geven, terwijl fairness, transparantie, auditbaarheid en menselijke eindverantwoordelijkheid aantoonbaar blijven?"

How Might We:
"Hoe kunnen we AI alleen de minimaal noodzakelijke, gepseudonimiseerde informatie geven en risicovolle uitkomsten automatisch blokkeren voor menselijke beoordeling?"

Succescriteria:
- 4/4 testcases slagen;
- geen naam/adres/geboortedatum/citizenId in AI-input;
- fairness-term => review;
- ernst hoog => review;
- aiConsent=false => duidelijke fout;
- auditregel bevat benodigde velden.

Te maken bewijs: foto/screenshot van probleemstatement + succescriteria.

## 3. Develop — oplossingen verkennen (±20 min)
Overweeg minimaal drie opties en noteer waarom gekozen/niet gekozen:

A. Echt LLM + uitgebreide frontend. Niet gekozen voor kernprototype: te veel integratierisico en onvoorspelbare output binnen vier uur.

B. AI-stub + n8n + FastAPI + Postgres. Gekozen: snel, reproduceerbaar, privacy/fairness goed aantoonbaar.

C. Alles in n8n Code-nodes. Niet gekozen: minder scheiding van verantwoordelijkheden en lastiger unit-testbaar.

Te maken bewijs: schets van drie architectuuropties + keuzecriteria.

## 4. Deliver — bouwen, testen, verbeteren (rest sprint)
- oplossing starten;
- vier testcases draaien;
- twee niet-ICT-studenten laten testen;
- onduidelijkheden aanpassen;
- presentatie oefenen bij andere groep;
- feedback verwerken;
- bewijs verzamelen.

Te maken bewijs: screenshots van testresultaten, audit-log, gewijzigde tekst/UI en feedbacktabel.
