# Sprint 28.3 - Drill-down Detailpagina's

## Summary
Sprint 28.3 is afgerond op 29 april 2026. Besluitvraag- en opvolgactiepagina's blijven nu korter: de volledige bronbasis, beleidsbasis en reviewdetails staan op aparte `onderbouwing`-pagina's.

## What Changed
- `src/render_site.py` maakt voor elke besluitvraag en opvolgactie een aparte onderbouwingspagina.
- Hoofdpagina's tonen een compacte sectie `Onderbouwing en drill-down` met klikbare tellingen voor bronverwijzingen, beleidsbasis en reviewpunten.
- Reviewtags op besluitvraagkaarten linken direct naar `onderbouwing/#menselijke-duiding`.
- `src/build_site_view_models.py` neemt de nieuwe `decision_evidence`- en `action_evidence`-pagina's op in de site-manifestlaag.
- De zoekindex bevat de nieuwe onderbouwingspagina's als aparte vindbare pagina's.
- `tests/test_site_generation.py` controleert dat reviewdetails niet meer op de hoofd-detailpagina staan, maar wel op de onderbouwingspagina.

## Public Wording Rule
Houd overzichtspagina's en hoofd-detailpagina's kort. Gebruik aparte onderbouwingspagina's voor lange bronlijsten, reviewdetails, autoriteitsduiding en controleerbare herleidbaarheid.

## Verification
- Site view models and rendered pages regenerated.
- Internal review dashboard regenerated.
- `python -m pytest` passed.

## Carry Forward
Fase 29 kan de tijdlijn verder als beleidsinstrument uitwerken. Dezelfde drill-downregel geldt daar: overzicht eerst, herleidbaarheid achter een klik.
