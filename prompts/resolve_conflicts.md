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

## Resolution Order

1. Higher authority beats lower authority.
2. If authority is equal, later effective date beats earlier.
3. If both are equal, leave the conflict unresolved.
4. Guidance may clarify but not override a stronger norm.
5. Municipal or regional claims may localize implementation but not override national obligations.

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
