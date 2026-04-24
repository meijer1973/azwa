# Phase 1 and Phase 2

This repository now has the first inventory and structural extraction baseline for the AZWA corpus.

## Phase 1

`data/extracted/document_inventory.json` is the normalized inventory for the 18 source items.

It adds:

- source classification: `primary`, `derivative`, or `supporting_commentary`
- curation bucket: `canonical` or `context`
- topic and extraction flags, including D5/D6, finance, governance, monitoring, and municipal relevance
- extraction priority labels derived from the stable `priority_rank`

## Phase 2

The structural extraction outputs live in:

- `data/intermediate/text/`
- `data/intermediate/chunks/`
- `data/intermediate/tables/`

The current extraction pass uses the repository's raw-derived Markdown conversions as the text substrate:

- PDF-derived Markdown is parsed into page-based text objects
- HTML-derived Markdown is parsed into section-based text objects
- chunks preserve `page_start` and `page_end` for PDFs
- HTML sources use section-based traceability because they do not have page numbers

## Known limitations

- table extraction is heuristic and should be treated as a first-pass aid, not a final truth layer
- some PDF tables remain partially linearized because the source conversion is text-first rather than layout-first
- the raw files in `data/raw/` remain authoritative for later evidence checks and claim review
