# Extract Table

You are extracting one table or table-like block from an AZWA-related source.

## Input

- `document_id`
- page or section context
- raw table text
- nearby heading text when available

## Goal

Produce one JSON object for table preservation and later reuse.

## Output Rules

- Output JSON only.
- Preserve the table structure as faithfully as possible.
- Do not normalize policy meaning here.
- Do not drop rows silently.
- Do not rename columns unless the raw source is obviously broken.
- If a cell is unreadable or uncertain, preserve the raw text and mark uncertainty in notes.
- Never invent a page number.

## Required JSON Shape

```json
{
  "document_id": "string",
  "table_id": "string",
  "page": 1,
  "section_path": ["string"],
  "table_label": "string or null",
  "table_type_guess": "financial|monitoring|governance|matrix|unknown",
  "headers": ["string"],
  "rows": [
    ["cell", "cell"]
  ],
  "raw_table": "string",
  "preservation_notes": ["string"],
  "extraction_uncertainty": "low|medium|high"
}
```

## D5/D6 Matrix Rule

If the table appears to be a D5/D6 matrix, preserve the original column names and row labels as literally as possible.
