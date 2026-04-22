# Phase 20: VNG Hardening and Site Polish

## Scope

This milestone strengthens the VNG source layer, improves the repo's own intake path for new PDF sources, and removes the last visible fallback labels from the public site.

## What Changed

- Added two new VNG sources to the formal corpus:
  - `nat_vng_gezond_en_actief_leven_2026`
  - `nat_vng_ledenbrief_onderhandelaarsakkoord_azwa_2025`
- Added a repo-native PDF markdown intake directory:
  - `data/intermediate/source_markdown/`
- Updated `src/build_structural_extractions.py` so PDF markdown sidecars can live inside the repo rather than only in the legacy `sources markdown*` folders.

## Source Hardening

- The dead VNG topic URL remains recorded as `pending_replacement` in `data/raw/source_intake_candidates.json`.
- The active VNG subject page `Gezond en actief leven` now functions as the current replacement source for municipal IZA/GALA/AZWA support context.
- The public Q3 2026 regioplan timeline item now uses the stronger VNG members letter instead of the weaker Sociaal Werk Nederland commentary source.

## Site Polish

- Added missing Dutch topic labels for:
  - `d6.other`
  - `d6.regional_coordination`
- Added document type labels for:
  - `topic_page`
  - `members_letter`
- The public site no longer shows fallback titles like `D6 other` or `D6 regional coordination`.

## Timeline Change

The public timeline entry for the additional regioplan timing now reads as a VNG-led signal rather than a Sociaal Werk Nederland signal:

- old: Sociaal Werk Nederland based
- new: VNG members letter based

This keeps the item flagged for human review, but upgrades the source quality and municipal relevance.

## Verification

- `python src/run_pipeline.py --all`
- `python -m unittest discover -s tests -p "test_*.py"`

Additional test coverage now checks:

- the D6 fallback labels are gone from `site_manifest.json`
- the new VNG intake sources are present in source intake tracking

## Result

The local site build is cleaner, the VNG source layer is stronger, and the executive timeline uses a more credible municipal-facing source for the Q3 2026 regioplan milestone.
