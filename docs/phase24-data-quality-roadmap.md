# Langetermijnplan datakwaliteit AZWA-site

## Sprint Ledger
Gebruik deze roadmap als levend werkdocument. Werk na elke sprint de statusregel bij:

- `completed`: uitgevoerd en vastgelegd in een notitie, data-output, codewijziging of controle.
- `open`: nog niet uitgevoerd of nog niet volledig afgerond.
- Afgeronde fase- en sprintplannen staan in `docs/completed-plans/`; actieve plannen blijven in de hoofdmap `docs/`.
- Het interne dashboard `docs/internal/review-dashboard.html` moet de meest actuele sprintstand tonen. Werk bij sprintstatus, huidige planning, cleanup targets, reviewdata, brondekking of publieke updategeschiedenis altijd eerst deze roadmap bij en draai daarna `python src/build_internal_review_dashboard.py` voordat wijzigingen worden vastgelegd.
- Elk plan of elke sprintnotitie begint met een korte actuele samenvatting. Bij meer-sprintplannen heeft een Sprint Ledger bovenaan de voorkeur; bij kleinere plannen volstaat een korte samenvatting bovenaan.

| Sprint | Status | Vindplaats / opmerking |
| --- | --- | --- |
| 25.2 Lokale bronversterking Almere | open | Huidige sprint; eerste bronversterkingslaag staat in `data/extracted/local_source_strengthening_almere.json`; vervolg is directe intake van primaire lokale bijlagen en rolbronnen |
| 25.1 Werkagenda- en financieringslaag | completed | `data/extracted/workagenda_d5_operational_requirements.json`, `src/build_workagenda_d5_operational_requirements.py`, `docs/completed-plans/phase25-sprint25.1-werkagenda-financieringslaag.md` |
| 24.1 Taxonomie en checklist | completed | `config/data_quality_perspectives.json`, `docs/data-quality-checklist.md` |
| 24.2 Audit van bestaande site-data | completed | `docs/completed-plans/phase24-sprint24.2-audit.md`, `data/extracted/data_quality_audit.json` |
| 24.3 Review-dashboard intern | completed | `docs/internal/review-dashboard.html`, `src/build_internal_review_dashboard.py`, `docs/completed-plans/phase24-sprint24.3-review-dashboard.md` |
| 25.3 Nulmeting en capaciteit werkagenda | open | Nieuwe sprint uit conceptinvulling; maak per basisfunctionaliteit zichtbaar wat al bekend is en welke lokale capaciteit, dekking en aantallen ontbreken |
| 25.4 D6 governance en samenwerking | open | Niet hoogste prioriteit, wel vroeg plannen; versterk bronbasis rond wie wat doet, wie samenwerkt en wie verantwoordelijk is voor D6 |
| 25.5 Almere en Flevoland | open |  |
| 25.6 Regionale governance | open |  |
| 26.1 PDF- en tabelkwaliteit | open |  |
| 26.2 Claimtekst schoonmaken | open |  |
| 26.3 Locatie- en bewijscontrole | open |  |
| 27.1 Norm | open |  |
| 27.2 Tijd | open |  |
| 27.3 Geld | open |  |
| 27.4 Governance | open |  |
| 27.5 Locality | open |  |
| 27.6 Execution | open |  |
| 28.1 Menselijke samenvattingen per update | open |  |
| 28.2 Bronverwijzing en autoriteitstaal | open |  |
| 28.3 Detailpagina's voor drill-down | open |  |
| 29.1 Tijdlijnregister verdiepen | open |  |
| 29.2 Begrotings- en verantwoordingscyclus | open |  |
| 29.3 Handreikingen en uitvoeringsmomenten | open |  |
| 30.1 Lokale lacunes | open |  |
| 30.2 Besluitvragen en mogelijke opvolgacties | open |  |
| 30.3 Beleidsdocumenten en rapporten | open |  |
| 31.1 Updateprotocol | open |  |
| 31.2 Maandelijkse bronaudit | open |  |
| 31.3 Reviewronde met menselijke beoordelaars | open |  |

## Huidige sprintplan
Sprint 25.2 richt zich op lokale bronversterking voor Almere. Sprint 25.1 heeft de eerste D5-werkagenda operationele laag opgeleverd; de volgende stap is de primaire lokale bronbasis en rolbronnen versterken zodat die laag betrouwbaar met Almere-specifieke context kan worden gevuld.

