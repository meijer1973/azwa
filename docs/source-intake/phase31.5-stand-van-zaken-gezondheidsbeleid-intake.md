# Sprint 31.5 - Stand van zaken Gezondheidsbeleid Intake

## Summary

Current sprint: Sprint 31.5 - Deep-research bronintake en top-layer verificatie.

The deep-research report in `docs/dr/Stable public source check for “Stand van zaken Gezondheidsbeleid (IZA en GALA)”.md` is an intake signal, not a corpus source. It found a stable public Documentwijzer landing URL for the Almere council item `Stand van zaken Gezondheidsbeleid (IZA en GALA)`.

This closes the narrow discovery question: a stable public landing page exists. It does not yet close the evidence question, because the underlying raadsbrief text or downloadable attachment has not been retrieved.

## Source Candidate

| Field | Value |
| --- | --- |
| Candidate ID | `mun_almere_stand_van_zaken_gezondheidsbeleid_iza_gala_2025` |
| Title | `Stand van zaken Gezondheidsbeleid (IZA en GALA)` |
| Landing URL | `https://documentwijzer.raadvanalmere.nl/app/instrument/item%2F1015051` |
| Publisher | Raad van Almere / Gemeente Almere |
| Candidate type | Raadsbrief / Documentwijzer item |
| Intake status | `pending_full_text` |

## Intake Decision

The candidate is recorded in `data/raw/source_intake_candidates.json` with status `pending_full_text`.

It is not added to `data/raw/manifest.json` yet. A local download of the landing URL on 2026-05-01 returned only the Raadzaam single-page application shell, not the raadsbrief body, PDF, attachment or stable extractable source text.

## Potential D6 Relevance

If the underlying full text is retrieved, this source may strengthen public context for:

- GGD Flevoland-coordinatie;
- JGZ Almere;
- Positief Gezond Almere / Zorgzaam Flevoland-interface;
- financiering en budgetafbakening;
- possibly Gezonde School / mentale gezonde school if the text contains school-prevention wording.

It should not currently be used as evidence for:

- formal D6 classification;
- ownership, coordination or mandate;
- component-level funding;
- digital and operational infrastructure;
- burgerinitiatieven / informele steun;
- settled status in the D6 responsibility register.

## Top-Layer Verification

Because no claim-ready source text was ingested, no pipeline top-layer claim is expected yet.

The top-layer update is instead limited to the intake and review layers:

- `data/raw/source_intake_candidates.json` records the stable landing URL as `pending_full_text`;
- `docs/review/almere_d6_open_questions.md` no longer says that no stable URL was found;
- `docs/review/almere_d6_deep_research_learnings.md` records that the named public-source gap narrowed but did not produce claim-ready evidence.

## Remaining Task

Retrieve the underlying raadsbrief full text, PDF or attachment from Documentwijzer/Raadzaam. Only then decide whether it belongs in the raw manifest and source corpus.
