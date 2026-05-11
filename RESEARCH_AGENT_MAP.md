# Research Agent Map

Agent-executable navigation and access specification for the AZWA / IZA / GALA corpus and derived data layers.

## Minimal Research Guidance

This file is a repository map, not a substitute for independent source evaluation.

Use the derived data layers to navigate the corpus efficiently:

- `data/extracted` for structured claims, timelines, and Almere/D5/D6 views.
- `data/site` for synthesized orientation.
- `sources markdown canonical` and `sources canonical` when exact wording, dates, obligations, or public citations matter.

Do not treat generated data-layer files as public policy sources. They are research aids derived from the source corpus.

For workagenda filling, use public sources as far as they go. When a field requires non-public local knowledge, staff confirmation, or a formal local decision, mark it as a validation gap or decision question instead of treating it as a blocker to the public-source structure.

For Almere local-gap reasoning, use `data/extracted/municipal/almere_current_view.json` and `data/extracted/municipal/almere_d6_responsibility_register.json` as the structured basis. `data/site/site_almere_view.json` contains a human-readable local-gap synthesis with what public sources show, what they do not prove, and safe wording, but it remains an orientation layer rather than primary evidence.

Decision and action site view models are human-readable choice-question layers. Their `source_basis_summary` explains what the public source base raises; `almere_choice_space` explains what Almere still has to decide or validate. Do not treat possible follow-up actions as assigned tasks unless a canonical source or validation record supports that.

For report use, check `docs/rapporten/report-status.json` before treating a markdown report as current. Superseded drafts are retained for traceability and may contain known anti-patterns; current public-review candidates must avoid internal datalayer language and unsupported exact capacity, budget, appendix or internal-planning claims.

For source-intake and public update history, follow `docs/updateprotocol.md`. A source intake or source correction that changes public interpretation, claims, timeline moments, review status, report-readiness or public pages must be recorded in `config/site_updates.json` and regenerated into `data/site/site_updates_view.json`, the public `/updates/` page and the internal dashboard mirror.

For monthly source monitoring, use `config/monthly_source_audit.json`, `data/extracted/monthly_source_audit.json`, and `docs/internal/monthly-source-audit-2026-04-30.md`. Watchlist rows, expected publications and pending intake candidates are not public evidence until source intake, manifest registration and pipeline processing have happened.

For human review routing, use `data/extracted/human_review_round.json` and `docs/review/archive/phase31/phase31.3-human-review-round.md`. Reviewer decisions must be recorded as human review decisions or validation records; they do not become source claims unless backed by a canonical source or explicit validation evidence.

For deep-research delegation, use `data/extracted/review_triage_deep_research_offload.json`, `docs/review/archive/phase31/phase31.4-review-triage-deep-research-offload.md`, and `docs/review/archive/phase31/phase31.4-deep-research-agent-prompts.md`. Deep research agents may reduce public-source gaps and source-authority uncertainty, but they must not settle D6 classification, ownership, mandate, funding, safe wording, or register status.

For human-readable review navigation, start with `docs/review/README.md`. Archived review notes under `docs/review/archive/` are provenance only, not current entry points.

For D6 validation handoff, use `docs/review/almere_d6_deep_research_learnings.md` to see what public-source intake added, `docs/review/almere_d6_open_questions.md` to see what still must be asked, and `docs/review/almere_d6_validation_ticket_matrix.md` to turn those questions into plain-language stakeholder choices. Do not merge those categories when drafting conclusions.

For deep-research intake, use `docs/dr/README.md`. Reports placed in `docs/dr/` are not corpus evidence. Treat them as source-discovery signals: ingest selected public sources through the raw manifest and pipeline, then verify that the findings appear in top data layers before marking the report processed.

For regional governance around Flevoland and Almere, always load `docs/regional-roles-and-splits-almere-flevoland.md` and `data/curated/regional_roles_and_splits_almere_flevoland.json`. In SPUK/mandaatgemeente tables, read the region field and mandate-municipality field separately: regio Flevoland plus gemeente Almere as mandaatgemeente. Keep the province Flevoland, IZA/AZWA-regio Flevoland, gemeente Almere, Verbindende Coalitie Zorgzaam Flevoland and Netwerkbureau Zorgzaam Flevoland separate unless a source explicitly links a role.

