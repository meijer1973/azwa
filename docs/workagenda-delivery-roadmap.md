# Werkagenda-delivery roadmap

## Summary
Current sprint: Sprint 31.5 - Deep-research bronintake en top-layer verificatie.

This roadmap is the transition plan from a research repository to a workagenda-delivery system. It has been checked against the current repository state on 2026-05-02. It is a planning layer only: no D5 delivery sprint has started from this document yet.

The proposed direction is sound. The repository already contains many of the source, claim, review and D6 validation building blocks. The missing layer is a delivery-control layer that can show, per D5 component and per workagenda field, whether the answer is source-backed, needs local validation, needs finance/controller confirmation, needs a decision, depends on D6, waits for national guidance, or is ready for workagenda drafting.

## Sprint Ledger

| Sprint | Status | Goal | Main output |
| --- | --- | --- | --- |
| 32.0 Scope en stuurmodel vastzetten | planned | Fix the D5 scope, delivery statuses, milestones and owner/workstream model. | Werkagenda D5 stuurmodel v0.1. |
| 32.1 D5-statusmatrix bouwen | planned | Build one central matrix showing whether the workagenda is on track. | Werkagenda D5 statusmatrix v1. |
| 32.2 D5-validatie voorbereiden | planned | Create constrained D5 validation questions and workbook/format structure. | D5 validatieformats. |
| 32.3 Eerste menselijke validatieronde | blocked | Process stakeholder confirmations after validation packets are distributed. | Validatielog D5 ronde 1. |
| 32.4 Handreikingen en tijdsafhankelijke bronnen verwerken | planned | Watch and process D5 handreikingen, RPI/regioscan and other expected sources. | Bronupdate D5 handreikingen en wijzigingenlog. |
| 32.5 Gap compression en besluit-tickets | planned | Convert remaining gaps into validation, decision, finance or D6 dependency tickets. | Besluitlijst werkagenda D5 v1. |
| 32.6 Finance/controller en zorgverzekeraar integreren | planned | Build component-level finance and insurer confirmation status. | Finance/controller matrix D5 v1. |
| 32.7 D6-afhankelijkheden integreren | planned | Connect each D5 component to required D6 infrastructure. | D5-D6 afhankelijkhedenkaart v1. |
| 32.8 Prioritering, fasering en 2030-ingroeipad | planned | Convert inventory into choices, phasing and consequences. | Prioritering en fasering D5 v1. |
| 32.9 Concept-werkagenda v0.8 | blocked | Draft a bestuurlijk concept with explicit unresolved points. | Werkagenda D5 Almere/Flevoland concept v0.8. |
| 32.10 Governance-ready versie | blocked | Prepare version for IZA governance and college route. | Werkagenda D5 governance-ready v1.0. |
| 32.11 Vaststelling en VWS-verzending | blocked | Track decision route, changes and evidence. | Definitieve werkagenda + bewijs- en wijzigingslog. |
| 32.12 Uitvoeringsstart 2027 en lerende cyclus | blocked | Convert workagenda into execution steering and monitoring. | Uitvoeringsdashboard D5 2027. |

## Repository Fit Check

| Roadmap requirement | Current repository status | Fit |
| --- | --- | --- |
| Source-backed D5 workagenda requirements | Present in `data/extracted/workagenda_d5_operational_requirements.json`, with the D5 assignment, format, process note and financing letter as core sources. | Good starting point. |
| Public-source prefill for D5 current state and capacity | Present in `data/extracted/workagenda_nulmeting_capacity.json`; public-source boundary and local fill fields are explicit. | Good starting point, but not yet a delivery statusmatrix. |
| D6 dependency layer | Present for D6 as validation handoff: `data/extracted/municipal/almere_d6_responsibility_register.json`, `docs/review/almere_d6_deep_research_learnings.md`, `docs/review/almere_d6_open_questions.md`, and `docs/review/almere_d6_validation_ticket_matrix.md`. | Strong for D6 validation, not yet connected to D5 per component. |
| Timeline and source watch | Present via `data/site/timeline_register.json`, `config/monthly_source_audit.json`, `data/extracted/monthly_source_audit.json`, and Sprint 29/31 notes. | Good basis for handreiking and deadline tracking. |
| Finance separation | Present as perspective status and guardrail logic; D6 has funding gaps visible; D5 has funding-source awareness in operational requirements. | Needs a dedicated D5 finance/controller matrix. |
| Decision and validation workflow | Present for D6 and review queues; not yet available as a D5 workagenda decision register or D5 validation log. | Needs D5 delivery artifacts. |
| Human-readable steering dashboard | Internal review dashboard exists, but it is quality/review oriented rather than workagenda-delivery oriented. | Needs a workagenda dashboard view. |
| Workagenda writing readiness | Report grounding and public-text guardrails exist; no D5 workagenda concept generation should start until status, validation, finance and D6 dependency layers exist. | Roadmap correctly delays drafting until later sprints. |

## Current Gap

The repository can answer many research questions, but it cannot yet steer the workagenda as a delivery process. The missing delivery layer consists of:

- one D5 statusmatrix;
- D5 validation tickets and formats;
- D5 validation log;
- D5 finance/controller matrix;
- D5 decision register;
- D5-D6 dependency map;
- D5 source-update log for handreikingen and time-sensitive sources;
- workagenda dashboard view with red/yellow/green steering.

## Delivery Status Model

Every D5 component and workagenda field should use one of these statuses:

