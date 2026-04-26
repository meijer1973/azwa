# Sprint 25.4 - D6 Almere responsibility pack

## Summary
Status: open.

Sprint 25.4 is heropend na inhoudelijke review. De eerste D6-governance-laag is bruikbaar als publieke prefill, maar nog niet genoeg voor een uitvoeringsklare Almere-werkagenda. De heropende sprint richt zich daarom op een D6 Almere responsibility pack: publieke lokale en regionale bronnen versterken, D6-componenten aan actoren/schaal/financiering/besluitstatus koppelen, en expliciet markeren wat feit, interpretatie, voorstel, lokale validatie of later besluit is.

## Sprint Ledger

| Onderdeel | Status | Output |
| --- | --- | --- |
| 25.4a D6 publieke governance-prefill | completed | `data/extracted/d6_governance_collaboration.json`, `docs/completed-plans/phase25-sprint25.4-d6-governance-samenwerking.md` |
| 25.4b D6 Almere responsibility pack | open | Dit plan; eerste registerlaag `data/extracted/municipal/almere_d6_responsibility_register.json` |

## Kernbesluit
D6 wordt in deze sprint behandeld als basisinfrastructuur onder D5: herkenbare toegang en inloop, wijkteams/stevige lokale teams, sociale basis, GGD/JGZ, school- en mentale-gezondheidspreventie, monitoring/data/leren, regionale en lokale uitvoeringsgovernance, en financieringsafbakening.

De sprint mag geen definitieve lokale verantwoordelijkheid invullen zonder bron of lokale validatie. Als publieke bronnen geen eigenaar, uitvoerder, mandaat, budget of besluitstatus geven, wordt dat een review- of besluitveld.

## Te versterken bronbasis

Gebruik de bestaande D5/D6-bronnen eerst als backbone:

- AZWA definitief en CW 3.1 D5/D6-kader.
- VWS/VNG-financieringsmateriaal en werkagenda-opdracht, format en proces/financieringstoelichting.
- SPUK/DUS-I/wetten-bronnen.
- IZA, GALA, Regioplan IZA Flevoland, PGA-transformatieplan en PGA/SEO-businesscase.
- `docs/regional-roles-and-splits-almere-flevoland.md` en `data/curated/regional_roles_and_splits_almere_flevoland.json`.

Verifieer en intake daarna deze kandidaatbronnen als publieke D6-uitvoeringsbronnen:

| Prioriteit | Kandidaatbron | Doel in deze sprint | Eerste repository-actie |
| ---: | --- | --- | --- |
| 1 | Raad van Almere - Stevige Lokale Teams en inzet Investeringsfonds Jeugd en Gezin | Lokale besluitinformatie over wijkgerichte teams, mandaat, regie, startgebieden en verbinding met JGZ/wijkteams | Verifieer raadspagina en onderliggende Documentwijzer-stukken; converteer zo nodig naar page-markdown |
| 2 | Wijkteams Almere | Bestaande lokale toegang en sociale infrastructuur | Voeg toe als lokale implementatiebron |
| 3 | VNG Richtinggevend Kader toegang, lokale teams en integrale dienstverlening | Landelijk beoordelingskader voor toegang/lokale teams | Voeg toe als normerend of toetsend kader, niet als Almere-besluit |
| 4 | Toezicht Sociaal Domein - Basisfuncties lokale teams | Kwaliteits- en beoordelingskader voor lokale teams | Voeg toe als assessmentkader |
| 5 | GGD Flevoland Begroting/Ontwerpbegroting 2026 | GGD-governance, JGZ Almere, Kennis & Advies, dashboards, preventie en GGD-regioschaal | Voeg toe aan raw manifest en koppel aan D6 GGD/JGZ/monitoring |
| 6 | GGD Flevoland Kennis en Advies | Monitoring, epidemiologie, dashboards, data-analyse en advies | Voeg toe als monitoring/kennisbron |
| 7 | GGD Flevoland/JGZ Almere profiel | Jeugdgezondheid, school/familieverbinding en lokale teamrelatie | Voeg toe als D6/JGZ-uitvoeringsbron |
| 8 | Samen Sterker in de Wijk en Almere samenwerkingsprojecten | Mentale-gezondheidssamenwerking, wijkinfrastructuur, steunkring en leerbijeenkomsten | Voeg toe als lokale/regionale uitvoeringsbron |
| 9 | Actuele Positief Gezond Almere-samenwerking | Huidige lokale coalitie en praktische zorg/welzijnssamenwerking | Actualiseer of voeg toe als PGA-uitvoeringscontext |
| 10 | GGZ Centraal Flevoland en partnerpagina's | Psychiatrische wijkteams en relatie met wijkteams/huisartsen | Selectief toevoegen als ondersteunende bron |

