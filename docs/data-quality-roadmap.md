# Datakwaliteitsroadmap AZWA-site

## Sprint Ledger
Gebruik deze roadmap als levend werkdocument. Werk na elke sprint de statusregel bij:

- `completed`: uitgevoerd en vastgelegd in een notitie, data-output, codewijziging of controle.
- `open`: nog niet uitgevoerd of nog niet volledig afgerond.
- Afgeronde fase- en sprintplannen staan in `docs/completed-plans/`; actieve plannen blijven in de hoofdmap `docs/`.
- Het interne dashboard `docs/internal/review-dashboard.html` moet de meest actuele sprintstand tonen. Werk bij sprintstatus, huidige planning, cleanup targets, reviewdata, brondekking of publieke updategeschiedenis altijd eerst deze roadmap bij en draai daarna `python src/build_internal_review_dashboard.py` voordat wijzigingen worden vastgelegd.
- Elk plan of elke sprintnotitie begint met een korte actuele samenvatting. Bij meer-sprintplannen heeft een Sprint Ledger bovenaan de voorkeur; bij kleinere plannen volstaat een korte samenvatting bovenaan.

| Sprint | Status | Vindplaats / opmerking |
| --- | --- | --- |
| 25.2 Lokale bronversterking Almere | completed | `data/extracted/local_source_strengthening_almere.json`, `docs/internal/source-intake/phase25.2-public-source-assessment.md`, `docs/completed-plans/phase25-sprint25.2-lokale-bronversterking.md` |
| 25.1 Werkagenda- en financieringslaag | completed | `data/extracted/workagenda_d5_operational_requirements.json`, `src/build_workagenda_d5_operational_requirements.py`, `docs/completed-plans/phase25-sprint25.1-werkagenda-financieringslaag.md` |
| 24.1 Taxonomie en checklist | completed | `config/data_quality_perspectives.json`, `docs/data-quality-checklist.md` |
| 24.2 Audit van bestaande site-data | completed | `docs/completed-plans/phase24-sprint24.2-audit.md`, `data/extracted/data_quality_audit.json` |
| 24.3 Review-dashboard intern | completed | `docs/internal/review-dashboard.html`, `src/build_internal_review_dashboard.py`, `docs/completed-plans/phase24-sprint24.3-review-dashboard.md` |
| 25.3 Nulmeting en capaciteit werkagenda | completed | `data/extracted/workagenda_nulmeting_capacity.json`, `src/build_workagenda_nulmeting_capacity.py`, `docs/completed-plans/phase25-sprint25.3-nulmeting-capaciteit.md` |
| 25.4 D6 governance en samenwerking | open | Heropend voor D6 Almere responsibility pack: `docs/phase25-sprint25.4-d6-almere-responsibility-pack-plan.md`; registerlaag staat in `data/extracted/municipal/almere_d6_responsibility_register.json` en schema in `data/schemas/almere_d6_responsibility_register.schema.json` |
| 24.6 D6 commit, verify and stabilize | completed | Remediation is gecommit/gepusht; verificatie via `python src/run_pipeline.py --all`, gerichte tests en schema-validatie |
| 24.7 D6 register evidence audit | completed | Registerrijen gecontroleerd op status, eigenaar, uitvoerder, schaal, financiering, bewijs en open reviewvraag |
| 24.8 D6 local validation preparation | completed | Interne validatiepack: `docs/review/almere_d6_validation_pack.md` |
| 25.5 D6 stakeholder validation handoff | completed | Repository-side handoff compleet; wacht op policy-maker stakeholdervalidatie. Artifacts in `docs/review/almere_d6_public_source_boundary.md`, `docs/review/almere_d6_validation_handoff_summary.md`, `docs/review/almere_d6_validation_pack.md`, `docs/review/almere_d6_stakeholder_validation_log.md`, `docs/review/almere_d6_stakeholder_information_request.md`, `docs/review/almere_d6_decision_needed.md`, `docs/review/almere_d6_funding_gap_table.md` en `docs/review/almere_d6_safe_wording.md` |
| 25.6 Post-validation register hardening | parked | Geparkeerd tot stakeholder-validatierecords, lokale/interne documenten, finance/controller bevestiging of expliciet beleidsbesluit beschikbaar zijn; blokkeert Fase 26 niet |
| 26.1 Rough-claim audit hercalibratie | completed | `src/build_data_quality_audit.py`, `tests/test_data_quality_audit.py`, `data/extracted/data_quality_audit.json`, `docs/completed-plans/phase26-sprint26.1-rough-claim-audit-recalibration.md` |
| 26.2 Deterministische tekstfixes | completed | `src/build_structural_extractions.py`, `src/build_document_extractions.py`, `data/extracted/voting_records.json`, `data/logs/phase26_text_cleanup.json`, `docs/completed-plans/phase26-sprint26.2-deterministic-text-fixes.md` |
| 26.3 Sentence-boundary en dedup | completed | `src/build_claims_top5.py`, `src/verify_claim_id_references.py`, `data/extracted/claims/sentence_validator_rejects.json`, `data/extracted/claims/dedup_log.json`, `docs/completed-plans/phase26-sprint26.3-sentence-boundary-dedup.md` |
| 27.1 Norm | completed | `src/build_claims_top5.py`, `data/schemas/claim.schema.json`, `data/extracted/data_quality_audit.json`, `docs/completed-plans/phase27-sprint27.1-norm.md` |
| 27.2 Tijd | completed | `src/build_claims_top5.py`, `data/schemas/claim.schema.json`, `data/extracted/data_quality_audit.json`, `data/site/timeline_register.json`, `docs/completed-plans/phase27-sprint27.2-tijd.md` |
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
Fase 27 is de actieve repository-side perspectiefverfijningsfase. Sprint 25.6 blijft geparkeerd omdat post-validatie hardening pas verantwoord is na stakeholdervalidatierecords, lokale/interne documenten, finance/controller bevestiging of een expliciet beleidsbesluit. Dat is geen blocker voor verdere datakwaliteitswerk: de repository kan intussen norm-, tijd-, geld-, governance-, locality- en execution-guardrails verbeteren zonder D6-inhoud te overclaimen.

