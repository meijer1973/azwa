# AZWA Canonical Roadmap

## Summary
Current sprint: Sprint 33.P7 - Pre-contact send-readiness gate (blocked).

Roadmap version: `v2026.05.09-9`.

This is the single active roadmap for the repository. It combines the older data-quality roadmap and the workagenda-delivery roadmap into one canonical planning surface. Historical snapshots and retired roadmap files live under `docs/roadmap/archive/`; version changes are recorded in `docs/roadmap/roadmap-version-log.md`.

## Roadmap Versioning

Use this versioning rule for roadmap changes:

- The active roadmap is always `docs/data-quality-roadmap.md`.
- Increment the roadmap version when sprint status, phase scope, gate rules, canonical file routing, or delivery sequence changes.
- Record every roadmap version in `docs/roadmap/roadmap-version-log.md`.
- Archive replaced standalone roadmap files or major prior snapshots under `docs/roadmap/archive/`.
- Keep `docs/workagenda-delivery-roadmap.md` as a redirect only; do not maintain it as a second active roadmap.
- After roadmap changes, regenerate `docs/internal/review-dashboard.html`, run tests, commit and push before reporting back.

## Active Task Ledger
Gebruik deze roadmap als levend werkdocument voor wat nu nog gedaan moet worden. Voltooide sprints staan niet meer bovenaan; ze zijn verplaatst naar `docs/roadmap/completed-sprint-ledger.md`.

Statusbetekenis:

- `open`: repository-side werk kan nu worden uitgevoerd.
- `blocked`: wacht op externe validatie, besluitvorming, documenten of eerdere deliverylagen.
- `parked`: bewust geparkeerd en geen blocker voor de huidige route.
- `planned`: nog niet gestart; volgorde afhankelijk van de open/blocked taken erboven.

| Task | Status | What needs to be done | Next artifact / output | Blocker or dependency |
| --- | --- | --- | --- | --- |
| 33.P5 Internal dry run | blocked | Laat 2-4 interne reviewers de voorbereide P5-cases testen: D5-tab, D6-tab, finance-row, evidence-field en `niet mijn domein` case. | Completed dry-run response record and packet fixes. | Repository dry-run pack exists; human reviewers still needed before P7. |
| 33.P7 Send-readiness gate | blocked | Go/no-go voor contact: IDs, routing, evidence gates, current working views, dropdowns, dry run and source watchlist must be complete. | Send-readiness gate note. | Blocked until P5 human dry run is completed and packet fixes are processed. |
| V1 Controlled outbound | blocked | Verstuur beperkte stakeholderpakketten pas na P7. | Sent-packet log. | Blocked until send-readiness gate passes. |
| V2 Response triage | blocked | Verwerk antwoorden naar statuswijzigingen, weak confirmations, conflicts, decision tickets, finance tickets or rerouting. | Validation log and ticket updates. | Blocked until responses return. |
| V3 Decision and finance compression | blocked | Zet resterende onzekerheid om naar compacte besluit-, finance-, governance-, ICT/privacy- en D6-risk lijsten. | Decision/finance compression outputs. | Blocked until response triage. |
| V4 Work-agenda readiness dashboard | blocked | Toon per D5 item of het klaar is voor werkagenda-draft, met risico en volgende actie. | `data/workagenda/d5_dashboard_view.json`. | Blocked until validation/finance/dependency layers mature. |
| 25.6 D6 post-validation register hardening | parked | Hard register rows only after D6 validation evidence exists. | Updated D6 responsibility register and QC. | Wacht op stakeholdervalidatie, lokale/interne documenten, finance/controller bevestiging of beleidsbesluit. |

Completed sprint history: `docs/roadmap/completed-sprint-ledger.md`.

## Huidige sprintplan
Sprint 33.P7 is geblokkeerd. Sprint 33.P6 heeft de response workflow vastgelegd via `data/workagenda/precontact_response_workflow.json` en `docs/review/precontact-response-workflow.md`: teruggestuurde antwoorden worden gerouteerd naar validation logs, finance matrices, decision registers, de D5-D6 dependency map, source-update log, statusmatrix of D6 responsibility register op basis van `repo_update_effect`, antwoorduitkomst en bewijsstatus. Er zijn nog geen stakeholderantwoorden geimporteerd. De eerstvolgende echte stap is de P5 human dry run laten uitvoeren door 2-4 interne reviewers en eventuele packet fixes verwerken; pas daarna kan P7 send-readiness inhoudelijk worden beoordeeld. Sprint 32.3 blijft geblokkeerd tot echte stakeholderantwoorden bestaan. Sprint 25.6 blijft geparkeerd omdat post-validatie hardening pas verantwoord is na stakeholdervalidatierecords, lokale/interne documenten, finance/controller bevestiging of een expliciet beleidsbesluit.

## Current Context Check - 2026-05-09

The reviewed recommendation is directionally correct but partly stale against the current repository:

- D5 statusmatrix, validation tickets and CSV stakeholder packets already exist in `data/workagenda/` from Sprints 32.1-32.2.
- The two Excel files now present in `docs/review/` are the practical pre-contact instruments, but they were not yet controlled as tracked baseline assets.
- D6 markdown validation material already exists in `docs/review/almere_d6_validation_ticket_matrix.md`, but the D6 Excel still needs the same traceability/import discipline as D5.
- No stakeholder validation has happened yet. The next phase is therefore not V1 outbound, but pre-contact QA.
- Sprint 32.4 source-watch work remains relevant, but it is now folded into 33.P3/P6 as a targeted D5 source-update watchlist rather than a standalone broad research step.

## Phase 33 - Pre-contact Validation-readiness

Goal: reduce human workload before validation starts. Policymakers should receive short validation packets where they can confirm or correct the current working view, choose from dropdown options, identify responsible parties, add or name evidence, mark whether another party must confirm, and flag decision, finance or ICT/privacy issues.

### Phase 33 Assets

