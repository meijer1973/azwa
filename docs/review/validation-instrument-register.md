# Validation Instrument Register

## Summary
Current sprint: Sprint 33.P0 - Freeze validation instruments.

Recorded on: 2026-05-03.

This register treats the current D5 and D6 Excel workbooks as pre-validation baseline instruments. They are not final policy truth, not corpus sources, and not stakeholder validation results.

Use this register before editing, sending, or importing answers from the workbooks.

## Current Instruments

| Instrument | Path | Version | Status | Sheets | Purpose | Source basis | Next QA action |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| D5 validatieformat werkagenda Almere | `docs/review/D5_validatieformat_werkagenda_Almere_v0.1.xlsx` | `v0.1` | pre-validation baseline | 20 | Prepare D5 workagenda validation before contacting policymakers. | `data/workagenda/d5_status_matrix.json`, `data/workagenda/d5_validation_tickets.json`, `data/workagenda/d5_validation_packets.json`, source corpus and generated evidence layers. | Check IDs, routing, current working views, evidence gates, stakeholder packet fit and import path. |
| Almere D6 validatieformats | `docs/review/Almere_D6_validatieformats.xlsx` | current imported baseline | pre-validation baseline | 15 | Prepare D6 infrastructure, ownership, mandate, funding and safe-wording validation. | `docs/review/almere_d6_deep_research_learnings.md`, `docs/review/almere_d6_open_questions.md`, `docs/review/almere_d6_validation_ticket_matrix.md`, `data/extracted/municipal/almere_d6_responsibility_register.json`. | Check IDs, routing, plain-language answer choices, evidence gates and validation-log path. |

## Freeze Rule

Do not make uncontrolled edits to these workbooks while pre-contact QA is running. Changes should either:

- update the workbook version;
- be reflected in repository validation ticket/log structures;
- or be recorded as a review note before stakeholder contact.

The current baseline may be improved during Sprint 33.P1-33.P6, but every material change should be intentional and traceable.

## Shared Vocabulary

Use this shared vocabulary across D5 and D6 where possible:

- `Bevestigd met bewijs`
- `Deels bevestigd`
- `Nog te valideren`
- `Besluit nodig`
- `Finance/controller nodig`
- `ICT/privacy nodig`
- `Niet mijn domein`
- `Onbekend`
- `Anders, toelichten`

## Import Rule

Human answers should not silently become source claims.

| Answer type | Processing route |
| --- | --- |
| Public source found | Add source, ingest, rerun/check evidence layer. |
| Stakeholder confirmation | Add to validation log. |
| Finance/controller confirmation | Add to finance matrix and validation log. |
| Formal decision | Add to decision register and evidence log. |
| Conflicting answers | Mark review needed. |
| Unknown | Keep unresolved. |

## Send-readiness Rule

Do not contact policymakers with these workbooks until the send-readiness gate confirms:

- every validation question has a stable ID;
- each row has a stakeholder group;
- dropdowns include `onbekend`, `niet mijn domein` and `anders`;
- each human-facing tab has a concise current working view;
- each answer path has an evidence field;
- finance and ICT/privacy questions are separated where relevant;
- an internal dry run has been completed;
- the route back into validation logs, finance matrices, decision registers or source intake is clear.

## Sheet Inventory

### D5 Workbook

- Start hier
- Stakeholderpakketten
- Overzicht D5
- Laagdremp. steunpunten
- Sociaal verwijzen
- Mentale gezondheid
- Valpreventie
- Overgewicht volwassenen
- Kansrijke Start
- Integrale gezinspoli
- Nu Niet Zwanger
- Overgewicht kinderen
- Optionele ontwikkelagenda
- Financiering
- Governance rollen
- Monitoring cyclus
- D6 afhankelijkheden
- Validatielog
- Bronnen wijzigingen
- Keuzelijsten

### D6 Workbook

- Instructies
- Keuzelijsten
- Inloopvoorzieningen
- Wijkteams
- SLT
- JGZ Almere
- GGD Flevoland
- Gezonde School
- Monitoring
- Samen Sterker
- PGA-Zorgzaam-Flever
- Digitaal-operationeel
- Informele steun
- Financiering
- Stakeholderpakketten