For roadmap navigation, use `docs/data-quality-roadmap.md` as the single canonical roadmap. Its top Active Task Ledger shows work still to do. Completed sprint history lives in `docs/roadmap/completed-sprint-ledger.md`. `docs/workagenda-delivery-roadmap.md` is only a redirect; do not maintain it as a second active roadmap. Use `docs/roadmap/roadmap-version-log.md` for roadmap version history.

For Sprint 32.0-32.2 workagenda-delivery scope, use `docs/workagenda-d5-stuurmodel.md`, `data/workagenda/d5_stuurmodel.json`, `docs/workagenda-d5-statusmatrix.md`, `data/workagenda/d5_status_matrix.json`, `docs/workagenda-d5-validation-tickets.md`, `data/workagenda/d5_validation_tickets.json`, `docs/workagenda-d5-validation-format.md`, and `data/workagenda/d5_validation_packets.json`. These files define the D5 scope, delivery status values, workagenda fields, milestones, the first D5 delivery-status matrix, constrained validation tickets and stakeholder packet formats. They are control layers, not local decisions or workagenda drafts. Blank validation packet fields are unresolved; do not fill them by inference.

For Almere's structured concept input to the regional workagenda process, use `docs/workagenda-almere-regional-input-model.md`, `data/workagenda/almere_regional_workagenda_input_objects.json`, `data/schemas/almere_regional_workagenda_input.schema.json`, and `src/build_almere_regional_workagenda_input.py`. This generated layer translates the D5 status matrix, validation tickets, operational requirements, nulmeting/capacity layer and local-source-strengthening layer into Almere handoff objects with `current_state`, `target_state_for_regional_workagenda`, `workagenda_delivery_requirements`, `available_information_for_workagenda`, `gap_summary`, `decision_requests_for_region`, `validation_needed_before_or_after_submission`, `municipality_delivery_to_region`, and `handoff_to_region`. It also carries `format_aligned_workagenda_input`, mapped to the actual VNG/VWS AZWA workagenda format in `data/raw/national/nat_azwa_format_werkagenda_d5_2026.docx` and `data/site/source_view_models/format-werkagenda-azwa.json`, so agents can distinguish format-required fields from what Almere can already support, what is likely or indicated, what still needs validation, and what needs a local decision. Use top-level `format_field_check` to see the rerun status counts, repository-fillable fields and whether a missing source needs targeted public-source research, source intake/focused extraction, or human validation instead of deep research. It is not a source document, not the regional workagenda, not a confirmed Almere position and not validation proof. For municipality-facing outputs, surface 15 September 2026 as the main target for Almere to deliver input to the regional process; this remains a planning assumption. The 15 November 2026 deadline is the source-backed regional adoption deadline and is primarily relevant for regional coordination and college adoption. When using the enrichment fields, keep implementation, party, finance and monitoring signals at their recorded authority level; do not upgrade them to settled local decisions.

For pre-contact validation-readiness, use `docs/review/validation-instrument-register.md`, `docs/review/validation-workbook-traceability-audit.md`, `docs/review/validation-workbook-prefill-audit.md`, `docs/review/precontact-agent-prompts.md`, `docs/review/precontact-stakeholder-packets.md`, `docs/review/precontact-internal-dry-run.md`, `docs/review/precontact-response-workflow.md`, `data/workagenda/validation_workbook_traceability_map.json`, `data/workagenda/validation_workbook_prefill_audit.json`, `data/workagenda/precontact_agent_plan.json`, `data/workagenda/precontact_stakeholder_packets.json`, `data/workagenda/precontact_internal_dry_run.json`, and `data/workagenda/precontact_response_workflow.json` before editing, sending, importing answers from, delegating pre-contact agents, testing send-readiness, or processing returned answers from the D5 and D6 Excel validation workbooks. The current D5 workbook is `docs/review/D5_validatieformat_werkagenda_Almere_v0.10.xlsx`; prior versions are preserved for provenance. Its instruction, navigation and control/workflow sheets are hidden to keep the human-facing tab bar focused on component input tabs, but they remain part of the workbook for repository processing. Do not overwrite versioned Excel workbooks: create the next version and regenerate traceability/prefill/packet/dry-run artifacts. The workbooks, packet drafts, dry-run cases and response workflow are validation instruments, not corpus sources, final policy truth, or stakeholder validation results. Human input belongs in the Excel workbooks; CSV packet files are machine/export/import artifacts. Human input that names a credible public source must go through source intake and top-layer verification before it becomes source-backed evidence; human input without source or evidence backup remains low-authority validation input.