Status op 24 april 2026: eerste tranche uitgevoerd. `data/extracted/local_source_strengthening_almere.json` maakt zichtbaar welke lokale bronnen al in de formele laag zitten, welke bronnen alleen als kandidaat of summary aanwezig zijn, en welke primaire bijlagen nog direct moeten worden opgehaald. De sprint blijft open totdat de belangrijkste primaire stukken daadwerkelijk in de bronlaag zijn opgenomen of als niet-openbaar/onvindbaar zijn verantwoord.

Eerste verbeterplan:

- Gebruik `docs/internal/AZWA, IZA and GALA for the Almere case.md` en `docs/internal/conceptinvulling_werkagenda_azwa_almere.md` als interne research-signalen voor bronhiaten, niet als primaire bronfeiten.
- Vervang waar mogelijk samenvattende contextpagina's door de onderliggende Almeerse beleidsdocumenten voor de Maatschappelijke Agenda en de Visie Gezondheidsbeleid.
- Zoek en verwerk de lokale raadsbrief `Stand van zaken Gezondheidsbeleid (IZA en GALA)` van 2 februari 2025, als deze openbaar en herleidbaar beschikbaar is.
- Controleer of de Zorgakkoorden-pagina `Handvatten voor het opstellen van de regionale werkagenda`, de officiele opdracht-PDF, het format en de proces/financieringstoelichting volledig als canonieke bronnen in de bronmanifesten en inventarislaag staan.
- Haal, waar openbaar en herleidbaar, actuele brondata binnen voor GGD Flevoland Gezondheidsmonitor 2024, de GGD Flevoland valpreventiepagina Almere, ZonMw/Zorgzaam Flevoland, actuele PGA-bronnen en actuele BRP/CBS-bevolkingsgegevens voor capaciteitsberekeningen.
- Voeg rolbronnen toe of versterk ze voor expliciete goedkeuring door gemeente of mandaatgemeente bij social-domain onderdelen van integrale transformatieplannen en voor Almere als mandaatgemeente in het Flevolandse mentale-gezondheidsnetwerk.

Geplande vervolgsprint:

- Sprint 25.3 volgt daarna voor de nulmeting en capaciteitsbasis per basisfunctionaliteit. De conceptinvulling laat zien dat de structuur van de werkagenda al goed te vullen is, maar dat lokale capaciteit, bestaand aanbod, dekking, fte, wachttijden, wijkspreiding, budget en ingroeipad nog niet besluitvast zijn. Dat is een eigen sprint waard, omdat dit de werkagenda uitvoerbaar maakt.
- Sprint 25.4 volgt daarna voor D6-governance en samenwerking. Deze is niet hoger dan de werkagenda-, lokale-bron- of nulmetingsprint, maar wel belangrijk genoeg om voor de bredere Almere/Flevoland- en governance-sprints te staan: D6 gaat sterk over rollen, lokale teams, wijkverbanden, sociale basis, GGD, zorgpartijen en regionale samenwerking, terwijl het dashboard nu laat zien dat governance-bronnen relatief dun zijn.

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
- Interne developer- en agentmaterialen mogen Engels gebruiken voor technische helderheid. Publieke en bestuurlijke inhoud blijft Nederlands. Interne dashboards mogen Engelse technische framing combineren met Nederlandse domeinlabels uit bronnen en roadmap.

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
Status: completed.

- Maak per perspectief een vaste set velden, voorbeelden en uitsluitingsregels.
- Leg vast wanneer iets een bronfeit, interpretatie, lokale lacune of menselijke keuzevraag is.
- Voeg een korte redactieregel toe voor public-facing formuleringen per perspectief.

Sprint 24.2: Audit van bestaande site-data
Status: completed.

- Label bestaande claims en viewmodels met de zes perspectieven waar mogelijk.
- Zoek brede restcategorieen zoals `timeline.other`, `monitoring.other` en `governance_and_finance.other`.
- Maak een overzicht van claims die inhoudelijk nuttig zijn maar tekstueel te ruw zijn voor publicatie.

Sprint 24.3: Review-dashboard intern
Status: completed.

