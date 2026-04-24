# AZWA Corpus

This repository contains the AZWA / D5-D6 source corpus and the working materials for building a structured extraction pipeline.

## Repository Layout

- `data/raw/`: Phase 0 corpus used by the pipeline, organized into `national`, `regional`, and `municipal`
- `data/intermediate/`: structural extraction outputs such as text, chunks, and tables
- `data/extracted/`: document JSON, claim outputs, municipality views, QC report, and review queue
- `data/site/`: derived site view models for the public executive publication layer
- `data/schemas/`: JSON schema and validation assets
- `data/logs/`: run logs and extraction diagnostics
- `config/`: authority rules, pipeline settings, and resolution logic
- `prompts/`: reusable LLM extraction and review prompts
- `src/`: pipeline scripts and application code
- `templates/`: HTML templates for the static site renderer
- `assets/`: CSS and JavaScript assets for the public site
- `dist/`: generated static site output for local preview and GitHub Pages deployment
- `tests/`: automated checks
- `docs/`: active process notes and implementation documentation
- `docs/completed-plans/`: completed phase and sprint plans kept out of the active docs root

## Source Collections

- `sources/`: original downloaded files plus earlier working copies
- `sources markdown/`: Markdown conversions of the original files
- `sources canonical/`: curated raw files recommended as the primary evidence set
- `sources markdown canonical/`: curated Markdown files for reading and comparison
- `sources context/`: supporting context files that are useful for interpretation but weaker as primary evidence
- `sources markdown context/`: Markdown versions of the context set

## Phase 0 Decisions

- `data/raw/manifest.json` is the canonical inventory for the pipeline
- each numbered source item is represented by one selected raw file in `data/raw/...`
- raw PDF or HTML files are authoritative for extraction; Markdown is a convenience layer, not the sole evidence base
- the original `sources*` folders are preserved and not rewritten by the pipeline

## Curation Artifacts

- `source-curation.md`: human-readable recommendation for canonical vs context material
- `source-curation.json`: machine-readable version of the curation decision
- `docs/completed-plans/phase0.md`: Phase 0 repository setup and corpus assumptions

## Working Principle

The repository is being prepared for a three-layer architecture:

1. source-faithful document extraction
2. append-only normalized claims
3. computed municipality views, including Almere

## Pipeline Usage

- list stages: `python src/run_pipeline.py --list`
- evaluate the current end-to-end implemented path: `python src/run_pipeline.py --all`
- render the current public site and its prerequisites: `python src/run_pipeline.py --stage phase13_site_render`
- evaluate one stage plus prerequisites: `python src/run_pipeline.py --stage phase4_claims_all_docs`
- evaluate one stage and downstream stages: `python src/run_pipeline.py --from-stage phase6_current_interpretation`
- preview without running scripts: `python src/run_pipeline.py --all --dry-run`

Pipeline runs are logged under `data/logs/pipeline_runs/`.

The current default pipeline target is the static public-site render layer, which writes:

- `data/site/...`
- `dist/...`

The QC outputs remain available upstream in:

- `data/extracted/qc_report.json`
- `data/extracted/review_queue.json`

## Prompt Assets

The reusable extraction and reasoning prompts live in `prompts/`:

- `extract_document.md`
- `extract_table.md`
- `extract_claims.md`
- `resolve_conflicts.md`
- `build_municipal_view.md`

## Public Site Layer

The repository now includes a machine-generated Dutch executive site for Almere:

- derived view models are written to `data/site/`
- the static renderer writes HTML, assets, and `search-index.json` to `dist/`
- the public wording around besluitvragen and opvolgacties is deliberately careful: these are possible follow-up items based on the current public source base, unless the source base itself shows a settled agreement

GitHub Pages deployment is handled through `.github/workflows/deploy-pages.yml`.
