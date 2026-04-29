# Sprint 27.4 - Governance

## Summary
Sprint 27.4 is afgerond op 29 april 2026. De claimlaag splitst governance nu expliciet uit, zodat besluitvorming, coordinatie, aanvraag/indiening, uitvoering, verantwoording, goedkeuring, review, governancegaten en losse actorcontext niet meer als een algemene rolclaim worden gelezen.

## What Changed
- `src/build_claims_top5.py` voegt `governance_status` toe aan iedere claim.
- `data/schemas/claim.schema.json` beschrijft de nieuwe governancestatusvelden, actor-signalen en toegestane waarden.
- `config/data_quality_perspectives.json` en `docs/data-quality-checklist.md` benoemen governancestatuswaarden en actor-signalen.
- `src/build_site_view_models.py` neemt governancestatus mee in evidence entries en update-claimlijsten.
- `src/build_quality_control.py` controleert dat alle claims een geldige governancestatus hebben en markeert governancegaten, actorcontext en vage `regio`-actoren als reviewpunt.
- `src/build_data_quality_audit.py` schrijft een `governance_status_audit` met statusverdeling, actor-signaalverdeling en verificatie-samples.

## Governance Status Values
- `decision_role`: bron noemt besluitvorming, vaststelling of instemming.
- `coordination_role`: bron noemt coordinatie, regie of afstemming.
- `application_role`: bron noemt aanvraag, indiening, aanlevering of penvoerderschap.
- `execution_role`: bron noemt uitvoering, organisatie, implementatie of realisatie.
- `accountability_role`: bron noemt verantwoording, eigenaarschap, aanspreekbaarheid of verantwoordelijkheid.
- `approval_role`: bron noemt goedkeuring, akkoord of formele vaststelling.
- `review_role`: bron noemt toetsing, monitoring, evaluatie of controle.
- `governance_gap`: publieke bronbasis laat rol, mandaat, eigenaar of besluitroute nog open.
- `actor_context`: bron noemt actor(en), maar niet genoeg om een specifieke rol te claimen.
- `not_governance`: geen zelfstandige governanceclaim.

## Actor Signals
De eerste actor-signalen zijn: `ministerie`, `vng`, `fondsbeheerder`, `mandaatgemeente`, `regio`, `gemeente`, `gemeenteraad`, `college`, `zorgverzekeraar` en `uitvoeringspartner`.

## Verification
- Downstream regeneration from claims through site render completed.
- `python src/verify_claim_id_references.py` passed.
- `python -m pytest` passed.

## Carry Forward
Sprint 27.5 should separate locality claims into explicit Almere, explicit Flevoland, regional-split, national-only-with-local-relevance, inferred local relevance and local adoption gaps. Sprint 25.6 remains parked until stakeholder validation or explicit policy decisions are available.