| Code | Status | Meaning |
| --- | --- | --- |
| A | Beantwoord uit bron | Public/corpus source directly answers the field. |
| B | Bron suggereert antwoord, validatie nodig | Source-backed working view exists, but local validation is required. |
| C | Lokale validatie nodig | Local practice, owner, coverage, capacity or evidence must be confirmed. |
| D | Bestuurlijk besluit nodig | A decision is needed before the field can be used as workagenda position. |
| E | Finance/controller nodig | Funding, structural continuation or double-counting must be checked. |
| F | Zorgverzekeraar/Zvw-bevestiging nodig | Zvw-side purchase, contract or insurer role must be confirmed. |
| G | ICT/privacy/data-bevestiging nodig | Data, privacy, dashboard, reporting or operational accountability must be confirmed. |
| H | Wachten op landelijke handreiking | National guidance or template still expected. |
| I | Optioneel / niet van toepassing | Item is optional, excluded or not applicable for the current scope. |
| J | Onbekend | Not enough information to classify yet. |

## D5 Scope

The first delivery-control sprint should create the canonical D5 scope list. The proposed roadmap should be treated as a starting structure, not as a settled local choice.

| Category | Components |
| --- | --- |
| D5 basisfunctionaliteiten | Laagdrempelige steunpunten; Sociaal verwijzen; Valpreventie; Ketenaanpak overgewicht en obesitas volwassenen; Kansrijke Start; Integrale gezinspoli; Nu Niet Zwanger. |
| Lopende ontwikkelagenda-items | Mentale gezondheidsnetwerken; Ketenaanpak overgewicht en obesitas kinderen. |
| Optionele nieuwe ontwikkelagenda-items | Dementie; Nicotinevrij; Rookvrije start; Multiproblematiek in NPLV-gebieden. |
| Overige of later te beoordelen initiatieven | Alleen opnemen als de regio daar expliciet voor kiest and the workagenda scope supports it. |

## Milestones To Track

These milestones should be stored in the delivery-control layer as planning targets and checked against source wording before external/public use:

| Moment | Meaning for delivery steering |
| --- | --- |
| Eind mei 2026 | Handreikingen basisfunctionaliteiten and process clarity for beproevende regio's expected. |
| Medio juli 2026 | RESV-related plans toward insurer/process track. |
| Half september 2026 | Practical workagenda readiness for IZA governance and college route. |
| 15 november 2026 | Formal deadline for regional workagenda adoption and VWS transmission. |
| December 2026 | Further clarity expected for later development-agenda items. |
| 1 januari 2027 | Start of implementation. |
| 2030 | Regional coverage/end-state horizon. |

## Proposed Core Files

| File | Function | Initial status |
| --- | --- | --- |
| `data/workagenda/d5_status_matrix.json` | Central status per D5 component and workagenda field. | Planned. |
| `data/workagenda/d5_validation_tickets.json` | Human validation questions with constrained answer options. | Planned. |
| `data/workagenda/d5_validation_log.json` | Who confirmed what, when, with what evidence. | Planned. |
| `data/workagenda/d5_finance_matrix.json` | Funding, double-counting, structural/project status and controller status. | Planned. |
| `data/workagenda/d5_decision_register.json` | Governance and bestuurlijke decision tickets. | Planned. |
| `data/workagenda/d5_d6_dependency_map.json` | D6 preconditions per D5 component. | Planned. |
| `data/workagenda/d5_source_update_log.json` | Handreikingen, regioscan, rode-dradenanalyse and time-sensitive source changes. | Planned. |
| `data/workagenda/d5_dashboard_view.json` | Red/yellow/green workagenda steering view. | Planned. |
| `docs/workagenda/` | Human-readable delivery notes, validation formats and handoff material. | Planned; avoid mixing with unreviewed source packages. |

## Workstreams

| Workstream | Repository-side task | External dependency |
| --- | --- | --- |
| Repository/data | Build status, validation, finance, decision, dependency and dashboard layers. | None for initial structure; later validation data needed. |
| Human validation D5 | Prepare constrained questions and evidence fields. | Stakeholders must confirm/correct and supply evidence. |
| Targeted research agents | Monitor handreikingen, RPI/regioscan, development-agenda updates and named local sources. | New publications or named source leads. |
| Finance/controller | Prepare matrix and double-counting questions. | Controller, finance and insurer confirmation. |
| D6 dependencies | Link D5 execution to the D6 responsibility and validation layers. | D6 validation remains a policy-maker/stakeholder dependency. |

## Gate Rules

- Do not start D5 workagenda drafting from this roadmap alone.
- Do not mark a D5 field ready if it only has a source-backed working view and still needs local validation.
- Do not use finance wording as confirmed unless finance/controller or insurer evidence exists.
- Do not hide D6 prerequisites inside D5 programme text; record them as dependencies.
- Do not send broad research agents unless a named source, expected publication or explicit source gap exists.
- Do not move from Sprint 32.2 to Sprint 32.3 until the validation formats are constrained enough that stakeholders can answer by confirming, correcting, choosing and attaching evidence.
- Do not move to Sprint 32.9 drafting until the statusmatrix, validation tickets, finance matrix, decision register and D5-D6 dependency map exist.

## Recommended Next Step

The next executable sprint is Sprint 32.0, not Sprint 32.1. Although the proposed roadmap suggests starting Sprint 1 and 2 in parallel, the current repository should first create the delivery-control contract:

- canonical D5 scope list;
- accepted delivery statuses;
- milestone model;
- file/schema choices;
- relationship to existing D5 and D6 data layers;
- dashboard design boundary.

After Sprint 32.0, Sprints 32.1 and 32.2 can run in parallel.
