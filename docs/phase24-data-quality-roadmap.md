# Langetermijnplan datakwaliteit AZWA-site

## Doel
De website is werkbaar als V1. De volgende ontwikkelfase richt zich daarom niet primair op de gebruikersinterface, maar op betere bronkwaliteit, betere extracties, betere claimstructuur en betere Nederlandse siteteksten.

Het doel is dat beleidsmakers de site kunnen beoordelen langs zes vaste perspectieven:

| Perspectief | Centrale vraag |
| --- | --- |
| Norm | Wat is vereist, toegestaan, verwacht of bindend? |
| Tijd | Welke data, deadlines, fasering, herijkingsmomenten en begrotingsmomenten zijn relevant? |
| Geld | Welke middelenstromen, budgetvensters, voorwaarden en cofinancieringslogica gelden? |
| Governance | Wie besluit, coordineert, is eigenaar of moet goedkeuren? |
| Locality | Wat betekent dit specifiek voor Almere of Flevoland? |
| Execution | Wat moet feitelijk worden georganiseerd, voorbereid of in volgorde gezet? |

## Werkprincipes
- Nieuwe informatie gaat eerst door de bron- en datapijplijn voordat de website-inhoud wordt aangepast.
- Public-facing tekst mag geen interne datalaagnamen of technische pipeline-taal bevatten.
- Elke verbetering moet herleidbaar blijven naar bron, claim, tijdlijnitem of menselijke reviewtaak.
- UI-werk blijft beperkt tot noodzakelijke leesbaarheid, klikbaarheid en traceerbaarheid totdat de datakwaliteit stabieler is.
- Onzekere punten worden zichtbaar gemaakt als beoordelingspunt, niet opgelost door de generator.

## Sprintcadans
Elke sprint heeft dezelfde basisvolgorde:

1. Bronnen bepalen en prioriteren.
2. Bronnen downloaden of actualiseren.
3. Bronnen door de volledige pijplijn halen.
4. Extracties, claims, tijdlijn en site-viewmodels controleren.
5. Wijzigingen vastleggen in een changelog.
6. Public-facing teksten controleren op toon, bronvastheid en klikbaarheid.

Elke sprint eindigt met:

- een korte datakwaliteitsnotitie;
- een lijst van nieuwe of gewijzigde bronnen;
- een lijst van inhoudelijke wijzigingen op de site;
- een lijst van open reviewpunten;
- testresultaten voor pipeline en site.

## Fase 24 - Kwaliteitskader per perspectief
Doel: de zes perspectieven omzetten in een vaste beoordelingsstructuur voor bronnen, claims en site-tekst.

Sprint 24.1: Taxonomie en checklist

- Maak per perspectief een vaste set velden, voorbeelden en uitsluitingsregels.
- Leg vast wanneer iets een bronfeit, interpretatie, lokale lacune of menselijke keuzevraag is.
- Voeg een korte redactieregel toe voor public-facing formuleringen per perspectief.

Sprint 24.2: Audit van bestaande site-data

- Label bestaande claims en viewmodels met de zes perspectieven waar mogelijk.
- Zoek brede restcategorieen zoals `timeline.other`, `monitoring.other` en `governance_and_finance.other`.
- Maak een overzicht van claims die inhoudelijk nuttig zijn maar tekstueel te ruw zijn voor publicatie.

Sprint 24.3: Review-dashboard intern

- Maak een intern overzicht met open kwaliteitsissues per perspectief.
- Splits issues in bronprobleem, extractieprobleem, claimprobleem, interpretatieprobleem en tekstprobleem.
- Houd dit intern; public-facing site mag deze technische categorieen niet tonen.

## Fase 25 - Bronkwaliteit en bronhiaten
Doel: de bronbasis versterken, vooral voor geld, tijd, governance en lokale relevantie.

Sprint 25.1: Financieringsbronnen

- Controleer VWS, VNG, DUS-I, wetten.nl en gemeentefondsbronnen op AZWA, SPUK, meicirculaire, werkagenda en verantwoordingsmomenten.
- Markeer welke bronnen normatief zijn en welke alleen toelichtend of praktisch zijn.
- Zoek expliciet naar regels over besteding, reservering, doorschuiven, aanvraag en verantwoording van middelen.

Sprint 25.2: Almere en Flevoland

- Zoek bestuurlijke agenda's, raadsinformatie, begrotingsstukken en lokale beleidsdocumenten die AZWA, IZA, GALA, preventie, sociaal domein of gezondheid raken.
- Voeg alleen bronnen toe die openbaar en herleidbaar zijn.
- Leg vast waar landelijke doelen nog niet zichtbaar lokaal zijn overgenomen.

Sprint 25.3: Regionale governance