Status op 26 april 2026: Sprint 25.2 is afgerond als publieke bronversterkingssprint. `data/extracted/local_source_strengthening_almere.json` maakt zichtbaar welke lokale bronnen in de formele laag zitten, welke publieke bronnen als assessmentmateriaal zijn beoordeeld, en welke vragen naar later in de workflow gaan omdat de publieke bronbasis is uitgeput of omdat een geschoonde validatiestap nodig is. De geselecteerde Documentwijzer-bijlagen voor Visie Gezondheidsbeleid en Maatschappelijke Agenda zijn eerst naar page-markdown omgezet en daarna opgenomen in `data/raw/manifest.json`. Ook de GGD-tabellenboeken voor volwassenen en ouderen, de GGD-valpreventiepagina Almere en de ZonMw-bron zijn opgenomen in `data/raw/manifest.json`, door inventory/extractie/claims/site-viewmodels verwerkt en blijven reviewmateriaal voordat ze bestuurlijk of public-facing worden gebruikt. Niet-publieke informatie, ontbrekende lokale bevestiging en formele besluitvragen blokkeren deze fase niet; ze worden als gaten of carry-over taken zichtbaar gemaakt voor lokale medewerkers en latere besluitvorming.

Status op 26 april 2026: Sprint 25.4a is afgerond in `data/extracted/d6_governance_collaboration.json`. De laag gebruikt de publieke claims, de regionale rollen/splits-guardrail en de nulmeting uit Sprint 25.3 om per D6-dimensie de publieke brondekking, actorrollen, verantwoordelijkheidsprefill, lokale validatievelden en besluitvragen zichtbaar te maken. Niet-publieke rolverdeling, eigenaarschap, budget, monitoring en schaalkeuzes blijven invul- of besluitvragen.

Status op 26 april 2026: Sprint 25.4b is geopend in `docs/phase25-sprint25.4-d6-almere-responsibility-pack-plan.md`. De nieuwe focus is niet een algemene D6-samenvatting, maar een Almere responsibility pack rond lokale toegang, wijkteams, Stevige Lokale Teams, GGD/JGZ, mentale-gezondheidswijkinfrastructuur, monitoring/data, regionale/lokale uitvoering en financieringsafbakening.

