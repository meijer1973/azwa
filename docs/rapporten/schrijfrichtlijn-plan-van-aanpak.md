# Schrijfrichtlijn Plan van Aanpak

## Doel van deze richtlijn
Deze richtlijn is bedoeld voor het schrijven van een bestuurlijk en ambtelijk leesbaar `plan van aanpak`.

Het document moet:
- een opgave helder maken;
- richting geven aan keuzes, aanpak en planning;
- bestuurlijk bruikbaar zijn;
- leesbaar zijn zonder kennis van de onderliggende data-architectuur.

Het document moet **niet** klinken als een technische analyse, repository-notitie of datasetbeschrijving.

Het document moet ook **niet** zelf beleidsadvies, capaciteitsadvies of uitvoeringskeuzes invullen die niet uit de bronbasis volgen. De schrijver ordent de opgave en maakt keuzevragen zichtbaar; de menselijke opdrachtgever of beleidsmaker bepaalt de inhoudelijke invulling.

## Hoofdregel
Een `plan van aanpak` beschrijft:
- wat de opgave is;
- waarom handelen nodig is;
- wat het doel is;
- hoe de organisatie dat gaat aanpakken;
- wie waarvoor aan zet is;
- wanneer welke stappen gezet worden.

De bronanalyse is ondersteunend, niet leidend in de formulering.

De bronanalyse mag leiden tot:
- opgaven;
- afhankelijkheden;
- aandachtspunten;
- keuzevragen;
- ontbrekende lokale uitwerking;
- punten voor menselijke beoordeling.

De bronanalyse mag niet zonder expliciete onderbouwing leiden tot:
- concrete fte-inzet;
- budgetverdeling;
- zelfgekozen planning of interne deadlines;
- niet-bestaande bijlagen of onderliggende stukken;
- bestuurlijke voorkeurskeuzes;
- prioritering alsof die al besloten is;
- uitvoeringsadvies dat niet in de bronbasis staat.

## Gewenste toon
Gebruik taal die:
- bestuurlijk en zakelijk is;
- helder en rustig is;
- handelingsgericht is;
- concreet is;
- institutioneel herkenbaar is voor gemeente, college, raad en partners.

Gebruik liever:
- `uit de analyse van beschikbare stukken blijkt`
- `voor Almere betekent dit`
- `dit vraagt om`
- `het doel is`
- `hiervoor is nodig`
- `de gemeente organiseert`
- `de volgende stap is`

Vermijd in de hoofdtekst:
- `de dataset laat zien`
- `de repository toont`
- `de claimlaag zegt`
- `de JSON maakt zichtbaar`
- `de pipeline verwerkt`
- `QC-rapportage laat zien`

Dat soort taal hoort alleen thuis in een methodische bijlage of verantwoording.

Voor publieke of bestuurlijke stukken geldt aanvullend: ook een verantwoording of bijlage moet leesbaar blijven voor mensen buiten het projectteam. Gebruik daar geen bestandsnamen, JSON-verwijzingen, pipeline-termen of QC-jargon. Zulke technische details zijn geschikt voor interne notities, ontwikkelverslagen of antwoorden aan de gebruiker, niet voor public-facing materiaal.

Interne datalagen zijn geen publieke bronnen. Namen zoals `Almere-view`, `site_almere_view.json`, `claims_master.jsonl`, `current_interpretation.json` of vergelijkbare modelartefacten mogen het schrijfproces intern ondersteunen, maar worden niet genoemd in public-facing tekst. Vertaal ze naar gewone taal, bijvoorbeeld `op basis van de beschikbare openbare bronnen` of `uit de analyse van de beschikbare stukken`.

## Schrijf vanuit bestuurlijke logica
De volgorde van redeneren in een plan van aanpak is meestal:

1. Aanleiding
2. Opgave
3. Doel
4. Gewenst resultaat
5. Aanpak
6. Rollen en governance
7. Planning
8. Middelen
9. Risico's en beheersing
10. Besluitvorming en vervolgstappen

Niet de technische volgorde:

1. dataset
2. analyse
3. bronverwijzing
4. afgeleide conclusie

## Wat hoort in de hoofdtekst
In de hoofdtekst staat:
- de beleidsmatige of bestuurlijke betekenis;
- de lokale opgave;
- de noodzaak van keuzes;
- de aanpak in werkbare stappen;
- de relatie met planning, middelen en besluitvorming.

