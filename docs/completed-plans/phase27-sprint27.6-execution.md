# Sprint 27.6 - Execution

## Summary
Sprint 27.6 is afgerond op 29 april 2026. De claimlaag splitst uitvoeringsbetekenis nu expliciet uit, zodat operationele vereisten, zichtbare activiteiten, besluitvragen, afhankelijkheden, volgorde- of faseringsvragen, capaciteitsvragen, reviewtaken en algemene uitvoeringscontext niet meer op dezelfde manier worden gelezen.

## What Changed
- `src/build_claims_top5.py` voegt `execution_status` toe aan iedere claim.
- `data/schemas/claim.schema.json` beschrijft de nieuwe executionstatusvelden, need-signalen en toegestane waarden.
- `config/data_quality_perspectives.json` en `docs/data-quality-checklist.md` benoemen executionstatuswaarden en guardrails.
- `src/build_site_view_models.py` neemt executionstatus mee in evidence entries en update-claimlijsten.
- `src/build_quality_control.py` controleert dat alle claims een geldige executionstatus hebben en markeert uitvoeringsbesluitvragen, afhankelijkheden, capaciteit, sequencing, reviewtaken en algemene uitvoeringscontext als reviewpunt.
- `src/build_data_quality_audit.py` schrijft een `execution_status_audit` met statusverdeling, need-signalverdeling en verificatie-samples.

## Execution Status Values
- `operational_requirement`: bron noemt wat ingericht, voorbereid of georganiseerd moet worden.
- `implementation_activity`: bron beschrijft een zichtbare uitvoeringsactiviteit, project, programma of implementatie.
- `decision_question`: uitvoering vraagt een besluit, keuze of prioritering.
- `dependency`: uitvoering hangt af van een randvoorwaarde, aansluiting of andere actor.
- `sequencing_need`: bron geeft fasering, volgorde, stap of planning als uitvoeringssignaal.
- `capacity_need`: bron raakt capaciteit, fte, bemensing of uitvoeringskracht.
- `review_task`: bron vraagt review, monitoring, validatie, toetsing, leren of evaluatie.
- `execution_context`: bron is relevant voor uitvoering, maar noemt geen specifieke actie, afhankelijkheid of status.
- `not_execution`: geen zelfstandige uitvoeringsclaim.

## Verification
- Downstream regeneration from claims through site render completed.
- `python src/verify_claim_id_references.py` passed.
- `python -m pytest` passed.

## Carry Forward
Phase 27 is now complete for the six perspective splits. Later site-text sprints should use the status guardrails to keep possible follow-up actions, dependencies and review tasks separate from source-backed actions that are already underway or decided.
