# Phase 23 - Site updates layer and curated April/May 2026 timeline moments

## Goal

Make two kinds of change visible on the public site:

1. newly relevant operational/timeline moments that are already supported by ingested sources
2. what a concrete data update changed in the dataset and on the website

## What changed

- added a curated `supplemental_entries` block to [config/timeline_curation.json](C:/Projects/azwa/config/timeline_curation.json)
- added two new timeline moments based on already ingested April 2026 sources:
  - `23 april 2026, 12.00-13.00 uur` - VWS/VNG webinar over AZWA-middelen en regionale werkagenda
  - `26 mei 2026` - landelijke thematafel Medisch-Sociaal en Preventie waarna handreikingen volgen
- added [config/site_updates.json](C:/Projects/azwa/config/site_updates.json) as structured public update metadata
- generated [data/site/site_updates_view.json](C:/Projects/azwa/data/site/site_updates_view.json)
- rendered a new public page at [dist/updates/index.html](C:/Projects/azwa/dist/updates/index.html)
- added `Updates` to the site navigation and search index
- added a `Laatste data-update` section on the homepage

## Why this matters

The public site previously showed new sources and new timeline items, but not a clear public explanation of what a fresh data addition changed in the dataset. The new update layer closes that gap without turning the site into a manual CMS.

## Design choice

The webinar and thematafel were added as curated supplemental timeline entries, not as direct claim-derived moments. That keeps the provenance explicit:

- both moments are grounded in already ingested April 2026 source documents
- both are operational/support moments rather than stronger norm-setting decisions
- both therefore remain visibly source-backed and marked as needing human interpretation

## Verification

- `python -m unittest discover -s tests -p "test_*.py"`
- `python src/run_pipeline.py --all`