Status op 27 april 2026: eerste 25.4b-bronintake uitgevoerd. Zeven publieke bronnen zijn toegevoegd aan `data/raw/manifest.json` en door inventory, structural extraction, document extraction, claims, current interpretation, D6-lagen, QC, site-viewmodels en intern dashboard verwerkt: Stevige Lokale Teams raadspagina, Wijkteams Almere, VNG Richtinggevend Kader, Toezicht Sociaal Domein Basisfuncties, GGD Flevoland Begroting 2026, GGD Flevoland Kennis en Advies, en GGD Flevoland/JGZ Almere profiel. Onderliggende Documentwijzer-stukken bij Stevige Lokale Teams en de Almere Samen Sterker/samenwerkingsprojectenpagina's blijven open intakewerk omdat ze gerichte selectie of hernieuwde publieke download/verificatie vragen.

Status op 27 april 2026: gate-remediation gestart. De sprint gaat niet door naar rapportproductie of bestuurlijke werkagenda-drafting; de toegestane vervolgstap is alleen D6 responsibility implementation/remediation. Zes extra bronnen zijn toegevoegd: vier Documentwijzer/Notubiz-stukken bij Stevige Lokale Teams, de Almere Samenwerkingsprojecten/Samen Sterker-bron en een actuele PGA-homepage. De lokale decision layer bevat nu een source-backed publieke raadbeslissing voor Stevige Lokale Teams, met D6-classificatie nog expliciet op `review_needed`.

Status op 28 april 2026: Sprint 25.6 is geparkeerd als policy-maker/stakeholder-afhankelijkheid en blokkeert repository-side datakwaliteitswerk niet. Fase 26 is gestart met rough-claim cleanup. Sprint 26.1 is afgerond als audit-hercalibratie: de lengte-only rough-code is vervangen door `unverified_extraction_length`, langere excerpts geven reviewers meer context, en regressietests bewaken dat lange maar goed gevormde claims niet alleen door lengte rough worden. Sprint 26.2 is afgerond als deterministische tekstfix: mojibake, letterhead, TOC-/Drupal-ruis en stemuitslagen worden uit claim-input gehouden; stemuitslagen blijven apart bewaard in `data/extracted/voting_records.json`. Sprint 26.3 is afgerond als sentence-boundary/dedup sprint: lowercase mid-zin-claims worden uit de masterlaag geweerd, duplicate openings binnen document/topic/subtopic worden geconsolideerd, en `src/verify_claim_id_references.py` controleert downstream claim-id verwijzingen.

Status op 29 april 2026: Sprint 27.1 is afgerond als norm-splitsing. Elke claim krijgt nu een `normative_status` met de waarden `binding`, `agreement`, `expectation`, `guidance`, `lower_authority_signal` of `contextual`. De audit bevat een `normative_status_audit`, de site-evidence draagt normstatus mee, en QC markeert lagere-autoriteitssignalen expliciet als reviewpunt zodat FAQ's, toelichtingen en regionale/lokale context niet als harde norm worden gelezen.

Status op 29 april 2026: Sprint 27.2 is afgerond als tijd-splitsing. Elke claim krijgt nu een `time_status` met onderscheid tussen formele deadlines, verwachte momenten, review-/actualisatiemomenten, budgetkalendermomenten, implementatiehorizons, lokale planningscontext, bronverankerde tijdmomenten, publicatie-/contextdata en ongedateerde context. De audit bevat een `time_status_audit`, site-evidence en tijdlijnitems dragen tijdstatus mee, en QC markeert verwachte momenten en lokale planningscontext als reviewpunt zodat indicatieve momenten en lokale raadsagenda's niet als harde D5/D6-deadlines worden gelezen.

Afgeronde aanpak voor Sprint 25.4a:

- Gebruik publieke bronnen eerst om D6-rollen te ordenen; als bronnen geen taak, eigenaar of besluit geven, markeer dit als lokale validatie of besluitvraag.
- Houd IZA/AZWA-regio, GGD-regio, zorgkantoorregio en lokale uitvoering strikt uit elkaar.
- Maak per D6-dimensie zichtbaar welke bron alleen samenwerking of ambitie noemt en welke bron ook besluitvorming, uitvoering, financiering of monitoring aanwijst.
- Gebruik `data/extracted/d6_governance_collaboration.json` als werklijst voor lokale medewerkers: lokale teams, wijkverbanden, inloopvoorzieningen, sociale basispartners, monitoring en eigenaarschap.
- Schuif formele mandaat-, budget- en schaalkeuzes door naar besluitvorming wanneer de publieke bronbasis geen vastgesteld antwoord geeft.

Aanpak voor heropende Sprint 25.4b:

