# Phase 7 and Phase 8

Phase 7 and Phase 8 generate the first downstream policy views from the interpretation layer.

## Outputs

- `data/extracted/claims/d5_d6_master.json`
- `data/extracted/municipal/almere_current_view.json`
- `data/extracted/municipal/almere_local_decisions.json`
- `src/build_master_views.py`

## Design notes

- `d5_d6_master.json` is generated from the interpreted claim graph and keeps unresolved items visible instead of flattening them away.
- `almere_current_view.json` is computed only: it lists applicable items, gaps, dependencies, uncertainty, obsolete material, and political-choice points for Almere.
- `almere_local_decisions.json` is reserved for human-entered local choices. The generator creates it only if it does not already exist.
- The municipal view surfaces local gaps by comparing national and regional requirements with the current Almere-specific claim set rather than by inventing local commitments.