## Responsibility register

Maak een register met minimaal deze velden:

- `component_id`
- `component_label`
- `existing_almere_provision`
- `required_upgrade`
- `owner`
- `executors`
- `cooperation_partners`
- `scale`
- `funding_sources`
- `decision_status`: `settled`, `source_backed_prefill`, `inferred`, `proposed`, `review_needed`, `decision_needed`
- `evidence_sources`
- `confidence`
- `open_issue`
- `human_review_needed`
- `fact_interpretation_proposal_status`

Eerste generator: `src/build_almere_d6_responsibility_register.py`.

Start met deze D6-componenten:

1. Inloopvoorzieningen sociaal en gezond.
2. Wijkteams Almere.
3. Stevige Lokale Teams.
4. JGZ Almere.
5. GGD Flevoland-coordinatie.
6. Gezonde School / mentale gezonde school.
7. Kennis & Advies / monitoring / dashboards.
8. Samen Sterker in de Wijk / mentale-gezondheidswijkinfrastructuur.
9. Positief Gezond Almere / Zorgzaam Flevoland-interface.
10. Digitale en operationele infrastructuur: RTP Almere, RSO, Monitoring@home, gedeeld informatiebeeld.
11. Burgerinitiatieven en informele steun.
12. Financiering en budgetafbakening.

## Werkwijze

1. Controleer welke kandidaatbronnen al in `data/raw/manifest.json` of `sources/manifest.json` zitten.
2. Verifieer publieke URLs en onderliggende documenten voordat ze als bron worden opgenomen.
3. Voeg alleen openbare, herleidbare bronnen toe aan de raw manifest.
4. Converteer PDF's of Documentwijzer-bijlagen eerst naar page-markdown wanneer dat nodig is voor traceerbare extractie.
5. Draai de volledige relevante pijplijn: inventory, structural extraction, document extraction, claims, current interpretation, D5/D6 views, QC, site-viewmodels en intern dashboard.
6. Bouw of actualiseer het D6 responsibility register vanuit publieke bronnen en bestaande guardrails.
7. Registreer ontbrekende lokale kennis als lokale validatie of later besluit, niet als blocker.
8. Maak pas daarna bestuurlijke tekst of een D6-onepager, en alleen met bronstatus per claim.

## Acceptatiecriteria

- Sprint 25.4 staat weer `open` in de roadmap zolang het D6 Almere responsibility pack nog niet is opgeleverd.
- De kandidaatbronnen zijn beoordeeld op publieke beschikbaarheid en intakebaarheid.
- Nieuwe bronnen zijn opgenomen of expliciet afgewezen met reden.
- Het responsibility register bestaat en bevat de twaalf startcomponenten.
- Elke registerrij heeft schaal, actorvelden, financieringsstatus, besluitstatus, bronstatus en open issue.
- De regionale schaalguardrail blijft zichtbaar: Almere-local, IZA/AZWA-regio Flevoland, GGD-regio Flevoland, zorgkantoorregio en project-/programmaschaal worden niet samengevoegd.
- Dashboard en research-agent map verwijzen naar de actuele sprintstand.

## Niet doen in deze sprint

- Geen definitieve eigenaar, uitvoerder of budgetclaim invullen zonder bron of lokale validatie.
- Geen site- of bestuurlijke tekst baseren op interne JSON als publieke bron.
- Geen D6, D5, GALA/SPUK, PGA en reguliere gemeentelijke middelen samenvoegen zonder financieringsbron.
- Geen privacygevoelige contactgegevens of persoonsdetails uit publieke pagina's promoveren naar claims.

## Open reviewpunten

- Bevestigen of Stevige Lokale Teams, Wijkteams Almere, JGZ Almere, GGD Flevoland, PGA en Samen Sterker in de Wijk formele D6-infrastructuur, ondersteunende infrastructuur, kandidaat-infrastructuur of buiten-D6 maar implementatierelevant zijn.
- Vaststellen welke lokale besluitdocumenten een `settled` status mogen dragen.
- Bepalen welke onderdelen na publieke bronuitputting naar lokale medewerkers gaan en welke naar bestuurlijke besluitvorming.