- Verifieer en intake publieke D6-uitvoeringsbronnen: Stevige Lokale Teams, Wijkteams Almere, VNG Richtinggevend Kader, Toezicht Sociaal Domein Basisfuncties, GGD Flevoland Begroting/Ontwerpbegroting 2026, GGD Kennis en Advies, JGZ Almere, Samen Sterker in de Wijk, actuele PGA-samenwerking en selectieve GGZ/partnerbronnen.
- Maak een D6 responsibility register voor Almere met bestaande voorziening, benodigde upgrade, eigenaar, uitvoerder, partners, schaal, financiering, besluitstatus, bronstatus, confidence en open issue. Eerste uitvoer: `data/extracted/municipal/almere_d6_responsibility_register.json`.
- Markeer elke rij als feit, interpretatie, voorstel, lokale validatie of later besluit.
- Gebruik lokale besluitdocumenten alleen als `settled` wanneer de bronpassage dit draagt; behandel andere invulling als prefill of reviewtaak.
- Houd Almere-local, IZA/AZWA-regio Flevoland, GGD-regio Flevoland, zorgkantoorregio en project-/programmaschaal strikt gescheiden.

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
Status: completed.

- Eerste uitvoerlaag toegevoegd: `data/extracted/local_source_strengthening_almere.json`.
- Deze laag behandelt interne deep-research documenten alleen als bronhiatensignaal en maakt kandidaatbronnen expliciet voordat ze als feiten in claims of publieke tekst mogen belanden.
- Publieke bronprobe uitgevoerd en beoordeeld in `docs/internal/source-intake/phase25.2-public-source-assessment.md`. Eerste intakebatch is inhoudelijk afgebakend; MGN-contactgegevens en andere persoons-/contactdetails mogen niet als claim of publieke tekst worden gepromoveerd.
- Eerste formele intakebatch toegevoegd aan `data/raw/manifest.json`: GGD Flevoland tabellenboeken 2024 voor volwassenen en ouderen, GGD Flevoland Valpreventie Gemeente Almere, en ZonMw Doorontwikkeling Zorgzaam Flevoland. Deze bronnen zijn verwerkt tot inventory, extracties, claims, site-viewmodels en intern dashboard; claims blijven reviewmateriaal.
- Eerste Documentwijzer-intake toegevoegd aan `data/raw/manifest.json`: beleidstekst, geamendeerd raadsvoorstel en besluitenlijst voor de Visie Gezondheidsbeleid; Brede SPUK/GALA plan van aanpak; beleidstekst, geamendeerd raadsvoorstel, besluitenlijst en evaluatie-opzet voor de Maatschappelijke Agenda. Alle acht stukken zijn eerst geconverteerd naar page-markdown en daarna door de pipeline verwerkt; claims blijven reviewmateriaal.
- `docs/internal/AZWA, IZA and GALA for the Almere case.md` en `docs/internal/conceptinvulling_werkagenda_azwa_almere.md` zijn vastgelegd als interne research-signalen voor bronhiaten, niet als primaire bronfeiten.
- Samenvattende contextpagina's voor Maatschappelijke Agenda en Visie Gezondheidsbeleid zijn versterkt met onderliggende Documentwijzer-bijlagen.
- De lokale raadsbrief `Stand van zaken Gezondheidsbeleid (IZA en GALA)` van 2 februari 2025 is niet gevonden in de publieke probe en is daarom doorgeschoven naar lokale validatie; dit blokkeert de publieke werkagenda-structuur niet.
- De Zorgakkoorden-opdracht, het format en de proces/financieringstoelichting voor de werkagenda zijn al onderdeel van de formele bronlaag vanuit Sprint 25.1.
- GGD Flevoland Gezondheidsmonitor-tabellenboeken 2024, de GGD Flevoland valpreventiepagina Almere en ZonMw/Zorgzaam Flevoland zijn opgenomen; haal daarna nog actuele PGA-bronnen en stabiele BRP/CBS-bronnen binnen voor capaciteitsberekeningen.
- MGN-rol/geografie is doorgeschoven naar een geschoonde validatiestap omdat de publieke pagina contactgegevens bevat; dit blokkeert de publieke werkagenda-structuur niet.
- De nieuwe bronnen zijn gekoppeld aan locality, governance en execution claims waar mogelijk; claims blijven reviewmateriaal totdat ze bestuurlijk of public-facing worden gebruikt.
- Open lokale bronvragen zijn expliciet carry-over naar Sprint 25.3, lokale medewerkers of latere besluitvorming wanneer publieke informatie is uitgeput.

