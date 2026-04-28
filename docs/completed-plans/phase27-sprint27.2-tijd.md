# Sprint 27.2 - Tijd

## Summary
Sprint 27.2 is afgerond op 29 april 2026. De claimlaag splitst tijdinformatie nu expliciet uit, zodat formele deadlines, verwachte momenten, reviewcycli, budgetkalendermomenten, implementatiehorizons, lokale planningscontext en publicatiedata niet meer door elkaar worden gelezen.

## What Changed
- `src/build_claims_top5.py` voegt `time_status` toe aan iedere claim.
- `data/schemas/claim.schema.json` beschrijft de nieuwe tijdstatusvelden en toegestane waarden.
- `config/data_quality_perspectives.json` en `docs/data-quality-checklist.md` benoemen de tijdstatuswaarden en redactionele guardrails.
- `src/build_site_view_models.py` neemt tijdstatus mee in evidence entries, update-claimlijsten en tijdlijnitems.
- `src/build_quality_control.py` controleert dat alle claims een geldige tijdstatus hebben en markeert verwachte momenten en lokale planningscontext als reviewpunt.
- `src/build_data_quality_audit.py` schrijft een `time_status_audit` met statusverdeling, date-signal verdeling en review-samples.

## Time Status Values
- `formal_deadline`: formele of harde termijn die expliciet uit de bronpassage volgt.
- `expected_moment`: verwacht, indicatief of bronafhankelijk moment; geen harde deadline.
- `review_or_update_moment`: evaluatie-, herijkings- of actualisatiemoment.
- `budget_calendar_moment`: begrotings-, subsidie-, circulaire- of verantwoordingsmoment.
- `implementation_horizon`: meerjarige horizon of fasering voor uitvoering.
- `local_planning_context`: lokale bestuurlijke planning of vergadercontext; niet automatisch inhoudelijke D5/D6-deadline.
- `source_dated_moment`: bronverankerd tijdmoment zonder extra deadline- of budgetduiding.
- `publication_or_context_date`: publicatie- of contextdatum van een bron.
- `undated_context`: geen zelfstandig tijdmoment.

## Output
- Claims: regenerated with `time_status`.
- Timeline entries: regenerated with timeline-level `time_status`.
- Audit: `data/extracted/data_quality_audit.json` includes `time_status_audit`.
- QC: expected and local-planning time signals are review items, not blockers.

## Verification
- Downstream regeneration from claims through site render completed.
- `python src/verify_claim_id_references.py` passed.
- `python -m pytest` passed.

## Carry Forward
Sprint 27.3 should separate money and funding claims into funding routes, budget windows, allocation conditions, reporting/accountability moments, local funding gaps, and double-counting risks. Sprint 25.6 remains parked until stakeholder validation or explicit policy decisions are available.
