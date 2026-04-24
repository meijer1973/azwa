# Phase 4

Phase 4 adds an append-only claim layer for the top five documents.

## Outputs

- `data/extracted/claims/{document_id}.json`
- `data/extracted/claims/claims_master.jsonl`
- `data/schemas/claim.schema.json`
- `config/authority_rules.json`
- `config/claim_resolution_rules.json`
- `src/build_claims_top5.py`

## Design notes

- Claims remain append-only.
- Direct national D5/D6 statements are kept separate from contextual regional and municipal implementation signals.
- Contextual claims are still useful, but they should not be treated as higher-authority norm-setting text.
- Claim relations are explicit and never imply silent deletion of older claims.
- Claim IDs are stable per extracted source statement so later conflict logic can reference them without rekeying.
- The first-pass relation map is intentionally small and conservative: it only links obvious supersession, clarification, implementation, and dependency paths.