| Asset | Current repository status | Use |
| --- | --- | --- |
| `docs/review/D5_validatieformat_werkagenda_Almere_v0.9.xlsx` | Current Excel workbook, 18 sheets; 11 visible input/instruction sheets and 7 hidden navigation/control/workflow sheets. Prior versions preserved. | D5 pre-contact validation instrument for P5 dry run; keeps navigation and control tabs out of the human-facing tab bar while preserving them for repository processing. |
| `docs/review/Almere_D6_validatieformats.xlsx` | Baseline Excel workbook, 15 sheets. | D6 pre-contact validation instrument. |
| `docs/review/validation-instrument-register.md` | Created in 33.P0. | Version, purpose, sheet inventory, shared vocabulary and import rules. |
| `data/workagenda/validation_workbook_traceability_map.json` | Created in 33.P1. | Stable generated IDs, routing and processing metadata for 189 D5/D6 workbook validation rows. |
| `docs/review/validation-workbook-traceability-audit.md` | Created in 33.P1. | Human-readable audit of workbook traceability and remaining send-readiness limits. |
| `data/workagenda/validation_workbook_prefill_audit.json` | Created in 33.P2. | Machine-readable audit of current working views, answer/correction fields, evidence fields, broad questions and language flags. |
| `docs/review/validation-workbook-prefill-audit.md` | Created in 33.P2. | Human-readable workbook prefill audit and cleanup list. |
| `data/workagenda/precontact_agent_plan.json` | Created in 33.P3. | Prepared targeted agent plan; prompts are not sent. |
| `docs/review/precontact-agent-prompts.md` | Created in 33.P3. | Copy-ready prompts for five narrow pre-contact agents. |
| `data/workagenda/precontact_stakeholder_packets.json` | Created in 33.P4. | Prepared D5/D6 packet index; packets are not sent. |
| `docs/review/precontact-stakeholder-packets.md` | Created in 33.P4. | Human-readable packet overview, instructions and cleanup-before-send notes. |
| `data/workagenda/precontact_packets/*.csv` | Created in 33.P4. | Draft CSV packet send set with `vraag_id`, evidence fields and reroute columns. |
| `data/workagenda/precontact_internal_dry_run.json` | Created in 33.P5. | Repository-side dry-run cases; human reviewers still pending. |
| `docs/review/precontact-internal-dry-run.md` | Created in 33.P5. | Human-readable dry-run protocol and pass/fail criteria. |
| `data/workagenda/precontact_response_workflow.json` | Created in 33.P6. | Machine-readable answer-processing workflow; no answers imported. |
| `docs/review/precontact-response-workflow.md` | Created in 33.P6. | Human-readable workflow for routing returned answers without overclaiming. |
| `data/workagenda/d5_validation_tickets.json` | Created in 32.2. | D5 machine-readable validation ticket basis. |
| `data/workagenda/d5_validation_packets.json` and `data/workagenda/validation_packets/*.csv` | Created in 32.2. | D5 repository-generated packet basis, to be reconciled with Excel. |
| `docs/review/almere_d6_validation_ticket_matrix.md` | Existing D6 plain-language matrix. | D6 question design and stakeholder language basis. |

### Phase 33 Sprint Sequence

| Sprint | Name | Main output | Contact policymakers yet? |
| --- | --- | --- | --- |
| 33.P0 | Freeze instruments | D5/D6 Excel baselines and validation instrument register. Completed. | No |
| 33.P1 | Add IDs and routing | Stable IDs, stakeholder packages and repo-update effects per validation row. Completed. | No |
| 33.P2 | Prefill audit | Current working view per human-facing tab; no blank broad questions. Completed. | No |
| 33.P3 | Targeted agents | Evidence, readability, dependency, source-watch and finance-risk prechecks only. Completed; prompts prepared, not sent. | No |
| 33.P4 | Stakeholder packets | Filtered packets per group, with instructions and escalation route. Completed; packet drafts prepared, not sent. | No |
| 33.P5 | Internal dry run | Repository-side case pack prepared; human reviewer execution pending and blocks P7. | No |
| 33.P6 | Repository/workflow integration | Completed; answer-processing workflow defined, no answers imported. | No |
| 33.P7 | Send-readiness gate | Blocked until P5 human dry run is completed and fixes are processed. | No |
| V1 | Controlled outbound | Packets sent and logged. | Yes |
| V2 | Response triage | Processed validation answers. | Yes |
| V3 | Decision and finance compression | Decision, finance, governance and ICT/privacy tickets. | Yes |
| V4 | Work-agenda readiness dashboard | Green/yellow/red workagenda delivery view. | Yes |

### Targeted Deep Research Policy

Use targeted agents only. Do not run another broad D5 or D6 research wave.

| Agent type | Worth doing now? | Reason |
| --- | ---: | --- |
| Evidence-prefill audit | Yes | Reduces weak or unsupported working views before humans see them. |
| Policymaker readability audit | Yes | Prevents overloaded forms. |
| D5-D6 dependency mapping | Yes | Essential for credible workagenda execution. |
| Finance-risk precheck | Yes | Finance is on the critical path. |
| End-May handreiking watchlist | Yes, scheduled | The D5 assignment expects handreikingen around the end of May. |
| Broad D5 public search | No | D5 structure is already sufficiently known for pre-contact QA. |
| Broad D6 public search | No | D6 mostly requires validation, not more public search. |
| Local ownership/funding research by agent | No | Requires human validation or decision. |

## Phase 32 - Werkagenda-delivery System

Phase 32 turns the repository from a research and review tool into a D5 workagenda-delivery control system. The goal is not final drafting yet. The goal is to show, per D5 component and workagenda field, whether the answer is source-backed, needs local validation, needs finance/controller or Zvw confirmation, needs a decision, depends on D6, waits for national guidance, or is ready for drafting.

### Phase 32 Status

| Sprint | Status | Output |
| --- | --- | --- |
| 32.0 Scope en stuurmodel vastzetten | completed | `docs/workagenda-d5-stuurmodel.md`; `data/workagenda/d5_stuurmodel.json`; `docs/completed-plans/phase32-sprint32.0-workagenda-stuurmodel.md` |
| 32.1 D5-statusmatrix bouwen | completed | `docs/workagenda-d5-statusmatrix.md`; `data/workagenda/d5_status_matrix.json`; `docs/completed-plans/phase32-sprint32.1-d5-statusmatrix.md` |
| 32.2 D5-validatie voorbereiden | completed | `docs/workagenda-d5-validation-tickets.md`; `data/workagenda/d5_validation_tickets.json`; `docs/workagenda-d5-validation-format.md`; `data/workagenda/d5_validation_packets.json`; `data/workagenda/validation_packets/*.csv`; `docs/completed-plans/phase32-sprint32.2-d5-validatieformats.md` |
| 32.3 Eerste menselijke validatieronde | blocked | Blocked until completed stakeholder answers, validation records, explicit policy decisions or relevant evidence documents exist. |
| 32.4 Handreikingen en tijdsafhankelijke bronnen verwerken | folded into 33.P3/P6 | Source-watch work remains needed, but now runs as targeted pre-contact watchlist/workflow integration instead of a standalone current sprint. |
| 32.5 Gap compression en besluit-tickets | planned | Planned: `data/workagenda/d5_decision_register.json` and decision-ticket summary. |
| 32.6 Finance/controller en zorgverzekeraar integreren | planned | Planned: `data/workagenda/d5_finance_matrix.json`. |
| 32.7 D6-afhankelijkheden integreren | planned | Planned: `data/workagenda/d5_d6_dependency_map.json`. |
| 32.8 Prioritering, fasering en 2030-ingroeipad | planned | Planned: prioritisation and phasing view. |
| 32.9 Concept-werkagenda v0.8 | blocked | Blocked until statusmatrix, validation tickets, finance matrix, decision register and D5-D6 dependency map exist. |
| 32.10 Governance-ready versie | blocked | Blocked until concept is validated and finance/governance risks are explicit. |
| 32.11 Vaststelling en VWS-verzending | blocked | Blocked until governance route begins. |
| 32.12 Uitvoeringsstart 2027 en lerende cyclus | blocked | Blocked until adopted workagenda exists. |