Sprint 25.3: Nulmeting en capaciteit werkagenda
Status: completed.

- Eerste uitvoerlaag toegevoegd: `data/extracted/workagenda_nulmeting_capacity.json`.
- De laag vult de werkagenda-structuur zo ver mogelijk met publieke bronnen en markeert lokale invulvelden expliciet voor medewerkers of latere besluitvorming.
- Indicatieve berekeningen zijn toegevoegd voor sociaal verwijzen en valpreventie met CBS KWB 2025 Almere als denominator; deze berekeningen blijven indicatief totdat lokaal gevalideerd.
- GGD Flevoland 2024-indicatoren zijn gekoppeld aan relevante targets zoals valpreventie, overgewicht/obesitas volwassenen, laagdrempelige steunpunten en mentale gezondheidsnetwerken; claims uit de tabellenboeken blijven reviewmateriaal.
- De resterende capaciteit, fte, wachttijden, wijkspreiding, budget, eigenaar en besluitstatus zijn als lokale invulvelden vastgelegd in plaats van ingevuld zonder bron.
- Bouw een nulmetingslaag per basisfunctionaliteit/aanpak, gekoppeld aan de werkagenda-targets uit Sprint 25.1.
- Leg per target vast: bestaand aanbod, locaties, bereik, capaciteit/fte, wachttijden, aanbieders, huidige financiering, wijk- of stadsdeeldekking, doelgroepomvang en bronstatus.
- Maak aparte berekenvelden voor landelijke richtwaarden die de bronbasis draagt, zoals verwijzingen per 10.000 inwoners, brugfunctionaris-fte per 10.000 inwoners, valrisico-inschatting bij 65-plussers en jeugd-/ouderenindicatoren. Gebruik actuele BRP/CBS-peildatum en markeer berekeningen als indicatief totdat bestuurlijk gevalideerd.
- Gebruik actuele GGD 2024-data alleen na opname of verificatie van de primaire tabellenboeken; koppel deze aan overgewicht, valpreventie, eenzaamheid, mentale gezondheid en kwetsbaarheid.
- Houd PGA-IZA-transformatieplan, AZWA-D5/SPUK-middelen, GALA-afspraken en reguliere gemeentelijke middelen strikt gescheiden om dubbeltelling of verkeerde financieringsclaims te voorkomen.
- Voeg per target een `decision_needed`-veld toe voor prioritering 2027-2030, schaalkeuze, eigenaar, uitvoerder, budget, monitoring en formele besluitvorming.
- Markeer expliciet welke onderdelen conceptueel te vullen zijn en welke pas na lokale of regionale besluitvorming verantwoord kunnen worden ingevuld.

Sprint 25.4: D6 governance en samenwerking
Status: open.

- Eerste uitvoerlaag toegevoegd: `data/extracted/d6_governance_collaboration.json`.
- De laag splitst D6 in basisinfrastructuur, lokale teams/wijkverbanden, inloopvoorzieningen/steunpunten, regionale coordinatie en monitoring/leren.
- Actorrollen voor Almere, GGD Flevoland, Zorgzaam Flevoland/Flever, zorgverzekeraar/zorgkantoor, welzijn/sociaal werk en huisartsen/eerstelijn zijn als publieke rolhypothese of bronstatus opgenomen met validatievelden.
- Verantwoordelijkheidssloten toegevoegd voor besluitvorming, coordinatie, uitvoering, financiering en monitoring/verantwoording.
- Per D6-dimensie zijn besluitvragen toegevoegd met publieke prefill waar mogelijk en lokale validatiestatus waar publieke bronnen geen vastgesteld antwoord geven.
- Het interne dashboard toont D6-governance als apart aandachtspunt met dimensies, actorrollen, verantwoordelijkheidsprefill en besluitvragen.
- Niet-publieke rolverdeling, mandaat, budget, monitoring en schaalkeuzes zijn doorgeschoven naar lokale validatie of latere besluitvorming.
- Sprint 25.4 is heropend met `docs/phase25-sprint25.4-d6-almere-responsibility-pack-plan.md` omdat de bronbasis rond lokale D6-verantwoordelijkheid voor Almere nog versterking vraagt.
- Eerste D6 Almere responsibility register toegevoegd in `data/extracted/municipal/almere_d6_responsibility_register.json` met twaalf startcomponenten, publieke bronstatus en lokale validatie-/besluitvelden.
- Registerintegratie aangescherpt met schema, research-agent routing en QC-checks voor bewijs per rij, toegestane besluitstatus, lokale autoriteitsbron bij `settled`, en uitsluiting van `data/site` als registerbewijs.
- Interne D6-validatiepack toegevoegd in `docs/review/almere_d6_validation_pack.md`; dit is validatiemateriaal en geen finale publicatie of bestuurlijke werkagendatekst.

