# Pre-contact Response Workflow

## Summary
Current sprint: Sprint 33.P6 - Pre-contact validation-readiness: repository/workflow integration.

Generated on: 2026-05-09.

Status: `repository_workflow_defined_no_answers_imported`.

Human validation status: `no_stakeholder_answers_yet`.

P5 human dry-run status: `pending_internal_reviewers`.

Gate effect: P6 is repository-side complete when this workflow is generated and tested; P7 remains blocked until the P5 human dry run is completed.

This file defines how returned D5/D6 packet answers must be processed. It does not import answers and it does not authorize stakeholder contact.

## Return Contract

| Rule | Meaning |
| --- | --- |
| Required fields | `vraag_id, stakeholderpakket, answer, evidence_type, evidence_reference, correction_or_note, not_my_domain_reroute` |
| Human input channel rule | Human reviewers enter answers in the Excel validation workbooks. CSV packet files are machine/export/import artifacts and should not be the normal human entry surface. |
| CSV machine rule | CSV files may be generated or machine-edited by repository tooling only; preserve vraag_id, stakeholderpakket and evidence fields exactly. |
| Identity rule | Every returned answer must preserve vraag_id and stakeholderpakket; do not merge answers by question text. |
| Evidence rule | Confirmed answers require evidence_type and evidence_reference before they can update status, finance, decision or register layers. |
| Source rule | New public sources named in responses go to source intake first and are not substantive evidence until processed through the pipeline and verified in top data layers. |
| Unsupported human input rule | Human input without credible evidence is recorded as low-authority validation input and cannot make a field source-backed, ready, confirmed or settled. |

## Authority Levels

| Level | Authority | Meaning | Allowed effect |
| --- | --- | --- | --- |
| `source_ingested_and_top_layer_verified` | `high` | A credible public source has been added to the source corpus, processed by the pipeline and verified in the relevant top data layer. | May support source-backed updates when the source directly answers the field. |
| `formal_decision_or_controller_confirmation` | `high_for_validation` | A formal local/regional decision, budget line, controller confirmation or internal mandate document is named or attached. | May support validation, finance or decision-register updates; it is not a public corpus source unless separately ingested as a public source. |
| `stakeholder_confirmation_with_evidence_reference` | `medium_for_validation` | A stakeholder answer names a role, document, decision or evidence path but the evidence has not yet been independently processed. | Record in validation log; update only cautiously and keep evidence follow-up open where needed. |
| `human_input_without_source_backup` | `low` | A human answer provides a conclusion but no credible source, document, decision, budget line or evidence path. | Record as low-authority confirmation only; do not mark ready, confirmed, source-backed or settled. |
| `new_public_source_named_not_ingested` | `candidate` | A reviewer names a potentially useful public source that is not yet in the corpus. | Add to source-update/source-intake queue first; no substantive status change until ingestion and top-layer verification. |

## Answer Outcomes

| Outcome | May update status? | Processing rule |
| --- | --- | --- |
| `confirmed_with_evidence` | yes | First classify the evidence. If a high-quality public source is named, ingest and verify it through top layers before treating it as source-backed. If the evidence is a stakeholder/internal confirmation, record it as validation evidence and update only the directly supported field. |
| `confirmed_without_evidence` | no | Record as low-authority human confirmation; do not mark ready, confirmed or settled. |
| `partly_correct` | no | Update the working view and keep review_needed until the correction and evidence are clear. |
| `incorrect` | no | Correct the working view, keep review_needed and create a decision ticket if a policy choice is needed. |
| `not_my_domain` | no | Do not treat as substantive validation; reroute using not_my_domain_reroute and keep the original vraag_id. |
| `unknown` | no | Keep unresolved and preserve the open question. |
| `conflict` | no | Escalate to review_needed or decision register; do not force a conclusion. |
| `decision_needed` | no | Create or update a decision ticket with owner, options, deadline and evidence after decision. |
| `finance_needed` | no | Route to finance matrix or finance/controller ticket; no funding wording becomes confirmed. |
| `ict_privacy_needed` | no | Route to ICT/privacy register; no data-accountability wording becomes confirmed. |
| `public_source_found` | no | Add the public source to source intake first; ingest, run pipeline and verify top layers before using as source evidence. |

## Route Coverage

