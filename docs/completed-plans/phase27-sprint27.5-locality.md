# Sprint 27.5 - Locality

## Summary
Sprint 27.5 is afgerond op 29 april 2026. De claimlaag splitst lokale en regionale relevantie nu expliciet uit, zodat expliciete Almeerse bronnen, Flevolandse bronnen, regionale schaalcontext, landelijke lijnen met lokale relevantie, afgeleide lokale relevantie en lokale adoptiegaten niet meer op dezelfde manier worden gelezen.

## What Changed
- `src/build_claims_top5.py` voegt `locality_status` toe aan iedere claim.
- `data/schemas/claim.schema.json` beschrijft de nieuwe localitystatusvelden, regionale split-signalen en toegestane waarden.
- `config/data_quality_perspectives.json` en `docs/data-quality-checklist.md` benoemen localitystatuswaarden en regionale split-signalen.
- `src/build_site_view_models.py` neemt localitystatus mee in evidence entries en update-claimlijsten.
- `src/build_quality_control.py` controleert dat alle claims een geldige localitystatus hebben en markeert nationale claims met lokale relevantie, afgeleide lokale relevantie, lokale adoptiegaten en regionale split-context als reviewpunt.
- `src/build_data_quality_audit.py` schrijft een `locality_status_audit` met statusverdeling, regionale split-verdeling en verificatie-samples.

## Locality Status Values
- `explicit_almere`: bron of passage gaat expliciet over Almere.
- `explicit_flevoland`: bron of passage gaat expliciet over Flevoland of GGD/Zorgzaam Flevoland.
- `regional_split_context`: regionale context waarbij de schaal moet worden benoemd.
- `national_general`: algemene landelijke lijn zonder zelfstandige lokale claim.
- `national_with_local_relevance`: landelijke lijn die relevant is voor Almere, maar geen lokale vaststelling is.
- `inferred_local_relevance`: lokale relevantie is afgeleid en vraagt lokale verificatie.
- `local_adoption_gap`: landelijke of regionale lijn zichtbaar, maar lokale openbare overname of documentatie ontbreekt.
- `municipal_context`: gemeentelijke context waarbij moet worden gecontroleerd of het Almere betreft.
- `no_locality_signal`: geen zelfstandig locality-signaal.

## Regional Split Signals
De eerste regionale split-signalen zijn: `IZA/AZWA-regio`, `GGD-regio`, `zorgkantoorregio`, `ROAZ/subregio`, `provincie` en `gemeentelijk`.

## Verification
- Downstream regeneration from claims through site render completed.
- `python src/verify_claim_id_references.py` passed.
- `python -m pytest` passed.

## Carry Forward
Sprint 27.6 should separate execution claims into possible follow-up actions, decision questions, dependencies, sequencing needs, implementation requirements and review tasks without turning generated suggestions into decided policy.