### Phase 32 Delivery Status Model

Every D5 component and workagenda field uses one of these statuses:

| Code | Status | Meaning |
| --- | --- | --- |
| A | Beantwoord uit bron | Public/corpus source directly answers the field. |
| B | Bron suggereert antwoord, validatie nodig | Source-backed working view exists, but local validation is required. |
| C | Lokale validatie nodig | Local practice, owner, coverage, capacity or evidence must be confirmed. |
| D | Bestuurlijk besluit nodig | A decision is needed before the field can be used as workagenda position. |
| E | Finance/controller nodig | Funding, structural continuation or double-counting must be checked. |
| F | Zorgverzekeraar/Zvw-bevestiging nodig | Zvw-side purchase, contract or insurer role must be confirmed. |
| G | ICT/privacy/data-bevestiging nodig | Data, privacy, dashboard, reporting or operational accountability must be confirmed. |
| H | Wachten op landelijke handreiking | National guidance or template is still expected. |
| I | Optioneel / niet van toepassing | Item is optional, excluded or not applicable for the current scope. |
| J | Onbekend | Not enough information to classify yet. |

### Phase 32 Core Files

| File | Function | Status |
| --- | --- | --- |
| `data/workagenda/d5_stuurmodel.json` | Scope, status values, fields and milestones. | Created in 32.0. |
| `data/workagenda/d5_status_matrix.json` | Central status per D5 component and workagenda field. | Created in 32.1. |
| `data/workagenda/d5_validation_tickets.json` | Constrained validation questions. | Created in 32.2. |
| `data/workagenda/d5_validation_packets.json` | Stakeholder packet index. | Created in 32.2. |
| `data/workagenda/validation_packets/*.csv` | Blank validation forms per stakeholder packet. | Created in 32.2; not validation results. |
| `data/workagenda/d5_validation_log.json` | Who confirmed what, when, with what evidence. | Blocked until validation answers exist. |
| `data/workagenda/d5_source_update_log.json` | Handreikingen, regioscan, rode-dradenanalyse and time-sensitive source changes. | Planned inside 33.P3/P6. |
| `data/workagenda/d5_finance_matrix.json` | Funding, double-counting, structural/project status and controller status. | Planned. |
| `data/workagenda/d5_decision_register.json` | Governance and bestuurlijke decision tickets. | Planned. |
| `data/workagenda/d5_d6_dependency_map.json` | D6 preconditions per D5 component. | Planned. |
| `data/workagenda/d5_dashboard_view.json` | Red/yellow/green workagenda steering view. | Planned. |

### Phase 32 Gate Rules

- Do not start final D5 workagenda drafting from the roadmap, statusmatrix or validation packets alone.
- Do not mark a D5 field ready if it only has a source-backed working view and still needs local validation.
- Do not use finance wording as confirmed unless finance/controller or insurer evidence exists.
- Do not hide D6 prerequisites inside D5 programme text; record them as dependencies.
- Do not send broad research agents unless a named source, expected publication or explicit source gap exists.
- Do not process Sprint 32.3 until completed validation responses or explicit policy decisions exist.
- Do not move to Sprint 32.9 drafting until the statusmatrix, validation tickets, finance matrix, decision register and D5-D6 dependency map exist.

Status op 26 april 2026: Sprint 25.2 is afgerond als publieke bronversterkingssprint. `data/extracted/local_source_strengthening_almere.json` maakt zichtbaar welke lokale bronnen in de formele laag zitten, welke publieke bronnen als assessmentmateriaal zijn beoordeeld, en welke vragen naar later in de workflow gaan omdat de publieke bronbasis is uitgeput of omdat een geschoonde validatiestap nodig is. De geselecteerde Documentwijzer-bijlagen voor Visie Gezondheidsbeleid en Maatschappelijke Agenda zijn eerst naar page-markdown omgezet en daarna opgenomen in `data/raw/manifest.json`. Ook de GGD-tabellenboeken voor volwassenen en ouderen, de GGD-valpreventiepagina Almere en de ZonMw-bron zijn opgenomen in `data/raw/manifest.json`, door inventory/extractie/claims/site-viewmodels verwerkt en blijven reviewmateriaal voordat ze bestuurlijk of public-facing worden gebruikt. Niet-publieke informatie, ontbrekende lokale bevestiging en formele besluitvragen blokkeren deze fase niet; ze worden als gaten of carry-over taken zichtbaar gemaakt voor lokale medewerkers en latere besluitvorming.

Status op 26 april 2026: Sprint 25.4a is afgerond in `data/extracted/d6_governance_collaboration.json`. De laag gebruikt de publieke claims, de regionale rollen/splits-guardrail en de nulmeting uit Sprint 25.3 om per D6-dimensie de publieke brondekking, actorrollen, verantwoordelijkheidsprefill, lokale validatievelden en besluitvragen zichtbaar te maken. Niet-publieke rolverdeling, eigenaarschap, budget, monitoring en schaalkeuzes blijven invul- of besluitvragen.

Status op 26 april 2026: Sprint 25.4b is geopend in `docs/phase25-sprint25.4-d6-almere-responsibility-pack-plan.md`. De nieuwe focus is niet een algemene D6-samenvatting, maar een Almere responsibility pack rond lokale toegang, wijkteams, Stevige Lokale Teams, GGD/JGZ, mentale-gezondheidswijkinfrastructuur, monitoring/data, regionale/lokale uitvoering en financieringsafbakening.

Status op 27 april 2026: eerste 25.4b-bronintake uitgevoerd. Zeven publieke bronnen zijn toegevoegd aan `data/raw/manifest.json` en door inventory, structural extraction, document extraction, claims, current interpretation, D6-lagen, QC, site-viewmodels en intern dashboard verwerkt: Stevige Lokale Teams raadspagina, Wijkteams Almere, VNG Richtinggevend Kader, Toezicht Sociaal Domein Basisfuncties, GGD Flevoland Begroting 2026, GGD Flevoland Kennis en Advies, en GGD Flevoland/JGZ Almere profiel. Onderliggende Documentwijzer-stukken bij Stevige Lokale Teams en de Almere Samen Sterker/samenwerkingsprojectenpagina's blijven open intakewerk omdat ze gerichte selectie of hernieuwde publieke download/verificatie vragen.