Sprint 25.5: D6 stakeholder validation handoff
Status: repository-side complete; awaiting policy-maker stakeholder validation.

Repository-team verantwoordelijkheid:

- Completeer de publieke-brongrens in `docs/review/almere_d6_public_source_boundary.md`.
- Onderhoud de validatiepack, informatie-uitvraag, decision-needed lijst, funding-gap tabel en safe-wording bibliotheek.
- Documenteer welke D6-classificatie-, eigenaarschap-, mandaat-, financierings- en woordingsvragen niet meer uit publieke bronnen kunnen worden beantwoord.
- Houd de registerstatus conservatief: geen `settled` zonder traceerbare validatie of autoritatieve lokale bron.

Policy-maker/stakeholder verantwoordelijkheid:

- Voer feitelijke validatiesessies met Gemeente Almere, Wijkteams Almere, JGZ Almere/GGD Flevoland, PGA/Zorgzaam/Flever, mentale-gezondheids/wijkgerichte samenwerking en regionale werkagenda-governance.
- Lever lokale/interne documenten, finance/controller bevestiging of validatierecords.
- Bevestig of corrigeer eigenaarschap, mandaat, financiering, schaal en veilige werkagendaformulering.

Gate-conditie:

- Sprint 25.5 is repository-side afgerond. De daadwerkelijke stakeholdervalidatie blijft een policy-maker afhankelijkheid.
- Sprint 25.6 blijft geblokkeerd tot zulke validatierecords of besluiten beschikbaar zijn.

Sprint 25.6: Post-validation register hardening
Status: parked until stakeholder validation records or explicit policy decisions exist.

- Verwerk alleen gevalideerde stakeholderrecords, lokale/interne documenten, finance/controller bevestigingen of expliciete beleidsbesluiten.
- Verander geen D6-registerrij naar `settled` zonder traceerbaar bewijs.
- Drafting of finale werkagendatekst blijft geblokkeerd tot deze hardening is afgerond en opnieuw gegatet.
- Deze sprint is een externe beleidsvalidatie-afhankelijkheid en blokkeert Fase 26 niet; repository-side datakwaliteitswerk mag doorgaan zolang D6-rijen niet inhoudelijk worden ingevuld zonder validatie.

## Fase 26 - Ruwe claim cleanup en extractiekwaliteit
Doel: het aantal ruwe publicatieclaims terugbrengen door eerst de auditdrempels te kalibreren en daarna deterministische extractie- en claimtekstfixes door te voeren. Deze fase wijzigt niet automatisch beleidsinhoud; zij verbetert detectie, reviewbaarheid en tekstkwaliteit.

Sprint 26.1: Rough-claim audit hercalibratie
Status: completed.

- Herkalibreer de audit zodat lengte alleen nog rough wordt wanneer er ook een extractiesignaal is: lowercase fragmentstart buiten whitelist, ontbrekende slotpunctuatie of tabel-/kolommerging.
- Hernoem de lengtecode van `long_raw_excerpt` naar `unverified_extraction_length`.
- Vergroot de review-excerpt in de audit naar 400 tekens zodat menselijke reviewers meer context zien.
- Voeg regressietests toe voor lange maar goed gevormde claims, lowercase fragmenten, tabelmerge-fingerprints en excerptlengte.
- Laat claimcontent zelf ongemoeid; deze sprint verbetert alleen detectie, auditoutput en dashboard/QC-compatibiliteit.

Sprint 26.2: Deterministische tekstfixes
Status: completed.

- Pak na de audit-hercalibratie de echte bron van ruwe claims aan: mojibake, letterhead, inhoudsopgavefragmenten, navigatietekst, stemmings-/raadsmetadata en andere deterministische extractieruis.
- Pas filters toe in de vroegste veilige pipelinefase, bij voorkeur structural extraction of claimvorming, zodat downstream lagen minder ruis ontvangen.
- Voeg regressietests toe voor bekende probleemvormen en controleer dat inhoudelijke bronzinnen niet worden weggefilterd.
- Eerste uitvoer: `encoding_noise` en `raw_letterhead` zijn naar 0 gebracht; Drupal-linkruis en stemuitslagclaims zijn niet meer aanwezig in `claims_master.jsonl`.
- Stemuitslagen zijn niet weggegooid, maar apart vastgelegd in `data/extracted/voting_records.json`.

