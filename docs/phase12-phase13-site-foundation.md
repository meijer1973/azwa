# Phase 12 / Phase 13

This milestone adds the first public executive publication layer on top of the existing AZWA extraction pipeline.

## Scope

- `phase12_site_view_models` derives Dutch site-facing view models from:
  - the current Almere municipal view
  - the D5/D6 master and claim interpretation layers
  - the document inventory and source metadata
  - the review queue for uncertainty-aware wording
- `phase13_site_render` renders a static site for GitHub Pages with:
  - start page
  - Almere page
  - besluitvragen overview plus detail pages
  - opvolgacties overview plus detail pages
  - dashboard
  - placeholder routes for later theme, timeline, reference, and source sections

## Key design choices

- Public page text is in Dutch.
- The site is executive-first rather than encyclopedic.
- Generated besluitvragen and opvolgacties are explicitly framed as possible follow-up items derived from the current public source base.
- Lower-authority or inferred-local items remain traceable through evidence lists and careful wording.
- The site renderer uses relative links so the output works as a GitHub Pages project site.

## Repository additions

- `config/site_taxonomy.json`
- `src/build_site_view_models.py`
- `src/render_site.py`
- `templates/base.html`
- `assets/site.css`
- `assets/site.js`
- `data/site/`
- `.github/workflows/deploy-pages.yml`

## Build flow

1. existing extraction, claim, interpretation, and QC stages run first
2. site view models are derived into `data/site/`
3. the static renderer writes HTML and assets into `dist/`
4. GitHub Actions can publish `dist/` to GitHub Pages
