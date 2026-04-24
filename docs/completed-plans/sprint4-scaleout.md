# Sprint 4 Scale-Out

This checkpoint expands the working extraction and claim chain from the original seed set to the full curated 18-document corpus.

## Outputs

- `data/extracted/documents/{document_id}.json` for all 18 curated documents
- `data/extracted/claims/{document_id}.json` for all 18 curated documents
- `data/extracted/claims/claims_master.jsonl`
- refreshed `data/extracted/claims/conflict_register.json`
- refreshed `data/extracted/claims/current_interpretation.json`
- refreshed `data/extracted/claims/d5_d6_master.json`
- refreshed `data/extracted/municipal/almere_current_view.json`

## Design notes

- The original top-5 document extractions remain manual curated overrides.
- The remaining documents use a conservative structural auto-extraction path over chunks and table candidates.
- Auto extraction is intentionally source-near and cautious. Weakly signaled items are more likely to be omitted or marked as contextual relevance than force-fit into strong claims.
- The claim layer now covers all 18 documents in inventory order, while keeping the explicit relation map only for the original high-confidence seed claims.
- National reference agreements such as IZA and GALA are preserved as historical or contextual layers instead of silently replacing current AZWA claims.
- FAQ and commentary-derived claims are retained with lower confidence and human-review flags so they can inform interpretation without posing as stronger norm-setting text.