Sprint 26.3: Sentence-boundary en dedup
Status: completed.

- Verbeter zinsegmentatie zodat claims niet halverwege een zin beginnen of zonder zelfstandig einde worden gepubliceerd.
- Verminder overlap en dubbele claims die uit dezelfde passage voortkomen.
- Controleer daarna opnieuw locatie- en bewijsvelden; claims zonder bruikbare locatie blijven reviewmateriaal.
- Eerste uitvoer: `claims_master.jsonl` bevat 524 claims, 0 lowercase mid-zin-starts en 0 duplicate first-200-char groepen binnen document/topic/subtopic.
- De sentence-boundary gate heeft 84 claims geweerd en 34 langere claims met ontbrekende slotpunctuatie als review-only gelogd in `data/extracted/claims/sentence_validator_rejects.json`.
- De dedup-pass heeft 7 duplicate groepen geconsolideerd in `data/extracted/claims/dedup_log.json`.
- `src/verify_claim_id_references.py` is toegevoegd en draait groen op `data/extracted` en `data/site`.

## Fase 27 - Claimmodel per perspectief
Doel: van algemene claims naar beleidsmatig bruikbare claims per Norm, Tijd, Geld, Governance, Locality en Execution.

Sprint 27.1: Norm
Status: completed.

- Splits normclaims in bindend, afspraak, verwachting, toelichting en lagere-autoriteitssignaal.
- Voorkom dat VNG-FAQ's, nieuwsberichten of toelichtingen klinken als harde norm.
- Maak conflicten of onzekerheid expliciet in mensentaal.
- Eerste uitvoer: alle 524 claims dragen een `normative_status`.
- Verdeling: 2 `binding`, 74 `agreement`, 34 `expectation`, 190 `guidance`, 150 `lower_authority_signal`, 74 `contextual`.
- QC voegt `lower_authority_norm_signal` toe als reviewreden; dit verhoogt het aantal review-items bewust omdat lagere-autoriteitsnormen nu zichtbaar zijn in plaats van impliciet.
- D6-registerrijen zijn niet inhoudelijk gehard; Sprint 25.6 blijft geparkeerd tot stakeholdervalidatie beschikbaar is.

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
De beste eerstvolgende sprint is Sprint 27.2: Tijd.

Waarom:

- Sprint 24.1 heeft de taxonomie en checklist opgeleverd;
- Sprint 24.2 heeft een interne auditbasis opgeleverd;
- Sprint 24.3 heeft een lokaal intern review-dashboard opgeleverd;
- Sprint 25.1 heeft de werkagenda-operatielaag opgeleverd;
- Sprint 25.2 heeft de publieke lokale bronbasis versterkt;
- Sprint 25.3 heeft de publieke nulmeting en capaciteitsvelden per werkagenda-target gevuld;
- Sprint 25.4 en 25.5 hebben D6-verantwoordelijkheden en validatiehandoff voorbereid;
- Sprint 25.6 is terecht geparkeerd tot beleidsvalidatie beschikbaar is;
- Sprint 26.1 heeft de rough-claim audit herijkt, waardoor de resterende ruwe claims beter als echte extractie-/tekstproblemen kunnen worden aangepakt;
- Sprint 26.2 heeft deterministische tekstfilters toegevoegd en de eerste ruwe categorieen weggewerkt zonder D6-inhoud te overclaimen;
- Sprint 26.3 heeft sentence-boundary en dedup-logica toegevoegd en de claim-id verwijzingen downstream verifieerbaar gemaakt;
- Sprint 27.1 heeft normclaims gesplitst naar bindend, afspraak, verwachting, toelichting, lagere-autoriteitssignaal en context.

De concrete deliverables zijn:

- deadlines, verwachte publicatiemomenten, reviewmomenten en begrotingsmomenten apart modelleren;
- tijdlijnitems chronologisch en per momenttype controleerbaar maken;
- verwachte momenten zichtbaar anders labelen dan formele deadlines;
- geen D6-registerrijen inhoudelijk harden zolang stakeholdervalidatie voor Sprint 25.6 ontbreekt.
