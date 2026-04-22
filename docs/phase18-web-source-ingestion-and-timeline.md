# Phase 18 — Web source ingestion and timeline enrichment

## What changed

This phase expands the AZWA repository with official web-native sources that matter for timing, funding, and local governance:

- `nat_dusi_spuk_transformatiemiddelen_2024_2028`
- `nat_wetten_spuk_transformatiemiddelen_regeling`
- `nat_zorgakkoorden_azwa_programmapagina_2025`
- `mun_almere_begroting_2026_webpagina`
- `nat_bzk_gemeentefonds_cyclus`

The structural extractor now supports a raw-HTML fallback, so new website sources no longer need a hand-made Markdown conversion before they can enter the formal pipeline.

## Why this matters

The timeline needed more than PDF publication moments. Important deadlines and local governance moments often live on official websites instead:

- SPUK aanvraagdeadline (`31 maart 2027`)
- jaarlijkse verantwoordingsdeadline (`15 juli` na het uitvoeringsjaar)
- Almere begrotingsaanbieding en -vaststelling
- gemeentefonds-cyclus (`mei`, `september`, `december`)

With this phase, these moments are now source-backed through the same `raw -> manifest -> extractie -> claims -> interpretatie -> site` chain as the rest of the repository.

## Implementation notes

- `src/build_structural_extractions.py`
  - added raw HTML parsing with section extraction
  - added generic navigation/footer filtering for web pages
- `src/build_document_extractions.py`
  - expanded keyword rules for web-native D6, funding, and timeline signals
- `config/timeline_curation.json`
  - added pipeline-backed timeline entries for:
    - Almere budget milestones
    - SPUK regulation source moment
    - SPUK application deadline
    - annual accountability deadline
    - expected meicirculaire moment based on the ingested gemeentefonds cycle page
- `data/raw/source_intake_candidates.json`
  - now distinguishes between ingested and still-pending candidate sources

## Current publication rule

The public timeline still only shows moments that are backed by ingested pipeline sources.
Expected or recurring moments can be shown, but only when the underlying cycle itself has first been ingested as a source and the public wording makes the expectation explicit.