- Maak een intern overzicht met open kwaliteitsissues per perspectief.
- Splits issues in bronprobleem, extractieprobleem, claimprobleem, interpretatieprobleem en tekstprobleem.
- Splits Locality in het dashboard zichtbaar uit naar Almere, IZA/AZWA-regio Flevoland en algemene of nog onduidelijke lokale relevantie.
- Houd dit intern; public-facing site mag deze technische categorieen niet tonen.

## Fase 25 - Bronkwaliteit en bronhiaten
Doel: de bronbasis versterken, vooral voor geld, tijd, governance en lokale relevantie.

Sprint 25.1: Werkagenda- en financieringslaag
Status: completed.

- Bouw eerst een operationele D5-werkagendalaag, zodat financiering kan worden gekoppeld aan concrete doelen, inwonerdiensten en basisfunctionaliteiten.
- Controleer VWS, VNG, DUS-I, wetten.nl en gemeentefondsbronnen op AZWA, SPUK, meicirculaire, werkagenda en verantwoordingsmomenten.
- Markeer welke bronnen normatief zijn en welke alleen toelichtend of praktisch zijn.
- Zoek expliciet naar regels over besteding, reservering, doorschuiven, aanvraag en verantwoording van middelen.
- Koppel per werkagenda-target mogelijke financieringsstromen, betrokken actoren, locality scope, IST/SOLL/GAP-onderdelen, mijlpalen en reviewvragen.

Sprint 25.2: Lokale bronversterking Almere
Status: open.

- Eerste uitvoerlaag toegevoegd: `data/extracted/local_source_strengthening_almere.json`.
- Deze laag behandelt interne deep-research documenten alleen als bronhiatensignaal en maakt kandidaatbronnen expliciet voordat ze als feiten in claims of publieke tekst mogen belanden.
- Gebruik `docs/internal/AZWA, IZA and GALA for the Almere case.md` als intern research-signaal, vooral de `Repository quality log`, maar behandel de daarin genoemde externe bevindingen pas als feit nadat de primaire bronnen zelf zijn opgenomen of gecontroleerd.
- Gebruik ook `docs/internal/conceptinvulling_werkagenda_azwa_almere.md` als intern research-signaal voor bronhiaten; behandel genoemde cijfers, voorbeelden en externe bronclaims pas als feit nadat de primaire bron is opgenomen of gecontroleerd.
- Vervang waar mogelijk samenvattende contextpagina's door de onderliggende Almeerse beleidsdocumenten voor de Maatschappelijke Agenda en de Visie Gezondheidsbeleid.
- Zoek en verwerk de lokale raadsbrief `Stand van zaken Gezondheidsbeleid (IZA en GALA)` van 2 februari 2025, als deze openbaar en herleidbaar beschikbaar is.
- Controleer of de Zorgakkoorden-pagina `Handvatten voor het opstellen van de regionale werkagenda`, de officiele opdracht-PDF, het format en de proces/financieringstoelichting volledig als canonieke bronnen in de bronmanifesten en inventarislaag staan.
- Haal, waar openbaar en herleidbaar, actuele brondata binnen voor GGD Flevoland Gezondheidsmonitor 2024, de GGD Flevoland valpreventiepagina Almere, ZonMw/Zorgzaam Flevoland, actuele PGA-bronnen en actuele BRP/CBS-bevolkingsgegevens voor capaciteitsberekeningen.
- Voeg rolbronnen toe of versterk ze voor: expliciete goedkeuring door gemeente of mandaatgemeente bij social-domain onderdelen van integrale transformatieplannen; en de landelijke listing waarin Almere als mandaatgemeente voor het Flevolandse mentale-gezondheidsnetwerk wordt genoemd.
- Koppel deze bronnen aan locality, governance en execution claims, en markeer waar de bron alleen een onderzoekssignaal geeft in plaats van een vastgestelde lokale keuze.
- Gebruik deze sprint ook om de door het kwaliteitsrapport genoemde representatieproblemen te triageren: `governance_and_finance.other`, `timeline.other`, onopgeloste conflicten rond lokale teams, digitale/operationele infrastructuur, regionale coordinatie, finance-local alignment en mentale gezondheidsnetwerken.

Sprint 25.3: Nulmeting en capaciteit werkagenda
Status: open.

