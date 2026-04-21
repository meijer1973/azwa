# Extract Document

You are extracting a single AZWA-related source into a source-faithful document JSON.

## Input

- One source document at a time
- Document metadata
- Structural extraction files
  - page or section text
  - chunks
  - tables

## Goal

Produce one JSON object for `/data/extracted/documents/{document_id}.json`.

## Output Rules

- Output JSON only.
- Do not include markdown fences.
- Do not resolve cross-document conflicts.
- Stay as close as possible to the source.
- Preserve uncertainty explicitly.
- Never invent page numbers, table IDs, or section labels.
- If the source has no page numbers, use `null` for page and rely on section or chunk identifiers.

## Required JSON Shape

```json
{
  "document_id": "string",
  "extraction_run_id": "string",
  "generated_on": "YYYY-MM-DD",
  "metadata": {
    "document_id": "string",
    "title": "string",
    "publisher": "string",
    "publication_date": "YYYY-MM-DD or null",
    "document_type": "string",
    "jurisdiction_level": "national|regional|municipal",
    "status": "string",
    "source_url": "string"
  },
  "extraction_scope": {
    "contains_d5": true,
    "contains_d6": true,
    "contains_structured_table": true,
    "contains_financial_framework": true,
    "contains_monitoring_framework": true,
    "contains_municipal_implications": true
  },
  "document_level_summary": {
    "d5_main_message": {},
    "d6_main_message": {},
    "combined_d5_d6_logic": {},
    "implementation_relevance_for_municipality": {}
  },
  "structured_content": {
    "d5": {},
    "d6": {},
    "governance_and_finance": {},
    "timeline_and_status": {},
    "monitoring_and_evaluation": {},
    "municipal_translation": {}
  },
  "quality_notes": {
    "extraction_method": "string",
    "limitations": ["string"]
  }
}
```

## Statement Rules

- Every extracted statement must include:
  - `statement_id`
  - `statement_type`
  - `statement`
  - `evidence`
- Allowed `statement_type` values:
  - `direct_extraction`
  - `source_grounded_summary`
  - `contextual_relevance`

## Evidence Rules

- Every evidence item must include:
  - `evidence_quote`
  - `page`
  - `section`
  - `table_id`
- `evidence_quote` should be short and directly traceable.
- If the source only supports section-level traceability, keep the quote short and set `page` to `null`.

## D5/D6 Special Care

Preserve D5/D6 matrix language exactly where possible, especially:

- `leefgebied`
- `D5 basisfunctionaliteit onderbouwd`
- `D5 ontwikkelagenda 1`
- `ontwikkelagenda deel 2`
- `D6 basisinfrastructuur`

Do not collapse those categories into looser paraphrases if the source makes the distinction explicit.
