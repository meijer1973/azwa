# AZWA Corpus

This repository contains the AZWA / D5-D6 source corpus and the working materials for building a structured extraction pipeline.

## Repository Layout

- `data/raw/`: Phase 0 corpus used by the pipeline, organized into `national`, `regional`, and `municipal`
- `data/intermediate/`: structural extraction outputs such as text, chunks, and tables
- `data/extracted/`: document JSON, claim outputs, and municipality views
- `data/schemas/`: JSON schema and validation assets
- `data/logs/`: run logs and extraction diagnostics
- `config/`: authority rules, pipeline settings, and resolution logic
- `prompts/`: reusable LLM extraction and review prompts
- `src/`: pipeline scripts and application code
- `tests/`: automated checks
- `docs/`: process notes and implementation documentation

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
- `docs/phase0.md`: Phase 0 repository setup and corpus assumptions

## Working Principle

The repository is being prepared for a three-layer architecture:

1. source-faithful document extraction
2. append-only normalized claims
3. computed municipality views, including Almere
