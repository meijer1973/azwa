# Sprint 30.2 - Besluitvragen en mogelijke opvolgacties

## Summary
Sprint 30.2 is completed. The current sprint is Sprint 30.3 - Beleidsdocumenten en rapporten. Sprint 25.6 remains parked until stakeholder validation records, local/internal documents, finance/controller confirmation, or an explicit policy decision exist.

## What Changed
- Decision and action view models now separate `source_basis_summary`, `almere_choice_space`, `safe_use_note` and `perspective_summary`.
- Decision and action cards show what the public source base raises and what Almere still has to fill in.
- Decision and action detail pages include a `Bronbasis en lokale keuze` section before the working direction or action rationale.
- Possible follow-up actions were softened from instruction language such as `Werk uit`, `Leg vast` and `Breng in kaart` to `Verken` wording.
- Owner and participant wording now says where validation is needed instead of implying settled responsibility.

## Source Boundary
This sprint did not create new decisions, assign owners or settle follow-up actions. It only made existing decision/action pages clearer about their evidence boundary and their status as human choice questions.

## Files
- `src/build_site_view_models.py`
- `src/render_site.py`
- `tests/test_site_generation.py`
- `data/site/decision_view_models/*.json`
- `data/site/action_view_models/*.json`
- `data/site/site_home_view.json`
- `data/site/site_almere_view.json`
- `data/site/dashboard_view.json`
- `docs/data-quality-roadmap.md`

## Verification
Verification for this sprint should include:

```powershell
python src/build_site_view_models.py
python src/render_site.py
python src/build_internal_review_dashboard.py
python -m pytest tests/test_site_generation.py
python -m pytest
```
