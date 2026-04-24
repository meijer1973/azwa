# Research Agent Map

Agent-executable navigation and access specification for the AZWA / IZA / GALA corpus and derived data layers.

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
    "data/site",
    "data/curated",
    "data/schemas",
    "config",
    "docs",
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
      "data/extracted/claims/claims_master.jsonl",
      "data/extracted/claims/conflict_register.json",
      "data/extracted/claims/current_interpretation.json",
      "data/extracted/claims/d5_d6_master.json",
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
    "config/site_taxonomy.json",
    "config/data_quality_perspectives.json",
    "config/authority_rules.json",
    "config/claim_resolution_rules.json",
    "config/timeline_curation.json",
    "config/pipeline_graph.json"
  ],
  "curated_aids": [
    "data/curated/regional_roles_and_splits_almere_flevoland.json",
    "docs/regional-roles-and-splits-almere-flevoland.md",
    "docs/data-quality-checklist.md",
    "docs/human-review-guidance.md"
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
   - Use this file for the full 33-document raw layer.
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
- `data/site/action_view_models/act_d6_lokale_structuur_verduidelijken.json`
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
    "data/site/theme_view_models/basisfunctionaliteiten-d5.json",
    "data/site/theme_view_models/basisinfrastructuur-d6.json"
  ],
  "almere_reasoning": [
    "data/extracted/municipal/almere_current_view.json",
    "data/extracted/municipal/almere_local_decisions.json",
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
    "docs/data-quality-checklist.md"
  ],
  "public_report_review": [
    "docs/rapporten/schrijfrichtlijn-plan-van-aanpak.md",
    "docs/rapporten/plan-van-aanpak-v3.md"
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
- Keep source numbers 1 through 18 separate from the 33-document derived layer.
- Ground factual statements in source corpus files, generated model data, or an actually performed verification step.
- Label interpretation, proposals, review tasks, and unresolved issues explicitly.
- Check `data/extracted/review_queue.json` when a claim has `needs_human_review`.
- Check `data/extracted/claims/conflict_register.json` before reporting source disagreement.
- Use Dutch search terms for corpus text and claims.
- Use `docs/regional-roles-and-splits-almere-flevoland.md` and `data/curated/regional_roles_and_splits_almere_flevoland.json` before drawing regional conclusions about Almere, Flevoland, mandaatgemeente, GGD-regio, zorgkantoorregio, ROAZ, Zeewolde, or practical task ownership.

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
