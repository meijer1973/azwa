# Phase 9 and Phase 10

Phase 9 and Phase 10 make the repo operational as a repeatable extraction workflow.

## Outputs

- `prompts/extract_document.md`
- `prompts/extract_table.md`
- `prompts/extract_claims.md`
- `prompts/resolve_conflicts.md`
- `prompts/build_municipal_view.md`
- `config/pipeline_graph.json`
- `src/run_pipeline.py`
- `tests/test_pipeline_graph.py`

## Design notes

- The prompt set is intentionally strict about JSON-only outputs, traceability, and uncertainty handling.
- The pipeline runner executes the currently implemented stages in dependency order and skips stages whose outputs are newer than their inputs and upstream outputs.
- Asset stages are verified rather than executed. This keeps prompt files and orchestration metadata inside the same stage registry without pretending they are generated.
- The current orchestration is stage-level incremental. It is ready for later document-level invalidation once more builders accept narrower input scopes.
