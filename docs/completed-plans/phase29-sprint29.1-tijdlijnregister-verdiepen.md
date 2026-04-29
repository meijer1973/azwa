# Phase 29 Sprint 29.1 - Tijdlijnregister Verdiepen

## Summary

Current sprint at completion: Sprint 29.1. This sprint made the timeline usable as a policy-orientation layer instead of only a chronological list.

Each timeline item now carries a compact policy metadata block:

- `moment_type`
- `source_status`
- `authority`
- `actor_summary`
- `primary_perspective`
- `timeline_policy_note`

The public timeline page renders these fields next to the summary and consequence for Almere.

## Completed Work

- Added policy metadata enrichment in `src/build_site_view_models.py`.
- Rendered the metadata in `src/render_site.py` under each clickable timeline item.
- Added compact CSS for timeline metadata in `assets/site.css`.
- Fixed stale claim references in `config/timeline_curation.json` so curated timeline entries point to existing claim IDs.
- Added tests that every timeline item carries the new metadata and that curation claim IDs resolve.
- Regenerated site view models, rendered site, and the internal dashboard.

## Verification

- `python src/build_site_view_models.py`
- `python src/render_site.py`
- `python src/build_internal_review_dashboard.py`
- `python -m pytest`

## Notes For Sprint 29.2

Sprint 29.2 can now build on `primary_perspective`, `moment_type`, and `source_status` when adding or sharpening budget-cycle and accountability-cycle timeline items.

Keep the D6 validation boundary intact: timeline metadata may show review need or source authority, but must not mark unresolved D6 ownership, funding, or local classification as settled.