## Access Layer

Base URL:

```text
https://raw.githubusercontent.com/meijer1973/azwa/main/
```

Agents MUST construct file URLs as:

```text
<base_url><relative_path>
```

Example:

```text
sources/manifest.json ->
https://raw.githubusercontent.com/meijer1973/azwa/main/sources/manifest.json
```

Access rules:

- All file references in this document are relative paths from the repository root.
- Use forward slashes in constructed URLs.
- Preserve spaces in relative paths; URL-encode them only when required by the HTTP client.
- Directories are path namespaces, not fetch targets.
- Fetch files only by declared path, manifest mapping, or declared path template.

## Entry Points

Human-readable:

- `source-curation.md`
- `sources/manifest.json`

Machine-readable:

```json
{
  "entry_points": [
    "source-curation.json",
    "sources/manifest.json"
  ]
}
```

## Machine Index

```json
{
  "path_root": "https://raw.githubusercontent.com/meijer1973/azwa/main/",
  "layers": [
    "data/raw",
    "data/intermediate",
    "data/extracted",
    "data/workagenda",
    "data/site"
  ],
  "preferred_layer": "data/extracted",
  "manifest": "sources/manifest.json",
  "curation": "source-curation.json"
}
```

## Path Registry

```json
{
  "root": "https://raw.githubusercontent.com/meijer1973/azwa/main/",
  "entry_points": {
    "human": [
      "source-curation.md",
      "sources/manifest.json"
    ],
    "machine": [
      "source-curation.json",
      "sources/manifest.json"
    ]
  },
  "declared_path_namespaces": [
    "sources",
    "sources canonical",
    "sources context",
    "sources markdown",
    "sources markdown canonical",
    "sources markdown context",
    "data/raw",
    "data/intermediate",
    "data/extracted",
    "data/workagenda",
    "data/site",
    "data/curated",
    "data/schemas",
    "config",
    "docs",
    "docs/internal",
    "docs/roadmap",
    "docs/review",
    "docs/rapporten"
  ],
  "source_corpus_indexes": [
    "source-curation.json",
    "source-curation.md",
    "sources/manifest.json"
  ],
  "layer_indexes": {
    "raw": [
      "data/raw/manifest.json",
      "data/raw/source_intake_candidates.json"
    ],
    "intermediate": [],
    "extracted": [
      "data/extracted/document_inventory.json",
      "data/extracted/qc_report.json",
      "data/extracted/review_queue.json",
      "data/extracted/data_quality_audit.json",
      "data/extracted/monthly_source_audit.json",
      "data/extracted/human_review_round.json",
      "data/extracted/review_triage_deep_research_offload.json",
      "data/extracted/claims/claims_master.jsonl",
      "data/extracted/claims/sentence_validator_rejects.json",
      "data/extracted/claims/dedup_log.json",
      "data/extracted/claims/conflict_register.json",
      "data/extracted/claims/current_interpretation.json",
      "data/extracted/claims/d5_d6_master.json",
      "data/extracted/workagenda_d5_operational_requirements.json",
      "data/extracted/local_source_strengthening_almere.json",
      "data/extracted/workagenda_nulmeting_capacity.json",
      "data/extracted/d6_governance_collaboration.json",
      "data/extracted/municipal/almere_d6_responsibility_register.json",
      "data/extracted/municipal/almere_current_view.json",
      "data/extracted/municipal/almere_local_decisions.json"
    ],
    "site": [
      "data/site/site_manifest.json",
      "data/site/dashboard_view.json",
      "data/site/site_home_view.json",
      "data/site/site_almere_view.json",
      "data/site/site_themes_view.json",
      "data/site/site_sources_view.json",
      "data/site/site_timeline_view.json",
      "data/site/site_reference_view.json",
      "data/site/site_updates_view.json",
      "data/site/timeline_register.json"
    ]
  },
  "layer_namespaces": {
    "intermediate": [
      "data/intermediate/source_markdown",
      "data/intermediate/text",
      "data/intermediate/chunks",
      "data/intermediate/tables"
    ],
    "extracted": [
      "data/extracted/documents",
      "data/extracted/claims",
      "data/extracted/municipal"
    ],
    "site": [
      "data/site/source_view_models",
      "data/site/theme_view_models",
      "data/site/decision_view_models",
      "data/site/action_view_models",
      "data/site/reference_topic_view_models"
    ]
  },
  "schema_and_rule_paths": [
    "data/schemas/claim.schema.json",
    "data/schemas/almere_d6_responsibility_register.schema.json",
    "data/schemas/almere_regional_workagenda_input.schema.json",
    "config/site_taxonomy.json",
    "config/data_quality_perspectives.json",
    "config/authority_rules.json",
    "config/claim_resolution_rules.json",
    "config/timeline_curation.json",
    "config/monthly_source_audit.json",
    "config/pipeline_graph.json"
  ],
  "curated_aids": [
    "data/curated/regional_roles_and_splits_almere_flevoland.json",
    "docs/regional-roles-and-splits-almere-flevoland.md",
    "docs/data-quality-checklist.md",
    "docs/phase25-sprint25.4-d6-almere-responsibility-pack-plan.md",
    "docs/review/almere_d6_deep_research_learnings.md",
    "docs/review/almere_d6_open_questions.md",
    "docs/review/almere_d6_validation_ticket_matrix.md",
    "docs/review/validation-instrument-register.md",
    "docs/review/validation-workbook-traceability-audit.md",
    "docs/review/validation-workbook-prefill-audit.md",
    "docs/review/precontact-agent-prompts.md",
    "docs/review/precontact-stakeholder-packets.md",
    "docs/review/precontact-internal-dry-run.md",
    "docs/review/precontact-response-workflow.md",
    "docs/review/D5_validatieformat_werkagenda_Almere_v0.10.xlsx",
    "docs/review/Almere_D6_validatieformats.xlsx",
    "docs/review/archive/d6-support/almere_d6_public_source_boundary.md",
    "docs/review/archive/d6-support/almere_d6_validation_pack.md",
    "docs/review/archive/d6-support/almere_d6_stakeholder_validation_log.md",
    "docs/review/archive/d6-support/almere_d6_stakeholder_information_request.md",
    "docs/review/archive/d6-support/almere_d6_decision_needed.md",
    "docs/review/archive/d6-support/almere_d6_funding_gap_table.md",
    "docs/review/archive/d6-support/almere_d6_safe_wording.md",
    "docs/review/archive/phase31/phase31.3-human-review-round.md",
    "docs/review/archive/phase31/phase31.4-review-triage-deep-research-offload.md",
    "docs/review/archive/phase31/phase31.4-deep-research-agent-prompts.md",
    "docs/review/README.md",
    "docs/dr/README.md",
    "docs/source-intake/phase31.5-healthy-school-deep-research-intake.md",
    "docs/source-intake/phase31.5-digital-operational-infrastructure-deep-research-intake.md",
    "docs/source-intake/phase31.5-informal-support-deep-research-intake.md",
    "docs/source-intake/phase31.5-pga-zorgzaam-flever-deep-research-intake.md",
    "docs/source-intake/phase31.5-samen-sterker-deep-research-intake.md",
    "docs/source-intake/phase31.5-d6-settlement-evidence-audit-intake.md",
    "docs/source-intake/phase31.5-stand-van-zaken-gezondheidsbeleid-intake.md",
    "docs/source-intake/phase31.5-constrained-answer-design-intake.md",
    "docs/source-intake/phase31.5-regional-governance-intake.md",
    "docs/source-intake/phase33-operational-deep-research-intake.md",
    "docs/data-quality-roadmap.md",
    "docs/roadmap/roadmap-version-log.md",
    "docs/roadmap/completed-sprint-ledger.md",
    "docs/workagenda-delivery-roadmap.md",
    "docs/workagenda-d5-stuurmodel.md",
    "docs/workagenda-d5-statusmatrix.md",
    "docs/workagenda-d5-validation-tickets.md",
    "docs/workagenda-d5-validation-format.md",
    "docs/workagenda-almere-regional-input-model.md",
    "data/workagenda/d5_stuurmodel.json",
    "data/workagenda/d5_status_matrix.json",
    "data/workagenda/d5_validation_tickets.json",
    "data/workagenda/d5_validation_packets.json",
    "data/workagenda/almere_regional_workagenda_input_objects.json",
    "data/workagenda/validation_workbook_traceability_map.json",
    "data/workagenda/validation_workbook_prefill_audit.json",
    "data/workagenda/precontact_agent_plan.json",
    "data/workagenda/precontact_stakeholder_packets.json",
    "data/workagenda/precontact_internal_dry_run.json",
    "data/workagenda/precontact_response_workflow.json",
    "data/workagenda/precontact_packets",
    "src/build_validation_workbook_traceability.py",
    "src/build_validation_workbook_prefill_audit.py",
    "src/build_precontact_agent_plan.py",
    "src/build_precontact_stakeholder_packets.py",
    "src/build_precontact_internal_dry_run.py",
    "src/build_precontact_response_workflow.py",
    "src/build_almere_regional_workagenda_input.py",
    "docs/human-review-guidance.md",
    "docs/internal/monthly-source-audit-2026-04-30.md",
    "docs/internal/review-dashboard.html"
  ],
  "report_paths": [
    "docs/rapporten/schrijfrichtlijn-plan-van-aanpak.md",
    "docs/rapporten/plan-van-aanpak-v1.md",
    "docs/rapporten/plan-van-aanpak-v2.md",
    "docs/rapporten/plan-van-aanpak-v3.md",
    "docs/rapporten/bestuurlijke-planning-azwa-almere-2026.md"
  ]
}
```