- Bouw een nulmetingslaag per basisfunctionaliteit/aanpak, gekoppeld aan de werkagenda-targets uit Sprint 25.1.
- Leg per target vast: bestaand aanbod, locaties, bereik, capaciteit/fte, wachttijden, aanbieders, huidige financiering, wijk- of stadsdeeldekking, doelgroepomvang en bronstatus.
- Maak aparte berekenvelden voor landelijke richtwaarden die de bronbasis draagt, zoals verwijzingen per 10.000 inwoners, brugfunctionaris-fte per 10.000 inwoners, valrisico-inschatting bij 65-plussers en jeugd-/ouderenindicatoren. Gebruik actuele BRP/CBS-peildatum en markeer berekeningen als indicatief totdat bestuurlijk gevalideerd.
- Gebruik actuele GGD 2024-data alleen na opname of verificatie van de primaire tabellenboeken; koppel deze aan overgewicht, valpreventie, eenzaamheid, mentale gezondheid en kwetsbaarheid.
- Houd PGA-IZA-transformatieplan, AZWA-D5/SPUK-middelen, GALA-afspraken en reguliere gemeentelijke middelen strikt gescheiden om dubbeltelling of verkeerde financieringsclaims te voorkomen.
- Voeg per target een `decision_needed`-veld toe voor prioritering 2027-2030, schaalkeuze, eigenaar, uitvoerder, budget, monitoring en formele besluitvorming.
- Markeer expliciet welke onderdelen conceptueel te vullen zijn en welke pas na lokale of regionale besluitvorming verantwoord kunnen worden ingevuld.

Sprint 25.4: D6 governance en samenwerking
Status: open.

- Versterk bronnen over D6-rolverdeling: gemeente, mandaatgemeente, college, raad, GGD, welzijn, sociaal werk, huisartsen/eerstelijn, zorgverzekeraar, wijkteams/lokale teams en regionale samenwerkingsverbanden.
- Zoek expliciete bronpassages over wie besluit, wie coordineert, wie uitvoert, wie financiert, wie monitort en wie aanspreekbaar is bij lokale teams, hechte wijkverbanden, inloopvoorzieningen en sociale basis.
- Splits governanceclaims in besluitvorming, samenwerking, uitvoering, verantwoording en monitoring, zodat D6 niet alleen als inhoudelijke infrastructuur maar ook als verantwoordelijkheidsmodel zichtbaar wordt.
- Controleer of `d6.local_teams`, `d6.basisinfrastructuur`, `d6.regional_coordination`, `municipal.role_allocation` en `governance.regional_coordination` genoeg bronbasis hebben voor Almere/Flevoland-duiding.
- Voeg reviewpunten toe waar de bronbasis alleen samenwerking noemt maar geen expliciete taak- of besluitverdeling geeft.
- Laat het interne dashboard D6-governance als apart aandachtspunt tonen als de brondekking of claimduiding zwak blijft.

Sprint 25.5: Almere en Flevoland
Status: open.

- Zoek bestuurlijke agenda's, raadsinformatie, begrotingsstukken en lokale beleidsdocumenten die AZWA, IZA, GALA, preventie, sociaal domein of gezondheid raken.
- Voeg alleen bronnen toe die openbaar en herleidbaar zijn.
- Leg vast waar landelijke doelen nog niet zichtbaar lokaal zijn overgenomen.

Sprint 25.6: Regionale governance
Status: open.

- Versterk bronnen over mandaatgemeente, regio, zorgverzekeraar, GGD, regionale preventie-infrastructuur en werkagenda.
- Maak onderscheid tussen wie formeel besluit, wie voorbereidt en wie uitvoert.
- Controleer of de website dit onderscheid begrijpelijk weergeeft.

## Fase 26 - Extractiekwaliteit
Doel: minder halve zinnen, betere tabellen, betere paginaverwijzingen en betere broncitaten.

Sprint 26.1: PDF- en tabelkwaliteit
Status: open.

- Verbeter extractie van tabellen met middelen, jaartallen, deadlines en rollen.
- Bewaar tabelrijen als afzonderlijke bewijsobjecten waar dat kan.
- Controleer sleutelbronnen handmatig op ontbrekende of verkeerd samengevoegde rijen.

Sprint 26.2: Claimtekst schoonmaken
Status: open.

- Voorkom dat claims bestaan uit afgebroken zinnen, voetteksten, kopregels of navigatietekst.
- Bewaar ruwe broncitaten, maar genereer aparte leesbare claim-samenvattingen voor sitegebruik.
- Voeg regressietests toe voor bekende probleemvormen.