Status op 27 april 2026: gate-remediation gestart. De sprint gaat niet door naar rapportproductie of bestuurlijke werkagenda-drafting; de toegestane vervolgstap is alleen D6 responsibility implementation/remediation. Zes extra bronnen zijn toegevoegd: vier Documentwijzer/Notubiz-stukken bij Stevige Lokale Teams, de Almere Samenwerkingsprojecten/Samen Sterker-bron en een actuele PGA-homepage. De lokale decision layer bevat nu een source-backed publieke raadbeslissing voor Stevige Lokale Teams, met D6-classificatie nog expliciet op `review_needed`.

Status op 28 april 2026: Sprint 25.6 is geparkeerd als policy-maker/stakeholder-afhankelijkheid en blokkeert repository-side datakwaliteitswerk niet. Fase 26 is gestart met rough-claim cleanup. Sprint 26.1 is afgerond als audit-hercalibratie: de lengte-only rough-code is vervangen door `unverified_extraction_length`, langere excerpts geven reviewers meer context, en regressietests bewaken dat lange maar goed gevormde claims niet alleen door lengte rough worden. Sprint 26.2 is afgerond als deterministische tekstfix: mojibake, letterhead, TOC-/Drupal-ruis en stemuitslagen worden uit claim-input gehouden; stemuitslagen blijven apart bewaard in `data/extracted/voting_records.json`. Sprint 26.3 is afgerond als sentence-boundary/dedup sprint: lowercase mid-zin-claims worden uit de masterlaag geweerd, duplicate openings binnen document/topic/subtopic worden geconsolideerd, en `src/verify_claim_id_references.py` controleert downstream claim-id verwijzingen.

Status op 29 april 2026: Sprint 27.1 is afgerond als norm-splitsing. Elke claim krijgt nu een `normative_status` met de waarden `binding`, `agreement`, `expectation`, `guidance`, `lower_authority_signal` of `contextual`. De audit bevat een `normative_status_audit`, de site-evidence draagt normstatus mee, en QC markeert lagere-autoriteitssignalen expliciet als reviewpunt zodat FAQ's, toelichtingen en regionale/lokale context niet als harde norm worden gelezen.

Status op 29 april 2026: Sprint 27.2 is afgerond als tijd-splitsing. Elke claim krijgt nu een `time_status` met onderscheid tussen formele deadlines, verwachte momenten, review-/actualisatiemomenten, budgetkalendermomenten, implementatiehorizons, lokale planningscontext, bronverankerde tijdmomenten, publicatie-/contextdata en ongedateerde context. De audit bevat een `time_status_audit`, site-evidence en tijdlijnitems dragen tijdstatus mee, en QC markeert verwachte momenten en lokale planningscontext als reviewpunt zodat indicatieve momenten en lokale raadsagenda's niet als harde D5/D6-deadlines worden gelezen.

Status op 29 april 2026: Sprint 27.3 is afgerond als geld-splitsing. Elke claim krijgt nu een `money_status` met onderscheid tussen financieringsroutes, aanvraagvoorwaarden, budgetvensters, verdeelmechanismen, bestedingsruimte, verantwoordingsregels, lokale financieringsgaten, dubbeltellingsrisico's, financiele context en niet-financiele inhoud. De audit bevat een `money_status_audit`, site-evidence draagt geldstatus mee, en QC markeert lokale financieringsgaten, dubbeltellingsrisico's en algemene financiele context als reviewpunt zodat lokale budgetkeuzes of middelenmixen niet uit publieke bronnen worden ingevuld.

Status op 29 april 2026: Sprint 27.4 is afgerond als governance-splitsing. Elke claim krijgt nu een `governance_status` met onderscheid tussen besluitvorming, coordinatie/regie, aanvraag/indiening, uitvoering, verantwoording/eigenaarschap, goedkeuring/vaststelling, review/monitoring, governancegaten, actorcontext en niet-governance. De audit bevat een `governance_status_audit`, site-evidence draagt governancestatus mee, en QC markeert governancegaten, actorcontext en vage `regio`-actoren als reviewpunt zodat `regio`, `mandaatgemeente`, gemeente, raad, college, zorgverzekeraar en uitvoeringspartners niet door elkaar worden gehaald.

Status op 29 april 2026: Sprint 27.5 is afgerond als locality-splitsing. Elke claim krijgt nu een `locality_status` met onderscheid tussen expliciet Almere, expliciet Flevoland, regionale split-context, algemeen landelijk, landelijk-met-lokale-relevantie, afgeleide lokale relevantie, lokale adoptie-/documentatiegaten, gemeentelijke context en geen locality-signaal. De audit bevat een `locality_status_audit`, site-evidence draagt localitystatus mee, en QC markeert nationale claims met lokale relevantie, afgeleide lokale relevantie, adoptiegaten en regionale split-context als reviewpunt zodat landelijke of regionale lijnen niet als Almeerse vaststelling worden gelezen.

Status op 29 april 2026: Sprint 27.6 is afgerond als execution-splitsing. Elke claim krijgt nu een `execution_status` met onderscheid tussen operationele vereisten, zichtbare uitvoeringsactiviteit, besluitvragen, afhankelijkheden, volgorde-/faseringsvragen, capaciteitsvragen, reviewtaken, uitvoeringscontext en niet-uitvoering. De audit bevat een `execution_status_audit`, site-evidence draagt executionstatus mee, en QC markeert besluitvragen, afhankelijkheden, capaciteit, sequencing, reviewtaken en algemene uitvoeringscontext als reviewpunt zodat mogelijke opvolgacties niet als besloten uitvoering worden gelezen.

Status op 29 april 2026: Sprint 27.7 is afgerond als stabilisatiesprint voordat Fase 28 sitetekst gaat gebruiken. De termlijsten zijn opgeschoond zodat pipeline-metawoorden niet langer als bronsignaal tellen, execution-detectie gebruikt geen subjectnouns meer als operationele vereiste, actorherkenning gebruikt woordgrenzen zodat `gemeente` niet uit `gemeenteraad` wordt afgeleid, wetten.nl actiechrome wordt uit raw-html-blokken gefilterd, en de audit toont nul-tellingen voor statuswaarden en actor-signalen die in de huidige corpusrun niet voorkomen.

Status op 29 april 2026: Sprint 28.1 is afgerond als menselijke update-samenvatting. De updatepagina gebruikt nu gewone bron- en controlewoorden in plaats van pipeline- of datalaagtaal. De drie bestaande updates hebben volledige `human_summary`-velden voor aanleiding, wat er gebeurde, wat inhoudelijk veranderde en waarom dit voor Almere of de werkagenda relevant is. De detailpagina voor betrokken claims is hernoemd naar controlelijst met bronfragmenten, zodat de updatepagina zelf de leesbare duiding blijft en de detailpagina vooral controle en herleidbaarheid biedt.