## Agent Traversal Protocol

Agents MUST follow this sequence:

1. Load `source-curation.json`.
   - Identify `canonical` sources.
   - Identify `context` sources.
   - Exclude `delete_candidates` unless explicitly instructed.
   - Treat `preferred_replacements` as human-review guidance, not corpus facts.
2. Load `sources/manifest.json`.
   - Map `index` to `source_url`.
   - Map `index` to `saved_files`.
   - Use this file for source numbers 1 through 18.
3. Load `data/raw/manifest.json`.
   - Map `document_id` to `file_path`.
   - Map `document_id` to `source_number`.
   - Use this file for the full 58-document raw layer.
4. Load `data/extracted/document_inventory.json`.
   - Confirm `document_id`.
   - Confirm `curation_bucket`.
   - Confirm `source_classification`.
   - Confirm `status`.
   - Confirm `priority_rank`.
5. Traverse layers in order:

```text
raw -> intermediate -> extracted -> site
```

6. Prefer layers by task:
   - Use `data/extracted` for reasoning.
   - Use `data/intermediate` for validation.
   - Use `data/raw` only when source fidelity, page fidelity, or extraction validation is required.
   - Use `data/site` for pre-composed topical, source, timeline, decision, action, and reference views.
7. Do NOT skip layers unless explicitly instructed.