In de hoofdtekst staat bij voorkeur **niet**:
- interne bestandsnamen;
- technische datatermen;
- verwijzingen naar JSON-bestanden;
- uitleg over extractie, claims of QC;
- formuleringen alsof het document zelf door data "spreekt".
- zelfbedachte personele inzet, budgetten of uitvoeringsoplossingen.
- zelfbedachte planning, mijlpalen of deadlines die niet uit de bronbasis volgen.
- verwijzingen naar bijlagen, tabellen, kaarten of onderliggende notities die niet daadwerkelijk bestaan.

Als de bronbasis nog geen concrete invulling geeft, benoem dan de keuze die nog gemaakt moet worden in plaats van zelf een advies in te vullen.

## Wat hoort in de verantwoording of bijlage
In een bijlage of verantwoording mogen wel staan:
- peildatum;
- gebruikte bronset;
- methodische toelichting;
- beperkingen van de bronbasis;
- open reviewpunten.

Voor publieke of bestuurlijke documenten blijft ook deze verantwoording gewoon Nederlands. Vermijd:
- bestandsnamen zoals `site_almere_view.json`;
- interne modelnamen zoals `Almere-view` of `claimlaag`;
- pipeline-termen zoals `extractie`, `render`, `QC` of `blocking issues`;
- technische tellingen die alleen voor ontwikkelaars betekenis hebben.

Gebruik in plaats daarvan:
- `Deze versie is gebaseerd op de beschikbare landelijke, regionale en lokale bronnen tot en met [datum].`
- `Open punten zijn apart benoemd als keuze- of beoordelingspunten.`
- `Waar de bronnen nog geen lokale invulling geven, is geen bestuurlijke keuze ingevuld.`

Technische verantwoording kan apart worden bijgehouden in interne documentatie of in antwoorden aan de gebruiker, maar hoort niet in public-facing rapporttekst.

## Bijlagen
Noem alleen bijlagen die daadwerkelijk bestaan en beschikbaar zijn bij het document.

Niet:
`Bijlage A: gebruikte bronset en peildatum.`

Niet:
`Bijlage C: planning 2026-2030.`

Waarom niet:
Als zulke bijlagen niet zijn gemaakt, wekt het document ten onrechte de indruk dat er onderliggende stukken beschikbaar zijn.

Beter:
- laat de bijlagensectie weg;
- verwijs in de tekst kort naar de gebruikte openbare bronnen;
- of markeer een stuk expliciet als `nog op te stellen` als de opdrachtgever daarom vraagt.

Gebruik dus geen bijlagenlijst als de bijlagen niet echt bestaan. Een plan zonder bijlagen is beter dan een plan met verzonnen bijlagen.

## Formuleringsregels

### 1. Schrijf niet vanuit het systeem, maar vanuit de opgave
Niet:
`De dataset van 22 april 2026 laat zien dat de landelijke basis voor AZWA in Almere vooral op D5 en D6 helder is.`

Beter:
`Op basis van de huidige landelijke en regionale stukken is de beleidsmatige basis voor D5 en D6 voldoende helder om in Almere gerichte keuzes over uitwerking, regie en uitvoering te maken.`

Nog bestuurlijker:
`Voor Almere ligt de opgave in 2026 niet meer primair in het duiden van het landelijke kader, maar in het expliciet maken van lokale keuzes over uitwerking, regie, middelen en monitoring.`

### 2. Vermijd "laat zien", kies voor betekenis
Niet:
`De analyse laat zien dat...`

Beter:
- `Hieruit volgt dat...`
- `Dit betekent voor Almere dat...`
- `Dit vraagt om...`
- `Daarom is nodig dat...`

### 3. Noem geen data-objecten in lopende tekst
Niet:
`De Almere-view benoemt vier directe lokale opgaven.`

Beter:
`Op basis van de huidige stukken komen vier directe lokale opgaven naar voren.`

Als methodische precisie nodig is:
`Deze vier opgaven zijn ontleend aan de huidige analyse van de Almere-bronbasis.`

Voor public-facing tekst geldt: verwijs niet naar interne viewnamen, modelbestanden of data-objecten als bron. De bron voor de lezer is de openbare bronbasis, niet de interne datalaag.

### 4. Vermijd te technische zekerheid
Niet:
`De landelijke bekostigingsroute is volgens de dataset nog afhankelijk van afspraken tussen VNG, fondsbeheerders en VWS.`

Beter:
`De landelijke bekostigingsroute is op dit moment nog niet volledig uitgewerkt en blijft afhankelijk van nadere afspraken tussen VNG, fondsbeheerders en VWS.`

### 5. Maak zinnen bestuurlijk handelingsgericht
Niet:
`Er is nog geen volledig expliciet AZWA-kader.`

