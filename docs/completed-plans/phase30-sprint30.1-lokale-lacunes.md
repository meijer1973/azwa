# Sprint 30.1 - Lokale lacunes

## Summary
Sprint 30.1 is completed. The current sprint is Sprint 30.2 - Besluitvragen en mogelijke opvolgacties. Sprint 25.6 remains parked until stakeholder validation records, local/internal documents, finance/controller confirmation, or an explicit policy decision exist.

## What Changed
- The Almere site view now enriches `local_gaps` with theme label, gap type, public-source support, public-source limits, a follow-up question, safe wording, related topics and evidence references.
- A D6 validation-boundary gap is added from `data/extracted/municipal/almere_d6_responsibility_register.json` when the register still has non-settled rows.
- The Almere page renders local gaps as expandable items under `#lokale-hiaten`, so human reviewers can read the unresolved question before the evidence list.
- Sprint regression tests now check that local gaps remain human-readable and that the D6 validation boundary keeps `settled_count` at zero.

## Source Boundary
Sprint 30.1 did not settle any local D6 responsibility, owner, execution mandate, funding source or formal D6 classification. It only made the public-source boundary easier to read on the Almere page.

## Files
- `src/build_site_view_models.py`
- `src/render_site.py`
- `tests/test_site_generation.py`
- `data/site/site_almere_view.json`
- `dist/almere/index.html`
- `docs/data-quality-roadmap.md`

## Verification
Verification for this sprint should include:

```powershell
python src/build_site_view_models.py
python src/render_site.py
python src/build_internal_review_dashboard.py
python -m pytest tests/test_site_generation.py
```