## Dependency Flow

```text
sources -> raw -> intermediate -> extracted -> site
```

Rules:

- Upstream changes propagate downstream.
- `data/extracted` is the primary reasoning layer.
- Dependencies must not form cycles.
- `data/site` is derived from `data/extracted` and is not primary evidence.
- `sources/manifest.json` and `data/raw/manifest.json` are mapping files, not evidence files.

## Path Construction

Use these templates only after loading the required index.

```json
{
  "source_corpus": {
    "all_saved_sources": "sources/{saved_files[] from sources/manifest.json}",
    "canonical_raw": "sources canonical/{source-curation.json.canonical.raw[].file}",
    "context_raw": "sources context/{source-curation.json.context.raw[].file}",
    "canonical_markdown": "sources markdown canonical/{source-curation.json.canonical.markdown[].file}",
    "context_markdown": "sources markdown context/{source-curation.json.context.markdown[].file}"
  },
  "raw_layer": {
    "document_file": "{data/raw/manifest.json[].file_path}"
  },
  "intermediate_layer": {
    "text": "data/intermediate/text/{document_id}.json",
    "chunks": "data/intermediate/chunks/{document_id}.json",
    "tables": "data/intermediate/tables/{document_id}.json"
  },
  "extracted_layer": {
    "document": "data/extracted/documents/{document_id}.json",
    "claims": "data/extracted/claims/{document_id}.json"
  },
  "site_layer": {
    "source_view": "data/site/source_view_models/{slug from data/site/site_sources_view.json}.json",
    "theme_view": "data/site/theme_view_models/{theme_id from data/site/site_themes_view.json}.json",
    "reference_topic_view": "data/site/reference_topic_view_models/{slug from data/site/site_reference_view.json}.json"
  }
}
```