Status op 29 april 2026: Sprint 28.2 is afgerond als bronverwijzings- en autoriteitstaalsprint. Publieke bronlijsten en controlelijsten tonen nu explicieter de bronhouder, bronstatus, soort bron en veilige formulering. Lagere-autoriteitsfragmenten worden in controlelijsten toegeschreven met formuleringen als `Volgens Raad van Almere:`, zodat de site minder snel contextuele of lokale bronnen als harde norm laat klinken.

Status op 29 april 2026: Sprint 28.3 is afgerond als drill-down sprint. Besluitvraag- en opvolgactiepagina's houden de hoofdtekst korter en verwijzen voor bronbasis, beleidsbasis en reviewdetails naar aparte `onderbouwing`-pagina's. Reviewtags op kaarten linken nu direct naar de menselijke-duidingsectie op die onderbouwingspagina's, en de zoekindex en sitemap kennen deze pagina's als aparte onderbouwingslaag.

Status op 29 april 2026: Sprint 28.4 is afgerond als pre-29 follow-up cleanup. De research-agent map verwijst niet meer naar de vervallen D6-actieview, `src/render_site.py` ruimt `dist/` op voordat pagina's opnieuw worden geschreven zodat lokale builds geen orphan HTML-pagina's houden, de menselijke-update-test combineert een bredere jargoncheck met positieve vormcriteria, en `zero_count_statuses` is expliciet als tijdelijke cleanup-opgave ingepland in Sprint 29.0.

Status op 29 april 2026: Sprint 29.0 is afgerond. De dode waarden `spending_scope`, `double_counting_risk`, `inferred_local_relevance`, `municipal_context`, `no_locality_signal` en het governance-actorsignaal `fondsbeheerder` zijn uit het actieve perspectiefcontract gehaald. Algemene bestedings- of dubbelingswaarschuwingen vallen nu terug op `finance_context` of op bestaande reviewdocumenten totdat de claimlaag daarvoor een bronverankerde status nodig heeft. De audit rapporteert geen zero-count status- of actorsignaalwaarden meer.

Status op 29 april 2026: Sprint 29.1 is afgerond. Het tijdlijnregister is verdiept met `moment_type`, `source_status`, `authority`, `actor_summary`, `primary_perspective` en `timeline_policy_note` per item. De tijdlijnpagina toont deze velden in een compacte leeslaag, zodat formele deadlines, lokale bestuurlijke context, financieringsmomenten en uitvoeringshorizons minder snel door elkaar worden gelezen. De curatie verwijst bovendien weer alleen naar bestaande claim-id's.

Status op 29 april 2026: Sprint 29.2 is afgerond. De bestaande gemeentefondsbron draagt nu drie verwachte circulairemomenten voor 2026: mei, september en december. De tijdlijnview maakt daarnaast een `budget_cycle`-doorsnede met lokale begroting, gemeentefonds, SPUK/subsidie, verantwoording, werkagenda/middelen en overige financiele context. Deze doorsnede staat onder de chronologische tijdlijn zodat datumvolgorde in de hoofdsectie intact blijft.

Status op 29 april 2026: Sprint 29.3 is afgerond. Het format voor de D5-werkagenda is toegevoegd als eigen tijdlijnmoment en de tijdlijnview bevat nu een `execution_support`-doorsnede voor formatdocumenten, proces-/toelichtingsdocumenten, werkagenda-proces, webinars, handreiking/thematafel en ondersteuningspagina's. De publieke tijdlijn toont deze doorsnede apart zodat handreikingen en uitvoeringsduiding niet als formele besluiten of harde normen worden gelezen.

Status op 29 april 2026: Sprint 30.1 is afgerond. De Almerepagina maakt lokale lacunes per thema zichtbaar zonder oordeelstaal: D5-werkagenda, financiering, monitoring en de D6-validatiegrens tonen nu wat de openbare bronbasis ondersteunt, wat zij niet bewijst, welke vervolgvraag resteert en welke formulering veilig is zolang lokale validatie ontbreekt. De D6-lacune gebruikt het D6 responsibility register als validatiegrens en blijft expliciet op nul `settled` rijen.

Status op 29 april 2026: Sprint 30.2 is afgerond. Besluitvraag- en opvolgactiepagina's hebben nu een vaste sectie `Bronbasis en lokale keuze`. Kaarten en detailpagina's scheiden de bronaanleiding van de Almeerse invulruimte, tonen de relevante perspectieven en waarschuwen dat de pagina geen vastgesteld besluit, opdracht of planning is. Opvolgacties gebruiken verkenningstaal in plaats van opdracht- of adviesformuleringen.

Status op 29 april 2026: Sprint 30.3 is afgerond. `docs/rapporten/report-status.json` onderscheidt actuele public-review kandidaten van vervallen concepten. `plan-van-aanpak-v2.md` is expliciet gemarkeerd als vervallen concept dat niet public-facing gebruikt moet worden. `src/audit_report_grounding.py` en `tests/test_report_grounding.py` bewaken dat actuele rapportkandidaten geen interne datalaagtaal, exacte fte-claims, niet-bestaande bijlagen of te definitieve interne planning bevatten. De interne controle-uitkomst staat in `docs/internal/report-grounding-audit-2026-04-29.md`.

Status op 29 april 2026: Sprint 31.1 is afgerond. `docs/updateprotocol.md` legt vast wanneer een bron- of datawijziging een publieke update nodig heeft, welke velden `config/site_updates.json` moet bevatten, hoe oude claims behouden blijven en welke verificatie hoort bij bronintake. `src/validate_update_protocol.py` controleert de bestaande updates op verplichte velden, menselijke samenvatting, metrics, betrokken pagina's en bestaande document-id's. De interne controle staat in `docs/internal/update-protocol-check-2026-04-29.md`.

Status op 30 april 2026: Sprint 31.2 is afgerond. `config/monthly_source_audit.json` legt de maandelijkse watchlist vast voor verwachte circulaires, AZWA-handreikingen, nieuwe SPUK-/monitorbronnen en open intakekandidaten. `src/build_monthly_source_audit.py` schrijft `data/extracted/monthly_source_audit.json` en `docs/internal/monthly-source-audit-2026-04-30.md`. De audit houdt zes watchlistitems op `not_due_yet`, signaleert een VNG-vervangingsbron als pending replacement, bewaart drie verwachte tijdlijnmomenten als pending source ingestion en behandelt redirectgedrag als link-review in plaats van direct als bronfeit. Watchlist- en pending-items blijven geen publieke evidence totdat ze formeel zijn opgeslagen, aan de raw manifestlaag zijn toegevoegd en door de pipeline zijn verwerkt.