- Versterk bronnen over mandaatgemeente, regio, zorgverzekeraar, GGD, regionale preventie-infrastructuur en werkagenda.
- Maak onderscheid tussen wie formeel besluit, wie voorbereidt en wie uitvoert.
- Controleer of de website dit onderscheid begrijpelijk weergeeft.

## Fase 26 - Extractiekwaliteit
Doel: minder halve zinnen, betere tabellen, betere paginaverwijzingen en betere broncitaten.

Sprint 26.1: PDF- en tabelkwaliteit

- Verbeter extractie van tabellen met middelen, jaartallen, deadlines en rollen.
- Bewaar tabelrijen als afzonderlijke bewijsobjecten waar dat kan.
- Controleer sleutelbronnen handmatig op ontbrekende of verkeerd samengevoegde rijen.

Sprint 26.2: Claimtekst schoonmaken

- Voorkom dat claims bestaan uit afgebroken zinnen, voetteksten, kopregels of navigatietekst.
- Bewaar ruwe broncitaten, maar genereer aparte leesbare claim-samenvattingen voor sitegebruik.
- Voeg regressietests toe voor bekende probleemvormen.

Sprint 26.3: Locatie- en bewijscontrole

- Controleer dat belangrijke claims minimaal pagina, sectie, quote of chunk-id hebben.
- HTML-bronnen krijgen sectie- en chunkverwijzingen als paginanummers niet bestaan.
- Claims zonder bruikbare locatie gaan naar review.

## Fase 27 - Claimmodel per perspectief
Doel: van algemene claims naar beleidsmatig bruikbare claims per Norm, Tijd, Geld, Governance, Locality en Execution.

Sprint 27.1: Norm

- Splits normclaims in bindend, afspraak, verwachting, toelichting en lagere-autoriteitssignaal.
- Voorkom dat VNG-FAQ's, nieuwsberichten of toelichtingen klinken als harde norm.
- Maak conflicten of onzekerheid expliciet in mensentaal.

Sprint 27.2: Tijd

- Maak deadlines, verwachte publicatiemomenten, reviewmomenten en begrotingsmomenten aparte tijdclaims.
- Sorteer en groepeer tijdlijnitems structureel chronologisch.
- Markeer verwachte momenten duidelijk anders dan vastgestelde deadlines.

Sprint 27.3: Geld

- Maak claims voor financieringsinstrument, aanvraagvoorwaarde, budgetvenster, verdeelmechanisme, bestedingsruimte en verantwoording.
- Leg onzekerheden over uitkering, overloop, reservering en besteding apart vast.
- Voeg een zoekbare categorie toe voor "te verifieren financieringsregel".

Sprint 27.4: Governance

- Maak rollen expliciet: ministerie, VNG, fondsbeheerder, mandaatgemeente, regio, gemeente, raad, college, zorgverzekeraar, uitvoeringspartner.
- Splits besluitvorming, coordinatie, aanvraag, uitvoering en verantwoording.
- Voorkom dat "regio" als actor wordt gebruikt als de bron specifieker is.

Sprint 27.5: Locality

- Markeer claims die expliciet over Almere gaan anders dan claims die alleen algemeen voor gemeenten gelden.
- Markeer Flevolandse claims apart van Almeerse claims.
- Houd adoptiegaten zichtbaar: landelijk doel aanwezig, lokale openbare uitwerking nog niet gevonden.

Sprint 27.6: Execution

- Vertaal bronclaims naar mogelijke uitvoeringsvragen zonder beleidsadvies toe te voegen.
- Splits mogelijke besluitvragen, mogelijke opvolgacties, afhankelijkheden en reviewvragen.
- Laat de site niet suggereren dat een actie al is besloten als alleen de bronbasis aanleiding geeft om deze te onderzoeken.

## Fase 28 - Tekstkwaliteit van de website
Doel: minder technische of ruwe tekst, meer bestuurlijk leesbare Nederlandse samenvattingen.

Sprint 28.1: Menselijke samenvattingen per update

- Elke data-update krijgt een korte, leesbare samenvatting.
- Leg uit welke publicatie aanleiding was voor de update.
- Benoem wat inhoudelijk is veranderd, zonder interne datatermen.

Sprint 28.2: Bronverwijzing en autoriteitstaal

- Lagere-autoriteitsbronnen worden expliciet toegeschreven, bijvoorbeeld "Volgens de VNG-toelichting..." of "DUS-I vermeldt...".
- Normatieve bronnen krijgen sterkere formulering, maar alleen waar de bron dat draagt.
- Onzekerheden blijven zichtbaar zonder dramatische woorden als urgent of kritisch.

Sprint 28.3: Detailpagina's voor drill-down

- Overzichtspagina's blijven kort.
- Lange claimlijsten, bronlijsten en reviewdetails gaan naar aparte detailpagina's.
- Elke klikbare tegel of telling moet naar de onderliggende items leiden.

