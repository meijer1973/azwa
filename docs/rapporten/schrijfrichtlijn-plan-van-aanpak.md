# Schrijfrichtlijn Plan van Aanpak

## Doel van deze richtlijn
Deze richtlijn is bedoeld voor het schrijven van een bestuurlijk en ambtelijk leesbaar `plan van aanpak`.

Het document moet:
- een opgave helder maken;
- richting geven aan keuzes, aanpak en planning;
- bestuurlijk bruikbaar zijn;
- leesbaar zijn zonder kennis van de onderliggende data-architectuur.

Het document moet **niet** klinken als een technische analyse, repository-notitie of datasetbeschrijving.

## Hoofdregel
Een `plan van aanpak` beschrijft:
- wat de opgave is;
- waarom handelen nodig is;
- wat het doel is;
- hoe de organisatie dat gaat aanpakken;
- wie waarvoor aan zet is;
- wanneer welke stappen gezet worden.

De bronanalyse is ondersteunend, niet leidend in de formulering.

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

## Wat hoort in de verantwoording of bijlage
In een bijlage of verantwoording mogen wel staan:
- peildatum;
- gebruikte bronset;
- methodische toelichting;
- datatoets;
- kwaliteitscontrole;
- beperkingen van de bronbasis;
- open reviewpunten.

Daar mag de taal technischer zijn, zolang die duidelijk van de hoofdtekst is gescheiden.

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

### Planning
Beantwoord:
- wat de eerstvolgende ijkmomenten zijn;
- welke besluiten of producten wanneer nodig zijn.

### Middelen
Beantwoord:
- welke middelen beschikbaar zijn of worden verwacht;
- welke onzekerheden er nog zijn;
- hoe daarmee wordt omgegaan.

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
- Zijn technische termen uit de hoofdtekst verwijderd?
- Is methodische taal verplaatst naar verantwoording of bijlage?
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
