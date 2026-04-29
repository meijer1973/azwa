# Updateprotocol AZWA-site

## Summary
Current sprint: Sprint 31.1 - Updateprotocol. This protocol describes how new public source information is added without overwriting older claims or silently changing public pages.

## Purpose
Every meaningful source intake or source correction must leave a readable trail:

- what source information changed;
- which documents, claims, timeline moments or pages were affected;
- what the change means for Almere;
- what remains uncertain or review-needed;
- which generated outputs were refreshed.

The public `/updates/` page and the internal dashboard mirror must be updated when source intake changes the public source base, claim layer, timeline, Almere page, source pages, decision/action pages or report candidates.

## When To Create An Update
Create a new entry in `config/site_updates.json` when one or more of these happen:

- new public sources are added to `data/raw/manifest.json`;
- existing source files are replaced, corrected or substantially re-extracted;
- source intake changes claim counts, review counts, timeline entries or source pages;
- an update changes the public interpretation of D5, D6, financing, governance, locality, execution or Almere-specific gaps;
- report candidates or review packs are updated because source evidence changed.

Do not create a public update for purely internal code refactors unless they change public source interpretation, public pages, review status or report-readiness.

## Required Update Fields
Every update in `config/site_updates.json` must include:

- `update_id`: stable, unique and date-bearing where possible.
- `published_on`: ISO date.
- `title`: human-readable Dutch title.
- `summary`: short plain-language summary.
- `source_reference`: primary trigger source or representative source.
- `human_summary`: with `intro`, `what_happened`, `what_changed`, `why_it_matters`.
- `change_highlights`: each item with `summary` and `detail`.
- `key_points`: short bullet points for the update.
- `metrics`: before/after values for sources, claims, review items, timeline items or other relevant counts.
- `affected_pages`: public pages or dashboard pages touched by the update.
- `affected_document_ids`: document IDs that exist in `data/extracted/document_inventory.json`.
- `highlighted_timeline_entry_keys`: empty list allowed, but present.

## Human Summary Rules
The human summary is the readable changelog. It must:

- use ordinary Dutch;
- say what happened, not just which file changed;
- say what changed in meaning for Almere;
- explain uncertainty or validation boundaries;
- avoid pipeline jargon such as `JSON`, `manifest`, `view model`, `QC`, `pipeline`, `claim layer` or `review_needed`.

Technical detail belongs in internal sprint notes, not in public update text.

## Source Intake Sequence
Use this order for source intake:

1. Add or update the source in `data/raw/manifest.json` and save the raw/source file where possible.
2. Run the full pipeline or the appropriate upstream stages.
3. Check generated source pages, claims, timeline entries, review queue and affected site views.
4. Add or update `config/site_updates.json` with the human changelog.
5. Run:

```powershell
python src/validate_update_protocol.py
python src/build_site_view_models.py
python src/render_site.py
python src/build_internal_review_dashboard.py
python -m pytest tests/test_update_protocol.py tests/test_site_generation.py
```

6. Commit and push before reporting back.

## Old Claims
Old claims are not overwritten as a policy conclusion. New claims may:

- add new evidence;
- clarify an older claim;
- narrow an older interpretation;
- contradict an older interpretation;
- move an item into review or decision-needed status.

If a new source changes meaning, describe that delta in `human_summary.what_changed` and, where relevant, in `change_highlights`.

## Public Boundary
The update page is not a final policy report. It is a traceable change log. Use careful wording:

- `deze bron maakt zichtbaar`;
- `de update scherpt aan`;
- `blijft lokale validatie vragen`;
- `nog niet vastgesteld`;
- `niet gebruiken als definitieve bestuurlijke tekst`.

Avoid:

- final ownership claims without validation;
- final funding claims without finance/controller confirmation;
- final D6 classification without local validation;
- internal filenames as public evidence.
