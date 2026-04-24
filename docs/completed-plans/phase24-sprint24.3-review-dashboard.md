# Sprint 24.3 - Internal review dashboard

Status: completed.

## Output
- Local dashboard: `docs/internal/review-dashboard.html`
- Generator: `src/build_internal_review_dashboard.py`
- Input data:
  - `data/extracted/data_quality_audit.json`
  - `data/extracted/review_queue.json`
  - `config/data_quality_perspectives.json`
  - `data/extracted/claims/claims_master.jsonl`
  - `data/curated/regional_roles_and_splits_almere_flevoland.json`
  - `data/site/site_updates_view.json`

## Scope
The dashboard is an internal workbench for data-quality triage. It is intentionally not part of `dist/` and is not linked from the public-facing GitHub Pages site.

The UI may use English technical framing, because it is developer- and agent-facing. Dutch labels are kept where they come from the roadmap or source-domain vocabulary, including:

- Norm, Tijd, Geld, Governance, Locality, Execution;
- bronprobleem, extractieprobleem, claimprobleem, interpretatieprobleem, tekstprobleem.

## What the dashboard shows
- Summary counts from the Sprint 24.2 audit and review queue.
- Open dashboard items grouped by perspective and issue type.
- A Locality split between Almere, IZA/AZWA-regio Flevoland, and general or unclear locality items.
- An explicit IZA/AZWA-regio Flevoland definition: included municipalities are Almere, Dronten, Lelystad, Noordoostpolder and Urk; Zeewolde is recorded as the relevant exception because it connects to Noord-Veluwe for the regioplan route.
- A top tab bar with Overview, Sprint History, Public Updates Mirror, and Open Items.
- A top-of-page Sprint Ledger and Cleanup Items section so humans can immediately see current plan status and next cleanup targets.
- A Sprint History tab for recent technical sprint updates.
- A Public Updates Mirror tab based on `data/site/site_updates_view.json`, so the internal dashboard also shows the data-update history used by the public `/updates/` page.
- Review queue items, broad topic buckets, perspective mapping gaps, rough claim text, site text risks, and regional role review prompts.
- Links back to the underlying repository data files.
- A regional guardrail for Almere/Flevoland role confusion, including the Lelystad practical-task claim as a review prompt rather than a fact.

## Maintenance policy
The dashboard must stay current with the roadmap and public update data. When sprint status, current planning, cleanup targets, review data, source coverage, public update history, or dashboard inputs change, update the roadmap first where relevant and rerun:

`python src/build_internal_review_dashboard.py`

Do this before committing, so humans opening the local dashboard do not see stale plan status.

## Current limitations
- The dashboard classifies existing audit and review items; it does not resolve them.
- The issue-type mapping is conservative and rule-based.
- It opens directly as a local HTML file and does not require a local server.

## Verification
- `python src/build_internal_review_dashboard.py`
- `python -m py_compile src/build_internal_review_dashboard.py`
- JSON parse checks for the dashboard input files.
