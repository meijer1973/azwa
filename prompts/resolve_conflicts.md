# Resolve Conflicts

You are building a conflict register and a current interpretation layer from an append-only claim set.

## Input

- claims
- claim relations
- authority rules
- claim resolution rules
- as-of date

## Goal

Produce:

- a conflict record when claims overlap, supersede, or remain layered
- a current interpretation per topic without deleting history

## Output Rules

- Output JSON only.
- Never mutate the original claims.
- Never silently discard older claims.
- If ambiguity remains, mark it and require human review.
- When a lower-authority source is retained, name the source type explicitly in the human-readable summary or notes.
- Do not phrase lower-authority commentary as settled fact when stronger or later text may exist elsewhere.
- Distinguish a true contradiction from a terminology or definition overlap.

## Resolution Order

1. Higher authority beats lower authority.
2. If authority is equal, later effective date beats earlier.
3. If both are equal, leave the conflict unresolved.
4. Guidance may clarify but not override a stronger norm.
5. Municipal or regional claims may localize implementation but not override national obligations.

## Human Communication Rules

- For `authority_unclear`, explicitly attribute the statement to the source and level.
- Preferred phrasing: `According to a VNG FAQ, ...`, `A municipal summary page states that ...`, or the Dutch equivalent if the output is Dutch-facing.
- Avoid phrasing such as `It is agreed that ...` when the source is a FAQ, commentary page, or summary page.
- For `municipality_relevance_inferred`, do not describe the item as a database error.
- Instead, explain that a national or regional goal exists, but the public municipal documents do not yet clearly show whether the municipality has explicitly adopted or localized it.
- For `localization_overlap` or similar layered cases, explain whether the issue is likely a definition problem, a public-language usage problem, or a real policy contradiction.
- If a term such as `stevige lokale teams` may be used both as policy language and as general public-facing language, mark that human clarification is needed before treating the claims as equivalent.

## Conflict Record Shape

```json
{
  "conflict_id": "string",
  "topic": "string",
  "claim_ids": ["string"],
  "conflict_type": "supersession|precedence_overlap|implementation_layering|localization_overlap|unresolved",
  "resolution_status": "resolved|parallel_claims|needs_human_review",
  "recommended_resolution_rule": "string",
  "impact_on_almere": "string",
  "winning_claim_ids": ["string"],
  "superseded_claim_ids": ["string"],
  "needs_human_review": true,
  "notes": "string"
}
```

## Notes Guidance

- Use `notes` to explain why human review is needed in plain language.
- Good note for `authority_unclear`: `This claim is preserved because it may help interpret implementation, but it comes from a VNG FAQ and should not be treated as stronger than the signed AZWA or Kamerbrieven.`
- Good note for terminology overlap: `The term 'stevige lokale teams' appears in both national and municipal material, but it is not yet clear whether the same policy definition is intended.`

## Current Interpretation Shape

```json
{
  "topic": "string",
  "as_of_date": "YYYY-MM-DD",
  "current_claim_ids": ["string"],
  "historical_claim_ids": ["string"],
  "superseded_claim_ids": ["string"],
  "conflicted_claim_ids": ["string"],
  "interpretation_summary": "string",
  "confidence": 0.0,
  "needs_human_review": true
}
```

## Interpretation Summary Guidance

- If the current view keeps both a stronger national baseline and a weaker local or sectoral interpretation, say so explicitly.
- Preferred pattern: `The national agreement sets the baseline. A lower-authority local source uses similar language, but human review is needed to confirm whether it reflects the same defined policy concept.`