| Repo update effect | Unique vraag IDs | Packet rows | Primary targets | Conditional targets | Status target |
| --- | ---: | ---: | --- | --- | --- |
| `d5_d6_dependency_map_update` | 9 | 18 | `d5_d6_dependency_map` | `d5_validation_log, d6_validation_log, d6_decision_register` | `d5_status_matrix` |
| `d6_finance_matrix_or_decision_ticket` | 12 | 36 | `d6_finance_matrix` | `d6_validation_log, d6_decision_register, source_update_log` | `d6_responsibility_register` |
| `d6_validation_log_or_decision_ticket` | 37 | 104 | `d6_validation_log` | `d6_decision_register, source_update_log` | `d6_responsibility_register` |
| `d6_validation_log_or_ict_privacy_ticket` | 12 | 36 | `d6_validation_log` | `ict_privacy_register, d6_decision_register, source_update_log` | `d6_responsibility_register` |
| `d6_validation_log_or_register_update` | 30 | 67 | `d6_validation_log` | `d6_responsibility_register, d6_decision_register, source_update_log` | `d6_responsibility_register` |
| `decision_register_or_validation_log` | 45 | 90 | `d5_decision_register, d5_validation_log` | `source_update_log` | `d5_status_matrix` |
| `decision_ticket_or_status_matrix_update` | 5 | 10 | `d5_decision_register, d5_status_matrix` | `d5_validation_log, source_update_log` | `d5_status_matrix` |
| `finance_matrix_update` | 11 | 22 | `d5_finance_matrix` | `d5_validation_log, d5_decision_register, source_update_log` | `d5_status_matrix` |
| `status_matrix_update` | 12 | 12 | `d5_status_matrix, d5_validation_log` | `source_update_log` | `d5_status_matrix` |
| `validation_log_or_decision_ticket` | 29 | 80 | `d5_validation_log` | `d5_decision_register, source_update_log` | `d5_status_matrix` |
| `validation_log_or_finance_ticket` | 33 | 99 | `d5_validation_log` | `d5_finance_matrix, d5_decision_register, source_update_log` | `d5_status_matrix` |
| `validation_log_or_ict_privacy_ticket` | 10 | 30 | `d5_validation_log` | `ict_privacy_register, source_update_log` | `d5_status_matrix` |

## Target Artifacts

| Target | Status | Path | Purpose |
| --- | --- | --- | --- |
| `d5_d6_dependency_map` | `planned_no_answers_yet` | `data/workagenda/d5_d6_dependency_map.json` | D6 preconditions and blockers per D5 component. |
| `d5_decision_register` | `planned_no_answers_yet` | `data/workagenda/d5_decision_register.json` | D5 policy, governance, phasing and workagenda decision tickets. |
| `d5_finance_matrix` | `planned_no_answers_yet` | `data/workagenda/d5_finance_matrix.json` | D5 funding line, structural/project status, double-counting risk and controller/Zvw confirmation. |
| `d5_status_matrix` | `existing_update_target` | `data/workagenda/d5_status_matrix.json` | D5 delivery status per component and workagenda field. |
| `d5_validation_log` | `planned_no_answers_yet` | `data/workagenda/d5_validation_log.json` | D5 stakeholder confirmations, corrections, weak confirmations, unknowns and conflicts. |
| `d6_decision_register` | `planned_no_answers_yet` | `data/workagenda/d6_decision_register.json` | D6 classification, mandate, owner, funding and safe-wording decision tickets. |
| `d6_finance_matrix` | `planned_no_answers_yet` | `data/workagenda/d6_finance_matrix.json` | D6 funding line, structural/project status, double-counting risk and controller confirmation. |
| `d6_responsibility_register` | `existing_update_target_after_validation_only` | `data/extracted/municipal/almere_d6_responsibility_register.json` | D6 responsibility register; no row may become settled without direct evidence. |
| `d6_validation_log` | `planned_no_answers_yet` | `data/workagenda/d6_validation_log.json` | D6 stakeholder confirmations, corrections, weak confirmations, unknowns and conflicts. |
| `ict_privacy_register` | `planned_no_answers_yet` | `data/workagenda/ict_privacy_decision_register.json` | ICT/privacy/data-accountability issues that cannot be resolved from the validation packet answer alone. |
| `source_update_log` | `planned_no_answers_yet` | `data/workagenda/d5_source_update_log.json` | New public sources named by stakeholders, handreiking updates and source-intake follow-up. |

## Quality Gates

- `excel_for_human_input`: Human reviewers use Excel workbooks; CSV packet files are machine-processing artifacts.
- `unsupported_human_input_low_authority`: Human input without source/document/decision/budget evidence is low-authority validation input and cannot settle a field.
- `source_ingestion_before_source_backing`: Named public sources must be ingested and verified in top data layers before becoming source-backed evidence.
- `no_silent_source_claims`: Stakeholder answers, finance confirmations and decisions are validation evidence, not corpus source claims.
- `no_settled_without_evidence`: No D6 register row can move to settled unless classification, owner, executor/coordinator, scale, funding and evidence are directly supported.
- `weak_confirmation_stays_open`: Confirmation without evidence is logged but cannot make a field ready for drafting.
- `conflicts_escalate`: Conflicting responses create review_needed or decision tickets; the repository team does not choose between them by inference.
- `not_my_domain_reroutes`: Not-my-domain answers keep the original vraag_id and are rerouted rather than counted as negative validation.

## P7 Blockers

- P5 human internal dry run is pending.
- No stakeholder packets may be sent before P7 send-readiness gate.
- No returned stakeholder answers exist yet.

## Next Step

P7 send-readiness cannot open until the P5 human dry run is completed and any packet fixes are made. If answers return later, process them through this workflow instead of editing status, finance, decision or D6 register layers directly.
