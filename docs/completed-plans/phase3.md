# Phase 3

Phase 3 adds immutable per-document extraction JSON for the top five priority documents.

## Scope

The current extraction set covers:

1. `nat_azwa_2025_definitief`
2. `nat_azwa_2025_onderhandelaarsakkoord`
3. `nat_azwa_2026_cw31_kader_d5_d6`
4. `reg_flevoland_2023_regioplan_iza`
5. `mun_almere_pga_transformatieplan`

## Output shape

Each file in `data/extracted/documents/` contains:

- metadata
- extraction scope
- document-level summary
- structured content for `d5`, `d6`, `governance_and_finance`, `timeline_and_status`, `monitoring_and_evaluation`, and `municipal_translation`
- evidence excerpts with page and section references

## Direct vs contextual

Two statement types are used:

- `direct_extraction`: the source explicitly states the substance being extracted
- `contextual_relevance`: the source does not explicitly use D5/D6 language, but the passage is still relevant as regional or municipal implementation context

This distinction is especially important for:

- `reg_flevoland_2023_regioplan_iza`
- `mun_almere_pga_transformatieplan`

These documents are useful for downstream municipality reasoning, but they should not be mistaken for explicit national D5/D6 norm-setting sources.
