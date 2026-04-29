# Phase 29 Sprint 29.3 - Handreikingen en Uitvoeringsmomenten

## Summary

Current sprint at completion: Sprint 29.3. This sprint completed Phase 29 by separating guidance and execution-support moments from formal decisions and hard deadlines in the timeline.

The current sprint after completion is Sprint 30.1 - Lokale lacunes.

## Completed Work

- Added the D5 workagenda format document as its own timeline item.
- Added `execution_support` grouping to the timeline register and timeline view.
- Grouped support moments into:
  - format;
  - process note;
  - workagenda process;
  - webinar;
  - guidance release / thematafel;
  - support page.
- Rendered a separate “Handreikingen en uitvoeringsmomenten” section on the timeline page.
- Added safe-use text stating that these moments are preparation or guidance, not formal decisions or hard norms without a separate source.
- Added tests for the new format timeline item and support grouping.

## Verification

- `python src/build_site_view_models.py`
- `python src/render_site.py`
- `python src/build_internal_review_dashboard.py`
- `python -m pytest`

## Notes For Sprint 30.1

Sprint 30.1 should use the Phase 29 timeline distinctions when describing local gaps. If a gap depends on a handreiking, format, webinar, thematafel, or process note, keep it framed as a preparation or validation issue unless a formal local or national source settles it.

Sprint 25.6 remains parked until stakeholder validation records, local/internal documents, finance/controller confirmation, or an explicit policy decision are available.
