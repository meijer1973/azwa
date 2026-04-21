# Phase 0

Phase 0 establishes the repository structure and a stable raw corpus for the AZWA extraction pipeline.

## Scope

- create the project folders required by the implementation plan
- place one selected raw artifact per source item into `data/raw/...`
- generate `data/raw/manifest.json` with stable metadata
- preserve the legacy `sources*` folders as historical working material

## Corpus Rule

The pipeline uses raw source files as its authority layer:

- PDFs remain the preferred source when available
- HTML is used when no stronger downloaded artifact exists for that source item
- Markdown files are useful for reading and drafting, but not as the sole basis for page-sensitive or table-sensitive extraction

## Phase 0 Script

`src/phase0_setup.py` creates the directory structure, copies the selected source files into `data/raw/...`, and writes the manifest.

## Initial Priority Order

The top five documents for end-to-end pipeline work are:

1. `nat_azwa_2025_definitief`
2. `nat_azwa_2025_onderhandelaarsakkoord`
3. `nat_azwa_2026_cw31_kader_d5_d6`
4. `reg_flevoland_2023_regioplan_iza`
5. `mun_almere_pga_transformatieplan`