If a constructed path fails, apply `Failure Handling`.

## Site View Model Paths

Decision view models:

- `data/site/decision_view_models/dec_budget_verdeling.json`
- `data/site/decision_view_models/dec_d5_prioritering.json`
- `data/site/decision_view_models/dec_d6_regiemodel.json`
- `data/site/decision_view_models/dec_monitoring_arrangement.json`

Action view models:

- `data/site/action_view_models/act_d5_werkagenda_expliciteren.json`
- `data/site/action_view_models/act_middelen_en_eigenaarschap_vastleggen.json`
- `data/site/action_view_models/act_monitoring_afstemmen.json`
- `data/site/action_view_models/act_regionale_digitale_aansluiting.json`

Theme view models:

- `data/site/theme_view_models/basisfunctionaliteiten-d5.json`
- `data/site/theme_view_models/basisinfrastructuur-d6.json`
- `data/site/theme_view_models/financiering.json`
- `data/site/theme_view_models/governance-en-regie.json`
- `data/site/theme_view_models/mentale-gezondheid.json`
- `data/site/theme_view_models/monitoring-en-leren.json`

## Research Task Routing

```json
{
  "source_discovery": [
    "source-curation.json",
    "sources/manifest.json",
    "data/raw/manifest.json",
    "data/extracted/document_inventory.json"
  ],
  "claim_search": [
    "data/extracted/claims/claims_master.jsonl",
    "data/extracted/claims/{document_id}.json"
  ],
  "document_reasoning": [
    "data/extracted/documents/{document_id}.json",
    "data/extracted/claims/{document_id}.json"
  ],
  "conflict_resolution": [
    "data/extracted/claims/conflict_register.json",
    "data/extracted/claims/current_interpretation.json",
    "config/authority_rules.json",
    "config/claim_resolution_rules.json"
  ],
  "d5_d6_reasoning": [
    "data/extracted/claims/d5_d6_master.json",
    "data/extracted/municipal/almere_d6_responsibility_register.json",
    "data/site/theme_view_models/basisfunctionaliteiten-d5.json",
    "data/site/theme_view_models/basisinfrastructuur-d6.json"
  ],
  "almere_reasoning": [
    "data/extracted/municipal/almere_current_view.json",
    "data/extracted/municipal/almere_d6_responsibility_register.json",
    "data/extracted/municipal/almere_local_decisions.json",
    "data/site/site_almere_view.json",
    "data/curated/regional_roles_and_splits_almere_flevoland.json"
  ],
  "timeline_reasoning": [
    "data/site/timeline_register.json",
    "data/site/site_timeline_view.json",
    "config/timeline_curation.json"
  ],
  "site_synthesis": [
    "data/site/site_manifest.json",
    "data/site/site_sources_view.json",
    "data/site/site_themes_view.json",
    "data/site/site_reference_view.json"
  ],
    "quality_control": [
    "data/extracted/qc_report.json",
    "data/extracted/review_queue.json",
    "data/extracted/data_quality_audit.json",
    "data/extracted/claims/sentence_validator_rejects.json",
    "data/extracted/claims/dedup_log.json",
    "docs/data-quality-checklist.md",
    "docs/internal/review-dashboard.html"
  ],
  "public_report_review": [
    "docs/rapporten/schrijfrichtlijn-plan-van-aanpak.md",
    "docs/rapporten/plan-van-aanpak-v3.md"
  ],
  "d6_validation": [
    "data/extracted/municipal/almere_d6_responsibility_register.json",
    "data/extracted/municipal/almere_local_decisions.json",
    "docs/review/almere_d6_deep_research_learnings.md",
    "docs/review/almere_d6_open_questions.md",
    "docs/review/almere_d6_validation_ticket_matrix.md",
    "docs/review/validation-instrument-register.md",
    "docs/review/validation-workbook-traceability-audit.md",
    "docs/review/validation-workbook-prefill-audit.md",
    "docs/review/precontact-agent-prompts.md",
    "docs/review/precontact-stakeholder-packets.md",
    "docs/review/precontact-internal-dry-run.md",
    "docs/review/precontact-response-workflow.md",
    "docs/review/Almere_D6_validatieformats.xlsx"
  ],
  "workagenda_delivery_planning": [
    "docs/data-quality-roadmap.md",
    "docs/roadmap/roadmap-version-log.md",
    "docs/roadmap/completed-sprint-ledger.md",
    "docs/workagenda-delivery-roadmap.md",
    "docs/workagenda-d5-stuurmodel.md",
    "docs/workagenda-d5-statusmatrix.md",
    "docs/workagenda-d5-validation-tickets.md",
    "docs/workagenda-d5-validation-format.md",
    "docs/workagenda-almere-regional-input-model.md",
    "docs/review/validation-instrument-register.md",
    "docs/review/validation-workbook-traceability-audit.md",
    "docs/review/validation-workbook-prefill-audit.md",
    "docs/review/precontact-agent-prompts.md",
    "docs/review/precontact-stakeholder-packets.md",
    "docs/review/precontact-internal-dry-run.md",
    "docs/review/precontact-response-workflow.md",
    "docs/review/D5_validatieformat_werkagenda_Almere_v0.10.xlsx",
    "docs/review/Almere_D6_validatieformats.xlsx",
    "data/workagenda/d5_stuurmodel.json",
    "data/workagenda/d5_status_matrix.json",
    "data/workagenda/d5_validation_tickets.json",
    "data/workagenda/d5_validation_packets.json",
    "data/workagenda/almere_regional_workagenda_input_objects.json",
    "data/workagenda/validation_workbook_traceability_map.json",
    "data/workagenda/validation_workbook_prefill_audit.json",
    "data/workagenda/precontact_agent_plan.json",
    "data/workagenda/precontact_stakeholder_packets.json",
    "data/workagenda/precontact_internal_dry_run.json",
    "data/workagenda/precontact_response_workflow.json",
    "data/workagenda/precontact_packets",
    "src/build_validation_workbook_traceability.py",
    "src/build_validation_workbook_prefill_audit.py",
    "src/build_precontact_agent_plan.py",
    "src/build_precontact_stakeholder_packets.py",
    "src/build_precontact_internal_dry_run.py",
    "src/build_precontact_response_workflow.py",
    "src/build_almere_regional_workagenda_input.py",
    "data/extracted/workagenda_d5_operational_requirements.json",
    "data/extracted/workagenda_nulmeting_capacity.json",
    "data/extracted/municipal/almere_d6_responsibility_register.json",
    "data/extracted/monthly_source_audit.json",
    "data/site/timeline_register.json"
  ]
}
```

