# Completed Sprint Ledger

## Summary
Current roadmap version: `v2026.05.03-2`.

This file stores completed sprint history that used to live at the top of `docs/data-quality-roadmap.md`. The active roadmap now keeps only open, blocked, parked and planned work at the top.

Use this file for provenance. Do not use it as the active task list.

## Completed Sprints

| Sprint | Status | Vindplaats / opmerking |
| --- | --- | --- |
| 25.2 Lokale bronversterking Almere | completed | `data/extracted/local_source_strengthening_almere.json`, `docs/internal/source-intake/phase25.2-public-source-assessment.md`, `docs/completed-plans/phase25-sprint25.2-lokale-bronversterking.md` |
| 25.1 Werkagenda- en financieringslaag | completed | `data/extracted/workagenda_d5_operational_requirements.json`, `src/build_workagenda_d5_operational_requirements.py`, `docs/completed-plans/phase25-sprint25.1-werkagenda-financieringslaag.md` |
| 24.1 Taxonomie en checklist | completed | `config/data_quality_perspectives.json`, `docs/data-quality-checklist.md` |
| 24.2 Audit van bestaande site-data | completed | `docs/completed-plans/phase24-sprint24.2-audit.md`, `data/extracted/data_quality_audit.json` |
| 24.3 Review-dashboard intern | completed | `docs/internal/review-dashboard.html`, `src/build_internal_review_dashboard.py`, `docs/completed-plans/phase24-sprint24.3-review-dashboard.md` |
| 25.3 Nulmeting en capaciteit werkagenda | completed | `data/extracted/workagenda_nulmeting_capacity.json`, `src/build_workagenda_nulmeting_capacity.py`, `docs/completed-plans/phase25-sprint25.3-nulmeting-capaciteit.md` |
| 25.4 D6 governance en samenwerking | completed | Heropend en afgerond als D6 Almere responsibility pack: `docs/phase25-sprint25.4-d6-almere-responsibility-pack-plan.md`; registerlaag staat in `data/extracted/municipal/almere_d6_responsibility_register.json` en schema in `data/schemas/almere_d6_responsibility_register.schema.json` |
| 24.6 D6 commit, verify and stabilize | completed | Remediation is gecommit/gepusht; verificatie via `python src/run_pipeline.py --all`, gerichte tests en schema-validatie |
| 24.7 D6 register evidence audit | completed | Registerrijen gecontroleerd op status, eigenaar, uitvoerder, schaal, financiering, bewijs en open reviewvraag |
| 24.8 D6 local validation preparation | completed | Interne validatiepack gearchiveerd in `docs/review/archive/d6-support/almere_d6_validation_pack.md`; actuele menselijke ingang staat in `docs/review/almere_d6_open_questions.md` |
| 25.5 D6 stakeholder validation handoff | completed | Repository-side handoff compleet; wacht op policy-maker stakeholdervalidatie. Start via `docs/review/README.md`. Current artifacts are `docs/review/almere_d6_deep_research_learnings.md` for learned public-source information and `docs/review/almere_d6_open_questions.md` for remaining questions; detailed support files are archived in `docs/review/archive/d6-support/`. |
| 26.1 Rough-claim audit hercalibratie | completed | `src/build_data_quality_audit.py`, `tests/test_data_quality_audit.py`, `data/extracted/data_quality_audit.json`, `docs/completed-plans/phase26-sprint26.1-rough-claim-audit-recalibration.md` |
| 26.2 Deterministische tekstfixes | completed | `src/build_structural_extractions.py`, `src/build_document_extractions.py`, `data/extracted/voting_records.json`, `data/logs/phase26_text_cleanup.json`, `docs/completed-plans/phase26-sprint26.2-deterministic-text-fixes.md` |
| 26.3 Sentence-boundary en dedup | completed | `src/build_claims_top5.py`, `src/verify_claim_id_references.py`, `data/extracted/claims/sentence_validator_rejects.json`, `data/extracted/claims/dedup_log.json`, `docs/completed-plans/phase26-sprint26.3-sentence-boundary-dedup.md` |
| 27.1 Norm | completed | `src/build_claims_top5.py`, `data/schemas/claim.schema.json`, `data/extracted/data_quality_audit.json`, `docs/completed-plans/phase27-sprint27.1-norm.md` |
| 27.2 Tijd | completed | `src/build_claims_top5.py`, `data/schemas/claim.schema.json`, `data/extracted/data_quality_audit.json`, `data/site/timeline_register.json`, `docs/completed-plans/phase27-sprint27.2-tijd.md` |
| 27.3 Geld | completed | `src/build_claims_top5.py`, `data/schemas/claim.schema.json`, `data/extracted/data_quality_audit.json`, `docs/completed-plans/phase27-sprint27.3-geld.md` |
| 27.4 Governance | completed | `src/build_claims_top5.py`, `data/schemas/claim.schema.json`, `data/extracted/data_quality_audit.json`, `docs/completed-plans/phase27-sprint27.4-governance.md` |
| 27.5 Locality | completed | `src/build_claims_top5.py`, `data/schemas/claim.schema.json`, `data/extracted/data_quality_audit.json`, `docs/completed-plans/phase27-sprint27.5-locality.md` |
| 27.6 Execution | completed | `src/build_claims_top5.py`, `data/schemas/claim.schema.json`, `data/extracted/data_quality_audit.json`, `docs/completed-plans/phase27-sprint27.6-execution.md` |
| 27.7 Perspectiefmodel stabilisatie | completed | `src/build_claims_top5.py`, `src/build_structural_extractions.py`, `src/build_data_quality_audit.py`, `config/data_quality_perspectives.json`, `docs/completed-plans/phase27-sprint27.7-perspectiefmodel-stabilisatie.md` |
| 28.1 Menselijke samenvattingen per update | completed | `config/site_updates.json`, `config/site_taxonomy.json`, `src/render_site.py`, `tests/test_site_generation.py`, `docs/completed-plans/phase28-sprint28.1-menselijke-update-samenvattingen.md` |
| 28.2 Bronverwijzing en autoriteitstaal | completed | `src/render_site.py`, `src/build_site_view_models.py`, `tests/test_site_generation.py`, `docs/completed-plans/phase28-sprint28.2-bronverwijzing-autoriteitstaal.md` |
| 28.3 Detailpagina's voor drill-down | completed | `src/render_site.py`, `src/build_site_view_models.py`, `tests/test_site_generation.py`, `docs/completed-plans/phase28-sprint28.3-drilldown-detailpaginas.md` |
| 28.4 Pre-29 follow-up cleanup | completed | `RESEARCH_AGENT_MAP.md`, `src/render_site.py`, `tests/test_site_generation.py`, `docs/completed-plans/phase28-sprint28.4-pre29-followup-cleanup.md` |
| 29.0 Perspectiefschema zero-count cleanup | completed | `src/build_claims_top5.py`, `config/data_quality_perspectives.json`, `data/schemas/claim.schema.json`, `src/build_quality_control.py`, `data/extracted/data_quality_audit.json`, `docs/completed-plans/phase29-sprint29.0-perspectiefschema-zero-count-cleanup.md` |
| 29.1 Tijdlijnregister verdiepen | completed | `src/build_site_view_models.py`, `src/render_site.py`, `config/timeline_curation.json`, `data/site/timeline_register.json`, `docs/completed-plans/phase29-sprint29.1-tijdlijnregister-verdiepen.md` |
| 29.2 Begrotings- en verantwoordingscyclus | completed | `config/timeline_curation.json`, `src/build_site_view_models.py`, `src/render_site.py`, `data/site/site_timeline_view.json`, `docs/completed-plans/phase29-sprint29.2-begrotings-verantwoordingscyclus.md` |
| 29.3 Handreikingen en uitvoeringsmomenten | completed | `config/timeline_curation.json`, `src/build_site_view_models.py`, `src/render_site.py`, `data/site/site_timeline_view.json`, `docs/completed-plans/phase29-sprint29.3-handreikingen-uitvoeringsmomenten.md` |
| 30.1 Lokale lacunes | completed | `src/build_site_view_models.py`, `src/render_site.py`, `data/site/site_almere_view.json`, `dist/almere/index.html`, `docs/completed-plans/phase30-sprint30.1-lokale-lacunes.md` |
| 30.2 Besluitvragen en mogelijke opvolgacties | completed | `src/build_site_view_models.py`, `src/render_site.py`, `data/site/decision_view_models/*.json`, `data/site/action_view_models/*.json`, `docs/completed-plans/phase30-sprint30.2-besluitvragen-opvolgacties.md` |
| 30.3 Beleidsdocumenten en rapporten | completed | `docs/rapporten/report-status.json`, `src/audit_report_grounding.py`, `docs/internal/report-grounding-audit-2026-04-29.md`, `tests/test_report_grounding.py`, `docs/completed-plans/phase30-sprint30.3-beleidsdocumenten-rapporten.md` |
| 31.1 Updateprotocol | completed | `docs/updateprotocol.md`, `src/validate_update_protocol.py`, `docs/internal/update-protocol-check-2026-04-29.md`, `tests/test_update_protocol.py`, `docs/completed-plans/phase31-sprint31.1-updateprotocol.md` |
| 31.2 Maandelijkse bronaudit | completed | `config/monthly_source_audit.json`, `src/build_monthly_source_audit.py`, `data/extracted/monthly_source_audit.json`, `docs/internal/monthly-source-audit-2026-04-30.md`, `docs/completed-plans/phase31-sprint31.2-maandelijkse-bronaudit.md` |
| 31.3 Reviewronde met menselijke beoordelaars | completed | `src/build_human_review_round.py`, `data/extracted/human_review_round.json`, `docs/review/archive/phase31/phase31.3-human-review-round.md`, `docs/completed-plans/phase31-sprint31.3-reviewronde-menselijke-beoordelaars.md` |
| 31.4 Reviewtriage en deep-research offload | completed | `src/build_review_triage.py`, `data/extracted/review_triage_deep_research_offload.json`, `docs/review/archive/phase31/phase31.4-review-triage-deep-research-offload.md`, `docs/review/archive/phase31/phase31.4-deep-research-agent-prompts.md`, `docs/completed-plans/phase31-sprint31.4-review-triage-deep-research-offload.md` |
| 31.5 Deep-research bronintake en top-layer verificatie | completed | Afgerond in `docs/completed-plans/phase31-sprint31.5-deep-research-bronintake.md`. Deep-researchrapporten zijn verwerkt als bronsignaal of ontwerpinput, geselecteerde bronnen zijn via manifest/pipeline getoetst, niet-claim-ready bronvondsten blijven intakekandidaat, en de D6-validatiehandoff is aangescherpt zonder D6-rijen te harden. |
| 32.0 Werkagenda-delivery scope en stuurmodel | completed | `docs/workagenda-d5-stuurmodel.md`, `data/workagenda/d5_stuurmodel.json`, `tests/test_workagenda_d5_stuurmodel.py`, `docs/completed-plans/phase32-sprint32.0-workagenda-stuurmodel.md` |
| 32.1 D5-statusmatrix bouwen | completed | `docs/workagenda-d5-statusmatrix.md`, `data/workagenda/d5_status_matrix.json`, `src/build_workagenda_d5_status_matrix.py`, `tests/test_workagenda_d5_status_matrix.py`, `docs/completed-plans/phase32-sprint32.1-d5-statusmatrix.md` |
| 32.2 D5-validatie voorbereiden | completed | `docs/workagenda-d5-validation-tickets.md`, `data/workagenda/d5_validation_tickets.json`, `docs/workagenda-d5-validation-format.md`, `data/workagenda/d5_validation_packets.json`, `data/workagenda/validation_packets/*.csv`, `docs/completed-plans/phase32-sprint32.2-d5-validatieformats.md` |

