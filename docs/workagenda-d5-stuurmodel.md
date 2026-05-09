# Werkagenda D5 stuurmodel v0.1

## Summary
Current sprint: Sprint 32.0 - Werkagenda-delivery scope en stuurmodel.

This is the first delivery-control contract for the D5 workagenda track. It does not start drafting the workagenda. It fixes the scope, statuses, fields, milestones and guardrails that Sprint 32.1 and Sprint 32.2 should use when building the D5 statusmatrix and validation formats.

Machine-readable version: `data/workagenda/d5_stuurmodel.json`.

## Purpose

The next phase turns the repository from a research tool into a workagenda-delivery system. The delivery system must show, per D5 component and workagenda field:

- what is answered by sources;
- what still needs local validation;
- what needs finance/controller or insurer confirmation;
- what needs a bestuurlijk decision;
- what depends on D6 infrastructure;
- what waits for national guidance;
- what is ready for workagenda drafting.

## Status Model

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

## D5 Scope

| D5 component | Category | Required in workagenda? |
| --- | --- | --- |
| Laagdrempelige steunpunten | Basisfunctionaliteit | Yes |
| Sociaal verwijzen | Basisfunctionaliteit | Yes |
| Valpreventie | Basisfunctionaliteit | Yes |
| Ketenaanpak overgewicht en obesitas volwassenen | Basisfunctionaliteit | Yes |
| Kansrijke Start | Basisfunctionaliteit | Yes |
| Integrale gezinspoli | Basisfunctionaliteit | Yes |
| Nu Niet Zwanger | Basisfunctionaliteit | Yes |
| Mentale gezondheidsnetwerken | Ontwikkelagenda 1 lopend | Yes |
| Ketenaanpak overgewicht en obesitas kinderen | Ontwikkelagenda 1 lopend | Yes |
| Ontwikkelagenda 1 nieuw: dementie, nicotinevrij, rookvrije start, multiproblematiek NPLV | Conditioneel | No, unless the region chooses to act as a pilot region for one or more of these approaches. |
| Ontwikkelagenda 2 en overige initiatieven | Optional | No, unless the region explicitly chooses to include them. |

## Workagenda Fields

Each D5 component should eventually be scored on these fields:

| Field | Use |
| --- | --- |
| Huidige situatie | What exists now, and how strong the evidence is. |
| Gewenste situatie | Target state or intended arrangement. |
| Ingroeipad 2030 | Build-up and coverage path toward 2030. |
| Aantallen/capaciteit | Capacity, population, volume or indicative numbers. |
| Financiering | Funding line, structural/project status and double-counting risk. |
| Verantwoordelijkheid/governance | Owner, coordinator, executor, partner and decision route. |
| Monitoring/lerende cyclus | Indicators, reporting owner and adjustment cycle. |
| Mijlpalen | Relevant deadline, planning or implementation moment. |
| D6-afhankelijkheden | Required social-base, access, monitoring or infrastructure preconditions. |
| Open besluiten/risico's | Decisions, blockers and explicit risks. |

## Milestones

| Moment | Delivery meaning |
| --- | --- |
| Eind mei 2026 | Handreikingen basisfunctionaliteiten and process clarity for pilot regions / regions trying new approaches in practice expected. |
| Medio juli 2026 | RESV-related plans toward insurer/process track. |
| Half september 2026 | Practical workagenda readiness for IZA governance and college route. |
| 15 november 2026 | Formal deadline for regional workagenda adoption and VWS transmission. |
| December 2026 | Further clarity expected for later development-agenda items. |
| 1 januari 2027 | Start of implementation. |
| 2030 | Regional coverage/end-state horizon. |

## Planned Delivery Files

| File | Status |
| --- | --- |
| `data/workagenda/d5_status_matrix.json` | Planned for Sprint 32.1. |
| `data/workagenda/d5_validation_tickets.json` | Planned for Sprint 32.2. |
| `data/workagenda/d5_validation_log.json` | Planned after validation responses. |
| `data/workagenda/d5_finance_matrix.json` | Planned for finance/controller track. |
| `data/workagenda/d5_decision_register.json` | Planned for decision tickets. |
| `data/workagenda/d5_d6_dependency_map.json` | Planned for D5-D6 dependency mapping. |
| `data/workagenda/d5_source_update_log.json` | Planned for handreikingen and time-sensitive source changes. |
| `data/workagenda/d5_dashboard_view.json` | Planned for red/yellow/green steering. |

## Guardrails

- This stuurmodel is not a local decision.
- Do not treat source-backed working views as locally validated answers.
- Do not mark finance as confirmed without finance/controller or insurer evidence.
- Do not start workagenda drafting until status, validation, finance, decision and D5-D6 dependency layers exist.
- Do not hide D6 prerequisites inside D5 programme text; record them as dependencies.

## Done For Sprint 32.0

Sprint 32.0 is complete when:

- this human-readable stuurmodel exists;
- the machine-readable JSON contract exists;
- tests verify the D5 scope and status contract;
- the roadmap points to this stuurmodel;
- Sprint 32.1 and Sprint 32.2 can safely start from this contract.