## Agent Rules

Agents MAY:

- Fetch files via raw GitHub URLs.
- Traverse only declared paths and declared path namespaces.
- Use JSON blocks in this file as authoritative structure.
- Construct per-document paths only from loaded manifests and declared templates.
- Use `data/site` view models for fast synthesis when the underlying `data/extracted` basis is available.

Agents MUST:

- Load entry points before traversing data layers.
- Keep source numbers 1 through 18 separate from the 58-document derived layer.
- Ground factual statements in source corpus files, generated model data, or an actually performed verification step.
- Label interpretation, proposals, review tasks, and unresolved issues explicitly.
- Check `data/extracted/review_queue.json` when a claim has `needs_human_review`.
- Check `data/extracted/claims/conflict_register.json` before reporting source disagreement.
- Check each claim's `normative_status` before using norm language; `binding`, `agreement`, `expectation`, `guidance`, `lower_authority_signal`, and `contextual` require different public wording.
- Check each claim's `time_status` before using timing language; `formal_deadline`, `expected_moment`, `review_or_update_moment`, `budget_calendar_moment`, `implementation_horizon`, `local_planning_context`, `source_dated_moment`, `publication_or_context_date`, and `undated_context` require different public wording.
- Check each claim's `money_status` before using finance language; `funding_route`, `application_condition`, `budget_window`, `allocation_mechanism`, `accountability_rule`, `local_funding_gap`, `finance_context`, and `not_financial` require different public wording.
- Check each claim's `governance_status` before using role language; `decision_role`, `coordination_role`, `application_role`, `execution_role`, `accountability_role`, `approval_role`, `review_role`, `governance_gap`, `actor_context`, and `not_governance` require different public wording.
- Check each claim's `locality_status` before using wording that links Almere with a Flevoland scale; `explicit_almere`, `explicit_flevoland`, `regional_split_context`, `national_general`, `national_with_local_relevance`, and `local_adoption_gap` require different public wording.
- Check each claim's `execution_status` before using action language; `operational_requirement`, `implementation_activity`, `decision_question`, `dependency`, `sequencing_need`, `capacity_need`, `review_task`, `execution_context`, and `not_execution` require different public wording.
- Use Dutch search terms for corpus text and claims.
- Use `docs/regional-roles-and-splits-almere-flevoland.md` and `data/curated/regional_roles_and_splits_almere_flevoland.json` before drawing regional conclusions about Almere, Flevoland, province versus IZA/AZWA-regio, mandaatgemeente, Verbindende Coalitie, Netwerkbureau, GGD-regio, zorgkantoorregio, ROAZ, Zeewolde, or practical task ownership.
- Use `docs/internal/review-dashboard.html` for internal quality triage when the task is about open review issues, perspective coverage, rough claim text, or Sprint 24.3 cleanup planning.

