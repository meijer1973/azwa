# Sprint 27.1 - Norm

## Summary
Sprint 27.1 is afgerond op 29 april 2026. De claimlaag splitst normatieve kracht nu expliciet uit, zodat bindende bronpassages, akkoordafspraken, verwachtingen, toelichtingen, lagere-autoriteitssignalen en context niet meer op dezelfde manier kunnen worden gelezen.

## What Changed
- `src/build_claims_top5.py` voegt `normative_status` toe aan iedere claim.
- `data/schemas/claim.schema.json` beschrijft de nieuwe normstatusvelden en toegestane waarden.
- `config/data_quality_perspectives.json` en `docs/data-quality-checklist.md` benoemen de normstatuswaarden en redactionele guardrails.
- `src/build_site_view_models.py` neemt normstatus mee in evidence entries en gebruikt normstatus in autoriteitsnotities.
- `src/build_quality_control.py` controleert dat alle claims een geldige normstatus hebben en markeert lagere-autoriteitsnormen als reviewpunt.
- `src/build_data_quality_audit.py` schrijft een `normative_status_audit` met statusverdeling en attributie-samples.

## Norm Status Values
- `binding`: formeel verplichtend of bindend volgens broncategorie en normatieve bronpassage.
- `agreement`: afspraak of akkoordtekst; bestuurlijk relevant maar niet automatisch een wettelijke plicht voor Almere.
- `expectation`: richtinggevende verwachting of uitwerkingskader.
- `guidance`: toelichting, format, handreiking, advies of praktische uitleg.
- `lower_authority_signal`: lagere-autoriteitsbron met normachtige taal; altijd expliciet toeschrijven.
- `contextual`: contextueel signaal zonder zelfstandige normkracht.

## Output
- Claims: 524.
- Normstatusverdeling: 2 `binding`, 74 `agreement`, 34 `expectation`, 190 `guidance`, 150 `lower_authority_signal`, 74 `contextual`.
- QC: 0 blocking, 6 warning, 111 review items.
- Nieuwe reviewreden: `lower_authority_norm_signal`.

## Verification
- Downstream regeneration from claims through site render completed.
- `python src/verify_claim_id_references.py` passed.
- `python -m pytest` passed with 53 tests.

## Carry Forward
Sprint 27.2 should separate time claims into formal deadlines, expected publication moments, review moments, budget-calendar moments, and local planning context. Sprint 25.6 remains parked until stakeholder validation or explicit policy decisions are available.