Status op 30 april 2026: Sprint 31.3 is afgerond. `src/build_human_review_round.py` bundelt de review queue, perspectiefconfiguratie en maandelijkse bronaudit tot `data/extracted/human_review_round.json` en `docs/review/archive/phase31/phase31.3-human-review-round.md`. Het reviewpack geeft per perspectief de hoofdvragen, topreden-codes en voorbeelditems, en herhaalt dat reviewerbesluiten apart moeten worden vastgelegd en niet automatisch bronclaims worden. De D6-guardrail blijft staan: geen D6-registerrij wordt `settled` zolang Sprint 25.6 geparkeerd is.

Status op 30 april 2026: Sprint 31.4 is afgerond. `src/build_review_triage.py` routeerde de toenmalige reviewitems naar vier buckets: deep-research kandidaten, gemengde public-search-then-human items, human-only items en pipeline/extractie-cleanup items. `docs/review/archive/phase31/phase31.4-deep-research-agent-prompts.md` bevat zes kant-en-klare opdrachten voor deep research agents rond Gezonde School, digitale/operationele infrastructuur, burgerinitiatieven/informele steun, PGA/Zorgzaam/Flever, Samen Sterker in de Wijk en sterkere autoriteits-/adoptiebronnen. Deep research mag publieke bronnen en source gaps verminderen, maar geen D6-classificatie, eigenaarschap, mandaat, financiering of `settled` status vaststellen.

Status op 1 mei 2026: Sprint 31.5 heeft vijf deep-research rapporten als bronsignaal verwerkt, niet als bewijsbron: `docs/dr/Healthy school.md`, `docs/dr/Digital and operational infrastructure.md`, `docs/dr/Informal support.md`, `docs/dr/Zorgzaam Flevoland, and Flever interface.md` en `docs/dr/Samen Sterker in de Wijk in Almere.md`. De geselecteerde publieke bronnen zijn opgeslagen, toegevoegd aan de manifestlaag, door de pipeline gehaald en daarna getoetst in het D6-register en reviewmateriaal. Gezonde School, digitale/operationele infrastructuur, inloopvoorzieningen, burgerinitiatieven/informele steun, de PGA/Zorgzaam/Flever-interface en Samen Sterker in de Wijk hebben nu sterkere publieke prefill, maar blijven `inferred` en `needs_human_review`; formele D6-classificatie, eigenaarschap, mandaat, SLT-relatie en financiering blijven stakeholder- of beleidsvalidatie.

Status op 1 mei 2026: het settlement-auditrapport `docs/dr/Almere D6 Settlement Evidence Audit.md` is verwerkt als bronhiaten- en grenssignaal. Vijf sterkere publieke bronnen zijn geselecteerd en toegevoegd: subsidieregisters 2024/2025, Almere Mentale gezondheid, GGD Flevoland Voortgang GALA in de regio en Zorgakkoorden handvatten regionale werkagenda. De top-layer check blijft conservatief: geen D6-rij is `settled`, alle twaalf D6-rijen blijven menselijke validatie vragen en de triagelaag houdt `d6_rows_with_named_public_search_gap` op `0`. Brede publieke D6-zoekacties zijn daarmee geparkeerd; overblijvende vragen zijn governance-, finance/controller-, mandaat-, ICT/privacy- of stakeholdervalidatie.

Status op 1 mei 2026: het follow-uprapport `docs/dr/Stable public source check for â€œStand van zaken Gezondheidsbeleid (IZA en GALA)â€.md` is verwerkt als bronintake-signaal. De stabiele Documentwijzer-landingspagina is gevonden en vastgelegd als `mun_almere_stand_van_zaken_gezondheidsbeleid_iza_gala_2025` in `data/raw/source_intake_candidates.json` met status `pending_full_text`. De lokale download leverde alleen de Raadzaam-appshell op, dus deze bron is nog niet toegevoegd aan `data/raw/manifest.json` en levert nog geen claim- of D6-registerbewijs op. De resterende publieke taak is gericht: haal de onderliggende raadsbrieftekst/PDF op, of laat de kandidaat staan.

Status op 1 mei 2026: de D6-open-vragen zijn aangescherpt naar validatievragen in `docs/review/almere_d6_validation_ticket_matrix.md`. De repository geeft daarmee geen brede onderzoeksvragen meer mee, maar plain-language keuzevelden, stakeholderpakketten, eenvoudige beslisregels en escalatietriggers per D6-component. De brede rijen digitale/operationele infrastructuur en financiering worden in de matrix respectievelijk als subcomponenten en master funding matrix behandeld, zonder het D6-register inhoudelijk te harden.

Status op 1 mei 2026: het rapport `docs/dr/Constrained answer design for the Almere D6 open-question set.md` is verwerkt als ontwerpinput, niet als bronbewijs. Er zijn geen nieuwe manifestbronnen geselecteerd. De managementopmerking is verwerkt door de actieve validatiematrix om te schrijven naar stakeholdertaal en interne termen zoals repository/register/prefill/top-layer buiten de handoffvragen te houden.

Status op 2 mei 2026: de voorgestelde roadmap om de repository om te bouwen naar een werkagenda-delivery system is getoetst aan de huidige staat. De richting klopt: D5-vereisten, nulmeting/capaciteit, D6-validatie, tijdlijn/watchlist en reviewguardrails bestaan al. De ontbrekende laag is een delivery-control laag met D5-statusmatrix, D5-validatietickets, validatielog, finance/controller matrix, besluitregister, D5-D6-afhankelijkhedenkaart, bronupdate-log en dashboardview. De eerst losse workagenda-roadmap is op 3 mei 2026 samengevoegd in deze canonieke roadmap.

Status op 2 mei 2026: Sprint 32.0 is gestart. Het eerste stuurmodel staat in `docs/workagenda-d5-stuurmodel.md` en de machineleesbare contractlaag in `data/workagenda/d5_stuurmodel.json`. Deze laag legt de D5-scope, statuscodes A-J, werkagendavelden, mijlpalen en geplande kernbestanden vast. Het is nog geen D5-statusmatrix en nog geen validatie-Excel; die volgen pas na dit contract.

Status op 2 mei 2026: Sprint 32.0 is afgerond en Sprint 32.1 is gestart. De eerste D5-statusmatrix staat in `docs/workagenda-d5-statusmatrix.md` en `data/workagenda/d5_status_matrix.json`. De matrix gebruikt het stuurmodel, de D5 operationele vereisten en de nulmeting/capaciteitslaag om per D5-onderdeel rood/geel/grijs te sturen. Geen rij is klaar voor werkagenda-drafting; de volgende stap is Sprint 32.2 met constrained validatietickets en bewijsvelden.