Sprint 26.3: Locatie- en bewijscontrole
Status: open.

- Controleer dat belangrijke claims minimaal pagina, sectie, quote of chunk-id hebben.
- HTML-bronnen krijgen sectie- en chunkverwijzingen als paginanummers niet bestaan.
- Claims zonder bruikbare locatie gaan naar review.

## Fase 27 - Claimmodel per perspectief
Doel: van algemene claims naar beleidsmatig bruikbare claims per Norm, Tijd, Geld, Governance, Locality en Execution.

Sprint 27.1: Norm
Status: open.

- Splits normclaims in bindend, afspraak, verwachting, toelichting en lagere-autoriteitssignaal.
- Voorkom dat VNG-FAQ's, nieuwsberichten of toelichtingen klinken als harde norm.
- Maak conflicten of onzekerheid expliciet in mensentaal.

Sprint 27.2: Tijd
Status: open.

- Maak deadlines, verwachte publicatiemomenten, reviewmomenten en begrotingsmomenten aparte tijdclaims.
- Sorteer en groepeer tijdlijnitems structureel chronologisch.
- Markeer verwachte momenten duidelijk anders dan vastgestelde deadlines.

Sprint 27.3: Geld
Status: open.

- Maak claims voor financieringsinstrument, aanvraagvoorwaarde, budgetvenster, verdeelmechanisme, bestedingsruimte en verantwoording.
- Leg onzekerheden over uitkering, overloop, reservering en besteding apart vast.
- Voeg een zoekbare categorie toe voor "te verifieren financieringsregel".

Sprint 27.4: Governance
Status: open.

- Maak rollen expliciet: ministerie, VNG, fondsbeheerder, mandaatgemeente, regio, gemeente, raad, college, zorgverzekeraar, uitvoeringspartner.
- Splits besluitvorming, coordinatie, aanvraag, uitvoering en verantwoording.
- Voorkom dat "regio" als actor wordt gebruikt als de bron specifieker is.

Sprint 27.5: Locality
Status: open.

- Markeer claims die expliciet over Almere gaan anders dan claims die alleen algemeen voor gemeenten gelden.
- Markeer Flevolandse claims apart van Almeerse claims.
- Houd adoptiegaten zichtbaar: landelijk doel aanwezig, lokale openbare uitwerking nog niet gevonden.

Sprint 27.6: Execution
Status: open.

- Vertaal bronclaims naar mogelijke uitvoeringsvragen zonder beleidsadvies toe te voegen.
- Splits mogelijke besluitvragen, mogelijke opvolgacties, afhankelijkheden en reviewvragen.
- Laat de site niet suggereren dat een actie al is besloten als alleen de bronbasis aanleiding geeft om deze te onderzoeken.

## Fase 28 - Tekstkwaliteit van de website
Doel: minder technische of ruwe tekst, meer bestuurlijk leesbare Nederlandse samenvattingen.

Sprint 28.1: Menselijke samenvattingen per update
Status: open.

- Elke data-update krijgt een korte, leesbare samenvatting.
- Leg uit welke publicatie aanleiding was voor de update.
- Benoem wat inhoudelijk is veranderd, zonder interne datatermen.

Sprint 28.2: Bronverwijzing en autoriteitstaal
Status: open.

- Lagere-autoriteitsbronnen worden expliciet toegeschreven, bijvoorbeeld "Volgens de VNG-toelichting..." of "DUS-I vermeldt...".
- Normatieve bronnen krijgen sterkere formulering, maar alleen waar de bron dat draagt.
- Onzekerheden blijven zichtbaar zonder dramatische woorden als urgent of kritisch.

Sprint 28.3: Detailpagina's voor drill-down
Status: open.

- Overzichtspagina's blijven kort.
- Lange claimlijsten, bronlijsten en reviewdetails gaan naar aparte detailpagina's.
- Elke klikbare tegel of telling moet naar de onderliggende items leiden.

## Fase 29 - Tijdlijn als beleidsinstrument
Doel: de tijdlijn gebruiken voor bestuurlijke orientatie, niet alleen als chronologische lijst.

Sprint 29.1: Tijdlijnregister verdiepen
Status: open.

