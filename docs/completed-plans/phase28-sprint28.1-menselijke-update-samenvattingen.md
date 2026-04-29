# Sprint 28.1 - Menselijke Update-Samenvattingen

## Summary
Sprint 28.1 is afgerond op 29 april 2026. De updatepagina gebruikt nu menselijke samenvattingen als primaire leeslaag en vermijdt publieke tekst over interne datalagen, pipeline-stappen of technische claimmodellen.

## What Changed
- `config/site_updates.json` is herschreven zodat de drie bestaande updates gewone publiekswoorden gebruiken voor aanleiding, verandering en betekenis.
- `config/site_taxonomy.json` gebruikt in de sitebrede scope-regel geen interne claimlaagtaal meer.
- Elke update behoudt een `human_summary` met `intro`, `what_happened`, `what_changed` en `why_it_matters`.
- `src/render_site.py` noemt de detailpagina niet meer een ruwe claimlaag, maar een controlelijst met bronfragmenten.
- De updatepagina legt uit dat bronpagina's en tijdlijnmomenten leidend blijven voor inhoudelijke duiding.
- `tests/test_site_generation.py` controleert dat menselijke update-samenvattingen geen technische termen zoals `dataset`, `claimlaag`, `bronlaag`, `pijplijn`, `data/raw`, `manifest`, `review_needed`, `source-backed` of `ingested` gebruiken.

## Public Wording Rule
Gebruik op de updatepagina:

- `bronnen`, `bronfragmenten`, `controlelijst`, `tijdlijn`, `overzicht`, `lokale validatie`;
- geen interne termen zoals `claimlaag`, `bronlaag`, `pipeline`, `manifest`, `viewmodel`, `dataset`, `QC` of statuscodes.

## Verification
- Site view models and rendered pages regenerated.
- `python -m pytest` passed.

## Carry Forward
Sprint 28.2 should focus on attribution and authority language: lower-authority sources must be named explicitly, and stronger wording should only be used where the source status supports it.
