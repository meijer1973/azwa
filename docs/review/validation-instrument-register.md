# Validation Instrument Register

## Summary
Current roadmap sprint: Sprint 33.P7 - Send-readiness gate blocked.

Recorded on: 2026-05-09.

Created during Sprint 33.P0 and updated through Sprint 33.P6. This register treats the current D5 and D6 Excel workbooks as pre-validation baseline instruments. They are not final policy truth, not corpus sources, and not stakeholder validation results.

Use this register before editing, sending, or importing answers from the workbooks.

## Current Instruments

| Instrument | Path | Version | Status | Sheets | Purpose | Source basis | Next QA action |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| D5 validatieformat werkagenda Almere | `docs/review/D5_validatieformat_werkagenda_Almere_v0.1.xlsx` | `v0.1` | pre-validation baseline | 20 | Prepare D5 workagenda validation before contacting policymakers. | `data/workagenda/d5_status_matrix.json`, `data/workagenda/d5_validation_tickets.json`, `data/workagenda/d5_validation_packets.json`, source corpus and generated evidence layers. | Complete P5 human dry run and packet fixes before P7 send-readiness. |
| Almere D6 validatieformats | `docs/review/Almere_D6_validatieformats.xlsx` | current imported baseline | pre-validation baseline | 15 | Prepare D6 infrastructure, ownership, mandate, funding and safe-wording validation. | `docs/review/almere_d6_deep_research_learnings.md`, `docs/review/almere_d6_open_questions.md`, `docs/review/almere_d6_validation_ticket_matrix.md`, `data/extracted/municipal/almere_d6_responsibility_register.json`. | Complete P5 human dry run and packet fixes before P7 send-readiness. |

## Traceability Layer

Sprint 33.P1 created:

- `data/workagenda/validation_workbook_traceability_map.json`
- `docs/review/validation-workbook-traceability-audit.md`
- `src/build_validation_workbook_traceability.py`

The traceability map assigns generated stable IDs, component IDs, stakeholder packages, answer types, evidence requirements, repo-update effects and pre-contact deadlines to 245 validation rows across the D5 and D6 workbooks. The workbooks themselves should still not be sent as raw files until outgoing packets include visible/protected row identity or another controlled answer-processing route.

## Prefill Audit Layer

Sprint 33.P2 created:

- `data/workagenda/validation_workbook_prefill_audit.json`
- `docs/review/validation-workbook-prefill-audit.md`
- `src/build_validation_workbook_prefill_audit.py`

The prefill audit checks current working views, assessment/correction fields, evidence fields, broad questions and internal jargon. It does not validate policy content. Its main finding is that the workbooks are usable as pre-contact drafts, but the outgoing packets still need targeted cleanup before stakeholder contact.

## Pre-contact Agent Plan

Sprint 33.P3 created:

- `data/workagenda/precontact_agent_plan.json`
- `docs/review/precontact-agent-prompts.md`
- `src/build_precontact_agent_plan.py`

The agent plan prepares five narrow prompts: evidence-prefill audit, D5 source-update watchlist, D5-D6 dependency mapping, policymaker readability and finance-risk precheck. They are marked `prepared_not_sent`. They must not be used to contact stakeholders or settle local validation, ownership, mandate, funding, D6 classification or final workagenda wording.

## Pre-contact Stakeholder Packet Layer

Sprint 33.P4 created:

- `data/workagenda/precontact_stakeholder_packets.json`
- `docs/review/precontact-stakeholder-packets.md`
- `data/workagenda/precontact_packets/*.csv`
- `src/build_precontact_stakeholder_packets.py`

The packet layer creates filtered D5/D6 validation packet drafts with `vraag_id`, component IDs, answer type, evidence fields, repo-update effects and `not_my_domain_reroute` columns. Packets are marked `prepared_not_sent`; they are not validation records and must not be sent before the P7 send-readiness gate. The broad Gemeente Almere sociaal-domein route is split into three packets: D5 local input, D6 validation and sturing/afhankelijkheden.

## Internal Dry-run Layer

Sprint 33.P5 created:

- `data/workagenda/precontact_internal_dry_run.json`
- `docs/review/precontact-internal-dry-run.md`
- `src/build_precontact_internal_dry_run.py`

The dry-run layer defines five exact cases for internal reviewers: a D5 tab, a D6 tab, a finance row, an evidence-field case and a `not_my_domain_reroute` case. The repository-side case pack is complete, but the human dry run is still pending. This blocks P7 send-readiness and policymaker contact; it does not block Sprint 33.P6 workflow integration.

## Response Workflow Layer

Sprint 33.P6 created:

- `data/workagenda/precontact_response_workflow.json`
- `docs/review/precontact-response-workflow.md`
- `src/build_precontact_response_workflow.py`

The response workflow maps every current `repo_update_effect` route to validation logs, finance matrices, decision registers, the D5-D6 dependency map, source-update log, statusmatrix or D6 responsibility register. It also defines answer outcomes, evidence gates and no-overclaim rules. It imports no answers and does not authorize stakeholder contact.

Human input belongs in the Excel validation workbooks. CSV packet files are machine/export/import artifacts and should only be generated or machine-edited by repository tooling. If a human answer names a credible public source, add the source to source intake and verify it through top data layers before treating it as source-backed. If a human answer gives a conclusion without a source, document, decision, budget line or evidence path, record it as low-authority validation input only.

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
