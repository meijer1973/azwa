# Sprint 26.3 - Sentence-boundary en dedup

## Summary
Sprint 26.3 is afgerond op 28 april 2026. De claimlaag heeft nu een sentence-boundary gate, dedup-pass en claim-id verifier. Dit is repository-side kwaliteitswerk: er zijn geen D6-registerrijen inhoudelijk gehard en er is geen bestuurlijke interpretatie toegevoegd.

## What Changed
- `src/build_document_extractions.py` houdt afgebroken regels en semicolon-lijsten beter bij elkaar voordat zinskandidaten worden gemaakt.
- `src/build_claims_top5.py` weert lowercase mid-zin-starts en korte/headingachtige fragmenten zonder slotpunctuatie uit `claims_master.jsonl`.
- Langere claims zonder slotpunctuatie blijven bewaard maar worden review-only gelogd.
- Duplicate claimopeningen binnen dezelfde `(source_document_id, topic, subtopic)` groep worden geconsolideerd; de langste claim blijft behouden.
- `src/verify_claim_id_references.py` controleert of alle claim-id verwijzingen in `data/extracted` en `data/site` naar `claims_master.jsonl` resolven.
- `src/build_site_view_models.py` ruimt gegenereerde JSON-directories op voordat nieuwe viewmodels worden geschreven, zodat stale generated files geen dode claim-id verwijzingen achterlaten.

## Outputs
- `data/extracted/claims/sentence_validator_rejects.json`
- `data/extracted/claims/dedup_log.json`
- `src/verify_claim_id_references.py`
- Geregenereerde claim-, interpretatie-, site-, audit- en dashboardlagen.

## Before / After
Baseline na Sprint 26.2:

- Claims: 590.
- Rough claims: 159.
- Lowercase mid-zin-starts: 89.
- Missing terminal punctuation: 189.
- Duplicate first-200-char groups within document/topic/subtopic: 7 groups / 15 entries.

Na Sprint 26.3:

- Claims: 524.
- Rough claims: 119.
- Lowercase mid-zin-starts: 0.
- Missing terminal punctuation: 33.
- Duplicate first-200-char groups within document/topic/subtopic: 0.
- Sentence-boundary rejects: 84.
- Sentence-boundary review-only claims: 34.
- Dedup groups consolidated: 7.
- Superseded duplicate claims: 7.

## Verification
- Downstream regeneration from document extraction through site render completed.
- `python src/verify_claim_id_references.py` passed.
- QC summary after regeneration: 0 blocking, 6 warning, 74 review items.

## Carry Forward
The remaining rough claims are now concentrated in non-deterministic categories, especially English summary-like claims and longer extraction fragments that need perspective-specific treatment. The next logical sprint is Sprint 27.1 Norm, with D6 post-validation hardening still parked until policy-maker validation records or explicit decisions exist.
