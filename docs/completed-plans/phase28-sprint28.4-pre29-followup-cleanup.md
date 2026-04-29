# Sprint 28.4 - Pre-29 Follow-up Cleanup

## Summary
Sprint 28.4 is afgerond op 29 april 2026. Deze korte cleanup voorkomt dat Phase 29 voortbouwt op verouderde routing, lokale orphan HTML-pagina's of onduidelijke statusmodel-signalen.

## What Changed
- `RESEARCH_AGENT_MAP.md` verwijst niet meer naar `data/site/action_view_models/act_d6_lokale_structuur_verduidelijken.json`, omdat die actie in de huidige gegenereerde viewlaag niet meer bestaat.
- `src/render_site.py` wist de lokale `dist/`-map veilig voordat de site opnieuw wordt geschreven. Daardoor blijven oude, niet meer gegenereerde HTML-pagina's niet lokaal rondzingen.
- De Sprint 28.1-test op menselijke update-samenvattingen is aangescherpt: hij controleert nu niet alleen jargonpatronen, maar ook aanwezigheid van alle vier `human_summary`-velden, minimale lengte en basale Nederlandse prozavorm.
- `zero_count_statuses` en `zero_count_actor_signals` zijn expliciet als tijdelijke cleanup-opgave ingepland in Sprint 29.0.

## Attribution Decision
`normative_attribution_prefix` blijft bewust beperkt tot controlelijsten met losse bronfragmenten, waar een ruwe passage anders te snel als zelfstandige claim leest. Thema-, bron-, home- en onderbouwingspagina's gebruiken in plaats daarvan de zichtbare broncontext: `Bronhouder`, `Bronstatus`, `Soort bron` en `Veilige formulering`. Dat houdt overzichtstekst leesbaar zonder de bronstatus te verbergen.

## Zero-count Decision
`zero_count_statuses` is geen gewenste permanente fixture. Het blijft een tijdelijk design-audit signaal totdat Sprint 29.0 per nulwaarde beslist of het schema-veld bewust blijft, classifierlogica moet worden aangepast, of de waarde uit schema/config moet verdwijnen.

## Verification
- Site view models and rendered pages regenerated.
- Internal review dashboard regenerated.
- `python -m pytest` passed.
- `git diff --check` passed.
