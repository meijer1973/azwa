# Phase 29 Sprint 29.2 - Begrotings- en Verantwoordingscyclus

## Summary

Current sprint at completion: Sprint 29.2. This sprint made the financial cycle visible as a policy navigation layer on top of the timeline.

The timeline now includes expected 2026 gemeentefonds moments for May, September, and December, based on the existing BZK gemeentefonds source. The timeline view also carries a generated `budget_cycle` grouping.

## Completed Work

- Added expected Septembercirculaire and Decembercirculaire 2026 timeline items, both marked as expected/review-needed until the concrete circulars are ingested.
- Added `budget_cycle` grouping to `data/site/site_timeline_view.json` and `data/site/timeline_register.json`.
- Grouped financial timeline items into:
  - local budget;
  - municipal fund / gemeentefonds;
  - SPUK and subsidy;
  - accountability;
  - workagenda and funds;
  - other financial context.
- Rendered a human-readable “Begrotings- en verantwoordingscyclus” section on the timeline page.
- Kept the budget-cycle section below the chronological timeline so date-order tests continue to check the main timeline sequence.
- Added tests for the new expected circular moments and budget-cycle grouping.

## Verification

- `python src/build_site_view_models.py`
- `python src/render_site.py`
- `python src/build_internal_review_dashboard.py`
- `python -m pytest`

## Notes For Sprint 29.3

Sprint 29.3 can use the same timeline metadata pattern to separate handreikingen, webinars, thematafels, formats and other execution-support moments from formal decisions or binding deadlines.

Do not turn expected circular moments into factual publication moments until the actual circular source has been ingested.