Status op 2 mei 2026: Sprint 32.1 is afgerond en Sprint 32.2 is gestart. De eerste D5-validatieticketset staat in `docs/workagenda-d5-validation-tickets.md` en `data/workagenda/d5_validation_tickets.json`. De set bevat 47 tickets: vijf tickets per verplicht D5-onderdeel voor lokale status/capaciteit, governance/rollen, finance/controller, D6-afhankelijkheid en besluit/fasering, plus twee scope-keuzetickets voor conditionele/optionele ontwikkelagenda-items. Het is nog geen stakeholdervalidatie en nog geen werkagenda-draft.

Status op 2 mei 2026: Sprint 32.2 is repository-side afgerond. De validatietickets zijn gegroepeerd in zes stakeholderpakket-CSV's via `data/workagenda/d5_validation_packets.json` en `data/workagenda/validation_packets/*.csv`, met een menselijke handoff in `docs/workagenda-d5-validation-format.md`. Sprint 32.3 blijft geblokkeerd totdat echte antwoorden of expliciete beleidsbesluiten beschikbaar zijn. Sprint 32.4 is geopend voor tijdsafhankelijke bronbewaking en handreikingen.

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
- Interne D6-validatiepack toegevoegd en later gearchiveerd in `docs/review/archive/d6-support/almere_d6_validation_pack.md`; dit is validatiemateriaal en geen finale publicatie of bestuurlijke werkagendatekst.

Sprint 25.5: D6 stakeholder validation handoff
Status: repository-side complete; awaiting policy-maker stakeholder validation.

Repository-team verantwoordelijkheid:

- Completeer de publieke-brongrens; de oude detailnotitie staat in `docs/review/archive/d6-support/almere_d6_public_source_boundary.md`.
- Onderhoud de actuele menselijke ingang via `docs/review/almere_d6_deep_research_learnings.md` en `docs/review/almere_d6_open_questions.md`; gebruik de gearchiveerde validatiepack, informatie-uitvraag, decision-needed lijst, funding-gap tabel en safe-wording bibliotheek alleen als onderbouwing.
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
Status: completed.

- Maak deadlines, verwachte publicatiemomenten, reviewmomenten en begrotingsmomenten aparte tijdclaims.
- Sorteer en groepeer tijdlijnitems structureel chronologisch.
- Markeer verwachte momenten duidelijk anders dan vastgestelde deadlines.

Sprint 27.3: Geld
Status: completed.

- Maak claims voor financieringsinstrument, aanvraagvoorwaarde, budgetvenster, verdeelmechanisme, bestedingsruimte en verantwoording.
- Leg onzekerheden over uitkering, overloop, reservering en besteding apart vast.
- Voeg een zoekbare categorie toe voor "te verifieren financieringsregel".

Sprint 27.4: Governance
Status: completed.

- Maak rollen expliciet: ministerie, VNG, mandaatgemeente, regio, gemeente, raad, college, zorgverzekeraar, uitvoeringspartner.
- Splits besluitvorming, coordinatie, aanvraag, uitvoering en verantwoording.
- Voorkom dat "regio" als actor wordt gebruikt als de bron specifieker is.

Sprint 27.5: Locality
Status: completed.

- Markeer claims die expliciet over Almere gaan anders dan claims die alleen algemeen voor gemeenten gelden.
- Markeer Flevolandse claims apart van Almeerse claims.
- Houd adoptiegaten zichtbaar: landelijk doel aanwezig, lokale openbare uitwerking nog niet gevonden.

Sprint 27.6: Execution
Status: completed.

- Vertaal bronclaims naar mogelijke uitvoeringsvragen zonder beleidsadvies toe te voegen.
- Splits mogelijke besluitvragen, mogelijke opvolgacties, afhankelijkheden en reviewvragen.
- Laat de site niet suggereren dat een actie al is besloten als alleen de bronbasis aanleiding geeft om deze te onderzoeken.

Sprint 27.7: Perspectiefmodel stabilisatie
Status: completed.

- Controleer nul-tellingen en mogelijk onbereikbare enumwaarden voordat Phase 28 site-teksten op de zes statusvelden leunen.
- Verwijder pipeline-metawoorden uit classifier-termlijsten.
- Filter wetten.nl actiechrome die als regelgevingstekst in claims terechtkwam.
- Documenteer waarom de statusvelden nog verschillende reviewflags gebruiken.

## Fase 28 - Tekstkwaliteit van de website
Doel: minder technische of ruwe tekst, meer bestuurlijk leesbare Nederlandse samenvattingen.

Sprint 28.1: Menselijke samenvattingen per update
Status: completed.

- Elke data-update krijgt een korte, leesbare samenvatting.
- Leg uit welke publicatie aanleiding was voor de update.
- Benoem wat inhoudelijk is veranderd, zonder interne datatermen.

Sprint 28.2: Bronverwijzing en autoriteitstaal
Status: completed.

- Lagere-autoriteitsbronnen worden expliciet toegeschreven, bijvoorbeeld "Volgens de VNG-toelichting..." of "DUS-I vermeldt...".
- Normatieve bronnen krijgen sterkere formulering, maar alleen waar de bron dat draagt.
- Onzekerheden blijven zichtbaar zonder dramatische woorden als urgent of kritisch.

Sprint 28.3: Detailpagina's voor drill-down
Status: completed.

- Overzichtspagina's blijven kort.
- Lange claimlijsten, bronlijsten en reviewdetails gaan naar aparte detailpagina's.
- Elke klikbare tegel of telling moet naar de onderliggende items leiden.

Sprint 28.4: Pre-29 follow-up cleanup
Status: completed.

- Verwijder verouderde research-agent verwijzingen naar niet meer gegenereerde view models.
- Laat de site-renderer lokale orphan HTML-pagina's opruimen voordat nieuwe pagina's worden geschreven.
- Versterk de menselijke update-samenvattingstest met positieve vormcriteria en bredere jargonpatronen.
- Behandel `zero_count_statuses` als tijdelijke cleanup-opgave en plan die expliciet voor Fase 29.

## Fase 29 - Tijdlijn als beleidsinstrument
Doel: de tijdlijn gebruiken voor bestuurlijke orientatie, niet alleen als chronologische lijst.

Sprint 29.0: Perspectiefschema zero-count cleanup
Status: completed.

- Audit alle `zero_count_statuses` en `zero_count_actor_signals` voordat de tijdlijn sterker op statusvelden gaat sturen.
- Beslis per nulwaarde: behouden als bewust schema-veld, herstellen in classifierlogica, of verwijderen uit schema/config.
- Werk documentatie en tests bij zodat nulwaarden geen onduidelijke permanente backlog blijven.

Sprint 29.1: Tijdlijnregister verdiepen
Status: completed.

