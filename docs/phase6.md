# Phase 6

Phase 6 adds a computed interpretation layer on top of the append-only claims.

## Outputs

- `data/extracted/claims/conflict_register.json`
- `data/extracted/claims/current_interpretation.json`
- `src/build_current_interpretation.py`

## Design notes

- The engine never edits or deletes original claims.
- Historical and superseded claims stay visible in the interpretation outputs.
- The conflict register is conservative: it records clear precedence overlaps, explicit supersessions, and national-versus-local layering where review may still matter.
- Lower-authority regional and municipal claims can stay current as localization or implementation signals, but they do not override higher-authority national claims.
- Interpretation entries expose `historical_claim_ids` so topics with only preserved draft or legacy material do not disappear from view.