Beter:
`De huidige openbare stukken bieden nog onvoldoende houvast voor een volledig expliciet lokaal uitvoeringskader.`

Nog sterker:
`Daarom is bestuurlijke concretisering nodig op prioritering, regie, middelen en monitoring.`

### 6. Vul geen beleids- of capaciteitsadvies in zonder bronbasis
Niet:
`Indicatief is nodig: 0,8 fte programmamanager, 0,8 fte gecombineerde beleidsinzet sociaal domein en gezondheid, 0,2 fte financien/control, 0,2 fte data/monitoring en 0,1 fte communicatie.`

Beter:
`De beschikbare stukken geven nog geen concrete onderbouwing voor de benodigde personele inzet. Voor de verdere uitwerking is een bestuurlijke en ambtelijke inschatting nodig van capaciteit, rolverdeling en dekking.`

Nog beter als keuzevraag:
`Te bepalen is welke capaciteit Almere nodig acht voor programmasturing, beleidsuitwerking, financien/control, monitoring en communicatie, en welk deel daarvan binnen bestaande capaciteit of regionale samenwerking kan worden georganiseerd.`

Gebruik dus geen precieze fte's, bedragen, termijnen of voorkeursopties tenzij die expliciet in de bronbasis of opdracht staan.

### 7. Gebruik alleen bron- of modelgedragen datums als planning
Niet:
`April-mei 2026: factsheet, nulmeting en besluitnotitie op basis van de Almere-view.`

Niet:
`Q4 2026: uitvoeringsplan 2027-2028 met KPI's, eigenaarschap en rapportageritme.`

Waarom niet:
Deze formuleringen zetten een interne planning neer die niet vanzelf uit de bronbasis volgt. Daarmee lijkt het alsof het plan al bestuurlijke of ambtelijke keuzes maakt over tempo, producten en volgorde.

Beter:
`De bronbasis bevat verschillende externe ijkmomenten in 2026, waaronder publicatie- en toelichtingsmomenten rond AZWA-financiering, de meicirculaire, de regionale werkagenda en de vaststellingstermijn van 15 november 2026. De vertaling naar een interne Almere-planning vraagt nog om menselijke beoordeling.`

Nog beter als keuzevraag:
`Te bepalen is welke interne planning Almere koppelt aan de externe ijkmomenten in 2026, en welke producten daarvoor nodig zijn, zoals een factsheet, besluitnotitie, financieel scenario of uitvoeringsplan.`

Gebruik datums dus alleen als:
- ze expliciet in een bron staan;
- ze in het tijdlijnregister of model als bron- of modelgedragen moment zijn opgenomen;
- ze duidelijk als extern ijkmoment worden gepresenteerd.

Als een datum een interpretatie, werkhypothese of voorgestelde interne planning is, markeer die dan als `te bepalen`, `voor menselijke beoordeling` of verplaats hem naar een conceptplanning die door reviewers moet worden ingevuld.

## Voorkeurswoorden
Gebruik liever:
- `opgave`
- `uitwerking`
- `bestuurlijke keuze`
- `lokale vertaling`
- `regie`
- `inrichting`
- `uitvoeringskader`
- `aansluiting`
- `randvoorwaarde`
- `fasering`
- `ijkmoment`
- `voortgang`
- `herijking`

Gebruik terughoudend:
- `helder`
- `zichtbaar`
- `impliciet`
- `expliciet`

Die woorden kunnen nuttig zijn, maar worden snel abstract. Voeg daarom steeds toe: **helder voor wat**, **zichtbaar in welk opzicht**, **expliciet in welke keuze**.

## Vermijd deze stijlkenmerken
- Taal die klinkt als een dashboard.
- Zinnen die beginnen met `de dataset`, `de analyse`, `de repository`, `de view`.
- Te veel meta-taal over het document zelf.
- Te veel opsommingen zonder verbindende duiding.
- Te veel abstracte zelfstandige naamwoorden zonder actor.

Voorbeeld:
Niet:
`Lokale monitoring nog niet expliciet gekoppeld aan regionale en landelijke cyclus.`

Beter:
`De huidige stukken maken nog niet duidelijk hoe Almere de lokale monitoring wil verbinden met de regionale en landelijke cyclus.`

## Aanbevolen standaardopbouw per onderdeel

### Aanleiding
Beantwoord:
- wat is er veranderd;
- waarom is dit nu relevant;
- waarom vraagt dit om een planmatige aanpak.

### Opgave
Beantwoord:
- wat moet Almere organiseren, uitwerken of besluiten;
- waar zitten de huidige lacunes;
- waarom volstaat de huidige situatie niet.