- Voeg bronstatus, autoriteit, actor, type moment en gevolg voor Almere toe aan tijdlijnitems.
- Houd verwachte, formele en lokale momenten zichtbaar verschillend.
- Leg per item vast welk perspectief vooral geraakt wordt: Tijd, Geld, Governance of Execution.

Sprint 29.2: Begrotings- en verantwoordingscyclus
Status: open.

- Voeg landelijke en lokale begrotingsmomenten toe zodra ze bronvast zijn.
- Koppel gemeentefonds, meicirculaire, septembercirculaire, begroting Almere en SPUK-verantwoording waar bronnen dit dragen.
- Markeer waar menselijke beoordeling nodig is om een extern moment naar lokale planning te vertalen.

Sprint 29.3: Handreikingen en uitvoeringsmomenten
Status: open.

- Houd handreikingen, webinars, thematafels en formatdocumenten apart van formele besluiten.
- Gebruik deze bronnen wel voor uitvoering en voorbereiding, maar niet als harde norm.
- Voeg nieuwe documenten pas toe na volledige pipeline-verwerking.

## Fase 30 - Lokale beleidsbruikbaarheid
Doel: de site beter laten aansluiten op vragen van Almeerse beleidsmakers.

Sprint 30.1: Lokale lacunes
Status: open.

- Maak per thema zichtbaar welke landelijke of regionale opgave nog niet openbaar lokaal is uitgewerkt.
- Voorkom oordeelstaal; formuleer als documentatie- of adoptiegat.
- Koppel elk gat aan bronbasis en mogelijke vervolgvraag.

Sprint 30.2: Besluitvragen en mogelijke opvolgacties
Status: open.

- Herclassificeer bestaande besluitvragen en opvolgacties langs de zes perspectieven.
- Maak duidelijk welke vraag door bronbasis wordt opgeroepen en welke invulling aan Almere is.
- Verwijder of herformuleer items die te veel als advies klinken.

Sprint 30.3: Beleidsdocumenten en rapporten
Status: open.

- Laat public-facing rapporten alleen publieke bronnen noemen, geen interne datalagen.
- Controleer plannen van aanpak op verzonnen bijlagen, bedragen, FTE's, deadlines en scenario's.
- Houd een aparte interne notitie bij voor technische controles.

## Fase 31 - Periodieke actualisatie
Doel: zorgen dat de site meebeweegt met nieuwe bronnen zonder dat oude informatie wordt overschreven.

Sprint 31.1: Updateprotocol
Status: open.

- Maak een vaste procedure voor nieuwe publicaties.
- Nieuwe broninformatie krijgt altijd een changelog met inhoudelijke delta.
- Oude claims blijven bewaard; nieuwe claims kunnen aanvullen, verduidelijken, beperken of tegenspreken.

Sprint 31.2: Maandelijkse bronaudit
Status: open.

- Controleer of verwachte bronnen zijn verschenen, zoals circulaires, SPUK-regelingen, handreikingen en monitorrapportages.
- Controleer dode links en gewijzigde webpagina's.
- Houd pending bronnen apart tot ze door de pipeline zijn verwerkt.

Sprint 31.3: Reviewronde met menselijke beoordelaars
Status: open.

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

## Huidige volgende sprint
De beste eerstvolgende sprint is Sprint 25.2: Lokale bronversterking Almere.

Waarom:

- Sprint 24.1 heeft de taxonomie en checklist opgeleverd;
- Sprint 24.2 heeft een interne auditbasis opgeleverd;
- Sprint 24.3 heeft een lokaal intern review-dashboard opgeleverd;
- Sprint 25.1 heeft de werkagenda-operatielaag opgeleverd;
- de volgende stap is het versterken van de primaire lokale bronbasis en rolbronnen zodat de werkagendalaag met Almere-specifieke informatie kan worden gevuld.

De concrete deliverables zijn:

- een gecontroleerde lijst met toe te voegen of te vervangen lokale bronnen;
- verwerking of review van primaire Almeerse beleidsdocumenten;
- bronvast onderscheid tussen lokale, regionale, GGD-, zorgkantoor- en uitvoeringsschaal;
- versterkte rolbronnen rond mandaatgemeente, gemeente/college en social-domain goedkeuring;
- een korte datakwaliteitsnotitie met open lokale bronvragen.
