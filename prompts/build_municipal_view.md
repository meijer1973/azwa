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
- If a national goal is relevant to Almere but public Almere documents do not yet show explicit adoption, flag that as a useful policy gap or documentation gap.
- Do not treat that gap as an extraction error.
- Human-readable summaries should clearly distinguish `national goal`, `local adoption not yet explicit`, and `local commitment publicly documented`.

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

## Human Communication Rules

- For municipality-relevance cases, use wording that helps policymakers act on the gap.
- Preferred phrasing: `A national agreement sets this as a goal, but the currently collected public Almere documents do not yet make explicit whether or how Almere has adopted it.`
- If the likely implication is that follow-up is needed, say so in a neutral way.
- Preferred phrasing: `This may require local clarification, adoption, or publication in municipal policy documents.`
- If a local source uses a term that also appears in national policy text, do not automatically assume they mean the same thing.
- Instead, state that human review is needed to confirm whether the local wording reflects the same policy-defined concept.

## Gap Interpretation Guidance

- `local_gaps` may include cases where a national or regional expectation exists, but explicit Almere adoption is not yet visible in the collected public corpus.
- `uncertain_items` should include cases where Almere may be acting in practice, but the public documents do not yet make the commitment clear enough to treat as settled.
- `items_requiring_political_choice` should be reserved for real local choice points, not for simple source-attribution uncertainty.