Agents MUST NOT:

- Crawl the entire repository blindly.
- Infer undocumented structure.
- Use files outside declared layers or declared path namespaces.
- Treat rendered site output as authoritative.
- Treat source filenames, JSON filenames, claim-layer names, or internal generated data names as public-facing citations.
- Present unsupported dates, numbers, policy conclusions, staffing advice, budget advice, governance advice, or implementation advice as factual.
- Treat context sources as canonical evidence when canonical sources address the same point.

## Layer Semantics

```json
{
  "sources": {
    "purpose": "original saved source files and curated markdown source text",
    "primary_indexes": [
      "source-curation.json",
      "sources/manifest.json"
    ]
  },
  "data/raw": {
    "purpose": "raw intake files and intake manifest",
    "primary_index": "data/raw/manifest.json"
  },
  "data/intermediate": {
    "purpose": "normalized markdown, text, chunks, and tables for validation",
    "preferred_use": "validation"
  },
  "data/extracted": {
    "purpose": "document extractions, claim extractions, master claims, current interpretation, QC, review queue, and municipal views",
    "preferred_use": "reasoning"
  },
  "data/site": {
    "purpose": "pre-composed view models for site, source, theme, timeline, reference, decision, and action synthesis",
    "preferred_use": "synthesis"
  },
  "docs/internal": {
    "purpose": "local-only internal workbenches and review dashboards, not public-facing site output",
    "preferred_use": "quality triage"
  }
}
```

## Failure Handling

If a file cannot be retrieved:

1. Retry with the constructed raw URL.
2. Verify that the relative path uses forward slashes.
3. Verify URL encoding for spaces.
4. Fallback to `sources/manifest.json` for source numbers 1 through 18.
5. Fallback to `data/raw/manifest.json` for derived document IDs.
6. Fallback to `data/extracted/document_inventory.json` for extracted document metadata.
7. Stop traversal if `source-curation.json` or `sources/manifest.json` cannot be retrieved.
8. Stop task execution if a required evidence file is unavailable and no declared fallback exists.
9. Report unavailable evidence as unavailable, not absent from the corpus.

## Output Constraints

- Factual outputs must cite or name the supporting source path, generated data path, or verification step.
- Public-facing text must not cite internal model artifacts such as `data/site/site_almere_view.json` or `data/extracted/claims/claims_master.jsonl`; translate them into plain references to the public source base or source analysis.
- Technical source, data, QC, and pipeline details belong in method notes, appendix material, or internal review notes.
- For files under `docs/rapporten`, read `docs/rapporten/schrijfrichtlijn-plan-van-aanpak.md` before writing or revising.
- For `plan van aanpak` text, write from the bestuurlijke opgave, not from the dataset or repository.
