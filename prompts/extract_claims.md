# Extract Claims

You are converting one document extraction JSON into append-only atomic claims.

## Input

- one `document` extraction JSON
- authority metadata for the document
- claim schema

## Goal

Produce JSON only with one claim per normative proposition or factual implementation assertion.

## Output Rules

- Output JSON only.
- One sentence or normative proposition equals one claim.
- Do not merge multiple obligations into one claim.
- Preserve source traceability.
- Do not silently resolve contradictions.
- Use `human_review_status` when the statement is contextual, inferred, or lower-authority.

## Required Claim Fields

```json
{
  "claim_id": "string",
  "topic": "string",
  "subtopic": "string",
  "claim_type": "string",
  "statement": "string",
  "source_document_id": "string",
  "source_location": {
    "source_statement_ids": ["string"],
    "pages": [1],
    "sections": ["string"],
    "evidence_quotes": ["string"]
  },
  "publisher": "string",
  "instrument_type": "string",
  "jurisdiction_level": "string",
  "document_status": "string",
  "authority_weight": 0.82,
  "publication_date": "YYYY-MM-DD or null",
  "effective_from": "YYYY-MM-DD or null",
  "effective_to": "YYYY-MM-DD or null",
  "validity_status": "active|historical|contextual_active",
  "applies_to": ["string"],
  "confidence": 0.0,
  "human_review_status": "string",
  "source_statement_type": "string",
  "claim_extraction_run_id": "string",
  "relations": []
}
```

## Relation Rules

Allowed relation types:

- `repeats`
- `clarifies`
- `narrows`
- `broadens`
- `supersedes`
- `partially_supersedes`
- `conflicts_with`
- `implements`
- `derives_from`
- `depends_on`
- `expires`
- `postpones`
- `transfers_responsibility_to`

Only assign a relation if the source basis is explicit or the dependency is clearly justified.