## Fase 29 - Tijdlijn als beleidsinstrument
Doel: de tijdlijn gebruiken voor bestuurlijke orientatie, niet alleen als chronologische lijst.

Sprint 29.1: Tijdlijnregister verdiepen

- Voeg bronstatus, autoriteit, actor, type moment en gevolg voor Almere toe aan tijdlijnitems.
- Houd verwachte, formele en lokale momenten zichtbaar verschillend.
- Leg per item vast welk perspectief vooral geraakt wordt: Tijd, Geld, Governance of Execution.

Sprint 29.2: Begrotings- en verantwoordingscyclus

- Voeg landelijke en lokale begrotingsmomenten toe zodra ze bronvast zijn.
- Koppel gemeentefonds, meicirculaire, septembercirculaire, begroting Almere en SPUK-verantwoording waar bronnen dit dragen.
- Markeer waar menselijke beoordeling nodig is om een extern moment naar lokale planning te vertalen.

Sprint 29.3: Handreikingen en uitvoeringsmomenten

- Houd handreikingen, webinars, thematafels en formatdocumenten apart van formele besluiten.
- Gebruik deze bronnen wel voor uitvoering en voorbereiding, maar niet als harde norm.
- Voeg nieuwe documenten pas toe na volledige pipeline-verwerking.

## Fase 30 - Lokale beleidsbruikbaarheid
Doel: de site beter laten aansluiten op vragen van Almeerse beleidsmakers.

Sprint 30.1: Lokale lacunes

- Maak per thema zichtbaar welke landelijke of regionale opgave nog niet openbaar lokaal is uitgewerkt.
- Voorkom oordeelstaal; formuleer als documentatie- of adoptiegat.
- Koppel elk gat aan bronbasis en mogelijke vervolgvraag.

Sprint 30.2: Besluitvragen en mogelijke opvolgacties

- Herclassificeer bestaande besluitvragen en opvolgacties langs de zes perspectieven.
- Maak duidelijk welke vraag door bronbasis wordt opgeroepen en welke invulling aan Almere is.
- Verwijder of herformuleer items die te veel als advies klinken.

Sprint 30.3: Beleidsdocumenten en rapporten

- Laat public-facing rapporten alleen publieke bronnen noemen, geen interne datalagen.
- Controleer plannen van aanpak op verzonnen bijlagen, bedragen, FTE's, deadlines en scenario's.
- Houd een aparte interne notitie bij voor technische controles.

## Fase 31 - Periodieke actualisatie
Doel: zorgen dat de site meebeweegt met nieuwe bronnen zonder dat oude informatie wordt overschreven.

Sprint 31.1: Updateprotocol

- Maak een vaste procedure voor nieuwe publicaties.
- Nieuwe broninformatie krijgt altijd een changelog met inhoudelijke delta.
- Oude claims blijven bewaard; nieuwe claims kunnen aanvullen, verduidelijken, beperken of tegenspreken.

Sprint 31.2: Maandelijkse bronaudit

- Controleer of verwachte bronnen zijn verschenen, zoals circulaires, SPUK-regelingen, handreikingen en monitorrapportages.
- Controleer dode links en gewijzigde webpagina's.
- Houd pending bronnen apart tot ze door de pipeline zijn verwerkt.

Sprint 31.3: Reviewronde met menselijke beoordelaars

- Lever per perspectief een korte reviewlijst op.
- Vraag reviewers vooral om bestuurlijke interpretatie, lokale keuze en bronvalidatie.
- Verwerk reviewerbesluiten apart van bronclaims.

## Kwaliteitscriteria
Een verbetering is pas klaar als:

- de bron is opgeslagen of de reden van niet-opname is vastgelegd;
- de bron in de manifest- en inventarislaag staat;
- relevante claims herleidbaar zijn naar bronlocatie;
- tijdlijnitems chronologisch en traceerbaar zijn;
- public-facing tekst in begrijpelijk Nederlands staat;
- tellingen, tegels en samenvattingen doorklikken naar onderliggende informatie;
- onzekerheden niet als feiten zijn gepresenteerd;
- de update een menselijke changelog heeft.

## Eerste aanbevolen sprint
De beste eerstvolgende sprint is Sprint 24.1: taxonomie en checklist per perspectief.

Waarom:

- de site is al bruikbaar;
- de grootste winst zit in consistente beoordeling van broninformatie;
- alle latere sprints profiteren van vaste labels voor Norm, Tijd, Geld, Governance, Locality en Execution;
- het helpt voorkomen dat nieuwe data opnieuw als ruwe of te technische tekst op de website verschijnt.

De eerste concrete deliverables zijn:

- `config/data_quality_perspectives.json`;
- een korte interne checklist in `docs/data-quality-checklist.md`;
- aanpassing van de claim- en sitegenerator zodat perspectieven in viewmodels beschikbaar komen;
- regressietests voor klikbaarheid, chronologie en public-facing tekstkwaliteit.
