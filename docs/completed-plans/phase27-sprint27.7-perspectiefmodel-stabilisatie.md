# Sprint 27.7 - Perspectiefmodel Stabilisatie

## Summary
Sprint 27.7 is afgerond op 29 april 2026. Deze sprint controleert en stabiliseert het Phase 27-claimmodel voordat Phase 28 publieke sitetekst op de zes statusvelden gaat baseren.

## Review Check
De reviewopmerking was grotendeels terecht:

- Sommige statuswaarden kwamen in de huidige corpusrun niet voor. Dat is nu expliciet zichtbaar in de audit als `zero_count_statuses`, in plaats van impliciet verborgen in schema/config.
- `fondsbeheerder` kwam niet voor als actor-signaal. De governance-audit toont dit nu als `zero_count_actor_signals`.
- Pipeline-metawoorden stonden in classifier-termlijsten. Die zijn verwijderd uit de claimstatus-classifiers.
- Wetten.nl actiechrome kwam in regelgevingclaims terecht. Raw-html blocks met actieknoppen worden nu gefilterd.
- `gemeente` werd via substringdetectie ook in `gemeenteraad` gevonden. Actorherkenning gebruikt nu woordgrenzen.

## What Changed
- `src/build_structural_extractions.py` filtert wetten.nl actieknoppen zoals `Toon relaties in LiDO`, `Maak een permanente link`, `Druk het regelingonderdeel af` en `Sla het regelingonderdeel op`.
- `src/build_claims_top5.py` verwijdert pipeline-meta strings uit money/governance/locality/execution termlijsten.
- `src/build_claims_top5.py` beperkt `EXECUTION_OPERATIONAL_REQUIREMENT_TERMS` tot actie- en inrichtingswerkwoorden; subjectnouns zoals `basisfunctionaliteiten`, `basisinfrastructuur`, `inloop`, `toegang`, `lokale teams` en `wijkteams` zijn geen zelfstandig operationeel signaal meer.
- `src/build_claims_top5.py` gebruikt woordgrenzen voor governance actor detection, zodat `gemeente` niet uit `gemeenteraad` wordt afgeleid.
- `config/data_quality_perspectives.json` documenteert waarom de statusvelden verschillende reviewflags gebruiken: `needs_attribution`, `needs_review` en `needs_verification`.
- `src/build_data_quality_audit.py` voegt `zero_count_statuses` toe aan alle status-audits en `zero_count_actor_signals` aan governance.

## Verification
- Downstream regeneration from structural extraction through site render completed.
- `python src/verify_claim_id_references.py` passed.
- `python -m pytest` passed.

## Carry Forward
Phase 28 may use the six statusfields for site text, but should read `zero_count_statuses` as a design-audit signal. A zero-count value is not automatically wrong, but it should be consciously kept, repaired, or removed in a later model cleanup sprint.
