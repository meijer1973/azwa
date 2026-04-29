# Sprint 28.2 - Bronverwijzing en Autoriteitstaal

## Summary
Sprint 28.2 is afgerond op 29 april 2026. De publieke site maakt nu explicieter wie de bronhouder is, welke bronstatus een passage heeft en welke formulering veilig is bij lagere-autoriteits- of contextbronnen.

## What Changed
- `src/render_site.py` toont bij ondersteunende bronnen nu bronhouder, bronstatus, soort bron en veilige formulering.
- Controlelijsten met bronfragmenten schrijven lagere-autoriteitsfragmenten expliciet toe, bijvoorbeeld `Volgens Raad van Almere:`.
- Reviewsecties met bronnen die extra duiding vragen nemen nu dezelfde autoriteitscontext mee.
- `src/build_site_view_models.py` geeft `normative_status` en `authority_note` door aan review-source-signals zodat de site de juiste bronstatus kan tonen.
- `tests/test_site_generation.py` borgt dat lagere-autoriteitsfragmenten zichtbaar worden toegeschreven en dat bronstatus/veilige formulering op detailpagina's aanwezig zijn.

## Public Wording Rule
Gebruik sterkere taal alleen wanneer de bronstatus dat draagt. Bij lagere-autoriteit, guidance, verwachting, akkoordtekst of afgeleide lokale relevantie moet de tekst expliciet maken wie de bronhouder is en wat de bron wel of niet bewijst.

## Verification
- Site view models and rendered pages regenerated.
- Internal review dashboard regenerated.
- `python -m pytest` passed.

## Carry Forward
Sprint 28.3 should move longer drill-down material to dedicated detail pages while keeping overview pages short and readable.