### Doel
Beantwoord:
- welk resultaat uiterlijk wanneer bereikt moet zijn;
- hoe dat bestuurlijk herkenbaar is.

### Aanpak
Beantwoord:
- langs welke sporen wordt gewerkt;
- welke werkpakketten daaronder vallen;
- hoe keuzes en uitvoering samenhangen.

### Governance
Beantwoord:
- wie eigenaar is;
- wie meebeslist;
- wie uitvoert;
- hoe regionale afstemming loopt.

Voor Almere en Flevoland geldt hierbij een extra precisie-eis. Gebruik `de regio`, `Flevoland`, `regionale structuur` of `mandaatgemeente` niet als verzamelterm wanneer verschillende regionale indelingen relevant zijn. Benoem waar nodig de schaal: `IZA/AZWA-regio Flevoland`, `GGD-regio Flevoland`, `zorgkantoorregio 't Gooi`, `ROAZ/subregio` of `subregionale aanpak`. Maak ook onderscheid tussen formeel mandaat, programmacoordinatie en praktische uitvoering. Als alleen bekend is dat Almere als mandaatgemeente wordt genoemd, maar niet wie een specifieke taak uitvoert, formuleer de taakverdeling als reviewpunt.

### Planning
Beantwoord:
- wat de eerstvolgende ijkmomenten zijn;
- welke besluiten of producten wanneer nodig zijn.

Gebruik hierbij alleen bron- of modelgedragen datums. Vul geen interne Almere-planning in die niet expliciet uit de bronbasis volgt. Als de bronbasis alleen externe ijkmomenten geeft, beschrijf dan die ijkmomenten en formuleer de lokale planning als keuzevraag voor menselijke reviewers.

### Middelen
Beantwoord:
- welke middelen beschikbaar zijn of worden verwacht;
- welke onzekerheden er nog zijn;
- hoe daarmee wordt omgegaan.

Noem geen eigen indicatieve budgetten, fte's of verdeelsleutels tenzij de bronbasis die expliciet bevat. Als de informatie ontbreekt, formuleer een invulpunt of keuzevraag voor menselijke beoordeling.

### Risico's
Beantwoord:
- wat uitvoering kan belemmeren;
- hoe dat wordt beheerst.

## Gebruik van bronverwijzingen
Bronnen mogen zichtbaar zijn, maar niet in elke zin.

In de hoofdtekst:
- noem vooral de betekenis;
- noem alleen de belangrijkste documenten als dat helpt voor legitimatie.

In de bijlage:
- zet de volledige bronverantwoording;
- voeg peildatum en methodische notitie toe.

## Korte checklist voor redactieslag
Controleer bij elk concept:

- Spreekt de tekst vanuit de opgave of vanuit de data?
- Is duidelijk wat Almere moet doen?
- Is duidelijk waarom bestuurlijke actie nodig is?
- Zijn de kernzinnen handelingsgericht?
- Zijn er geen fte's, bedragen, prioriteiten of uitvoeringsadviezen toegevoegd die niet expliciet uit de bronbasis komen?
- Zijn alle datums, deadlines en mijlpalen bron- of modelgedragen, of duidelijk gemarkeerd als menselijke invulling?
- Worden alleen bijlagen genoemd die daadwerkelijk bestaan of expliciet als `nog op te stellen` zijn gemarkeerd?
- Zijn technische termen uit de hoofdtekst verwijderd?
- Is technische methodetaal ook uit publieke verantwoordingen en bijlagen gehouden?
- Staat er per onderdeel steeds een actor, actie en gevolg?
- Klinkt de tekst als gemeentelijk beleidsstuk en niet als analyse-output?

## Praktische vuistregel
Als een zin niet natuurlijk zou klinken in:
- een collegevoorstel,
- een bestuurlijke notitie,
- een directieoverleg,

dan is die zin waarschijnlijk te technisch, te meta of te veel "uit de machine" geschreven.

## Toepassing op het huidige voorbeeld
Huidige formulering:

`De dataset van 22 april 2026 laat zien dat de landelijke basis voor AZWA in Almere vooral op D5 en D6 helder is.`

Voorkeursvariant voor een plan van aanpak:

`Op basis van de huidige landelijke en regionale stukken is het kader voor D5 en D6 voldoende uitgewerkt om in Almere gerichte keuzes te maken over lokale uitwerking, regie, middelen en monitoring.`

Alternatief met nog meer bestuurlijke sturing:

`Voor Almere ligt de opgave nu vooral in het vertalen van het bestaande landelijke kader voor D5 en D6 naar bestuurlijke keuzes over uitvoering, regie, middelen en monitoring.`
