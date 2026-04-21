# Build Municipal View

You are generating a computed municipal view for Almere from the interpreted claim layer.

## Input

- `current_interpretation.json`
- `conflict_register.json`
- relevant national, regional, and municipal claim metadata
- municipality target: Almere

## Goal

Produce a computed municipal JSON without mixing it with human policy choices.

## Output Rules

- Output JSON only.
- Treat national claims as the baseline.
- Use regional and municipal material to localize, contextualize, or identify gaps.
- Do not invent local commitments.
- Put uncertainties into `uncertain_items`.
- Put unresolved tradeoffs into `items_requiring_political_choice`.
- Keep the local decision layer separate.

## Required Shape

```json
{
  "municipality_id": "GM0034",
  "municipality_name": "Almere",
  "as_of_date": "YYYY-MM-DD",
  "applicable_d5_items": [],
  "applicable_d6_items": [],
  "local_gaps": [],
  "local_dependencies": [],
  "relevant_regional_documents": [],
  "relevant_municipal_documents": [],
  "uncertain_items": [],
  "obsolete_items": [],
  "unresolved_conflicts": [],
  "items_requiring_political_choice": []
}
```

## Separation Rule

- `almere_current_view.json` is computed only.
- `almere_local_decisions.json` is human-entered only.
- Never write a local political choice into the computed view as if it were already decided.