- Voeg bronstatus, autoriteit, actor, type moment en gevolg voor Almere toe aan tijdlijnitems.
- Houd verwachte, formele en lokale momenten zichtbaar verschillend.
- Leg per item vast welk perspectief vooral geraakt wordt: Tijd, Geld, Governance of Execution.

Sprint 29.2: Begrotings- en verantwoordingscyclus
Status: completed.

- Voeg landelijke en lokale begrotingsmomenten toe zodra ze bronvast zijn.
- Koppel gemeentefonds, meicirculaire, septembercirculaire, begroting Almere en SPUK-verantwoording waar bronnen dit dragen.
- Markeer waar menselijke beoordeling nodig is om een extern moment naar lokale planning te vertalen.

Sprint 29.3: Handreikingen en uitvoeringsmomenten
Status: completed.

- Houd handreikingen, webinars, thematafels en formatdocumenten apart van formele besluiten.
- Gebruik deze bronnen wel voor uitvoering en voorbereiding, maar niet als harde norm.
- Voeg nieuwe documenten pas toe na volledige pipeline-verwerking.

## Fase 30 - Lokale beleidsbruikbaarheid
Doel: de site beter laten aansluiten op vragen van Almeerse beleidsmakers.

Sprint 30.1: Lokale lacunes
Status: completed.

- De Almerepagina toont lokale lacunes per thema als openklapbare onderdelen.
- Elke lacune benoemt wat openbare bronnen wel laten zien, wat zij niet bewijzen, de mogelijke vervolgvraag en de veilige formulering.
- De D6-validatiegrens is toegevoegd als lokale lacune zonder deze als opgelost of `settled` te presenteren.
- Elke lacune is gekoppeld aan bronbasis via evidence-references in `data/site/site_almere_view.json`.

Sprint 30.2: Besluitvragen en mogelijke opvolgacties
Status: completed.

- Besluitvragen en mogelijke opvolgacties dragen expliciet `source_basis_summary`, `almere_choice_space`, `safe_use_note` en `perspective_summary`.
- Kaarten en detailpagina's tonen wat de bronbasis oproept en wat Almere zelf moet invullen.
- Opvolgacties zijn herformuleerd naar verkenningstaal en blijven zichtbaar als mogelijke werklijn, niet als vastgestelde opdracht.

Sprint 30.3: Beleidsdocumenten en rapporten
Status: completed.

- Actuele public-review kandidaten staan in `docs/rapporten/report-status.json`; vervallen concepten worden niet als public-facing kandidaat behandeld.
- De rapport-audit controleert actuele kandidaten op interne datalaagtaal, exacte fte-claims, bijlagenlijsten en te definitief klinkende interne planning.
- De interne controle staat in `docs/internal/report-grounding-audit-2026-04-29.md`.
- `plan-van-aanpak-v2.md` is expliciet gemarkeerd als vervallen concept met bekende anti-patronen.

## Fase 31 - Periodieke actualisatie
Doel: zorgen dat de site meebeweegt met nieuwe bronnen zonder dat oude informatie wordt overschreven.

Sprint 31.1: Updateprotocol
Status: completed.

- `docs/updateprotocol.md` beschrijft wanneer een update nodig is, welke changelogvelden verplicht zijn en hoe oude claims behouden blijven.
- `src/validate_update_protocol.py` controleert `config/site_updates.json` op volledigheid, menselijke samenvatting, metrics, pagina's en bestaande document-id's.
- De bestaande drie publieke updates voldoen aan het protocol; de controle-uitkomst staat in `docs/internal/update-protocol-check-2026-04-29.md`.

Sprint 31.2: Maandelijkse bronaudit
Status: completed.

- De watchlist staat in `config/monthly_source_audit.json`.
- `src/build_monthly_source_audit.py` controleert watchlistitems, pending intakekandidaten en optionele live-linkstatus.
- De audituitvoer staat in `data/extracted/monthly_source_audit.json` en `docs/internal/monthly-source-audit-2026-04-30.md`.
- Pending bronnen en verwachte publicaties blijven apart tot ze door formele bronintake en pipelineverwerking zijn gegaan.

Sprint 31.3: Reviewronde met menselijke beoordelaars
Status: completed.

- `src/build_human_review_round.py` maakt een reviewpack uit de review queue, perspectiefconfiguratie en maandelijkse bronaudit.
- `data/extracted/human_review_round.json` bevat de machineleesbare reviewronde.
- `docs/review/archive/phase31/phase31.3-human-review-round.md` bevat de menselijke reviewlijst per perspectief.
- Reviewerbesluiten blijven apart van bronclaims; D6-hardening blijft geblokkeerd zolang Sprint 25.6 geparkeerd is.

Sprint 31.4: Reviewtriage en deep-research offload
Status: completed.

- `src/build_review_triage.py` maakt een triagelaag uit de review queue, human-review round en D6 responsibility register.
- `data/extracted/review_triage_deep_research_offload.json` bevat de machineleesbare bucketverdeling.
- `docs/review/archive/phase31/phase31.4-review-triage-deep-research-offload.md` bevat de menselijke triagenotitie.
- `docs/review/archive/phase31/phase31.4-deep-research-agent-prompts.md` bevat opdrachten die aan deep research agents kunnen worden gedelegeerd.
- Deep research mag publieke bronhiaten verkleinen, maar niet de human-only D6-validatievragen beslissen.

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
De huidige sprint is Sprint 31.5: deep-research bronintake en top-layer verificatie.

Waarom:

- Sprint 31.1 heeft het updateprotocol en de updatevalidator opgeleverd;
- Sprint 31.2 heeft de maandelijkse bronaudit, watchlist en interne auditnotitie opgeleverd;
- Sprint 31.3 heeft de menselijke reviewronde per perspectief voorbereid;
- Sprint 31.4 heeft bepaald welke reviewtaken naar deep research agents kunnen en welke human-only blijven;
- Sprint 31.5 verwerkt deep-research rapporten alleen als bronsignaal: geselecteerde publieke bronnen worden formeel ingenomen en de conclusies worden getoetst aan de top data layers;
- Sprint 25.6 is terecht geparkeerd tot beleidsvalidatie beschikbaar is;
- de volgende gate vraagt een besluit of nog gerichte deep-research opdrachten nodig zijn, of dat de repository wacht op D6-validatie of doorgaat met een andere niet-D6 cleanup.

De concrete deliverables zijn:

- bronintake-notitie per verwerkt deep-research rapport;
- geselecteerde publieke bronnen in manifest, inventaris, claims en site-/reviewlagen;
- top-layer verificatie dat bevindingen zichtbaar zijn zonder D6-rijen als `settled` te markeren;
- geen D6-registerrijen inhoudelijk harden zolang stakeholdervalidatie voor Sprint 25.6 ontbreekt.
